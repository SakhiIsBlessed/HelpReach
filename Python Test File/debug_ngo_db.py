#!/usr/bin/env python3
"""
Quick debug script to check NGO database
Run this to verify everything is working
"""

import sys
sys.path.insert(0, 'backend_python')

from db import get_db_connection

print("=" * 60)
print("🔍 HelpReach NGO Database Debug Check")
print("=" * 60)

try:
    # Connect to database
    print("\n1️⃣ Connecting to database...")
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    print("✅ Database connected successfully!")
    
    # Check total NGOs
    print("\n2️⃣ Checking NGO counts...")
    cursor.execute("SELECT COUNT(*) as count FROM ngos")
    total = cursor.fetchone()['count']
    print(f"   Total NGOs in database: {total}")
    
    # Check verified NGOs
    cursor.execute("SELECT COUNT(*) as count FROM ngos WHERE verified = 1")
    verified = cursor.fetchone()['count']
    print(f"   Verified NGOs: {verified}")
    
    # Check unverified NGOs
    cursor.execute("SELECT COUNT(*) as count FROM ngos WHERE verified = 0")
    unverified = cursor.fetchone()['count']
    print(f"   Unverified NGOs: {unverified}")
    
    # Show recent NGOs
    print("\n3️⃣ Recent NGOs in database...")
    cursor.execute("SELECT id, name, verified FROM ngos ORDER BY id DESC LIMIT 10")
    recent = cursor.fetchall()
    
    if recent:
        for ngo in recent:
            status = "✅" if ngo['verified'] == 1 else "❌"
            print(f"   {status} ID:{ngo['id']} - {ngo['name']}")
    else:
        print("   ⚠️ No NGOs found!")
    
    # Check API response
    print("\n4️⃣ Checking what API will return...")
    
    if verified > 0:
        cursor.execute("SELECT id, name, address, phone, email FROM ngos WHERE verified = 1 LIMIT 3")
        print("   API will return VERIFIED NGOs:")
        for ngo in cursor.fetchall():
            print(f"   - {ngo['name']} ({ngo['phone']})")
    elif total > 0:
        cursor.execute("SELECT id, name, address, phone, email FROM ngos LIMIT 3")
        print("   API will return ALL NGOs (fallback, no verified ones):")
        for ngo in cursor.fetchall():
            print(f"   - {ngo['name']} ({ngo['phone']})")
    else:
        print("   ⚠️ Database is EMPTY - No NGOs found!")
    
    cursor.close()
    db.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if total == 0:
        print("❌ DATABASE IS EMPTY!")
        print("   Action: Insert test NGOs into database")
    elif verified == 0 and total > 0:
        print("⚠️ ALL NGOs ARE UNVERIFIED")
        print("   Status: API will still show them (fallback enabled)")
        print("   Action: Run: UPDATE ngos SET verified = 1;")
    elif verified > 0:
        print(f"✅ EVERYTHING LOOKS GOOD!")
        print(f"   - {verified} verified NGOs will be displayed")
        print(f"   - {unverified} unverified NGOs won't be shown")
    
    print("\n" + "=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nPossible issues:")
    print("1. MySQL is not running")
    print("2. Database 'helpreach_db' doesn't exist")
    print("3. Wrong credentials in db.py")
    print("4. ngos table doesn't exist")
    print("\n" + "=" * 60)
