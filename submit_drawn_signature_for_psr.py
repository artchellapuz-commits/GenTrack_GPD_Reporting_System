#!/usr/bin/env python3
"""
Submit a drawn signature for the PSR document
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

def create_realistic_signature_image():
    """Create a realistic signature-like drawing"""
    width, height = 500, 200
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Create a more realistic signature with curves and loops
    # This simulates the drawn signature from your first image
    
    # First part - "J" like curve
    points1 = [
        (50, 80), (60, 70), (70, 75), (80, 85), (90, 95), 
        (100, 105), (110, 115), (120, 125), (130, 130)
    ]
    
    # Second part - "M" like peaks
    points2 = [
        (150, 130), (160, 110), (170, 90), (180, 100), (190, 120),
        (200, 100), (210, 80), (220, 90), (230, 110), (240, 130)
    ]
    
    # Third part - "M" continuation and flourish
    points3 = [
        (260, 130), (270, 110), (280, 90), (290, 100), (300, 120),
        (310, 100), (320, 80), (330, 90), (340, 110), (350, 130)
    ]
    
    # Final flourish
    points4 = [
        (370, 130), (380, 120), (390, 110), (400, 105), (410, 100),
        (420, 95), (430, 90), (440, 95), (450, 100)
    ]
    
    # Draw all parts with varying thickness
    all_points = [points1, points2, points3, points4]
    
    for i, points in enumerate(all_points):
        width_line = 3 if i < 2 else 2  # Thicker for first parts
        for j in range(len(points) - 1):
            draw.line([points[j], points[j + 1]], fill='black', width=width_line)
    
    # Add some connecting strokes
    draw.line([(130, 130), (150, 130)], fill='black', width=2)
    draw.line([(240, 130), (260, 130)], fill='black', width=2)
    draw.line([(350, 130), (370, 130)], fill='black', width=2)
    
    # Convert to base64
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    
    image_data = base64.b64encode(buffer.getvalue()).decode()
    data_url = f"data:image/png;base64,{image_data}"
    
    return data_url

def submit_drawn_signature():
    """Submit a drawn signature for the PSR document"""
    print("=== SUBMITTING DRAWN SIGNATURE FOR PSR ===\n")
    
    # Get the pending signature request
    pending_request = SignatureRequest.objects.filter(
        status='PENDING', 
        signer_name='JMM_MATA'
    ).order_by('-created_at').first()
    
    if not pending_request:
        print("No pending signature request found")
        return
    
    print(f"Using signature request: {pending_request.id}")
    print(f"Token: {pending_request.token}")
    print(f"Document: {pending_request.document.title}")
    
    # Create realistic signature image
    signature_data_url = create_realistic_signature_image()
    print(f"Created signature image (length: {len(signature_data_url)})")
    
    # Prepare form data
    form_data = {
        'signature_type': 'DRAWN',
        'signature_data': signature_data_url,
        'width': '500',
        'height': '200'
    }
    
    # Submit to API
    api_url = f"http://localhost:8000/api/signing/sign/{pending_request.token}/"
    
    try:
        print(f"Submitting to: {api_url}")
        response = requests.post(api_url, data=form_data)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ SUCCESS: Drawn signature submitted!")
            
            # Check what was saved
            pending_request.refresh_from_db()
            if hasattr(pending_request, 'signature'):
                sig = pending_request.signature
                print(f"\nSaved signature details:")
                print(f"  ID: {sig.id}")
                print(f"  Type: {sig.signature_type}")
                print(f"  Image: {sig.signature_image}")
                print(f"  Image URL: http://localhost:8000/media/{sig.signature_image}")
                
                # Verify image file
                image_path = f"npc-reporting-system/backend/media/{sig.signature_image}"
                if os.path.exists(image_path):
                    size = os.path.getsize(image_path)
                    print(f"  Image file: {size} bytes")
                    print("  ✅ Image file created successfully!")
                else:
                    print("  ❌ Image file not found")
            
        else:
            print(f"❌ FAILED: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    submit_drawn_signature()