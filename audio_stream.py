import sounddevice as sd
import numpy as np
import time  
from pedalboard import Pedalboard, VST3Plugin, Reverb, Delay  # <--- Εδώ είναι το έτοιμο εργαλείο vst

vst_path = r'C:\TAL-Vocoder-2.vst3\Contents\x86_64-win\TAL-Vocoder-2.vst3' # will figure out earlier 
vocoder_vst = VST3Plugin(vst_path)
board = Pedalboard([
    Reverb(room_size=0.8, wet_level=0.5),
    Delay(delay_seconds=0.3, feedback=0.4, mix=0.5)
])
#board = Pedalboard([vocoder_vst])


def get_wasapi_details():
    """
    Βρίσκει αυτόματα τις WASAPI συσκευές ήχου και το σωστό sample rate.
    Αν δεν βρει WASAPI (π.χ. σε Mac/Linux), επιστρέφει τις default συσκευές του συστήματος.
    """
    host_apis = sd.query_hostapis()
    wasapi_api = None
    
    # Ψάχνουμε το Windows WASAPI στη λίστα των APIs
    for api in host_apis:
        if api['name'] == 'Windows WASAPI':
            wasapi_api = api
            break
            
    if wasapi_api:
        input_id = wasapi_api['default_input_device']
        output_id = wasapi_api['default_output_device']
        
        # Ρωτάμε τη συσκευή εξόδου ποιο είναι το εργοστασιακό της sample rate
        device_info = sd.query_devices(output_id)
        samplerate = int(device_info['default_samplerate'])
        
        print(f"-> Εντοπίστηκε WASAPI! Input ID: {input_id}, Output ID: {output_id}, Sample Rate: {samplerate}Hz")
        return input_id, output_id, samplerate
    else:
        # Fallback σε περίπτωση που τρέξει κάπου εκτός Windows
        print("-> Το Windows WASAPI δεν βρέθηκε. Χρήση default ρυθμίσεων συστήματος.")
        default_in, default_out = sd.default.device
        return default_in, default_out, 44100

# first no bluetooth earphone cause they have delay ~100 - 300 ms
# second drivers of windows -> WASAPI
input_device, output_device, samplerate = get_wasapi_details()

channels = 2
blocksize = 512

def audio_callback(indata, outdata, frames, time_info, status):
    if status:
        print(status)
        
    # Διαχείριση Stereo πίνακα
    # Το sounddevice δίνει τον ήχο ως (samples, channels) -> (512, 2)
    # Το pedalboard τον θέλει ως (channels, samples) -> (2, 512)
    # Κάνουμε ανάστροδο πίνακα με το .T για να συμφωνούν
    audio_data = indata.T
    
    # Περνάμε τον Stereo ήχο από το VST
    effected = board.process(audio_data, sample_rate=samplerate, reset=False)
    
    # Έλεγχος ασφαλείας (τώρα ελέγχουμε τη δεύτερη διάσταση του πίνακα)
    if effected.shape[1] == frames:
        # Μετατρέπουμε τον ήχο ξανά σε (samples, channels) για την έξοδο
        outdata[:] = effected.T
    else:
        outdata.fill(0)
    
try:
    with sd.Stream(
        device=(input_device, output_device),       
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
