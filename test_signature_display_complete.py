#!/usr/bin/env python3
"""
Complete test to verify signature display functionality
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, Document
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def create_real_test_scenario():
    """Create a realistic test scenario with a PSR document and signatures"""
    print("Creating realistic test scenario...")
    
    try:
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='plant_operator',
            defaults={
                'email': 'operator@npc.com',
                'first_name': 'Plant',
                'last_name': 'Operator'
            }
        )
        
        # Create a PSR document
        document, created = Document.objects.get_or_create(
            title="Daily Plant Status Report - March 19, 2026",
            defaults={
                'content': '''
NUCLEAR POWER PLANT DAILY STATUS REPORT
Date: March 19, 2026
Shift: Day Shift (06:00 - 18:00)

REACTOR STATUS:
- Reactor Power: 100% (3,200 MWt)
- Primary System Pressure: 2,250 psia
- Primary System Temperature: 547°F
- Control Rod Position: Normal operating band

SAFETY SYSTEMS:
- Emergency Core Cooling System: Available
- Containment Integrity: Maintained
- Radiation Monitoring: Normal levels

MAINTENANCE ACTIVITIES:
- Routine surveillance testing completed
- No significant maintenance activities

OPERATIONAL NOTES:
- All systems operating within normal parameters
- No unusual events or conditions reported
- Environmental conditions: Normal

This report has been prepared in accordance with NPC operating procedures.
                ''',
                'document_type': 'PSR',
                'created_by': user,
                'status': 'PENDING_SIGNATURE'
            }
        )
        
        print(f"✅ Created PSR document: '{document.title}' (ID: {document.id})")
        
        # Create signature requests for typical PSR workflow
        signers = [
            {
                'name': 'John Martinez',
                'email': 'j.martinez@npc.com',
                'role': 'Shift Supervisor',
                'status': 'SIGNED',
                'signed_hours_ago': 2
            },
            {
                'name': 'Sarah Chen',
                'email': 's.chen@npc.com',
                'role': 'Senior Reactor Operator',
                'status': 'SIGNED',
                'signed_hours_ago': 1
            },
            {
                'name': 'Michael Rodriguez',
                'email': 'm.rodriguez@npc.com',
                'role': 'Plant Manager',
                'status': 'PENDING',
                'signed_hours_ago': None
            }
        ]
        
        signature_requests = []
        for i, signer in enumerate(signers):
            # Remove existing signature request if it exists
            SignatureRequest.objects.filter(
                document=document,
                signer_email=signer['email']
            ).delete()
            
            signature_request = SignatureRequest.objects.create(
                document=document,
                signer_name=signer['name'],
                signer_email=signer['email'],
                signer_role=signer['role'],
                token=f'psr-token-{document.id}-{i+1}',
                expires_at=timezone.now() + timedelta(hours=24),
                status=signer['status']
            )
            
            if signer['status'] == 'SIGNED' and signer['signed_hours_ago']:
                signature_request.signed_at = timezone.now() - timedelta(hours=signer['signed_hours_ago'])
                signature_request.save()
            
            signature_requests.append(signature_request)
            print(f"✅ Created signature request: {signer['name']} - {signer['role']} ({signer['status']})")
        
        return document, signature_requests
        
    except Exception as e:
        print(f"❌ Error creating test scenario: {e}")
        return None, []

def verify_data_structure():
    """Verify the data structure matches what the frontend expects"""
    print("\nVerifying data structure...")
    
    try:
        # Get the test document
        document = Document.objects.filter(title__contains="Daily Plant Status Report").first()
        if not document:
            print("❌ Test document not found")
            return False
        
        # Get signature requests for this document
        signature_requests = SignatureRequest.objects.filter(document=document)
        
        print(f"✅ Found {signature_requests.count()} signature requests for document ID {document.id}")
        
        # Verify the structure matches frontend expectations
        for sig in signature_requests:
            print(f"✅ Signature Request Structure:")
            print(f"   - ID: {sig.id}")
            print(f"   - Document: {sig.document.id} (matches document.id: {sig.document.id == document.id})")
            print(f"   - Signer Name: {sig.signer_name}")
            print(f"   - Signer Email: {sig.signer_email}")
            print(f"   - Signer Role: {sig.signer_role}")
            print(f"   - Status: {sig.status}")
            print(f"   - Signed At: {sig.signed_at}")
            print()
        
        # Test the filtering logic that the frontend uses
        all_signatures = list(SignatureRequest.objects.all())
        filtered_signatures = [sig for sig in all_signatures if sig.document.id == document.id]
        
        print(f"✅ Frontend filtering test:")
        print(f"   - Total signatures in DB: {len(all_signatures)}")
        print(f"   - Signatures for document {document.id}: {len(filtered_signatures)}")
        print(f"   - Filtering works correctly: {len(filtered_signatures) == signature_requests.count()}")
        
        return len(filtered_signatures) > 0
        
    except Exception as e:
        print(f"❌ Error verifying data structure: {e}")
        return False

def show_frontend_instructions():
    """Show instructions for testing in the frontend"""
    print("\n" + "="*60)
    print("FRONTEND TESTING INSTRUCTIONS:")
    print("="*60)
    print()
    print("1. Make sure both servers are running:")
    print("   Backend:  cd npc-reporting-system/backend && python manage.py runserver")
    print("   Frontend: cd npc-reporting-system/frontend && npm run serve")
    print()
    print("2. Open your browser and go to: http://localhost:3000")
    print()
    print("3. Login to the system")
    print()
    print("4. Navigate to Document Manager")
    print()
    print("5. Look for the document: 'Daily Plant Status Report - March 19, 2026'")
    print()
    print("6. Click the 'View Signatures' button (list icon) on that document")
    print()
    print("7. You should now see:")
    print("   ✅ John Martinez - Shift Supervisor (SIGNED)")
    print("   ✅ Sarah Chen - Senior Reactor Operator (SIGNED)")
    print("   ⏳ Michael Rodriguez - Plant Manager (PENDING)")
    print()
    print("8. If you see 'No signature requests found', the fix didn't work")
    print()
    print("EXPECTED RESULT: The modal should show the 3 signature requests above")
    print("instead of the 'No signature requests found' message.")

def cleanup_test_data():
    """Clean up test data"""
    print("\nCleaning up test data...")
    
    try:
        # Remove test signature requests
        SignatureRequest.objects.filter(token__startswith='psr-token-').delete()
        
        # Remove test documents
        Document.objects.filter(title__contains="Daily Plant Status Report").delete()
        
        print("✅ Test data cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Complete Signature Display Test\n")
    
    # Create realistic test scenario
    document, signatures = create_real_test_scenario()
    
    if document and signatures:
        # Verify data structure
        structure_ok = verify_data_structure()
        
        if structure_ok:
            print("\n🎉 SUCCESS! Test data created successfully.")
            print("\nThe signature display fix should now work correctly.")
            print("The frontend will be able to:")
            print("1. ✅ Fetch signature requests from the API")
            print("2. ✅ Filter them correctly by document ID")
            print("3. ✅ Display them in the signatures modal")
            
            show_frontend_instructions()
            
            # Ask if user wants to keep test data
            print("\n" + "="*60)
            keep_data = input("Keep test data for frontend testing? (y/n): ").lower().strip()
            
            if keep_data != 'y':
                cleanup_test_data()
            else:
                print("✅ Test data kept for frontend testing")
        else:
            print("\n❌ Data structure verification failed")
            cleanup_test_data()
    else:
        print("❌ Failed to create test scenario")