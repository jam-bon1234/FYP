from db import get_connection
from flask import request, jsonify, Blueprint
import traceback

preferences_bp = Blueprint('preferences', __name__, url_prefix='/preferences')
@preferences_bp.route('/preferences', methods=['POST'])
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