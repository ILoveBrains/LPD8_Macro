from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)
CONFIG_FILE = 'config.json'

# 1. Serve the HTML interface
@app.route('/')
def serve_ui():
    return send_from_directory('static', 'index.html')

# 2. API to send the current JSON to the browser
@app.route('/api/config', methods=['GET'])
def get_config():
    if not os.path.exists(CONFIG_FILE):
        return jsonify({"program_1": {"pads": {}, "knobs": {}}})
    with open(CONFIG_FILE, 'r') as f:
        return jsonify(json.load(f))

# 3. API to save changes from the browser back to the JSON file
@app.route('/api/config', methods=['POST'])
def save_config():
    new_config = request.json
    with open(CONFIG_FILE, 'w') as f:
        json.dump(new_config, f, indent=4)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    print("Starting LPD8 Web UI on http://127.0.0.1:5000")
    # debug=True automatically reloads the server if you change the Python code
    app.run(host='127.0.0.1', port=5000, debug=True)