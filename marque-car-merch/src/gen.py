# -*- coding: utf-8 -*-
"""MARQUE — World Motor Index.
Generates a uniform 'archive plate' design per car (print-ready SVG), plus a
self-contained HTML gallery with garment + calendar mockups.

Design DNA shared by every product (so the whole line reads as one series):
  frame + corner crop-marks, MARQUE housemark, No. XX/10 registry,
  full-width MAKE/MODEL wordmark, national-flag stamp, mono spec grid,
  footer registry line + barcode motif, one type system (Saira Condensed + IBM Plex Mono).
Per-car variation: model, flag, accent, silhouette, specs, entry number.
"""
import base64, os, hashlib
from sil import silhouette, SIL, GY
from flags import flag

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(HERE, "node_modules", "@fontsource")

# ---- palette ---------------------------------------------------------------
INK     = "#14151A"   # dark garment ground (near-black, blue bias)
CREAM   = "#ECE7DB"   # primary ink on dark
MUTE    = "#9A9488"   # muted cream
LINE    = "#ECE7DB"   # hairlines (used at low opacity)

PLATE_W, PLATE_H = 1200, 1600
CX0, CX1 = 96, 1104           # content left / right
CW = CX1 - CX0                # content width 1008

def _b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def font_face(family, weight, fname):
    p = os.path.join(FONTDIR, fname)
    return (f"@font-face{{font-family:'{family}';font-style:normal;font-weight:{weight};"
            f"font-display:block;src:url(data:font/woff2;base64,{_b64(p)}) format('woff2');}}")

