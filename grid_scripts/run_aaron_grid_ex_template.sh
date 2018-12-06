#! /bin/bash

# the repository
cd /vol/grid-solar/sgeusers/yimingpeng/cmaes_baselines/grid_scripts/ACKTR/

# setting the grid env
need sgegrid
qsub -t 1-5:1 HalfCheetah.sh




