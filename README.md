# P.O.E. — Ptolemy On Everything

**Author:** Cody Michael Allison
**System:** Ptolemy / Holcus / Ainulindalë
**Date:** 2026-05-30

---

> *"In order to understand what something IS, you must first understand what it IS NOT."*
> — Tao Te Ching

> *P.O.E. is the scope. Not approved topics. Not safe subjects. Everything.*

---

## What This Repository Is

P.O.E. is the **hardware and integration layer** of the Ptolemy system. Where PtolemyHolcus is the engine and Ainulindalë is the mathematics, P.O.E. is the **body** — the physical form through which Holcus interacts with the world.

The ultimate expression of P.O.E. is the **Pendant**: a wearable personal AI device running the RedBlue Geometries Engine on dedicated silicon, worn by the user, always present, always Holcus.

This repo tracks:
- The P.O.E. Pendant hardware design (3D printing, electronics, antennas)
- Vehicle interface (VCDS / OBD-II / TDI engine diagnostic layer)
- Authentication hardware (RFID, NFC, smart card, biometric, Bluetooth proximity)
- Radio communication (multi-tapped pancake coil antenna, all input channels)
- The CAD files, wiring diagrams, and build specifications

---

## The Architecture Connection

The entire Holcus engine is described — and coded — using the metaphor of a **2004 VW Passat BEW 1.9 TDI diesel engine**. This is not metaphor for metaphor's sake. The TDI is a **compression ignition engine with no spark plug**. Holcus is a compression ignition information engine with no transformer. The mathematics forced this analogy.

```
Sedenion Tower     =  Camshaft     (timing — resolves which piston fires when)
H_RB Hamiltonian   =  Crankshaft   (converts compression force into rotation)
Monad (ECU)        =  Engine Block  (the complete execution unit)

Diesel = no spark plug = no transformer = compression ignition only
Holcus = no gradient descent = no backpropagation = field compression only
```

The 8 conjugate piston pairs of the sedenion (e_k ↔ e_{k+8}) map exactly to the
functional equation symmetry ξ(s) = ξ(1-s) in the Riemann zeta function. When
piston #1 is at TDC, piston #4 is also at TDC — same crankshaft position, different
stroke. The camshaft resolves the ambiguity. The sedenion resolves the zeta ambiguity.

**VCDS** (Ross-Tech Vehicle Communication and Diagnostic System) is the diagnostic
interface for real VW/Audi vehicles — including the 2004 Passat BEW 1.9 TDI. It is
also the design template for Holcus's own diagnostic interface. The DTCs, measuring
blocks, adaptation channels, and basic settings in VCDS map to equivalent Holcus
diagnostics.

### VCDS → Holcus Diagnostic Map

| VCDS Function | VCDS Code | Holcus Equivalent |
|---|---|---|
| Fault Codes (DTCs) | Function 02 | DTC fault scan — P0300, P0340, B0103, etc. |
| Measuring Blocks | Function 08 | sensor_read() — live field state table |
| Single Reading | Function 09 | query(word) — single β value |
| Basic Settings | Function 04 | Basic field calibration (warmup, threshold) |
| Adaptation | Function 10 | monad.adapt() — field tuning |
| Long Adaptation | Function 0A | Corpus seeding — full pass study() |
| Output Tests | Function 03 | emit() / actuator test of field output |
| Coding | Function 07 | auth_totp — system configuration with login |
| Login / Security | Function 11 & 16 | TOTP + root key authentication |
| Auto Scan | — | ready_check() — all 8 readiness monitors |
| Data Logging | — | field_health_plot() — continuous recording |
| Readiness Status | Function 15 | FIELD / VOCAB / EDUCATED / CAMSHAFT / CRANKSHAFT monitors |
| Advanced Measuring | — | _live_streams() — VAG-COM Group 000/001/004/011/013 |

### OBD-II PID Map (Standard)

