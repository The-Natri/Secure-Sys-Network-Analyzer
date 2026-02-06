# SECURE.SYS // Hybrid Network Security Analyzer

## 🛡️ Project Overview

SECURE.SYS is a next-generation network traffic analyzer that combines **Deterministic Finite Automata (DFA)** with **Machine Learning (AI)** to detect cyber threats in real-time. Unlike traditional firewalls that rely solely on static rules, this system uses a hybrid approach:

1.  **DFA Layer 1 (Structure):** Validates packet integrity using a strict state machine ($O(n)$ complexity).
2.  **DFA Layer 2 (Firewall):** Scans for malicious signatures (SQLi, XSS) using Multi-Pattern Matching.
3.  **AI Core (Anomaly Detection):** Uses Naive Bayes & Entropy Analysis to detect obfuscated attacks.

## 🚀 Features

- **Real-Time Visuals:** Live State Transition Graph (q0 → q1 → q2) animated as you type.
- **Zero-Latency Scanning:** Linear time complexity for immediate threat detection.
- **Hybrid Intelligence:** Catches both known attacks (Signatures) and unknown threats (Entropy/ML).
- **Interactive Dashboard:** Cyberpunk UI with live terminal logs and status modules.

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3 (Neon UI), JavaScript (Live Visualization).
- **Backend:** Python (Flask).
- **Logic:** Custom DFA Implementation (No Regex), Scikit-Learn (ML).

## 🎓 Theory Used

- **Finite Automata:** Used for strict protocol parsing.
- **Transition Functions:** $\delta(q, \sigma) \to q'$ mapping input characters to states.
- **Probability Theory:** $P(Attack | Text)$ used in the Naive Bayes Classifier.

🛠️ Installation & Setup Guide
Follow these steps to set up SECURE.SYS on your local machine.

Prerequisites
Python 3.x installed (Type python --version in your terminal to check).

VS Code (Recommended) or any code editor.

Step 1: Get the Project
Download the project folder (or clone the repository).

Open the folder in VS Code.

Open a New Terminal (Ctrl + `).

Step 2: Create a Virtual Environment (Recommended)
This isolates our project so it doesn't conflict with other Python apps.

For Windows:

Bash
python -m venv venv
.\venv\Scripts\Activate
(You should see a green (venv) appear at the start of your terminal line. If you get a permission error, type Set-ExecutionPolicy Unrestricted -Scope Process and try again).

For Mac / Linux:

Bash
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
This installs Flask, Scikit-Learn, and the AI tools.

Bash
pip install -r requirements.txt
Alternatively, you can install them manually:

Bash
pip install flask scikit-learn joblib numpy
Step 4: Wake up the AI Brain 🧠
Before running the website, we need to teach the AI what an attack looks like. Run the training script once.

Bash
python train_model.py
Success Message: You should see [INFO] Model trained and saved to ml/security_model.pkl.

Step 5: Launch the System 🚀
Start the main server.

Bash
python app.py
Success Message:

Plaintext
🚀 Advanced Classifier Running...

- Running on http://127.0.0.1:5100
  Step 6: Access the Dashboard
  Open your web browser (Chrome/Edge) and go to: 👉 http://127.0.0.1:5100

❌ Troubleshooting
Q: I get ModuleNotFoundError: No module named 'flask' A: You forgot Step 3. Run pip install flask. If that doesn't work, ensure your virtual environment is active (Step 2).

Q: The website shows a 404 Error. A: Make sure you are visiting port 5100 (not 5000). Check the URL in your terminal.

Q: I get "Access Denied" when creating the venv. A: Run VS Code as Administrator or use the command: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser.

Q: The AI verdict is always "SKIPPED". A: This happens if security_model.pkl is missing. Run python train_model.py again.
