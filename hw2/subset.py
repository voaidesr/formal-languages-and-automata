from itertools import count
from collections import deque
from automata import NFA, DFA, LAMBDA

__all__ = ["nfa_to_dfa"]

def _lambda_closure(nfa: NFA, states: set[str]) -> set[str]:
    closure = set(states)
    stack = list(states)
    while stack:
        st = stack.pop()
        if st in nfa.transition and LAMBDA in nfa.transition[st]:
            for nxt in nfa.transition[st][LAMBDA]:
                if nxt not in closure:
                    closure.add(nxt)
                    stack.append(nxt)
    return closure


def _move(nfa: NFA, state_set: set[str], symbol: str) -> set[str]:
    out: set[str] = set()
    for st in state_set:
        if st in nfa.transition and symbol in nfa.transition[st]:
            out.update(nfa.transition[st][symbol])
    return out

def nfa_to_dfa(nfa: NFA) -> DFA:
    """
    Convert λ-NFA to DFA with subset construction.
    """

    dfa_alphabet = set(a for a in nfa.alphabet if a != LAMBDA)

    name_of: dict[frozenset[str], str] = {}
    counter = count()
    def _name(S: frozenset[str]) -> str:
        if S not in name_of:
            name_of[S] = f"q{next(counter)}"
        return name_of[S]

    start_set = frozenset(_lambda_closure(nfa, {nfa.initial_state}))
    worklist = deque([start_set])

    dfa_trans: dict[str, dict[str, str]] = {}
    dfa_states: set[str] = set()
    dfa_finals: set[str] = set()

    while worklist:
        T = worklist.popleft()
        T_name = _name(T)
        dfa_states.add(T_name)
        if T & nfa.final_states:
            dfa_finals.add(T_name)

        for sym in dfa_alphabet:
            U = frozenset(_lambda_closure(nfa, _move(nfa, T, sym)))
            if not U:
                continue
            U_name = _name(U)
            dfa_trans.setdefault(T_name, {})[sym] = U_name
            if U_name not in dfa_states:
                worklist.append(U)

    return DFA(dfa_states, dfa_alphabet, dfa_trans, _name(start_set), dfa_finals)
