# -*- coding: utf-8 -*-
"""Lookbook v3 — leads with Series 03 (Art / car-hero), then Series 02 (Vintage)
and Series 01 (Modern) as compact strips. Republishes to gallery.html."""
import os
import gen, vintage, poster
from gen import CARS, font_face, esc, plate_inner, PLATE_W, PLATE_H
from vintage import vintage_inner
from poster import poster_inner, poster_badge

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
CMAP = {c["key"]: c for c in CARS}

FONTS = "".join([
    font_face("Grot",900,"archivo/files/archivo-latin-900-normal.woff2"),
    font_face("Grot",700,"archivo/files/archivo-latin-700-normal.woff2"),
    font_face("Saira",600,"saira-condensed/files/saira-condensed-latin-600-normal.woff2"),
    font_face("Saira",700,"saira-condensed/files/saira-condensed-latin-700-normal.woff2"),
    font_face("Saira",800,"saira-condensed/files/saira-condensed-latin-800-normal.woff2"),
    font_face("Plex",400,"ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2"),
    font_face("Plex",600,"ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2"),
    font_face("Serif",400,"libre-baskerville/files/libre-baskerville-latin-400-normal.woff2"),
    font_face("SerifI",400,"libre-baskerville/files/libre-baskerville-latin-400-italic.woff2"),
])

GARMENTS = {"black":"#17181C","sand":"#E1D8C0","charcoal":"#2C2E34"}

def tee_badge(car, garment):
    base = GARMENTS[garment]
    p=[f'<ellipse cx="500" cy="1120" rx="330" ry="34" fill="#000" fill-opacity="0.20"/>']
    tee=("M335 170 L430 165 Q500 240 570 165 L665 170 L835 190 L890 372 "
         "L715 346 L764 1082 L236 1082 L285 346 L110 372 L165 190 Z")
    p.append(f'<path d="{tee}" fill="{base}" stroke="#000" stroke-opacity="0.22" stroke-width="2"/>')
    p.append('<path d="M424 164 Q500 250 576 164" fill="none" stroke="#000" stroke-opacity="0.22" stroke-width="7"/>')
    bw=560.0; sc=bw/1000.0; bx=(1000-bw)/2; by=300
    p.append(f'<g transform="translate({bx:.0f},{by:.0f}) scale({sc:.4f})">{poster_badge(car)}</g>')
    return "".join(p),1000,1180

def svg_tag(inner,w,h,cls):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'

