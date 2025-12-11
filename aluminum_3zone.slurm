#!/bin/bash

#SBATCH --job-name=aluminum_3zone
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=500G
#SBATCH --output=slurm-%j.out
#SBATCH --time=5:00:00
#SBATCH --constraint=amd
#SBATCH --qos=high               # high priority queue
#SBATCH --qos=urgent             # urgent priority queue (if available)
#SBATCH --mail-type=all         # send email if job fails
#SBATCH --mail-user=rl8728@princeton.edu

module purge
module load gurobi/12.0.0
module load julia/1.12.1

# Run case
GUROBI_HOME=/usr/licensed/gurobi/12.0.0/linux64 \
LD_LIBRARY_PATH=/usr/licensed/gurobi/12.0.0/linux64/lib:$LD_LIBRARY_PATH \
julia --project=. ExampleSystems/aluminum_3zone/run.jl