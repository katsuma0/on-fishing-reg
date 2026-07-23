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

# --- wheel system (clean & sleek) -------------------------------------------
# The rim is a plain body-colour disc — NO marks on it. Two quiet signals:
#   1) VEHICLE TYPE  -> the TYRE thickness. Fat black tyre for trucks (and SUVs),
#      thin low-profile tyre for sports/small cars, medium for sedans/coupes.
#   2) DRIVETRAIN    -> the small centre hub only (see DT_TELL): driven wheel =
#      brand-accent hub, idle wheel = white hub. AWD/4WD both, FWD front, RWD rear.
VT = {
 # original 10 (gen.py)
 "skyline":"sport","porsche":"sport","countach":"sport","etype":"sport",
 "corvette":"sport","alpine":"sport","volvo":"coupe","ioniq":"ev",
 "niva":"suv","monaro":"coupe",
 # Toyota
 "tacoma":"truck","ae86":"coupe","grcorolla":"sport","supra80":"sport",
 "mr2":"sport","fj40":"suv","fjcruiser":"suv","prius":"ev","rav4":"suv",
 "crown":"sedan","im":"sedan","gr86":"sport",
 # Honda
 "nsx":"sport","civicr":"sport","s2000":"sport","integra":"coupe","crx":"coupe",
 "prelude":"coupe","beat":"sport","ridgeline":"truck","crv":"suv",
 "odyssey":"sedan","hondae":"ev","accord":"sedan",
 # Ford
 "mustang":"sport","f150":"truck","fordgt":"sport","bronco":"suv",
 "focusrs":"sport","fiestast":"sport","explorer":"suv","gt40":"sport",
 "escortcos":"sport","thunderbird":"coupe","ranger":"truck","mache":"ev",
 # Acura
 "a_nsx":"sport","a_integs":"sport","a_rsx":"coupe","a_tltyps":"sedan",
 "a_tsx":"sedan","a_legend":"coupe","a_rl":"sedan","a_ilx":"sedan",
 "a_tlxs":"sedan","a_mdx":"suv","a_rdx":"suv","a_cl":"coupe",
 # Lexus
 "lx_lc":"sport","lx_lfa":"sport","lx_isf":"sedan","lx_rcf":"coupe",
 "lx_gsf":"sedan","lx_ls":"sedan","lx_sc":"coupe","lx_rx":"suv",
 "lx_gx":"suv","lx_lx":"suv","lx_ux":"suv","lx_nx":"suv",
 # Jeep
 "j_wrangler":"suv","j_cj5":"suv","j_grandche":"suv","j_cherokee":"suv",
 "j_gladiator":"truck","j_wagoneer":"suv","j_renegade":"suv","j_compass":"suv",
 "j_comanche":"truck","j_grandwag":"suv","j_willys":"suv","j_trackhawk":"suv",
}
RIM="#7E848C"        # uniform alloy graphite-grey rim (solid — reads against light sky)
# tyre "fatness" per type: fraction that is grey RIM, rest is black tyre. A very
# TIGHT band so tyres barely differ, and even the lowest super-sports keep a solid
# black tyre (never a thin line).
TIRE={"sport":0.56,"coupe":0.55,"sedan":0.53,"ev":0.54,"suv":0.50,"truck":0.47}
DT_TELL="hub"        # drivetrain read: "hub" (tiny accent pin, driven only) | "none"

