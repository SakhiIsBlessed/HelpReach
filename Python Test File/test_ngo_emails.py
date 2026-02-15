#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from email_service import send_email
from db import get_db_connection

print("\n" + "=" * 70)
print("🧪 TESTING NGO EMAIL NOTIFICATION")
print("=" * 70)

# Test fetching NGOs
db = get_db_connection()
cursor = db.cursor(dictionary=True)
cursor.execute('SELECT id, name, contact_email FROM ngos WHERE contact_email IS NOT NULL')
ngos = cursor.fetchall()

print(f"\n📋 Found {len(ngos)} NGOs:")
for ngo in ngos:
    print(f"  • {ngo['name']}: {ngo['contact_email']}")

# Test sending email
print('\n' + "-" * 70)
print("Testing email notifications...")
print("-" * 70 + "\n")

if ngos:
    for ngo in ngos[:2]:  # Test with first 2 NGOs
        subject = "🎁 New Donation Available: Medical Supplies"
        message = f"""
Hi {ngo['name']},

A new donation has been posted:

📦 Donation: Medical Supplies
   Description: First aid kits
   Quantity: 500

Log in to claim this donation!

Best regards,
HelpReach Team
"""
        print(f"📧 Sending to {ngo['name']}...")
        result = send_email(ngo['contact_email'], subject, message)
        if result:
            print(f"   ✅ Email sent successfully\n")
        else:
            print(f"   ❌ Email failed\n")

cursor.close()
db.close()

print("=" * 70 + "\n")
