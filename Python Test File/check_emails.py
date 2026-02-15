#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from db import get_db_connection

# Check donors and NGO emails
db = get_db_connection()
cursor = db.cursor(dictionary=True)

print("=" * 50)
print("📧 DONOR EMAILS IN DATABASE:")
print("=" * 50)
cursor.execute("SELECT id, name, email FROM users LIMIT 5")
donors = cursor.fetchall()
for donor in donors:
    print(f"ID: {donor['id']}, Name: {donor['name']}, Email: {donor['email']}")

print("\n" + "=" * 50)
print("🏢 NGO CONTACT EMAILS IN DATABASE:")
print("=" * 50)
cursor.execute("SELECT id, name, contact_email FROM ngos LIMIT 5")
ngos = cursor.fetchall()
for ngo in ngos:
    print(f"ID: {ngo['id']}, Name: {ngo['name']}, Contact Email: {ngo['contact_email']}")

print("\n" + "=" * 50)
print("🎁 DONATIONS IN DATABASE:")
print("=" * 50)
cursor.execute("""
    SELECT d.id, d.title, d.donor_id, u.email as donor_email 
    FROM donations d
    JOIN users u ON d.donor_id = u.id
    LIMIT 5
""")
donations = cursor.fetchall()
for donation in donations:
    print(f"ID: {donation['id']}, Title: {donation['title']}, Donor Email: {donation['donor_email']}")

cursor.close()
db.close()

print("\n✅ Database check complete. Check your email addresses above.")
