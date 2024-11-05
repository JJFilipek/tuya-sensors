import os
from flask import Flask, jsonify, request
import tinytuya
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# Function to retrieve the status of a device
def get_device_status(device_id, api_region, api_key, api_secret):
    cloud = tinytuya.Cloud(
        apiRegion=api_region,
        apiKey=api_key,
        apiSecret=api_secret,
        apiDeviceID=device_id
    )
    logging.info(f"Fetching status for device ID: {device_id}")
    return cloud.getstatus(device_id)

# Function to retrieve details of a device
def get_device_details(device_id, api_region, api_key, api_secret):
    cloud = tinytuya.Cloud(
        apiRegion=api_region,
        apiKey=api_key,
        apiSecret=api_secret
    )
    logging.info("Fetching device list from cloud")
    devices = cloud.getdevices()
    device_details = next((device for device in devices if device['id'] == device_id), None)
    if device_details:
        logging.info(f"Details found for device ID: {device_id}")
    else:
        logging.warning(f"No details found for device ID: {device_id}")
    return device_details

# Endpoint to retrieve the status of multiple devices provided in the request
@app.route('/devices', methods=['GET'])
def get_multiple_devices():
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    device_ids = request.args.getlist('device_id')

    # Check if all required data is provided
    if not all([api_region, api_key, api_secret, device_ids]):
        logging.error("Missing API credentials or device IDs")
        return jsonify({"error": "Missing API credentials or device IDs"}), 400

    all_statuses = []
    for device_id in device_ids:
        status = get_device_status(device_id, api_region, api_key, api_secret)
        all_statuses.append({
            "id": device_id,
            "status": status
        })
    logging.info(f"Retrieved statuses for {len(device_ids)} devices")
    return jsonify(all_statuses)

# Endpoint to retrieve the status of a single device by ID
@app.route('/device/<device_id>', methods=['GET'])
def get_single_device(device_id):
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    
    # Check if all required data is provided
    if not all([api_region, api_key, api_secret]):
        logging.error("Missing API credentials")
        return jsonify({"error": "Missing API credentials"}), 400

    # Retrieve device status
    status = get_device_status(device_id, api_region, api_key, api_secret)
    logging.info(f"Status retrieved for device ID: {device_id}")
    return jsonify({
        "id": device_id,
        "status": status
    })

# New endpoint to retrieve details of a device by ID
@app.route('/device/<device_id>/details', methods=['GET'])
def get_device_details_endpoint(device_id):
    api_region = request.headers.get('API-Region')
    api_key = request.headers.get('API-Key')
    api_secret = request.headers.get('API-Secret')
    
    # Check if all required data is provided
    if not all([api_region, api_key, api_secret]):
        logging.error("Missing API credentials")
        return jsonify({"error": "Missing API credentials"}), 400

    # Retrieve device details
    details = get_device_details(device_id, api_region, api_key, api_secret)
    if not details:
        logging.warning(f"Device not found: {device_id}")
        return jsonify({"error": "Device not found"}), 404

    logging.info(f"Details retrieved for device ID: {device_id}")
    return jsonify({
        "id": device_id,
        "details": details
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
