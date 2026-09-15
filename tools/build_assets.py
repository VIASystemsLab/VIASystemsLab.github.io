#!/usr/bin/env python3
"""Regenerate the site's derived assets from their sources.

Nothing in `img/` (except `img/original/` and `img/logos/`), nothing in
`icons/` (except `favicon.svg`) and no line of `sitemap.xml` is written by hand. This script
produces all of it, so the committed artifacts can always be reconstructed.

    python3 tools/build_assets.py            # regenerate everything
    python3 tools/build_assets.py --sitemap  # just the sitemap
    python3 tools/build_assets.py --check    # verify the artifacts are current

`--check` is what CI runs. It does not compare image bytes, because two
versions of an encoder legitimately produce different bytes for the same
picture. Instead it compares a hash of each *source* against `assets.lock.json`
and confirms every derivative listed there still exists. That catches the real
mistake — editing artwork and forgetting to rebuild — without failing a build
because someone has a newer libwebp.

Requires `cwebp` and `rsvg-convert` on PATH, plus ImageMagick or, on macOS,
the built-in `sips`. See README.md for how to install them.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINALS = os.path.join(ROOT, "img", "original")
LOGOS = os.path.join(ROOT, "img", "logos")
LOCKFILE = os.path.join(ROOT, "assets.lock.json")

SITE_ORIGIN = "https://viasystemslab.github.io"

# Pages that are part of the published site, with their sitemap settings.
# via.html is the superseded first draft and is deliberately absent.
SITEMAP_PAGES = [
    ("index.html", "1.0", "monthly"),
    ("projects.html", "0.8", "monthly"),
    ("publications.html", "0.8", "weekly"),
]

# Brand colours, kept in step with the tokens at the top of css/custom.css.
TRAVERTINE = "#efe8dc"
PETROL = "#22434f"
TERRACOTTA = "#9c4f38"


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            f"command failed: {' '.join(cmd)}\n{result.stdout}\n{result.stderr}"
        )


def require(*tools: str) -> None:
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        raise SystemExit(
            f"missing required tool(s): {', '.join(missing)}. See README.md."
        )


def resize(source: str, longest_side: int, target: str) -> None:
    """Fit an image inside a square of `longest_side`, preserving aspect ratio."""
    if shutil.which("magick"):
        run(["magick", source, "-resize", f"{longest_side}x{longest_side}", target])
    elif shutil.which("convert"):
        run(["convert", source, "-resize", f"{longest_side}x{longest_side}", target])
    elif shutil.which("sips"):
        run(["sips", "-Z", str(longest_side), source, "--out", target])
    else:
        raise SystemExit("need ImageMagick (magick/convert) or macOS sips to resize")


def to_webp(source: str, target: str, quality: int, alpha_quality: int = 90) -> None:
    run(
        [
            "cwebp", "-quiet",
            "-q", str(quality),
            "-alpha_q", str(alpha_quality),
            "-m", "6",
            source, "-o", target,
        ]
    )


def sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def svg_to_png(svg_path: str, width: int, height: int, target: str) -> None:
    run(["rsvg-convert", "-w", str(width), "-h", str(height), svg_path, "-o", target])


def data_uri(path: str) -> str:
    with open(path, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode("ascii")


# --------------------------------------------------------------------------
# Builders. Each returns the list of files it produced, relative to ROOT.
# --------------------------------------------------------------------------


def build_images(tmp: str) -> list[str]:
    require("cwebp")
    produced: list[str] = []
    out = os.path.join(ROOT, "img")

    # The emblem carries the hero. It is the one image big enough to be worth
    # three widths, and it is served as WebP with a single PNG fallback.
    pictorial = os.path.join(ORIGINALS, "via-logo-pictorial.png")
    for width in (480, 720, 1080):
        staged = os.path.join(tmp, f"pictorial-{width}.png")
        resize(pictorial, width, staged)
        target = os.path.join(out, f"via-logo-pictorial-{width}.webp")
        to_webp(staged, target, quality=80)
        produced.append(os.path.relpath(target, ROOT))
    fallback = os.path.join(out, "via-logo-pictorial-480.png")
    resize(pictorial, 480, fallback)
    produced.append(os.path.relpath(fallback, ROOT))

    # The plaque only ever appears on the footer band, which is dark in both
    # colour schemes, so only the white cut is served. The black original is
    # still needed — build_og_card draws the social card from it.
    for width in (280, 560):
        source = os.path.join(ORIGINALS, "via-logo-horizontal-w.png")
        png = os.path.join(out, f"via-logo-horizontal-w-{width}.png")
        resize(source, width, png)
        webp = os.path.join(out, f"via-logo-horizontal-w-{width}.webp")
        to_webp(png, webp, quality=90)
        produced += [os.path.relpath(png, ROOT), os.path.relpath(webp, ROOT)]

    # The seal sits in the masthead, whose surface does follow the colour
    # scheme, so that one does need both cuts.
    for variant in ("b", "w"):
        source = os.path.join(ORIGINALS, f"via-logo-circle-{variant}.png")
        png = os.path.join(out, f"via-logo-circle-{variant}-240.png")
        resize(source, 240, png)
        webp = os.path.join(out, f"via-logo-circle-{variant}-240.webp")
        to_webp(png, webp, quality=90)
        produced += [os.path.relpath(png, ROOT), os.path.relpath(webp, ROOT)]

    return produced


# Third-party marks: the university lockup, the EU emblem and the ARMADA logo.
# Reproduced as supplied, only resized. See img/logos/README.md.
#   (source file, output stem, widths)
PARTNER_LOGOS = [
    ("uvrdlls.png", "univr-dlls", (480, 960)),
    ("euflag.png", "eu-flag", (192,)),
    ("armada-logo-w-h.png", "armada-logo-w", (280, 560)),
    # The DataGEMS source is only 387px wide, so it is not upscaled past that.
    ("datagems-logo-w.png", "datagems-logo-w", (280, 387)),
]


def build_partner_logos(tmp: str) -> list[str]:
    require("cwebp")
    produced: list[str] = []
    out = os.path.join(ROOT, "img")
    for filename, stem, widths in PARTNER_LOGOS:
        source = os.path.join(LOGOS, filename)
        for width in widths:
            png = os.path.join(out, f"{stem}-{width}.png")
            resize(source, width, png)
            webp = os.path.join(out, f"{stem}-{width}.webp")
            # Quality 92: these are someone else's trademarks, and a visible
            # compression artefact in a partner's logo is not ours to create.
            to_webp(png, webp, quality=92, alpha_quality=95)
            produced += [os.path.relpath(png, ROOT), os.path.relpath(webp, ROOT)]
    return produced


def build_og_card(tmp: str) -> list[str]:
    """The 1200x630 card social platforms show when the site is shared.

    It is a PNG on purpose: several scrapers still refuse WebP, and a link that
    unfurls with no picture looks broken.
    """
    require("rsvg-convert")
    plaque = data_uri(os.path.join(ORIGINALS, "via-logo-horizontal-b.png"))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="{TRAVERTINE}"/>
  <rect x="26" y="26" width="1148" height="578" fill="none" stroke="{PETROL}" stroke-width="3"/>
  <rect x="38" y="38" width="1124" height="554" fill="none" stroke="{PETROL}" stroke-width="1" stroke-opacity=".55"/>
  <image x="270" y="78" width="660" height="371" xlink:href="{plaque}"/>
  <rect x="510" y="497" width="180" height="3" fill="{TERRACOTTA}"/>
  <circle cx="562" cy="498.5" r="8" fill="{PETROL}"/>
  <circle cx="600" cy="489" r="9" fill="{TERRACOTTA}"/>
  <circle cx="638" cy="498.5" r="8" fill="{PETROL}"/>
</svg>
"""
    staged = os.path.join(tmp, "og.svg")
    with open(staged, "w", encoding="utf-8") as fh:
        fh.write(svg)
    target = os.path.join(ROOT, "img", "og-card.png")
    svg_to_png(staged, 1200, 630, target)
    return [os.path.relpath(target, ROOT)]


