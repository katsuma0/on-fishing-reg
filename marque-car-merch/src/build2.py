# -*- coding: utf-8 -*-
"""Combined lookbook: Series 02 (Vintage) lead + Series 01 (Modern) below,
plus cream-tee mockups. Republishes to the same gallery.html / Artifact URL."""
import os
import gen, build, vintage
from gen import CARS, plate_inner, PLATE_W, PLATE_H, esc
from vintage import vintage_inner, standalone as v_standalone, FONT_CSS_V

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CMAP = {c["key"]: c for c in CARS}

LIGHT_GARMENTS = {
    "sand": ("#E1D8C0", "#D2C7AC"),
    "bone": ("#ECE6D8", "#DCD4C1"),
    "oat":  ("#E7E0CE", "#D6CDB6"),
}

def vtee_inner(car, garment="bone"):
    base, dark = LIGHT_GARMENTS[garment]
    uid = f'vt{car["key"]}'
    p = [f'<defs><radialGradient id="g{uid}" cx="50%" cy="34%" r="62%">'
         f'<stop offset="0%" stop-color="{base}"/><stop offset="100%" stop-color="{dark}"/>'
         f'</radialGradient></defs>']
    p.append('<ellipse cx="500" cy="1120" rx="330" ry="34" fill="#000" fill-opacity="0.16"/>')
    tee = ("M335 170 L430 165 Q500 240 570 165 L665 170 L835 190 L890 372 "
           "L715 346 L764 1082 L236 1082 L285 346 L110 372 L165 190 Z")
    p.append(f'<path d="{tee}" fill="url(#g{uid})" stroke="#000" stroke-opacity="0.18" stroke-width="2"/>')
    p.append('<path d="M424 164 Q500 250 576 164" fill="none" stroke="#000" stroke-opacity="0.16" stroke-width="7"/>')
    sw = 470.0; sc = sw / PLATE_W; px = (1000 - sw) / 2; py = 292
    p.append(f'<g transform="translate({px:.1f},{py:.1f}) scale({sc:.4f})">{vintage_inner(car, show_ground=False)}</g>')
    return "".join(p), 1000, 1180

def svg_tag(inner, w, h, cls):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'

