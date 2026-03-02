"""
Generate sample Excel files for each Agus-Pulangi plant
"""
import pandas as pd
from datetime import datetime, timedelta
import random

# Plant configurations with their units
PLANTS = {
    'AGUS1': {'units': [1, 2, 3, 4], 'capacity_per_unit': 30},
    'AGUS2': {'units': [1, 2], 'capacity_per_unit': 25},
    'AGUS4': {'units': [1, 2], 'capacity_per_unit': 50},
    'AGUS5': {'units': [1, 2], 'capacity_per_unit': 50},
    'AGUS6': {'units': [1, 2, 3, 4], 'capacity_per_unit': 50},
    'AGUS7': {'units': [1, 2, 3, 4], 'capacity_per_unit': 51.3},
    'PULANGI4': {'units': [1, 2, 3, 4], 'capacity_per_unit': 70}
}

def generate_sample_data(plant_code, units, capacity_per_unit, start_date, num_days=30):
    """Generate sample generation data for a plant"""
    data = []
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        for unit_number in units:
            # Generate realistic operational data
            # Assume 70-95% availability
            availability_hours = random.uniform(16.8, 22.8)  # 70-95% of 24 hours
            
            # Operating hours should be <= availability hours
            operating_hours = random.uniform(availability_hours * 0.8, availability_hours)
            
            # Forced outage hours (0-3 hours typically)
            forced_outage_hours = random.uniform(0, 3) if random.random() < 0.3 else 0
            
            # Scheduled outage hours (0-8 hours occasionally)
            scheduled_outage_hours = random.uniform(0, 8) if random.random() < 0.2 else 0
            
            # Ensure total hours don't exceed 24
            total_outage = forced_outage_hours + scheduled_outage_hours
            if availability_hours + total_outage > 24:
                availability_hours = 24 - total_outage
            if operating_hours > availability_hours:
                operating_hours = availability_hours
            
            # Calculate generation based on operating hours and capacity
            # Assume 70-95% capacity factor when operating
            capacity_factor = random.uniform(0.70, 0.95)
            generation_kwh = operating_hours * capacity_per_unit * 1000 * capacity_factor
            
            # Add some remarks occasionally
            remarks = ""
            if forced_outage_hours > 0:
                remarks = "Forced outage due to equipment maintenance"
            elif scheduled_outage_hours > 0:
                remarks = "Scheduled maintenance"
            elif operating_hours < 12:
                remarks = "Low water level"
            
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'unit_number': unit_number,
                'generation_kwh': round(generation_kwh, 2),
                'operating_hours': round(operating_hours, 2),
                'availability_hours': round(availability_hours, 2),
                'forced_outage_hours': round(forced_outage_hours, 2),
                'scheduled_outage_hours': round(scheduled_outage_hours, 2),
                'remarks': remarks
            })
    
    return data

def create_excel_file(plant_code, data, output_dir='sample_data'):
    """Create an Excel file with the sample data"""
    df = pd.DataFrame(data)
    
    # Create Excel writer
    filename = f'{output_dir}/{plant_code}_Sample_Report.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Generation Report', index=False)
        
        # Get the worksheet
        worksheet = writer.sheets['Generation Report']
        
        # Format the header row
        for cell in worksheet[1]:
            cell.font = cell.font.copy(bold=True)
            cell.fill = cell.fill.copy(fgColor="366092")
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print(f"Created: {filename}")
    return filename

def main():
    """Generate sample Excel files for all plants"""
    import os
    
    # Create output directory if it doesn't exist
    output_dir = 'sample_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Start date for sample data (30 days ago)
    start_date = datetime.now() - timedelta(days=30)
    
    print("Generating sample Excel files for Agus-Pulangi plants...")
    print("=" * 60)
    
    for plant_code, config in PLANTS.items():
        print(f"\nGenerating data for {plant_code}...")
        data = generate_sample_data(
            plant_code,
            config['units'],
            config['capacity_per_unit'],
            start_date,
            num_days=30
        )
        
        create_excel_file(plant_code, data, output_dir)
        print(f"  - {len(data)} records generated")
        print(f"  - Units: {config['units']}")
        print(f"  - Capacity per unit: {config['capacity_per_unit']} MW")
    
    print("\n" + "=" * 60)
    print(f"All sample files created in '{output_dir}/' directory")
    print("\nYou can now upload these files to test the system:")
    for plant_code in PLANTS.keys():
        print(f"  - {plant_code}_Sample_Report.xlsx")

if __name__ == '__main__':
    main()
