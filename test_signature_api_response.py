#!/usr/bin/env python3
"""
Test script to check the actual API response for signature data
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

def test_signature_api_response():
    """Test what the API actually returns for signature data"""
    print("🔍 Testing Signature API Response")
    print("=" * 50)
    
    try:
        # Get all authorizations
        authorizations = SignatoryAuthorization.objects.all()
        print(f"📊 Found {authorizations.count()} authorizations")
        
        for auth in authorizations:
            print(f"\n🔍 Authorization: {auth.signatory_name}")
            print(f"   User: {auth.user.username}")
            print(f"   Signature Created: {auth.signature_created}")
            
            # Test the serializer
            serializer = SignatoryAuthorizationSerializer(auth)
            data = serializer.data
            
            print(f"   API Response:")
            print(f"     signature_created: {data.get('signature_created')}")
            print(f"     has_signature: {data.get('has_signature')}")
            print(f"     signature_url: {data.get('signature_url')}")
            
            # Check if file exists manually
            if auth.signature_created:
                import glob
                from django.conf import settings
                
                base_filename = auth.signatory_name.lower().replace(' ', '_').replace('.', '_')
                admin_signatures_dir = os.path.join(settings.MEDIA_ROOT, 'admin_signatures')
                glob_pattern = os.path.join(admin_signatures_dir, f"{base_filename}*signature*")
                matching_files = glob.glob(glob_pattern)
                
                print(f"     Expected pattern: {base_filename}*signature*")
                print(f"     Matching files: {[os.path.basename(f) for f in matching_files]}")
                
                # Also check exact filename
                exact_filename = f"{base_filename}_signature.png"
                exact_path = os.path.join(admin_signatures_dir, exact_filename)
                print(f"     Exact filename: {exact_filename}")
                print(f"     Exact file exists: {os.path.exists(exact_path)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_signature_api_response()