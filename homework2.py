# --------------------------------------------------
#
# HOMEWORK 2
#
# Due: Tue, Oct 8 2024 (23h59)
#
# Name: Daniel Liao
#
# Email: yliao1@babson.edu
#
# Remarks, if any:
#
#
#
# --------------------------------------------------
#
# Please fill in this file with your solutions and submit it
#
# The functions below are stubs that you should replace with your
# own implementation.
#
# PLEASE DO NOT CHANGE THE SIGNATURE IN THE STUBS BELOW.
# Doing so risks making it impossible for me to test your code.
#
# --------------------------------------------------
import typing

from homework1 import DFA

NFAState: typing.TypeAlias = int | frozenset[int]


class NFA(typing.TypedDict):
    states: "list[NFAState]"
    alphabet: "list[str]"
    delta: "list[tuple[NFAState, str, NFAState]]"
    start: "int"
    final: "list[NFAState]"


#
# Some sample DFAs.
#

DFA_MOD_3 = {
    "states": [1, 2, 3],
    "alphabet": ["a", "b", "c"],
    "delta": [
        (1, "a", 2),
        (2, "a", 3),
        (3, "a", 1),
        (1, "b", 1),
        (2, "b", 2),
        (3, "b", 3),
        (1, "c", 1),
        (2, "c", 2),
        (3, "c", 3),
    ],
    "start": 1,
    "final": [1],
}

DFA_START_END = {
    "states": [0, 1, 2, 99],
    "alphabet": ["a", "b", "c"],
    "delta": [
        (0, "a", 1),
        (0, "b", 99),
        (0, "c", 99),
        (1, "a", 1),
        (1, "b", 1),
        (1, "c", 2),
        (2, "a", 1),
        (2, "b", 1),
        (2, "c", 2),
        (99, "a", 99),
        (99, "b", 99),
        (99, "c", 99),
    ],
    "start": 0,
    "final": [2],
}

#
# Some sample NFAs.
#

NFA_LAST: NFA = {
    "states": [0, 1],
    "alphabet": ["a", "b", "c"],
    "delta": [(0, "a", 0), (0, "b", 0), (0, "c", 0), (0, "a", 1)],
    "start": 0,
    "final": [1],
}


def NFA_FIXED(n):
    if n > 0:
        return {
            "states": [-1] + list(range(n)),
            "alphabet": ["a", "b", "c"],
            "delta": [(-1, "a", -1), (-1, "b", -1), (-1, "c", -1), (-1, "a", 0)]
            + [(i - 1, "a", i) for i in range(1, n)]
            + [(i - 1, "b", i) for i in range(1, n)]
            + [(i - 1, "c", i) for i in range(1, n)],
            "start": -1,
            "final": [n - 1],
        }
    raise Exception(f"Number {n} not supported")


#
# Function to print the language of a finite automaton
# up to a certain string length.
#


def language(m, n, accept):

    def to_base_n_rev(num, n):
        result = []
        while num > 0:
            result.append(num % n)
            num = num // n
        return result

    def enum(size):
        result = []
        for num in range(len(alphabet) ** size):
            digits = to_base_n_rev(num, len(alphabet))
            digits.extend([0] * (size - len(digits)))
            result.append("".join(alphabet[digits[size - i - 1]] for i in range(size)))
        return result

    alphabet = m["alphabet"]
    for size in range(n + 1):
        for input in enum(size):
            if accept(m, input):
                print(input or "<empty string>")


#
# Question 1
#
def next_states(
    delta: "list[tuple[NFAState, str, NFAState]]",
    current: "NFAState",
    sym: str,
) -> "NFAState":
    result = set()

    if isinstance(current, int):
        current = frozenset({current})

    for state in current:
        for transition in delta:
            if transition[0] == state and transition[1] == sym:
                result.add(transition[2])

    if len(result) > 0:
        return frozenset(result)
    else:
        return result.pop()


def accept_nfa(m: NFA, input: str) -> bool:
    current_states: NFAState = m["start"]

    for letter in input:
        current_states = next_states(m["delta"], current_states, letter)

    if isinstance(current_states, int):
        current_states = frozenset({current_states})

    # if there is at least one state in current_states that is a final state
    return len(set(current_states).intersection(m["final"])) > 0


#
# Question 2
#


