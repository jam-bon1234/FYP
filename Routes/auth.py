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
                "SELECT UserID, FName, LName, Email, Age, TotalPoints FROM Users WHERE Email=%s AND Password=%s",
                (email, password)
            )
            user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "UserID": user['UserID'],
                "FName": user['FName'],
                "LName": user['LName'],
                "Email": user['Email'],
                "Age": user['Age'],
                "TotalPoints": user['TotalPoints']
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        fname = data.get('FName')
        lname = data.get('LName')
        email = data.get('Email')
        age = data.get('Age')
        password = data.get('Password')

        if not all([fname, lname, email, age, password]):
            return jsonify({"error": "FName, LName, Email, Age, and Password are required"}), 400

        conn = get_connection()
        with conn.cursor() as cursor:
            # Check if email already exists
            cursor.execute("SELECT * FROM Users WHERE Email=%s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "Email already registered"}), 400

            # Get current max UserID and increment it
            cursor.execute("SELECT MAX(UserID) AS max_id FROM Users")
            result = cursor.fetchone()
            user_id = (result['max_id'] or 0) + 1

            total_points = 0  # default points

            cursor.execute(
                """
                INSERT INTO Users (UserID, FName, LName, Email, Age, TotalPoints, Password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (user_id, fname, lname, email, age, total_points, password)
            )
            conn.commit()

        conn.close()
        return jsonify({
            "status": "ok",
            "UserID": user_id,
            "FName": fname,
            "LName": lname,
            "Email": email,
            "Age": age,
            "TotalPoints": total_points
        }), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
