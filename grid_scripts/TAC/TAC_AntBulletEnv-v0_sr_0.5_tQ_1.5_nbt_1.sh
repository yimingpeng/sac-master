#!/bin/sh
#
# force bourne shell if not sun grid engine default shell (you never know!)
#
#$ -s /bin/sh
#
# i know i have a directory here so i'll use it as my initial working directory
#
#$ -wd /vol/grid-solar/sgeusers/yimingpeng
#

#
# end of the setup directives
#
# now let's do something useful, but first change into the job-specific
# directory that should have been created for us
#
# check we have somewhere to work now and if we don't, exit nicely.
#
if [ -d /local/tmp/yimingpeng/$job_id.$sge_task_id ]; then
        cd /local/tmp/yimingpeng/$job_id.$sge_task_id
else
        echo "uh oh ! there's no job directory to change into "
        echo "something is broken. i should inform the programmers"
        echo "save some information that may be of use to them"
        echo "here's local tmp "
        ls -la /local/tmp
        echo "and local tmp yimingpeng "
        ls -la /local/tmp/yimingpeng
        echo "exiting"
        exit 1
fi
#
# now we are in the job-specific directory so now can do something useful
#
# stdout from programs and shell echos will go into the file
#    scriptname.o$job_id
#  so we'll put a few things in there to help us see what went on
#
#
# do specific stuff here. here i need to first use bash, then conda env list, source activate openai-neat.
#
echo ==uname==
uname -n
echo ==who am i and groups==
id
groups
echo ==sge_o_workdir==
echo $sge_o_workdir
echo ==/local/tmp==
ls -ltr /local/tmp/
echo ==/vol/grid-solar==
ls -l /vol/grid-solar/sgeusers/
#
# ok, where are we starting from and what's the environment we're in
#
echo ==run home==
pwd
ls
echo ==env==
env
echo ==set==
set
#
echo == whats in local/tmp on the machine we are running on ==
ls -ltra /local/tmp | tail
#
echo == whats in local tmp yimingpeng job_id at the start==
ls -la

#c
# run python environment in bash
#
echo ==setup bash==
bash
export path=/vol/grid-solar/sgeusers/yimingpeng/miniconda3/bin/:$path
source activate sac

#define path
experimentfolder="sac-master"
experimentname="examples"
pyname="pybullet_test_tac.py"

#
# copy the input file to the local directory
#
cp -r /vol/grid-solar/sgeusers/yimingpeng/$experimentfolder .

#
# cd into repo
#
echo ==going into experiment directory==
cd $experimentfolder/$experimentname/
#
# run experiment
#
echo ==running experiment==
python $pyname --env antbulletenv-v0 --seed $sge_task_id --scale-reward 0.5 --tsallisq 1.5 --num-of-train 1
#
echo ==and now, having done somthing useful and created some output==
ls -la

#
# now we move the output to a place to pick it up from later
#  (really should check that directory exists too, but this is just a test)
#
echo ==copy program run files==
mkdir -p /vol/grid-solar/sgeusers/yimingpeng/$experimentfolder/$job_id.$sge_task_id
cp -r ./logs /vol/grid-solar/sgeusers/yimingpeng/$experimentfolder/$job_id.$sge_task_id

#
echo "ran through ok"
