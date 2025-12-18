#!/bin/bash

#SBATCH --job-name=china_elec_8760_one_stage
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=20
#SBATCH --mem=100G
#SBATCH --output=slurm-%j.out
#SBATCH --time=24:00:00
#SBATCH --constraint=amd
#SBATCH --qos=high               # high priority queue
#SBATCH --qos=urgent             # urgent priority queue (if available)
#SBATCH --mail-type=all          # send email on all events
#SBATCH --mail-user=rl8728@princeton.edu

module purge
module load gurobi/13.0.0
module load julia/1.12.1

# 运行 Ver12 案例（Benders）
julia --project=@. ExampleSystems/china_elec_8760_one_stage/run.jl


