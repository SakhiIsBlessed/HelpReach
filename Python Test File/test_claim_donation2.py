#!/usr/bin/env python3
import requests
import json

print("\n" + "=" * 70)
print("🧪 TESTING DONATION CLAIM #2 WITH EMAIL NOTIFICATION")
print("=" * 70)

# Test with donation ID 2 and NGO ID 1
donation_id = 2
ngo_id = 1

print(f"\n📋 Test Parameters:")
print(f"   Donation ID: {donation_id}")
print(f"   NGO ID: {ngo_id}")

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
    print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: Donation claimed!")
        print("\n📋 BACKEND LOGS - Check the backend terminal window for:")
        print("  📋 CLAIM DONATION REQUEST:")
        print("  📧 Sending email to NGO at: ...")
        print("  📧 Email sent successfully to: ... (NGO)")
        print("  📧 Sending email to Donor at: ...")
        print("  📧 Email sent successfully to: ... (Donor)")
        print("  ✅ Donation claimed successfully!")
    else:
        print(f"\n❌ Error: {response.json()}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 70 + "\n")
