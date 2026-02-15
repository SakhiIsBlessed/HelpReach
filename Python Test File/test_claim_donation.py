#!/usr/bin/env python3
import requests
import json

print("=" * 70)
print("🧪 TESTING DONATION CLAIM WITH EMAIL NOTIFICATION")
print("=" * 70)

# Example: Claim donation ID 1 by NGO ID 1
donation_id = 1
ngo_id = 1

print(f"\n📋 Test Parameters:")
print(f"   Donation ID: {donation_id}")
print(f"   NGO ID: {ngo_id}")
print(f"   Backend URL: http://127.0.0.1:5000")

print("\n" + "-" * 70)
print("Sending claim request...")
print("-" * 70)

try:
    response = requests.post(
        "http://127.0.0.1:5000/api/claim-donation",
        json={"donation_id": donation_id, "ngo_id": ngo_id},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📥 Response Body: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: Donation claimed!")
        print("\nCheck your backend terminal for email sending logs:")
        print("  Look for: '📧 Sending email to...'")
        print("  Look for: '✅ Email sent successfully to...'")
    else:
        print(f"\n❌ ERROR: {response.json()}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to backend!")
    print("   Make sure the backend is running at http://127.0.0.1:5000")
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 70)
