# -*- coding: utf-8 -*-
"""One page to review: the fixes (right-facing, light windshield, solid rims,
floating taxi sign) + an ABSTRACTION LADDER (level 1 current -> 4 polygon)."""
import os
from styles import STYLES, FONTS, PW, IMG_H, esc
import toyota, honda, ford  # register geoms/paints

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")

# representative cars across body types
def car(make, model, key, acc, dt, sub, country, lvl, cscale=None, sky=None):
    c=dict(sil=key,key=key,make=make,model=model,accent=acc,drivetrain=dt,sub=sub,
           country=country,abstract=lvl)
    if cscale: c["cscale"]=cscale
    if sky: c["sky"]=sky
    return c

ROW=[  # (label, key, make, model, acc, dt, sub, country, cscale, sky)
 ("HONDA NSX · sports","nsx","HONDA","NSX","#E1051E","RWD","sports","JAPAN",None,None),
 ("TOYOTA CROWN · taxi","crown","TOYOTA","CROWN","#E01F26","RWD","sedan","JAPAN",None,"#CBA24E"),
 ("FORD F-150 · truck","f150","FORD","F-150","#0057B8","4WD","truck","UNITED STATES",1.08,None),
]
LEVELS=[(1,"Level 1 — Clean","what we have now: soft two-tone body + light windshield"),
        (2,"Level 2 — Bold","fewer, bolder planes + a hood highlight"),
        (3,"Level 3 — Faceted","hard angular planes start to break up the body"),
        (4,"Level 4 — Polygon","full low-poly: crystalline shards, most abstract & unique")]

def panel(c):
    content,_,_,_ = STYLES["rally"][1](c, f'e{c["key"]}{c["abstract"]}')
    return (f'<svg viewBox="0 0 {PW} {IMG_H}" class="art" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="geometricPrecision">{content}</svg>')

CSS="""
:root{--bg:#131418;--card:#1E1F25;--ink:#EDE6D6;--mute:#9A9488;--line:rgba(237,230,214,.12);--spot:#E0A43A}
:root[data-theme="light"]{--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E7DECA;--card:#F1EBDD;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#B26A12}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Grot','Arial Black',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header{padding:46px 0 24px;border-bottom:1px solid var(--line)}
.kick{font-weight:700;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
h1{font-weight:900;font-size:clamp(36px,7vw,66px);line-height:.92;margin:8px 0 0}
.lede{font-family:'Serif',Georgia,serif;font-style:italic;max-width:64ch;margin:14px 0 0;color:var(--mute);font-size:16px}
.fixes{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.chip{font-size:12px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:20px;padding:6px 12px}
.chip b{color:var(--spot)}
section{padding:26px 0}
.lvl{border-top:1px solid var(--line);padding:24px 0}
.lvlhead{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}
.lvlhead h2{font-weight:900;font-size:clamp(20px,3.4vw,30px);margin:0}
.lvlhead p{margin:0;color:var(--mute);font-size:13.5px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:820px){.grid{grid-template-columns:1fr}}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.art{display:block;width:100%;height:auto}
figcaption{padding:9px 14px 12px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.toggle{position:fixed;top:14px;right:14px;z-index:9;background:var(--card);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
footer{padding:26px 0 66px;color:var(--mute);font-family:'Plex',monospace;font-size:11px}
"""

def build():
    rows=""
    for lvl,title,desc in LEVELS:
        cells=""
        for label,key,mk,md,acc,dt,sub,ctry,cs,sky in ROW:
            c=car(mk,md,key,acc,dt,sub,ctry,lvl,cs,sky)
            cells+=f'<figure>{panel(c)}<figcaption>{esc(label)}</figcaption></figure>'
        rows+=(f'<div class="lvl"><div class="lvlhead"><h2>{esc(title)}</h2><p>{esc(desc)}</p></div>'
               f'<div class="grid">{cells}</div></div>')
    body=f"""<style>{FONTS}{CSS}</style>
<button class="toggle" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header><div class="wrap"><div class="kick">MARQUE · design options · one page</div>
<h1>Pick an abstract level.</h1>
<p class="lede">All your fixes are in below. Then the same three cars are shown at four levels of abstraction — from what we have now down to a full low-poly / polygon look. Tell me which level to lock in (and I'll roll it across all six brands).</p>
<div class="fixes"><span class="chip"><b>Cars face right</b></span>
<span class="chip"><b>Windshield</b> = the light pane on top</span>
<span class="chip"><b>Solid rims</b> (not see-through)</span>
<span class="chip"><b>Taxi sign floats</b> · no post · no middle bar</span></div></div></header>
<section><div class="wrap">{rows}</div></section>
<footer><div class="wrap">Reply with a level (1–4). Everything else — colours, wheels, motif — stays as-is.</div></footer>"""
    os.makedirs(OUT,exist_ok=True); open(os.path.join(OUT,"design-options.html"),"w").write(body)
    print("wrote design-options.html")

if __name__=="__main__":
    build()
