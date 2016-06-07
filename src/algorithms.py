
from collections import defaultdict
from transducer import MealyMachine, InitialAutomaton, State
from string_alg import word_minus, cut_off
import graphs
import copy

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
        for st2 in mch2.states:
            pair_to_state[st1, st2] = res.add_state(st1.name + ', ' + st2.name)

    for st1 in mch1.states:
        for st2 in mch2.states:
            st = pair_to_state[st1, st2]
            for (let, (out1, to1)) in st1.trans.items():
                (out2, to2) = mch2.transition(st2, out1)
                st.add_trans(let, out2, pair_to_state[to1, to2])
    return (res, pair_to_state)

def mul_automata(aut1, aut2):
    res, pair_to_state = mul_machines(aut1.machine, aut2.machine)
    return InitialAutomaton(res, pair_to_state[aut1.init_state, aut2.init_state])

def add_nonlazy_trans(state, let, to, out_word, node_to, aut):
    if node_to.inf_word:
        out_word += node_to.period
        u, v = cut_off(out_word, len(node_to.period))
        nstate = aut.machine.add_state(
                state.name + "|" + let + "|loop")
        state.trans[let] = (u, nstate)
        for x in aut.machine.alphabet:
            nstate.trans[x] = (v, nstate)
    else:
        state.trans[let] = (out_word, to)


def get_nonlazy(aut):
    aut = copy.deepcopy(aut)
    state_to_node, gr = graphs.machine_to_graph(aut.machine)
    graphs.compute_laziness(gr)
  

    init_node = state_to_node[aut.init_state]
    new_init = aut.machine.add_state("-1")

    for (let, (out, to)) in aut.init_state.trans.iteritems():
        node_to = state_to_node[to]
        out_word = out + node_to.lazy_word
        add_nonlazy_trans(new_init, let, to, out_word, node_to, aut)
    aut.init_state = new_init

    for state in aut.machine.states:
        if state in state_to_node:
            node_from = state_to_node[state]
            if node_from.inf_word:
                for (let, (out, to)) in state.trans.items():
                    state.trans[let] = ("", state)
            else:
                for (let, (out, to)) in state.trans.items():
                    node_to = state_to_node[to]
                    out_word = word_minus(out + node_to.lazy_word,
                            node_from.lazy_word)
                    add_nonlazy_trans(state, let, to, out_word, node_to, aut)
    return aut

