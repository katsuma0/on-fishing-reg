# -*- coding: utf-8 -*-
"""Lexus Rally Calendar — 12 iconic Lexus (Japan), cel-shaded Rally style.
Shares the Japan rising-sun origin motif; a deep-sapphire accent sets the
premium F-badge tone apart from Toyota/Honda/Acura."""
from sil import SIL, GY
from art import PAINT

LEXUS_GEOM = {
 "lx_lc": dict(nose_x=28,tail_x=958,belly=292,nose_y=256,tail_y=248,hood_y=238,
    cowl_x=452,roof_fy=156,roof_ry=158,roof_fx=540,roof_rx=690,deck_x=892,deck_y=242,
    fwx=254,rwx=780,wr=66,belt=214,splitter=True),
 "lx_lfa": dict(nose_x=30,tail_x=956,belly=294,nose_y=260,tail_y=248,hood_y=248,
    cowl_x=372,roof_fy=168,roof_ry=176,roof_fx=452,roof_rx=616,deck_x=838,deck_y=238,
    fwx=252,rwx=778,wr=64,belt=228,splitter=True),
 "lx_isf": dict(nose_x=34,tail_x=956,belly=288,nose_y=242,tail_y=228,hood_y=214,
    cowl_x=372,roof_fy=134,roof_ry=136,roof_fx=462,roof_rx=702,deck_x=846,deck_y=216,
    fwx=250,rwx=772,wr=66,belt=196),
 "lx_rcf": dict(nose_x=32,tail_x=954,belly=290,nose_y=250,tail_y=238,hood_y=224,
    cowl_x=418,roof_fy=146,roof_ry=150,roof_fx=506,roof_rx=692,deck_x=888,deck_y=230,
    fwx=252,rwx=772,wr=68,belt=204,splitter=True),
 "lx_gsf": dict(nose_x=32,tail_x=958,belly=288,nose_y=242,tail_y=228,hood_y=214,
    cowl_x=378,roof_fy=132,roof_ry=134,roof_fx=470,roof_rx=706,deck_x=852,deck_y=216,
    fwx=250,rwx=776,wr=66,belt=196),
 "lx_ls": dict(nose_x=32,tail_x=960,belly=288,nose_y=240,tail_y=226,hood_y=212,
    cowl_x=380,roof_fy=128,roof_ry=128,roof_fx=474,roof_rx=712,deck_x=820,deck_y=212,
    fwx=250,rwx=780,wr=64,belt=194),
 "lx_sc": dict(nose_x=34,tail_x=950,belly=290,nose_y=250,tail_y=240,hood_y=226,
    cowl_x=428,roof_fy=152,roof_ry=156,roof_fx=516,roof_rx=680,deck_x=884,deck_y=232,
    fwx=252,rwx=772,wr=64,belt=206),
 "lx_rx": dict(nose_x=48,tail_x=952,belly=272,nose_y=216,tail_y=206,hood_y=196,
    cowl_x=356,roof_fy=108,roof_ry=114,roof_fx=452,roof_rx=748,deck_x=890,deck_y=200,
    fwx=254,rwx=758,wr=78,belt=172),
 "lx_gx": dict(nose_x=56,tail_x=944,belly=262,nose_y=202,tail_y=188,hood_y=190,
    cowl_x=352,roof_fy=96,roof_ry=96,roof_fx=444,roof_rx=756,deck_x=882,deck_y=190,
    fwx=254,rwx=752,wr=86,belt=162,rear_spare=True),
 "lx_lx": dict(nose_x=42,tail_x=958,belly=266,nose_y=210,tail_y=202,hood_y=192,
    cowl_x=346,roof_fy=100,roof_ry=104,roof_fx=444,roof_rx=776,deck_x=896,deck_y=196,
    fwx=252,rwx=762,wr=84,belt=168),
 "lx_ux": dict(nose_x=52,tail_x=948,belly=274,nose_y=220,tail_y=210,hood_y=200,
    cowl_x=360,roof_fy=114,roof_ry=120,roof_fx=452,roof_rx=730,deck_x=884,deck_y=204,
    fwx=256,rwx=754,wr=74,belt=178),
 "lx_nx": dict(nose_x=50,tail_x=950,belly=272,nose_y=218,tail_y=208,hood_y=198,
    cowl_x=356,roof_fy=112,roof_ry=118,roof_fx=452,roof_rx=740,deck_x=886,deck_y=202,
    fwx=254,rwx=756,wr=76,belt=176),
}
LEXUS_PAINT = {
 "lx_lc":"#E4A72E","lx_lfa":"#E9E4D8","lx_isf":"#2F73C4","lx_rcf":"#C86A2A",
 "lx_gsf":"#9EA2A5","lx_ls":"#B79A54","lx_sc":"#7A2E3A","lx_rx":"#9E2A2E",
 "lx_gx":"#3E5240","lx_lx":"#6A6E72","lx_ux":"#2E7E86","lx_nx":"#4C6272",
}
SIL.update(LEXUS_GEOM)
PAINT.update(LEXUS_PAINT)

ACCENT="#1F4E82"  # Lexus F deep sapphire

def _car(no, key, model, meta, dt="RWD", sky=None, cscale=None):
    d = dict(no=no, key=key, sil=key, make="LEXUS", model=model, country="JAPAN",
             flag="japan", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1], drivetrain=dt)
    if sky: d["sky"] = sky
    if cscale: d["cscale"] = cscale
    return d

CARS_L = [
 _car(1,"lx_lc","LC 500","GRAND TOURER · 2017–", dt="RWD"),
 _car(2,"lx_lfa","LFA","V10 SUPERCAR · 2010–2012", dt="RWD", sky="#8792A0"),
 _car(3,"lx_isf","IS F","V8 SPORT SEDAN · 2007–2014", dt="RWD"),
 _car(4,"lx_rcf","RC F","V8 COUPE · 2014–", dt="RWD"),
 _car(5,"lx_gsf","GS F","V8 SPORT SEDAN · 2015–2020", dt="RWD"),
 _car(6,"lx_ls","LS 400","FLAGSHIP · 1989–1994", dt="RWD"),
 _car(7,"lx_sc","SC 430","HARDTOP · 2001–2010", dt="RWD"),
 _car(8,"lx_rx","RX","LUXURY CROSSOVER · 2023–", dt="AWD", cscale=1.03),
 _car(9,"lx_gx","GX","BODY-ON-FRAME 4X4 · 2024–", dt="4WD", cscale=1.05),
 _car(10,"lx_lx","LX","FULL-SIZE 4X4 · 2022–", dt="4WD", cscale=1.06),
 _car(11,"lx_ux","UX","COMPACT · 2019–", dt="AWD", cscale=0.94),
 _car(12,"lx_nx","NX","COMPACT SUV · 2022–", dt="AWD", cscale=0.99),
]

if __name__=="__main__":
    import os
    from styles import car_flat, FONTS, T
    cols=3; cw=1040; ch=440; rows=4; W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_L):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, LEXUS_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']} · {c['drivetrain']}",24,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    os.makedirs("out",exist_ok=True); open("out/lexus_shapes.svg","w").write(svg); print("shapes",W,H)
