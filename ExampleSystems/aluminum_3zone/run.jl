# Set Gurobi environment variables to use system installation (12.0.0)
# CRITICAL: These must be set BEFORE loading Gurobi to force use of system library
ENV["GUROBI_HOME"] = "/usr/licensed/gurobi/12.0.0/linux64"
ENV["LD_LIBRARY_PATH"] = ENV["GUROBI_HOME"] * "/lib:" * get(ENV, "LD_LIBRARY_PATH", "")
# Fix OMP_NUM_THREADS warning
ENV["OMP_NUM_THREADS"] = get(ENV, "OMP_NUM_THREADS", "1")

# Force Julia to use system Gurobi library by preloading it with RTLD_GLOBAL
# This ensures the system library (12.0.0) is loaded and available globally
import Libdl
gurobi_lib_path = ENV["GUROBI_HOME"] * "/lib"
system_gurobi_lib = joinpath(gurobi_lib_path, "libgurobi120.so")
if isfile(system_gurobi_lib)
    try
        # Preload with RTLD_GLOBAL to make symbols available to all modules
        Libdl.dlopen(system_gurobi_lib, Libdl.RTLD_LAZY | Libdl.RTLD_GLOBAL)
        println("✓ Preloaded system Gurobi 12.0.0 library")
    catch e
        println("Warning: Could not preload system library: ", e)
    end
end

using MacroEnergy
# Gurobi is now in deps, so it will be automatically installed with Pkg.instantiate()
# LD_PRELOAD in SLURM script should force use of system Gurobi 12.0.0 library
using Gurobi

(system, model) = run_case(
    @__DIR__;
    optimizer=Gurobi.Optimizer,
    optimizer_attributes=("Method" => 2, "Crossover" => 0, "BarConvTol" => 1e-3),
    lazy_load=false,
);

