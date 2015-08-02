
from collections import defaultdict

def get_minimized(machine, init_state):
    init_partition = defaultdict(list)
    for st in machine.states:
        init_partition[st.trans] += st
    to_process = list(init_partition.items())
    processed = []
    while to_process:
        
