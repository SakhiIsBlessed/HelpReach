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

Security notes
- Use HTTPS in production.
- Move DB credentials to environment variables when deploying.
- Validate and sanitize all inputs.

Next steps I can do for you
- Wire `donate.html` and `login.html` forms to call these endpoints.
- Add file upload handling for donation images.
- Add NGO registration endpoints and admin verification flow.

If you'd like me to scaffold further (AJAX wiring, uploads, migrations), tell me and I'll continue.
