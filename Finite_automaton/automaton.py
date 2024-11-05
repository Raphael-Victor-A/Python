class Automaton:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def step(self, state, symbol):
        """Realiza uma transição com base no estado atual e no símbolo."""
        return self.transitions.get((state, symbol), None)

    def is_accepted(self, input_string):
        current_state = self.initial_state
        print(f"Iniciando no estado: {current_state}")

        for symbol in input_string:
            if (current_state, symbol) in self.transitions:
                current_state = self.transitions[(current_state, symbol)]
                print(f"Transição para estado: {current_state} com símbolo: {symbol}")
            else:
                print(f"Transição não encontrada para o símbolo: {symbol}")
                return False

# Classes específicas para NFA, DFA e ε-NFA podem ser derivadas dessa classe base.
