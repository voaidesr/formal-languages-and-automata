import itertools
import copy
from automata import NFA, LAMBDA

__all__ = ["postfix_to_nfa"]

# adds new states keeping count of how many states there are already
def _new_state(counter: itertools.count) -> str:
    return f"q{next(counter)}"

def _merge_trans(dst: dict, src: dict) -> dict:
    """
    This combines two transition functions: it adds the transitions from src to dst by creating a new state key,
    if it doesn't exist or, if it exists, by appending the transitions associated to it from src
    """
    out = copy.deepcopy(dst)
    for state, trans in src.items():
        st_dict = out.setdefault(state, {}) # if state doesn't already exist in the dst transition, create an empty set of transitions
        for sym, targets in trans.items():
            st_dict.setdefault(sym, set()).update(targets) # add the transitions from src
    return out

def postfix_to_nfa(tokens: list[str]) -> NFA:
    """
    This uses Thompson's algorithm to turn a regex in postfix notation to an
    """
    counter = itertools.count()
    stack: list[tuple[str, str, dict]] = [] # stack of tuples (start_state, accept_state, transitions)
    alphabet: set[str] = set()

    for token in tokens:
        if token not in {'.', '|', '*', '+', '?'}:
            s = _new_state(counter)
            f = _new_state(counter)
            transitions = {s: {token: {f}}}
            alphabet.add(token)
            stack.append((s, f, transitions))
            continue

        if token == '.':
            s2, f2, t2 = stack.pop()
            s1, f1, t1 = stack.pop()
            merged = _merge_trans(t1, t2)
            merged.setdefault(f1, {}).setdefault(LAMBDA, set()).add(s2)
            stack.append((s1, f2, merged))

        elif token == '|':
            s2, f2, t2 = stack.pop()
            s1, f1, t1 = stack.pop()
            s_new, f_new = _new_state(counter), _new_state(counter)
            trans = _merge_trans(t1, t2)
            trans.setdefault(s_new, {}).setdefault(LAMBDA, set()).update({s1, s2})
            trans.setdefault(f1, {}).setdefault(LAMBDA, set()).add(f_new)
            trans.setdefault(f2, {}).setdefault(LAMBDA, set()).add(f_new)
            stack.append((s_new, f_new, trans))

        elif token == '*':
            s_old, f_old, trans = stack.pop()
            s_new, f_new = _new_state(counter), _new_state(counter)
            trans.setdefault(s_new, {}).setdefault(LAMBDA, set()).update({s_old, f_new})
            trans.setdefault(f_old, {}).setdefault(LAMBDA, set()).update({s_old, f_new})
            stack.append((s_new, f_new, trans))

        elif token == '+':
            s_old, f_old, trans = stack.pop()
            s_new, f_new = _new_state(counter), _new_state(counter)
            trans.setdefault(s_new, {}).setdefault(LAMBDA, set()).add(s_old)
            trans.setdefault(f_old, {}).setdefault(LAMBDA, set()).update({s_old, f_new})
            stack.append((s_new, f_new, trans))

        elif token == '?':
            s_old, f_old, trans = stack.pop()
            s_new, f_new = _new_state(counter), _new_state(counter)
            trans.setdefault(s_new, {}).setdefault(LAMBDA, set()).update({s_old, f_new})
            trans.setdefault(f_old, {}).setdefault(LAMBDA, set()).add(f_new)
            stack.append((s_new, f_new, trans))

    start, accept, transitions = stack.pop()

    states: set[str] = set(transitions)
    for adict in transitions.values():
        for trg_set in adict.values():
            states.update(trg_set)

    return NFA(states, alphabet, transitions, start, {accept})
