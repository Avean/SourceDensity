#= Run the existing Warsaw TRBDF solver for poster section 3.4.

This is a wrapper: it never edits the solver or its model files.  It runs
GiererMainhardtRho.jl with a fixed ZigZag profile and
GiererMainhardtSourceTau.jl with the same profile stored in the evolving `sd`
field.  Both simulations start from u = 0 plus identical random local wounds.

Run from poster2:
  julia --project="C:/Users/Szymon/Documents/Github/MathBio Warsaw/Julia/Solver" \
    scripts/run_rho_static_dynamic.jl

Results are CSV files in generated/rho_static_dynamic_data/ for a separate
plotting script.  The only dynamic-model override is tau = 1e3.
=#
using DelimitedFiles
using Random

const SOLVER = raw"C:\Users\Szymon\Documents\Github\MathBio Warsaw\Julia\Solver"
const ROOT = normpath(joinpath(@__DIR__, ".."))
const OUT = joinpath(ROOT, "generated", "rho_static_dynamic_data")
mkpath(OUT)

include(joinpath(SOLVER, "src", "ReactionDiffusionApp.jl"))
using .ReactionDiffusionApp

const N = 401
const T_SNAPSHOTS = [0.0, 10.0, 100.0, 1000.0]
const TAU_DYNAMIC = 1.0e3
const X1, X2 = 0.20, 0.90
const WOUND_WIDTH, WOUND_AMPLITUDE = 0.025, 4.0
const RNG_SEED = 17


"""The three-ramp profile used in GiererMainhardtRho.jl."""
function zigzag(x, rho0, rho1)
    return [xx < X1 ? rho0 + rho1 * xx :
            xx < X2 ? rho0 + rho1 * (xx - X1) :
                      rho0 + rho1 * (xx - X2) for xx in x]
end


function wound_profile(x)
    rng = MersenneTwister(RNG_SEED)
    noise1 = 0.86 .+ 0.28 .* rand(rng, length(x))
    noise2 = 0.86 .+ 0.28 .* rand(rng, length(x))
    g1 = exp.(-0.5 .* ((x .- X1) ./ WOUND_WIDTH) .^ 2)
    g2 = exp.(-0.5 .* ((x .- X2) ./ WOUND_WIDTH) .^ 2)
    return WOUND_AMPLITUDE .* (noise1 .* g1 .+ noise2 .* g2)
end


function model_for(filename)
    key = "Gierer Mainhardt/" * filename
    return ReactionDiffusionApp.MODEL_REGISTRY[key]
end


function prepare_static()
    model = model_for("GiererMainhardtRho.jl")
    sim = create_simulation_state(model; N = N, dtmax = 1e-2, reltol = 1e-6, abstol = 1e-8)
    rho = zigzag(sim.x, sim.params[:ρ0], sim.params[:ρ1])
    sim.params[ReactionDiffusionApp.spatial_profile_override_key("ρ")] = rho
    U = ReactionDiffusionApp.solution_matrix(sim)
    U[:, 1] .= wound_profile(sim.x)
    U[:, 2] .= 0.0
    ReactionDiffusionApp.restart_after_manual_change!(sim, vec(U); dt_after_kick = 1e-7)
    return sim, rho
end


function prepare_dynamic()
    model = model_for("GiererMainhardtSourceTau.jl")
    sim = create_simulation_state(model; N = N, dtmax = 1e-2, reltol = 1e-6, abstol = 1e-8)
    sim.params[:τ] = TAU_DYNAMIC
    # The model's default Dsd is tied to its original tau.  Keep the intended
    # scaling Dsd = 15/tau in this wrapper as well.
    sim.params[:Dsd] = 15.0 / TAU_DYNAMIC
    rho = zigzag(sim.x, sim.params[:ρ0], sim.params[:ρ1])
    U = ReactionDiffusionApp.solution_matrix(sim)
    U[:, 1] .= wound_profile(sim.x)
    U[:, 2] .= 0.0
    U[:, 3] .= rho
    ReactionDiffusionApp.restart_after_manual_change!(sim, vec(U); dt_after_kick = 1e-7)
    return sim
end


function advance_to!(sim, target)
    while ReactionDiffusionApp.current_display_time(sim) < target
        ReactionDiffusionApp.step_simulation!(sim)
    end
end


function save_snapshot(prefix, sim, rho, t)
    U = ReactionDiffusionApp.solution_matrix(sim)
    data = hcat(sim.x, U[:, 1], rho)
    path = joinpath(OUT, "$(prefix)_t$(lpad(round(Int, t), 5, '0')).csv")
    open(path, "w") do io
        println(io, "x,u,rho")
        writedlm(io, data, ',')
    end
    println("wrote ", path)
end


function run_case(prefix, sim; dynamic = false)
    for t in T_SNAPSHOTS
        advance_to!(sim, t)
        U = ReactionDiffusionApp.solution_matrix(sim)
        rho = dynamic ? copy(U[:, 3]) : sim.params[ReactionDiffusionApp.spatial_profile_override_key("ρ")]
        save_snapshot(prefix, sim, rho, t)
        println(prefix, " t=", t, "  max(u)=", round(maximum(U[:, 1]); digits = 4))
    end
end


function main()
    static, _ = prepare_static()
    dynamic = prepare_dynamic()
    run_case("static", static)
    run_case("dynamic", dynamic; dynamic = true)
end

main()
