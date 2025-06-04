# Homework 3 - CFGs

Engine to define context-free grammars, generate random words, and test word acceptance with derivations.


## Features

- Input grammar productions from keyboard (`Nonterminal -> productions`, `#` for empty string)
- Automatically detects start symbol, terminals, and nonterminals
- Generate random words from the grammar
- Test if a word is accepted by the grammar using an Earley-style parser
- Display derivation steps for accepted words


## Usage

1. Run the script
2. Enter productions line by line, empty line to finish
3. View generated words
4. Input words to test acceptance, empty line to quit

## Input Example

```
S -> aSb | #
A -> aA | a
```

Generated words:

```
  #
  aaaaabbbbb
  aabb
  aaabbb
  ab
  aaaabbbb
```
Word acceptance:

```
Type words to test (blank line to quit):

aabb
Derivation for 'aabb':
Current word: S : S -> aSb
Current word: aSb : S -> aSb
Current word: aaSbb : S -> #
 -> accepted
```

