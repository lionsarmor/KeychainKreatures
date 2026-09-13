# Cleanup and simplification review — 2026-09-11

**Historical cleanup record.** The draft routing counts and unfinished tasks below describe 2026-09-11, not the current C.6/P.3 release. Use [current documentation](README.md) and [release index](C6_P3_RELEASE_INDEX.json). Original move manifests and their hashes are unchanged.

## Completed

- Moved 146 files/directories to the revision archive or original-source documents folder. Every moved file was hash-verified; nothing was deleted.
- Verified that 119 active CAD, local library and model files remained byte-for-byte unchanged.
- Kept the C.5 main project and P.2 power project at their existing current paths. Removed the incompatible legacy power project and old fabrication ZIPs from the active power folder.
- Corrected the stale power status from P.1 to P.2 and added a project entry point at [START_HERE.md](../START_HERE.md).
- Archived old BOMs, reports and unfinished routing candidates. Retained the C.4 datasheet packet because the current C.5 assembly guide still uses it.
- Preserved three compatibility links for older main-board reference paths. Retained C.5 helper code that imports earlier revision utilities.
- Excluded revision archives and their compatibility paths from normal VS Code watching/search. No extension was removed or disabled. No router or renderer was launched.
- Recorded a [power simplification review](../KK_power_module/SIMPLIFICATION_REVIEW.md) with explicit retain/review decisions. No component substitutions or circuit changes were made.

## Lightweight verification

Command: `node tools/check_project.mjs`

Result: **zero errors**. Checked archive and active-file hashes, 17 distinct project-local CAD library/model references, saved power-manifest/netlist consistency and the four-pin power/main harness. Verified USB data/SBU pins remain disconnected in the saved power netlist, and battery return / thermistor ground labels remain as intended.

System-installed KiCad model paths are reported as unchecked. This was not a fresh ERC/DRC run, a powered test, a simulation or a complete fit check. No electrical performance claim follows from unchanged files.

## Remaining work

The current power draft still contains 14 ICs, 108 fitted electrical components and 28 bare test pads. Its last saved native DRC contains **138 unconnected items and three dangling-via warnings**, with no saved schematic-parity issues. The 50 × 50 mm draft remains unrouted in substantial areas.

Component-level simplification, completion of the electrical/assembly review, final placement/routing, final ERC/DRC and the power-board manufacturing/BOM package remain unfinished. No five-board order package is approved by this cleanup.

Existing user Git staging/deletions were not reset, unstaged or committed. See [the move manifest](../revisions/2026-09-11_cleanup/MOVE_MANIFEST.json) for reversible recovery to a separate scratch workspace.
