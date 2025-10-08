# SRD → Rules Corpus Converter

Drop your 5-page SRD-style Markdown into `srd.md` and run:

```bash
python tools/srd_to_rules.py --input srd.md --out shadowdark_tui/rules --map config/rulemap.json
```

What this does:

- Splits the SRD by `##` (H2) and `###` (H3) headings.
- Generates stable rule IDs based on a prefix and an incrementing counter per category.
- Writes each rule as Markdown with YAML front-matter into the appropriate folder (`mechanics/`, `conditions/`, etc.).
- Builds a `manifest.json` that maps IDs → files → headings for traceability.
- Optional: `config/rulemap.json` to steer category, phase, priority, and tags by heading regex.

You can safely iterate on the SRD and re-run; unchanged sections keep their IDs if the headings match.
