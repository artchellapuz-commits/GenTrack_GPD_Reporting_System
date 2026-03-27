#!/usr/bin/env python3
"""
Test script to verify signature link generation fix
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, Document
from django.contrib.auth.models import User
from django.conf import settings

def test_signature_url_generation():
    """Test that signature URLs are generated with correct base URL"""
    print("Testing signature URL generation...")
    print(f"SITE_URL setting: {getattr(settings, 'SITE_URL', 'Not set')}")
    
    # Create a test signature request (without saving to DB)
    signature_request = SignatureRequest(token='test-token-123')
    
    # Test default URL generation (should use SITE_URL from settings)
    default_url = signature_request.generate_signing_url()
    print(f"Default URL: {default_url}")
    
    # Test with custom base URL
    custom_url = signature_request.generate_signing_url('http://custom-domain.com')
    print(f"Custom URL: {custom_url}")
    
    # Verify the URLs
    expected_default = f"{settings.SITE_URL}/sign/test-token-123"
    expected_custom = "http://custom-domain.com/sign/test-token-123"
    
    print("\nVerification:")
    print(f"Default URL correct: {default_url == expected_default}")
    print(f"Custom URL correct: {custom_url == expected_custom}")
    
    if default_url == expected_default and custom_url == expected_custom:
        print("\n✅ Signature URL generation is working correctly!")
        return True
    else:
        print("\n❌ Signature URL generation has issues!")
        return False

def test_frontend_route_structure():
    """Test that the frontend route structure is correct"""
    print("\nTesting frontend route structure...")
    
    # Check if the router file has the correct route
    router_file = 'npc-reporting-system/frontend/src/router/index.js'
    
    try:
        with open(router_file, 'r') as f:
            content = f.read()
            
        # Check for the signing route
        if "path: '/sign/:token'" in content and "name: 'SigningPage'" in content:
            print("✅ Frontend signing route is correctly configured")
            return True
        else:
            print("❌ Frontend signing route is missing or misconfigured")
            return False
            
    except FileNotFoundError:
        print(f"❌ Router file not found: {router_file}")
        return False

def test_vue_config():
    """Test that vue.config.js is properly configured for history mode"""
    print("\nTesting Vue.js configuration...")
    
    vue_config_file = 'npc-reporting-system/frontend/vue.config.js'
    
    try:
        with open(vue_config_file, 'r') as f:
            content = f.read()
            
        # Check for historyApiFallback configuration
        if "historyApiFallback" in content:
            print("✅ Vue.js history API fallback is configured")
            return True
        else:
            print("❌ Vue.js history API fallback is not configured")
            return False
            
    except FileNotFoundError:
        print(f"❌ Vue config file not found: {vue_config_file}")
        return False

if __name__ == '__main__':
    print("🔧 Testing Signature Link Fix\n")
    
    url_test = test_signature_url_generation()
    route_test = test_frontend_route_structure()
    vue_test = test_vue_config()
    
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"URL Generation: {'✅ PASS' if url_test else '❌ FAIL'}")
    print(f"Frontend Routes: {'✅ PASS' if route_test else '❌ FAIL'}")
    print(f"Vue.js Config: {'✅ PASS' if vue_test else '❌ FAIL'}")
    
    if all([url_test, route_test, vue_test]):
        print("\n🎉 All tests passed! Signature links should work correctly now.")
        print("\nNext steps:")
        print("1. Restart the Django backend server")
        print("2. Restart the Vue.js frontend server")
        print("3. Test by creating a signature request and clicking the email link")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")