def build_icons(tmp: str) -> list[str]:
    """Two icon families, because they are read at very different sizes.

    The favicon is a drawn V with the emblem's node-and-link rule under it: the
    full seal turns to mud at 16px. The app icons use the real seal, which is
    legible from 180px up.
    """
    require("rsvg-convert")
    produced: list[str] = []
    icons = os.path.join(ROOT, "icons")

    favicon = os.path.join(icons, "favicon.svg")
    for size in (16, 32):
        target = os.path.join(icons, f"favicon-{size}.png")
        svg_to_png(favicon, size, size, target)
        produced.append(os.path.relpath(target, ROOT))

    seal = data_uri(os.path.join(ORIGINALS, "via-logo-circle-b.png"))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 512 512">
  <rect width="512" height="512" fill="{TRAVERTINE}"/>
  <image x="36" y="36" width="440" height="440" xlink:href="{seal}"/>
</svg>
"""
    staged = os.path.join(tmp, "seal.svg")
    with open(staged, "w", encoding="utf-8") as fh:
        fh.write(svg)
    for size, filename in ((512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")):
        target = os.path.join(icons, filename)
        svg_to_png(staged, size, size, target)
        produced.append(os.path.relpath(target, ROOT))

    return produced


def build_sitemap() -> list[str]:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name, priority, frequency in SITEMAP_PAGES:
        if not os.path.exists(os.path.join(ROOT, name)):
            raise SystemExit(f"sitemap lists {name}, which does not exist")
        loc = f"{SITE_ORIGIN}/" if name == "index.html" else f"{SITE_ORIGIN}/{name}"
        lastmod = newest_content_date(name)
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{frequency}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    target = os.path.join(ROOT, "sitemap.xml")
    with open(target, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return ["sitemap.xml"]


def newest_content_date(name: str) -> str:
    """Last commit date for a page, falling back to today for uncommitted files."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", name],
        cwd=ROOT, capture_output=True, text=True,
    )
    stamp = result.stdout.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
        return stamp
    import datetime

    return datetime.date.today().isoformat()


