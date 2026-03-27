#!/usr/bin/env python3
"""
Test script to approve a request and trigger the approval email with signature setup link
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatoryAuthorizationRequest, User, SignatoryAuthorization
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.utils import timezone
import secrets

def test_approval_email():
    """Test the approval email with signature setup link"""
    print("🔐 Testing Approval Email with Signature Setup Link")
    print("=" * 60)
    
    # Find a pending request
    pending_request = SignatoryAuthorizationRequest.objects.filter(status='PENDING').first()
    
    if not pending_request:
        print("❌ No pending requests found. Creating a test request...")
        
        # Get admin user
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("❌ No admin user found")
            return False
        
        # Create a test request
        pending_request = SignatoryAuthorizationRequest.objects.create(
            user=admin_user,
            signatory_name='TEST APPROVAL EMAIL',
            role='Checked and Reviewed by',
            justification='Testing approval email with signature setup link',
            email='zahurtongtong@gmail.com',
            status='PENDING'
        )
        print(f"✅ Created test request ID: {pending_request.id}")
    
    print(f"\n📝 Processing request:")
    print(f"   ID: {pending_request.id}")
    print(f"   User: {pending_request.user.username}")
    print(f"   Signatory: {pending_request.signatory_name}")
    print(f"   Email: {pending_request.email}")
    
    # Get admin user for approval
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ No admin user found for approval")
        return False
    
    print(f"   Approving as: {admin_user.username}")
    
    try:
        # Create the authorization (simulate approval)
        print(f"\n🔄 Creating authorization...")
        
        # Generate secure token
        setup_token = secrets.token_urlsafe(32)
        
        authorization = SignatoryAuthorization.objects.create(
            user=pending_request.user,
            signatory_name=pending_request.signatory_name,
            authorized_by=admin_user,
            authorization_date=timezone.now(),
            is_active=True,
            requires_2fa=True,
            notes='Test approval for email verification',
            setup_token=setup_token,
            token_expires=timezone.now() + timezone.timedelta(hours=24),
            signature_created=False
        )
        
        print(f"✅ Authorization created with ID: {authorization.id}")
        print(f"✅ Setup token: {setup_token[:20]}...")
        
        # Update request status
        pending_request.status = 'APPROVED'
        pending_request.reviewed_by = admin_user
        pending_request.reviewed_at = timezone.now()
        pending_request.admin_notes = 'Approved for testing email functionality'
        pending_request.save()
        
        print(f"✅ Request status updated to APPROVED")
        
        # Send approval email
        print(f"\n📧 Sending approval email with signature setup link...")
        
        viewset = SignatoryAuthorizationViewSet()
        viewset._notify_user_of_approval(pending_request, authorization)
        
        print(f"✅ Approval email sent!")
        print(f"📬 Check your email: {pending_request.email}")
        print(f"🔗 The email should contain a signature setup link")
        print(f"🖊️ Click the link to open the signature drawing pad")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during approval: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🧪 APPROVAL EMAIL TESTER")
    print("=" * 30)
    
    success = test_approval_email()
    
    print(f"\n🎯 RESULT")
    print("=" * 15)
    
    if success:
        print("✅ Approval email test completed!")
        print("📧 You should now receive an email with:")
        print("   • Subject: 'E-Signature Authorization APPROVED'")
        print("   • Secure signature setup link")
        print("   • Instructions for creating signature")
        print("\n🖊️ Next steps:")
        print("   1. Check your email inbox")
        print("   2. Click the signature setup link")
        print("   3. Draw your signature")
        print("   4. Click 'Save Signature'")
    else:
        print("❌ Approval email test failed!")

if __name__ == "__main__":
    main()