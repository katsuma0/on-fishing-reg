# -*- coding: utf-8 -*-
"""Simplified but recognizable national flags, drawn to fit a WxH box at (0,0).

Each flag is framed as a 'stamp' with a cream hairline border + band dividers so
that black/white fields still read on a dark garment. Returns an SVG <g> string.
"""
import math

CREAM = "#ECE7DB"
INK_BLACK = "#23242B"   # lifted 'black' so it stays visible on a dark tee

def _frame(W, H):
    return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" '
            f'stroke="{CREAM}" stroke-width="2.5" stroke-opacity="0.85"/>')

def _clip(uid, W, H):
    return f'<clipPath id="fc{uid}"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>'

def flag(kind, W, H, uid="0"):
    b = [f'<g>', _clip(uid, W, H), f'<g clip-path="url(#fc{uid})">']
    k = kind
    if k == "japan":
        b.append(f'<rect width="{W}" height="{H}" fill="{CREAM}"/>')
        b.append(f'<circle cx="{W/2}" cy="{H/2}" r="{H*0.30}" fill="#BC002D"/>')
    elif k == "germany":
        for i,c in enumerate(("#1A1B22","#DD0000","#FFCE00")):
            b.append(f'<rect x="0" y="{i*H/3}" width="{W}" height="{H/3}" fill="{c}"/>')
    elif k == "italy":
        for i,c in enumerate(("#008C45",CREAM,"#CD212A")):
            b.append(f'<rect x="{i*W/3}" y="0" width="{W/3}" height="{H}" fill="{c}"/>')
    elif k == "france":
        for i,c in enumerate(("#0055A4",CREAM,"#EF4135")):
            b.append(f'<rect x="{i*W/3}" y="0" width="{W/3}" height="{H}" fill="{c}"/>')
    elif k == "russia":
        for i,c in enumerate((CREAM,"#0039A6","#D52B1E")):
            b.append(f'<rect x="0" y="{i*H/3}" width="{W}" height="{H/3}" fill="{c}"/>')
    elif k == "sweden":
        b.append(f'<rect width="{W}" height="{H}" fill="#006AA7"/>')
        cx=W*0.34; cw=H*0.20
        b.append(f'<rect x="0" y="{H/2-cw/2}" width="{W}" height="{cw}" fill="#FECC02"/>')
        b.append(f'<rect x="{cx-cw/2}" y="0" width="{cw}" height="{H}" fill="#FECC02"/>')
    elif k == "uk":
        b.append(f'<rect width="{W}" height="{H}" fill="#012169"/>')
        # white saltire
        b.append(f'<path d="M0 0 L{W} {H} M{W} 0 L0 {H}" stroke="{CREAM}" stroke-width="{H*0.16}"/>')
        # red saltire (thinner, offset via clipped diagonals)
        b.append(f'<path d="M0 0 L{W} {H} M{W} 0 L0 {H}" stroke="#C8102E" stroke-width="{H*0.075}"/>')
        # white cross
        b.append(f'<rect x="{W/2-H*0.11}" y="0" width="{H*0.22}" height="{H}" fill="{CREAM}"/>')
        b.append(f'<rect x="0" y="{H/2-H*0.11}" width="{W}" height="{H*0.22}" fill="{CREAM}"/>')
        # red cross
        b.append(f'<rect x="{W/2-H*0.06}" y="0" width="{H*0.12}" height="{H}" fill="#C8102E"/>')
        b.append(f'<rect x="0" y="{H/2-H*0.06}" width="{W}" height="{H*0.12}" fill="#C8102E"/>')
    elif k == "usa":
        sh = H/13.0
        for i in range(13):
            b.append(f'<rect x="0" y="{i*sh}" width="{W}" height="{sh}" fill="{"#B31942" if i%2==0 else CREAM}"/>')
        cw, ch = W*0.42, sh*7
        b.append(f'<rect x="0" y="0" width="{cw}" height="{ch}" fill="#0A3161"/>')
        for r in range(5):
            for c in range(6):
                sx = cw*(0.09+0.16*c); sy = ch*(0.13+0.19*r)
                b.append(f'<circle cx="{sx}" cy="{sy}" r="{H*0.018}" fill="{CREAM}"/>')
    elif k == "korea":
        b.append(f'<rect width="{W}" height="{H}" fill="{CREAM}"/>')
        cx, cy = W/2, H/2; R = H*0.28
        # taegeuk: blue base disc + red 'comma' on top (canonical two-arc S)
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#0047A0"/>')
        b.append(f'<path d="M {cx-R} {cy} A {R} {R} 0 0 1 {cx+R} {cy} '
                 f'A {R/2} {R/2} 0 0 1 {cx} {cy} A {R/2} {R/2} 0 0 0 {cx-R} {cy} Z" fill="#CD2E3A"/>')
        # four trigrams (three bars each) at the corners
        bl, bt, gap = R*0.62, R*0.14, R*0.11
        def trigram(gx, gy, ang, breaks):
            g=[f'<g transform="translate({gx},{gy}) rotate({ang})">']
            for i,brk in enumerate(breaks):
                yy = (i-1)*(bt+gap)
                if brk:
                    g.append(f'<rect x="{-bl/2}" y="{yy-bt/2}" width="{bl*0.42}" height="{bt}" fill="{INK_BLACK}"/>')
                    g.append(f'<rect x="{bl*0.08}" y="{yy-bt/2}" width="{bl*0.42}" height="{bt}" fill="{INK_BLACK}"/>')
                else:
                    g.append(f'<rect x="{-bl/2}" y="{yy-bt/2}" width="{bl}" height="{bt}" fill="{INK_BLACK}"/>')
            g.append('</g>'); return "".join(g)
        d = R*1.9
        b.append(trigram(cx-d*0.7, cy-d*0.7, 45, [0,0,0]))   # heaven (all solid)
        b.append(trigram(cx+d*0.7, cy-d*0.7, -45, [1,0,1]))
        b.append(trigram(cx-d*0.7, cy+d*0.7, -45, [0,1,0]))
        b.append(trigram(cx+d*0.7, cy+d*0.7, 45, [1,1,1]))   # earth (all broken)
    elif k == "australia":
        b.append(f'<rect width="{W}" height="{H}" fill="#012169"/>')
        # canton union jack (simplified)
        cw, ch = W*0.42, H*0.5
        b.append(f'<g><rect x="0" y="0" width="{cw}" height="{ch}" fill="#012169"/>')
        b.append(f'<path d="M0 0 L{cw} {ch} M{cw} 0 L0 {ch}" stroke="{CREAM}" stroke-width="{ch*0.14}"/>')
        b.append(f'<rect x="{cw/2-ch*0.10}" y="0" width="{ch*0.20}" height="{ch}" fill="{CREAM}"/>')
        b.append(f'<rect x="0" y="{ch/2-ch*0.10}" width="{cw}" height="{ch*0.20}" fill="{CREAM}"/>')
        b.append(f'<rect x="{cw/2-ch*0.05}" y="0" width="{ch*0.10}" height="{ch}" fill="#C8102E"/>')
        b.append(f'<rect x="0" y="{ch/2-ch*0.05}" width="{cw}" height="{ch*0.10}" fill="#C8102E"/></g>')
        # commonwealth star + southern cross (cream stars)
        def star(cx, cy, r, pts=7):
            p=[]
            for i in range(pts*2):
                ang = math.pi/2 + i*math.pi/pts
                rr = r if i%2==0 else r*0.42
                p.append(f"{cx+rr*math.cos(ang):.1f},{cy-rr*math.sin(ang):.1f}")
            return f'<polygon points="{" ".join(p)}" fill="{CREAM}"/>'
        b.append(star(cw*0.5, ch+ (H-ch)*0.42, H*0.075, 7))
        for (sx,sy,r) in [(0.72,0.30,0.05),(0.82,0.55,0.055),(0.72,0.78,0.05),(0.62,0.58,0.04),(0.78,0.44,0.028)]:
            b.append(star(W*sx, H*sy, H*r, 5))
    else:
        b.append(f'<rect width="{W}" height="{H}" fill="#333"/>')
    b.append('</g>')
    b.append(_frame(W, H))
    b.append('</g>')
    return "".join(b)

FLAG_KINDS = ["japan","germany","italy","france","russia","sweden","uk","usa","korea","australia"]

if __name__ == "__main__":
    cols=2; fw=520; fh=340; padx=60; pady=80; lab=44
    rows=(len(FLAG_KINDS)+cols-1)//cols
    W=cols*(fw+padx)+padx; H=rows*(fh+pady)+pady
    body=[f'<rect width="{W}" height="{H}" fill="#171719"/>']
    for i,k in enumerate(FLAG_KINDS):
        gx=padx+(i%cols)*(fw+padx); gy=pady+(i//cols)*(fh+pady)
        body.append(f'<text x="{gx}" y="{gy-14}" fill="#8a867c" font-family="monospace" font-size="26">{k}</text>')
        body.append(f'<g transform="translate({gx},{gy})">{flag(k,fw,fh,uid=str(i))}</g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+"".join(body)+"</svg>"
    open("flag_contact.svg","w").write(svg)
    print("wrote flag_contact.svg", W, H)
