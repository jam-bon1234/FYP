from flask import request, jsonify, Blueprint
from db import get_connection
import traceback


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
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


@auth_bp.route('/signup', methods=['POST'])
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
            if cursor.fetchone():
                return jsonify({"error": "Email already registered"}), 400

            # Generate new UserID
            cursor.execute("SELECT MAX(UserID) AS max_id FROM Users")
            max_id = cursor.fetchone()['max_id']
            new_user_id = (max_id or 0) + 1

            # Insert user
            cursor.execute(
                "INSERT INTO Users (UserID, Email, Password) VALUES (%s, %s, %s)",
                (new_user_id, email, password)
            )
            conn.commit()

        conn.close()
        return jsonify({"status": "ok", "UserID": new_user_id}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
