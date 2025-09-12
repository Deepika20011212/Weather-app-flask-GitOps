from flask import Flask, render_template, request
import os, requests

app = Flask(__name__, template_folder="templates")
WEATHER_API = os.getenv("WEATHER_API_BASE", "http://weather-service:5001")
AIR_API = os.getenv("AIR_API_BASE", "http://air-service:5002")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/weather", methods=["GET","POST"])
def weather_dashboard():
    data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city","").strip()
        try:
            resp = requests.get(f"{WEATHER_API}/weather/{city}", timeout=6).json()
            f = requests.get(f"{WEATHER_API}/forecast/{city}", timeout=6).json()
            data = {"current": resp, "forecast": f.get("forecast",[])}
        except Exception as e:
            error = str(e)
    return render_template("weather.html", weather=data, error=error)

@app.route("/air", methods=["GET","POST"])
def air_dashboard():
    data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city","").strip()
        try:
            resp = requests.get(f"{AIR_API}/air/{city}", timeout=6).json()
            data = {"current": resp}
        except Exception as e:
            error = str(e)
    return render_template("air.html", air=data, error=error)

@app.route("/health")
def health():
    return {"status":"ok"}
