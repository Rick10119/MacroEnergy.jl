#!/bin/bash

#SBATCH --job-name=aluminum_3zone
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=500G
#SBATCH --output=slurm-%j.out
#SBATCH --time=00:05:00
#SBATCH --constraint=amd
#SBATCH --qos=high               # high priority queue
#SBATCH --qos=urgent             # urgent priority queue (if available)
#SBATCH --mail-type=all         # send email if job fails
#SBATCH --mail-user=rl8728@princeton.edu

module purge
module load gurobi/13.0.0
module load julia/1.12.1

export GUROBI_HOME=/usr/licensed/gurobi/13.0.0/linux64
export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
export OMP_NUM_THREADS=1

# julia --project=. -e 'using Pkg; Pkg.instantiate()'

# Run case (--project=. now refers to MacroEnergy.jl root)
julia --project=. ExampleSystems/aluminum_3zone/run.jl