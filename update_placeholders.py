#!/usr/bin/env python
"""
Script to update all placeholder images to black color
Run this with: python manage.py shell < update_placeholders.py
Or: python update_placeholders.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Product
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Create a black placeholder image with text
def create_black_placeholder_image():
    """Create a black placeholder image with white text"""
    # Create black image
    img = Image.new('RGB', (400, 400), color='#000000')
    draw = ImageDraw.Draw(img)
    
    # Try to add text (optional - if font is available)
    try:
        # Try to use a default font
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except:
        try:
            font = ImageFont.load_default()
        except:
            font = None
    
    # Add white text
    text = "No Image"
    if font:
        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((400 - text_width) // 2, (400 - text_height) // 2)
        draw.text(position, text, fill='#ffffff', font=font)
    else:
        # Fallback: just draw a simple white rectangle in center
        draw.rectangle([150, 180, 250, 220], fill='#ffffff', outline='#ffffff')
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return ImageFile(buffer, name='placeholder.png')

# Update all products with placeholder images
print("Updating placeholder images to black...")
black_placeholder = create_black_placeholder_image()

products_updated = 0
for product in Product.objects.all():
    # Check if product has a placeholder image
    if product.image and ('placeholder' in product.image.name.lower() or product.image.name.endswith('.png')):
        try:
            # Save new black placeholder
            product.image.save(f'placeholder_{product.id}.png', black_placeholder, save=True)
            products_updated += 1
            print(f"Updated placeholder for: {product.name}")
        except Exception as e:
            print(f"Error updating {product.name}: {e}")

print(f"\n✅ Updated {products_updated} product placeholder images to black!")
print(f"Total Products: {Product.objects.count()}")