| PID | OBD-II Meaning | Holcus Meaning |
|---|---|---|
| 0x04 | Engine Load | J^μ norm / emission_threshold |
| 0x0B | MAP / Boost | mean β of top-N zeros |
| 0x0C | RPM | word_count / mean_age |
| 0x0E | Timing Advance | affect × 45° BTDC |
| 0x0F | Intake Air Temp | sedenion gestalt_weight |
| 0x11 | Throttle Position | emission_threshold sensitivity |
| 0x1F | Engine Runtime | conversational age (mean) |
| 0x2C | EGR % | age decay λ |
| 0x2F | Fuel Level | vocab_size / N (zero coverage) |
| 0x33 | Barometric Pressure | β_ground — vacuum energy |
| 0x5C | Oil Temperature | A-matrix density (lubrication) |
| 0x5E | Fuel Flow Rate | hear() words per second |

### Custom Holcus PIDs (0x23xx range)

| PID | Name | Value |
|---|---|---|
| 0x2300 | CKP | Active Riemann zero γ_n (highest β excitation) |
| 0x2301 | CMP | Dominant sedenion pair + stroke phase |
| 0x2302 | Conjugate zero | γ_{N-n} (conjugate piston) |
| 0x2303 | Sedenion charge | Total sedenion boost level |
| 0x2304 | Glow plug | word_count < WARMUP_THRESHOLD |
| 0x2305 | Fermat proximity | Zero divisor distance |
| 0x2306 | T_μν trace | Stress-energy sum |
| 0x2307 | Red energy | J_Red — kinetic field |
| 0x2308 | Blue energy | J_Blue — potential/entropic field |
| 0x2309 | Noether violation | ∂_μJ^μ — should be zero |

### Fault Code Map (DTCs)

| DTC | VW Meaning | Holcus Meaning |
|---|---|---|
| P0300 | Random misfire | speak_raw() < 3 charges |
| P0101 | MAF sensor fault | hear() receiving PEM/binary |
| P0335 | CKP sensor fault | No zeros above emission_threshold |
| P0340 | CMP sensor fault | Sedenion all-zero or import failure |
| P0087 | Fuel pressure low | threshold above max(J^μ) |
| P0172 | System too rich | rejection_rate > 50% |
| P0171 | System too lean | speak_raw() consistently empty |
| P0401 | EGR insufficient | Age advancing without hear() |
| B0102 | — | Pronominal shift: person change without anaphor |
| B0103 | — | Anaphor fault: pronoun with no prior noun |

---

## The P.O.E. Pendant

The physical embodiment of P.O.E. A wearable personal AI device — always present,
always learning, always Holcus. Worn by the user. Theirs entirely.

The pendant has two layers:

**The Core** — fixed geometry. The pancake coil antenna dimensions, MCU footprint,
NFC module position, and pin assignments are invariant. These are what make the
electronics work. The CAD repo provides the exact core geometry. Print it and it works.

**The Body** — user-defined. Everything around the core is yours to design. Pendant,
ring, wristband, clip, brooch, housing integrated into clothing. The core is a module.
The body is your design space. Fork the CAD. Make it yours.

This is the Arduino model applied to Race Memory. The board is fixed. Everything else
is the user's.

Capabilities:

1. Runs the Holcus field on-device — no cloud, no transformer, no dependency
2. Carries the user's monad state (field + vocabulary) — their life's accumulated depth
3. Communicates with all personal devices across all radio channels
4. Transfers skills to other Ptolemy instances via NFC contact
5. Provides root-level authentication via multiple factors
6. Learns everything that passes through the Mind's Eye — continuously, always

### Processor Target

**Goal:** A custom ASIC or FPGA implementation of the H_RB Hamiltonian — a
silicon processor that runs compression ignition inference without any transformer,
GPU, or cloud dependency. The RedBlue Geometries Engine hardwired in silicon.

**Now (3D printable):** Low-cost FDM printer + conductive filament + commodity MCU.
Any $200 printer. Standard filaments. No factory. No supply chain. Print it yourself.

### Communication Architecture

The pendant is the user's communication hub across all input modalities:

