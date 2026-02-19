from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings
import os
from ..models import GenerationReport, Plant
from ..models_scheduled import ScheduledReport, ReportExecution
from .excel_exporter import ExcelExporter
import logging

logger = logging.getLogger(__name__)


class AutomatedReportService:
    """Service for generating and sending automated reports"""
    
    def __init__(self):
        self.excel_exporter = ExcelExporter()
    
    def get_due_reports(self):
        """Get all reports that are due to run"""
        now = timezone.now()
        return ScheduledReport.objects.filter(
            status='ACTIVE',
            next_run__lte=now
        )
    
    def execute_report(self, scheduled_report):
        """Execute a scheduled report"""
        execution = ReportExecution.objects.create(
            scheduled_report=scheduled_report,
            status='RUNNING'
        )
        
        try:
            # Generate report data
            data = self._generate_report_data(scheduled_report)
            
            # Create report file
            file_path = self._create_report_file(scheduled_report, data)
            
            # Send to recipients
            sent, failed = self._send_report(scheduled_report, file_path)
            
            # Update execution
            execution.status = 'COMPLETED'
            execution.completed_at = timezone.now()
            execution.duration_seconds = (execution.completed_at - execution.started_at).seconds
            execution.file_path = file_path
            execution.file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            execution.records_processed = len(data)
            execution.recipients_sent = sent
            execution.recipients_failed = failed
            execution.save()
            
            # Update scheduled report
            scheduled_report.last_run = timezone.now()
            scheduled_report.next_run = self._calculate_next_run(scheduled_report)
            scheduled_report.run_count += 1
            scheduled_report.save()
            
            logger.info(f"Report executed successfully: {scheduled_report.name}")
            return True
            
        except Exception as e:
            execution.status = 'FAILED'
            execution.completed_at = timezone.now()
            execution.error_message = str(e)
            execution.save()
            
            logger.error(f"Report execution failed: {scheduled_report.name} - {str(e)}")
            return False
    
    def _generate_report_data(self, scheduled_report):
        """Generate report data based on type"""
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=scheduled_report.date_range_days)
        
        # Get plants
        plants = scheduled_report.plants.all()
        if not plants.exists():
            plants = Plant.objects.filter(is_active=True)
        
        # Query based on report type
        if scheduled_report.report_type == 'GENERATION_SUMMARY':
            return self._get_generation_summary(plants, start_date, end_date)
        elif scheduled_report.report_type == 'CAPACITY_FACTOR':
            return self._get_capacity_factor_data(plants, start_date, end_date)
        elif scheduled_report.report_type == 'AVAILABILITY':
            return self._get_availability_data(plants, start_date, end_date)
        elif scheduled_report.report_type == 'PERFORMANCE_METRICS':
            return self._get_performance_metrics(plants, start_date, end_date)
        else:
            return []
    
    def _get_generation_summary(self, plants, start_date, end_date):
        """Get generation summary data"""
        reports = GenerationReport.objects.filter(
            plant__in=plants,
            report_date__range=[start_date, end_date]
        ).select_related('plant', 'unit').order_by('report_date', 'plant', 'unit')
        
        return [{
            'date': r.report_date,
            'plant': r.plant.name,
            'unit': r.unit.unit_number,
            'generation_kwh': float(r.generation_kwh),
            'operating_hours': float(r.operating_hours),
            'capacity_factor': float(r.capacity_factor or 0),
            'availability_factor': float(r.availability_factor or 0)
        } for r in reports]
    
    def _get_capacity_factor_data(self, plants, start_date, end_date):
        """Get capacity factor analysis"""
        from django.db.models import Avg, Sum
        
        data = []
        for plant in plants:
            stats = GenerationReport.objects.filter(
                plant=plant,
                report_date__range=[start_date, end_date]
            ).aggregate(
                avg_capacity_factor=Avg('capacity_factor'),
                total_generation=Sum('generation_kwh'),
                avg_operating_hours=Avg('operating_hours')
            )
            
            data.append({
                'plant': plant.name,
                'avg_capacity_factor': float(stats['avg_capacity_factor'] or 0),
                'total_generation_mwh': float(stats['total_generation'] or 0) / 1000,
                'avg_operating_hours': float(stats['avg_operating_hours'] or 0)
            })
        
        return data
    
    def _get_availability_data(self, plants, start_date, end_date):
        """Get availability data"""
        from django.db.models import Avg, Sum
        
        data = []
        for plant in plants:
            stats = GenerationReport.objects.filter(
                plant=plant,
                report_date__range=[start_date, end_date]
            ).aggregate(
                avg_availability=Avg('availability_factor'),
                total_forced_outage=Sum('forced_outage_hours'),
                total_scheduled_outage=Sum('scheduled_outage_hours')
            )
            
            data.append({
                'plant': plant.name,
                'avg_availability': float(stats['avg_availability'] or 0),
                'total_forced_outage_hours': float(stats['total_forced_outage'] or 0),
                'total_scheduled_outage_hours': float(stats['total_scheduled_outage'] or 0)
            })
        
        return data
    
    def _get_performance_metrics(self, plants, start_date, end_date):
        """Get comprehensive performance metrics"""
        from django.db.models import Avg, Sum, Count
        
        data = []
        for plant in plants:
            stats = GenerationReport.objects.filter(
                plant=plant,
                report_date__range=[start_date, end_date]
            ).aggregate(
                avg_capacity_factor=Avg('capacity_factor'),
                avg_availability=Avg('availability_factor'),
                total_generation=Sum('generation_kwh'),
                total_operating_hours=Sum('operating_hours'),
                report_count=Count('id')
            )
            
            data.append({
                'plant': plant.name,
                'capacity_mw': float(plant.capacity_mw),
                'avg_capacity_factor': float(stats['avg_capacity_factor'] or 0),
                'avg_availability': float(stats['avg_availability'] or 0),
                'total_generation_mwh': float(stats['total_generation'] or 0) / 1000,
                'total_operating_hours': float(stats['total_operating_hours'] or 0),
                'days_reported': stats['report_count']
            })
        
        return data
    
    def _create_report_file(self, scheduled_report, data):
        """Create report file (Excel or PDF)"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{scheduled_report.report_type}_{timestamp}"
        
        # Create exports directory if not exists
        export_dir = os.path.join(settings.MEDIA_ROOT, 'automated_reports')
        os.makedirs(export_dir, exist_ok=True)
        
        if scheduled_report.format in ['EXCEL', 'BOTH']:
            file_path = os.path.join(export_dir, f"{filename}.xlsx")
            self._create_excel_report(file_path, scheduled_report, data)
            return file_path
        
        # For now, default to Excel
        file_path = os.path.join(export_dir, f"{filename}.xlsx")
        self._create_excel_report(file_path, scheduled_report, data)
        return file_path
    
    def _create_excel_report(self, file_path, scheduled_report, data):
        """Create Excel report file"""
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        
        wb = Workbook()
        ws = wb.active
        ws.title = scheduled_report.report_type[:31]
        
        # Header
        ws['A1'] = scheduled_report.name
        ws['A1'].font = Font(size=16, bold=True)
        ws['A2'] = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Data headers
        if data:
            headers = list(data[0].keys())
            for col, header in enumerate(headers, 1):
                cell = ws.cell(row=4, column=col, value=header.replace('_', ' ').title())
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
                cell.font = Font(color='FFFFFF', bold=True)
            
            # Data rows
            for row_idx, item in enumerate(data, 5):
                for col_idx, header in enumerate(headers, 1):
                    ws.cell(row=row_idx, column=col_idx, value=item[header])
        
        wb.save(file_path)
    
    def _send_report(self, scheduled_report, file_path):
        """Send report to recipients"""
        recipients = list(scheduled_report.recipients.values_list('email', flat=True))
        
        # Add additional emails
        if scheduled_report.additional_emails:
            additional = [e.strip() for e in scheduled_report.additional_emails.split('\n') if e.strip()]
            recipients.extend(additional)
        
        if not recipients:
            return 0, 0
        
        subject = f"Automated Report: {scheduled_report.name}"
        body = f"""
        Dear Recipient,
        
        Please find attached the automated report: {scheduled_report.name}
        
        Report Type: {scheduled_report.get_report_type_display()}
        Frequency: {scheduled_report.get_frequency_display()}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        This is an automated message from NPC Reporting System.
        """
        
        try:
            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients
            )
            
            if os.path.exists(file_path):
                email.attach_file(file_path)
            
            email.send()
            return len(recipients), 0
            
        except Exception as e:
            logger.error(f"Failed to send report: {str(e)}")
            return 0, len(recipients)
    
    def _calculate_next_run(self, scheduled_report):
        """Calculate next run time"""
        now = timezone.now()
        schedule_time = scheduled_report.schedule_time
        
        if scheduled_report.frequency == 'DAILY':
            next_run = now.replace(hour=schedule_time.hour, minute=schedule_time.minute, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
        
        elif scheduled_report.frequency == 'WEEKLY':
            next_run = now.replace(hour=schedule_time.hour, minute=schedule_time.minute, second=0, microsecond=0)
            days_ahead = (scheduled_report.schedule_day - now.weekday()) % 7
            if days_ahead == 0 and next_run <= now:
                days_ahead = 7
            next_run += timedelta(days=days_ahead)
        
        elif scheduled_report.frequency == 'MONTHLY':
            next_run = now.replace(day=scheduled_report.schedule_day, hour=schedule_time.hour, 
                                  minute=schedule_time.minute, second=0, microsecond=0)
            if next_run <= now:
                # Move to next month
                if now.month == 12:
                    next_run = next_run.replace(year=now.year + 1, month=1)
                else:
                    next_run = next_run.replace(month=now.month + 1)
        
        else:  # QUARTERLY
            next_run = now.replace(hour=schedule_time.hour, minute=schedule_time.minute, second=0, microsecond=0)
            next_run += timedelta(days=90)
        
        return next_run
