#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from db import get_db_connection
from email_service import send_email

print('\n' + '='*70)
print('🧪 TESTING DONATION POSTING & NGO EMAIL NOTIFICATIONS')
print('='*70 + '\n')

db = get_db_connection()
cursor = db.cursor(dictionary=True)

# Get all NGOs
cursor.execute('SELECT id, name, contact_email FROM ngos WHERE contact_email IS NOT NULL')
ngos = cursor.fetchall()

print(f'✅ Found {len(ngos)} NGOs to notify:\n')

title = 'Test Donation - Medical Supplies'
description = 'First aid kits and medical supplies'
quantity = 100
pickup_info = 'Available at HelpReach Center'

for ngo in ngos:
    print(f'   📧 {ngo["name"]}: {ngo["contact_email"]}')
    
print(f'\n📢 Sending NGO notifications...\n')

success_count = 0
for ngo in ngos:
    ngo_subject = f'🎁 New Donation Available: {title}'
    ngo_message = f'Hi {ngo["name"]},\n\nA new donation has been posted!\n\nTitle: {title}\nDescription: {description}\nQuantity: {quantity}\n\nLog in to claim it!\n\nBest regards,\nHelpReach'
    
    try:
        send_email(ngo["contact_email"], ngo_subject, ngo_message)
        print(f'   ✅ Email sent to {ngo["name"]}')
        success_count += 1
    except Exception as e:
        print(f'   ❌ Failed for {ngo["name"]}: {e}')

cursor.close()
db.close()

print(f'\n✅ Successfully notified {success_count}/{len(ngos)} NGOs')
print('='*70 + '\n')