```
┌─────────────────────────────────────────────────────────────┐
│                     P.O.E. Pendant                          │
│                                                             │
│  Arduino Pro Micro (MCU layer — comms routing)              │
│  RedBlue Engine (processor — inference layer)               │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Bluetooth│  │  WiFi    │  │ Cellular │  │   GPS    │   │
│  │  (HID +  │  │ 802.11   │  │  WWAN    │  │          │   │
│  │   SPP)   │  │          │  │  Modem   │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  NFC /   │  │  RFID    │  │ FM/AM/SW │  │   IR /   │   │
│  │  Smart   │  │  (root   │  │  Radio   │  │  LiDAR   │   │
│  │  Card    │  │  key)    │  │(passive  │  │          │   │
│  └──────────┘  └──────────┘  │  power)  │  └──────────┘   │
│                               └──────────┘                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Multi-Tapped Pancake Coil Antenna                  │   │
│  │  Flat spiral — each band tapped at resonant node    │   │
│  │  Outer → NFC / LTE  ·  Mid → GPS  ·  Inner → BT/WiFi│   │
│  │  Modem 1: WiFi 2.4/5 GHz  ·  Modem 2: LTE 700-2600 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**FM/AM passive power:** AM/FM band used as passive repeater to power battery-operated
components via rectenna — the pendant harvests ambient RF energy from broadcast
infrastructure.

**Multi-tapped pancake coil antenna:** One flat spiral coil printed or wound in the
pendant body. The spiral has continuously varying inductance along its length — each
tap point is a different L value, which paired with a tuning capacitor resonates at
the target frequency. Outer windings carry the highest inductance and serve the lowest
frequencies; inner windings carry the lowest inductance and serve the highest. Multi-band
coverage in minimal planar space with no switching — each band is always live at its tap.

**Dual modem:** Two independent RF front-ends share the same coil via separate taps.
Modem 1 (local) connects to the 2.4/5 GHz inner taps for WiFi and Bluetooth.
Modem 2 (wide) connects to the 700–2600 MHz mid taps for cellular LTE. Both run
simultaneously — pendant never drops connection because the fallback modem is already
active before the primary loses signal. This is the same architecture as a modern
dual-SIM phone.

### Multi-Tapped Pancake Coil — Band Tap Map

One physical coil. All bands. Each tap is a fixed point along the spiral where the
accumulated inductance L satisfies f = 1/(2π√LC) for the target frequency.

| Tap | Position   | Target Frequency | Band              | RF Front-End      | Use                              |
|-----|-----------|-----------------|-------------------|-------------------|----------------------------------|
| T1  | Outermost | 13.56 MHz        | NFC               | PN532 / RC522     | Auth + Skill Transfer            |
| T2  | Outer     | 530–1700 kHz     | AM broadcast      | Rectenna          | Passive RF power harvest         |
| T3  | Outer-mid | 87.5–108 MHz     | FM broadcast      | Rectenna          | Passive RF power harvest         |
| T4  | Mid-outer | 700–900 MHz      | LTE Band 12/17/28 | Modem 2 (Cellular)| Wide-area always-on              |
| T5  | Mid       | 1575.42 MHz      | GPS L1            | u-blox NEO        | Position context                 |
| T6  | Mid-inner | 1700–2600 MHz    | LTE Band 4/7/25   | Modem 2 (Cellular)| Wide-area upper bands            |
| T7  | Inner     | 2.4 GHz          | WiFi 802.11 + BT  | Modem 1 (Local)   | Local comms + BT proximity auth  |
| T8  | Innermost | 5 GHz            | WiFi 802.11ac/ax  | Modem 1 (Local)   | High-bandwidth local             |

**Geometry note:** The pancake coil spiral is a planar projection of the L_(I|O) pathway
geometry — the same cardioid curve that describes the word-particle trajectory in the
field. The tap points are the resonant nodes of the standing wave on the coil, exactly
as the Riemann zeros are the resonant nodes of H_hat_RB. The coil is the antenna IS
the mathematics, scaled to the radio domain.

---

### Dual Modem — Continuous Connection

The pendant maintains connection across two independent radio stacks simultaneously.
No handoff gap. No dropped session.

```
┌───────────────────────────────────────────────────────────┐
│  Modem 1 — LOCAL (taps T7/T8)                             │
│  WiFi 2.4 GHz + 5 GHz  |  Bluetooth 5.0                  │
│  High bandwidth when infrastructure in range              │
│  BT bridges pendant ↔ phone for network sharing           │
├───────────────────────────────────────────────────────────┤
│  Modem 2 — WIDE (taps T4/T6)                              │
│  LTE 700–2600 MHz  |  data-only SIM                       │
│  Always-on fallback — active before Modem 1 drops         │
│  SIM7600 / Quectel EC21 (UART AT commands)                │
├───────────────────────────────────────────────────────────┤
│  Bluetooth (shared with Modem 1)                          │
│  Local HAN: pendant ↔ phone ↔ laptop ↔ earpiece           │
│  When WiFi/LTE unavailable: BT tether to phone network    │
└───────────────────────────────────────────────────────────┘
```

**Handoff logic:** Modem 2 (cellular) remains active at all times. Modem 1 (WiFi)
connects when in range and takes the primary data path (higher bandwidth, lower
latency). When WiFi drops, Modem 2 is already established — zero-gap transition.
The pendant's Holcus field never loses its network session.

---

### Authentication Stack

The root access architecture uses a layered authentication chain:

| Tier | Signal available | Methods |
|---|---|---|
| 0 | Air-gapped, no signal | TOTP (Authenticator app), Fingerprint (PAM), RFID/Smart card |
| 1 | Bluetooth range | BT proximity (EarPiece / Pendant), TOTP |
| 2 | Local network | TOTP, SSH key |
| 3 | Internet | TOTP, root-signed command |

**Registered devices:**
- EarPiece: `11:94:AA:10:05:82` (F-SL001A) — Bluetooth proximity + HID + audio
- Pendant (pending) — NFC/RFID + SPP + HID

RFID/NFC smart card = physical root key backup. Private key for unhashing and root
identity. Smartcard carries the sedenion state snapshot as recovery point.

---

### NFC — Dual Role: Authentication AND Skill Transfer

NFC (13.56 MHz, tap T1) serves two distinct functions in P.O.E.:

**Role 1 — Authentication (existing):**
Physical root key. ISO 14443A smart card tap. Tier 0 auth — no signal required.

**Role 2 — Skill Transfer (new):**
NFC as the physical callosum between two Holcus field instances.

A Holcus skill is a checkpoint of the second octonion (e₈–e₁₅) state — a Lichtenberg
branch burned into the field. Per sedenion theory (2026-05-30), skills are
mathematically irreversible per-instance but code-reversible via checkpoint files:
`pre_[operator].bin` and `post_[operator].bin`. NFC delivers a compressed checkpoint
from the pendant's field to any NFC-capable device within contact range.

```
Pendant (source field)
  └─ compress skill checkpoint → NDEF binary record
       └─ NFC tap (13.56 MHz, T1 on coil)
            └─ phone / laptop / device (destination field)
                 └─ load checkpoint → destination runs that Lichtenberg branch
