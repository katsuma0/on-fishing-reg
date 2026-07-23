# -*- coding: utf-8 -*-
"""Curated calendar-first lookbook: the four styles worth selling + a 2026
spread of the winner. Research-backed picks (2026 neo-print, retro poster,
blueprint B&W, clean line-art)."""
import os
import styles
from styles import calendar_page, STYLES, FONTS, PW, PH
from gen import CARS, esc

OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"out")
CMAP={c["key"]:c for c in CARS}

# 2026 month table: (name, first_weekday Sun=0, days)
MONTHS=[("JANUARY",4,31),("FEBRUARY",0,28),("MARCH",0,31),("APRIL",3,30),
        ("MAY",5,31),("JUNE",1,30),("JULY",3,31),("AUGUST",6,31),
        ("SEPTEMBER",2,30),("OCTOBER",4,31),("NOVEMBER",0,30),("DECEMBER",2,31)]

CURATED=[
 ("rally","corvette","Retro Rally Poster","THE MASS-MARKET BESTSELLER",
  "Warm sunburst, flat shapes, a month you can read across the room. Broadest appeal, photographs beautifully for a listing thumbnail, and instantly ‘vintage’ without being niche."),
 ("halftone","porsche","Halftone Neo-Print","THE 2026 TREND PICK",
  "Visible dots, off-register ink, film grain — the defining graphic trend of 2026. Reads as a real screenprint. Tailor-made for the fashion / Gen-Z ‘modern-vintage’ buyer."),
 ("blueprint","countach","Blueprint (B&W)","THE ENTHUSIAST / GIFT SKU",
  "The collector’s pick and the black-and-white option the market already asks for. Real dimension callouts read as credibility — the calendar a gearhead actually wants on the wall."),
 ("lineart","etype","Clean Line-Art","THE WIDEST-APPEAL / CHEAPEST PRINT",
  "Minimal, tasteful, gender-neutral décor. The easiest to keep perfectly uniform across twelve months and the cheapest to print (one or two colours)."),
]
WINNER="rally"

def svg_tag(inner,cls):
    return f'<svg class="{cls}" viewBox="0 0 {PW} {PH}" xmlns="http://www.w3.org/2000/svg" role="img">{inner}</svg>'

CSS="""
:root{--bg:#211E18;--wall:#2A271F;--card:#141310;--ink:#EDE6D6;--mute:#A79F8C;--line:rgba(237,230,214,.16);--line2:rgba(237,230,214,.08);--spot:#D79A3E}
:root[data-theme="light"]{--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.20);--line2:rgba(35,31,23,.08);--spot:#8A5A28}
@media(prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#E4DAC4;--wall:#DCD2B8;--card:#EFE9DB;--ink:#231F17;--mute:#6C6452;--line:rgba(35,31,23,.20);--line2:rgba(35,31,23,.08);--spot:#8A5A28}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Serif',Georgia,serif;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.grot{font-family:'Grot','Arial Black',sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:0 26px}
header.hero{padding:66px 0 40px;border-bottom:1px solid var(--line)}
.kick{font-family:'Grot';font-weight:700;font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--spot)}
.hero h1{font-family:'Grot';font-weight:900;font-size:clamp(52px,10vw,132px);line-height:.9;margin:12px 0 0;letter-spacing:-.01em}
.hero .lede{max-width:64ch;font-size:17px;font-style:italic;margin:22px 0 0}
.hero ul{max-width:70ch;margin:18px 0 0;padding-left:18px;font-size:14.5px;color:var(--mute)}
.hero ul b{color:var(--ink)}
section{padding:54px 0;border-bottom:1px solid var(--line)}
.shead{margin-bottom:30px}
.shead h2{font-family:'Grot';font-weight:900;font-size:clamp(26px,4.6vw,46px);margin:0}
.shead p{margin:8px 0 0;max-width:60ch;color:var(--mute);font-style:italic}
.four{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
@media(max-width:820px){.four{grid-template-columns:1fr}}
.pick{background:var(--wall);border:1px solid var(--line2);border-radius:6px;overflow:hidden}
.pick .art{display:block;width:100%;height:auto;background:#141310}
.pick .body{padding:20px 22px 24px}
.pick .rank{font-family:'Grot';font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--spot)}
.pick h3{font-family:'Grot';font-weight:900;font-size:24px;margin:6px 0 8px}
.pick p{margin:0;font-size:14.5px;color:var(--mute)}
.spread{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
@media(max-width:820px){.spread{grid-template-columns:repeat(2,1fr)}}
.spread .art{display:block;width:100%;height:auto;border-radius:4px;box-shadow:0 10px 28px rgba(0,0,0,.34)}
.note{font-size:15px;color:var(--mute);max-width:74ch}.note b{color:var(--ink)}.note ul{padding-left:18px}
footer{padding:38px 0 70px;color:var(--mute);font-family:'Grot';font-size:12px;letter-spacing:.14em;text-transform:uppercase}
.toggle{position:fixed;top:16px;right:16px;z-index:9;background:var(--wall);border:1px solid var(--line);color:var(--ink);font-family:'Grot';font-size:11px;letter-spacing:.16em;padding:8px 12px;border-radius:20px;cursor:pointer;text-transform:uppercase}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

def gallery():
    picks=[]
    for i,(sk,ck,name,rank,why) in enumerate(CURATED):
        mn,fw,dd=MONTHS[2]
        page=calendar_page(CMAP[ck], sk, month="MARCH", year="2026", first_wd=fw, days=dd)
        picks.append(f'<figure class="pick">{svg_tag(page,"art")}<div class="body">'
                     f'<div class="rank">Pick {i+1} · {esc(rank)}</div><h3 class="grot">{esc(name)}</h3>'
                     f'<p>{esc(why)}</p></div></figure>')
    four='<div class="four">'+"".join(picks)+'</div>'

    spread=[]
    for i,c in enumerate(CARS):
        mn,fw,dd=MONTHS[i]
        page=calendar_page(c, WINNER, month=mn, year="2026", first_wd=fw, days=dd)
        spread.append(f'<div>{svg_tag(page,"art")}</div>')
    spread_html='<div class="spread">'+"".join(spread)+'</div>'

    note=('<p class="note"><b>On the 2026 calendar.</b> A wall calendar runs twelve months; the collection here is ten '
          'marques, so two more complete the year (easy to add — each new car is one row of data). Every month shares the '
          'same frame, type and grid, so the set reads as one product. Print-ready at A3 / 12&times;12in; the line-art and '
          'blueprint cuts are 1–2 colours (cheapest to print), the rally and halftone cuts are full colour.</p>'
          '<p class="note">Marque &amp; model <b>names are trademarks</b> — a print-on-demand run can drop to ‘safe mode’ '
          '(era + chassis code + origin) and keep the art identical. Copy, silhouettes and colours are original to this project.</p>')

    body=f"""
