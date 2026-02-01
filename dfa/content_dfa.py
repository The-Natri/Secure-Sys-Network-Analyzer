# dfa/content_dfa.py

class ContentDFA:
    def __init__(self):
        self.start_state = 'q0'
        self.current_state = 'q0'
        self.transitions = {}
        self.output_table = {} 
        
        # EXPANDED PATTERN DATABASE
        self.signatures = {
            "SQL_INJECTION": [
                "SELECT", "DROP", "UNION", "OR 1=1", "DELETE", "INSERT", "UPDATE", "--", "/*"
            ],
            "XSS_ATTACK": [
                "SCRIPT", "ALERT", "ONERROR", "IFRAME", "BODY", "IMG SRC", "ONCLICK", "JAVASCRIPT"
            ],
            "CMD_INJECTION": [
                "RM -RF", "WHOAMI", "CAT /ETC/PASSWD", "NC -E", "BASH -I", "SUDO", "PING -C"
            ],
            "PATH_TRAVERSAL": [
                "../", "..\\", "/ETC/", "C:\\WINDOWS"
            ],
            "SPAM": [
                "FREE MONEY", "CLICK HERE", "WINNER", "URGENT", "BUY NOW", "LIMITED OFFER", "CONGRATULATIONS"
            ]
        }
        
        self._build_transition_table()

    def _build_transition_table(self):
        self.transitions = {}
        for category, patterns in self.signatures.items():
            for word in patterns:
                current = 'q0'
                for i, char in enumerate(word):
                    next_state = f"q_{word[:i+1]}"
                    self.transitions[(current, char)] = next_state
                    current = next_state
                self.output_table[current] = category

    def classify_content(self, content_string):
        self.current_state = self.start_state
        detected_categories = set()
        
        # Normalize to UPPERCASE for scanning
        content_upper = content_string.upper()
        
        print(f"\n[Firewall Scan] Input: '{content_string}'")
        
        for i, char in enumerate(content_upper):
            if (self.current_state, char) in self.transitions:
                self.current_state = self.transitions[(self.current_state, char)]
                if self.current_state in self.output_table:
                    cat = self.output_table[self.current_state]
                    print(f"  ⚠ Match: {cat}")
                    detected_categories.add(cat)
            else:
                if ('q0', char) in self.transitions:
                    self.current_state = self.transitions[('q0', char)]
                else:
                    self.current_state = 'q0'
        
        if not detected_categories:
            return ["NORMAL_CHAT"]
        return list(detected_categories)

def advanced_classify(content_string):
    dfa = ContentDFA()
    return dfa.classify_content(content_string)