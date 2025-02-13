import Test
using Logging
using MacroEnergy


test_logger = ConsoleLogger(stderr, Logging.Warn)

with_logger(test_logger) do
    Test.@testset verbose = true "Load Inputs" begin
        include("test_workflow.jl")
    end

    Test.@testset verbose = true "Writing Outputs" begin
        include("test_output.jl")
    end
    return nothing
end
