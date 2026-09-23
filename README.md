# 500 Queens Venture Capital

A public proposal for women developing as CEOs, enterprise leaders and decision makers. Built from Luke Nathan Hayes's current planning document and original enterprise archive.

Live website: https://auraofintelligence.github.io/500-Queens-VC-2026/

## Build and check

Python 3 is sufficient for the static site:

```text
python scripts/build.py
python scripts/check.py
python -m http.server 8768 --bind 127.0.0.1
```

The optional browser check uses Playwright with installed Microsoft Edge. Set `PLAYWRIGHT_MODULE` if Playwright is not installed in the project environment, then run `node scripts/browser-check.cjs` with the preview server running.

## Content and sources

- `data/chapters.json`: public explanatory chapters.
- `data/ventures.json`: 18 connected public project concepts, checked on 23 September 2026.
- `data/enterprise-catalogue.json`: 120 original suggestions, source locations and mentor pairings.
- `data/reference-library.json`: original document metadata and SHA-256 checksums, plus supplied website links.
- `references/documents/`: 27 supplied originals, preserved byte-for-byte.
- `assets/images/provenance.json`: original GenAI artwork prompts and provenance.

The 23 September 2026 planning document guides the public explanation. Historical archives retain their original wording, local links and obsolete references. Named premises, partners, funding, programmes and global relationships are proposals unless explicitly evidenced otherwise. C-Hour recognises community contribution and has no economic equivalent.

The site has no account system, analytics, payment collection or application backend. The starting-note tool downloads a local text file. Its contents are not submitted. Site fonts are bundled locally under their original open font licences.

## Licence

Strange But True Public Source Licence. Non-commercial use with attribution is permitted; commercial rights remain reserved to Luke Nathan Hayes / Strange But True / Aura of Intelligence. See `LICENSE`. Third-party source material keeps its own rights.
