#!/usr/bin/env python3
"""DFA simulator. Zero dependencies."""

class DFA:
    def __init__(self, states, alphabet, transitions, start, accept):
        self.states = states; self.alphabet = alphabet
        self.transitions = transitions; self.start = start; self.accept = set(accept)

    def run(self, input_str):
        state = self.start
        for ch in input_str:
            key = (state, ch)
            if key not in self.transitions: return False, state
            state = self.transitions[key]
        return state in self.accept, state

    def accepts(self, input_str):
        return self.run(input_str)[0]

    def trace(self, input_str):
        path = [self.start]; state = self.start
        for ch in input_str:
            key = (state, ch)
            if key not in self.transitions: return path, False
            state = self.transitions[key]; path.append(state)
        return path, state in self.accept

    def minimize(self):
        # Hopcroft-like partition refinement
        P = [self.accept, self.states - self.accept]
        P = [p for p in P if p]
        changed = True
        while changed:
            changed = False
            new_P = []
            for group in P:
                split = {}
                for s in group:
                    sig = tuple(next((i for i, g in enumerate(P) if self.transitions.get((s,a)) in g), -1) for a in self.alphabet)
                    split.setdefault(sig, set()).add(s)
                parts = list(split.values())
                if len(parts) > 1: changed = True
                new_P.extend(parts)
            P = new_P
        return len(P)

if __name__ == "__main__":
    # DFA accepting strings ending in "ab"
    d = DFA({"q0","q1","q2"}, {"a","b"},
            {("q0","a"):"q1",("q0","b"):"q0",("q1","a"):"q1",("q1","b"):"q2",("q2","a"):"q1",("q2","b"):"q0"},
            "q0", {"q2"})
    print(f"'ab': {d.accepts('ab')}, 'aa': {d.accepts('aa')}")
