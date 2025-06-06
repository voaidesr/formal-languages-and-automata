from collections import deque
from graphviz import Source, Digraph

def _dot_base(name: str = "automaton") -> "Digraph":
    g = Digraph(name=name, format="png")
    g.attr(rankdir="LR", fontsize="12", labelloc="t", fontname="Helvetica")
    g.attr("node", fontname="Helvetica")
    return g

LAMBDA = "λ"
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
                return False
            # no transition available for the current state
            if current_state not in self.transition:
                return False
            if char not in self.transition[current_state]:
                return False
            current_state = self.transition[current_state][char]
        # verifies if the dfa has reached a final state
        return current_state in self.final_states

    def to_dot(self) -> str:
        if Digraph is None:
            raise RuntimeError("python-graphviz not installed.")
        g = _dot_base("DFA")
        g.node("start", shape="point")
        g.edge("start", self.initial_state, label="")
        for state in self.states:
            shape = "doublecircle" if state in self.final_states else "circle"
            g.node(state, shape=shape)
        for src, adict in self.transition.items():
            grouped: dict[str, list[str]] = {}
            for sym, dst in adict.items():
                grouped.setdefault(dst, []).append(sym)
            for dst, syms in grouped.items():
                g.edge(src, dst, label=",".join(sorted(syms)))
        return g.source

    def render(self, path: str, format: str = "png") -> None:
        if Digraph is None:
            raise RuntimeError("python-graphviz not installed.")
        Source(self.to_dot(), filename=path, format=format).render(cleanup=True)

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
        def lambda_closure(states: set) -> set:
            closure = set(states)
            stack = list(states)
            while stack:
                state = stack.pop()
                if state in self.transition:
                    if LAMBDA in self.transition[state]:
                        for next_state in self.transition[state][LAMBDA]:
                            if next_state not in closure:
                                closure.add(next_state)
                                stack.append(next_state)
            return closure

        current_states = lambda_closure({self.initial_state})

        for char in string:
            next_states = set()
            for state in current_states:
                if state in self.transition and char in self.transition[state]:
                    next_states.update(self.transition[state][char])
            current_states = lambda_closure(next_states)

        for state in current_states:
            if state in self.final_states:
                return True
        return False

    def to_dot(self) -> str:
        if Digraph is None:
            raise RuntimeError("python-graphviz not installed.")
        g = _dot_base("NFA")
        g.node("start", shape="point")
        g.edge("start", self.initial_state, label="")
        for state in self.states:
            shape = "doublecircle" if state in self.final_states else "circle"
            g.node(state, shape=shape)
        for src, adict in self.transition.items():
            grouped: dict[frozenset[str], list[str]] = {}
            for sym, dst_set in adict.items():
                for dst in dst_set:
                    grouped.setdefault((dst,), []).append(sym)
            for (dst,), syms in grouped.items():
                g.edge(src, dst, label=",".join(sorted(syms)))
        return g.source

    def render(self, path: str, format: str = "png") -> None:
        if Digraph is None:
            raise RuntimeError("python-graphviz not installed.")
        Source(self.to_dot(), filename=path, format=format).render(cleanup=True)