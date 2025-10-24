from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

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
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT UserID, Fname, Email FROM Users")
        result = cursor.fetchall()
    conn.close()
    return jsonify(result)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user_id = data.get('id')       # Get UserID from Flutter
    name = data.get('name')
    email = data.get('email')

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Users (UserID, Fname, email) VALUES (%s, %s, %s)",
            (user_id, name, email)   # Match the placeholders
        )
        conn.commit()
    conn.close()
    return jsonify({"status": "ok"})


@app.route('/trigger', methods=['POST'])
def trigger_make():
    # Example Make.com webhook call
    import requests
    webhook_url = "old9ixd4qaj6breiddwhprpijm94iinz@hook.eu2.make.com"
    requests.post(webhook_url, json={"action": "demo"})
    return jsonify({"status": "triggered"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
