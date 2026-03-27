#!/usr/bin/env python3
"""
Test script to verify that the direct signature link is included in emails
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.test import RequestFactory
from unittest.mock import patch
import json

def test_direct_signature_email():
    """Test that emails contain direct signature links"""
    
    print("🧪 Testing Direct Signature Email Links...")
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='test_signatory',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    # Create authorization request
    auth_request = SignatoryAuthorizationRequest.objects.create(
        user=user,
        signatory_name='C.C. AMIGABLE JR.',
        role='Checked and Reviewed by',
        justification='Testing direct signature link functionality',
        email='test@example.com'
    )
    
    print(f"✅ Created test authorization request: {auth_request.id}")
    
    # Create viewset instance
    viewset = SignatoryAuthorizationViewSet()
    
    # Mock send_mail to capture email content
    captured_emails = []
    
    def mock_send_mail(subject, message, from_email, recipient_list, fail_silently=True):
        captured_emails.append({
            'subject': subject,
            'message': message,
            'from_email': from_email,
            'recipient_list': recipient_list
        })
        print(f"📧 Email captured: {subject}")
        return True
    
    # Test the confirmation email with direct signature link
    with patch('reports.views_authorization.send_mail', side_effect=mock_send_mail):
        viewset._send_confirmation_email(auth_request)
    
    # Verify email was sent
    if captured_emails:
        email = captured_emails[0]
        print(f"\n📧 Email Subject: {email['subject']}")
        print(f"📧 Email Recipients: {email['recipient_list']}")
        print(f"\n📧 Email Content:")
        print("=" * 60)
        print(email['message'])
        print("=" * 60)
        
        # Check if signature setup link is in the email
        if 'signature-setup/' in email['message']:
            print("\n✅ SUCCESS: Direct signature link found in email!")
            print("🖊️ Users can click the link to go directly to signature drawing")
        else:
            print("\n❌ ERROR: No direct signature link found in email")
            
        # Check if proper instructions are included
        if 'CREATE YOUR E-SIGNATURE NOW' in email['message']:
            print("✅ Clear call-to-action found")
        else:
            print("❌ Missing clear call-to-action")
            
        if 'Draw your signature using your mouse or touch screen' in email['message']:
            print("✅ Drawing instructions found")
        else:
            print("❌ Missing drawing instructions")
            
        if 'Click "Save Signature" to submit it to the system' in email['message']:
            print("✅ Save instructions found")
        else:
            print("❌ Missing save instructions")
            
    else:
        print("❌ No email was sent!")
    
    # Check if authorization was auto-created
    from reports.models import SignatoryAuthorization
    authorizations = SignatoryAuthorization.objects.filter(
        signatory_name='C.C. AMIGABLE JR.',
        user=user
    )
    
    if authorizations.exists():
        auth = authorizations.first()
        print(f"\n✅ Authorization auto-created with setup token")
        print(f"🔑 Token expires: {auth.token_expires}")
        print(f"🔒 Requires 2FA: {auth.requires_2fa}")
        print(f"✏️ Signature created: {auth.signature_created}")
    else:
        print("\n❌ No authorization was auto-created")
    
    # Clean up
    auth_request.delete()
    if authorizations.exists():
        authorizations.delete()
    
    print(f"\n🧹 Cleaned up test data")
    print("🎉 Test completed!")

if __name__ == '__main__':
    test_direct_signature_email()