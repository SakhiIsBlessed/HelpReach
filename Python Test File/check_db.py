#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend_python')
from db import get_db_connection

db = get_db_connection()
cursor = db.cursor()

# Check if claimed_donations table exists
cursor.execute("""
    SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = 'helpreach_db' AND TABLE_NAME = 'claimed_donations'
""")

if cursor.fetchone():
    print("✅ claimed_donations table already exists")
else:
    print("❌ claimed_donations table does not exist - creating it now...")
    
    cursor.execute("""
        CREATE TABLE claimed_donations (
            id INT PRIMARY KEY AUTO_INCREMENT,
            donation_id INT NOT NULL,
            ngo_id INT NOT NULL,
            claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (donation_id) REFERENCES donations(id) ON DELETE CASCADE,
            FOREIGN KEY (ngo_id) REFERENCES ngos(id) ON DELETE CASCADE,
            UNIQUE KEY unique_claim (donation_id, ngo_id)
        )
    """)
    db.commit()
    print("✅ claimed_donations table created successfully")

cursor.close()
db.close()
