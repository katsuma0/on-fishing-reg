# -*- coding: utf-8 -*-
"""Build deliverables: standalone plate SVGs, garment + calendar mockups,
and a self-contained lookbook gallery (fonts embedded once)."""
import os, html
from gen import (CARS, plate_inner, standalone_svg, FONT_CSS, T, esc,
                 INK, CREAM, MUTE, PLATE_W, PLATE_H)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# ---------------------------------------------------------------- garment tee
GARMENTS = {
    "black":    ("#17181C", "#0E0F12"),
    "charcoal": ("#2C2E34", "#1D1E23"),
    "navy":     ("#1B2536", "#121A28"),
}

def tee_inner(car, garment="black"):
    base, dark = GARMENTS[garment]
    a = car["accent"]
    uid = f'tee{car["key"]}'
    p = []
    p.append(f'<defs><radialGradient id="g{uid}" cx="50%" cy="34%" r="62%">'
             f'<stop offset="0%" stop-color="{base}"/><stop offset="100%" stop-color="{dark}"/>'
             f'</radialGradient></defs>')
    # soft floor shadow
    p.append(f'<ellipse cx="500" cy="1120" rx="330" ry="34" fill="#000" fill-opacity="0.28"/>')
    tee = ("M335 170 L430 165 Q500 240 570 165 L665 170 L835 190 L890 372 "
           "L715 346 L764 1082 L236 1082 L285 346 L110 372 L165 190 Z")
    p.append(f'<path d="{tee}" fill="url(#g{uid})" stroke="#000" stroke-opacity="0.35" stroke-width="2"/>')
    # collar rib
    p.append('<path d="M424 164 Q500 250 576 164" fill="none" stroke="#000" stroke-opacity="0.30" stroke-width="7"/>')
    p.append('<path d="M430 172 Q500 238 570 172" fill="none" stroke="#fff" stroke-opacity="0.06" stroke-width="4"/>')
    # sleeve hem hints
    p.append('<path d="M150 300 L200 322" stroke="#000" stroke-opacity="0.22" stroke-width="6"/>')
    p.append('<path d="M850 300 L800 322" stroke="#000" stroke-opacity="0.22" stroke-width="6"/>')
    # chest print: the transparent plate art
    sw = 470.0
    sc = sw / PLATE_W
    px = (1000 - sw) / 2
    py = 292
    p.append(f'<g transform="translate({px:.1f},{py:.1f}) scale({sc:.4f})">{plate_inner(car, show_ground=False)}</g>')
    return "".join(p), 1000, 1180

# ------------------------------------------------------------------- calendar
def _month_grid(first_wd, days, circle_day, a):
    """7-col month grid starting Sunday; returns SVG for weekday header + dates."""
    hdr = ["S", "M", "T", "W", "T", "F", "S"]
    out = []
    x0, y0, cw, ch = 60, 946, (880) / 7.0, 66
    for i, d in enumerate(hdr):
        out.append(T(x0 + i*cw + cw/2, y0, d, 20, "Plex", 600, MUTE, anchor="middle", ls=1))
    day = 1
    row = 0
    col = first_wd
    while day <= days:
        cx = x0 + col*cw + cw/2
        cy = y0 + 44 + row*ch
        if day == circle_day:
            out.append(f'<circle cx="{cx:.1f}" cy="{cy-10:.1f}" r="27" fill="{a}"/>')
            out.append(T(cx, cy, str(day), 30, "Saira", 600, "#14151A", anchor="middle"))
        else:
            out.append(T(cx, cy, str(day), 30, "Saira", 600, CREAM, anchor="middle"))
        col += 1
        if col > 6:
            col = 0; row += 1
        day += 1
    return "".join(out)

