#!/usr/bin/env python3
"""
Test live email sending when submitting e-signature request
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatoryAuthorizationRequest, User
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.utils import timezone
from unittest.mock import Mock

def test_live_email_request():
    """Test submitting a live e-signature request and check if emails are sent"""
    print("🧪 Testing Live E-Signature Request Email Flow")
    print("=" * 60)
    
    # Get or create a test user
    try:
        user = User.objects.get(username='Admin')
        print(f"✅ Using existing user: {user.username}")
    except User.DoesNotExist:
        print("❌ No test user found. Please create a user first.")
        return False
    
    # Create test request data
    test_data = {
        'signatory_name': 'TEST EMAIL SIGNATORY',
        'role': 'Checked and Reviewed by',
        'justification': 'Testing live email sending functionality for e-signature requests',
        'email': 'zahurtongtong@gmail.com'
    }
    
    print(f"\n📝 Creating test request:")
    print(f"   User: {user.username}")
    print(f"   Signatory: {test_data['signatory_name']}")
    print(f"   Email: {test_data['email']}")
    print(f"   Justification: {test_data['justification']}")
    
    # Create the request directly (simulating the API call)
    try:
        print(f"\n🔄 Creating authorization request...")
        
        auth_request = SignatoryAuthorizationRequest.objects.create(
            user=user,
            signatory_name=test_data['signatory_name'],
            role=test_data['role'],
            justification=test_data['justification'],
            email=test_data['email'],
            status='PENDING'
        )
        
        print(f"✅ Request created with ID: {auth_request.id}")
        
        # Now test the email methods directly
        print(f"\n📧 Testing email methods...")
        
        viewset = SignatoryAuthorizationViewSet()
        
        # Test admin notification
        print(f"   📤 Sending admin notification...")
        viewset._notify_admins_of_request(auth_request)
        
        # Test user confirmation
        print(f"   📤 Sending user confirmation...")
        viewset._send_confirmation_email(auth_request)
        
        print(f"\n✅ Email methods executed successfully!")
        print(f"📬 Check your email inbox: {test_data['email']}")
        print(f"📬 Also check spam/junk folder")
        
        # Clean up
        print(f"\n🧹 Cleaning up test data...")
        auth_request.delete()
        print(f"✅ Test request deleted")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_recent_requests():
    """Check recent authorization requests to see if any were created"""
    print(f"\n📋 Checking Recent Authorization Requests")
    print("=" * 50)
    
    recent_requests = SignatoryAuthorizationRequest.objects.all().order_by('-created_at')[:10]
    
    if not recent_requests:
        print("❌ No authorization requests found")
        return
    
    print(f"📝 Found {len(recent_requests)} recent requests:")
    
    for i, req in enumerate(recent_requests, 1):
        print(f"\n   {i}. Request ID: {req.id}")
        print(f"      User: {req.user.username}")
        print(f"      Email: {req.email}")
        print(f"      Signatory: {req.signatory_name}")
        print(f"      Status: {req.status}")
        print(f"      Created: {req.created_at}")
        
        # Check if this request should have triggered emails
        if req.status == 'PENDING' and req.created_at:
            time_diff = timezone.now() - req.created_at
            if time_diff.total_seconds() < 3600:  # Within last hour
                print(f"      🔔 This request should have triggered emails!")

def main():
    print("🔍 LIVE EMAIL REQUEST TESTER")
    print("=" * 40)
    
    # Check recent requests first
    check_recent_requests()
    
    # Test live email request
    success = test_live_email_request()
    
    print(f"\n🎯 TEST RESULT")
    print("=" * 20)
    
    if success:
        print("✅ Live email test completed successfully!")
        print("💡 If you didn't receive emails, check:")
        print("   • Email spam/junk folder")
        print("   • Django server console for error messages")
        print("   • Email configuration in .env file")
    else:
        print("❌ Live email test failed!")
        print("💡 Check the error messages above for details")

if __name__ == "__main__":
    main()