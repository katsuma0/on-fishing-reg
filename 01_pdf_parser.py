#!/usr/bin/env python3
"""
Ontario Fishing Regulations PDF Parser - v2

Extracts zones, species regulations, seasons, limits, and waterbody exceptions
from the Ontario Fishing Regulations Summary PDF.

Usage:
    python 01_pdf_parser.py <pdf_path> [--output-json <path>] [--output-csv <path>]
"""

import pdfplumber
import json
import re
import sys
import argparse
import statistics
from typing import Dict, List, Tuple
from pathlib import Path


# Lines that act as section/zone headers. When one of these appears as a
# left-only line in the two-column body it must flush the column buffers,
# otherwise content from different zones/sections gets interleaved.
# A header line is matched only when the WHOLE line is the header (anchored
# ^...$). Without the end anchor, intro prose such as "...listed in the Species
# Exceptions, Waterbody Exceptions and Fish Sanctuaries" would be mistaken for a
# section header and trigger a column flush mid-species — which dropped the
# second timeframe of two-period seasons (e.g. Zone 11 Largemouth Bass).
HEADER_RE = re.compile(
    r'^(?:'
    r'Zone\s+\d+(?:\s*,\s*\d+)*(?:\s+Zone\s+\d+(?:\s*,\s*\d+)*)?'  # zone / running headers
    r'|General Information'
    r'|Zone-wide Seasons and Limits'
    r'|Species Exceptions'
    r'|Waterbody Exceptions'
    r'|Additional Fishing Opportunities'
    r'|Fish Sanctuaries'
    r')\s*$',
    re.IGNORECASE,
)


