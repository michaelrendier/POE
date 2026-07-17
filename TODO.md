# P.O.E. TODO

Active work items, hardware targets, and design decisions.

---

## PENDANT HARDWARE

### [ ] Core CAD — Fixed Geometry (OpenSCAD)

The invariant geometry every pendant must implement. Exact dimensions derived from
coil calculations. Print this and the electronics work. This is the deliverable that
makes open manufacturing real.

**Files to produce:**
- [ ] `pendant/core/coil.scad` — pancake coil with T1–T8 tap positions marked
- [ ] `pendant/core/mcu_footprint.scad` — Pro Micro / ESP32 mounting holes + trace routing
- [ ] `pendant/core/nfc_mount.scad` — PN532 position coaxial with T1
- [ ] `pendant/core/core_assembly.scad` — full core as one importable module
- [ ] `pendant/reference/pendant_v1.scad` — reference body (40 mm OD) showing core usage
- [ ] `pendant/bom/bom_v1.md` — commodity BOM, globally sourceable components only

**Coil geometry — CALCULATED (Mohan et al. 1999, 2026-06-28):**

```
OD = 38mm  ID = 10mm  pitch = 0.8mm  trace = 0.5mm  gap = 0.3mm  turns = 17

Tap       Turns   r_out    L          Target                 C
T_full    17      19mm     3.58 μH    NFC 13.56 MHz          38.5 pF (fixed)
T_full    17      19mm     3.58 μH    AM  530–1700 kHz       2.4–25 nF (variable)
T_full    17      19mm     3.58 μH    SW  1.6–10 MHz         71–2750 pF (switched)
T3         3       7.4mm    95 nH      SW  15–30 MHz          300–1200 pF
T5         5       9.0mm   258 nH      FM  87.5–108 MHz       8.4–12.8 pF (2-cap)

Above 200 MHz: chip antennas required (required L < coil parasitic ~2 nH)
  GPS L1 1575 MHz → 12×12mm ceramic patch (RHCP)
  LTE 700-2600 MHz → wideband chip antenna
  WiFi/BT 2.4 GHz → 2.4 GHz chip antenna
  WiFi 5G → 5 GHz chip antenna
```

Resonant condition at each tap: XL = XC → tan(phase) = 1 → sin = cos → σ = ½.
The coil finds the Riemann balance point by electromagnetic law.

**Remaining antenna work:**
- [ ] Simulate impedance at each tap (QUCS or LTSpice) — confirm 50Ω match
- [ ] Verify with NanoVNA on a wound prototype
- [ ] Design variable/switched capacitor networks for AM and SW bands
- [ ] Design FM 2-cap switch (8.4 pF / 12.8 pF for 108 MHz / 87.5 MHz)
- [ ] SVG trace layout for conductive PLA deposition (coil.scad → SVG export)

**Design principles:**
- OpenSCAD only — parametric, version-controllable, no proprietary CAD software
- All dimensions in mm, all tolerances for FDM printing (not injection moulding)
- Conductive trace routing must be printable without support material
- Core module is importable: `use <core/core_assembly.scad>`

---

### [ ] Reference Pendant v1 — First Printable Unit

Complete, printable, functional pendant using the core module. This is the proof
of concept that open manufacturing works. Everything else follows from here.

**Scope:**
- [ ] Body: structural PLA, 40 mm OD, wearable thickness (≤ 8 mm)
- [ ] Coil: conductive PLA traces, dual-extrusion or insert-print
- [ ] MCU: Pro Micro or ESP32-S3 mini
- [ ] NFC: PN532 breakout, I²C
- [ ] Battery: flat LiPo 100 mAh (fits 40 mm OD × 5 mm)
- [ ] Charging: USB-C pad or wireless Qi coil (separate from antenna coil)
- [ ] Test: all 8 tap frequencies confirmed with antenna analyser or NanoVNA

**Filament stack:**
- Body: PLA (any $20/kg generic spool)
- Traces: Proto-Pasta Conductive PLA or Functionalize F-Electric (~$30–50/spool)
- Flex: TPU 95A for strain relief at MCU and battery connection points

---

### [ ] Community Body Design Protocol

The process for users to submit their own pendant body designs:

- [ ] Document the core module interface: what the body must provide (mounting points, clearances)
- [ ] Write `pendant/community/CONTRIBUTING.md` — how to submit a design
- [ ] Establish naming convention: `pendant/community/[designer]/[design_name].scad`
- [ ] First community design target: non-pendant form factor (ring or wristband)

---

### [ ] Arduino Pro Micro — Pendant Communication Layer

Primary MCU for the pendant. Handles comms routing between:
- RedBlue Engine processor
- All radio modules (BT, WiFi, NFC, RFID, GPS, cellular)
- User devices (phone, laptop, desktop)
- Authentication hardware

