#!/usr/bin/env python3
import argparse, re, json, hashlib
from pathlib import Path
from typing import Dict, Any, List

HEADING_RE = re.compile(r'^(#{2,3})\s+(.*)$')  # H2 or H3
FRONTMATTER = """---
id: {id}
tags: {tags}
version: {version}
source: "{source}"
kind: {kind}
applies_to: {applies_to}
phase: {phase}
priority: {priority}
---

{body}
"""

def slugify(text: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9]+', '-', text.strip().lower()).strip('-')
    return s or "rule"

def pick_bucket(head: str, cfg_rules: List[Dict[str, Any]], defaults: Dict[str, Any]):
    for r in cfg_rules:
        if re.search(r["match"], head):
            return {
                "category": r.get("category", defaults["category"]),
                "phase": r.get("phase", defaults["phase"]),
                "priority": r.get("priority", defaults["priority"]),
                "tags": r.get("tags", defaults["tags"]),
                "id_hint": r.get("id_hint", None)
            }
    return {
        "category": defaults["category"],
        "phase": defaults["phase"],
        "priority": defaults["priority"],
        "tags": defaults["tags"],
        "id_hint": None
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="SRD markdown file")
    ap.add_argument("--out", required=True, help="rules output dir (folder with category subdirs)")
    ap.add_argument("--map", required=False, default=None, help="config json to map headings -> categories/tags/phase/priority")
    ap.add_argument("--applies", default='["attack", "check", "save"]', help="applies_to array (json) for defaults")
    ap.add_argument("--id-prefix", default=None, help="override prefix from config")
    args = ap.parse_args()

    src = Path(args.input).read_text(encoding="utf-8")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = {"defaults": {"prefix": "SD", "source": "SRD", "version": 1, "phase": "roll", "priority": 100, "category": "mechanics", "tags": []}, "rules": []}
    if args.map:
        cfg = json.loads(Path(args.map).read_text(encoding="utf-8"))

    defaults = cfg["defaults"]
    if args.id_prefix:
        defaults["prefix"] = args.id_prefix

    applies_to = json.loads(args.applies)

    # Split into sections by H2/H3
    lines = src.splitlines()
    sections = []
    current = {"head": None, "level": None, "body": []}
    for line in lines:
        m = HEADING_RE.match(line)
        if m:
            if current["head"]:
                sections.append(current)
            current = {"head": m.group(2).strip(), "level": len(m.group(1)), "body": []}
        else:
            current["body"].append(line)
    if current["head"]:
        sections.append(current)

    # Counters per id_hint/category
    counters = {}
    manifest = {"generated": [], "source": str(Path(args.input).resolve())}

    for sec in sections:
        head = sec["head"]
        body = "\n".join(sec["body"]).strip()
        bucket = pick_bucket(head, cfg.get("rules", []), defaults)
        category = bucket["category"]
        id_hint = bucket["id_hint"] or slugify(head).upper()[:6]
        key = f"{category}:{id_hint}"
        counters[key] = counters.get(key, 0) + 1
        num = counters[key]
        rule_id = f'{defaults["prefix"]}-{id_hint}-{num:03d}'.upper()

        # Path and kind
        cat_dir = out_dir / category
        cat_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{rule_id}.md"
        path = cat_dir / filename
        kind = "mechanic" if category == "mechanics" else "condition" if category == "conditions" else "rule"

        fm = FRONTMATTER.format(
            id=rule_id,
            tags=json.dumps(bucket["tags"]),
            version=defaults["version"],
            source=defaults["source"],
            kind=kind,
            applies_to=json.dumps(applies_to),
            phase=bucket["phase"],
            priority=bucket["priority"],
            body=body if body else f"**{head}**\\n(Details to be filled.)"
        )
        path.write_text(fm, encoding="utf-8")
        manifest["generated"].append({"id": rule_id, "file": str(path), "heading": head, "category": category})

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(manifest['generated'])} rules. Manifest at {out_dir/'manifest.json'}")

if __name__ == "__main__":
    main()
