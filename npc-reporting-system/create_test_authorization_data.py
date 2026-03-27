#!/usr/bin/env python
"""
Script to create test data for SignatoryAuthorizationRequest component
Run this from the backend directory: python create_test_authorization_data.py
"""

import os
import django
from django.utils import timezone
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorization, SignatoryAuthorizationRequest

def create_test_data():
    """Create test authorization data"""
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✓ Created test user: {user.username}")
    else:
        print(f"✓ Using existing user: {user.username}")
    
    # Create active authorizations
    signatories = [
        ('O.M. LAVA', 'Approved by'),
        ('JMM MATA', 'Checked and Reviewed by'),
    ]
    
    for signatory_name, role in signatories:
        auth, created = SignatoryAuthorization.objects.get_or_create(
            user=user,
            signatory_name=signatory_name,
            role=role,
            defaults={
                'is_active': True,
                'authorization_date': timezone.now(),
                'expiry_date': timezone.now() + timedelta(days=365),
                'requires_2fa': True,
                'is_valid': True
            }
        )
        
        if created:
            print(f"✓ Created authorization: {signatory_name} ({role})")
        else:
            print(f"✓ Authorization already exists: {signatory_name} ({role})")
    
    # Create pending requests
    pending_requests = [
        ('EL ADIONG', 'Prepared by', 'I need to prepare reports for the GPD department'),
        ('C.C. AMIGABLE JR.', 'Approved by', 'I require approval authority for departmental reports'),
    ]
    
    for signatory_name, role, justification in pending_requests:
        req, created = SignatoryAuthorizationRequest.objects.get_or_create(
            user=user,
            signatory_name=signatory_name,
            role=role,
            defaults={
                'justification': justification,
                'status': 'PENDING',
                'created_at': timezone.now(),
                'admin_notes': ''
            }
        )
        
        if created:
            print(f"✓ Created pending request: {signatory_name} ({role})")
        else:
            print(f"✓ Pending request already exists: {signatory_name} ({role})")
    
    # Print summary
    print("\n" + "="*60)
    print("TEST DATA SUMMARY")
    print("="*60)
    print(f"User: {user.username} ({user.email})")
    print(f"Active Authorizations: {SignatoryAuthorization.objects.filter(user=user, is_active=True).count()}")
    print(f"Pending Requests: {SignatoryAuthorizationRequest.objects.filter(user=user, status='PENDING').count()}")
    print(f"Available Signatories: 6")
    print("="*60)
    print("\nYou can now log in with:")
    print(f"  Username: {user.username}")
    print(f"  Password: testpass123")
    print("\nThe stats cards should now display:")
    print("  - Active Authorizations: 2")
    print("  - Pending Requests: 2")
    print("  - Available Signatories: 6")

if __name__ == '__main__':
    try:
        create_test_data()
        print("\n✓ Test data created successfully!")
    except Exception as e:
        print(f"\n✗ Error creating test data: {e}")
        import traceback
        traceback.print_exc()
