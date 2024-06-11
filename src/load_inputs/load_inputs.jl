# Base.@kwdef struct InputFilesNames
#     network::String = "Network.csv"
#     tedges::String = "TEdges.csv"
#     demand::String = "Demand.csv"
#     resources::String = "Resources.csv"
#     storage::String = "Storage.csv"
#     nodes::String = "Nodes.csv"
#     transformations::String = "Transformations.csv"
#     variability::String = "Variability.csv"
#     fuel_prices::String = "Fuel_Price.csv"
#     constraints::String = "Constraints.csv"
# end

# struct InputData
#     settings::NamedTuple
#     nodes::Dict
#     networks::Dict
#     resources::Dict
#     storage::Dict
#     transformations::Dict
# end
# settings(data::InputData) = data.settings
# nodes(data::InputData) = data.nodes
# networks(data::InputData) = data.networks
# resources(data::InputData) = data.resources
# storage(data::InputData) = data.storage
# transformations(data::InputData) = data.transformations

# @doc raw"""
# 	load_inputs(setup::Dict,path::AbstractString)

# Loads various data inputs from multiple input .csv files in path directory and stores variables in a Dict (dictionary) object for use in model() function

# inputs:
# setup - dict object containing setup parameters
# path - string path to working directory

# returns: Dict (dictionary) object containing all data inputs
# """
function load_inputs(settings::NamedTuple, input_path::AbstractString)

    # filenames = InputFilesNames()
    # @info "Reading in CSV Files from $input_path"

    # #hours_per_subperiod = settings.HoursPerSubperiod
    # period_length = settings.PeriodLength
    system_path = joinpath(input_path, "system")
    # Read in all the commodities
    commodities = load_commodities_json(system_path)

    # Read in time data
    time_data = load_time_json(system_path, commodities)

    # Read in all the nodes
    nodes = load_nodes_json(system_path, time_data)

    # Read in demand data
    load_demand_data!(nodes, system_path, commodities)

    # Read in fuel data
    fuel_data, co2_emission = load_fuel_data(system_path, commodities)

end

    # Define data structures to store input data
#     nodes_all = Dict()
#     networks = Dict(zip(commodities, repeat([], length(commodities))))
#     resources = Dict(zip(commodities, repeat(Vector{Resource}[], length(commodities))))
#     storages = Dict(zip(commodities, [Storage() for c in commodities]))
#     transformations = Vector{TEdge}()

#     # Read in data for each commodity
#     for commodity_name in keys(settings.Commodities)
#         commodity = commodity_type(commodity_name)

#         inputfolder_path = joinpath(input_path, commodity_name)

#         # Commodity specific settings
#         commodity_settings = settings.Commodities[commodity_name]

#         hours_per_timestep = commodity_settings["HoursPerTimeStep"]
#         hours_per_subperiod = commodity_settings["HoursPerSubperiod"]
#         time_interval = 1:hours_per_timestep:period_length
#         subperiods = collect(
#             Iterators.partition(
#                 time_interval,
#                 Int(hours_per_subperiod / hours_per_timestep),
#             ),
#         )

#         # Read nodes, demand, and fuel prices
#         node_file = filenames.nodes
#         demand_file = filenames.demand
#         fuel_prices_file = filenames.fuel_prices
#         nodes = load_nodes(
#             joinpath(inputfolder_path, node_file),
#             joinpath(inputfolder_path, demand_file),
#             joinpath(inputfolder_path, fuel_prices_file),
#             commodity,
#             time_interval,
#         )
#         nodes_all[commodity] = nodes

#         # Read in network related inputs
#         network_file = filenames.network
#         if isfile(joinpath(inputfolder_path, network_file))
#             networks[commodity] = load_network(
#                 joinpath(inputfolder_path, network_file),
#                 nodes,
#                 commodity,
#                 time_interval,
#             )
#         end

