#! /bin/bash

# the repository
cd /vol/grid-solar/sgeusers/achen/cmaes_baselines/grid_scripts/ACKTR/

# clone the repository
# git clone https://yimingpeng:Aa19820713@github.com/yimingpeng/cmaes_baselines &
# cd ./cmaes_baselines/grid_scripts/ACKTR/

# setting the grid env
need sgegrid
qsub -t 1-10:1 ACKTR_HalfCheetah.sh
qsub -t 1-10:1 ACKTR_Hopper.sh
qsub -t 1-10:1 ACKTR_InvertedDoublePendulum.sh
qsub -t 1-10:1 ACKTR_InvertedPendulum.sh
qsub -t 1-10:1 ACKTR_InvertedPendulumSwingup.sh
qsub -t 1-10:1 ACKTR_Reacher.sh
qsub -t 1-10:1 ACKTR_Walker2D.sh
qsub -t 1-10:1 ACKTR_BipedalWalker.sh
qsub -t 1-10:1 ACKTR_BipedalWalkerHardcore.sh
qsub -t 1-10:1 ACKTR_LunarLanderContinuous.sh





