#!/usr/bin/env python3
"""
Year-over-year comparison of the Ontario fishing regulations (2025 vs 2026).

This script was written to answer "what changed since last year?" — and, just
as importantly, to MEASURE how trustworthy an automated answer can be when the
underlying data is extracted from PDFs. It compares the cleaned datasets at
three levels of strictness and cross-checks against the ministry's own *NEW*
change markers. See CHANGES_ANALYSIS.md for the write-up of the findings.

Inputs : fishing_zones_2025_clean.json, fishing_zones_clean.json (2026)
Output : changes_report.json  + a printed summary
"""
import json
import re

Y2025 = "fishing_zones_2025_clean.json"
Y2026 = "fishing_zones_clean.json"
OUT = "changes_report.json"


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower().rstrip(".")


def limit_signature(s):
    """Structured catch-limit tokens (S-n, C-n, sizes) — ignores prose noise."""
    return frozenset(re.findall(r"s-\d+|c-\d+|\d+\s*cm|\d+-\d+\s*cm", s.lower()))


def season_signature(s):
    s = s.lower()
    return frozenset(re.findall(
        r"january|february|march|april|may|june|july|august|september|october"
        r"|november|december|labour day|open all year|closed all year"
        r"|\d+(?:st|nd|rd|th)?\s+(?:saturday|sunday)", s))


def substring_related(a, b):
    a, b = norm(a), norm(b)
    return a in b or b in a


def looks_like_extraction_gap(a, b):
    """One side missing a number it should have (e.g. 'greater than  cm')."""
    return bool(re.search(r"(greater|less) than\s+cm", a + " " + b)) \
        or "not specified" in (norm(a), norm(b))


def main():
    a = json.load(open(Y2025, encoding="utf-8"))
    b = json.load(open(Y2026, encoding="utf-8"))

    raw = {"added": [], "removed": [], "changed": []}
    high_conf = []

    for z in map(str, range(1, 21)):
        A = {r["species"]: r for r in a.get(z, {}).get("species_regulations", [])}
        B = {r["species"]: r for r in b.get(z, {}).get("species_regulations", [])}

        for sp in B:
            if sp not in A:
                raw["added"].append({"zone": z, "species": sp})
        for sp in A:
            if sp not in B:
                raw["removed"].append({"zone": z, "species": sp})

        for sp in set(A) & set(B):
            for field, sig in (("season", season_signature), ("limits", limit_signature)):
                old, new = A[sp][field], B[sp][field]
                if norm(old) == norm(new):
                    continue
                raw["changed"].append({"zone": z, "species": sp, "field": field,
                                       "from": old, "to": new})
                # High-confidence filter: a real change, not an extraction artifact.
                if (not looks_like_extraction_gap(old, new)
                        and not substring_related(old, new)
                        and sig(old) != sig(new)):
                    high_conf.append({"zone": z, "species": sp, "field": field,
                                      "from": old, "to": new})

    # Ministry's own change markers in the 2026 data (authoritative but sparse).
    new_flags = []
    for z in map(str, range(1, 21)):
        zd = b.get(z, {})
        for g in zd.get("general_info", []):
            if "*NEW*" in g:
                new_flags.append({"zone": z, "type": "general_info", "text": g})
        for r in zd.get("species_regulations", []):
            if "NEW" in (r["season"] + r["limits"]):
                new_flags.append({"zone": z, "type": "species", "species": r["species"],
                                  "season": r["season"], "limits": r["limits"]})

    report = {
        "raw_differences": {
            "added": len(raw["added"]), "removed": len(raw["removed"]),
            "changed": len(raw["changed"]),
            "total": len(raw["added"]) + len(raw["removed"]) + len(raw["changed"]),
        },
        "high_confidence_changes": high_conf,
        "ministry_new_flags": new_flags,
        "raw_detail": raw,
    }
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    rd = report["raw_differences"]
    print(f"Raw differences detected: {rd['total']} "
          f"(added {rd['added']}, removed {rd['removed']}, changed {rd['changed']})")
    print(f"After strict noise filtering: {len(high_conf)} high-confidence changes")
    print(f"Ministry *NEW* markers captured: {len(new_flags)}")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
