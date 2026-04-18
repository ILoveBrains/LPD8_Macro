from comtypes import CoInitialize
from pycaw.pycaw import AudioUtilities

class WindowsAudio:
    def __init__(self):
        # We must initialize COM to allow background threads to touch Windows Audio
        CoInitialize()
        
        # Get the default speakers
        device = AudioUtilities.GetSpeakers()
        
        # The new, modern pycaw syntax directly exposes the volume interface!
        self.master_volume = device.EndpointVolume

    def set_master(self, midi_value):
        """Converts a MIDI knob turn (0-127) to Windows Volume (0.0 to 1.0)"""
        # Prevent division by zero and cap the math perfectly
        volume_scalar = max(0.0, min(midi_value / 127.0, 1.0))
        
        # Instantly set the Windows master volume
        self.master_volume.SetMasterVolumeLevelScalar(volume_scalar, None)