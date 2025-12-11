# Set Gurobi environment variables to use system installation (12.0.0)
# CRITICAL: These must be set BEFORE loading Gurobi to force use of system library
ENV["GUROBI_HOME"] = "/usr/licensed/gurobi/12.0.0/linux64"
ENV["LD_LIBRARY_PATH"] = ENV["GUROBI_HOME"] * "/lib:" * get(ENV, "LD_LIBRARY_PATH", "")
# Fix OMP_NUM_THREADS warning
ENV["OMP_NUM_THREADS"] = get(ENV, "OMP_NUM_THREADS", "1")

# Force Julia to use system Gurobi library by preloading it
# This ensures the system library (12.0.0) is loaded instead of any downloaded version
import Libdl
gurobi_lib_path = ENV["GUROBI_HOME"] * "/lib"
system_gurobi_lib = joinpath(gurobi_lib_path, "libgurobi120.so")
if isfile(system_gurobi_lib)
    try
        # Preload the system Gurobi library to ensure it's used
        Libdl.dlopen(system_gurobi_lib, Libdl.RTLD_LAZY | Libdl.RTLD_GLOBAL)
        println("✓ Preloaded system Gurobi 12.0.0 library")
    catch e
        println("Note: Could not preload system library: ", e)
    end
end

using MacroEnergy
# Gurobi is now in deps, so it will be automatically installed with Pkg.instantiate()
# The system library should be used due to preloading and LD_LIBRARY_PATH
using Gurobi

(system, model) = run_case(
    @__DIR__;
    optimizer=Gurobi.Optimizer,
    optimizer_attributes=("Method" => 2, "Crossover" => 0, "BarConvTol" => 1e-3),
    lazy_load=false,
);

