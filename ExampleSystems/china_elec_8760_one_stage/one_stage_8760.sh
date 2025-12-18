#!/bin/bash

#SBATCH --job-name=china_31_provinces_8760
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=1000G
#SBATCH --output=slurm-%j.out
#SBATCH --time=72:00:00
#SBATCH --constraint=amd
#SBATCH --mail-type=all
#SBATCH --mail-user=al3792@princeton.edu

module purge
module load gurobi/13.0.0
module load julia/1.12.1

# Move to MacroEnergy directory
cd /home/al3792/MacroEnergy.jl

# Run case
julia --project=. "ExampleSystems/china_elec_8760_one_stage/run.jl"