from backend_python.db import get_db_connection

db = get_db_connection()
cursor = db.cursor(dictionary=True)
cursor.execute('SELECT id, title, photo_filename FROM donations ORDER BY id DESC LIMIT 5')
rows = cursor.fetchall()
print('Recent donations:')
for row in rows:
    print(f"ID: {row['id']}, Title: {row['title']}, Photo: {row['photo_filename']}")
cursor.close()
db.close()
