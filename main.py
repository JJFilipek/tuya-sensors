from flask import Flask, jsonify, request
import tinytuya

app = Flask(__name__)

# Funkcja do pobrania stanu urządzenia
def get_device_status(device_id, api_region, api_key, api_secret):
    # Inicjalizacja połączenia z chmurą Tuya
    cloud = tinytuya.Cloud(
        apiRegion=api_region,
        apiKey=api_key,
        apiSecret=api_secret,
        apiDeviceID=device_id
    )
    # Pobranie statusu urządzenia
    status = cloud.getstatus(device_id)
    return status

# Endpoint zwracający status pojedynczego urządzenia na podstawie ID
@app.route('/device/<device_id>', methods=['GET'])
def get_single_device(device_id):
    # Pobranie danych API z nagłówków żądania
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    
    # Sprawdzenie, czy wszystkie wymagane dane zostały dostarczone
    if not all([api_region, api_key, api_secret]):
        return jsonify({"error": "Brak danych uwierzytelniających API"}), 400

    # Pobranie statusu urządzenia
    status = get_device_status(device_id, api_region, api_key, api_secret)
    return jsonify({
        "id": device_id,
        "status": status
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
