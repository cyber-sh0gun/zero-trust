# zta_policy_enforcer_monica.py
#
# MONICA - Monitor Of Network Integrity, Context, and Access
#
# Vibe: Calm but always watching.  She sees what you're doing, checks your
# device's posture, and denies you for even looking suspicious
#
# "She doesn't trust you.  Ever. And she's right."

import datetime

# Simulated policy config
TRUST_POLICIES = {
    "identity_weight": 15,
    "device_weight": 10,
    "time_weight": 15,
    "mfa_weight": 15,
    "geoip_weight": 10,
    "edr_weight": 10,
    "patch_weight": 10,
    "behavior_weight": 15,
    "min_required_score": 70,
    "trusted_user": "trusted_user",
    "trusted_device": "ztclient",
    "trusted_ip_range": "13.57.",
    "trusted_countries": ["US"],
    "working_hours": (9, 17),  # 9 AM to 5 PM
    "resource_path": "/opt/secrets/zero_trust_secret.txt",
    "granted_copy_path": "/home/{user}/zero_trust_secret.txt"
}

def calculate_trust_score(data):
    trust_score = 0

    if data["user"] == TRUST_POLICIES["trusted_user"]:
        trust_score += TRUST_POLICIES["identity_weight"]

    if data["device"] == TRUST_POLICIES["trusted_device"]:
        trust_score += TRUST_POLICIES["device_weight"]

    if TRUST_POLICIES["working_hours"][0] <= datetime.datetime.now().hour <= TRUST_POLICIES["working_hours"][1]:
        trust_score += TRUST_POLICIES["time_weight"]

    if data.get("mfa_verified"):
        trust_score += TRUST_POLICIES["mfa_weight"]

    if data.get("ip", "").startswith(TRUST_POLICIES["trusted_ip_range"]):
        trust_score += TRUST_POLICIES["geoip_weight"]

    geo = data.get("geo", {})
    if geo.get("country") in TRUST_POLICIES["trusted_countries"]:
        trust_score += TRUST_POLICIES["geoip_weight"]

    if data.get("edr_installed"):
        trust_score += TRUST_POLICIES["edr_weight"]

    if data.get("patched"):
        trust_score += TRUST_POLICIES["patch_weight"]

    trust_score += data.get("behavior_score", 0)

    return {
        "user": data["user"],
        "device": data["device"],
        "ip": data["ip"],
        "trust_score": trust_score,
        "granted": trust_score >= TRUST_POLICIES["min_required_score"]
    }

