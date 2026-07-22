# -*- coding: utf-8 -*-
"""Calendar-first style exploration. One shared calendar frame + several
interchangeable ART styles for the image panel, so a whole 12-month calendar
stays uniform. Built to survey what would sell (2026 neo-print/halftone,
retro poster, distressed vintage, clean line-art, blueprint B&W)."""
import os, math
from gen import CARS, font_face, esc
from sil import SIL, GY, silhouette
from art import _outline, PAINT, light, dark, mix, car_art
import vintage

CMAP={c["key"]:c for c in CARS}
PW,PH=1200,1680
IMG_H=1030

FONTS="".join([
 font_face("Grot",900,"archivo/files/archivo-latin-900-normal.woff2"),
 font_face("Grot",700,"archivo/files/archivo-latin-700-normal.woff2"),
 font_face("Saira",700,"saira-condensed/files/saira-condensed-latin-700-normal.woff2"),
 font_face("Saira",800,"saira-condensed/files/saira-condensed-latin-800-normal.woff2"),
 font_face("Plex",400,"ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2"),
 font_face("Plex",600,"ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2"),
 font_face("Serif",400,"libre-baskerville/files/libre-baskerville-latin-400-normal.woff2"),
])

def T(x,y,s,size,fam,fill,anchor="start",ls=0,op=1.0,weight=400):
    a=f' text-anchor="{anchor}"' if anchor!="start" else ""
    l=f' letter-spacing="{ls}"' if ls else ""
    o=f' fill-opacity="{op}"' if op!=1.0 else ""
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{weight}" font-size="{size}" fill="{fill}"{a}{l}{o}>{esc(s)}</text>'

def _place(inner, s, tx, ty):
    return f'<g transform="translate({tx},{ty}) scale({s})">{inner}</g>'