FONT_CSS = "".join([
    font_face("Saira", 600, "saira-condensed/files/saira-condensed-latin-600-normal.woff2"),
    font_face("Saira", 800, "saira-condensed/files/saira-condensed-latin-800-normal.woff2"),
    font_face("Plex", 400, "ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2"),
    font_face("Plex", 600, "ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2"),
])

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---- data ------------------------------------------------------------------
CARS = [
 dict(key="skyline", no=1, make="NISSAN", model="SKYLINE GT-R", msize=112,
   country="JAPAN", iso="JP", flag="japan", accent="#E4384C", sil="skyline",
   meta="GRAN TURISMO · TYPE BNR34 · 1999–2002",
   tag="ARCHIVE ENTRY", blurb=["ALL-WHEEL-DRIVE GIANT-SLAYER;","THE RB26 LEGEND FROM SKUNKWORKS."],
   specs=[("ENGINE","RB26DETT 2.6"),("LAYOUT","FR · AWD"),("OUTPUT","276 HP"),
          ("0–100 KM/H","4.9 S"),("TOP SPEED","265 KM/H"),("BUILT","1999–02")]),
 dict(key="porsche", no=2, make="PORSCHE", model="911 CARRERA", msize=110,
   country="GERMANY", iso="DE", flag="germany", accent="#E7B10A", sil="porsche",
   meta="TYPE 993 · AIR-COOLED FLAT-SIX · 1993–1998",
   tag="ARCHIVE ENTRY", blurb=["THE LAST AIR-COOLED 911;","REAR-ENGINED, RUTHLESSLY RESOLVED."],
   specs=[("ENGINE","3.6 FLAT-6"),("LAYOUT","RR · RWD"),("OUTPUT","272 HP"),
          ("0–100 KM/H","5.3 S"),("TOP SPEED","270 KM/H"),("BUILT","1993–98")]),
 dict(key="countach", no=3, make="LAMBORGHINI", model="COUNTACH", msize=132,
   country="ITALY", iso="IT", flag="italy", accent="#22A555", sil="countach",
   meta="LP5000 QUATTROVALVOLE · V12 · 1974–1990",
   tag="ARCHIVE ENTRY", blurb=["THE POSTER ON EVERY WALL;","BERTONE'S WEDGE OF PURE EXCESS."],
   specs=[("ENGINE","5.2 V12"),("LAYOUT","MID · RWD"),("OUTPUT","449 HP"),
          ("0–100 KM/H","4.9 S"),("TOP SPEED","295 KM/H"),("BUILT","1974–90")]),
 dict(key="etype", no=4, make="JAGUAR", model="E-TYPE", msize=150,
   country="UNITED KINGDOM", iso="GB", flag="uk", accent="#D8452F", sil="etype",
   meta="SERIES 1 · 4.2 XK · 1961–1975",
   tag="ARCHIVE ENTRY", blurb=["‘THE MOST BEAUTIFUL CAR","EVER MADE’ — ENZO FERRARI."],
   specs=[("ENGINE","4.2 I6"),("LAYOUT","FR · RWD"),("OUTPUT","265 HP"),
          ("0–100 KM/H","7.0 S"),("TOP SPEED","241 KM/H"),("BUILT","1961–75")]),
 dict(key="corvette", no=5, make="CHEVROLET", model="CORVETTE", msize=132,
   country="UNITED STATES", iso="US", flag="usa", accent="#3E7BD1", sil="corvette",
   meta="C3 STINGRAY · SMALL-BLOCK V8 · 1968–1982",
   tag="ARCHIVE ENTRY", blurb=["CHROME-BUMPER COKE-BOTTLE;","AMERICA'S SPORTS CAR, PEAK SWAGGER."],
   specs=[("ENGINE","5.7 V8"),("LAYOUT","FR · RWD"),("OUTPUT","300 HP"),
          ("0–100 KM/H","6.5 S"),("TOP SPEED","225 KM/H"),("BUILT","1968–82")]),
 dict(key="alpine", no=6, make="ALPINE", model="A110", msize=150,
   country="FRANCE", iso="FR", flag="france", accent="#2F6BE6", sil="alpine",
   meta="BERLINETTE · REAR-ENGINE · 1961–1977",
   tag="ARCHIVE ENTRY", blurb=["THE RALLY GIANT-KILLER;","FIBREGLASS, FEATHERWEIGHT, FEARLESS."],
   specs=[("ENGINE","1.6 I4"),("LAYOUT","RR · RWD"),("OUTPUT","138 HP"),
          ("0–100 KM/H","6.3 S"),("TOP SPEED","210 KM/H"),("BUILT","1961–77")]),
 dict(key="volvo", no=7, make="VOLVO", model="P1800", msize=150,
   country="SWEDEN", iso="SE", flag="sweden", accent="#F2C200", sil="volvo",
   meta="GRAND TOURER · 2.0 I4 · 1961–1973",
   tag="ARCHIVE ENTRY", blurb=["THE SAINT'S COUPE;","SWEDISH STEEL, ITALIAN LINES."],
   specs=[("ENGINE","2.0 I4"),("LAYOUT","FR · RWD"),("OUTPUT","115 HP"),
          ("0–100 KM/H","9.5 S"),("TOP SPEED","185 KM/H"),("BUILT","1961–73")]),
 dict(key="ioniq", no=8, make="HYUNDAI", model="IONIQ 5 N", msize=118,
   country="SOUTH KOREA", iso="KR", flag="korea", accent="#E23A56", sil="ioniq",
   meta="DUAL-MOTOR EV · N GRIN BOOST · 2024–",
   tag="ARCHIVE ENTRY", blurb=["THE EV THAT SHIFTS GEARS;","641 HORSES OF PIXELATED FURY."],
   specs=[("ENGINE","DUAL E-MOTOR"),("LAYOUT","AWD"),("OUTPUT","641 HP"),
          ("0–100 KM/H","3.4 S"),("TOP SPEED","260 KM/H"),("BUILT","2024–")]),
 dict(key="niva", no=9, make="LADA", model="NIVA", msize=150,
   country="USSR · RUSSIA", iso="SU", flag="russia", accent="#4C74D6", sil="niva",
   meta="VAZ-2121 · PERMANENT 4×4 · 1977–PRESENT",
   tag="ARCHIVE ENTRY", blurb=["THE PEASANT'S LAND ROVER;","UNSTOPPABLE, UNKILLABLE, UNBOTHERED."],
   specs=[("ENGINE","1.7 I4"),("LAYOUT","F · 4WD"),("OUTPUT","83 HP"),
          ("0–100 KM/H","17 S"),("TOP SPEED","140 KM/H"),("BUILT","1977–")]),
 dict(key="monaro", no=10, make="HOLDEN", model="MONARO", msize=140,
   country="AUSTRALIA", iso="AU", flag="australia", accent="#E8A21F", sil="monaro",
   meta="GTS 350 · SMALL-BLOCK V8 · 1968–1977",
   tag="ARCHIVE ENTRY", blurb=["BATHURST-BRED MUSCLE;","THE LION'S ANSWER TO DETROIT."],
   specs=[("ENGINE","5.7 V8"),("LAYOUT","FR · RWD"),("OUTPUT","300 HP"),
          ("0–100 KM/H","6.3 S"),("TOP SPEED","215 KM/H"),("BUILT","1968–77")]),
]

