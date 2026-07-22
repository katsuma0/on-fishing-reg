# -*- coding: utf-8 -*-
"""Ford Rally Calendar — 12 iconic Fords (USA), cel-shaded Rally style.
Shows the USA stars-&-stripes origin motif."""
from sil import SIL, GY
from art import PAINT

FORD_GEOM = {
 "mustang": dict(nose_x=32,tail_x=956,belly=290,nose_y=250,tail_y=238,hood_y=224,
    cowl_x=452,roof_fy=146,roof_ry=150,roof_fx=536,roof_rx=712,deck_x=886,deck_y=232,
    fwx=252,rwx=780,wr=66,belt=206,splitter=True),
 "f150": dict(nose_x=36,tail_x=964,belly=268,nose_y=214,tail_y=228,hood_y=196,
    cowl_x=326,roof_fy=98,roof_ry=98,roof_fx=410,roof_rx=520,deck_x=560,deck_y=220,
    fwx=250,rwx=796,wr=92,belt=168,pickup=True),
 "fordgt": dict(nose_x=28,tail_x=958,belly=296,nose_y=264,tail_y=248,hood_y=254,
    cowl_x=356,roof_fy=182,roof_ry=186,roof_fx=436,roof_rx=596,deck_x=812,deck_y=236,
    fwx=250,rwx=776,wr=64,belt=236,splitter=True),
 "bronco": dict(nose_x=60,tail_x=942,belly=262,nose_y=200,tail_y=186,hood_y=190,
    cowl_x=350,roof_fy=94,roof_ry=94,roof_fx=442,roof_rx=760,deck_x=884,deck_y=188,
    fwx=254,rwx=752,wr=88,belt=160),
 "focusrs": dict(nose_x=46,tail_x=952,belly=288,nose_y=238,tail_y=224,hood_y=212,
    cowl_x=360,roof_fy=124,roof_ry=128,roof_fx=448,roof_rx=708,deck_x=890,deck_y=224,
    fwx=256,rwx=756,wr=72,belt=192,splitter=True,wing=(848,948,150)),
 "fiestast": dict(nose_x=58,tail_x=934,belly=288,nose_y=240,tail_y=224,hood_y=216,
    cowl_x=372,roof_fy=128,roof_ry=132,roof_fx=452,roof_rx=706,deck_x=882,deck_y=224,
    fwx=258,rwx=748,wr=64,belt=196),
 "explorer": dict(nose_x=44,tail_x=956,belly=270,nose_y=214,tail_y=206,hood_y=196,
    cowl_x=346,roof_fy=104,roof_ry=110,roof_fx=440,roof_rx=770,deck_x=892,deck_y=200,
    fwx=252,rwx=764,wr=82,belt=172),
 "gt40": dict(nose_x=26,tail_x=966,belly=302,nose_y=272,tail_y=258,hood_y=266,
    cowl_x=376,roof_fy=196,roof_ry=200,roof_fx=452,roof_rx=596,deck_x=812,deck_y=250,
    fwx=246,rwx=784,wr=60,belt=248,splitter=True),
 "escortcos": dict(nose_x=48,tail_x=950,belly=288,nose_y=238,tail_y=224,hood_y=214,
    cowl_x=372,roof_fy=126,roof_ry=130,roof_fx=456,roof_rx=700,deck_x=884,deck_y=224,
    fwx=256,rwx=756,wr=70,belt=196,splitter=True,wing=(842,952,142)),
 "thunderbird": dict(nose_x=28,tail_x=958,belly=292,nose_y=248,tail_y=234,hood_y=222,
    cowl_x=430,roof_fy=148,roof_ry=150,roof_fx=520,roof_rx=712,deck_x=890,deck_y=226,
    fwx=252,rwx=778,wr=64,belt=200),
 "ranger": dict(nose_x=44,tail_x=958,belly=278,nose_y=220,tail_y=232,hood_y=204,
    cowl_x=330,roof_fy=110,roof_ry=110,roof_fx=414,roof_rx=548,deck_x=580,deck_y=226,
    fwx=252,rwx=790,wr=78,belt=180,pickup=True),
 "mache": dict(nose_x=42,tail_x=952,belly=280,nose_y=222,tail_y=210,hood_y=202,
    cowl_x=352,roof_fy=118,roof_ry=124,roof_fx=452,roof_rx=712,deck_x=888,deck_y=206,
    fwx=254,rwx=760,wr=76,belt=182),
}
FORD_PAINT = {
 "mustang":"#C41E1E","f150":"#E0731E","fordgt":"#1E5AA0","bronco":"#3E6B4A",
 "focusrs":"#2A9BD8","fiestast":"#4E8A5A","explorer":"#8A8C8E","gt40":"#5C9AD0",
 "escortcos":"#EDE7D8","thunderbird":"#2FA0A0","ranger":"#2E5C7A","mache":"#7C2E3A",
}
SIL.update(FORD_GEOM)
PAINT.update(FORD_PAINT)

ACCENT="#0057B8"  # Ford blue

def _car(no, key, model, meta, dt="RWD", sky=None, cscale=None):
    d = dict(no=no, key=key, sil=key, make="FORD", model=model, country="UNITED STATES",
             flag="usa", accent=ACCENT, meta=meta, sub=meta.split("· ")[-1], drivetrain=dt)
    if sky: d["sky"] = sky
    if cscale: d["cscale"] = cscale
    return d

CARS_F = [
 _car(1,"mustang","MUSTANG","GT FASTBACK · 1964–", dt="RWD"),
 _car(2,"f150","F-150","RAPTOR · 1975–", dt="4WD", cscale=1.08),
 _car(3,"fordgt","GT","SUPERCAR · 2005/2017", dt="RWD"),
 _car(4,"bronco","BRONCO","4X4 · 1966–", dt="4WD", cscale=1.06),
 _car(5,"focusrs","FOCUS RS","MK3 · 2016–2018", dt="AWD"),
 _car(6,"fiestast","FIESTA ST","HOT HATCH · 2013–2019", dt="FWD", cscale=0.86),
 _car(7,"explorer","EXPLORER","3-ROW SUV · 2020–", dt="AWD", cscale=1.05),
 _car(8,"gt40","GT40","LE MANS · 1966", dt="RWD"),
 _car(9,"escortcos","ESCORT RS","COSWORTH · 1992–1996", dt="AWD", sky="#7C93A6"),
 _car(10,"thunderbird","THUNDERBIRD","1961–1966", dt="RWD"),
 _car(11,"ranger","RANGER","MID-SIZE · 2019–", dt="4WD"),
 _car(12,"mache","MUSTANG MACH-E","EV · 2021–", dt="AWD", cscale=1.02),
]

if __name__=="__main__":
    import os
    from styles import car_flat, FONTS, T
    cols=3; cw=1040; ch=440; rows=4; W,H=cols*cw, rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#B6AD97"/>']
    for i,c in enumerate(CARS_F):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body,_,_=car_flat(c, FORD_PAINT[c["key"]], "#20201C")
        b.append(f'<g transform="translate({gx},{gy})"><rect width="1000" height="400" fill="#E8E1CE" rx="10"/>')
        b.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="#c3bba6" stroke-width="2"/>')
        b.append(T(16,36,f"{c['model']} · {c['drivetrain']}",24,"Grot","#241E16",weight=900))
        b.append(f'<g transform="translate(0,10)">{body}</g></g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>"
    os.makedirs("out",exist_ok=True); open("out/ford_shapes.svg","w").write(svg); print("shapes",W,H)
