#!/bin/sh
#
# Force Bourne Shell if not Sun Grid Engine default shell (you never know!)
#
#$ -S /bin/sh
#
# I know I have a directory here so I'll use it as my initial working directory
#
#$ -wd /vol/grid-solar/sgeusers/achen
#

#
# End of the setup directives
#
# Now let's do something useful, but first change into the job-specific
# directory that should have been created for us
#
# Check we have somewhere to work now and if we don't, exit nicely.
#
if [ -d /local/tmp/achen/$JOB_ID.$SGE_TASK_ID ]; then
        cd /local/tmp/achen/$JOB_ID.$SGE_TASK_ID
else
        echo "Uh oh ! There's no job directory to change into "
        echo "Something is broken. I should inform the programmers"
        echo "Save some information that may be of use to them"
        echo "Here's LOCAL TMP "
        ls -la /local/tmp
        echo "AND LOCAL TMP achen "
        ls -la /local/tmp/achen
        echo "Exiting"
        exit 1
fi
#
# Now we are in the job-specific directory so now can do something useful
#
# Stdout from programs and shell echos will go into the file
#    scriptname.o$JOB_ID
#  so we'll put a few things in there to help us see what went on
#
#
# Do specific stuff here. Here i need to first use bash, then conda env list, source activate openai-neat.
#
echo ==UNAME==
uname -n
echo ==WHO AM I and GROUPS==
id
groups
echo ==SGE_O_WORKDIR==
echo $SGE_O_WORKDIR
echo ==/LOCAL/TMP==
ls -ltr /local/tmp/
echo ==/VOL/GRID-SOLAR==
ls -l /vol/grid-solar/sgeusers/
#
# OK, where are we starting from and what's the environment we're in
#
echo ==RUN HOME==
pwd
ls
echo ==ENV==
env
echo ==SET==
set
#
echo == WHATS IN LOCAL/TMP ON THE MACHINE WE ARE RUNNING ON ==
ls -ltra /local/tmp | tail
#
echo == WHATS IN LOCAL TMP achen JOB_ID AT THE START==
ls -la

#c
# Run python environment in bash
#
echo ==SETUP BASH==
bash
export PATH=/vol/grid-solar/sgeusers/achen/miniconda3/bin/:$PATH
source activate sac

#Define path
experimentFolder="sac-master"
experimentName="examples"
pyName="pybullet_test_rac.py"

#
# Copy the input file to the local directory
#
cp -r /vol/grid-solar/sgeusers/achen/$experimentFolder .

#
# cd into repo
#
echo ==GOING INTO EXPERIMENT DIRECTORY==
cd $experimentFolder/$experimentName/

#
# Run experiment
#
echo ==RUNNING EXPERIMENT==
python $pyName --env AntBulletEnv-v0 --seed $SGE_TASK_ID --scale-reward 3.0 --renyiQ 1.8
#
echo ==AND NOW, HAVING DONE SOMTHING USEFUL AND CREATED SOME OUTPUT==
ls -la

#
# Now we move the output to a place to pick it up from later
#  (really should check that directory exists too, but this is just a test)
#
echo ==COPY PROGRAM RUN FILES==
mkdir -p /vol/grid-solar/sgeusers/achen/$experimentFolder/$JOB_ID.$SGE_TASK_ID
cp -r ./logs /vol/grid-solar/sgeusers/achen/$experimentFolder/$JOB_ID.$SGE_TASK_ID

#
echo "Ran through OK"
