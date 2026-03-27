#!/usr/bin/env python3
"""
Create test digital signatures for testing the signature display functionality
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import SignatureRequest, DigitalSignature
from django.utils import timezone

def create_signature_image(text, width=400, height=150):
    """Create a signature image with the given text"""
    # Create image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to use a nice font
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position (centered)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the signature text in a script-like style
    draw.text((x, y), text, fill='#1e40af', font=font)
    
    # Add a decorative underline
    line_y = y + text_height + 10
    draw.line([(x, line_y), (x + text_width, line_y)], fill='#1e40af', width=2)
    
    # Save to BytesIO
    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    
    return output.getvalue()

def create_test_digital_signatures():
    """Create test digital signatures for existing signature requests"""
    print("Creating test digital signatures...")
    
    try:
        # Get signed signature requests that don't have digital signatures yet
        signed_requests = SignatureRequest.objects.filter(
            status='SIGNED'
        ).exclude(
            signature__isnull=False
        )
        
        print(f"Found {signed_requests.count()} signed requests without digital signatures")
        
        created_count = 0
        for request in signed_requests:
            # Create a signature image
            signature_text = request.signer_name
            image_data = create_signature_image(signature_text)
            
            # Create the digital signature
            digital_signature = DigitalSignature.objects.create(
                signature_request=request,
                signature_type='DRAWN',
                signature_data='',  # We're not storing base64 data for this test
                verification_hash=f'test-hash-{request.id}',
                width=400,
                height=150,
                ip_address='127.0.0.1',
                user_agent='Test Script'
            )
            
            # Save the signature image
            filename = f"signature_{request.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.png"
            digital_signature.signature_image.save(
                filename,
                ContentFile(image_data),
                save=True
            )
            
            print(f"✅ Created digital signature for {request.signer_name}")
            created_count += 1
        
        print(f"\n✅ Created {created_count} digital signatures")
        return created_count > 0
        
    except Exception as e:
        print(f"❌ Error creating digital signatures: {e}")
        return False

def verify_digital_signatures():
    """Verify that digital signatures were created correctly"""
    print("\nVerifying digital signatures...")
    
    try:
        digital_signatures = DigitalSignature.objects.all()
        print(f"✅ Found {digital_signatures.count()} digital signatures in database")
        
        for ds in digital_signatures:
            print(f"✅ Digital Signature:")
            print(f"   - ID: {ds.id}")
            print(f"   - Signer: {ds.signature_request.signer_name}")
            print(f"   - Document: {ds.signature_request.document.title}")
            print(f"   - Type: {ds.signature_type}")
            print(f"   - Image: {ds.signature_image.url if ds.signature_image else 'No image'}")
            print(f"   - Size: {ds.width}x{ds.height}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying digital signatures: {e}")
        return False

def test_api_response():
    """Test what the API returns for digital signatures"""
    print("Testing API response structure...")
    
    try:
        import requests
        
        # Test the digital signatures API
        response = requests.get('http://localhost:8000/api/digital-signatures/')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API returned {len(data.get('results', data))} digital signatures")
            
            # Show structure of first signature
            if data.get('results'):
                first_sig = data['results'][0]
            elif isinstance(data, list) and data:
                first_sig = data[0]
            else:
                first_sig = None
            
            if first_sig:
                print("✅ Sample digital signature API structure:")
                for key, value in first_sig.items():
                    print(f"   - {key}: {value}")
                
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Backend server is not running")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def cleanup_test_signatures():
    """Clean up test digital signatures"""
    print("\nCleaning up test digital signatures...")
    
    try:
        # Delete digital signatures with test verification hashes
        deleted_count = DigitalSignature.objects.filter(
            verification_hash__startswith='test-hash-'
        ).delete()[0]
        
        print(f"✅ Deleted {deleted_count} test digital signatures")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Creating Test Digital Signatures\n")
    
    # Create digital signatures
    creation_success = create_test_digital_signatures()
    
    if creation_success:
        # Verify they were created
        verification_success = verify_digital_signatures()
        
        # Test API response
        api_success = test_api_response()
        
        print("\n" + "="*60)
        print("SUMMARY:")
        print(f"Digital Signature Creation: {'✅ PASS' if creation_success else '❌ FAIL'}")
        print(f"Verification: {'✅ PASS' if verification_success else '❌ FAIL'}")
        print(f"API Test: {'✅ PASS' if api_success else '❌ FAIL'}")
        
        if all([creation_success, verification_success]):
            print("\n🎉 Test digital signatures created successfully!")
            print("\nNow you can test the signature display:")
            print("1. Go to Document Manager")
            print("2. Click 'View Signatures' on a document")
            print("3. You should see the actual signature images displayed")
            print("4. Signed signatures will show the drawn signature image")
            print("5. Pending signatures will show 'Awaiting signature' placeholder")
            
            # Ask if user wants to keep test data
            print("\n" + "="*60)
            keep_data = input("Keep test digital signatures for testing? (y/n): ").lower().strip()
            
            if keep_data != 'y':
                cleanup_test_signatures()
            else:
                print("✅ Test digital signatures kept for testing")
        else:
            print("\n⚠️  Some operations failed. Please review the issues above.")
    else:
        print("❌ Failed to create test digital signatures")