**Tasks:**
- [ ] Map all free I/O pins on Pro Micro
- [ ] Assign pins: I²C bus, SPI bus, UART for each radio module
- [ ] Define firmware protocol: SPP bridge between pendant and phone
- [ ] Power management: sleep/wake on BT proximity event
- [ ] HID profile: pendant acts as keyboard/pointing device when needed

---

### [ ] Multi-Tapped Pancake Coil Antenna Design

Single flat spiral coil — one physical structure — covering all required bands via
tap points along the winding. Each tap has a different accumulated inductance L;
paired with a tuning capacitor it resonates at the target frequency.

| Tap | Frequency        | Band              | RF Module             | Use                        |
|-----|-----------------|-------------------|-----------------------|----------------------------|
| T1  | 13.56 MHz        | NFC               | PN532 / RC522         | Auth + Skill Transfer      |
| T2  | 530–1700 kHz     | AM broadcast      | Rectenna              | Passive power harvest      |
| T3  | 87.5–108 MHz     | FM broadcast      | Rectenna              | Passive power harvest      |
| T4  | 700–900 MHz      | LTE low band      | Modem 2 (SIM7600)     | Cellular always-on         |
| T5  | 1575.42 MHz      | GPS L1            | u-blox NEO-6M         | Position context           |
| T6  | 1700–2600 MHz    | LTE mid/high band | Modem 2 (SIM7600)     | Cellular upper bands       |
| T7  | 2.4 GHz          | WiFi 802.11 + BT  | Modem 1 (ESP32 / CM4) | Local comms + BT auth      |
| T8  | 5 GHz            | WiFi 802.11ac/ax  | Modem 1               | High-bandwidth local       |

**Design targets:**
- [ ] Calculate coil geometry: number of turns, inner/outer radius, trace width for pendant dimensions
- [ ] Calculate L at each tap position from spiral inductance formula: L = (r²n²)/(8r+11w) (Wheeler)
- [ ] Select tuning capacitor C at each tap: C = 1/(4π²f²L)
- [ ] Simulate impedance at each tap (LTSpice or QUCS) — confirm 50 Ω match or transformer ratio
- [ ] Design for pendant body: target OD ≤ 40 mm, trace width ≥ 0.3 mm for conductive filament
- [ ] Output: printable SVG for conductive trace deposition, or wind spec for manual coil

**Dual modem targets:**
- [ ] Modem 1 (local): ESP32 or CM4 module — WiFi 2.4/5 GHz + Bluetooth 5.0 on taps T7/T8
- [ ] Modem 2 (wide): SIM7600 or Quectel EC21 — LTE on taps T4/T6; data-only SIM
- [ ] Firmware: Modem 2 always-on at idle; Modem 1 primary when WiFi in range
- [ ] Handoff: no session drop — Modem 2 keeps socket alive while Modem 1 connects/disconnects
- [ ] BT tether path: pendant → BT → phone network (tertiary fallback when both modems unreachable)

---

### [ ] Passive RF Power Harvesting

AM/FM broadcast as passive power source for low-power components:
- [ ] Rectenna circuit design (diode bridge + capacitor storage)
- [ ] Power budget: what can be sustained from ambient RF at indoor levels?
- [ ] Priority load: always-on presence beacon (BT advertisement)

---

## AUTHENTICATION

### [ ] EarPiece Integration (F-SL001A — 11:94:AA:10:05:82)

Bluetooth proximity authentication — user wearing the earpiece = Tier 1 auth present.

**Services available on device:**
- SPP (Serial Port Profile) — 00001101-0000-1000-8000-00805f9b34fb
- Headset — 00001108-0000-1000-8000-00805f9b34fb
- Audio Sink — 0000110b-0000-1000-8000-00805f9b34fb
- HID (Human Interface Device) — 00001124-0000-1000-8000-00805f9b34fb
- Handsfree — 0000111e-0000-1000-8000-00805f9b34fb

**Tasks:**
- [ ] Add F-SL001A to Holcus auth_totp allowed devices list
- [ ] Implement BT proximity check: `hcitool rssi 11:94:AA:10:05:82` → signal strength
  - Signal -65 dBm at enrollment (from EarPiece.txt)
  - Presence threshold: above -80 dBm = user in range
- [ ] Integrate proximity into Tier 1 auth (no TOTP required if earpiece in range)
- [ ] Audio output: Holcus can speak through the earpiece via audio sink
- [ ] HID input: earpiece button presses as Holcus input triggers

---

### [ ] RFID / NFC Smart Card Root Key

Physical root key — the one authentication method that cannot be phished or remotely
compromised. Smart card backup of sedenion field state + private key.

- [ ] Select card form factor (ISO 14443A vs ISO 15693)
- [ ] Define data layout: private key + compressed state snapshot
- [ ] Implement signing protocol for root commands
- [ ] Test with Arduino Pro Micro NFC module (PN532 or similar)

---

### [ ] NFC Skill Transfer

NFC as callosum between Holcus field instances. One tap transfers one skill branch
(compressed second-octonion checkpoint) from pendant to any NFC-capable device.

