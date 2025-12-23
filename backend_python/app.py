from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
import hashlib

app = Flask(__name__)
CORS(app)

# ---------- TEST ROUTE ----------
@app.route("/")
def home():
    return {"message": " HelpReach Python Backend Running Python backend is running 🚀"}

# ---------- REGISTER ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
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

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
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
    else:
        return {"error": "Invalid credentials"}, 401

# ---------- GET DONATIONS ----------
@app.route("/donations", methods=["GET"])
def get_donations():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.*, u.name AS donor_name
        FROM donations d
        JOIN users u ON u.id = d.donor_id
        ORDER BY d.created_at DESC
    """)

    donations = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(donations)

# ---------- POST DONATION ----------
@app.route("/donate", methods=["POST"])
def donate():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    quantity = data.get("quantity")
    pickup_info = data.get("pickup_info")
    donor_id = data.get("donor_id")

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

    return {"ok": True, "message": "Donation added"}

# ---------- RUN SERVER ----------
if __name__ == "__main__":
    app.run(debug=True)
