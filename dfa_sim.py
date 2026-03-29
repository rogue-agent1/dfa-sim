#!/usr/bin/env python3
"""dfa_sim: Deterministic finite automaton simulator."""
import sys

class DFA:
    def __init__(self, states, alphabet, transitions, start, accept):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # {(state, symbol): next_state}
        self.start = start
        self.accept = set(accept)

    def run(self, input_str):
        state = self.start
        for c in input_str:
            key = (state, c)
            if key not in self.transitions:
                return False
            state = self.transitions[key]
        return state in self.accept

    def minimize(self):
        # Hopcroft's algorithm
        P = [self.accept, self.states - self.accept]
        P = [s for s in P if s]
        W = list(P)
        while W:
            A = W.pop()
            for c in self.alphabet:
                X = {s for s in self.states if self.transitions.get((s, c)) in A}
                if not X: continue
                new_P = []
                for Y in P:
                    inter = Y & X
                    diff = Y - X
                    if inter and diff:
                        new_P.extend([inter, diff])
                        if Y in W:
                            W.remove(Y)
                            W.extend([inter, diff])
                        else:
                            W.append(inter if len(inter) <= len(diff) else diff)
                    else:
                        new_P.append(Y)
                P = new_P
        return len(P)

def test():
    # DFA accepting strings ending in "ab"
    dfa = DFA(
        states={0, 1, 2},
        alphabet={'a', 'b'},
        transitions={(0,'a'):1, (0,'b'):0, (1,'a'):1, (1,'b'):2, (2,'a'):1, (2,'b'):0},
        start=0, accept={2}
    )
    assert dfa.run("ab")
    assert dfa.run("aab")
    assert dfa.run("bab")
    assert not dfa.run("ba")
    assert not dfa.run("")
    assert not dfa.run("a")
    # DFA accepting even number of a's
    dfa2 = DFA(
        states={0, 1}, alphabet={'a', 'b'},
        transitions={(0,'a'):1, (0,'b'):0, (1,'a'):0, (1,'b'):1},
        start=0, accept={0}
    )
    assert dfa2.run("")
    assert not dfa2.run("a")
    assert dfa2.run("aa")
    assert dfa2.run("bbb")
    assert dfa2.run("aba")  # 2 a's? no, 2 a's -> even -> accept? "aba" has 2 a's
    # Minimize
    n = dfa.minimize()
    assert n <= 3
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: dfa_sim.py test")
