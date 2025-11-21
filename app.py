from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import os
from blueprints import register_blueprints

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


register_blueprints(app)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
