from collections import defaultdict

class Node(object):
    def __init__(self):
        self.edges = []
        self.lazy = 0
        self.lazy_word = ""
        self.vis = -1

def dfs(n, it):
    n.vis = 0
    for (out, to) in n.edges:
        if (not out) and (to.vis == -1):
            it = dfs(to, it)
    n.vis = it
    return it + 1

# consider only eps edges, the entire graph need not be acyclic
def topol_sort(nodes):
    it = 1
    for n in nodes:
        if n.vis == -1:
            it = dfs(n, it)
    return sorted(nodes, key=lambda n : -n.vis)

def machine_to_graph(machine):
    state_to_node = {}
    nodes = []
    
    for st in machine.states:
        n = Node()
        nodes += [n]
        state_to_node[st] = n

    for st in machine.states:
        for (let, (out, to)) in st.trans.iteritems():
            word = out
            cnode = state_to_node[st]
            while len(word) > 1:
                n = Node()
                nodes += [n]
                cnode.edges += [(word[0], n)]
                cnode = n
                word = word[1:]
            cnode.edges += [(word, state_to_node[to])]

    return state_to_node, topol_sort(nodes)

def compute_laziness(nodes):
    N = len(nodes)
    for k in range(1, 3 * N + 1):
        for n in reversed(nodes):
            if n.lazy >= k - 1:
                good = True
                kth_letters = set()
                for (out, to) in n.edges:
                    if len(out) + to.lazy < k:
                        good = False
                        break
                    if (k == 1) and (len(out) == 1):
                        kth_letters.add(out)
                    else:
                        kth_letters.add(to.lazy_word[k-len(out)-1])
                    if len(kth_letters) > 1:
                        good = False
                        break
                if good:
                    n.lazy = k
                    n.lazy_word += kth_letters.pop()
