# -*- coding: utf-8 -*-
"""Series 03 — ART. Car-as-hero illustration: filled body with paint shading,
tinted glass + reflection, alloy wheels, ground shadow. Minimal type.
Reuses the SIL geometry from sil.py; upgrades the render from line-art to a
screenprint-style poster illustration."""
from sil import SIL, GY

# ---- colour utils ----------------------------------------------------------
def _hx(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def mix(h1, h2, t):
    a, b = _hx(h1), _hx(h2)
    return '#%02x%02x%02x' % tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))
def light(h, t): return mix(h, '#ffffff', t)
def dark(h, t):  return mix(h, '#000000', t)

# iconic paint per car
PAINT = {
 "skyline":"#1E5AA8","porsche":"#CE1B26","countach":"#E9B200","etype":"#16402A",
 "corvette":"#D2601A","alpine":"#0A57B0","volvo":"#B0281F","ioniq":"#7C848C",
 "niva":"#5E6A3A","monaro":"#E0A21A",
}
GLASS = "#28323C"

def _outline(g):
    nose,tail,belly = g["nose_x"],g["tail_x"],g["belly"]
    nose_y,tail_y,hood_y = g["nose_y"],g["tail_y"],g["hood_y"]
    cowl=g["cowl_x"]; rf_y,rr_y=g["roof_fy"],g["roof_ry"]; rf_x,rr_x=g["roof_fx"],g["roof_rx"]
    deck_x,deck_y=g["deck_x"],g["deck_y"]; fwx,rwx,wr=g["fwx"],g["rwx"],g["wr"]
    top=[(nose,belly),(nose+6,nose_y),(cowl-70,hood_y+4),(cowl,hood_y),
         (rf_x,rf_y),(rr_x,rr_y),(deck_x,deck_y),(tail-4,tail_y),(tail,belly)]
    aw=wr+12
    d=f"M {top[0][0]} {top[0][1]} " + "".join(f"L {x} {y} " for x,y in top[1:])
    d+=f"L {rwx+aw} {belly} A {aw} {aw} 0 0 0 {rwx-aw} {belly} "
    d+=f"L {fwx+aw} {belly} A {aw} {aw} 0 0 0 {fwx-aw} {belly} L {nose} {belly} Z"
    return d

def alloy(cx, cy, r, accent, uid):
    rim = f'<radialGradient id="rim{uid}" cx="42%" cy="38%" r="65%"><stop offset="0%" stop-color="#F2F1EC"/><stop offset="60%" stop-color="#B9B7AE"/><stop offset="100%" stop-color="#6E6C64"/></radialGradient>'
    s=[f'<defs>{rim}</defs>']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111216"/>')                 # tyre
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.92:.1f}" fill="#0a0b0e"/>')          # sidewall
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.64:.1f}" fill="url(#rim{uid})"/>')   # rim
    for i in range(5):                                                                  # spokes
        import math
        a=math.radians(i*72-90)
        x2=cx+math.cos(a)*r*0.58; y2=cy+math.sin(a)*r*0.58
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#3b3a36" stroke-width="{r*0.15:.1f}" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.64:.1f}" fill="none" stroke="#54524c" stroke-width="2.5"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.17:.1f}" fill="{accent}"/>')          # hub cap
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.17:.1f}" fill="none" stroke="#2a2a28" stroke-width="1.6"/>')
    return "".join(s)

