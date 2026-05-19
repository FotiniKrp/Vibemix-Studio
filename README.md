# Vibemix-Studio

Video Branch 
opencv, mediapipe σε python

Audio Branch

βιβλιοθήκες: sounddevice, pedalboard, vocoder άκυρο python έχει καθυστέρηση by default
JUCE framework(C++) επικοινωνεί απευθείας με hardware
OSC λειτουργεί μέσω δικτύου. Εφόσον και η Python τρέχει στον ίδιο υπολογιστή, τα μηνύματα ταξιδεύουν εσωτερικά μέσω της διεύθυνσης Localhost (δηλαδή την IP: 127.0.0.1). Το μόνο που ορίζεις είναι μια "πόρτα" (Port), π.χ. την 8000.
Βήμα 1: Φτιάχνεις ένα άδειο JUCE Standalone App που απλά στέλνει το μικρόφωνο στα ηχεία.

Βήμα 2: Ενσωματώνεις τον OSC Listener στο JUCE. Βάζεις την Python να στέλνει νούμερα και τυπώνεις αυτά τα νούμερα στην κονσόλα της C++.

Βήμα 3: Συνδέεις τον std::atomic<float> του OSC με το Gain του μικροφώνου (για να ελέγχεις την ένταση με το χέρι).

Το JUCE δημιουργεί ένα "αόρατο" παράθυρο browser (χρησιμοποιώντας το WebView2 στα Windows ή το WKWebView στο Mac) μέσα στο .exe. Μέσα σε αυτό το παράθυρο, φορτώνει το React App σου.
