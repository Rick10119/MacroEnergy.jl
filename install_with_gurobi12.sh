#!/bin/bash
# Installation script for MacroEnergy with Gurobi 12.0.0
# This script ensures that Gurobi.jl is built against the correct Gurobi version

echo "=========================================="
echo "Installing MacroEnergy with Gurobi 12.0.0"
echo "=========================================="

# Load required modules
module purge
module load gurobi/12.0.0
module load julia/1.12.1

# Set Gurobi environment variables
if [ -z "$GUROBI_HOME" ]; then
    GUROBI_BIN=$(which gurobi_cl 2>/dev/null)
    if [ -n "$GUROBI_BIN" ]; then
        export GUROBI_HOME=$(dirname $(dirname "$GUROBI_BIN"))
    fi
fi

if [ -n "$GUROBI_HOME" ] && [ -d "$GUROBI_HOME/lib" ]; then
    export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
    export PATH=${GUROBI_HOME}/bin:${PATH}
    echo "✓ Using Gurobi from: $GUROBI_HOME"
else
    echo "✗ Error: GUROBI_HOME not properly set"
    exit 1
fi

# Verify Gurobi version
echo "✓ Gurobi version:"
gurobi_cl --version 2>&1 | head -1

# Navigate to MacroEnergy directory
# Update this path to match your server setup
MACROENERGY_DIR="${MACROENERGY_DIR:-/home/al3792/MacroEnergy.jl}"
if [ ! -d "$MACROENERGY_DIR" ]; then
    echo "✗ Error: MacroEnergy directory not found at $MACROENERGY_DIR"
    echo "   Please set MACROENERGY_DIR environment variable or update this script"
    exit 1
fi

cd "$MACROENERGY_DIR"
echo "✓ Working directory: $(pwd)"

# Install/update dependencies
echo ""
echo "Installing Julia packages..."
julia --project=. -e 'using Pkg; Pkg.instantiate()'

# Build Gurobi.jl with the correct Gurobi version
echo ""
echo "Building Gurobi.jl with Gurobi 12.0.0..."
julia --project=. -e 'using Pkg; Pkg.build("Gurobi"; verbose=true)'

# Verify the installation
echo ""
echo "Verifying Gurobi.jl installation..."
julia --project=. -e 'using Gurobi; println("✓ Gurobi.jl loaded successfully")'

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "You can now run your jobs with:"
echo "  sbatch aluminum_3zone.slurm"
echo ""