# --- car in flat 2-colour (for halftone / rally) ---------------------------
def car_flat(car, body, key, glass="#2A333B", cel=False):
    g=SIL[car["sil"]]; d=_outline(g)
    cowl,hood_y=g["cowl_x"],g["hood_y"]; rf_y,rr_y,rf_x,rr_x=g["roof_fy"],g["roof_ry"],g["roof_fx"],g["roof_rx"]
    deck_x,deck_y,belt=g["deck_x"],g["deck_y"],g["belt"]; fwx,rwx,wr=g["fwx"],g["rwx"],g["wr"]
    nose=g["nose_x"]; tail=g["tail_x"]; belly=g["belly"]; nose_y=g["nose_y"]; uid=car["key"]
    if g.get("pickup"):
        gl=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {rr_x} {rr_y} L {rr_x} {belt} L {cowl} {belt} Z"
    else:
        gl=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {rr_x} {rr_y} L {deck_x} {deck_y} L {cowl} {belt} Z"
    P=[]
    if cel:
        P.append(f'<clipPath id="cc{uid}"><path d="{d}"/></clipPath>')
    P.append(f'<path d="{d}" fill="{body}"/>')
    if cel:
        # hard-edged posterized shadow on the lower body (no gradient)
        sh=f"M {nose-14} {belly+14} L {tail+14} {belly+14} L {tail+14} {belt+26} L {nose-14} {belt+8} Z"
        P.append(f'<g clip-path="url(#cc{uid})"><path d="{sh}" fill="{dark(body,0.30)}"/>'
                 f'<rect x="{nose-14}" y="{belly-16}" width="{tail-nose+28}" height="34" fill="{dark(body,0.5)}"/></g>')
    P.append(f'<path d="{gl}" fill="{glass}"/>')
    if cel:
        # glass: hard reflection stripe + gloss + clean outline; hard top highlights; spec spots
        r0=cowl+(rf_x-cowl)*0.2
        P.append(f'<polygon points="{r0:.0f},{belt} {r0+66:.0f},{rf_y+16} {r0+128:.0f},{rf_y+16} {r0+58:.0f},{belt}" fill="{light(glass,0.5)}"/>')
        P.append(f'<path d="{gl}" fill="none" stroke="{key}" stroke-width="4"/>')
        P.append(f'<circle cx="{rf_x+20}" cy="{rf_y+24}" r="9" fill="#fff" fill-opacity="0.85"/>')
        hood=f"M {nose+24} {nose_y+2} L {cowl} {hood_y+2} L {cowl} {hood_y+16} L {nose+30} {nose_y+16} Z"
        roof=f"M {rf_x} {rf_y+1} L {rr_x} {rr_y+1} L {rr_x} {rr_y+13} L {rf_x} {rf_y+13} Z"
        P.append(f'<g clip-path="url(#cc{uid})"><path d="{hood}" fill="{light(body,0.34)}"/>'
                 f'<path d="{roof}" fill="{light(body,0.34)}"/></g>')
    if g.get("white_roof"):
        rp=f"M {rf_x} {rf_y} L {rr_x} {rr_y} L {rr_x} {rr_y+26} L {rf_x} {rf_y+26} Z"
        P.append(f'<path d="{rp}" fill="#ECE8DD"/>')
        P.append(f'<path d="M {rf_x} {rf_y} L {rr_x} {rr_y}" fill="none" stroke="{key}" stroke-width="4"/>')
    if g.get("taxi"):
        rx=(rf_x+rr_x)/2; ry=min(rf_y,rr_y)
        P.append(f'<rect x="{rx-8}" y="{ry-14}" width="16" height="16" fill="{key}"/>')            # post
        P.append(f'<rect x="{rx-48}" y="{ry-44}" width="96" height="32" rx="8" fill="#F3C24E"/>')  # andon
        P.append(f'<rect x="{rx-48}" y="{ry-44}" width="96" height="32" rx="8" fill="none" stroke="{key}" stroke-width="4"/>')
        P.append(f'<line x1="{rx-30}" y1="{ry-28}" x2="{rx+30}" y2="{ry-28}" stroke="{key}" stroke-width="3"/>')
    if g.get("splitter"):
        P.append(f'<path d="M {nose-40} {belly+2} L {nose+120} {belly+2} L {nose+120} {belly+15} L {nose-48} {belly+17} Z" fill="{dark(body,0.55)}"/>')
    if g.get("wing"):
        x0,x1,wy=g["wing"]
        P.append(f'<rect x="{x0}" y="{wy}" width="{x1-x0}" height="12" rx="3" fill="{body}"/>')
        P.append(f'<rect x="{x0}" y="{wy}" width="{x1-x0}" height="12" rx="3" fill="none" stroke="{key}" stroke-width="4"/>')
        P.append(f'<rect x="{x0+10}" y="{wy}" width="10" height="{belt-wy+18}" fill="{key}"/>')
        P.append(f'<rect x="{x1-20}" y="{wy}" width="10" height="{belt-wy+18}" fill="{key}"/>')
    if g.get("rear_spare"):
        sr=wr*0.82; sx=tail-16; sy=belly-sr-2
        P.append(f'<rect x="{tail-34}" y="{sy-9}" width="34" height="18" rx="4" fill="{dark(body,0.3)}"/>')  # bracket
        P.append(f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="{key}"/>')                         # tyre
        P.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*0.6:.0f}" fill="{dark(body,0.12)}"/>')      # cover
        P.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*0.6:.0f}" fill="none" stroke="{key}" stroke-width="4"/>')
        P.append(f'<circle cx="{sx}" cy="{sy}" r="{sr*0.14:.0f}" fill="{key}"/>')
    for cx in (fwx,rwx):
        cy=GY-wr
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{wr}" fill="{key}"/>')
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{wr*0.5:.0f}" fill="{g.get("wheel", body)}"/>')
        if cel:
            P.append(f'<circle cx="{cx}" cy="{cy}" r="{wr*0.5:.0f}" fill="none" stroke="{key}" stroke-width="3"/>')
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{wr*0.16:.0f}" fill="{key}"/>')
    return "".join(P), d, gl

# ============================ STYLE PANELS ==================================
# each returns svg filling a 1200 x IMG_H box (with own background)

