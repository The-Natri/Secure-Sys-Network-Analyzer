# ml/anomaly_detector.py
import joblib
import os
import math

class AnomalyDetector:
    def __init__(self):
        # 1. Load AI
        model_path = os.path.join(os.path.dirname(__file__), 'security_model.pkl')
        try:
            self.model = joblib.load(model_path)
            self.model_loaded = True
        except FileNotFoundError:
            self.model_loaded = False
        
        # 2. TUNED THRESHOLDS
        self.MAX_ENTROPY = 4.0  # Bumped up slightly to be safer
        self.MAX_SPECIAL_RATIO = 0.35 
        self.MIN_LENGTH_FOR_ENTROPY = 25 # NEW: Ignore entropy for short texts

    def calculate_entropy(self, text):
        if not text: return 0
        entropy = 0
        length = len(text)
        for x in range(256):
            p_x = float(text.count(chr(x))) / length
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def predict(self, message):
        # Feature 1: Entropy
        entropy = self.calculate_entropy(message)
        
        # Feature 2: Special Character Ratio 
        # (Ignore spaces and protocol chars 'HT}')
        clean_msg = [c for c in message if c not in [' ', '}', 'H', 'T']]
        if len(clean_msg) > 0:
            specials = sum(1 for c in clean_msg if not c.isalnum())
            special_ratio = specials / len(clean_msg)
        else:
            special_ratio = 0

        # Feature 3: AI Prediction
        ai_result = "NORMAL"
        confidence = 0
        if self.model_loaded and message:
            ai_result = self.model.predict([message])[0]
            confidence = self.model.predict_proba([message]).max()

        print(f"\n[Hybrid Scan] Input: '{message}'")
        print(f"  - Length: {len(message)}")
        print(f"  - Entropy: {entropy:.2f}")
        print(f"  - Symbols: {special_ratio:.2f}")

        # --- DECISION LOGIC ---
        
        # 1. Trust High-Confidence AI Attack Detection
        if ai_result != "NORMAL" and confidence > 0.60:
            return f"ANOMALOUS ({ai_result})"
        
        # 2. Check Density (Catches "!@#$")
        if special_ratio > self.MAX_SPECIAL_RATIO:
            return "ANOMALOUS (Suspicious Symbols)"

        # 3. Check Entropy (ONLY if message is long enough)
        # This fixes the "Meeting at 10am" bug
        if len(message) > self.MIN_LENGTH_FOR_ENTROPY:
            if entropy > self.MAX_ENTROPY:
                return "ANOMALOUS (High Entropy)"

        return "NORMAL"

def check_anomaly(message):
    detector = AnomalyDetector()
    return detector.predict(message)