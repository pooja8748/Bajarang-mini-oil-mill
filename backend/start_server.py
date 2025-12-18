#!/usr/bin/env python3
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oilmill_backend.settings')
    
    # Set default Razorpay keys if not provided
    if not os.environ.get('RAZORPAY_KEY_ID'):
        os.environ['RAZORPAY_KEY_ID'] = 'rzp_test_dummy'
    if not os.environ.get('RAZORPAY_KEY_SECRET'):
        os.environ['RAZORPAY_KEY_SECRET'] = 'dummy_secret'
    
    execute_from_command_line(['manage.py', 'runserver'])