# ---- plate builder ---------------------------------------------------------
def T(x, y, s, size, fam, weight, fill, anchor="start", ls=0, op=1.0, tl=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    o = f' fill-opacity="{op}"' if op != 1.0 else ""
    t = f' textLength="{tl}" lengthAdjust="spacingAndGlyphs"' if tl else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}"{a}{l}{o}{t}>{esc(s)}</text>')

def barcode(x_end, y, seed, h=26):
    rnd = hashlib.md5(seed.encode()).digest()
    widths = [2 + (b % 6) for b in rnd[:22]]
    out = []
    x = x_end - sum(w + 3 for w in widths)
    for i, w in enumerate(widths):
        if i % 2 == 0:
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w}" height="{h}" fill="{CREAM}" fill-opacity="0.8"/>')
        x += w + 3
    return "".join(out)

def plate_inner(car, ground=INK, ink=CREAM, mute=MUTE, show_ground=True):
    a = car["accent"]
    P = []
    if show_ground:
        P.append(f'<rect x="0" y="0" width="{PLATE_W}" height="{PLATE_H}" fill="{ground}"/>')
    # frame + corner crop marks
    P.append(f'<rect x="54" y="54" width="{PLATE_W-108}" height="{PLATE_H-108}" fill="none" stroke="{ink}" stroke-width="2" stroke-opacity="0.32"/>')
    for (cx, cy) in [(54,54),(PLATE_W-54,54),(54,PLATE_H-54),(PLATE_W-54,PLATE_H-54)]:
        P.append(f'<path d="M{cx-16} {cy} H{cx+16} M{cx} {cy-16} V{cy+16}" stroke="{a}" stroke-width="2.4"/>')

    # ---- header
    P.append(T(CX0, 150, "MARQUE", 46, "Saira", 800, ink, ls=1))
    P.append(T(CX0+2, 178, "WORLD MOTOR INDEX", 15, "Plex", 400, mute, ls=6))
    P.append(T(CX1, 132, "SERIES 01 — FIELD GUIDE", 13, "Plex", 400, mute, anchor="end", ls=2))
    P.append(T(CX1, 172, f"No. {car['no']:02d} / 10", 30, "Saira", 800, a, anchor="end", ls=1))
    P.append(f'<line x1="{CX0}" y1="210" x2="{CX1}" y2="210" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.28"/>')

    # ---- hero wordmark
    P.append(T(CX0+3, 278, car["make"], 24, "Plex", 600, a, ls=8))
    P.append(T(CX0-4, 432, car["model"], car["msize"], "Saira", 800, ink, ls=0))
    P.append(T(CX0+3, 486, car["meta"], 17, "Plex", 400, mute, ls=2))
    P.append(f'<line x1="{CX0}" y1="520" x2="{CX1}" y2="520" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.28"/>')

    # ---- mid band: left dossier + right flag stamp
    # flag stamp
    fw, fh = 360, 232
    fx, fy = CX1 - fw, 566
    P.append(f'<g transform="translate({fx},{fy})">{flag(car["flag"], fw, fh, uid=car["key"])}</g>')
    P.append(T(fx, fy + fh + 40, car["country"], 30, "Saira", 600, ink, ls=1))
    P.append(T(CX1, fy + fh + 40, f"ORIGIN · {car['iso']}", 15, "Plex", 400, mute, anchor="end", ls=2))
    # left dossier
    P.append(T(CX0+3, 590, car["tag"], 13, "Plex", 400, mute, ls=4))
    P.append(T(CX0-6, 792, f"{car['no']:02d}", 235, "Saira", 800, a, op=0.16))
    by = 700
    for i, ln in enumerate(car["blurb"]):
        P.append(T(CX0+3, by + i*30, ln, 18, "Plex", 400, ink, ls=1, op=0.85))

    # ---- silhouette band (full width)
    sy = 900
    scale = CW / 1000.0
    P.append(f'<g transform="translate({CX0},{sy}) scale({scale:.4f})">')
    P.append(f'<line x1="0" y1="{GY}" x2="1000" y2="{GY}" stroke="{ink}" stroke-width="2" stroke-opacity="0.22"/>')
    P.append(silhouette(SIL[car["sil"]], stroke=ink, accent=a, sw=7.5))
    P.append('</g>')

    # ---- spec grid: 3 cols x 2 rows
    gy0, gy1 = 1248, 1436
    P.append(f'<line x1="{CX0}" y1="{gy0}" x2="{CX1}" y2="{gy0}" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.28"/>')
    P.append(f'<line x1="{CX0}" y1="{gy1}" x2="{CX1}" y2="{gy1}" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.28"/>')
    colw = CW / 3.0
    rows = [gy0, (gy0+gy1)/2]
    for ci in range(3):
        cx = CX0 + ci*colw
        if ci > 0:
            P.append(f'<line x1="{cx}" y1="{gy0}" x2="{cx}" y2="{gy1}" stroke="{ink}" stroke-width="1.5" stroke-opacity="0.18"/>')
    for idx, (label, val) in enumerate(car["specs"]):
        ci, ri = idx % 3, idx // 3
        cx = CX0 + ci*colw + 16
        ry = rows[ri]
        P.append(T(cx, ry + 34, label, 13, "Plex", 400, mute, ls=2))
        P.append(T(cx-2, ry + 78, val, 38, "Saira", 600, ink, ls=0))

    # ---- footer registry
    P.append(f'<line x1="{CX0}" y1="1470" x2="{CX1}" y2="1470" stroke="{a}" stroke-width="2.5"/>')
    foot = f"MARQUE™   ·   WORLD MOTOR INDEX   ·   ORIGIN {car['country']}   ·   PLATE {car['iso']}-{car['no']:02d}"
    P.append(T(CX0, 1506, foot, 14, "Plex", 400, mute, ls=1))
    P.append(barcode(CX1, 1490, car["key"], h=26))
    return "".join(P)

def standalone_svg(car):
    inner = plate_inner(car)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PLATE_W}" height="{PLATE_H}" '
            f'viewBox="0 0 {PLATE_W} {PLATE_H}"><defs><style>{FONT_CSS}'
            f'text{{dominant-baseline:auto}}</style></defs>{inner}</svg>')

if __name__ == "__main__":
    os.makedirs("out/svg", exist_ok=True)
    for car in CARS:
        svg = standalone_svg(car)
        open(f"out/svg/{car['no']:02d}_{car['key']}.svg", "w").write(svg)
    print("wrote", len(CARS), "plate SVGs to out/svg/")
