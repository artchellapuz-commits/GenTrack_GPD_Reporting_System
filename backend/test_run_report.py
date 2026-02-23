"""
Test script to verify Run Now functionality
Run this to test if report generation works
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models_scheduled import ScheduledReport
from reports.services.automated_reports import AutomatedReportService

def test_run_report():
    """Test running a scheduled report"""
    print("=" * 60)
    print("Testing Automated Report Execution")
    print("=" * 60)
    
    # Get first active report
    report = ScheduledReport.objects.filter(status='ACTIVE').first()
    
    if not report:
        print("❌ No active reports found!")
        print("\nCreating a test report...")
        from django.contrib.auth.models import User
        user = User.objects.first()
        
        report = ScheduledReport.objects.create(
            name="Test Report",
            report_type="GENERATION_SUMMARY",
            frequency="DAILY",
            schedule_time="08:00",
            format="EXCEL",
            date_range_days=30,
            status="ACTIVE",
            created_by=user
        )
        print(f"✅ Created test report: {report.name}")
    
    print(f"\n📊 Running report: {report.name}")
    print(f"   Type: {report.get_report_type_display()}")
    print(f"   Format: {report.format}")
    print(f"   Date Range: {report.date_range_days} days")
    
    try:
        service = AutomatedReportService()
        service.execute_report(report)
        
        print("\n✅ SUCCESS! Report executed successfully!")
        print(f"\n📁 Check for generated file in:")
        print(f"   backend/media/automated_reports/")
        
        # Show execution details
        execution = report.executions.latest('started_at')
        print(f"\n📋 Execution Details:")
        print(f"   Status: {execution.status}")
        print(f"   Records: {execution.records_processed}")
        print(f"   Duration: {execution.duration_seconds}s")
        print(f"   File: {execution.file_path}")
        
        if execution.error_message:
            print(f"   Error: {execution.error_message}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nCommon issues:")
        print("1. No generation data in database")
        print("2. Missing Python packages (openpyxl)")
        print("3. File permission issues")
        
        import traceback
        print("\nFull error:")
        traceback.print_exc()

if __name__ == '__main__':
    test_run_report()
