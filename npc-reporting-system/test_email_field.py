#!/usr/bin/env python3
"""
Test script to verify the email field implementation in authorization requests
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

def test_email_field():
    """Test that the email field works correctly"""
    
    print("🧪 Testing email field implementation...")
    
    # Create a test user if it doesn't exist
    test_user, created = User.objects.get_or_create(
        username='test_email_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Using existing test user: {test_user.username}")
    
    # Test creating an authorization request with email
    test_email = "notification@example.com"
    
    try:
        auth_request = SignatoryAuthorizationRequest.objects.create(
            user=test_user,
            signatory_name='O.M. LAVA',
            role='Prepared by',
            email=test_email,
            justification='Testing email field implementation for authorization requests'
        )
        
        print(f"✅ Created authorization request with email: {auth_request.email}")
        print(f"   - ID: {auth_request.id}")
        print(f"   - User: {auth_request.user.username}")
        print(f"   - Signatory: {auth_request.signatory_name}")
        print(f"   - Email: {auth_request.email}")
        print(f"   - Status: {auth_request.status}")
        
        # Verify the email field is saved correctly
        retrieved_request = SignatoryAuthorizationRequest.objects.get(id=auth_request.id)
        assert retrieved_request.email == test_email, f"Email mismatch: {retrieved_request.email} != {test_email}"
        
        print("✅ Email field verification successful!")
        
        # Test email validation (this would be done in the frontend/serializer)
        valid_emails = [
            "user@example.com",
            "test.email+tag@domain.co.uk",
            "user123@test-domain.com"
        ]
        
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user space@domain.com"
        ]
        
        print("\n📧 Testing email validation patterns:")
        
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        
        for email in valid_emails:
            is_valid = bool(re.match(email_regex, email))
            print(f"   ✅ {email}: {'Valid' if is_valid else 'Invalid'}")
            assert is_valid, f"Valid email marked as invalid: {email}"
        
        for email in invalid_emails:
            is_valid = bool(re.match(email_regex, email))
            print(f"   ❌ {email}: {'Valid' if is_valid else 'Invalid'}")
            assert not is_valid, f"Invalid email marked as valid: {email}"
        
        print("\n🎉 All tests passed! Email field implementation is working correctly.")
        
        # Clean up
        auth_request.delete()
        if created:
            test_user.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing email field: {e}")
        return False

if __name__ == '__main__':
    success = test_email_field()
    sys.exit(0 if success else 1)