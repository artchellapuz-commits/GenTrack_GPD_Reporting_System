"""
PSR Implementation Verification Script
Checks that all sections from the reference image are implemented
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def verify_psr_sections():
    """Verify all PSR sections are implemented"""
    
    print("=" * 80)
    print("PSR IMPLEMENTATION VERIFICATION")
    print("=" * 80)
    print()
    
    # Read the PSR exporter file
    psr_file = 'backend/reports/services/psr_exporter.py'
    
    with open(psr_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define all required sections
    required_sections = {
        'Main Report Sections': [
            ('_add_header', 'Header with NPC branding and FOR section'),
            ('_add_column_headers', 'Column headers (Plant Name, Rated Capacity, etc.)'),
            ('_add_plant_data', 'Plant data with units (AGUS1-7, PULANGI4)'),
            ('_add_forecasted_load', 'Agus-Pulangi Forecasted Load section'),
            ('_add_ipp_section', 'IPP section (MCFPP STEAG)'),
            ('_add_notes_section', 'Charts and notes section'),
            ('_add_footer', 'Footer with signatures'),
        ],
        'Right Side Sections': [
            ('_add_right_side_sections', 'Main right side sections method'),
            ('PRIMARY STORAGE OF HYDRO HEPs', 'Storage levels table'),
            ('HYDRO INFLOW/OUTFLOW', 'Inflow/outflow data'),
            ('GENERATION DATA', 'Today, MTD, YTD generation'),
            ('CAPACITY FACTOR', 'Capacity factor percentages'),
        ],
        'Gate & Elevation Section': [
            ('_add_gate_elevation_section', 'Gate and elevation method'),
            ('REMARKS', 'Remarks column with stars'),
            ('GATE#1', 'Gate columns'),
            ('ELEVATION', 'Elevation column'),
        ],
        'Helper Methods': [
            ('_calculate_generation_data', 'Generation data calculator'),
            ('_calculate_capacity_factor', 'Capacity factor calculator'),
            ('_get_unit_remarks', 'Unit remarks generator'),
        ],
        'Charts': [
            ('PieChart', 'NPC-PSALM Capacity Mix pie chart'),
            ('BarChart', 'MinGen Forecasted Load Share bar chart'),
        ],
    }
    
    # Verify each section
    all_present = True
    
    for category, sections in required_sections.items():
        print(f"\n{category}:")
        print("-" * 80)
        
        for section_name, description in sections:
            if section_name in content:
                print(f"  ✅ {section_name:40} - {description}")
            else:
                print(f"  ❌ {section_name:40} - {description} [MISSING]")
                all_present = False
    
    print()
    print("=" * 80)
    
    # Check for specific data elements
    print("\nData Elements Verification:")
    print("-" * 80)
    
    data_elements = [
        ('Lake Lanao', 'Lake Lanao storage data'),
        ('Agus 2 Forebay', 'Agus 2 forebay data'),
        ('Pulangi IV Reservoir', 'Pulangi IV reservoir data'),
        ('701.20', 'Lake Lanao elevation'),
        ('637.30', 'Agus 2 elevation'),
        ('283.50', 'Pulangi IV elevation'),
        ('GATE#1', 'Gate column headers'),
        ('★', 'Yellow star for remarks'),
        ('TOTAL AGUS', 'Total Agus row'),
        ('TOTAL HYDRO', 'Total Hydro row'),
        ('TOTAL IPP', 'Total IPP row'),
        ('TOTAL NPC-PSALM', 'Total NPC-PSALM row'),
    ]
    
    for element, description in data_elements:
        if element in content:
            print(f"  ✅ {element:30} - {description}")
        else:
            print(f"  ❌ {element:30} - {description} [MISSING]")
            all_present = False
    
    print()
    print("=" * 80)
    
    # Check column widths
    print("\nColumn Width Configuration:")
    print("-" * 80)
    
    required_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB']
    
    for col in required_columns:
        search_str = f"ws.column_dimensions['{col}'].width"
        if search_str in content:
            print(f"  ✅ Column {col:3} width configured")
        else:
            print(f"  ❌ Column {col:3} width NOT configured [MISSING]")
            all_present = False
    
    print()
    print("=" * 80)
    
    # Final summary
    if all_present:
        print("\n✅ ALL SECTIONS IMPLEMENTED SUCCESSFULLY!")
        print("The PSR report includes all required sections from the reference image.")
    else:
        print("\n⚠️  SOME SECTIONS ARE MISSING!")
        print("Please review the missing sections above.")
    
    print()
    print("=" * 80)
    
    return all_present

if __name__ == '__main__':
    success = verify_psr_sections()
    sys.exit(0 if success else 1)
