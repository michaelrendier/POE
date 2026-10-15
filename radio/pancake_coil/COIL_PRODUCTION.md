# Pancake coil — production guide (copper first; printed conductive PLA in Appendix A)

**Status: DRAFT design guide.** Nothing here has been wound, etched or measured. Every number marked *estimate* comes from `coil_design.py`
(run it: `python3 coil_design.py`, `--svg coil.svg` for the artwork). Measurement on a real sample, with a NanoVNA, decides every one of them.
Replaces the single-formula inductances and the conductive-PLA assumption in the earlier primer (see section 2 and Appendix A).

## 1. What the coil must do

One flat spiral, several uses: **NFC** (13.56 MHz, authentication and skill transfer), **passive RF harvest** (AM and FM broadcast into a rectenna),
**shortwave listening**, and room for the **wireless-charging** receiver. Cellular, GPS, WiFi and Bluetooth stay on chip antennas (above about
200 MHz the coil is a transmission line, not a lumped inductor). All the uses share one physical structure, so every design decision below is a
trade between them.

Geometry (reference core): 17 turns, pitch 0.8 mm (trace 0.5 mm, gap 0.3 mm), innermost radius 5 mm → OD 37.2 mm (nominal 38). Trace length 1.26 m.

## 2. The numbers (estimates)

| tap | turns | L, earlier formula | L, current-sheet (Mohan 1999) | C for the target |
|---|---|---|---|---|
| whole coil (17) | 17 | 3.5 µH | **6.5 µH** | 21 pF at 13.56 MHz |
| NFC loop = outer 5 turns | 5 | 0.8 µH | **1.6 µH** | 88 pF at 13.56 MHz |
| FM tap = inner 5 turns | 5 | 258 nH | **477 nH** | 5.5 pF at 98 MHz |
| SW-high tap = inner 3 turns | 3 | 95 nH | **179 nH** | 293 pF at 22 MHz |

The earlier inductances came from `μ₀ n² d_avg / (1 + 2.46 ρ)` with no leading constant; the current-sheet expansion for a circular spiral
(coefficients 1.00, 2.46, 0, 0.20) gives about 1.8× more. The first measurement you make (section 6) decides which is right; build the
capacitor networks as trimmable until it does.

**Self-resonance (estimate).** Parasitic capacitance between turns of 2–5 pF (assumed) puts the whole coil's self-resonance at about 28–44 MHz.
Above that the whole coil is not an inductor. FM must therefore use the inner taps; the full coil serves NFC, AM and shortwave only.

**Skin depth** in copper: 18 µm at 13.56 MHz, 6.7 µm at 98 MHz. A 35 µm (1 oz) foil is about two skin depths thick at NFC, ample.

**Q.** Copper foil, 1 oz: R_dc ≈ 1.2 Ω, X_L ≈ 550 Ω at 13.56 MHz → Q ≈ 450 before proximity and AC losses (real Q will be well below that,
perhaps 50–150). That is *too high* for NFC (Q of roughly 10–30 is wanted so the sidebands pass): add a damping resistor in the NFC branch.
High Q is wanted for AM/FM/SW harvest.

## 3. Copper design A — etched or PCB spiral (recommended first build)

1. **Artwork.** `python3 coil_design.py --svg coil.svg` writes the spiral and the tap pad positions (centre start, inner 3, inner 5, outer 5,
   outer end). Import into a PCB tool (KiCad) as a polyline with 0.5 mm track width, or draw it with the tool's spiral plug-in.
2. **Stack-up.** 2-layer, FR-4 0.8 mm, 1 oz copper both sides, ENIG finish. Spiral on the top layer. The inner end needs an underpass: a via at the
   centre, a short trace on the bottom layer out to the edge, a second via to a pad. Keep the underpass off the turns (it adds capacitance).
3. **Taps.** Each tap is a small pad on the track at the specified turn, with a 0.3 mm neck so it does not add a stub. Route each tap to its own
   pad on the bottom layer through a via placed *in* the pad, short leads. Unused taps are left open; they load the used section (section 5).
4. **Keep-outs.** No ground plane or copper pour under or within 5 mm of the coil (eddy currents lower L and Q). If a shield is needed, use a
   ferrite sheet behind the coil (section 7), not copper.
5. **Order.** 5 boards, with a 6th artwork that has only the whole coil for a control. Request controlled impedance off (not needed).
6. **Tuning parts.** C0G/NP0 ceramics (1% where available) and trimmer capacitors: 2–10 pF at FM, 20–60 pF trimmer at NFC. X7R and Y5V drift
   and have voltage and temperature coefficients that detune a high-Q circuit.

## 4. Copper design B — wound wire on a printed former

For a prototype before ordering boards: 0.40 mm enamelled copper wire (26 AWG) wound in a spiral groove printed in the body with 0.8 mm
pitch, ends pulled through holes; each tap is a short soldered pigtail at the right turn (scrape the enamel, tin, solder). Glue (cyanoacrylate)
every few turns so the pitch does not move: pitch changes inductance. Wire has lower resistance than foil at these frequencies and the form of the
spiral stays an Archimedean spiral, which the formula assumes.

