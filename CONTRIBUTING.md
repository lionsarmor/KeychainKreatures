# Working on Keychain Kreatures

Use the current projects linked in [README.md](README.md). The active publishing branch for this update is `development`; `main` is not automatically merged or changed. Keep edits scoped and preserve unrelated work.

## Hardware changes

1. Start a new branch/revision from the current native CAD, with all local libraries. Do not generate over a routed board or import an old SES.
2. Keep schematic pins/nets, PCB pads, exact BOM package/polarity, footprint and 3D models consistent. Main is a student through-hole kit; power is factory SMT. Do not hide errors by weakening safety/clearance rules.
3. Refill copper and run KiCad ERC, DRC and schematic parity. Inspect independent trace widths, actual power paths, mounting/antenna clearances and both sides of the assembly. Run heavy jobs sequentially with one CPU where available.
4. Run `node tools/check_project.mjs` to check the saved release. A source edit should make the old release check fail until the new revision has been properly verified and packaged; do not update hashes merely to silence failures.
5. Issue new source-bound reports and manufacturing packages. Never silently overwrite an issued ZIP, change archived evidence, or confuse an old BOM/fit sheet with a new PCB.

Power J3/main J1 must stay pin-for-pin 5 V, GND, 3.3 V, 3.2 V unless an explicit interface revision is reviewed. Preserve BAT_NEG isolation, protection/NTC functions, default-safe outputs and USB backfeed restrictions. A clean CAD report does not establish safe charging or toy compliance.

## Documentation and firmware

Update README, START_HERE, docs/README, release notes and relevant current assembly/BOM/fit instructions together. Keep historical documents labeled with their actual revision; do not rewrite their findings as current evidence. Use repository-relative links and distinguish measured results from calculated targets and proposed features.

The old ESP32-C3 factory-test firmware is incompatible. Current S3 bring-up/game/upload firmware is not provided by this hardware release. Test output defaults, rail sequencing, SD interrupted writes, IR, RGB, audio/motor limits and recovery before claiming features work. Keep Wi-Fi credentials and private keys outside the repository.

Project-wide licensing is still unresolved. Preserve third-party attribution/terms and do not add a license or certification claim on the owner's behalf. Propose licensing decisions separately.
