import os
import random
import sys
import time

import psutil

current_directory = os.path.dirname(os.path.abspath("test_gw.py"))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

from fimdp.io import prism_to_consmdp
from fimdp.energy_solvers import BasicES
from fimdp.objectives import BUCHI, SAFE, POS_REACH
import stormpy
from MRP import cmdp2n_mdp,cmdp2p_mdp,p_mdp2q_mdp
from translate_to_sas import cmdp2sas

def show_info(start):
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss/1024
    return memory


for i in range(10, 80, 10):
    constants = {
        "size_x": i,
        "size_y": "size_x",
        "capacity": i,
    }
    mdp = prism_to_consmdp("gw_param.prism", constants=constants)
    print("mdp construction over!")
    states = []
    while len(states) == 0:

        targets = [random.randint(0, i*i)]
        cap = i

        solver = BasicES(mdp, cap, targets)

        SF = solver.get_min_levels(SAFE)
        SFR = solver.get_min_levels(POS_REACH)
        SFRR = solver.get_min_levels(BUCHI)

        n_mdp = cmdp2n_mdp.naive_flattened_mdp(mdp, targets, cap, SF)


        p_mdp = cmdp2p_mdp.pruned_mdp(mdp, targets, cap, SF, SFR, SFRR)
        print(p_mdp.states)
        states = p_mdp.states
    state = p_mdp.states[0]
    name = "grid" + str(i) + "_n"
    cmdp2sas.cmdp_2_sas(n_mdp, 0, name)
    print("naive over")
    ind = p_mdp.states.index(state)
    name = "grid" + str(i) + "_p"
    cmdp2sas.cmdp_2_sas(p_mdp, ind, name)
    print("pruned over")

    q_mdp = p_mdp2q_mdp.quotient_mdp(p_mdp, SFR, SFRR)
    num = q_mdp.equivalence_class_map[state]
    ind = q_mdp.states.index(num)
    name = "grid" + str(i) + "_q"
    cmdp2sas.cmdp_2_sas(q_mdp, ind, name)
    print("quotient over")