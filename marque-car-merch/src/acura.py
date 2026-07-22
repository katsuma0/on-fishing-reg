# -*- coding: utf-8 -*-
"""Acura Rally Calendar — 12 iconic Acuras (Japan), cel-shaded Rally style.
Shares the Japan rising-sun origin motif with Toyota/Honda/Lexus so the whole
shelf reads as one family. Acura-only nameplates keep it distinct from Honda."""
from sil import SIL, GY
from art import PAINT

ACURA_GEOM = {
 "a_nsx": dict(nose_x=30,tail_x=958,belly=294,nose_y=262,tail_y=248,hood_y=250,
    cowl_x=352,roof_fy=172,roof_ry=178,roof_fx=436,roof_rx=606,deck_x=822,deck_y=236,
    fwx=250,rwx=778,wr=64,belt=232,splitter=True),
 "a_integs": dict(nose_x=46,tail_x=952,belly=288,nose_y=240,tail_y=226,hood_y=214,
    cowl_x=356,roof_fy=128,roof_ry=132,roof_fx=446,roof_rx=706,deck_x=892,deck_y=224,
    fwx=256,rwx=758,wr=74,belt=192,splitter=True),
 "a_rsx": dict(nose_x=40,tail_x=950,belly=288,nose_y=246,tail_y=232,hood_y=220,
    cowl_x=400,roof_fy=140,roof_ry=146,roof_fx=488,roof_rx=700,deck_x=888,deck_y=228,
    fwx=252,rwx=766,wr=66,belt=200),
 "a_tltyps": dict(nose_x=34,tail_x=956,belly=288,nose_y=242,tail_y=228,hood_y=214,
    cowl_x=372,roof_fy=134,roof_ry=136,roof_fx=464,roof_rx=706,deck_x=852,deck_y=216,
    fwx=250,rwx=772,wr=66,belt=196),
 "a_tsx": dict(nose_x=36,tail_x=950,belly=288,nose_y=244,tail_y=230,hood_y=216,
    cowl_x=380,roof_fy=138,roof_ry=140,roof_fx=470,roof_rx=692,deck_x=838,deck_y=218,
    fwx=252,rwx=768,wr=64,belt=198),
 "a_legend": dict(nose_x=30,tail_x=956,belly=290,nose_y=250,tail_y=238,hood_y=224,
    cowl_x=430,roof_fy=150,roof_ry=150,roof_fx=520,roof_rx=706,deck_x=890,deck_y=228,
    fwx=252,rwx=776,wr=62,belt=204),
 "a_rl": dict(nose_x=34,tail_x=958,belly=288,nose_y=242,tail_y=228,hood_y=214,
    cowl_x=370,roof_fy=130,roof_ry=130,roof_fx=456,roof_rx=696,deck_x=800,deck_y=212,
    fwx=250,rwx=778,wr=64,belt=194),
 "a_ilx": dict(nose_x=38,tail_x=952,belly=288,nose_y=244,tail_y=230,hood_y=216,
    cowl_x=376,roof_fy=136,roof_ry=138,roof_fx=466,roof_rx=690,deck_x=812,deck_y=216,
    fwx=252,rwx=770,wr=62,belt=198),
 "a_tlxs": dict(nose_x=32,tail_x=958,belly=288,nose_y=240,tail_y=224,hood_y=210,
    cowl_x=364,roof_fy=128,roof_ry=132,roof_fx=470,roof_rx=724,deck_x=884,deck_y=214,
    fwx=250,rwx=776,wr=68,belt=192,splitter=True),
 "a_mdx": dict(nose_x=42,tail_x=958,belly=270,nose_y=214,tail_y=206,hood_y=196,
    cowl_x=348,roof_fy=106,roof_ry=112,roof_fx=444,roof_rx=772,deck_x=894,deck_y=202,
    fwx=252,rwx=764,wr=80,belt=172),
 "a_rdx": dict(nose_x=50,tail_x=950,belly=272,nose_y=216,tail_y=208,hood_y=198,
    cowl_x=354,roof_fy=110,roof_ry=116,roof_fx=450,roof_rx=744,deck_x=888,deck_y=202,
    fwx=254,rwx=758,wr=78,belt=174),
 "a_cl": dict(nose_x=32,tail_x=954,belly=290,nose_y=248,tail_y=236,hood_y=222,
    cowl_x=436,roof_fy=148,roof_ry=150,roof_fx=524,roof_rx=700,deck_x=884,deck_y=226,
    fwx=252,rwx=774,wr=64,belt=204),
}
ACURA_PAINT = {
 "a_nsx":"#C21F2A","a_integs":"#285F9E","a_rsx":"#B7BBBE","a_tltyps":"#3C4046",
 "a_tsx":"#E7E2D6","a_legend":"#2E5E48","a_rl":"#6A7686","a_ilx":"#8E2233",
 "a_tlxs":"#1F4C86","a_mdx":"#55595E","a_rdx":"#8A5A34","a_cl":"#5E2A34",
}
SIL.update(ACURA_GEOM)
PAINT.update(ACURA_PAINT)

ACCENT="#A6192E"  # Acura deep performance red

def _car(no, key, model, meta, dt="FWD", sky=None, cscale=None):
    d = dict(no=no, key=key, sil=key, make="ACURA", model=model, country="JAPAN",
             flag="japan", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1], drivetrain=dt)
    if sky: d["sky"] = sky
    if cscale: d["cscale"] = cscale
    return d

CARS_A = [
 _car(1,"a_nsx","NSX","NC1 SUPERCAR · 2016–2022", dt="AWD"),
 _car(2,"a_integs","INTEGRA TYPE S","DE5 · 2024–", dt="FWD"),
 _car(3,"a_rsx","RSX TYPE-S","DC5 · 2002–2006", dt="FWD"),
 _car(4,"a_tltyps","TL TYPE-S","UA7 · 2007–2008", dt="FWD"),
 _car(5,"a_tsx","TSX","CL9 · 2004–2008", dt="FWD"),
 _car(6,"a_legend","LEGEND","COUPE · 1990–1995", dt="FWD"),
 _car(7,"a_rl","RL","SH-AWD · 2005–2012", dt="AWD"),
 _car(8,"a_ilx","ILX","2013–2022", dt="FWD", cscale=0.96),
 _car(9,"a_tlxs","TLX TYPE-S","SH-AWD · 2021–", dt="AWD"),
 _car(10,"a_mdx","MDX","SH-AWD · 2022–", dt="AWD", cscale=1.05),
 _car(11,"a_rdx","RDX","SH-AWD · 2019–", dt="AWD", cscale=1.03),
 _car(12,"a_cl","CL TYPE-S","2001–2003", dt="FWD"),
]

if __name__=="__main__":
    import os
    from styles import car_flat, FONTS, T
    cols=3; cw=1040; ch=440; rows=4; W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_A):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, ACURA_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']} · {c['drivetrain']}",24,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    os.makedirs("out",exist_ok=True); open("out/acura_shapes.svg","w").write(svg); print("shapes",W,H)
