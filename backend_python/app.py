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



from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
import hashlib

app = Flask(__name__)
CORS(app)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return {"message": "HelpReach backend running 🚀"}

# ---------------- REGISTER ----------------
@app.route("/api/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    data = request.form if request.form else request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {"error": "Missing fields"}, 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
            (name, email, password_hash)
        )
        db.commit()
        return {"ok": True, "message": "User registered"}
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cursor.close()
        db.close()

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

    cursor.execute(
        "SELECT id, name FROM users WHERE email=%s AND password_hash=%s",
        (email, password_hash)
    )

    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        return {"ok": True, "user": user}

    return {"error": "Invalid credentials"}, 401

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
    donor_id = data.get("donor_id", 1)

    if not title or not donor_id:
        return {"error": "Missing fields"}, 400

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO donations (title, description, quantity, pickup_info, donor_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, quantity, pickup_info, donor_id))

    db.commit()
    cursor.close()
    db.close()

    return {"ok": True, "message": "Donation added successfully"}

if __name__ == "__main__":
    app.run(debug=True)