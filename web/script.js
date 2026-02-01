async function analyzeMessage() {
    const input = document.getElementById('messageInput').value;
    const btn = document.getElementById('scanBtn');
    
    if (!input) { logToTerminal("ERROR: Input stream empty. Aborting.", "red"); return; }

    // 1. UI: Set Scanning State
    btn.innerText = "SCANNING...";
    btn.disabled = true;
    resetModules();
    logToTerminal(`[INIT] Packet intercepted: "${input}"`, "white");
    
    // Simulate Processing Delay for Effect
    await new Promise(r => setTimeout(r, 600)); 

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: input })
        });
        const data = await response.json();

        // 2. UI: Update Structure Module
        logToTerminal("[DFA-1] Validating Structure...", "cyan");
        updateModule('mod-structure', data.structure_valid ? "STRICT PROTOCOL" : "RAW / UNSTRUCTURED", data.structure_valid);
        
        await new Promise(r => setTimeout(r, 400)); // Small delay

        // 3. UI: Update Firewall Module
        logToTerminal("[DFA-2] Scanning Signatures...", "cyan");
        const firewallStatus = data.classification.join(" + ");
        const isSafeContent = data.classification.includes("NORMAL_CHAT");
        updateModule('mod-firewall', firewallStatus, isSafeContent);

        // 4. UI: Update ML Module
        logToTerminal("[ML-CORE] Calculating Entropy & Probability...", "cyan");
        const isNormalML = data.ml_result === "NORMAL";
        updateModule('mod-ml', data.ml_result, isNormalML);

        // 5. UI: Final Verdict
        const verdictBox = document.getElementById('final-verdict-box');
        const verdictText = document.getElementById('verdict-text');
        verdictBox.classList.remove('hidden');
        verdictText.innerText = data.final_status;
        
        // Color the Verdict Text
        if (data.final_status.includes("ACCEPTED") || data.final_status === "ALLOWED") {
            verdictText.style.color = "var(--accent-green)";
            logToTerminal("VERDICT: PACKET ACCEPTED.", "lime");
        } else {
            verdictText.style.color = "var(--accent-red)";
            logToTerminal(`VERDICT: ${data.final_status}`, "red");
        }

    } catch (error) {
        logToTerminal("FATAL: Server connection lost.", "red");
    }

    btn.innerText = "INITIATE SCAN";
    btn.disabled = false;
}

function updateModule(id, text, isSafe) {
    const mod = document.getElementById(id).querySelector('.mod-status');
    mod.innerText = text;
    mod.className = 'mod-status ' + (isSafe ? 'safe' : 'danger');
}

function resetModules() {
    document.querySelectorAll('.mod-status').forEach(el => {
        el.innerText = "PROCESSING...";
        el.className = 'mod-status pending';
    });
}

function logToTerminal(msg, color) {
    const term = document.getElementById('terminal-logs');
    const line = document.createElement('div');
    line.className = 'log-line';
    line.innerText = msg;
    if (color) line.style.color = color;
    term.appendChild(line);
    term.scrollTop = term.scrollHeight; // Auto scroll
}

// --- LIVE DFA VISUALIZER LOGIC ---

// Listen for typing in the input box
document.getElementById('messageInput').addEventListener('input', function(e) {
    updateDFAVisual(e.target.value);
});

function updateDFAVisual(text) {
    // 1. Reset everything to grey
    resetVisuals();
    
    // 2. Determine Current State
    // q0 = Start
    // q1 = Has 'H'
    // q2 = Has 'H' + 'T'
    // q3 = Has 'H' + 'T' + ... + '}'
    
    let currentState = 'q0';
    let error = false;

    // Handle Empty Input
    if (text.length === 0) {
        highlightState('q0');
        return;
    }

    // Step 1: Check First Char (H)
    if (text[0] === 'H' || text[0] === 'h') {
        currentState = 'q1';
    } else {
        error = true;
    }

    // Step 2: Check Second Char (T)
    if (!error && text.length > 1) {
        if (text[1] === 'T' || text[1] === 't') {
            currentState = 'q2';
        } else {
            error = true;
        }
    }

    // Step 3: Check End Char (})
    if (!error && text.length > 2) {
        currentState = 'q2'; // Still in data...
        if (text.endsWith('}')) {
            currentState = 'q3';
        }
    }

    // 3. Apply Colors based on State
    if (error) {
        document.getElementById('node-q0').classList.add('active-error');
    } else {
        // Walk through the states lighting them up
        if (currentState === 'q0') {
            highlightState('q0');
        }
        else if (currentState === 'q1') {
            highlightState('q0');
            activateConn('0-1');
            highlightState('q1');
        }
        else if (currentState === 'q2') {
            highlightState('q0'); activateConn('0-1');
            highlightState('q1'); activateConn('1-2');
            highlightState('q2');
        }
        else if (currentState === 'q3') {
            highlightState('q0'); activateConn('0-1');
            highlightState('q1'); activateConn('1-2');
            highlightState('q2'); activateConn('2-3');
            highlightState('q3', true); // TRUE = Success Green
        }
    }
}

// Helper: Turn on a node
function highlightState(id, isSuccess=false) {
    const node = document.getElementById('node-' + id);
    node.classList.add('active');
    if (isSuccess) node.classList.add('active-success');
}

// Helper: Turn on a line
function activateConn(id) {
    document.getElementById('conn-' + id).classList.add('active');
}

// Helper: Turn off everything
function resetVisuals() {
    document.querySelectorAll('.state-node').forEach(el => {
        el.className = 'state-node'; // Remove active/error classes
        if (el.id === 'node-q3') el.classList.add('double-ring'); // Keep the ring
    });
    document.querySelectorAll('.connector').forEach(el => {
        el.classList.remove('active');
    });
}

function clearLogs() {
    document.getElementById('terminal-logs').innerHTML = '';
    logToTerminal("[SYS] Logs cleared. Ready for new input.", "gray");
}