import requests
import json

BASE_URL = "http://localhost:8000/api"

# Login first to get token
print("1. Logging in...")
login_response = requests.post(f"{BASE_URL}/auth/login/", json={
    "username": "Admin",
    "password": "admin123"
})

if login_response.status_code == 200:
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    print(f"   ✓ Logged in successfully")
else:
    print(f"   ✗ Login failed: {login_response.status_code}")
    exit(1)

# Test by-signatory endpoint
print("\n2. Testing by-signatory endpoint...")
response = requests.get(
    f"{BASE_URL}/e-signatures/by-signatory/",
    params={'name': 'JMM MATA'},
    headers=headers
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✓ Found {len(response.json())} signatures")
else:
    print(f"   ✗ Error: {response.text}")

# Test create-from-data endpoint
print("\n3. Testing create-from-data endpoint...")
test_signature = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
response = requests.post(
    f"{BASE_URL}/e-signatures/create-from-data/",
    json={
        'signatory_name': 'TEST ENDPOINT',
        'signatory_title': 'Test',
        'signatory_role': 'Prepared by:',
        'signature_type': 'DRAW',
        'signature_data': test_signature,
        'is_default': True
    },
    headers=headers
)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    sig_id = response.json()['id']
    print(f"   ✓ Signature created: ID={sig_id}")
    
    # Test sign-report endpoint
    print("\n4. Testing sign-report endpoint...")
    response = requests.post(
        f"{BASE_URL}/report-signatures/sign-report/",
        json={
            'report_date': '2026-03-18',
            'report_type': 'PSR',
            'signature': sig_id,
            'signatory_name': 'TEST ENDPOINT',
            'signatory_role': 'Prepared by:'
        },
        headers=headers
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        print(f"   ✓ Report signed successfully")
    else:
        print(f"   ✗ Error: {response.text}")
else:
    print(f"   ✗ Error: {response.text}")

print("\nTest complete!")
