"""
Excel Template Generator Service
Generates downloadable Excel templates for data import
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta
from django.http import HttpResponse
import io


class TemplateGenerator:
    """Generate Excel templates for data import"""
    
    # Color scheme
    HEADER_FILL = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    SAMPLE_FILL = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
    INSTRUCTION_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
    INSTRUCTION_FONT = Font(italic=True, size=10)
    
    THIN_BORDER = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    @staticmethod
    def _style_header_row(ws, row_num, columns):
        """Apply styling to header row"""
        for col_num, _ in enumerate(columns, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.fill = TemplateGenerator.HEADER_FILL
            cell.font = TemplateGenerator.HEADER_FONT
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = TemplateGenerator.THIN_BORDER
    
    @staticmethod
    def _style_sample_row(ws, row_num, num_columns):
        """Apply styling to sample data row"""
        for col_num in range(1, num_columns + 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.fill = TemplateGenerator.SAMPLE_FILL
            cell.border = TemplateGenerator.THIN_BORDER
    
    @staticmethod
    def _auto_size_columns(ws):
        """Auto-size columns based on content"""
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    @staticmethod
    def generate_daily_generation_template():
        """Generate Daily Generation Report template"""
        wb = Workbook()
        
        # Data sheet
        ws_data = wb.active
        ws_data.title = "Daily Generation Data"
        
        # Headers
        headers = [
            'Date (YYYY-MM-DD)',
            'Unit Number',
            'Generation (kWh)',
            'Operating Hours',
            'Capacity Factor (%)',
            'Availability Factor (%)',
            'Forced Outage Hours',
            'Scheduled Outage Hours',
            'Remarks'
        ]
        
        ws_data.append(headers)
        TemplateGenerator._style_header_row(ws_data, 1, headers)
        
        # Sample data
        today = datetime.now()
        sample_data = [
            today.strftime('%Y-%m-%d'),
            '1',
            '50000',
            '24',
            '85.5',
            '95.0',
            '0',
            '0',
            'Normal operation'
        ]
        ws_data.append(sample_data)
        TemplateGenerator._style_sample_row(ws_data, 2, len(headers))
        
        # Add a few empty rows for data entry
        for i in range(5):
            ws_data.append([''] * len(headers))
        
        TemplateGenerator._auto_size_columns(ws_data)
        
        # Instructions sheet
        ws_inst = wb.create_sheet("Instructions")
        instructions = [
            ["Daily Generation Report Template - Instructions"],
            [""],
            ["Column Descriptions:"],
            ["Date", "Format: YYYY-MM-DD (e.g., 2026-02-19)"],
            ["Unit Number", "Enter the unit number (1, 2, 3, etc.)"],
            ["Generation (kWh)", "Total energy generated in kilowatt-hours"],
            ["Operating Hours", "Number of hours the unit operated (0-24)"],
            ["Capacity Factor (%)", "Percentage of maximum possible generation (0-100)"],
            ["Availability Factor (%)", "Percentage of time unit was available (0-100)"],
            ["Forced Outage Hours", "Hours of unplanned outages"],
            ["Scheduled Outage Hours", "Hours of planned maintenance"],
            ["Remarks", "Any additional notes or comments"],
            [""],
            ["Important Notes:"],
            ["• All fields are required except Remarks"],
            ["• Date must be in YYYY-MM-DD format"],
            ["• Numeric values should not contain commas or currency symbols"],
            ["• Percentages should be entered as numbers (e.g., 85.5 not 85.5%)"],
            ["• Operating Hours cannot exceed 24"],
            ["• Delete the sample data row before uploading"],
            [""],
            ["For support, contact your system administrator."]
        ]
        
        for row in instructions:
            ws_inst.append(row)
        
        # Style instructions
        ws_inst['A1'].font = Font(bold=True, size=14)
        ws_inst['A3'].font = Font(bold=True, size=12)
        ws_inst['A14'].font = Font(bold=True, size=12)
        
        TemplateGenerator._auto_size_columns(ws_inst)
        
        return wb
    
    @staticmethod
    def generate_water_nomination_template():
        """Generate Water Nomination template"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Water Nomination"
        
        # Headers
        headers = ['Hour'] + [f'Hour {i:02d}' for i in range(24)]
        ws.append(['Date:', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        ws.append(['Plant:', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        ws.append(['Nomination Type:', 'DAY_AHEAD or REAL_TIME', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        ws.append([])
        
        # Hourly data headers
        hourly_headers = ['Hour', 'Nominated MW']
        ws.append(hourly_headers)
        TemplateGenerator._style_header_row(ws, 5, hourly_headers)
        
        # Sample hourly data
        for hour in range(24):
            ws.append([f'{hour:02d}:00', '50.0'])
        
        TemplateGenerator._auto_size_columns(ws)
        
        # Instructions sheet
        ws_inst = wb.create_sheet("Instructions")
        instructions = [
            ["Water Nomination Template - Instructions"],
            [""],
            ["How to Fill:"],
            ["1. Enter the date in YYYY-MM-DD format in cell B1"],
            ["2. Enter the plant code in cell B2 (e.g., AGUS1, AGUS2)"],
            ["3. Enter nomination type in cell B3 (DAY_AHEAD or REAL_TIME)"],
            ["4. Fill in the nominated MW for each hour (00:00 to 23:00)"],
            [""],
            ["Important Notes:"],
            ["• All 24 hours must have values"],
            ["• MW values should be realistic for your plant capacity"],
            ["• Use decimal points for fractional MW (e.g., 50.5)"],
            ["• Do not leave any hour blank"],
            [""],
            ["For support, contact your system administrator."]
        ]
        
        for row in instructions:
            ws_inst.append(row)
        
        ws_inst['A1'].font = Font(bold=True, size=14)
        TemplateGenerator._auto_size_columns(ws_inst)
        
        return wb
    
    @staticmethod
    def generate_historical_data_template():
        """Generate Historical Data Import template"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Historical Data"
        
        headers = [
            'Date (YYYY-MM-DD)',
            'Plant Code',
            'Generation (MWh)',
            'Capacity Factor (%)',
            'Availability Factor (%)',
            'Operating Hours',
            'Peak Load (MW)',
            'Average Load (MW)',
            'Remarks'
        ]
        
        ws.append(headers)
        TemplateGenerator._style_header_row(ws, 1, headers)
        
        # Sample data for last 7 days
        today = datetime.now()
        for i in range(7):
            date = today - timedelta(days=i)
            sample = [
                date.strftime('%Y-%m-%d'),
                'AGUS1',
                '1200',
                '85.5',
                '95.0',
                '24',
                '55.0',
                '50.0',
                'Normal operation'
            ]
            ws.append(sample)
            if i == 0:
                TemplateGenerator._style_sample_row(ws, 2, len(headers))
        
        TemplateGenerator._auto_size_columns(ws)
        
        # Instructions sheet
        ws_inst = wb.create_sheet("Instructions")
        instructions = [
            ["Historical Data Import Template - Instructions"],
            [""],
            ["Column Descriptions:"],
            ["Date", "Format: YYYY-MM-DD"],
            ["Plant Code", "Use official plant codes (AGUS1, AGUS2, etc.)"],
            ["Generation (MWh)", "Total daily generation in megawatt-hours"],
            ["Capacity Factor (%)", "Daily capacity factor percentage"],
            ["Availability Factor (%)", "Daily availability percentage"],
            ["Operating Hours", "Total operating hours for the day"],
            ["Peak Load (MW)", "Maximum load during the day"],
            ["Average Load (MW)", "Average load for the day"],
            ["Remarks", "Optional notes"],
            [""],
            ["Important Notes:"],
            ["• You can import multiple days at once"],
            ["• Dates should be in chronological order"],
            ["• All numeric fields are required"],
            ["• First row with gray background is sample data - delete before upload"],
            [""],
            ["For support, contact your system administrator."]
        ]
        
        for row in instructions:
            ws_inst.append(row)
        
        ws_inst['A1'].font = Font(bold=True, size=14)
        TemplateGenerator._auto_size_columns(ws_inst)
        
        return wb
    
    @staticmethod
    def generate_plant_capacity_template():
        """Generate Plant Capacity template"""
        wb = Workbook()
        ws = wb.active
        ws.title = "Plant Capacity"
        
        headers = [
            'Plant Code',
            'Plant Name',
            'Installed Capacity (MW)',
            'Dependable Capacity (MW)',
            'Number of Units',
            'Effective Date (YYYY-MM-DD)',
            'Remarks'
        ]
        
        ws.append(headers)
        TemplateGenerator._style_header_row(ws, 1, headers)
        
        # Sample data
        samples = [
            ['AGUS1', 'Agus 1 Hydroelectric Power Plant', '50.0', '48.0', '1', datetime.now().strftime('%Y-%m-%d'), 'Active'],
            ['AGUS2', 'Agus 2 Hydroelectric Power Plant', '100.0', '95.0', '2', datetime.now().strftime('%Y-%m-%d'), 'Active'],
        ]
        
        for sample in samples:
            ws.append(sample)
        
        TemplateGenerator._style_sample_row(ws, 2, len(headers))
        TemplateGenerator._auto_size_columns(ws)
        
        # Instructions sheet
        ws_inst = wb.create_sheet("Instructions")
        instructions = [
            ["Plant Capacity Template - Instructions"],
            [""],
            ["Column Descriptions:"],
            ["Plant Code", "Unique plant identifier (e.g., AGUS1)"],
            ["Plant Name", "Full name of the power plant"],
            ["Installed Capacity (MW)", "Total installed capacity"],
            ["Dependable Capacity (MW)", "Reliable capacity under normal conditions"],
            ["Number of Units", "Total number of generating units"],
            ["Effective Date", "Date when this capacity became effective (YYYY-MM-DD)"],
            ["Remarks", "Additional notes"],
            [""],
            ["Important Notes:"],
            ["• Plant Code must be unique"],
            ["• Capacities should be in MW (megawatts)"],
            ["• Delete sample data rows before uploading"],
            [""],
            ["For support, contact your system administrator."]
        ]
        
        for row in instructions:
            ws_inst.append(row)
        
        ws_inst['A1'].font = Font(bold=True, size=14)
        TemplateGenerator._auto_size_columns(ws_inst)
        
        return wb
    
    @staticmethod
    def create_http_response(workbook, filename):
        """Create HTTP response with Excel file"""
        output = io.BytesIO()
        workbook.save(output)
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