def calendar_inner(car, month="MARCH", year="2026", first_wd=0, days=31):
    a = car["accent"]
    uid = f'cal{car["key"]}'
    W, H = 1000, 1360
    p = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{INK}"/>']
    p.append(f'<rect x="8" y="8" width="{W-16}" height="{H-16}" fill="none" stroke="{CREAM}" stroke-width="1.5" stroke-opacity="0.25"/>')
    # spiral binding
    for i in range(14):
        bx = 70 + i*63
        p.append(f'<rect x="{bx-9}" y="26" width="18" height="34" rx="9" fill="none" stroke="{MUTE}" stroke-width="4"/>')
    # image window (letterboxed plate)
    wx, wy, ww, wh = 50, 84, 900, 700
    p.append(f'<clipPath id="{uid}"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}"/></clipPath>')
    p.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="#0C0D10"/>')
    sc = wh / PLATE_H                       # contain-fit by height (whole plate visible)
    pw = PLATE_W * sc
    ox = wx + (ww - pw) / 2
    oy = wy
    p.append(f'<g clip-path="url(#{uid})"><g transform="translate({ox:.1f},{oy:.1f}) scale({sc:.4f})">'
             f'{plate_inner(car, show_ground=True)}</g></g>')
    p.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="none" stroke="{CREAM}" stroke-width="2" stroke-opacity="0.3"/>')
    # month header
    p.append(T(60, 878, month, 96, "Saira", 800, CREAM))
    p.append(T(940, 838, year, 26, "Plex", 400, MUTE, anchor="end", ls=3))
    p.append(T(940, 878, f"No.{car['no']:02d} · {car['model']} · {car['country']}", 20, "Plex", 400, a, anchor="end", ls=1))
    p.append(f'<line x1="60" y1="906" x2="940" y2="906" stroke="{CREAM}" stroke-width="1.5" stroke-opacity="0.28"/>')
    p.append(_month_grid(first_wd, days, car["no"], a))
    p.append(f'<line x1="60" y1="1300" x2="940" y2="1300" stroke="{a}" stroke-width="2.5"/>')
    p.append(T(60, 1334, "MARQUE™ CALENDAR · WORLD MOTOR INDEX · 12 ORIGINS", 14, "Plex", 400, MUTE, ls=1))
    return "".join(p), W, H

