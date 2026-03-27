#!/usr/bin/env python3
"""
Test the email method directly to see if it works
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, 'npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest
from reports.views_authorization import SignatoryAuthorizationViewSet

def test_email_method():
    print("Testing email method directly...")
    
    # Get a pending request
    pending_request = SignatoryAuthorizationRequest.objects.filter(
        status='PENDING'
    ).first()
    
    if not pending_request:
        print("❌ No pending requests found")
        return
    
    print(f"Found pending request: {pending_request.signatory_name}")
    
    # Create ViewSet instance
    viewset = SignatoryAuthorizationViewSet()
    
    try:
        # Call the email method directly
        print("Calling _send_confirmation_email method...")
        viewset._send_confirmation_email(pending_request)
        
        # Check if request was updated
        pending_request.refresh_from_db()
        print(f"Request status after email: {pending_request.status}")
        
        # Check if authorization was created
        from reports.models import SignatoryAuthorization
        auth = SignatoryAuthorization.objects.filter(
            user=pending_request.user,
            signatory_name=pending_request.signatory_name
        ).first()
        
        if auth:
            print(f"✅ Authorization created: ID={auth.id}")
            print(f"Setup token: {auth.setup_token[:20]}..." if auth.setup_token else "None")
        else:
            print("❌ No authorization created")
            
    except Exception as e:
        print(f"❌ Error calling email method: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_email_method()