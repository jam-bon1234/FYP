from flask import request, jsonify, Blueprint
from db import get_connection
import traceback
from app import app

auth_bp = Blueprint('auth', __name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('Email')
        password = data.get('Password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT UserID, Email FROM Users WHERE Email=%s AND Password=%s",
                (email, password)
            )
            user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({"UserID": user['UserID'], "Email": user['Email']}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('Email')
        password = data.get('Password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        conn = get_connection()
        with conn.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT * FROM Users WHERE Email=%s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "Email already registered"}), 400

            cursor.execute(
                "INSERT INTO Users (Email, Password) VALUES (%s, %s)",
                (email, password)
            )
            conn.commit()
        conn.close()
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500