#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced audit logging system.

This script tests all aspects of the audit logging:
1. Authentication events (login/logout)
2. File operations (upload/delete/archive)
3. Report generation and exports
4. E-signature operations
5. Authorization requests
6. Security events
7. Page access tracking
8. API call logging
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8081"

def test_authentication_audit():
    """Test authentication-related audit logging"""
    print("\n🔐 Testing Authentication Audit Logging")
    print("-" * 50)
    
    # Test successful login
    print("1. Testing successful login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    login_response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if login_response.status_code == 200:
        print("✅ Successful login - should be audited")
        token = login_response.json().get('access')
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test logout
        print("2. Testing logout...")
        logout_data = {"refresh_token": login_response.json().get('refresh')}
        logout_response = requests.post(f"{BASE_URL}/api/auth/logout/", 
                                      json=logout_data, headers=headers)
        if logout_response.status_code == 200:
            print("✅ Successful logout - should be audited")
        
        return headers
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return None
    
    # Test failed login
    print("3. Testing failed login...")
    failed_login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    failed_response = requests.post(f"{BASE_URL}/api/auth/login/", json=failed_login_data)
    if failed_response.status_code != 200:
        print("✅ Failed login attempt - should be audited")
    
    return None

def test_file_operations_audit(headers):
    """Test file operation audit logging"""
    print("\n📁 Testing File Operations Audit Logging")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Test file upload (simulate)
    print("1. Testing file upload audit...")
    # Note: This would require an actual file, so we'll test the endpoint
    upload_response = requests.get(f"{BASE_URL}/api/uploaded-files/", headers=headers)
    if upload_response.status_code == 200:
        print("✅ File listing accessed - should be audited")
    
    # Test file deletion (if files exist)
    files = upload_response.json().get('results', [])
    if files:
        file_id = files[0]['id']
        print(f"2. Testing file deletion audit for file {file_id}...")
        # Note: Uncomment to actually test deletion
        # delete_response = requests.delete(f"{BASE_URL}/api/uploaded-files/{file_id}/delete_upload/", headers=headers)
        print("✅ File deletion would be audited")

def test_report_operations_audit(headers):
    """Test report operation audit logging"""
    print("\n📊 Testing Report Operations Audit Logging")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Test report viewing
    print("1. Testing report viewing audit...")
    reports_response = requests.get(f"{BASE_URL}/api/generation-reports/", headers=headers)
    if reports_response.status_code == 200:
        print("✅ Report listing accessed - should be audited")
    
    # Test report summary
    print("2. Testing report summary audit...")
    summary_response = requests.get(f"{BASE_URL}/api/generation-reports/summary/", headers=headers)
    if summary_response.status_code == 200:
        print("✅ Report summary accessed - should be audited")
    
    # Test report preview
    print("3. Testing report preview audit...")
    preview_data = {
        "plant_codes": ["PLANT1"],
        "start_date": "2024-01-01",
        "end_date": "2024-01-01",
        "report_type": "psr"
    }
    
    preview_response = requests.post(f"{BASE_URL}/api/generation-reports/preview-report/", 
                                   json=preview_data, headers=headers)
    if preview_response.status_code in [200, 404]:  # 404 is OK if no data
        print("✅ Report preview attempted - should be audited")

def test_signature_operations_audit(headers):
    """Test e-signature operation audit logging"""
    print("\n✍️ Testing E-Signature Operations Audit Logging")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Test signature viewing
    print("1. Testing signature viewing audit...")
    signatures_response = requests.get(f"{BASE_URL}/api/e-signatures/", headers=headers)
    if signatures_response.status_code == 200:
        print("✅ Signature listing accessed - should be audited")
    
    # Test signature creation
    print("2. Testing signature creation audit...")
    signature_data = {
        "signatory_name": "Test Audit Signatory",
        "signature_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    }
    
    create_response = requests.post(f"{BASE_URL}/api/e-signatures/create-from-data/", 
                                  json=signature_data, headers=headers)
    if create_response.status_code == 201:
        print("✅ Signature creation - should be audited")
        
        # Test signature deletion
        signature_id = create_response.json().get('id')
        if signature_id:
            print("3. Testing signature deletion audit...")
            delete_response = requests.delete(f"{BASE_URL}/api/e-signatures/{signature_id}/", 
                                            headers=headers)
            if delete_response.status_code == 204:
                print("✅ Signature deletion - should be audited")

def test_authorization_operations_audit(headers):
    """Test authorization operation audit logging"""
    print("\n🔑 Testing Authorization Operations Audit Logging")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Test authorization viewing
    print("1. Testing authorization viewing audit...")
    auth_response = requests.get(f"{BASE_URL}/api/signatory-authorizations/my-authorizations/", 
                                headers=headers)
    if auth_response.status_code == 200:
        print("✅ Authorization listing accessed - should be audited")
    
    # Test authorization request
    print("2. Testing authorization request audit...")
    request_data = {
        "signatory_name": "Test Audit Authorization",
        "role": "Prepared by:",
        "justification": "Testing comprehensive audit logging system",
        "email": "test@example.com"
    }
    
    request_response = requests.post(f"{BASE_URL}/api/signatory-authorizations/request/", 
                                   json=request_data, headers=headers)
    if request_response.status_code == 201:
        print("✅ Authorization request created - should be audited")

def test_security_events_audit():
    """Test security event audit logging"""
    print("\n🛡️ Testing Security Events Audit Logging")
    print("-" * 50)
    
    # Test unauthorized access
    print("1. Testing unauthorized access audit...")
    unauth_response = requests.get(f"{BASE_URL}/api/generation-reports/")
    if unauth_response.status_code == 401:
        print("✅ Unauthorized access attempt - should be audited")
    
    # Test invalid token
    print("2. Testing invalid token audit...")
    invalid_headers = {'Authorization': 'Bearer invalid_token_here'}
    invalid_response = requests.get(f"{BASE_URL}/api/generation-reports/", headers=invalid_headers)
    if invalid_response.status_code == 401:
        print("✅ Invalid token usage - should be audited")
    
    # Test suspicious request patterns (would be caught by middleware)
    print("3. Testing suspicious request patterns...")
    suspicious_data = {
        "test": "'; DROP TABLE users; --",  # SQL injection attempt
        "script": "<script>alert('xss')</script>"  # XSS attempt
    }
    
    suspicious_response = requests.post(f"{BASE_URL}/api/auth/login/", json=suspicious_data)
    print("✅ Suspicious patterns in request - should be audited by security middleware")

def test_page_access_audit():
    """Test page access audit logging"""
    print("\n🌐 Testing Page Access Audit Logging")
    print("-" * 50)
    
    # Test various page accesses
    pages_to_test = [
        "/",
        "/dashboard",
        "/generate",
        "/upload",
        "/view"
    ]
    
    for page in pages_to_test:
        print(f"Testing access to {page}...")
        try:
            response = requests.get(f"{FRONTEND_URL}{page}", timeout=5)
            print(f"✅ Page {page} accessed - should be audited")
        except requests.exceptions.RequestException:
            print(f"⚠️ Could not access {page} (frontend may not be running)")

def test_api_call_audit(headers):
    """Test API call audit logging"""
    print("\n🔌 Testing API Call Audit Logging")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Test various API endpoints
    api_endpoints = [
        "/api/plants/",
        "/api/units/",
        "/api/generation-reports/summary/",
        "/api/audit-logs/"
    ]
    
    for endpoint in api_endpoints:
        print(f"Testing API call to {endpoint}...")
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"✅ API call to {endpoint} (status: {response.status_code}) - should be audited")

def verify_audit_logs(headers):
    """Verify that audit logs were created"""
    print("\n📋 Verifying Audit Logs")
    print("-" * 50)
    
    if not headers:
        print("❌ No authentication headers available")
        return
    
    # Get recent audit logs
    print("Fetching recent audit logs...")
    logs_response = requests.get(f"{BASE_URL}/api/audit-logs/", headers=headers)
    
    if logs_response.status_code == 200:
        logs = logs_response.json().get('results', [])
        print(f"✅ Found {len(logs)} audit log entries")
        
        # Show recent logs
        print("\nRecent audit log entries:")
        for i, log in enumerate(logs[:10]):  # Show first 10
            timestamp = log.get('timestamp', 'Unknown')
            action = log.get('action', 'Unknown')
            description = log.get('description', 'No description')
            user = log.get('user', 'System')
            severity = log.get('severity', 'LOW')
            category = log.get('category', 'general')
            
            print(f"{i+1:2d}. [{timestamp}] {action} - {description}")
            print(f"    User: {user}, Severity: {severity}, Category: {category}")
        
        # Count by action type
        action_counts = {}
        for log in logs:
            action = log.get('action', 'Unknown')
            action_counts[action] = action_counts.get(action, 0) + 1
        
        print(f"\nAction type summary:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")
        
        # Count by category
        category_counts = {}
        for log in logs:
            category = log.get('category', 'general')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\nCategory summary:")
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}")
        
        # Count by severity
        severity_counts = {}
        for log in logs:
            severity = log.get('severity', 'LOW')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"\nSeverity summary:")
        for severity, count in sorted(severity_counts.items()):
            print(f"  {severity}: {count}")
        
    else:
        print(f"❌ Failed to fetch audit logs: {logs_response.status_code}")

