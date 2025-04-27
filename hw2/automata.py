from collections import deque

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

class NFA:
    def __init__(self, states: set, alphabet: set, transitions: dict, initial_state: str, final_states: set):
        self.states = states
        self.alphabet = alphabet
        self.transition = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def has_accepting_path(self) -> bool: # BFS
        visited_states = set()

        queue = deque([self.initial_state])

        while queue:
            current_state = queue.popleft()
            if current_state in self.final_states:
                return True
            if current_state in visited_states:
                continue
            visited_states.add(current_state)

            for letter in self.alphabet:
                if current_state not in self.transition:
                    continue
                if letter not in self.transition[current_state]:
                    continue
                following_states = self.transition[current_state][letter]
                for state in following_states:
                    if state not in visited_states:
                        queue.append(state)
        return False

    def accepts(self, string: str) -> bool:
        current_states = {self.initial_state} # using set of states instead of a single state
        for char in string:
            if char not in self.alphabet:
                raise ValueError(f"The symbol {char} is not in the alphabet.")
            next_states = set()
            for state in current_states:
                # no transition for current state, avoid errror when calling the dictionary
                if state not in self.transition:
                    continue
                if char in self.transition[state]:
                    next_states.update(self.transition[state][char])
            current_states = next_states
        for state in current_states:
            if state in self.final_states:
                return True
        return False
