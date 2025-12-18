#!/usr/bin/env python3
import os
import django
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oilmill_backend.settings')
django.setup()

# Test authentication
user = authenticate(username='admin', password='admin123')
if user:
    print(f"✅ Authentication successful: {user.username}, is_staff: {user.is_staff}")
else:
    print("❌ Authentication failed")
    
# Check user exists
from django.contrib.auth.models import User
try:
    admin_user = User.objects.get(username='admin')
    print(f"✅ User exists: {admin_user.username}, is_staff: {admin_user.is_staff}")
    print(f"Password check: {admin_user.check_password('admin123')}")
except User.DoesNotExist:
    print("❌ Admin user does not exist")