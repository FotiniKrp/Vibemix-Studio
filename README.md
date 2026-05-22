# Vibemix-Studio

Video Branch 
opencv, mediapipe σε python

Audio Branch

βιβλιοθήκες: sounddevice, pedalboard, vocoder άκυρο python έχει καθυστέρηση 
JUCE framework(C++) επικοινωνεί απευθείας με hardware
+ OSC για επικοινωνία με Python εφόσον τρέχει στον ίδιο υπολογιστή, τα μηνύματα μπορούν να ταξιδέψουν εσωτερικά μέσω της διεύθυνσης Localhost (δηλαδή την IP: 127.0.0.1).

Βήμα 1: άδειο JUCE Standalone App που απλά στέλνει το μικρόφωνο στα ηχεία.

Βήμα 2: OSC Listener στο JUCE. Βάζεις την Python να στέλνει νούμερα και τυπώνεις αυτά τα νούμερα στην κονσόλα της C++.

Επίσης, το JUCE δημιουργεί ένα "αόρατο" παράθυρο browser (χρησιμοποιώντας το WebView2 στα Windows ή το WKWebView στο Mac) μέσα στο .exe. Μέσα σε αυτό το παράθυρο, φορτώνει το React App σου.
Πώς μιλάνε μεταξύ τους: Το JUCE σου δίνει μια "γέφυρα" (JavaScript Bridge). Μέσα στο React, καλείς συναρτήσεις JavaScript (π.χ. window.juce.sendParameter('gain', 0.8)), και το JUCE τις πιάνει ακαριαία στη C++ για να αλλάξει τον ήχο!
