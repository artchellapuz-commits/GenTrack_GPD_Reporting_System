from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import FileResponse
from django.db.models import Sum, Avg, Q
from datetime import datetime
import hashlib
import os
import tempfile

from .models import Plant, Unit, UploadedFile, GenerationReport, PlantCapacity, HistoricalData, WaterNomination, ActualGeneration, Testimonial, AuditLog
from .serializers import (
    PlantSerializer, UnitSerializer, UploadedFileSerializer,
    GenerationReportSerializer, GenerationReportListSerializer,
    ExcelUploadSerializer, ReportGenerationSerializer,
    PlantCapacitySerializer, HistoricalDataSerializer, HistoricalDataUploadSerializer,
    WaterNominationSerializer, ActualGenerationSerializer, NominationVarianceSerializer,
    TestimonialSerializer, AuditLogSerializer
)
from .pagination import CustomPageNumberPagination
from .services.excel_importer import ExcelImporter
from .services.psr_exporter import PSRExporter
from .services.historical_data_importer import HistoricalDataImporter
from .services.template_generator import TemplateGenerator
from .services.daily_status_exporter import generate_daily_status_report
from .utils import get_location_from_ip, get_client_ip


class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plant.objects.filter(is_active=True)
    serializer_class = PlantSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for internal system
    pagination_class = None  # Disable pagination for plants


class UnitViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Unit.objects.filter(is_active=True).select_related('plant')
    serializer_class = UnitSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for internal system
    
    def get_queryset(self):
        queryset = super().get_queryset()
        plant_code = self.request.query_params.get('plant_code')
        if plant_code:
            queryset = queryset.filter(plant__code=plant_code)
        return queryset


class UploadedFileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UploadedFile.objects.all().select_related('plant', 'uploaded_by')
    serializer_class = UploadedFileSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access for internal system
    
    @action(detail=False, methods=['get'], url_path='download-template/daily-generation')
    def download_daily_generation_template(self, request):
        """Download Daily Generation Report template"""
        wb = TemplateGenerator.generate_daily_generation_template()
        return TemplateGenerator.create_http_response(wb, 'Daily_Generation_Template.xlsx')
    
    @action(detail=False, methods=['get'], url_path='download-template/water-nomination')
    def download_water_nomination_template(self, request):
        """Download Water Nomination template"""
        wb = TemplateGenerator.generate_water_nomination_template()
        return TemplateGenerator.create_http_response(wb, 'Water_Nomination_Template.xlsx')
    
    @action(detail=False, methods=['get'], url_path='download-template/historical-data')
    def download_historical_data_template(self, request):
        """Download Historical Data Import template"""
        wb = TemplateGenerator.generate_historical_data_template()
        return TemplateGenerator.create_http_response(wb, 'Historical_Data_Template.xlsx')
    
    @action(detail=False, methods=['get'], url_path='download-template/plant-capacity')
    def download_plant_capacity_template(self, request):
        """Download Plant Capacity template"""
        wb = TemplateGenerator.generate_plant_capacity_template()
        return TemplateGenerator.create_http_response(wb, 'Plant_Capacity_Template.xlsx')
    
    @action(detail=False, methods=['get'], url_path='download-template/plant-status')
    def download_plant_status_template(self, request):
        """Download Plant Status template"""
        wb = TemplateGenerator.generate_plant_status_template()
        return TemplateGenerator.create_http_response(wb, 'Plant_Status_Template.xlsx')
    
    @action(detail=False, methods=['get'], url_path='download-template/psr')
    def download_psr_template(self, request):
        """Download PSR (Plant Status Report) template with right side section"""
        wb = TemplateGenerator.generate_psr_template()
        return TemplateGenerator.create_http_response(wb, 'PSR_Template.xlsx')
    
    @action(detail=True, methods=['delete'])
    def delete_upload(self, request, pk=None):
        """Delete an uploaded file and all its associated generation reports"""
        try:
            uploaded_file = self.get_object()
            
            # Delete associated generation reports first
            deleted_reports = GenerationReport.objects.filter(uploaded_file=uploaded_file).delete()
            
            # Delete the uploaded file record and physical file
            file_path = uploaded_file.file.path if uploaded_file.file else None
            uploaded_file.delete()
            
            # Try to delete physical file
            if file_path:
                try:
                    import os
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not delete physical file: {e}")
            
            return Response({
                'message': 'File and associated records deleted successfully',
                'reports_deleted': deleted_reports[0] if deleted_reports else 0
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = ExcelUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        file = serializer.validated_data['file']
        plant_code = serializer.validated_data['plant_code']
        
        try:
            plant = Plant.objects.get(code=plant_code)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate checksum
        file.seek(0)
        checksum = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)
        
        # Check for duplicate
        if UploadedFile.objects.filter(checksum=checksum, plant=plant).exists():
            return Response({'error': 'This file has already been uploaded'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Create uploaded file record
        uploaded_file = UploadedFile.objects.create(
            file=file,
            original_filename=file.name,
            plant=plant,
            uploaded_by=request.user if request.user.is_authenticated else None,
            file_size=file.size,
            checksum=checksum,
            status='PROCESSING'
        )
        
        # Process the file
        try:
            importer = ExcelImporter(uploaded_file)
            records_imported = importer.process()
            
            uploaded_file.status = 'COMPLETED'
            uploaded_file.records_imported = records_imported
            uploaded_file.save()
            
            return Response({
                'message': 'File uploaded and processed successfully',
                'records_imported': records_imported,
                'file_id': uploaded_file.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            uploaded_file.status = 'FAILED'
            uploaded_file.error_message = str(e)
            uploaded_file.save()
            
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GenerationReportViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):
    queryset = GenerationReport.objects.all().select_related('plant', 'unit', 'uploaded_file')
    permission_classes = [AllowAny]  # Allow unauthenticated access for internal system
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GenerationReportListSerializer
        return GenerationReportSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by plant - handle both plant_code and plant_code[] formats
        plant_codes = self.request.query_params.getlist('plant_code[]') or self.request.query_params.getlist('plant_code')
        print(f"DEBUG: plant_codes from getlist = {plant_codes}")
        print(f"DEBUG: query_params = {dict(self.request.query_params)}")
        
        if plant_codes:
            queryset = queryset.filter(plant__code__in=plant_codes)
            print(f"DEBUG: Filtered queryset count = {queryset.count()}")
        else:
            print(f"DEBUG: NO plant_codes filter, returning all {queryset.count()} records")
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(report_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(report_date__lte=end_date)
        
        # Filter by unit
        unit_id = self.request.query_params.get('unit_id')
        if unit_id:
            queryset = queryset.filter(unit_id=unit_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get aggregated summary statistics"""
        queryset = self.get_queryset()
        
        summary = queryset.aggregate(
            total_generation=Sum('generation_kwh'),
            avg_capacity_factor=Avg('capacity_factor'),
            avg_availability_factor=Avg('availability_factor'),
            total_operating_hours=Sum('operating_hours'),
            total_forced_outage_hours=Sum('forced_outage_hours')
        )
        
        return Response(summary)
    
    @action(detail=False, methods=['post'], url_path='generate-report')
    def generate_report(self, request):
        """Generate Excel report based on filters"""
        serializer = ReportGenerationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        report_type = data.get('report_type', 'psr')
        
        # Get filtered data
        reports = GenerationReport.objects.filter(
            plant__code__in=data['plant_codes'],
            report_date__gte=data['start_date'],
            report_date__lte=data['end_date']
        ).select_related('plant', 'unit').order_by('report_date', 'plant', 'unit')
        
        if not reports.exists():
            return Response({'error': 'No data found for the specified criteria'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        # Generate Excel file
        try:
            report_date = data['start_date']
            
            if report_type == 'daily_status':
                # Generate Daily Status Report
                filename = f"DAILY_PLANT_STATUS_{report_date.strftime('%Y%m%d')}.xlsx"
                file_path = generate_daily_status_report(report_date, filename)
                report_name = "Daily Status Report"
            else:
                # Generate PSR report (default)
                exporter = PSRExporter(reports, report_date)
                file_path = exporter.generate()
                filename = f"PLANT_STATUS_{report_date.strftime('%Y%m%d')}.xlsx"
                report_name = "PSR Report"
            
            # Create audit log for report generation
            try:
                plant_names = ', '.join([code for code in data['plant_codes']])
                ip_address = get_client_ip(request)
                location = get_location_from_ip(ip_address)
                
                AuditLog.objects.create(
                    user=request.user,
                    action='EXPORT',
                    model_name='GenerationReport',
                    description=f'Generated {report_name} for plants: {plant_names}, Date: {report_date.strftime("%Y-%m-%d")}',
                    ip_address=ip_address,
                    location=location
                )
            except Exception as audit_error:
                # Log the error but don't fail the report generation
                print(f"Audit log error: {audit_error}")
            
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoricalDataViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for historical data"""
    queryset = HistoricalData.objects.all().select_related('plant')
    serializer_class = HistoricalDataSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by plant
        plant_codes = self.request.query_params.getlist('plant_code[]') or self.request.query_params.getlist('plant_code')
        if plant_codes:
            queryset = queryset.filter(plant__code__in=plant_codes)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['post'], url_path='import')
    def import_historical(self, request):
        """Import historical data from Excel files"""
        serializer = HistoricalDataUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        capacity_file = serializer.validated_data.get('capacity_file')
        historical_file = serializer.validated_data.get('historical_file')
        
        try:
            importer = HistoricalDataImporter()
            results = {}
            
            # Save files temporarily
            temp_files = []
            
            if capacity_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    for chunk in capacity_file.chunks():
                        tmp.write(chunk)
                    capacity_path = tmp.name
                    temp_files.append(capacity_path)
                
                results['capacity'] = importer.import_plant_capacity(capacity_path)
            
            if historical_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                    for chunk in historical_file.chunks():
                        tmp.write(chunk)
                    historical_path = tmp.name
                    temp_files.append(historical_path)
                
                results['historical'] = importer.import_historical_data(historical_path)
            
            # Clean up temp files
            for temp_file in temp_files:
                try:
                    os.unlink(temp_file)
                except:
                    pass
            
            # Calculate totals
            total_imported = sum(r.get('imported', 0) for r in results.values())
            all_errors = []
            all_warnings = []
            
            for key, result in results.items():
                all_errors.extend(result.get('errors', []))
                all_warnings.extend(result.get('warnings', []))
            
            return Response({
                'success': all(r.get('success', False) for r in results.values()),
                'total_imported': total_imported,
                'errors': all_errors,
                'warnings': all_warnings,
                'details': results
            }, status=status.HTTP_201_CREATED if total_imported > 0 else status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlantCapacityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for plant capacity records"""
    queryset = PlantCapacity.objects.all().select_related('plant')
    serializer_class = PlantCapacitySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by plant
        plant_codes = self.request.query_params.getlist('plant_code[]') or self.request.query_params.getlist('plant_code')
        if plant_codes:
            queryset = queryset.filter(plant__code__in=plant_codes)
        
        # Filter by date
        effective_date = self.request.query_params.get('effective_date')
        if effective_date:
            queryset = queryset.filter(effective_date=effective_date)
        
        return queryset


class WaterNominationViewSet(viewsets.ModelViewSet):
    """ViewSet for water nominations"""
    queryset = WaterNomination.objects.all().select_related('plant', 'submitted_by', 'approved_by')
    serializer_class = WaterNominationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by plant
        plant_codes = self.request.query_params.getlist('plant_code[]') or self.request.query_params.getlist('plant_code')
        if plant_codes:
            queryset = queryset.filter(plant__code__in=plant_codes)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(nomination_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(nomination_date__lte=end_date)
        
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by nomination type
        nomination_type = self.request.query_params.get('nomination_type')
        if nomination_type:
            queryset = queryset.filter(nomination_type=nomination_type)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user if self.request.user.is_authenticated else None)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a nomination for approval"""
        nomination = self.get_object()
        
        if nomination.status != 'DRAFT':
            return Response({'error': 'Only draft nominations can be submitted'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        nomination.status = 'SUBMITTED'
        nomination.submitted_at = datetime.now()
        nomination.submitted_by = request.user if request.user.is_authenticated else None
        nomination.save()
        
        return Response({'message': 'Nomination submitted successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a submitted nomination"""
        nomination = self.get_object()
        
        if nomination.status != 'SUBMITTED':
            return Response({'error': 'Only submitted nominations can be approved'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        nomination.status = 'APPROVED'
        nomination.approved_at = datetime.now()
        nomination.approved_by = request.user if request.user.is_authenticated else None
        nomination.save()
        
        return Response({'message': 'Nomination approved successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a submitted nomination"""
        nomination = self.get_object()
        
        if nomination.status != 'SUBMITTED':
            return Response({'error': 'Only submitted nominations can be rejected'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        remarks = request.data.get('remarks', '')
        nomination.status = 'REJECTED'
        nomination.remarks = remarks
        nomination.save()
        
        return Response({'message': 'Nomination rejected'}, status=status.HTTP_200_OK)


class ActualGenerationViewSet(viewsets.ModelViewSet):
    """ViewSet for actual generation data"""
    queryset = ActualGeneration.objects.all().select_related('plant')
    serializer_class = ActualGenerationSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by plant
        plant_codes = self.request.query_params.getlist('plant_code[]') or self.request.query_params.getlist('plant_code')
        if plant_codes:
            queryset = queryset.filter(plant__code__in=plant_codes)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(generation_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(generation_date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def variance_analysis(self, request):
        """Compare nominations with actual generation"""
        plant_code = request.query_params.get('plant_code')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not all([plant_code, start_date, end_date]):
            return Response({'error': 'plant_code, start_date, and end_date are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            plant = Plant.objects.get(code=plant_code)
        except Plant.DoesNotExist:
            return Response({'error': 'Plant not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get nominations and actuals
        nominations = WaterNomination.objects.filter(
            plant=plant,
            nomination_date__gte=start_date,
            nomination_date__lte=end_date,
            status='APPROVED'
        )
        
        actuals = ActualGeneration.objects.filter(
            plant=plant,
            generation_date__gte=start_date,
            generation_date__lte=end_date
        )
        
        # Build comparison data
        results = []
        for nomination in nominations:
            try:
                actual = actuals.get(generation_date=nomination.nomination_date)
                
                # Calculate variance
                variance_mwh = float(actual.total_actual_mwh) - float(nomination.total_nominated_mwh)
                variance_percent = (variance_mwh / float(nomination.total_nominated_mwh) * 100) if nomination.total_nominated_mwh > 0 else 0
                
                # Hourly comparison
                hourly_comparison = []
                for i in range(24):
                    hour_field = f'hour_{str(i).zfill(2)}'
                    nominated = float(getattr(nomination, hour_field, 0) or 0)
                    actual_val = float(getattr(actual, hour_field, 0) or 0)
                    hourly_comparison.append({
                        'hour': i,
                        'time': f"{str(i).zfill(2)}:00-{str(i+1).zfill(2)}:00",
                        'nominated_mw': nominated,
                        'actual_mw': actual_val,
                        'variance_mw': actual_val - nominated,
                        'variance_percent': ((actual_val - nominated) / nominated * 100) if nominated > 0 else 0
                    })
                
                results.append({
                    'date': nomination.nomination_date,
                    'plant_code': plant.code,
                    'plant_name': plant.name,
                    'nomination_type': nomination.nomination_type,
                    'total_nominated_mwh': nomination.total_nominated_mwh,
                    'total_actual_mwh': actual.total_actual_mwh,
                    'variance_mwh': variance_mwh,
                    'variance_percent': round(variance_percent, 2),
                    'hourly_comparison': hourly_comparison
                })
            except ActualGeneration.DoesNotExist:
                # No actual data for this nomination
                pass
        
        return Response(results, status=status.HTTP_200_OK)


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    API endpoint for testimonials
    - GET: Public access to view active testimonials
    - POST: Authenticated users can submit testimonials (pending approval)
    """
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]  # Allow public read and authenticated write
    
    def get_queryset(self):
        # Only show active testimonials for list/retrieve
        if self.action in ['list', 'retrieve']:
            return Testimonial.objects.filter(is_active=True).order_by('order', '-created_at')
        # For admin actions, show all
        return Testimonial.objects.all()
    
    def perform_create(self, serializer):
        # New testimonials default to inactive (pending admin approval)
        serializer.save(
            submitted_by=self.request.user if self.request.user.is_authenticated else None,
            is_active=False
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for audit logs
    - GET: List all audit logs with filtering
    - Requires authentication
    """
    queryset = AuditLog.objects.all().select_related('user')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by action type
        action = self.request.query_params.get('action')
        if action:
            queryset = queryset.filter(action=action)
        
        # Filter by username
        username = self.request.query_params.get('username')
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        
        end_date = self.request.query_params.get('end_date')
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset.order_by('-timestamp')
    
    @action(detail=False, methods=['get'], url_path='export')
    def export_logs(self, request):
        """Export audit logs to Excel"""
        queryset = self.get_queryset()
        
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Audit Logs"
        
        # Headers
        headers = ['Timestamp', 'User', 'Action', 'Model', 'Description', 'IP Address', 'Location']
        ws.append(headers)
        
        # Style headers
        header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col_num, _ in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Data rows
        for log in queryset:
            ws.append([
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                log.user.username if log.user else 'System',
                log.action,
                log.model_name,
                log.description,
                log.ip_address or 'N/A',
                log.location or 'Unknown'
            ])
        
        # Auto-size columns
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
        
        # Create response
        import io
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        from django.http import HttpResponse
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="Audit_Logs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        
        return response
