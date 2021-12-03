# Environment
The experiment was done on the Ubuntu 18.04 LTS.

# Dependencies
Our artifacts depend on several other tools and the recommended dependencies are as follows:

## FiMDP
- for pre-calculating the safety vector, positive reachability vector, almost-sure repeated reachability vector.
- **FiMDP** can be installed using pip from PyPI: pip install -U fimdp.

## Storm and Stormpy
- for reading PRISM models and calculating the maximal reachability/repeated reachability probability vectors.
- Install **Stormpy** by following the instructions on GitHub site: [Stormpy](https://moves-rwth.github.io/stormpy/).

## fd-prob
- for calculating the maximal (repeated) reachability by applying the heuristic algorithms in **MaxProb** problem.
- download **fd-prob** and install it by following the instruction in **README** file: [fd-prob](fai.cs.uni-saarland.de/downloads/fd-prob.zip).

# Usage
- We provide an intermediate translator which translates the flattened mdp into a SAS file.
- The SAS file is passed to the **fd-prob** planner to calculate the maximal (repeated) reachability probability.
- The directory "MRP" and "MRRP" contain the python files that have implemented three construction algorithms presented in our paper.
    - you can calculate the maximal reachability probability by calling the function interfaces in "MRP_calculate.py";
    - you can calculate the maximal repeated reahcability probability by calling the function interfaces in "MRRP_calculate.py".
- The directory "aev_examples" contains the data files of aev CMDP models and some experimental programs.
    - You can easily run the python files with prefix "test_MRP" to obtain the maximal reachability probability in each instance;
    - You can easily run the python files with prefix "test_MRRP" to obtain themaximal repeated reahcability probability in each instance.
- The directory "gw_examples" contains the prism file for gridworld.
    - you can easily run the python file "test_gw.py" to obtain the results.



