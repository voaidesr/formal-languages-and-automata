import json
import sys
from parser import to_postfix
from thompson import postfix_to_nfa
from subset import nfa_to_dfa
from minimise import minimise_dfa

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BLUE = "\033[94m"

def test_all(json_path: str) -> None:
    with open(json_path, 'r') as f:
        cases = json.load(f)

    all_passed = True
    for case in cases:
        name = case['name']
        regex = case['regex']
        postfix = to_postfix(regex)
        nfa = postfix_to_nfa(postfix)
        dfa = nfa_to_dfa(nfa)
        min_dfa = minimise_dfa(dfa)

        print(f"=== {name}: {BLUE}{regex}{RESET} ===")
        for tst in case['test_strings']:
            inp = tst['input']
            exp = tst['expected']

            res_full = dfa.accepts(inp)
            res_min  = min_dfa.accepts(inp)

            status_full = f"{GREEN}OK{RESET}" if res_full == exp else f"{RED}FAIL{RESET}"
            status_min  = f"{GREEN}OK{RESET}" if res_min  == exp else f"{RED}FAIL{RESET}"

            print(f"  input={inp!r:8} expected={exp!s:5} "
                  f"dfa={res_full!s:5}[{status_full}] "
                  f"min={res_min!s:5}[{status_min}]")
            if res_full != exp or res_min != exp:
                all_passed = False

    if all_passed:
        print(f"\n{GREEN}All tests passed.{RESET}")
        sys.exit(0)
    else:
        print(f"\n{RED}Some tests failed.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_tests.py path/to/cases.json")
        sys.exit(2)
    test_all(sys.argv[1])
