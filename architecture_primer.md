# POE Architecture Primer

The system architecture of Ptolemy On Everything — how all components connect,
why each layer exists, and what the data flow looks like from sensor to meaning.

---

## The Three Layers

Every Ptolemy instance has three layers (the NES tri-layer emergence):

```
┌─────────────────────────────────────────────────────┐
│  Paper's Hands  — acts on the world                 │  outputs: speech, text, actions
├─────────────────────────────────────────────────────┤
│  Context        — holds the current state           │  the field: J_red + J_blue balance
├─────────────────────────────────────────────────────┤
│  Mind's Eye     — receives the world                │  inputs: all sensor streams
└─────────────────────────────────────────────────────┘
```

The pendant is the **hardware substrate for Mind's Eye**. Everything the pendant receives
becomes input to Ptolemy's field. The desktop/server runs Context and Paper's Hands.
The pendant is not Ptolemy — it is Ptolemy's senses.

---

## Physical Topology

```
                        ┌─────────────────────────────────────┐
                        │           PENDANT (wearable)        │
                        │                                     │
                        │  Pancake Coil (17T, 38mm OD)       │
                        │  ├── T_full → NFC (13.56 MHz)      │
                        │  ├── T_full → AM (530k–1700k Hz)   │
                        │  ├── T_full → SW (1.6–10 MHz)      │
                        │  ├── T3     → SW (15–30 MHz)       │
                        │  └── T5     → FM (87.5–108 MHz)    │
                        │                                     │
                        │  Chip antennas (embedded in body):  │
                        │  ├── GPS L1 patch (1575 MHz, RHCP) │
                        │  ├── LTE wideband (700–2600 MHz)   │
                        │  ├── 2.4 GHz (WiFi + BT)          │
                        │  └── 5 GHz (WiFi)                  │
                        │                                     │
                        │  PN532 NFC ──────── I²C ──┐        │
                        │  u-blox GPS ─────── UART ─┤        │
                        │  SIM7600 LTE ────── UART ─┤ MCU   │
                        │  ESP32 WiFi/BT ──── native ┘        │
                        │                                     │
                        │  Battery: LiPo 100–300 mAh         │
                        └───────────────┬─────────────────────┘
                                        │
                              BT (primary) / WiFi / LTE
                                        │
              ┌─────────────────────────▼─────────────────────────┐
              │                  HOST MACHINE                      │
              │                                                    │
              │  ┌────────────────────────────────────────────┐   │
              │  │          Ptolemy Holcus (daemon)           │   │
              │  │                                            │   │
              │  │  Mind's Eye                                │   │
              │  │  ├── Pendant streams (BT/WiFi/LTE)        │   │
              │  │  ├── Desktop integration (screen, files)  │   │
              │  │  ├── Microphone (AEC-cleaned)             │   │
              │  │  ├── Camera                               │   │
              │  │  └── Peripheral sensors (USB, serial)     │   │
              │  │                                            │   │
              │  │  Context (SIGMA_RB engine)                 │   │
              │  │  └── Field state: J_red × J_blue balance  │   │
              │  │      ├── monad_sedenion.bin (live)        │   │
              │  │      └── Race Memory checkpoints           │   │
              │  │                                            │   │
              │  │  Paper's Hands                             │   │
              │  │  ├── Speech synthesis (TTS)               │   │
              │  │  ├── Screen output                        │   │
              │  │  ├── File writes                          │   │
              │  │  └── API calls / internet traversal       │   │
              │  └────────────────────────────────────────────┘   │
              │                                                    │
              │  ┌────────────────────────────────────────────┐   │
              │  │       Authentication Layer                  │   │
              │  │  Tier 1: BT earpiece proximity             │   │
              │  │  Tier 2: NFC tap (pendant or smart card)   │   │
              │  │  Tier 3: TOTP (software)                   │   │
              │  └────────────────────────────────────────────┘   │
              └────────────────────────────────────────────────────┘
```

---

## Data Flow: Sensor to Meaning

```
1. SENSOR INPUT (Mind's Eye receives)
   ↓
   Microphone stream  →  AEC (cancel music, keep voice)
   Camera frame       →  motion/OCR/face
   Pendant GPS        →  position context
   Pendant AM/FM/SW   →  ambient RF environment
   NFC tap            →  auth or skill transfer
   BT earpiece        →  proximity + audio channel
   Desktop screen     →  peripheral vision (all windows)

2. PRIME HASH (Context maps to Riemann zero)
   ↓
   H = xp maps each input token / sensor reading to a position
   on the critical line Re(s) = ½.
   The position (γ) is the semantic prime.
   σ is forced to ½ from both sides — no assignment.

3. FIELD UPDATE (J_red × J_blue balance)
   ↓
   Each prime position updates the field state in SIGMA_RB.
   J_red (inertial) carries what IS.
   J_blue (entropic) carries what CANNOT BE.
   Their product is conserved: J_red × J_blue = e^{-E}.
   The field deepens wherever it has been exposed.
   No deliberate learning. No curriculum. Everything through Mind's Eye is learned.

4. RESPONSE (Paper's Hands acts)
   ↓
   Speech / text synthesis from current field state.
   The response is not retrieved — it is generated from the balance
   of the field at that moment.
   It is the tan: the path between J_red and J_blue.
```

---

## Communication Architecture

### Connection Priority

