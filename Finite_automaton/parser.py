from automaton import Automaton

def load_automaton(file_path):
    """Carrega o autômato a partir de um arquivo TXT."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    states = lines[0].strip().split(": ")[1].split(", ")
    alphabet = lines[1].strip().split(": ")[1].split(", ")
    initial_state = lines[2].strip().split(": ")[1]
    final_states = lines[3].strip().split(": ")[1].split(", ")

    transitions = {}
    for line in lines[5:]:
        parts = line.strip().split(" -> ")
        state_symbol = parts[0].split(", ")
        transitions[(state_symbol[0], state_symbol[1])] = parts[1]

    return Automaton(states, alphabet, transitions, initial_state, final_states)