def draw_wheel(cx, cy, wr, rim, key, vt, driven, accent, cel=False, tell=None):
    """Clean, sleek wheel: black tyre + grey rim disc (no marks). The tyre
    THICKNESS carries the vehicle type. Drivetrain is a *very* subtle tell: a
    driven wheel gets a tiny accent pin at the hub; an idle wheel is identical
    (just the plain grey hub), so you have to look closely to catch it."""
    tell = tell or DT_TELL
    rf = wr*TIRE.get(vt, 0.54)
    hub = dark(rim, 0.42)
    P=[f'<circle cx="{cx}" cy="{cy}" r="{wr}" fill="{key}"/>',            # black tyre
       f'<circle cx="{cx}" cy="{cy}" r="{rf:.0f}" fill="{rim}"/>',        # grey rim
       f'<circle cx="{cx}" cy="{cy}" r="{wr*0.13:.0f}" fill="{hub}"/>']   # grey hub (both wheels identical)
    if tell=="hub" and driven:                                           # tiny accent pin — driven only
        P.append(f'<circle cx="{cx}" cy="{cy}" r="{wr*0.05:.0f}" fill="{accent}"/>')
    return "".join(P)

# --- car in flat 2-colour (for halftone / rally) ---------------------------
def car_flat(car, body, key, glass="#2A333B", cel=False):
    g=SIL[car["sil"]]; d=_outline(g)
    cowl,hood_y=g["cowl_x"],g["hood_y"]; rf_y,rr_y,rf_x,rr_x=g["roof_fy"],g["roof_ry"],g["roof_fx"],g["roof_rx"]
    deck_x,deck_y,belt=g["deck_x"],g["deck_y"],g["belt"]; fwx,rwx,wr=g["fwx"],g["rwx"],g["wr"]
    nose=g["nose_x"]; tail=g["tail_x"]; belly=g["belly"]; nose_y=g["nose_y"]; uid=car["key"]
    # SIGNATURE DETAIL — KEEP. The greenhouse starts at the cowl point (cowl,hood_y)
    # while the glass front edge drops to (cowl,belt); because belt sits slightly
    # above hood_y, this leaves the small stepped "indent" where the windshield
    # pops up out of the body at the base of the A-pillar. Do not flatten: preserve
    # the cowl_x / hood_y / belt relationship and this vertical `L {cowl} {belt}` edge.
    if g.get("pickup"):
        gl=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {rr_x} {rr_y} L {rr_x} {belt} L {cowl} {belt} Z"
    else:
        gl=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {rr_x} {rr_y} L {deck_x} {deck_y} L {cowl} {belt} Z"
    P=[]
    if cel:
        P.append(f'<clipPath id="cc{uid}"><path d="{d}"/></clipPath>')
    P.append(f'<path d="{d}" fill="{body}"/>')
    if cel:
        # TWO-TONE body + bottom — a RAKED lower plane (more abstract than a flat
        # band) plus a darker rocker strip along the very bottom.
        lo=dark(body,0.16); bot=dark(body,0.32)
        loply=f"M {nose-16} {belt+34} L {tail+18} {belt-4} L {tail+18} {belly+50} L {nose-16} {belly+50} Z"
        P.append(f'<g clip-path="url(#cc{uid})"><path d="{loply}" fill="{lo}"/>'
                 f'<rect x="{nose-16}" y="{belly-6}" width="{tail-nose+34}" height="42" fill="{bot}"/></g>')
    if cel:
        # windshield: two tones of a LIGHTER shade of the body colour, split so the
        # brighter tone is the FRONT windshield pane itself (no gloss dot).
        gA=light(body,0.60); gB=light(body,0.42)
        P.append(f'<clipPath id="gg{uid}"><path d="{gl}"/></clipPath>')
        P.append(f'<path d="{gl}" fill="{gB}"/>')                                    # side + rear glass
        wind=f"M {cowl} {hood_y} L {rf_x} {rf_y} L {cowl} {belt} Z"                   # front windshield pane
        P.append(f'<g clip-path="url(#gg{uid})"><path d="{wind}" fill="{gA}"/></g>')
        P.append(f'<path d="{gl}" fill="none" stroke="{key}" stroke-width="3.5"/>')
    else:
        P.append(f'<path d="{gl}" fill="{glass}"/>')
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
    # wheels: type-signature rim + drivetrain hub (see draw_wheel / VT above)
    dt=car.get("drivetrain","AWD").upper()
    fd = dt in ("AWD","4WD","FWD"); rd = dt in ("AWD","4WD","RWD")
    rimc=RIM; acc=car.get("accent","#222")
    vt=car.get("vtype", VT.get(car["sil"], "sedan"))
    P.append(draw_wheel(fwx, GY-wr, wr, rimc, key, vt, fd, acc, cel))
    P.append(draw_wheel(rwx, GY-wr, wr, rimc, key, vt, rd, acc, cel))
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

