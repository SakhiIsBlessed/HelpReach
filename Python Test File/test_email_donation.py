#!/usr/bin/env python3
"""
Test script to verify email sending on donation
"""
import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("TESTING EMAIL SENDING ON DONATION")
print("=" * 60)

# Step 1: Register a test user
print("\n📝 Step 1: Registering test user...")
register_data = {
    "name": "Test Donor",
    "email": "testdonor@example.com",
    "phone": "9876543210",
    "location": "Test City",
    "password": "test123"
}

try:
    response = requests.post(f"{BASE_URL}/api/register", json=register_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("ok"):
        user_id = result.get("user", {}).get("id")
        user_email = result.get("user", {}).get("email")
        print(f"✅ User registered with ID: {user_id}, Email: {user_email}")
    else:
        print(f"❌ Registration failed: {result.get('message')}")
        exit(1)
except Exception as e:
    print(f"❌ Error during registration: {e}")
    exit(1)

# Step 2: Submit a donation
print("\n🎁 Step 2: Submitting donation...")
donation_data = {
    "title": "Food Supplies for Families",
    "description": "Donating rice and essential food items",
    "quantity": "50 kg",
    "pickup_info": "123 Main St | 2026-01-18 14:00",
    "donor_id": user_id,
    "donor_email": user_email  # Email from registered user
}

try:
    response = requests.post(f"{BASE_URL}/api/donations", json=donation_data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    if result.get("ok"):
        print(f"✅ Donation submitted successfully!")
        print(f"\n📧 Check your email ({user_email}) for a thank-you message!")
        print(f"📊 Donation submitted by user ID: {user_id}")
    else:
        print(f"❌ Donation failed: {result.get('message')}")
except Exception as e:
    print(f"❌ Error during donation: {e}")
    exit(1)

print("\n" + "=" * 60)
print("TEST COMPLETE - Check backend console for email logs")
print("=" * 60)
time.sleep(2)
