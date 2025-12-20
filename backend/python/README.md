Python Flask backend (MySQL)
=================================

Quick start (Windows / PowerShell)
1. Create a virtual environment and install dependencies:
```powershell
cd 'C:\Users\ASUS\OneDrive\Documents\GitHub\HelpReach\backend\python'
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Configure database credentials: create a `.env` file in this folder with:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=helpreach_db
DB_USER=root
DB_PASS=
SECRET_KEY=change_this_secret
UPLOAD_FOLDER=../uploads
```

3. Create uploads folder (project root) and ensure writable:
```powershell
mkdir ..\uploads
```

4. Ensure MySQL database exists and import `backend/schema.sql` (or let Flask create tables automatically):
```powershell
# import via mysql client
mysql -u root -p helpreach_db < ..\schema.sql
```

5. Run the app:
```powershell
python app.py
# or set FLASK_APP and use flask run
```

API endpoints (examples)
- POST `/api/register` form/json: name,email,password
- POST `/api/login` form/json: email,password
- GET `/api/logout` or POST `/api/logout`
- GET `/api/donations` — list
- POST `/api/donations` multipart/form-data or JSON (requires session): title,description,quantity,pickup_info, photos[]

Notes
- Uses SQLAlchemy and will call `db.create_all()` automatically on first request (good for dev). For production, use migrations.
- Configure `.env` with your MySQL credentials.
