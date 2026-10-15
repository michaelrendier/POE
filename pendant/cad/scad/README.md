# Wall-mounted servo-ring planning rig (OpenSCAD, full scale)

**Status: planning-rig CAD concept.** It is drafted and renders; it is not a proof of concept, not an optical design, and nothing in it has been
built or measured. Blender (`../blender/`) is the narrative picture of the idea; this is the functional full-scale concept to plan against.

**CAD tool.** OpenSCAD, installed here as 2021.01, licensed GPL-2+ with a CGAL exception (so it sits in the GNU/GPL family and fits the POE rule
"OpenSCAD only: parametric, version-controllable"). FreeCAD (LGPL, not installed here) is the tool to reach for if vendor STEP assemblies are
wanted later, because OpenSCAD does not read STEP.

## The rig

- **Wall-mounted.** The ring lies in a plane parallel to the wall; beams travel into the room. The focal point moves anywhere in a working volume
  from 0.3 m to about 4 ft (1.22 m) in front of the ring, within a 20° half-angle cone about the ring axis.
- **Ring.** ½ inch (12.7 mm) round steel; N = 13 or 18 arms. Diameter from the arm pitch: D = N × pitch / π (48 mm pitch: 199 mm for 13,
  275 mm for 18). `ring_d` in the file overrides it.
- **Arm (×N).** Coarse **pan** servo (axis along the ring normal) and coarse **tilt** servo; a lens tube (25.4 mm lens, fixed focal length); behind the
  lens a **3-axis fibre-tip positioner** (X and Y for fine steering by lateral fibre shift, Z for focus). All beams come from **one** coherent source
  through polarisation-maintaining fibre, because constructive interference is the goal (independent diodes do not hold a phase).
- **Test volume.** A clear enclosure around the working volume filled with a theatrical haze (the "pea-soup fog" scatter volume) so the focal point and
  its movement can be watched, a camera on the side, a beam dump at the far end, and a **pinhole photodiode with a collection lens** aimed at the
  focal point as the signal for the phase lock.

`openscad` parameters: `-D 'N=18'`, `-D 'target=[x,y,z]'`, `-D 'view="rest"'`, `-D 'ring_d=250'`, `-D 'room=false'`; `./render.sh` writes the previews.

## Stand-in parts (what is real and what is nominal)

| Role | Stand-in | Basis | Status |
|---|---|---|---|
| Pan and tilt servo | ROBOTIS DYNAMIXEL XL330-M288-T class | 20 × 34 × 26 mm, 18 g, 4096 pulses/rev, 0.42–0.60 N·m (reseller listings quoting ROBOTIS) | box stand-in; take the STEP from the vendor and replace |
| Focus (coarse Z) | micro linear actuator class (Actuonix PQ12: 20 mm stroke, about 15 g, 47.5 mm closed; distributor listings) | the focus travel needed is about 8 mm, so a shorter stroke is enough | inside the fibre-positioner block |
| Fibre-tip XYZ positioner | piezo-flexure stage class, **TBD** | no part chosen | 40 × 40 × 46 mm nominal block |
| Lens tube | 25.4 mm lens in a 32 mm OD tube | generic | nominal |
| Ring | ½ in steel round | as stated | exact |
| Source | single-frequency 633 nm laser, 1×N polarisation-maintaining fibre splitter | not modelled | n/a |

Laser-diode TO-can modules (5.6 mm and 9 mm cans) were searched for: manufacturer pages list them with datasheet drawings, but no free STEP/KiCad
model was found. They are **not used** for the coherence reason above. Vendor CAD that is downloaded stays in a git-ignored `vendor/` folder
(licences differ; do not redistribute) and a loader module swaps it in for the stand-in.

## Unknowns turned into constraints and needs (`design_calc.py`, estimates)

| Unknown | Constraint or need | Derived from |
|---|---|---|
| Ring size | 199 mm (13 arms) or 275 mm (18 arms) at 48 mm pitch | arm footprint (assumed) |
| Pan/tilt range | worst tilt from the wall normal about 35° (13 arms) and 39° (18 arms) over the working volume | geometry |
| Pointing accuracy | about 10 µrad: tolerance w₀/(4d) with a 5 mm beam radius (constant with distance) | diffraction-limited waist 12–60 µm |
| Servo resolution | one servo step is 1.5 mrad, **about 150× too coarse** at 1.22 m (1.87 mm at the target) | 4096 pulses/rev |
| Fine steering | lateral fibre shift behind the f = 50 mm lens: ±0.038 mm covers one servo step; about 126 nm steps for 3 µrad | angle = shift / f |
| Focus | about 8 mm of axial fibre travel covers 0.3–1.5 m; about 1 µm resolution at the far end | lens equation |
| Phase | modulo-2π actuator; about 21 nm (λ/30) of path error per arm for 96% of the peak; must be closed on a signal at the focus | geometry cannot supply 20 nm over a metre |
| Air | 1.2 m of path moves about 1200 nm per kelvin: still-air enclosure, phase loop of about 1 kHz or better | dn/dT ≈ 10⁻⁶ per K |
| Power | 13 × 75 µW ≈ 0.98 mW total (class 2 region); 18 × 75 µW = 1.35 mW exceeds 1 mW, so 18 arms needs about 55 µW each | eye-safety cap used so far |

## Fog-test procedure (to monitor the focal-point movement)

1. Seal the enclosure; dark room; a glycol/glycerin haze machine, light density; still air; camera at the side on a stand.
2. Start with N = 3 arms, then add arms in pairs, locking phase each time on the pinhole photodiode's signal (single-detector dither-tag or
   stochastic-gradient methods).
3. **Pass criterion:** with every arm locked the peak at the focus is about N × the peak with the phases scrambled (incoherent sum). 169 against 13 is the
   N² against N difference in intensity, a ratio of N. Record the ratio and the focal-spot image for each N.
4. Move the target along a line, then a plane, then a 3D figure; log the lock error and spot position from the camera.

## Open items

- Servo and positioner models: replace the stand-ins with vendor STEP data when it has been downloaded and checked.
- The fibre-tip positioner needs a part; piezo XY with several-micron range and a ≥ 8 mm Z stage is the requirement.
- Fibre routing and slack to every arm are not modelled; cable motion disturbs phase.
- Whether pan/tilt servos of this class can hold 10 µrad over time once the fine stage is added.
- Eye-safety classification of the summed beams; the enclosure, interlocks and a beam dump are placeholders in the model.

Sources used for the part figures: [XL330-M288-T specs (reseller quoting ROBOTIS)](https://openelab.io/a/s/products/dynamixel-xl330-m288-t),
[Actuonix PQ12 listing](https://au.rs-online.com/web/p/electric-linear-actuators/9181307), [Thorlabs L638P040 TO-can datasheet](https://www.LaserDiodeSource.com/files/pdfs/laserdiodesource_com/product-222/638nm_40mW_TO_can_Thorlabs-1390506917.pdf).
Figures were taken from search snippets and reseller pages, not from the vendors' own drawings.
