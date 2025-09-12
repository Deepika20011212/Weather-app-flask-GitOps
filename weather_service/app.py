# weather_service/app.py
from flask import Flask, jsonify
import os, requests
import redis, time

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
OW_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
OW_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

def fetch_current(city):
    params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
    resp = requests.get(OW_CURRENT, params=params, timeout=8)
    resp.raise_for_status()
    d = resp.json()
    return {
        "city": city,
        "temperature": d["main"]["temp"],
        "description": d["weather"][0]["description"],
        "icon": d["weather"][0]["icon"],
        "source": "openweather",
        "ts": int(time.time())
    }

@app.route("/weather/<city>")
def current(city):
    key = f"weather:{city.lower()}"
    if r:
        cached = r.get(key)
        if cached:
            return jsonify({"source": "cache", **eval(cached)})

    try:
        data = fetch_current(city)
    except Exception as e:
        # fallback: if cache exists, return it
        if r:
            cached = r.get(key)
            if cached:
                return jsonify({"source": "cache", **eval(cached)})
        return jsonify({"error": str(e)}), 502

    if r:
        r.set(key, repr(data), ex=300)  # cache 5 minutes
    return jsonify(data)

@app.route("/forecast/<city>")
def forecast(city):
    params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
    resp = requests.get(OW_FORECAST, params=params, timeout=8)
    resp.raise_for_status()
    d = resp.json()
    # Condense to daily forecast (simple)
    out = []
    for item in d.get("list", [])[:40]:
        out.append({
            "ts": item["dt"],
            "temp": item["main"]["temp"],
            "desc": item["weather"][0]["description"]
        })
    return jsonify({"city": city, "forecast": out})
