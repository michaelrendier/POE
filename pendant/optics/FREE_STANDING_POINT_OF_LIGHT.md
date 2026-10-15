# The free-standing point of light — concept and macro-scale mock-up

**Status: CONCEPT. Nothing here has been built or measured.** This page records the design as the author states it, the constraints that are
fixed, the stated working figures, and the questions still open, so that integrated-circuit, nanotechnology and mechanical engineers can start
from one page. The narrative 3D mock-up is `pendant/cad/blender/poe_servo_ring.py` (Blender 4.x, python3); the full-scale planning rig is OpenSCAD in
`pendant/cad/scad/` (wall-mounted ring, working volume to about 4 ft, derived constraints in its README); a Fritzing board map for the electronics
is next.

## The idea

Several weak, individually near-invisible red laser beams, aimed from a ring so that they all pass through one point, are made to arrive there
**in phase**. At that point the fields add (constructive interference): with N equal beams the peak intensity is N² times one beam's, against N
times for incoherent beams. The point can be moved in three dimensions, so that shapes can be traced, by re-aiming every beam
and re-phasing it. It is conceptually close to an optical trap: many beams, one focus. The pendant is the miniaturised form of the same
mechanism; the macro-scale ring is the prototype to build from and against.

## Fixed design constraints (do not budge)

1. **The beams must constructively interfere at the focal point.** All other choices serve this one.
2. **Weak beams.** Each beam is low-amplitude, deep red, non-ionising; the target is class 1–2 per beam with a small total accessible power.
3. **The point is steerable in 3D** by the arms moving independently in unison.
4. **A hard-no field:** no beam ever crosses a cone around the direction toward the wearer's eyes (below).
5. **Macro-scale first, brute force, off-the-shelf hardware**, handed to engineers to miniaturise.

## Mechanism (macro scale)

- **Ring.** ½ inch (12.7 mm) round steel stock bent to a ring, about 160 mm across in the mock-up, carrying **13** arms (an odd number).
- **Three axes per arm.** To aim a beam at a point r and put its waist there an arm needs a direction (pan, tilt) and a distance
  (a slide that moves the lens toward or away from the focus). A planar or one-axis actuator cannot do this. Each arm is therefore a pan/tilt
  gimbal with a focus slide carrying a fibre collimator and lens.
- **Source and distribution.** One coherent source split to all arms (a 633 nm HeNe or a stabilised single-mode red diode, then
  polarisation-maintaining fibre, 1×16 splitter, 13 used). Interference needs one wavelength and one phase reference; independent lasers do not
  hold a fixed phase.
- **Phase.** A fast per-arm phase actuator (piezo fibre stretcher or phase modulator) locked at the focus (dither-tag methods such as LOCSET).
  Stated working tolerance: λ/30 (≈20 nm) of path per arm keeps ≈96% of the peak (simulation, plane-wave model).
- **Pointing.** Coarse stage plus fine stage per axis; the target is about 50 µrad at a 100 mm lens-to-focus distance, which a stepper with a
  fine-pitch screw and a lever (≈2 µrad per microstep) can resolve, closed by a camera on the focus.
- **Control.** A real-time controller computes each arm's pan, tilt, slide and phase from the target position; a separate safety processor
  checks every beam direction against the hard-no field and removes the laser power on any violation or lost heartbeat.
- **Environment.** Air changes path length by about 100 nm per kelvin over 10 cm, so the prototype lives in a sealed or still enclosure and the phase loop absorbs the rest.

## Stated working figures (author's; unverified)

633 nm · 13 arms · about 75 µW per arm (about 1 mW total accessible, roughly class 2) · lens-to-focus 100 mm · beam waist about 20 µm ·
cone half-angle about 20–25° · arm spacing about 38 mm on an 80 mm-radius ring. The mock-up uses these as annotations and geometry; Blender draws
geometry, not optics.

## The hard-no field

The pendant frame has a fixed "toward the wearer's eyes" axis. A cone of **45° half-angle** around it is forbidden: no beam direction, and no
point of any beam beyond the housing, may lie inside it (the idea is the shoulder-launcher back-blast area: a defined volume that is always
clear). It is enforced in hardware, independent of the main controller:

- mechanical stops limit every arm to the allowed envelope;
- a separate safety microcontroller reads each arm's encoders, computes each beam's direction, and cuts the laser (shutter or fast kill) on
  any violation or on loss of its heartbeat;
- an IMU removes the beams when the pendant is tilted out of its allowed attitude;
- the beams continue past the focus and are caught by a beam dump or baffle;
- worn forward-out, away from the face; on a bench or wall it points away from the user;
- **intended safety engineering (later):** a small convolutional network tracking eyes so that the beams steer clear of light entering them at any angle.

In the mock-up the check runs over the whole animation: smallest angle between any beam and the wearer axis, rays inside the cone, carriage
travel, and lens-to-lens spacing (printed when the script runs).

## What the mock-up contains

Steel ring and chest plate; 13 arms, each with base, pan disc, yoke, tilt trunnion, rail, carriage, collimator, lens and beam; fibre leads to a
1×16 splitter, the HeNe and a controller board behind the plate; the focal point with its own light; the beams continuing to a beam dump; the
45° cone; a schematic head with eyes; the copper pancake coil with tap markers; named lights, four cameras (one with the depth-of-field aperture)
and a 120-frame animation in which the focal point traces a 3D figure while all 13 arms move.

## Open questions (stated plainly)

- **Visibility of the point.** In the design there is no scattering medium. Rayleigh scattering from the air in the bright region is very
  small: a rough estimate (Rayleigh coefficient taken from memory, needle about 120 µm × 1 µm²) gives about 10⁻¹⁴ W from the focus at 75 µW per arm,
  against about 10⁻⁹ W from the 13 beam paths; see `ContextPlease/claude/scratchpad/2026-10-14_poe_servo_ring/`. Whether the point can be seen
  without a scatterer, and what would make it visible, is the research question this prototype exists to answer. Instruments (a pinhole
  photodiode or a camera at the focus) measure the amplitude directly without needing visibility.
- **Coherence over 13 arms, with moving cables:** fibre motion disturbs phase; slack, slow motion and the phase loop have to be demonstrated.
- **Moving the focus without a detector at the new point:** calibration at a grid of points plus a locked reference point, with geometry
  feed-forward; accuracy depends on the arms' position sensing.
- **Rival maxima:** with 13 beams the pattern has secondary maxima near the peak (about 40% at a few microns off axis in a plane-wave estimate).
- **Eye-safety classification of the summed beams** (all beams enter the pupil together at the focus) needs a formal assessment.
- **The miniaturised form:** an integrated optical phased array or chip-scale phase-locked source; aperture and numerical aperture bound the focal
  spot and depth. This is for the integrated-circuit and nanotechnology engineers.

## Prior work to read (not downloaded by the author or the assistant)

Coherent beam combining and tiled-aperture phasing (T. Y. Fan, IEEE J. Sel. Top. Quantum Electron. 2005; LOCSET, Shay et al.); optical traps and
the photophoretic-trap volumetric display (Smalley et al., Nature 2018); femtosecond-plasma aerial graphics (Ochiai et al., ACM TOG 2016). Cited
from memory; to be checked against the papers.
