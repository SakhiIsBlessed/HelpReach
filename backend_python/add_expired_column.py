import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="helpreach_db"
    )
    cursor = conn.cursor()

    # Add expired_at column if it doesn't exist
    alter_query = """
    ALTER TABLE donations
    ADD COLUMN expired_at TIMESTAMP NULL DEFAULT NULL
    """

    cursor.execute(alter_query)
    conn.commit()
    print("✅ Column 'expired_at' added successfully to donations table!")

except mysql.connector.Error as err:
    if "Duplicate column name" in str(err):
        print("⚠️ Column 'expired_at' already exists in the table.")
    else:
        print(f"❌ Error: {err}")

finally:
    try:
        if conn.is_connected():
            cursor.close()
            conn.close()
    except Exception:
        pass
