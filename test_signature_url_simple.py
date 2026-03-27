#!/usr/bin/env python3
"""
Simple test to check signature URLs
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatoryAuthorization
from reports.serializers_security import SignatoryAuthorizationSerializer

def test_signature_urls():
    """Test signature URLs"""
    print("Testing Signature URLs")
    print("=" * 40)
    
    # Get authorizations with signatures
    auths_with_sigs = SignatoryAuthorization.objects.filter(signature_created=True)
    
    for auth in auths_with_sigs[:5]:  # Test first 5
        print(f"\nAuthorization: {auth.signatory_name}")
        
        serializer = SignatoryAuthorizationSerializer(auth)
        data = serializer.data
        
        print(f"  signature_url: {data.get('signature_url')}")
        print(f"  has_signature: {data.get('has_signature')}")

if __name__ == "__main__":
    test_signature_urls()