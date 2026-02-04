from flask import Flask, request, jsonify, send_from_directory  #Flask:Web framework that is use to create backend Api,request:Reads the data sent from fromtend,jsonify:Converts python data into json
from flask_cors import CORS #Cross-Origin Resource Sharing:Allows frontend (html,js) to call backend api
from db import get_db_connection #custom function used to connect to mysql database
import json
try:
    from pywebpush import webpush, WebPushException
except Exception:
    # pywebpush may not be installed in some environments (linting / CI)
    # Provide safe fallbacks so the app can run without the package.
    webpush = None
    class WebPushException(Exception):
        pass
import hashlib # used to securely hashed passwords bcoz we should not store password in plain text
import random # used to generate random OTP
from email_service import send_email
import os
import sys
import time # used for OTP expiry
import uuid # used to generate unique tokens
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='..', static_url_path='') # serves static files from parent directory

# VAPID config (set these in your environment):
VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY')
VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY')
VAPID_CLAIMS = {"sub": os.environ.get('VAPID_SUB', 'mailto:admin@example.com')}

# 📁 File upload configuration
UPLOAD_FOLDER = os.path.join('..', 'uploads', 'donations')
# Documents upload folder for NGO files
UPLOAD_FOLDER_DOCS = os.path.join('..', 'uploads', 'ngo_documents')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_DOC_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt'}

# Create upload folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_DOCS, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_doc_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DOC_EXTENSIONS

# 🔹 Enhanced CORS configuration to support credentials
# For local development allow all origins so static files opened from filesystem or other ports can call APIs.
CORS(
    app,
    origins="*",
    allow_headers=["Content-Type", "X-Requested-With"],
    supports_credentials=True
)

# Dictionary to store OTP temporarily
otp_store = {}

# � Serve uploaded donation photos
@app.route('/uploads/donations/<filename>')
def serve_photo(filename):
    """Serve uploaded donation photos"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# 🗂️ Serve NGO uploaded documents
@app.route('/uploads/ngo_documents/<filename>')
def serve_ngo_doc(filename):
    """Serve uploaded NGO document files"""
    return send_from_directory(UPLOAD_FOLDER_DOCS, filename)

@app.route('/api/ngo/<int:ngo_id>/documents', methods=['GET', 'POST', 'OPTIONS'])
def ngo_documents(ngo_id):
    """Upload or list NGO documents. Authenticated via 'ngo_id' cookie."""
    if request.method == 'OPTIONS':
        return jsonify({"ok": True}), 200

    cookie_ngo_id = request.cookies.get('ngo_id')
    print(f"🔍 /api/ngo/{ngo_id}/documents called. Cookie ngo_id=", cookie_ngo_id)

    if not cookie_ngo_id:
        return {"error": "Not logged in as NGO"}, 401

    if str(cookie_ngo_id) != str(ngo_id):
        return {"error": "Permission denied"}, 403

    # Ensure DB table exists (safe to run repeatedly)
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ngo_documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ngo_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL,
                original_filename VARCHAR(255),
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        db.commit()
    except Exception as e:
        print("❌ Error ensuring ngo_documents table:", e)
    finally:
        try:
            cursor.close()
            db.close()
        except Exception:
            pass


@app.route('/api/vapid_public_key', methods=['GET'])
def vapid_public_key():
    """Return VAPID public key for client subscription."""
    if not VAPID_PUBLIC_KEY:
        return jsonify({"error": "VAPID_PUBLIC_KEY not configured on server"}), 500
    return jsonify({"publicKey": VAPID_PUBLIC_KEY})


def ensure_push_table():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS push_subscriptions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                endpoint TEXT NOT NULL,
                p256dh VARCHAR(255),
                auth VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        ''')
        db.commit()
    except Exception as e:
        print('❌ Error ensuring push_subscriptions table:', e)
    finally:
        try:
            cursor.close()
            db.close()
        except Exception:
            pass


@app.route('/api/subscribe', methods=['POST', 'OPTIONS'])
def api_subscribe():
    if request.method == 'OPTIONS':
        return jsonify({'ok': True}), 200

    data = request.get_json() or {}
    endpoint = data.get('endpoint')
    keys = data.get('keys') or {}
    p256dh = keys.get('p256dh')
    auth_key = keys.get('auth')

    if not endpoint:
        return jsonify({'error': 'Missing subscription endpoint'}), 400

    ensure_push_table()
    try:
        db = get_db_connection()
        cursor = db.cursor()
        # avoid duplicates
        cursor.execute('SELECT id FROM push_subscriptions WHERE endpoint=%s', (endpoint,))
        if cursor.fetchone():
            cursor.close(); db.close()
            return jsonify({'ok': True, 'message': 'Subscription already exists'})

        cursor.execute('INSERT INTO push_subscriptions (endpoint, p256dh, auth) VALUES (%s, %s, %s)', (endpoint, p256dh, auth_key))
        db.commit()
        cursor.close(); db.close()
        return jsonify({'ok': True})
    except Exception as e:
        print('❌ Error saving subscription:', e)
        return jsonify({'error': 'Server error'}), 500


def send_push(subscription_info, payload):
    if not VAPID_PUBLIC_KEY or not VAPID_PRIVATE_KEY:
        print('⚠️ VAPID keys not configured; skipping push')
        return False

    try:
        webpush(
            subscription_info=subscription_info,
            data=json.dumps(payload),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        return True
    except WebPushException as ex:
        print('❌ WebPush error:', repr(ex))
        return False

    # GET -> list documents
    if request.method == 'GET':
        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT id, filename, original_filename, uploaded_at FROM ngo_documents WHERE ngo_id=%s ORDER BY uploaded_at DESC", (ngo_id,))
            docs = cursor.fetchall()
            cursor.close()
            db.close()

            for d in docs:
                d['url'] = f"/uploads/ngo_documents/{d['filename']}"

            return jsonify({"ok": True, "documents": docs})
        except Exception as e:
            print("❌ Error fetching ngo documents:", e)
            return {"error": "Server error"}, 500

    # POST -> upload files
    if 'documents' not in request.files:
        return {"error": "No files uploaded"}, 400

    files = request.files.getlist('documents')
    saved = []

    try:
        db = get_db_connection()
        cursor = db.cursor()

        for file in files:
            if file and file.filename and allowed_doc_file(file.filename):
                orig = secure_filename(file.filename)
                fname = secure_filename(f"{uuid.uuid4()}_{orig}")
                path = os.path.join(UPLOAD_FOLDER_DOCS, fname)
                try:
                    file.save(path)
                    cursor.execute("INSERT INTO ngo_documents (ngo_id, filename, original_filename) VALUES (%s, %s, %s)", (ngo_id, fname, orig))
                    db.commit()
                    doc_id = cursor.lastrowid
                    saved.append({"id": doc_id, "filename": fname, "original_filename": orig, "url": f"/uploads/ngo_documents/{fname}"})
                    print(f"✅ NGO document saved: {fname}")
                except Exception as e:
                    print("❌ Error saving NGO document:", e)
            else:
                print("⚠️  NGO document not allowed or empty:", getattr(file, 'filename', None))

        cursor.close()
        db.close()

        return jsonify({"ok": True, "saved": saved})

    except Exception as e:
        print("❌ Error processing NGO document upload:", e)
        return {"error": "Server error"}, 500

# (Moved static file route to bottom so API routes are matched first)

# ---------------- HOME ----------------
@app.route("/")
def home():#simple test route that tells backend is running
    return {"message": "HelpReach backend running 🚀"} # if you open http://127.0.0.1:5000 you will see this msg

# ---------------- REGISTER ----------------
@app.route("/api/register", methods=["POST", "OPTIONS"]) #This line tells Flask to create an API endpoint at /api/register POST:usrd to register new user
def register():#This function runs whenever /api/register is called
    if request.method == "OPTIONS": #OPTIONS: used to check browser before post,this is used to check cross origin requests
        return jsonify({"ok": True}), 200  # This avoids CORS errors

    try:
        data = request.form if request.form else request.json # read data from the backend if data comes form data use request.form else use request.json

        name = data.get("name") # fetch user input values sent from frontend These match the users table columns
        email = data.get("email")
        password = data.get("password")
        location = data.get("location")
        phone = data.get("phone")

        if not name or not email or not password: #Ensures required fields are not empty if empty return error
            return {"error": "Missing fields"}, 400

        password_hash = hashlib.sha256(password.encode()).hexdigest() #Converts password into a secure hash

        db = get_db_connection() #Connects to the database
        cursor = db.cursor() #cursor is used to execute SQL queries

        try: #Starts error‑handling block,Prevents app crash if database error occurs
            cursor.execute(
                "INSERT INTO users (name, email, password_hash,location,phone) VALUES (%s, %s, %s, %s, %s)", #Inserts new user data into users table
                (name, email, password_hash, location, phone) #%s prevents SQL injection value come from frontend
            )
            db.commit() #Permanently saves data into database
            print(f"✅ User registered: {email}")
            
            # 🔹 Send welcome email after successful registration (non-blocking)
            try:
                send_email(
                    to_email=email,
                    subject="Welcome to HelpReach 🎉",
                    message=f"""
