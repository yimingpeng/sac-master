#!/usr/bin/env python
import inspect
import os
import sys


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.abspath(os.path.join(os.getcwd(), os.pardir)), os.pardir)))
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
os.sys.path.insert(0, parentdir)

"""Description:
"""
__author__ = "Yiming Peng"
__copyright__ = "Copyright 2018, baselines"
__credits__ = ["Yiming Peng"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Yiming Peng"
__email__ = "yiming.peng@ecs.vuw.ac.nz"
__status__ = "Prototype"

# Scripts for generating GCP startup scripts
import os

person = 'yimingpeng'
# person = 'achen'

if person == 'achen':
    f = open("../grid_scripts/aaron_template.sh")
    f2 = open("../grid_scripts/run_aaron_grid_ex_template.sh")
else:
    f = open("../grid_scripts/template.sh")
    f2 = open("../grid_scripts/run_grid_ex_template.sh")
algorithms = ["SAC", "EAC", "RAC", "TAC"]
problems = ["HalfCheetahBulletEnv-v0", "HopperBulletEnv-v0", "Walker2DBulletEnv-v0", "ReacherBulletEnv-v0",
            "AntBulletEnv-v0", "LunarLanderContinuous-v2"]
scale_rewards = [0.5, 1.0, 3.0]
tsallisQs = [1.5, 2.0, 2.5]
renyiQs = [1.5, 2.0, 2.5]
num_of_trains = [1, 4]  # for Ant & HalfCheetah

seeds = range(5)
script_names = []


# Generate for Bullet problems

def generate_script(algorithm, scale_reward, tasllisQ = 2.0, renyiQ = 2.0, num_of_train=1):
    directory = "../grid_scripts/" + str(algorithm)
    for problem in problems:
        if not os.path.exists(directory):
            os.makedirs(directory)
        script_name = ""
        if algorithm == "RAC":
            script_name = directory + "/" + algorithm + "_" + problem + "_sr_" + str(scale_reward) + "_rQ_" + str(
                renyiQ) + "_nbt_" + str(num_of_train) + ".sh"
            f1 = open(script_name, 'w')
        elif algorithm == "TAC":
            script_name = directory + "/" + algorithm + "_" + problem + "_sr_" + str(scale_reward) + "_tQ_" + str(
                tasllisQ) + "_nbt_" + str(num_of_train) + ".sh"
            f1 = open(script_name, 'w')
        else:
            script_name = directory + "/" + algorithm + "_" + problem + "_sr_" + str(scale_reward) + "_nbt_" + str(
                num_of_train) + ".sh"
            f1 = open(script_name, 'w')
        script_names.append(script_name)
        for line in f:
            if 'pyName="pybullet_test_sac.py"' in line:
                line = line.replace("sac", algorithm.lower())
            if "BipedalWalker-v2" in line:
                if algorithm == "RAC":
                    line = "python $pyName --env {} " \
                           "--seed $SGE_TASK_ID --scale-reward {} --renyiQ {} --num-of-train {}\n" \
                        .format(problem, scale_reward, renyiQ, num_of_train)
                elif algorithm == "TAC":
                    line = "python $pyName --env {} " \
                           "--seed $SGE_TASK_ID --scale-reward {} --tsallisQ {} --num-of-train {}\n" \
                        .format(problem, scale_reward, tasllisQ, num_of_train)
                else:
                    line = "python $pyName --env {} " \
                           "--seed $SGE_TASK_ID --scale-reward {} --num-of-train {}\n".format(problem, scale_reward,
                                                                                              num_of_train)
            f1.write(line)
        f1.close()
        f.seek(0)


if __name__ == '__main__':
    for algorithm in algorithms:
        for scale_reward in scale_rewards:
            if algorithm == "RAC":
                for renyiQ in renyiQs:
                    for num_of_train in num_of_trains:
                        generate_script(algorithm, scale_reward, tasllisQ = 2.0, renyiQ = renyiQ, num_of_train = num_of_train)
            elif algorithm == "TAC":
                for tsallisQ in tsallisQs:
                    for num_of_train in num_of_trains:
                        generate_script(algorithm, scale_reward, tasllisQ = tsallisQ, renyiQ = 2.0, num_of_train = num_of_train)
            else:
                for num_of_train in num_of_trains:
                    generate_script(algorithm, scale_reward, num_of_train)

        f3 = open("../grid_scripts/" + str(algorithm) + "/run_grid_ex_" + algorithm + ".sh", 'w')
        for line_f2 in f2:
            if "ACKTR" in line_f2:
                line_f2 = line_f2.replace("ACKTR", algorithm)
            if "# scripts starts here" in line_f2:
                import glob

                all_files = glob.glob("../grid_scripts/" + str(algorithm) + "/*.sh")
                line_f2 += "\n"
                for file in all_files:
                    if "run_grid" not in file.split("/")[-1]:
                        line_f2 += "qsub -t 1-10:1 {}\n".format(file.split("/")[-1])
            f3.write(line_f2)
        f3.close()
        f2.seek(0)

# Generate for gym control problems
# for algorithm in algorithms:
#     for problem in gym_problems:
#         directory = "../../grid_scripts/" + str(algorithm)
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#         f1 = open(directory + "/" + algorithm + "_" +
#                   problem + ".sh", 'w')
#         for line in f:
#             if 'pyName="run_pybullet.py"' in line:
#                 if algorithm == "DDPG":
#                     line = line.replace("run_pybullet.py", "main.py")
#                 else:
#                     line = 'pyName="run_simple_ctrl.py"'
#             if "$experimentFolder/$experimentName/ppo1/" in line:
#                 line = "cd $experimentFolder/$experimentName/" + algorithm.lower() + "/\n"
#             if "BipedalWalker-v2" in line:
#                 if algorithm == "DDPG":
#                     line = "python $pyName --env-id " + problem + "-v2" + " --seed $SGE_TASK_ID\n"
#                 else:
#                     line = "python $pyName --env " + problem + "-v2" + " --seed $SGE_TASK_ID\n"
#             f1.write(line)
#         f1.close()
#         f.seek(0)
#
#     f3 = open(directory + "/run_grid_ex_" + algorithm + ".sh", 'w')
#     for line in f2:
#         if "ACKTR" in line:
#             line = line.replace("ACKTR", algorithm)
#         f3.write(line)
#     f3.close()
#     f2.seek(0)
# f.close()
