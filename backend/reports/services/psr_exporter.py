"""
Plant Status Report (PSR) Excel Exporter
Generates Excel reports matching 100% the exact PSR format from PSR REPORT-8AM.xlsx
INCLUDING: Forecasted Load, IPP sections, Charts, and Notes
"""

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.chart import PieChart, BarChart, Reference
    from openpyxl.chart.label import DataLabelList
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

from datetime import datetime
import os
from django.conf import settings


class PSRExporter:
    """Service class for generating Plant Status Report (PSR) Excel files"""
    
    # Plant configuration matching the template EXACTLY
    PLANTS_CONFIG = {
        'AGUS1': {
            'name': 'AGUS 1',
            'units': [
                {'num': 1, 'label': 'unit 1', 'capacity': 40, 'nominated': 0},
                {'num': 2, 'label': 'unit 2', 'capacity': 40, 'nominated': 0}
            ]
        },
        'AGUS2': {
            'name': 'AGUS 2',
            'units': [
                {'num': 1, 'label': 'unit  1', 'capacity': 60, 'nominated': 60},
                {'num': 2, 'label': 'unit  2', 'capacity': 60, 'nominated': 60},
                {'num': 3, 'label': 'unit  3', 'capacity': 60, 'nominated': 60}
            ]
        },
        'AGUS4': {
            'name': 'AGUS 4',
            'units': [
                {'num': 1, 'label': 'unit  1', 'capacity': 52.7, 'nominated': 0},
                {'num': 2, 'label': 'unit  2', 'capacity': 52.7, 'nominated': 52.7},
                {'num': 3, 'label': 'unit  3', 'capacity': 52.7, 'nominated': 52.7}
            ]
        },
        'AGUS5': {
            'name': 'AGUS 5',
            'units': [
                {'num': 1, 'label': 'unit 1', 'capacity': 27.5, 'nominated': 27.5},
                {'num': 2, 'label': 'unit 2', 'capacity': 27.5, 'nominated': 27.5}
            ]
        },
        'AGUS6': {
            'name': 'AGUS 6',
            'units': [
                {'num': 1, 'label': '  unit  1', 'capacity': 34.5, 'nominated': 20},
                {'num': 2, 'label': '  unit  2', 'capacity': 34.5, 'nominated': 21},
                {'num': 3, 'label': 'unit  3', 'capacity': 50, 'nominated': 42},
                {'num': 4, 'label': 'unit  4', 'capacity': 50, 'nominated': 38},
                {'num': 5, 'label': 'unit  5', 'capacity': 50, 'nominated': 44}
            ]
        },
        'AGUS7': {
            'name': 'AGUS 7',
            'units': [
                {'num': 1, 'label': 'unit 1', 'capacity': 27, 'nominated': 27},
                {'num': 2, 'label': 'unit 2', 'capacity': 27, 'nominated': 27}
            ]
        },
        'PULANGI4': {
            'name': 'PULANGI IV',
            'units': [
                {'num': 1, 'label': 'unit  1', 'capacity': 85, 'nominated': 75},
                {'num': 2, 'label': 'unit  2', 'capacity': 85, 'nominated': 70},
                {'num': 3, 'label': 'unit  3', 'capacity': 85, 'nominated': 70}
            ]
        }
    }
    
    def __init__(self, queryset, report_date):
        if not EXCEL_AVAILABLE:
            raise ImportError("openpyxl is required for Excel export")
        
        self.queryset = queryset
        self.report_date = report_date
        self.data_by_plant = self._organize_data()
    
    def _organize_data(self):
        """Organize queryset data by plant and unit"""
        data = {}
        for report in self.queryset:
            plant_code = report.plant.code.upper()
            unit_num = report.unit.unit_number
            
            if plant_code not in data:
                data[plant_code] = {}
            
            data[plant_code][unit_num] = {
                'generation': float(report.generation_kwh),
                'operating_hours': float(report.operating_hours),
                'forced_outage': float(report.forced_outage_hours),
                'scheduled_outage': float(report.scheduled_outage_hours),
                'remarks': report.remarks or ''
            }
        
        return data
    
    def generate(self):
        """Generate PSR Excel file matching 100% the exact format"""
        wb = Workbook()
        ws = wb.active
        ws.title = "PSR PSALM Edit (2)"
        
        # Set column widths EXACTLY as template
        ws.column_dimensions['A'].width = 25.86
        ws.column_dimensions['B'].width = 15.14
        ws.column_dimensions['C'].width = 13.71
        ws.column_dimensions['D'].width = 15.71
        ws.column_dimensions['E'].width = 13.71
        ws.column_dimensions['F'].width = 13.57
        ws.column_dimensions['G'].width = 13.29
        ws.column_dimensions['H'].width = 14.71
        ws.column_dimensions['I'].width = 13.0
        ws.column_dimensions['J'].width = 13.0
        ws.column_dimensions['K'].width = 13.0
        ws.column_dimensions['L'].width = 13.0
        ws.column_dimensions['M'].width = 15.71
        ws.column_dimensions['N'].width = 14.71
        
        # Add all sections
        self._add_header(ws)
        self._add_column_headers(ws)
        current_row = self._add_plant_data(ws)
        current_row = self._add_forecasted_load(ws, current_row)
        current_row = self._add_ipp_section(ws, current_row)
        current_row = self._add_notes_section(ws, current_row)
        self._add_footer(ws, current_row)
        
        # Save file
        file_path = self._get_file_path()
        wb.save(file_path)
        return file_path
    
    def _add_header(self, ws):
        """Add header section EXACTLY as template (rows 1-12)"""
        # Row 1: Empty with specific formatting
        ws['A1'] = ' '
        ws['A1'].font = Font(size=20, bold=True)
        ws['A1'].alignment = Alignment(horizontal='center')
        ws.row_dimensions[1].height = 29.45
        
        # Row 2: MINDANAO GENERATION
        ws['A2'] = 'MINDANAO GENERATION'
        ws['A2'].font = Font(size=20, bold=True)
        ws['A2'].alignment = Alignment(horizontal='center')
        ws.merge_cells('A2:N2')
        ws.row_dimensions[2].height = 25.5
        
        # Row 3: (PSALM PORTFOLIO)
        ws['A3'] = '(PSALM PORTFOLIO)'
        ws['A3'].font = Font(size=14, bold=True)
        ws['A3'].alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells('A3:N3')
        ws.row_dimensions[3].height = 14.25
        
        # Row 4-5: Empty
        ws.row_dimensions[4].height = 15.95
        ws.row_dimensions[5].height = 8.25
        
        # Row 6: FOR section
        ws['A6'] = 'FOR     :'
        ws['A6'].font = Font(size=14, bold=True)
        ws['A6'].alignment = Alignment(horizontal='right')
        
        ws['B6'] = 'MR. LARRY I. SABELLINA'
        ws['B6'].font = Font(size=14, bold=True)
        
        ws['G6'] = 'MR. DENNIS EDWARD A. DELA SERNA'
        ws['G6'].font = Font(size=14, bold=True)
        
        ws['K6'] = 'MR. ARNOLD C. FRANCISCO'
        ws['K6'].font = Font(size=14, bold=True)
        
        ws.row_dimensions[6].height = 15.95
        
        # Row 7: Titles
        ws['B7'] = 'VP, Mindanao Generation'
        ws['B7'].font = Font(size=12)
        
        ws['G7'] = 'President and CEO, PSALM'
        ws['G7'].font = Font(size=12)
        
        ws['K7'] = 'VP - PAMG, PSALM'
        ws['K7'].font = Font(size=12)
        ws['K7'].alignment = Alignment(horizontal='left')
        
        ws.row_dimensions[7].height = 15.95
        
        # Row 8: Empty
        ws.row_dimensions[8].height = 8.25
        
        # Row 9: PLANT STATUS REPORT
        ws['A9'] = ' PLANT STATUS REPORT'
        ws['A9'].font = Font(size=18, bold=True, italic=True)
        ws['A9'].alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells('A9:N9')
        ws.row_dimensions[9].height = 24.95
        
        # Row 10: Date
        date_str = self.report_date.strftime('%A, %d %B %Y')
        ws['A10'] = f'as of 0800H {date_str}'
        ws['A10'].font = Font(size=14, bold=True)
        ws['A10'].alignment = Alignment(horizontal='center', vertical='center')
        ws.merge_cells('A10:N10')
        ws.row_dimensions[10].height = 22.5
        
        # Row 11: Empty
        ws.row_dimensions[11].height = 7.5
        
        # Row 12: Separator
        ws['A12'] = ' '
        ws['A12'].font = Font(size=9, bold=True)
        ws['A12'].alignment = Alignment(horizontal='left')
        ws.row_dimensions[12].height = 3.75
    
    def _add_column_headers(self, ws):
        """Add column headers EXACTLY as template (rows 13-16)"""
        # Row 13-16: Headers with exact formatting
        ws['A13'] = 'PLANT NAME'
        ws['A13'].font = Font(size=14, bold=True)
        ws['A13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('A13:A16')
        
        ws['B13'] = 'Rated Capacity (MW)'
        ws['B13'].font = Font(size=12, bold=True)
        ws['B13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('B13:B16')
        
        ws['C13'] = 'Nominated'
        ws['C13'].font = Font(size=12, bold=True)
        ws['C13'].alignment = Alignment(horizontal='center')
        
        ws['C16'] = 'Capability'
        ws['C16'].font = Font(size=12, bold=True)
        ws['C16'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws['D13'] = 'Available Capacity (MW)'
        ws['D13'].font = Font(size=12, bold=True)
        ws['D13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('D13:D16')
        
        ws['F13'] = 'Lake Lanao Projected Ave. Outflow'
        ws['F13'].font = Font(size=12, bold=True)
        ws['F13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('F13:F16')
        
        ws['G13'] = 'Load at 0800H '
        ws['G13'].font = Font(size=12, bold=True)
        ws['G13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('G13:G16')
        
        ws['H13'] = 'REMARKS'
        ws['H13'].font = Font(size=14, bold=True)
        ws['H13'].alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.merge_cells('H13:N16')
        
        # Set row heights
        ws.row_dimensions[13].height = 15.75
        ws.row_dimensions[14].height = 15.75
        ws.row_dimensions[15].height = 7.5
        ws.row_dimensions[16].height = 15.75
    
    def _add_plant_data(self, ws):
        """Add plant data starting from row 17 EXACTLY as template"""
        current_row = 17
        
        # Process each plant in order
        for plant_code in ['AGUS1', 'AGUS2', 'AGUS4', 'AGUS5', 'AGUS6', 'AGUS7']:
            current_row = self._add_plant_section(ws, plant_code, current_row)
        
        # Add TOTAL AGUS row
        ws[f'A{current_row}'] = ' TOTAL AGUS'
        ws[f'A{current_row}'].font = Font(size=14, bold=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'A{current_row}'].fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        ws.row_dimensions[current_row].height = 23.45
        current_row += 1
        
        # Add PULANGI IV
        current_row = self._add_plant_section(ws, 'PULANGI4', current_row)
        
        # Add TOTAL HYDRO row
        ws[f'A{current_row}'] = 'TOTAL HYDRO'
        ws[f'A{current_row}'].font = Font(size=14, bold=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'A{current_row}'].fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        ws.row_dimensions[current_row].height = 23.45
        current_row += 1
        
        return current_row
    
    def _add_plant_section(self, ws, plant_code, start_row):
        """Add a plant section with all its units EXACTLY as template"""
        if plant_code not in self.PLANTS_CONFIG:
            return start_row
        
        config = self.PLANTS_CONFIG[plant_code]
        plant_data = self.data_by_plant.get(plant_code, {})
        
        # Plant header row
        ws[f'A{start_row}'] = config['name']
        ws[f'A{start_row}'].font = Font(size=14, bold=True, italic=True)
        ws[f'A{start_row}'].alignment = Alignment(vertical='center')
        
        # Calculate totals
        total_capacity = sum(u['capacity'] for u in config['units'])
        total_nominated = sum(u['nominated'] for u in config['units'])
        total_available = 0
        total_load = 0
        
        for unit in config['units']:
            if unit['num'] in plant_data:
                unit_data = plant_data[unit['num']]
                total_load += unit_data['generation']
                total_available += unit['capacity']
        
        ws[f'B{start_row}'] = total_capacity
        ws[f'B{start_row}'].font = Font(size=14, bold=True)
        ws[f'B{start_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'C{start_row}'] = total_nominated
        ws[f'C{start_row}'].font = Font(size=14, bold=True)
        ws[f'C{start_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'D{start_row}'] = total_available
        ws[f'D{start_row}'].font = Font(size=14, bold=True)
        ws[f'D{start_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'E{start_row}'] = 0
        ws[f'E{start_row}'].font = Font(size=12, bold=True)
        ws[f'E{start_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'G{start_row}'] = total_load
        ws[f'G{start_row}'].font = Font(size=14, bold=True)
        ws[f'G{start_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        # Add remarks for plant
        if plant_code.startswith('AGUS'):
            remarks = 'Lake Lanao Elevation is 701.50 m.a.s.l.'
        elif plant_code == 'PULANGI4':
            remarks = 'Reservoir Elevation is 290.00 m.a.s.l.'
        else:
            remarks = ''
        
        ws[f'H{start_row}'] = remarks
        ws[f'H{start_row}'].font = Font(size=12, bold=True)
        ws[f'H{start_row}'].alignment = Alignment(horizontal='left', vertical='center')
        
        ws.row_dimensions[start_row].height = 23.45
        current_row = start_row + 1
        
        # Add unit rows
        for unit in config['units']:
            ws[f'A{current_row}'] = unit['label']
            ws[f'A{current_row}'].font = Font(size=12)
            ws[f'A{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
            
            ws[f'B{current_row}'] = unit['capacity']
            ws[f'B{current_row}'].font = Font(size=12)
            ws[f'B{current_row}'].alignment = Alignment(horizontal='right', vertical='center')
            
            ws[f'C{current_row}'] = unit['nominated']
            ws[f'C{current_row}'].font = Font(size=12)
            ws[f'C{current_row}'].alignment = Alignment(horizontal='right', vertical='center')
            
            if unit['num'] in plant_data:
                unit_data = plant_data[unit['num']]
                
                ws[f'D{current_row}'] = unit['capacity']
                ws[f'D{current_row}'].font = Font(size=12)
                ws[f'D{current_row}'].alignment = Alignment(horizontal='right', vertical='center')
                
                ws[f'G{current_row}'] = unit_data['generation']
                ws[f'G{current_row}'].font = Font(size=12)
                ws[f'G{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
                
                # Add remarks
                unit_remarks = self._get_unit_remarks(unit_data)
                ws[f'H{current_row}'] = unit_remarks
                ws[f'H{current_row}'].font = Font(size=12)
                ws[f'H{current_row}'].alignment = Alignment(vertical='center', wrap_text=True)
            else:
                ws[f'D{current_row}'] = 0
                ws[f'D{current_row}'].font = Font(size=12)
                ws[f'D{current_row}'].alignment = Alignment(horizontal='right', vertical='center')
                
                ws[f'G{current_row}'] = 0
                ws[f'G{current_row}'].font = Font(size=12)
                ws[f'G{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
                
                ws[f'H{current_row}'] = 'No data'
                ws[f'H{current_row}'].font = Font(size=12)
                ws[f'H{current_row}'].alignment = Alignment(vertical='center', wrap_text=True)
            
            ws.row_dimensions[current_row].height = 21.75
            current_row += 1
        
        return current_row
    
    def _get_unit_remarks(self, unit_data):
        """Generate remarks for a unit based on its data"""
        remarks = []
        
        if unit_data['forced_outage'] > 0:
            remarks.append(f"Forced outage: {unit_data['forced_outage']:.1f}h")
        
        if unit_data['scheduled_outage'] > 0:
            remarks.append(f"Scheduled outage: {unit_data['scheduled_outage']:.1f}h")
        
        if unit_data['remarks']:
            remarks.append(unit_data['remarks'])
        
        if not remarks:
            if unit_data['generation'] > 0:
                return 'OPERATIONAL'
            else:
                return 'STANDBY'
        
        return '. '.join(remarks)
    
    def _add_forecasted_load(self, ws, current_row):
        """Add Agus-Pulangi Forecasted Load section (yellow highlighted row) EXACTLY as template"""
        # Calculate forecasted loads (example values - can be made dynamic)
        agus_forecast = 500.8
        pulangi_forecast = 150.0
        total_forecast = agus_forecast + pulangi_forecast
        
        # Forecasted load row with yellow background - EXACTLY as template
        date_str = self.report_date.strftime('%b %d, %Y')
        forecast_text = f'Agus-Pulangi Forecasted Load @ 6pm, {date_str} : Agus = {agus_forecast} MW & Pulangui IV = {pulangi_forecast} MW, Total Load: {total_forecast} MW'
        
        ws[f'A{current_row}'] = forecast_text
        ws[f'A{current_row}'].font = Font(size=11, bold=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='center', wrap_text=False)
        ws[f'A{current_row}'].fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        ws.merge_cells(f'A{current_row}:N{current_row}')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        return current_row
    
    def _add_ipp_section(self, ws, current_row):
        """Add IPP (Independent Power Producer) section EXACTLY as template"""
        # MCFPP (STEAG), unit 1
        ws[f'A{current_row}'] = 'MCFPP (STEAG), unit 1'
        ws[f'A{current_row}'].font = Font(size=11)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        
        ws[f'B{current_row}'] = 116.0
        ws[f'B{current_row}'].font = Font(size=11)
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'C{current_row}'] = 105.0
        ws[f'C{current_row}'].font = Font(size=11)
        ws[f'C{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'D{current_row}'] = 105.00
        ws[f'D{current_row}'].font = Font(size=11)
        ws[f'D{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'D{current_row}'].number_format = '0.00'
        
        ws[f'E{current_row}'] = 61.50
        ws[f'E{current_row}'].font = Font(size=11)
        ws[f'E{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'E{current_row}'].number_format = '0.00'
        
        ws[f'H{current_row}'] = 'Normal Operation'
        ws[f'H{current_row}'].font = Font(size=11)
        ws[f'H{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # MCFPP (STEAG), unit 2
        ws[f'A{current_row}'] = 'MCFPP (STEAG), unit 2'
        ws[f'A{current_row}'].font = Font(size=11)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        
        ws[f'B{current_row}'] = 116.0
        ws[f'B{current_row}'].font = Font(size=11)
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'C{current_row}'] = 105.0
        ws[f'C{current_row}'].font = Font(size=11)
        ws[f'C{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        
        ws[f'D{current_row}'] = 105.00
        ws[f'D{current_row}'].font = Font(size=11)
        ws[f'D{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'D{current_row}'].number_format = '0.00'
        
        ws[f'E{current_row}'] = 62.60
        ws[f'E{current_row}'].font = Font(size=11)
        ws[f'E{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'E{current_row}'].number_format = '0.00'
        
        ws[f'H{current_row}'] = 'Normal Operation'
        ws[f'H{current_row}'].font = Font(size=11)
        ws[f'H{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # TOTAL IPP
        ws[f'A{current_row}'] = 'TOTAL IPP'
        ws[f'A{current_row}'].font = Font(size=11, bold=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        ws[f'A{current_row}'].fill = PatternFill(start_color='CCECFF', end_color='CCECFF', fill_type='solid')
        
        ws[f'B{current_row}'] = 232.00
        ws[f'B{current_row}'].font = Font(size=11, bold=True)
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'B{current_row}'].fill = PatternFill(start_color='CCECFF', end_color='CCECFF', fill_type='solid')
        ws[f'B{current_row}'].number_format = '0.00'
        
        ws[f'C{current_row}'] = 210.00
        ws[f'C{current_row}'].font = Font(size=11, bold=True)
        ws[f'C{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'C{current_row}'].fill = PatternFill(start_color='CCECFF', end_color='CCECFF', fill_type='solid')
        ws[f'C{current_row}'].number_format = '0.00'
        
        ws[f'D{current_row}'] = 210.00
        ws[f'D{current_row}'].font = Font(size=11, bold=True)
        ws[f'D{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'D{current_row}'].fill = PatternFill(start_color='CCECFF', end_color='CCECFF', fill_type='solid')
        ws[f'D{current_row}'].number_format = '0.00'
        
        ws[f'E{current_row}'] = 124.10
        ws[f'E{current_row}'].font = Font(size=11, bold=True)
        ws[f'E{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'E{current_row}'].fill = PatternFill(start_color='CCECFF', end_color='CCECFF', fill_type='solid')
        ws[f'E{current_row}'].number_format = '0.00'
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # TOTAL NPC-PSALM
        ws[f'A{current_row}'] = 'TOTAL NPC-PSALM'
        ws[f'A{current_row}'].font = Font(size=11, bold=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='center')
        ws[f'A{current_row}'].fill = PatternFill(start_color='99CCFF', end_color='99CCFF', fill_type='solid')
        
        ws[f'B{current_row}'] = '1,233.10'
        ws[f'B{current_row}'].font = Font(size=11, bold=True)
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'B{current_row}'].fill = PatternFill(start_color='99CCFF', end_color='99CCFF', fill_type='solid')
        
        ws[f'C{current_row}'] = '1,021.3'
        ws[f'C{current_row}'].font = Font(size=11, bold=True)
        ws[f'C{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'C{current_row}'].fill = PatternFill(start_color='99CCFF', end_color='99CCFF', fill_type='solid')
        
        ws[f'D{current_row}'] = '857.00'
        ws[f'D{current_row}'].font = Font(size=11, bold=True)
        ws[f'D{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'D{current_row}'].fill = PatternFill(start_color='99CCFF', end_color='99CCFF', fill_type='solid')
        
        ws[f'E{current_row}'] = '759.59'
        ws[f'E{current_row}'].font = Font(size=11, bold=True)
        ws[f'E{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'E{current_row}'].fill = PatternFill(start_color='99CCFF', end_color='99CCFF', fill_type='solid')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # Add empty row
        ws.row_dimensions[current_row].height = 6.0
        current_row += 1
        
        return current_row
    
    def _add_notes_section(self, ws, current_row):
        """Add charts and notes section EXACTLY as template"""
        # Store the starting row for charts
        charts_start_row = current_row
        
        # Add charts section headers
        ws[f'B{current_row}'] = 'NPC-PSALM Capacity Mix'
        ws[f'B{current_row}'].font = Font(size=11, bold=True, color='FFFFFF')
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'B{current_row}'].fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        ws.merge_cells(f'B{current_row}:D{current_row}')
        
        ws[f'H{current_row}'] = 'MinGen Forecasted Load Share (MW), @6pm Today'
        ws[f'H{current_row}'].font = Font(size=11, bold=True, color='FFFFFF')
        ws[f'H{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'H{current_row}'].fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        ws.merge_cells(f'H{current_row}:N{current_row}')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # Create PIE CHART - NPC-PSALM Capacity Mix
        pie_chart = PieChart()
        pie_chart.title = None  # No title, we have the header above
        pie_chart.width = 10
        pie_chart.height = 10
        
        # Add data for pie chart (Hydro vs Coal Fired Thermal)
        # Create hidden data cells for the chart
        data_row = current_row
        ws[f'A{data_row}'] = 'Hydro'
        ws[f'B{data_row}'] = 811.31
        ws[f'A{data_row}'].font = Font(size=1, color='FFFFFF')  # Hidden
        ws[f'B{data_row}'].font = Font(size=1, color='FFFFFF')  # Hidden
        
        data_row += 1
        ws[f'A{data_row}'] = 'Coal Fired Thermal'
        ws[f'B{data_row}'] = 210.00
        ws[f'A{data_row}'].font = Font(size=1, color='FFFFFF')  # Hidden
        ws[f'B{data_row}'].font = Font(size=1, color='FFFFFF')  # Hidden
        
        # Set chart data
        labels = Reference(ws, min_col=1, min_row=current_row, max_row=current_row+1)
        data = Reference(ws, min_col=2, min_row=current_row, max_row=current_row+1)
        pie_chart.add_data(data)
        pie_chart.set_categories(labels)
        
        # Style the pie chart
        pie_chart.dataLabels = DataLabelList()
        pie_chart.dataLabels.showVal = True
        pie_chart.dataLabels.showPercent = True
        pie_chart.dataLabels.showCatName = False
        
        # Add pie chart to worksheet
        ws.add_chart(pie_chart, f'B{current_row + 2}')
        
        # Create BAR CHART - MinGen Forecasted Load Share
        bar_chart = BarChart()
        bar_chart.type = "col"  # Column chart
        bar_chart.title = None
        bar_chart.width = 15
        bar_chart.height = 10
        bar_chart.y_axis.title = None
        bar_chart.x_axis.title = None
        
        # Add data for bar chart (Plant forecasted loads)
        bar_data_start = current_row + 3
        plants_data = [
            ('AGUS 1', 60.0),
            ('AGUS 2', 120.0),
            ('AGUS 4', 96.0),
            ('AGUS 5', 40.0),
            ('AGUS 6', 144.8),
            ('AGUS 7', 40.0),
            ('PULANGI IV', 150.0)
        ]
        
        for idx, (plant, load) in enumerate(plants_data):
            row = bar_data_start + idx
            ws[f'F{row}'] = plant
            ws[f'G{row}'] = load
            ws[f'F{row}'].font = Font(size=1, color='FFFFFF')  # Hidden
            ws[f'G{row}'].font = Font(size=1, color='FFFFFF')  # Hidden
        
        # Set bar chart data
        bar_labels = Reference(ws, min_col=6, min_row=bar_data_start, max_row=bar_data_start + len(plants_data) - 1)
        bar_data = Reference(ws, min_col=7, min_row=bar_data_start, max_row=bar_data_start + len(plants_data) - 1)
        bar_chart.add_data(bar_data)
        bar_chart.set_categories(bar_labels)
        
        # Style the bar chart
        bar_chart.dataLabels = DataLabelList()
        bar_chart.dataLabels.showVal = True
        
        # Add bar chart to worksheet
        ws.add_chart(bar_chart, f'H{current_row + 2}')
        
        # Add space for charts (rows for visual representation)
        for i in range(12):
            ws.row_dimensions[current_row].height = 15.0
            current_row += 1
        
        # Add legend row
        ws[f'B{current_row}'] = '■ Hydro     ■ Coal Fired Thermal'
        ws[f'B{current_row}'].font = Font(size=11, bold=True)
        ws[f'B{current_row}'].alignment = Alignment(horizontal='center', vertical='center')
        ws[f'B{current_row}'].fill = PatternFill(start_color='FFC000', end_color='FFC000', fill_type='solid')
        ws.merge_cells(f'B{current_row}:D{current_row}')
        
        ws.row_dimensions[current_row].height = 18.0
        current_row += 1
        
        # Add empty row
        ws.row_dimensions[current_row].height = 6.0
        current_row += 1
        
        # Notes header
        ws[f'A{current_row}'] = 'Note:'
        ws[f'A{current_row}'].font = Font(size=10, bold=True, italic=True)
        ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='top')
        ws.row_dimensions[current_row].height = 15.0
        current_row += 1
        
        # Notes content - EXACTLY as template
        notes = [
            "1. Dependable Capacity (DC) is the maximum capacity, modified for ambient limitations for a specific period of time, such as month or a season.",
            "2. Available Capacity (AC) is the dependable capacity, modified for equipment limitations for any time.",
            "3. The usual occurrence of Peak is at 1200H.",
            "4. AGUS 5 HEP gate no. 2 clogged at 0.10m for Nawlach Pulp Inc. (NPI) plant water use."
        ]
        
        for note in notes:
            ws[f'A{current_row}'] = note
            ws[f'A{current_row}'].font = Font(size=9)
            ws[f'A{current_row}'].alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            ws.merge_cells(f'A{current_row}:N{current_row}')
            ws.row_dimensions[current_row].height = 13.5
            current_row += 1
        
        return current_row
    
    def _add_footer(self, ws, start_row):
        """Add footer section with signatures EXACTLY as template"""
        # Add spacing
        start_row += 2
        
        # Prepared by, Checked by, Approved by
        ws[f'A{start_row}'] = 'Prepared by:'
        ws[f'A{start_row}'].font = Font(size=10)
        ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        
        ws[f'G{start_row}'] = 'Checked and Reviewed by:'
        ws[f'G{start_row}'].font = Font(size=10)
        ws[f'G{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        ws.merge_cells(f'G{start_row}:H{start_row}')
        
        ws[f'K{start_row}'] = 'Approved by:'
        ws[f'K{start_row}'].font = Font(size=10)
        ws[f'K{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        
        ws.row_dimensions[start_row].height = 13.5
        start_row += 1
        
        # Empty rows for signature space
        for i in range(3):
            ws.row_dimensions[start_row].height = 13.5
            start_row += 1
        
        # Names
        ws[f'A{start_row}'] = 'DRB CAIRO'
        ws[f'A{start_row}'].font = Font(size=11, bold=True)
        ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        
        ws[f'G{start_row}'] = 'JMM MATA'
        ws[f'G{start_row}'].font = Font(size=11, bold=True)
        ws[f'G{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        ws.merge_cells(f'G{start_row}:H{start_row}')
        
        ws[f'K{start_row}'] = 'DB ESMADE, JR.'
        ws[f'K{start_row}'].font = Font(size=11, bold=True)
        ws[f'K{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        ws.merge_cells(f'K{start_row}:M{start_row}')
        
        ws.row_dimensions[start_row].height = 13.5
        start_row += 1
        
        # Titles
        ws[f'A{start_row}'] = 'Prin. Engr. A, GPD'
        ws[f'A{start_row}'].font = Font(size=10)
        ws[f'A{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        
        ws[f'G{start_row}'] = 'Manager, GPD'
        ws[f'G{start_row}'].font = Font(size=10)
        ws[f'G{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        
        ws[f'K{start_row}'] = 'Dept. Manager, OPD'
        ws[f'K{start_row}'].font = Font(size=10)
        ws[f'K{start_row}'].alignment = Alignment(horizontal='left', vertical='top')
        ws.merge_cells(f'K{start_row}:M{start_row}')
        
        ws.row_dimensions[start_row].height = 13.5
    
    def _get_file_path(self):
        """Generate file path for PSR export"""
        export_dir = os.path.join(settings.MEDIA_ROOT, 'exports')
        os.makedirs(export_dir, exist_ok=True)
        
        date_str = self.report_date.strftime('%Y%m%d')
        filename = f'PSR_REPORT_{date_str}.xlsx'
        
        return os.path.join(export_dir, filename)
