#!/usr/bin/env python3
"""
Test script for the e-signature workflow system
"""

import os
import sys
import django
import requests
import json
from datetime import datetime, timedelta

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import Document, SignatureRequest, DigitalSignature
from reports.views_signature import DocumentViewSet, SignatureRequestViewSet

def test_esignature_workflow():
    """Test the complete e-signature workflow"""
    
    print("🔧 Testing E-Signature Workflow System")
    print("=" * 50)
    
    # Test 1: Check if models are properly created
    print("\n1. Testing Database Models...")
    try:
        # Check if we can create a document
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        document = Document.objects.create(
            title="Test PSR Report",
            document_type="PSR",
            content="This is a test Plant Status Report requiring signatures.",
            created_by=user
        )
        print(f"✅ Document created: {document.title}")
        
        # Check if we can create a signature request
        signature_request = SignatureRequest.objects.create(
            document=document,
            signer_name="John Doe",
            signer_email="john.doe@example.com",
            signer_role="Prepared by",
            token="test_token_123456789",
            expires_at=datetime.now() + timedelta(days=7)
        )
        print(f"✅ Signature request created for: {signature_request.signer_name}")
        
    except Exception as e:
        print(f"❌ Database model test failed: {e}")
        return False
    
    # Test 2: Check API endpoints
    print("\n2. Testing API Endpoints...")
    try:
        base_url = "http://127.0.0.1:8000"
        
        # Test document list endpoint
        response = requests.get(f"{base_url}/api/documents/")
        if response.status_code == 200:
            print("✅ Document API endpoint accessible")
        else:
            print(f"⚠️  Document API returned status: {response.status_code}")
        
        # Test signature request endpoint
        response = requests.get(f"{base_url}/api/signature-requests/")
        if response.status_code == 200:
            print("✅ Signature Request API endpoint accessible")
        else:
            print(f"⚠️  Signature Request API returned status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Django server not running. Please start with 'python manage.py runserver'")
    except Exception as e:
        print(f"❌ API test failed: {e}")
    
    # Test 3: Check frontend components
    print("\n3. Testing Frontend Components...")
    try:
        frontend_url = "http://localhost:8081"
        
        # Test if frontend is accessible
        response = requests.get(frontend_url, timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server accessible")
        else:
            print(f"⚠️  Frontend returned status: {response.status_code}")
            
        # Test report storage route
        response = requests.get(f"{frontend_url}/report-storage", timeout=5)
        if response.status_code == 200:
            print("✅ Report Storage route accessible")
        else:
            print(f"⚠️  Document Manager route returned status: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Frontend server not running. Please start with 'npm run serve'")
    except Exception as e:
        print(f"❌ Frontend test failed: {e}")
    
    # Test 4: Check email configuration
    print("\n4. Testing Email Configuration...")
    try:
        from django.core.mail import send_mail
        from django.conf import settings
        
        if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
            print(f"✅ Email host configured: {settings.EMAIL_HOST}")
            print(f"✅ Email port: {settings.EMAIL_PORT}")
            print(f"✅ Email TLS: {settings.EMAIL_USE_TLS}")
        else:
            print("⚠️  Email not configured. Signature request emails won't be sent.")
            
    except Exception as e:
        print(f"❌ Email configuration test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 E-Signature Workflow Test Complete!")
    print("\nNext Steps:")
    print("1. Access Report Storage at: http://localhost:8081/report-storage")
    print("2. Create a report and request signatures")
    print("3. Check email for signature request links")
    print("4. Use signature links to sign documents")
    
    # Cleanup test data
    try:
        signature_request.delete()
        document.delete()
        print("\n🧹 Test data cleaned up")
    except:
        pass
    
    return True

if __name__ == "__main__":
    test_esignature_workflow()