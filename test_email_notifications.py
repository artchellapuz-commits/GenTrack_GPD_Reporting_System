#!/usr/bin/env python3
"""
Test script to verify email notifications for authorization requests
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest
from reports.views_authorization import SignatoryAuthorizationViewSet
from django.core.mail import send_mail
from django.conf import settings
from unittest.mock import Mock

def test_email_configuration():
    """Test email configuration"""
    print("📧 Testing Email Configuration...")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
        print("   ⚠️  Using console backend - emails will print to console")
    else:
        print("   ✅ Using SMTP backend - emails will be sent")

def test_basic_email_sending():
    """Test basic email sending functionality"""
    print("\n📤 Testing Basic Email Sending...")
    
    try:
        send_mail(
            'Test Email from NPC Reporting System',
            'This is a test email to verify email functionality.',
            settings.DEFAULT_FROM_EMAIL,
            ['test@example.com'],
            fail_silently=False,
        )
        print("   ✅ Basic email sending works!")
        return True
    except Exception as e:
        print(f"   ❌ Email sending failed: {e}")
        return False

def test_authorization_request_notifications():
    """Test authorization request email notifications"""
    print("\n🔐 Testing Authorization Request Notifications...")
    
    # Get or create a test user
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("   ❌ No admin user found for testing")
        return False
    
    print(f"   Using user: {user.username}")
    
    # Create a test authorization request
    test_email = "test.user@example.com"
    auth_request = SignatoryAuthorizationRequest.objects.create(
        user=user,
        signatory_name='O.M. LAVA',
        role='Prepared by',
        email=test_email,
        justification='Testing email notification system for authorization requests'
    )
    
    print(f"   ✅ Created test request with email: {auth_request.email}")
    
    # Test the notification methods
    viewset = SignatoryAuthorizationViewSet()
    
    try:
        # Test admin notification
        print("   📧 Testing admin notification...")
        viewset._notify_admins_of_request(auth_request)
        print("   ✅ Admin notification sent")
        
        # Test approval notification
        print("   📧 Testing approval notification...")
        from reports.models import SignatoryAuthorization
        authorization = SignatoryAuthorization.objects.create(
            user=user,
            signatory_name=auth_request.signatory_name,
            authorized_by=user,
            requires_2fa=True,
            notes="Test authorization"
        )
        viewset._notify_user_of_approval(auth_request, authorization)
        print("   ✅ Approval notification sent")
        
        # Test rejection notification
        print("   📧 Testing rejection notification...")
        auth_request.admin_notes = "Test rejection for email verification"
        viewset._notify_user_of_rejection(auth_request)
        print("   ✅ Rejection notification sent")
        
        # Clean up
        authorization.delete()
        auth_request.delete()
        
        return True
        
    except Exception as e:
        print(f"   ❌ Notification test failed: {e}")
        # Clean up on error
        auth_request.delete()
        return False

if __name__ == '__main__':
    print("🧪 Email Notification Testing Suite")
    print("=" * 50)
    
    test_email_configuration()
    email_works = test_basic_email_sending()
    notifications_work = test_authorization_request_notifications()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Email Configuration: ✅ OK")
    print(f"   Basic Email Sending: {'✅ OK' if email_works else '❌ FAILED'}")
    print(f"   Authorization Notifications: {'✅ OK' if notifications_work else '❌ FAILED'}")
    
    if email_works and notifications_work:
        print("\n🎉 All email tests passed!")
        print("\nNote: If using console backend, check the console output above for email content.")
    else:
        print("\n⚠️  Some email tests failed. Check configuration.")
    
    sys.exit(0 if (email_works and notifications_work) else 1)