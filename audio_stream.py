import sounddevice as sd
import numpy as np
import time  

# first no bluetooth earphone cause they have delay ~100 - 300 ms
# second drivers of windows -> WASAPI?

samplerate = 48000
channels = 1
blocksize = 128

def audio_callback(indata, outdata, frames, time_info, status):
    # απλό passthrough (χωρίς επεξεργασία)
    outdata[:] = indata

# Χρησιμοποιούμε try/except για να "πιάσουμε" το Ctrl+C κομψά
try:
    with sd.Stream(
        device=(17, 16),       # <--- Εδώ βάλαμε τις WASAPI συσκευές σου!
        samplerate=samplerate,
        channels=channels,
        blocksize=blocksize,
        latency='low',
        callback=audio_callback
    ):
        print("Running... Press Ctrl+C to stop")
        
        # Αντί για sd.sleep, κάνουμε μικρά sleep σε infinite loop
        while True:
            time.sleep(0.1)  # Αυτό επιτρέπει στην Python να ακούει τα signals

except KeyboardInterrupt:
    print("\nΤο πρόγραμμα τερματίστηκε επιτυχώς από τον χρήστη.")