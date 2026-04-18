<<<<<<< Updated upstream
from flask import Flask, jsonify, request, send_from_directory
=======
from flask import Flask, jsonify, request, send_from_directory, send_file
>>>>>>> Stashed changes
import json
import os

app = Flask(__name__)
<<<<<<< Updated upstream
CONFIG_FILE = 'config.json'
=======
CONFIG_FILE = 'config.JSON'
>>>>>>> Stashed changes

# 1. Serve the HTML interface
@app.route('/')
def serve_ui():
<<<<<<< Updated upstream
    return send_from_directory('static', 'index.html')
=======
    static_path = os.path.join(os.getcwd(), 'static', 'index.html')
    if os.path.exists(static_path):
        return send_file(static_path)
    return "Static UI files not found. Please ensure the 'static' folder exists.", 404
>>>>>>> Stashed changes

# 2. API to send the current JSON to the browser
@app.route('/api/config', methods=['GET'])
def get_config():
    if not os.path.exists(CONFIG_FILE):
        return jsonify({"program_1": {"pads": {}, "knobs": {}}})
    with open(CONFIG_FILE, 'r') as f:
<<<<<<< Updated upstream
        return jsonify(json.load(f))

=======
        try:
            return jsonify(json.load(f))
        except json.JSONDecodeError:
            return jsonify({"error": "Malformed configuration file"}), 500
            
>>>>>>> Stashed changes
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