def car_art(car, uid="0"):
    g = SIL[car["sil"]]
    body = PAINT[car["key"]]
    acc  = car["accent"]
    lo, dk, deep = light(body,0.34), dark(body,0.28), dark(body,0.5)
    nose,tail,belly = g["nose_x"],g["tail_x"],g["belly"]
    cowl,hood_y = g["cowl_x"],g["hood_y"]
    rf_y,rr_y,rf_x,rr_x = g["roof_fy"],g["roof_ry"],g["roof_fx"],g["roof_rx"]
    deck_x,deck_y,belt = g["deck_x"],g["deck_y"],g["belt"]
    fwx,rwx,wr = g["fwx"],g["rwx"],g["wr"]
    d = _outline(g)
    P=[]
    P.append(f'<defs>'
             f'<linearGradient id="bd{uid}" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="{lo}"/><stop offset="42%" stop-color="{body}"/>'
             f'<stop offset="100%" stop-color="{deep}"/></linearGradient>'
             f'<linearGradient id="gl{uid}" x1="0" y1="0" x2="1" y2="1">'
             f'<stop offset="0%" stop-color="{light(GLASS,0.25)}"/><stop offset="55%" stop-color="{GLASS}"/>'
             f'<stop offset="100%" stop-color="{dark(GLASS,0.25)}"/></linearGradient>'
             f'<filter id="sh{uid}" x="-20%" y="-40%" width="140%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>'
             f'<clipPath id="bc{uid}"><path d="{d}"/></clipPath></defs>')
    # ground shadow
    P.append(f'<ellipse cx="{(nose+tail)/2:.0f}" cy="{GY+16}" rx="{(tail-nose)*0.46:.0f}" ry="15" fill="#000" fill-opacity="0.30" filter="url(#sh{uid})"/>')
    # body
    P.append(f'<path d="{d}" fill="url(#bd{uid})"/>')
    # lower rocker shadow (clipped darker band)
    P.append(f'<g clip-path="url(#bc{uid})"><rect x="{nose}" y="{belly-46}" width="{tail-nose}" height="60" fill="{deep}" fill-opacity="0.55"/>'
             f'<ellipse cx="{fwx}" cy="{GY-wr}" rx="{wr+20}" ry="{wr+20}" fill="#000" fill-opacity="0.12"/>'
             f'<ellipse cx="{rwx}" cy="{GY-wr}" rx="{wr+20}" ry="{wr+20}" fill="#000" fill-opacity="0.12"/></g>')
    # glass
    glass=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {rr_x} {rr_y} L {deck_x} {deck_y} L {cowl} {belt} Z"
    P.append(f'<path d="{glass}" fill="url(#gl{uid})"/>')
    # glass reflection streak
    P.append(f'<g clip-path="url(#bc{uid})"></g>')
    P.append(f'<path d="{glass}" fill="none" stroke="{dark(body,0.35)}" stroke-width="3"/>')
    rx0=cowl+ (rf_x-cowl)*0.3
    P.append(f'<polygon points="{cowl+22},{belt-4} {cowl+70},{rf_y+18} {cowl+120},{rf_y+18} {cowl+50},{belt-4}" fill="#ffffff" fill-opacity="0.12"/>')
    # top highlight streak
    P.append(f'<path d="M {cowl-60} {hood_y+6} L {cowl} {hood_y+3} L {rf_x} {rf_y+3} L {rr_x} {rr_y+3}" fill="none" stroke="{lo}" stroke-width="5" stroke-opacity="0.6" stroke-linecap="round"/>')
    # character line
    P.append(f'<line x1="{nose+40}" y1="{belt+30}" x2="{deck_x}" y2="{belt+26}" stroke="{lo}" stroke-width="3" stroke-opacity="0.4"/>')
    # headlight + taillight
    P.append(f'<ellipse cx="{nose+22}" cy="{(g["nose_y"]+belly)/2-6}" rx="16" ry="12" fill="#FFF3D0" fill-opacity="0.9"/>')
    P.append(f'<rect x="{tail-30}" y="{(g["tail_y"]+belly)/2-10}" width="20" height="16" rx="3" fill="{acc}"/>')
    # body outline
    P.append(f'<path d="{d}" fill="none" stroke="{dark(body,0.55)}" stroke-width="3.5" stroke-linejoin="round"/>')
    # wheels
    P.append(alloy(fwx, GY-wr, wr, acc, uid+"f"))
    P.append(alloy(rwx, GY-wr, wr, acc, uid+"r"))
    # wheel arch trim
    aw=wr+12
    for cx in (fwx,rwx):
        P.append(f'<path d="M {cx-aw} {belly} A {aw} {aw} 0 0 1 {cx+aw} {belly}" fill="none" stroke="{dark(body,0.55)}" stroke-width="3.5"/>')
    return "<g>"+"".join(P)+"</g>"

if __name__ == "__main__":
    from sil import GY as _
    order=list(SIL.keys())
    cols,cw,ch=2,1060,440
    rows=(len(order)+cols-1)//cols
    W,H=cols*cw,rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#Dcd3bf"/>']
    class C(dict):
        pass
    for i,k in enumerate(order):
        car={"sil":k,"key":k,"accent":"#E4384C"}
        gx=(i%cols)*cw+30; gy=(i//cols)*ch+30
        b.append(f'<g transform="translate({gx},{gy})">')
        b.append(f'<rect width="1000" height="400" fill="#E7DECA" rx="10"/>')
        b.append(f'<text x="16" y="34" fill="#8a867c" font-family="monospace" font-size="22">{k}</text>')
        b.append(car_art(car, uid=str(i)))
        b.append('</g>')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+"".join(b)+"</svg>"
    open("art_contact.svg","w").write(svg)
    print("wrote art_contact.svg", W, H)