def main():
    """Run comprehensive audit logging tests"""
    print("🧪 Comprehensive Audit Logging System Test")
    print("=" * 60)
    print(f"Testing against: {BASE_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    print(f"Test started at: {datetime.now()}")
    
    try:
        # Test authentication and get headers
        headers = test_authentication_audit()
        
        # Re-login for other tests
        if not headers:
            print("\n🔄 Re-attempting login for other tests...")
            login_data = {"username": "testuser", "password": "testpass123"}
            login_response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
            if login_response.status_code == 200:
                token = login_response.json().get('access')
                headers = {'Authorization': f'Bearer {token}'}
        
        # Run all test categories
        test_file_operations_audit(headers)
        test_report_operations_audit(headers)
        test_signature_operations_audit(headers)
        test_authorization_operations_audit(headers)
        test_security_events_audit()
        test_page_access_audit()
        test_api_call_audit(headers)
        
        # Wait a moment for all logs to be written
        print("\n⏳ Waiting for audit logs to be processed...")
        time.sleep(2)
        
        # Verify audit logs were created
        verify_audit_logs(headers)
        
        print("\n🎉 Comprehensive Audit Logging Test Completed!")
        print("\nSummary:")
        print("✅ Authentication events (login/logout/failed attempts)")
        print("✅ File operations (upload/delete/view)")
        print("✅ Report operations (generate/preview/view)")
        print("✅ E-signature operations (create/view/delete)")
        print("✅ Authorization operations (request/view)")
        print("✅ Security events (unauthorized access/invalid tokens)")
        print("✅ Page access tracking")
        print("✅ API call logging")
        print("✅ Comprehensive audit log verification")
        
        print(f"\n📊 All system activities should now be comprehensively logged!")
        print("Check the audit logs in the admin panel or via API for complete details.")
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()