# -*- coding: utf-8 -*-
"""Toyota Rally Calendar — 12 months, one iconic Toyota each, in the Rally style.
Adds Toyota-specific silhouette geometries so the cars actually resemble the
real models, then reuses the Rally panel + calendar frame."""
import os
from sil import SIL, GY
from art import PAINT
import styles
from styles import calendar_page, page_svg, FONTS, PW, PH, car_flat, T

# --- 12 Toyota geometries (1000x380 box, ground GY=322) --------------------
# tuned per model: long-hood GT, boxy AE86, wedge MR2, boxy FJ40, pickup Hilux,
# one-box Prius, hot hatch, notchback sedan, modern sports.
TOYO_GEOM = {
 "gt2000": dict(nose_x=26,tail_x=946,belly=292,nose_y=254,tail_y=250,hood_y=240,
    cowl_x=486,roof_fy=156,roof_ry=162,roof_fx=576,roof_rx=706,deck_x=884,deck_y=244,
    fwx=250,rwx=788,wr=58,belt=218),
 "ae86": dict(nose_x=48,tail_x=950,belly=286,nose_y=246,tail_y=232,hood_y=214,
    cowl_x=388,roof_fy=132,roof_ry=130,roof_fx=474,roof_rx=712,deck_x=884,deck_y=222,
    fwx=254,rwx=760,wr=60,belt=196),
 "celica": dict(nose_x=40,tail_x=950,belly=288,nose_y=248,tail_y=238,hood_y=220,
    cowl_x=402,roof_fy=142,roof_ry=150,roof_fx=488,roof_rx=700,deck_x=902,deck_y=232,
    fwx=250,rwx=768,wr=60,belt=202),
 "supra80": dict(nose_x=34,tail_x=956,belly=290,nose_y=252,tail_y=244,hood_y=234,
    cowl_x=424,roof_fy=150,roof_ry=150,roof_fx=512,roof_rx=676,deck_x=886,deck_y=238,
    fwx=250,rwx=772,wr=62,belt=214,wing=(848,946,152)),
 "mr2": dict(nose_x=40,tail_x=956,belly=290,nose_y=258,tail_y=234,hood_y=248,
    cowl_x=332,roof_fy=166,roof_ry=170,roof_fx=414,roof_rx=566,deck_x=744,deck_y=222,
    fwx=248,rwx=766,wr=58,belt=228),
 "fj40": dict(nose_x=66,tail_x=938,belly=266,nose_y=206,tail_y=188,hood_y=192,
    cowl_x=352,roof_fy=100,roof_ry=100,roof_fx=444,roof_rx=772,deck_x=884,deck_y=188,
    fwx=252,rwx=752,wr=80,belt=166),
 "hilux": dict(nose_x=46,tail_x=958,belly=282,nose_y=226,tail_y=236,hood_y=210,
    cowl_x=316,roof_fy=120,roof_ry=120,roof_fx=392,roof_rx=500,deck_x=540,deck_y=236,
    fwx=248,rwx=786,wr=72,belt=186,pickup=True),
 "prius": dict(nose_x=36,tail_x=956,belly=288,nose_y=234,tail_y=208,hood_y=210,
    cowl_x=320,roof_fy=122,roof_ry=126,roof_fx=436,roof_rx=548,deck_x=902,deck_y=212,
    fwx=246,rwx=770,wr=64,belt=190),
 "yaris": dict(nose_x=54,tail_x=946,belly=286,nose_y=238,tail_y=222,hood_y=210,
    cowl_x=372,roof_fy=122,roof_ry=126,roof_fx=452,roof_rx=706,deck_x=884,deck_y=222,
    fwx=258,rwx=752,wr=66,belt=192),
 "supra90": dict(nose_x=34,tail_x=952,belly=290,nose_y=252,tail_y=246,hood_y=236,
    cowl_x=432,roof_fy=152,roof_ry=156,roof_fx=520,roof_rx=660,deck_x=884,deck_y=240,
    fwx=252,rwx=774,wr=64,belt=214),
 "crown": dict(nose_x=36,tail_x=958,belly=288,nose_y=244,tail_y=228,hood_y=214,
    cowl_x=356,roof_fy=128,roof_ry=128,roof_fx=440,roof_rx=700,deck_x=760,deck_y=210,
    fwx=250,rwx=778,wr=62,belt=196,taxi=True),
 "gr86": dict(nose_x=36,tail_x=952,belly=288,nose_y=252,tail_y=242,hood_y=232,
    cowl_x=442,roof_fy=150,roof_ry=152,roof_fx=526,roof_rx=680,deck_x=884,deck_y=234,
    fwx=252,rwx=772,wr=62,belt=210),
}

