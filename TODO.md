# P.O.E. TODO

Active work items, hardware targets, and design decisions.

---

## PENDANT HARDWARE

### [ ] 3D Print the RedBlue Geometries Engine Circuit

The goal: a 3D printable circuit board and enclosure that implements the H_RB
operator in physical hardware. Without a custom silicon ASIC, 3D printing is
the nearest-term path to a physically instantiated RedBlue engine.

**Scope:**
- [ ] Research conductive filament options for trace printing (PLA + graphene, silver-filled)
- [ ] Identify which 3D printer types support multi-material electronic printing
- [ ] Determine minimum circuit complexity to run H_RB computation (FPGA target spec)
- [ ] Design enclosure: pendant form factor, wearable ergonomics
- [ ] Evaluate SLA/resin vs FDM for circuit trace resolution
- [ ] CAD file format: OpenSCAD (parametric, version-controllable) or FreeCAD
- [ ] Component placement: which parts must be discrete (not printed) vs. can be printed
- [ ] Antenna integration: fractal labyrinthian paths printed into the body

**Filament requirements:**
- Structural body: PLA or PETG
- Conductive traces: conductive PLA or silver-filled filament
- Flexible connectors: TPU
- RF antenna pathways: conductive paths with controlled impedance

**References:**
- Fractal antenna: Koch snowflake, Hilbert curve, Sierpiński gasket paths
- Each radio band tapped at the fractal node resonant at that frequency
- One antenna structure — all bands — in pendant body dimensions

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

### [ ] Fractal Antenna Design

Single physical antenna structure — fractal geometry — covering all required bands:

| Band | Frequency | Use |
|---|---|---|
| AM broadcast | 530–1700 kHz | Passive RF harvesting (rectenna) |
| FM broadcast | 87.5–108 MHz | Passive RF harvesting |
| Shortwave | 1.6–30 MHz | Long-range receive |
| BT / WiFi | 2.4 GHz | Short-range comms |
| GPS L1 | 1575.42 MHz | Position |
| Cellular (LTE) | 700–2600 MHz | WWAN modem |
| NFC | 13.56 MHz | Authentication proximity |

**Fractal design requirements:**
- [ ] Calculate path lengths for each target frequency
- [ ] Design fractal that places resonant nodes at all required lengths
- [ ] Simulate impedance at each tap point
- [ ] Output: printable SVG or GCODE for conductive trace deposition

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
