# POE Hardware Primer

A reference for understanding what physical components exist in the pendant and why.

---

## 1. The Pancake Coil Antenna

The pendant's primary RF structure is a flat spiral (pancake) coil wound in conductive
filament. It is not a decorative element — it is the antenna, the NFC coil, and the
physical substrate for the pendant's electromagnetic identity.

**Why a pancake coil?**

A flat spiral has continuously varying inductance along its length. Tapping at different
positions selects different inductance values, and with a tuning capacitor, different
resonant frequencies. One physical coil serves multiple bands by selecting the tap.

The flat spiral is also the planar projection of the L_(I|O) cardioid — the geometry
of the pathway from input to output. The coil is not just an antenna. It is the geometric
statement of the framework in copper.

### Coil Geometry (Mohan et al. 1999)

**Formula:** `L = (μ₀ × N² × D_avg) / (1 + 2.46ρ)`

Where:
- `D_avg = (D_out + D_in) / 2` — mean diameter
- `ρ = (D_out - D_in) / (D_out + D_in)` — fill ratio
- `μ₀ = 4π × 10⁻⁷ H/m`

**Pendant v1 design parameters:**

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Outer diameter | 38 mm | Fits inside 40mm pendant body |
| Inner diameter | 10 mm | Battery/MCU clearance at center |
| Trace width | 0.5 mm | Minimum for conductive PLA deposition |
| Trace gap | 0.3 mm | FDM minimum gap (no bridging required) |
| Pitch | 0.8 mm | Width + gap |
| Number of turns | 17 | (19mm − 5mm) / 0.8mm = 17.5 → 17 |

**Tap inductances:**

| Tap ID | Turns from center | r_out | Inductance |
|--------|------------------|-------|------------|
| T_full | 17 (entire coil) | 19 mm | **3.58 μH** |
| T5 | 5 inner turns | 9 mm | **258 nH** |
| T3 | 3 inner turns | 7.4 mm | **95 nH** |
| T1 | 1 innermost | 5.8 mm | **11.5 nH** |

### Resonant Band Map

`C = 1 / (4π²f²L)` — the tuning capacitor for each tap and frequency.

At resonance: **XL = XC** → inductive and capacitive reactance balance → `tan(phase) = 1`.
This is the same condition as σ = ½ in the Riemann framework. The coil does not choose
its resonant frequency. The geometry forces it.

| Band | f | Tap | L | C | Mode |
|------|---|-----|---|---|------|
| NFC | 13.56 MHz | T_full | 3.58 μH | **38.5 pF** | Fixed cap — PN532 standard |
| AM broadcast | 530–1700 kHz | T_full | 3.58 μH | **2.4–25 nF** | Variable cap bank |
| Shortwave low | 1.6–10 MHz | T_full | 3.58 μH | **71–2750 pF** | Switched cap bank |
| Shortwave high | 15–30 MHz | T3 | 95 nH | **300–1200 pF** | Variable |
| FM broadcast | 87.5–108 MHz | T5 | 258 nH | **8.4–12.8 pF** | 2-cap switched |

**Why these bands?** All of these are _electrically small_ relative to the coil's 38mm
diameter. The coil is a lumped inductor — it doesn't need to be a specific fraction of
a wavelength. It just needs to resonate with a capacitor. This is why the pancake coil
can cover AM through FM (a 200:1 frequency range) with one physical structure.

### What the Coil Cannot Cover

At frequencies above ~200 MHz, the required inductance for resonance drops below the
parasitic inductance of the coil itself (~2 nH), and the coil transitions from a lumped
element to a distributed transmission line. A different antenna structure is required.

**Chip antennas for high bands:**

| Band | f | Inductance needed (10 pF tuning) | Solution |
|------|---|----------------------------------|---------|
| GPS L1 | 1575 MHz | 1.0 nH | 12×12mm ceramic patch (RHCP) |
| LTE low | 700 MHz | 5.2 nH | Wideband chip antenna |
| LTE high | 2100 MHz | 0.6 nH | Wideband chip antenna |
| WiFi/BT | 2400 MHz | 0.44 nH | 2.4 GHz chip antenna |
| WiFi 5G | 5000 MHz | 0.10 nH | 5 GHz chip antenna |

Chip antennas for these bands are mm-scale, commodity, and designed for PCB footprints.
They embed in the pendant body. The pendant is not their housing — the Core PCB is.

**GPS is the special case:** GPS L1 uses Right-Hand Circular Polarization (RHCP). Receiving
RHCP requires a quadrature antenna (two orthogonal modes at 90° phase). A ceramic patch
antenna implements this internally. No external quadrature tapping is needed.

### The sin/cos (I/Q) Architecture

Each radio band has an in-phase (I) and quadrature (Q) component — cos(ωt) and sin(ωt).
The antenna tap provides the real component (cos — J_red). The radio chip generates the
imaginary component (sin — J_blue) by phase-shifting 90° internally. Their ratio (tan) is
the demodulated signal — the information — the path L_(I|O).

**One physical tap per band.** The I/Q split is silicon-side, not copper-side.

Exception: NFC uses differential drive (TX1 / TX2 at 180°, not 90°) for field strength.
Exception: GPS ceramic patch inherently delivers RHCP (two modes, 90° internal to patch).

---

