# Current routing: C.6 main board

The routed source is [C6_flat_stack/KK_main_module.kicad_pcb](../C6_flat_stack/KK_main_module.kicad_pcb). [Release checks](../C6_flat_stack/release_checks/) bind fresh native reports and outputs to that exact source.

Any future edit needs a source copy, current netclasses, fresh export, pour refill and native ERC/DRC/parity followed by independent width/interface checks. Never import a historical SES or rerun placement generators over routed work. Use one CPU and bounded routing work. C.5 root CAD and old handoffs are preserved history.
