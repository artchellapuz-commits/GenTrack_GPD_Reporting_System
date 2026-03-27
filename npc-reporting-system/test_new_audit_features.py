#!/usr/bin/env python3
"""
Test script to trigger new audit logging features
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import AuditLog, Plant, UploadedFile, WaterNomination, Testimonial
from reports.audit_utils import AuditLogger, audit_file_upload, audit_report_generation

def test_new_audit_features():
    """Test the new comprehensive audit logging features"""
    
    print("🧪 TESTING NEW AUDIT LOGGING FEATURES")
    print("=" * 60)
    
    # Get or create a test user
    test_user, created = User.objects.get_or_create(
        username='audit_test_user',
        defaults={
            'email': 'audit_test@example.com',
            'first_name': 'Audit',
            'last_name': 'Test'
        }
    )
    
    if created:
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Using existing test user: {test_user.username}")
    
    initial_count = AuditLog.objects.count()
    print(f"📊 Initial audit log count: {initial_count}")
    
    # Test 1: User Action Logging
    print("\n🧪 Test 1: User Action Logging")
    AuditLogger.log_user_action(
        user=test_user,
        action='TEST_ACTION',
        description='Testing user action logging',
        category='testing',
        severity='LOW'
    )
    print("✅ Logged user action")
    
    # Test 2: Security Event Logging
    print("\n🧪 Test 2: Security Event Logging")
    AuditLogger.log_security_event(
        user=test_user,
        action='TEST_SECURITY',
        description='Testing security event logging',
        severity='HIGH'
    )
    print("✅ Logged security event")
    
    # Test 3: File Operation Logging
    print("\n🧪 Test 3: File Operation Logging")
    AuditLogger.log_file_operation(
        user=test_user,
        action='FILE_TEST',
        filename='test_file.xlsx',
        description='Testing file operation logging'
    )
    print("✅ Logged file operation")
    
    # Test 4: Report Operation Logging
    print("\n🧪 Test 4: Report Operation Logging")
    AuditLogger.log_report_operation(
        user=test_user,
        action='REPORT_TEST',
        report_info={'date': '2026-03-18', 'type': 'PSR'}
    )
    print("✅ Logged report operation")
    
    # Test 5: Signature Operation Logging
    print("\n🧪 Test 5: Signature Operation Logging")
    AuditLogger.log_signature_operation(
        user=test_user,
        action='SIGNATURE_TEST',
        signatory_name='Test Signatory'
    )
    print("✅ Logged signature operation")
    
    # Test 6: Data Access Logging
    print("\n🧪 Test 6: Data Access Logging")
    AuditLogger.log_data_access(
        user=test_user,
        model_name='TestModel',
        object_id=123,
        action='DATA_VIEW',
        description='Testing data access logging'
    )
    print("✅ Logged data access")
    
    # Test 7: System Action Logging
    print("\n🧪 Test 7: System Action Logging")
    AuditLogger.log_system_action(
        action='SYSTEM_TEST',
        description='Testing system action logging'
    )
    print("✅ Logged system action")
    
    # Test 8: Convenience Function - File Upload
    print("\n🧪 Test 8: File Upload Audit")
    audit_file_upload(
        user=test_user,
        filename='test_upload.xlsx',
        file_size=1024
    )
    print("✅ Logged file upload")
    
    # Test 9: Convenience Function - Report Generation
    print("\n🧪 Test 9: Report Generation Audit")
    audit_report_generation(
        user=test_user,
        report_date='2026-03-18',
        report_type='PSR'
    )
    print("✅ Logged report generation")
    
    # Check results
    final_count = AuditLog.objects.count()
    new_entries = final_count - initial_count
    
    print(f"\n📊 Final audit log count: {final_count}")
    print(f"📈 New entries created: {new_entries}")
    
    # Verify categories
    print("\n🎯 VERIFYING NEW CATEGORIES:")
    print("-" * 40)
    
    categories = ['testing', 'security', 'file_operation', 'reporting', 'e_signature', 'data_access', 'system']
    for category in categories:
        count = AuditLog.objects.filter(category=category).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {category}: {count} entries")
    
    # Verify actions
    print("\n🎯 VERIFYING NEW ACTIONS:")
    print("-" * 40)
    
    actions = ['TEST_ACTION', 'TEST_SECURITY', 'FILE_TEST', 'REPORT_TEST', 'SIGNATURE_TEST', 'DATA_VIEW', 'SYSTEM_TEST', 'FILE_UPLOAD', 'REPORT_GENERATE']
    for action in actions:
        count = AuditLog.objects.filter(action=action).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {action}: {count} entries")
    
    # Verify severity levels
    print("\n🎯 VERIFYING SEVERITY LEVELS:")
    print("-" * 40)
    
    for severity in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
        count = AuditLog.objects.filter(severity=severity).count()
        print(f"🔸 {severity}: {count} entries")
    
    # Show recent test entries
    print("\n📋 RECENT TEST ENTRIES:")
    print("-" * 40)
    
    test_logs = AuditLog.objects.filter(user=test_user).order_by('-timestamp')[:10]
    for log in test_logs:
        print(f"🔸 {log.timestamp.strftime('%H:%M:%S')} | {log.action} | {log.category} | {log.severity}")
        print(f"   📝 {log.description}")
    
    print(f"\n✅ NEW AUDIT FEATURES TEST COMPLETED!")
    print(f"📊 Successfully created {new_entries} new audit entries")
    
    return new_entries

if __name__ == '__main__':
    try:
        new_entries = test_new_audit_features()
        
        if new_entries >= 9:
            print(f"\n🎉 SUCCESS! All new audit logging features are working correctly!")
        else:
            print(f"\n⚠️  WARNING! Expected 9 entries, but only created {new_entries}")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()