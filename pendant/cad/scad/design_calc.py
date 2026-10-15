#!/usr/bin/env python3
"""
design_calc.py -- turn the unknowns of the wall-mounted servo-ring rig into numbers (stdlib only, ESTIMATES, not measurements).

Rig: ring plane parallel to a wall (z = 0, beams travel +z into the room); N arms on a 1/2 inch round-stock ring; the focal point is moved
anywhere in a working volume from Z_MIN to Z_MAX (about 4 feet = 1.22 m) in front of the ring. Each arm = coarse pan/tilt (robotics servos)
+ a 3-axis fibre-tip positioner behind a fixed lens (fine steering by lateral fibre shift, focus by axial fibre shift). Printed: what each
arm must do, what accuracy the geometry demands, and what that implies for the parts. Run:  python3 design_calc.py
"""
from math import atan, atan2, acos, degrees, pi, sqrt, tan

LAM = 633e-9
N_LIST = (13, 18)
PITCH = 0.048                 # m, ring length per arm (servo + swept tube footprint), assumed
Z_MIN, Z_MAX = 0.30, 1.22     # working depth, m (1 ft .. 4 ft)
LAT_HALF_ANGLE = 20.0         # working volume: lateral radius = depth * tan(20 deg)
LENS_F = 0.050                # m, fixed lens focal length per arm (assumed)
BEAM_W = 0.005                # m, beam radius at the lens (1/e^2), 10 mm beam on a 25.4 mm lens (assumed)
SERVO_STEP = 2 * pi / 4096    # rad: XL330-class servo output resolution (4096 pulses/rev, reseller-quoted)
STOCK = 0.0127                # 1/2 inch round stock


def ring_diameter(n, pitch=PITCH):
    return n * pitch / pi


def arm_positions(n, R):
    return [(R * __import__("math").cos(2 * pi * i / n), R * __import__("math").sin(2 * pi * i / n), 0.0) for i in range(n)]


def sweep(n):
    D = ring_diameter(n)
    R = D / 2
    arms = arm_positions(n, R)
    worst_tilt, worst_d, min_d = 0.0, 0.0, 9.0
    for zi in range(0, 11):
        z = Z_MIN + (Z_MAX - Z_MIN) * zi / 10
        lat = z * tan(LAT_HALF_ANGLE * pi / 180)
        for k in range(0, 8):
            a = 2 * pi * k / 8
            for rr in (0.0, lat):
                tx, ty = rr * __import__("math").cos(a), rr * __import__("math").sin(a)
                for (ax, ay, az) in arms:
                    dx, dy, dz = tx - ax, ty - ay, z
                    L = sqrt(dx * dx + dy * dy + dz * dz)
                    worst_tilt = max(worst_tilt, degrees(acos(dz / L)))
                    worst_d, min_d = max(worst_d, L), min(min_d, L)
    return D, R, worst_tilt, min_d, worst_d


def main():
    print("RING SIZE for pitch %.0f mm per arm (1/2 in stock, ring centre-line diameter):" % (PITCH * 1e3))
    for n in N_LIST:
        print(f"  N = {n}: D = {ring_diameter(n)*1e3:6.0f} mm  (R = {ring_diameter(n)*500:5.0f} mm)   circumference {n*PITCH*1e3:.0f} mm")
    print(f"\nWORKING VOLUME: depth {Z_MIN:.2f}..{Z_MAX:.2f} m, lateral radius = depth x tan({LAT_HALF_ANGLE:.0f} deg)")
    for n in N_LIST:
        D, R, wt, dmin, dmax = sweep(n)
        print(f"  N = {n}: worst tilt from the wall normal {wt:5.1f} deg; arm-to-focus distance {dmin:.2f}..{dmax:.2f} m")
    print("\nPER-DISTANCE BEAM FIGURES (diffraction-limited waist w0 = lambda d / (pi W), W = %.1f mm; lens f = %.0f mm):" % (BEAM_W * 1e3, LENS_F * 1e3))
    print("   d (m)   w0 (um)   Rayleigh z_R (mm)   pointing tolerance w0/(4d) (urad)   fibre-tip focus shift f^2/(d-f) (mm)")
    for d in (0.3, 0.6, 0.9, 1.22, 1.5):
        w0 = LAM * d / (pi * BEAM_W)
        zr = pi * w0 * w0 / LAM
        print(f"  {d:6.2f}  {w0*1e6:8.0f}  {zr*1e3:14.0f}   {w0/(4*d)*1e6:30.0f}   {LENS_F**2/(d-LENS_F)*1e3:30.2f}")
    d = Z_MAX
    w0 = LAM * d / (pi * BEAM_W)
    tol = w0 / (4 * d)
    print(f"\nCOARSE SERVO vs REQUIREMENT at {d} m: one servo step = {SERVO_STEP*1e6:.0f} urad (= {degrees(SERVO_STEP):.3f} deg) -> {SERVO_STEP*d*1e3:.2f} mm at the target;")
    print(f"  tolerance w0/(4d) = {tol*1e6:.0f} urad  ->  the servo step is {SERVO_STEP/tol:.0f}x too coarse by itself. A fine stage is REQUIRED.")
    print(f"FINE STAGE (lateral fibre-tip shift behind the lens, angle = shift / f): to cover one servo step needs +-{SERVO_STEP/2*LENS_F*1e3:.3f} mm of shift;")
    print(f"  to resolve {tol/4*1e6:.0f} urad needs {tol/4*LENS_F*1e9:.0f} nm steps: piezo-class, not a hobby actuator.")
    print("\nFOCUS (axial fibre-tip shift): about %.0f mm of travel covers 0.3 m to 1.5 m for f = %.0f mm; resolution needed ~ z_R / 20 at the far end." % (
        (LENS_F ** 2 / (0.3 - LENS_F) - LENS_F ** 2 / (1.5 - LENS_F)) * 1e3, LENS_F * 1e3))
    print("\nPHASE: path from each arm to a point changes by up to ~%.1f m as the point moves: the phase actuator must wrap modulo 2 pi;" % (Z_MAX))
    print("  keeping 96%% of the peak needs about lambda/30 = %.0f nm of path error per arm; mechanical metrology cannot give that over a metre," % (LAM / 30 * 1e9))
    print("  so phase has to be closed on a signal at the focus (fog-lit point -> pinhole photodiode), not set from geometry alone.")
    print("AIR: dn/dT ~ 1e-6 per K, so 1.2 m of path moves %.0f nm per K; a still-air tent and a phase loop of ~1 kHz or better are assumed." % (1.2e-6 * 1e9))
    print("\nPOWER at the test: 13 arms x 75 uW = 0.98 mW total (about class 2); 18 arms x 75 uW = 1.35 mW (check the class: 18 x 75 uW exceeds 1 mW).")


if __name__ == "__main__":
    main()
