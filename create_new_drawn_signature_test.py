#!/usr/bin/env python3
"""
Create a new signature request for the PSR document and test drawn signature
"""

import os
import sys
import django
import secrets
from datetime import timedelta

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, Document
from django.utils import timezone

def create_new_signature_request():
    """Create a new signature request for testing drawn signatures"""
    print("=== CREATING NEW SIGNATURE REQUEST ===\n")
    
    # Get the PSR document
    try:
        psr_doc = Document.objects.get(title="PSR")
        print(f"Found document: {psr_doc.title} (ID: {psr_doc.id})")
    except Document.DoesNotExist:
        print("PSR document not found")
        return
    
    # Create a new signature request
    token = secrets.token_urlsafe(32)
    expires_at = timezone.now() + timedelta(hours=24)
    
    signature_request = SignatureRequest.objects.create(
        document=psr_doc,
        signer_name="JMM_MATA",
        signer_email="zahurtongtong@gmail.com",
        signer_role="Checked and Reviewed by",
        token=token,
        expires_at=expires_at,
        signature_x=100,
        signature_y=100,
        signature_page=1
    )
    
    print(f"Created new signature request:")
    print(f"  ID: {signature_request.id}")
    print(f"  Token: {signature_request.token}")
    print(f"  Signer: {signature_request.signer_name}")
    print(f"  Status: {signature_request.status}")
    print(f"  Expires: {signature_request.expires_at}")
    
    signing_url = signature_request.generate_signing_url()
    print(f"  Signing URL: {signing_url}")
    
    return signature_request

if __name__ == "__main__":
    create_new_signature_request()