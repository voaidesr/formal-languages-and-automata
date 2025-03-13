class DFA:
    def __init__(self, states: set, alphabet: set, transitions: dict, initial_state: str, final_states: set):
        self.states = states
        self.alphabet = alphabet
        self.transition = transitions
        self.initial_state = initial_state
        self.final_states = final_states
    
    def accepts(self, string: str) -> bool:
        current_state = self.initial_state
        for char in string: 
            if char not in self.alphabet:
                # print(f"The symbol {char} is not in the alphabet\n")
                # smarter:
                raise ValueError(f"The symbol {char} is not in the alphabet.")
            # TODO: check case when no transition is found
            if char not in self.transition[current_state]:
                return False
            current_state = self.transition[current_state][char]
        # verifies if the dfa has reached a final state
        return current_state in self.final_states
    
def read_cfg(path: str) -> DFA: 
    try: 
        states = set()
        alphabet = set()
        transition = {}
        initial_state = ""
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
                        if len(line) > 1:
                            cat = line[1]
                        else:
                            cat = None
                        states.add(state)
                        if cat == "S":
                            initial_state = state
                        elif cat == "F":
                            final_states.add(state)
                        continue
                    case "transitions":
                        start, letter, end = line.split(', ')
                        if start not in transition:
                            transition[start] = {letter:end}
                        else:
                            transition[start][letter] = end
                        continue
        return DFA(states, alphabet, transition, initial_state, final_states)
    except FileNotFoundError:
        print("The file at f{path} not found.")
        return None

def word_processor(dfa: DFA) -> None:
    print("Word processing started. Please enter a word to check if it is accepted by the DFA.")
    while True:
        word = input("Enter a word: ")
        if word == "exit":
            print("Exiting word processor.")
            break
        if dfa.accepts(word):
            print(f"The word {word} is accepted by the DFA.")
        else:
            print(f"The word {word} is not accepted by the DFA.")
    return
    
def main():
    # states = {'q1', 'q2', 'q3', 'q4', 'q5'}
    # alphabet = {0, 1}
    # transitions = {
    #     'q1' : {0: 'q2', 1:'q4'},
    #     'q2' : {0: 'q3'},
    #     'q3' : {0: 'q2', 1: 'q2'},
    #     'q4' : {0: 'q5', 1: 'q5'},
    #     'q5' : {0: 'q4', 1:'q4'}
    # }
    # initial_state = 'q1'
    # final_states = {'q2', 'q5'}
    # dfa = DFA(states, alphabet, transitions, initial_state, final_states)
    # print(dfa.accepts('01'))
    path = "/home/robertvoaides/Academic/s2/LFA/lab/lfa_teme/hw1/1.txt"
    dfa = read_cfg(path)
    if dfa is not None:
        word_processor(dfa)
if __name__ == "__main__":
    main()