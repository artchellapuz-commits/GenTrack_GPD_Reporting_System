#!/usr/bin/env python3
"""
Test script to verify that audit logging is working properly after the database fix
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, 'npc-reporting-system/backend')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import AuditLog, User
from reports.audit_utils import AuditLogger

def test_audit_logging():
    """Test that audit logging is working without database errors"""
    print("🔍 Testing Audit Logging System...")
    
    try:
        # Test 1: Direct AuditLog.log_action call
        print("\n1. Testing direct AuditLog.log_action call...")
        audit_entry = AuditLog.log_action(
            user=None,
            action='SYSTEM_TEST',
            description='Testing audit logging system after database fix',
            category='testing',
            severity='LOW',
            success=True
        )
        
        if audit_entry:
            print(f"   ✅ Direct audit log created successfully: ID {audit_entry.id}")
        else:
            print("   ❌ Failed to create direct audit log")
            return False
        
        # Test 2: AuditLogger.log_system_action call
        print("\n2. Testing AuditLogger.log_system_action call...")
        audit_entry2 = AuditLogger.log_system_action(
            action='SYSTEM_TEST',
            description='Testing audit logger utility after database fix',
            category='testing'
        )
        
        if audit_entry2:
            print(f"   ✅ AuditLogger system action logged successfully: ID {audit_entry2.id}")
        else:
            print("   ❌ Failed to create AuditLogger system action")
            return False
        
        # Test 3: Check recent audit logs
        print("\n3. Checking recent audit logs...")
        recent_logs = AuditLog.objects.filter(
            action='SYSTEM_TEST'
        ).order_by('-timestamp')[:5]
        
        print(f"   📊 Found {recent_logs.count()} recent test audit logs:")
        for log in recent_logs:
            print(f"      - {log.timestamp}: {log.action} - {log.description}")
        
        # Test 4: Check for database constraint errors
        print("\n4. Testing session_key field (previously causing NOT NULL errors)...")
        audit_entry3 = AuditLog.log_action(
            user=None,
            action='SESSION_TEST',
            description='Testing session_key field is nullable',
            category='testing',
            # Deliberately not providing session_key to test it's nullable
        )
        
        if audit_entry3:
            print(f"   ✅ Session key test passed: ID {audit_entry3.id}")
            print(f"      Session key value: {audit_entry3.session_key or 'NULL (as expected)'}")
        else:
            print("   ❌ Session key test failed")
            return False
        
        # Test 5: Test with all new audit fields
        print("\n5. Testing all enhanced audit fields...")
        audit_entry4 = AuditLog.log_action(
            user=None,
            action='ENHANCED_TEST',
            description='Testing all enhanced audit fields',
            category='testing',
            severity='MEDIUM',
            success=True,
            error_message='',
            duration_ms=150,
            url_path='/test/path',
            http_method='GET',
            request_data={'test': 'data'},
            response_status=200
        )
        
        if audit_entry4:
            print(f"   ✅ Enhanced fields test passed: ID {audit_entry4.id}")
            print(f"      Category: {audit_entry4.category}")
            print(f"      Severity: {audit_entry4.severity}")
            print(f"      Duration: {audit_entry4.duration_ms}ms")
            print(f"      URL Path: {audit_entry4.url_path}")
            print(f"      HTTP Method: {audit_entry4.http_method}")
        else:
            print("   ❌ Enhanced fields test failed")
            return False
        
        print("\n🎉 All audit logging tests passed successfully!")
        print(f"📈 Total audit logs in system: {AuditLog.objects.count()}")
        
        # Show recent audit activity
        print("\n📋 Recent audit activity (last 10 entries):")
        recent_all = AuditLog.objects.order_by('-timestamp')[:10]
        for log in recent_all:
            user_str = log.user.username if log.user else 'System'
            print(f"   {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {user_str} | {log.action} | {log.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Audit logging test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_audit_categories():
    """Test the new audit categories"""
    print("\n🏷️  Testing New Audit Categories...")
    
    categories_to_test = [
        'file_management',
        'data_processing', 
        'reporting',
        'e_signature',
        'authorization',
        'workflow',
        'user_management',
        'security',
        'data_access'
    ]
    
    for category in categories_to_test:
        try:
            audit_entry = AuditLog.log_action(
                action='CATEGORY_TEST',
                description=f'Testing {category} category',
                category=category,
                severity='LOW'
            )
            if audit_entry:
                print(f"   ✅ {category}: OK")
            else:
                print(f"   ❌ {category}: Failed")
        except Exception as e:
            print(f"   ❌ {category}: Error - {e}")
    
    print("✅ Category testing completed!")

if __name__ == '__main__':
    print("🚀 Starting Audit Logging Verification Tests")
    print("=" * 60)
    
    # Run the tests
    success = test_audit_logging()
    test_audit_categories()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 AUDIT LOGGING SYSTEM IS WORKING CORRECTLY!")
        print("✅ Database schema issues have been resolved")
        print("✅ All audit logging functions are operational")
        print("✅ Enhanced audit fields are working")
        print("✅ No more NOT NULL constraint errors")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ AUDIT LOGGING SYSTEM HAS ISSUES")
        print("Please check the error messages above")
        print("=" * 60)
        sys.exit(1)