import pytest
from src.nfa import NFA, validate_nfa, read_cfg
import os

from src.nfa import NFA, validate_nfa
from collections import defaultdict

states = {'q0', 'q1', 'q2'}
alphabet = {'a', 'b'}
transitions = {
    'q0': {'a': {'q0', 'q1'}},
    'q1': {'b': {'q2'}},
    'q2': {}
}
initial_state = 'q0'
final_states = {'q2'}

nfa = NFA(states, alphabet, transitions, initial_state, final_states)

def test_accepts_valid_word():
    assert nfa.accepts("ab") is True
    assert nfa.accepts("aaab") is True
    assert nfa.accepts("aab") is True

def test_rejects_invalid_word():
    assert nfa.accepts("bb") is False
    assert nfa.accepts("ba") is False
    assert nfa.accepts("aaba") is False

def test_invalid_symbols():
    try:
        nfa.accepts("abc")
    except ValueError as e:
        assert "not in the alphabet" in str(e)

def test_lambda_word():
    assert nfa.accepts("") is False

def test_accepts_lambda_if_start_is_final():
    states = {'q0'}
    alphabet = {'a'}
    transitions = {}
    initial_state = 'q0'
    final_states = {'q0'}
    nfa = NFA(states, alphabet, transitions, initial_state, final_states)
    assert nfa.accepts("") is True

def test_has_accepting_path_true():
    assert nfa.has_accepting_path() is True

def test_has_accepting_path_false():
    states = {'q0', 'q1'}
    alphabet = {'a'}
    transitions = {
        'q0': {'a': {'q0'}}
    }
    initial_state = 'q0'
    final_states = {'q1'}
    nfa = NFA(states, alphabet, transitions, initial_state, final_states)
    assert nfa.has_accepting_path() is False

def test_validate_nfa_valid():
    states = {'q0', 'q1'}
    alphabet = {'a'}
    transitions = {
        'q0': {'a': {'q1'}}
    }
    initial_state = {'q0'}
    final_states = {'q1'}
    assert validate_nfa(states, alphabet, transitions, initial_state, final_states) is True

def test_validate_nfa_invalid_start_state():
    states = {'q0'}
    alphabet = {'a'}
    transitions = {}
    initial_state = {'qX'}
    final_states = {'q0'}
    assert validate_nfa(states, alphabet, transitions, initial_state, final_states) is False

def test_validate_nfa_multiple_start_states():
    states = {'q0', 'q1'}
    alphabet = {'a'}
    transitions = {}
    initial_state = {'q0', 'q1'}
    final_states = {'q1'}
    assert validate_nfa(states, alphabet, transitions, initial_state, final_states) is False

def test_nfa2():
    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    transitions = {
        'q0': {
            'a': {'q0'},
            'b': {'q1', 'q2'}
        },
        'q1': {},
        'q2': {}
    }
    initial_state = 'q0'
    final_states = {'q1', 'q2'}

    nfa = NFA(states, alphabet, transitions, initial_state, final_states)

    assert nfa.accepts("b") is True
    assert nfa.accepts("ab") is True
    assert nfa.accepts("aaaab") is True
    assert nfa.accepts("a") is False
    assert nfa.has_accepting_path() is True
    assert validate_nfa(states, alphabet, transitions, {initial_state}, final_states)

def test_nfa3():
    states = {'q0', 'q1', 'q2', 'q3', 'qx'}
    alphabet = {'a', 'b', 'c'}
    transitions = {
        'q0': {'a': {'q1'}},
        'q1': {'b': {'q2'}},
        'q2': {'c': {'q3'}},
        'qx': {'a': {'qx'}, 'b': {'qx'}, 'c': {'qx'}}
    }
    initial_state = 'q0'
    final_states = {'q3'}

    nfa = NFA(states, alphabet, transitions, initial_state, final_states)

    assert nfa.accepts("abc") is True
    assert nfa.accepts("a") is False
    assert nfa.accepts("ab") is False
    assert nfa.has_accepting_path() is True
    assert validate_nfa(states, alphabet, transitions, {initial_state}, final_states)
