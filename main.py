from flask import Flask, jsonify
import json
import tinytuya
import os

# Ustawienia API z użyciem zmiennych środowiskowych
api_region = os.environ.get('API_REGION')
api_key = os.environ.get('API_KEY')
api_secret = os.environ.get('API_SECRET')

# Dane urządzeń w formacie JSON (wstawione bezpośrednio w kod lub zdefiniowane jako zmienna środowiskowa)
devices = json.loads(os.environ.get('DEVICES_JSON'))

app = Flask(__name__)

# Funkcja do pobrania stanu urządzenia
def get_device_status(current_device):
    cloud = tinytuya.Cloud(
        apiRegion=api_region,
        apiKey=api_key,
        apiSecret=api_secret,
        apiDeviceID=current_device['id']
    )
    return cloud.getstatus(current_device['id'])

# Endpoint zwracający status wszystkich urządzeń
@app.route('/devices', methods=['GET'])
def get_all_devices():
    all_statuses = []
    for device in devices:
        status = get_device_status(device)
        all_statuses.append({
            "name": device["name"],
            "id": device["id"],
            "status": status
        })
    return jsonify(all_statuses)

# Endpoint zwracający status konkretnego urządzenia na podstawie ID
@app.route('/device/<device_id>', methods=['GET'])
def get_single_device(device_id):
    device = next((d for d in devices if d['id'] == device_id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404
    
    status = get_device_status(device)
    return jsonify({
        "name": device["name"],
        "id": device["id"],
        "status": status
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
