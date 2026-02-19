"""
Create placeholder PWA icons to stop 404 errors
This creates simple colored squares as temporary icons
"""

import os
from pathlib import Path

def create_svg_icon(size, output_path):
    """Create a simple SVG icon and save as file"""
    svg_content = f'''<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{size}" height="{size}" fill="#3b82f6"/>
  <text x="50%" y="50%" font-family="Arial" font-size="{size//3}" fill="white" 
        text-anchor="middle" dominant-baseline="middle" font-weight="bold">NPC</text>
</svg>'''
    
    with open(output_path, 'w') as f:
        f.write(svg_content)
    print(f"✓ Created {output_path}")

def main():
    print("Creating placeholder PWA icons...")
    print()
    
    # Create icons directory
    icons_dir = Path('frontend/public/icons')
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    # Icon sizes needed
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    for size in sizes:
        output_path = icons_dir / f'icon-{size}x{size}.svg'
        create_svg_icon(size, output_path)
    
    print()
    print("=" * 60)
    print("✅ Placeholder icons created!")
    print()
    print("These are temporary SVG icons to stop 404 errors.")
    print()
    print("For proper icons:")
    print("1. Go to https://www.pwabuilder.com/imageGenerator")
    print("2. Upload your logo")
    print("3. Download PNG icons")
    print("4. Replace the SVG files with PNG files")
    print("=" * 60)

if __name__ == '__main__':
    main()
