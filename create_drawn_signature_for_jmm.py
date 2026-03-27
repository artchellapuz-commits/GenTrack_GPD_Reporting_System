#!/usr/bin/env python3
"""
Create a proper drawn signature for JMM_MATA to replace the typed signature
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

def create_realistic_drawn_signature(name, width=400, height=150):
    """Create a realistic hand-drawn style signature"""
    # Create image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Use a more script-like approach for the signature
    # Simulate hand-drawn curves and flourishes
    
    # Draw the signature with curves and flourishes
    # This simulates a more realistic hand-drawn signature
    
    # Start with the first letter (larger and more stylized)
    start_x = 50
    start_y = height // 2
    
    # Draw "J" with flourish
    draw.arc([start_x, start_y-30, start_x+40, start_y+10], 180, 360, fill='#1e40af', width=3)
    draw.line([start_x+20, start_y-30, start_x+20, start_y+20], fill='#1e40af', width=3)
    
    # Draw "MM" with connected strokes
    x = start_x + 60
    # First M
    draw.line([x, start_y+20, x, start_y-20], fill='#1e40af', width=2)
    draw.line([x, start_y-20, x+15, start_y], fill='#1e40af', width=2)
    draw.line([x+15, start_y, x+30, start_y-20], fill='#1e40af', width=2)
    draw.line([x+30, start_y-20, x+30, start_y+20], fill='#1e40af', width=2)
    
    # Second M
    x += 40
    draw.line([x, start_y+20, x, start_y-20], fill='#1e40af', width=2)
    draw.line([x, start_y-20, x+15, start_y], fill='#1e40af', width=2)
    draw.line([x+15, start_y, x+30, start_y-20], fill='#1e40af', width=2)
    draw.line([x+30, start_y-20, x+30, start_y+20], fill='#1e40af', width=2)
    
    # Draw underscore with flourish
    x = start_x + 150
    draw.line([start_x, start_y+30, x, start_y+30], fill='#1e40af', width=2)
    
    # Add "MATA" in a more flowing script
    x = start_x + 180
    
    # Draw "MATA" in cursive style
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((x, start_y-10), "MATA", fill='#1e40af', font=font)
    
    # Add some decorative flourishes
    # Top flourish
    draw.arc([start_x-20, start_y-50, start_x+20, start_y-30], 0, 180, fill='#1e40af', width=2)
    
    # Bottom flourish
    draw.arc([x+50, start_y+20, x+90, start_y+40], 180, 360, fill='#1e40af', width=2)
    
    # Save to BytesIO
    output = BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    
    return output.getvalue()

def replace_typed_with_drawn_signature():
    """Replace the typed signature with a drawn signature for JMM_MATA"""
    print("Replacing typed signature with drawn signature for JMM_MATA...")
    
    try:
        # Find the PSR REPORT 2 document
        from reports.models import Document
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
        
        # Delete the existing typed signature if it exists
        try:
            existing_sig = sig_request.signature
            print(f"✅ Found existing signature: {existing_sig.signature_type}")
            existing_sig.delete()
            print("✅ Deleted existing typed signature")
        except DigitalSignature.DoesNotExist:
            print("✅ No existing signature to replace")
        
        # Create a new drawn signature
        signature_image_data = create_realistic_drawn_signature("JMM_MATA")
        
        # Create the digital signature
        digital_signature = DigitalSignature.objects.create(
            signature_request=sig_request,
            signature_type='DRAWN',  # This is the key change!
            signature_data='',  # We're not storing base64 data for this test
            verification_hash=f'drawn-hash-{sig_request.id}',
            width=400,
            height=150,
            ip_address='127.0.0.1',
            user_agent='Signature Replacement Script'
        )
        
        # Save the signature image
        filename = f"drawn_signature_{sig_request.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.png"
        digital_signature.signature_image.save(
            filename,
            ContentFile(signature_image_data),
            save=True
        )
        
        print(f"✅ Created drawn signature for {sig_request.signer_name}")
        print(f"✅ Signature type: {digital_signature.signature_type}")
        print(f"✅ Image URL: {digital_signature.signature_image.url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error replacing signature: {e}")
        return False

def verify_signature_replacement():
    """Verify that the signature was replaced correctly"""
    print("\nVerifying signature replacement...")
    
    try:
        from reports.models import Document
        doc = Document.objects.filter(title='PSR REPORT 2').first()
        sig_request = SignatureRequest.objects.filter(
            document=doc,
            signer_name='JMM_MATA'
        ).first()
        
        if sig_request:
            try:
                digital_sig = sig_request.signature
                print(f"✅ Signature verification:")
                print(f"   - Signer: {sig_request.signer_name}")
                print(f"   - Document: {sig_request.document.title}")
                print(f"   - Type: {digital_sig.signature_type}")
                print(f"   - Image: {digital_sig.signature_image.url}")
                print(f"   - File exists: {os.path.exists(digital_sig.signature_image.path)}")
                
                if digital_sig.signature_type == 'DRAWN':
                    print("✅ SUCCESS: Signature is now DRAWN type!")
                    return True
                else:
                    print(f"❌ FAIL: Signature is still {digital_sig.signature_type} type")
                    return False
                    
            except DigitalSignature.DoesNotExist:
                print("❌ No digital signature found")
                return False
        else:
            print("❌ Signature request not found")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying signature: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Replacing Typed Signature with Drawn Signature\n")
    
    # Replace the signature
    replacement_success = replace_typed_with_drawn_signature()
    
    if replacement_success:
        # Verify the replacement
        verification_success = verify_signature_replacement()
        
        if verification_success:
            print("\n🎉 SUCCESS! Signature replacement complete!")
            print("\nNow when you view signatures for 'PSR REPORT 2':")
            print("✅ JMM_MATA should show a hand-drawn signature image")
            print("✅ Type should show 'Hand Drawn' instead of 'Typed Text'")
            print("✅ You should see an actual signature drawing")
            
            print("\n📋 To test:")
            print("1. Refresh the Document Manager page")
            print("2. Click 'View Signatures' on 'PSR REPORT 2'")
            print("3. You should now see a drawn signature instead of typed text")
        else:
            print("\n⚠️  Signature replacement failed verification")
    else:
        print("\n❌ Failed to replace signature")