#!/usr/bin/env python3
"""Build the public Omada incident/anomaly dictionary from a Settings snapshot.

Input: the JSON an Omada controller returns for Site > Incidents > Settings
(result.data[] with anomalyCode, category, level, params, objectType, and a
per-instance enable flag). Raw snapshots stay OUT of the repo because they
record enable state. This script drops enable and writes:

  omada-incident-dictionary.json   one object per anomalyCode
  omada-incident-dictionary.csv    same rows, flat
  incidents.md                     tables between the GENERATED markers

Names and definitions come from sources/omada-ui-incident-titles.json, extracted
from the controller web UI bundle (Settings-page incident dictionary).

Usage:
  build-omada-incident-dictionary.py --settings incident-settings.json \
      --titles docs/services/omada-log-inventory/sources/omada-ui-incident-titles.json \
      --out docs/services/omada-log-inventory \
      --captured YYYY-MM-DD \
      --controller "Omada Software Controller (version: x.y.z)"

Stdlib only. Captured rows keep the controller's order. Bundle-only types
(present in the UI dictionary but not in this Settings response) are appended
after, marked inControllerList=false.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

# Category number → name. The Settings JSON has no names. The UI bundle
# (ABNORMAL_INCIDENT) lists these nine labels. Each captured type's UI title
# belongs to exactly one official list, and the JSON category number follows
# this order. The bundle does not contain a literal "11: Access" assignment.
CATEGORY_NAMES = {
    11: "Access",
    12: "Authentication",
    13: "Roaming",
    14: "Wireless Network",
    15: "Wired Network",
    16: "Link",
    17: "WAN & Services",
    18: "Device Status",
    19: "Security",
}

# Level number → name. The Settings JSON uses 0–3. The UI bundle labels the
# four incident levels Critical, Error, Warning, Info (INCIDENT_CRITICAL etc.,
# also ABNORMAL_SETTINGS). The mapping itself is from statistic counts (see
# validate_settings).
LEVEL_NAMES = {
    0: "Critical",
    1: "Error",
    2: "Warning",
    3: "Info",
}

STAT_LEVEL = {0: "critical", 1: "error", 2: "warning", 3: "info"}

SITE_PLACEHOLDER_RE = re.compile(r"\{SITE(?:_LOWER)?\}", re.I)


def display_text(s: str) -> str:
    """Replace UI i18n site-word placeholders with the word 'site'."""
    return SITE_PLACEHOLDER_RE.sub("site", s)


def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def format_params(params: dict, definition: str) -> str:
    """Observed param values, with units taken from the UI definition when present."""
    if not params:
        return "—"
    parts = []
    for key, val in params.items():
        unit = unit_for(key, definition)
        if unit:
            parts.append(f"{key}={val} {unit}")
        else:
            parts.append(f"{key}={val}")
    return ", ".join(parts)


KNOWN_UNITS = {"dBm", "dB", "ms", "s", "min", "Mb", "W", "%"}
COUNT_KEYS = {
    "retryCnt", "changedTimes", "offlineCount", "disconnectCount", "avgDisconnectCount",
}
PERCENT_KEYS = {
    "count", "count2g", "count5g", "count5g2", "count6g",
    "disconnectApPercent", "addressPoolRate", "successRate",
    "ratio2g", "ratio5g", "ratio5g2", "ratio6g",
    "util2g", "util5g", "util5g2", "util6g",
}


def unit_for(key: str, definition: str) -> str:
    """Best-effort unit from the UI definition text around %key%."""
    if not definition:
        return ""
    m = re.search(rf"%{re.escape(key)}%(%%)?(?:\s+([A-Za-zµμ]+))?", definition)
    doubled = bool(m and m.group(1))
    word = (m.group(2) if m else "") or ""
    word = word.strip()
    # "%%" in the JS string is a literal percent sign after the value.
    if doubled:
        return "%"
    if word in KNOWN_UNITS:
        return word
    if key in PERCENT_KEYS:
        return "%"
    if key in COUNT_KEYS:
        return "times"
    if key == "timeRange_s":
        return "s"
    if key == "timeRange":
        return "min"
    if key == "threshold":
        if re.search(r"or more times", definition):
            return "times"
        # Word-boundary search: "ms" is also a substring of "roams".
        for unit in ("dBm", "dB", "ms"):
            if re.search(rf"\b{unit}\b", definition):
                return unit
        if re.search(r"%threshold%\s+s\b", definition):
            return "s"
        if "%%" in definition or "%" in definition:
            return "%"
    return ""


def load_titles(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
    out = {}
    for e in entries:
        code = e["anomalyCode"]
        if code in out:
            sys.exit(f"{path}: duplicate anomalyCode {code}")
        out[code] = e
    if not out:
        sys.exit(f"{path}: no titles")
    return out


def validate_settings(raw: dict) -> tuple[list[dict], dict]:
    if raw.get("errorCode") not in (0, None):
        sys.exit(f"settings JSON errorCode={raw.get('errorCode')} {raw.get('msg')}")
    result = raw.get("result") or {}
    rows = result.get("data") or []
    total = result.get("totalRows")
    if total is not None and total != len(rows):
        sys.exit(f"totalRows={total} but data has {len(rows)} rows")
    codes = [r.get("anomalyCode") for r in rows]
    if any(not c for c in codes):
        sys.exit("a row is missing anomalyCode")
    if len(codes) != len(set(codes)):
        sys.exit("duplicate anomalyCode in settings JSON")
    for r in rows:
        if "enable" not in r:
            sys.exit(f"{r.get('anomalyCode')}: missing enable (expected in raw snapshots)")
        for req in ("category", "level", "objectType", "params"):
            if req not in r:
                sys.exit(f"{r.get('anomalyCode')}: missing {req}")
    stat = result.get("statistic") or {}
    from collections import Counter
    levels = Counter(r["level"] for r in rows)
    for num, name in STAT_LEVEL.items():
        expected = stat.get(name)
        if expected is not None and levels.get(num, 0) != expected:
            sys.exit(
                f"level mapping check failed: {levels.get(num, 0)} rows at level {num} "
                f"but statistic.{name}={expected}"
            )
    if stat.get("all") not in (None, len(rows)):
        sys.exit(f"statistic.all={stat.get('all')} but {len(rows)} rows")
    return rows, stat


def replace_generated(path: Path, body: list[str]) -> None:
    start, end = "<!-- GENERATED:START (build-omada-incident-dictionary.py) -->", "<!-- GENERATED:END -->"
    text = path.read_text(encoding="utf-8")
    if start not in text or end not in text:
        sys.exit(f"{path}: missing GENERATED markers")
    pre, rest = text.split(start, 1)
    _, post = rest.split(end, 1)
    path.write_text(pre + start + "\n" + "\n".join(body) + "\n" + end + post, encoding="utf-8")


def captured_entry(row: dict, titles: dict[str, dict]) -> dict:
    code = row["anomalyCode"]
    if code not in titles:
        sys.exit(f"{code}: in the Settings snapshot but not in the UI title list")
    title = titles[code]["title"]
    definition = titles[code]["content"]
    cat = row["category"]
    lvl = row["level"]
    params = row["params"] or {}
    if not isinstance(params, dict):
        sys.exit(f"{code}: params is not an object")
    return {
        "anomalyCode": code,
        "inControllerList": True,
        "category": cat,
        "categoryName": CATEGORY_NAMES.get(cat, ""),
        "categoryNameBasis": "inferred from UI titles plus the Settings category number; see incidents.md",
        "objectType": row["objectType"],
        "level": lvl,
        "levelName": LEVEL_NAMES.get(lvl, ""),
        "levelNameBasis": "inferred from statistic counts; see incidents.md",
        "paramsObserved": params,
        "name": display_text(title),
        "nameVerbatim": title,
        "definition": display_text(definition),
        "definitionVerbatim": definition,
    }


def bundle_only_entry(code: str, title_row: dict) -> dict:
    title = title_row["title"]
    definition = title_row["content"]
    return {
        "anomalyCode": code,
        "inControllerList": False,
        "category": None,
        "categoryName": "",
        "categoryNameBasis": "",
        "objectType": "",
        "level": None,
        "levelName": "",
        "levelNameBasis": "",
        "paramsObserved": {},
        "name": display_text(title),
        "nameVerbatim": title,
        "definition": display_text(definition),
        "definitionVerbatim": definition,
    }


def md_table_captured(rows: list[dict]) -> list[str]:
    out = [
        "| # | anomalyCode | Category | objectType | Level | Observed params | Name (from UI bundle) | Incident definition (from UI bundle) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        cat = r["categoryName"] or str(r["category"])
        if r["categoryName"]:
            cat = f"{r['category']} {r['categoryName']}"
        lvl = r["levelName"] or str(r["level"])
        if r["levelName"]:
            lvl = f"{r['level']} {r['levelName']}"
        params = format_params(r["paramsObserved"], r["definitionVerbatim"])
        out.append(
            f"| {i} | `{r['anomalyCode']}` | {md_escape(cat)} | {md_escape(r['objectType'])} "
            f"| {md_escape(lvl)} | {md_escape(params)} | {md_escape(r['name'])} "
            f"| {md_escape(r['definition'])} |"
        )
    return out


def md_table_bundle_only(rows: list[dict]) -> list[str]:
    out = [
        "| # | anomalyCode | Name (from UI bundle) | Incident definition (from UI bundle) |",
        "|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        out.append(
            f"| {i} | `{r['anomalyCode']}` | {md_escape(r['name'])} | {md_escape(r['definition'])} |"
        )
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--settings", required=True, type=Path)
    ap.add_argument("--titles", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--captured", default="unknown")
    ap.add_argument("--controller", default="Omada Software Controller (version: <fill in>)")
    a = ap.parse_args()

    titles = load_titles(a.titles)
    raw = json.loads(a.settings.read_text(encoding="utf-8"))
    rows, stat = validate_settings(raw)
    captured = [captured_entry(r, titles) for r in rows]
    captured_codes = {r["anomalyCode"] for r in captured}
    bundle_only = [
        bundle_only_entry(code, titles[code])
        for code in titles
        if code not in captured_codes
    ]

    from collections import Counter
    level_counts = Counter(r["level"] for r in captured)
    category_counts = Counter(r["category"] for r in captured)
    counts = {
        "captured": len(captured),
        "bundleTitles": len(titles),
        "bundleOnly": len(bundle_only),
        "byLevel": {LEVEL_NAMES[k]: level_counts[k] for k in sorted(level_counts)},
        "byCategory": {
            f"{k} {CATEGORY_NAMES.get(k, '?')}": category_counts[k]
            for k in sorted(category_counts)
        },
        "statistic": {
            "all": stat.get("all"),
            "critical": stat.get("critical"),
            "error": stat.get("error"),
            "warning": stat.get("warning"),
            "info": stat.get("info"),
        },
    }

    meta = {
        "name": "Omada incident/anomaly dictionary",
        "captured": a.captured,
        "controller": a.controller,
        "method": (
            "Site Incidents > Settings JSON, read-only. Per-instance enable flags removed. "
            "Names and definitions from the Omada controller web UI bundle "
            "(Settings-page incident dictionary; version per README)."
        ),
        "levelMapping": {
            "map": {str(k): v for k, v in LEVEL_NAMES.items()},
            "basis": (
                "Inference: the Settings JSON statistic counts for critical/error/warning/info "
                "match the number of rows at level 0/1/2/3. Labels are from the UI bundle "
                "(INCIDENT_CRITICAL, INCIDENT_ERROR, INCIDENT_WARNING, INCIDENT_INFO and "
                "ABNORMAL_SETTINGS)."
            ),
        },
        "categoryMapping": {
            "map": {str(k): v for k, v in CATEGORY_NAMES.items()},
            "basis": (
                "Inference: the Settings JSON numbers categories 11–19 with no names. "
                "The UI bundle (ABNORMAL_INCIDENT) lists these nine labels. Each captured "
                "type's UI title belongs to exactly one of those categories, and the JSON "
                "category number follows this order. The bundle has no literal 11: Access assignment."
            ),
        },
        "paramsObserved": (
            "Parameter values as returned in the Settings snapshot. These are observed "
            "values (typically the controller defaults), not a record of a site's policy. "
            "Units are taken from the UI definition text."
        ),
        "counts": counts,
    }

    all_entries = captured + bundle_only
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "omada-incident-dictionary.json").write_text(
        json.dumps({"meta": meta, "entries": all_entries}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    cols = [
        "anomalyCode", "inControllerList", "category", "categoryName", "objectType",
        "level", "levelName", "paramsObserved", "name", "definition",
    ]
    with (a.out / "omada-incident-dictionary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in all_entries:
            w.writerow({
                "anomalyCode": r["anomalyCode"],
                "inControllerList": r["inControllerList"],
                "category": "" if r["category"] is None else r["category"],
                "categoryName": r["categoryName"],
                "objectType": r["objectType"],
                "level": "" if r["level"] is None else r["level"],
                "levelName": r["levelName"],
                "paramsObserved": json.dumps(r["paramsObserved"], ensure_ascii=False, separators=(",", ":")),
                "name": r["name"],
                "definition": r["definition"],
            })

    body = [
        f"**{len(captured)} types** were in this controller's Incidents > Settings list. "
        f"The UI bundle lists **{len(titles)}** types; **{len(bundle_only)}** of those were not on this controller.",
        "",
        "Category names and level names are labeled as inferred (see above). "
        "Parameter values are observed values from the Settings response, not a record of anyone's enable/threshold policy. "
        "`{SITE}` / `{SITE_LOWER}` in the UI strings are placeholders for the word “site” and are rendered as `site` here.",
        "",
        "### Types on this controller",
        "",
    ] + md_table_captured(captured) + [
        "",
        "### Types in the UI bundle, not on this controller's list",
        "",
        "These codes appear in the same Settings-page dictionary in the UI bundle, but they were not in this controller's Settings response. "
        "No category, level, objectType or params were captured for them. They may exist on other controller types, versions or licenses.",
        "",
    ] + md_table_bundle_only(bundle_only)

    replace_generated(a.out / "incidents.md", body)
    print(json.dumps(counts, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
