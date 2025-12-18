#!/bin/bash

#SBATCH --job-name=ver12_china_aluminum_288
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mem=500G
#SBATCH --output=slurm-%j.out
#SBATCH --time=5:00:00
#SBATCH --constraint=amd
#SBATCH --qos=high               # high priority queue
#SBATCH --qos=urgent             # urgent priority queue (if available)
#SBATCH --mail-type=all          # send email on all events
#SBATCH --mail-user=rl8728@princeton.edu

module purge
module load gurobi/13.0.0
module load julia/1.12.1

export OMP_NUM_THREADS=1

julia --project=@. -e '
    using Pkg;
    Pkg.add("Gurobi");
    Pkg.build("Gurobi"; verbose=true);
'

# 更新package

# 运行 Ver12 案例（Benders）
julia --project=@. ExampleSystems/Ver12_China_elec_multistage_288_7_v1107CO2cap-CO2cap1_CCS/run_benders.jl