**Skill transfer spec — [ STUB — specification discussion to follow ]**

> The NDEF record structure, payload encoding, compression, versioning, field
> compatibility check, partial transfer chunking, and security signing protocol
> will be defined here once the skill transfer specification format is decided.

**Implementation targets (post-spec):**
- [ ] Define NDEF record type for skill checkpoint (custom TNF or MIME)
- [ ] Implement checkpoint compression: delta from base.bin only (not full field)
- [ ] Implement field compatibility check before load (version header match)
- [ ] Implement NFC write on pendant side (PN532 via I²C to Pro Micro)
- [ ] Implement NFC read + checkpoint load on phone/laptop side
- [ ] Test: pendant writes Crawford N-S skill → phone Ptolemy loads it → verify vocabulary active
- [ ] Security: sign checkpoint with pendant private key; destination verifies before load

---

### [ ] Fingerprint Sensor

Hardware present (built-in). Linux integration pending. See PtolemyHolcus TODO S8.

---

## VEHICLE INTERFACE

### [ ] VCDS / OBD-II Integration

Connect Holcus diagnostic layer to the actual 2004 VW Passat BEW 1.9 TDI.

**Protocol:**
- Interface: HEX-V2 or HEX-NET (USB to K-line / CAN bridge)
- K-line protocol: ISO 9141-2 / KWP2000 (KWP 1281 for older VAG modules)
- CAN: ISO 15765-4 (for newer modules on BEW)

**Tasks:**
- [ ] Implement KWP1281 reader in Python (no VCDS dependency — open protocol)
- [ ] Map VCDS Function 08 Measuring Blocks → Holcus sensor_read() polling
- [ ] Map VCDS Function 02 DTCs → Holcus fault_scan() output format
- [ ] Live data: RPM, boost, MAF, EGT, injection timing → real OBD PIDs feeding into
  Holcus OBD PID map (0x0C, 0x0B, etc.)
- [ ] Adaptation channel read/write → monad.adapt() integration
- [ ] Log vehicle field state to monad: the TDI teaches the TDI engine about itself

---

## RADIO

### [ ] Cellular Modem

WWAN connectivity for the pendant — Holcus on the network independently of WiFi.

- [ ] Module selection: SIM7600 or Quectel EC21 (USB or UART)
- [ ] SIM: data-only SIM for Holcus communication
- [ ] Integration with Pro Micro via UART AT commands

---

### [ ] GPS

Position awareness for context:
- [ ] Module: u-blox NEO-6M or equivalent
- [ ] Integration: NMEA sentences → location context for Holcus field state

---

## LONG RANGE

### [ ] Holcus Traversing the Internet Autonomously

When the persistent server is live and all Prime Directives are seated:

- [ ] URL traversal: Holcus discovers and reads pages autonomously
  (explicit root-signed enable required each session)
- [ ] Distributed seeding: random text boxes seeded with next lines of code —
  Holcus's code can be reconstructed from the Sedenion Hyperindex without
  physical storage
- [ ] Sedenion Hyperindex as distributed code location — the code lives in the
  field, not on a disk

---

## GAMES / UNIVERSE SIMULATIONS

*From OfflineNotes — long-range applications once the engine is proven:*

- [ ] Minecraft / No Man's Sky universe variant using H_RB as the universe engine
  (100 billion stars in a galaxy is trivial next to the hyperpermutation)
- [ ] No Man's Sky: Ptolemy Class — find Earth in the hyperpermutation
- [ ] EVE Online: Milky Way Galaxy from first principles if Earth's location
  in the hyperpermutation is found
- [ ] Dark life confirmed — the engine predicts life in non-baryonic matter halos

---

## MATHEMATICS / PHYSICS (Engineering TODOs)

- [ ] Formal definition of the two octonians of the sedenion that emerge the Boundary
- [ ] Timescale: galactic resonant cavity → human time frame referential 'stillness'
  (time scale needs to be both into and out of the galactic simulation equation)
- [ ] Bifurcation fractal → windows of order → limit the search space for missing
  variables in an equation (modular math addition = subtraction windows)
- [ ] XOR and (I|O) — if XOR IS Inside-Out, what are the inside-out of public/private
  keys in relation to content/hash? Can the private key cancel itself out in the
  return path of the modular function?
- [ ] Waveform spectral isolation: can spectrum + cepstrum + x-affinities identify
  missing variables from an equation, or speech formulation layer gaps?

---

## NOTES

*"Ptolemy contains the blueprints to 3D print a pendant."*
— This repo is where those blueprints live.

*"The P.O.E. Pendant as a personal AI pendant."*
— Without a RedBlue Engine hardwired silicon processor, 3D printable options
exist to achieve the same result with commodity electronics.

*"A path to a destination intimately defines its return path."*
— The pendant communicates in both directions. Every input channel is also
an output channel. The sedenion handles this natively: ξ(s) = ξ(1-s).
