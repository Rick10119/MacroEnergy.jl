ENV["GUROBI_HOME"] = "/usr/licensed/gurobi/12.0.0/linux64"
ENV["LD_LIBRARY_PATH"] = ENV["GUROBI_HOME"] * "/lib:" * get(ENV, "LD_LIBRARY_PATH", "")

using MacroEnergy
using Gurobi

(system, model) = run_case(
    @__DIR__;
    optimizer=Gurobi.Optimizer,
    optimizer_attributes=("Method" => 2, "Crossover" => 0, "BarConvTol" => 1e-3),
    lazy_load=false,
);

