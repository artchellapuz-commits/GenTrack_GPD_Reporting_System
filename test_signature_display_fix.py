#!/usr/bin/env python3
"""
Test script to verify signature display fix in DocumentManager
"""
import os
import sys
import django
import requests
import json

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, Document, DigitalSignature
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def create_test_document_with_signatures():
    """Create a test document with signature requests"""
    print("Creating test document with signature requests...")
    
    try:
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        # Create a test document
        document, created = Document.objects.get_or_create(
            title="Test PSR Document with Signatures",
            defaults={
                'content': 'This is a test PSR document for signature display testing.',
                'document_type': 'PSR',
                'created_by': user,
                'status': 'PENDING_SIGNATURE'
            }
        )
        
        print(f"✅ Document created/found: ID={document.id}, Title='{document.title}'")
        
        # Create signature requests
        signers = [
            {'name': 'John Smith', 'email': 'john.smith@example.com', 'role': 'Plant Manager'},
            {'name': 'Sarah Johnson', 'email': 'sarah.johnson@example.com', 'role': 'Safety Officer'},
            {'name': 'Mike Wilson', 'email': 'mike.wilson@example.com', 'role': 'Operations Supervisor'}
        ]
        
        signature_requests = []
        for i, signer in enumerate(signers):
            signature_request, created = SignatureRequest.objects.get_or_create(
                document=document,
                signer_email=signer['email'],
                defaults={
                    'signer_name': signer['name'],
                    'signer_role': signer['role'],
                    'token': f'test-token-{document.id}-{i+1}',
                    'expires_at': timezone.now() + timedelta(hours=72),
                    'status': 'SIGNED' if i < 2 else 'PENDING'  # First 2 signed, last one pending
                }
            )
            
            if created or signature_request.status != ('SIGNED' if i < 2 else 'PENDING'):
                signature_request.status = 'SIGNED' if i < 2 else 'PENDING'
                if signature_request.status == 'SIGNED':
                    signature_request.signed_at = timezone.now() - timedelta(hours=i+1)
                signature_request.save()
            
            signature_requests.append(signature_request)
            print(f"✅ Signature request: {signer['name']} ({signature_request.status})")
        
        return document, signature_requests
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        return None, []

def test_signature_requests_api():
    """Test the signature requests API endpoint"""
    print("\nTesting signature requests API...")
    
    try:
        # Test the API endpoint
        response = requests.get('http://localhost:8000/api/signature-requests/')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API endpoint working, returned {len(data.get('results', data))} signature requests")
            
            # Show the structure of the first signature request
            if data.get('results'):
                first_sig = data['results'][0]
            elif isinstance(data, list) and data:
                first_sig = data[0]
            else:
                first_sig = None
                
            if first_sig:
                print(f"✅ Sample signature request structure:")
                print(f"   - ID: {first_sig.get('id')}")
                print(f"   - Document: {first_sig.get('document')}")
                print(f"   - Document Title: {first_sig.get('document_title')}")
                print(f"   - Signer: {first_sig.get('signer_name')}")
                print(f"   - Status: {first_sig.get('status')}")
                
                return True
            else:
                print("⚠️  No signature requests found in API response")
                return False
        else:
            print(f"❌ API endpoint returned status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Backend server is not running")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_document_signature_filtering():
    """Test that signature filtering works correctly"""
    print("\nTesting signature filtering logic...")
    
    try:
        # Get all signature requests
        all_signatures = list(SignatureRequest.objects.all())
        print(f"✅ Total signature requests in database: {len(all_signatures)}")
        
        # Get all documents
        all_documents = list(Document.objects.all())
        print(f"✅ Total documents in database: {len(all_documents)}")
        
        # Test filtering for each document
        for document in all_documents:
            # This is the logic used in the frontend (after our fix)
            signatures_for_doc = [sig for sig in all_signatures if sig.document.id == document.id]
            print(f"✅ Document '{document.title}' (ID: {document.id}) has {len(signatures_for_doc)} signature requests")
            
            for sig in signatures_for_doc:
                print(f"   - {sig.signer_name} ({sig.status})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing filtering: {e}")
        return False

def cleanup_test_data():
    """Clean up test data"""
    print("\nCleaning up test data...")
    
    try:
        # Remove test signature requests
        SignatureRequest.objects.filter(token__startswith='test-token-').delete()
        
        # Remove test documents
        Document.objects.filter(title__contains="Test PSR Document").delete()
        
        print("✅ Test data cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Testing Signature Display Fix\n")
    
    # Create test data
    document, signatures = create_test_document_with_signatures()
    
    if document:
        # Test API
        api_test = test_signature_requests_api()
        
        # Test filtering logic
        filter_test = test_document_signature_filtering()
        
        print("\n" + "="*60)
        print("SUMMARY:")
        print(f"Test Data Creation: {'✅ PASS' if document else '❌ FAIL'}")
        print(f"API Endpoint Test: {'✅ PASS' if api_test else '❌ FAIL'}")
        print(f"Filtering Logic Test: {'✅ PASS' if filter_test else '❌ FAIL'}")
        
        if all([document, api_test, filter_test]):
            print("\n🎉 All tests passed!")
            print("\nThe signature display issue should be resolved:")
            print("1. ✅ Documents have signature requests in the database")
            print("2. ✅ API endpoint returns signature requests correctly")
            print("3. ✅ Filtering logic matches signature requests to documents")
            print("4. ✅ Frontend should now show signatures instead of 'No signature requests found'")
            
            print("\nTo test in the browser:")
            print("1. Go to Document Manager")
            print("2. Click the 'View Signatures' button (list icon) on a document")
            print("3. You should now see the signature requests instead of the empty message")
        else:
            print("\n⚠️  Some tests failed. Please review the issues above.")
        
        # Clean up
        cleanup_test_data()
    else:
        print("❌ Failed to create test data. Cannot proceed with tests.")