class OntarioFishingPDFParser:
    """Parse Ontario Fishing Regulations Summary PDF."""

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.all_data = {}

    def parse(self):
        """Main entry point: parse entire PDF."""
        print("[1/2] Scanning PDF for zone content...")
        with pdfplumber.open(self.pdf_path) as pdf:
            all_text = self._extract_all_text(pdf)

        print("[2/2] Extracting zone regulations...")
        self.all_data = self._extract_zones_from_text(all_text)

        print(f"\n✓ Extraction complete!")
        print(f"  Total zones extracted: {len(self.all_data)}")
        return self.all_data

    def _extract_all_text(self, pdf) -> str:
        """Extract all text from PDF, reconstructing the two-column layout.

        The regulations pages mix full-width content (General Information
        bullets) with a two-column body (species seasons/limits). A plain
        page.extract_text() reads each visual row left-to-right and so
        interleaves the two columns, scrambling species data. Here we
        rebuild a clean reading order: full-width lines stay inline, and
        each two-column block is read left column top-to-bottom, then the
        right column top-to-bottom.
        """
        # Zone content begins around page 28. The earlier front-matter pages
        # (maps, large tables) are irrelevant here and very slow to process,
        # so we skip them. A small safety margin is kept before page 28.
        first_page = 24  # 0-indexed → page 25
        full_text = ""
        for page_num, page in enumerate(pdf.pages):
            if page_num < first_page:
                continue
            text = self._reconstruct_page(page)
            if text:
                full_text += f"\n--- PAGE {page_num + 1} ---\n{text}"
        return full_text

    def _reconstruct_page(self, page, gap_thresh=26, gut_lo=160,
                          gut_hi=410, tol=3, edge=12) -> str:
        """Rebuild a single page's text in proper reading order.

        Strategy:
          1. Group words into visual rows by their vertical position.
          2. Estimate the column gutter (x) from rows that contain a wide
             internal gap near the middle of the page.
          3. Classify each row:
               - header line  -> flush column buffers, emit on its own line
               - full-width    -> flush buffers, emit the row inline
               - otherwise     -> a column row; bucket its words into the
                                   left/right buffer by the gutter.
          4. Flushing emits the buffered left column (top-to-bottom) then
             the right column (top-to-bottom).
        """
        words = page.extract_words()
        if not words:
            return ""

        rows = self._group_rows(words, tol)

        # Estimate the gutter from clearly two-column rows.
        gutters = []
        for row in rows:
            rs = sorted(row, key=lambda w: w['x0'])
            for a, b in zip(rs, rs[1:]):
                gap = b['x0'] - a['x1']
                mid = (a['x1'] + b['x0']) / 2
                if gap >= gap_thresh and gut_lo < mid < gut_hi:
                    gutters.append(mid)
        G = statistics.median(gutters) if gutters else page.width / 2

        out: List[str] = []
        left_buf: List[dict] = []
        right_buf: List[dict] = []

        def flush():
            for line in self._lines_from_words(left_buf, tol):
                out.append(line)
            for line in self._lines_from_words(right_buf, tol):
                out.append(line)
            left_buf.clear()
            right_buf.clear()

        for row in rows:
            rs = sorted(row, key=lambda w: w['x0'])
            left_words = [w for w in rs if (w['x0'] + w['x1']) / 2 < G]
            right_words = [w for w in rs if (w['x0'] + w['x1']) / 2 >= G]
            left_text = ' '.join(w['text'] for w in left_words).strip()

            has_left = any(w['x1'] < G - edge for w in rs)
            has_right = any(w['x0'] > G + edge for w in rs)
            straddle = max(
                [b['x0'] - a['x1'] for a, b in zip(rs, rs[1:])
                 if a['x1'] <= G <= b['x0']] + [0]
            )
            full_width = has_left and has_right and straddle < gap_thresh

            if HEADER_RE.match(left_text):
                # A header line (possibly the left half of a two-column row
                # whose right half is the first species, e.g.
                # "Zone-wide Seasons and Limits | Lake Whitefish").
                flush()
                out.append(left_text)
                right_buf.extend(right_words)
            elif full_width:
                flush()
                out.append(' '.join(w['text'] for w in rs))
            else:
                left_buf.extend(left_words)
                right_buf.extend(right_words)

        flush()
        return '\n'.join(out)

    @staticmethod
    def _group_rows(words, tol=3) -> List[List[dict]]:
        """Cluster words into visual rows by their 'top' coordinate."""
        rows: List[List[dict]] = []
        cur: List[dict] = []
        last = None
        for w in sorted(words, key=lambda w: (round(w['top']), w['x0'])):
            if last is None or abs(w['top'] - last) <= tol:
                cur.append(w)
            else:
                rows.append(cur)
                cur = [w]
            last = w['top']
        if cur:
            rows.append(cur)
        return rows

    @classmethod
    def _lines_from_words(cls, words, tol=3) -> List[str]:
        """Turn a bag of words into lines, ordered top-to-bottom."""
        if not words:
            return []
        lines = []
        for row in cls._group_rows(words, tol):
            row = sorted(row, key=lambda w: w['x0'])
            lines.append(' '.join(w['text'] for w in row))
        return lines

    def _extract_zones_from_text(self, full_text: str) -> Dict:
        """Extract all zones from full PDF text.

        A single zone spans many pages, and each page repeats the zone as a
        running header. We segment the text at every zone-header line, assign
        each segment to its zone, then CONCATENATE all segments belonging to
        the same zone so multi-page zones keep their full content.
        """
        zones_data = {}

        # Skip front matter; zone content starts around page 28.
        zone_content_start = full_text.find('--- PAGE 28 ---')
        if zone_content_start == -1:
            zone_content_start = 0
        zone_text_only = full_text[zone_content_start:]

        # A header line is *purely* zone tokens, e.g.:
        #   "Zone 1, 2 Zone 1"   (combined running header + section title)
        #   "Zone 2"             (section title / running header)
        # This avoids matching body prose like "Zone 2 boundary, including...".
        # Some divider pages render the header in a bold font that the text
        # layer doubles every character on, e.g. "ZZoonnee 88" for "Zone 8";
        # such lines are normalised before testing (see _normalize_header).
        header_re = re.compile(
            r'^Zone\s+\d+(?:\s*,\s*\d+)*(?:\s+Zone\s+\d+(?:\s*,\s*\d+)*)?\s*$'
        )

        # Scan line by line so we can normalise doubled-character headers while
        # keeping each header's true offset for slicing.
        boundaries = []  # (offset, active_zone)
        offset = 0
        for raw_line in zone_text_only.split('\n'):
            line = self._normalize_header(raw_line.strip())
            if header_re.match(line):
                nums = [int(n) for n in re.findall(r'\d+', line)]
                if nums:
                    # The active zone is the last token on the header line: for
                    # "Zone 1, 2 Zone 1" the section that follows is Zone 1; for
                    # a plain "Zone 2" it is Zone 2.
                    boundaries.append((offset, nums[-1]))
            offset += len(raw_line) + 1  # +1 for the split '\n'

        # Collect text segments per zone number.
        segments: Dict[int, List[str]] = {}
        for i, (start_pos, active_zone) in enumerate(boundaries):
            end_pos = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(zone_text_only)
            segments.setdefault(active_zone, []).append(
                zone_text_only[start_pos:end_pos]
            )

        for zone_num in sorted(segments):
            if not 1 <= zone_num <= 20:  # Ontario has 20 fishing zones
                continue
            print(f"   Processing Zone {zone_num}...")
            combined = '\n'.join(segments[zone_num])
            zones_data[zone_num] = {
                'zone_number': zone_num,
                'general_info': self._extract_general_info(combined),
                'species_regulations': self._extract_species_regulations(combined),
                'waterbody_exceptions': self._extract_waterbody_exceptions(combined),
            }

        return zones_data

    @staticmethod
    def _normalize_header(line: str) -> str:
        """Collapse doubled-character header artifacts, e.g. 'ZZoonnee 88'.

        Only applied to lines that look like a doubled "Zone" header so normal
        prose (which can legitimately contain double letters) is left intact.
        """
        if re.match(r'Z\s*Z', line):
            return re.sub(r'(.)\1', r'\1', line)
        return line

    def _extract_general_info(self, text: str) -> List[str]:
        """Extract general information bullet points."""
        info = []

        # Find General Information section
        match = re.search(
            r'General Information\s*(.*?)(?=Zone-wide Seasons|Waterbody Exceptions|Species Exceptions|$)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        if not match:
            return info

        section = match.group(1)
        for line in section.split('\n'):
            line = line.strip()
            if line and line.startswith('•'):
                info.append(line[1:].strip())

        return info

    # Boilerplate/intro lines inside the "Zone-wide Seasons and Limits"
    # section that are not species data and should be ignored.
    _SPECIES_NOISE_RE = re.compile(
        r'^(Zone-wide seasons'
        r'|waters in the Zone'
        r'|and species listed'
        r'|Waterbody Exceptions and'
        r'|\(including'
        r'|total daily catch'
        r'|possession limit'
        r'|species combined)',
        re.IGNORECASE,
    )

    # Date-like content used to recognise a wrapped second line of a season.
    _DATE_RE = re.compile(
        r'(January|February|March|April|May|June|July|August|September'
        r'|October|November|December|Labour Day|Saturday|Sunday|open all year'
        r'|closed|\bto\b|^\d)',
        re.IGNORECASE,
    )

    # Limit-like content: catch-limit numbers and size rules. Used to route a
    # wrapped continuation line to the right field, so limit text from an
    # adjacent column does not bleed into a season (and vice-versa).
    _LIMIT_RE = re.compile(
        r'(\bcm\b|S-\d|C-\d|greater than|less than|between|no size|size limit'
        r'|possession|daily catch|must be|none greater|in one day)',
        re.IGNORECASE,
    )

    # A standalone species-name line (used by the rescue pass to recover
    # zone-wide species pushed past the section boundary on dense pages).
    _FISH_NAME_RE = re.compile(
        r'^(Aggregate Limits for Trout and Salmon'
        r'|Atlantic Salmon|Pacific Salmon'
        r'|Brook Trout|Brown Trout|Rainbow Trout|Lake Trout|Splake'
        r'|Lake Whitefish|Lake Sturgeon|Lake Herring \(Cisco\)'
        r'|Northern Pike|Muskellunge|Walleye and Sauger combined'
        r'|Yellow Perch|Sunfish|Crappie|Channel Catfish'
        r'|Largemouth and Smallmouth Bass combined)\s*$',
        re.IGNORECASE,
    )

    # A field left grammatically hanging (its wrapped remainder is on a later,
    # out-of-order line). Used to reunite an orphan continuation with its owner.
    _INCOMPLETE_END_RE = re.compile(
        r'(greater|less|than|between|\band\b|\bmore\b|none|of which|\bto\b|,'
        r'|residents?|:)\s*$',   # "...Ontario and Canadian residents" -> awaits bullets
        re.IGNORECASE,
    )

    def _extract_species_regulations(self, text: str) -> List[Dict]:
        """Extract species with their seasons and limits.

        Operates on column-reconstructed text where each species appears as a
        contiguous block:

            Lake Whitefish
            Season: open all year
            Limits: S-12 and C-6

        A species *name* line starts a new entry; "Season:" / "Limits:" lines
        fill its fields; lines that begin lowercase, with a digit, or with a
        bracket are continuations of the field currently being read (limits
        and seasons frequently wrap across lines).
        """
        regulations: List[Dict] = []

        # Terminate the section only on a *standalone* subsection header line
        # (anchored with ^...$). The intro blurb contains the phrase
        # "...listed in the Species Exceptions, Waterbody Exceptions and Fish
        # Sanctuaries", so an unanchored match would cut the section off after
        # the first species. The per-zone text is already isolated, so running
        # to the end (\Z) when no subsection header exists is safe.
        match = re.search(
            r'Zone-wide Seasons and Limits(.*?)'
            r'(?=^(?:Species Exceptions|Waterbody Exceptions|'
            r'Additional Fishing Opportunities|Fish Sanctuaries)\s*$|\Z)',
            text,
            re.DOTALL | re.MULTILINE | re.IGNORECASE,
        )
        if not match:
            return regulations

        lines = [
            l.strip() for l in match.group(1).split('\n')
            if l.strip() and not self._SPECIES_NOISE_RE.match(l.strip())
        ]

        # Stack-based assignment. In simple zones a species is a contiguous
        # block (name / Season / Limits). But in dense zones (e.g. Zone 17) two
        # species names sit side by side and their Season/Limits blocks appear
        # later and out of order, e.g.
        #     Atlantic Salmon
        #     Largemouth and Smallmouth Bass combined
        #     Season: ...        <- belongs to Largemouth (the most recent name)
        #     Limits: ...
        #     ... (more species) ...
        #     Season: ...        <- finally Atlantic Salmon's, an "orphan" block
        #     Limits: ...
        # So each name is pushed onto a stack, and a Season/Limits line is given
        # to the most recently pushed name that still lacks that field. This
        # recovers species a strictly-sequential parser would drop.
        stack: List[Dict] = []   # names awaiting season/limits (LIFO)
        order: List[Dict] = []   # entries in the order their names appeared
        last_season = None       # entry whose season was written most recently
        last_limits = None       # entry whose limits was written most recently
        last = None              # (entry, field) most recently written, fallback

        def new_entry(name="Unknown"):
            e = {'species': name, 'season': 'Not specified', 'limits': 'Not specified'}
            stack.append(e)
            order.append(e)
            return e

        def target_missing(field):
            for e in reversed(stack):
                if e[field] == 'Not specified':
                    return e
            return new_entry()

        def find_incomplete(field):
            # The most recent entry whose field was left hanging mid-phrase.
            for e in reversed(order):
                v = e[field]
                if v != 'Not specified' and self._INCOMPLETE_END_RE.search(v):
                    return e
            return None

        for line in lines:
            season_m = re.match(r'^Season:\s*(.*)$', line, re.IGNORECASE)
            if season_m:
                e = target_missing('season')
                e['season'] = season_m.group(1).strip()
                last_season = e; last = (e, 'season')
                continue

            if 'Limits:' in line:
                e = target_missing('limits')
                e['limits'] = re.search(r'Limits:\s*(.*)$', line).group(1).strip()
                last_limits = e; last = (e, 'limits')
                continue

            # A wrapped continuation line (starts lowercase / digit / bracket).
            # Route it by what it looks like, so limit text from an adjacent
            # column doesn't get appended to a season (the Zone 17 Lake Sturgeon
            # bug) and date text doesn't end up in a limit.
            if line[0].islower() or line[0].isdigit() or line[0] in '(•*-':
                if self._LIMIT_RE.search(line):
                    e = find_incomplete('limits') or last_limits
                    if e is not None:
                        e['limits'] += f" {line}"; last_limits = e; last = (e, 'limits')
                    elif last:
                        last[0][last[1]] += f" {line}"
                elif self._DATE_RE.search(line):
                    e = find_incomplete('season') or last_season
                    if e is not None:
                        e['season'] += f" {line}"; last_season = e; last = (e, 'season')
                    elif last:
                        last[0][last[1]] += f" {line}"
                elif last:
                    last[0][last[1]] += f" {line}"
                continue

            # A capitalized date-like line continues a season's second period,
            # e.g. "July 1 to December 31" after "January 1 to April 30 and".
            if last_season is not None and last and last[1] == 'season' and self._DATE_RE.search(line):
                last_season['season'] += f" {line}"
                continue

            # Otherwise it's a new species name.
            new_entry(line)

        for entry in order:
            if entry['season'] == 'Not specified' and entry['limits'] == 'Not specified':
                continue
            entry['species'] = re.sub(r'\s+', ' ', entry['species']).strip()
            entry['season'] = re.sub(r'\s+', ' ', entry['season']).strip()
            entry['limits'] = re.sub(r'\s+', ' ', entry['limits']).strip().rstrip(' ;,and')
            if 2 < len(entry['species']) < 70 and entry['species'] != 'Unknown':
                regulations.append(entry)

        # Rescue pass: on dense pages the multi-column reconstruction can push a
        # zone-wide species (name + Season + Limits) past the section boundary
        # into the text that follows (e.g. Zone 2 Muskellunge). Recover any
        # known-fish block that appears later in the zone but wasn't captured.
        captured = {r['species'].lower() for r in regulations}
        tail = [l.strip() for l in text[match.end():].split('\n') if l.strip()]
        i = 0
        while i < len(tail):
            if self._FISH_NAME_RE.match(tail[i]) and tail[i].lower() not in captured:
                name = tail[i]
                season, limits, mode, j = '', '', None, i + 1
                while j < len(tail) and j < i + 10:
                    L = tail[j]
                    if self._FISH_NAME_RE.match(L):
                        break
                    if L.startswith('Fishing Regulations Summary') or re.fullmatch(r'\d{1,3}', L):
                        break   # page footer / number ends the block
                    sm = re.match(r'^Season:\s*(.*)$', L, re.IGNORECASE)
                    lm = re.search(r'Limits:\s*(.*)$', L)
                    if sm:
                        season = sm.group(1).strip(); mode = 'season'
                    elif lm:
                        limits = lm.group(1).strip(); mode = 'limits'
                    elif mode == 'season':
                        season += ' ' + L
                    elif mode == 'limits':
                        limits += ' ' + L
                    j += 1
                # Only accept a clean block that actually captured season+limits.
                if season and limits:
                    regulations.append({
                        'species': name,
                        'season': re.sub(r'\s+', ' ', season).strip(),
                        'limits': re.sub(r'\s+', ' ', limits).strip().rstrip(' ;,and'),
                    })
                    captured.add(name.lower())
                i = j
            else:
                i += 1

        return regulations

    def _extract_waterbody_exceptions(self, text: str) -> List[Dict]:
        """Extract waterbody-specific exceptions.

        Each entry is a named waterbody (usually carrying GPS coordinates,
        e.g. "Big Vermilion Lake (50°02'00\"N, 92°13'00\"W)") followed by a
        list of bullet rules. Both names and rules can wrap across lines.
        """
        exceptions = []

        # Anchor to the *standalone* "Waterbody Exceptions" header line, and
        # stop at the next standalone subsection header. Anchoring matters:
        # the General Information blurb contains the phrase "...Species
        # Exceptions, Waterbody Exceptions and Fish Sanctuaries", which an
        # unanchored pattern would latch onto. Per-zone text is isolated, so
        # running to the end (\Z) when there is no following header is safe.
        match = re.search(
            r'^Waterbody Exceptions\s*$(.*?)'
            r'(?=^(?:Species Exceptions|Additional Fishing Opportunities|'
            r'Fish Sanctuaries|Changes)\s*$|\Z)',
            text,
            re.DOTALL | re.MULTILINE | re.IGNORECASE,
        )
        if not match:
            return exceptions

        lines = [l.strip() for l in match.group(1).split('\n') if l.strip()]

        current_waterbody = None
        current_rules: List[str] = []

        def save():
            if current_waterbody and current_rules:
                exceptions.append({
                    'waterbody': re.sub(r'\s+', ' ', current_waterbody).strip(),
                    'rules': current_rules,
                })

        for line in lines:
            # Page-footer noise: a bare page number or the running footer.
            if re.fullmatch(r'\d{1,3}', line) or 'Fishing Regulations Summary' in line:
                continue

            if line.startswith('•') or line.startswith('*'):
                # A bullet rule (only meaningful once we have a waterbody).
                if current_waterbody:
                    current_rules.append(line[1:].strip())
                continue

            is_continuation = line[0].islower() or line[0].isdigit() or line[0] in '(),'
            if is_continuation:
                # Wrapped text: extend the last rule, or the name if no rules
                # have been seen yet (coordinates often wrap onto a new line).
                if current_rules:
                    current_rules[-1] += f" {line}"
                elif current_waterbody:
                    current_waterbody += f" {line}"
                continue

            # A new waterbody name (skip species/limit/season fragments).
            if ('Limits:' in line or 'Season:' in line):
                if current_rules:
                    current_rules[-1] += f" {line}"
                continue

            save()
            current_waterbody = line
            current_rules = []

        save()
        return exceptions

    def save_to_json(self, output_path: str):
        """Save parsed data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.all_data, f, indent=2)
        print(f"✓ Saved JSON to {output_path}")

    def save_to_csv(self, output_path: str):
        """Save species regulations to CSV."""
        import csv

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Zone', 'Species', 'Season', 'Limits'])

            for zone_num in sorted(self.all_data.keys()):
                zone_data = self.all_data[zone_num]
                for reg in zone_data.get('species_regulations', []):
                    writer.writerow([
                        zone_num,
                        reg['species'],
                        reg['season'],
                        reg['limits']
                    ])

        print(f"✓ Saved CSV to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Parse Ontario Fishing Regulations PDF'
    )
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument(
        '--output-json',
        default='fishing_zones.json',
        help='Output JSON file path (default: fishing_zones.json)'
    )
    parser.add_argument(
        '--output-csv',
        default='fishing_zones.csv',
        help='Output CSV file path (default: fishing_zones.csv)'
    )

    args = parser.parse_args()

    if not Path(args.pdf_path).exists():
        print(f"Error: PDF file not found: {args.pdf_path}")
        sys.exit(1)

    print("\n" + "="*70)
    print("Ontario Fishing Regulations PDF Parser (v2)")
    print("="*70 + "\n")

    parser_obj = OntarioFishingPDFParser(args.pdf_path)
    data = parser_obj.parse()

    print("\n" + "="*70)
    print("Saving results...")
    print("="*70 + "\n")
    parser_obj.save_to_json(args.output_json)
    parser_obj.save_to_csv(args.output_csv)

    # Show sample
    print("\n" + "="*70)
    print("Sample: Zone 1")
    print("="*70)
    if 1 in data:
        zone_1 = data[1]
        print(f"\n✓ General Info: {len(zone_1['general_info'])} points")
        print(f"✓ Species: {len(zone_1['species_regulations'])} species")
        for reg in zone_1['species_regulations'][:5]:
            print(f"    {reg['species']}: {reg['season']}")

        print(f"✓ Waterbody Exceptions: {len(zone_1['waterbody_exceptions'])}")
        for exc in zone_1['waterbody_exceptions'][:2]:
            print(f"    {exc['waterbody']}")


if __name__ == '__main__':
    main()
