import comtypes
from pycaw.pycaw import AudioUtilities

class WindowsAudio:
    def __init__(self):
        self.master_volume = None
        self.app_map = {}  # knob_id (int) -> process_name (str)

    def _get_volume_interface(self):
        """Initializes COM and gets the volume interface for the current thread."""
        try:
            comtypes.CoInitialize()
        except Exception:
            # Already initialized in this thread
            pass
        device = AudioUtilities.GetSpeakers()
        return device.EndpointVolume

    def set_master(self, midi_value):
        """Converts a MIDI knob turn (0-127) to Windows Volume (0.0 to 1.0)"""
        if self.master_volume is None:
            self.master_volume = self._get_volume_interface()
        # Prevent division by zero and cap the math perfectly
        volume_scalar = max(0.0, min(midi_value / 127.0, 1.0))
        
        # Instantly set the Windows master volume
        self.master_volume.SetMasterVolumeLevelScalar(volume_scalar, None)

    def set_app_volume(self, knob_id, midi_value, reserved_knobs):
        """
        Updates sessions and sets volume for the app assigned to knob_id.
        reserved_knobs: list of knob IDs used for other things in config.JSON
        """
        try:
            comtypes.CoInitialize()
        except Exception:
            pass
        
        sessions = AudioUtilities.GetAllSessions()
        # Filter for apps that have an active process
        active_sessions = {s.Process.name(): s for s in sessions if s.Process}
        active_names = set(active_sessions.keys())

        # 1. Cleanup: Remove apps that are no longer running
        for k, name in list(self.app_map.items()):
            if name not in active_names:
                print(f"[AUDIO] App '{name}' closed. Knob {k} is now free.")
                del self.app_map[k]

        # 2. Assignment: Assign new apps to available knobs (checking slots 1-20)
        for name in active_names:
            if name not in self.app_map.values():
                assigned = False
                for k in range(1, 21): 
                    if str(k) not in reserved_knobs and k not in self.app_map:
                        self.app_map[k] = name
                        print(f"[AUDIO] New app detected: '{name}'. Assigned to knob {k}.")
                        assigned = True
                        break
                if not assigned and name not in self.app_map.values():
                    print(f"[WARNING] Knobs are full! Cannot assign '{name}'.")

        # 3. Apply volume if this specific knob is mapped to an app
        if knob_id in self.app_map:
            app_name = self.app_map[knob_id]
            session = active_sessions.get(app_name)
            if session:
                volume = session.SimpleAudioVolume
                volume_scalar = max(0.0, min(midi_value / 127.0, 1.0))
                volume.SetMasterVolume(volume_scalar, None)
                return app_name
        return None