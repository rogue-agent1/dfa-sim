#!/usr/bin/env python3
"""DFA simulator — deterministic finite automaton."""
import sys, json

class DFA:
    def __init__(self, states, alphabet, transitions, start, accept):
        self.states = states; self.alphabet = alphabet
        self.transitions = transitions; self.start = start; self.accept = set(accept)
    def run(self, input_str):
        state = self.start; path = [state]
        for c in input_str:
            key = (state, c)
            if key not in self.transitions: return False, path
            state = self.transitions[key]; path.append(state)
        return state in self.accept, path
    def minimize(self):
        # Hopcroft's algorithm (simplified)
        P = [self.accept, self.states - self.accept]
        W = [self.accept.copy()]
        while W:
            A = W.pop()
            for c in self.alphabet:
                X = {s for s in self.states if self.transitions.get((s, c)) in A}
                new_P = []
                for Y in P:
                    inter = Y & X; diff = Y - X
                    if inter and diff:
                        new_P.extend([inter, diff])
                        if Y in W: W.remove(Y); W.extend([inter, diff])
                        else: W.append(inter if len(inter) <= len(diff) else diff)
                    else: new_P.append(Y)
                P = new_P
        return len(P)

if __name__ == "__main__":
    # DFA that accepts strings ending in "01"
    dfa = DFA(
        states={"q0","q1","q2"}, alphabet={"0","1"},
        transitions={("q0","0"):"q1",("q0","1"):"q0",("q1","0"):"q1",("q1","1"):"q2",("q2","0"):"q1",("q2","1"):"q0"},
        start="q0", accept={"q2"})
    tests = ["01","001","101","0101","11","00","1001"]
    print("DFA: accepts strings ending in '01'")
    for t in tests:
        accepted, path = dfa.run(t)
        print(f"  {t:>6s}: {'✅' if accepted else '❌'} path={' → '.join(path)}")
