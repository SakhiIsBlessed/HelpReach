Backend (PHP + MySQL) setup
=================================

This folder contains a minimal PHP backend scaffold for HelpReach.

What is included
- `config.php` - database credentials (edit with your values)
- `db.php` - mysqli connection helper
- `schema.sql` - SQL to create database and tables
- `register.php` - user registration (POST)
- `login.php` - user login (POST) - starts session
- `logout.php` - ends session
- `post_donation.php` - create a donation (POST)
- `get_donations.php` - returns JSON list of donations (GET)

Quick start (local)
1. Install PHP and MySQL (or use XAMPP/MAMP/WAMP).
2. Create a database and user, or run the `schema.sql` file to create tables:
   - mysql -u root -p < backend/schema.sql
3. Edit `backend/config.php` and set your DB credentials.
4. Run a local PHP server from the repo root for testing:
   - From PowerShell:
     ```powershell
     cd 'C:\Users\ASUS\OneDrive\Documents\GitHub\HelpReach'
     php -S localhost:8000
     ```
   - The backend endpoints will be reachable under `http://localhost:8000/backend/*.php`.

XAMPP-specific quick start
1) Install XAMPP for Windows
   - https://www.apachefriends.org → download and run the XAMPP installer.
   - Keep default components (Apache, MySQL, PHP, phpMyAdmin).
2) Start Apache and MySQL using the XAMPP Control Panel.
3) Verify: open `http://localhost/` and `http://localhost/phpmyadmin` in your browser.
4) Create the database (phpMyAdmin or SQL):
   - Database name: `helpreach_db` (collation `utf8mb4_general_ci`)
   - Optional: create a dedicated DB user (recommended):
     ```sql
     CREATE DATABASE helpreach_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
     CREATE USER 'helpreach_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
     GRANT ALL PRIVILEGES ON helpreach_db.* TO 'helpreach_user'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - Or import the `backend/schema.sql` file via phpMyAdmin → Import.
5) Copy project to XAMPP `htdocs` (or create an Apache alias)
   - Folder: `C:\xampp\htdocs\helpreach\`
   - Copy the repository files there (or only the `public` files and `backend` folder). Your site will be at `http://localhost/helpreach/`.
6) Configure `backend/config.php`:
   - For XAMPP default MySQL root (no password):
     ```php
     define('DB_USER','root');
     define('DB_PASS','');
     ```
   - If you created `helpreach_user`, set those credentials instead.
7) Import schema (if not done): use phpMyAdmin → SQL tab or the CLI:
   ```powershell
   mysql -u root -p < backend/schema.sql
   ```
8) Restart Apache after any `php.ini` changes (e.g. upload limits).

Testing endpoints (example PowerShell / curl)
```powershell
# Register (creates session cookie)
curl -X POST -d "name=Test&email=test@example.com&password=pass123" http://localhost/helpreach/backend/register.php -c cookies.txt

# Login
curl -X POST -d "email=test@example.com&password=pass123" http://localhost/helpreach/backend/login.php -c cookies.txt

# Post donation (use saved cookie to authenticate)
curl -X POST -d "title=Food&description=Leftovers&quantity=20&pickup_info=Noon" http://localhost/helpreach/backend/post_donation.php -b cookies.txt

# List donations
curl http://localhost/helpreach/backend/get_donations.php
```

Useful php.ini settings (increase upload size for images):
```
upload_max_filesize = 16M
post_max_size = 32M
```

Notes
- If Apache won't start, port 80/443 may be in use. Stop the conflicting app or change Apache ports.
- For local dev XAMPP root often has no password; for production always use a dedicated DB user and secure credentials.


Security notes
- Use HTTPS in production.
- Move DB credentials to environment variables when deploying.
- Validate and sanitize all inputs.

Next steps I can do for you
- Wire `donate.html` and `login.html` forms to call these endpoints.
- Add file upload handling for donation images.
- Add NGO registration endpoints and admin verification flow.

If you'd like me to scaffold further (AJAX wiring, uploads, migrations), tell me and I'll continue.