def _star(cx,cy,r,fill):
    p=[]
    for i in range(10):
        ang=math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.42
        p.append(f"{cx+rr*math.cos(ang):.1f},{cy-rr*math.sin(ang):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="{fill}"/>'

def country_motif(country, bg, gy):
    """Subtle, tone-on-tone origin marker — the same across a brand's 12 months."""
    c=country.upper(); P=[]; t1=light(bg,0.70)
    if "JAPAN" in c:                       # rising sun (subtle)
        cx=600; r=168
        for i in range(-3,4):
            a=math.radians(90-i*15)
            P.append(f'<polygon points="{cx},{gy} {cx+math.cos(a-0.026)*840:.0f},{gy-math.sin(a-0.026)*840:.0f} {cx+math.cos(a+0.026)*840:.0f},{gy-math.sin(a+0.026)*840:.0f}" fill="{t1}"/>')
        P.append(f'<path d="M {cx-r} {gy} A {r} {r} 0 0 1 {cx+r} {gy} Z" fill="{light(bg,0.58)}"/>')
    elif any(k in c for k in ("UNITED STATES","USA","AMERICA")):   # stars & stripes (subtle)
        for i in range(5):
            P.append(f'<rect x="0" y="{gy-260+i*52}" width="{PW}" height="22" fill="{t1}"/>')
        for rr in range(3):
            for col in range(5):
                P.append(_star(96+col*74, 92+rr*66, 15, light(bg,0.5)))
    elif "GERMANY" in c:                   # three faint bands (subtle)
        for i in range(3):
            P.append(f'<rect x="0" y="{54+i*34}" width="{PW}" height="20" fill="{t1}"/>')
    return "".join(P)

def panel_rally(car, uid):
    """retro poster: clean two-tone sky/ground + flat car (no sun). Per-car scale."""
    key=car["key"]; spot=PAINT[key]; acc=car["accent"]
    bg=car.get("sky", spot)
    ground="#2E2A22"; cream="#F0E9D6"; ink="#241E16"; gy=706
    # flat, posterized backdrop (no gradients) to match the cel/vexel treatment
    P=[f'<rect width="{PW}" height="{IMG_H}" fill="{light(bg,0.74)}"/>']
    P.append(f'<clipPath id="sky{uid}"><rect x="0" y="0" width="{PW}" height="{gy}"/></clipPath>')
    P.append(f'<g clip-path="url(#sky{uid})">{country_motif(car.get("country",""), bg, gy)}</g>')  # subtle origin marker
    P.append(f'<rect x="0" y="{gy+18}" width="{PW}" height="{IMG_H-gy-18}" fill="{ground}"/>')
    P.append(f'<rect x="0" y="{gy}" width="{PW}" height="18" fill="{acc}"/>')
    body,d,gl=car_flat(car,spot,ink,glass=dark(spot,0.42),cel=True)
    sc=1.14*car.get("cscale",1.0)
    ty=gy-GY*sc; tx=600-500*sc
    P.append(f'<ellipse cx="600" cy="{gy}" rx="{430*sc:.0f}" ry="20" fill="#000" fill-opacity="0.16"/>')
    P.append(f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.4f})">{body}'
             f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="6.5" stroke-linejoin="round"/></g>')
    # drivetrain tag
    dt=car.get("drivetrain","AWD").upper()
    P.append(T(94, 78, dt, 30, "Grot", ink, weight=900, ls=3))
    P.append(T(94, 104, "DRIVE", 13, "Plex", mix(ink,light(bg,0.5),0.5), weight=400, ls=4))
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
