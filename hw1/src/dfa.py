from collections import deque
import os

class DFA:
    def __init__(self, states: set, alphabet: set, transitions: dict, initial_state: str, final_states: set):
        self.states = states
        self.alphabet = alphabet
        self.transition = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def has_accepting_path(self) -> bool: # BFS
        visited_states = set()

        queue = deque([self.initial_state]) # expects iterable, do not avoid the brackets for the list because it will iterate over the string

        while queue:
            current_state = queue.popleft()
            if current_state in self.final_states:
                return True
            if current_state in visited_states:
                continue
            visited_states.add(current_state)

            for letter in self.alphabet:
                if letter not in self.transition[current_state]:
                    continue
                following_state = self.transition[current_state][letter]
                if following_state not in visited_states:
                    queue.append(following_state)
        # if no path to a final states is reached up until this point, the dfa has a void language
        return False

    def accepts(self, string: str) -> bool:
        current_state = self.initial_state
        for char in string:
            if char not in self.alphabet:
                raise ValueError(f"The symbol {char} is not in the alphabet.")
            # no transition available for the current state
            if current_state not in self.transition:
                return False
            if char not in self.transition[current_state]:
                return False
            current_state = self.transition[current_state][char]
        # verifies if the dfa has reached a final state
        return current_state in self.final_states

def validate_dfa(states: set, alphabet: set, transitions: dict, initial_state: set, final_states: set) -> bool:
    errors = set()
    # condition 1: Functia de tranzitie sa aiba starile din multimea de stari declarata
    for state in transitions:
        if state not in states:
            errors.add(f"State {state} is not in the set of states.")
        for key, value in transitions[state].items(): # the value is unique for dfa #TODO: generalise for nfa
            if value not in states:
                errors.add(f"State {value} is not in the set of states.")
            # condition 2: Functia de tranzitie sa contina simboluri din alfabetul definit
            if key not in alphabet:
                errors.add(f"Symbol {key} is not in the alphabet.")

    for state in initial_state:
        if state not in states:
            errors.add(f"Initial state {state} is not in the set of states.")

    for state in final_states:
        if state not in states:
            errors.add(f"Final state {state} is not in the set of states.")
    # condition 3: Să avem o singură stare de început (start)
    if len(initial_state) > 1:
        errors.add(f"Initial state is not unique.")
    elif len(initial_state) == 0:
        errors.add(f"Initial state is not defined.")
    # condition 4: Dacă se comenteaza elemente ale alfabetului sau ale multimii starilor
    # si sunt utilizate in functia de tranzitie atunci automatul este INVALID

    # valid through the parsing of the data - if a symbol is commented, then it will not be added to the alphabet
    # and the check (3) will fail
    if len(errors) > 0:
        print("\33[91mThe data does not create a valid DFA.\33[0m")
        print("Errors:")
        for error in errors:
            print(error)
        return False
    return True

def read_cfg(path: str) -> DFA:
    try:
        states = set()
        alphabet = set()
        transition = {}
        initial_state = set()
        final_states = set()
        # keep track of the section in the file
        section = None
        with open(path) as f:
            for line in f:
                line = line.strip()
                line = line.strip(":")
                if line[0] == "#":
                    continue
                # identify section of cfg file
                match line.lower():
                    case "sigma":
                        section = "sigma"
                        continue
                    case "states":
                        section = "states"
                        continue
                    case "transitions":
                        section = "transitions"
                        continue
                    case "end":
                        section = None
                        continue
                # parse each section's data
                match section:
                    case None:
                        continue
                    case "sigma":
                        alphabet.add(line)
                        continue
                    case "states":
                        line = line.split(", ")
                        state = line[0]
                        # see if the state is final or initial
                        states.add(state)
                        if len(line) == 2:
                            if line[1].lower() == "s":
                                initial_state.add(state)
                            elif line[1].lower() == "f":
                                final_states.add(state)
                        elif len(line) == 3: # e.g q0, S, F
                            initial_state.add(state)
                            final_states.add(state)
                        continue
                    case "transitions":
                        start, letter, end = line.split(', ')
                        if start not in transition:
                            transition[start] = {letter:end}
                        else:
                            transition[start][letter] = end
                        continue
        if validate_dfa(states, alphabet, transition, initial_state, final_states):
            return DFA(states, alphabet, transition, initial_state.pop(), final_states)
        else:
            return
    except FileNotFoundError:
        print("The file at f{path} not found.")
        return None

def word_processor(dfa: DFA) -> None:
    while True:
        word = input("Enter a word: ")
        if word == "exit":
            print("\033[93mExiting word processor.\033[0m")
            break
        if dfa.accepts(word) and word != "":
            print(f"\033[92mThe word {word} is accepted by the DFA.\033[0m")
        elif word != "":
            print(f"\033[91mThe word {word} is not accepted by the DFA.\033[0m")

        if dfa.accepts(word) and word == "":
            print(f"\033[92mThe word λ is accepted by the DFA.\033[0m")
        elif word == "":
            print(f"\033[91mThe word λ is not accepted by the DFA.\033[0m")
    return

def main():

    config_filename = input("Enter name of config file: ").strip()
    path = os.path.join(os.path.dirname(__file__), '..', 'config', config_filename)
    dfa = read_cfg(path)
    if dfa is None:
        return
    if not dfa.has_accepting_path():
        print("The DFA has a void language.")
    else:
        word_processor(dfa)
if __name__ == "__main__":
    main()