# ------------------------------------------------------------------- gallery
PAGE_CSS = """
:root{
  --bg:#101116; --panel:#16171D; --card:#1B1C22; --ink:#ECE7DB; --mute:#8F8B80;
  --line:rgba(236,231,219,.16); --line2:rgba(236,231,219,.09);
}
:root[data-theme="light"]{
  --bg:#E9E4D8; --panel:#F2EDE2; --card:#EFE9DD; --ink:#1B1C22; --mute:#6B675E;
  --line:rgba(27,28,34,.18); --line2:rgba(27,28,34,.08);
}
@media (prefers-color-scheme:light){
  :root:not([data-theme="dark"]){
    --bg:#E9E4D8; --panel:#F2EDE2; --card:#EFE9DD; --ink:#1B1C22; --mute:#6B675E;
    --line:rgba(27,28,34,.18); --line2:rgba(27,28,34,.08);
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'Plex',ui-monospace,monospace;line-height:1.65;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
.saira{font-family:'Saira','Arial Narrow',sans-serif}
.eyebrow{font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--mute)}
a{color:inherit}
hr.rule{border:0;border-top:1px solid var(--line);margin:0}

header.hero{padding:64px 0 40px;border-bottom:1px solid var(--line)}
.hero .mk{font-family:'Saira';font-weight:800;font-size:clamp(64px,13vw,168px);
  line-height:.86;letter-spacing:.01em;margin:14px 0 0;text-wrap:balance}
.hero .sub{font-size:clamp(13px,2.2vw,17px);letter-spacing:.42em;color:var(--mute);
  text-transform:uppercase;margin-top:14px}
.hero .lede{max-width:60ch;margin:28px 0 0;font-size:15.5px;color:var(--ink)}
.hero .meta{display:flex;flex-wrap:wrap;gap:10px 26px;margin-top:26px;
  font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}
.hero .meta b{color:var(--ink);font-weight:600}
.ticker{margin-top:30px;display:flex;flex-wrap:wrap;gap:8px}
.iso{font-size:11px;letter-spacing:.14em;border:1px solid var(--line);
  padding:5px 9px;color:var(--mute)}

section{padding:56px 0;border-bottom:1px solid var(--line)}
.shead{display:flex;align-items:baseline;justify-content:space-between;gap:20px;
  margin-bottom:34px;flex-wrap:wrap}
.shead h2{font-family:'Saira';font-weight:800;font-size:clamp(26px,4.4vw,46px);
  margin:0;letter-spacing:.005em}
.shead p{margin:0;max-width:44ch;color:var(--mute);font-size:14px}
.num{color:var(--mute);font-size:12px;letter-spacing:.24em}

.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:26px}
@media(max-width:720px){.grid{grid-template-columns:1fr;gap:20px}}
.card{background:var(--card);border:1px solid var(--line2);border-radius:6px;
  padding:20px;transition:transform .35s ease, box-shadow .35s ease}
.card:hover{transform:translateY(-4px);box-shadow:0 24px 60px rgba(0,0,0,.4)}
.card .art{display:block;width:100%;height:auto;border-radius:2px;
  box-shadow:0 10px 34px rgba(0,0,0,.34)}
.cap{display:flex;justify-content:space-between;align-items:baseline;
  margin-top:16px;gap:12px}
.cap .t{font-family:'Saira';font-weight:600;font-size:19px;letter-spacing:.02em}
.cap .c{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}

.tees{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
@media(max-width:720px){.tees{grid-template-columns:1fr}}
.tee{background:var(--panel);border:1px solid var(--line2);border-radius:6px;padding:14px}
.tee svg{display:block;width:100%;height:auto}
.tee .lbl{margin-top:8px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--mute);text-align:center}

.caljoin{display:grid;grid-template-columns:1.05fr .95fr;gap:34px;align-items:center}
@media(max-width:820px){.caljoin{grid-template-columns:1fr}}
.calwrap{background:var(--panel);border:1px solid var(--line2);border-radius:6px;padding:16px}
.calwrap svg{display:block;width:100%;height:auto;box-shadow:0 14px 40px rgba(0,0,0,.34)}
.calnote h3{font-family:'Saira';font-weight:800;font-size:30px;margin:0 0 10px}
.calnote p{color:var(--mute);font-size:14.5px;margin:0 0 14px;max-width:46ch}

.sys{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:720px){.sys{grid-template-columns:1fr}}
.sys .box{border:1px solid var(--line);padding:18px 20px;border-radius:4px}
.sys .box h4{margin:0 0 12px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}
.sys ul{margin:0;padding:0;list-style:none}
.sys li{padding:7px 0;border-top:1px solid var(--line2);font-size:14px;display:flex;gap:12px}
.sys li:first-child{border-top:0}
.sys li b{font-family:'Saira';font-weight:600;min-width:104px;letter-spacing:.02em}

.note{font-size:13.5px;color:var(--mute);max-width:70ch}
.note b{color:var(--ink);font-weight:600}
.note ul{padding-left:18px}
footer{padding:40px 0 70px;color:var(--mute);font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.toggle{position:fixed;top:16px;right:16px;z-index:9;background:var(--card);
  border:1px solid var(--line);color:var(--ink);font-family:'Plex';font-size:11px;
  letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def svg_tag(inner, w, h, cls):
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'

def build_gallery():
    cards = []
    for car in CARS:
        art = svg_tag(plate_inner(car), PLATE_W, PLATE_H, "art")
        cards.append(
            f'<figure class="card">{art}'
            f'<figcaption class="cap"><span class="t">{esc(car["make"].title())} '
            f'{esc(car["model"])}</span>'
            f'<span class="c">{esc(car["country"])} · No.{car["no"]:02d}</span></figcaption></figure>')
    grid = '<div class="grid">' + "".join(cards) + '</div>'

    tee_specs = [("skyline", "black"), ("countach", "charcoal"), ("ioniq", "navy")]
    tees = []
    cmap = {c["key"]: c for c in CARS}
    for key, g in tee_specs:
        inner, w, h = tee_inner(cmap[key], g)
        tees.append(f'<div class="tee">{svg_tag(inner, w, h, "teesvg")}'
                    f'<div class="lbl">{esc(cmap[key]["model"])} · {g} tee</div></div>')
    tees_html = '<div class="tees">' + "".join(tees) + '</div>'

    cinner, cw, ch = calendar_inner(cmap["countach"], "MARCH", "2026", first_wd=0, days=31)
    cal_html = (
        '<div class="caljoin"><div class="calwrap">' + svg_tag(cinner, cw, ch, "calsvg") + '</div>'
        '<div class="calnote"><h3>Twelve origins, twelve months.</h3>'
        '<p>The same plate becomes a calendar page — one machine per month, the origin flag as the color of the month. '
        'A wall calendar that reads as one collection, not twelve stock photos.</p>'
        '<p>Print-ready at A3 / 12&times;12in. Every month shares the frame, the housemark, the spec grid and the barcode line — '
        'so a customer who buys the calendar and a customer who buys the tee own the same brand.</p></div></div>')

    dna = ["Frame + corner crop-marks", "MARQUE housemark + WORLD MOTOR INDEX",
           "No. XX / 10 registry number", "Full-bleed MAKE / MODEL wordmark",
           "National-flag origin stamp", "Monospace 6-cell spec grid",
           "Footer registry line + barcode", "Saira Condensed + IBM Plex Mono"]
    var = [("Model", "the car's name, set to the same weight every time"),
           ("Flag", "drawn from the country of manufacture"),
           ("Accent", "one colour pulled from that flag, recolouring the whole plate"),
           ("Silhouette", "a side-profile from one shared line-art family"),
           ("Spec grid", "six factual data points"),
           ("Entry No.", "its place in the archive, 01–10")]
    sys_html = (
        '<div class="sys"><div class="box"><h4>Constant — the DNA</h4><ul>'
        + "".join(f'<li>{esc(x)}</li>' for x in dna) +
        '</ul></div><div class="box"><h4>Variable — per machine</h4><ul>'
        + "".join(f'<li><b>{esc(k)}</b><span>{esc(v)}</span></li>' for k, v in var) +
        '</ul></div></div>')

    isos = "".join(f'<span class="iso">{c["iso"]} · {c["make"]}</span>' for c in CARS)

    note_html = (
        '<p class="note"><b>On the source & selling.</b> These designs are built from public, factual '
        'reference — country of origin, drivetrain, era, national flags — not from copyrighted brochure '
        'artwork. The flags are public domain and the specs are facts. Two things to keep in mind before a '
        'print-on-demand launch:</p>'
        '<ul class="note"><li><b>Marque &amp; model names are trademarks.</b> Printing “PORSCHE 911” or “SKYLINE GT-R” '
        'on a shirt to sell is trademark use — POD platforms (Printful, Redbubble, Teespring) routinely take those '
        'listings down. A “safe mode” of this template swaps the marque for the era + chassis code + origin '
        '(e.g. “TYPE BNR34 · JAPAN · 1999”) and keeps every other element, so the line still looks identical.</li>'
        '<li><b>The brochure PDFs weren’t needed and can’t be scraped here</b> — this environment blocks '
        'autocatalogarchive.com at the network level. The design system stands on its own facts.</li></ul>')

    body = f"""
