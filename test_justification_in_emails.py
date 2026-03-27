#!/usr/bin/env python3
"""
Test script to verify that justification details are included in authorization request emails.
This script will create a test authorization request and check the email content.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.core.mail import send_mail
from django.test import RequestFactory
from unittest.mock import patch
import io
import sys

def test_justification_in_emails():
    """Test that justification details are included in both admin and user emails"""
    
    print("🧪 Testing Justification Details in Authorization Request Emails")
    print("=" * 70)
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        username='test_user_justification',
        defaults={
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"✅ Using existing test user: {user.username}")
    
    # Create a test authorization request with detailed justification
    test_justification = """I need authorization to sign documents as the Plant Manager for the following reasons:

1. I am the designated Plant Manager for NPC Mindanao Operations
2. I need to approve daily plant status reports and operational documents
3. My supervisor has delegated signing authority to me for routine operations
4. This authorization is required for compliance with company policies

Please approve this request so I can fulfill my operational responsibilities."""
    
    auth_request = SignatoryAuthorizationRequest.objects.create(
        user=user,
        email='testuser@example.com',
        signatory_name='Test Plant Manager',
        role='Plant Manager',
        justification=test_justification,
        status='PENDING'
    )
    
    print(f"✅ Created test authorization request with ID: {auth_request.id}")
    print(f"📝 Justification length: {len(test_justification)} characters")
    
    # Create view instance
    factory = RequestFactory()
    request = factory.post('/test/')
    request.user = user
    
    view = SignatoryAuthorizationViewSet()
    
    # Capture email content by mocking send_mail
    captured_emails = []
    
    def mock_send_mail(subject, message, from_email, recipient_list, fail_silently=True):
        captured_emails.append({
            'subject': subject,
            'message': message,
            'from_email': from_email,
            'recipients': recipient_list
        })
        return True
    
    # Test admin notification email
    print("\n📧 Testing Admin Notification Email...")
    with patch('reports.views_authorization.send_mail', side_effect=mock_send_mail):
        view._notify_admins_of_request(auth_request)
    
    if captured_emails:
        admin_email = captured_emails[0]
        print(f"✅ Admin email subject: {admin_email['subject']}")
        
        # Check if justification is in the email
        if test_justification in admin_email['message']:
            print("✅ Justification details found in admin email")
            print("📄 Admin email preview:")
            print("-" * 50)
            # Show relevant part of the email
            lines = admin_email['message'].split('\n')
            justification_started = False
            for line in lines:
                if 'Justification:' in line:
                    justification_started = True
                if justification_started:
                    print(line)
                    if line.strip() == '' and justification_started:
                        break
            print("-" * 50)
        else:
            print("❌ Justification details NOT found in admin email")
            print("📄 Full admin email content:")
            print(admin_email['message'])
    else:
        print("❌ No admin email was sent")
    
    # Clear captured emails for user confirmation test
    captured_emails.clear()
    
    # Test user confirmation email
    print("\n📧 Testing User Confirmation Email...")
    with patch('reports.views_authorization.send_mail', side_effect=mock_send_mail):
        view._send_confirmation_email(auth_request)
    
    if captured_emails:
        user_email = captured_emails[0]
        print(f"✅ User email subject: {user_email['subject']}")
        
        # Check if justification is in the email
        if test_justification in user_email['message']:
            print("✅ Justification details found in user confirmation email")
            print("📄 User email preview:")
            print("-" * 50)
            # Show relevant part of the email
            lines = user_email['message'].split('\n')
            justification_started = False
            for line in lines:
                if 'Justification Details:' in line:
                    justification_started = True
                if justification_started:
                    print(line)
                    if line.strip() == '' and justification_started and 'What happens next:' in line:
                        break
            print("-" * 50)
        else:
            print("❌ Justification details NOT found in user confirmation email")
            print("📄 Full user email content:")
            print(user_email['message'])
    else:
        print("❌ No user confirmation email was sent")
    
    # Clean up test data
    auth_request.delete()
    if created:
        user.delete()
    
    print("\n🎉 Test completed!")
    print("✅ Both admin and user emails should now include justification details")
    print("📋 Summary:")
    print("   - Admin emails show justification under 'Justification:' section")
    print("   - User emails show justification under 'Justification Details:' section")
    print("   - This helps admins understand why authorization is needed")

if __name__ == '__main__':
    test_justification_in_emails()