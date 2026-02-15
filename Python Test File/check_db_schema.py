#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from db import get_db_connection

db = get_db_connection()
cursor = db.cursor()

print("\n" + "="*70)
print("DONATIONS TABLE FIELDS")
print("="*70)

cursor.execute('DESCRIBE donations')
fields = cursor.fetchall()

for field in fields:
    print(f"  {field[0]:20} | {field[1]}")

cursor.close()
db.close()
