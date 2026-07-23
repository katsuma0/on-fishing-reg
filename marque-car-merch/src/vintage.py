# -*- coding: utf-8 -*-
"""MARQUE — Series 02 · VINTAGE.
A 1970s/80s automotive print-ad take on the same archive: a bold grotesque
headline, a blueprint car with dimension callouts, original ad copy, an
understated marque, and a small 'made in' flag stamp — on warm paper with grain.
Reuses the car dataset, silhouettes and flags from Series 01.
"""
import os
from gen import CARS, font_face, esc, PLATE_W, PLATE_H, CX0, CX1, CW
from sil import silhouette, SIL, GY
from flags import flag

PAPER = "#E7DECA"    # warm aged paper
INKV  = "#201D16"    # warm near-black ink
MUTE  = "#7C7462"

FONT_CSS_V = "".join([
    font_face("Grot", 900, "archivo/files/archivo-latin-900-normal.woff2"),
    font_face("Grot", 700, "archivo/files/archivo-latin-700-normal.woff2"),
    font_face("Serif", 400, "libre-baskerville/files/libre-baskerville-latin-400-normal.woff2"),
    font_face("SerifI", 400, "libre-baskerville/files/libre-baskerville-latin-400-italic.woff2"),
])

CMAP = {c["key"]: c for c in CARS}

# per-car: muted spot colour, 3-line headline, ad copy, real-ish dimensions (mm)
VINT = {
 "skyline": dict(spot="#9E3A2E", head=["IT DOESN'T BRAKE","FOR ANYONE'S","REPUTATION."],
   body="Tokyo built a coupe that humbled supercars twice its price, then rated it a modest 276 horsepower and let the world underestimate it. The world learned. All-wheel drive, one twin-turbo conscience, zero apologies.",
   L=4600,H=1360,WB=2665),
 "porsche": dict(spot="#3E5647", head=["HOW TO ARRIVE","BEFORE YOU EVEN","LEFT THE HOUSE."],
   body="Air-cooled, rear-engined, and stubbornly the same shape for thirty years — because when the silhouette is right the first time, you don't call a meeting about it. You just build the next one, quietly faster.",
   L=4245,H=1300,WB=2272),
 "countach": dict(spot="#8A4A2C", head=["DOORS UP.","EXPECTATIONS","EVEN HIGHER."],
   body="A wedge so severe it made the seventies look tame. Twelve cylinders behind your head, no rear visibility worth the name, and a poster on every bedroom wall from Milan to Manila. Practicality was never the assignment.",
   L=4140,H=1070,WB=2450),
 "etype": dict(spot="#3C5142", head=["THE LOVELIEST","CAR EVER MADE.","ENZO SAID SO."],
   body="Nine feet of bonnet, a straight-six that sang, and a price that undercut cars half as quick. Britain's finest hour arrived at 150 miles an hour, wearing racing green and a knowing smile.",
   L=4458,H=1220,WB=2438),
 "corvette": dict(spot="#2F4B6E", head=["CHROME, CURVES,","AND ABSOLUTELY","NO REMORSE."],
   body="A small-block V8, a coke-bottle body, and the confidence of a country that measured horsepower the way it measured everything — generously. America's sports car never once asked for permission.",
   L=4635,H=1245,WB=2489),
 "alpine": dict(spot="#34517E", head=["IT WEIGHS","NEXT TO NOTHING.","IT WINS EVERYTHING."],
   body="Fibreglass, rear-engined and barely there — the little blue berlinette danced through rally stages while heavier machinery understeered into the scenery. Featherweight. Fearless. Unmistakably French.",
   L=3850,H=1130,WB=2100),
 "volvo": dict(spot="#96762C", head=["SAFE HAS NEVER","LOOKED THIS","GOOD IN A HURRY."],
   body="Swedish steel wearing Italian tailoring — a grand tourer so handsome a saint drove one on television. One example ran past three million miles. Beauty, it turns out, can also be built to last.",
   L=4350,H=1280,WB=2450),
 "ioniq": dict(spot="#7A3340", head=["THE FUTURE SHIFTS","GEARS IT DOESN'T","EVEN HAVE."],
   body="Six hundred and forty-one electric horses, a phantom gearbox that's more fun than most real ones, and pixels for headlights. Seoul didn't join the race late. It quietly rewrote the rulebook.",
   L=4715,H=1585,WB=3000),
 "niva": dict(spot="#5B6650", head=["IT WILL OUTLIVE","THE ROAD.","AND PROBABLY YOU."],
   body="Born in 1977 and stubbornly still in production — permanent four-wheel drive, a tractor's soul, and the ability to start at forty below out of sheer spite. Simplicity, done right, is a superpower.",
   L=3720,H=1640,WB=2200),
 "monaro": dict(spot="#7A5A2A", head=["BATHURST BRED.","SUBURBIA","STRICTLY OPTIONAL."],
   body="A V8 coupe from the country that takes its muscle seriously — the lion's answer to Detroit, forged on the mountain at Mount Panorama. Loud, long, and unapologetically Australian.",
   L=4640,H=1350,WB=2819),
}

