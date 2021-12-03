import os
from fractions import Fraction
def decimal_to_fraction(decimal_num):
    num = Fraction(decimal_num)
    numerator = num.numerator
    denominator = num.denominator
    return numerator, denominator

def cmdp_2_sas(mdp, ini_state, file_name):
    """
    :param mdp: the mdp which the initial CMDP is converted to, i.e. NAIVE_FLATTENED_MDP, PRUNED_MDP, QUOTIENT_MDP
    :param ini_state: the iniitial state to which the heuristic algorithm is applied
    :return:output.sas as the input of the MAXPROB solver
    """
    variable_file = open("variable.sas", mode="w")
    variable_no = 0
    operator_file = open("operator.sas", mode="w")

    add_state = [ini_state]
    state_num = [ini_state]

    targets = []

    cnt_operator = 0

    variable_file.write("begin_variable\n")
    variable_file.write("var{}\n".format(variable_no))
    variable_no += 1
    variable_file.write("-1\n2\nAtom atState(s{})\nNegatedAtom atState(s{})\n".format(variable_no, variable_no))
    variable_file.write("end_variable\n")
    while add_state:

        cur_state = add_state[0]
        add_state.remove(cur_state)

        if cur_state in mdp.new_targets:
            targets.append(cur_state)

        for ele in mdp.actions_for_state(cur_state):
            label = ele.label
            if len(ele.distr.keys()) == 1:
                key = list(ele.distr.keys())[0]
                if key == cur_state:
                    operator_file.write("begin_operator\n")

                    operator_file.write("{} s{} s{}\n".format(label, state_num.index(cur_state) + 1,
                                                            state_num.index(cur_state) + 1))
                    operator_file.write("0\n1\n0 {} 0 0\n0\n".format(state_num.index(cur_state)))
                    operator_file.write("end_operator\n")
                    cnt_operator += 1
                else:
                    if key not in state_num:
                        # add Variable
                        variable_file.write("begin_variable\n")
                        variable_file.write("var{}\n".format(variable_no))
                        variable_no += 1
                        state_num.append(key)
                        variable_file.write(
                            "-1\n2\nAtom atState(s{})\nNegatedAtom atState(s{})\n".format(variable_no, variable_no))
                        variable_file.write("end_variable\n")

                        add_state.append(key)
                    # add Operator
                    operator_file.write("begin_operator\n")

                    operator_file.write("{} s{} s{}\n".format(label, state_num.index(cur_state)+1,
                                                            state_num.index(key) + 1))
                    operator_file.write("0\n2\n0 {} 0 1\n0 {} 1 0\n0\n".format(state_num.index(cur_state),
                                                                               state_num.index(key)))
                    operator_file.write("end_operator\n")

                    cnt_operator += 1
            else:
                no = 0
                for key in ele.distr.keys():
                    num1, num2 = decimal_to_fraction(ele.distr[key])
                    if key not in state_num:
                        # add Variable
                        variable_file.write("begin_variable\n")
                        variable_file.write("var{}\n".format(variable_no))
                        variable_no += 1
                        state_num.append(key)
                        variable_file.write(
                            "-1\n2\nAtom atState(s{})\nNegatedAtom atState(s{})\n".format(variable_no, variable_no))
                        variable_file.write("end_variable\n")

                        add_state.append(key)

                    # add Operator
                    operator_file.write("begin_operator\n")

                    operator_file.write("{}_DETDUP_{}_WEIGHT_{}_{} s{} ss\n".format(label, no, num1, num2,state_num.index(cur_state) + 1))

                    operator_file.write("0\n2\n0 {} 0 1\n0 {} 1 0\n0\n".format(state_num.index(cur_state),
                                                                               state_num.index(key)))
                    operator_file.write("end_operator\n")

                    cnt_operator += 1
                    no += 1
    variable_file.close()
    operator_file.close()

    filename = "output" + file_name + ".sas"
    sas_file = open(filename, mode="w")
    sas_file.writelines(["begin_version\n","3\n","end_version\n","begin_metric\n","1\n","end_metric\n"])

    variable = open("variable.sas", mode="r")
    operator = open("operator.sas", mode="r")

    print(len(state_num), variable_no)

    num_variable = variable_no
    sas_file.write("{}\n".format(num_variable))
    # Group of Variables
    sas_file.write(variable.read())

    # Group of Mutex_group
    sas_file.writelines(["1\n","begin_mutex_group\n"])
    sas_file.write("{}\n".format(num_variable))
    for i in range(num_variable):
        sas_file.write("{} 1\n".format(i))
    sas_file.write("end_mutex_group\n")

    # Begin_state
    sas_file.write("begin_state\n")
    for i in range(num_variable):
        if state_num[i] == ini_state:
            sas_file.write("0\n")
        else:
            sas_file.write("1\n")
    sas_file.write("end_state\n")

    # Begin_goal
    sas_file.write("begin_goal\n")
    sas_file.write("{}\n".format(num_variable - len(targets)))
    for i in range(num_variable):
        if state_num[i] in targets:
            pass
        else:
            sas_file.write("{} 1\n".format(i))
    sas_file.write("end_goal\n")

    # Begin_operator
    sas_file.write("{}\n".format(cnt_operator))
    sas_file.write(operator.read())
    sas_file.write("0\n")
    sas_file.close()

    variable.close()
    operator.close()
    os.remove("variable.sas")
    os.remove("operator.sas")



# cnt_operator = 0
#     operator_file = open("operator_file.sas", mode="w")
#     for i in range(num_variable):
#         for ele in mdp.actions_for_state(i):
#             label = ele.label
#             if len(ele.distr) == 1:
#                 succ = list(ele.distr.keys())[0]
#                 operator_file.write("begin_operator\n")
#                 operator_file.write("{} s{} s{}\n".format(label, i, succ))
#                 operator_file.write("0\n")
#                 if i == succ:
#                     operator_file.write("1\n")
#                     operator_file.write("0 {} 0 0\n".format(i))
#                 else:
#                     operator_file.write("2\n")
#                     operator_file.write("0 {} 0 1\n".format(i))
#                     operator_file.write("0 {} 1 0\n".format(succ))
#                 operator_file.write("0\n")
#                 operator_file.write("end_operator\n")
#                 cnt_operator += 1
#             else:
#                 no = 0
#                 print("============")
#                 for succ in ele.distr.keys():
#                     num1, num2 = decimal_to_fraction(ele.distr[succ])
#                     print(ele.distr[succ], num1, num2)
#                     operator_file.write("begin_operator\n")
#                     operator_file.write("{}_DETDUP_{}_WEIGHT_{}_{} s{} s{}\n".format(label, no, num1, num2, i, succ))
#                     operator_file.write("0\n")
#                     operator_file.write("2\n")
#                     operator_file.write("0 {} 0 1\n".format(i))
#                     operator_file.write("0 {} 1 0\n".format(succ))
#                     operator_file.write("0\n")
#                     operator_file.write("end_operator\n")
#                     cnt_operator += 1
#                     no += 1
#     operator_file.write("0")
#     operator_file.close()
