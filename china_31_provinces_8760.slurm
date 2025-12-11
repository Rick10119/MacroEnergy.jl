#!/bin/bash

#SBATCH --job-name=china_31_provinces_8760
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

# Ensure Julia uses the correct Gurobi version
# The module system should set GUROBI_HOME, but we ensure library paths are correct
if [ -z "$GUROBI_HOME" ]; then
    # Fallback: try to find Gurobi installation from the loaded module
    GUROBI_BIN=$(which gurobi_cl 2>/dev/null)
    if [ -n "$GUROBI_BIN" ]; then
        export GUROBI_HOME=$(dirname $(dirname "$GUROBI_BIN"))
    fi
fi

# Set library path to ensure Julia can find Gurobi libraries
if [ -n "$GUROBI_HOME" ] && [ -d "$GUROBI_HOME/lib" ]; then
    export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
    export PATH=${GUROBI_HOME}/bin:${PATH}
    echo "Using Gurobi from: $GUROBI_HOME"
else
    echo "Warning: GUROBI_HOME not properly set. Julia may not find Gurobi 12.0.0"
fi

# Verify Gurobi version (for debugging)
echo "Gurobi version:"
gurobi_cl --version 2>&1 | head -1 || echo "  Could not determine version"

# Move to MacroEnergy directory
cd /home/al3792/MacroEnergy.jl

# Rebuild Gurobi.jl to ensure it uses the correct Gurobi version (12.0.0)
# This is important if the environment was originally installed with a different Gurobi version
echo "Rebuilding Gurobi.jl with Gurobi 12.0.0..."
julia --project=@. -e 'using Pkg; Pkg.build("Gurobi"; verbose=true)'

# Run case
julia --project=@. ExampleSystems/china_provinces_1_period_elec_cement_retrofit_agg_demand_one_co2_sink_uc_8760/run.jl