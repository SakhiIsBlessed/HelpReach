


from urllib import response
from flask import Flask, request, jsonify  #Flask:Web framework that is use to create backend Api,request:Reads the data sent from fromtend,jsonify:Converts python data into json
from flask_cors import CORS #Cross-Origin Resource Sharing:Allows frontend (html,js) to call backend api
from db import get_db_connection #custom function used to connect to mysql database
import hashlib # used to securely hashed passwords bcoz we should not store password in plain text
import random # used to generate random OTP

from email_service import send_email


app = Flask(__name__) # creates a flask application 
app.secret_key = "helpreach-secret"
CORS(app, supports_credentials=True) # Enables cross origin resource sharing,so frontend can access backend api

# Dictionary to store OTP temporarily
otp_store = {}

# ---------------- HOME ----------------
@app.route("/")
def home():#simple test route that tells backend is running
    return {"message": "HelpReach backend running 🚀"} # if you open http://127.0.0.1:5000 you will see this msg

# ---------------- REGISTER ----------------
@app.route("/api/register", methods=["POST", "OPTIONS"]) #This line tells Flask to create an API endpoint at /api/register POST:usrd to register new user
def register():#This function runs whenever /api/register is called
    if request.method == "OPTIONS": #OPTIONS: used to check browser before post,this is used to check cross origin requests
        return jsonify({"ok": True}), 200  # This avoids CORS errors

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
        # 🔹 Send welcome email after successful registration
        try:
            send_email(
                to_email=email,
                subject="Welcome to HelpReach 🎉",
                message=f"""
Hello {name}, 

Welcome to the HelpReach family! 🌟

Your account has been successfully created, and now you can start donating items and supporting NGOs to make a real difference in people's lives.

Thank you for joining us—your kindness matters! 💖

Warm regards,
– Team HelpReach
"""
            )
        except Exception as email_error:
            print(f"❌ Email error: {email_error}")
        return {"ok": True, "message": "User registered"} #Sends success message to frontend
    except Exception as e: #Catches database or server errors, return error msg
        return {"error": str(e)}, 500
    finally:
        cursor.close() #Closes database connection,Prevents memory leaks
        db.close() #Executes whether success or error occurs

        
# ---------------- LOGIN ----------------
@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.json
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

If this was not you, please secure your account immediately.

– Team HelpReach
"""
            )
        except Exception as e:
            print("❌ Login email error:", e)

        return jsonify({"ok": True, "user": user})
     # ✅ SET COOKIE (THIS IS THE KEY)
    response.set_cookie(
        "user_id",
        str(user["id"]),
        httponly=True,
        samesite="Lax"
    )

    return response
    return jsonify({"error": "Invalid credentials"}), 401


# ---------------- DONATIONS ----------------
@app.route("/api/donations", methods=["GET", "POST", "OPTIONS"])
def api_donations():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

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
    data = request.form if request.form else request.json

    title = data.get("title")
    description = data.get("description")
    quantity = data.get("quantity")
    pickup_info = data.get("pickup_info")
    # donor_id = data.get("donor_id")
    donor_email = data.get("donor_email")
    donor_id = request.cookies.get("user_id")


    if not title or not donor_id:
        return {"error": "user not logged in"}, 401
        

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO donations (title, description, quantity, pickup_info, donor_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, quantity, pickup_info, donor_id))

    db.commit()
    cursor.close()
    db.close()

    # 🔹 Send thank-you email to logged-in user
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT name, email FROM users WHERE id = %s", (donor_id,))
        user = cursor.fetchone()

        if donor_email and user:
            send_email(
                to_email=donor_email,
                subject="Thank you for your donation ❤️",
                message=f"""
Hello {user['name']},

We are truly grateful for your generous donation towards “{title}”.
Your kindness and willingness to support this cause mean more than words can express.

Because of thoughtful donors like you, we are able to help NGOs continue their mission, reach those in need, and create a positive impact in countless lives. Every contribution—big or small—brings us one step closer to a better, kinder world.

Your support inspires hope and encourages meaningful change. We deeply appreciate the trust you have placed in HelpReach and the cause you chose to support.

If you have any questions or would like updates on how your contribution is making a difference, feel free to reach out to us anytime.

Once again, thank you for being a part of this journey of compassion and generosity 💖

With heartfelt gratitude,
Team HelpReach
Connecting kindness with causes that matter
"""
            )

        cursor.close()
        db.close()

    except Exception as e:
        print("❌ Email error:", e)

    return {"ok": True, "message": "Donation added successfully"}


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
             category, contact_person, phone, address, password_hash)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            name, description, contact_email, registration_number,
            category, contact_person, phone, address, password_hash
        ))
        db.commit()
        insert_cursor.close()

        # 🔹 EMAIL (safe)
        try:
            send_email(
                to_email=contact_email,
                subject="NGO Registration Successful ✔️",
                message=f"""Hello {contact_person},

Your NGO "{name}" has been registered successfully on HelpReach.

You can now log in using your registered email and password.

– Team HelpReach
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

        return jsonify({
            "ok": True,
            "ngo": ngo
        })

    except Exception as e:
        print("❌ DB ERROR:", e)
        return jsonify({"error": "Database error"}), 500

    finally:
        db.close()

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
        send_email(
            to_email=ngo["contact_email"],
            subject="NGO Login Alert 🔔",
            message=f"""
Hello {ngo['name']},

Your NGO account has just logged in successfully on HelpReach.

If this was you, no action is required.  
If you did not log in, please reset your password immediately.

– Team HelpReach
"""
        )

        return jsonify({
            "ok": True,
            "ngo": ngo
        })
    
     #  STORE NGO ID IN HTTP-ONLY COOKIE
        response.set_cookie(
            "ngo_id",
            str(ngo["id"]),
            httponly=True,
            samesite="Lax"
        )

        return response

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return jsonify({"error": "Server error"}), 500

    finally:
        cursor.close()
        db.close()
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

Thank you for contacting HelpReach.

We have received your enquiry with the following details:

Inquiry Type: {inquiry_type}
Message: {message}

Our team will contact you shortly.

– Team HelpReach
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
    resp.set_cookie("user_id", str(user["id"]), httponly=True)

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


if __name__ == "__main__":
    app.run(debug=True)



    