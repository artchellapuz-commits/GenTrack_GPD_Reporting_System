#!/usr/bin/env python3
"""
Test script to check filename generation for signature files.
"""

import os
import glob

def test_filename_generation():
    """Test filename generation for C.C. AMIGABLE JR."""
    print("🔍 Testing Filename Generation")
    print("=" * 40)
    
    signatory_name = "C.C. AMIGABLE JR."
    print(f"Original name: {signatory_name}")
    
    # Generate filename like the serializer does
    base_filename = signatory_name.lower().replace(' ', '_').replace('.', '_')
    print(f"Base filename: {base_filename}")
    
    # Try multiple filename patterns
    patterns = [
        f"{base_filename}_signature.png",
        f"{base_filename}_signature.jpg",
        f"{base_filename}_signature.jpeg",
    ]
    
    print(f"\nExpected patterns:")
    for pattern in patterns:
        print(f"  - {pattern}")
    
    # Check what files actually exist
    admin_signatures_dir = "npc-reporting-system/backend/media/admin_signatures"
    print(f"\nActual files in {admin_signatures_dir}:")
    
    if os.path.exists(admin_signatures_dir):
        files = os.listdir(admin_signatures_dir)
        cc_files = [f for f in files if 'cc' in f.lower() or 'amigable' in f.lower()]
        for file in cc_files:
            print(f"  - {file}")
        
        # Test glob pattern
        glob_pattern = os.path.join(admin_signatures_dir, f"{base_filename}*signature*")
        print(f"\nGlob pattern: {glob_pattern}")
        matching_files = glob.glob(glob_pattern)
        print(f"Glob matches: {len(matching_files)}")
        for match in matching_files:
            print(f"  - {os.path.basename(match)}")
            
        # Test broader glob pattern
        broad_pattern = os.path.join(admin_signatures_dir, "*amigable*")
        print(f"\nBroad pattern: {broad_pattern}")
        broad_matches = glob.glob(broad_pattern)
        print(f"Broad matches: {len(broad_matches)}")
        for match in broad_matches:
            print(f"  - {os.path.basename(match)}")
    else:
        print(f"❌ Directory not found: {admin_signatures_dir}")

if __name__ == "__main__":
    test_filename_generation()