import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="helpreach_db"
    )
    cursor = conn.cursor()
    
    # Add received_at column if it doesn't exist
    alter_query = """
    ALTER TABLE claimed_donations 
    ADD COLUMN received_at TIMESTAMP NULL DEFAULT NULL
    """
    
    cursor.execute(alter_query)
    conn.commit()
    print("✅ Column 'received_at' added successfully to claimed_donations table!")
    
except mysql.connector.Error as err:
    if "Duplicate column name" in str(err):
        print("⚠️ Column 'received_at' already exists in the table.")
    else:
        print(f"❌ Error: {err}")
        
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
