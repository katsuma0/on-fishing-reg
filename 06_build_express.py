#!/usr/bin/env python3
"""
Build the EXPRESS edition: everything except the map, in one lightweight page
made for phones. Same design system, same data, same features (zone tiles,
seasons and limits with open/closed, waterbody search, species compare,
about/versions dialogs, offline PWA). The waterbody search still reports the
zone: the page quietly fetches the zone boundaries once (no rendering) and
does the point in zone test in the browser.

Output: express/index.html plus manifest/sw/icons, zipped as
ontario-fishing-express.zip for a separate GitHub repo.
"""
import json
import datetime
import os
import shutil
import zipfile

CLEAN = "fishing_zones_clean.json"
OUTDIR = "express"
ZIP = "ontario-fishing-express.zip"

VERSION = "v0.44"
VERSIONS = [
    ("v0.44", "Search rebuilt to the Site Journal spec, pills and inline results"),
    ("v0.43", "Sectioned page, colour tagged search with fish, lake and zone toggle"),
    ("v0.42", "Search towns, cities and parks, bigger zone tiles on phones"),
    ("v0.41", "Search drops down under the bar, full lake pages from Fish ON-Line"),
    ("v0.40", "Search thousands of stocked lakes with stocking history"),
    ("v0.39", "Simpler tab name"),
    ("v0.38", "New title, spec header and sheets, link to the full map"),
    ("v0.37", "First express release, everything but the map"),
]

SERVICE = ("https://ws.lioservices.lrc.gov.on.ca/arcgis2/rest/services/"
           "LIO_OPEN_DATA/LIO_Open07/MapServer/14")
OFFICIAL = "https://www.ontario.ca/document/ontario-fishing-regulations-summary"

