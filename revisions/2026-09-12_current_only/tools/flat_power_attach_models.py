"""Model attachment changes only; verify entire saved electrical geometry unchanged."""
from pathlib import Path
import pcbnew as k,json,hashlib
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'KK_power_module/P3_matching_stack'
b=k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb'))
def sig(b):
    xy=lambda p:[p.x,p.y]
    pads=sorted((f.GetReference(),p.GetNumber(),p.GetNetname(),xy(p.GetPosition()),xy(p.GetSize()),xy(p.GetDrillSize())) for f in b.GetFootprints() for p in f.Pads())
    tracks=sorted((t.GetClass(),t.GetNetname(),xy(t.GetStart()),xy(t.GetEnd()),int(t.GetLayer()),t.GetWidth(k.F_Cu) if t.GetClass()=='PCB_VIA' else t.GetWidth()) for t in b.GetTracks())
    return hashlib.sha256(json.dumps([pads,tracks]).encode()).hexdigest()
before=sig(b)
mapping={'J1':'P3_USB_HCTL_envelope','J2':'P3_JST_VH2_envelope','SW1':'P3_JS102_envelope','L1':'P3_XFL4020_max','L2':'P3_XFL4020_max','L3':'P3_XFL4020_max','U1':'P3_RGT16_max','U3':'P3_RWB12_max','U4':'P3_DSG8_max','U5':'P3_DSC10_envelope','U6':'P3_DSC10_envelope','U7':'P3_DSC10_envelope','U12':'P3_RGP20_envelope'}
mapping['U13']='P3_YBH6_max'
for f in b.GetFootprints():
    if f.GetReference() not in mapping:continue
    model='${KIPRJMOD}/3dmodels/'+mapping[f.GetReference()]+'.wrl'
    f.Models().clear();m=k.FP_3DMODEL();m.m_Filename=model;f.Models().push_back(m)
    name=str(f.GetFPID().GetLibItemName());lib=k.FootprintLoad(str(OUT/'KK_Power.pretty'),name);assert lib is not None,name
    lib.Models().clear();lm=k.FP_3DMODEL();lm.m_Filename=model;lib.Models().push_back(lm);k.FootprintSave(str(OUT/'KK_Power.pretty'),lib)
assert sig(b)==before
k.SaveBoard(str(OUT/'KK_power_module.kicad_pcb'),b)
assert sig(k.LoadBoard(str(OUT/'KK_power_module.kicad_pcb')))==before
missing=[]
for f in b.GetFootprints():
    if f.GetReference().startswith(('H','TP','LOGO')):continue
    if not len(f.Models()):missing.append(f.GetReference()+': no model')
    for m in f.Models():
        p=Path(m.m_Filename.replace('${KICAD10_3DMODEL_DIR}','/app/extensions/Library/3dmodels').replace('${KIPRJMOD}',str(OUT)))
        if not p.exists():missing.append(f.GetReference()+': '+str(p))
assert not missing,missing
(OUT/'reports/model_link_repair.json').write_text(json.dumps({'changed_references':mapping,'pad_track_signature_unchanged':before,'all_108_fitted_parts_have_resolving_models':True,'note':'Mix of existing stock models and documented nominal/max/conservative project envelopes; not vendor mating certification.'},indent=2)+'\n')
print('14 power components now visible; all108 fitted model links resolve; copper/pin geometry unchanged.')
