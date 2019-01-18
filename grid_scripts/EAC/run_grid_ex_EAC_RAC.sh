#! /bin/bash

# the repository
cd /vol/grid-solar/sgeusers/achen/sac-master/grid_scripts/EAC/

# setting the grid env
need sgegrid


# scripts starts here

qsub -t 1-5:1 EAC_RAC_AntBulletEnv-v0_sr_3.0_nbt_1_qvalue_1.5.sh










