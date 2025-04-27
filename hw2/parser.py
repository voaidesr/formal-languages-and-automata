def tokenize(regex:str) -> list[str]:
    """
    This breaks a regex into tokens (characters and the operators "|+*?()")
    Also, it inserts "."as the concatenation operarator where it is implicit.
    """
    tokens, L = [], len(regex)
    operators = set("|+*?()")

    # to verify that a token is not an operator
    def is_literal(token: str) -> bool:
        return token and (token not in operators) and (token != ".")

    for i in range(0, L):
        tokens.append(regex[i])

        if i < L - 1:
            current = regex[i]
            next = regex[i+1]
            if (is_literal(current) or current in ")*?") and (is_literal(next) or next == "("):
                tokens.append(".")

    return tokens


def to_postfix(regex: str) -> list[str]:
    """

    This converts regex into postfix using the Shunting-Yard algorithm.
    Many thanks https://blog.cernera.me/converting-regular-expressions-to-postfix-notation-with-the-shunting-yard-algorithm/
    """

    prec = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
    left_assoc = {"|", "."}

    output: list[str] = []
    op_stack: list[str] = []

    for token in tokenize(regex):
        if token in prec:
            while ((op_stack and op_stack[-1] != "(") and
                (prec[op_stack[-1]] > prec[token] or
                (prec[op_stack[-1]] == prec[token] and token in left_assoc))):
                output.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack[-1] != "(":
                output.append(op_stack.pop())
            op_stack.pop()
        else:
            output.append(token)

    while op_stack:
        output.append(op_stack.pop())
    return output