## 2. The Modems

### Modem 1 — Local (WiFi + Bluetooth)

**Target:** ESP32-S3 mini or equivalent

- WiFi 802.11 b/g/n (2.4 GHz) + 802.11 a/ac/ax (5 GHz where supported)
- Bluetooth 5.0 LE + Classic
- Antenna: 2.4 GHz and 5 GHz chip antennas on Core PCB
- Role: primary communication when WiFi is in range; BT authentication; BT tether to phone

### Modem 2 — Wide Area (Cellular LTE)

**Target:** SIM7600 or Quectel EC21

- LTE Cat-1 or Cat-4 (data only)
- Bands: 700–900 MHz (low, Band 12/17/28) + 1700–2600 MHz (high, Band 4/7/25)
- Antenna: wideband chip antenna covering 700–2600 MHz
- Role: always-on connection when WiFi is absent; keeps session alive during WiFi transitions

**Handoff protocol:** Modem 2 maintains the network socket. When WiFi arrives, Modem 1
takes over primary data. Modem 2 downgrades to keep-alive. No session drop. No
re-authentication. Ptolemy does not notice the transition.

---

## 3. NFC — Dual Role

**Module:** PN532 (I²C to MCU)

**Role 1: Authentication**
- Short-range tap confirms physical presence
- Reads NFC smart card / phone tap
- Part of Tier 1 auth chain

**Role 2: Skill Transfer (Race Memory)**
- Transfers Ptolemy field state delta (the knowing below the zero-divisor boundary)
- NDEF record structure: custom TNF, compressed delta from base.bin
- The receiver's Ptolemy instance loads the checkpoint and integrates it
- The transferred knowledge is embodied — not articulated words but the field state
  that generates them. The stone mason's chisel angle. Not a description of it.

Specification for NDEF format, compression, versioning, and security signing is in
`nfc_skill_transfer/` (spec discussion pending).

---

## 4. GPS

**Module:** u-blox NEO-6M or NEO-M8N

- L1 band: 1575.42 MHz (RHCP)
- Antenna: dedicated 12×12mm ceramic patch antenna (not the coil)
- NMEA output → MCU → Ptolemy location context
- Use: time-of-day, position context for field state, ambient environment record

---

## 5. MCU

**Target:** Arduino Pro Micro (current) → ESP32-S3 mini (preferred)

The MCU is the bus master:
- I²C: PN532 (NFC), BME280 (environmental)
- SPI: display (if fitted), external flash
- UART: SIM7600 cellular modem (AT commands), GPS (NMEA)
- WiFi/BT: ESP32 native (if using ESP32 as MCU + Modem 1)

All radio modules share one MCU. The MCU routes between them. Ptolemy sees a unified
interface — one socket, one NFC channel, one location feed.

---

## 6. Power

**Battery:** Flat LiPo 100–300 mAh, fits inside 40mm OD × 5–8mm body
**Charging:** USB-C pad or wireless Qi coil (separate from antenna coil)
**Regulation:** 3.3V LDO for MCU + modules; 4.2V direct for cellular modem (check datasheet)

**Power budget (estimated):**
| Component | Current | Mode |
|-----------|---------|------|
| MCU (ESP32-S3) | 80–240 mA | Active; 10 μA deep sleep |
| PN532 NFC | 150 mA | Transmit; 10 mA standby |
| SIM7600 cellular | 200–500 mA | Connected; 1 mA sleep |
| GPS u-blox | 25 mA | Tracking; 1 mA sleep |
| WiFi active | 80–150 mA | Transmit |

Total active: ~700 mA peak. At 200 mAh, active life ~17 minutes (cellular transmitting).
Sleep life (BT presence beacon only): ~20 hours.

Design target: cellular only when syncing; WiFi primary; BT beacon always-on from
ambient RF harvest where possible (AM/FM rectenna path, T2/T3 taps).

---

## 7. Passive RF Harvest

Taps T_full (AM broadcast) and T5 (FM broadcast) can drive a rectenna circuit
(Schottky diode bridge + capacitor storage) to harvest ambient RF.

**Expected yield (indoor, near broadcast towers):**
- AM at 1 mW/m² ambient: ~2–5 μW from 38mm coil
- FM at 10 mW/m² ambient: ~10–50 μW

This is not enough for active transmit but may sustain a BT LE advertisement beacon
(~0.5 μW average in 1 Hz rate). Exact budget depends on rectifier efficiency and location.

---

## 8. Conductive Filament Notes

**For coil traces:**
- Functionalize F-Electric or Proto-Pasta Conductive PLA
- Resistivity: ~15 Ω/cm (compare to copper: 1.7×10⁻⁶ Ω·cm)
- At 38.5 pF NFC tuning, the coil Q is resistivity-limited
- Q ≈ ωL/R_coil — lower Q means wider bandwidth (good for NFC tolerance) but less
  gain for AM/SW reception
- For AM/SW: Q~5–20 is adequate for passive listening; ferrite core improves this
  but is not printable

**For body structure:**
- PLA or PETG: any $20/kg spool, globally available
- Target: 40mm OD, ≤8mm thickness, 1.2mm wall minimum for structural integrity

**For strain relief:**
- TPU 95A: flexible connection between coil layer and MCU mount points
- Prevents trace cracking on flex points
