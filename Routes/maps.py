from flask import request, jsonify
import requests
import os
from dotenv import load_dotenv
from blueprints import maps_bp

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")   # ONE KEY


def get_pois(lat, lng, interests):
    pois = []
    for interest in interests:
        url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            f"?location={lat},{lng}"
            "&radius=2000"
            f"&type={interest.lower()}"
            f"&key={GOOGLE_MAPS_KEY}"
        )

        resp = requests.get(url)

        if resp.status_code == 200:
            results = resp.json().get("results", [])
            for r in results:
                pois.append({
                    "name": r.get("name"),
                    "lat": r["geometry"]["location"]["lat"],
                    "lng": r["geometry"]["location"]["lng"],
                    "type": interest
                })

    return pois


def get_directions(start_lat, start_lng, end_lat, end_lng, mode):
    url = (
        "https://maps.googleapis.com/maps/api/directions/json"
        f"?origin={start_lat},{start_lng}"
        f"&destination={end_lat},{end_lng}"
        f"&mode={mode}"
        f"&key={GOOGLE_MAPS_KEY}"
    )

    resp = requests.get(url)

    if resp.status_code == 200:
        routes = resp.json().get("routes", [])
        if routes:
            return routes[0]["overview_polyline"]["points"]

    return None


@maps_bp.route("/generate_route", methods=["POST"])
def generate_route():
    data = request.json

    lat = data.get("lat")
    lng = data.get("lng")
    interests = data.get("interests", [])
    mode = data.get("mode", "walking")
    preferred_time = data.get("preferred_time", 30)

    if not lat or not lng:
        return jsonify({"error": "Latitude and longitude required"}), 400

    # Step 1: Get POIs
    pois = get_pois(lat, lng, interests)

    # Step 2: Pick first POI (same logic as your original)
    if not pois:
        return jsonify({"error": "No POIs found"}), 404

    end = pois[0]
    polyline = get_directions(lat, lng, end["lat"], end["lng"], mode)

    # Step 3: Send back to Flutter
    return jsonify({
        "start": {"lat": lat, "lng": lng},
        "end": end,
        "pois": pois,
        "polyline": polyline,
        "mode": mode,
        "preferred_time": preferred_time
    })
