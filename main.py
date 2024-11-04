from flask import Flask, jsonify, request
import tinytuya

app = Flask(__name__)

# Funkcja do pobrania stanu urządzenia
def get_device_status(device_id, api_region, api_key, api_secret):
    cloud = tinytuya.Cloud(
        apiRegion=api_region,
        apiKey=api_key,
        apiSecret=api_secret,
        apiDeviceID=device_id
    )
    return cloud.getstatus(device_id)

# Endpoint zwracający status wszystkich urządzeń podanych w parametrach
@app.route('/devices', methods=['GET'])
def get_multiple_devices():
    # Pobierz dane API z nagłówków żądania
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    
    # Pobierz listę identyfikatorów urządzeń z parametru żądania
    device_ids = request.args.getlist('device_id')
    
    # Sprawdź, czy wszystkie wymagane dane zostały dostarczone
    if not all([api_region, api_key, api_secret, device_ids]):
        return jsonify({"error": "Missing API credentials or device IDs"}), 400

    # Pobierz status dla każdego urządzenia
    all_statuses = []
    for device_id in device_ids:
        status = get_device_status(device_id, api_region, api_key, api_secret)
        all_statuses.append({
            "id": device_id,
            "status": status
        })
    return jsonify(all_statuses)

# Endpoint zwracający status pojedynczego urządzenia na podstawie ID
@app.route('/device/<device_id>', methods=['GET'])
def get_single_device(device_id):
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    
    # Sprawdź, czy wszystkie wymagane dane zostały dostarczone
    if not all([api_region, api_key, api_secret]):
        return jsonify({"error": "Missing API credentials"}), 400

    # Pobierz status dla urządzenia
    status = get_device_status(device_id, api_region, api_key, api_secret)
    return jsonify({
        "id": device_id,
        "status": status
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