data = json.load(open(CLEAN, encoding="utf-8"))
reg_json = json.dumps(data, ensure_ascii=False)
build_date = datetime.date.today().isoformat()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>ON Fishing Reg Express</title>
<meta name="description" content="Ontario's 20 fishing zones with seasons, limits and what is open right now. The quick version, no map."/>
<meta name="theme-color" content="#00753A"/>
<link rel="manifest" href="manifest.json"/>
<link rel="apple-touch-icon" href="icon-192.png"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#F1F6F1; --card:#FFFFFF; --ink:#0F1F17; --forest:#00753A; --forest-2:#18A05A;
    --forest-press:#005C2C; --green-tint:#E7F3EB; --green-tint-2:#D6EBDC; --moss:#40564B;
    --mist:#E4EDE4; --mist-2:#C7D7C9; --line:#D3E0D4; --amber:#EFBF25; --amber-soft:#FBEEDC;
    --danger:#B0574A;
    --r:16px; --r-sm:12px; --r-xs:8px;
    --gap-s:6px; --gap-m:10px; --gap-l:12px;
    --pad-card:14px 16px; --pad-row:12px 14px;
    --shadow-sm:0 1px 2px rgba(15,31,23,.06);
    --shadow:0 2px 12px rgba(15,31,23,.08);
    --shadow-btn:0 3px 10px rgba(0,117,58,.30);
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html,body{margin:0;min-height:100%;background:var(--paper);color:var(--ink);
    font-family:"Hanken Grotesk",system-ui,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.5}
  button,input,select{font-family:inherit}
  .inner{max-width:720px;margin:0 auto;padding:0 18px}

  /* header, per the measured Site Journal spec */
  .appbar{padding:calc(20px + env(safe-area-inset-top)) 0 14px}
  .eyebrow{font-size:11.5px;font-weight:800;letter-spacing:.15em;text-transform:uppercase;color:var(--forest)}
  .titlebar{display:flex;align-items:baseline;justify-content:space-between;gap:9px}
  h1{font-weight:800;font-size:30px;letter-spacing:-.02em;margin:5px 0 0;cursor:pointer}
  .ver{appearance:none;border:none;background:none;cursor:pointer;font-family:inherit;
    font-weight:800;font-size:15px;letter-spacing:-.02em;color:var(--ink);white-space:nowrap;
    padding:0;margin:5px 0 0}
  .sub{color:var(--moss);font-size:13.5px;margin-top:5px}
  .sub a{color:var(--forest);text-underline-offset:2px}
  .seclabel{font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;
    color:var(--forest);margin:22px 2px 12px;display:flex;align-items:center;gap:var(--gap-m)}
  .seclabel::after{content:"";flex:1;height:1px;background:var(--line)}
  .zhead{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:18px 0 2px}
  .zhead h2{font-size:20px;font-weight:800;letter-spacing:-.01em;color:var(--forest);margin:0}
  .meta{font-size:13px;color:var(--moss);margin:4px 0 0;font-variant-numeric:tabular-nums}
  .empty{font-size:13.5px;color:var(--moss);text-align:center;padding:34px 10px}

  .gsearch{display:flex;align-items:center;gap:10px;background:var(--card);border:1px solid var(--line);
    border-radius:12px;padding:12px 14px;margin:2px 0 12px}
  .gsearch svg{flex:none;color:var(--moss)}
  .gsearch input{border:none;background:none;outline:none;font-family:inherit;font-size:16px;width:100%;color:var(--ink)}
  .gclear{appearance:none;border:none;background:none;color:var(--moss);cursor:pointer;font-size:16px;
    line-height:1;padding:2px 4px;display:none}
  .gsearch.has .gclear{display:block}
  .gresults{margin:0 0 14px}
  .gresult{width:100%;text-align:left;appearance:none;background:var(--card);border:1px solid var(--line);
    border-radius:12px;padding:12px 14px;margin-bottom:10px;cursor:pointer;display:flex;align-items:center;gap:10px}
  .tag{flex:0 0 46px;width:46px;height:22px;display:flex;align-items:center;justify-content:center;align-self:center;
    font-size:9.5px;font-weight:800;letter-spacing:.03em;text-transform:uppercase;line-height:1;padding:0;
    color:var(--paper);background:var(--forest);border-radius:99px}
  .tag.fish{background:var(--forest-2)}
  .tag.water{background:#3E7CA6}
  .tag.town{background:var(--amber)}
  .tag.park{background:var(--amber)}
  .tag.area{background:var(--amber)}
  .grow{flex:1;min-width:0}
  .gt{display:block;font-weight:700;font-size:15px}
  .gs{display:block;font-size:12.5px;color:var(--moss);margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .gnone{color:var(--moss);font-size:14px;padding:18px 6px;text-align:center;border:1px solid var(--line);border-radius:12px;background:var(--card)}
  .seclabel.grey{color:var(--moss)}
  .filters{display:flex;flex-wrap:wrap;gap:8px;margin:var(--gap-l) 0}
  .fchip{display:inline-flex;align-items:center;justify-content:center;gap:var(--gap-s);
    border:1px solid var(--line);background:var(--card);color:var(--moss);font-weight:700;
    font-size:12.5px;border-radius:99px;padding:10px 14px;min-width:44px;cursor:pointer;
    transition:background .12s,transform .14s}
  .fchip.on{background:var(--forest);border-color:var(--forest);color:var(--paper)}
  .fchip:active{transform:scale(.97)}
  .zonegrid{display:grid;grid-template-columns:repeat(10,1fr);gap:6px;margin:var(--gap-l) 0}
  .ztile{position:relative;aspect-ratio:1/1;display:flex;align-items:center;justify-content:center;
    border:1px solid var(--line);background:var(--card);color:var(--ink);font-weight:800;font-size:14px;
    border-radius:var(--r-xs);cursor:pointer;font-variant-numeric:tabular-nums;
    transition:transform .14s,background .12s}
  .ztile::after{content:"";position:absolute;inset:-7px}
  .ztile.on{background:var(--forest);border-color:var(--forest);color:var(--paper)}
  .ztile:active{transform:scale(.97)}
  .ztile[disabled]{opacity:.35;cursor:default}
  @media (max-width:520px){ .zonegrid{grid-template-columns:repeat(5,1fr);gap:6px} .ztile{font-size:15px} }

  .srow{display:flex;align-items:flex-start;gap:var(--gap-m);width:100%;text-align:left;
    border:1px solid var(--line);background:var(--card);border-radius:var(--r-sm);
    padding:var(--pad-card);margin-bottom:var(--gap-m);color:var(--ink);
    transition:border-color .15s,transform .14s}
  button.srow{cursor:pointer}
  button.srow:active{transform:scale(.985)}
  .srow .col{flex:1;min-width:0}
  .srow .nm{font-size:16px;font-weight:700;letter-spacing:-.01em;color:var(--forest)}
  .srow[data-st="closed"] .nm{color:var(--danger)}
  .srow .mt{font-size:13px;color:var(--moss);margin-top:3px;line-height:1.45}
  .pill{flex:none;font-weight:800;font-size:12.5px;border:1px solid var(--line);border-radius:99px;
    padding:8px 13px;color:var(--forest);min-width:62px;text-align:center}
  .pill.open{background:var(--green-tint);border-color:transparent;color:var(--forest)}
  .pill.closed{background:#F6E8E5;border-color:transparent;color:var(--danger)}
  .pill.unknown{background:var(--mist);border-color:transparent;color:var(--moss)}

  details.blk{border:1px solid var(--line);background:var(--card);border-radius:var(--r-sm);
    margin-bottom:var(--gap-m);overflow:hidden}
  details.blk>summary{list-style:none;cursor:pointer;padding:var(--pad-card);font-weight:700;
    font-size:14.5px;color:var(--ink);display:flex;justify-content:space-between;align-items:center;gap:8px}
  details.blk>summary::-webkit-details-marker{display:none}
  details.blk .body{padding:0 16px 14px}
  .rcount{color:var(--moss);font-weight:600;font-size:12.5px}
  .body ul{margin:0;padding-left:18px}
  .body li{font-size:13px;color:var(--moss);line-height:1.5;margin-bottom:6px}
  .wb{padding:8px 0;border-bottom:1px solid var(--line)}
  .wb:last-child{border-bottom:none}
  .wb b{display:block;font-size:14px;color:var(--ink);margin-bottom:4px}

  .backdrop{position:fixed;inset:0;background:rgba(15,31,23,.35);opacity:0;pointer-events:none;
    transition:opacity .25s;z-index:40}
  .backdrop.on{opacity:1;pointer-events:auto}
  .sheet{position:fixed;left:0;right:0;bottom:0;margin:0 auto;transform:translateY(102%);
    width:min(540px,100%);background:var(--paper);z-index:50;
    border-radius:16px 16px 0 0;
    padding:8px 22px calc(26px + env(safe-area-inset-bottom));
    box-shadow:0 -8px 40px rgba(19,32,25,.22);
    transition:transform .34s cubic-bezier(.32,1.22,.38,1);
    max-height:92vh;overflow:auto}
  .sheet.on{transform:translateY(0)}
  .grabber{width:40px;height:4px;border-radius:99px;background:var(--mist-2);margin:7px auto 16px}
  .kind{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--forest)}
  .sheet a{color:var(--forest);text-underline-offset:2px}
  .aboutbody p{margin:1em 0}
  .closing{font-size:12px;font-weight:600;color:var(--moss);text-align:center;margin-top:12px}
  .vrow{display:flex;gap:12px;align-items:baseline;padding:9px 0;
    border-bottom:1px dashed var(--line);font-size:13.5px;color:var(--ink);line-height:1.45}
  .vrow:last-child{border-bottom:none}
  .vv{flex:none;font-weight:800;font-size:12.5px;color:var(--forest);
    font-variant-numeric:tabular-nums;min-width:46px}

  footer{max-width:720px;margin:0 auto;padding:20px 18px 40px;color:var(--moss);
    font-size:11.5px;line-height:1.55}
  footer a{color:inherit;text-decoration:underline;text-underline-offset:2px}
  @media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="backdrop" id="backdrop"></div>
<div class="sheet" id="versions" role="dialog" aria-modal="true" aria-label="Versions">
  <div class="grabber"></div>
  <div class="kind" style="margin-bottom:12px">Versions</div>
  <div class="vlist">__VERSION_ROWS__</div>
</div>
<div class="sheet" id="about" role="dialog" aria-modal="true" aria-label="About">
  <div class="grabber"></div>
  <div class="kind" style="margin-bottom:12px">About</div>
  <div class="aboutbody">
    <p>Every year Ontario puts out the new fishing regulations as a 148 page PDF. Every season, every
      limit, every lake with its own special rules is buried somewhere in there, and to be frank,
      reading it on your phone at the boat launch is not it.</p>
    <p>This is the mapless version of <a href="/on-fishing-reg/">ON Fishing Regulation</a>, easier to
      check on your phone for when you are out. Tap your zone and the seasons and limits are right
      there, with what is open today and what is closed.</p>
    <p>It makes the check quick, a glance before you head out instead of twenty minutes of scrolling,
      and you can cast knowing you looked it up.</p>
  </div>
  <div class="closing">Regulations from the 2026 summary · Zone boundaries from the Government of
    Ontario · Data prepared __BUILD_DATE__</div>
</div>

<main class="inner">
  <header class="appbar">
    <div class="eyebrow">Ministry of Natural Resources</div>
    <div class="titlebar">
      <h1 id="logobtn" tabindex="0" role="button">ON Fishing Regulation Express</h1>
      <button class="ver" id="verbtn">__VERSION__</button>
    </div>
    <p class="sub">Express, no map. Not an official source. The data is pulled automatically from the
      148 page guide, so check the <a href="__OFFICIAL__" target="_blank" rel="noopener">official
      summary</a> before you fish, especially the waterbody exceptions.</p>
  </header>
  <div class="seclabel" style="margin-top:10px">Zones</div>
  <div class="zonegrid" id="zones"></div>
  <div class="seclabel">Search</div>
  <div class="gsearch" id="gsearch">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input id="search" inputmode="search" autocomplete="off" placeholder="Search zones, species, or lakes">
        <button class="gclear" id="gclear" aria-label="Clear search">✕</button>
      </div>
      <div id="gresults" class="gresults" hidden></div>
  <div id="detail"></div>
</main>
<footer>
  Not an official source. Always check the official summary before you fish.<br>
  Created by <a href="https://katsuma0.github.io" target="_blank" rel="noopener">Katsuma Onishi</a>
</footer>

<script>
const REG = __REG_JSON__;
const BOUNDS_URL="__SERVICE__/query?where=1%3D1&outFields=FISHERIES_MANAGEMENT_ZONE_ID"
  +"&returnGeometry=true&maxAllowableOffset=0.01&geometryPrecision=4&outSR=4326&f=geojson";

function esc(s){ return (s||"").replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
function label(st){ return st==='open'?'Open':st==='closed'?'Closed':'Check'; }

let selectedZone=null;
let exploreSpecies=null;
let speciesMap={};
const zoneFeatures=[];

/* boundaries: fetched once, only to answer "which zone is this lake in" */
fetch(BOUNDS_URL).then(r=>r.json()).then(gj=>{
  gj.features.forEach(f=>{
    if(f.geometry) zoneFeatures.push({z:f.properties.FISHERIES_MANAGEMENT_ZONE_ID, geometry:f.geometry});
  });
}).catch(()=>{});
function pointInRing(pt, ring){
  let inside=false, x=pt[0], y=pt[1];
  for(let i=0,j=ring.length-1;i<ring.length;j=i++){
    const xi=ring[i][0],yi=ring[i][1],xj=ring[j][0],yj=ring[j][1];
    if(((yi>y)!==(yj>y)) && (x < (xj-xi)*(y-yi)/(yj-yi)+xi)) inside=!inside;
  }
  return inside;
}
function pointInPolygon(pt, poly){
  if(!pointInRing(pt, poly[0])) return false;
  for(let k=1;k<poly.length;k++) if(pointInRing(pt, poly[k])) return false;
  return true;
}
function zoneAt(lng,lat){
  const pt=[lng,lat];
  for(const f of zoneFeatures){
    const g=f.geometry;
    if(g.type==='Polygon'){ if(pointInPolygon(pt,g.coordinates)) return f.z; }
    else if(g.type==='MultiPolygon'){ for(const p of g.coordinates) if(pointInPolygon(pt,p)) return f.z; }
  }
  return null;
}

const WATER=[
 ["Lake Superior",48.60,-87.30],["Lake Huron",44.80,-82.20],["Georgian Bay",45.30,-80.90],
 ["North Channel",46.05,-82.60],["Lake Erie",42.25,-81.00],["Lake Ontario",43.70,-78.10],
 ["Lake St. Clair",42.40,-82.70],["St. Lawrence River",44.55,-75.75],["Bay of Quinte",44.15,-77.25],
 ["Niagara River",43.10,-79.05],["Detroit River",42.15,-83.10],["Long Point Bay",42.60,-80.30],
 ["Lake of the Woods",49.30,-94.60],["Rainy Lake",48.65,-93.20],["Lac Seul",50.35,-92.30],
 ["Eagle Lake (Dryden)",49.75,-93.20],["Wabigoon Lake",49.60,-92.70],["Red Lake",51.05,-93.80],
 ["Lake St. Joseph",51.05,-90.80],["Big Vermilion Lake",50.03,-92.22],["Dinorwic Lake",49.63,-92.55],
 ["Minnitaki Lake",49.97,-91.95],["Winnipeg River",49.90,-94.80],
 ["Lake Nipigon",49.83,-88.50],["Nipigon River",49.00,-88.25],["Thunder Bay",48.40,-89.15],
 ["Black Bay",48.65,-88.45],["Shebandowan Lake",48.62,-90.15],["Dog Lake (Thunder Bay)",48.72,-89.55],
 ["Lake Abitibi",48.70,-79.90],["Lake Temiskaming",47.30,-79.50],
 ["Kabinakagami Lake",48.85,-84.35],["Nagagami Lake",49.45,-84.60],["Missinaibi Lake",48.30,-83.65],
 ["Michipicoten River",47.95,-84.90],["Groundhog River",49.20,-82.10],["Moose River",51.20,-80.60],
 ["Albany River",51.35,-85.00],["Attawapiskat River",52.60,-86.00],["Winisk River",54.50,-86.50],
 ["Severn River (north)",55.20,-88.30],
 ["Lake Nipissing",46.28,-79.80],["Lake Temagami",47.00,-80.07],["French River",46.00,-80.55],
 ["Lake Wanapitei",46.75,-80.75],["Ramsey Lake",46.47,-80.96],["Lake Panache",46.25,-81.35],
 ["Lake Nosbonsing",46.28,-79.10],["Trout Lake (North Bay)",46.32,-79.36],["Lake Talon",46.31,-79.09],
 ["Restoule Lake",46.06,-79.78],["Onaping Lake",46.87,-81.44],
 ["Lake Muskoka",45.00,-79.42],["Lake Rosseau",45.18,-79.60],["Lake Joseph",45.15,-79.73],
 ["Lake of Bays",45.28,-79.05],["Mary Lake",45.24,-79.28],["Fairy Lake",45.33,-79.19],
 ["Peninsula Lake",45.34,-79.14],["Vernon Lake",45.33,-79.26],["Skeleton Lake",45.24,-79.44],
 ["Three Mile Lake",45.17,-79.45],
 ["Lake Opeongo",45.70,-78.37],["Algonquin Park",45.60,-78.40],
 ["Kennisis Lake",45.22,-78.65],["Haliburton Lake",45.15,-78.50],["Lake Kashagawigamog",45.00,-78.55],
 ["Twelve Mile Lake",45.12,-78.68],["Boshkung Lake",45.06,-78.73],["Eagle Lake (Haliburton)",45.13,-78.52],
 ["Lake Simcoe",44.42,-79.35],["Lake Couchiching",44.65,-79.35],["Severn River",44.80,-79.60],
 ["Rice Lake",44.17,-78.20],["Lake Scugog",44.20,-78.85],["Balsam Lake",44.60,-78.85],
 ["Sturgeon Lake",44.47,-78.70],["Pigeon Lake",44.45,-78.50],["Stoney Lake",44.55,-78.15],
 ["Buckhorn Lake",44.48,-78.39],["Lower Buckhorn Lake",44.55,-78.49],["Lovesick Lake",44.55,-78.45],
 ["Chemong Lake",44.43,-78.38],["Katchewanooka Lake",44.41,-78.27],["Clear Lake (Kawarthas)",44.52,-78.24],
 ["Cameron Lake",44.55,-78.76],["Canal Lake",44.57,-79.02],["Mitchell Lake",44.57,-78.93],
 ["Dalrymple Lake",44.66,-79.10],["Trent River",44.30,-77.80],["Kawartha Lakes",44.45,-78.55],
 ["Ottawa River",45.55,-76.40],["Big Rideau Lake",44.72,-76.25],["Rideau River",45.10,-75.70],
 ["Charleston Lake",44.50,-76.05],["Bobs Lake",44.70,-76.60],["Madawaska River",45.50,-77.30],
 ["Loughborough Lake",44.38,-76.42],["Sydenham Lake",44.41,-76.58],["Devil Lake",44.58,-76.48],
 ["Newboro Lake",44.65,-76.32],["Upper Rideau Lake",44.68,-76.33],["Mississippi Lake",45.02,-76.20],
 ["White Lake (Lanark)",45.30,-76.52],["Calabogie Lake",45.29,-76.75],
 ["Grand River",43.30,-80.30],["Saugeen River",44.30,-81.20],["Nottawasaga River",44.40,-79.90],
 ["Maitland River",43.75,-81.60],["Thames River",42.90,-81.50],["Fanshawe Lake",43.03,-81.18],
 ["Belwood Lake",43.79,-80.33],["Conestogo Lake",43.68,-80.71],["Guelph Lake",43.60,-80.27],
 ["Island Lake (Orangeville)",43.93,-80.07],["Pittock Reservoir",43.14,-80.77]
];

const STOCK_URL='https://services1.arcgis.com/TJH5KDher0W13Kgo/arcgis/rest/services/'
  +'FishStockingDataForRecreationalPurposes/FeatureServer/0/query';
const ARA_URL='https://ws.lioservices.lrc.gov.on.ca/arcgis2/rest/services/'
  +'LIO_OPEN_DATA/LIO_Open07/MapServer/2/query';
async function searchStocked(q){
  const like="'%"+q.replace(/'/g,"''").toUpperCase()+"%'";
  const p=new URLSearchParams({
    where:"UPPER(Official_Waterbody_Name) LIKE "+like+" OR UPPER(Unoffcial_Waterbody_Name) LIKE "+like,
    outFields:'Official_Waterbody_Name,Unoffcial_Waterbody_Name,Species,Stocking_Year,Latitude,Longitude,Geographic_Township,MNRF_District',
    returnGeometry:'false', resultRecordCount:'400', f:'json'});
  const j=await (await fetch(STOCK_URL+'?'+p)).json();
  const g={};
  (j.features||[]).forEach(f=>{
    const a=f.attributes||{};
    let n=a.Official_Waterbody_Name||a.Unoffcial_Waterbody_Name;
    if(!n) return;
    n=n.replace(/\s*\(Unofficial Name\)/i,'');
    const key=n.toLowerCase()+'|'+(a.Latitude!=null?a.Latitude.toFixed(1):'')+','+(a.Longitude!=null?a.Longitude.toFixed(1):'');
    const e=g[key]||(g[key]={n:n,lat:a.Latitude,lng:a.Longitude,sp:{},town:a.Geographic_Township,dist:a.MNRF_District});
    if(!e.town&&a.Geographic_Township) e.town=a.Geographic_Township;
    if(a.Species) e.sp[a.Species]=Math.max(e.sp[a.Species]||0,a.Stocking_Year||0);
  });
  return Object.values(g);
}
// Fish ON-Line waterbody index (every lake it knows, stocked or not).
async function araSearch(q){
  const like="'%"+q.replace(/'/g,"''").toUpperCase()+"%'";
  const p=new URLSearchParams({
    where:"UPPER(OFFICIAL_WATERBODY_NAME) LIKE "+like+" OR UPPER(CORPORATE_WATERBODY_NAME) LIKE "+like,
    outFields:'OFFICIAL_WATERBODY_NAME,CORPORATE_WATERBODY_NAME,FISHERIES_MANAGEMENT_ZONE_ID,'
      +'WATERBODY_TYPE,FISH_SPECIES_SUMMARY,SURFACE_AREA,MAXIMUM_DEPTH,MEAN_DEPTH,WATERBODY_LID',
    returnGeometry:'false', resultRecordCount:'150', f:'json'});
  const j=await (await fetch(ARA_URL+'?'+p)).json();
  const g={};
  (j.features||[]).forEach(f=>{
    const a=f.attributes||{};
    const n=a.OFFICIAL_WATERBODY_NAME||a.CORPORATE_WATERBODY_NAME;
    if(!n) return;
    const key=(a.WATERBODY_LID||n.toLowerCase()+'|'+(a.FISHERIES_MANAGEMENT_ZONE_ID||''));
    const e=g[key]||(g[key]={n:n,z:a.FISHERIES_MANAGEMENT_ZONE_ID,lid:a.WATERBODY_LID,
      type:a.WATERBODY_TYPE,area:null,maxd:null,meand:null,spset:new Set()});
    if(a.SURFACE_AREA!=null) e.area=Math.max(e.area||0,a.SURFACE_AREA);
    if(a.MAXIMUM_DEPTH!=null) e.maxd=Math.max(e.maxd||0,a.MAXIMUM_DEPTH);
    if(a.MEAN_DEPTH!=null) e.meand=Math.max(e.meand||0,a.MEAN_DEPTH);
    (a.FISH_SPECIES_SUMMARY||'').split(',').forEach(s=>{ s=s.trim(); if(s) e.spset.add(s); });
  });
  return Object.values(g).map(e=>({n:e.n,z:e.z,lid:e.lid,type:e.type,area:e.area,
    maxd:e.maxd,meand:e.meand,species:[...e.spset]}));
}
async function araCentre(lid){
  const p=new URLSearchParams({where:"WATERBODY_LID='"+lid.replace(/'/g,"''")+"'",
    outFields:'WATERBODY_LID',returnGeometry:'true',maxAllowableOffset:'0.05',
    outSR:'4326',resultRecordCount:'1',f:'json'});
  const j=await (await fetch(ARA_URL+'?'+p)).json();
  const f=(j.features||[])[0];
  if(!f||!f.geometry||!f.geometry.rings||!f.geometry.rings[0]) return null;
  const ring=f.geometry.rings[0];
  let x=0,y=0; ring.forEach(pt=>{x+=pt[0];y+=pt[1];});
  return {lng:x/ring.length, lat:y/ring.length};
}
// Sport fish first when listing what swims in a lake.
const SPORT=['Walleye','Sauger','Largemouth Bass','Smallmouth Bass','Northern Pike','Muskellunge',
 'Yellow Perch','Black Crappie','Crappie','Lake Trout','Brook Trout','Rainbow Trout','Brown Trout',
 'Splake','Lake Whitefish','Channel Catfish','Atlantic Salmon','Chinook Salmon','Coho Salmon',
 'Pumpkinseed','Bluegill','Rock Bass','Lake Sturgeon','Lake Herring (Cisco)','Cisco'];
function sortSpecies(list){
  const ix=n=>{const i=SPORT.indexOf(n); return i<0?100:i;};
  return [...list].sort((a,b)=>ix(a)-ix(b)||a.localeCompare(b));
}
// Towns, cities, parks: federal geographic names service, Ontario only.
const PLACE_TYPES={CITY:'City',TOWN:'Town',VILG:'Village',HAM:'Hamlet',UNP:'Community',
 MUN1:'Municipality',MUN2:'Municipality',MUN:'Municipality',PARK:'Park',ISL:'Island',
 GEOG:'Area',PROV:'Provincial park'};
async function placeSearch(q){
  const p=new URLSearchParams({q:q, province:'35', num:'20'});
  const j=await (await fetch('https://geogratis.gc.ca/services/geoname/en/geonames.json?'+p)).json();
  const places=[], waters=[];
  const WATERC=['LAKE','RIV','BAY','CHAN','FALL','FALLS','RAPS','CRK','STM'];
  (j.items||[]).forEach(it=>{
    if(it.latitude==null) return;
    const code=(it.concise||{}).code||'';
    if(PLACE_TYPES[code]) places.push({n:it.name, lat:it.latitude, lng:it.longitude, place:true,
      ptype:PLACE_TYPES[code], loc:it.location||''});
    else if(WATERC.includes(code)) waters.push({nl:(it.name||'').toLowerCase(), loc:it.location||'',
      z:zoneAt(it.longitude,it.latitude)});
  });
  return {places, waters};
}


const ORDER=["Largemouth and Smallmouth Bass combined","Largemouth Bass","Smallmouth Bass",
 "Walleye and Sauger combined","Northern Pike","Yellow Perch","Sunfish","Crappie","Muskellunge",
 "Lake Trout","Lake Trout and Splake","Brook Trout","Rainbow Trout","Brown Trout and Rainbow Trout",
 "Brown Trout","Splake","Lake Whitefish","Channel Catfish","Atlantic Salmon","Pacific Salmon",
 "Lake Herring (Cisco)","Lake Sturgeon","Aggregate Limits for Trout and Salmon"];
const ORDER_IX={}; ORDER.forEach((n,i)=>{ ORDER_IX[n]=i; });
function rankName(a,b){
  const ia=ORDER_IX[a]!=null?ORDER_IX[a]:900, ib=ORDER_IX[b]!=null?ORDER_IX[b]:900;
  return ia-ib || a.localeCompare(b);
}
function bySpecies(a,b){
  const ca=seasonStatus(a.season).status==='closed'?0:1;
  const cb=seasonStatus(b.season).status==='closed'?0:1;
  return ca-cb || rankName(a.species,b.species);
}

/* season status */
const MONTHS={january:0,february:1,march:2,april:3,may:4,june:5,july:6,august:7,september:8,october:9,november:10,december:11};
const WD={sunday:0,monday:1,tuesday:2,wednesday:3,thursday:4,friday:5,saturday:6};
const ORD={first:1,'1st':1,second:2,'2nd':2,third:3,'3rd':3,fourth:4,'4th':4,fifth:5,'5th':5};
function nthWeekday(year,monthIdx,wd,n){
  const d=new Date(year,monthIdx,1); let count=0;
  while(d.getMonth()===monthIdx){ if(d.getDay()===wd){ count++; if(count===n) return new Date(d); } d.setDate(d.getDate()+1); }
  return null;
}
function parseToken(tok,year){
  tok=tok.trim().toLowerCase();
  if(/before|after/.test(tok)) return null;
  if(/labour day/.test(tok)) return nthWeekday(year,8,1,1);
  let m=tok.match(/^(first|second|third|fourth|fifth|1st|2nd|3rd|4th|5th)\s+(sunday|monday|tuesday|wednesday|thursday|friday|saturday)\s+in\s+([a-z]+)/);
  if(m && ORD[m[1]]!=null && WD[m[2]]!=null && MONTHS[m[3]]!=null) return nthWeekday(year,MONTHS[m[3]],WD[m[2]],ORD[m[1]]);
  m=tok.match(/^([a-z]+)\s+(\d{1,2})/);
  if(m && MONTHS[m[1]]!=null) return new Date(year,MONTHS[m[1]],parseInt(m[2],10));
  return null;
}
function rangesOf(season,year){
  const s=season.toLowerCase();
  if(/open all year/.test(s)) return {allyear:'open'};
  if(/closed all year/.test(s)) return {allyear:'closed'};
  const ranges=[]; let unknown=false;
  for(const part of season.split(/\s+and\s+/i)){
    const i=part.toLowerCase().indexOf(' to ');
    if(i<0){ unknown=true; continue; }
    const a=parseToken(part.slice(0,i),year), b=parseToken(part.slice(i+4),year);
    if(!a||!b){ unknown=true; continue; }
    ranges.push([new Date(a.getFullYear(),a.getMonth(),a.getDate()),
                 new Date(b.getFullYear(),b.getMonth(),b.getDate(),23,59,59)]);
  }
  return {ranges,unknown};
}
function seasonStatus(season){
  if(!season) return {status:'unknown'};
  const now=new Date(), year=now.getFullYear(), r=rangesOf(season,year);
  if(r.allyear) return {status:r.allyear};
  let open=false, activeEnd=null, nextStart=null;
  for(const [a,b] of r.ranges){
    if(now>=a && now<=b){ open=true; if(!activeEnd||b<activeEnd) activeEnd=b; }
    if(a>now && (!nextStart||a<nextStart)) nextStart=a;
  }
  const DAY=86400000;
  if(open){ const days=activeEnd?Math.ceil((activeEnd-now)/DAY):null;
    return {status:'open', soon:(days!=null&&days<=14)?{type:'closing',days}:null}; }
  if(r.ranges.length){ const days=nextStart?Math.ceil((nextStart-now)/DAY):null;
    return {status:'closed', soon:(days!=null&&days<=14)?{type:'opening',days}:null}; }
  return {status:'unknown'};
}
function openStatus(season){ return seasonStatus(season).status; }

/* zone tiles */
const zonesEl=document.getElementById('zones');
for(let z=1;z<=20;z++){
  const c=document.createElement('button');
  c.className='ztile'; c.textContent=z; c.dataset.zone=z;
  if(!REG[z]) c.disabled=true;
  c.onclick=()=>selectZone(z);
  zonesEl.appendChild(c);
}
const detailEl=document.getElementById('detail');
const searchEl=document.getElementById('search');
function showEmpty(){ detailEl.innerHTML='<p class="empty">Pick a zone to see its rules.</p>'; }
showEmpty();

function paintTiles(){
  document.querySelectorAll('.ztile[data-zone]').forEach(c=>
    c.classList.toggle('on',Number(c.dataset.zone)===selectedZone));
}
function clearZone(){
  selectedZone=null; lastWater=null; paintTiles();
  history.replaceState(null,'',location.pathname+location.search);
  showEmpty();
}
function selectZone(z, fromWater){
  z=Number(z);
  if(!fromWater) lastWater=null;
  if(z===selectedZone){ clearZone(); return; }
  selectedZone=z; searchEl.value='';
  paintTiles(); renderPanel(z);
  if(('#zone='+z)!==location.hash) history.replaceState(null,'','#zone='+z);
  window.scrollTo({top:0});
}

function speciesRow(r, st, ss){
  const soon = ss && ss.soon ? `<div class="mt">${ss.soon.type==='closing'?'Closes':'Opens'} in ${ss.soon.days} days</div>` : '';
  return `<div class="srow" data-st="${st}"><div class="col">
      <div class="nm">${esc(r.species)}</div>
      <div class="mt">${esc(r.season)}</div>
      <div class="mt">${esc(r.limits)}</div>${soon}
    </div><span class="pill ${st}">${label(st)}</span></div>`;
}

function renderPanel(z){
  if(typeof showDetail==='function') showDetail();
  const d=REG[z];
  if(!d){ detailEl.innerHTML=`<p class="empty">No data for zone ${z}.</p>`; return; }
  const info=(d.general_info||[]).filter(Boolean);
  const sp=[...(d.species_regulations||[])].sort(bySpecies);
  const wb=d.waterbody_exceptions||[];

  let html='';
  const chips=[];
  if(exploreSpecies) chips.push(`<button class="fchip" id="backexp">Back to ${esc(exploreSpecies)}</button>`);
  if(lastWater) chips.push(`<button class="fchip" id="backwater">Back to ${esc(lastWater.n)}</button>`);
  if(chips.length) html+=`<div class="filters">${chips.join('')}</div>`;
  html+=`<div class="seclabel">Zone ${z}</div>
    <div id="splist">${sp.map(r=>{const ss=seasonStatus(r.season); return speciesRow(r, ss.status, ss);}).join('')}</div>`;
  if(wb.length){
    html+=`<details class="blk"><summary>Waterbody exceptions <span class="rcount">${wb.length}</span></summary>
      <div class="body">${wb.map(w=>`<div class="wb"><b>${esc(w.waterbody)}</b>${
        w.rules&&w.rules.length?`<ul>${w.rules.map(r=>`<li>${esc(r)}</li>`).join('')}</ul>`:''
      }</div>`).join('')}</div></details>`;
  }
  if(info.length){
    html+=`<details class="blk"><summary>General information <span class="rcount">${info.length}</span></summary>
      <div class="body"><ul>${info.map(i=>`<li>${esc(i)}</li>`).join('')}</ul></div></details>`;
  }
  detailEl.innerHTML=html;
  const be=document.getElementById('backexp');
  if(be) be.onclick=()=>renderExplore(exploreSpecies);
  const bw=document.getElementById('backwater');
  if(bw) bw.onclick=()=>renderWater(lastWater);
}

/* waterbody search */
const IS_MAP = (typeof goToWater==='function');
const gsearch=document.getElementById('gsearch');
const gclear=document.getElementById('gclear');
const rbox=document.getElementById('gresults');
let searchSeq=0;
let lastWater=null;
function showDetail(){ rbox.hidden=true; detailEl.hidden=false; }
function showResults(){ rbox.hidden=false; detailEl.hidden=true; }
function restoreList(){ rbox.hidden=true; rbox.innerHTML=''; detailEl.hidden=false;
  if(selectedZone) renderPanel(selectedZone); else showEmpty(); }

// Word based matching; filler words are ignored so "zone 15 walleye" works.
const FILLERS=['zone','lake','the'];
function qTokens(q){ return q.toLowerCase().split(/\s+/).filter(t=>t&&!FILLERS.includes(t)); }
function matchName(name,tokens){ const n=name.toLowerCase(); return tokens.length&&tokens.every(t=>n.includes(t)); }
function catOf(r){
  if(r.kind==='zone') return 'zone';
  if(r.fish) return 'fish';
  if(r.place){ const t=(r.ptype||'').toLowerCase();
    if(t.includes('park')) return 'park';
    if(t==='island'||t==='area') return 'area';
    return 'town'; }
  return 'water';
}
const CAT_RANK={zone:0,fish:1,water:2,park:3,town:3,area:3};
function pill(r){
  const c=catOf(r);
  if(c==='zone') return ['Zone','zone'];
  if(c==='fish') return ['Fish','fish'];
  if(c==='park') return ['Park','park'];
  if(c==='area') return ['Area','area'];
  if(c==='town') return [(r.ptype||'').toLowerCase()==='city'?'City':'Town','town'];
  const ty=((r.type||'')+' '+r.n).toLowerCase();
  if(ty.includes('river')||ty.includes('stream')||ty.includes('creek')) return ['River','water'];
  return ['Lake','water'];
}
function score(r,q){
  const n=r.n.toLowerCase(), ql=q.trim().toLowerCase();
  if(n===ql) return 12;
  if(n.startsWith(ql)) return 6;
  return 0;
}
function finalize(list,q){
  const seen=new Set(); const out=[];
  list.forEach(r=>{ const k=catOf(r)+'|'+r.n.toLowerCase();
    if(seen.has(k)) return; seen.add(k); out.push(r); });
  out.sort((a,b)=>(CAT_RANK[catOf(a)]??9)-(CAT_RANK[catOf(b)]??9) || score(b,q)-score(a,q));
  return out.slice(0,15);
}
function buildLocal(q){
  const tokens=qTokens(q); const out=[];
  tokens.forEach(t=>{ const num=parseInt(t,10);
    if(String(num)===t && num>=1 && num<=20 && REG[num])
      out.push({kind:'zone', n:'Zone '+num, z:num,
        sub:(REG[num].species_regulations||[]).length+' species · Seasons and limits'}); });
  Object.keys(speciesMap).filter(n=>matchName(n,tokens)).sort(rankName).slice(0,6)
    .forEach(n=>out.push({fish:true, n:n, sub:'In '+Object.keys(speciesMap[n]).length+' zones'}));
  WATER.forEach(w=>{ if(matchName(w[0],tokens)){ const z=zoneAt(w[2],w[1]);
    out.push({n:w[0], lat:w[1], lng:w[2], z:z, curated:true, sub:z?('Zone '+z):'Ontario'}); }});
  return out;
}
function renderResults(list){
  if(!list.length){ rbox.innerHTML='<div class="gnone">No matches. Try a zone, a species, or a lake.</div>'; return; }
  rbox.innerHTML=list.map((r,i)=>{ const p=pill(r);
    return `<button class="gresult" data-i="${i}"><span class="tag ${p[1]}">${p[0]}</span>`
      +`<span class="grow"><span class="gt">${esc(r.n)}</span><span class="gs">${esc(r.sub||'')}</span></span></button>`;
  }).join('');
  rbox.querySelectorAll('.gresult').forEach(el=>el.onclick=()=>gotoResult(list[Number(el.dataset.i)]));
}
function gotoResult(r){
  searchEl.value=r.n; gsearch.classList.add('has');
  if(r.kind==='zone'){ showDetail(); if(selectedZone===r.z) renderPanel(r.z); else selectZone(r.z); return; }
  if(r.fish){ openFish(r.n); return; }
  openWater(r);
}
function onSearch(){
  const q=searchEl.value;
  gsearch.classList.toggle('has', !!q.trim());
  const seq=++searchSeq;
  if(!q.trim()){ restoreList(); return; }
  showResults();
  renderResults(finalize(buildLocal(q), q));
  if(q.trim().length<3) return;
  setTimeout(()=>{
    if(seq!==searchSeq) return;
    Promise.allSettled([araSearch(q), placeSearch(q)]).then(res=>{
      if(seq!==searchSeq) return;
      const rem=res[0].status==='fulfilled'?res[0].value:[];
      const pr=res[1].status==='fulfilled'?res[1].value:{places:[],waters:[]};
      pr.places.forEach(p=>{ p.z=zoneAt(p.lng,p.lat);
        p.sub=[p.ptype, p.z?('Zone '+p.z):'', p.loc||''].filter(Boolean).join(' · '); });
      rem.forEach(w=>{ const e=pr.waters.find(x=>x.nl===w.n.toLowerCase()&&(!x.z||!w.z||x.z===w.z));
        if(e&&e.loc) w.loc=e.loc;
        w.sub=[w.z?('Zone '+w.z):'', w.type||'', w.loc||''].filter(Boolean).join(' · '); });
      renderResults(finalize(buildLocal(q).concat(pr.places, rem), q));
    });
  },350);
}
searchEl.addEventListener('input', onSearch);
gclear.addEventListener('click', ()=>{ searchEl.value=''; onSearch(); });
searchEl.addEventListener('keydown', e=>{ if(e.key==='Escape'){ searchEl.value=''; onSearch(); searchEl.blur(); } });

function metaLine(w){
  const parts=[];
  if(w.z) parts.push('Zone '+w.z);
  if(w.type) parts.push(w.type);
  if(w.area) parts.push(w.area.toLocaleString()+' ha');
  if(w.maxd) parts.push('Max depth '+w.maxd+' m');
  else if(w.meand) parts.push('Mean depth '+w.meand+' m');
  if(w.loc) parts.push(w.loc);
  return parts.join(' · ');
}
function openWater(w){
  if(w.place){ if(IS_MAP&&w.lat!=null) goToWater(w.n,w.lat,w.lng,null); renderPlace(w); return; }
  if(IS_MAP){
    if(w.curated && w.lat!=null) goToWater(w.n,w.lat,w.lng,null);
    else if(w.lid) araCentre(w.lid).then(c=>{ if(c) goToWater(w.n,c.lat,c.lng,null); }).catch(()=>{});
  }
  renderWater(w);
  if(w.curated){
    araSearch(w.n).then(list=>{
      const hit=list.find(x=>x.n.toLowerCase()===w.n.toLowerCase());
      if(hit){ hit.lat=w.lat; hit.lng=w.lng; hit.curated=false; renderWater(hit); }
    }).catch(()=>{});
  }
}
function renderPlace(w){
  showDetail();
  const meta=[w.ptype||'Place', w.z?('Zone '+w.z):'Zone unknown', w.loc||''].filter(Boolean).join(' · ');
  let html=`<div class="zhead"><h2>${esc(w.n)}</h2>
      <button class="fchip" id="wclear">Clear</button></div>
    <p class="meta">${esc(meta)}</p>`;
  if(w.z) html+=`<div class="filters"><button class="fchip on" id="wzone">Zone ${w.z} rules</button></div>`;
  html+=`<p class="meta" style="margin-top:14px">Place data from the Canadian Geographical Names Database.</p>`;
  detailEl.innerHTML=html;
  document.getElementById('wclear').onclick=()=>{ searchEl.value=''; onSearch(); };
  const zb=document.getElementById('wzone');
  if(zb) zb.onclick=()=>selectZone(w.z,true);
}
function renderWater(w){
  showDetail();
  lastWater=w;
  let html=`<div class="zhead"><h2>${esc(w.n)}</h2>
      <button class="fchip" id="wclear">Clear</button></div>
    <p class="meta">${esc(metaLine(w)||'No details on record')}</p>`;
  if(w.z) html+=`<div class="filters"><button class="fchip on" id="wzone">Zone ${w.z} rules</button></div>`;
  if(w.species && w.species.length){
    html+=`<div class="seclabel grey">Fish found here</div>
      <div class="srow"><div class="col"><div class="mt" style="margin:0">${esc(sortSpecies(w.species).join(' · '))}</div></div></div>`;
  }
  html+=`<div class="seclabel grey">Stocking</div><div id="wstock"><p class="empty">Checking stocking records</p></div>
    <p class="meta" style="margin-top:14px">Lake data from Fish ON-Line and MNRF stocking records.</p>`;
  detailEl.innerHTML=html;
  document.getElementById('wclear').onclick=()=>{ searchEl.value=''; onSearch(); };
  const zb=document.getElementById('wzone');
  if(zb) zb.onclick=()=>selectZone(w.z,true);
  searchStocked(w.n).then(list=>{
    const el=document.getElementById('wstock'); if(!el) return;
    const hits=list.filter(x=>x.n.toLowerCase()===w.n.toLowerCase());
    if(!hits.length){ el.innerHTML='<p class="empty">No stocking records since 2017.</p>'; return; }
    const sp={}; hits.forEach(h=>Object.entries(h.sp).forEach(([s,y])=>{ sp[s]=Math.max(sp[s]||0,y); }));
    const where=[hits[0].town, hits[0].dist].filter(Boolean).join(' · ');
    el.innerHTML=(where?`<p class="meta" style="margin:0 0 8px">${esc(where)}</p>`:'')+
      Object.entries(sp).sort((a,b)=>b[1]-a[1]).map(([s,y])=>
      `<div class="srow"><div class="col"><div class="nm">${esc(s)}</div>
        <div class="mt">Last stocked ${y}</div></div></div>`).join('');
  }).catch(()=>{ const el=document.getElementById('wstock'); if(el) el.innerHTML='<p class="empty">Stocking data not reachable.</p>'; });
}
/* species compare */
for(const z in REG) for(const r of REG[z].species_regulations||[]){
  (speciesMap[r.species]=speciesMap[r.species]||{})[z]={season:r.season,limits:r.limits};
}
function openFish(name){
  exploreSpecies=name;
  if(typeof setOverlay==='function' && typeof overlayOn!=='undefined' && !overlayOn) setOverlay(true);
  if(typeof fmz!=='undefined' && fmz) fmz.setStyle(styleFn);
  renderExplore(name);
}
function clearDetail(){ if(selectedZone) renderPanel(selectedZone); else showEmpty(); }
function exitExplore(){ exploreSpecies=null; clearDetail(); }
function renderExplore(name){
  const m=speciesMap[name]||{}, present=[];
  for(let z=1;z<=20;z++){ if(m[z]) present.push({z,rec:m[z],st:seasonStatus(m[z].season).status}); }
  const openN=present.filter(r=>r.st==='open').length;
  detailEl.innerHTML=`<div class="zhead"><h2>${esc(name)}</h2>
      <button class="fchip" id="exitexp">Clear</button></div>
    <p class="meta">${openN} zones open now · in ${present.length} zones</p>
    <div class="seclabel">By zone</div>`
    + present.map(r=>`<button class="srow" data-z="${r.z}"><div class="col">
        <div class="nm">Zone ${r.z}</div>
        <div class="mt">${esc(r.rec.season)}</div>
        <div class="mt">${esc(r.rec.limits)}</div>
      </div><span class="pill ${r.st}">${label(r.st)}</span></button>`).join('');
  document.getElementById('exitexp').onclick=exitExplore;
  detailEl.querySelectorAll('.srow[data-z]').forEach(row=>row.onclick=()=>selectZone(row.dataset.z));
}

/* dialogs */
const backdrop=document.getElementById('backdrop');
const aboutEl=document.getElementById('about'), versionsEl=document.getElementById('versions');
function closeModals(){ aboutEl.classList.remove('on'); versionsEl.classList.remove('on'); backdrop.classList.remove('on'); }
function openModal(el){ closeModals(); el.classList.add('on'); backdrop.classList.add('on'); el.scrollTop=0; }
[aboutEl,versionsEl].forEach(sh=>{
  let sy=null;
  sh.addEventListener('touchstart',e=>{ sy = sh.scrollTop<=0 ? e.touches[0].clientY : null; },{passive:true});
  sh.addEventListener('touchmove',e=>{ if(sy!=null && e.touches[0].clientY-sy>70){ closeModals(); sy=null; } },{passive:true});
});
document.getElementById('verbtn').onclick=()=>openModal(versionsEl);
const logo=document.getElementById('logobtn');
logo.onclick=()=>openModal(aboutEl);
logo.onkeydown=e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); openModal(aboutEl); } };
backdrop.onclick=closeModals;
document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeModals(); });

/* deep links */
function fromHash(){ const m=(location.hash||'').match(/zone=(\d+)/); if(m) selectZone(Number(m[1])); }
window.addEventListener('hashchange',fromHash);
fromHash();

/* offline */
if('serviceWorker' in navigator && location.protocol.startsWith('http')){
  window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
}
</script>
</body>
</html>
"""

MANIFEST = """{
  "name": "ON Fishing Regulation Express",
  "short_name": "ON fishing",
  "description": "Ontario's 20 fishing zones with seasons, limits and what is open right now. The quick version, no map.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#F1F6F1",
  "theme_color": "#00753A",
  "icons": [
    { "src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable" },
    { "src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
"""

SW = """/* Offline support for the express edition. */
const CACHE = 'onfish-express-__VERSION__';
const SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.open(CACHE).then(async cache => {
    const cached = await cache.match(e.request);
    const network = fetch(e.request)
      .then(resp => { if (resp && (resp.ok || resp.type === 'opaque')) cache.put(e.request, resp.clone()); return resp; })
      .catch(() => cached);
    return cached || network;
  }));
});
"""

README = """# Ontario Fishing Regulation, express

The quick, no map edition of the Ontario fishing regulations map. One page:
pick your zone, see the seasons, limits, and what is open right now. Works
offline once loaded and installs to a phone home screen.

Live at `https://katsuma0.github.io/on-fishing-reg-express/` once GitHub
Pages is on (Settings, Pages, deploy from branch `main`, root).

Not an official source. Always check the official
[Ontario Fishing Regulations Summary](https://www.ontario.ca/document/ontario-fishing-regulations-summary)
before you fish.
"""

version_rows = "".join(
    f'<div class="vrow"><span class="vv">{v}</span><span>{t}</span></div>'
    for v, t in VERSIONS)

html = (HTML.replace("__VERSION_ROWS__", version_rows)
            .replace("__REG_JSON__", reg_json)
            .replace("__SERVICE__", SERVICE)
            .replace("__OFFICIAL__", OFFICIAL)
            .replace("__BUILD_DATE__", build_date)
            .replace("__VERSION__", VERSION))

os.makedirs(OUTDIR, exist_ok=True)
with open(f"{OUTDIR}/index.html", "w", encoding="utf-8") as f:
    f.write(html)
with open(f"{OUTDIR}/manifest.json", "w", encoding="utf-8") as f:
    f.write(MANIFEST)
with open(f"{OUTDIR}/sw.js", "w", encoding="utf-8") as f:
    f.write(SW.replace("__VERSION__", VERSION))
with open(f"{OUTDIR}/README.md", "w", encoding="utf-8") as f:
    f.write(README)
for icon in ("icon-192.png", "icon-512.png"):
    shutil.copy(icon, f"{OUTDIR}/{icon}")

with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for name in sorted(os.listdir(OUTDIR)):
        zf.write(f"{OUTDIR}/{name}", name)

print(f"Wrote {OUTDIR}/ ({len(html)//1024} KB page) and {ZIP}")