CSS = """
:root{--bg:#221E17;--wall:#2A251C;--card:#322C21;--ink:#EDE6D6;--mute:#A79F8C;
  --line:rgba(237,230,214,.16);--line2:rgba(237,230,214,.08);--spot:#C08A3E}
:root[data-theme="light"]{--bg:#DED3B9;--wall:#D6CBAF;--card:#CFC3A4;--ink:#221E17;
  --mute:#6A6250;--line:rgba(34,30,23,.20);--line2:rgba(34,30,23,.09);--spot:#8A5A28}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#DED3B9;--wall:#D6CBAF;
  --card:#CFC3A4;--ink:#221E17;--mute:#6A6250;--line:rgba(34,30,23,.20);--line2:rgba(34,30,23,.09);--spot:#8A5A28}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Serif',Georgia,serif;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.grot{font-family:'Grot','Arial Black',sans-serif}
.wrap{max-width:1220px;margin:0 auto;padding:0 26px}
a{color:inherit}
header.hero{padding:70px 0 44px;border-bottom:1px solid var(--line)}
.kick{font-family:'Grot';font-weight:700;font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
.hero h1{font-family:'Grot';font-weight:900;font-size:clamp(70px,14vw,190px);line-height:.84;margin:12px 0 0;letter-spacing:-.01em}
.hero .s{font-family:'Grot';font-weight:700;font-size:clamp(14px,2.4vw,20px);letter-spacing:.3em;text-transform:uppercase;color:var(--mute);margin-top:16px}
.hero .lede{max-width:62ch;font-size:18px;font-style:italic;margin:26px 0 0}
.hero .meta{font-family:'Grot';display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:24px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
section{padding:58px 0;border-bottom:1px solid var(--line)}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:32px;flex-wrap:wrap}
.shead h2{font-family:'Grot';font-weight:900;font-size:clamp(28px,5vw,52px);margin:0;letter-spacing:-.01em}
.shead p{margin:0;max-width:46ch;color:var(--mute);font-style:italic;font-size:16px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:26px}
@media(max-width:760px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line2);border-radius:5px;padding:16px;transition:transform .3s,box-shadow .3s}
.card:hover{transform:translateY(-4px);box-shadow:0 26px 60px rgba(0,0,0,.42)}
.card .art{display:block;width:100%;height:auto;box-shadow:0 12px 34px rgba(0,0,0,.36)}
.cap{display:flex;justify-content:space-between;align-items:baseline;margin-top:14px;gap:12px;font-family:'Grot'}
.cap .t{font-weight:900;font-size:18px;letter-spacing:.01em}
.cap .c{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute)}
.tees{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
@media(max-width:760px){.tees{grid-template-columns:1fr}}
.tee{background:var(--wall);border:1px solid var(--line2);border-radius:5px;padding:14px}
.tee svg{display:block;width:100%;height:auto}
.tee .l{font-family:'Grot';margin-top:8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);text-align:center}
.mini{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
@media(max-width:760px){.mini{grid-template-columns:repeat(2,1fr)}}
.mini .art{display:block;width:100%;height:auto;border-radius:3px;box-shadow:0 8px 22px rgba(0,0,0,.3)}
.note{font-size:15px;color:var(--mute);max-width:70ch}
.note b{color:var(--ink)} .note ul{padding-left:18px}
footer{padding:40px 0 72px;color:var(--mute);font-family:'Grot';font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.toggle{position:fixed;top:16px;right:16px;z-index:9;background:var(--card);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def gallery():
    FONT = FONT_CSS_V + gen.FONT_CSS
    vcards = []
    for c in CARS:
        vcards.append(f'<figure class="card">{svg_tag(vintage_inner(c),PLATE_W,PLATE_H,"art")}'
                      f'<figcaption class="cap"><span class="t">{esc(c["make"].title())} {esc(c["model"])}</span>'
                      f'<span class="c">Made in {esc(c["country"].title())}</span></figcaption></figure>')
    vgrid = '<div class="grid">'+"".join(vcards)+'</div>'

    tees = []
    for key, g in [("porsche","bone"),("etype","oat"),("countach","sand")]:
        inner,w,h = vtee_inner(CMAP[key], g)
        tees.append(f'<div class="tee">{svg_tag(inner,w,h,"t")}<div class="l">{esc(CMAP[key]["model"])} · {g} tee</div></div>')
    vtees = '<div class="tees">'+"".join(tees)+'</div>'

    minis = "".join(f'<div>{svg_tag(plate_inner(c),PLATE_W,PLATE_H,"art")}</div>' for c in CARS)
    mini = '<div class="mini">'+minis+'</div>'

    note = ('<p class="note"><b>On selling.</b> Copy and silhouettes are original; the ad lines are written for '
            'this project, not lifted from any manufacturer. Marque &amp; model <b>names are trademarks</b>, so for a '
            'print-on-demand launch a "safe mode" swaps the marque for era + chassis code + origin '
            '(e.g. <em>TYPE&nbsp;993 · GERMANY · 1993</em>) and keeps every other element identical. '
            'The reference site autocatalogarchive.com is blocked by this environment, so its PDFs weren\'t used or needed.</p>')

    body = f"""
<button class="toggle grot" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header class="hero"><div class="wrap">
  <div class="kick">Series 02 — Vintage Cut</div>
  <h1 class="grot">MARQUE</h1>
  <div class="s">World Motor Index</div>
  <p class="lede">Ten machines, drawn as if they were torn from a 1970s magazine spread: a bold headline, a blueprint with the real dimensions, a line of ad copy — and a small stamp for the country that built it. Every poster from the same template, so the whole line hangs together.</p>
  <div class="meta"><span>10 plates</span><span>Blueprint + ad copy</span><span>Tees · Prints · Calendars</span><span>Made-in flag stamp</span></div>
</div></header>

<section><div class="wrap"><div class="shead"><h2 class="grot">The archive</h2><p>Same template, ten origins — the spot colour and the flag change, nothing else.</p></div>{vgrid}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">On the blank</h2><p>Dark ink on cream cotton — the way the old ads were printed.</p></div>{vtees}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Series 01 — the modern cut</h2><p>The first pass: a technical spec-plate on dark garments. Same cars, same system, different voice — kept here so you can compare.</p></div>{mini}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Notes</h2></div>{note}</div></section>
<footer><div class="wrap">MARQUE™ · World Motor Index · Series 01 + 02 · one uniform system</div></footer>
"""
    return f'<style>{FONT}{CSS}</style>{body}'

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT,"vintage"), exist_ok=True)
    os.makedirs(os.path.join(OUT,"mockups"), exist_ok=True)
    for c in CARS:
        open(os.path.join(OUT,"vintage",f'{c["no"]:02d}_{c["key"]}.svg'),"w").write(v_standalone(c))
    def wrap(inner,w,h):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
                f'<defs><style>{FONT_CSS_V}</style></defs>{inner}</svg>')
    ti,tw,th = vtee_inner(CMAP["porsche"],"bone")
    open(os.path.join(OUT,"mockups","vtee_porsche_bone.svg"),"w").write(wrap(ti,tw,th))
    open(os.path.join(OUT,"gallery.html"),"w").write(gallery())
    print("wrote combined gallery + vintage plates + vintage tee")
