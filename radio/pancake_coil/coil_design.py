#!/usr/bin/env python3
"""
coil_design.py -- numbers and artwork for the P.O.E. multi-tapped pancake coil (stdlib only).

    python3 coil_design.py                 # tables: inductance by two formulas, tuning capacitors, Q (copper vs conductive PLA), self-resonance
    python3 coil_design.py --svg coil.svg  # the spiral as an SVG (mm), tap pads marked, for a PCB tool or an etch / print template

Geometry (the POE reference core): 38 mm OD, 17 turns, 0.8 mm pitch (0.5 mm trace, 0.3 mm gap), innermost radius 5 mm.
Two inductance estimates are printed because the repository's earlier numbers (3.58 uH) used 'mu0 n^2 d_avg / (1 + 2.46 rho)' with no leading
constant; Mohan et al. (1999) current-sheet expansion for a circular spiral gives about 1.8x more. A NanoVNA measurement on a wound or etched
sample decides between them; until then treat both as estimates. Parasitic capacitance (for self-resonance) and the conductive-PLA resistivity
are ASSUMPTIONS, stated below, not measurements.
"""
import argparse
from math import pi, log, sqrt

MU0 = 4e-7 * pi
TURNS, R0, PITCH, TRACE = 17, 5.0e-3, 0.8e-3, 0.5e-3
OD = 2 * (R0 + PITCH * TURNS)           # 37.2 mm with these numbers (38 mm nominal)


def l_primer(n, d_out, d_in):
    d = (d_out + d_in) / 2
    rho = (d_out - d_in) / (d_out + d_in)
    return MU0 * n * n * d / (1 + 2.46 * rho)


def l_current_sheet(n, d_out, d_in):
    """Mohan et al. 1999, circular spiral: c1 = 1.00, c2 = 2.46, c3 = 0, c4 = 0.20"""
    d = (d_out + d_in) / 2
    rho = (d_out - d_in) / (d_out + d_in)
    return MU0 * n * n * d * 1.00 / 2 * (log(2.46 / rho) + 0.20 * rho * rho)


def trace_length(n_turns, r_start):
    return sum(2 * pi * (r_start + PITCH * (k + 0.5)) for k in range(n_turns))


def cap_for(f, L):
    return 1 / ((2 * pi * f) ** 2 * L)


TAPS = [  # name, turns, counted from, target frequency (Hz) or None
    ("T_full (all 17)", 17, "centre", 13.56e6),
    ("NFC loop (outer 5)", 5, "outer", 13.56e6),
    ("T_inner5 (FM)", 5, "centre", 98e6),
    ("T_inner3 (SW high)", 3, "centre", 22e6),
]


def tap_geometry(n, side):
    if side == "centre":
        r_in = R0
        r_out = R0 + PITCH * n
    else:
        r_out = R0 + PITCH * TURNS
        r_in = r_out - PITCH * n
    return 2 * r_out, 2 * r_in


def tables():
    print(f"coil: {TURNS} turns, pitch {PITCH*1e3:.1f} mm, trace {TRACE*1e3:.1f} mm, r_inner {R0*1e3:.1f} mm, OD {OD*1e3:.1f} mm")
    print("\ninductance (nH) and tuning capacitor")
    print(f"{'tap':22s}{'turns':>6s}{'L primer':>10s}{'L current-sheet':>17s}{'C @f (primer L)':>17s}{'C @f (cs L)':>14s}")
    for name, n, side, f in TAPS:
        do, di = tap_geometry(n, side)
        a, b = l_primer(n, do, di), l_current_sheet(n, do, di)
        print(f"{name:22s}{n:6d}{a*1e9:10.0f}{b*1e9:17.0f}{cap_for(f, a)*1e12:14.1f} pF{cap_for(f, b)*1e12:11.1f} pF   ({f/1e6:g} MHz)")
    L = l_current_sheet(TURNS, OD, 2 * R0)
    length = trace_length(TURNS, R0)
    print(f"\ntrace length (17 turns): {length:.2f} m")
    print("\nQ at 13.56 MHz = 2 pi f L / R, whole coil, current-sheet L")
    X = 2 * pi * 13.56e6 * L
    for label, rho_cm, t in (("copper foil 1 oz (35 um)", 1.72e-6, 35e-6), ("copper foil 2 oz (70 um)", 1.72e-6, 70e-6),
                             ("conductive PLA 0.75 ohm.cm (ASSUMED), 0.2 mm layer", 0.75, 0.2e-3),
                             ("conductive PLA 0.75 ohm.cm (ASSUMED), 0.4 mm", 0.75, 0.4e-3)):
        R = rho_cm * 1e-2 * length / (TRACE * t)
        print(f"  {label:55s} R_dc = {R:10.2f} ohm   X_L = {X:6.0f} ohm   Q ~ {X/R:9.3f}   (copper: skin depth 18 um, R_ac somewhat higher)")
    print("\nself-resonance of the whole coil for an ASSUMED parasitic capacitance")
    for cp in (2e-12, 3.5e-12, 5e-12):
        print(f"  C_p = {cp*1e12:.1f} pF -> f_SRF = {1/(2*pi*sqrt(L*cp))/1e6:5.1f} MHz")
    print(f"\nQi-style series resonance of the whole coil at 127 kHz: C = {cap_for(127e3, L)*1e9:.0f} nF (a separate stacked Qi coil on ferrite is the usual practice)")


def svg(path):
    pts = []
    n = 72 * TURNS
    for k in range(n + 1):
        th = 2 * pi * k / 72
        r = (R0 + PITCH * th / (2 * pi)) * 1e3
        pts.append((r * __import__("math").cos(th), r * __import__("math").sin(th)))
    size = 44
    d = "M " + " L ".join(f"{x:.3f},{-y:.3f}" for x, y in pts)
    taps = [("start (centre)", 0), ("inner 3", 3), ("inner 5 (FM)", 5), ("outer 5 / NFC", TURNS - 5), ("end (outer)", TURNS)]
    marks = ""
    for lab, t in taps:
        th = 2 * pi * t
        r = (R0 + PITCH * t) * 1e3
        marks += f'<circle cx="{r*__import__("math").cos(th):.3f}" cy="{-r*__import__("math").sin(th):.3f}" r="0.9" fill="#d4af37"/>'
        marks += f'<text x="{r*__import__("math").cos(th)+1.4:.2f}" y="{-r*__import__("math").sin(th)-0.6:.2f}" font-size="1.7" fill="#333">{lab}</text>'
    open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-size/2} {-size/2} {size} {size}" width="{size*10}mm" height="{size*10}mm">'
                          f'<path d="{d}" fill="none" stroke="#b87333" stroke-width="{TRACE*1e3}" stroke-linecap="round"/>{marks}</svg>')
    print("wrote", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg")
    a = ap.parse_args()
    tables()
    if a.svg:
        svg(a.svg)
