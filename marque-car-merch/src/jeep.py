# -*- coding: utf-8 -*-
"""Jeep Rally Calendar — 12 iconic Jeeps (USA), cel-shaded Rally style.
Shares the USA stars-&-stripes origin motif with Ford; an army-olive accent and
mostly-4x4 drivetrains (both wheels driven) signal the go-anywhere identity."""
from sil import SIL, GY
from art import PAINT

JEEP_GEOM = {
 "j_wrangler": dict(nose_x=64,tail_x=938,belly=260,nose_y=198,tail_y=184,hood_y=188,
    cowl_x=364,roof_fy=92,roof_ry=92,roof_fx=452,roof_rx=752,deck_x=876,deck_y=186,
    fwx=256,rwx=748,wr=90,belt=158,rear_spare=True),
 "j_cj5": dict(nose_x=76,tail_x=922,belly=258,nose_y=196,tail_y=182,hood_y=186,
    cowl_x=372,roof_fy=96,roof_ry=96,roof_fx=452,roof_rx=690,deck_x=852,deck_y=186,
    fwx=262,rwx=742,wr=86,belt=160,rear_spare=True),
 "j_grandche": dict(nose_x=44,tail_x=956,belly=268,nose_y=212,tail_y=204,hood_y=194,
    cowl_x=348,roof_fy=102,roof_ry=108,roof_fx=444,roof_rx=766,deck_x=892,deck_y=198,
    fwx=252,rwx=760,wr=84,belt=170),
 "j_cherokee": dict(nose_x=54,tail_x=944,belly=264,nose_y=204,tail_y=190,hood_y=192,
    cowl_x=356,roof_fy=98,roof_ry=98,roof_fx=446,roof_rx=748,deck_x=880,deck_y=190,
    fwx=254,rwx=752,wr=84,belt=162),
 "j_gladiator": dict(nose_x=48,tail_x=958,belly=266,nose_y=210,tail_y=222,hood_y=190,
    cowl_x=336,roof_fy=94,roof_ry=94,roof_fx=420,roof_rx=560,deck_x=600,deck_y=214,
    fwx=256,rwx=792,wr=90,belt=160,pickup=True),
 "j_wagoneer": dict(nose_x=52,tail_x=948,belly=262,nose_y=202,tail_y=188,hood_y=190,
    cowl_x=350,roof_fy=96,roof_ry=96,roof_fx=444,roof_rx=792,deck_x=888,deck_y=188,
    fwx=254,rwx=756,wr=84,belt=162),
 "j_renegade": dict(nose_x=58,tail_x=940,belly=272,nose_y=214,tail_y=200,hood_y=198,
    cowl_x=360,roof_fy=106,roof_ry=108,roof_fx=452,roof_rx=724,deck_x=878,deck_y=200,
    fwx=258,rwx=748,wr=78,belt=170),
 "j_compass": dict(nose_x=52,tail_x=950,belly=272,nose_y=214,tail_y=206,hood_y=196,
    cowl_x=354,roof_fy=108,roof_ry=114,roof_fx=452,roof_rx=740,deck_x=886,deck_y=202,
    fwx=254,rwx=756,wr=78,belt=172),
 "j_comanche": dict(nose_x=50,tail_x=958,belly=272,nose_y=214,tail_y=226,hood_y=198,
    cowl_x=332,roof_fy=104,roof_ry=104,roof_fx=414,roof_rx=540,deck_x=576,deck_y=224,
    fwx=254,rwx=792,wr=82,belt=170,pickup=True),
 "j_grandwag": dict(nose_x=40,tail_x=960,belly=266,nose_y=210,tail_y=202,hood_y=192,
    cowl_x=344,roof_fy=98,roof_ry=102,roof_fx=444,roof_rx=792,deck_x=898,deck_y=196,
    fwx=252,rwx=764,wr=84,belt=168),
 "j_willys": dict(nose_x=78,tail_x=924,belly=262,nose_y=200,tail_y=186,hood_y=192,
    cowl_x=386,roof_fy=110,roof_ry=110,roof_fx=470,roof_rx=690,deck_x=858,deck_y=188,
    fwx=266,rwx=746,wr=82,belt=166),
 "j_trackhawk": dict(nose_x=44,tail_x=956,belly=270,nose_y=214,tail_y=206,hood_y=196,
    cowl_x=348,roof_fy=106,roof_ry=112,roof_fx=444,roof_rx=766,deck_x=892,deck_y=200,
    fwx=252,rwx=762,wr=82,belt=172,splitter=True),
}
JEEP_PAINT = {
 "j_wrangler":"#C4392E","j_cj5":"#E4B22E","j_grandche":"#565A5E","j_cherokee":"#2E4A34",
 "j_gladiator":"#2E7CA0","j_wagoneer":"#E7E2D6","j_renegade":"#D07A2A","j_compass":"#AEB2B5",
 "j_comanche":"#C2A265","j_grandwag":"#6A6E72","j_willys":"#5A6633","j_trackhawk":"#8E2230",
}
SIL.update(JEEP_GEOM)
PAINT.update(JEEP_PAINT)

ACCENT="#4B5320"  # Jeep army-olive

def _car(no, key, model, meta, dt="4WD", sky=None, cscale=None):
    d = dict(no=no, key=key, sil=key, make="JEEP", model=model, country="UNITED STATES",
             flag="usa", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1], drivetrain=dt)
    if sky: d["sky"] = sky
    if cscale: d["cscale"] = cscale
    return d

CARS_J = [
 _car(1,"j_wrangler","WRANGLER","RUBICON JL · 2018–", dt="4WD", cscale=1.05),
 _car(2,"j_cj5","CJ-5","1955–1983", dt="4WD", cscale=0.92),
 _car(3,"j_grandche","GRAND CHEROKEE","WK2 · 2011–2021", dt="4WD", cscale=1.03),
 _car(4,"j_cherokee","CHEROKEE XJ","1984–2001", dt="4WD", cscale=1.02),
 _car(5,"j_gladiator","GLADIATOR","JT PICKUP · 2020–", dt="4WD", cscale=1.07),
 _car(6,"j_wagoneer","WAGONEER SJ","1963–1991", dt="4WD", cscale=1.04),
 _car(7,"j_renegade","RENEGADE","TRAILHAWK · 2015–", dt="4WD", cscale=0.94),
 _car(8,"j_compass","COMPASS","2017–", dt="4WD", cscale=1.0),
 _car(9,"j_comanche","COMANCHE MJ","1986–1992", dt="4WD", cscale=1.03),
 _car(10,"j_grandwag","GRAND WAGONEER","2022–", dt="4WD", cscale=1.06),
 _car(11,"j_willys","WILLYS MB","1941–1945", sky="#7C8464", dt="4WD", cscale=0.9),
 _car(12,"j_trackhawk","GRAND CHEROKEE","TRACKHAWK SRT · 2018–", dt="AWD", cscale=1.03),
]

if __name__=="__main__":
    import os
    from styles import car_flat, FONTS, T
    cols=3; cw=1040; ch=440; rows=4; W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_J):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, JEEP_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']} · {c['drivetrain']}",24,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    os.makedirs("out",exist_ok=True); open("out/jeep_shapes.svg","w").write(svg); print("shapes",W,H)
