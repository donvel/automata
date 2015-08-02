
from collections import defaultdict
from transducer import MealyMachine, InitialAutomaton

def minimize(automaton):
    
    machine = automaton.machine

    partition_id = defaultdict(int)
    partition = defaultdict(list)
    
    for i in range(len(machine.states)):
        
        partition = defaultdict(list)
        for st in machine.states:
            trans_type = frozenset((let, out, partition_id[to])
                    for (let, (out, to)) in st.trans.items())
            partition[trans_type] += [st]

        for (j, group) in enumerate(partition.values()):
            for st in group:
                partition_id[st] = j

    minimized = MealyMachine(machine.alphabet)
    reps = [(partition_id[group[0]], group[0]) for group in partition.values()]
    new_states = {}

    for (i, rep) in reps:
        new_states[i] = minimized.add_state()
    
    for (i, rep) in reps:
        for (let, (out, to)) in rep.trans.items():
            new_states[i].add_trans(let, out, new_states[partition_id[to]])

    return InitialAutomaton(minimized,
            new_states[partition_id[automaton.init_state]])


def mul_machines(mch1, mch2):
    assert mch1.alphabet == mch2.alphabet

    alp = mch1.alphabet
    res = MealyMachine(alp)
    pair_to_state = {}

    for st1 in mch1.states:
        for st2 in mch2.states
            pair_to_state[st1, st2] = res.add_state(st1.name + 'x' + st2.name)

    for st1 in mch1.states:
        for st2 in mch2.states:
            st = pair_to_state[st1, st2]
            for (let, (out1, to1)) in st1.trans.items():
                (out2, to2) = mch2.transition(st2, out)
                st.add_trans(let, pair_to_state[to1, to2])

def mul_automata(aut1, aut2):
    pass
