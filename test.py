from dfa_sim import DFA
d = DFA({"q0","q1","q2"}, {"a","b"},
        {("q0","a"):"q1",("q0","b"):"q0",("q1","a"):"q1",("q1","b"):"q2",("q2","a"):"q1",("q2","b"):"q0"},
        "q0", {"q2"})
assert d.accepts("ab")
assert d.accepts("aab")
assert not d.accepts("aa")
assert not d.accepts("")
path, acc = d.trace("ab")
assert path == ["q0","q1","q2"] and acc
assert d.minimize() >= 2
print("dfa_sim tests passed")
