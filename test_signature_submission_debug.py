#!/usr/bin/env python3
"""
Test script to debug signature submission and see what data is being received
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import DigitalSignature, SignatureRequest, Document
from reports.serializers_signature import SignDocumentSerializer

def test_signature_data_processing():
    """Test how signature data is processed"""
    print("=== SIGNATURE DATA PROCESSING TEST ===\n")
    
    # Get the most recent signature request
    recent_request = SignatureRequest.objects.filter(status='SIGNED').order_by('-signed_at').first()
    
    if not recent_request:
        print("No signed requests found")
        return
    
    print(f"Recent signed request: {recent_request.id}")
    print(f"Signer: {recent_request.signer_name}")
    print(f"Document: {recent_request.document.title}")
    print(f"Status: {recent_request.status}")
    
    # Get the digital signature
    if hasattr(recent_request, 'signature'):
        sig = recent_request.signature
        print(f"\nDigital Signature Details:")
        print(f"ID: {sig.id}")
        print(f"Type: {sig.signature_type}")
        print(f"Image Path: {sig.signature_image}")
        print(f"Data (first 100 chars): {sig.signature_data[:100]}...")
        print(f"Width x Height: {sig.width} x {sig.height}")
        
        # Check if this should have been a drawn signature
        if sig.signature_data.startswith('data:image/png;base64,'):
            print("\n⚠️  WARNING: This looks like base64 image data but was saved as TYPED!")
            print("This indicates the signature_type was incorrectly set to TYPED instead of DRAWN")
        elif sig.signature_data and not sig.signature_data.startswith('data:'):
            print(f"\n✓ This appears to be typed text: '{sig.signature_data}'")
    else:
        print("No digital signature found for this request")
    
    # Test the serializer with sample drawn signature data
    print("\n=== TESTING SERIALIZER WITH DRAWN SIGNATURE ===")
    
    sample_drawn_data = {
        'signature_type': 'DRAWN',
        'signature_data': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
        'width': 500,
        'height': 200
    }
    
    serializer = SignDocumentSerializer(data=sample_drawn_data)
    if serializer.is_valid():
        print("✓ Drawn signature data is valid")
        print(f"Validated data: {serializer.validated_data}")
    else:
        print("✗ Drawn signature data is invalid")
        print(f"Errors: {serializer.errors}")
    
    # Test with typed signature data
    print("\n=== TESTING SERIALIZER WITH TYPED SIGNATURE ===")
    
    sample_typed_data = {
        'signature_type': 'TYPED',
        'signature_data': 'JMM_MATA',
        'width': 400,
        'height': 100
    }
    
    serializer = SignDocumentSerializer(data=sample_typed_data)
    if serializer.is_valid():
        print("✓ Typed signature data is valid")
        print(f"Validated data: {serializer.validated_data}")
    else:
        print("✗ Typed signature data is invalid")
        print(f"Errors: {serializer.errors}")

if __name__ == "__main__":
    test_signature_data_processing()