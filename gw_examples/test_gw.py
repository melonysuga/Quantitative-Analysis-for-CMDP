import os
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


constants = {
    "size_x" : 60,
    "size_y" : "size_x",
    "capacity" : 60,
}
mdp = prism_to_consmdp("gw_param.prism", constants=constants)
print("mdp construction over!")
targets = [2789,2768,2915,2786,2566,2302,3408,2260,2641,2176,
           2695,2881,2893,3414,2361,1835,2199,2267,2967,2983,
           2672,2977,2176,2367,3326,3448,2903,2549,2659,3408,
           2776,2385,3185,3421,2195,3292,2109,2379,3018,3224,
           2559,3112,2956,2448,2294,2790,2464,3291,2294,2546,
           2200,625,676,729,2547,2386,2696,2177,2660,2295,2110]
# 2641,1835,2956,3291
for target in targets:
    target = [target]
    print("========construction on randomly chosen target========")
    print("target:", target)
    cap = 60



    solver = BasicES(mdp, cap, target)

    SF = solver.get_min_levels(SAFE)
    SFR = solver.get_min_levels(POS_REACH)
    SFRR = solver.get_min_levels(BUCHI)



    n_mdp = cmdp2n_mdp.naive_flattened_mdp(mdp, target, cap, SF)

    state = n_mdp.states[0]


    name = str(target) + "_n"
    cmdp2sas.cmdp_2_sas(n_mdp, 0, name)
    print("naive over")



    p_mdp = cmdp2p_mdp.pruned_mdp(mdp, target, cap, SF, SFR, SFRR)
    state = p_mdp.states[0]

    ind = p_mdp.states.index(state)
    name = str(target) + "_p"
    cmdp2sas.cmdp_2_sas(p_mdp, ind, name)
    print("pruned over")
    #
    #

    q_mdp = p_mdp2q_mdp.quotient_mdp(p_mdp, SFR, SFRR)

    num = q_mdp.equivalence_class_map[state]
    ind = q_mdp.states.index(num)
    name = str(target) + "_q"
    cmdp2sas.cmdp_2_sas(q_mdp, ind, name)

    # print("-----the MRP vector: get each entry when given an initial state and an initial resource level-----")
    # for state in smart_mdp.states:
    #     print(f"MRP for state: {state}")
    #     n_ind = bisimulation_mdp.states.index(state)
    #     print("by naive construction:",nstorm_result.at(n_ind))
    #     s_ind = smart_mdp.states.index(state)
    #     print("by pruned construction:",storm_result.at(s_ind))
    #     equivalence_class = smarter_mdp.equivalence_class_map[state]
    #     ind = smarter_mdp.states.index(equivalence_class)
    #     print("by quotient construction:",smarter_storm_result.at(ind))

