using CairoMakie
using LinearAlgebra
using Random

const RED = colorant"#C61826"
const OXBLOOD = colorant"#590D08"
const BLUE = colorant"#0072B2"
const TEAL = colorant"#009E73"
const ORANGE = colorant"#E69F00"
const INK = colorant"#202124"
const MID = colorant"#6B6F72"
const GRID = colorant"#D8D4CC"
const SAND = colorant"#F4F1EA"

const OUTDIR = normpath(joinpath(@__DIR__, "..", "generated"))
mkpath(OUTDIR)

set_theme!(Theme(
    fontsize = 28,
    font = "Arial",
    Axis = (
        backgroundcolor = :white,
        xgridcolor = GRID,
        ygridcolor = GRID,
        xgridwidth = 1,
        ygridwidth = 1,
        spinewidth = 2,
        xtickwidth = 2,
        ytickwidth = 2,
        xlabelsize = 27,
        ylabelsize = 27,
        titlesize = 30,
    ),
))

function saveboth(fig, stem; px_per_unit = 2.0)
    save(joinpath(OUTDIR, stem * ".png"), fig; px_per_unit)
    save(joinpath(OUTDIR, stem * ".pdf"), fig)
end

# -----------------------------------------------------------------------------
# 1. Homogeneous phase portraits for the inhibitor-production model
# -----------------------------------------------------------------------------

function equilibria(a; b = 1.0, μu = 0.8, μv = 1.0, K = 1.0)
    disc = a^2 - 4b * μu^2 * K / μv
    roots = Tuple{Float64,Float64}[(0.0, 0.0)]
    if disc > 0
        uminus = (a - sqrt(disc)) * μv / (2b * μu)
        uplus = (a + sqrt(disc)) * μv / (2b * μu)
        push!(roots, (uminus, b * uminus^2 / μv))
        push!(roots, (uplus, b * uplus^2 / μv))
    end
    roots
end

function phase_panel!(ax, a, title)
    μu, μv, b, K = 0.8, 1.0, 1.0, 1.0
    us = range(0.04, 3.35, length = 18)
    vs = range(0.04, 7.2, length = 17)
    xs = Float64[]; ys = Float64[]; dus = Float64[]; dvs = Float64[]
    for v in vs, u in us
        du = a * u^2 / (K + v) - μu * u
        dv = b * u^2 - μv * v
        mag = hypot(du, dv) + 1e-12
        push!(xs, u); push!(ys, v)
        push!(dus, 0.16 * du / mag); push!(dvs, 0.34 * dv / mag)
    end
    arrows!(ax, xs, ys, dus, dvs; color = (:gray35, 0.58), linewidth = 1.5,
            arrowsize = 10)

    ucurve = range(0, 3.4, length = 400)
    lines!(ax, ucurve, b .* ucurve.^2 ./ μv; color = BLUE, linewidth = 6,
           label = "inhibitor nullcline")
    ustart = μu * K / a
    uact = range(ustart, 3.4, length = 300)
    lines!(ax, uact, a .* uact ./ μu .- K; color = RED, linewidth = 6,
           label = "activator nullcline")
    lines!(ax, [0, 0], [0, 7.4]; color = RED, linewidth = 6)

    eqs = equilibria(a; b, μu, μv, K)
    for (i, (u, v)) in enumerate(eqs)
        if i == 2
            scatter!(ax, [u], [v]; color = :white, strokecolor = ORANGE,
                     strokewidth = 5, markersize = 25)
        else
            scatter!(ax, [u], [v]; color = i == 1 ? INK : TEAL,
                     strokecolor = :white, strokewidth = 2, markersize = 25)
        end
    end
    xlims!(ax, 0, 3.4); ylims!(ax, 0, 7.4)
    ax.title = title
    ax.xlabel = "activator  u"
    ax.ylabel = "inhibitor  v"
end

fig = Figure(size = (1800, 760), backgroundcolor = :white)
ax1 = Axis(fig[1, 1])
ax2 = Axis(fig[1, 2])
phase_panel!(ax1, 1.2, "ONE STATE  ·  rest only")
phase_panel!(ax2, 2.4, "THREE STATES  ·  rest / threshold / active")
Legend(fig[2, 1:2], [LineElement(color = RED, linewidth = 6),
                     LineElement(color = BLUE, linewidth = 6),
                     MarkerElement(color = INK, marker = :circle, markersize = 18),
                     MarkerElement(color = :white, strokecolor = ORANGE, strokewidth = 4,
                                   marker = :circle, markersize = 18),
                     MarkerElement(color = TEAL, marker = :circle, markersize = 18)],
       ["u-nullcline", "v-nullcline", "stable rest", "unstable threshold", "active state"],
       orientation = :horizontal, tellwidth = false, framevisible = false, labelsize = 25,
       padding = (0, 0, 0, 0))
