# Year-over-Year Change Detection: A Data-Quality Case Study

**Question:** *What fishing regulations changed in Ontario between 2025 and 2026?*

**Short answer:** The honest one is that you **cannot answer this reliably by
diffing the two PDFs** — and finding that out, and proving it with numbers, is
the interesting part. This document walks through the attempt, the measurement,
and the decision that followed.

Reproduce with: `python3 04_compare_years.py` (writes `changes_report.json`).

---

## 1. The goal

Anglers don't re-read a 148-page regulations booklet every year — they want to
know *what changed*. So the plan was simple: parse the 2025 and 2026 summaries
into structured data (already done for 2026), then compare them per zone and
per species to surface added species, removed species, and changed
seasons/limits.

## 2. Method

1. Ran the existing pipeline (`01_pdf_parser.py` → `02_clean_for_map.py`) on the
   **2025** PDF, producing `fishing_zones_2025_clean.json` — the same shape as
   the 2026 data (20 zones, ~295 species rows each).
2. Compared the two datasets at three levels of strictness:
   - **Raw:** any difference in a species' season or limits string.
   - **High-confidence:** ignore differences that are clearly extraction
     artifacts — "not specified" on either side, one string being a truncation
     of the other, number-gaps like "greater than ___ cm", and changes where the
     structured catch-limit signature (the `S-n` / `C-n` / size tokens) is
     actually identical.
   - **Authoritative:** the ministry's own `*NEW*` markers, which the PDF prints
     next to genuinely new rules.

## 3. Findings

| Level | Differences detected | Interpretation |
|------:|:--------------------:|:---------------|
| Raw diff | **53** | Almost all are extraction noise, not real changes |
| After strict filtering | **8** | Most are *still* extraction gaps |
| Genuinely real (manual review) | **~1–3** | e.g. Zone 9 Muskellunge size limit |
| Ministry `*NEW*` flags captured | **3** | Authoritative, but parser captures only a subset |

The single clearest real change — Zone 9 Muskellunge minimum size **91 cm →
137 cm** — is one the PDF itself labels `*NEW*`, which is a useful sanity check
that the few survivors include the right answer.

### What the false positives look like

The 53 raw "changes" are dominated by differences in *how the text extracted*,
not differences in *the regulation*:

| Zone / species | 2025 (extracted) | 2026 (extracted) | Why it's not a real change |
|---|---|---|---|
| Z1 Northern Pike | `S-6; not more than 2 greater than 61` | `S-6; ... 61 cm, of which not more than 1...` | 2025 truncated mid-sentence |
| Z9 Lake Whitefish | `open all year 76` | `open all year` | A page number ("76") leaked into 2025 |
| Z2 Lake Trout | `...greater than  cm from September 1` | `...greater than 56 cm from September 1` | 2025 dropped the number "56" |
| Z7 Lake Whitefish | `S-25 and C-12` | `S-25 and C-12 cm` | Stray "cm" bled in from 2026 |

None of these are regulation changes — they're two noisy extractions of the
**same** rule.

## 4. Why diffing fails here

The two documents are laid out in a dense, multi-column format that has to be
reconstructed from raw text positions. That reconstruction is good but not
perfect, and — critically — it makes **different** small mistakes on each year's
PDF (a truncation here, a leaked page number there, a neighbouring column
bleeding in). When you diff two datasets that each carry their own independent
noise, the noise itself shows up as "changes." The true change signal (a
handful of real edits) is buried under a much larger layer of extraction
artifacts, giving a false-positive rate of roughly **90%+** at the raw level.

This is a general lesson, not specific to fishing: **a diff is only as
trustworthy as the consistency of the two inputs.** Comparing two imperfect
extractions amplifies their imperfections.

## 5. The decision

Rather than ship a "What changed" feature that would put obviously-wrong changes
in front of users, the right call is:

- **Don't present the automated diff as authoritative.** It would undermine the
  credibility the rest of the project works to earn.
- **Prefer the source's own change markers.** The ministry already flags real
  changes with `*NEW*`; those are trustworthy. The follow-up work is to parse
  them completely (including the Species Exceptions and Additional Opportunities
  sections the current parser skips), rather than to infer changes by diffing.

The comparison code and `changes_report.json` are kept in the repo as the
evidence behind this decision.

## 6. What this demonstrates

- Building a reproducible comparison pipeline over two real-world datasets.
- **Quantifying data quality** instead of assuming it — measuring a false-positive
  rate and using tiered filters to separate signal from noise.
- Knowing **when not to ship**: recognising that a technically-working feature
  can still be the wrong thing to publish, and choosing an authoritative data
  source over a convenient but noisy inferred one.
