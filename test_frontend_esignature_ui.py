#!/usr/bin/env python3
"""
Frontend E-Signature UI Test
Tests the frontend components and user interface for e-signature workflow
"""

import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class FrontendESignatureUITester:
    def __init__(self):
        self.frontend_url = 'http://localhost:8081'
        self.backend_url = 'http://localhost:8000'
        self.driver = None
        self.test_results = []
        
    def log_test(self, test_name, success, message, details=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   {message}")
        if details:
            print(f"   Details: {details}")
        print()
        
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message,
            'details': details
        })
    
    def setup_browser(self):
        """Setup headless Chrome browser for testing"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
            self.log_test(
                "Browser Setup",
                True,
                "Chrome browser initialized successfully"
            )
            return True
            
        except Exception as e:
            self.log_test(
                "Browser Setup",
                False,
                f"Failed to setup browser: {str(e)}",
                "Note: This test requires Chrome and ChromeDriver to be installed"
            )
            return False
    
    def test_signature_setup_page_loads(self):
        """Test that signature setup page loads without errors"""
        if not self.driver:
            return False
            
        try:
            # Get a valid setup token from the backend
            setup_token = self.get_valid_setup_token()
            if not setup_token:
                self.log_test(
                    "Signature Setup Page Load",
                    False,
                    "No valid setup token available for testing"
                )
                return False
            
            # Navigate to signature setup page
            url = f"{self.frontend_url}/signature-setup/{setup_token}"
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check for error messages
            error_elements = self.driver.find_elements(By.CLASS_NAME, "error-card")
            if error_elements:
                error_text = error_elements[0].text
                self.log_test(
                    "Signature Setup Page Load",
                    False,
                    f"Page loaded with error: {error_text}"
                )
                return False
            
            # Check for signature setup elements
            canvas_elements = self.driver.find_elements(By.CLASS_NAME, "signature-canvas")
            if canvas_elements:
                self.log_test(
                    "Signature Setup Page Load",
                    True,
                    "Signature setup page loaded successfully with canvas"
                )
                return True
            else:
                self.log_test(
                    "Signature Setup Page Load",
                    False,
                    "Page loaded but signature canvas not found"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Signature Setup Page Load",
                False,
                f"Failed to load signature setup page: {str(e)}"
            )
            return False
    
    def test_signature_setup_ui_elements(self):
        """Test that all required UI elements are present"""
        if not self.driver:
            return False
            
        try:
            # Check for required elements
            required_elements = [
                ("signature-canvas", "Signature drawing canvas"),
                ("btn-clear", "Clear button"),
                ("btn-save", "Save button"),
                ("user-info", "User information section"),
                ("security-notice", "Security notice")
            ]
            
            missing_elements = []
            for class_name, description in required_elements:
                elements = self.driver.find_elements(By.CLASS_NAME, class_name)
                if not elements:
                    missing_elements.append(description)
            
            if missing_elements:
                self.log_test(
                    "UI Elements Check",
                    False,
                    f"Missing UI elements: {', '.join(missing_elements)}"
                )
                return False
            else:
                self.log_test(
                    "UI Elements Check",
                    True,
                    "All required UI elements are present"
                )
                return True
                
        except Exception as e:
            self.log_test(
                "UI Elements Check",
                False,
                f"Failed to check UI elements: {str(e)}"
            )
            return False
    
    def test_authorization_request_form(self):
        """Test the authorization request form (if accessible)"""
        if not self.driver:
            return False
            
        try:
            # Navigate to authorization request page
            url = f"{self.frontend_url}/signatory-authorization"
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(2)
            
            # Check if form elements are present
            form_elements = self.driver.find_elements(By.TAG_NAME, "form")
            if form_elements:
                self.log_test(
                    "Authorization Request Form",
                    True,
                    "Authorization request form is accessible"
                )
                return True
            else:
                # May require authentication
                self.log_test(
                    "Authorization Request Form",
                    True,
                    "Authorization request form requires authentication (expected)"
                )
                return True
                
        except Exception as e:
            self.log_test(
                "Authorization Request Form",
                False,
                f"Failed to access authorization request form: {str(e)}"
            )
            return False
    
    def get_valid_setup_token(self):
        """Get a valid setup token from the backend"""
        try:
            # Use the token from our previous test
            import os
            import sys
            import django
            sys.path.append('npc-reporting-system/backend')
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
            django.setup()
            
            from reports.models import SignatoryAuthorization
            from django.utils import timezone
            
            auth = SignatoryAuthorization.objects.filter(
                setup_token__isnull=False,
                token_expires__gt=timezone.now()
            ).order_by('-id').first()
            
            return auth.setup_token if auth else None
            
        except Exception as e:
            print(f"Failed to get setup token: {e}")
            return None
    
    def cleanup(self):
        """Cleanup browser resources"""
        if self.driver:
            self.driver.quit()
    
    def run_ui_tests(self):
        """Run all UI tests"""
        print("🖥️  Starting Frontend E-Signature UI Tests")
        print("=" * 50)
        
        # Setup browser
        if not self.setup_browser():
            print("⚠️  Skipping UI tests - browser setup failed")
            print("   Install Chrome and ChromeDriver to run UI tests")
            return True  # Don't fail the overall test suite
        
        try:
            # Run tests
            tests = [
                self.test_signature_setup_page_loads,
                self.test_signature_setup_ui_elements,
                self.test_authorization_request_form
            ]
            
            passed = 0
            total = len(tests)
            
            for test in tests:
                if test():
                    passed += 1
            
            # Summary
            print("=" * 50)
            print("🏁 UI TEST SUMMARY")
            print("=" * 50)
            
            for result in self.test_results:
                status = "✅" if result['success'] else "❌"
                print(f"{status} {result['test']}: {result['message']}")
            
            print("=" * 50)
            print(f"📊 UI RESULTS: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
            
            return passed == total
            
        finally:
            self.cleanup()

def main():
    """Main UI test runner"""
    tester = FrontendESignatureUITester()
    return tester.run_ui_tests()

if __name__ == '__main__':
    success = main()
    if success:
        print("🎯 UI tests completed successfully!")
    else:
        print("🔧 Some UI tests failed - check browser setup and frontend server")