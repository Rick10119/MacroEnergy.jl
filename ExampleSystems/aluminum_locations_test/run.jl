using MacroEnergy
using Gurobi

# Create Gurobi environment with parameters
if !(@isdefined GRB_ENV)
    const GRB_ENV = Gurobi.Env()
end

# Run the case with Gurobi optimizer and environment
(system, model) = run_case(@__DIR__; 
    optimizer=Gurobi.Optimizer, 
    optimizer_env=GRB_ENV
);