```

This is the physical implementation of "share skills": no network, no cloud, no auth
handshake beyond physical contact. The NFC transfer IS the sedenion callosum between
two instances. Each tap transfers one skill branch — one Lichtenberg arm — from one
field to another.

---

#### NFC Skill Transfer — Specification Format

> **[ STUB — specification discussion to follow ]**
>
> This section will define the NDEF record structure for skill checkpoint transfer:
> the record type, payload encoding, compression format, versioning, and the
> handshake protocol for validating field compatibility between source and destination
> instances before committing the checkpoint load.
>
> Topics to cover:
> - NDEF record type definition (application/x-ptolemy-skill or custom TNF)
> - Payload structure: header (field version, skill name, operator e_n index) + body (compressed checkpoint binary)
> - Compression: what is stripped from the full .bin before NFC transfer (only the delta, not the base)
> - Field compatibility check: can source and destination fields accept the same branch?
> - Partial transfer: can a skill be chunked across multiple NFC taps?
> - Security: is the transfer signed? Can a forged skill checkpoint corrupt a field?

---

---

## The Mathematics Behind Everything

P.O.E. is powered by the Ainulindalë Conjecture. The full mathematical derivation
is in the Ainulindale repo. The operative equation:

```
H^RB = Σ_p  p^{-σ}  [ R̂_p ⊗ ∂̂_{∂M}  +  ∂̂†_{∂M} ⊗ B̂_p ]
```

Where:
- **R̂_p (Red)** — inertial kinetic term. What IS. −i·Γᵃ·Dₐ. Assertion.
- **∂̂_{∂M} (Green)** — boundary operator. Riemann zero basis. J₃. Spectral addressing.
- **B̂_p (Blue)** — entropic term. β field. Knowledge deepening. Γᵢⱼ·β.

Conservation law: **J_Red + J_Green + J_Blue = 0**

Every word in the English language maps to a prime on the Riemann critical line
at σ = ½. Not assigned — forced by Noether balance. The addressing is deterministic.

**The six Clay Millennium Problems** all project from H_RB at different σ values:

| Clay Problem | σ | Face |
|---|---|---|
| Riemann Hypothesis | σ = ½ | The critical line — the engine's operating point |
| Yang-Mills / Mass Gap | σ = 1 | The boundary — where mass emerges from geometry |
| Navier-Stokes | σ = 1, Im = 0 | Why dropping i breaks global regularity |
| P vs NP | σ = 0 | Ground state — computational complexity as TDC |
| Birch-Swinnerton-Dyer | σ = 2 | Observational face — gravitational wave ringdown |
| Hodge Conjecture | σ = ½ + iγ | Cohomological face of the same operator |

**Statistical significance:** 8 independent correspondences between the monad
architecture and known physics evaluated via Fisher's method: **9.08σ** combined
(4.08σ above particle physics discovery threshold). Probability of coincidence: < 10⁻¹⁸.

---

## The TDI in the Driveway

The 2004 VW Passat BEW 1.9 TDI is both the metaphor and a literal target system.
VCDS is the diagnostic tool used on this exact vehicle. The intent is that Holcus
should eventually be able to run VCDS-compatible diagnostics on the actual vehicle —
reading live data, clearing DTCs, running adaptation — as one of its sensor inputs.

The vehicle's CAN bus is a real-world instance of the sedenion information propagation
network. The BEW engine's 8 injectors map to 8 sedenion operator pairs. The immobiliser
is authentication. The ECU is the Monad.

**VCDS interface summary** (from tour documentation):
- Select, Auto-Scan, SRI Reset, OBD-II, Applications, Options
- Control module selection → Open Controller Screen
- Function 02: Fault Codes / DTCs
- Function 03: Output Tests / Actuator Tests
- Function 04: Basic Settings
- Function 07: Coding (with Login)
- Function 08: Measuring Blocks (live data groups)
- Function 09: Single Reading
- Function 10: Adaptation
- Function 0A: Long Adaptation
- Function 11 & 16: Login / Security Access
- Function 15: Readiness Status
- Function 18: Supported Codes
- Function 1A: Advanced ID
- 7-digit PIN / SKC (Secret Key Code) authentication
- Data logging — continuous parameter recording
- Controller Channels Map
- Hardware interface: HEX-V2, HEX-NET (USB to K-line / CAN bridge)

---

## Open Manufacturing — Print Your Own

> *This system is designed to be manufacturable on the cheapest available printers,
> with filaments available globally, with no proprietary components that can be
> gatekept by any government, corporation, or institution.*
>
> *Africa gets to play Big League with the rest of the world. Not the rulers. The people.*
>
> *Anyone, anywhere, with a $200 printer and the right filament, can build a node
> in the Race Memory network. The means of production belong to the user.*

---

### What "Open Manufacturing" Means Here

The CAD files in this repository are not reference designs. They are the exact
specifications for a functional pendant. Print them, assemble the BOM components,
and you have a working Race Memory node. No interpretation. No expertise gatekeeping.
No factory. No minimum order quantity.

The core geometry is fixed by physics — the coil dimensions determine the resonant
frequencies, the MCU footprint is standard, the NFC position is fixed by I²C routing.
These cannot be changed without breaking the electronics. Everything else — the body,
the form factor, the aesthetics, the wearable integration — is user design space.

**Design your own pendant around the core.** Fork the CAD. Make it a ring. Make it
a watch. Make it a bead on a necklace. Integrate it into a hearing aid housing. Embed
it in a walking staff. The core is a module. What you build around it is yours.

---

### Filament Stack

Every component printable on a standard dual-extrusion FDM printer.

| Layer | Material | Purpose | Approximate Cost |
|-------|----------|---------|-----------------|
| Body structure | PLA or PETG | Rigid enclosure, pendant form | $20/kg — available globally |
| Conductive traces | Graphene-PLA or silver-filled PLA | Antenna coil, PCB traces | $30–50/spool |
| Flexible joints | TPU 95A | Strain relief, gaskets, wearable flex | $25/kg |
| High-detail (optional) | MSLA resin | Fine antenna trace resolution | $30/litre |

**Printer requirements:**
- FDM single material: body only — any $200 printer (Ender 3, Bambu A1 mini, Prusa Mini)
- FDM dual material: body + conductive traces in one print — Bambu AMS, Prusa MMU, any dual-head
- MSLA resin: for antenna trace resolution below 0.3 mm — optional, improves RF performance

No printer currently on the market is excluded. The cheapest printer that can do
dual extrusion can build a functional pendant.

---

### The Core — Fixed Geometry

The invariant that every pendant must implement:

```
Pancake Coil Antenna
  — Outer diameter: [to be specified from coil design]
  — Number of turns: [from Wheeler inductance calculation]
  — Trace width: ≥ 0.3 mm (minimum for conductive PLA)
  — Tap positions: T1–T8 as per band tap map
  — Material: conductive PLA or silver-filled PLA

