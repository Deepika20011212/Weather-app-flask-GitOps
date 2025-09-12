# air_service/app.py
from flask import Flask, jsonify
import os, requests, time
import redis

app = Flask(__name__)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
USE_REDIS = os.getenv("USE_REDIS", "true").lower() != "false"
r = None
if USE_REDIS:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    except Exception:
        r = None

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")
# OpenWeather Air Pollution API uses lat/lon — this example will call geocoding first
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"
AIR_URL = "http://api.openweathermap.org/data/2.5/air_pollution"

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

def get_latlon(city):
    params = {"q": city, "limit": 1, "appid": OPENWEATHER_KEY}
    rgeo = requests.get(GEO_URL, params=params, timeout=8).json()
    if not rgeo:
        raise ValueError("location not found")
    return rgeo[0]["lat"], rgeo[0]["lon"]

@app.route("/air/<city>")
def air(city):
    key = f"air:{city.lower()}"
    if r:
        cached = r.get(key)
        if cached:
            return jsonify({"source": "cache", **eval(cached)})

    try:
        lat, lon = get_latlon(city)
        params = {"lat": lat, "lon": lon, "appid": OPENWEATHER_KEY}
        resp = requests.get(AIR_URL, params=params, timeout=8)
        resp.raise_for_status()
        d = resp.json()
        # extract AQI: d['list'][0]['main']['aqi'] (1-5)
        aqi_raw = d.get("list", [{}])[0].get("main", {}).get("aqi", 0)
        mapping = {1: 50, 2: 100, 3:150,4:200,5:300}
        aqi = mapping.get(aqi_raw, 100)
        status = "Good" if aqi < 50 else "Moderate" if aqi < 100 else "Unhealthy"
        payload = {"city": city, "aqi": aqi, "status": status, "source": "openweather", "ts": int(time.time())}
    except Exception as e:
        if r:
            cached = r.get(key)
            if cached:
                return jsonify({"source": "cache", **eval(cached)})
        return jsonify({"error": str(e)}), 502

    if r:
        r.set(key, repr(payload), ex=300)
    return jsonify(payload)
