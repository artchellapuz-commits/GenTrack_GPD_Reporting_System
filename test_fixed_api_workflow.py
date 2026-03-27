#!/usr/bin/env python3
"""
Test the fixed API workflow to ensure emails are sent with signature setup links
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization
from reports.views_authorization import SignatoryAuthorizationViewSet
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
import json

def test_api_workflow():
    print("Testing fixed API workflow...")
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"Created test user: {user.username}")
    else:
        print(f"Using existing test user: {user.username}")
    
    # Test data
    test_data = {
        "signatory_name": "TEST API WORKFLOW",
        "role": "Test Role",
        "email": "test@example.com",
        "justification": "Testing the fixed API workflow to ensure emails are sent with signature setup links"
    }
    
    # Create a mock request
    factory = APIRequestFactory()
    request = factory.post('/api/signatory-authorizations/request/', test_data, format='json')
    request.user = user
    
    # Create ViewSet instance and call the method
    viewset = SignatoryAuthorizationViewSet()
    viewset.request = Request(request)
    viewset.format_kwarg = None
    
    try:
        # Call the request_authorization method directly
        response = viewset.request_authorization(Request(request))
        
        print(f"Response status: {response.status_code}")
        print(f"Response data: {json.dumps(response.data, indent=2)}")
        
        # Check if authorization request was created
        auth_request = SignatoryAuthorizationRequest.objects.filter(
            signatory_name="TEST API WORKFLOW"
        ).first()
        
        if auth_request:
            print(f"\nAuthorization request created:")
            print(f"- ID: {auth_request.id}")
            print(f"- Status: {auth_request.status}")
            print(f"- Email: {auth_request.email}")
            print(f"- Signatory: {auth_request.signatory_name}")
            
            # Check if authorization was auto-created
            authorization = SignatoryAuthorization.objects.filter(
                user=user,
                signatory_name="TEST API WORKFLOW"
            ).first()
            
            if authorization:
                print(f"\nAuthorization auto-created:")
                print(f"- ID: {authorization.id}")
                print(f"- Active: {authorization.is_active}")
                print(f"- Setup Token: {authorization.setup_token[:20]}..." if authorization.setup_token else "None")
                print(f"- Token Expires: {authorization.token_expires}")
                print(f"- Signature Created: {authorization.signature_created}")
                
                if authorization.setup_token:
                    setup_url = f"http://localhost:8081/signature-setup/{authorization.setup_token}"
                    print(f"- Setup URL: {setup_url}")
                    print("\n✅ SUCCESS: Email workflow should have been triggered with signature setup link!")
                else:
                    print("\n❌ ERROR: No setup token generated")
            else:
                print("\n❌ ERROR: No authorization was auto-created")
        else:
            print("\n❌ ERROR: No authorization request was created")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_workflow()