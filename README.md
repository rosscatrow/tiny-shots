# tiny-shots

A tiny photo gallery for lo-fi Kodak Charmera photos. Photos are displayed at sticker size — the whole point is they're small.

Live at [shots.catrow.net](https://shots.catrow.net)

## Adding photos

Drop JPEGs into `photos/`, then update the `photos` array near the top of `index.html`:

```js
const photos = [
  { file: "IMG_0001.jpg", caption: "optional caption" },
  { file: "IMG_0002.jpg" },
];
```

## Tech

Single-file site. No build step, no dependencies, no framework. Just an HTML file with inline CSS and JS.

Shot on Kodak Charmera · 1.6MP · 2026