def panel_halftone(car, uid):
    """2026 neo-print: flat colour + misregistered key line + halftone + grain."""
    paper="#EAE3D0"; ink="#211C17"; spot=PAINT[car["key"]]
    body,d,gl=car_flat(car,spot,ink,glass=dark(spot,0.4))
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{paper}"/>']
    P.append(f'<defs><pattern id="ht{uid}" width="14" height="14" patternTransform="rotate(12)" patternUnits="userSpaceOnUse">'
             f'<circle cx="4" cy="4" r="3.1" fill="{ink}"/></pattern>'
             f'<pattern id="hs{uid}" width="12" height="12" patternTransform="rotate(12)" patternUnits="userSpaceOnUse">'
             f'<circle cx="4" cy="4" r="2.2" fill="{spot}"/></pattern>'
             f'<filter id="gr{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>'
             f'<clipPath id="cl{uid}"><path d="{d}"/></clipPath></defs>')
    s=1.16; tx=32; ty=300
    # halftone field in the sky (spot dots, light)
    P.append(f'<rect x="60" y="90" width="{PW-120}" height="720" fill="url(#hs{uid})" opacity="0.24"/>')
    P.append(f'<g transform="translate({tx},{ty}) scale({s})">')
    # colour fill layer
    P.append(body)
    # halftone shading inside lower body
    P.append(f'<g clip-path="url(#cl{uid})"><rect x="0" y="{SIL[car["sil"]]["belly"]-150}" width="1000" height="230" fill="url(#ht{uid})" opacity="0.55"/></g>')
    P.append('</g>')
    # misregistered key line (offset)
    P.append(f'<g transform="translate({tx+10},{ty+12}) scale({s})">'
             f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="{gl}" fill="none" stroke="{ink}" stroke-width="4"/></g>')
    # grain
    P.append(f'<rect width="{PW}" height="{IMG_H}" filter="url(#gr{uid})" opacity="0.08"/>')
    return "".join(P), paper, ink, spot

def panel_rally(car, uid):
    """retro poster: clean two-tone sky/ground + flat car (no sun). Per-car scale."""
    key=car["key"]; spot=PAINT[key]; acc=car["accent"]
    bg=car.get("sky", spot)
    ground="#2E2A22"; cream="#F0E9D6"; ink="#241E16"; gy=706
    # flat, posterized backdrop (no gradients) to match the cel/vexel treatment
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{light(bg,0.74)}"/>']
    P.append(f'<rect x="0" y="{gy-150}" width="{PW}" height="150" fill="{light(bg,0.62)}"/>')  # hard horizon band
    P.append(f'<rect x="0" y="{gy+18}" width="{PW}" height="{IMG_H-gy-18}" fill="{ground}"/>')
    P.append(f'<rect x="0" y="{gy}" width="{PW}" height="18" fill="{acc}"/>')
    body,d,gl=car_flat(car,spot,ink,glass=dark(spot,0.42),cel=True)
    sc=1.14*car.get("cscale",1.0)
    ty=gy-GY*sc; tx=600-500*sc
    P.append(f'<ellipse cx="600" cy="{gy}" rx="{430*sc:.0f}" ry="20" fill="#000" fill-opacity="0.16"/>')
    P.append(f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.4f})">{body}'
             f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="6.5" stroke-linejoin="round"/></g>')
    return "".join(P), cream, ink, acc

def panel_distressed(car, uid):
    """distressed vintage band-tee: illustrated car + heavy grain + arc badge."""
    paper="#E7DECA"; ink="#25201A"; acc=car["accent"]
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{paper}"/>']
    P.append(f'<defs><filter id="dg{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></defs>')
    P.append(_place(car_art(car,uid="d"+uid),1.2,0,300))
    # heavy grain over everything (distress)
    P.append(f'<rect width="{PW}" height="{IMG_H}" filter="url(#dg{uid})" opacity="0.13"/>')
    # torn-band top/bottom hint
    P.append(f'<rect x="0" y="0" width="{PW}" height="10" fill="{paper}"/>')
    return "".join(P), paper, ink, acc

def panel_lineart(car, uid):
    """clean minimal line-art on cream."""
    cream="#EEE7D6"; ink="#232019"; acc=car["accent"]
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{cream}"/>']
    P.append(f'<line x1="90" y1="720" x2="1110" y2="720" stroke="{ink}" stroke-width="2" stroke-opacity="0.3"/>')
    P.append(_place(silhouette(SIL[car["sil"]], stroke=ink, accent=acc, sw=7.0),1.14,30,352))
    return "".join(P), cream, ink, acc

def panel_blueprint(car, uid):
    """technical blueprint B&W (the enthusiast/'black and white' option)."""
    navy="#16283C"; line="#CBD8E6"; acc="#E8B04B"
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{navy}"/>']
    # faint grid
    P.append(f'<defs><pattern id="bg{uid}" width="46" height="46" patternUnits="userSpaceOnUse"><path d="M46 0H0V46" fill="none" stroke="{line}" stroke-opacity="0.12" stroke-width="1"/></pattern></defs>')
    P.append(f'<rect width="{PW}" height="{IMG_H}" fill="url(#bg{uid})"/>')
    v=vintage.VINT[car["key"]]
    P.append(_place(vintage.blueprint(car, v, ink=line, spot=acc),1.05,80,352))
    return navy_wrap(P), navy, line, acc

