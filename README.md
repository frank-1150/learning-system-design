# DDIA System Design Learning

A Chinese learning site for Martin Kleppmann's *Designing Data-Intensive Applications* (First Edition):

- 12 interactive chapter walkthroughs
- 36 system design interview questions
- Product design, infrastructure mechanism, and production incident practice
- Local-only learning progress stored under `ddia-progress:v1`

## Development

```bash
npm install
npm run content:generate
npm run docs:dev
npm run docs:build
```

The site is served at `http://localhost:5173/learning-system-design/` in development and is published through GitHub Actions Pages.

## Private source material

The source book and split PDFs are intentionally excluded from Git. Place the source at:

```text
private/books/ddia/original.pdf
```

Then run:

```bash
python3 scripts/split_ddia.py
```

The script validates all 613 physical PDF pages and writes 14 private segments plus `data/ddia-chapters.json`.

## Copyright

Site code and original implementation are available under the MIT License. Original learning notes and interview exercises remain attributed to this repository's author. Quoted concepts and referenced figures from *Designing Data-Intensive Applications* remain the property of Martin Kleppmann and O'Reilly Media; the source PDF is not distributed.