Hello {name},

Welcome to the HelpReach family. We're glad you're here.
You can now start donating items and supporting NGOs to make a real difference.

If you need help getting started, reply to this email and we'll assist you.

Warm regards,
Team HelpReach
"""
                )
            except Exception as email_error:
                print(f"❌ Email error (non-blocking): {email_error}")
                # Don't fail the registration if email fails
            
            # 🔹 FETCH the newly created user
            fetch_cursor = db.cursor(dictionary=True)
            fetch_cursor.execute(
                "SELECT id, name, email, role, phone, location FROM users WHERE email=%s",
                (email,)
            )
            new_user = fetch_cursor.fetchone()
            fetch_cursor.close()
            
            # 🔹 Set cookie with user_id for session management (dev-friendly SameSite)
            response = jsonify({"ok": True, "message": "User registered", "user": new_user})
            response.set_cookie(
    "user_id",
    str(new_user["id"]),
    max_age=86400,
    httponly=True,
    samesite="Lax",  # Lax works better for local testing
    secure=False  # True only on HTTPS
)

            return response
        except Exception as e: #Catches database or server errors, return error msg
            print(f"❌ Database error: {str(e)}")
            return {"error": str(e)}, 500
        finally:
            cursor.close() #Closes database connection,Prevents memory leaks
            db.close() #Executes whether success or error occurs
    except Exception as outer_error:
        print(f"❌ Outer error in register: {str(outer_error)}")
        return {"error": f"Server error: {str(outer_error)}"}, 500

@app.route("/api/debug-cookie")
def debug_cookie():
    return jsonify(dict(request.cookies))
        
# ---------------- LOGIN ----------------
@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.form if request.form else request.json
    email = data.get("email")
    password = data.get("password")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email, role,phone,location
        FROM users
        WHERE email=%s AND password_hash=%s
    """, (email, password_hash))

    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        # 🔹 Send login notification email
        try:
            send_email(
                to_email=user["email"],
                subject="Login Successful – HelpReach",
                message=f"""
Hello {user['name']},

You have successfully logged in to your HelpReach account.

If you did not log in, please reset your password or contact support immediately.

Team HelpReach
"""
            )
        except Exception as e:
            print("❌ Login email error:", e)

        # 🔹 Set cookie with user_id for session management (dev-friendly SameSite)
        response = jsonify({"ok": True, "user": user})
        response.set_cookie(
    "user_id",
    str(user["id"]),
    max_age=86400,
    httponly=True,
    samesite="Lax",  # Lax works better for local testing
    secure=False  # True only on HTTPS
)

        return response


    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- DONATIONS ----------------
@app.route("/api/donations", methods=["GET", "POST", "OPTIONS"])
def api_donations():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    # Debug: show cookies for troubleshooting 401s
    print("🔍 /api/donations called. Cookies:", dict(request.cookies))
    sys.stdout.flush()

    if request.method == "GET":
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT d.*, u.name AS donor_name
            FROM donations d
            JOIN users u ON u.id = d.donor_id
            ORDER BY d.created_at DESC
        """)

        data = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(data)

    # POST
    # 🔐 Get logged-in user ID from cookie (not from request data to prevent spoofing)
    donor_id = request.cookies.get("user_id")
    if not donor_id:
        return {"error": "User not logged in"}, 401
    
    data = request.form if request.form else request.json

    title = data.get("title")
    description = data.get("description")
    quantity = data.get("quantity")
    pickup_info = data.get("pickup_info")
    category = data.get("category")
    pickup_location = data.get("pickup_location")
    photo_filename = None

    # 📸 Handle photo uploads
    if 'photos' in request.files:
        files = request.files.getlist('photos')  # Handle multiple files if uploaded
        if files and files[0]:
            file = files[0]  # Get first file
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                try:
                    file.save(filepath)
                    photo_filename = filename
                    print(f"✅ Photo saved: {filename}")
                except Exception as e:
                    print(f"❌ Error saving photo: {e}")
            else:
                print(f"⚠️  File not allowed or empty: {file.filename if file else 'None'}")
    else:
        print("⚠️  No photos in request.files")

    if not title:
        return {"error": "Missing donation title"}, 400
        

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO donations (title, description, quantity, pickup_info, category, pickup_location, donor_id, photo_filename)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (title, description, quantity, pickup_info, category, pickup_location, donor_id, photo_filename))

    db.commit()
    cursor.close()
    db.close()

    # 🔹 Send thank-you email to logged-in user
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT name, email FROM users WHERE id = %s", (donor_id,))
        user = cursor.fetchone()

        if user and user.get("email"):
            send_email(
                to_email=user["email"],
                subject="Thank you for your donation ❤️",
                message=f"""
Hello {user['name']},

Thank you for your generous donation of "{title}". Your support helps NGOs continue their important work and reach those in need.

We appreciate your kindness. If you would like updates on how your donation is being used, reply to this email or check your dashboard.

With heartfelt gratitude,
Team HelpReach
"""
            )
            print(f"✅ Donation thank-you email sent to {user['email']}")

        cursor.close()
        db.close()

    except Exception as e:
        print("❌ Email error:", e)

    # 🔹 Send notification emails to all registered NGOs
    try:
        db_ngo = get_db_connection()
        cursor_ngo = db_ngo.cursor(dictionary=True)

        print(f"\n📢 NEW DONATION POSTED: {title}")
        
        # Get all NGOs with contact emails
        cursor_ngo.execute("""
            SELECT id, name, contact_email FROM ngos WHERE contact_email IS NOT NULL
        """)
        ngos = cursor_ngo.fetchall()
        
        print(f"   Notifying {len(ngos)} NGOs...\n")
        
        for ngo in ngos:
            ngo_subject = f"🎁 New Donation Available: {title}"
            ngo_message = f"""
