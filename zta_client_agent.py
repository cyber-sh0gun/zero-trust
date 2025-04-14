from flask import Flask, jsonify
import platform
import getpass
import subprocess
import os
import requests

app = Flask(__name__)

def get_public_ip():
    try:
        return subprocess.check_output(["curl", "-s", "https://ipinfo.io/ip"]).decode().strip()
    except:
        return "Unknown"

def get_geo_from_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country"),
            "loc": data.get("loc")  # latitude,longitude
        }
    except Exception as e:
        return {"error": f"Failed to get geolocation: {str(e)}"}

@app.route("/trust-data", methods=["GET"])
def trust_data():
    ip = get_public_ip()
    geo = get_geo_from_ip(ip)
    user = getpass.getuser()
    device = platform.node()

    return jsonify({
        "user": user,
        "device": device,
        "ip": ip,
        "geo": geo,
        "mfa_verified": os.environ.get("MFA_VERIFIED") == "true",
        "edr_installed": os.path.exists(f"/home/{user}/edr_agent"),
        "patched": os.path.exists(f"/home/{user}/patched"),
        "behavior_score": 12
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)