def navy_wrap(P): return "".join(P)

STYLES={
 "halftone":  ("Halftone Neo-Print", panel_halftone),
 "rally":     ("Retro Rally Poster",  panel_rally),
 "distressed":("Distressed Vintage",  panel_distressed),
 "lineart":   ("Clean Line-Art",      panel_lineart),
 "blueprint": ("Blueprint B&W",       panel_blueprint),
}

# ============================ CALENDAR FRAME ================================
def month_grid(x, y, w, ink, mute, accent, first_wd, days, circle_day):
    hdr=["S","M","T","W","T","F","S"]; cw=w/7.0; out=[]
    for i,dd in enumerate(hdr):
        out.append(T(x+i*cw+cw/2, y, dd, 22, "Plex", mute, anchor="middle", ls=1, weight=600))
    day=1; row=0; col=first_wd; ch=74
    while day<=days:
        ccx=x+col*cw+cw/2; ccy=y+52+row*ch
        if day==circle_day:
            out.append(f'<circle cx="{ccx:.0f}" cy="{ccy-11:.0f}" r="29" fill="{accent}"/>')
            out.append(T(ccx, ccy, str(day), 34, "Saira", "#fff", anchor="middle", weight=700))
        else:
            out.append(T(ccx, ccy, str(day), 34, "Saira", ink, anchor="middle", weight=700))
        col+=1
        if col>6: col=0; row+=1
        day+=1
    return "".join(out)

def calendar_page(car, style_key, month="MARCH", year="2026", first_wd=0, days=31):
    label, panel = STYLES[style_key]
    inner, page_bg, ink, accent = panel(car, uid=style_key+car["key"])
    mute=mix(ink, page_bg, 0.45)
    P=[f'<rect width="{PW}" height="{PH}" fill="{page_bg}"/>']
    P.append(inner)  # image panel fills top IMG_H
    P.append(f'<line x1="90" y1="{IMG_H}" x2="{PW-90}" y2="{IMG_H}" stroke="{ink}" stroke-width="2" stroke-opacity="0.25"/>')
    # month header
    my=IMG_H+96
    P.append(T(90, my, month, 92, "Grot", ink, weight=900))
    P.append(T(PW-90, my-46, year, 26, "Plex", mute, anchor="end", ls=3))
    sub=car.get("sub", car["country"])
    P.append(T(PW-90, my-8, f"{car['make']} {car['model']} · {sub}", 19, "Plex", accent, anchor="end", ls=1))
    P.append(f'<line x1="90" y1="{my+28}" x2="{PW-90}" y2="{my+28}" stroke="{ink}" stroke-width="2" stroke-opacity="0.25"/>')
    P.append(month_grid(96, my+92, PW-192, ink, mute, accent, first_wd, days, car["no"]))
    P.append(T(90, PH-40, f"MARQUE™  ·  WORLD MOTOR INDEX  ·  No.{car['no']:02d}/12", 15, "Plex", mute, ls=1))
    return "".join(P)

def page_svg(car, style_key, **kw):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}" '
            f'shape-rendering="geometricPrecision" text-rendering="geometricPrecision">'
            f'<defs><style>{FONTS}</style></defs>{calendar_page(car, style_key, **kw)}</svg>')

if __name__=="__main__":
    os.makedirs("out/styles", exist_ok=True)
    # one representative car per style for the survey
    demo=[("halftone","porsche"),("rally","corvette"),("distressed","skyline"),
          ("lineart","etype"),("blueprint","countach")]
    cols=len(demo); sc=0.42; cw=int(PW*sc); chh=int(PH*sc)
    body=[f'<rect width="{cols*cw}" height="{chh+60}" fill="#B9B0999"/>']
    body=[f'<rect width="{cols*cw}" height="{chh+60}" fill="#B0A892"/>']
    for i,(sk,ck) in enumerate(demo):
        gx=i*cw
        body.append(T(gx+16, 40, STYLES[sk][0], 30, "Grot", "#241E16", weight=900))
        body.append(f'<g transform="translate({gx},60) scale({sc})">{calendar_page(CMAP[ck], sk)}</g>')
    W,H=cols*cw, chh+60
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(body)+"</svg>"
    open("out/styles_contact.svg","w").write(svg); print("contact",W,H)