CSS="""
:root{--bg:#22201A;--wall:#2A271F;--card:#EDE6D6;--ink:#EDE6D6;--mute:#A79F8C;--line:rgba(237,230,214,.16);--line2:rgba(237,230,214,.08);--spot:#C79A4E}
:root[data-theme="light"]{--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.20);--line2:rgba(35,31,23,.08);--spot:#8A5A28}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.20);--line2:rgba(35,31,23,.08);--spot:#8A5A28}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Serif',Georgia,serif;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.grot{font-family:'Grot','Arial Black',sans-serif}
.wrap{max-width:1220px;margin:0 auto;padding:0 26px}
header.hero{padding:70px 0 44px;border-bottom:1px solid var(--line)}
.kick{font-family:'Grot';font-weight:700;font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--spot)}
.hero h1{font-family:'Grot';font-weight:900;font-size:clamp(70px,14vw,196px);line-height:.84;margin:12px 0 0;letter-spacing:-.01em}
.hero .s{font-family:'Grot';font-weight:700;font-size:clamp(14px,2.4vw,20px);letter-spacing:.3em;text-transform:uppercase;color:var(--mute);margin-top:16px}
.hero .lede{max-width:60ch;font-size:18px;font-style:italic;margin:26px 0 0}
.hero .meta{font-family:'Grot';display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:24px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
section{padding:58px 0;border-bottom:1px solid var(--line)}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:20px;margin-bottom:32px;flex-wrap:wrap}
.shead h2{font-family:'Grot';font-weight:900;font-size:clamp(28px,5vw,52px);margin:0;letter-spacing:-.01em}
.shead p{margin:0;max-width:48ch;color:var(--mute);font-style:italic;font-size:16px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:26px}
@media(max-width:760px){.grid{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--line2);border-radius:5px;padding:14px;transition:transform .3s,box-shadow .3s}
.card:hover{transform:translateY(-4px);box-shadow:0 26px 60px rgba(0,0,0,.45)}
.card .art{display:block;width:100%;height:auto}
.cap{display:flex;justify-content:space-between;align-items:baseline;margin-top:12px;gap:12px;font-family:'Grot';color:#231F17}
.cap .t{font-weight:900;font-size:18px}
.cap .c{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#8A8474}
.tees{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
@media(max-width:760px){.tees{grid-template-columns:1fr}}
.tee{background:var(--wall);border:1px solid var(--line2);border-radius:5px;padding:14px}
.tee svg{display:block;width:100%;height:auto}
.tee .l{font-family:'Grot';margin-top:8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);text-align:center}
.mini{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
@media(max-width:760px){.mini{grid-template-columns:repeat(2,1fr)}}
.mini .art{display:block;width:100%;height:auto;border-radius:3px;box-shadow:0 8px 22px rgba(0,0,0,.32)}
.note{font-size:15px;color:var(--mute);max-width:72ch}.note b{color:var(--ink)}.note ul{padding-left:18px}
footer{padding:40px 0 72px;color:var(--mute);font-family:'Grot';font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.toggle{position:fixed;top:16px;right:16px;z-index:9;background:var(--wall);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def gallery():
    art=[]
    for c in CARS:
        art.append(f'<figure class="card">{svg_tag(poster_inner(c),PLATE_W,PLATE_H,"art")}'
                   f'<figcaption class="cap"><span class="t">{esc(c["model"])}</span>'
                   f'<span class="c">{esc(c["make"].title())} · {esc(c["country"].title())}</span></figcaption></figure>')
    agrid='<div class="grid">'+"".join(art)+'</div>'

    tees=[]
    for key,g in [("porsche","black"),("skyline","sand"),("countach","charcoal")]:
        inner,w,h=tee_badge(CMAP[key],g)
        tees.append(f'<div class="tee">{svg_tag(inner,w,h,"t")}<div class="l">{esc(CMAP[key]["model"])} · {g} tee</div></div>')
    tees_html='<div class="tees">'+"".join(tees)+'</div>'

    vmini="".join(f'<div>{svg_tag(vintage_inner(c),PLATE_W,PLATE_H,"art")}</div>' for c in CARS)
    mmini="".join(f'<div>{svg_tag(plate_inner(c),PLATE_W,PLATE_H,"art")}</div>' for c in CARS)

    note=('<p class="note"><b>Three cuts, one system.</b> Every product is generated from the same car dataset — '
          'change the voice, keep the line coherent. Art (car-hero badge), Vintage (1970s ad), Modern (spec-plate). '
          'Silhouettes, colours and copy are original; marque &amp; model <b>names are trademarks</b>, so a POD launch '
          'can run in "safe mode" (era + chassis code + origin). The reference site autocatalogarchive.com is blocked by '
          'this environment, so its PDFs weren\'t used or needed.</p>')

    body=f"""
<button class="toggle grot" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header class="hero"><div class="wrap">
  <div class="kick">Series 03 — Art Cut</div>
  <h1 class="grot">MARQUE</h1>
  <div class="s">World Motor Index</div>
  <p class="lede">The car, front and centre. Each machine is drawn as a poster — painted body, tinted glass, real alloys — mounted on a tonal stage in its own colour, with the type pulled right back. Ten origins, one badge template; the flag decides the palette, the car does the talking.</p>
  <div class="meta"><span>10 car-hero posters</span><span>Tonal stage per marque</span><span>Tees · Prints · Calendars</span></div>
</div></header>

<section><div class="wrap"><div class="shead"><h2 class="grot">The archive</h2><p>Same badge, ten cars — the disc takes the car's colour, the type stays quiet.</p></div>{agrid}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">On the blank</h2><p>The emblem is self-contained, so it drops onto any garment colour.</p></div>{tees_html}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Also in the system — Vintage</h2><p>Series 02: the 1970s print-ad cut, for cream tees.</p></div><div class="mini">{vmini}</div></div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Also in the system — Modern</h2><p>Series 01: the technical spec-plate, for dark tees.</p></div><div class="mini">{mmini}</div></div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Notes</h2></div>{note}</div></section>
<footer><div class="wrap">MARQUE™ · World Motor Index · Series 01 + 02 + 03 · one uniform system</div></footer>
"""
    return f'<style>{FONTS}{CSS}</style>{body}'

if __name__=="__main__":
    os.makedirs(os.path.join(OUT,"art"),exist_ok=True)
    for c in CARS:
        open(os.path.join(OUT,"art",f'{c["no"]:02d}_{c["key"]}.svg'),"w").write(poster.standalone(c))
    def wrap(inner,w,h):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
                f'<defs><style>{poster.FONT_CSS_P}</style></defs>{inner}</svg>')
    ti,tw,th=tee_badge(CMAP["porsche"],"black")
    open(os.path.join(OUT,"mockups","atee_porsche_black.svg"),"w").write(wrap(ti,tw,th))
    open(os.path.join(OUT,"gallery.html"),"w").write(gallery())
    print("wrote v3 gallery + art posters + art tee")
