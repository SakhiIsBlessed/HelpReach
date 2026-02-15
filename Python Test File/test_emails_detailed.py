#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')

print("\n" + "=" * 70)
print("🧪 DIRECT TEST OF CLAIM FUNCTIONALITY")
print("=" * 70)

# Direct test without HTTP
from db import get_db_connection
from email_service import send_email

donation_id = 17  # Using jeans donation ID from database check
ngo_id = 1

db = get_db_connection()
cursor = db.cursor(dictionary=True)

print(f"\nTesting donation claim {donation_id} by NGO {ngo_id}...\n")

# Check if already claimed
cursor.execute("""
    SELECT id FROM claimed_donations 
    WHERE donation_id = %s AND ngo_id = %s
""", (donation_id, ngo_id))

if cursor.fetchone():
    print("❌ Already claimed!")
else:
    # Get donation details
    cursor.execute("""
        SELECT d.id, d.title, d.description, d.quantity, d.donor_id, u.name as donor_name, u.email as donor_email
        FROM donations d
        JOIN users u ON d.donor_id = u.id
        WHERE d.id = %s
    """, (donation_id,))

    donation = cursor.fetchone()
    
    # Get NGO details
    cursor.execute("SELECT name, contact_email FROM ngos WHERE id = %s", (ngo_id,))
    ngo = cursor.fetchone()
    
    if donation and ngo:
        print(f"Donation: {donation['title']} by {donation['donor_name']}")
        print(f"NGO: {ngo['name']}")
        print("\n" + "-" * 70)
        print("SENDING EMAILS...\n")
        
        # Test NGO email
        ngo_subject = "🎉 Donation Claimed Successfully!"
        ngo_message = f"Hi {ngo['name']}, You claimed: {donation['title']}"
        print(f"📧 NGO Email: {ngo['contact_email']}")
        ngo_result = send_email(ngo['contact_email'], ngo_subject, ngo_message)
        
        # Test Donor email
        donor_subject = "✅ Your Donation Has Been Claimed!"
        donor_message = f"Hi {donation['donor_name']}, Your '{donation['title']}' was claimed by {ngo['name']}"
        print(f"\n📧 Donor Email: {donation['donor_email']}")
        donor_result = send_email(donation['donor_email'], donor_subject, donor_message)
        
        print("\n" + "-" * 70)
        if ngo_result and donor_result:
            print("✅ SUCCESS: Both emails sent!")
        else:
            print("❌ FAILED: One or both emails failed")
    else:
        print("❌ Donation or NGO not found")

cursor.close()
db.close()
print("\n" + "=" * 70 + "\n")
