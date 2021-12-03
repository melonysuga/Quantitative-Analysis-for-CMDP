import os
import sys
from decimal import Decimal

import psutil

current_directory = os.path.dirname(os.path.abspath("test_MRP_AEV_601.py"))
root_path = os.path.abspath(os.path.dirname(current_directory) + os.path.sep + ".")
sys.path.append(root_path)

import aev_examples.read_cmdp_data
import time
from MRP import cmdp2n_mdp,cmdp2p_mdp,p_mdp2q_mdp
from MRRP import cmdp2p_mdp_RR,p_mdp2q_mdp_RR
from translate_to_sas import cmdp2sas


"""
In the context, the initial states in AEV examples of different sizes are given as follows:
    MRP:
    AEV_601_cap80   ->  (219,80)
    AEV_1006_cap120 ->  (659,120)
    AEV_3502_cap160 ->  (3178,152)
    AEV_7378_cap200 ->  (654,184)
    MRRP:
    AEV_601_cap80   ->  (287,79)
    AEV_1006_cap120 ->  (659,120)
    AEV_3502_cap160 ->  (3205,151)
    AEV_7378_cap200 ->  (7106,199)
"""

def show_info(start):
    pid = os.getpid()
    print(pid)
    print("pid--",type(pid))
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss/1024
    return memory


cmdp_info = aev_examples.read_cmdp_data.cmdp_info("AEV_601_cap80", 80)
mdp = cmdp_info.cmdp
cap = cmdp_info.cap
targets = cmdp_info.targets
SF = cmdp_info.SF
SFR = cmdp_info.SFR
SFRR = cmdp_info.SFRR



# n_mdp = cmdp2n_mdp.naive_flattened_mdp(mdp, targets, cap, SF)
# p_mdp = cmdp2p_mdp.pruned_mdp(mdp, targets, cap, SF,SFR,SFRR)
p_mdp = cmdp2p_mdp_RR.pruned_mdp(mdp,targets,cap,SF,SFR,SFRR)
print("pruned flattened mdp over!")
state = p_mdp.states.index((219,80))
namep = str(cap) + "_p"
cmdp2sas.cmdp_2_sas(p_mdp, state, namep)



q_mdp = p_mdp2q_mdp_RR.quotient_mdp(p_mdp,SFR,SFRR)
print("quotient flattened mdp over!")



# # print(naive_flattened_mdp.states[0])

# ind = n_mdp.states.index((659,120))

# ind = p_mdp.states.index((3178,152))

num = q_mdp.equivalence_class_map[(219,80)]
ind = q_mdp.states.index(num)


# ind = naive_flattened_mdp.states.index((601,85))
# print(ind)
# ind = 0
# cmdp2sas.cmdp_2_sas(p_mdp, ind)
nameq = str(cap) + "_q"
cmdp2sas.cmdp_2_sas(q_mdp, ind, nameq)
print("translate to sas file over!")





