#!/usr/bin/env python3
import requests
import json

print("\n" + "=" * 70)
print("🧪 TEST DONATION CLAIM #3")
print("=" * 70)

donation_id = 3
ngo_id = 1

print(f"\nAttempting to claim donation {donation_id} by NGO {ngo_id}...\n")

try:
    response = requests.post(
        "http://127.0.0.1:5000/api/claim-donation",
        json={"donation_id": donation_id, "ngo_id": ngo_id}
    )
    
    if response.status_code == 200:
        print("✅ SUCCESS!\n")
        print(json.dumps(response.json(), indent=2))
        print("\n⬇️  BACKEND LOGS SHOULD SHOW:")
        print("  📋 CLAIM DONATION REQUEST:")
        print("  📧 Sending email to NGO at: smitatapre2104@gmail.com")
        print("  📧 Email sent successfully to: smitatapre2104@gmail.com")
        print("  📧 Sending email to Donor at: sakhitapre9@gmail.com")
        print("  📧 Email sent successfully to: sakhitapre9@gmail.com")
        print("  ✅ Donation claimed successfully!")
    else:
        print(f"❌ Error {response.status_code}:")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70 + "\n")
