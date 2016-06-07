import drawer
import copy
import algorithms
import graphs

class State(object):

    def __init__(self, name):
        self.name = name
        self.trans = {}

    def add_trans(self, let, out, to):
        self.trans[let] = (out, to)

class MealyMachine(object):

    def __init__(self, alp=None, name=None):
        if alp is None:
            alp = {'a', 'b'}
        self.alphabet = alp
        self.name = name
        self.states = set()
        self.state_names = set()
        self.name_suffix = 1

    def add_state(self, name=None):
        if name is None:
            name = 'v' + str(self.name_suffix)
            self.name_suffix += 1
        s = State(name)
        assert name not in self.state_names
        self.state_names.add(name)
        self.states.add(s)
        return s

    def transition(self, state, word):
        cstate = state
        output = ''
        for c in word:
            (out, to) = cstate.trans[c]
            output += out
            cstate = to
        return (output, cstate)

class InitialAutomaton(object):

    def __init__(self, mch, ini):
        self.machine = mch
        self.init_state = ini

    def get_reachable(self):
        clone = copy.deepcopy(self)
        to_process = [clone.init_state]
        processed = set()
        while to_process:
            state = to_process.pop()
            if state in processed:
                continue
            processed.add(state)
            for (let, (out, to)) in state.trans.iteritems():
                to_process += [to]

        clone.machine.states = processed
        return clone

    def get_minimized(self):
        clone = self.get_reachable()
        return algorithms.minimize(clone)

    def output(self, word):
        return self.machine.transition(self.init_state, word)[0]

    def get_nonlazy(self):
        return algorithms.get_nonlazy(self)

    def get_canonical(self):
        return self.get_nonlazy().get_minimized()


def test():
    X = {'0', '1'}
    mch = MealyMachine(X, 'Thompson F')
    
    x1 = mch.add_state('x1')
    x0 = mch.add_state('x0')
    r = mch.add_state()
    b = mch.add_state()
    
    x1.add_trans('1', '1', x0)
    x1.add_trans('0', '0', b)
    x0.add_trans('1', '', r)
    x0.add_trans('0', '00', b)
    r.add_trans('1', '1', b)
    r.add_trans('0', '01', b)
    b.add_trans('1', '1', b)
    b.add_trans('0', '0', b)

    aut0 = InitialAutomaton(mch, x0)
    aut1 = InitialAutomaton(mch, x1)
 
    graph = drawer.get_graph(aut0)
    graph.draw('ThompsonF.svg', prog='dot')


    aut0_reach = aut0.get_reachable()
    
    drawer.get_graph(aut0_reach).draw('ThompsonFReach.svg', prog='dot')
    
    #aut1_early = aut1.get_early()
    
    #drawer.get_graph(aut1_early).draw('ThompsonFEarly.svg', prog='dot')

    dup = MealyMachine(X, 'Duplicated')

    a = dup.add_state('a')
    b1 = dup.add_state('b1')
    b2 = dup.add_state('b2')
    c = dup.add_state('c')
    
    a.add_trans('1', '011', b1)
    a.add_trans('0', '1011', b2)
    b1.add_trans('0', '01', b2)
    b1.add_trans('1', '101', c)
    b2.add_trans('0', '01', b2)
    b2.add_trans('1', '101', c)
    c.add_trans('0', '111', b1)
    c.add_trans('1', '111', a)

    autd = InitialAutomaton(dup, a)
    
    autd_mini = autd.get_minimized()

    drawer.get_graph(autd).draw('Dup.svg', prog='dot')
    drawer.get_graph(autd_mini).draw('DupMini.svg', prog='dot')

    print autd.output('010010010101001111')
    print autd_mini.output('010010010101001111')

    aut_mul = algorithms.mul_automata(aut0.get_reachable(), aut1.get_reachable()).get_reachable()
    drawer.get_graph(aut_mul).draw('Multi.svg', prog='dot')

    mch = MealyMachine(X, 'Lazy Automaton')
    a = mch.add_state('a')
    b = mch.add_state('b')
    c = mch.add_state('c')
    a.add_trans('0', '01', c)
    a.add_trans('1', '0', b)
    b.add_trans('0', '11', c)
    b.add_trans('1', '10', c)
    c.add_trans('0', '01', c)
    c.add_trans('1', '0', c)

    aut_lazy = InitialAutomaton(mch, a)
    drawer.get_graph(aut_lazy).draw('Lazy.svg', prog='dot')
    
    gr = graphs.machine_to_graph(aut_lazy.machine)[1]
    drawer.prepare_graph(gr).draw('AutLazyGraph.svg', prog='dot')
    graphs.compute_laziness(gr)
    drawer.prepare_lazy_graph(gr).draw('AutLazyGraphLazy.svg', prog='dot')


    nonlazy = algorithms.get_nonlazy(aut_lazy)
    drawer.get_graph(nonlazy).draw('Nonlazy.svg', prog='dot')

    mch = MealyMachine(X, 'Lazy Loop Automaton')
    a = mch.add_state('a')
    a.add_trans('0', '01', a)
    a.add_trans('1', '01', a)
    aut_loop = InitialAutomaton(mch, a)

    gr = graphs.machine_to_graph(aut_loop.machine)[1]
    drawer.prepare_graph(gr).draw('AutLazyLoopGraph.svg', prog='dot')
    graphs.compute_laziness(gr)
    drawer.prepare_lazy_graph(gr).draw('AutLazyLoopGraphLazy.svg', prog='dot')
    nonlazy = aut_loop.get_nonlazy()
    drawer.get_graph(nonlazy).draw('NonlazyLoop.svg', prog='dot')
    drawer.get_graph(nonlazy.get_minimized()).draw('NonlazyLoop.svg', prog='dot')
    
    
    drawer.get_graph(aut_loop.get_canonical()).draw('CanonLoop.svg', prog='dot')
    drawer.get_graph(aut_lazy.get_canonical()).draw('CanonLazy.svg', prog='dot')
    drawer.get_graph(aut_mul.get_canonical()).draw('CanonMulti.svg', prog='dot')
    drawer.get_graph(aut0.get_canonical()).draw('CanonThomp.svg', prog='dot')

    """

    aut0_canon = aut0.get_canon()
    aut1_canon = aut1.get_canon()

    print(aut0_canon)
    print(aut1_canon)

    print(aut0 == aut1)
    """


if __name__ == "__main__":
    test()
