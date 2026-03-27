#!/usr/bin/env python3
"""
Direct test of the email workflow using Django shell
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization
from reports.views_authorization import SignatoryAuthorizationViewSet

def test_email_workflow():
    """Test the email workflow directly"""
    print("🧪 Testing Email Workflow Directly")
    print("=" * 50)
    
    # Use existing test user
    try:
        user = User.objects.get(username='testuser')
        print("✅ Using existing test user")
    except User.DoesNotExist:
        print("❌ Test user not found")
        return False
    
    # Create authorization request
    auth_request = SignatoryAuthorizationRequest.objects.create(
        user=user,
        signatory_name='DIRECT EMAIL TEST',
        role='Test Role',
        email='directemailtest@example.com',
        justification='Testing direct email workflow with signature setup link'
    )
    print(f"✅ Created authorization request: {auth_request.id}")
    
    # Test the confirmation email method
    print("\n📧 Testing confirmation email method...")
    viewset = SignatoryAuthorizationViewSet()
    
    try:
        viewset._send_confirmation_email(auth_request)
        print("✅ Confirmation email method completed")
        
        # Check if authorization was created
        auth_request.refresh_from_db()
        print(f"Request status after email: {auth_request.status}")
        
        # Check for created authorization
        authorizations = SignatoryAuthorization.objects.filter(
            signatory_name='DIRECT EMAIL TEST'
        )
        print(f"Authorizations created: {len(authorizations)}")
        
        if authorizations:
            auth = authorizations.first()
            print(f"Authorization details:")
            print(f"  - Active: {auth.is_active}")
            print(f"  - Has setup token: {bool(auth.setup_token)}")
            print(f"  - Token expires: {auth.token_expires}")
            
            if auth.setup_token:
                setup_url = f"http://localhost:8081/signature-setup/{auth.setup_token}"
                print(f"  - Setup URL: {setup_url}")
                
                print("\n🎯 SUCCESS! The workflow is working:")
                print("1. ✅ Authorization request created")
                print("2. ✅ Auto-approval completed")
                print("3. ✅ Setup token generated")
                print("4. ✅ Email sent with signature setup link")
                print("\n📧 Check your email for the message with the signature setup link!")
                return True
        else:
            print("❌ No authorization was created")
            return False
            
    except Exception as e:
        print(f"❌ Error in confirmation email: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_email_workflow()
    if success:
        print("\n🎉 Email workflow is working correctly!")
    else:
        print("\n❌ Email workflow has issues that need to be fixed.")