def to_dfa(m: NFA) -> DFA:
    new_delta = set()

    all_states = set[NFAState](m["states"])
    used_states = set()

    while used_states != all_states:
        states_to_add = set()

        for state in all_states:
            used_states.add(state)
            for letter in m["alphabet"]:
                at_least_one_transition = False

                for transition in m["delta"]:
                    start = transition[0]
                    sym = transition[1]
                    if state == start and sym == letter:
                        end = next_states(m["delta"], start, sym)

                        new_delta.add((hash(state), sym, hash(end)))
                        states_to_add.add(end)

                        at_least_one_transition = True

                if not at_least_one_transition:
                    new_delta.add((hash(state), letter, hash(state)))

        all_states = all_states.union(states_to_add)

    return {
        "states": [hash(x) for x in all_states],
        "alphabet": m["alphabet"],
        "delta": list(new_delta),
        "start": hash(m["start"]),
        "final": [hash(x) for x in all_states if x in m["final"]],
    }


#
# Question 3
#


# Helper functions for Question 3.


def re_sym(a):
    return ("symbol", a)


def re_seq(r1, r2):
    return ("sequence", r1, r2)


def re_plus(r1, r2):
    return ("plus", r1, r2)


def re_star(r):
    return ("star", r)


def parse(string):
    alpha = "abcdefghiklmnopqrstuvwxyz"

    def parse_sym(s, syms):
        if not s:
            return None
        if s[0] in syms:
            return (s[0], s[1:])
        return None

    # Grammar:
    #   E ::= T
    #         E + T
    #   T ::= F
    #         T F
    #   F ::= S
    #         F*
    #   S ::= sym
    #         (E)
    # + remove left recursion
    def parse_E(s):
        if parse_T(s):
            (t, rest) = parse_T(s)
            if parse_E1(rest):
                (f, rest) = parse_E1(rest)
                return (f(t), rest)
        return None

    def parse_E1(s):
        if parse_sym(s, "+"):
            (_, rest) = parse_sym(s, "+")
            if parse_T(rest):
                (t, rest) = parse_T(rest)
                if parse_E1(rest):
                    (f, rest) = parse_E1(rest)
                    return (lambda e: f(re_plus(e, t)), rest)
        return (lambda e: e, s)

    def parse_T(s):
        if parse_F(s):
            (t, rest) = parse_F(s)
            if parse_T1(rest):
                (f, rest) = parse_T1(rest)
                return (f(t), rest)
        return None

    def parse_T1(s):
        if parse_F(s):
            (t, rest) = parse_F(s)
            if parse_T1(rest):
                (f, rest) = parse_T1(rest)
                return (lambda e: f(re_seq(e, t)), rest)
        return (lambda e: e, s)

    def parse_F(s):
        if parse_S(s):
            (t, rest) = parse_S(s)
            if parse_F1(rest):
                (f, rest) = parse_F1(rest)
                return (f(t), rest)
        return None

    def parse_F1(s):
        if parse_sym(s, "*"):
            (_, rest) = parse_sym(s, "*")
            if parse_F1(rest):
                (f, rest) = parse_F1(rest)
                return (lambda e: f(re_star(e)), rest)
        return (lambda e: e, s)

    def parse_S(s):
        if parse_sym(s, alpha):
            (s, rest) = parse_sym(s, alpha)
            return (re_sym(s), rest)
        if parse_sym(s, "("):
            (_, rest) = parse_sym(s, "(")
            if parse_E(rest):
                (e, rest) = parse_E(rest)
                if parse_sym(rest, ")"):
                    (_, rest) = parse_sym(rest, ")")
                    return (e, rest)
        return None

    if parse_E(string):
        (exp, rest) = parse_E(string)
        if rest:
            raise Exception(f"""Cannot parse string""")
        return exp


def find_null_transition(delta):
    null_transitions = [(p, a, q) for (p, a, q) in delta if a is None]
    return null_transitions[0] if null_transitions else None


def remove_null(m):
    # Remove null transitions.
    states = m["states"]
    alphabet = m["alphabet"]
    delta = set(m["delta"])
    start = m["start"]
    final = set(m["final"])
    while True:
        null_transition = find_null_transition(delta)
        if not null_transition:
            # No more null transitions - we're done.
            break
        delta.remove(null_transition)
        (p0, _, q0) = null_transition
        delta.update([(p0, a, q) for (p, a, q) in delta if p == q0])
        if start == q0:
            start = p0
        if q0 in final:
            final.add(p0)
    return {
        "states": states,
        "alphabet": alphabet,
        "delta": list(delta),
        "start": start,
        "final": list(final),
    }


def to_nfa(r, alphabet):
    raise Exception("Not implemented")
