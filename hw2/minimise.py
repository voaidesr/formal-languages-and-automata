from collections import defaultdict, deque
from itertools import count
from typing import Set, Dict
from automata import DFA

__all__ = ["minimise_dfa"]

def minimise_dfa(dfa: DFA) -> DFA:
    finals = set(dfa.final_states)
    non_finals = set(dfa.states) - finals
    P = [block for block in (finals, non_finals) if block]
    W = deque(P.copy())

    alphabet = set(dfa.alphabet)
    inv: Dict[str, Dict[str, Set[str]]] = {c: defaultdict(set) for c in alphabet}
    for p in dfa.states:
        for c in alphabet:
            q = dfa.transition.get(p, {}).get(c)
            if q is not None:
                inv[c][q].add(p)

    while W:
        A = W.popleft()
        for c in alphabet:
            X = set()
            for q in A:
                X |= inv[c].get(q, set())
            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    new_P.extend([inter, diff])
                    if Y in W:
                        W.remove(Y)
                        W.extend([inter, diff])
                    else:
                        W.append(inter if len(inter) <= len(diff) else diff)
                else:
                    new_P.append(Y)
            P = new_P

    rep_map: Dict[str, str] = {}
    state_counter = count(1)
    initial_state_name = "q0"
    for block in P:
        if dfa.initial_state in block:
            name = initial_state_name
        else:
            name = f"q{next(state_counter)}"
        for state in block:
            rep_map[state] = name

    new_states = set(rep_map.values())
    new_initial = rep_map[dfa.initial_state]
    new_finals = {rep_map[s] for s in dfa.final_states}
    new_transitions: Dict[str, Dict[str, str]] = {}
    for p in dfa.states:
        for c in alphabet:
            q = dfa.transition.get(p, {}).get(c)
            if q is not None:
                p_new = rep_map[p]
                q_new = rep_map[q]
                new_transitions.setdefault(p_new, {})[c] = q_new

    return DFA(new_states, alphabet, new_transitions, new_initial, new_finals)
