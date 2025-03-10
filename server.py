from flask import Flask, jsonify
from flask_cors import CORS  # Added CORS support
import platform
import subprocess
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

def scan_wifi():
    system = platform.system()
    if system == "Linux":
        return scan_wifi_linux()
    elif system == "Windows":
        return scan_wifi_windows()
    else:
        return {"error": "Unsupported OS"}

def scan_wifi_linux():
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi"],
            capture_output=True, text=True
        )
        networks = []
        for line in result.stdout.strip().split("\n"):
            parts = line.split(":")
            if len(parts) >= 3 and parts[0]:  # Avoid empty SSIDs
                networks.append({
                    "ssid": parts[0],
                    "signal": int(parts[1]),
                    "security": parts[2]
                })
        return networks if networks else {"error": "No networks found"}
    except Exception as e:
        return {"error": str(e)}

def scan_wifi_windows():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "network", "mode=bssid"],
            capture_output=True, text=True
        )
        networks = []
        ssid = None
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line.lower().startswith("ssid") and ":" in line:
                ssid = line.split(":", 1)[1].strip()
            elif "Signal" in line and ssid:
                signal = int(re.findall(r"\d+", line.split(":")[-1])[0])
                if ssid not in [n["ssid"] for n in networks]:  # Avoid duplicates
                    networks.append({"ssid": ssid, "signal": signal})
        return networks if networks else {"error": "No networks found"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET"])
def get_wifi():
    return jsonify(scan_wifi())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
