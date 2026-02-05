from backend_python.db import get_db_connection

db = get_db_connection()
cursor = db.cursor()
try:
    cursor.execute('ALTER TABLE donations ADD COLUMN photo_filename VARCHAR(255)')
    db.commit()
    print('✅ Column photo_filename added successfully')
except Exception as e:
    if 'Duplicate column' in str(e):
        print('✅ Column photo_filename already exists')
    else:
        print(f'Error: {e}')
finally:
    cursor.close()
    db.close()
