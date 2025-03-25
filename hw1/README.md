# First homework
Implementing a [DFA](#the-determinist-finite-automaton-dfa) and [NFA](#the-nedeterminist-finite-automaton-nfa) from a configuration file.

## The Determinist Finite Automaton (DFA)

A DFA is a mathematical model of computation defined as a 5-tuple:

$$
M = (Q, \Sigma, \delta, q_0, F)
$$

Where:

- $Q$ is a **finite set** of states.
- $\Sigma$ is a **finite input alphabet**.
- $\delta: Q \times \Sigma \to Q$ is the **transition function**.
- $q_0 \in Q$ is the **start state**.
- $F \subseteq Q$ is the set of **accepting (final) states**.

## Implementation Overview

I have implemented the Deterministic Finite Automaton (DFA) as a Python class, providing methods for core operations such as simulating the automaton on input strings and checking whether the language it accepts is empty.

### The `DFA` Class

The `DFA` class encapsulates the definition and behavior of a deterministic finite automaton. It is initialized with:

- `states`: a set of all state names
- `alphabet`: a set of input symbols
- `transitions`: a nested dictionary representing the transition function $\delta$
- `initial_state`: the unique start state, as a string
- `final_states`: a set of accepting (final) states

#### `accepts(self, string: str) -> bool`

This method simulates the DFA on a given input string. It begins at the initial state and consumes the string symbol by symbol, following the corresponding transitions. If the string is fully consumed and the DFA ends in a final state, the method returns `True`; otherwise, it returns `False`. The method raises an error if the input contains symbols not in the alphabet.

#### `has_accepting_path(self) -> bool`

This method checks whether the DFA accepts any string at all (i.e., whether its language is non-empty). It uses breadth-first search (BFS) starting from the initial state to explore all reachable states. If any accepting state is reached during traversal, the method returns `True`. Otherwise, it returns `False`, indicating the DFA accepts no string.

### Configuration File Parsing

The function `read_cfg(path: str) -> DFA` parses a configuration file that describes a DFA. The file format includes labeled sections: `Sigma`, `States`, and `Transitions`, each ending with an `End` line. Comments beginning with `#` are ignored.

- The `Sigma` section defines the input alphabet.
- The `States` section defines all states, with optional tags:
  - `S` marks the start state.
  - `F` marks a final state.
- The `Transitions` section defines the transition function. Each line specifies a transition in the form:
  `source_state, input_symbol, destination_state`

The parser builds the corresponding internal data structures and calls `validate_dfa(...)` to verify that:

- All states used in transitions are defined.
- All input symbols used in transitions belong to the alphabet.
- Exactly one start state is defined.
- All final states are part of the set of states.

If the validation passes, the function returns a `DFA` object. Otherwise, it returns `None` and prints the validation errors.

### Word Processor Interface

The function `word_processor(dfa: DFA) -> None` provides a simple interactive loop that allows users to test whether input strings are accepted by the DFA. The loop continues until the user types `"exit"`.

### Entry Point

The `main()` function requests the path to a DFA configuration file, attempts to parse it, and then determines whether the DFA's language is empty using `has_accepting_path()`. If the language is not empty, it enters the word processing loop to allow the user to interact with the DFA.

## The Nedeterminist Finite Automaton (NFA)

An NFA (Nondeterministic Finite Automaton) is a generalization of a DFA in which, for a given state and input symbol, the automaton may transition to any number of next states (including none). It is defined as a 5-tuple:

$$
M = (Q, \Sigma, \delta, q_0, F)
$$

Where:

- $Q$ is a **finite set** of states.
- $\Sigma$ is a **finite input alphabet**.
- $\delta: Q \times \Sigma \to \mathcal{P}(Q)$ is the **transition function**, mapping to a set of states.
- $q_0 \in Q$ is the **start state**.
- $F \subseteq Q$ is the set of **accepting (final) states**.

## Implementation Overview

The workflow is almost identical to the implementation of the DFA.




