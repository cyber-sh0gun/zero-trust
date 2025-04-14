# 🔐 Zero Trust Architecture Demo

This project demonstrates a basic Zero Trust Architecture (ZTA) flow using Python. It simulates a client that requests access to a protected resource via a ZTA Gateway, which evaluates the request using a policy enforcement engine.

---

## 🧩 Components

### 1. **Client Agent (`zta_application.py`)**
Runs on the endpoint machine (e.g., a laptop) and performs the following:
- Gathers trust context:
  - Username
  - Device name
  - Public IP address
  - Geolocation (via ipinfo.io)
  - MFA status (via environment variable)
  - Patch status (`/var/log/system_compliant`)
  - EDR presence (`/opt/edr/edr_agent`)
  - Behavior score (simulated)
- Sends this context as a JSON `POST` to the `/secret` endpoint on the ZTA Gateway

### 2. **ZTA Gateway (`zta_web_server.py`)**
- Receives trust context from the client agent
- Forwards the data to the Policy Engine
- Responds with either:
  - ✅ Access granted + resource
  - ❌ Access denied + explanation

### 3. **Policy Enforcer (`zta_policy_enforcer.py`)**
- Accepts trust context
- Calculates a trust score based on configurable weights for each trust factor
- Returns access decision (`granted: True | False`) and metadata

---

## 🔁 Flow Overview

```
Client Agent → ZTA Gateway → Policy Enforcer
                 ↓                 ↑
        Access Decision ← Trust Score
                 ↓
   Resource Granted or Denied
```

---

## 🚀 Getting Started

### Client:
```bash
python3 zta_application.py
```

### ZTA Gateway:
- Must have Flask installed and running on port 5000:
```bash
python3 zta_web_server.py
```

### Policy Enforcer:
- Imported as a module by the web server; no standalone execution required

---

## ⚙️ Configuration
- Update `ZTA_GATEWAY_URL` in `zta_application.py` with your gateway server's IP or domain:
  ```python
  ZTA_GATEWAY_URL = "http://<your-server-ip>:5000/secret"
  ```
- To simulate failures, try:
  - Unsetting the `MFA_VERIFIED` env variable
  - Removing EDR or patch status files
  - Changing the username or device

---

## 📁 Files
- `zta_application.py`: Client trust context generator
- `zta_web_server.py`: Flask-based access gateway
- `zta_policy_enforcer_monica.py`: Trust scoring engine

---

## 🧠 Note
This demo is for educational purposes only and not intended for use in production environments.

