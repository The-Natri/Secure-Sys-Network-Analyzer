import os
from flask import Flask, request, jsonify, send_from_directory
from dfa.structure_dfa import validate_structure
from dfa.content_dfa import advanced_classify 
from ml.anomaly_detector import check_anomaly

# We remove 'static_url_path' here to handle routes manually for better control
app = Flask(__name__, static_folder='web')

# --- ROUTE 1: SHOW THE HOMEPAGE (This was missing!) ---
@app.route('/')
def index():
    # This looks inside the 'web' folder and sends 'index.html' to the browser
    return send_from_directory('web', 'index.html')

# --- ROUTE 2: SERVE CSS & JS FILES ---
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

# --- ROUTE 3: THE ANALYZER LOGIC ---
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    message = data.get('message', '')
    
    # 1. Structure Analysis
    structure_valid = validate_structure(message)
    
    # 2. Advanced Classification
    detected_types = advanced_classify(message)
    
    # 3. ML Analysis
    if "NORMAL_CHAT" in detected_types:
        ml_result = check_anomaly(message)
    else:
        ml_result = "SKIPPED (Signature Found)"

    # --- FINAL DECISION LOGIC ---
    final_verdict = "ALLOWED"
    
    # Priority 1: Known Cyberattacks
    if "SQL_INJECTION" in detected_types or "XSS_ATTACK" in detected_types or "CMD_INJECTION" in detected_types:
        final_verdict = "BLOCKED (Cyberattack)"
        
    # Priority 2: ML Anomaly
    elif "ANOMALOUS" in ml_result: 
        final_verdict = "QUARANTINED (Anomaly)"
        
    # Priority 3: Spam
    elif "SPAM" in detected_types:
        final_verdict = "FLAGGED (Spam)"
        
    # Priority 4: Invalid Protocol
    elif not structure_valid:
        final_verdict = "FLAGGED (Invalid Protocol)"
        
    return jsonify({
        "structure_valid": structure_valid,
        "classification": detected_types,
        "ml_result": ml_result,
        "final_status": final_verdict
    })

if __name__ == '__main__':
    print("🚀 Advanced Classifier Running...")
    # Note: You set the port to 5100, so the URL will change!
    app.run(debug=True, port=5100)