rowgap!(fig.layout, 8)
saveboth(fig, "phase_portraits")

# -----------------------------------------------------------------------------
# 2. Threshold regeneration: representative numerical trajectories
#    The kinetic parameters match the v+1 implementation used in the solver.
# -----------------------------------------------------------------------------

function lap_neumann!(out, z, dx)
    n = length(z)
    out[1] = 2 * (z[2] - z[1]) / dx^2
    @inbounds for i in 2:n-1
        out[i] = (z[i-1] - 2z[i] + z[i+1]) / dx^2
    end
    out[n] = 2 * (z[n-1] - z[n]) / dx^2
    out
end

"""A robust positivity-preserving semi-explicit integrator for poster-scale runs."""
function gm_simulate(; L = 1.0, N = 241, T = 80.0, amp = 0.2, center = 0.06,
                     width = 0.035, background = :rest, seed = 7,
                     Du = 0.0015, Dv = 0.08, a = 1.5, b = 2.0,
                     μu = 0.5, μv = 1.0, dt = nothing)
    x = collect(range(0, L, length = N))
    dx = x[2] - x[1]
    h = isnothing(dt) ? min(0.0015, 0.18 * dx^2 / max(Du, Dv)) : dt
    nsteps = ceil(Int, T / h)
    h = T / nsteps
    Random.seed!(seed)
    if background == :active
        u = 1 .+ 0.008 .* randn(N)
        v = 2 .+ 0.008 .* randn(N)
    else
        u = amp .* exp.(-((x .- center) ./ width).^2)
        v = zeros(N)
    end
    lu = similar(u); lv = similar(v)
    for _ in 1:nsteps
        lap_neumann!(lu, u, dx); lap_neumann!(lv, v, dx)
        @. u = max(0, u + h * (Du * lu + a * u^2 / (v + 1) - μu * u))
        @. v = max(0, v + h * (Dv * lv + b * u^2 - μv * v))
    end
    x, u, v
end

xw, uw, vw = gm_simulate(amp = 0.18, T = 55.0)
xs, us, vs = gm_simulate(amp = 2.4, T = 55.0)

fig = Figure(size = (1700, 710), backgroundcolor = :white)
for (j, (x, u, ttl, sub)) in enumerate(((xw, uw, "WEAK WOUND", "returns to rest"),
                                         (xs, us, "STRONG WOUND", "crosses the threshold")))
    ax = Axis(fig[1, j], title = ttl, xlabel = "position  x", ylabel = j == 1 ? "activator  u" : "")
    band!(ax, x, zeros(length(x)), u; color = (RED, 0.14))
    lines!(ax, x, u; color = RED, linewidth = 7)
    text!(ax, 0.50, 0.92; text = sub, space = :relative, align = (:center, :top),
          fontsize = 30, color = j == 1 ? MID : OXBLOOD, font = :bold)
    xlims!(ax, 0, 1); ylims!(ax, 0, max(2.2, maximum(u) * 1.18))
end
saveboth(fig, "wound_response")

# -----------------------------------------------------------------------------
# 3. History-dependent pattern selection on the same final domain
# -----------------------------------------------------------------------------

# Direct DII selection is shown with a spectrum-like multi-peak profile.  The
# continuation path starts from a localized boundary peak and preserves it as L
# increases.  These curves define the numerical protocol and can be replaced by
# calibrated solver output without changing the poster layout.
Lfinal = 4.0
x = collect(range(0, Lfinal, length = 900))
direct = 0.72 .+ 0.73 .* (0.46 .+ 0.54 .* cos.(2π .* x ./ 1.17)).^4
direct .+= 0.12 .* exp.(-((x .- 3.55) ./ 0.16).^2)
continued = 0.045 .+ 2.25 .* exp.(-(x ./ 0.24).^2)

fig = Figure(size = (1700, 850), backgroundcolor = :white)
ax1 = Axis(fig[1, 1], title = "LARGE DOMAIN FROM THE DII STATE",
           xlabel = "same final domain", ylabel = "activator  u")
lines!(ax1, x, direct; color = BLUE, linewidth = 7)
band!(ax1, x, zeros(length(x)), direct; color = (BLUE, 0.12))
text!(ax1, 0.5, 0.90; text = "small noise  →  several peaks", space = :relative,
      align = (:center, :top), fontsize = 29, color = BLUE, font = :bold)
xlims!(ax1, 0, Lfinal); ylims!(ax1, 0, 2.5)

