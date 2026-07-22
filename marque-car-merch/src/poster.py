# -*- coding: utf-8 -*-
"""Series 03 — ART. Car-hero poster: a tonal 'stage' disc, the illustrated car,
and minimal type (model + origin). Text is deliberately quiet; the car leads."""
import os, math
from gen import CARS, font_face, esc, PLATE_W, PLATE_H
from art import car_art, PAINT, light, dark
from flags import flag
from sil import SIL, GY

CMAP = {c["key"]: c for c in CARS}
PAPER = "#E7DECA"; INKV = "#201D16"; MUTE = "#7C7462"

FONT_CSS_P = "".join([
    font_face("Grot", 900, "archivo/files/archivo-latin-900-normal.woff2"),
    font_face("Grot", 700, "archivo/files/archivo-latin-700-normal.woff2"),
    font_face("Saira", 700, "saira-condensed/files/saira-condensed-latin-700-normal.woff2"),
    font_face("Plex", 400, "ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2"),
])

def txt(x, y, s, size, fam, fill, anchor="start", ls=0, op=1.0, weight=400):
    a=f' text-anchor="{anchor}"' if anchor!="start" else ""
    l=f' letter-spacing="{ls}"' if ls else ""
    o=f' fill-opacity="{op}"' if op!=1.0 else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}"{a}{l}{o}>{esc(s)}</text>')

