#!/usr/bin/env python3
"""
Test using Django shell to directly call the view method
"""

import subprocess
import sys

def test_django_shell():
    """Test using Django shell"""
    print("🧪 Testing Django Shell Direct Call")
    print("=" * 50)
    
    # Create Django shell command
    shell_command = '''
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.test import RequestFactory
from rest_framework.request import Request
import json

# Get test user
user = User.objects.get(username='testuser')

# Create a mock request
factory = RequestFactory()
django_request = factory.post('/api/signatory-authorizations/request/', 
    json.dumps({
        "signatory_name": "DJANGO SHELL TEST",
        "role": "Test Role", 
        "email": "shelltest@example.com",
        "justification": "Testing via Django shell"
    }),
    content_type='application/json'
)

# Convert to DRF request
request = Request(django_request)
request.user = user

# Parse the JSON data
import json
request._full_data = {
    "signatory_name": "DJANGO SHELL TEST",
    "role": "Test Role", 
    "email": "shelltest@example.com",
    "justification": "Testing via Django shell"
}

# Create viewset and call method
viewset = SignatoryAuthorizationViewSet()
viewset.request = request

print("DEBUG: About to call request_authorization method...")
try:
    response = viewset.request_authorization(request)
    print(f"SUCCESS: Method called successfully!")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.data}")
except Exception as e:
    print(f"ERROR: Error calling method: {e}")
    import traceback
    traceback.print_exc()
'''
    
    # Run Django shell command
    try:
        result = subprocess.run([
            sys.executable, 'manage.py', 'shell', '-c', shell_command
        ], 
        cwd='npc-reporting-system/backend',
        capture_output=True, 
        text=True, 
        timeout=30
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
            
        print(f"\nReturn code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
    except Exception as e:
        print(f"❌ Error running command: {e}")

if __name__ == "__main__":
    test_django_shell()