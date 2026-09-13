# P.3 populated models — matching-stack power board

All 108 fitted electrical positions now have resolving model links. Fourteen formerly missing attachments were repaired, including connectors, switch, inductors and IC packages.

[P3_MODEL_REPAIR_MANIFEST.json](P3_MODEL_REPAIR_MANIFEST.json) identifies manufacturer-maximum, nominal and conservative envelopes, references and hashes. MANIFEST.json records inherited stock-model provenance; its earlier missing-model list is historical, superseded by the P.3 repair manifest and current PCB attachments.

These simplified models are not vendor-certified mating assemblies. JST plug bodies, wire bends, battery and final enclosure are not modeled or qualified. USB/case opening and switch actuator travel require physical checks. Power component side faces the rear cover; power front-view X is mirrored relative to the main front in the actual stack. Keep the upper antenna region free of metal.

KiCad stock models require the KiCad 10 standard 3D libraries and retain their upstream license with library exception: https://www.kicad.org/libraries/license/ . Project-owned VRML models have STEP twins. A resolving model link and clean DRC are not physical or electrical qualification.