Hello {ngo['name']},

A new donation is available on HelpReach and may be relevant to your work. Here are the key details:

Title: {title}
Description: {description or 'N/A'}
Quantity: {quantity}
Pickup Info: {pickup_info or 'Contact donor for details'}

To claim this donation, please log in to your HelpReach Dashboard and follow the claim steps.

Best regards,
Team HelpReach
"""
            
            print(f"   📧 Notifying: {ngo['name']} ({ngo['contact_email']})")
            send_email(ngo['contact_email'], ngo_subject, ngo_message)
        
        cursor_ngo.close()
        db_ngo.close()
        
        print(f"✅ All NGO notification emails sent successfully!\n")

        # 🔔 Send web-push notifications to subscribers about the new donation
        try:
            ensure_push_table()
            db_push = get_db_connection()
            cur_push = db_push.cursor(dictionary=True)
            cur_push.execute('SELECT endpoint, p256dh, auth FROM push_subscriptions')
            subs = cur_push.fetchall()
            cur_push.close(); db_push.close()

            payload = {
                'title': f'New donation: {title}',
                'body': (description or '')[:200],
                'url': '/ngo_index.html'
            }

            print(f"   🔔 Sending web-push to {len(subs)} subscribers...")
            for s in subs:
                sub_obj = {
                    'endpoint': s['endpoint'],
                    'keys': {
                        'p256dh': s['p256dh'],
                        'auth': s['auth']
                    }
                }
                ok = send_push(sub_obj, payload)
                if not ok:
                    print('   ⚠️ Push failed for endpoint:', s['endpoint'])

            print('   ✅ Web-push send complete')
        except Exception as e:
            print('❌ Error sending web-push notifications:', e)

    except Exception as e:
        print(f"❌ NGO notification error: {e}\n")

    return {"ok": True, "message": "Donation added successfully", "photo_filename": photo_filename}


@app.route("/api/active-donations", methods=["GET", "OPTIONS"])
def api_active_donations():
    """Return donations that are not yet claimed (active/pending to claim)."""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Select donations that do not have a matching claimed_donations entry
        cursor.execute("""
            SELECT d.*, u.name AS donor_name
            FROM donations d
            JOIN users u ON u.id = d.donor_id
            LEFT JOIN claimed_donations cd ON cd.donation_id = d.id
            WHERE cd.donation_id IS NULL
            ORDER BY d.created_at DESC
        """)

        data = cursor.fetchall()
        cursor.close()
        db.close()

        return jsonify(data)
    except Exception as e:
        print('❌ Error fetching active donations:', e)
        try:
            cursor.close()
            db.close()
        except Exception:
            pass
        return jsonify([])


@app.route("/api/ngo/register", methods=["POST", "OPTIONS"])
def register_ngo():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    print("📥 Incoming NGO Data:", data)

    name = data.get("orgName")
    description = data.get("description")
    registration_number = data.get("registrationNumber")
    category = data.get("category")
    contact_person = data.get("contactPerson")
    contact_email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")
    password = data.get("password")

    if not name or not registration_number or not contact_email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db_connection()

    try:
        # 🔹 INSERT
        insert_cursor = db.cursor()
        insert_cursor.execute("""
            INSERT INTO ngos
            (name, description, contact_email, registration_number,
             category, contact_person, phone, address, password_hash, verified)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            name, description, contact_email, registration_number,
            category, contact_person, phone, address, password_hash, 1
        ))
        db.commit()
        insert_cursor.close()

        # 🔹 EMAIL (safe)
        try:
            send_email(
                to_email=contact_email,
                subject="NGO Registration Successful ✔️",
                message=f"""Hello {contact_person},

Congratulations — your NGO "{name}" is now registered on HelpReach. You can log in using your registered email and password to manage your profile and view donations.

If you have any questions, reply to this email and we'll assist.

Team HelpReach
"""
            )
        except Exception as email_error:
            print("❌ Email error:", email_error)

        # 🔹 SELECT (buffered cursor FIX)
        select_cursor = db.cursor(dictionary=True, buffered=True)
        select_cursor.execute("""
            SELECT
                id, name, description, registration_number,
                category, contact_person, contact_email,
                phone, address, verified
            FROM ngos
            WHERE contact_email = %s
        """, (contact_email,))

        ngo = select_cursor.fetchone()
        select_cursor.close()

        # 🔹 Create response and set cookie after registration
        response = jsonify({
            "ok": True,
            "ngo": ngo
        })
        
        response.set_cookie(
            "ngo_id",
            str(ngo["id"]),
            httponly=True,
            samesite="Lax",
            max_age=86400 * 7  # 7 days
        )

        return response

    except Exception as e:
        print("❌ DB ERROR:", e)
        return jsonify({"error": "Database error"}), 500

    finally:
        db.close()

# 🔹 Fetch all NGOs for directory
@app.route("/api/ngos", methods=["GET", "OPTIONS"])
def get_all_ngos():
    """Fetch all verified NGOs for directory display"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Fetch all verified NGOs, ordered by ID descending (latest first)
        cursor.execute("""
            SELECT
                id,
                name,
                description,
                address as location,
                category,
                contact_person,
                contact_email,
                phone,
                verified
            FROM ngos
            WHERE verified = 1
            ORDER BY id DESC
        """)
        
        ngos = cursor.fetchall()
        print(f"✅ Found {len(ngos)} verified NGOs")
        
        # If no verified NGOs, fetch all NGOs (fallback)
        if not ngos:
            print("⚠️ No verified NGOs found, fetching all NGOs...")
            cursor.execute("""
                SELECT
                    id,
                    name,
                    description,
                    address as location,
                    category,
                    contact_person,
                    contact_email,
                    phone,
                    verified
                FROM ngos
                ORDER BY id DESC
            """)
            ngos = cursor.fetchall()
            print(f"✅ Found {len(ngos)} total NGOs (including unverified)")
        
        cursor.close()
        db.close()
        
        return jsonify(ngos), 200
        
    except Exception as e:
        print(f"❌ Error fetching NGOs: {e}")
        return jsonify({"error": "Error fetching NGOs"}), 500


@app.route("/api/users", methods=["GET"])
def get_all_users():
    """Return a list of registered users (id, name, email, phone, location, role)."""
    try:
        print("🔍 /api/users called")
        sys.stdout.flush()
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, phone, location, role FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        print(f"   -> returning {len(users)} users")
        sys.stdout.flush()
        cursor.close()
        db.close()
        return jsonify(users), 200
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return jsonify({"error": "Server error"}), 500

# 🔹 Debug endpoint to check NGO database status
@app.route("/api/ngos/debug", methods=["GET"])
def debug_ngos():
    """Debug endpoint - shows all NGOs regardless of status"""
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Count by verified status
        cursor.execute("SELECT COUNT(*) as count FROM ngos WHERE verified = 1")
        verified_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM ngos WHERE verified = 0")
        unverified_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM ngos")
        total_count = cursor.fetchone()['count']
        
        # Get all NGOs
        cursor.execute("SELECT id, name, verified FROM ngos ORDER BY id DESC LIMIT 20")
        recent_ngos = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return jsonify({
            "total": total_count,
            "verified": verified_count,
            "unverified": unverified_count,
            "recent": recent_ngos,
            "status": "✅ Database connected" if total_count >= 0 else "❌ Database error"
        }), 200
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        return jsonify({"error": str(e), "status": "❌ Database connection failed"}), 500

# 🔹 Fetch all NGOs including unverified (for admin/internal use)
@app.route("/api/ngos/all", methods=["GET", "OPTIONS"])
def get_all_ngos_including_unverified():
    """Fetch all NGOs including unverified ones"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT
                id,
                name,
                description,
                address as location,
                category,
                contact_person,
                contact_email,
                phone,
                verified
            FROM ngos
            ORDER BY id DESC
        """)
        
        ngos = cursor.fetchall()
        cursor.close()
        db.close()
        
        return jsonify(ngos), 200
        
    except Exception as e:
        print(f"❌ Error fetching NGOs: {e}")
        return jsonify({"error": "Error fetching NGOs"}), 500


# ---------------- NGO LOGIN ----------------       
@app.route("/api/ngo/login", methods=["POST", "OPTIONS"])
def ngo_login():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    print("🔐 NGO Login Attempt:", data)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # 🔐 Hash password (same as registration)
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
    SELECT
        id,
        name,
        description,
        registration_number,
        category,
        contact_person,
        contact_email,
        phone,
        address,
        verified
    FROM ngos
    WHERE contact_email = %s AND password_hash = %s
""", (email, password_hash))

        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"error": "Invalid email or password"}), 401

        # Optional: block unverified NGOs
        # if ngo["verified"] == 0:
        #     return jsonify({"error": "Your NGO is not verified yet"}), 403

        # ✅ Send login notification email
        try:
            send_email(
                to_email=ngo["contact_email"],
                subject="NGO Login Alert 🔔",
                message=f"""
Hello {ngo['name']},

Your NGO account has just logged in to HelpReach.

If this was not you, please reset your password or contact support immediately.

Team HelpReach
"""
            )
        except Exception as email_err:
            print(f"❌ Email error during login: {email_err}")

        # 🔹 Create response and set cookie
        response = jsonify({
            "ok": True,
            "ngo": ngo
        })
        
        response.set_cookie(
            "ngo_id",
            str(ngo["id"]),
            httponly=True,
            samesite="Lax",
            max_age=86400 * 7  # 7 days
        )

        return response

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


