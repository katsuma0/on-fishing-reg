# -*- coding: utf-8 -*-
"""Honda Rally Calendar 2027 — 12 iconic Hondas, cel-shaded Rally style.
Adds Honda-specific silhouettes; reuses the Rally panel + calendar frame."""
import os
from sil import SIL, GY
from art import PAINT
import styles
from styles import calendar_page, page_svg, FONTS, PW, PH, car_flat, T

HONDA_GEOM = {
 "nsx": dict(nose_x=30,tail_x=958,belly=294,nose_y=262,tail_y=246,hood_y=252,
    cowl_x=346,roof_fy=176,roof_ry=182,roof_fx=430,roof_rx=592,deck_x=812,deck_y=232,
    fwx=250,rwx=776,wr=64,belt=234,splitter=True),
 "civicr": dict(nose_x=44,tail_x=952,belly=290,nose_y=240,tail_y=226,hood_y=214,
    cowl_x=356,roof_fy=126,roof_ry=130,roof_fx=446,roof_rx=708,deck_x=890,deck_y=224,
    fwx=254,rwx=756,wr=72,belt=192,splitter=True,wing=(848,948,150)),
 "s2000": dict(nose_x=30,tail_x=950,belly=292,nose_y=256,tail_y=246,hood_y=240,
    cowl_x=500,roof_fy=202,roof_ry=206,roof_fx=574,roof_rx=680,deck_x=852,deck_y=240,
    fwx=254,rwx=784,wr=62,belt=226,splitter=True),
 "integra": dict(nose_x=36,tail_x=952,belly=290,nose_y=250,tail_y=238,hood_y=224,
    cowl_x=420,roof_fy=146,roof_ry=150,roof_fx=506,roof_rx=690,deck_x=886,deck_y=232,
    fwx=252,rwx=772,wr=64,belt=204,splitter=True),
 "crx": dict(nose_x=60,tail_x=930,belly=288,nose_y=244,tail_y=222,hood_y=222,
    cowl_x=372,roof_fy=138,roof_ry=140,roof_fx=452,roof_rx=712,deck_x=884,deck_y=222,
    fwx=258,rwx=748,wr=62,belt=198),
 "prelude": dict(nose_x=30,tail_x=952,belly=290,nose_y=248,tail_y=236,hood_y=228,
    cowl_x=444,roof_fy=150,roof_ry=154,roof_fx=524,roof_rx=690,deck_x=888,deck_y=230,
    fwx=250,rwx=774,wr=62,belt=206),
 "beat": dict(nose_x=72,tail_x=926,belly=290,nose_y=256,tail_y=248,hood_y=250,
    cowl_x=362,roof_fy=188,roof_ry=192,roof_fx=442,roof_rx=584,deck_x=800,deck_y=246,
    fwx=270,rwx=742,wr=58,belt=226,splitter=True),
 "ridgeline": dict(nose_x=42,tail_x=958,belly=278,nose_y=222,tail_y=232,hood_y=206,
    cowl_x=330,roof_fy=110,roof_ry=112,roof_fx=414,roof_rx=560,deck_x=596,deck_y=224,
    fwx=252,rwx=790,wr=76,belt=182,pickup=True),
 "crv": dict(nose_x=52,tail_x=948,belly=272,nose_y=216,tail_y=208,hood_y=198,
    cowl_x=356,roof_fy=110,roof_ry=116,roof_fx=452,roof_rx=744,deck_x=886,deck_y=202,
    fwx=254,rwx=756,wr=78,belt=174),
 "odyssey": dict(nose_x=40,tail_x=958,belly=280,nose_y=214,tail_y=210,hood_y=200,
    cowl_x=300,roof_fy=104,roof_ry=104,roof_fx=420,roof_rx=830,deck_x=922,deck_y=206,
    fwx=248,rwx=792,wr=72,belt=180),
 "hondae": dict(nose_x=76,tail_x=922,belly=286,nose_y=228,tail_y=222,hood_y=214,
    cowl_x=360,roof_fy=124,roof_ry=126,roof_fx=452,roof_rx=712,deck_x=884,deck_y=222,
    fwx=262,rwx=746,wr=66,belt=192),
 "accord": dict(nose_x=34,tail_x=958,belly=288,nose_y=242,tail_y=228,hood_y=214,
    cowl_x=372,roof_fy=134,roof_ry=134,roof_fx=470,roof_rx=690,deck_x=760,deck_y=214,
    fwx=250,rwx=776,wr=62,belt=196),
}
HONDA_PAINT = {
 "nsx":"#C22030","civicr":"#EDE7D8","s2000":"#2C5C96","integra":"#E6B21C",
 "crx":"#2E8C7A","prelude":"#C46A2E","beat":"#D63A3A","ridgeline":"#86888C",
 "crv":"#4E8A5A","odyssey":"#7C2E3A","hondae":"#46A0A0","accord":"#2A4A78",
}
SIL.update(HONDA_GEOM)
PAINT.update(HONDA_PAINT)

ACCENT="#E1051E"  # Honda red — stripe + circled date

def _car(no, key, model, meta, sky=None, cscale=None, dt="AWD"):
    d = dict(no=no, key=key, sil=key, make="HONDA", model=model, country="JAPAN",
             flag="japan", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1], drivetrain=dt)
    if sky: d["sky"] = sky
    if cscale: d["cscale"] = cscale
    return d

CARS_H = [
 _car(1,"nsx","NSX","NA1 · 1990–2005", dt="RWD"),
 _car(2,"civicr","CIVIC TYPE R","FL5 · 2023–", sky="#6E86A0", dt="FWD"),
 _car(3,"s2000","S2000","AP1 ROADSTER · 1999–2009", dt="RWD"),
 _car(4,"integra","INTEGRA TYPE R","DC2 · 1995–2001", dt="FWD"),
 _car(5,"crx","CR-X","SiR · 1987–1991", cscale=0.90, dt="FWD"),
 _car(6,"prelude","PRELUDE","BB · 1991–1996", dt="FWD"),
 _car(7,"beat","BEAT","PP1 KEI · 1991–1996", cscale=0.72, dt="RWD"),
 _car(8,"ridgeline","RIDGELINE","UNIBODY · 2005–", cscale=1.05, dt="AWD"),
 _car(9,"crv","CR-V","2018–", cscale=1.04, dt="AWD"),
 _car(10,"odyssey","ODYSSEY","2018–", cscale=1.06, dt="FWD"),
 _car(11,"hondae","HONDA e","EV · 2020–2024", cscale=0.86, dt="RWD"),
 _car(12,"accord","ACCORD","2018–", dt="FWD"),
]

if __name__ == "__main__":
    cols=3; cw=1040; ch=440; rows=4
    W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_H):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, HONDA_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']}",26,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    open("out/honda_shapes.svg","w").write(svg); print("shapes",W,H)