# ------------------------------------------------------------------ text utils
def txt(x, y, s, size, fam, fill, anchor="start", ls=0, op=1.0, weight=400):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' fill-opacity="{op}"' if op != 1.0 else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}"{a}{l}{o}>{esc(s)}</text>')

def headline(x, y, lines, size, fill, lh):
    spans = "".join(f'<tspan x="{x}" dy="{0 if i==0 else lh}">{esc(t)}</tspan>' for i, t in enumerate(lines))
    return (f'<text x="{x}" y="{y}" font-family="Grot" font-weight="900" font-size="{size}" '
            f'fill="{fill}" letter-spacing="-0.5">{spans}</text>')

def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def paragraph(x, y, text, size, fill, width, lh, fam="SerifI"):
    max_chars = int(width / (size * 0.46))
    lines = wrap(text, max_chars)
    spans = "".join(f'<tspan x="{x}" dy="{0 if i==0 else lh}">{esc(t)}</tspan>' for i, t in enumerate(lines))
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="400" font-size="{size}" '
            f'fill="{fill}">{spans}</text>'), len(lines)

# --------------------------------------------------------------- blueprint car
def blueprint(car, v, ink=INKV, spot="#000"):
    """silhouette in thin blueprint stroke + dimension callouts (length/height/wheelbase)."""
    g = SIL[car["sil"]]
    nose, tail = g["nose_x"], g["tail_x"]
    fwx, rwx, wr = g["fwx"], g["rwx"], g["wr"]
    roof_y = min(g["roof_fy"], g["roof_ry"])
    p = [silhouette(g, stroke=ink, accent=spot, sw=4.0)]
    def dimline_h(x0, x1, y, label):
        s = []
        s.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{spot}" stroke-width="1.6"/>')
        for xx in (x0, x1):
            s.append(f'<line x1="{xx}" y1="{y-9}" x2="{xx}" y2="{y+9}" stroke="{spot}" stroke-width="1.6"/>')
        s.append(f'<rect x="{(x0+x1)/2-52}" y="{y-13}" width="104" height="26" fill="{PAPER}"/>')
        s.append(txt((x0+x1)/2, y+7, label, 20, "Grot", spot, anchor="middle", ls=1, weight=700))
        return "".join(s)
    # overall length (below car)
    p.append(dimline_h(nose, tail, GY+66, f"{v['L']:,} mm".replace(",", " ")))
    # wheelbase (just under car, between hubs)
    p.append(dimline_h(fwx, rwx, GY+26, f"{v['WB']:,} mm".replace(",", " ")))
    # height (left, vertical)
    hx = nose - 30
    p.append(f'<line x1="{hx}" y1="{roof_y}" x2="{hx}" y2="{GY}" stroke="{spot}" stroke-width="1.6"/>')
    for yy in (roof_y, GY):
        p.append(f'<line x1="{hx-9}" y1="{yy}" x2="{hx+9}" y2="{yy}" stroke="{spot}" stroke-width="1.6"/>')
    p.append(f'<g transform="translate({hx-14},{(roof_y+GY)/2}) rotate(-90)">'
             f'{txt(0,6,f"{v[chr(72)]:,} mm".replace(chr(44)," "),20,"Grot",spot,anchor="middle",ls=1,weight=700)}</g>')
    return "".join(p)

