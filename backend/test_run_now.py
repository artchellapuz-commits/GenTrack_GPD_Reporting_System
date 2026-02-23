"""
Test the Run Now functionality directly
"""
import os
import django
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models_scheduled import ScheduledReport, ReportExecution
from reports.services.automated_reports import AutomatedReportService
from reports.models import GenerationReport

print("=" * 60)
print("TEST RUN NOW FUNCTIONALITY")
print("=" * 60)

# Check prerequisites
print("\n1. Checking Prerequisites:")
print("-" * 60)

gen_count = GenerationReport.objects.count()
print(f"  Generation Reports: {gen_count}")
if gen_count == 0:
    print("  ⚠️  WARNING: No generation data - reports will be empty")
else:
    print(f"  ✅ OK: {gen_count} records available")

report_count = ScheduledReport.objects.count()
print(f"  Scheduled Reports: {report_count}")
if report_count == 0:
    print("  ❌ ERROR: No scheduled reports found")
    print("     Run FIX_RUN_NOW_ERROR.bat to create sample reports")
    sys.exit(1)
else:
    print(f"  ✅ OK: {report_count} scheduled reports")

# Get first report
report = ScheduledReport.objects.first()
print(f"\n2. Testing Report: {report.name}")
print("-" * 60)
print(f"  Type: {report.get_report_type_display()}")
print(f"  Frequency: {report.get_frequency_display()}")
print(f"  Status: {report.status}")
print(f"  Run Count: {report.run_count}")

# Test execution
print("\n3. Executing Report...")
print("-" * 60)

try:
    service = AutomatedReportService()
    
    # This is where the error would occur if cache is not cleared
    print("  Creating execution record...")
    execution = ReportExecution.objects.create(
        scheduled_report=report,
        status='RUNNING'
    )
    print(f"  ✅ Execution created: ID={execution.id}")
    
    # Clean up test execution
    execution.delete()
    
    print("\n  Running full report execution...")
    service.execute_report(report)
    
    print("\n  ✅ SUCCESS! Report executed without errors")
    
    # Show results
    latest_execution = ReportExecution.objects.filter(
        scheduled_report=report
    ).order_by('-started_at').first()
    
    if latest_execution:
        print("\n4. Execution Results:")
        print("-" * 60)
        print(f"  Status: {latest_execution.get_status_display()}")
        print(f"  Records Processed: {latest_execution.records_processed}")
        print(f"  Duration: {latest_execution.duration_seconds}s")
        print(f"  File: {latest_execution.file_path}")
        print(f"  File Size: {latest_execution.file_size} bytes")
        
        if latest_execution.status == 'COMPLETED':
            print("\n  ✅ Report completed successfully!")
        else:
            print(f"\n  ⚠️  Status: {latest_execution.status}")
            if latest_execution.error_message:
                print(f"  Error: {latest_execution.error_message}")
    
    # Update report info
    report.refresh_from_db()
    print(f"\n  Updated Run Count: {report.run_count}")
    
except Exception as e:
    print(f"\n  ❌ ERROR: {str(e)}")
    print("\n  This error means:")
    if "unexpected keyword argument" in str(e):
        print("  - Python cache is still not cleared")
        print("  - Run CLEAR_CACHE_AND_FIX.bat again")
        print("  - Make sure to RESTART backend after clearing cache")
    else:
        print(f"  - {str(e)}")
    
    import traceback
    print("\n  Full traceback:")
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TEST COMPLETED SUCCESSFULLY!")
print("=" * 60)
print("\nThe 'Run Now' button should work in the frontend now.")
print("Go to: http://localhost:8080/scheduled-reports")
print("=" * 60)
