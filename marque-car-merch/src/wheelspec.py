# -*- coding: utf-8 -*-
"""Wheel & vehicle-type system spec sheet.
Two lists to review/tweak:
  A) how the wheel reads for each DRIVETRAIN (the hub is the only tell)
  B) the rim SIGNATURE for each vehicle TYPE."""
import os
from styles import draw_wheel, _rim_motif, FONTS, IDLE_CAP

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")

KEY="#20201C"                 # tyre / mark black
DEMO="#6E7A86"                # neutral demo body/rim colour
ACC="#C8342E"                 # demo brand accent (driven hub)

def wheel_tile(vt, driven, box=280, wr=104):
    c=box/2
    inner=draw_wheel(c, c, wr, DEMO, KEY, vt, driven, ACC, cel=True)
    return (f'<svg viewBox="0 0 {box} {box}" class="wh" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="geometricPrecision">{inner}</svg>')

def pair(fd, rd):
    """front + rear wheel, labelled — shows which axle drives."""
    def one(driven, lab):
        return (f'<div class="axle"><div class="whwrap">{wheel_tile("sedan", driven)}</div>'
                f'<div class="ax">{lab} · {"DRIVEN" if driven else "idle"}</div></div>')
    return f'<div class="pairwrap">{one(fd,"FRONT")}{one(rd,"REAR")}</div>'

DRIVE=[
 ("AWD","All-wheel drive","Both hubs brand-colour — both wheels drive.", True, True),
 ("4WD","Four-wheel drive","Same read as AWD: both hubs coloured.", True, True),
 ("FWD","Front-wheel drive","Front hub coloured, rear hub white.", True, False),
 ("RWD","Rear-wheel drive","Rear hub coloured, front hub white.", False, True),
]
TYPES=[
 ("sport","Sports / supercar","5 black dots — open mesh face.","NSX · Supra · GT · LC500 · Type R"),
 ("coupe","Coupe","5 slim spokes.","AE86 · Integra · Legend · SC430 · T-Bird"),
 ("sedan","Sedan / saloon","Fine 10-hole turbine.","Crown · Accord · TLX · IS F · LS400"),
 ("suv","SUV / 4x4","Bead ring + 5 chunky lugs.","RAV4 · CR-V · MDX · RX · Wrangler"),
 ("truck","Pickup truck","Steel dish — 5 big vents.","Tacoma · F-150 · Gladiator · Ridgeline"),
 ("ev","EV / hybrid","Closed aero disc — thin slots.","Prius · Honda e · Mach-E"),
]

CSS="""
:root{--bg:#17181C;--card:#1E1F25;--ink:#EDE6D6;--mute:#9A9488;--line:rgba(237,230,214,.12);--spot:#E0A43A;--stage:#C8CDD3}
:root[data-theme="light"]{--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12;--stage:#D9DDE1}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12;--stage:#D9DDE1}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Grot','Arial Black',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{padding:46px 0 26px;border-bottom:1px solid var(--line)}
.kick{font-weight:700;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
h1{font-weight:900;font-size:clamp(38px,8vw,74px);line-height:.9;margin:8px 0 0;letter-spacing:-.01em}
.lede{font-family:'Serif',Georgia,serif;font-style:italic;max-width:60ch;margin:16px 0 0;color:var(--mute);font-size:16px}
section{padding:40px 0;border-bottom:1px solid var(--line)}
h2{font-weight:900;font-size:clamp(22px,4vw,34px);margin:0 0 4px}
.sub{color:var(--mute);font-size:14px;margin:0 0 26px;max-width:64ch}
.grid{display:grid;gap:16px}
.g4{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
@media(max-width:720px){.g4,.g3{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 18px 20px}
.card .tag{display:flex;align-items:baseline;gap:10px}
.card .code{font-weight:900;font-size:26px;letter-spacing:.02em}
.card .name{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.card p{margin:8px 0 0;color:var(--mute);font-size:13.5px;line-height:1.5}
.card .ex{margin-top:6px;font-family:'Plex',monospace;font-size:11px;color:var(--mute);letter-spacing:.02em}
.stage{margin:14px 0 2px;background:var(--stage);border-radius:10px;display:flex;justify-content:center;align-items:center;gap:8px;padding:14px}
.wh{display:block;width:150px;height:150px}
.pairwrap{display:flex;gap:10px;justify-content:center}
.axle{display:flex;flex-direction:column;align-items:center}
.whwrap{}
.ax{font-family:'Plex',monospace;font-size:10px;letter-spacing:.12em;color:#3a3a3a;margin-top:2px}
.legend{display:flex;flex-wrap:wrap;gap:18px;margin-top:6px}
.legend div{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--mute)}
.sw{width:16px;height:16px;border-radius:50%;border:2px solid var(--ink)}
.toggle{position:fixed;top:14px;right:14px;z-index:9;background:var(--card);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
footer{padding:30px 0 66px;color:var(--mute);font-family:'Plex',monospace;font-size:11px;letter-spacing:.08em}
"""

def build():
    dcards=""
    for code,name,desc,fd,rd in DRIVE:
        dcards+=(f'<div class="card"><div class="tag"><span class="code">{code}</span>'
                 f'<span class="name">{name}</span></div>'
                 f'<div class="stage">{pair(fd,rd)}</div><p>{desc}</p></div>')
    tcards=""
    for vt,name,desc,ex in TYPES:
        tcards+=(f'<div class="card"><div class="tag"><span class="name">{name}</span></div>'
                 f'<div class="stage">{wheel_tile(vt, True)}</div>'
                 f'<p>{desc}</p><div class="ex">{ex}</div></div>')
    body=f"""<style>{FONTS}{CSS}</style>
<button class="toggle" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header><div class="wrap"><div class="kick">MARQUE · World Motor Index · wheel system</div>
<h1>Wheels &amp; type,<br>two quiet tells.</h1>
<p class="lede">Everything stays two-tone: a black tyre, a body-colour rim, black marks. Two things change, both low-key. The <b>rim pattern</b> says what kind of car it is; the <b>centre hub</b> says which wheels drive. If you know, you know.</p>
<div class="legend"><div><span class="sw" style="background:{ACC}"></span>driven hub — brand accent</div>
<div><span class="sw" style="background:{IDLE_CAP}"></span>idle hub — white</div></div></div></header>
<section><div class="wrap"><h2>A · Drivetrain</h2>
<p class="sub">Only the hub colour moves. A coloured hub = that wheel drives; a white hub = it doesn't. AWD and 4WD both light up; FWD lights the front, RWD the rear.</p>
<div class="grid g4">{dcards}</div></div></section>
<section><div class="wrap"><h2>B · Vehicle type</h2>
<p class="sub">The rim's black pattern is a small signature per body style — never loud, but consistent, so a shelf of them reads as one system. (Hubs shown driven here.)</p>
<div class="grid g3">{tcards}</div></div></section>
<footer><div class="wrap">Draft for review — every value is easy to tweak (dot count, spoke width, which hub colour). Tell me what to change.</div></footer>"""
    os.makedirs(OUT,exist_ok=True)
    open(os.path.join(OUT,"wheel-system.html"),"w").write(body)
    print("wrote wheel-system.html")

if __name__=="__main__":
    build()