# ------------------------------------------------------------------- the plate
def vintage_inner(car, show_ground=True):
    v = VINT[car["key"]]
    spot = v["spot"]
    P = []
    if show_ground:
        P.append(f'<rect width="{PLATE_W}" height="{PLATE_H}" fill="{PAPER}"/>')
        # print grain + soft vignette
        P.append('<defs><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" '
                 'numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
                 '</filter><radialGradient id="vig" cx="50%" cy="46%" r="72%">'
                 '<stop offset="72%" stop-color="#000" stop-opacity="0"/>'
                 '<stop offset="100%" stop-color="#000" stop-opacity="0.10"/></radialGradient></defs>')
        P.append(f'<rect width="{PLATE_W}" height="{PLATE_H}" filter="url(#grain)" opacity="0.05"/>')

    # kicker (series DNA, subtle)
    P.append(txt(CX0, 128, "MARQUE — WORLD MOTOR INDEX", 15, "Grot", MUTE, ls=3, weight=700))
    P.append(txt(CX1, 128, f"SERIES 02 · No. {car['no']:02d}/10", 15, "Grot", spot, anchor="end", ls=2, weight=700))
    P.append(f'<line x1="{CX0}" y1="150" x2="{CX1}" y2="150" stroke="{INKV}" stroke-width="2" stroke-opacity="0.6"/>')

    # headline
    P.append(headline(CX0-3, 246, v["head"], 82, INKV, 82))

    # ghosted marque + blueprint hero
    P.append(txt(PLATE_W/2, 900, car["make"], 190, "Grot", INKV, anchor="middle", ls=-2, op=0.06, weight=900))
    sy, scale = 620, CW/1000.0
    P.append(f'<g transform="translate({CX0},{sy}) scale({scale:.4f})">{blueprint(car, v, ink=INKV, spot=spot)}</g>')

    # ad copy
    para, nlines = paragraph(CX0, 1180, v["body"], 23, INKV, CW, 40)
    P.append(para)

    # footer: rule + marque + model + made-in flag stamp
    fy = 1360
    P.append(f'<line x1="{CX0}" y1="{fy}" x2="{CX1}" y2="{fy}" stroke="{spot}" stroke-width="3"/>')
    P.append(txt(CX0, fy+52, car["make"], 40, "Grot", INKV, ls=1, weight=900))
    P.append(txt(CX0, fy+86, f"{car['model']} · {car['meta'].split(' · ')[-1]}", 20, "Serif", MUTE, ls=0))
    # made-in flag stamp (right)
    fw, fh = 132, 86
    fx, fyy = CX1 - fw, fy + 26
    P.append(f'<g transform="translate({fx},{fyy})">{flag(car["flag"], fw, fh, uid="v"+car["key"])}</g>')
    P.append(txt(CX1, fyy + fh + 26, f"MADE IN {car['country']}", 15, "Grot", INKV, anchor="end", ls=1, weight=700))

    if show_ground:
        P.append(f'<rect width="{PLATE_W}" height="{PLATE_H}" fill="url(#vig)"/>')
        P.append(f'<rect x="40" y="40" width="{PLATE_W-80}" height="{PLATE_H-80}" fill="none" stroke="{INKV}" stroke-width="1.5" stroke-opacity="0.35"/>')
    return "".join(P)

def standalone(car):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PLATE_W}" height="{PLATE_H}" '
            f'viewBox="0 0 {PLATE_W} {PLATE_H}"><defs><style>{FONT_CSS_V}</style></defs>'
            f'{vintage_inner(car)}</svg>')

if __name__ == "__main__":
    os.makedirs("out/vintage", exist_ok=True)
    for car in CARS:
        open(f"out/vintage/{car['no']:02d}_{car['key']}.svg", "w").write(standalone(car))
    print("wrote vintage plates")
