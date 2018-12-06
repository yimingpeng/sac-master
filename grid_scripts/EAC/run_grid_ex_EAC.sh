#! /bin/bash

# the repository
cd /vol/grid-solar/sgeusers/yimingpeng/sac-master/grid_scripts/EAC/

# setting the grid env
need sgegrid


# scripts starts here

qsub -t 1-3:1 EAC_HalfCheetahBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_BipedalWalker-v2_sr_1.0.sh
qsub -t 1-3:1 EAC_BipedalWalker-v2_sr_0.5.sh
qsub -t 1-3:1 EAC_HopperBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_ThrowerBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_PusherBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_PusherBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_HopperBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_LunarLanderContinuous-v2_sr_3.0.sh
qsub -t 1-3:1 EAC_ThrowerBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_Walker2DBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_AntBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_ReacherBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_HumanoidBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_AntBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_ReacherBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_HumanoidBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_Walker2DBulletEnv-v0_sr_0.5.sh
qsub -t 1-3:1 EAC_PusherBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_LunarLanderContinuous-v2_sr_0.5.sh
qsub -t 1-3:1 EAC_ThrowerBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_LunarLanderContinuous-v2_sr_1.0.sh
qsub -t 1-3:1 EAC_HopperBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_HumanoidBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_Walker2DBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_ReacherBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_AntBulletEnv-v0_sr_3.0.sh
qsub -t 1-3:1 EAC_BipedalWalker-v2_sr_3.0.sh
qsub -t 1-3:1 EAC_HalfCheetahBulletEnv-v0_sr_1.0.sh
qsub -t 1-3:1 EAC_HalfCheetahBulletEnv-v0_sr_0.5.sh










