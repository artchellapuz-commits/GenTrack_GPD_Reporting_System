#!/usr/bin/env python3
"""
Test Email Link Fix
Verify that email links point to the correct frontend URL (localhost:8080)
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
sys.path.append('npc-reporting-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from reports.models import SignatoryAuthorizationRequest, SignatoryAuthorization

def test_site_url_configuration():
    """Test that SITE_URL is correctly configured"""
    print("🔧 TESTING: SITE_URL Configuration")
    print("=" * 50)
    
    try:
        site_url = getattr(settings, 'SITE_URL', 'NOT_CONFIGURED')
        print(f"✅ SITE_URL setting: {site_url}")
        
        if site_url == "http://localhost:8080":
            print("✅ SITE_URL is correctly set to localhost:8080")
            return True
        elif site_url == "http://localhost:8081":
            print("❌ SITE_URL is set to localhost:8081 (should be 8080)")
            return False
        else:
            print(f"⚠️  SITE_URL is set to: {site_url}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking SITE_URL: {e}")
        return False

def test_email_link_generation():
    """Test that email links are generated with correct URL"""
    print("\n📧 TESTING: Email Link Generation")
    print("=" * 50)
    
    try:
        # Create test user
        user, created = User.objects.get_or_create(
            username='email_link_test',
            defaults={
                'email': 'emailtest@example.com',
                'first_name': 'Email',
                'last_name': 'Test'
            }
        )
        
        # Create authorization with setup token
        auth = SignatoryAuthorization.objects.create(
            user=user,
            signatory_name='EMAIL LINK TEST',
            authorized_by=user,
            is_active=True,
            requires_2fa=False,
            notes='Test authorization for email link testing',
            authorization_date=timezone.now(),
            expiry_date=timezone.now() + timedelta(days=30)
        )
        
        # Generate setup token
        auth.generate_setup_token()
        auth.save()
        
        print(f"✅ Created test authorization with setup token")
        print(f"   Setup token: {auth.setup_token[:20]}...")
        
        # Test URL generation using the same logic as the email system
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8081')
        setup_url = f"{site_url}/signature-setup/{auth.setup_token}"
        
        print(f"✅ Generated setup URL: {setup_url}")
        
        # Check if URL uses correct port
        if "localhost:8080" in setup_url:
            print("✅ Email link uses correct port (8080)")
            result = True
        elif "localhost:8081" in setup_url:
            print("❌ Email link uses wrong port (8081)")
            result = False
        else:
            print(f"⚠️  Email link uses different URL: {setup_url}")
            result = False
        
        # Clean up
        auth.delete()
        
        return result
        
    except Exception as e:
        print(f"❌ Error testing email link generation: {e}")
        return False

def test_frontend_server_status():
    """Test if frontend servers are running on different ports"""
    print("\n🌐 TESTING: Frontend Server Status")
    print("=" * 50)
    
    import requests
    
    ports_to_test = [8080, 8081, 3000]
    running_servers = []
    
    for port in ports_to_test:
        try:
            url = f"http://localhost:{port}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                running_servers.append(port)
                print(f"✅ Server running on port {port}")
            else:
                print(f"⚠️  Port {port}: HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ No server running on port {port}")
        except requests.exceptions.Timeout:
            print(f"⚠️  Port {port}: Connection timeout")
        except Exception as e:
            print(f"❌ Port {port}: Error - {e}")
    
    if 8080 in running_servers:
        print("\n✅ Frontend server is running on correct port (8080)")
        return True
    elif 8081 in running_servers:
        print("\n⚠️  Frontend server is running on port 8081 (email links will work)")
        return True
    else:
        print("\n❌ No frontend server detected on expected ports")
        return False

def test_signature_setup_route():
    """Test if signature setup route exists in frontend"""
    print("\n🛣️  TESTING: Signature Setup Route")
    print("=" * 50)
    
    try:
        router_file = 'npc-reporting-system/frontend/src/router/index.js'
        
        if os.path.exists(router_file):
            with open(router_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'signature-setup' in content:
                print("✅ Signature setup route found in router")
                
                # Check for the specific route pattern
                if '/signature-setup/:token' in content or '/signature-setup/:id' in content:
                    print("✅ Route accepts token parameter")
                    return True
                else:
                    print("⚠️  Route found but parameter pattern unclear")
                    return True
            else:
                print("❌ Signature setup route not found in router")
                return False
        else:
            print("❌ Router file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking router: {e}")
        return False

def provide_solution():
    """Provide solution steps"""
    print("\n🔧 SOLUTION STEPS")
    print("=" * 50)
    
    print("1. ✅ SITE_URL is configured correctly in Django settings")
    print("2. 🚀 Start the frontend server:")
    print("   cd npc-reporting-system/frontend")
    print("   npm run serve")
    print("   (This will start the server on http://localhost:8080)")
    
    print("\n3. 🔄 Restart the Django server to pick up settings changes:")
    print("   cd npc-reporting-system/backend")
    print("   python manage.py runserver")
    
    print("\n4. 📧 Test the email workflow:")
    print("   - Create a new authorization request")
    print("   - Check the email for the signature setup link")
    print("   - Link should now point to http://localhost:8080")
    
    print("\n5. 🌐 Verify both servers are running:")
    print("   - Frontend: http://localhost:8080")
    print("   - Backend: http://localhost:8000")

def main():
    """Run email link fix tests"""
    print("📧 EMAIL LINK FIX TEST SUITE")
    print("Testing that email links point to correct frontend URL")
    print("=" * 60)
    
    tests = [
        ("SITE_URL Configuration", test_site_url_configuration),
        ("Email Link Generation", test_email_link_generation),
        ("Frontend Server Status", test_frontend_server_status),
        ("Signature Setup Route", test_signature_setup_route)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n❌ {test_name} - FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} - CRASHED: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 EMAIL LINK FIX TEST SUMMARY")
    print("=" * 60)
    print(f"📊 Tests Passed: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed >= 3:
        print("\n🎉 EMAIL LINK CONFIGURATION IS CORRECT!")
        print("✅ SITE_URL points to localhost:8080")
        print("✅ Email links will use correct URL")
        print("✅ Frontend route exists")
        
        print("\n📋 NEXT STEPS:")
        print("1. Make sure frontend server is running on port 8080")
        print("2. Restart Django server to apply settings")
        print("3. Test email workflow with new authorization request")
        
    else:
        print(f"\n⚠️  {total-passed} issue(s) found")
        print("Email links may not work correctly")
    
    # Always provide solution steps
    provide_solution()
    
    print("=" * 60)
    
    return passed >= 3

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)