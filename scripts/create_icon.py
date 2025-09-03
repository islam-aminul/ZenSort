#!/usr/bin/env python3
"""Generate ZenSort icon files"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_icon():
    # Create 256x256 base image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw folder icon
    folder_color = (52, 152, 219)  # Blue
    draw.rectangle([40, 80, 216, 200], fill=folder_color)
    draw.rectangle([40, 60, 120, 80], fill=folder_color)
    
    # Draw sorting arrows
    arrow_color = (255, 255, 255)
    # Right arrow
    draw.polygon([(160, 120), (180, 140), (160, 160)], fill=arrow_color)
    # Down arrow  
    draw.polygon([(120, 120), (140, 140), (100, 140)], fill=arrow_color)
    
    return img

def main():
    # Create assets directory
    assets_dir = Path(__file__).parent.parent / 'assets'
    assets_dir.mkdir(exist_ok=True)
    
    # Generate base icon
    icon = create_icon()
    
    # Save PNG
    icon.save(assets_dir / 'icon.png')
    
    # Save ICO (Windows)
    icon.save(assets_dir / 'icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("Icons created successfully!")

if __name__ == '__main__':
    main()