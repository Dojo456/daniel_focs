import homework1
from homework2 import *


def test_q1():
    assert accept_nfa(NFA_LAST, "") == False
    assert accept_nfa(NFA_LAST, "a") == True
    assert accept_nfa(NFA_LAST, "ba") == True
    assert accept_nfa(NFA_LAST, "bba") == True
    assert accept_nfa(NFA_LAST, "bbba") == True
    assert accept_nfa(NFA_LAST, "bbbab") == False
    assert accept_nfa(NFA_LAST, "bbbabb") == False
    assert accept_nfa(NFA_LAST, "aaaab") == False


def test_q2():
    assert language(to_dfa(NFA_LAST), 4, homework1.accept_dfa) == language(
        NFA_LAST, 4, accept_nfa
    )

    print(language(to_dfa(NFA_LAST), 4, homework1.accept_dfa))