<button class="toggle" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')|| (matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header class="hero"><div class="wrap">
  <div class="eyebrow">Series 01 — A design system for print-on-demand</div>
  <h1 class="mk saira">MARQUE</h1>
  <div class="sub">World Motor Index</div>
  <p class="lede">Ten machines. Ten countries. One template. A collectible “archive plate” for every car —
  built so a t-shirt, a print and a calendar all read, at a glance, as the same line. The colour comes from
  the flag of the country that built the car; everything else stays fixed.</p>
  <div class="meta"><span><b>10</b> plates</span><span><b>10</b> origins</span>
  <span><b>1</b> template</span><span>tees · prints · <b>calendars</b></span></div>
  <div class="ticker">{isos}</div>
</div></header>

<section><div class="wrap">
  <div class="shead"><h2 class="saira">The archive</h2>
  <p>Every plate is generated from the same code — change the data, the design stays uniform.</p></div>
  {grid}
</div></section>

<section><div class="wrap">
  <div class="shead"><h2 class="saira">On the blank</h2><p>The same artwork, placed on the garment. Built for dark tees so the cream ink and flag read cleanly.</p></div>
  {tees_html}
</div></section>

<section><div class="wrap">
  <div class="shead"><h2 class="saira">The calendar</h2><span class="num">DROP-SHIP / A3 / 12×12in</span></div>
  {cal_html}
</div></section>

<section><div class="wrap">
  <div class="shead"><h2 class="saira">The system</h2><p>Why every product looks noticeably from this one project.</p></div>
  {sys_html}
</div></section>

<section><div class="wrap">
  <div class="shead"><h2 class="saira">Notes</h2></div>
  {note_html}
</div></section>

<footer><div class="wrap">MARQUE™ · World Motor Index · Series 01 · A uniform design system · {len(CARS)} plates</div></footer>
"""
    return f'<style>{FONT_CSS}{PAGE_CSS}</style>{body}'

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "mockups"), exist_ok=True)
    for car in CARS:
        open(os.path.join(OUT, "svg", f'{car["no"]:02d}_{car["key"]}.svg'), "w").write(standalone_svg(car))
    # standalone mockups (with fonts) for a couple, for sending as files
    def wrap(inner, w, h):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
                f'<defs><style>{FONT_CSS}</style></defs>{inner}</svg>')
    cmap = {c["key"]: c for c in CARS}
    ti, tw, th = tee_inner(cmap["skyline"], "black")
    open(os.path.join(OUT, "mockups", "tee_skyline_black.svg"), "w").write(wrap(ti, tw, th))
    ci, cw, ch = calendar_inner(cmap["countach"])
    open(os.path.join(OUT, "mockups", "calendar_march_countach.svg"), "w").write(wrap(ci, cw, ch))
    open(os.path.join(OUT, "gallery.html"), "w").write(build_gallery())
    print("wrote out/gallery.html + svgs + mockups")
