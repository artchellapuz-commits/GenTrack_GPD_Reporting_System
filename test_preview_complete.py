#!/usr/bin/env python3
"""
Test script to verify the complete PSR preview includes all sections
"""
import requests
import json
from datetime import datetime

def test_preview_complete():
    """Test that the preview endpoint returns all PSR sections"""
    
    # API endpoint
    url = "http://127.0.0.1:8000/api/generation-reports/preview-report/"
    
    # Test data
    test_data = {
        "plant_codes": ["AGUS1", "AGUS2", "AGUS4", "AGUS5", "AGUS6", "AGUS7", "PULANGI4"],
        "start_date": "2026-03-11",
        "end_date": "2026-03-11",
        "report_type": "psr"
    }
    
    print("Testing PSR Preview Completeness...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print("-" * 50)
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Preview endpoint successful!")
            
            # Check for all expected sections
            expected_sections = [
                'header',
                'plants_data', 
                'totals',
                'forecasted_load',
                'ipp_data',
                'notes',
                'storage_data',           # NEW
                'inflow_outflow_data',    # NEW
                'generation_data',        # NEW
                'capacity_factor_data',   # NEW
                'gate_elevation_data',    # NEW
                'operational_reference',  # NEW
                'input_workflow',         # NEW
                'signatures',
                'footer_note'
            ]
            
            print("\n📋 Section Completeness Check:")
            missing_sections = []
            
            for section in expected_sections:
                if section in data:
                    print(f"✅ {section}: Present")
                    
                    # Show sample data for new sections
                    if section in ['storage_data', 'inflow_outflow_data', 'generation_data', 
                                 'capacity_factor_data', 'gate_elevation_data']:
                        sample_data = data[section][:2] if isinstance(data[section], list) else data[section]
                        print(f"   Sample: {json.dumps(sample_data, indent=4)}")
                        
                else:
                    print(f"❌ {section}: MISSING")
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"\n⚠️  Missing sections: {missing_sections}")
                return False
            else:
                print(f"\n🎉 All {len(expected_sections)} sections present!")
                
                # Show total data size
                total_plants = len(data.get('plants_data', []))
                total_storage = len(data.get('storage_data', []))
                total_generation = len(data.get('generation_data', []))
                
                print(f"\n📊 Data Summary:")
                print(f"   Plants: {total_plants}")
                print(f"   Storage entries: {total_storage}")
                print(f"   Generation entries: {total_generation}")
                print(f"   Gate/elevation entries: {len(data.get('gate_elevation_data', []))}")
                print(f"   Operational reference entries: {len(data.get('operational_reference', {}).get('riparian_flow', []))}")
                
                return True
                
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Django server is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_preview_complete()
    if success:
        print("\n🎯 TEST PASSED: Preview includes all PSR Excel sections!")
    else:
        print("\n💥 TEST FAILED: Preview is missing sections!")
    
    exit(0 if success else 1)