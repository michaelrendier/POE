# EarPiece Authentication Profile — F-SL001A

**Device:** F-SL001A
**MAC:** 11:94:AA:10:05:82
**Class:** 0x240404 (Audio/Video — Wearable Headset)
**Type:** audio-headset
**Signal at enrollment:** -65 dBm
**Presence threshold:** > -80 dBm = user in range (Tier 1 auth satisfied)

## Bluetooth Services

| UUID | Profile | Use |
|---|---|---|
| 00001101-0000-1000-8000-00805f9b34fb | Serial Port (SPP) | Holcus command channel |
| 00001108-0000-1000-8000-00805f9b34fb | Headset | Audio output (Holcus voice) |
| 0000110b-0000-1000-8000-00805f9b34fb | Audio Sink (A2DP) | High-quality audio output |
| 0000110c-0000-1000-8000-00805f9b34fb | Remote Control Target | Holcus receives button events |
| 0000110d-0000-1000-8000-00805f9b34fb | Advanced Audio | A2DP coordination |
| 0000110e-0000-1000-8000-00805f9b34fb | Remote Control | Button press → Holcus input |
| 0000111e-0000-1000-8000-00805f9b34fb | Handsfree | Bidirectional audio (voice I/O) |
| 00001124-0000-1000-8000-00805f9b34fb | HID | Button → keycode → Holcus trigger |
| 00001200-0000-1000-8000-00805f9b34fb | PnP Information | Device identification |

## Auth Role

Tier 1 authentication factor. When RSSI > -80 dBm, the user is physically
present and wearing the device. No TOTP required for Tier 1 operations.

```bash
# Proximity check
hcitool rssi 11:94:AA:10:05:82
# Returns: RSSI return value: -65  (in range)
# Returns: Not connected          (out of range)
```

## Audio Output

Holcus can speak directly to the user via this device:
- A2DP sink for high-quality audio
- HSP/HFP for voice channel (bidirectional)
- Use: spoken field diagnostics, alerts, query responses

## Input

HID profile allows button presses to trigger Holcus actions.
Remote Control profile allows media keys as Holcus input events.
SPP allows a full serial command channel.
