#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')

print("\n" + "=" * 70)
print("🧪 TESTING CLAIM DONATION DIRECTLY (NO HTTP)")
print("=" * 70)

from db import get_db_connection
from email_service import send_email

# Simulate what happens when donation is claimed
db = get_db_connection()
cursor = db.cursor(dictionary=True)

donation_id = 1
ngo_id = 1

print(f"\n📋 Fetching donation {donation_id} and NGO {ngo_id} details...")

# Get donation details
cursor.execute("""
    SELECT d.id, d.title, d.description, d.quantity, d.donor_id, u.name as donor_name, u.email as donor_email
    FROM donations d
    JOIN users u ON d.donor_id = u.id
    WHERE d.id = %s
""", (donation_id,))

donation = cursor.fetchone()
if not donation:
    print("❌ Donation not found!")
else:
    print(f"✅ Donation found: {donation['title']} by {donation['donor_name']}")
    
    # Get NGO details
    cursor.execute("SELECT name, contact_email FROM ngos WHERE id = %s", (ngo_id,))
    ngo = cursor.fetchone()
    
    if not ngo:
        print("❌ NGO not found!")
    else:
        print(f"✅ NGO found: {ngo['name']} - {ngo['contact_email']}")
        
        print("\n" + "-" * 70)
        print("SENDING EMAILS...")
        print("-" * 70)
        
        # Send email to NGO
        ngo_subject = "🎉 Donation Claimed Successfully!"
        ngo_message = f"""Hi {ngo['name']},
        
Great news! You have successfully claimed: {donation['title']}
        
Best regards, HelpReach Team"""
        
        print(f"\n📧 SENDING EMAIL TO NGO:")
        print(f"   To: {ngo['contact_email']}")
        ngo_result = send_email(ngo['contact_email'], ngo_subject, ngo_message)
        print(f"   Result: {ngo_result}")
        
        # Send email to Donor
        donor_subject = "✅ Your Donation Has Been Claimed!"
        donor_message = f"""Hi {donation['donor_name']},
        
Great news! Your donation '{donation['title']}' has been claimed by {ngo['name']}
        
Best regards, HelpReach Team"""
        
        print(f"\n📧 SENDING EMAIL TO DONOR:")
        print(f"   To: {donation['donor_email']}")
        donor_result = send_email(donation['donor_email'], donor_subject, donor_message)
        print(f"   Result: {donor_result}")
        
        print("\n" + "-" * 70)
        if ngo_result and donor_result:
            print("✅ SUCCESS: Both emails sent successfully!")
        else:
            print("⚠️  WARNING: One or both emails failed to send")
            print(f"   NGO Email: {'✅' if ngo_result else '❌'}")
            print(f"   Donor Email: {'✅' if donor_result else '❌'}")

cursor.close()
db.close()

print("=" * 70 + "\n")
