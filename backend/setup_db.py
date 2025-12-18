#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oilmill_backend.settings')
    django.setup()
    
    # Run migrations
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created admin user: username=admin, password=admin123")
    else:
        print("Admin user already exists")