import platform
import subprocess
import re

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
            if len(parts) >= 3:
                networks.append({
                    "ssid": parts[0],
                    "signal": int(parts[1]),
                    "security": parts[2]
                })
        return networks
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
            if "SSID" in line:
                ssid = line.split(":")[-1].strip()
            elif "Signal" in line and ssid:
                signal = int(re.findall(r"\d+", line.split(":")[-1])[0])
                networks.append({"ssid": ssid, "signal": signal})
        return networks
    except Exception as e:
        return {"error": str(e)}
