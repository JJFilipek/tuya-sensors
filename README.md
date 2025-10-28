# Tuya Sensors API

A lightweight Flask application that exposes a REST API for querying Tuya-powered sensors through the [TinyTuya](https://github.com/jasonacox/tinytuya) cloud library. Use it to request live status information or detailed metadata for your devices registered in the Tuya IoT Cloud.

## Features
- Connects to the Tuya Cloud using TinyTuya credentials.
- Fetch the real-time status of one or many devices in a single request.
- Retrieve descriptive metadata (model, name, product category, etc.) for any registered device.
- Consistent JSON responses and informative logging for easier integration and debugging.

## Prerequisites
- Python 3.10+
- A Tuya IoT Cloud project with API access enabled
- The following credentials generated in the Tuya Cloud Console:
  - **API Region** (e.g. `eu`, `us`, `cn`)
  - **API Key**
  - **API Secret**

## Installation
1. Clone this repository and move into the project directory:
   ```bash
   git clone https://github.com/<your-account>/tuya-sensors.git
   cd tuya-sensors
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
The API reads the port from the optional `PORT` environment variable (defaults to `5000`).

The Tuya Cloud credentials are supplied per request through HTTP headers so you do not need to store them on the server.

## Running the Server
```bash
python main.py
```
The server listens on `0.0.0.0` (all interfaces) and uses the port defined above.

## API Usage
All endpoints expect the following HTTP headers to authenticate with the Tuya Cloud:

```
API-Region: <tuya-region>
API-Key: <tuya-api-key>
API-Secret: <tuya-api-secret>
```

### `GET /devices`
Retrieve the status for one or more devices by providing the `device_id` query parameter multiple times.

```bash
curl \
  -H "API-Region: eu" \
  -H "API-Key: $TUYA_KEY" \
  -H "API-Secret: $TUYA_SECRET" \
  "http://localhost:5000/devices?device_id=DEVICE_ID_1&device_id=DEVICE_ID_2"
```

**Sample response**
```json
[
  {
    "id": "DEVICE_ID_1",
    "status": {
      "result": [ ... ],
      "success": true
    }
  },
  {
    "id": "DEVICE_ID_2",
    "status": {
      "result": [ ... ],
      "success": true
    }
  }
]
```

### `GET /device/<device_id>`
Fetch the live status of a single device.

```bash
curl \
  -H "API-Region: eu" \
  -H "API-Key: $TUYA_KEY" \
  -H "API-Secret: $TUYA_SECRET" \
  "http://localhost:5000/device/DEVICE_ID"
```

**Sample response**
```json
{
  "id": "DEVICE_ID",
  "status": {
    "result": [ ... ],
    "success": true
  }
}
```

### `GET /device/<device_id>/details`
Return the metadata describing the device (name, product category, icon, etc.).

```bash
curl \
  -H "API-Region: eu" \
  -H "API-Key: $TUYA_KEY" \
  -H "API-Secret: $TUYA_SECRET" \
  "http://localhost:5000/device/DEVICE_ID/details"
```

**Sample response**
```json
{
  "id": "DEVICE_ID",
  "details": {
    "id": "DEVICE_ID",
    "name": "Living Room Sensor",
    "product_name": "Temp & Humidity",
    "category": "wsdcg"
  }
}
```

If a device cannot be found or the credentials are invalid, the API returns a descriptive JSON error with an appropriate HTTP status code.

## Logging
The application enables INFO level logging by default, which helps trace device lookups and potential issues. Adjust the `logging.basicConfig` configuration in `main.py` if you need a different verbosity.

## Development Notes
- The Flask development server is enabled with `debug=True`. Avoid using it directly in production—run the app behind a production-grade WSGI server (e.g. Gunicorn or uWSGI).
- TinyTuya communicates with the Tuya cloud; ensure the host machine has outbound internet access.

## License
This project is distributed under the terms of the [MIT License](LICENSE).
