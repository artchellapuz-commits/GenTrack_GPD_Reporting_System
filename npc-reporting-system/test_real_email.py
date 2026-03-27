#!/usr/bin/env python3
"""
Simple script to test real email delivery
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_real_email():
    print("📧 Testing Real Email Delivery")
    print("=" * 40)
    
    # Get recipient email from user
    recipient = input("Enter your email address to test: ").strip()
    
    if not recipient:
        print("❌ No email address provided")
        return False
    
    print(f"\n📤 Sending test email to: {recipient}")
    print(f"📤 From: {settings.DEFAULT_FROM_EMAIL}")
    print(f"📤 SMTP Host: {settings.EMAIL_HOST}")
    
    try:
        send_mail(
            subject='🧪 Test Email from NPC Reporting System',
            message='''Hello!

This is a test email from the NPC Reporting System to verify that email delivery is working correctly.

If you received this email, the email configuration is working properly and you will receive:
- Confirmation emails when you submit authorization requests
- Approval/rejection notifications when requests are processed

Test Details:
- System: NPC Reporting System
- Feature: Authorization Request Notifications
- Status: Email delivery working ✅

Best regards,
NPC Reporting System
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        print("✅ Email sent successfully!")
        print(f"\n📬 Check your inbox: {recipient}")
        print("📬 Also check spam/junk folder if not in inbox")
        
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
        
        if "Application-specific password required" in str(e):
            print("\n💡 Solution: You need to set up Gmail App Password")
            print("   1. Enable 2-Factor Authentication on Gmail")
            print("   2. Generate App Password for Mail")
            print("   3. Use App Password instead of regular password")
            print("   4. See GMAIL_SETUP_GUIDE.md for detailed steps")
        
        elif "Authentication failed" in str(e):
            print("\n💡 Solution: Check your email credentials")
            print("   1. Verify email address is correct")
            print("   2. Verify password/app password is correct")
            print("   3. Try a different email provider (Outlook, Yahoo)")
        
        return False

if __name__ == '__main__':
    success = test_real_email()
    
    if success:
        print("\n🎉 Email system is working!")
        print("✅ Users will receive real email notifications")
        print("✅ Authorization request emails will be delivered")
    else:
        print("\n⚠️  Email system needs configuration")
        print("📖 See GMAIL_SETUP_GUIDE.md for help")
    
    sys.exit(0 if success else 1)