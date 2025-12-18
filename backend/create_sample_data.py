#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oilmill_backend.settings')
django.setup()

from products.models import Product, ProductPrice

# Create sample products
products_data = [
    {
        'name_gujarati': 'મગફળીનું તેલ',
        'name_english': 'Groundnut Oil',
        'description': 'Pure groundnut oil extracted using traditional methods',
        'features': ['Cold Pressed', 'Chemical Free', 'Traditional Method']
    },
    {
        'name_gujarati': 'તલનું તેલ',
        'name_english': 'Sesame Oil',
        'description': 'Premium quality sesame oil',
        'features': ['Pure', 'Aromatic', 'Healthy']
    },
    {
        'name_gujarati': 'નારિયેળનું તેલ',
        'name_english': 'Coconut Oil',
        'description': 'Fresh coconut oil',
        'features': ['Virgin', 'Cold Pressed', 'Natural']
    }
]

for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name_english=product_data['name_english'],
        defaults=product_data
    )
    
    if created:
        # Add prices
        ProductPrice.objects.create(
            product=product,
            package_size='1',
            unit_type='Ltr',
            price=150.00
        )
        ProductPrice.objects.create(
            product=product,
            package_size='5',
            unit_type='Ltr',
            price=700.00
        )
        print(f"Created product: {product.name_english}")
    else:
        print(f"Product exists: {product.name_english}")

print("Sample data created successfully!")