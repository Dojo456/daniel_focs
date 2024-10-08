# --------------------------------------------------
#
# HOMEWORK 1
#
# Due: Sun, Sep 29, 2023 (23h59)
#
# Name: Daniel Liao
#
# Email: lyazheng@olin.edu
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


#
# Some sample DFAs.
#

import typing
from collections import deque

StateLabel: typing.TypeAlias = int


class DFA(typing.TypedDict):
    states: "list[StateLabel]"
    alphabet: "list[str]"
    delta: "list[tuple[StateLabel, str, StateLabel]]"
    start: "int"
    final: "list[StateLabel]"


DFA_MOD_3: DFA = {
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

DFA_START_END: DFA = {
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
# Function to print the language of a DFA
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


def accept_dfa(m: DFA, input: str):
    class State(typing.TypedDict):
        num: StateLabel
        transitions: dict[str, StateLabel]
        """
        character transitions to num of new state
        for example:
            # for sample state 1
            state = State(
            num = 1,
            transitions = {
                "a": 2,
                "b": 3,
                "c": 4,
            })
        """

    states = {
        state: State(
            num=state,
            transitions={
                transition[1]: transition[2]
                for transition in m["delta"]
                if transition[0] == state
            },
        )
        for state in m["states"]
    }

    current_state: StateLabel = m["start"]

    for letter in input:
        state = states[current_state]
        current_state = state["transitions"][letter]

    return current_state in m["final"]


#
# Question 2
#

DFA_Q2A: DFA = DFA(
    states=[1, 2, 3],
    alphabet=["a", "b", "c"],
    delta=[
        (1, "a", 2),
        (1, "b", 2),
        (1, "c", 2),
        (2, "a", 3),
        (2, "b", 3),
        (2, "c", 3),
        (3, "a", 1),
        (3, "b", 1),
        (3, "c", 1),
    ],
    start=1,
    final=[2, 3],
)


DFA_Q2B = DFA(
    states=[1, 2, 3, 99],
    alphabet=["a", "b", "c"],
    delta=[
        (1, "b", 99),
        (2, "b", 99),
        (3, "b", 99),
        (1, "a", 2),
        (2, "a", 3),
        (1, "c", 1),
        (2, "c", 2),
        (3, "c", 3),
        (3, "b", 99),
        (99, "a", 99),
        (99, "b", 99),
        (99, "c", 99),
    ],
    start=1,
    final=[3],
)


DFA_Q2C = DFA(
    states=[1, 2, 3],
    alphabet=["a", "b", "c"],
    delta=[
        (1, "b", 5),
        (1, "a", 2),
        (2, "a", 3),
        (2, "b", 4),
        (1, "c", 1),
        (3, "b", 5),
        (2, "c", 2),
        (3, "a", 3),
        (3, "c", 3),
        (4, "b", 4),
        (4, "c", 4),
        (4, "a", 6),
        (6, "a", 7),
        (5, "b", 99),
        (5, "a", 6),
        (5, "c", 5),
        (6, "b", 99),
        (6, "c", 6),
        (7, "b", 99),
        (7, "a", 99),
        (7, "c", 7),
        (99, "b", 99),
        (99, "c", 99),
        (99, "a", 99),
    ],
    start=1,
    final=[5, 6, 7],
)


DFA_Q2D = DFA(
    states=[1, 2, 3, 4],
    alphabet=["a", "b", "c"],
    delta=[
        (1, "a", 2),
        (2, "a", 1),
        (1, "b", 3),
        (3, "b", 1),
        (1, "c", 1),
        (2, "b", 4),
        (2, "c", 2),
        (3, "c", 3),
        (4, "a", 3),
        (3, "a", 4),
        (4, "c", 4),
        (4, "b", 2),
    ],
    start=1,
    final=[2],
)


DFA_Q2E = DFA(
    states=[1, 2, 3, 4, 5, 6, 7, 8, 99],
    alphabet=["a", "b", "c"],
    delta=[
        # a loop from 1 to 2
        (1, "a", 2),
        (2, "a", 1),
        # b loop from 1 to 3
        (1, "b", 3),
        (3, "b", 1),
        # b loop from 2 to 4
        (2, "b", 4),
        (4, "b", 2),
        # a loop from 4 to 3
        (4, "a", 3),
        (3, "a", 4),
        # if sees c once, goes to second stage
        (1, "c", 5),
        (2, "c", 6),
        (3, "c", 7),
        (4, "c", 8),
        # stage two, which is exact copy of stage one
        (5, "a", 6),
        (6, "a", 5),
        (5, "b", 7),
        (7, "b", 5),
        (6, "b", 8),
        (8, "b", 6),
        (8, "a", 7),
        (7, "a", 8),
        # in stage two, if see c, then go to sink state
        (5, "c", 99),
        (6, "c", 99),
        (7, "c", 99),
        (8, "c", 99),
        (99, "a", 99),
        (99, "b", 99),
        (99, "c", 99),
    ],
    start=1,
    final=[6],
)


#
# Question 3
#


def inter(dfa1: DFA, dfa2: DFA):
    alphabet = dfa1["alphabet"]

    def transition(dfa: DFA, state: int, letter: str):
        for transition in dfa["delta"]:
            if transition[0] == state and transition[1] == letter:

                return int(transition[2])

        raise ValueError("dfa should have transition for every letter in every state")

    new_delta: "set[tuple[tuple[int, int], str, tuple[int, int]]]" = set()

    for state1 in dfa1["states"]:
        for state2 in dfa2["states"]:
            for letter in alphabet:
                new_delta.add(
                    (
                        (state1, state2),
                        letter,
                        (
                            transition(dfa1, state1, letter),
                            transition(dfa2, state2, letter),
                        ),
                    )
                )

    return {
        "states": [(i, j) for i in dfa1["states"] for j in dfa2["states"]],
        "alphabet": alphabet,
        "delta": new_delta,
        "start": (dfa1["start"], dfa2["start"]),
        "final": [(i, j) for i in dfa1["final"] for j in dfa2["final"]],
    }
