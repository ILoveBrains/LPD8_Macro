import comtypes
from pycaw.pycaw import AudioUtilities

class WindowsAudio:
    def __init__(self):
        self.master_volume = None

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