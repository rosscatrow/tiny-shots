#!/usr/bin/env python3
"""
generate-feed.py

Builds feed.xml from rolls.json + photos.json.

- one <item> per roll
- password-protected rolls are excluded (their photos are gated)
- newest rolls first
- pubDate derived from the roll's id timestamp when available (roll-<unix_ms>),
  otherwise parsed from the `date` field ("YYYY", "YYYY-MM", "YYYY-MM-DD")
- description includes an inline thumbnail grid + photo titles linking to /photo.html

Usage: python3 scripts/generate-feed.py
Run from the repo root.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

SITE_URL = "https://shots.catrow.net"
SITE_TITLE = "tiny shots"
SITE_DESCRIPTION = "photos best viewed small \u00b7 shot on kodak charmera"
SITE_LANG = "en"

REPO_ROOT = Path(__file__).resolve().parent.parent
ROLLS_PATH = REPO_ROOT / "rolls.json"
PHOTOS_PATH = REPO_ROOT / "photos.json"
FEED_PATH = REPO_ROOT / "feed.xml"


def roll_datetime(roll: dict) -> datetime:
    """Best-effort roll timestamp for ordering + pubDate."""
    # IDs like "roll-1774405502282" encode unix milliseconds.
    m = re.match(r"^roll-(\d{10,})$", roll.get("id", ""))
    if m:
        try:
            ms = int(m.group(1))
            return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            pass

    # Fallback: parse `date` as YYYY, YYYY-MM, or YYYY-MM-DD.
    date_str = (roll.get("date") or "").strip()
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
        try:
            return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue

    # Last resort: epoch 0 so malformed rolls sink to the bottom.
    return datetime.fromtimestamp(0, tz=timezone.utc)


def build_item_description(roll: dict, photos: list[dict]) -> str:
    """HTML shown inside <description> — a thumbnail grid + titled links."""
    count = len(photos)
    if count == 0:
        return "<p>no shots on this roll yet.</p>"

    noun = "shot" if count == 1 else "shots"
    parts: list[str] = [f"<p>{count} {noun}</p>"]

    # Thumbnail grid (readers that render HTML will show the images).
    thumbs = []
    for p in photos:
        photo_url = (
            f"{SITE_URL}/photo.html"
            f"?file={xml_escape(p['file'])}&amp;roll={xml_escape(roll['id'])}"
        )
        img_url = f"{SITE_URL}/photos/{xml_escape(p['file'])}"
        alt = xml_escape(p.get("title", "") or p["file"])
        thumbs.append(
            f'<a href="{photo_url}">'
            f'<img src="{img_url}" alt="{alt}" '
            f'style="width:120px;height:120px;object-fit:cover;'
            f'border:2px solid #000;margin:2px;" />'
            f"</a>"
        )
    parts.append(
        '<p style="line-height:0;">' + "".join(thumbs) + "</p>"
    )

    # Titled list for text-only readers.
    list_items = []
    for p in photos:
        photo_url = (
            f"{SITE_URL}/photo.html"
            f"?file={xml_escape(p['file'])}&amp;roll={xml_escape(roll['id'])}"
        )
        title = xml_escape(p.get("title", "") or p["file"])
        list_items.append(f"<li><a href=\"{photo_url}\">{title}</a></li>")
    parts.append("<ul>" + "".join(list_items) + "</ul>")

    return "\n".join(parts)


def build_feed(rolls: list[dict], photos: list[dict]) -> str:
    photos_by_roll: dict[str, list[dict]] = {}
    for p in photos:
        photos_by_roll.setdefault(p["roll"], []).append(p)

    # Skip password-protected rolls entirely — their content is gated.
    public_rolls = [r for r in rolls if not r.get("password")]

    # Newest first.
    public_rolls.sort(key=roll_datetime, reverse=True)

    now = datetime.now(tz=timezone.utc)
    last_build = format_datetime(now)

    lines: list[str] = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        '<rss version="2.0" '
        'xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/">'
    )
    lines.append("  <channel>")
    lines.append(f"    <title>{xml_escape(SITE_TITLE)}</title>")
    lines.append(f"    <link>{SITE_URL}/</link>")
    lines.append(f"    <description>{xml_escape(SITE_DESCRIPTION)}</description>")
    lines.append(f"    <language>{SITE_LANG}</language>")
    lines.append(
        f'    <atom:link href="{SITE_URL}/feed.xml" '
        'rel="self" type="application/rss+xml" />'
    )
    lines.append(f"    <lastBuildDate>{last_build}</lastBuildDate>")
    lines.append(
        f"    <generator>tiny-shots feed generator</generator>"
    )

    for roll in public_rolls:
        roll_photos = photos_by_roll.get(roll["id"], [])
        pub = format_datetime(roll_datetime(roll))
        name = roll.get("name") or roll["id"]
        link = f"{SITE_URL}/#{roll['id']}"
        guid = roll["id"]
        desc = build_item_description(roll, roll_photos)

        lines.append("    <item>")
        lines.append(f"      <title>{xml_escape(name)}</title>")
        lines.append(f"      <link>{link}</link>")
        lines.append(
            f'      <guid isPermaLink="false">{xml_escape(guid)}</guid>'
        )
        lines.append(f"      <pubDate>{pub}</pubDate>")
        lines.append(f"      <description><![CDATA[{desc}]]></description>")
        lines.append("    </item>")

    lines.append("  </channel>")
    lines.append("</rss>")
    lines.append("")  # trailing newline

    return "\n".join(lines)


def main() -> int:
    try:
        rolls = json.loads(ROLLS_PATH.read_text())
        photos = json.loads(PHOTOS_PATH.read_text())
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"error: invalid json: {e}", file=sys.stderr)
        return 1

    feed = build_feed(rolls, photos)
    FEED_PATH.write_text(feed)

    public_count = sum(1 for r in rolls if not r.get("password"))
    skipped = len(rolls) - public_count
    msg = f"wrote {FEED_PATH.relative_to(REPO_ROOT)} with {public_count} item(s)"
    if skipped:
        msg += f" ({skipped} password-protected roll(s) skipped)"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
