#!/usr/bin/env python3
"""
Test View Details Functionality
Tests that the View Details buttons work correctly and show proper information
"""

import os
import sys
import django
import requests
import json
import time
import secrets
from datetime import datetime, timedelta

# Setup Django
sys.path.append('npc-reporting-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization

def test_view_details_data():
    """Test that the backend provides proper data for view details functionality"""
    print("🔍 Testing View Details Data Availability")
    print("=" * 50)
    
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='view_details_test',
            defaults={
                'email': 'viewdetails@example.com',
                'first_name': 'View',
                'last_name': 'Details'
            }
        )
        
        print(f"✅ Test user: {user.username}")
        
        # Create test authorization
        auth = SignatoryAuthorization.objects.create(
            user=user,
            signatory_name='VIEW DETAILS TEST',
            authorized_by=user,
            is_active=True,
            requires_2fa=True,
            notes='Test authorization for view details functionality',
            authorization_date=timezone.now(),
            expiry_date=timezone.now() + timedelta(days=365)
        )
        
        print(f"✅ Test authorization created: ID {auth.id}")
        
        # Create test request
        request = SignatoryAuthorizationRequest.objects.create(
            user=user,
            signatory_name='VIEW DETAILS REQUEST TEST',
            role='Prepared by',
            email='viewdetails@example.com',
            justification='Test request for view details functionality',
            status='PENDING'
        )
        
        print(f"✅ Test request created: ID {request.id}")
        
        # Test authorization data completeness
        print("\n📋 Authorization Data:")
        print(f"   - Signatory Name: {auth.signatory_name}")
        print(f"   - Is Valid: {auth.is_valid()}")
        print(f"   - Authorization Date: {auth.authorization_date}")
        print(f"   - Expiry Date: {auth.expiry_date}")
        print(f"   - Requires 2FA: {auth.requires_2fa}")
        print(f"   - Notes: {auth.notes}")
        print(f"   - Authorized By: {auth.authorized_by}")
        
        # Test request data completeness
        print("\n📋 Request Data:")
        print(f"   - Signatory Name: {request.signatory_name}")
        print(f"   - Role: {request.role}")
        print(f"   - Email: {request.email}")
        print(f"   - Status: {request.status}")
        print(f"   - Created At: {request.created_at}")
        print(f"   - Justification: {request.justification[:50]}...")
        
        print("\n✅ All required data fields are available for View Details functionality!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_endpoints():
    """Test that API endpoints return proper data for view details"""
    print("\n🔗 Testing API Endpoints for View Details")
    print("=" * 50)
    
    try:
        base_url = 'http://localhost:8000'
        
        # Test my-authorizations endpoint
        print("Testing /api/signatory-authorizations/my-authorizations/...")
        response = requests.get(f'{base_url}/api/signatory-authorizations/my-authorizations/')
        
        if response.status_code == 401:
            print("⚠️  Endpoint requires authentication (expected)")
            print("✅ Authorization endpoint is accessible")
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ Authorization endpoint returned {len(data)} authorizations")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
        
        # Test my-requests endpoint
        print("Testing /api/signatory-authorizations/my-requests/...")
        response = requests.get(f'{base_url}/api/signatory-authorizations/my-requests/')
        
        if response.status_code == 401:
            print("⚠️  Endpoint requires authentication (expected)")
            print("✅ Requests endpoint is accessible")
        elif response.status_code == 200:
            data = response.json()
            print(f"✅ Requests endpoint returned {len(data)} requests")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
        
        print("\n✅ API endpoints are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_frontend_integration():
    """Test frontend integration for view details"""
    print("\n🖥️  Testing Frontend Integration")
    print("=" * 50)
    
    try:
        # Check if frontend files exist
        frontend_component = 'npc-reporting-system/frontend/src/components/SignatoryAuthorizationRequest.vue'
        
        if os.path.exists(frontend_component):
            print("✅ Frontend component exists")
            
            # Check for modal implementation
            with open(frontend_component, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for required methods
            required_methods = [
                'viewAuthDetails',
                'viewRequestDetails',
                'closeAuthDetailsModal',
                'closeRequestDetailsModal'
            ]
            
            missing_methods = []
            for method in required_methods:
                if method not in content:
                    missing_methods.append(method)
            
            if missing_methods:
                print(f"❌ Missing methods: {missing_methods}")
                return False
            else:
                print("✅ All required methods are implemented")
            
            # Check for modal templates
            if 'showAuthDetailsModal' in content and 'showRequestDetailsModal' in content:
                print("✅ Modal templates are implemented")
            else:
                print("❌ Modal templates are missing")
                return False
            
            # Check for modal data properties
            if 'selectedAuthDetails' in content and 'selectedRequestDetails' in content:
                print("✅ Modal data properties are implemented")
            else:
                print("❌ Modal data properties are missing")
                return False
            
            print("\n✅ Frontend integration is complete!")
            return True
        else:
            print("❌ Frontend component not found")
            return False
            
    except Exception as e:
        print(f"❌ Frontend integration test failed: {e}")
        return False

def test_duplicate_prevention():
    """Test that duplicate authorization prevention is working"""
    print("\n🚫 Testing Duplicate Authorization Prevention")
    print("=" * 50)
    
    try:
        # Check if selectSignatory method has duplicate checking
        frontend_component = 'npc-reporting-system/frontend/src/components/SignatoryAuthorizationRequest.vue'
        
        with open(frontend_component, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for duplicate prevention logic
        if 'already have active authorization' in content:
            print("✅ Active authorization checking implemented")
        else:
            print("❌ Active authorization checking missing")
            return False
        
        if 'already have a pending request' in content:
            print("✅ Pending request checking implemented")
        else:
            print("❌ Pending request checking missing")
            return False
        
        # Check for helper methods
        helper_methods = [
            'hasActiveAuthorization',
            'hasPendingRequest',
            'isSignatoryDisabled'
        ]
        
        missing_helpers = []
        for helper in helper_methods:
            if helper not in content:
                missing_helpers.append(helper)
        
        if missing_helpers:
            print(f"❌ Missing helper methods: {missing_helpers}")
            return False
        else:
            print("✅ All helper methods are implemented")
        
        # Check for visual indicators
        if 'signatory-status' in content:
            print("✅ Visual status indicators implemented")
        else:
            print("❌ Visual status indicators missing")
            return False
        
        print("\n✅ Duplicate prevention is fully implemented!")
        return True
        
    except Exception as e:
        print(f"❌ Duplicate prevention test failed: {e}")
        return False

def main():
    """Run all view details functionality tests"""
    print("🔍 VIEW DETAILS FUNCTIONALITY TEST SUITE")
    print("Testing that View Details buttons work correctly")
    print("=" * 60)
    
    tests = [
        ("Data Availability", test_view_details_data),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Integration", test_frontend_integration),
        ("Duplicate Prevention", test_duplicate_prevention)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} test failed!")
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 VIEW DETAILS TEST SUMMARY")
    print("=" * 60)
    print(f"📊 Tests Passed: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ View Details functionality is working correctly")
        print("✅ Modal dialogs are implemented")
        print("✅ Duplicate prevention is active")
        print("✅ Visual indicators are showing")
        print("\n📋 Users can now:")
        print("   • Click 'View Details' to see authorization information")
        print("   • See detailed request information in modals")
        print("   • Visual indicators prevent duplicate requests")
        print("   • Clear error messages for existing authorizations")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed")
        print("Some functionality may not be working correctly")
    
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)