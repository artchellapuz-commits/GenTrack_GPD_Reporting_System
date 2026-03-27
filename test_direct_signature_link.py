#!/usr/bin/env python3
"""
Test the new direct signature link workflow
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

def test_direct_signature_link():
    """Test the new workflow with direct signature link in confirmation email"""
    print("🚀 Testing Direct Signature Link Workflow")
    print("=" * 60)
    
    # Get or create a test user
    try:
        user = User.objects.get(username='Admin')
        print(f"✅ Using existing user: {user.username}")
    except User.DoesNotExist:
        print("❌ No test user found. Please create a user first.")
        return False
    
    # Create test request
    test_data = {
        'signatory_name': 'DIRECT LINK TEST',
        'role': 'Checked and Reviewed by',
        'justification': 'Testing direct signature link in confirmation email',
        'email': 'zahurtongtong@gmail.com'
    }
    
    print(f"\n📝 Creating test authorization request...")
    auth_request = SignatoryAuthorizationRequest.objects.create(
        user=user,
        signatory_name=test_data['signatory_name'],
        role=test_data['role'],
        justification=test_data['justification'],
        email=test_data['email'],
        status='PENDING'
    )
    print(f"✅ Request created with ID: {auth_request.id}")
    
    # Test the new confirmation email with direct signature link
    print(f"\n📧 Sending confirmation email with direct signature setup link...")
    
    viewset = SignatoryAuthorizationViewSet()
    viewset._send_confirmation_email(auth_request)
    
    print(f"\n🎉 SUCCESS! Email sent with direct signature link!")
    print(f"📬 Check your email: {test_data['email']}")
    
    print(f"\n📋 New Simplified Workflow:")
    print(f"   1. ✅ User submits e-signature request")
    print(f"   2. ✅ User immediately gets email with signature link")
    print(f"   3. 🖊️ User clicks link and draws signature")
    print(f"   4. 💾 User clicks 'Save Signature'")
    print(f"   5. 🎉 E-signature ready for use!")
    
    print(f"\n🔗 Email should contain:")
    print(f"   ✅ Professional greeting: 'Dear LINK,'")
    print(f"   ✅ System requirement message")
    print(f"   ✅ Justification details")
    print(f"   ✅ Direct signature setup link")
    print(f"   ✅ Step-by-step instructions")
    print(f"   ✅ 24-hour expiry notice")
    
    # Clean up
    print(f"\n🧹 Cleaning up test data...")
    # Don't delete - let user test the link
    print(f"✅ Test data kept for testing the signature link")
    
    return True

def main():
    print("🔗 DIRECT SIGNATURE LINK TESTER")
    print("=" * 40)
    
    success = test_direct_signature_link()
    
    print(f"\n🎯 RESULT")
    print("=" * 20)
    
    if success:
        print("✅ Direct signature link email sent!")
        print("💡 No more waiting for admin approval!")
        print("💡 Users can create signatures immediately!")
        print("💡 Much faster and simpler workflow!")
        
        print(f"\n🖊️ Next steps:")
        print(f"   1. Check your email inbox")
        print(f"   2. Click the signature setup link")
        print(f"   3. Draw your signature")
        print(f"   4. Click 'Save Signature'")
        print(f"   5. Done! Ready to sign reports")
    else:
        print("❌ Test failed!")

if __name__ == "__main__":
    main()