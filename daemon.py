import mido
import keyboard
import mouse
import json
import os
import threading
from flask import Flask, jsonify, request, send_from_directory
from audio_mixer import WindowsAudio

# --- CONFIGURATION ---
TARGET_PORT = "LPD8 0" 
CONFIG_FILE = "config.JSON"

# --- WEB SERVER SETUP ---
app = Flask(__name__)

@app.route('/')
def serve_ui():
    return send_from_directory('static', 'index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    if not os.path.exists(CONFIG_FILE):
        return jsonify({"program_1": {"pads": {}, "knobs": {}}})
    with open(CONFIG_FILE, 'r') as f:
        try:
            return jsonify(json.load(f))
        except json.JSONDecodeError:
            return jsonify({"error": "Malformed configuration file"}), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(request.json, f, indent=4)
    return jsonify({"status": "success"})

def run_web_server():
    # Runs the Flask server quietly
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

# --- MIDI DAEMON SETUP ---
def load_config():
    if not os.path.exists(CONFIG_FILE): return {}
    with open(CONFIG_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def run_midi_daemon():
    audio = WindowsAudio()
    print(f"Connecting to {TARGET_PORT}...")
    
    try:
        with mido.open_input(TARGET_PORT) as inport:
            print("--- MIDI Listener Active ---")
            print("Check this window to see hardware IDs and triggered actions.\n")
            
            for msg in inport:
                # Refresh config on every event so Web UI changes are instant
                config = load_config()
                current_prog = "program_1"

                # Handle Pad Presses (Notes)
                if msg.type == 'note_on' and msg.velocity > 0:
                    note_str = str(msg.note)
                    action = config.get(current_prog, {}).get("pads", {}).get(note_str)
                    
                    if action:
                        print(f"[PAD] ID {note_str} -> Executing: {action}")
                        if action.startswith("mouse:"):
                            cmd = action.split(":")[1]
                            if cmd == "left": mouse.click('left')
                            elif cmd == "right": mouse.click('right')
                            elif cmd == "middle": mouse.click('middle')
                            elif cmd == "double": mouse.double_click('left')
                            elif cmd == "scroll_up": mouse.wheel(delta=5)
                            elif cmd == "scroll_down": mouse.wheel(delta=-5)
                        
                        elif action.startswith("type:"):
                            # Types the text following the colon
                            keyboard.write(action.split(":", 1)[1])
                        else:
                            # Default behavior: send keyboard shortcut
                            keyboard.send(action)
                    else:
                        print(f"[PAD] ID {note_str} is unmapped. (Velocity: {msg.velocity})")
                
                # Handle Knob Turns (Control Change)
                elif msg.type == 'control_change':
                    knob_id = msg.control
                    knob_str = str(knob_id)
                    knobs_config = config.get(current_prog, {}).get("knobs", {})
                    action = knobs_config.get(knob_str)
                    
                    if action == "volume_master":
                        audio.set_master(msg.value)
                        if msg.value % 10 == 0:
                            print(f"[KNOB] ID {knob_str} -> Master Volume: {msg.value}")
                    else:
                        # Try dynamic app volume assignment
                        reserved = list(knobs_config.keys())
                        app_name = audio.set_app_volume(knob_id, msg.value, reserved)
                        
                        if app_name:
                            if msg.value % 10 == 0:
                                print(f"[KNOB] ID {knob_id} -> {app_name} Volume: {msg.value}")
                        elif action:
                            print(f"[KNOB] ID {knob_str} -> Action: {action} (Value: {msg.value})")
                        else:
                            print(f"[KNOB] ID {knob_str} is unmapped. (Value: {msg.value})")

    except Exception as e:
        print(f"MIDI Error: {e}")

# --- START EVERYTHING ---
if __name__ == "__main__":
    # 1. Start Web Server in a background thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("Web UI available at http://127.0.0.1:5000")

    # 2. Start MIDI Daemon in the main thread
    run_midi_daemon()