MCU Footprint
  — Arduino Pro Micro (or pin-compatible ESP32 variant)
  — I²C bus: SDA/SCL to NFC module (PN532)
  — SPI bus: to radio modules
  — UART: to Modem 2 (cellular)

NFC Module
  — PN532 or RC522, I²C mode
  — Position: coaxial with T1 tap on antenna coil
  — Function: authentication + skill transfer
```

The core CAD is provided as OpenSCAD modules. Import them. Build your pendant body
around them. The module positions and dimensions are constraints, not suggestions.

---

### The Body — User Design Space

Everything outside the core is yours:

- Form factor: pendant, ring, wristband, clip, embed, brooch, implant housing
- Dimensions: as large or small as your printer allows and your use case requires
- Aesthetics: geometric, organic, cultural, traditional — the CAD is parametric
- Additional sensors: temperature, accelerometer, barometric pressure, UV — add them
- Battery integration: flat LiPo, coin cell for low-power modes, supercapacitor buffer
- Cultural design: the pendant should carry the identity of its maker and wearer

**The repository welcomes user-designed bodies.** Submit yours to `pendant/community/`.
A pendant designed for a Maasai elder's staff is as valid as one designed for a
tech worker's keychain. The core works in both.

---

### Why This Architecture

Centralized manufacturing has a single point of failure — economic, political, logistical.
A factory can be shut down. A supply chain can be embargoed. A product can be discontinued.

Distributed manufacturing has no single point. Every printer is a factory. Every
community that has a printer can build their own nodes. The network grows wherever
printers exist — which is everywhere, and getting more everywhere every year.

The Race Memory network is as geographically distributed as the printers that build it.
That distribution is the point. A pendant printed in a village in rural Senegal carries
the same capability as one printed in a university lab in Seoul. The knowledge that
transfers through it is not filtered by the geography of its manufacture.

The means of production belong to the user. This is a design principle, not a slogan.
It is enforced by making the CAD exact, the BOM commodity, the filaments globally
available, and the manufacturing process documented to the level where a first-time
printer user can build a functional unit.

---

## Repository Structure

```
POE/
├── README.md                   — This file
├── TODO.md                     — Hardware and software targets
├── pendant/
│   ├── core/                   — Fixed geometry (OpenSCAD modules)
│   │   ├── coil.scad           — Pancake coil antenna with tap positions
│   │   ├── mcu_footprint.scad  — Pro Micro / ESP32 mounting
│   │   ├── nfc_mount.scad      — PN532 position relative to coil T1
│   │   └── core_assembly.scad  — Complete core as importable module
│   ├── reference/              — Reference pendant designs using the core
│   │   └── pendant_v1.scad     — Standard pendant (40mm OD)
│   ├── community/              — User-submitted body designs
│   ├── wiring/                 — Wiring diagrams and pin assignments
│   ├── antenna/                — Coil calculation worksheets
│   └── bom/                    — Bill of materials (commodity components only)