# ================== FORGOT PASSWORD SYSTEM (OTP) ==================


@app.route('/api/test_push', methods=['POST', 'OPTIONS'])
def api_test_push():
    """Trigger a test push notification to all stored subscriptions.
    Use this after a browser has subscribed (open the dashboard and allow notifications).
    Request body (optional): { "title": "Test", "body": "Hello", "url": "/" }
    """
    if request.method == 'OPTIONS':
        return jsonify({'ok': True}), 200

    data = request.get_json() or {}
    title = data.get('title', 'HelpReach — Test Notification')
    body = data.get('body', 'This is a test notification')
    url = data.get('url', '/')

    try:
        ensure_push_table()
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT endpoint, p256dh, auth FROM push_subscriptions')
        subs = cursor.fetchall()
        cursor.close(); db.close()

        payload = { 'title': title, 'body': body, 'url': url }

        sent = 0
        for s in subs:
            sub_obj = { 'endpoint': s['endpoint'], 'keys': { 'p256dh': s['p256dh'], 'auth': s['auth'] } }
            ok = send_push(sub_obj, payload)
            if ok: sent += 1

        return jsonify({'ok': True, 'requested': len(subs), 'sent': sent})
    except Exception as e:
        print('❌ test_push error:', e)
        return jsonify({'error': 'Server error'}), 500


# �🔹 Serve static HTML files (placed at end so API routes take precedence)
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve HTML and other static files from the parent directory"""
    file_path = os.path.join('..', filename)
    if os.path.isfile(file_path):
        return send_from_directory('..', filename)
    return {"error": "File not found"}, 404


# Store OTP tokens and attempts: {token: {email, otp, attempts, expires}}
forgot_password_store = {}

@app.route("/api/ngo/forgot-password/request-otp", methods=["POST", "OPTIONS"])
def request_otp():
    """Request OTP for password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    email = data.get("email")

    if not email:
        return {"error": "Email is required"}, 400

    # Verify email exists in database
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, name FROM ngos WHERE contact_email = %s", (email,))
        ngo = cursor.fetchone()
        cursor.close()
        db.close()

        if not ngo:
            return {"error": "Email not found in our system"}, 404

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        token = str(uuid.uuid4())
        
        # Store OTP with expiry (10 minutes)
        forgot_password_store[token] = {
            "email": email,
            "ngo_id": ngo["id"],
            "otp": otp,
            "attempts": 0,
            "resend_count": 0,
            "expires": time.time() + 600  # 10 minutes
        }

        # Send OTP via email
        try:
            send_email(
                to_email=email,
                subject="🔐 Password Reset OTP - HelpReach",
                message=f"""
Hello {ngo['name']},

You requested to reset your HelpReach password. Your One-Time Password (OTP) is:

{otp}

This OTP is valid for 10 minutes.

Security note:
- Never share this OTP with anyone.
- HelpReach staff will never ask for your OTP.

If you did not request this, please ignore this email or contact support.

Best regards,
Team HelpReach
"""
            )
            print(f"✅ OTP sent to {email}: {otp}")
        except Exception as email_err:
            print(f"❌ OTP Email error: {email_err}")
            return {"error": "Failed to send OTP email"}, 500

        return {
            "ok": True,
            "message": "OTP sent successfully",
            "token": token
        }, 200

    except Exception as e:
        print(f"❌ Request OTP Error: {e}")
        return {"error": "Server error"}, 500


@app.route("/api/ngo/forgot-password/resend-otp", methods=["POST", "OPTIONS"])
def resend_otp():
    """Resend OTP for password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")

    if not token or token not in forgot_password_store:
        return {"error": "Invalid request. Please start over."}, 400

    otp_record = forgot_password_store[token]

    # Check if OTP has expired
    if time.time() > otp_record["expires"]:
        del forgot_password_store[token]
        return {"error": "OTP expired. Please request a new one."}, 400

    # Generate new OTP
    new_otp = str(random.randint(100000, 999999))
    otp_record["otp"] = new_otp
    otp_record["attempts"] = 0  # Reset attempts on resend
    otp_record["resend_count"] += 1
    otp_record["expires"] = time.time() + 600  # Reset expiry

    # Send new OTP for verification
    try:
        send_email(
            to_email=otp_record["email"],
            subject="🔐 New Password Reset OTP - HelpReach",
            message=f"""
Hello,

Here's your new One-Time Password (OTP):

{new_otp}

This OTP is valid for 10 minutes.

