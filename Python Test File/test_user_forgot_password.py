#!/usr/bin/env python3
"""
Test script for USER forgot password OTP system (index.html)
Tests the new /api/user/forgot-password/ endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# Test user email from the database
TEST_EMAIL = "sakhitapre9@gmail.com"

print("=" * 60)
print("🧪 TESTING USER FORGOT PASSWORD OTP SYSTEM")
print("=" * 60)

# ==================== TEST 1: Request OTP ====================
print("\n📧 TEST 1: Request OTP")
print("-" * 60)

response = requests.post(
    f"{BASE_URL}/api/user/forgot-password/request-otp",
    json={"email": TEST_EMAIL}
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        token = data.get("token")
        print(f"✅ OTP requested successfully!")
        print(f"📌 Token: {token}")
    else:
        print(f"❌ Failed: {data.get('error')}")
        exit(1)
else:
    print(f"❌ HTTP Error: {response.status_code}")
    exit(1)

# ==================== TEST 2: Test Invalid OTP ====================
print("\n\n🔢 TEST 2: Verify Invalid OTP")
print("-" * 60)

response = requests.post(
    f"{BASE_URL}/api/user/forgot-password/verify-otp",
    json={"token": token, "otp": "000000"}
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 401:
    data = response.json()
    print(f"✅ Invalid OTP rejected correctly!")
    print(f"📌 Attempts remaining: {data.get('attempts_remaining')}")
else:
    print(f"⚠️ Unexpected status code")

# ==================== TEST 3: Resend OTP ====================
print("\n\n🔄 TEST 3: Resend OTP")
print("-" * 60)

response = requests.post(
    f"{BASE_URL}/api/user/forgot-password/resend-otp",
    json={"token": token}
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 200:
    data = response.json()
    if data.get("ok"):
        print(f"✅ OTP resent successfully!")
        print(f"Attempts reset to 0, new OTP generated")
    else:
        print(f"❌ Failed: {data.get('error')}")
else:
    print(f"❌ HTTP Error: {response.status_code}")

# ==================== TEST 4: Test Invalid Email ====================
print("\n\n✉️ TEST 4: Request OTP with Invalid Email")
print("-" * 60)

response = requests.post(
    f"{BASE_URL}/api/user/forgot-password/request-otp",
    json={"email": "nonexistent@example.com"}
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 404:
    data = response.json()
    if "Email not found" in data.get("error", ""):
        print(f"✅ Invalid email rejected correctly!")
    else:
        print(f"⚠️ Different error message: {data.get('error')}")
else:
    print(f"❌ Unexpected status code: {response.status_code}")

# ==================== TEST 5: Test Invalid Token ====================
print("\n\n🔐 TEST 5: Verify OTP with Invalid Token")
print("-" * 60)

response = requests.post(
    f"{BASE_URL}/api/user/forgot-password/verify-otp",
    json={"token": "invalid-token-123", "otp": "123456"}
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

if response.status_code == 401:
    data = response.json()
    if "Invalid" in data.get("error", ""):
        print(f"✅ Invalid token rejected correctly!")
    else:
        print(f"⚠️ Different error message: {data.get('error')}")
else:
    print(f"❌ Unexpected status code: {response.status_code}")

print("\n" + "=" * 60)
print("✅ ALL TESTS COMPLETED!")
print("=" * 60)
print("\n📝 NOTES:")
print("- Users must register and have email in 'users' table")
print("- OTP is sent via email (check configured email)")
print("- OTP valid for 10 minutes")
print("- Maximum 3 OTP attempts per request")
print("- 60-second cooldown before resend")
print("- Password must have 8+ chars and 1 special character")
