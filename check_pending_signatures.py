#!/usr/bin/env python3
"""
Check for pending signature requests to test drawn signatures
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

def check_pending_signatures():
    """Check for pending signature requests"""
    print("=== PENDING SIGNATURE REQUESTS ===\n")
    
    pending_requests = SignatureRequest.objects.filter(status='PENDING').order_by('-created_at')
    
    if not pending_requests:
        print("No pending signature requests found.")
        return
    
    for req in pending_requests:
        print(f"Request ID: {req.id}")
        print(f"Signer: {req.signer_name}")
        print(f"Email: {req.signer_email}")
        print(f"Document: {req.document.title}")
        print(f"Token: {req.token}")
        print(f"Expires: {req.expires_at}")
        print(f"Signing URL: {req.generate_signing_url()}")
        print("-" * 50)

if __name__ == "__main__":
    check_pending_signatures()