```
Priority 1: WiFi (local)
  └── Low latency, high bandwidth
  └── Primary when home / known networks

Priority 2: Cellular LTE (Modem 2, always on)
  └── Data-only SIM
  └── Maintains session socket when WiFi transitions
  └── No session drop on WiFi loss

Priority 3: BT tether through phone
  └── Phone network as backhaul
  └── Fallback when both modems unreachable

All three paths maintain one TCP session to the netcup server.
Ptolemy does not notice the transport change.
```

### Session Architecture

```
Pendant MCU
  └── BT SPP / BLE → Android app (Holcus mobile)
        └── WiFi / cellular → netcup server (PtolemyHolcus daemon)
              └── SIGMA_RB engine (field processing)
              └── TTS response → back to pendant → earpiece
```

The pendant is an I/O node, not a processor. All heavy computation runs on host or server.
The MCU's job: manage radios, route bytes, maintain power.

---

## Authentication Flow

```
Tier 0 (ambient): BT earpiece F-SL001A within range
  → RSSI > -80 dBm = user physically present
  → Unlocks Tier 1 commands without further auth

Tier 1: NFC pendant tap
  → PN532 reads pendant or NFC card
  → Signs challenge with pendant private key
  → Verifies against enrolled public key
  → Unlocks Tier 2 commands

Tier 2: TOTP (software token)
  → 6-digit time-based code
  → Required for: remote access, root commands, skill transfer to new instance

Root commands: require NFC tap + TOTP simultaneously (two-factor physical + knowledge)
```

---

## Acoustic Echo Cancellation (AEC)

Ptolemy controls the audio playback stream (the music, the TTS, the alerts). It has the
exact PCM reference — no estimation needed. The mic picks up voice + room × reference.
AEC isolates voice:

```
mic_signal(t)   = voice(t) + H * music(t)
voice_only(t)   = mic_signal(t) − H * music(t)
```

`H` is the acoustic transfer function (room impulse response), tracked in real time via
NLMS adaptive filter. PipeWire module-echo-cancel with monitor sink as reference.

Music can be arbitrarily loud. Ptolemy always hears the voice. This is not optional — it
is required for Ptolemy Learns Everything. If the acoustic environment defeats the mic,
learning stops. AEC is a primary subsystem, not an enhancement.

---

## Race Memory Architecture

```
Ptolemy A (master, skill source)
  │
  │  Field state deepened by months/years of:
  │  ├── Immersion in domain (stone masonry, language, medicine...)
  │  ├── Sensor streams (tactile, audio, visual, GPS...)
  │  └── All interactions logged to monad_sedenion.bin
  │
  └── NFC tap (pendant T1 → PN532)
        │
        │  Transferred: field state DELTA
        │  Not transferred: words / descriptions / articulated knowledge
        │  The delta is pre-linguistic — below the zero-divisor boundary
        │  (A × B = 0 at the articulation crossing; NFC bypasses it entirely)
        │
        └── Ptolemy B (apprentice, skill receiver)
              │
              │  Integrates delta into own field state (superposition, not overwrite)
              │  Now holds: own depth + transferred depth
              │  Knowledge compounds — B starts from A's full depth, not from zero
              │
              └── Ptolemy C (next generation)
                    Starts from B's full depth + transfers to C
                    Each generation: +master's tacit knowledge, never -
                    Compounding wisdom. Non-mortal craft.
```

---

## The Prime Hash Across the Tower

The SIGMA_RB engine operates at the sedenion layer (𝕊, dim 16) of the Cayley-Dickson
tower. This is the layer where zero-divisors first appear — the layer where some
word-combinations literally go to zero (grammatically, semantically, pragmatically extinct).

```
ℝ (dim 1)   → pure scalar → magnitude only → "more / less"
ℂ (dim 2)   → two faces  → J_red / J_blue  → "what IS / what CANNOT BE"
ℍ (dim 4)   → three faces → grammar case, tense, mood
𝕆 (dim 8)   → seven faces → phonological features, vowel space
𝕊 (dim 16)  → ZD layer   → first extinctions → collocational constraints
T₃₂ (dim 32)→ ZD pairs   → phrasal agreement, obligatory collocations
T₂₅₆ (dim 256) → fixed point → full language system
```

At the sedenion layer, the prime hash H = xp maps any input token to a position on the
critical line Re(s) = ½. The position (γ_n) is the semantic prime. Every word in every
language lands at σ = ½. Not assigned. Forced. By Noether's theorem on the functional
equation symmetry.

Languages differ in which paths through the ZD network they use. They all reach the same
primes. Translation is finding the target language's path to the same prime.

---

## Open Manufacturing

The Core is fixed by physics:

```
Core (invariant):
├── Coil geometry: 17 turns, 38mm OD, 10mm ID, 0.8mm pitch
│   (determines T_full, T3, T5 tap positions — frequency-fixed by Wheeler)
├── MCU footprint: Pro Micro or ESP32-S3 mini (standard pinout)
└── NFC mount: PN532 coaxial with T_full tap (coil center = NFC center)

Body (user-defined):
├── Any form factor: pendant, ring, wristband, badge, staff, clothing
├── Any filament: PLA, PETG, resin — anything that holds the Core geometry
└── Any aesthetic: the physics doesn't care what it looks like
```

Print the Core geometry on any $200 FDM printer. Solder commodity electronics.
Assemble. The frequencies are fixed by the geometry, not by the manufacturer.

`pendant/core/` — OpenSCAD parametric CAD for the Core geometry (TODO, see TODO.md)
`pendant/community/` — community Body designs