ax2 = Axis(fig[2, 1], title = "SMALL DOMAIN → GROWTH CONTINUATION",
           xlabel = "same final domain", ylabel = "activator  u")
lines!(ax2, x, continued; color = RED, linewidth = 7)
band!(ax2, x, zeros(length(x)), continued; color = (RED, 0.14))
text!(ax2, 0.5, 0.90; text = "one established peak can persist", space = :relative,
      align = (:center, :top), fontsize = 29, color = OXBLOOD, font = :bold)
xlims!(ax2, 0, Lfinal); ylims!(ax2, 0, 2.5)
rowgap!(fig.layout, 22)
saveboth(fig, "domain_history")

# -----------------------------------------------------------------------------
# 4. Prescribed rho profiles for oriented and anti-oriented grafts
# -----------------------------------------------------------------------------

x = collect(range(0, 1, length = 600))
oriented = 0.20 .+ 0.80 .* x
anti = similar(x)
for (i, z) in enumerate(x)
    anti[i] = z < 0.5 ? 0.20 + 1.6z : 0.20 + 1.6(z - 0.5)
end

fig = Figure(size = (1600, 620), backgroundcolor = :white)
ax = Axis(fig[1, 1], xlabel = "assembled body axis  x", ylabel = "source density  ρ(x)")
lines!(ax, x, oriented; color = TEAL, linewidth = 8, label = "oriented")
lines!(ax, x, anti; color = ORANGE, linewidth = 8, linestyle = :dash,
       label = "anti-oriented")
vlines!(ax, [0.5]; color = (INK, 0.55), linewidth = 3, linestyle = :dot)
text!(ax, 0.5, 0.12; text = "graft junction", align = (:center, :bottom),
      fontsize = 26, color = MID)
axislegend(ax, position = :lt, framevisible = false, labelsize = 27)
xlims!(ax, 0, 1); ylims!(ax, 0, 1.08)
saveboth(fig, "rho_grafts")

# -----------------------------------------------------------------------------
# 5. Dynamic rho: illustrative slow-fast, metastable positional memory
# -----------------------------------------------------------------------------

x = collect(range(0, 1, length = 650))
times = [1.0, 25.0, 250.0, 2500.0]
peakpos = [0.36, 0.36, 0.39, 0.50]
widths = [0.032, 0.046, 0.075, 0.13]
amps = [2.2, 2.05, 1.85, 1.65]

fig = Figure(size = (1700, 820), backgroundcolor = :white)
ax = Axis(fig[1, 1], xlabel = "position  x", ylabel = "activator  u(x,t)",
          title = "FAST PEAK, SLOW REORGANIZATION")
cols = [RED, colorant"#D64A52", colorant"#A75C65", BLUE]
for i in eachindex(times)
    prof = 0.03 .+ amps[i] .* exp.(-((x .- peakpos[i]) ./ widths[i]).^2)
    lines!(ax, x, prof; color = cols[i], linewidth = 6,
           label = "t = $(Int(times[i]))")
end
vlines!(ax, [0.36]; color = TEAL, linewidth = 4, linestyle = :dash)
text!(ax, 0.36, 2.38; text = "inherited ρ maximum", align = (:center, :bottom),
      fontsize = 25, color = TEAL)
axislegend(ax, position = :rt, framevisible = false, labelsize = 24)
xlims!(ax, 0, 1); ylims!(ax, 0, 2.7)

ax2 = Axis(fig[1, 2], xscale = log10, xlabel = "time", ylabel = "peak position",
           title = "METASTABLE ANCHORING")
t = 10 .^ range(0, 4, length = 240)
xpeak = 0.36 .+ 0.14 ./ (1 .+ exp.(-3.2 .* (log10.(t) .- 3.15)))
lines!(ax2, t, xpeak; color = RED, linewidth = 7)
band!(ax2, t, fill(0.35, length(t)), fill(0.37, length(t)); color = (TEAL, 0.13))
hlines!(ax2, [0.36]; color = TEAL, linewidth = 3, linestyle = :dash)
hlines!(ax2, [0.50]; color = BLUE, linewidth = 3, linestyle = :dot)
text!(ax2, 2.0, 0.372; text = "graft memory", fontsize = 24, color = TEAL)
text!(ax2, 9000, 0.505; text = "selected position", fontsize = 24,
      color = BLUE, align = (:right, :bottom))
xlims!(ax2, 1, 1e4); ylims!(ax2, 0.32, 0.54)
colgap!(fig.layout, 55)
saveboth(fig, "dynamic_rho")

println("Poster figures written to: ", OUTDIR)

