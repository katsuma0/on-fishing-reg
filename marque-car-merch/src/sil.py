# -*- coding: utf-8 -*-
"""Parametric car side-profile silhouette engine (stroked line-art icon family).

Coordinate box per car: 1000 wide x 380 tall.
Ground (wheels rest) at GY. Silhouettes are built as a single closed outline
(top profile + belly with wheel-arch arcs) plus two wheels. All 10 cars share
this construction language so they read as one matched set.
"""

GY = 322            # ground line (wheel bottoms rest here)

def _pts(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

def silhouette(car, stroke="#ECE7DB", accent="#BC002D", sw=7.0):
    """Return an SVG <g> string (in the 1000x380 box) for one car.

    car is a dict of geometry:
      nose_x, tail_x        : horizontal extent of body
      belly                 : y of underbody line
      nose_y, tail_y        : y of front/rear lower fascia top corner
      hood_y                : y of hood top
      cowl_x                : x where windshield begins
      roof_fy, roof_ry      : roof height at front/rear (roofline)
      roof_fx, roof_rx      : x of roof front/rear (cabin)
      deck_x, deck_y        : rear deck corner
      fwx, rwx, wr          : front/rear wheel centre-x and wheel radius
      wing                  : optional (x0,x1,y) tuple -> rear wing
      belt                  : y of beltline (window bottom) for a door line
    """
    nose_x=car["nose_x"]; tail_x=car["tail_x"]; belly=car["belly"]
    nose_y=car["nose_y"]; tail_y=car["tail_y"]; hood_y=car["hood_y"]
    cowl_x=car["cowl_x"]
    rf_y=car["roof_fy"]; rr_y=car["roof_ry"]; rf_x=car["roof_fx"]; rr_x=car["roof_rx"]
    deck_x=car["deck_x"]; deck_y=car["deck_y"]
    fwx=car["fwx"]; rwx=car["rwx"]; wr=car["wr"]
    belt=car.get("belt", rr_y+34)

    # --- upper outline: nose -> hood -> windshield -> roof -> backlight -> deck -> tail
    top = []
    top.append((nose_x, belly))                 # front lower corner
    top.append((nose_x+6, nose_y))              # up the nose fascia
    top.append((cowl_x-70, hood_y+4))           # hood leading edge
    top.append((cowl_x, hood_y))                # cowl / base of windshield
    top.append((rf_x, rf_y))                    # top of windshield / roof front
    top.append((rr_x, rr_y))                    # roof rear
    top.append((deck_x, deck_y))               # backlight base / deck
    top.append((tail_x-4, tail_y))             # rear deck to tail top
    top.append((tail_x, belly))                 # rear lower corner

    # --- belly with wheel arches (travel rear -> front so arcs bump upward)
    aw = wr + 12                                 # arch half-width
    arch_top = belly - (wr + 20)                 # how high the arch cuts up
    d = f"M {top[0][0]:.1f} {top[0][1]:.1f} "
    for x, y in top[1:]:
        d += f"L {x:.1f} {y:.1f} "
    # now on bottom edge at (tail_x, belly); go left to rear arch
    d += f"L {rwx+aw:.1f} {belly:.1f} "
    d += f"A {aw:.1f} {aw:.1f} 0 0 0 {rwx-aw:.1f} {belly:.1f} "   # arch cuts up over rear wheel
    d += f"L {fwx+aw:.1f} {belly:.1f} "
    d += f"A {aw:.1f} {aw:.1f} 0 0 0 {fwx-aw:.1f} {belly:.1f} "   # arch cuts up over front wheel
    d += f"L {nose_x:.1f} {belly:.1f} Z"

    parts = []
    parts.append(f'<path d="{d}" fill="{accent}" fill-opacity="0.10" '
                 f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')

    # greenhouse / window line (a soft cream line following the cabin)
    win = [(cowl_x+8, hood_y+2), (rf_x+6, rf_y+16), (rr_x-6, rr_y+16), (deck_x-10, deck_y-2)]
    parts.append(f'<polyline points="{_pts(win)}" fill="none" stroke="{stroke}" '
                 f'stroke-width="{sw*0.7:.1f}" stroke-opacity="0.55" stroke-linejoin="round" stroke-linecap="round"/>')
    # beltline / door cut
    parts.append(f'<line x1="{cowl_x-30:.1f}" y1="{belt:.1f}" x2="{deck_x:.1f}" y2="{belt:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw*0.6:.1f}" stroke-opacity="0.4"/>')

    # optional rear wing
    if car.get("wing"):
        x0, x1, wy = car["wing"]
        parts.append(f'<rect x="{x0:.1f}" y="{wy:.1f}" width="{x1-x0:.1f}" height="{sw*1.4:.1f}" rx="3" fill="{stroke}"/>')
        parts.append(f'<rect x="{x0+8:.1f}" y="{wy:.1f}" width="{sw:.1f}" height="{belly-wy-40:.1f}" fill="{stroke}" fill-opacity="0.85"/>')
        parts.append(f'<rect x="{x1-8-sw:.1f}" y="{wy:.1f}" width="{sw:.1f}" height="{belly-wy-40:.1f}" fill="{stroke}" fill-opacity="0.85"/>')

    # wheels: tyre ring (cream) + accent hub
    for cx in (fwx, rwx):
        cy = GY - wr
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{wr:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw:.1f}"/>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{wr*0.52:.1f}" fill="none" stroke="{stroke}" stroke-width="{sw*0.7:.1f}" stroke-opacity="0.5"/>')
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{wr*0.14:.1f}" fill="{accent}"/>')

    return "<g>" + "".join(parts) + "</g>"


# --- 10 car geometries -------------------------------------------------------
# Tuned per car to capture signature proportions (hood length, roofline, tail).
SIL = {
 "skyline": dict(nose_x=52,tail_x=956,belly=286,nose_y=244,tail_y=232,hood_y=210,
    cowl_x=372,roof_fy=132,roof_ry=126,roof_fx=452,roof_rx=678,deck_x=804,deck_y=208,
    fwx=252,rwx=756,wr=62,belt=196,wing=(842,940,150)),
 "porsche": dict(nose_x=52,tail_x=948,belly=288,nose_y=248,tail_y=250,hood_y=236,
    cowl_x=322,roof_fy=158,roof_ry=166,roof_fx=406,roof_rx=560,deck_x=916,deck_y=244,
    fwx=236,rwx=760,wr=62,belt=216),
 "countach": dict(nose_x=36,tail_x=964,belly=286,nose_y=262,tail_y=220,hood_y=248,
    cowl_x=306,roof_fy=182,roof_ry=190,roof_fx=376,roof_rx=556,deck_x=752,deck_y=214,
    fwx=244,rwx=760,wr=58,belt=238),
 "etype": dict(nose_x=30,tail_x=940,belly=288,nose_y=252,tail_y=248,hood_y=240,
    cowl_x=524,roof_fy=158,roof_ry=164,roof_fx=612,roof_rx=738,deck_x=892,deck_y=246,
    fwx=252,rwx=782,wr=60,belt=216),
 "corvette": dict(nose_x=34,tail_x=956,belly=288,nose_y=254,tail_y=244,hood_y=240,
    cowl_x=456,roof_fy=156,roof_ry=156,roof_fx=540,roof_rx=684,deck_x=880,deck_y=238,
    fwx=250,rwx=768,wr=60,belt=214),
 "alpine": dict(nose_x=60,tail_x=940,belly=290,nose_y=250,tail_y=238,hood_y=238,
    cowl_x=342,roof_fy=160,roof_ry=162,roof_fx=436,roof_rx=590,deck_x=800,deck_y=232,
    fwx=248,rwx=752,wr=62,belt=214),
 "volvo": dict(nose_x=46,tail_x=950,belly=288,nose_y=244,tail_y=228,hood_y=222,
    cowl_x=400,roof_fy=142,roof_ry=146,roof_fx=490,roof_rx=684,deck_x=846,deck_y=214,
    fwx=252,rwx=760,wr=62,belt=202),
 "ioniq": dict(nose_x=40,tail_x=958,belly=286,nose_y=236,tail_y=200,hood_y=214,
    cowl_x=322,roof_fy=128,roof_ry=132,roof_fx=410,roof_rx=804,deck_x=912,deck_y=202,
    fwx=246,rwx=770,wr=70,belt=196),
 "niva": dict(nose_x=58,tail_x=938,belly=276,nose_y=214,tail_y=182,hood_y=200,
    cowl_x=360,roof_fy=118,roof_ry=118,roof_fx=456,roof_rx=800,deck_x=892,deck_y=182,
    fwx=252,rwx=752,wr=76,belt=176),
 "monaro": dict(nose_x=34,tail_x=956,belly=290,nose_y=250,tail_y=238,hood_y=226,
    cowl_x=436,roof_fy=148,roof_ry=146,roof_fx=524,roof_rx=706,deck_x=876,deck_y=224,
    fwx=250,rwx=772,wr=64,belt=208),
}

if __name__ == "__main__":
    # contact sheet of all 10 silhouettes to eyeball proportions
    order = list(SIL.keys())
    cols, cw, ch = 2, 1040, 420
    rows = (len(order)+cols-1)//cols
    W, H = cols*cw, rows*ch
    body = [f'<rect width="{W}" height="{H}" fill="#171719"/>']
    for i,k in enumerate(order):
        gx=(i%cols)*cw+20; gy=(i//cols)*ch+20
        body.append(f'<g transform="translate({gx},{gy})">')
        body.append(f'<rect width="1000" height="380" fill="#202024" rx="10"/>')
        body.append('<line x1="0" y1="%d" x2="1000" y2="%d" stroke="#3a3a40" stroke-width="2"/>'%(GY,GY))
        body.append(silhouette(SIL[k]))
        body.append(f'<text x="16" y="34" fill="#8a867c" font-family="monospace" font-size="22">{k}</text>')
        body.append('</g>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(body) + "</svg>"
    open("sil_contact.svg","w").write(svg)
    print("wrote sil_contact.svg", W, H)
