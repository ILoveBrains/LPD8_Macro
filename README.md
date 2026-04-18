### Akai LPD8 Macro Daemon
```python?code_reference&code_event_index=2


Akai LPD8 Macro Daemon is a lightweight, local background daemon and Web UI that transforms the Akai LPD8 MIDI controller into a system-wide macro pad and audio mixer. 

Built with Python and Flask, this tool bypasses heavy proprietary software and allows you to map pads to custom keyboard shortcuts and link knobs to your system volume, all managed through a live-updating web interface.

## Features

* **Hardware-to-OS Macros:** Map the 8 drum pads to execute system-level keyboard shortcuts (e.g., `ctrl+c`, `windows`, `ctrl+shift+esc`).
* **Zero-Latency Audio Mixing:** Map the 8 potentiometers directly to your Windows Master Volume using the Windows Core Audio API.
* **Local Web UI:** A sleek, Bootstrap-powered visual editor running on `localhost`.
* **Hot-Reloading JSON:** Macros are saved in a `config.JSON` file and reload instantly the moment you hit a physical pad. No restarting the daemon required.
* **Unified Threading:** The MIDI listener and Web Server run concurrently in a single script.

## Project Structure

LPD8_Macro/
├── daemon.py             # Main execution script (MIDI Listener + Flask Server)
├── audio_mixer.py        # Windows Core Audio API hook (pycaw)
├── config.JSON           # Live-updating configuration file
├── requirements.txt      # Python dependencies
└── static/
    └── index.html        # The Bootstrap Web UI
```

## Installation & Setup

### Prerequisites
* **Python 3.8+**
* **Windows 10/11** (The current audio and keyboard hooks use Windows-specific libraries, though the architecture is designed to be cross-platform adaptable).
* Ensure all other Akai Editor software or DAWs are **CLOSED**. Windows MIDI is single-client; if another app has the board open, this daemon cannot listen to it.

### 1. Set up the Environment
Open your terminal and clone/create the project folder, then set up a virtual environment:
```bash
mkdir LPD8_Macro
cd LPD8_Macro
python -m venv venv
```

Activate the environment:
* **Windows (Command Prompt):** `venv\\Scripts\\activate`
* **Windows (PowerShell):** `.\\venv\\Scripts\\Activate.ps1`

### 2. Install Dependencies
Install the required libraries to handle MIDI, HTTP requests, OS keystrokes, and Audio:
```bash
pip install mido python-rtmidi flask keyboard pycaw comtypes
```

## Usage

1. **Plug in the Akai LPD8.** Ensure the `PAD` button is illuminated on the hardware so it sends standard note data.
2. **Start the Daemon:**
   ```bash
   python daemon.py
   ```
3. **Open the Web UI:** Open your browser and navigate to `http://127.0.0.1:5000`.
4. **Map Your Board:** * Click any pad or knob on the screen.
   * Enter the **Hardware ID** (Check your terminal while twisting a knob or hitting a pad to find its ID).
   * Enter the **Action** (e.g., `volume_master`, `windows`, `ctrl+v`).
   * Click **Save**.
5. **Use it!** Your physical board is instantly updated and ready to go.

## Troubleshooting

* **"Error: Could not open LPD8 0"**: Another application (like Ableton, Chrome WebMIDI, or the official Akai Editor) is holding the MIDI port hostage. Close them and restart the script.
* **"ModuleNotFoundError: No module named 'flask'"**: You forgot to activate your virtual environment before running the script. Run `venv\\Scripts\\activate`.
* **Knobs/Pads not responding**: Make sure you have the correct Hardware IDs mapped in the Web UI. Twist a knob while looking at the terminal window to see its True ID.

---
*Built as a modular hardware controller project.*
```
