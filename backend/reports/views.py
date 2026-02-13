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

from .models import Plant, Unit, UploadedFile, GenerationReport, PlantCapacity, HistoricalData
from .serializers import (
    PlantSerializer, UnitSerializer, UploadedFileSerializer,
    GenerationReportSerializer, GenerationReportListSerializer,
    ExcelUploadSerializer, ReportGenerationSerializer,
    PlantCapacitySerializer, HistoricalDataSerializer, HistoricalDataUploadSerializer
)
from .services.excel_importer import ExcelImporter
from .services.excel_exporter import ExcelExporter
from .services.historical_data_importer import HistoricalDataImporter


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
            exporter = ExcelExporter(reports, data['report_type'])
            file_path = exporter.generate()
            
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            filename = f"NPC_Report_{data['report_type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
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
