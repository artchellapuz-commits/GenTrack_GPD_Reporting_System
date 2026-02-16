"""
Test uploading SAMPLE_PULANGI4.xlsx to see the exact error
"""
import requests
import os

# Configuration
API_URL = "http://localhost:8000"
EXCEL_FILE = "SAMPLE_PULANGI4.xlsx"
PLANT_CODE = "PULANGI4"

# Get authentication token (if needed)
# For testing, we'll try without auth first since views have AllowAny

print("=" * 60)
print("TESTING PULANGI 4 UPLOAD")
print("=" * 60)
print()

# Check if file exists
if not os.path.exists(EXCEL_FILE):
    print(f"❌ Error: {EXCEL_FILE} not found!")
    print(f"   Run: python CREATE_PULANGI4_SAMPLE.py")
    exit(1)

print(f"✓ Found file: {EXCEL_FILE}")
print(f"  File size: {os.path.getsize(EXCEL_FILE)} bytes")
print()

# Prepare upload
print(f"Uploading to: {API_URL}/api/uploads/upload/")
print(f"Plant code: {PLANT_CODE}")
print()

try:
    with open(EXCEL_FILE, 'rb') as f:
        files = {'file': (EXCEL_FILE, f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        data = {'plant_code': PLANT_CODE}
        
        response = requests.post(
            f"{API_URL}/api/uploads/upload/",
            files=files,
            data=data
        )
    
    print(f"Response Status: {response.status_code}")
    print()
    
    if response.status_code == 201:
        print("✓ SUCCESS!")
        result = response.json()
        print(f"  Records imported: {result.get('records_imported', 0)}")
        print(f"  File ID: {result.get('file_id', 'N/A')}")
        print(f"  Message: {result.get('message', '')}")
    else:
        print("❌ UPLOAD FAILED")
        print()
        print("Response Body:")
        try:
            error_data = response.json()
            print(f"  Error: {error_data.get('error', 'Unknown error')}")
            
            # Print detailed error if available
            if 'error' in error_data:
                error_msg = error_data['error']
                print()
                print("Detailed Error:")
                print("-" * 60)
                print(error_msg)
                print("-" * 60)
        except:
            print(response.text)
    
    print()
    
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to backend server!")
    print()
    print("Make sure backend is running:")
    print("  cd npc-reporting-system/backend")
    print("  venv\\Scripts\\activate")
    print("  python manage.py runserver")
    print()
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    print()
    import traceback
    traceback.print_exc()

print("=" * 60)