Best regards,
Team HelpReach
"""
        )
        print(f"✅ New OTP sent to {otp_record['email']}: {new_otp}")
    except Exception as email_err:
        print(f"❌ Resend OTP Email error: {email_err}")
        return {"error": "Failed to send OTP email"}, 500

    return {
        "ok": True,
        "message": "New OTP sent successfully",
        "token": token
    }, 200


@app.route("/api/ngo/forgot-password/verify-otp", methods=["POST", "OPTIONS"])
def verify_otp():
    """Verify OTP for password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")
    otp = data.get("otp")

    if not token or not otp:
        return {"error": "Token and OTP are required"}, 400

    if token not in forgot_password_store:
        return {"error": "Invalid request. Please start over."}, 400

    otp_record = forgot_password_store[token]

    # Check if OTP has expired
    if time.time() > otp_record["expires"]:
        del forgot_password_store[token]
        return {"error": "OTP expired. Please request a new one."}, 400

    # Check attempts limit (3 max)
    if otp_record["attempts"] >= 3:
        del forgot_password_store[token]
        return {"error": "Maximum OTP attempts exceeded. Please request a new OTP."}, 400

    # Verify OTP
    if otp_record["otp"] != otp:
        otp_record["attempts"] += 1
        print(f"❌ Invalid OTP attempt {otp_record['attempts']}/3 for {otp_record['email']}")
        return {
            "error": f"Invalid OTP. {3 - otp_record['attempts']} attempts remaining."
        }, 400

    # OTP verified! Create verification token for password reset
    verification_token = str(uuid.uuid4())
    forgot_password_store[token]["verified"] = True
    forgot_password_store[token]["verification_token"] = verification_token
    
    print(f"✅ OTP verified successfully for {otp_record['email']}")

    return {
        "ok": True,
        "message": "OTP verified successfully",
        "token": verification_token  # Return new token for password reset
    }, 200


@app.route("/api/ngo/forgot-password/reset-password", methods=["POST", "OPTIONS"])
def reset_password():
    """Reset password after OTP verification"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return {"error": "Token and password are required"}, 400

    # Find the OTP record with this verification token
    otp_record = None
    otp_token = None
    
    for tok, record in forgot_password_store.items():
        if record.get("verification_token") == token and record.get("verified"):
            otp_record = record
            otp_token = tok
            break

    if not otp_record:
        return {"error": "Invalid or expired request. Please start over."}, 400

    if len(new_password) < 8:
        return {"error": "Password must be at least 8 characters"}, 400

    # Update password in database
    db = get_db_connection()
    cursor = db.cursor()

    try:
        ngo_id = otp_record["ngo_id"]
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        cursor.execute(
            "UPDATE ngos SET password_hash = %s WHERE id = %s",
            (password_hash, ngo_id)
        )
        db.commit()

        # Send confirmation email
        try:
            send_email(
                to_email=otp_record["email"],
                subject="✅ Password Reset Successful - HelpReach",
                message=f"""
Hello,

Your HelpReach password has been successfully reset.

If you did not request this change, please contact us immediately at support@helpreach.org.

Stay secure,
Team HelpReach
"""
            )
        except Exception as email_err:
            print(f"❌ Confirmation email error: {email_err}")

        # Clean up the OTP record
        del forgot_password_store[otp_token]

        print(f"✅ Password reset successfully for NGO ID: {ngo_id}")

        return {
            "ok": True,
            "message": "Password reset successfully. Please log in with your new password."
        }, 200

    except Exception as e:
        print(f"❌ Reset Password Error: {e}")
        return {"error": "Failed to reset password"}, 500
    finally:
        cursor.close()
        db.close()


# ================== END FORGOT PASSWORD SYSTEM (NGO) ==================

# ================== FORGOT PASSWORD SYSTEM (REGULAR USERS) ==================

# Store OTP tokens and attempts for users: {token: {email, otp, attempts, expires, verified, verification_token}}
user_forgot_password_store = {}

@app.route("/api/user/forgot-password/request-otp", methods=["POST", "OPTIONS"])
def user_request_otp():
    """Request OTP for user password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    email = data.get("email")

    if not email:
        return {"error": "Email is required"}, 400

    # Verify email exists in users database
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id, name FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user:
            return {"error": "Email not found in our system"}, 404

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        token = str(uuid.uuid4())
        
        # Store OTP with expiry (10 minutes)
        user_forgot_password_store[token] = {
            "email": email,
            "user_id": user["id"],
            "otp": otp,
            "attempts": 0,
            "resend_count": 0,
            "expires": time.time() + 600,  # 10 minutes
            "verified": False
        }

        # Send OTP via email
        try:
            send_email(
                to_email=email,
                subject="🔐 Password Reset OTP - HelpReach",
                message=f"""
Hello {user['name']},

You requested to reset your HelpReach password. Your One-Time Password (OTP) is:

{otp}

This OTP is valid for 10 minutes.

Security note:
- Never share this OTP with anyone.
- HelpReach staff will never ask for your OTP.

If you did not request this, please ignore this email or contact support.

Best regards,
Team HelpReach
"""
            )
            print(f"✅ OTP sent to {email}: {otp}")
        except Exception as email_err:
            print(f"❌ OTP Email error: {email_err}")
            return {"error": "Failed to send OTP email"}, 500

        return {
            "ok": True,
            "message": "OTP sent successfully",
            "token": token
        }, 200

    except Exception as e:
        print(f"❌ Request OTP Error: {e}")
        return {"error": "Server error"}, 500


@app.route("/api/user/forgot-password/verify-otp", methods=["POST", "OPTIONS"])
def user_verify_otp():
    """Verify OTP for user password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")
    otp = data.get("otp")

    if not token or not otp:
        return {"error": "Token and OTP are required"}, 400

    # Find the OTP record
    otp_record = user_forgot_password_store.get(token)
    
    if not otp_record:
        return {"error": "Invalid or expired token"}, 401

    # Check if OTP has expired
    if time.time() > otp_record["expires"]:
        del user_forgot_password_store[token]
        return {"error": "OTP has expired"}, 401

    # Check attempts
    if otp_record["attempts"] >= 3:
        del user_forgot_password_store[token]
        return {"error": "Maximum attempts exceeded. Please request a new OTP"}, 401

    # Verify OTP
    if otp_record["otp"] != otp:
        otp_record["attempts"] += 1
        remaining = 3 - otp_record["attempts"]
        return {
            "error": "Invalid OTP",
            "attempts_remaining": remaining
        }, 401

    # Mark as verified and create verification token
    verification_token = str(uuid.uuid4())
    otp_record["verified"] = True
    otp_record["verification_token"] = verification_token
    
    print(f"✅ OTP verified successfully for {otp_record['email']}")

    return {
        "ok": True,
        "message": "OTP verified successfully",
        "token": verification_token
    }, 200


@app.route("/api/user/forgot-password/resend-otp", methods=["POST", "OPTIONS"])
def user_resend_otp():
    """Resend OTP for user password reset"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")

    if not token:
        return {"error": "Token is required"}, 400

    otp_record = user_forgot_password_store.get(token)
    
    if not otp_record:
        return {"error": "Invalid or expired token"}, 401

    # Generate new OTP and reset attempts
    new_otp = str(random.randint(100000, 999999))
    otp_record["otp"] = new_otp
    otp_record["attempts"] = 0
    otp_record["verified"] = False
    otp_record["expires"] = time.time() + 600

    # Send new OTP
    try:
        send_email(
            to_email=otp_record["email"],
            subject="🔐 New Password Reset OTP - HelpReach",
            message=f"""
Hello,

Here's your new One-Time Password (OTP) for password reset:

{new_otp}

This OTP is valid for 10 minutes.

Best regards,
Team HelpReach
"""
        )
        print(f"✅ New OTP sent to {otp_record['email']}: {new_otp}")
    except Exception as email_err:
        print(f"❌ Resend OTP Email error: {email_err}")
        return {"error": "Failed to send OTP email"}, 500

    return {
        "ok": True,
        "message": "New OTP sent successfully",
        "token": token
    }, 200