def poster_inner(car, show_ground=True):
    key=car["key"]; body=PAINT[key]; acc=car["accent"]
    cx, cy, R = 600, 690, 470
    ringw=62; sceneR=R-ringw
    uid=key
    tint_hi=light(body,0.80); tint_lo=light(body,0.40); ringdark=dark(body,0.52)
    P=[]
    if show_ground:
        P.append(f'<rect width="{PLATE_W}" height="{PLATE_H}" fill="{PAPER}"/>')
        P.append('<defs><filter id="pg"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></defs>')
        P.append(f'<rect width="{PLATE_W}" height="{PLATE_H}" filter="url(#pg)" opacity="0.045"/>')
    # defs: scene tonal gradient + arcs
    P.append(f'<defs><radialGradient id="sc{uid}" cx="50%" cy="42%" r="62%">'
             f'<stop offset="0%" stop-color="{tint_hi}"/><stop offset="100%" stop-color="{tint_lo}"/></radialGradient>'
             f'<clipPath id="scc{uid}"><circle cx="{cx}" cy="{cy}" r="{sceneR}"/></clipPath></defs>')
    # ring
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{ringdark}"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{dark(body,0.7)}" stroke-width="2"/>')
    # scene
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{sceneR}" fill="url(#sc{uid})"/>')
    P.append(f'<g clip-path="url(#scc{uid})">')
    # faint concentric detail + horizon
    for rr in (sceneR*0.82, sceneR*0.62):
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.0f}" fill="none" stroke="{light(body,0.2)}" stroke-width="1.5" stroke-opacity="0.25"/>')
    hy=cy+sceneR*0.34
    P.append(f'<rect x="{cx-sceneR}" y="{hy:.0f}" width="{2*sceneR}" height="{sceneR}" fill="{dark(body,0.18)}" fill-opacity="0.28"/>')
    # car
    g=SIL[key]; carw=790.0; sc=carw/1000.0
    ccx=cx-carw/2; ccy=hy-(GY*sc)+6
    P.append(f'<g transform="translate({ccx:.1f},{ccy:.1f}) scale({sc:.4f})">{car_art(car, uid="p"+key)}</g>')
    P.append('</g>')
    # ring text (arced)
    top_path=f"M {cx-(R-30)} {cy} A {R-30} {R-30} 0 0 1 {cx+(R-30)} {cy}"
    bot_path=f"M {cx-(R-30)} {cy} A {R-30} {R-30} 0 0 0 {cx+(R-30)} {cy}"
    P.append(f'<defs><path id="tp{uid}" d="{top_path}"/><path id="bp{uid}" d="{bot_path}"/></defs>')
    P.append(f'<text font-family="Grot" font-weight="700" font-size="26" fill="{PAPER}" letter-spacing="6">'
             f'<textPath href="#tp{uid}" startOffset="50%" text-anchor="middle">MARQUE — WORLD MOTOR INDEX</textPath></text>')
    era = car["meta"].split(" · ")[-1]
    P.append(f'<text font-family="Grot" font-weight="900" font-size="27" fill="{PAPER}" letter-spacing="3">'
             f'<textPath href="#bp{uid}" startOffset="50%" text-anchor="middle">{esc("MADE IN "+car["country"]+" · "+era)}</textPath></text>')
    for ang in (0, 180):
        dx=cx+math.cos(math.radians(ang))*(R-30); dy=cy+math.sin(math.radians(ang))*(R-30)
        P.append(f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="5" fill="{acc}"/>')
    # minimal type below
    ly=cy+R+92
    P.append(f'<g transform="translate({cx-66},{ly-70})">{flag(car["flag"],132,86,uid="pf"+key)}</g>')
    P.append(txt(cx, ly+82, car["model"], 72, "Saira", INKV, anchor="middle", ls=1, weight=700))
    P.append(f'<line x1="{cx-150}" y1="{ly+108}" x2="{cx+150}" y2="{ly+108}" stroke="{acc}" stroke-width="2.5"/>')
    P.append(txt(cx, ly+144, f"{car['make']}   ·   No. {car['no']:02d} / 10", 16, "Plex", MUTE, anchor="middle", ls=2))
    return "".join(P)

def poster_badge(car, cx=500, cy=500, R=460):
    """Just the disc emblem (self-contained, transparent) for garment prints."""
    key=car["key"]; body=PAINT[key]; acc=car["accent"]
    ringw=62; sceneR=R-ringw; uid="b"+key
    tint_hi=light(body,0.80); tint_lo=light(body,0.40); ringdark=dark(body,0.52)
    P=[f'<defs><radialGradient id="sc{uid}" cx="50%" cy="42%" r="62%">'
       f'<stop offset="0%" stop-color="{tint_hi}"/><stop offset="100%" stop-color="{tint_lo}"/></radialGradient>'
       f'<clipPath id="scc{uid}"><circle cx="{cx}" cy="{cy}" r="{sceneR}"/></clipPath></defs>']
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{ringdark}"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{dark(body,0.7)}" stroke-width="2"/>')
    P.append(f'<circle cx="{cx}" cy="{cy}" r="{sceneR}" fill="url(#sc{uid})"/>')
    P.append(f'<g clip-path="url(#scc{uid})">')
    for rr in (sceneR*0.82, sceneR*0.62):
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.0f}" fill="none" stroke="{light(body,0.2)}" stroke-width="1.5" stroke-opacity="0.25"/>')
    hy=cy+sceneR*0.34
    P.append(f'<rect x="{cx-sceneR}" y="{hy:.0f}" width="{2*sceneR}" height="{sceneR}" fill="{dark(body,0.18)}" fill-opacity="0.28"/>')
    carw=790.0; sc=carw/1000.0; ccx=cx-carw/2; ccy=hy-(GY*sc)+6
    P.append(f'<g transform="translate({ccx:.1f},{ccy:.1f}) scale({sc:.4f})">{car_art(car, uid="bp"+key)}</g></g>')
    top_path=f"M {cx-(R-30)} {cy} A {R-30} {R-30} 0 0 1 {cx+(R-30)} {cy}"
    bot_path=f"M {cx-(R-30)} {cy} A {R-30} {R-30} 0 0 0 {cx+(R-30)} {cy}"
    era=car["meta"].split(" · ")[-1]
    P.append(f'<defs><path id="tpb{uid}" d="{top_path}"/><path id="bpb{uid}" d="{bot_path}"/></defs>')
    P.append(f'<text font-family="Grot" font-weight="700" font-size="26" fill="{PAPER}" letter-spacing="6"><textPath href="#tpb{uid}" startOffset="50%" text-anchor="middle">{esc(car["make"]+" · "+car["model"])}</textPath></text>')
    P.append(f'<text font-family="Grot" font-weight="900" font-size="27" fill="{PAPER}" letter-spacing="3"><textPath href="#bpb{uid}" startOffset="50%" text-anchor="middle">{esc("MADE IN "+car["country"]+" · "+era)}</textPath></text>')
    for ang in (0,180):
        dx=cx+math.cos(math.radians(ang))*(R-30); dy=cy+math.sin(math.radians(ang))*(R-30)
        P.append(f'<circle cx="{dx:.0f}" cy="{dy:.0f}" r="5" fill="{acc}"/>')
    return "".join(P)

def standalone(car):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PLATE_W}" height="{PLATE_H}" '
            f'viewBox="0 0 {PLATE_W} {PLATE_H}"><defs><style>{FONT_CSS_P}</style></defs>{poster_inner(car)}</svg>')

if __name__ == "__main__":
    os.makedirs("out/art", exist_ok=True)
    for car in CARS:
        open(f"out/art/{car['no']:02d}_{car['key']}.svg","w").write(standalone(car))
    print("wrote art posters")
