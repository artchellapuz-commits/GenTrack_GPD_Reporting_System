#!/usr/bin/env python3
"""
Test the complete drawn signature workflow to identify the issue
"""

import os
import sys
import django
import requests
import base64
from io import BytesIO
from PIL import Image, ImageDraw

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest

def create_test_signature_image():
    """Create a test signature image similar to what would be drawn"""
    # Create a simple signature-like drawing
    width, height = 500, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a simple signature-like curve
    points = [
        (50, 100), (100, 80), (150, 120), (200, 90), 
        (250, 110), (300, 85), (350, 115), (400, 95), (450, 105)
    ]
    
    # Draw the signature curve
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill='black', width=3)
    
    # Convert to base64 like the frontend would
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Create data URL like canvas.toDataURL() would
    image_data = base64.b64encode(buffer.getvalue()).decode()
    data_url = f"data:image/png;base64,{image_data}"
    
    return data_url

def test_drawn_signature_submission():
    """Test submitting a drawn signature"""
    print("=== TESTING DRAWN SIGNATURE SUBMISSION ===\n")
    
    # Get the pending signature request
    pending_request = SignatureRequest.objects.filter(status='PENDING').first()
    
    if not pending_request:
        print("No pending signature request found")
        return
    
    print(f"Using signature request: {pending_request.id}")
    print(f"Token: {pending_request.token}")
    print(f"Signer: {pending_request.signer_name}")
    
    # Create test signature image
    signature_data_url = create_test_signature_image()
    print(f"Created signature data URL (length: {len(signature_data_url)})")
    print(f"Data URL prefix: {signature_data_url[:50]}...")
    
    # Prepare the form data like the frontend would
    form_data = {
        'signature_type': 'DRAWN',
        'signature_data': signature_data_url,
        'width': '500',
        'height': '200'
    }
    
    print(f"\nForm data to submit:")
    for key, value in form_data.items():
        if key == 'signature_data':
            print(f"  {key}: {value[:50]}... (length: {len(value)})")
        else:
            print(f"  {key}: {value}")
    
    # Submit to the API endpoint
    api_url = f"http://localhost:8000/api/signing/sign/{pending_request.token}/"
    
    try:
        print(f"\nSubmitting to: {api_url}")
        response = requests.post(api_url, data=form_data)
        
        print(f"Response status: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS: Signature submitted successfully!")
            
            # Check what was actually saved
            pending_request.refresh_from_db()
            if hasattr(pending_request, 'signature'):
                sig = pending_request.signature
                print(f"\nSaved signature details:")
                print(f"  Type: {sig.signature_type}")
                print(f"  Image path: {sig.signature_image}")
                print(f"  Data preview: {sig.signature_data[:50]}...")
                print(f"  Dimensions: {sig.width}x{sig.height}")
                
                # Check if image file was created
                if sig.signature_image:
                    image_path = f"npc-reporting-system/backend/media/{sig.signature_image}"
                    if os.path.exists(image_path):
                        file_size = os.path.getsize(image_path)
                        print(f"  Image file exists: {file_size} bytes")
                    else:
                        print(f"  ❌ Image file not found: {image_path}")
            else:
                print("❌ No digital signature was created")
        else:
            print(f"\n❌ FAILED: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")

if __name__ == "__main__":
    test_drawn_signature_submission()