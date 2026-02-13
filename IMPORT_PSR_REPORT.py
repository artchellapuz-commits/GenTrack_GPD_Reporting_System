"""
PSR Report Importer
Specialized script for importing PSR (Plant Status Report) Excel files
Handles the complex format with merged cells and multiple data columns
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

import openpyxl
from datetime import datetime, date
from decimal import Decimal
from django.db import transaction
from reports.models import Plant, PlantCapacity, HistoricalData


class PSRReportImporter:
    """Specialized importer for PSR Report format"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.imported_plants = 0
        self.imported_data = 0
    
    def import_file(self, file_path):
        """Import PSR report file"""
        print("=" * 70)
        print("PSR REPORT IMPORTER")
        print("=" * 70)
        print()
        print(f"📂 File: {os.path.basename(file_path)}")
        print()
        
        if not os.path.exists(file_path):
            print(f"❌ Error: File not found: {file_path}")
            return False
        
        try:
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            print(f"📊 Sheets found: {', '.join(workbook.sheetnames)}")
            print()
            
            # Process each sheet
            for sheet_name in workbook.sheetnames:
                print(f"Processing sheet: {sheet_name}")
                print("-" * 70)
                
                sheet = workbook[sheet_name]
                self._process_sheet(sheet, sheet_name)
                
                print()
            
            # Summary
            print("=" * 70)
            print("IMPORT SUMMARY")
            print("=" * 70)
            print(f"✓ Plants imported/updated: {self.imported_plants}")
            print(f"✓ Data records imported: {self.imported_data}")
            
            if self.warnings:
                print(f"⚠ Warnings: {len(self.warnings)}")
                for warning in self.warnings[:10]:
                    print(f"  - {warning}")
                if len(self.warnings) > 10:
                    print(f"  ... and {len(self.warnings) - 10} more")
            
            if self.errors:
                print(f"❌ Errors: {len(self.errors)}")
                for error in self.errors[:10]:
                    print(f"  - {error}")
                if len(self.errors) > 10:
                    print(f"  ... and {len(self.errors) - 10} more")
            
            print()
            print("=" * 70)
            
            return True
        
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _process_sheet(self, sheet, sheet_name):
        """Process a single sheet"""
        # Find where plant data starts
        data_start_row = self._find_data_start(sheet)
        
        if not data_start_row:
            self.warnings.append(f"Sheet '{sheet_name}': Could not find plant data")
            return
        
        print(f"  Data starts at row: {data_start_row}")
        
        # Extract report date
        report_date = self._extract_date(sheet)
        if report_date:
            print(f"  Report date: {report_date}")
        else:
            report_date = date.today()
            print(f"  Report date: {report_date} (using today)")
        
        # Find data columns
        data_columns = self._find_data_columns(sheet, data_start_row)
        print(f"  Data columns found: {len(data_columns)}")
        
        # Import plant data
        plants_in_sheet = 0
        data_in_sheet = 0
        
        with transaction.atomic():
            current_row = data_start_row
            
            while current_row <= sheet.max_row:
                try:
                    row = list(sheet[current_row])
                    
                    # Get plant code
                    if not row[0].value:
                        current_row += 1
                        continue
                    
                    plant_code = str(row[0].value).strip().upper()
                    
                    # Stop conditions
                    if (not plant_code or 
                        plant_code in ['TOTAL', 'SUBTOTAL', 'GRAND TOTAL', 'SUMMARY'] or
                        len(plant_code) > 15):
                        if plant_code in ['TOTAL', 'SUBTOTAL', 'GRAND TOTAL']:
                            break
                        current_row += 1
                        continue
                    
                    # Validate plant code pattern
                    if not self._is_valid_plant_code(plant_code):
                        current_row += 1
                        continue
                    
                    # Get or create plant
                    plant, created = Plant.objects.get_or_create(
                        code=plant_code,
                        defaults={'name': plant_code}
                    )
                    
                    if created:
                        plants_in_sheet += 1
                    
                    # Import data from columns
                    for col_idx, col_info in data_columns.items():
                        try:
                            value = row[col_idx].value
                            if value is not None:
                                generation = self._parse_decimal(value)
                                
                                if generation is not None and generation >= 0:
                                    # Determine what type of data this is
                                    data_type = col_info.get('type', 'generation')
                                    
                                    if data_type == 'generation':
                                        HistoricalData.objects.update_or_create(
                                            plant=plant,
                                            date=report_date,
                                            defaults={
                                                'actual_generation': generation,
                                                'remarks': f'Imported from PSR Report ({sheet_name})'
                                            }
                                        )
                                        data_in_sheet += 1
                                    elif data_type == 'capacity':
                                        # Update plant capacity
                                        PlantCapacity.objects.update_or_create(
                                            plant=plant,
                                            defaults={
                                                'dependable_capacity': generation,
                                                'installed_capacity': generation
                                            }
                                        )
                        
                        except Exception as e:
                            self.warnings.append(
                                f"Sheet '{sheet_name}', Row {current_row}, Col {col_idx}: {str(e)}"
                            )
                
                except Exception as e:
                    self.errors.append(f"Sheet '{sheet_name}', Row {current_row}: {str(e)}")
                
                current_row += 1
        
        self.imported_plants += plants_in_sheet
        self.imported_data += data_in_sheet
        
        print(f"  ✓ Imported {plants_in_sheet} plants, {data_in_sheet} data records")
    
    def _find_data_start(self, sheet):
        """Find the row where plant data starts"""
        for row_idx in range(1, 50):
            try:
                cell = sheet.cell(row_idx, 1)
                if cell.value:
                    text = str(cell.value).strip().upper()
                    
                    # Look for plant code pattern
                    if (len(text) <= 10 and 
                        any(c.isalpha() for c in text) and 
                        any(c.isdigit() for c in text) and
                        text not in ['PLANT', 'CODE', 'TOTAL', 'SUBTOTAL']):
                        return row_idx
            except:
                continue
        
        return None
    
    def _extract_date(self, sheet):
        """Extract report date from sheet"""
        # Check first 20 rows
        for row_idx in range(1, 21):
            for col_idx in range(1, 11):
                try:
                    cell = sheet.cell(row_idx, col_idx)
                    if cell.value:
                        # Check if it's a date object
                        if isinstance(cell.value, datetime):
                            return cell.value.date()
                        elif isinstance(cell.value, date):
                            return cell.value
                        
                        # Try to parse from string
                        text = str(cell.value).strip()
                        parsed_date = self._parse_date_text(text)
                        if parsed_date:
                            return parsed_date
                except:
                    continue
        
        return None
    
    def _parse_date_text(self, text):
        """Parse date from text"""
        import re
        
        # Try date patterns
        patterns = [
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    parts = [int(x) for x in match.groups()]
                    if len(parts) == 3:
                        # Try different date formats
                        for year, month, day in [
                            (parts[2], parts[0], parts[1]),  # MM/DD/YYYY
                            (parts[2], parts[1], parts[0]),  # DD/MM/YYYY
                            (parts[0], parts[1], parts[2]),  # YYYY-MM-DD
                        ]:
                            try:
                                if 1 <= month <= 12 and 1 <= day <= 31:
                                    return date(year, month, day)
                            except:
                                continue
                except:
                    pass
        
        # Look for month names
        months = {
            'JANUARY': 1, 'JAN': 1, 'FEBRUARY': 2, 'FEB': 2,
            'MARCH': 3, 'MAR': 3, 'APRIL': 4, 'APR': 4,
            'MAY': 5, 'JUNE': 6, 'JUN': 6, 'JULY': 7, 'JUL': 7,
            'AUGUST': 8, 'AUG': 8, 'SEPTEMBER': 9, 'SEP': 9,
            'OCTOBER': 10, 'OCT': 10, 'NOVEMBER': 11, 'NOV': 11,
            'DECEMBER': 12, 'DEC': 12
        }
        
        text_upper = text.upper()
        for month_name, month_num in months.items():
            if month_name in text_upper:
                year_match = re.search(r'\b(19|20)\d{2}\b', text)
                if year_match:
                    year = int(year_match.group())
                    day_match = re.search(r'\b(\d{1,2})\b', text)
                    day = int(day_match.group()) if day_match else 1
                    
                    try:
                        return date(year, month_num, day)
                    except:
                        pass
        
        return None
    
    def _find_data_columns(self, sheet, start_row):
        """Find columns containing numeric data"""
        data_columns = {}
        
        # Check the data start row for numeric values
        row = list(sheet[start_row])
        
        for col_idx in range(1, min(len(row), 30)):
            cell_value = row[col_idx].value
            
            if cell_value is not None and isinstance(cell_value, (int, float)):
                # This column has numeric data
                data_columns[col_idx] = {
                    'type': 'generation',
                    'index': col_idx
                }
        
        return data_columns
    
    def _is_valid_plant_code(self, code):
        """Check if string looks like a valid plant code"""
        if not code or len(code) > 15:
            return False
        
        # Must have at least one letter and one digit
        has_letter = any(c.isalpha() for c in code)
        has_digit = any(c.isdigit() for c in code)
        
        return has_letter and has_digit
    
    def _parse_decimal(self, value):
        """Parse value as Decimal"""
        if value is None or value == '':
            return None
        
        try:
            if isinstance(value, (int, float)):
                return Decimal(str(value))
            
            str_value = str(value).strip().replace(',', '')
            if not str_value or str_value == '-':
                return None
            
            return Decimal(str_value)
        except:
            return None


def main():
    """Main function"""
    print()
    
    # Default file
    default_file = r"REPORTS\8. PSR\PSR REPORT-8AM.xlsx"
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = default_file
        print("No file specified, using default PSR report...")
        print()
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print()
        print("Usage:")
        print(f"  python {sys.argv[0]} <path_to_psr_report.xlsx>")
        print()
        print("Example:")
        print(f'  python {sys.argv[0]} "REPORTS\\8. PSR\\PSR REPORT-8AM.xlsx"')
        return
    
    importer = PSRReportImporter()
    success = importer.import_file(file_path)
    
    if success:
        print("✅ Import completed successfully!")
    else:
        print("❌ Import failed!")
    
    print()


if __name__ == "__main__":
    main()
