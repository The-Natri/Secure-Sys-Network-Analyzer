# dfa/structure_dfa.py

class StructureDFA:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3', 'q_dead'}
        self.start_state = 'q0'
        self.accept_states = {'q3'}
        
        # H (Start) -> T (Type) -> ...
        self.transitions = {
            ('q0', 'H'): 'q1', ('q0', 'h'): 'q1',
            ('q1', 'T'): 'q2', ('q1', 't'): 'q2',
        }
        self.current_state = self.start_state

    def process_input(self, input_string):
        self.current_state = self.start_state
        
        for char in input_string:
            if self.current_state == 'q2':
                # NEW RULE: The delimiter is '}' (Shift+])
                # This allows you to type 'e' or 'E' inside the message safely.
                if char == '}': 
                    next_state = 'q3'
                else:
                    next_state = 'q2' # Stay in Data
            else:
                next_state = self.transitions.get((self.current_state, char), 'q_dead')
            
            self.current_state = next_state
            if self.current_state == 'q_dead': break

        return self.is_accepted()

    def is_accepted(self):
        return self.current_state in self.accept_states

def validate_structure(packet_string):
    dfa = StructureDFA()
    return dfa.process_input(packet_string)