TOYO_PAINT = {
 "gt2000":"#B23A2E","ae86":"#2F7D82","celica":"#C96A2B","supra80":"#2C5AA0",
 "mr2":"#E2A61E","fj40":"#40694C","hilux":"#B5642A","prius":"#3E86C0",
 "yaris":"#C6382C","supra90":"#D19A1E","crown":"#23252E","gr86":"#2E7D5B",
}
TOYO_GEOM.update({
 "tacoma": dict(nose_x=40,tail_x=960,belly=284,nose_y=222,tail_y=236,hood_y=202,
    cowl_x=322,roof_fy=108,roof_ry=108,roof_fx=402,roof_rx=522,deck_x=560,deck_y=228,
    fwx=250,rwx=792,wr=80,belt=176,pickup=True),
 "grcorolla": dict(nose_x=50,tail_x=950,belly=286,nose_y=238,tail_y=224,hood_y=212,
    cowl_x=364,roof_fy=122,roof_ry=126,roof_fx=452,roof_rx=706,deck_x=888,deck_y=222,
    fwx=256,rwx=756,wr=70,belt=192),
 "rav4": dict(nose_x=52,tail_x=950,belly=278,nose_y=220,tail_y=210,hood_y=198,
    cowl_x=352,roof_fy=110,roof_ry=116,roof_fx=448,roof_rx=748,deck_x=888,deck_y=204,
    fwx=252,rwx=758,wr=76,belt=176),
 "im": dict(nose_x=48,tail_x=950,belly=286,nose_y=236,tail_y=222,hood_y=210,
    cowl_x=356,roof_fy=124,roof_ry=130,roof_fx=444,roof_rx=688,deck_x=886,deck_y=222,
    fwx=254,rwx=758,wr=64,belt=190),
 "fjcruiser": dict(nose_x=58,tail_x=944,belly=274,nose_y=210,tail_y=196,hood_y=196,
    cowl_x=352,roof_fy=104,roof_ry=106,roof_fx=440,roof_rx=756,deck_x=886,deck_y=200,
    fwx=254,rwx=752,wr=80,belt=168,white_roof=True),
})
TOYO_PAINT.update({"tacoma":"#B5642A","grcorolla":"#C6382C","rav4":"#8B8D90",
                   "im":"#E9E6DE","fjcruiser":"#F2B400"})
SIL.update(TOYO_GEOM)
PAINT.update(TOYO_PAINT)

ACCENT="#E01F26"  # Toyota red — used for the stripe + circled date across the year

def _car(no, key, model, meta, sil=None, sky=None):
    d = dict(no=no, key=key, sil=sil or key, make="TOYOTA", model=model, country="JAPAN",
             flag="japan", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1])
    if sky: d["sky"] = sky
    return d

# 2027 lineup
CARS_T = [
 _car(1,"tacoma","TACOMA","TRD OFF-ROAD · 2024–"),
 _car(2,"ae86","COROLLA AE86","GT-S TRUENO · 1983–1987"),
 _car(3,"grcorolla","GR COROLLA","MORIZO EDITION · 2023–"),
 _car(4,"supra80","SUPRA A80","MK4 TWIN-TURBO · 1993–2002"),
 _car(5,"mr2","MR2","AW11 · 1984–1989"),
 _car(6,"fj40","LAND CRUISER","FJ40 · 1960–1984"),
 _car(7,"fjcruiser","FJ CRUISER","SUN FUSION 4X4 · 2006–2014"),
 _car(8,"prius","PRIUS","XW20 HYBRID · 2003–2009"),
 _car(9,"rav4","RAV4","ADVENTURE · 2019–"),
 _car(10,"crown","CROWN","COMFORT · TOKYO TAXI", sky="#E6C86E"),
 _car(11,"im","iM","COROLLA iM · 2016–2018", sky="#5C87A6"),
 _car(12,"gr86","86","GT86 BOXER · 2012–2021"),
]

if __name__ == "__main__":
    # shape check: 12 flat Toyotas on a neutral ground
    cols=3; cw=1040; ch=440; rows=4
    W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_T):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, TOYO_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']}",26,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    open("out/toyota_shapes.svg","w").write(svg); print("shapes",W,H)
