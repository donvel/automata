GRAPH_ATTRS = {
        'directed': True,
        'strict': False,
        'rankdir': 'LR',
        'ratio': '0.3',
        }

STATE_ATTRS = {
        'shape': 'circle',
        'height': '0.5',
        }

INIT_SHAPE = 'doublecircle'


def get_graph(aut):

    machine = aut.machine

    import pygraphviz as pgv

    graph = pgv.AGraph(title='machine', **GRAPH_ATTRS)
    graph.node_attr.update(STATE_ATTRS)

    for state in machine.states:
        shape = STATE_ATTRS['shape']
        if state == aut.init_state:
            shape = INIT_SHAPE
        graph.add_node(n=state.name, shape=shape)

    for state in machine.states:
        for (let, (out, to)) in state.trans.iteritems():
            label = let + ' | ' + (out if out else 'e')
            graph.add_edge(state.name, to.name, label=label)

    #graph.add_node('null', shape='plaintext', label=' ')
    #graph.add_edge('null', aut.init_state.name)


    return graph


def prepare_graph(nodes):
    import pygraphviz as pgv

    graph = pgv.AGraph(title='machine graph', **GRAPH_ATTRS)
    graph.node_attr.update(STATE_ATTRS)

    node_name = {}
    it = 0

    for node in nodes:
        node_name[node] = it
        it += 1
        graph.add_node(n=node_name[node], shape='circle') #, label="")

    for node in nodes:
        for (out, to) in node.edges:
            graph.add_edge(node_name[node], node_name[to],
                label=(out if out else 'e'))

    return graph

def prepare_lazy_graph(nodes):
    import pygraphviz as pgv

    graph = pgv.AGraph(title='machine graph', **GRAPH_ATTRS)
    graph.node_attr.update(STATE_ATTRS)

    node_name = {}
    it = 0

    for node in nodes:
        node_name[node] = it
        it += 1
        graph.add_node(n=node_name[node],
            shape=('square' if node.inf_word else 'circle'),
            label=node.lazy_word + ' ' +
            ('' if node.period == -1 else node.period)) #, label="")

    for node in nodes:
        for (out, to) in node.edges:
            graph.add_edge(node_name[node], node_name[to],
                label=(out if out else 'e'))

    return graph