<button class="toggle grot" onclick="(function(){{var r=document.documentElement;var d=(r.getAttribute('data-theme')||(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'))==='dark';r.setAttribute('data-theme',d?'light':'dark');}})()">Theme</button>
<header class="hero"><div class="wrap">
  <div class="kick">MARQUE Calendar 2026 · Curated for sell-through</div>
  <h1 class="grot">FOUR WAYS<br>TO SELL A YEAR.</h1>
  <p class="lede">I built a spread of calendar styles, then kept the four with the clearest path to sales — read against what the 2026 market is actually buying. Same car collection, same grid; only the art voice changes, so any pick stays a uniform twelve-month set.</p>
  <ul><li><b>Vintage-car & muscle-car calendars</b> are a proven Etsy niche, sold in colour <b>and</b> black-and-white.</li>
  <li><b>Neo-print / halftone</b> — dots, off-register ink, grain — is the defining 2026 graphic trend.</li>
  <li><b>Gen-Z ‘modern-vintage’</b> demand rewards authentic, tactile, screenprint-feeling art.</li></ul>
</div></header>

<section><div class="wrap"><div class="shead"><h2 class="grot">The four picks</h2>
  <p>Ranked by breadth of appeal. Each shown as a live calendar page.</p></div>{four}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">The winner, as a 2026 spread</h2>
  <p>Retro Rally across the collection — one template, the whole year. (Ten of twelve months; two more marques finish it.)</p></div>{spread_html}</div></section>

<section><div class="wrap"><div class="shead"><h2 class="grot">Notes</h2></div>{note}</div></section>
<footer><div class="wrap">MARQUE™ · World Motor Index · Calendar 2026 · curated styles</div></footer>
"""
    return f'<style>{FONTS}{CSS}</style>{body}'

if __name__=="__main__":
    os.makedirs(os.path.join(OUT,"calendar"),exist_ok=True)
    # standalone curated style pages (repo)
    for sk,ck,name,rank,why in CURATED:
        open(os.path.join(OUT,"calendar",f"style_{sk}_{ck}.svg"),"w").write(styles.page_svg(CMAP[ck],sk))
    # winner 2026 spread pages (repo)
    for i,c in enumerate(CARS):
        mn,fw,dd=MONTHS[i]
        open(os.path.join(OUT,"calendar",f"rally_{i+1:02d}_{mn.lower()}_{c['key']}.svg"),"w").write(
            styles.page_svg(c, WINNER, month=mn, year="2026", first_wd=fw, days=dd))
    open(os.path.join(OUT,"calendar_styles.html"),"w").write(gallery())
    print("wrote calendar_styles.html + curated pages + rally spread")
