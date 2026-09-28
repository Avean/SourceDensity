# Phase portraits for poster subsection 2.1
#
#   ∂t u = a u²/v − μu u
#   ∂t v = b u² − μv v + p_v
#
# Left : p_v = 0  -> one positive steady state, no resting state
# Right: p_v > 0  -> stable rest state E0, threshold E−, active state E+
#
# Run from the poster2 folder:  julia scripts/phase_portraits.jl
# Output: generated/phase_one_state.{pdf,png}, generated/phase_three_states.{pdf,png}

using CairoMakie

# ---------------------------------------------------------------- palette
const PAPER  = colorant"#F4F6F5"   # poster background
const PETROL = colorant"#123B4A"
const COPPER = colorant"#D0703C"
const UCOL   = colorant"#C61826"   # activator nullcline
const VCOL   = colorant"#0072B2"   # inhibitor nullcline
const INK    = colorant"#1E2A30"
const RULE   = colorant"#CFD8DA"
const ARROW  = colorant"#8A979C"

# ---------------------------------------------------------------- parameters (solver values)
const a, b, μu, μv = 1.5, 2.0, 0.5, 1.0
const ULIM, VLIM = (0.0, 2.0), (0.0, 6.0)

f(u, v) = a * u^2 / v - μu * u
g(u, v, pv) = b * u^2 - μv * v + pv

"Homogeneous steady states with their role (:rest, :threshold, :active)."
function steady_states(pv)
    if pv == 0
        ū = a * μv / (b * μu)
        return [(ū, a * ū / μu, :active)]
    end
    Δ = a^2 * μv^2 - 4μu^2 * b * pv
    states = [(0.0, pv / μv, :rest)]
    if Δ > 0
        for (s, role) in ((-1, :threshold), (1, :active))
            ū = (a * μv + s * sqrt(Δ)) / (2μu * b)
            push!(states, (ū, a * ū / μu, role))
        end
    end
    states
end

fontname = Sys.iswindows() || isfile("/Library/Fonts/Arial.ttf") ? "Arial" : "Liberation Sans"

function portrait(pv, stem)
    # 18.8 cm ≈ 533 pt wide -> 1:1 scale on the poster
    fig = Figure(size = (533, 350), backgroundcolor = PAPER, fontsize = 20,
                 fonts = (; regular = fontname, bold = fontname * " Bold"),
                 figure_padding = (4, 14, 4, 8))
    ax = Axis(fig[1, 1];
        backgroundcolor = PAPER,
        xlabel = "activator  u", ylabel = "inhibitor  v",
        xlabelcolor = UCOL, ylabelcolor = VCOL,
        xgridcolor = RULE, ygridcolor = RULE,
        topspinevisible = false, rightspinevisible = false,
        leftspinecolor = INK, bottomspinecolor = INK,
        xticks = 0:0.5:2, yticks = 0:2:6)
    limits!(ax, ULIM..., VLIM...)

    # direction field: arrows of equal visual length
    ru, rv = ULIM[2] - ULIM[1], VLIM[2] - VLIM[1]
    L = 0.034                                    # fraction of the axis box
    shafts = Point2f[]; tips = Point2f[]; angles = Float32[]
    for u in range(0.10, 1.95, length = 13), v in range(0.30, 5.85, length = 13)
        du, dv = f(u, v) / ru, g(u, v, pv) / rv   # direction in axis-normalised units
        n = hypot(du, dv); n < 1e-12 && continue
        eu, ev = du / n, dv / n
        p0 = Point2f(u - 0.5L * eu * ru, v - 0.5L * ev * rv)
        p1 = Point2f(u + 0.5L * eu * ru, v + 0.5L * ev * rv)
        push!(shafts, p0, p1); push!(tips, p1); push!(angles, atan(ev, eu) - π / 2)
    end
    linesegments!(ax, shafts; color = ARROW, linewidth = 1.6)
    scatter!(ax, tips; marker = :utriangle, rotation = angles, markersize = 8,
             color = ARROW, strokewidth = 0)

    # nullclines
    us = range(ULIM..., length = 400)
    lines!(ax, us, (b .* us .^ 2 .+ pv) ./ μv; color = VCOL, linewidth = 4)   # v-nullcline
    lines!(ax, us, a .* us ./ μu; color = UCOL, linewidth = 4)                # u-nullcline
    lines!(ax, [0.0, 0.0], [VLIM...]; color = UCOL, linewidth = 6)           # u = 0 branch
    limits!(ax, ULIM..., VLIM...)

    # steady states
    for (u, v, role) in steady_states(pv)
        if role == :rest
            scatter!(ax, [u], [v]; color = PETROL, markersize = 24,
                     strokecolor = PAPER, strokewidth = 2.5)
        elseif role == :threshold
            scatter!(ax, [u], [v]; color = PAPER, markersize = 22,
                     strokecolor = COPPER, strokewidth = 4)
        else
            scatter!(ax, [u], [v]; color = COPPER, markersize = 24,
                     strokecolor = PAPER, strokewidth = 2.5)
        end
    end

    outdir = normpath(joinpath(@__DIR__, "..", "generated"))
    mkpath(outdir)
    save(joinpath(outdir, stem * ".pdf"), fig)
    save(joinpath(outdir, stem * ".png"), fig; px_per_unit = 3)
end

portrait(0.0, "phase_one_state")
portrait(1.0, "phase_three_states")
println("phase portraits written to generated/")
