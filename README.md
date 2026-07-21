# Ontario Fishing Regulations — Interactive Zone Map

An interactive web map of Ontario's 20 **Fisheries Management Zones (FMZ)**.
Click a zone to see its fishing seasons, catch limits and waterbody exceptions,
extracted from the official 2026 *Ontario Fishing Regulations Summary* PDF.

**Live demo:** open `index.html` in a browser. (To publish, see
[Deploying to GitHub Pages](#deploying-to-github-pages).)

![zones](https://img.shields.io/badge/zones-20-blue) ![data](https://img.shields.io/badge/data-2026%20summary-green)

---

## About this project

I wanted to see what I could build with AI, so I picked something I'm actually
interested in: fishing. Ontario's official regulations come as a **148-page PDF**
that's slow to search and easy to misread, so I set out to turn it into something
you can actually use — an interactive map where you click your zone (or use your
location) and immediately see the seasons, catch limits, and what's open or closed
*right now*.

It turned into a full data pipeline: pull structured data out of a messy PDF, clean
it, and wire it to a live map of Ontario's official fishing zones. This README
explains how each part works.

**It was not fully automatic.** The AI did the heavy lifting — writing the parser,
the map, and the whole pipeline — but the PDF's dense multi-column tables scramble
so easily that a lot of **manual checking** was still needed. I went zone by zone
comparing the extracted species against the official guide, tracked down entries
whose data had bled between columns or whose names had been mangled, and
hand-transcribed the worst cases into `corrections.json` and verified them against
the source. So the result is AI-built but human-verified.

Built with **Claude Code (Opus 4.8 model)**.

## Features

- **Clickable map** of all 20 zones, drawn live from Ontario's official boundary
  service (always the current, accurate shapes).
- **Find my zone** — uses your device GPS to identify the zone you're standing in.
- **Click-to-identify** — click anywhere on the map to jump to that zone.
- **Lake search with stocking history** — search a curated list of well-known
  waters plus, live, the MNRF [Fish Stocking Data For Recreational Purposes](https://geohub.lio.gov.on.ca/datasets/mnrf::fish-stocking-data-for-recreational-purposes)
  layer (thousands of stocked waterbodies). Results show the water's zone
  (point-in-polygon against the official boundaries) and what it was stocked
  with, by year.
- **Species compare** — pick a species and see its season and limits across every zone.
- **Open now / closed now** — each zone shows how many species are open today, a
  colour dot per species, an **open-only filter**, and **opening/closing-soon**
  badges (within 14 days), all computed from the current date.
- **Species explorer** — pick a species and the whole province recolours by where
  it's open right now, with a per-zone list of seasons and limits.
- **Works offline / installable** — a service worker caches the app, boundaries
  and map tiles, so once loaded it works without a connection. On a phone you can
  "Add to Home Screen" and run it like an app (PWA).
- **Shareable links** — every zone has a deep link, e.g. `index.html#zone=5`.
- **Disclaimer + About** — a disclaimer gate on load and a reopenable "About"
  panel explaining the project, with a prominent note to verify waterbody
  exceptions against the official summary.
- **Self-contained** — regulations are embedded in the page.

## How it works

The project is a three-stage pipeline plus a live map:

```
PDF  ──①──►  fishing_zones.json  ──②──►  fishing_zones_clean.json  ──③──►  index.html
                                              ▲
                                   corrections.json (hand-verified fixes)
```

| Step | Script | What it does |
|------|--------|--------------|
| ① | `01_pdf_parser.py` | Reads the PDF and extracts each zone's species, seasons, limits and waterbody exceptions. |
| ② | `02_clean_for_map.py` | Cleans the extracted text and applies `corrections.json`. |
| ③ | `03_build_map.py` | Builds the standalone `index.html` with the data embedded. |
| + | `04_compare_years.py` | Year-over-year comparison (see [analysis](#year-over-year-analysis)). |

### Extracting the data from the PDF

The hard part is that the regulations are laid out in **dense two- and
three-column tables**, so reading the PDF top-to-bottom scrambles everything. The
parser rebuilds the real reading order and structure:

1. **Column-aware reconstruction.** Using [`pdfplumber`](https://github.com/jsvine/pdfplumber),
   every word is read with its `(x, y)` position. Words are grouped into rows,
   the page's column gutter is detected, and each column is read top-to-bottom in
   order — so a species and its season/limits stay together instead of interleaving
   with the neighbouring column. Full-width lines (like general-info bullets) are
   kept inline; two-column blocks are split.
2. **Zone sectioning.** Each of the 20 zones spans several pages and repeats itself
   in running headers. Segments are matched and merged per zone, including a fix
   for a bold font that doubles every character (`ZZoonnee 88` → `Zone 8`).
3. **Stack-based species parser.** Within a zone's "Zone-wide Seasons and Limits"
   section, each species is `Name → Season → Limits`. On dense pages two names sit
   side by side and their blocks arrive out of order, so each name is pushed onto a
   stack and a `Season:`/`Limits:` line is assigned to the most recent name still
   missing that field. Wrapped lines are routed to season vs limits by content
   (e.g. text containing "cm" or "C-2" is a limit; a month/weekday is a season), and
   an "incomplete-ending" heuristic reunites a fragment with the entry it belongs to.
4. **Rescue pass.** Some species get pushed past a section boundary by the column
   layout; a second pass recovers any known-fish `Name/Season/Limits` block that
   wasn't captured.
5. **Cleaning** (`02_clean_for_map.py`) strips page-number/footer noise, cuts limit
   text at GPS coordinates that bled in from the next section, and drops rows that
   aren't real species.
6. **Corrections overlay** (`corrections.json`). A handful of entries on the very
   worst-scrambled pages can't be reassembled automatically. Those are transcribed
   by hand from the official summary and applied last, so the published data is
   correct even where automated parsing can't be.

Result: **~309 species rows across all 20 zones**, plus general information and
(roughly extracted) waterbody exceptions.

### Building the map

The front-end is a single self-contained `index.html` (no build tools):

- **Map:** [Leaflet](https://leafletjs.com/) with a [CARTO](https://carto.com/basemaps/)
  basemap. The base tiles have no labels; a second labels layer is **clipped to the
  Ontario outline** with an SVG clip-path (kept in sync as you pan/zoom) so only
  Ontario shows place names.
- **Zone boundaries:** fetched live in the browser from Ontario's official
  **ArcGIS FeatureServer** via [esri-leaflet](https://developers.arcgis.com/esri-leaflet/),
  so the shapes are always the current official ones (nothing is stored in the repo).
- **The join:** each polygon carries `FISHERIES_MANAGEMENT_ZONE_ID` (1–20), which
  keys straight into the embedded regulations JSON. Click a zone → look up its data.
- **Find my zone / click-to-identify:** the browser's geolocation (or a map click)
  gives a point, and a **ray-casting point-in-polygon** test against the loaded zone
  geometry says which zone it's in — no server needed.
- **"Open now":** a small season parser resolves phrases like *"January 1 to April 14
  and third Saturday in May to December 31"* into real dates for the current year and
  compares them to today, driving the open/closed dots and the opening/closing-soon
  badges.
- **Offline / installable:** a service worker (`sw.js`) plus a web manifest make it a
  PWA — it caches the app, boundaries and tiles so it keeps working without signal.

### Built with

Python (`pdfplumber`) for extraction · plain HTML/CSS/JavaScript ·
Leaflet + esri-leaflet · Ontario Land Information ArcGIS services · CARTO basemaps.
No frameworks, no backend — the site is fully static.

## Regenerate the data

```bash
pip install pdfplumber
python3 01_pdf_parser.py mnr-2026-fishing-regulations-summary-en-2025-12-08.pdf
python3 02_clean_for_map.py
python3 03_build_map.py        # writes index.html
```

(Parsing the full 148-page PDF takes ~2 minutes.)

## Deploying to GitHub Pages

`index.html` is the entry point, so hosting is one step:

1. Create a new GitHub repository and push this folder to it.
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source = Deploy from a branch**, branch
   `main`, folder `/ (root)`, then **Save**.
4. Your site goes live at `https://<your-username>.github.io/<repo-name>/` within
   a minute or two.

No build step is required — it's a static site. The offline/installable (PWA)
features need `index.html`, `manifest.json`, `sw.js` and the two `icon-*.png`
files at the site root (they are already here), and only activate over https —
which GitHub Pages provides automatically.

## Data sources & licence

- **Zone boundaries:** [Fisheries Management Zone, Ontario GeoHub](https://geohub.lio.gov.on.ca/datasets/lio::fisheries-management-zone)
  — © King's Printer for Ontario, under the
  [Open Government Licence – Ontario](https://www.ontario.ca/page/open-government-licence-ontario).
- **Regulations:** [Ontario Fishing Regulations Summary](https://www.ontario.ca/document/ontario-fishing-regulations-summary).

## Year-over-year analysis

[`CHANGES_ANALYSIS.md`](CHANGES_ANALYSIS.md) is a short case study on detecting
what changed between the 2025 and 2026 regulations. It documents why a naive
diff of the two PDFs is unreliable (≈90% of detected "changes" are extraction
artifacts), how that false-positive rate was measured, and the decision to rely
on the source's own change markers instead. Reproduce with
`python3 04_compare_years.py`.

## ⚠️ Disclaimer

This is an **unofficial** tool. Species and seasons are reliable, but some catch
limits and waterbody exceptions are approximate (auto-extracted from a PDF).
**Always confirm against the official summary before fishing.**

## Known limitations

- A few entries that the PDF's dense multi-column layout scrambles beyond
  automatic reassembly are fixed by a small hand-verified overlay
  (`corrections.json`, applied during cleaning). The parser also runs a "rescue"
  pass that recovers zone-wide species pushed past a section boundary.
- Catch limits in zones with separate resident / non-resident rules (5, 7, 9, 11,
  17, 20) can still contain merged text from the PDF's multi-column tables.
- Waterbody exceptions are extracted roughly; treat them as pointers, not gospel.
- The "open now" indicator shows *check dates* for seasons with anchors it can't
  resolve (e.g. "Friday before the fourth Saturday in April").
