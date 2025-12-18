#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_create_order():
    """Test order creation"""
    order_data = {
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "customer_phone": "9876543210",
        "shipping_address": "123 Test Street, Test City",
        "notes": "Test order",
        "items": [
            {
                "product": 1,
                "quantity": 2,
                "package_size": "1",
                "unit_type": "Ltr",
                "price": 150.00
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/orders/", json=order_data)
    print(f"Create Order Status: {response.status_code}")
    if response.status_code == 201:
        print(f"Order Created: {response.json()}")
        return response.json()['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_admin_login():
    """Test admin login"""
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/admin/login/", json=login_data)
    print(f"Admin Login Status: {response.status_code}")
    if response.status_code == 200:
        token = response.json()['access']
        print("Admin login successful")
        return token
    else:
        print(f"Login Error: {response.text}")
        return None

def test_admin_orders(token):
    """Test admin orders endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/orders/admin/orders/", headers=headers)
    print(f"Admin Orders Status: {response.status_code}")
    if response.status_code == 200:
        orders = response.json()
        print(f"Total Orders: {len(orders)}")
        for order in orders[:3]:  # Show first 3 orders
            print(f"Order #{order['id']}: {order['customer_name']} - ₹{order['total_amount']}")
    else:
        print(f"Error: {response.text}")

def test_razorpay_order_creation(order_id):
    """Test Razorpay order creation"""
    razorpay_data = {
        "amount": 300.00,
        "order_id": order_id
    }
    
    response = requests.post(f"{BASE_URL}/orders/create-razorpay-order/", json=razorpay_data)
    print(f"Razorpay Order Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Razorpay Order: {response.json()}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("🧪 Testing Bajrang Mini Oil Mill API")
    print("=" * 50)
    
    # Test order creation
    print("\n1. Testing Order Creation...")
    order_id = test_create_order()
    
    # Test admin login
    print("\n2. Testing Admin Login...")
    admin_token = test_admin_login()
    
    # Test admin orders
    if admin_token:
        print("\n3. Testing Admin Orders...")
        test_admin_orders(admin_token)
    
    # Test Razorpay order creation
    if order_id:
        print("\n4. Testing Razorpay Order Creation...")
        test_razorpay_order_creation(order_id)
    
    print("\n✅ API Testing Complete!")