#         # Read in generator/resource related inputs
#         resource_file = filenames.resources
#         if isfile(joinpath(inputfolder_path, resource_file))
#             res = load_resources(
#                 joinpath(inputfolder_path, resource_file),
#                 nodes,
#                 commodity,
#                 time_interval,
#                 subperiods,
#             )

#             # Read in generator/resource availability profiles
#             variability_file = filenames.variability
#             load_variability!(joinpath(inputfolder_path, variability_file), res)
#             resources[commodity] = res
#         end

#         # Read in storage related inputs
#         storage_file = filenames.storage
#         if isfile(joinpath(inputfolder_path, storage_file))
#             storages[commodity] = load_storage(
#                 joinpath(inputfolder_path, storage_file),
#                 nodes,
#                 commodity,
#                 time_interval,
#                 subperiods,
#             )
#         end

#         # # Read constraints
#         # constraints_file = filenames.constraints
#         # load_constraints!(joinpath(inputfolder_path, constraints_file))
#     end

#     # collect all nodes actoss commodities
#     nodes = merge([nodes_all[i] for i in commodities]...)

#     # # Read in transformation related inputs
#     # tedges_file = filenames.tedges
#     # transformations_file = filenames.transformations
#     # transformations = load_tedges(
#     #     joinpath(input_path, tedges_file),
#     #     joinpath(input_path, transformations_file),
#     #     nodes,
#     # )

#     transformations = (node)

#     @info "CSV Files Successfully Read In From $input_path"
#     return InputData(settings, nodes, networks, resources, storages, transformations)
# end


function validate_id!(data::Dict{Symbol,Any})
    if !haskey(data, :id)
        throw(ArgumentError("TEdge data must have an id"))
    end
    return nothing
end

function validate_direction!(data::Dict{Symbol,Any})
    if haskey(data, :direction) && data[:direction] ∉ [:input, :output]
        if data[:direction] == "input"
            data[:direction] = :input
        elseif data[:direction] == "output"
            data[:direction] = :output
        else
            throw(ArgumentError("Invalid direction: $(data[:direction]) for TEdge $(data[:id])"))
        end        
    end
    return nothing
end

function validate_vector_symbol!(data::Dict{Symbol,Any}, key::Symbol)
    if haskey(data, key) && !isa(data[key], Vector{Symbol})
        data[key] = Symbol.(data[key])
    end
    return nothing
end

function validate_fuel_stoichiometry_name!(data::Dict{Symbol,Any})
    if haskey(data, :fuel_stoichiometry_name) && isa(data[:fuel_stoichiometry_name], String)
        data[:fuel_stoichiometry_name] = Symbol(data[:fuel_stoichiometry_name])
    else
        validate_vector_symbol!(data, :fuel_stoichiometry_name)
    end
    return nothing
end

function validate_stoichiometry_balance_names!(data::Dict{Symbol,Any})
    validate_vector_symbol!(data, :stoichiometry_balance_names)
    return nothing
end

function validate_data!(data::Dict{Symbol,Any})
    validate_id!(data)
    validate_direction!(data)
    validate_fuel_stoichiometry_name!(data)
    validate_stoichiometry_balance_names!(data)
    validate_constraints_data!(data)
    return nothing
end

function validate_constraints_data!(data::Dict{Symbol,Any})
    if haskey(data, :constraints) 
        constraints = Dict{Symbol,Any}()
        for (k,v) in data[:constraints]
            new_k = Symbol(join(push!(uppercasefirst.(split(string(k), "_")),"Constraint")))
            constraints[new_k] = v
        end
        data[:constraints] = constraints
    end
    return nothing 
end

function get_tedge_data(data::Dict{Symbol,Any}, commodity::Symbol, immutable::Bool=false)
    for (_, edge_data) in data[:edges]
        if edge_data[:type] == string(commodity)
            immutable && return edge_data
            return copy(edge_data)
        end
    end
    return nothing
end