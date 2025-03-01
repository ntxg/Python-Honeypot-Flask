from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime
import os
app = Flask(__name__)
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1314235578333790240/6lvqKF7AyKPQtq5T_BuyeV3YD_7n__06COmHmSgDrq1UvrfrUlSByFzYMfW0-3iOoRdu'
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return None
def send_to_discord(visit_info):
    payload = {
        "content": f"nieautoryzowane wejście!\n\n"
                    f"Timestamp: {visit_info['timestamp']}\n"
                    f"IP: {visit_info['ip']}\n"
                    f"Country: {visit_info.get('country', 'Unknown')}\n"
                    f"ISP: {visit_info.get('isp', 'Unknown')}\n"
                    f"Method: {visit_info['method']}\n"
                    f"Path: {visit_info['path']}\n"
                    f"User Agent: {visit_info['userAgent']}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    if response.status_code != 204:
        print("Błąd podczas wysyłania danych do Discorda:", response.text)
def save_to_log_file(visit_info):
    log_file_path = 'honeypot_logs.json'
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(visit_info)
    with open(log_file_path, 'w') as f:
        json.dump(logs, f, indent=4)
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def honeypot(path):
    visit_info = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.remote_addr,
        "method": request.method,
        "path": path,
        "userAgent": request.headers.get('User-Agent')
    }
    ip_info = get_ip_info(visit_info['ip'])
    if ip_info:
        visit_info['country'] = ip_info.get('country', 'Unknown')
        visit_info['isp'] = ip_info.get('isp', 'Unknown')
    else:
        visit_info['country'] = 'Unknown'
        visit_info['isp'] = 'Unknown'
    send_to_discord(visit_info)
    save_to_log_file(visit_info)
    return jsonify({"message": "Honeypot - available paths logged!"}), 200
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)