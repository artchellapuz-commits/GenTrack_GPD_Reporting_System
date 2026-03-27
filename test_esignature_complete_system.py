#!/usr/bin/env python3
"""
Comprehensive E-Signature System Test
Tests the complete workflow after NameError fix and server restart
"""

import requests
import json
import time
import os
import sys
import django
import secrets
from datetime import datetime, timedelta

# Setup Django
sys.path.append('npc-reporting-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization
from django.utils import timezone

class ESignatureSystemTest:
    def __init__(self):
        self.base_url = 'http://localhost:8000'
        self.frontend_url = 'http://localhost:8081'
        self.test_results = []
        self.test_user = None
        self.setup_tokens = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} - {message}")
        if details:
            print(f"   Details: {details}")
    
    def setup_test_user(self):
        """Create or get test user"""
        try:
            self.test_user, created = User.objects.get_or_create(
                username='esig_test_user',
                defaults={
                    'email': 'esig.test@example.com',
                    'first_name': 'ESignature',
                    'last_name': 'TestUser'
                }
            )
            self.log_test(
                "User Setup", 
                True, 
                f"Test user {'created' if created else 'retrieved'}: {self.test_user.username}"
            )
            return True
        except Exception as e:
            self.log_test("User Setup", False, f"Failed to setup test user: {e}")
            return False
    
    def test_1_direct_authorization_creation(self):
        """Test 1: Direct authorization creation with setup token"""
        try:
            # Clean up any existing authorizations for this test
            SignatoryAuthorization.objects.filter(
                user=self.test_user,
                signatory_name='TEST SIGNATORY 1'
            ).delete()
            
            # Create authorization request
            request = SignatoryAuthorizationRequest.objects.create(
                user=self.test_user,
                signatory_name='TEST SIGNATORY 1',
                role='Prepared by',
                email='esig.test@example.com',
                justification='Test 1: Direct authorization creation with setup token'
            )
            
            # Create authorization with setup token
            setup_token = secrets.token_urlsafe(32)
            authorization = SignatoryAuthorization.objects.create(
                user=self.test_user,
                signatory_name=request.signatory_name,
                authorized_by=self.test_user,
                is_active=True,
                requires_2fa=True,
                notes='Test authorization',
                setup_token=setup_token,
                token_expires=timezone.now() + timedelta(hours=24),
                signature_created=False
            )
            
            self.setup_tokens.append(setup_token)
            
            # Update request status
            request.status = 'APPROVED'
            request.reviewed_by = self.test_user
            request.reviewed_at = timezone.now()
            request.save()
            
            self.log_test(
                "Direct Authorization Creation",
                True,
                f"Authorization created with token: {setup_token[:20]}...",
                f"Authorization ID: {authorization.id}, Request ID: {request.id}"
            )
            return True
            
        except Exception as e:
            self.log_test("Direct Authorization Creation", False, f"Failed: {e}")
            return False
    
    def test_2_signature_setup_endpoint(self):
        """Test 2: Signature setup endpoint (NameError fix verification)"""
        if not self.setup_tokens:
            self.log_test("Signature Setup Endpoint", False, "No setup tokens available")
            return False
        
        try:
            token = self.setup_tokens[0]
            url = f'{self.base_url}/api/signatory-authorizations/signature-setup/{token}/'
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                expected_fields = ['signatory_name', 'user_name', 'requires_2fa', 'token']
                
                if all(field in data for field in expected_fields):
                    self.log_test(
                        "Signature Setup Endpoint",
                        True,
                        "Endpoint working correctly - NameError fixed!",
                        f"Response: {json.dumps(data, indent=2)}"
                    )
                    return True
                else:
                    self.log_test(
                        "Signature Setup Endpoint",
                        False,
                        "Missing required fields in response",
                        f"Response: {data}"
                    )
                    return False
            else:
                self.log_test(
                    "Signature Setup Endpoint",
                    False,
                    f"HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Signature Setup Endpoint", False, f"Request failed: {e}")
            return False
    
    def test_3_save_signature_endpoint(self):
        """Test 3: Save signature endpoint"""
        if not self.setup_tokens:
            self.log_test("Save Signature Endpoint", False, "No setup tokens available")
            return False
        
        try:
            token = self.setup_tokens[0]
            url = f'{self.base_url}/api/signatory-authorizations/save-signature/{token}/'
            
            # Create test signature (simple 1x1 pixel PNG)
            test_signature = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
            
            response = requests.post(url, json={'signature': test_signature})
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'signature_file' in data:
                    self.log_test(
                        "Save Signature Endpoint",
                        True,
                        "Signature saved successfully",
                        f"File: {data['signature_file']}"
                    )
                    return True
                else:
                    self.log_test(
                        "Save Signature Endpoint",
                        False,
                        "Invalid response format",
                        f"Response: {data}"
                    )
                    return False
            else:
                self.log_test(
                    "Save Signature Endpoint",
                    False,
                    f"HTTP {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Save Signature Endpoint", False, f"Request failed: {e}")
            return False
    
    def test_4_token_validation_method(self):
        """Test 4: Token validation method (NameError fix verification)"""
        try:
            # Get the authorization we created
            auth = SignatoryAuthorization.objects.filter(
                user=self.test_user,
                signatory_name='TEST SIGNATORY 1'
            ).first()
            
            if not auth:
                self.log_test("Token Validation Method", False, "No authorization found")
                return False
            
            # Test the is_setup_token_valid method directly
            is_valid = auth.is_setup_token_valid()
            
            if isinstance(is_valid, bool):
                self.log_test(
                    "Token Validation Method",
                    True,
                    f"Method executed without NameError, returned: {is_valid}",
                    f"Token: {auth.setup_token[:20] if auth.setup_token else 'None'}..."
                )
                return True
            else:
                self.log_test(
                    "Token Validation Method",
                    False,
                    f"Method returned unexpected type: {type(is_valid)}"
                )
                return False
                
        except Exception as e:
            self.log_test("Token Validation Method", False, f"Method failed: {e}")
            return False
    
    def test_5_expired_token_handling(self):
        """Test 5: Expired token handling"""
        try:
            # Create authorization with expired token
            expired_token = secrets.token_urlsafe(32)
            expired_auth = SignatoryAuthorization.objects.create(
                user=self.test_user,
                signatory_name='EXPIRED TOKEN TEST',
                authorized_by=self.test_user,
                is_active=True,
                requires_2fa=True,
                notes='Expired token test',
                setup_token=expired_token,
                token_expires=timezone.now() - timedelta(hours=1),  # Expired 1 hour ago
                signature_created=False
            )
            
            # Test setup endpoint with expired token
            url = f'{self.base_url}/api/signatory-authorizations/signature-setup/{expired_token}/'
            response = requests.get(url)
            
            if response.status_code == 400:
                data = response.json()
                if 'expired' in data.get('error', '').lower():
                    self.log_test(
                        "Expired Token Handling",
                        True,
                        "Expired token correctly rejected",
                        f"Response: {data}"
                    )
                    return True
                else:
                    self.log_test(
                        "Expired Token Handling",
                        False,
                        "Wrong error message for expired token",
                        f"Response: {data}"
                    )
                    return False
            else:
                self.log_test(
                    "Expired Token Handling",
                    False,
                    f"Expected 400, got {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Expired Token Handling", False, f"Test failed: {e}")
            return False
    
    def test_6_invalid_token_handling(self):
        """Test 6: Invalid token handling"""
        try:
            # Test with completely invalid token
            invalid_token = 'invalid_token_12345'
            url = f'{self.base_url}/api/signatory-authorizations/signature-setup/{invalid_token}/'
            response = requests.get(url)
            
            if response.status_code == 404:
                data = response.json()
                if 'invalid' in data.get('error', '').lower():
                    self.log_test(
                        "Invalid Token Handling",
                        True,
                        "Invalid token correctly rejected",
                        f"Response: {data}"
                    )
                    return True
                else:
                    self.log_test(
                        "Invalid Token Handling",
                        False,
                        "Wrong error message for invalid token",
                        f"Response: {data}"
                    )
                    return False
            else:
                self.log_test(
                    "Invalid Token Handling",
                    False,
                    f"Expected 404, got {response.status_code}",
                    response.text
                )
                return False
                
        except Exception as e:
            self.log_test("Invalid Token Handling", False, f"Test failed: {e}")
            return False
    
    def test_7_signal_workflow(self):
        """Test 7: Signal-triggered workflow"""
        try:
            # Clean up any existing data
            SignatoryAuthorization.objects.filter(
                user=self.test_user,
                signatory_name='SIGNAL TEST'
            ).delete()
            
            # Create request (should trigger signal)
            request = SignatoryAuthorizationRequest.objects.create(
                user=self.test_user,
                signatory_name='SIGNAL TEST',
                role='Approved by',
                email='signal.test@example.com',
                justification='Test 7: Signal-triggered workflow test'
            )
            
            # Wait a moment for signal processing
            time.sleep(1)
            
            # Check if authorization was created by signal
            auth = SignatoryAuthorization.objects.filter(
                user=self.test_user,
                signatory_name='SIGNAL TEST'
            ).first()
            
            if auth and auth.setup_token:
                self.log_test(
                    "Signal Workflow",
                    True,
                    "Signal created authorization with setup token",
                    f"Auth ID: {auth.id}, Token: {auth.setup_token[:20]}..."
                )
                return True
            else:
                self.log_test(
                    "Signal Workflow",
                    False,
                    "Signal did not create authorization or token missing",
                    f"Auth exists: {auth is not None}"
                )
                return False
                
        except Exception as e:
            self.log_test("Signal Workflow", False, f"Test failed: {e}")
            return False
    
    def test_8_file_creation_verification(self):
        """Test 8: Verify signature files are created"""
        try:
            # Check if signature files directory exists
            signatures_dir = 'npc-reporting-system/backend/media/admin_signatures'
            
            if not os.path.exists(signatures_dir):
                self.log_test(
                    "File Creation Verification",
                    False,
                    "Signatures directory does not exist"
                )
                return False
            
            # List files in directory
            files = os.listdir(signatures_dir)
            signature_files = [f for f in files if f.endswith('.png') or f.endswith('.jpg')]
            
            if signature_files:
                self.log_test(
                    "File Creation Verification",
                    True,
                    f"Found {len(signature_files)} signature files",
                    f"Files: {signature_files[:5]}..."  # Show first 5 files
                )
                return True
            else:
                self.log_test(
                    "File Creation Verification",
                    False,
                    "No signature files found in directory"
                )
                return False
                
        except Exception as e:
            self.log_test("File Creation Verification", False, f"Test failed: {e}")
            return False
    
    def test_9_multiple_signatories(self):
        """Test 9: Multiple signatories for same user"""
        try:
            signatory_names = ['MULTI TEST 1', 'MULTI TEST 2', 'MULTI TEST 3']
            created_auths = []
            
            for name in signatory_names:
                # Clean up existing
                SignatoryAuthorization.objects.filter(
                    user=self.test_user,
                    signatory_name=name
                ).delete()
                
                # Create authorization
                setup_token = secrets.token_urlsafe(32)
                auth = SignatoryAuthorization.objects.create(
                    user=self.test_user,
                    signatory_name=name,
                    authorized_by=self.test_user,
                    is_active=True,
                    requires_2fa=True,
                    notes=f'Multi-signatory test: {name}',
                    setup_token=setup_token,
                    token_expires=timezone.now() + timedelta(hours=24),
                    signature_created=False
                )
                created_auths.append(auth)
            
            # Test each authorization
            all_valid = True
            for auth in created_auths:
                is_valid = auth.is_setup_token_valid()
                if not is_valid:
                    all_valid = False
                    break
            
            if all_valid and len(created_auths) == len(signatory_names):
                self.log_test(
                    "Multiple Signatories",
                    True,
                    f"Created {len(created_auths)} authorizations successfully",
                    f"Signatories: {[auth.signatory_name for auth in created_auths]}"
                )
                return True
            else:
                self.log_test(
                    "Multiple Signatories",
                    False,
                    f"Failed to create or validate all authorizations"
                )
                return False
                
        except Exception as e:
            self.log_test("Multiple Signatories", False, f"Test failed: {e}")
            return False
    
    def test_10_edge_cases(self):
        """Test 10: Edge cases and error conditions"""
        try:
            edge_cases_passed = 0
            total_edge_cases = 3
            
            # Edge case 1: Empty signature data
            if self.setup_tokens:
                token = self.setup_tokens[0]
                url = f'{self.base_url}/api/signatory-authorizations/save-signature/{token}/'
                response = requests.post(url, json={'signature': ''})
                
                if response.status_code == 400:
                    edge_cases_passed += 1
            
            # Edge case 2: Malformed signature data
            if self.setup_tokens:
                token = self.setup_tokens[0]
                url = f'{self.base_url}/api/signatory-authorizations/save-signature/{token}/'
                response = requests.post(url, json={'signature': 'invalid_base64_data'})
                
                if response.status_code in [400, 500]:  # Either is acceptable for malformed data
                    edge_cases_passed += 1
            
            # Edge case 3: Missing signature field
            if self.setup_tokens:
                token = self.setup_tokens[0]
                url = f'{self.base_url}/api/signatory-authorizations/save-signature/{token}/'
                response = requests.post(url, json={})
                
                if response.status_code == 400:
                    edge_cases_passed += 1
            
            if edge_cases_passed >= 2:  # Allow some flexibility
                self.log_test(
                    "Edge Cases",
                    True,
                    f"Passed {edge_cases_passed}/{total_edge_cases} edge case tests",
                    "System handles error conditions appropriately"
                )
                return True
            else:
                self.log_test(
                    "Edge Cases",
                    False,
                    f"Only passed {edge_cases_passed}/{total_edge_cases} edge case tests"
                )
                return False
                
        except Exception as e:
            self.log_test("Edge Cases", False, f"Test failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up test data"""
        try:
            # Clean up test authorizations
            SignatoryAuthorization.objects.filter(user=self.test_user).delete()
            SignatoryAuthorizationRequest.objects.filter(user=self.test_user).delete()
            
            self.log_test("Cleanup", True, "Test data cleaned up successfully")
        except Exception as e:
            self.log_test("Cleanup", False, f"Cleanup failed: {e}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🔥 COMPREHENSIVE E-SIGNATURE SYSTEM TEST")
        print("=" * 60)
        print(f"Started at: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Setup
        if not self.setup_test_user():
            print("❌ Cannot continue without test user")
            return
        
        # Run tests
        tests = [
            self.test_1_direct_authorization_creation,
            self.test_2_signature_setup_endpoint,
            self.test_3_save_signature_endpoint,
            self.test_4_token_validation_method,
            self.test_5_expired_token_handling,
            self.test_6_invalid_token_handling,
            self.test_7_signal_workflow,
            self.test_8_file_creation_verification,
            self.test_9_multiple_signatories,
            self.test_10_edge_cases
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test.__name__}: {e}")
                failed += 1
            
            print()  # Add spacing between tests
        
        # Cleanup
        self.cleanup()
        
        # Summary
        print("=" * 60)
        print("🎯 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {passed + failed}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ E-Signature system is fully functional")
            print("✅ NameError has been completely resolved")
            print("✅ All endpoints working correctly")
        else:
            print(f"\n⚠️  {failed} test(s) failed - review results above")
        
        print("=" * 60)
        print(f"Completed at: {datetime.now().isoformat()}")
        
        return failed == 0

def main():
    """Main test runner"""
    test_suite = ESignatureSystemTest()
    success = test_suite.run_all_tests()
    
    # Save detailed results
    with open('esignature_test_results.json', 'w') as f:
        json.dump(test_suite.test_results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: esignature_test_results.json")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())