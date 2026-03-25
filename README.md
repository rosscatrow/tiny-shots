# tiny-shots

A tiny photo gallery for lo-fi Kodak Charmera photos. Photos are displayed at sticker size — the whole point is they're small.

Live at [shots.catrow.net](https://shots.catrow.net)

## Adding photos

Drop JPEGs into `photos/`, then add entries to `photos.json`:

```json
{ "file": "img_0001.jpeg", "title": "caption here", "roll": "roll-001" }
```

Rolls are defined in `rolls.json`. The gallery reads both files at runtime and renders cards with filterable roll tabs.

## Tech

Zero-dependency static site. No build step, no framework, no bundler. Classic Mac OS aesthetic with inline CSS and JS.

- `index.html` — public gallery
- `photos.json` / `rolls.json` — photo and roll metadata
- `admin.html` / `manage.html` / `upload.html` — admin tools
- `favicon.svg` / `favicon.ico` — pixel-art camera icon

Shot on Kodak Charmera · 1.6MP · 2026
