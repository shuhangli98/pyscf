#!/bin/bash
#SBATCH --job-name test
#SBATCH -o out/test-%A_%a.out
#SBATCH --nodes=1
#SBATCH --qos=gen
#SBATCH --partition=icc
#SBATCH --constraint=genoa
#SBATCH --time=7-0:00:00
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=48
#SBATCH --no-requeue
#SBATCH --array=0-0
#SBATCH --mem=1500G

source ~/.bashrc
source ~/environment.sh

XPWD=`pwd`

echo "===================================================="
echo "        Job ID is:         $SLURM_JOBID"
echo "        Job name is:       $SLURM_JOB_NAME"
echo "        Hostname is:       "`hostname`
echo "        This dir is:       $XPWD"
echo "        CPUs per Task is:  $SLURM_CPUS_PER_TASK"
echo "        Tasks per Node is: $SLURM_TASKS_PER_NODE"
echo "        Mem per CPU is:    $SLURM_MEM_PER_CPU"
echo "        Mem per GPU is:    $SLURM_MEM_PER_GPU"
echo "        Mem per node is:   $SLURM_MEM_PER_NODE"

export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export PYTHONUNBUFFERED=1
export LD_PRELOAD=

# mkdir /mnt/home/sli11/ceph/$SLURM_JOB_NAME

# export PYSCF_TMPDIR="/mnt/home/sli11/ceph/$SLURM_JOB_NAME"
export PYSCF_TMPDIR='/tmp'

IX=${SLURM_ARRAY_TASK_ID}

file_name=25-k_points_mpi_ccsd

# { time python3 -u ${file_name}.py ${IX}; } |& tee ${file_name}-${IX}.out
(orterun --map-by ppr:$SLURM_TASKS_PER_NODE:node:pe=$OMP_NUM_THREADS python3 -u ${file_name}.py ${IX}) |& tee ${file_name}-${IX}.out