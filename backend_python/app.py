# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from db import get_db_connection
# import hashlib

# app = Flask(__name__)
# CORS(app)

# # ---------------- HOME ----------------
# @app.route("/")
# def home():
#     return {"message": "HelpReach backend running 🚀"}

# # ---------------- REGISTER ----------------
# @app.route("/api/register", methods=["POST", "OPTIONS"])
# def register():
#     if request.method == "OPTIONS":
#         return jsonify({"ok": True}), 200

#     data = request.form if request.form else request.json

#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")

#     if not name or not email or not password:
#         return {"error": "Missing fields"}, 400

#     password_hash = hashlib.sha256(password.encode()).hexdigest()

#     db = get_db_connection()
#     cursor = db.cursor()

#     try:
#         cursor.execute(
#             "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
#             (name, email, password_hash)
#         )
#         db.commit()
#         return {"ok": True, "message": "User registered"}
#     except Exception as e:
#         return {"error": str(e)}, 500
#     finally:
#         cursor.close()
#         db.close()


# # ---------------- LOGIN ----------------
# @app.route("/api/login", methods=["POST", "OPTIONS"])
# def login():
#     if request.method == "OPTIONS":
#         return jsonify({"ok": True}), 200

#     data = request.form if request.form else request.json
#     email = data.get("email")
#     password = data.get("password")

#     password_hash = hashlib.sha256(password.encode()).hexdigest()

#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)

#     cursor.execute(
#         "SELECT id, name FROM users WHERE email=%s AND password_hash=%s",
#         (email, password_hash)
#     )

#     user = cursor.fetchone()
#     cursor.close()
#     db.close()

#     if user:
#         return {"ok": True, "user": user}

#     return {"error": "Invalid credentials"}, 401


# # ---------------- DONATIONS ----------------
# @app.route("/api/donations", methods=["GET", "POST", "OPTIONS"])
# def api_donations():
#     if request.method == "OPTIONS":
#         return jsonify({"ok": True}), 200

#     if request.method == "GET":
#         db = get_db_connection()
#         cursor = db.cursor(dictionary=True)

#         cursor.execute("""
#             SELECT d.*, u.name AS donor_name
#             FROM donations d
#             JOIN users u ON u.id = d.donor_id
#             ORDER BY d.created_at DESC
#         """)

#         data = cursor.fetchall()
#         cursor.close()
#         db.close()

#         return jsonify(data)

#     # POST
#     data = request.form if request.form else request.json

#     title = data.get("title")
#     description = data.get("description")
#     quantity = data.get("quantity")
#     pickup_info = data.get("pickup_info")
#     donor_id = data.get("donor_id", 1)

#     if not title or not donor_id:
#         return {"error": "Missing fields"}, 400

#     db = get_db_connection()
#     cursor = db.cursor()

#     cursor.execute("""
#         INSERT INTO donations (title, description, quantity, pickup_info, donor_id)
#         VALUES (%s, %s, %s, %s, %s)
#     """, (title, description, quantity, pickup_info, donor_id))

#     db.commit()
#     cursor.close()
#     db.close()

#     return {"ok": True, "message": "Donation added successfully"}


# if __name__ == "__main__":
#     app.run(debug=True)


# ---------------- LOGIN ----------------
# @app.route("/api/login", methods=["POST", "OPTIONS"])
# def login():
#     if request.method == "OPTIONS":
#         return jsonify({"ok": True}), 200

#     data = request.form if request.form else request.json
#     email = data.get("email")
#     password = data.get("password")

#     password_hash = hashlib.sha256(password.encode()).hexdigest()

#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)

#     cursor.execute(
#         "SELECT id, name FROM users WHERE email=%s AND password_hash=%s",
#         (email, password_hash)
#     )

#     user = cursor.fetchone()
#     cursor.close()
#     db.close()

#     if user:
#         return {"ok": True, "user": user}

#     return {"error": "Invalid credentials"}, 401





from flask import Flask, request, jsonify  #Flask:Web framework that is use to create backend Api,request:Reads the data sent from fromtend,jsonify:Converts python data into json
from flask_cors import CORS #Cross-Origin Resource Sharing:Allows frontend (html,js) to call backend api
from db import get_db_connection #custom function used to connect to mysql database
import hashlib # used to securely hashed passwords bcoz we should not store password in plain text
from werkzeug.security import check_password_hash

from email_service import send_email



app = Flask(__name__) # creates a flask application 
CORS(app) # Enables cross origin resource sharing,so frontend can access backend api

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
    donor_id = data.get("donor_id")
    donor_email = data.get("donor_email")


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

    # ✅ FIXED validation (no user_id)
    if not name or not registration_number or not contact_email:
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO ngos
            (name, description, contact_email, registration_number,
             category, contact_person, phone, address)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            name,
            description,
            contact_email,
            registration_number,
            category,
            contact_person,
            phone,
            address
        ))

        db.commit()

        # ✅ Confirmation Email
        send_email(
            to_email=contact_email,
            subject="NGO Registration Successful ✔️",
            message=f"""Hello {contact_person},

Your NGO "{name}" has been registered successfully on HelpReach.

Our team will review your details and get back to you shortly.

– Team HelpReach
"""
        )

        return jsonify({"ok": True})

    except Exception as e:
        print("❌ DB ERROR:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        db.close()



# ---------------- NGO LOGIN ----------------       
# @app.route("/api/ngo/login", methods=["POST"])
# def ngo_login():
#     data = request.get_json()
#     print("📥 NGO Login Data:", data)

#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Email and password required"}), 400

#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)

#     try:
#         cursor.execute(
#             "SELECT id, name, contact_email, password FROM ngos WHERE contact_email = %s",
#             (email,)
#         )
#         ngo = cursor.fetchone()

#         if not ngo:
#             return jsonify({"error": "NGO not found"}), 401

#         if not check_password_hash(ngo["password"], password):
#             return jsonify({"error": "Invalid password"}), 401

#         # ✅ Login success
#         return jsonify({
#             "ok": True,
#             "ngo": {
#                 "id": ngo["id"],
#                 "name": ngo["name"],
#                 "email": ngo["contact_email"],
#                 "role": "ngo"
#             }
#         })

#     except Exception as e:
#         print("❌ LOGIN ERROR:", e)
#         return jsonify({"error": "Server error"}), 500

#     finally:
#         cursor.close()
#         db.close()

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

if __name__ == "__main__":
    app.run(debug=True)



    