## 5. How the taps really behave (read before trusting the band table)

The earlier text says each tap is "always live" with no switching. A tapped single winding is not several independent coils: the turns beyond a
tap are still connected, open at their far end, and act as a lossy stub that detunes the used section and has its own self-resonance. At a
frequency near that stub's resonance the tap behaves badly. So, for **each** tap, measure with the others left open, then with each connected
to its real load, and expect to retune. Where a band needs a clean response (NFC), a dedicated loop of the outer turns is better than the whole
spiral tapped, because the reader chip is designed for a coil of roughly 1–3 µH.

## 6. Measuring and tuning (NanoVNA)

1. Calibrate (open/short/load) at the SMA end of the test lead, and use the shortest possible fixture.
2. **L:** one-port S11 across the tap and ground; with a small known capacitor (e.g. 47 pF C0G) the self-resonance in the S11 dip gives
   L = 1/((2πf)²C). Repeat with a second capacitor; the two results should agree, and the difference gives the parasitic capacitance.
3. **Self-resonance:** open circuit, find the first impedance peak; compare with section 2.
4. **Q:** loosely couple a small pickup loop and read the –3 dB bandwidth: Q = f₀ / Δf. Q is badly corrupted by tight coupling, so keep the
   pickup far enough that the dip is shallow.
5. **Tune:** adjust the trimmer until the resonance sits on the target (13.56 MHz; 88 MHz and 108 MHz for the FM edges; broadcast centres for AM).
6. **Record** L, C, f₀, Q per tap in a table and commit it with the board revision.

## 7. NFC, harvesting and wireless charging

- **NFC.** Use the outer 5 turns as the loop (estimate 1.6 µH) with the reader's recommended matching network (EMC filter and tuning capacitors
  from the chip vendor's reference design: use their values as the starting point, then trim on the VNA). Aim for Q about 10–30 with a damping
  resistor; check read range with a real card.
- **Passive harvest.** AM and FM taps feed a Schottky voltage-doubler (a zero-bias RF Schottky diode such as the SMS7630 class) and a
  storage capacitor, followed by a nano-power boost/charger IC for the battery (BQ25570 class). Expect microwatts (the earlier estimate is
  2–50 µW); it keeps a presence beacon alive and does not run the laser display. Measure real yield before designing around it.
- **Wireless charging.** Qi works near 100–200 kHz with a receiver coil of about 6–10 µH on a ferrite sheet; the whole spiral would resonate with
  about 240 nF at 127 kHz. In phones the Qi coil and the NFC loop are separate loops stacked on one ferrite sheet; do the same. A Qi receiver
  IC (BQ51013B class) sits on the Qi coil's own terminals.
- **Ferrite.** A thin ferrite sheet behind the coils (needed with any metal in the pendant, including the battery) raises L and the
  field strength; its permeability and loss at 13.56 MHz must be chosen for that band. The coil must be re-measured with it in place.

## 8. Quality checks before calling a coil good

DC resistance of the whole coil; L by two capacitors; SRF; Q by bandwidth; NFC read range; AM and FM harvest yield measured with a
known field if possible; a repeat on a second board to see the spread. Keep the numbers with the artwork revision.

## Appendix A — printed conductive PLA (secondary; prototype and former only)

The reference core was written for a coil printed in conductive PLA. With the numbers available the printed coil is a poor RF component:

- **Resistance.** With an assumed volume resistivity of about 0.75 Ω·cm (conductive PLA class, from memory; take it from the datasheet of the
  filament actually used) a 0.5 × 0.2 mm trace 1.26 m long has R ≈ 90 kΩ, against X_L ≈ 550 Ω at 13.56 MHz: **Q ≈ 0.006.** At 0.4 mm layer
  height, Q ≈ 0.012. A coil with a Q far below 1 does not resonate; it is a resistor. The estimate of rectenna yield and of NFC performance
  assumes a working coil and does not hold for the printed one. Even a 100× better filament leaves Q below 1.
- **Variation from the printing process.** Resistance depends on the filament lot, nozzle temperature, layer height, flow and bead overlap. A
  weld-like seam pattern between beads (infill direction, perimeter overlap, seams where a loop closes) makes the resistance, and so the loss and
  the inter-turn capacitance, different from print to print and along the same trace. Single-line perimeters (no infill), one print orientation,
  constant temperature and a fixed filament lot reduce it but do not remove it.
- **What the printed version is good for.** (1) Checking the geometry and the tap pad positions before ordering copper; (2) a former and a
  holder for wound wire; (3) DC and low-frequency traces; (4) a way to compare print settings by measuring DC resistance of test coupons.
- **If a printed coil must carry RF.** Plate it: electroplating copper onto conductive filament is a known technique; nickel/copper
  conductive paint or copper tape over the printed spiral lowers R by orders of magnitude. After plating the coil must be measured again; the
  plated layer, not the PLA, sets Q. This is the only route by which "print it and it works" can hold for the RF coil.
- **Measure before trusting:** four-wire DC resistance of a printed test trace of known length; then use the same R in
  `coil_design.py` (edit the resistivity line) to see Q.