@app.route("/api/user/forgot-password/reset-password", methods=["POST", "OPTIONS"])
def user_reset_password():
    """Reset password after OTP verification for regular users"""
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return {"error": "Token and password are required"}, 400

    # Find the OTP record with this verification token
    otp_record = None
    otp_token = None
    
    for tok, record in user_forgot_password_store.items():
        if record.get("verification_token") == token and record.get("verified"):
            otp_record = record
            otp_token = tok
            break

    if not otp_record:
        return {"error": "Invalid or unverified token"}, 401

    # Hash the new password
    password_hash = hashlib.sha256(new_password.encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Update password in users table
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE id = %s",
            (password_hash, otp_record["user_id"])
        )
        db.commit()

        # Send confirmation email
        try:
            send_email(
                to_email=otp_record["email"],
                subject="✅ Password Reset Successful - HelpReach",
                message=f"""
Hello,

Your HelpReach password has been successfully reset.

If you did not request this change, please contact our support team immediately.

Best regards,
Team HelpReach
"""
            )
        except Exception as email_err:
            print(f"❌ Confirmation email error: {email_err}")

        # Clean up
        if otp_token:
            del user_forgot_password_store[otp_token]

        return {
            "ok": True,
            "message": "Password reset successfully. Please log in with your new password."
        }, 200

    except Exception as e:
        print(f"❌ Reset Password Error: {e}")
        return {"error": "Failed to reset password"}, 500
    finally:
        cursor.close()
        db.close()

# ================== END FORGOT PASSWORD SYSTEM (USERS) ==================


# ---------------- NGO PROFILE ----------------
@app.route("/api/ngo/profile/<int:ngo_id>", methods=["GET"])
def get_ngo_profile(ngo_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                id,
                name,
                description,
                registration_number,
                category,
                contact_person,
                contact_email,
                phone,
                address,
                verified,
                created_at
            FROM ngos
            WHERE id = %s
        """, (ngo_id,))

        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"error": "NGO not found"}), 404

        return jsonify({
            "ok": True,
            "ngo": ngo
        })

    except Exception as e:
        print("❌ NGO PROFILE ERROR:", e)
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


@app.route("/api/ngo/me", methods=["GET"])
def get_logged_in_ngo():
    ngo_id = request.cookies.get("ngo_id")

    if not ngo_id:
        return jsonify({"ok": False, "guest": True}), 200

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                id,
                name,
                description,
                registration_number,
                category,
                contact_person,
                contact_email,
                phone,
                address,
                verified
            FROM ngos
            WHERE id = %s
        """, (ngo_id,))

        ngo = cursor.fetchone()

        if not ngo:
            return jsonify({"ok": False, "guest": True}), 200

        return jsonify({
            "ok": True,
            "ngo": ngo
        })

    finally:
        cursor.close()
        db.close()


@app.route("/api/ngo/logout", methods=["POST"])
def ngo_logout():
    response = jsonify({"ok": True})
    response.delete_cookie("ngo_id")
    return response

        
# ---------------- CONTACT ENQUIRY ----------------
@app.route("/api/contact", methods=["POST", "OPTIONS"])
def contact_enquiry():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    inquiry_type = data.get("inquiryType")
    message = data.get("message")

    if not name or not email or not inquiry_type or not message:
        return {"error": "Missing fields"}, 400

    # ✅ Send confirmation email to user
    try:
        send_email(
            to_email=email,
            subject="Enquiry Submitted Successfully ✔️",
            message=f"""
Hello {name},

Thank you for contacting HelpReach. We have received your enquiry and will reply shortly.

Inquiry Type: {inquiry_type}
Message: {message}

If this is urgent, reply to this email or call our support line.

Best regards,
Team HelpReach
"""
        )
    except Exception as e:
        print("❌ Email error:", e)

    return {"ok": True, "message": "Enquiry submitted"}



@app.route("/api/user/login", methods=["POST"])
def user_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = %s AND password_hash = %s
    """, (email, password_hash))

    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401

    resp = jsonify({"ok": True, "user": user})
    resp.set_cookie(
        "user_id",
        str(user["id"]),
        max_age=86400,
        httponly=True,
        samesite="Lax",
        secure=False
    )

    return resp


@app.route("/api/user/me", methods=["GET"])
def user_me():
    user_id = request.cookies.get("user_id")

    if not user_id:
        return jsonify({"ok": False}), 401

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({"ok": False}), 401

    return jsonify({"ok": True, "user": user})


@app.route("/api/user/logout", methods=["POST"])
def user_logout():
    resp = jsonify({"ok": True})
    resp.set_cookie("user_id", "", expires=0)
    return resp


# ============= CLAIM DONATION =============
@app.route("/api/claim-donation", methods=["POST", "OPTIONS"])
def claim_donation():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json
    donation_id = data.get("donation_id")
    ngo_id = data.get("ngo_id")

    print(f"\n📋 CLAIM DONATION REQUEST:")
    print(f"  Donation ID: {donation_id}, NGO ID: {ngo_id}")
    sys.stdout.flush()

    if not donation_id or not ngo_id:
        return jsonify({"error": "Missing donation_id or ngo_id"}), 400

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Check if donation exists and get donation details
        cursor.execute("""
            SELECT d.id, d.title, d.description, d.quantity, d.donor_id, u.name as donor_name, u.email as donor_email
            FROM donations d
            JOIN users u ON d.donor_id = u.id
            WHERE d.id = %s
        """, (donation_id,))
        donation = cursor.fetchone()
        if not donation:
            return jsonify({"error": "Donation not found"}), 404

        # Check if already claimed by this NGO
        cursor.execute("""
            SELECT id FROM claimed_donations 
            WHERE donation_id = %s AND ngo_id = %s
        """, (donation_id, ngo_id))
        
        if cursor.fetchone():
            return jsonify({"error": "You have already claimed this donation"}), 400

        # Get NGO details for email
        cursor.execute("SELECT name, contact_email FROM ngos WHERE id = %s", (ngo_id,))
        ngo = cursor.fetchone()
        if not ngo:
            return jsonify({"error": "NGO not found"}), 404

        # Insert claim record
        insert_cursor = db.cursor()
        insert_cursor.execute("""
            INSERT INTO claimed_donations (donation_id, ngo_id, claimed_at)
            VALUES (%s, %s, NOW())
        """, (donation_id, ngo_id))
        db.commit()
        insert_cursor.close()

        # Send email to NGO
        ngo_subject = "🎉 Donation Claimed Successfully!"
        ngo_message = f"""
Hello {ngo['name']},

You have successfully claimed the donation titled "{donation['title']}".

Please arrange pickup with the donor at your earliest convenience. If you need contact details, reply to this email.

Best regards,
Team HelpReach
"""
        print(f"  📧 Sending email to NGO at: {ngo['contact_email']}")
        
        donor_subject = "✅ Your Donation Has Been Claimed!"
        donor_message = f"""
Hello {donation['donor_name']},

Your donation "{donation['title']}" has been claimed by {ngo['name']}. The NGO will contact you soon to arrange the pickup.

Thank you for making a difference.

Best regards,
Team HelpReach
"""
        sys.stdout.flush()
        ngo_email_sent = send_email(ngo['contact_email'], ngo_subject, ngo_message)
        sys.stdout.flush()

        # Send email to Donor
        donor_subject = "✅ Your Donation Has Been Claimed!"
        donor_message = f"""
Hi {donation['donor_name']},

Wonderful news! Your generous donation has been claimed by an NGO:

📦 Donation Details:
  • Title: {donation['title']}
  • Description: {donation['description'] or 'N/A'}
  • Quantity: {donation['quantity']}
  • NGO Name: {ngo['name']}

The NGO will contact you soon to arrange for the pickup. Thank you for making a difference!

Best regards,
HelpReach Team
        """
        print(f"  📧 Sending email to Donor at: {donation['donor_email']}")
        sys.stdout.flush()
        donor_email_sent = send_email(donation['donor_email'], donor_subject, donor_message)
        sys.stdout.flush()

        print(f"  ✅ Donation claimed successfully!")
        print(f"  NGO Email Sent: {ngo_email_sent}, Donor Email Sent: {donor_email_sent}\n")
        sys.stdout.flush()

        email_status = "Emails sent" if (ngo_email_sent and donor_email_sent) else "Donation claimed but email delivery had issues"
        return jsonify({"ok": True, "message": "Donation claimed successfully", "email_status": email_status})

    except Exception as e:
        print(f"❌ Claim error: {e}")
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


# ============= GET CLAIMED DONATIONS FOR NGO =============
@app.route("/api/ngo/<int:ngo_id>/claimed-donations", methods=["GET"])
def get_claimed_donations(ngo_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                d.id,
                d.title,
                d.description,
                d.quantity,
                d.pickup_info,
                d.category,
                d.pickup_location,
                d.created_at,
                d.donor_id,
                d.photo_filename,
                u.name AS donor_name,
                cd.claimed_at
            FROM claimed_donations cd
            JOIN donations d ON d.id = cd.donation_id
            JOIN users u ON u.id = d.donor_id
            WHERE cd.ngo_id = %s AND cd.received_at IS NULL
            ORDER BY cd.claimed_at DESC
        """, (ngo_id,))

        donations = cursor.fetchall()
        return jsonify(donations)

    except Exception as e:
        print(f"❌ Error fetching claimed donations: {e}")
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


# ============= MARK DONATION AS RECEIVED =============
@app.route("/api/mark-donation-received", methods=["POST"])
def mark_donation_received():
    """Mark a claimed donation as received and move it to history"""
    data = request.json
    donation_id = data.get('donation_id')
    ngo_id = data.get('ngo_id')
    
    if not donation_id or not ngo_id:
        return jsonify({"error": "Missing donation_id or ngo_id"}), 400
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Update claimed_donations table with received_at timestamp
        cursor.execute("""
            UPDATE claimed_donations 
            SET received_at = NOW()
            WHERE donation_id = %s AND ngo_id = %s
        """, (donation_id, ngo_id))
        
        db.commit()
        
        # Get donation and NGO info for email
        cursor.execute("""
            SELECT d.title, d.description, d.quantity, u.name AS donor_name, u.email AS donor_email,
                   n.name AS ngo_name, n.contact_email AS ngo_email
            FROM claimed_donations cd
            JOIN donations d ON d.id = cd.donation_id
            JOIN users u ON u.id = d.donor_id
            JOIN ngos n ON n.id = cd.ngo_id
            WHERE cd.donation_id = %s AND cd.ngo_id = %s
        """, (donation_id, ngo_id))
        
        donation_info = cursor.fetchone()
        
        if donation_info:
            # Send email to donor
            donor_subject = "🎉 Your Donation Has Been Received!"
            donor_message = f"""
Hello {donation_info['donor_name']},

Good news — your donation "{donation_info['title']}" has been received by {donation_info['ngo_name']}.

Thank you for making a positive impact on the community. If you would like confirmation details, reply to this email and we'll assist.

Best regards,
Team HelpReach
"""
            send_email(donation_info['donor_email'], donor_subject, donor_message)
            
            # Send email to NGO
            ngo_subject = "✅ Donation Received - Thank You!"
            ngo_message = f"""
Hello {donation_info['ngo_name']},

Thank you for receiving the donation "{donation_info['title']}".

This donation has been marked as received in the HelpReach system. Thank you for your work in the community.

Best regards,
Team HelpReach
"""
            send_email(donation_info['ngo_email'], ngo_subject, ngo_message)
        
        return jsonify({
            "ok": True,
            "message": "Donation marked as received successfully"
        })
    
    except Exception as e:
        print(f"❌ Error marking donation as received: {e}")
        return jsonify({"error": "Server error"}), 500
    
    finally:
        cursor.close()
        db.close()


# ============= UPDATE DONATION STATUS - PICKED UP =============
@app.route("/api/donation-picked-up", methods=["POST"])
def donation_picked_up():
    """Mark a donation as picked up"""
    data = request.json
    donation_id = data.get('donation_id')
    ngo_id = data.get('ngo_id')
    
    if not donation_id or not ngo_id:
        return jsonify({"error": "Missing donation_id or ngo_id"}), 400
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Update status to PickedUp and store timestamp
        cursor.execute("""
            UPDATE claimed_donations 
            SET status = 'PickedUp', picked_up_at = NOW()
            WHERE donation_id = %s AND ngo_id = %s
        """, (donation_id, ngo_id))
        
        db.commit()
        
        return jsonify({
            "ok": True,
            "message": "Donation marked as picked up successfully",
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    except Exception as e:
        print(f"❌ Error marking donation as picked up: {e}")
        return jsonify({"error": "Server error"}), 500
    
    finally:
        cursor.close()
        db.close()


# ============= UPDATE DONATION STATUS - DELIVERED =============
@app.route("/api/donation-delivered", methods=["POST"])
def donation_delivered():
    """Mark a donation as delivered/completed"""
    data = request.json
    donation_id = data.get('donation_id')
    ngo_id = data.get('ngo_id')
    
    if not donation_id or not ngo_id:
        return jsonify({"error": "Missing donation_id or ngo_id"}), 400
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Update status to Completed
        cursor.execute("""
            UPDATE claimed_donations 
            SET status = 'Completed', received_at = NOW()
            WHERE donation_id = %s AND ngo_id = %s
        """, (donation_id, ngo_id))
        
        db.commit()
        
        # Get donation and NGO info for email notification
        cursor.execute("""
            SELECT d.title, u.name AS donor_name, u.email AS donor_email,
                   n.name AS ngo_name
            FROM claimed_donations cd
            JOIN donations d ON d.id = cd.donation_id
            JOIN users u ON u.id = d.donor_id
            JOIN ngos n ON n.id = cd.ngo_id
            WHERE cd.donation_id = %s AND cd.ngo_id = %s
        """, (donation_id, ngo_id))
        
        donation_info = cursor.fetchone()
        
        if donation_info:
            # Send completion email to donor
            donor_subject = "🎉 Your Donation Journey Complete!"
            donor_message = f"""
Hi {donation_info['donor_name']},

Wonderful news! Your donation has been successfully delivered!

📦 Donation: {donation_info['title']}
✅ Status: Completed
📍 Received by: {donation_info['ngo_name']}

Your generosity is making a real difference in the community. Thank you!

Best regards,
HelpReach Team
            """
            send_email(donation_info['donor_email'], donor_subject, donor_message)
        
        return jsonify({
            "ok": True,
            "message": "Donation marked as delivered successfully",
            "timestamp": str(__import__('datetime').datetime.now())
        })
    
    except Exception as e:
        print(f"❌ Error marking donation as delivered: {e}")
        return jsonify({"error": "Server error"}), 500
    
    finally:
        cursor.close()
        db.close()


# ============= GET DONATION CLAIM STATUS =============
@app.route("/api/donation-claim-status/<int:donation_id>/<int:ngo_id>", methods=["GET"])
def get_donation_claim_status(donation_id, ngo_id):
    """Get the current claim status of a donation"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT id, status, claimed_at, picked_up_at, received_at 
            FROM claimed_donations
            WHERE donation_id = %s AND ngo_id = %s
        """, (donation_id, ngo_id))
        
        claim = cursor.fetchone()
        
        if claim:
            return jsonify({
                "ok": True,
                "claim": claim
            })
        else:
            return jsonify({
                "ok": False,
                "message": "Claim not found"
            }), 404
    
    except Exception as e:
        print(f"❌ Error fetching claim status: {e}")
        return jsonify({"error": "Server error"}), 500
    
    finally:
        cursor.close()
        db.close()


# ============= GET RECEIVED DONATIONS FOR NGO (for history) =============
@app.route("/api/ngo/<int:ngo_id>/received-donations", methods=["GET"])
def get_received_donations(ngo_id):
    """Get all donations received (completed) by an NGO for history display"""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                d.id,
                d.title,
                d.description,
                d.quantity,
                d.pickup_info,
                d.photo_filename,
                d.category,
                d.pickup_location,
                u.name AS donor_name,
                cd.claimed_at,
                cd.received_at
            FROM claimed_donations cd
            JOIN donations d ON d.id = cd.donation_id
            JOIN users u ON u.id = d.donor_id
            WHERE cd.ngo_id = %s AND cd.received_at IS NOT NULL
            ORDER BY cd.received_at DESC
        """, (ngo_id,))

        donations = cursor.fetchall()
        return jsonify(donations)

    except Exception as e:
        print(f"❌ Error fetching received donations: {e}")
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


# Get all claimed donations (for donor dashboard)
@app.route("/api/all-claimed-donations", methods=["GET"])
def get_all_claimed_donations():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT 
                cd.donation_id,
                cd.ngo_id,
                n.name AS ngo_name,
                n.contact_email AS ngo_email,
                cd.claimed_at
            FROM claimed_donations cd
            JOIN ngos n ON n.id = cd.ngo_id
            ORDER BY cd.claimed_at DESC
        """)

        claimed = cursor.fetchall()
        return jsonify(claimed)

    except Exception as e:
        print(f"❌ Error fetching all claimed donations: {e}")
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()


