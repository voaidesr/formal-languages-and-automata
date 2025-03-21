from src.dfa import DFA, validate_dfa, read_cfg

def test_validity():
    assert validate_dfa(set(), set(), {}, set(), set()) == False
    assert validate_dfa({"q0"}, {"a"}, {"q0": {"a": "q0"}}, {"q0"}, {"q0"}) == True
    assert validate_dfa({"q0"}, {"a"}, {"q0": {"b": "q0"}}, {"q0"}, {"q0"}) == False
    assert validate_dfa({"q0"}, {"a"}, {"q0": {"a": "q0"}}, {"q0"}, {"q1"}) == False
    assert validate_dfa({"q0"}, {"a"}, {"q0": {"a": "q0"}}, {"q0", "q1"}, {"q0"}) == False

def test_has_accepting_path():
    dfa1 = DFA(
        states={'q0'},
        alphabet={'a', 'b'},
        transitions={'q0': {'a': 'q0', 'b': 'q0'}},
        initial_state='q0',
        final_states=set()
    )
    assert not dfa1.has_accepting_path()

    dfa2 = DFA(
        states={'q0', 'q1'},
        alphabet={'a'}, 
        transitions={
            'q0': {'a': 'q1'},
            'q1': {'a': 'q1'}
        },
        initial_state='q0',
        final_states={'q0'}
    )
    assert dfa2.has_accepting_path()    

def test_accepts():
    dfa1 = DFA(
        states={'q0'},
        alphabet={'a', 'b'},
        transitions={'q0': {'a': 'q0', 'b': 'q0'}},
        initial_state='q0',
        final_states=set()
    )
    assert not dfa1.accepts("")
    assert not dfa1.accepts("a")
    assert not dfa1.accepts("abababab")

    dfa2 = DFA(
        states={'q0', 'q1'},
        alphabet={'a'},
        transitions={
            'q0': {'a': 'q1'},
            'q1': {'a': 'q1'}
        },
        initial_state='q0',
        final_states={'q0'}
    )
    assert dfa2.accepts("")
    assert not dfa2.accepts("a")
    assert not dfa2.accepts("aa")

    dfa3 = DFA(
        states={'q0'},
        alphabet={'a', 'b'},
        transitions={
            'q0': {'a': 'q0', 'b': 'q0'}
        },
        initial_state='q0',
        final_states={'q0'}
    )
    assert dfa3.accepts("")
    assert dfa3.accepts("a")
    assert dfa3.accepts("ababab")

    dfa4 = DFA(
        states={'q0', 'q1'},
        alphabet={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q1', 'b': 'q0'}
        },
        initial_state='q0',
        final_states={'q1'}
    )
    assert not dfa4.accepts("")
    assert dfa4.accepts("a")
    assert dfa4.accepts("bba")
    assert not dfa4.accepts("babb")

    dfa5 = DFA(
        states={'q0', 'q1'},
        alphabet={'a'},
        transitions={
            'q0': {'a': 'q1'},
            'q1': {'a': 'q0'}
        },
        initial_state='q0',
        final_states={'q0'}
    )
    assert dfa5.accepts("")
    assert not dfa5.accepts("a")
    assert dfa5.accepts("aa")
    assert not dfa5.accepts("aaa")

    dfa6 = DFA(
        states={'q0', 'q1', 'q2'},
        alphabet={'a', 'b'},
        transitions={
            'q0': {'a': 'q1', 'b': 'q0'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a': 'q2', 'b': 'q2'}
        },
        initial_state='q0',
        final_states={'q2'}
    )
    assert not dfa6.accepts("")
    assert not dfa6.accepts("a")
    assert not dfa6.accepts("b")
    assert dfa6.accepts("ab")
    assert dfa6.accepts("aab")
    assert dfa6.accepts("baabbb")

    dfa7 = DFA(
        states={'q0', 'q1'},
        alphabet={'a', 'b', 'c'},
        transitions={
            'q0': {'a': 'q0', 'b': 'q0', 'c': 'q1'},
            'q1': {'a': 'q1', 'b': 'q1', 'c': 'q1'}
        },
        initial_state='q0',
        final_states={'q0'}
    )
    assert dfa7.accepts("")
    assert dfa7.accepts("ababab")
    assert not dfa7.accepts("ac")
    assert not dfa7.accepts("cc")

def test_read_cfg():
    assert read_cfg("./dfa_cfg_files/1.txt") is None

    assert read_cfg("./dfa_cfg_files/2.txt").has_accepting_path() == True
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("a") == False
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("b") == False
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("c") == False
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("ac") == True
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("abb") == True
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("acaaaaaaaa") == True
    assert read_cfg("./dfa_cfg_files/2.txt").accepts("acaaaaaaaaa") == False

    assert read_cfg("./dfa_cfg_files/3.txt") is None
    assert read_cfg("./dfa_cfg_files/4.txt").has_accepting_path() == False
