#!/usr/bin/env python3
"""
Reset the signature so the user can sign with their real signature
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, DigitalSignature, Document

def reset_signature_for_real_signing():
    """Reset the signature request so user can sign with their real signature"""
    print("Resetting signature for real signing...")
    
    try:
        # Find the PSR REPORT 2 document
        doc = Document.objects.filter(title='PSR REPORT 2').first()
        
        if not doc:
            print("❌ PSR REPORT 2 document not found")
            return False
        
        # Find the signature request for JMM_MATA
        sig_request = SignatureRequest.objects.filter(
            document=doc,
            signer_name='JMM_MATA'
        ).first()
        
        if not sig_request:
            print("❌ Signature request for JMM_MATA not found")
            return False
        
        print(f"✅ Found signature request for {sig_request.signer_name}")
        
        # Delete the test digital signature
        try:
            existing_sig = sig_request.signature
            print(f"✅ Found existing test signature: {existing_sig.signature_type}")
            existing_sig.delete()
            print("✅ Deleted test signature")
        except DigitalSignature.DoesNotExist:
            print("✅ No existing signature to delete")
        
        # Reset the signature request to PENDING so it can be signed again
        sig_request.status = 'PENDING'
        sig_request.signed_at = None
        sig_request.save()
        
        print(f"✅ Reset signature request status to PENDING")
        print(f"✅ Signature request token: {sig_request.token}")
        
        # Generate the signing URL
        signing_url = sig_request.generate_signing_url()
        print(f"✅ Signing URL: {signing_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resetting signature: {e}")
        return False

def show_signing_instructions():
    """Show instructions for signing with real signature"""
    print("\n" + "="*60)
    print("INSTRUCTIONS FOR REAL SIGNATURE SIGNING")
    print("="*60)
    print()
    print("The signature has been reset to PENDING status.")
    print("Now you can sign the document with your REAL signature:")
    print()
    print("METHOD 1 - Use Email Link (Recommended):")
    print("1. Check your email for the signature request")
    print("2. Click the signature link in the email")
    print("3. Draw your actual signature on the signature pad")
    print("4. Submit the signature")
    print()
    print("METHOD 2 - Direct URL:")
    print("1. Copy the signing URL shown above")
    print("2. Paste it in your browser")
    print("3. Draw your actual signature on the signature pad")
    print("4. Submit the signature")
    print()
    print("METHOD 3 - Document Manager:")
    print("1. Go to Document Manager")
    print("2. Find 'PSR REPORT 2'")
    print("3. Click 'Request Signatures' if available")
    print("4. Follow the signing process")
    print()
    print("IMPORTANT:")
    print("- Draw your ACTUAL signature, not a test signature")
    print("- The signature you draw will be saved and displayed")
    print("- Once signed, it will appear in the signature viewer")

if __name__ == '__main__':
    print("🔧 Resetting Signature for Real Signing\n")
    
    # Reset the signature
    reset_success = reset_signature_for_real_signing()
    
    if reset_success:
        show_signing_instructions()
        
        print("\n" + "="*60)
        print("✅ READY FOR REAL SIGNATURE!")
        print("="*60)
        print("The test signature has been removed.")
        print("You can now sign the document with your actual signature.")
        print("After signing, your REAL signature will be displayed in the viewer.")
    else:
        print("\n❌ Failed to reset signature")