from pathlib import Path
root=Path(__file__).resolve().parent.parent
s=(root/'pcb/export_fit_checks.py').read_text().replace("ROOT=Path(__file__).resolve().parent.parent","ROOT=Path(__file__).resolve().parent.parent/'C5_relayout'").replace('KK MAIN C.4 - REAR FIT CHECK / 80 x 115mm / PROTOTYPE','KK MAIN C.5 - REAR FIT CHECK / 84 x 95mm / PROTOTYPE').replace("ROOT/'pcb'/f'{side}-fit-check.pdf'","ROOT/f'{side}-fit-check.pdf'")
exec(compile(s,str(root/'pcb/export_fit_checks.py'),'exec'))
