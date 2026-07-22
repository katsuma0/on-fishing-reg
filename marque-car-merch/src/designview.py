# -*- coding: utf-8 -*-
"""Design-review view: the car artworks only (no dates/grid), stacked so you can
scroll through them. One page per brand."""
import os
import styles
from styles import STYLES, FONTS, PW, IMG_H, esc

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")

def panel_svg(car):
    content,_,_,_ = STYLES["rally"][1](car, "dv"+car["key"])
    return (f'<svg viewBox="0 0 {PW} {IMG_H}" class="art" xmlns="http://www.w3.org/2000/svg" '
            f'shape-rendering="geometricPrecision" preserveAspectRatio="xMidYMid meet">{content}</svg>')

CSS="""
:root{--bg:#17181C;--panel:#1E1F25;--ink:#EDE6D6;--mute:#9A9488;--line:rgba(237,230,214,.12);--spot:#E01F26}
:root[data-theme="light"]{--bg:#E7DECA;--panel:#F0EADC;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#C21A20}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E7DECA;--panel:#F0EADC;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.14);--spot:#C21A20}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Grot','Arial Black',sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:900px;margin:0 auto;padding:0 16px}
header{padding:44px 0 24px;text-align:center;border-bottom:1px solid var(--line)}
.kick{font-weight:700;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
h1{font-weight:900;font-size:clamp(44px,10vw,104px);line-height:.9;margin:8px 0 0;letter-spacing:-.01em}
.sub{font-size:12px;letter-spacing:.28em;text-transform:uppercase;color:var(--mute);margin-top:12px}
.stack{display:flex;flex-direction:column;gap:20px;padding:26px 0 70px}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
figure .art{display:block;width:100%;height:auto}
figcaption{display:flex;justify-content:space-between;align-items:baseline;padding:12px 18px 15px;gap:12px}
figcaption .n{font-weight:900;font-size:19px;letter-spacing:.01em}
figcaption .m{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.idx{font-family:'Plex',monospace;font-size:11px;color:var(--mute);letter-spacing:.16em}
.toggle{position:fixed;top:14px;right:14px;z-index:9;background:var(--panel);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
"""

def build(brand_title, country, cars, filename):
    figs=[]
    for c in cars:
        figs.append(
            f'<figure>{panel_svg(c)}<figcaption>'
            f'<span class="n">{esc(c["make"].title())} {esc(c["model"])}</span>'
            f'<span class="m">{esc(c.get("drivetrain",""))} · {esc(c.get("sub",""))}</span>'
            f'</figcaption></figure>')
    body=f"""<style>{FONTS}{CSS}</style>
<button class="toggle" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header><div class="wrap"><div class="kick">Design review · {esc(country)}</div>
<h1>{esc(brand_title)}</h1><div class="sub">MARQUE — World Motor Index · scroll the designs</div></div></header>
<div class="wrap"><div class="stack">{"".join(figs)}</div></div>"""
    open(os.path.join(OUT,filename),"w").write(body)
    print("wrote",filename)

if __name__=="__main__":
    import toyota, honda
    build("TOYOTA","Japan", toyota.CARS_T, "toyota-designs.html")
    build("HONDA","Japan", honda.CARS_H, "honda-designs.html")
