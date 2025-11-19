import traceback
from flask import request, jsonify, Blueprint
from db import get_connection


user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT UserID, Fname, Lname, Email FROM Users")
            result = cursor.fetchall()
        conn.close()
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        user_id = data.get('id')
        fname = data.get('fname')
        lname = data.get('lname')
        email = data.get('email')

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (UserID, Fname, Lname, Email) VALUES (%s, %s, %s, %s)",
                (user_id, fname, lname, email)
            )
            conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500