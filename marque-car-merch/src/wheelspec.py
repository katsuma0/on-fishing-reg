# -*- coding: utf-8 -*-
"""Wheel system v2 — clean & sleek. Rim is a plain body-colour disc (no marks).
Vehicle type reads from TYRE thickness; drivetrain from the small hub.
This sheet lists the options to pick from."""
import os
from sil import SIL, GY
from styles import draw_wheel, car_flat, FONTS, PAINT, TIRE, light, dark
import toyota, honda, acura, lexus, ford, jeep  # register geoms + paints

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")
KEY="#20201C"; DEMO="#6E7A86"; ACC="#C8342E"; INK="#241E16"

def wheel_tile(vt, driven=True, tell="hub", box=280, wr=104, rim=DEMO, acc=ACC):
    c=box/2
    inner=draw_wheel(c, c, wr, rim, KEY, vt, driven, acc, cel=True, tell=tell)
    return (f'<svg viewBox="0 0 {box} {box}" class="wh" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="geometricPrecision">{inner}</svg>')

def mini_car(key, acc, dt, tell="hub"):
    g=SIL[key]; body=PAINT[key]
    car={"sil":key,"key":key,"accent":acc,"drivetrain":dt}
    inner,d,gl=car_flat(car, body, INK, glass=dark(body,0.42), cel=True)
    # temporarily honour the requested tell by re-drawing wheels is overkill; car_flat
    # already used the module default. For samples we just show the default 'hub'.
    return (f'<svg viewBox="0 60 1000 288" class="car" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="geometricPrecision">{inner}'
            f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/></svg>')

# type ladder (thin -> fat tyre)
LADDER=[("SPORTS","sport"),("COUPE","coupe"),("SEDAN","sedan"),
        ("EV","ev"),("SUV","suv"),("TRUCK","truck")]
# real cars for the in-context strip
SAMPLES=[("HONDA NSX","sports","nsx","#E1051E","RWD"),
         ("TOYOTA CROWN","sedan","crown","#E01F26","RWD"),
         ("LEXUS RX","SUV","lx_rx","#1F4E82","AWD"),
         ("FORD F-150","truck","f150","#0057B8","4WD")]
# drivetrain options (front driven, rear idle -> FWD, to show the difference)
DTOPTS=[("Accent hub","hub","Driven wheel = brand colour, idle = white. One small dot."),
        ("Fill / hollow","fillhollow","Driven = solid dot, idle = open ring. Pure black-on-body, no colour."),
        ("No mark","none","Wheels identical & cleanest; drivetrain shown only by the AWD/FWD tag.")]

CSS="""
:root{--bg:#17181C;--card:#1E1F25;--ink:#EDE6D6;--mute:#9A9488;--line:rgba(237,230,214,.12);--spot:#E0A43A;--stage:#C8CDD3}
:root[data-theme="light"]{--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12;--stage:#DBDFE3}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12;--stage:#DBDFE3}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Grot','Arial Black',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header{padding:46px 0 26px;border-bottom:1px solid var(--line)}
.kick{font-weight:700;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
h1{font-weight:900;font-size:clamp(38px,8vw,72px);line-height:.9;margin:8px 0 0;letter-spacing:-.01em}
.lede{font-family:'Serif',Georgia,serif;font-style:italic;max-width:62ch;margin:16px 0 0;color:var(--mute);font-size:16px}
section{padding:38px 0;border-bottom:1px solid var(--line)}
h2{font-weight:900;font-size:clamp(22px,4vw,34px);margin:0 0 4px}
.sub{color:var(--mute);font-size:14px;margin:0 0 24px;max-width:66ch}
.cars{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.carcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 8px 12px}
.carcard .stage{background:var(--stage);border-radius:9px;padding:6px 4px}
.car{display:block;width:100%;height:auto}
.carcard .cap{display:flex;justify-content:space-between;padding:9px 8px 2px;font-size:12px}
.carcard .cap .m{color:var(--mute);text-transform:uppercase;letter-spacing:.12em;font-size:10px}
.ladder{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
@media(max-width:720px){.ladder{grid-template-columns:repeat(3,1fr)}.cars{grid-template-columns:1fr}}
.lcell{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 6px 8px;text-align:center}
.lcell .stage{background:var(--stage);border-radius:8px}
.wh{display:block;width:100%;height:auto}
.lcell .n{font-size:11px;letter-spacing:.14em;color:var(--mute);margin-top:6px}
.opts{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:720px){.opts{grid-template-columns:1fr}}
.opt{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}
.opt .name{font-weight:900;font-size:17px}
.opt .pair{display:flex;gap:8px;justify-content:center;background:var(--stage);border-radius:9px;margin:12px 0 10px;padding:12px}
.opt .pair .u{display:flex;flex-direction:column;align-items:center}
.opt .pair .u span{font-family:'Plex',monospace;font-size:9px;letter-spacing:.1em;color:#333;margin-top:2px}
.opt p{margin:0;color:var(--mute);font-size:13px;line-height:1.5}
.opt.rec{border-color:var(--spot)}
.badge{display:inline-block;font-size:10px;letter-spacing:.14em;color:var(--spot);border:1px solid var(--spot);border-radius:20px;padding:2px 8px;margin-left:8px;vertical-align:middle}
.ideas{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.ideas li{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:14px;color:var(--mute)}
.ideas b{color:var(--ink)}
.wh2{width:120px;height:120px}
.toggle{position:fixed;top:14px;right:14px;z-index:9;background:var(--card);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
footer{padding:30px 0 66px;color:var(--mute);font-family:'Plex',monospace;font-size:11px;letter-spacing:.06em}
"""

def build():
    # in-context sample cars
    cars="".join(
        f'<div class="carcard"><div class="stage">{mini_car(k,a,dt)}</div>'
        f'<div class="cap"><span>{name}</span><span class="m">{lab} · {dt}</span></div></div>'
        for name,lab,k,a,dt in SAMPLES)
    # tyre-size ladder
    ladder="".join(
        f'<div class="lcell"><div class="stage">{wheel_tile(vt, box=200, wr=88)}</div>'
        f'<div class="n">{name}</div></div>' for name,vt in LADDER)
    # drivetrain options
    def pair(tell):
        def one(driven,lab):
            svg=wheel_tile("sedan", driven=driven, tell=tell, box=150, wr=60)
            return f'<div class="u"><div style="width:90px">{svg}</div><span>{lab}</span></div>'
        return f'<div class="pair">{one(True,"FRONT")}{one(False,"REAR")}</div>'
    opts=""
    for i,(name,tell,desc) in enumerate(DTOPTS):
        rec=' rec' if i==0 else ''
        badge='<span class="badge">suggested</span>' if i==0 else ''
        opts+=f'<div class="opt{rec}"><div class="name">{name}{badge}</div>{pair(tell)}<p>{desc}</p></div>'

    body=f"""<style>{FONTS}{CSS}</style>
<button class="toggle" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header><div class="wrap"><div class="kick">MARQUE · wheel system · v2 — simple &amp; sleek</div>
<h1>Clean rim.<br>The tyre does the talking.</h1>
<p class="lede">No marks on the rim any more — just a black tyre and a plain body-colour disc. The car type reads from how <b>fat the tyre</b> is (thick on trucks &amp; SUVs, thin and low-profile on sports cars), and a single small hub says which wheels drive. Pick the drivetrain style below.</p></div></header>
<section><div class="wrap"><h2>In context</h2>
<p class="sub">Same clean wheel on four body styles — note the tyre getting fatter from sports → sedan → SUV → truck.</p>
<div class="cars">{cars}</div></div></section>
<section><div class="wrap"><h2>A · Type = tyre size</h2>
<p class="sub">The only thing that changes for body style is the black tyre's thickness. Thin/low-profile for sports, fattest for trucks. All rims stay a clean body-colour disc.</p>
<div class="ladder">{ladder}</div></div></section>
<section><div class="wrap"><h2>B · Drivetrain — pick one</h2>
<p class="sub">How the driven vs idle wheel reads (shown as FWD: front drives, rear idle). AWD/4WD lights both, RWD lights the rear.</p>
<div class="opts">{opts}</div></div></section>
<section><div class="wrap"><h2>C · More ideas on the table</h2>
<ul class="ideas">
<li><b>Rim tone.</b> Keep the rim body-colour (shown), or make every rim one sleek metallic silver/graphite for a more premium, uniform look across all brands.</li>
<li><b>Thin accent ring.</b> Instead of a coloured hub, a single hairline brand-colour ring inside the rim edge — brand tie with zero clutter.</li>
<li><b>Hub size = nothing else.</b> Drop drivetrain from the wheel entirely and let tyre size be the only wheel variable — the drivetrain word (AWD/FWD…) already prints on the panel.</li>
<li><b>Colour-match hub.</b> Hub always body-colour (disappears) on idle wheels, brand-accent on driven — the quietest possible tell.</li>
</ul></div></section>
<footer><div class="wrap">Draft v2 for review — tell me the drivetrain pick + any tweak, and I'll roll it across all six brands.</div></footer>"""
    os.makedirs(OUT,exist_ok=True)
    open(os.path.join(OUT,"wheel-system.html"),"w").write(body)
    print("wrote wheel-system.html (v2)")

if __name__=="__main__":
    build()
