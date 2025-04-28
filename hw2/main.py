from parser import to_postfix
from thompson import postfix_to_nfa
from subset import nfa_to_dfa
from minimise import minimise_dfa

def main():
    regex = "(a|b)*a(a|b)"
    postfix = to_postfix(regex)
    nfa = postfix_to_nfa(postfix)
    dfa = nfa_to_dfa(nfa)
    minimal_dfa = minimise_dfa(dfa)

    nfa.render("./diagrams/nfa_diagram")
    dfa.render("./diagrams/dfa_diagram")
    minimal_dfa.render("./diagrams/minimal_dfa_diagram")
    print("Diagrams written to ./diagrams/")

if __name__ == "__main__":
    main()
