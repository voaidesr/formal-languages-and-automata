import random
from typing import List, Dict, Set

class Grammar:
    def __init__(self) -> None:
        self.start_symbol: str | None = None
        self.nonterminals: Set[str] = set()
        self.terminals: Set[str] = set()
        self.productions: Dict[str, List[str]] = {}

    @classmethod
    def from_keyboard(cls) -> "Grammar":
        g = cls() # call constructor
        print("Enter grammar productions. Use # as lambda. Empty line to finish\n")
        while True:
            line = input().rstrip("\n")

            if line.strip() == "":
                break  # double enter ends input

            if "->" not in line:
                print("\033[91mInvalid, no ->. Please write another production.\033[0m")
                continue

            lhs, rhs_part = line.split("->")
            lhs = lhs.strip()
            # remove spaces
            rhs_alts = [alt.strip().replace(" ", "") for alt in rhs_part.split("|")]

            # start symbol
            if g.start_symbol is None:
                g.start_symbol = lhs

            if lhs not in g.productions:
                g.productions[lhs] = []


            for alt in rhs_alts:
                alt = "" if alt == "#" else alt
                g.productions[lhs].append(alt)

                for ch in alt:
                    if "A" <= ch <= "Z":
                        g.nonterminals.add(ch)
                    else:
                        g.terminals.add(ch)
            g.nonterminals.add(lhs)
        return g

    # this takes sentential form and expands it randomly through one nonterminal
    def _expand_once(self, sent: List[str]) -> List[str]:
        nt_positions = [i for i, s in enumerate(sent) if "A" <= s <= "Z"]
        idx = random.choice(nt_positions)
        nt = sent[idx]
        rhs = random.choice(self.productions[nt])
        replacement = list(rhs) if rhs else []
        return sent[:idx] + replacement + sent[idx + 1 :]

    def generate_word(self, max_steps: int = 25) -> str:
        if self.start_symbol is None:
            raise ValueError("Grammar has no start symbol.")

        sentential = [self.start_symbol]
        steps = 0
        while any("A" <= s <= "Z" for s in sentential) and steps < max_steps:
            sentential = self._expand_once(sentential)
            steps += 1
        return "".join(ch for ch in sentential)

    def generate_words(self, n: int = 10) -> List[str]:
        words: Set[str] = set()
        max_attempts = 1000
        attempts = 0
        while len(words) < n and attempts < max_attempts:
            word = self.generate_word()
            if len(word) <= 10:
                words.add(word)
            attempts += 1
        return list(words)

    def accepts(self, word: str) -> bool:
        if self.start_symbol is None:
            raise ValueError("Grammar has no start symbol.")
        if word == "#":
            word = ""
        n = len(word)
        chart: List[List[tuple]] = [[] for _ in range(n + 1)]

        def add(state: tuple, index: int) -> None:
            if state not in chart[index]:
                chart[index].append(state)

        for alt in self.productions[self.start_symbol]:
            add((self.start_symbol, alt, 0, 0), 0)

        for i in range(n + 1):
            changed = True
            while changed:
                changed = False
                for lhs, rhs, dot, origin in list(chart[i]):
                    if dot < len(rhs):
                        symbol = rhs[dot]
                        if "A" <= symbol <= "Z":
                            for alt in self.productions.get(symbol, []):
                                st = (symbol, alt, 0, i)
                                if st not in chart[i]:
                                    chart[i].append(st)
                                    changed = True
                    else:
                        for st_lhs, st_rhs, st_dot, st_origin in list(chart[origin]):
                            if st_dot < len(st_rhs) and st_rhs[st_dot] == lhs:
                                st2 = (st_lhs, st_rhs, st_dot + 1, st_origin)
                                if st2 not in chart[i]:
                                    chart[i].append(st2)
                                    changed = True
                if i < n:
                    for lhs, rhs, dot, origin in list(chart[i]):
                        if dot < len(rhs):
                            symbol = rhs[dot]
                            if not ("A" <= symbol <= "Z") and symbol != "":
                                if word[i] == symbol:
                                    add((lhs, rhs, dot + 1, origin), i + 1)

        for lhs, rhs, dot, origin in chart[n]:
            if (
                lhs == self.start_symbol
                and dot == len(rhs)
                and origin == 0
            ):
                # display derivation, if accepted
                self.display_derivation(word)
                return True
        return False

    def find_derivation(self, current: List[str], target: str, derivation: List[List[str]], max_depth: int = 20) -> List[List[str]] | None:
        if "".join(current) == target:
            return derivation + [current]
        # limit recursion
        if len(derivation) >= max_depth:
            return None
        # expand first nonterminal, expand all productions
        for i, symbol in enumerate(current):
            if "A" <= symbol <= "Z":
                for prod in self.productions.get(symbol, []):
                    new_sentential = current[:i] + list(prod) + current[i+1:]
                    result = self.find_derivation(new_sentential, target, derivation + [current], max_depth)
                    if result is not None:
                        return result
        return None

    def display_derivation(self, target: str) -> None:
        if self.start_symbol is None:
            print("No start symbol defined.")
            return
        deriv = self.find_derivation([self.start_symbol], target, [], max_depth=20)
        if deriv is None:
            print(f"No derivation found for '{target}'")
        else:
            print(f"Derivation for '{target}':")
            for i in range(len(deriv) - 1):
                prev = deriv[i]
                next_step = deriv[i + 1]
                prefix = 0
                while prefix < len(prev) and prefix < len(next_step) and prev[prefix] == next_step[prefix]:
                    prefix += 1
                suffix = 0
                while (
                    suffix < (len(prev) - prefix)
                    and suffix < (len(next_step) - prefix)
                    and prev[len(prev) - 1 - suffix] == next_step[len(next_step) - 1 - suffix]
                ):
                    suffix += 1
                nonterminal = prev[prefix] if prefix < len(prev) else ""
                production = (
                    "".join(next_step[prefix: len(next_step) - suffix])
                    if (len(next_step) - suffix) > prefix
                    else ""
                )
                if production == "":
                    production = "#"
                current_word = "".join(prev) or "#"
                print(
                    f"Current word: \033[94m{current_word}\033[0m : {nonterminal} -> {production}"
                )

def main() -> None:
    grammar = Grammar.from_keyboard()

    print("\nGenerated words:\n")
    for w in grammar.generate_words(10):
        print("  " + (w or "#"))

    print("\nType words to test (blank line to quit):\n")
    while True:
        w = input().rstrip("\n")
        if w.strip() == "":
            break
        verdict = "\033[92maccepted\033[0m" if grammar.accepts(w) else "\033[91mrejected\033[0m"
        print(f" -> {verdict}\n")


if __name__ == "__main__":
    main()
