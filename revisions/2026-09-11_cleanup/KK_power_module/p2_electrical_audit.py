"""Reproducible limit screening, not a substitute for powered qualification."""
from pathlib import Path
import json,math,itertools
out=Path(__file__).resolve().parent/'P2_compact'
# Semitec AT manufacturer table, nominal 103AT resistance in ohms.
rt=[(0,27280),(10,17960),(20,12090),(25,10000),(30,8313),(40,5827),(50,4160)]
def temperature(r):
    for (ta,ra),(tb,rb) in zip(rt,rt[1:]):
        if rb<=r<=ra:
            # Log resistance against inverse absolute temperature interpolation.
            f=math.log(r/ra)/math.log(rb/ra)
            return 1/((1-f)/(ta+273.15)+f/(tb+273.15))-273.15
    raise ValueError(r)
def threshold(rtop,rbot,ratio):
    parallel=rtop*ratio/(1-ratio)
    return 1/(1/parallel-1/rbot)
def r_at(t,rscale,bscale):
    # Manufacturer nominal curve, with a bounded first-order R25/B tolerance
    # perturbation. Not a guaranteed interchangeable thermistor specification.
    for (ta,ra),(tb,rb) in zip(rt,rt[1:]):
        if ta<=t<=tb:
            f=(1/(t+273.15)-1/(ta+273.15))/(1/(tb+273.15)-1/(ta+273.15))
            nominal=ra*math.exp(f*math.log(rb/ra))
            return nominal*rscale*math.exp(3435*(bscale-1)*(1/(t+273.15)-1/298.15))
    raise ValueError(t)
def root_temp(r,rs,bs):
    lo,hi=0.,50.
    for _ in range(60):
        mid=(lo+hi)/2
        if r_at(mid,rs,bs)>r:lo=mid
        else:hi=mid
    return (lo+hi)/2
windows={}
for name,ratios in [('cold',[.245,.25,.255]),('hot',[.12,.125,.13])]:
    vals=[]
    for a,z,q,rs,bs in itertools.product([.999,1.001],[.999,1.001],ratios,[.99,1.01],[.99,1.01]):
        vals.append(root_temp(threshold(31600*a,20000*z,q),rs,bs))
    windows[name]={'nominal_C':temperature(threshold(31600,20000,ratios[1])),
                   'screened_min_C':min(vals),'screened_max_C':max(vals)}
assert windows['cold']['screened_min_C']>0
assert windows['hot']['screened_max_C']<45
data={
 'status':'CALCULATED SCREENING ONLY; NOT POWERED OR BATTERY-SAFETY QUALIFICATION',
 'temperature':windows,
 'thermistor':'Semitec 103AT-2, 10k 1%, B25/85 3435K 1%; bonded and electrically insulated at cell',
 'temperature_method':'Manufacturer nominal R/T table interpolation; first-order R25/B tolerance envelope; comparator and 0.1% resistor corners. Actual thermistor thermal lag and pack limits require bench validation.',
 'NTC_open_ratio_nominal':20000/(31600+20000),
 'NTC_short_ratio':0,
 'charge_A':{'min':797/(2940*1.001),'nominal':890/2940,'max':975/(2940*.999)},
 'USB_C_internal_limit_A':{'min':1500/(1300*1.01),'nominal':1600/1300,'max':1700/(1300*.99)},
 'USB_A_external_limit_A':{'datasheet_min':.034,'typ':.05,'datasheet_max':.066,'note':'At 19.2k programming resistance; resistor tolerance and upstream consumption are additional. No enumeration or suspend support.'},
 'rails_nominal_V':{'MCU_5V':.5*(1+909/101),'LOGIC_3V3':.5*(1+560/100),'ACT_3V2':.5*(1+540/100)},
 'supervisor_nominal_V':{'MCU_5V':.4*(1+1060/100),'LOGIC_3V3':.4*(1+665/100),'ACT_3V2':.4*(1+649/100)},
 'prototype_load_targets_A':{'MCU_5V':.6,'LOGIC_3V3':.4,'ACT_3V2':.5},
 'battery_minimum_requirements':'1S conventional 4.2V Li-ion/LiPo; >=4A continuous discharge; charge capability >=0.34A; supplier documented 0..45C or wider charging range. Physical size/capacity and protection trip coordination not yet selected.',
 'power_interface_pin_order':['MCU_5V','GND','LOGIC_3V3','ACT_3V2'],
 'bench_tests_required':['USB-A current including startup and suspend behavior','USB-C attach current-mode transitions and weak source behavior','Battery simulator UVLO, source switchover and rail sequencing','Output regulation/ripple/transients into actual main-board loads','Short-circuit and fault recovery on a current-limited battery simulator','Charger thermal behavior, NTC open/short and temperature thresholds','Protected battery return isolation; never bond BAT_NEG to GND externally','Converter/charger/FET/fuse temperatures at minimum battery voltage','No simultaneous main ESP32 USB power until reverse-feed path is tested']}
(out/'electrical_screening.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=2))
