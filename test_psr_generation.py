"""
Test PSR Report Generation
Quick test to verify PSR exporter works correctly
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from datetime import date
from reports.models import GenerationReport
from reports.services.psr_exporter import PSRExporter

def test_psr_generation():
    """Test PSR report generation"""
    
    print("=" * 70)
    print("PSR REPORT GENERATION TEST")
    print("=" * 70)
    print()
    
    # Get any available data
    print("🔍 Looking for generation data...")
    reports = GenerationReport.objects.all().select_related('plant', 'unit').order_by('-report_date', 'plant__code', 'unit__unit_number')
    
    if not reports.exists():
        print("❌ No generation data found in database")
        print()
        print("To test PSR generation:")
        print("1. Upload Excel files with generation data")
        print("2. Or run: python backend/add_initial_data.py")
        return
    
    # Use the most recent date
    report_date = reports.first().report_date
    reports = reports.filter(report_date=report_date)
    print(f"✓ Found data for: {report_date.strftime('%A, %B %d, %Y')}")
    print()
    
    print(f"📊 Found {reports.count()} generation records")
    print()
    
    # Show data summary
    print("Data Summary:")
    print("-" * 70)
    plants_data = {}
    for report in reports:
        plant_code = report.plant.code
        if plant_code not in plants_data:
            plants_data[plant_code] = {
                'name': report.plant.name,
                'units': 0,
                'total_gen': 0
            }
        plants_data[plant_code]['units'] += 1
        plants_data[plant_code]['total_gen'] += float(report.generation_kwh)
    
    for plant_code, data in sorted(plants_data.items()):
        print(f"  {plant_code:10s} - {data['name']:20s} - {data['units']} units - {data['total_gen']:8.2f} MW")
    
    print()
    print("=" * 70)
    print("GENERATING PSR REPORT...")
    print("=" * 70)
    print()
    
    try:
        # Generate PSR report
        exporter = PSRExporter(reports, report_date)
        file_path = exporter.generate()
        
        print("✅ PSR Report Generated Successfully!")
        print()
        print(f"📁 File Location: {file_path}")
        print(f"📏 File Size: {os.path.getsize(file_path):,} bytes")
        print()
        
        # Check if file exists and is readable
        if os.path.exists(file_path):
            print("✓ File exists and is accessible")
            
            # Try to open with openpyxl to verify it's valid
            try:
                import openpyxl
                wb = openpyxl.load_workbook(file_path)
                ws = wb.active
                print(f"✓ Excel file is valid")
                print(f"✓ Sheet name: {ws.title}")
                print(f"✓ Dimensions: {ws.dimensions}")
                print()
                
                # Show first few rows
                print("Preview (first 10 rows):")
                print("-" * 70)
                for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=10), start=1):
                    row_data = []
                    for cell in row[:5]:  # First 5 columns
                        if cell.value:
                            value = str(cell.value)
                            if len(value) > 20:
                                value = value[:17] + "..."
                            row_data.append(value)
                        else:
                            row_data.append("")
                    if any(row_data):
                        print(f"Row {row_idx:2d}: {' | '.join(row_data)}")
                
                wb.close()
                
            except Exception as e:
                print(f"⚠️  Warning: Could not verify Excel file: {e}")
        else:
            print("❌ File was not created")
        
        print()
        print("=" * 70)
        print("TEST COMPLETE")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("1. Open the generated file in Excel")
        print("2. Verify the format matches the template")
        print("3. Check that all data is correctly populated")
        print("4. Test from frontend: Generate Report > Select PSR type")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_psr_generation()
