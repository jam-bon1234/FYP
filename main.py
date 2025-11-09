from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv
import traceback

load_dotenv()
# Code for creating database connections from tutorials slightly altered to allow for cross-origin resource sharing
app = Flask(__name__)
CORS(app)


def get_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )


@app.route('/users', methods=['GET'])
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

@app.route('/users', methods=['POST'])
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
# Code for post and get methods practiced in Advanced Web Development Lectures altered to send success/error messages
@app.route('/preferences', methods=['POST'])
def add_preferences():
    try:
        data = request.json

        preference_id = data.get('PreferenceID')
        user_id = data.get('UserID')
        transport_mode = data.get('TransportMode')
        time_available = data.get('TimeAvailable')
        interests = data.get('Interests')  # list from Flutter
        activity_level = data.get('ActivityLevel')
        mood = data.get('Mood')
        notifications = data.get('Notifications')

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO Preferences
                (PreferenceID, UserID, TransportMode, TimeAvailable, Interests, ActivityLevel, Mood, Notifications)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    preference_id,
                    user_id,
                    transport_mode,
                    time_available,
                    ','.join(interests) if interests else None,
                    activity_level,
                    mood,
                    notifications
                )
            )
            conn.commit()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/trigger', methods=['POST'])
def trigger_make():
    try:
        import requests
        webhook_url = "https://hook.eu2.make.com/iwc4012dqoi9m93xg7wkiadi6nsowsus"
        requests.post(webhook_url, json={"action": "demo"})
        return jsonify({"status": "triggered"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
