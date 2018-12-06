#! /bin/bash

# the repository
cd /vol/grid-solar/sgeusers/yimingpeng/sac-master/grid_scripts/RAC/

# setting the grid env
need sgegrid


# scripts starts here

qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_0.5_rQ_1.5.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_0.5_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HopperBulletEnv-v0_sr_3.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_0.5_rQ_1.8.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_3.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_HumanoidBulletEnv-v0_sr_3.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_0.5_rQ_1.2.sh
qsub -t 1-3:1 RAC_Walker2DBulletEnv-v0_sr_1.0_rQ_1.5.sh
qsub -t 1-3:1 RAC_ThrowerBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_HalfCheetahBulletEnv-v0_sr_1.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_BipedalWalker-v2_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_AntBulletEnv-v0_sr_3.0_rQ_2.0.sh
qsub -t 1-3:1 RAC_ReacherBulletEnv-v0_sr_1.0_rQ_1.8.sh
qsub -t 1-3:1 RAC_PusherBulletEnv-v0_sr_1.0_rQ_1.2.sh
qsub -t 1-3:1 RAC_LunarLanderContinuous-v2_sr_3.0_rQ_1.2.sh










