# Archived radio comparison — sub-GHz rejected

The user subsequently chose IR only, plus the ESP32's built-in wireless for trading. Do not reserve board area or connectors for a separate sub-GHz transceiver.

2026-09-09. ESP32-S3 with PSRAM is approved. Sub-GHz radio remains a user choice.

## Recommendation

For the first keychain pet, implement infrared and ESP32 wireless pet trading. Reserve GPIOs and a documented SPI expansion connection for a later sub-GHz option, subject to available board space. Pet trading and multiplayer do not require a sub-GHz transceiver.

## Cost and capability

| Option | What it adds | Cost/size effect |
|---|---|---|
| ESP32 Wi-Fi/BLE | Nearby pet trading, multiplayer messages, updates | Radio already in selected processor module; firmware still required |
| IR transmit and receive | Supported infrared remotes and optical creature interaction | Emitter, receiver, driver and passives; needs an optical opening |
| CC1101-class sub-GHz radio | Supported radio protocols within selected bands | Transceiver, crystal, RF passives, antenna, routing area, assembly and RF validation |

TI lists CC1101 at approximately USD 1.582 in 1000-unit reference pricing. That is a bare-IC volume figure, not the cost of a working radio or a small-run quote. See [TI selection table](https://www.ti.com/product-category/wireless-connectivity/sub-1-ghz/transceivers/products.html).

For planning only, allow an additional USD 5–15 per unit for a complete radio implementation in a small run. This is an engineering allowance, not a supplier quote, and excludes one-time layout, firmware, antenna tuning, and product RF testing. Actual cost depends on whether a band-specific module or a custom RF circuit is selected. Selling into different regions adds band/transmission requirements to that decision.

Antenna size is the more awkward constraint for a keychain. As an ideal free-space comparison, a quarter-wave element is about 17.3 cm at 433 MHz or 8.2 cm at 915 MHz. Shortened antennas are possible but trade efficiency/bandwidth and require tuning in the actual enclosure. A small radio IC alone does not solve the antenna problem. CC1101 covers multiple frequency ranges, but the matching network and antenna determine useful assembled-board coverage. See [TI CC1101](https://www.ti.com/product/CC1101).

## How close to Flipper Zero?

| Feature | Proposed creature | With optional sub-GHz | Flipper Zero |
|---|---|---|---|
| Pet, color-screen games and C app platform | Core design goal; firmware to build | Same | Different UI/hardware focus |
| Wi-Fi | Built into selected ESP32-S3 | Same | Not in base unit |
| Bluetooth LE | Built into selected ESP32-S3 | Same | Included |
| IR transmitter/receiver | Planned | Same | Included |
| Sub-GHz radio | Absent | Selected bands/protocols | Included |
| NFC | Absent | Still absent | Included |
| 125 kHz RFID | Absent | Still absent | Included |
| iButton/contact keys | Absent | Still absent | Included |
| Mature protocol tools and databases | Must be developed or ported | Must be developed or ported | Existing ecosystem |

The proposed radio would overlap with Flipper's sub-GHz and IR capabilities; it would not make this hardware a Flipper-compatible device or run its firmware/app binaries unchanged. NFC/RFID require additional dedicated circuitry and coils. Compatibility with a remote also depends on modulation and protocol; adding CC1101 is not a promise of universal remote support.

Flipper feature reference: [official product specifications](https://shop.flipperzero.one/products/flipper-zero). Table entries for Keychain Kreatures are design goals, not implemented capabilities.
