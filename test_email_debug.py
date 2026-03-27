#!/usr/bin/env python3
"""
Debug script to test email functionality for e-signature requests
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from reports.models import SignatoryAuthorizationRequest, User
from django.utils import timezone

def test_email_configuration():
    """Test basic email configuration"""
    print("🔧 Testing Email Configuration")
    print("=" * 40)
    
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")
    
    # Test basic email sending
    try:
        print("\n📧 Sending test email...")
        send_mail(
            'Test Email from NPC Reporting System',
            'This is a test email to verify SMTP configuration.',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
            ['zahurtongtong@gmail.com'],
            fail_silently=False,
        )
        print("✅ Test email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        return False

def test_authorization_request_emails():
    """Test the authorization request email flow"""
    print("\n🖊️ Testing Authorization Request Email Flow")
    print("=" * 50)
    
    # Check if we have any authorization requests
    requests = SignatoryAuthorizationRequest.objects.all().order_by('-created_at')[:5]
    
    if not requests:
        print("❌ No authorization requests found in database")
        return False
    
    print(f"📋 Found {requests.count()} authorization requests")
    
    for req in requests:
        print(f"\n📝 Request ID: {req.id}")
        print(f"   User: {req.user.username}")
        print(f"   Email: {req.email}")
        print(f"   Signatory: {req.signatory_name}")
        print(f"   Status: {req.status}")
        print(f"   Created: {req.created_at}")
        
        # Test sending confirmation email manually
        try:
            print("   📧 Testing confirmation email...")
            
            # Extract last name for greeting
            signatory_parts = req.signatory_name.split()
            if len(signatory_parts) > 1:
                last_name = signatory_parts[-1]
                if last_name.upper() in ['JR.', 'JR', 'SR.', 'SR', 'III', 'II']:
                    last_name = signatory_parts[-2] if len(signatory_parts) > 2 else signatory_parts[0]
                greeting = f"Dear {last_name},"
            else:
                greeting = f"Dear {req.signatory_name},"
            
            recipient_email = req.email or req.user.email
            if not recipient_email:
                print("   ❌ No email address found")
                continue
            
            subject = f'E-Signature Required - {req.signatory_name}'
            message = f"""
{greeting}

The NPC Reporting System requires your e-signature for the following:

Signatory Name: {req.signatory_name}
Role: {req.role}

Reason for E-Signature Request:
{req.justification}

Please coordinate with the Data Manager or System Administrator to complete your e-signature setup for the reporting system.

Best regards,
NPC Reporting System
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@npc-reporting.com',
                [recipient_email],
                fail_silently=False,
            )
            print(f"   ✅ Email sent to {recipient_email}")
            
        except Exception as e:
            print(f"   ❌ Failed to send email: {e}")
    
    return True

def check_django_logs():
    """Check for any Django errors"""
    print("\n📋 Checking Django Configuration")
    print("=" * 40)
    
    # Check if we can import the views
    try:
        from reports.views_authorization import SignatoryAuthorizationViewSet
        print("✅ Authorization views imported successfully")
    except Exception as e:
        print(f"❌ Failed to import authorization views: {e}")
        return False
    
    # Check if email methods exist
    viewset = SignatoryAuthorizationViewSet()
    if hasattr(viewset, '_send_confirmation_email'):
        print("✅ _send_confirmation_email method exists")
    else:
        print("❌ _send_confirmation_email method missing")
    
    if hasattr(viewset, '_notify_admins_of_request'):
        print("✅ _notify_admins_of_request method exists")
    else:
        print("❌ _notify_admins_of_request method missing")
    
    return True

def main():
    print("🔍 E-SIGNATURE EMAIL DEBUG TOOL")
    print("=" * 50)
    
    # Test 1: Basic email configuration
    email_works = test_email_configuration()
    
    # Test 2: Django configuration
    django_ok = check_django_logs()
    
    # Test 3: Authorization request emails
    if email_works and django_ok:
        test_authorization_request_emails()
    
    print("\n🎯 DEBUGGING COMPLETE")
    print("=" * 30)
    
    if not email_works:
        print("❌ ISSUE: Email configuration problem")
        print("💡 SOLUTION: Check SMTP settings in .env file")
    elif not django_ok:
        print("❌ ISSUE: Django configuration problem")
        print("💡 SOLUTION: Check views_authorization.py file")
    else:
        print("✅ All systems appear to be working")
        print("💡 If emails still not received, check:")
        print("   • Spam/junk folder")
        print("   • Gmail app password is correct")
        print("   • Django server logs for errors")

if __name__ == "__main__":
    main()