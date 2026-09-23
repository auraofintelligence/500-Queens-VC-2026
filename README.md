# 500 Queens Venture Capital

A public proposal for women developing as CEOs, enterprise leaders and decision makers. Built from Luke Nathan Hayes's current planning document and original enterprise archive.

Live website: https://auraofintelligence.github.io/500-Queens-VC-2026/

The public edition connects 24 individual AI Queen profiles, 11 enterprise category guides and all 120 original startup suggestions across 172 pages. It includes original GenAI artwork, the original brand mark, a women-led equality design brief, a private planning pathway, source downloads, search and an illustrative funding calculator. Published in review batches from 23 September 2026.

## Build and check

Python 3 is sufficient for the static site:

```text
python scripts/build.py
python scripts/check.py
python scripts/check-network.py
python -m http.server 8768 --bind 127.0.0.1
```

The optional browser check uses Playwright with installed Microsoft Edge. Set `PLAYWRIGHT_MODULE` if Playwright is not installed in the project environment, then run `node scripts/browser-check.cjs` with the preview server running.

`node scripts/check-network-browser.cjs` checks the expanded network, saving, exports and layouts. `node scripts/verify-interactions.cjs` checks all main pages on phone and desktop, plus search, calculator, menu and local note-download behaviour. `python scripts/check-live.py` verifies the deployed pages, artwork and original reference download checksums over the public internet.

## Content and sources

- `data/chapters.json`: public explanatory chapters.
- `data/ventures.json`: 18 connected public project concepts, checked on 23 September 2026.
- `data/enterprise-catalogue.json`: 120 original suggestions, source locations and mentor pairings.
- `data/queens.json`: 24 individual fictional mentor profiles, session guides and representations.
- `data/enterprise-details-*.json` and `data/category-details-*.json`: developed concept briefs and category guides.
- `data/network.json`: generated Queen, category and enterprise connections.
- `data/reference-library.json`: original document metadata and SHA-256 checksums, plus supplied website links.
- `references/documents/`: 27 supplied originals, preserved byte-for-byte.
- `assets/images/provenance.json`: original GenAI artwork prompts and provenance.

The 23 September 2026 planning document guides the public explanation. Historical archives retain their original wording, local links and obsolete references. Named premises, partners, funding, programmes and global relationships are proposals unless explicitly evidenced otherwise. C-Hour recognises community contribution and has no economic equivalent.

The site has no account system, analytics, payment collection or application backend. The pathway and equality brief save in the visitor's browser and can be downloaded as Markdown. They are not submitted or publicly shared. The starting-note tool downloads a local text file. The Queens are fictional mentor concepts with written session guides; a live AI conversation service is not connected. Site fonts are bundled locally under their original open font licences.

## Licence

Strange But True Public Source Licence. Non-commercial use with attribution is permitted; commercial rights remain reserved to Luke Nathan Hayes / Strange But True / Aura of Intelligence. See `LICENSE`. Third-party source material keeps its own rights.
