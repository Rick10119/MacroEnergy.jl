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

# Set Gurobi environment variables
export GUROBI_HOME=/usr/licensed/gurobi/12.0.0/linux64
export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
export OMP_NUM_THREADS=1

# CRITICAL: Use LD_PRELOAD to force system Gurobi 12.0.0 library to be loaded first
# This overrides any downloaded Gurobi 13 library
export LD_PRELOAD=${GUROBI_HOME}/lib/libgurobi120.so

# Change to MacroEnergy.jl root directory
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl

# Install/update dependencies (Gurobi is now in deps, so it will be installed automatically)
# Note: Even if Gurobi.jl downloads Gurobi 13, we'll force use of system Gurobi 12.0.0 at runtime
julia --project=. -e 'using Pkg; Pkg.instantiate()'

# Run case (--project=. now refers to MacroEnergy.jl root)
julia --project=. ExampleSystems/aluminum_3zone/run.jl