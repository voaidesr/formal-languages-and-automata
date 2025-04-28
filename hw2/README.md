# Second Homework — Formal Languages and Automata

Building a DFA from a regular expression.

## How to Run

First, clone the repository and navigate to the `hw2` directory.

Ensure `graphviz` is installed if it is not already:

```bash
pip install graphviz
```

To check that the algorithms are functioning correctly:

```bash
python run_test.py ./tests/test.json
```

To create diagrams with the NFA, DFA and minimal DFA constructed from a regex, replace in `main.py` the desired expression and run:
```bash
python main.py
```

## Project Structure

This project is designed to be modular and organized into clear components:

- `automata.py` — Defines classes for DFA and NFA.
  Includes support for λ-NFA and Graphviz visualization.

- `parser.py` — Provides utilities for parsing regular expressions and converting them into postfix notation using the Shunting Yard algorithm.

- `thompson.py` — Implements Thompson's construction algorithm to build an λ-NFA from a postfix regular expression.

- `subset.py` — Contains the subset construction algorithm to transform an λ-NFA into an equivalent DFA.

- `minimise.py` — Applies Hopcroft's algorithm to minimize a DFA and obtain an equivalent minimal DFA.

- `main.py` — Example script that:
  - Reads a regular expression,
  - Builds the corresponding NFA, DFA, and minimized DFA,
  - Outputs the diagrams for each into the `./diagrams/` directory.


