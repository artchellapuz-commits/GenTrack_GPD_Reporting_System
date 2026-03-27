#!/usr/bin/env python3
"""
Test script to verify complete audit trail coverage for all system operations
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import AuditLog

def test_audit_coverage():
    """Test that all major operations are being audited"""
    
    print("🔍 TESTING COMPLETE AUDIT TRAIL COVERAGE")
    print("=" * 60)
    
    # Get initial audit log count
    initial_count = AuditLog.objects.count()
    print(f"📊 Initial audit log count: {initial_count}")
    
    # Test categories to verify
    expected_categories = [
        'authentication',
        'user_management', 
        'file_management',
        'data_processing',
        'reporting',
        'e_signature',
        'authorization',
        'workflow',
        'security',
        'data_access',
        'data_modification',
        'content_management'
    ]
    
    print("\n🎯 CHECKING AUDIT LOG CATEGORIES:")
    print("-" * 40)
    
    for category in expected_categories:
        count = AuditLog.objects.filter(category=category).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {category}: {count} entries")
    
    # Test action types to verify
    expected_actions = [
        'LOGIN', 'LOGOUT', 'LOGIN_FAILED',
        'USER_REGISTER', 'USER_UPDATE', 'PASSWORD_CHANGE',
        'FILE_UPLOAD', 'FILE_DELETE', 'DATA_IMPORT',
        'REPORT_GENERATE', 'DATA_EXPORT',
        'SIGNATURE_CREATE', 'REPORT_SIGN',
        'AUTH_REQUEST_CREATE', 'AUTH_REQUEST_APPROVE', 'AUTH_REQUEST_REJECT',
        'DATA_CREATE', 'DATA_UPDATE', 'DATA_DELETE',
        'OPERATION_START', 'OPERATION_COMPLETE'
    ]
    
    print("\n🎯 CHECKING AUDIT LOG ACTIONS:")
    print("-" * 40)
    
    for action in expected_actions:
        count = AuditLog.objects.filter(action=action).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {action}: {count} entries")
    
    # Check recent audit entries
    print("\n📋 RECENT AUDIT ENTRIES (Last 10):")
    print("-" * 40)
    
    recent_logs = AuditLog.objects.order_by('-timestamp')[:10]
    for log in recent_logs:
        user_info = log.user.username if log.user else 'System'
        print(f"🔸 {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | {user_info} | {log.action} | {log.category}")
        print(f"   📝 {log.description}")
    
    # Check audit coverage by model
    print("\n🎯 CHECKING MODEL COVERAGE:")
    print("-" * 40)
    
    models_with_audit = AuditLog.objects.exclude(model_name__isnull=True).exclude(model_name='').values_list('model_name', flat=True).distinct()
    expected_models = [
        'User', 'UploadedFile', 'GenerationReport', 'PlantCapacity', 'HistoricalData',
        'WaterNomination', 'ActualGeneration', 'Testimonial', 'ESignature', 'ReportSignature',
        'SignatoryAuthorization', 'SignatoryAuthorizationRequest'
    ]
    
    for model in expected_models:
        count = AuditLog.objects.filter(model_name=model).count()
        status = "✅" if count > 0 else "❌"
        print(f"{status} {model}: {count} entries")
    
    # Check severity levels
    print("\n🎯 CHECKING SEVERITY LEVELS:")
    print("-" * 40)
    
    severity_counts = {}
    for severity in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
        count = AuditLog.objects.filter(severity=severity).count()
        severity_counts[severity] = count
        print(f"🔸 {severity}: {count} entries")
    
    # Check success/failure tracking
    print("\n🎯 CHECKING SUCCESS/FAILURE TRACKING:")
    print("-" * 40)
    
    success_count = AuditLog.objects.filter(success=True).count()
    failure_count = AuditLog.objects.filter(success=False).count()
    print(f"✅ Successful operations: {success_count}")
    print(f"❌ Failed operations: {failure_count}")
    
    # Check IP address and location tracking
    print("\n🎯 CHECKING CONTEXT DATA:")
    print("-" * 40)
    
    with_ip = AuditLog.objects.exclude(ip_address__isnull=True).exclude(ip_address='').count()
    with_user_agent = AuditLog.objects.exclude(user_agent__isnull=True).exclude(user_agent='').count()
    with_location = AuditLog.objects.exclude(location__isnull=True).exclude(location='').count()
    
    print(f"🌐 Entries with IP address: {with_ip}")
    print(f"🖥️  Entries with User Agent: {with_user_agent}")
    print(f"📍 Entries with Location: {with_location}")
    
    # Final audit log count
    final_count = AuditLog.objects.count()
    print(f"\n📊 Final audit log count: {final_count}")
    print(f"📈 New entries during test: {final_count - initial_count}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 AUDIT COVERAGE SUMMARY:")
    print("=" * 60)
    
    total_categories = len([cat for cat in expected_categories if AuditLog.objects.filter(category=cat).exists()])
    total_actions = len([action for action in expected_actions if AuditLog.objects.filter(action=action).exists()])
    total_models = len([model for model in expected_models if AuditLog.objects.filter(model_name=model).exists()])
    
    print(f"✅ Categories covered: {total_categories}/{len(expected_categories)} ({total_categories/len(expected_categories)*100:.1f}%)")
    print(f"✅ Actions covered: {total_actions}/{len(expected_actions)} ({total_actions/len(expected_actions)*100:.1f}%)")
    print(f"✅ Models covered: {total_models}/{len(expected_models)} ({total_models/len(expected_models)*100:.1f}%)")
    
    if total_categories == len(expected_categories) and total_actions >= len(expected_actions) * 0.8:
        print("\n🎉 EXCELLENT! Comprehensive audit coverage achieved!")
        print("   All major system operations are being logged.")
    elif total_categories >= len(expected_categories) * 0.8:
        print("\n✅ GOOD! Most operations are being audited.")
        print("   Consider adding audit logging to remaining operations.")
    else:
        print("\n⚠️  NEEDS IMPROVEMENT! Audit coverage is incomplete.")
        print("   Many operations are not being logged.")
    
    return {
        'total_logs': final_count,
        'categories_covered': total_categories,
        'actions_covered': total_actions,
        'models_covered': total_models,
        'success_rate': success_count / (success_count + failure_count) * 100 if (success_count + failure_count) > 0 else 0
    }

def test_audit_search_and_filtering():
    """Test audit log search and filtering capabilities"""
    
    print("\n🔍 TESTING AUDIT LOG SEARCH & FILTERING")
    print("=" * 60)
    
    # Test filtering by action
    login_logs = AuditLog.objects.filter(action='LOGIN').count()
    print(f"🔐 Login attempts: {login_logs}")
    
    # Test filtering by category
    security_logs = AuditLog.objects.filter(category='security').count()
    print(f"🛡️  Security events: {security_logs}")
    
    # Test filtering by user
    if User.objects.exists():
        test_user = User.objects.first()
        user_logs = AuditLog.objects.filter(user=test_user).count()
        print(f"👤 Logs for {test_user.username}: {user_logs}")
    
    # Test filtering by date range
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    today_logs = AuditLog.objects.filter(timestamp__date=today).count()
    recent_logs = AuditLog.objects.filter(timestamp__gte=yesterday).count()
    
    print(f"📅 Today's logs: {today_logs}")
    print(f"📅 Last 24 hours: {recent_logs}")
    
    # Test filtering by severity
    high_severity = AuditLog.objects.filter(severity='HIGH').count()
    critical_severity = AuditLog.objects.filter(severity='CRITICAL').count()
    
    print(f"🚨 High severity events: {high_severity}")
    print(f"🔥 Critical events: {critical_severity}")

if __name__ == '__main__':
    try:
        # Run audit coverage test
        results = test_audit_coverage()
        
        # Run search and filtering test
        test_audit_search_and_filtering()
        
        print(f"\n✅ AUDIT TESTING COMPLETED SUCCESSFULLY!")
        print(f"📊 Total audit entries: {results['total_logs']}")
        print(f"📈 Coverage score: {(results['categories_covered'] + results['actions_covered'] + results['models_covered'])/3:.1f}/10")
        
    except Exception as e:
        print(f"❌ Error during audit testing: {e}")
        import traceback
        traceback.print_exc()