# --------------------------------------------------------------------------


def source_hashes() -> dict[str, str]:
    sources = {}
    for name in sorted(os.listdir(ORIGINALS)):
        if name.endswith(".png"):
            sources[f"img/original/{name}"] = sha256(os.path.join(ORIGINALS, name))
    for filename, _, _ in PARTNER_LOGOS:
        sources[f"img/logos/{filename}"] = sha256(os.path.join(LOGOS, filename))
    sources["icons/favicon.svg"] = sha256(os.path.join(ROOT, "icons", "favicon.svg"))
    return sources


def check() -> int:
    if not os.path.exists(LOCKFILE):
        print("assets.lock.json is missing; run: python3 tools/build_assets.py")
        return 1
    with open(LOCKFILE, encoding="utf-8") as fh:
        lock = json.load(fh)

    problems: list[str] = []
    current = source_hashes()
    for path, digest in current.items():
        if lock["sources"].get(path) != digest:
            problems.append(f"{path} changed since the artifacts were built")
    for path in lock["sources"]:
        if path not in current:
            problems.append(f"{path} is recorded in the lock file but no longer exists")
    for path in lock["artifacts"]:
        if not os.path.exists(os.path.join(ROOT, path)):
            problems.append(f"{path} is missing")

    if problems:
        for problem in problems:
            print(f"  ERROR  {problem}")
        print("\nrun: python3 tools/build_assets.py")
        return 1
    print(
        f"artifacts are current: {len(lock['artifacts'])} files "
        f"from {len(lock['sources'])} sources"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    parser.add_argument("--images", action="store_true", help="only image derivatives")
    parser.add_argument("--icons", action="store_true", help="only favicons and app icons")
    parser.add_argument("--sitemap", action="store_true", help="only the sitemap")
    args = parser.parse_args()

    if args.check:
        return check()

    everything = not (args.images or args.icons or args.sitemap)
    artifacts: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        if everything or args.images:
            artifacts += build_images(tmp)
            artifacts += build_partner_logos(tmp)
            artifacts += build_og_card(tmp)
        if everything or args.icons:
            artifacts += build_icons(tmp)
        if everything or args.sitemap:
            artifacts += build_sitemap()

    if everything:
        with open(LOCKFILE, "w", encoding="utf-8") as fh:
            json.dump(
                {"sources": source_hashes(), "artifacts": sorted(artifacts)},
                fh,
                indent=2,
            )
            fh.write("\n")
        artifacts.append("assets.lock.json")

    for path in sorted(artifacts):
        size = os.path.getsize(os.path.join(ROOT, path))
        print(f"  {path:48s} {size / 1024:8.1f} KB")
    print(f"\nwrote {len(artifacts)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
