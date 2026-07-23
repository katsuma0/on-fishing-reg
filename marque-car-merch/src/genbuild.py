# -*- coding: utf-8 -*-
"""Generic per-brand calendar builder (2027). Reusable for any brand module."""
import os
from styles import calendar_page, page_svg, FONTS, PW, PH
from gen import esc

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")
MONTHS=[("JANUARY",5,31),("FEBRUARY",1,28),("MARCH",1,31),("APRIL",4,30),
        ("MAY",6,31),("JUNE",2,30),("JULY",4,31),("AUGUST",0,31),
        ("SEPTEMBER",3,30),("OCTOBER",5,31),("NOVEMBER",1,30),("DECEMBER",3,31)]
YEAR="2027"

def _css(spot):
    return f""":root{{--bg:#201D17;--wall:#2A261E;--card:#0E0D0B;--ink:#EDE6D6;--mute:#A79F8C;--line:rgba(237,230,214,.16);--line2:rgba(237,230,214,.08);--spot:{spot}}}
:root[data-theme="light"]{{--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.2);--line2:rgba(35,31,23,.08);--spot:{spot}}}
@media(prefers-color-scheme:light){{:root:not([data-theme="dark"]){{--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.2);--line2:rgba(35,31,23,.08);--spot:{spot}}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:'Serif',Georgia,serif;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
.grot{{font-family:'Grot','Arial Black',sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 26px}}
header.hero{{padding:66px 0 40px;border-bottom:1px solid var(--line)}}
.kick{{font-family:'Grot';font-weight:700;font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--spot)}}
.hero h1{{font-family:'Grot';font-weight:900;font-size:clamp(56px,11vw,150px);line-height:.86;margin:12px 0 0;letter-spacing:-.01em}}
.hero .s{{font-family:'Grot';font-weight:700;font-size:clamp(13px,2.2vw,19px);letter-spacing:.3em;text-transform:uppercase;color:var(--mute);margin-top:14px}}
.hero .lede{{max-width:62ch;font-size:17px;font-style:italic;margin:22px 0 0}}
section{{padding:52px 0;border-bottom:1px solid var(--line)}}
.shead{{margin-bottom:28px}}
.shead h2{{font-family:'Grot';font-weight:900;font-size:clamp(24px,4.4vw,44px);margin:0}}
.shead p{{margin:8px 0 0;max-width:60ch;color:var(--mute);font-style:italic}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
@media(max-width:900px){{.grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:560px){{.grid{{grid-template-columns:1fr}}}}
.m{{background:var(--card);border:1px solid var(--line2);border-radius:5px;overflow:hidden}}
.m .art{{display:block;width:100%;height:auto}}
.note{{font-size:15px;color:var(--mute);max-width:74ch}}.note b{{color:var(--ink)}}
footer{{padding:38px 0 70px;color:var(--mute);font-family:'Grot';font-size:12px;letter-spacing:.14em;text-transform:uppercase}}
.toggle{{position:fixed;top:16px;right:16px;z-index:9;background:var(--wall);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}}"""

def _tag(inner):
    return f'<svg class="art" viewBox="0 0 {PW} {PH}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'

def build(brand, country, cars, prefix, spot):
    os.makedirs(os.path.join(OUT,f"{prefix}_cal"),exist_ok=True)
    for i,c in enumerate(cars):
        mn,fw,dd=MONTHS[i]
        open(os.path.join(OUT,f"{prefix}_cal",f"{i+1:02d}_{mn.lower()}_{c['key']}.svg"),"w").write(
            page_svg(c,"rally",month=mn,year=YEAR,first_wd=fw,days=dd))
    cells="".join(f'<div class="m">{_tag(calendar_page(c,"rally",month=MONTHS[i][0],year=YEAR,first_wd=MONTHS[i][1],days=MONTHS[i][2]))}</div>' for i,c in enumerate(cars))
    note=(f'<p class="note"><b>The {brand.title()} year.</b> Twelve icons, one per month, cel-shaded Rally style '
          f'with drivetrain-encoded wheels and a subtle {country} origin motif. Same template across every MARQUE brand '
          f'calendar, so the whole shelf hangs together.</p>'
          f'<p class="note">Marks are trademarks; design study — licence or use a mark-free cut for sale.</p>')
    body=f"""<style>{FONTS}{_css(spot)}</style>
<button class="toggle grot" onclick="(function(){{{{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}}}})()">Theme</button>
<header class="hero"><div class="wrap"><div class="kick">Rally Calendar · 2027 · {esc(country)}</div>
<h1 class="grot">{esc(brand)}<br>THE YEAR.</h1><div class="s">A MARQUE World Motor Index Calendar</div>
<p class="lede">Twelve icons from one marque, one per month, in the cel-shaded Retro Rally style — drivetrain wheels, subtle origin motif, sharp vector.</p></div></header>
<section><div class="wrap"><div class="shead"><h2 class="grot">The 2027 wall</h2><p>January → December.</p></div><div class="grid">{cells}</div></div></section>
<section><div class="wrap"><div class="shead"><h2 class="grot">Notes</h2></div>{note}</div></section>
<footer><div class="wrap">MARQUE™ · {esc(brand)} Rally Calendar 2027 · vector · uniform 12-month</div></footer>"""
    open(os.path.join(OUT,f"{prefix}_calendar.html"),"w").write(body)
    # spread
    cols=3; sc=0.34; cw=int(PW*sc); ch=int(PH*sc); rows=(len(cars)+cols-1)//cols; W,H=cols*cw,rows*ch
    b=[f'<rect width="{W}" height="{H}" fill="#2A261E"/>']
    for i,c in enumerate(cars):
        mn,fw,dd=MONTHS[i]; gx=(i%cols)*cw; gy=(i//cols)*ch
        b.append(f'<g transform="translate({gx},{gy}) scale({sc})">{calendar_page(c,"rally",month=mn,year=YEAR,first_wd=fw,days=dd)}</g>')
    open(os.path.join(OUT,f"{prefix}_spread.svg"),"w").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{FONTS}</style></defs>'+"".join(b)+"</svg>")
    print("built",prefix,W,H)

if __name__=="__main__":
    import ford, acura, lexus, jeep
    build("FORD","United States", ford.CARS_F, "ford", ford.ACCENT)
    build("ACURA","Japan", acura.CARS_A, "acura", acura.ACCENT)
    build("LEXUS","Japan", lexus.CARS_L, "lexus", lexus.ACCENT)
    build("JEEP","United States", jeep.CARS_J, "jeep", jeep.ACCENT)
