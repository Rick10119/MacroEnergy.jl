
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl
# Load required modules
module purge
module load gurobi/13.0.0
module load julia/1.12.1


# Install/update dependencies
echo ""
echo "Installing Julia packages..."
julia --project=. -e 'using Pkg; Pkg.instantiate()'


julia --project=. -e 'using Gurobi; println("✓ Gurobi.jl loaded successfully")'

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "You can now run your jobs with:"
echo "  sbatch aluminum_3zone.slurm"
echo ""

