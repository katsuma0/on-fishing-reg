#!/usr/bin/env python3
"""
Light cleanup of fishing_zones.json for the interactive map demo.

This does NOT re-parse the PDF. It just tidies the existing extraction so the
regulations panel reads cleanly:
  - removes leaked page markers ("--- PAGE 68 ---") and trailing page numbers
  - fixes the "Not specifie" truncation
  - drops junk "species" rows that are really stray text fragments
  - keeps only waterbody entries that look like real named waters

Output: fishing_zones_clean.json
"""
import json
import re

SRC = "fishing_zones.json"
OUT = "fishing_zones_clean.json"

# A row is a real species only if its name mentions a known fish (or is the
# zone-wide "Aggregate" trout/salmon note).
FISH_TOKENS = [
    "Trout", "Salmon", "Pike", "Walleye", "Sauger", "Perch", "Bass",
    "Whitefish", "Sturgeon", "Muskellunge", "Muskie", "Crappie", "Sunfish",
    "Splake", "Catfish", "Herring", "Cisco", "Eel", "Smelt", "Aggregate",
]


def clean_text(s: str) -> str:
    if not s:
        return s
    # Remove a leaked page-footer number sitting right before a page marker,
    # then the marker itself. We deliberately do NOT strip other trailing
    # numbers, because day-of-month ("September 30") and limits ("C-50") end
    # in numbers too.
    s = re.sub(r"\s*\d{1,3}\s*---\s*PAGE\s*\d+\s*---", " ", s)
    s = re.sub(r"---\s*PAGE\s*\d+\s*---", " ", s)
    s = re.sub(r"\bNot specifie\b", "Not specified", s)
    s = s.replace(" • ", "; ").replace("• ", "; ")   # bullets -> semicolons
    # Label the resident sub-tables so the merged columns at least read clearly.
    s = re.sub(r"Ontario and Canadian residents", "Residents:", s, flags=re.I)
    s = re.sub(r"Non-Canadian residents", "| Non-Canadian:", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip("; ").strip()
    return s


# Intro-paragraph phrases that sometimes bleed into a field on dense pages.
_BLURB = re.compile(
    r'(in the Zone except for the specific waters'
    r'|and species listed in the Species Exceptions'
    r'|species listed in the Species Exceptions'
    r'|Waterbody Exceptions and Fish Sanctuaries'
    r'|Zone-wide seasons and limits apply.*)',
    re.IGNORECASE,
)
# Tokens that belong to a catch limit, never to a season. A season is cut here.
_LIMIT_TOKEN = re.compile(
    r'\b(S-\d|C-\d|\d+\s*cm|cm|possession|than|must be|none greater|in one day)\b',
    re.IGNORECASE,
)


def clean_season(s: str) -> str:
    """Clean a season and strip any limit/blurb text that bled into it."""
    s = _BLURB.sub('', clean_text(s))
    m = _LIMIT_TOKEN.search(s)
    if m:
        s = s[:m.start()]
    s = re.sub(r'\s+', ' ', s).strip(' ,;')
    s = re.sub(r'\b(and|to)\s*$', '', s).strip(' ,;')   # drop dangling connectors
    return s


def clean_limit(s: str) -> str:
    """Clean a limit and cut off any waterbody text that bled in from the next
    section (a real catch limit never contains GPS coordinates or a lake name)."""
    s = clean_text(s)
    m = re.search(r"\d+\s*°", s)                 # GPS coordinate
    if m:
        s = s[:m.start()]
    # strip a trailing dangling waterbody name, e.g. "...C-25; Meggisi Lake ("
    s = re.sub(r"[;,]?\s*[A-Z][\w'’.\- ]*\b(Lake|River|Creek|Bay)\b\s*\(?\s*$", "", s)
    return re.sub(r"\s+", " ", s).strip(" ;,")


def is_real_species(name: str) -> bool:
    return any(tok.lower() in name.lower() for tok in FISH_TOKENS)


def looks_like_waterbody(name: str) -> bool:
    """A real waterbody mentions a water feature or carries coordinates."""
    if re.search(r"\d+\s*°", name):  # GPS coordinates
        return True
    return bool(re.search(
        r"\b(Lake|River|Creek|Bay|Pond|Reservoir|Falls|Rapids|Channel|"
        r"Harbour|Narrows|Township|Waters?)\b", name))


def apply_corrections(out, path="corrections.json"):
    """Overlay hand-verified fixes for entries the dense PDF layout scrambles."""
    import os
    if not os.path.exists(path):
        return
    fixes = json.load(open(path, encoding="utf-8"))
    n = 0
    for zone, per_species in fixes.items():
        if zone.startswith("_") or zone not in out:
            continue
        per_species = dict(per_species)
        full = per_species.pop("_full", False)   # replace the whole zone's list
        existing = {sp["species"]: sp for sp in out[zone]["species_regulations"]}
        for name, fix in per_species.items():
            if name in existing:
                existing[name].update(fix)          # correct a scrambled entry
            else:
                out[zone]["species_regulations"].append({"species": name, **fix})  # add a missing one
            n += 1
        if full:  # drop any leftover scrambled/junk entries not in the overlay
            keep = set(per_species)
            out[zone]["species_regulations"] = [
                sp for sp in out[zone]["species_regulations"] if sp["species"] in keep]
        out[zone]["species_regulations"].sort(key=lambda r: r["species"])
    if n:
        print(f"Applied {n} manual correction(s) from {path}")


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    out = {}
    dropped_species = 0
    for z, zd in data.items():
        species = []
        for r in zd.get("species_regulations", []):
            name = clean_text(r["species"])
            if not is_real_species(name):
                dropped_species += 1
                continue
            species.append({
                "species": name,
                "season": clean_season(r["season"]),
                "limits": clean_limit(r["limits"]),
            })

        waterbodies = []
        for e in zd.get("waterbody_exceptions", []):
            wb = clean_text(e["waterbody"])
            if not looks_like_waterbody(wb):
                continue
            rules = [clean_text(x) for x in e.get("rules", []) if clean_text(x)]
            waterbodies.append({"waterbody": wb, "rules": rules})

        out[z] = {
            "zone_number": zd["zone_number"],
            "general_info": [clean_text(g) for g in zd.get("general_info", [])],
            "species_regulations": species,
            "waterbody_exceptions": waterbodies,
        }

    apply_corrections(out)

    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    total_sp = sum(len(z["species_regulations"]) for z in out.values())
    total_wb = sum(len(z["waterbody_exceptions"]) for z in out.values())
    print(f"Wrote {OUT}: {len(out)} zones, {total_sp} species rows "
          f"({dropped_species} junk dropped), {total_wb} waterbody entries")


if __name__ == "__main__":
    main()
