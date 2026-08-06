# Vibemix-Studio

Video Branch 
opencv, mediapipe σε python

Audio Branch

βιβλιοθήκες: sounddevice, pedalboard, vocoder άκυρο python έχει καθυστέρηση 
JUCE framework(C++) επικοινωνεί απευθείας με hardware
+ OSC για επικοινωνία με Python εφόσον τρέχει στον ίδιο υπολογιστή, τα μηνύματα μπορούν να ταξιδέψουν εσωτερικά μέσω της διεύθυνσης Localhost (δηλαδή την IP: 127.0.0.1).

Web sockets για επικοινωνία python output με react app!! to do

For johnny: Αν αλλάζεις το roomSize του DSP Reverb ακαριαία κάθε φορά που φτάνει ένα OSC πακέτο, ο ήχος θα κάνει ψηφιακά "clicks" / "zipper noise".
-> Χρησιμοποιούμε ένα juce::SmoothedValue για να δημιουργήσουμε μια ομαλή γραμμική μετάβαση από δείγμα σε δείγμα.

thread saftey:
Στην εφαρμογή σου τρέχουν δύο διαφορετικά νήματα (threads) ταυτόχρονα: λαμβάνονται τα OSC πακέτα από την Python/κάμερα. Κάθε φορά που έρχεται ένα πακέτο, αυτό το thread προσπαθεί να γράψει τη νέα τιμή. To auido thread εκτελείται σε πραγματικό χρόνο (π.χ. κάθε 5-10 milliseconds) και διαβάζει τις τιμές για να επεξεργαστεί τα δείγματα ήχου. 

```text
 ┌────────────────────────────────────────────────────────┐
 │           ΠΗΓΗ ΧΕΙΡΟΝΟΜΙΩΝ (Python / Camera)           │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼ (Network Thread @ 30-60 Hz)
                 [OSC Packets: "/gesture/y"]
                             │
 ┌───────────────────────────▼────────────────────────────┐
 │                  JUCE OSC RECEIVER                     │
 │  1. Κανονικοποίηση (Normalize: 0.0 - 1.0)              │
 │  2. Thread-Safe Αποθήκευση σε std::atomic              │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼ (Shared Memory)
                [ std::atomic<float> gestureY ]
                             │
 ┌───────────────────────────▼────────────────────────────┐
 │                JUCE AUDIO THREAD / DSP                 │
 │                  (processBlock @ 44.1 kHz)             │
 │                                                        │
 │  1. Read Atomic Value ────────► std::atomic            │
 │  2. Smooth Value (50ms) ──────► juce::SmoothedValue    │
 │  3. Value Mapping ─────► Reverb / Filter / etc. │
 └───────────────────────────┬────────────────────────────┘
                             │
                             ▼
                 [ AUDIO OUTPUT / SPEAKER ]
```
Ιδεες εφε
Λογική:
```text
[Επίπεδο Χρήστη / Χειρονομιών]
         │
         ▼ (Έλεγχος 1-2 Macro Παραμέτρων, π.χ. Gesture X/Y)
┌────────────────────────────────────────────────────────┐
│  PRESET: "Ethereal Vocal Shimmer Pad"                  │
│  - Macro 1: "Ether Intensity" (Ελέγχει 4 DSP μαζί)     │
│  - Macro 2: "Space Size"      (Ελέγχει Reverb/Filter)  │
└────────────────────────────────────────────────────────┘
         │
         ▼ (Εσωτερική Δρομολόγηση)
[Εσωτερικό DSP Chain] ── HPF ➔ Delay ➔ Pitch Shift ➔ Reverb
```

1. Underwater/muffled voice
2. Autotuned/robotic
3. Vintage radio/telephone
4. Ariana garnde voice stacking haha (pop)
5. Choir εφε
6. Singing in empty church or something
7. glitch voice -> κλεινει η παλαμη π.χ. κι κολλαει
