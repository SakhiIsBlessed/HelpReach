"""
Test script to verify:
1. Registration saves user ID
2. Login returns user ID
3. Donation uses the correct donor_id
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

# Test data
test_email = f"testuser_{int(time.time())}@test.com"
test_password = "TestPass@123"
test_name = "Test User"
test_location = "Test City"
test_phone = "9876543210"

print("=" * 60)
print("🧪 DONATION FLOW TEST")
print("=" * 60)

# ============= TEST 1: REGISTRATION =============
print("\n[TEST 1] Registration - Should return user ID")
print(f"Registering user: {test_email}")

reg_response = requests.post(
    f"{BASE_URL}/api/register",
    json={
        "name": test_name,
        "email": test_email,
        "password": test_password,
        "location": test_location,
        "phone": test_phone
    }
)

print(f"Status: {reg_response.status_code}")
print(f"Response: {json.dumps(reg_response.json(), indent=2)}")

if reg_response.status_code == 200:
    reg_data = reg_response.json()
    if reg_data.get("user") and reg_data["user"].get("id"):
        registered_user_id = reg_data["user"]["id"]
        print(f"✅ Registration successful! User ID: {registered_user_id}")
    else:
        print("❌ Registration response missing user ID")
        print("Response keys:", reg_data.keys())
else:
    print("❌ Registration failed!")
    exit(1)

# ============= TEST 2: LOGIN =============
print("\n[TEST 2] Login - Should return same user ID")
print(f"Logging in with: {test_email}")

login_response = requests.post(
    f"{BASE_URL}/api/login",
    json={
        "email": test_email,
        "password": test_password
    }
)

print(f"Status: {login_response.status_code}")
print(f"Response: {json.dumps(login_response.json(), indent=2)}")

if login_response.status_code == 200:
    login_data = login_response.json()
    if login_data.get("user") and login_data["user"].get("id"):
        login_user_id = login_data["user"]["id"]
        print(f"✅ Login successful! User ID: {login_user_id}")
        
        # Verify IDs match
        if registered_user_id == login_user_id:
            print(f"✅ IDs match! Both are: {login_user_id}")
        else:
            print(f"❌ IDs don't match! Registration: {registered_user_id}, Login: {login_user_id}")
    else:
        print("❌ Login response missing user ID")
else:
    print("❌ Login failed!")
    exit(1)

# ============= TEST 3: DONATION =============
print("\n[TEST 3] Donation - Should use correct donor_id")
print(f"Creating donation with donor_id: {login_user_id}")

tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
donation_time = "14:00"

donation_response = requests.post(
    f"{BASE_URL}/api/donations",
    json={
        "title": "Test Rice Donation",
        "description": "food",
        "quantity": "25 kg",
        "pickup_info": f"Test Address | {tomorrow} {donation_time}",
        "donor_id": login_user_id,
        "donor_email": test_email
    }
)

print(f"Status: {donation_response.status_code}")
print(f"Response: {json.dumps(donation_response.json(), indent=2)}")

if donation_response.status_code == 200:
    don_data = donation_response.json()
    if don_data.get("ok"):
        print(f"✅ Donation created successfully!")
    else:
        print("❌ Donation creation failed")
else:
    print("❌ Donation request failed!")
    exit(1)

# ============= TEST 4: VERIFY DONATIONS =============
print("\n[TEST 4] Fetching all donations to verify donor_id")

all_donations_response = requests.get(f"{BASE_URL}/api/donations")

print(f"Status: {all_donations_response.status_code}")

if all_donations_response.status_code == 200:
    all_donations = all_donations_response.json()
    
    # Find our donation
    test_donation = None
    for donation in all_donations:
        if donation.get("title") == "Test Rice Donation":
            test_donation = donation
            break
    
    if test_donation:
        print(f"\n📦 Found test donation:")
        print(f"  Title: {test_donation.get('title')}")
        print(f"  Donor ID: {test_donation.get('donor_id')}")
        print(f"  Donor Name: {test_donation.get('donor_name')}")
        print(f"  Description: {test_donation.get('description')}")
        print(f"  Quantity: {test_donation.get('quantity')}")
        print(f"  Pickup Info: {test_donation.get('pickup_info')}")
        
        if test_donation.get("donor_id") == login_user_id:
            print(f"\n✅ SUCCESS! Donation is using correct donor_id: {login_user_id}")
        else:
            print(f"\n❌ FAILURE! Donation donor_id ({test_donation.get('donor_id')}) doesn't match login user ID ({login_user_id})")
    else:
        print("❌ Could not find test donation in the list")
        print(f"Total donations: {len(all_donations)}")
        if all_donations:
            print("Latest donations:")
            for don in all_donations[:3]:
                print(f"  - {don.get('title')} (donor_id: {don.get('donor_id')})")
else:
    print("❌ Failed to fetch donations")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE!")
print("=" * 60)
