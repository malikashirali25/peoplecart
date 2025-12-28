#!/usr/bin/env python
"""
Script to create sample data for PeopleCart
Run this with: python manage.py shell < create_sample_data.py
Or: python create_sample_data.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
django.setup()

from store.models import Category, Product
from django.core.files.images import ImageFile
from io import BytesIO
from PIL import Image

# Create sample categories
categories_data = [
    {'name': 'Fiction'},
    {'name': 'Non-Fiction'},
    {'name': 'Science'},
    {'name': 'History'},
    {'name': 'Biography'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(name=cat_data['name'])
    categories[cat_data['name']] = cat
    if created:
        print(f"Created category: {cat.name}")

# Create a simple placeholder image
def create_placeholder_image():
    """Create a simple placeholder image with black background"""
    img = Image.new('RGB', (400, 400), color='#000000')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return ImageFile(buffer, name='placeholder.png')

# Create sample products
products_data = [
    {
        'name': 'The Great Gatsby',
        'price': 12.99,
        'category': 'Fiction',
        'description': 'A classic American novel by F. Scott Fitzgerald',
        'is_sale': False,
    },
    {
        'name': 'To Kill a Mockingbird',
        'price': 14.99,
        'category': 'Fiction',
        'description': 'Harper Lee\'s masterpiece about justice and childhood',
        'is_sale': True,
        'sale_price': 9.99,
    },
    {
        'name': 'Sapiens: A Brief History of Humankind',
        'price': 18.99,
        'category': 'Non-Fiction',
        'description': 'Yuval Noah Harari\'s exploration of human history',
        'is_sale': False,
    },
    {
        'name': 'A Brief History of Time',
        'price': 15.99,
        'category': 'Science',
        'description': 'Stephen Hawking\'s explanation of the universe',
        'is_sale': True,
        'sale_price': 11.99,
    },
    {
        'name': 'The Diary of Anne Frank',
        'price': 10.99,
        'category': 'History',
        'description': 'The diary of a young girl during World War II',
        'is_sale': False,
    },
    {
        'name': 'Steve Jobs',
        'price': 16.99,
        'category': 'Biography',
        'description': 'Walter Isaacson\'s biography of Apple co-founder',
        'is_sale': False,
    },
    {
        'name': '1984',
        'price': 13.99,
        'category': 'Fiction',
        'description': 'George Orwell\'s dystopian masterpiece',
        'is_sale': True,
        'sale_price': 8.99,
    },
    {
        'name': 'The Catcher in the Rye',
        'price': 11.99,
        'category': 'Fiction',
        'description': 'J.D. Salinger\'s coming-of-age novel',
        'is_sale': False,
    },
]

# Create placeholder image
placeholder_img = create_placeholder_image()

# Create products
for prod_data in products_data:
    category = categories[prod_data['category']]
    
    # Check if product already exists
    product, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'price': prod_data['price'],
            'category': category,
            'description': prod_data['description'],
            'is_sale': prod_data.get('is_sale', False),
            'sale_price': prod_data.get('sale_price', 0),
        }
    )
    
    # Add image if product was just created and doesn't have one
    if created and not product.image:
        product.image.save('placeholder.png', placeholder_img, save=True)
        print(f"Created product: {product.name} with image")
    elif created:
        print(f"Created product: {product.name}")
    else:
        print(f"Product already exists: {product.name}")

print("\n✅ Sample data created successfully!")
print(f"Total Categories: {Category.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