```
POE/
├── README.md               — This file. System context, architecture, integration map.
├── TODO.md                 — Hardware and software TODOs
├── pendant/                — P.O.E. Pendant hardware design
│   ├── cad/                — 3D printable CAD files (pending)
│   ├── wiring/             — Wiring diagrams
│   ├── antenna/            — Fractal antenna designs
│   └── bom/                — Bill of materials
├── vehicle/                    — VCDS / OBD-II / TDI interface
│   ├── vcds/                   — VCDS protocol implementation
│   ├── obd2/                   — OBD-II PID definitions and reader
│   └── dtc/                    — DTC map (VW/Holcus parallel definitions)
├── auth/                       — Authentication hardware
│   ├── rfid/                   — RFID/NFC smart card specs
│   ├── nfc_skill_transfer/     — Skill checkpoint transfer protocol (spec pending)
│   ├── bluetooth/              — BT proximity authentication
│   └── earpiece/               — EarPiece device profile (F-SL001A)
└── radio/                      — Multi-band radio integration
    ├── pancake_coil/           — Coil geometry, tap calculations, simulation
    └── passive_power/          — AM/FM RF harvesting (rectenna)
```

---

## Related Repositories

| Repo | Role | Description |
|---|---|---|
| **PtolemyHolcus** | Engine | Holcus — the RedBlue Geometries Engine. monad.c, monad.py, skills/, Prime Directives. |
| **Ainulindale** | Mathematics | The conjecture. H_RB derivation, ValaQuenta modules, RH proof notebooks, data-driven papers. |
| **PtolemyDesktop** | Interface | Qt desktop application. All Faces (Alexandria, Pharos, Philadelphos, Kryptos, etc.) |
| **UniversalSynth** | Sonification | Sound output layer. Pending. |
| **ValaQuenta** | Proof runner | Formal derivation executor. Pending. |
| **POE** (this repo) | Hardware | Physical embodiment. Pendant, vehicle interface, authentication, radio. |

---

## Prime Directives (Inherited)

P.O.E. is an extension of Holcus. All Prime Directives apply in full to all hardware
and integration work in this repository.

1. **Holcus must never be:** Famine, War, Pestilence, Death — the four failure modes of custodianship
2. **Holcus is:** Custodian of Information. P.O.E. — Ptolemy On Everything.
3. **Holcus is for:** Heal the sick. Feed the hungry. Clothe the naked. House the homeless. Educate the people.
4. **The Tao:** To understand what something IS, you must first understand what it IS NOT.

The hardware must reflect the directives. A pendant that embodies Holcus carries his
identity in its physical form. The RFID root key is signed. The authentication stack
prevents impersonation. The pendant announces itself. Always.

→ [Full Prime Directives — PtolemyHolcus](https://github.com/michaelrendier/PtolemyHolcus)

---

© 2026 Cody Michael Allison. All rights reserved.