user_name = None

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    global user_name
    msg = request.json.get("message", "").lower()

    # ---------------- GREETINGS ----------------
    if msg in ["hi", "hello", "hey", "hii", "hola"]:
        reply = "Hello 👋 How can I help you today?"

    elif "how are you" in msg:
        reply = "I'm doing great 😊 Thanks for asking! How can I help?"

    elif "good morning" in msg:
        reply = "Good morning ☀️ Hope you have a great day!"

    elif "good evening" in msg:
        reply = "Good evening 🌙 How can I assist you?"

    elif "good night" in msg:
        reply = "Good night 🌙 Take care!"

    # ---------------- NAME HANDLING ----------------
    elif msg.startswith("hi i am ") or msg.startswith("hello i am "):
        user_name = msg.split("i am")[-1].strip().title()
        reply = f"Nice to meet you, {user_name} 😊 How can I help you?"

    elif msg.startswith("my name is "):
        user_name = msg.replace("my name is", "").strip().title()
        reply = f"Hello {user_name}! 👋 What can I do for you?"

    elif "what is my name" in msg:
        reply = f"Your name is {user_name} 😊" if user_name else \
                "I don't know your name yet 😄 Tell me by saying *My name is ...*"

    # ---------------- BOT INFO ----------------
    elif "who are you" in msg:
        reply = "I'm 🤖 HelpReach AI, your assistant for donations and NGOs."

    elif "are you real" in msg:
        reply = "I'm a virtual assistant 😊 but always here to help!"

    elif "where are you from" in msg:
        reply = "I live inside the HelpReach website 🌐"

    elif "how old are you" in msg:
        reply = "I was created recently 😄 but I learn every day!"

    elif msg in ["help", "what can you do", "what can you help with"]:
        reply = (
            "I can help you with:\n"
            "• Login & Register\n"
            "• Donating items\n"
            "• NGO Dashboard\n"
            "• Claiming donations\n"
            "• Account support 😊"
        )

    # ---------------- DONATION QUESTIONS ----------------
    elif "how to donate" in msg:
        reply = "Login → Go to Donate → Fill the donation form."

    elif "what can i donate" in msg:
        reply = "You can donate food, clothes, books, and essentials."

    elif "food donation" in msg:
        reply = "Food donations should be fresh and properly packed."

    elif "clothes donation" in msg:
        reply = "Clothes should be clean and in usable condition."

    elif "donation pickup" in msg:
        reply = "Pickup details depend on the NGO claiming your donation."

    elif "donation safe" in msg:
        reply = "Yes 👍 all donations are visible only to verified NGOs."

    elif "donation status" in msg:
        reply = "You can check donation status from your dashboard."

    elif "donate" in msg:
        reply = "To donate, please login first and fill the donation form."

    # ---------------- NGO QUESTIONS ----------------
    elif "ngo register" in msg:
        reply = "NGOs can register using the NGO Register option."

    elif "ngo dashboard" in msg:
        reply = "The NGO Dashboard shows active donations available to claim."

    elif "ngo history" in msg:
        reply = "NGO History shows donations you have already claimed."

    elif "how ngo claim" in msg:
        reply = "NGOs can claim donations directly from the dashboard."

    elif "ngo verification" in msg:
        reply = "Only verified NGOs can claim donations."

    elif "ngo" in msg:
        reply = "NGOs can view and claim donations posted by donors."

    # ---------------- ACCOUNT ----------------
    elif "register" in msg or "signup" in msg:
        reply = "Click on Register and create your HelpReach account."

    elif "login" in msg:
        reply = "Use your registered email and password to login."

    elif "forgot password" in msg:
        reply = "Use the 'Forgot Password' option on the login page."

    elif "change password" in msg:
        reply = "You can change your password from profile settings."

    elif "delete account" in msg:
        reply = "Please contact support to delete your account."

    elif "logout" in msg:
        reply = "You can logout using the profile menu."

    # ---------------- WEBSITE HELP ----------------
    elif "how this works" in msg or "how website works" in msg:
        reply = "Donors post donations → NGOs claim them → Help reaches people ❤️"

    elif "features" in msg:
        reply = "Main features include donations, NGO dashboard, and notifications."

    # ---------------- POLITE / FUN ----------------
    elif "thank" in msg or "thanks" in msg:
        reply = "You're welcome 😊 Happy to help!"

    elif "bye" in msg or "goodbye" in msg:
        reply = "Goodbye 👋 Have a wonderful day!"

    elif "ok" in msg or "okay" in msg:
        reply = "👍 Let me know if you need anything else!"

    elif "joke" in msg:
        reply = "Why did the computer go to the NGO? 😄 To donate bytes!"

    elif "bored" in msg:
        reply = "Try donating something useful today 😊 It feels great!"

    # ---------------- FALLBACK ----------------
    else:
        reply = (
            "Hmm 🤔 I didn't quite get that.\n\n"
            "Try asking about:\n"
            "• Donate / Claim Donation\n"
            "• NGO Dashboard / History\n"
            "• Login / Register\n"
            "• Or tell me your name 😊"
        )

    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=False)
