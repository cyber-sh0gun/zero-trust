from flask import Flask, jsonify, request
import requests
from zta_policy_enforcer_monica import calculate_trust_score, TRUST_POLICIES

app = Flask(__name__)

CLIENT_AGENT_URL = "http://13.57.202.150:6000/trust-data"  # Update as needed

def get_client_data():
    try:
        # Request trust context from client agent
        client_response = requests.get(CLIENT_AGENT_URL, timeout=5)
        return client_response.json()
    except Exception as e:
        print(f"[Error] Failed to retrieve trust data: {e}")
        return None

@app.route("/secret", methods=["GET"])
def get_secret():
    client_data = get_client_data()
    if not client_data:
        return jsonify({
            "status": "error",
            "message": "Unable to retrieve client trust context"
        }), 500

    result = calculate_trust_score(client_data)
    print(f"[ZT MONICA CHECK] User: {result['user']}, Device: {result['device']}, IP: {result['ip']}, Trust Score: {result['trust_score']}")

    if result["granted"]:
        try:
            with open(TRUST_POLICIES["resource_path"], "r") as f:
                secret = f.read()
            return secret
            #jsonify({
                #"status": "granted",
               # "trust_score": result["trust_score"],
                #"geo": client_data.get("geo"),
                #"resource": secret
            #})
        except FileNotFoundError:
            return jsonify({
                "status": "granted",
                "trust_score": result["trust_score"],
                "geo": client_data.get("geo"),
                "error": "Resource file not found"
            }), 500
        except PermissionError:
            return jsonify({
                "status": "granted",
                "trust_score": result["trust_score"],
                "geo": client_data.get("geo"),
                "error": "Access blocked by file permissions"
            }), 403
    else:
        return jsonify({
            "status": "denied",
            "trust_score": result["trust_score"],
            "geo": client_data.get("geo"),
            "message": "Trust score too low"
        }), 403

@app.route("/trust-check", methods=["GET"])
def trust_check():
    client_data = get_client_data()
    if not client_data:
        return jsonify({
            "status": "error",
            "message": "Unable to retrieve client trust context"
        }), 500

    result = calculate_trust_score(client_data)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
