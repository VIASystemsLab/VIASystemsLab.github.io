#!/usr/bin/env python3
"""Static checks for the VIA Systems Lab website.

The site has no build step and no test suite, so this script is the only thing
standing between a typo and a broken public page. It uses the standard library
only, so it runs from a git hook without anything installed.

    python3 tools/lint.py            # structure, links, metadata, CSS
    python3 tools/lint.py --external # also resolve every outbound URL (slow)

Exit code is 0 when every check passes and 1 otherwise. Warnings never fail the
run; they are printed so that a human can judge them.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html import unescape
from urllib.parse import urldefrag, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Every .html file at the root is part of the published site and is linted.
EXCLUDED_PAGES: set[str] = set()

SITE_ORIGIN = "https://viasystemslab.github.io"

# Namespaces are identified by an http: IRI by definition and must not be
# "fixed" to https:, which would change the identifier.
ALLOWED_HTTP_PREFIXES = (
    "http://purl.org/",
    "http://xmlns.com/",
    "http://www.w3.org/",
    "http://iptc.org/",
    "http://cv.iptc.org/",
)

# An @id pointing into a controlled vocabulary is supposed to leave the page
# graph: the term is defined by whoever publishes the vocabulary, not by us.
CONTROLLED_VOCABULARIES = (
    "http://cv.iptc.org/newscodes/",
    "http://purl.org/dc/",
    "https://schema.org/",
)

errors: list[str] = []
warnings: list[str] = []


def fail(page: str, msg: str) -> None:
    errors.append(f"{page}: {msg}")


def warn(page: str, msg: str) -> None:
    warnings.append(f"{page}: {msg}")


def strip_comments(html: str) -> str:
    """Remove HTML comments so that markup templates inside them are not linted."""
    return re.sub(r"<!--.*?-->", "", html, flags=re.S)


def visible_text(html: str) -> str:
    """The words a reader sees: tags dropped, entities decoded, spaces collapsed.

    Tags are dropped before entities are decoded. The other order would turn an
    escaped `&lt;p&gt;` in the copy into a tag and then strip the text away.
    """
    return " ".join(unescape(re.sub(r"<[^>]+>", " ", html)).split())


def element_text(html: str, element_id: str) -> str | None:
    """The visible text of the element carrying `element_id`, or None if absent.

    The end of the element is found by counting opening and closing tags of its
    own name, which is enough for hand-written markup that nests properly.
    """
    start = re.search(rf'<(\w+)[^>]*\sid="{re.escape(element_id)}"[^>]*>', html)
    if not start:
        return None
    tag = start.group(1)
    depth = 0
    for token in re.finditer(rf"<(/?){tag}\b[^>]*>", html[start.start() :]):
        if token.group(1):
            depth -= 1
            if depth == 0:
                return visible_text(html[start.start() : start.start() + token.end()])
        elif not token.group(0).endswith("/>"):
            depth += 1
    return visible_text(html[start.start() :])


def pages() -> list[str]:
    found = [
        f
        for f in sorted(os.listdir(ROOT))
        if f.endswith(".html") and f not in EXCLUDED_PAGES
    ]
    if not found:
        fail("repository", "no HTML pages found")
    return found


def page_ids(name: str) -> set[str]:
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return set(re.findall(r'\sid="([^"]+)"', strip_comments(fh.read())))


# --------------------------------------------------------------------------
# Per-page checks
# --------------------------------------------------------------------------


def check_head(name: str, html: str) -> None:
    if not re.search(r'<html lang="[a-z]{2}(-[A-Z]{2})?"', html):
        fail(name, "<html> is missing a lang attribute")
    if '<meta name="viewport"' not in html:
        fail(name, "missing viewport meta")
    if not re.search(r"<title>.+</title>", html):
        fail(name, "missing or empty <title>")
    if not re.search(r'<meta name="description" content=".{20,}?">', html):
        fail(name, "missing or too-short meta description")

    expected = f"{SITE_ORIGIN}/" if name == "index.html" else f"{SITE_ORIGIN}/{name}"
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canonical:
        fail(name, "missing canonical link")
    elif canonical.group(1) != expected:
        fail(name, f"canonical is {canonical.group(1)}, expected {expected}")

    og_url = re.search(r'<meta property="og:url" content="([^"]+)"', html)
    if og_url and canonical and og_url.group(1) != canonical.group(1):
        fail(name, "og:url does not match the canonical URL")

    for sheet in (
        "css/fonts.css",
        "css/pure.css",
        "css/grids-responsive.css",
        "css/custom.css",
    ):
        if f'href="{sheet}"' not in html:
            fail(name, f"does not link {sheet}")

    if 'rel="author" type="text/plain" href="humans.txt"' not in html:
        fail(name, "does not link humans.txt (see https://humanstxt.org)")

    # The site declares AI provenance in its structured data; the same claim has
    # to be legible to a person, or the declaration is only for machines. This
    # checks the words, not a class name, so the footer can be restyled freely.
    visible = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    for needle, what in (
        ("ChatGPT", "the tool that generated the artwork"),
        ("Claude", "the tool that drafted the code"),
        ("humans.txt", "a link to the full statement"),
    ):
        if needle not in visible:
            fail(name, f"the visible provenance note does not name {what} ({needle!r})")


def check_structure(name: str, html: str) -> None:
    ids = re.findall(r'\sid="([^"]+)"', html)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        fail(name, f"duplicate id attributes: {', '.join(dupes)}")

    idset = set(ids)
    for attr in ("aria-labelledby", "aria-describedby"):
        for match in re.findall(rf'{attr}="([^"]+)"', html):
            for target in match.split():
                if target not in idset:
                    fail(name, f"{attr} points at missing id #{target}")

    heads = [
        (int(m.group(1)), " ".join(re.sub(r"<[^>]+>", "", m.group(2)).split()))
        for m in re.finditer(r"<h([1-6])[^>]*>(.*?)</h\1>", html, re.S)
    ]
    h1s = [t for level, t in heads if level == 1]
    if len(h1s) != 1:
        fail(name, f"expected exactly one h1, found {len(h1s)}")
    previous = 0
    for level, text in heads:
        if previous and level > previous + 1:
            fail(name, f"heading level jumps h{previous} to h{level} at {text!r}")
        previous = level

    if 'href="#main"' not in html:
        fail(name, "missing skip link to #main")
    if 'id="main"' not in idset and "main" not in idset:
        fail(name, "missing an element with id=main")

    # Surface colours are positional, not per-section. A modifier like
    # section--about ties a background to a named piece of content, which is
    # what made the band under the hero change colour when the sections were
    # reordered. See the note above .section:nth-of-type in css/custom.css.
    for modifier in sorted(set(re.findall(r"\bsection--[a-z-]+\b", html))):
        fail(
            name,
            f"{modifier} keys a surface to a named section; the band rhythm is "
            "positional (.section:nth-of-type) — drop the modifier",
        )

    for tag in re.findall(r"<img\b[^>]*>", html):
        src = re.search(r'src="([^"]+)"', tag)
        where = src.group(1) if src else tag[:40]
        if "alt=" not in tag:
            fail(name, f"<img> without alt: {where}")
        if "width=" not in tag or "height=" not in tag:
            fail(name, f"<img> without width/height (causes layout shift): {where}")


def local_targets(html: str) -> set[str]:
    """Collect local file references from href/src/srcset only.

    meta content is deliberately excluded: it holds prose and keywords, not paths.
    """
    found: set[str] = set()
    for attr in ("href", "src"):
        for value in re.findall(rf'\b{attr}="([^"]+)"', html):
            found.add(value)
    for value in re.findall(r'\bsrcset="([^"]+)"', html):
        for candidate in value.split(","):
            token = candidate.strip().split(" ")[0]
            if token:
                found.add(token)
    return found


def check_links(name: str, html: str, all_ids: dict[str, set[str]]) -> None:
    for target in sorted(local_targets(html)):
        if target.startswith(("http://", "https://", "mailto:", "data:", "tel:")):
            continue
        path, fragment = urldefrag(target)
        if not path:
            if fragment and fragment not in all_ids[name]:
                fail(name, f"dangling in-page anchor #{fragment}")
            continue
        if not os.path.exists(os.path.join(ROOT, path)):
            fail(name, f"link target does not exist: {path}")
            continue
        if fragment and path.endswith(".html"):
            if path in all_ids and fragment not in all_ids[path]:
                fail(name, f"link {path}#{fragment} points at an id that {path} lacks")

    for url in re.findall(r'href="(http://[^"]+)"', html):
        if not url.startswith(ALLOWED_HTTP_PREFIXES):
            fail(name, f"insecure http link: {url}")


def check_jsonld(name: str, html_with_comments: str, site_ids: set[str]) -> None:
    blocks = re.findall(
        r'<script type="application/ld\+json">(.*?)</script>',
        html_with_comments,
        re.S,
    )
    if not blocks:
        fail(name, "no JSON-LD block")
        return
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError as exc:
            fail(name, f"JSON-LD does not parse: {exc}")
            continue

        graph = data.get("@graph")
        if not isinstance(graph, list):
            fail(name, "JSON-LD has no @graph array")
            continue

        defined = [node.get("@id") for node in graph]
        if None in defined:
            fail(name, "every node in @graph needs a stable @id")
        dupes = sorted({i for i in defined if i and defined.count(i) > 1})
        if dupes:
            fail(name, f"duplicate @id in @graph: {', '.join(dupes)}")

        refs: set[str] = set()

        def collect(node: object) -> None:
            if isinstance(node, dict):
                if set(node) == {"@id"}:
                    refs.add(node["@id"])
                else:
                    for value in node.values():
                        collect(value)
            elif isinstance(node, list):
                for item in node:
                    collect(item)

        collect(graph)
        for ref in sorted(refs):
            if ref in defined or ref in site_ids:
                continue
            if ref.startswith(CONTROLLED_VOCABULARIES):
                continue
            if urlparse(ref).scheme in ("http", "https"):
                warn(name, f"@id reference resolved outside the page graph: {ref}")
            else:
                fail(name, f"@id reference is neither defined nor a URL: {ref}")

        # A claim in structured data that the page does not show is a claim a
        # reader cannot check. Identity claims — an ORCID iD, an email address —
        # must be visible; a DOI or a grant number is only warned about, since
        # those are commonly reached through the link rather than printed.
        visible = strip_comments(html_with_comments)
        visible = re.sub(
            r'<script type="application/ld\+json">.*?</script>', "", visible, flags=re.S
        )

        literals: set[str] = set()

        def collect_literals(node: object) -> None:
            if isinstance(node, dict):
                # A bare {"@id": ...} is a reference to something described
                # elsewhere, not a claim made by this page. Pointing at a
                # person does not oblige the page to print their ORCID.
                if set(node) == {"@id"}:
                    return
                for value in node.values():
                    collect_literals(value)
            elif isinstance(node, list):
                for item in node:
                    collect_literals(item)
            elif isinstance(node, str):
                literals.add(node)

        collect_literals(graph)

        orcid = re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b")
        email = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
        doi = re.compile(r"\b10\.\d{4,9}/\S+\b")

        for literal in sorted(literals):
            for pattern, kind, hard in (
                (orcid, "ORCID iD", True),
                (email, "email address", True),
                (doi, "DOI", False),
            ):
                found = pattern.search(literal)
                if not found:
                    continue
                if found.group(0) in visible:
                    continue
                message = (
                    f"JSON-LD asserts the {kind} {found.group(0)} but the page "
                    "never shows it, so a reader cannot check it"
                )
                (fail if hard else warn)(name, message)
                break

        # A DefinedTerm's description *is* the term's definition, and the page
        # prints it in full. Unlike a project abstract, which condenses a longer
        # CORDIS record, there is nothing here to summarise, so a paraphrase is
        # only ever two descriptions of one term where a reader can check one.
        #
        # The text is compared against the block the term's @id fragment points
        # at, never against the page as a whole: a page-wide search accepts any
        # paragraph anywhere, so two terms whose definitions had been swapped
        # would both pass it.
        #
        # Scoped to DefinedTerm on purpose. The organisation and the projects
        # legitimately carry a condensed description, so the same rule applied
        # to every `description` would be wrong.
        for node in graph:
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if "DefinedTerm" not in types:
                continue
            described = node.get("description")
            if not described:
                continue
            fragment = urldefrag(node.get("@id") or "").fragment
            block = element_text(visible, fragment) if fragment else None
            if block is None:
                fail(
                    name,
                    f"DefinedTerm {node.get('@id')} carries a description but "
                    "the page has no element with that fragment as its id, so "
                    "there is nothing to check the definition against",
                )
                continue
            if " ".join(described.split()) not in block:
                fail(
                    name,
                    f"DefinedTerm {node.get('@id')} is described in words the "
                    "page does not print under it; a term's description is its "
                    "visible text, copied verbatim",
                )


# --------------------------------------------------------------------------
# Repository-wide checks
# --------------------------------------------------------------------------


def collect_site_ids(names: list[str]) -> set[str]:
    """Every @id defined anywhere in the site, so cross-page references resolve."""
    found: set[str] = set()
    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            html = fh.read()
        for block in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S
        ):
            try:
                graph = json.loads(block).get("@graph", [])
            except json.JSONDecodeError:
                continue
            for node in graph:
                if isinstance(node, dict) and node.get("@id"):
                    found.add(node["@id"])
    return found


def check_css() -> None:
    path = os.path.join(ROOT, "css", "custom.css")
    with open(path, encoding="utf-8") as fh:
        css = fh.read()

    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    if stripped.count("{") != stripped.count("}"):
        fail("css/custom.css", f"unbalanced braces: {stripped.count('{')} open, {stripped.count('}')} close")

    declared = set(re.findall(r"(?:^|[;{])\s*(--[a-zA-Z0-9-]+)\s*:", stripped, re.M))
    used = set(re.findall(r"var\(\s*(--[a-zA-Z0-9-]+)", stripped))
    # var(--x, fallback) is a deliberate option: a component exposes a knob a
    # caller may override and otherwise supplies its own value. Only a var()
    # with no fallback has to resolve to a declaration.
    required = set(re.findall(r"var\(\s*(--[a-zA-Z0-9-]+)\s*\)", stripped))
    undefined = sorted(required - declared)
    if undefined:
        fail("css/custom.css", f"var() references undeclared custom properties: {', '.join(undefined)}")

    unused = sorted(declared - used)
    if unused:
        warn("css/custom.css", f"declared but never used: {', '.join(unused)}")

    # Blocks that sit side by side share a top edge. Offsetting alternate items
    # with :nth-child reads as a mistake rather than as composition.
    # See docs/DESIGN-GUIDE.md §7.
    for selector, body in re.findall(r"([^{}]*:nth-child[^{}]*)\{([^}]*)\}", stripped):
        if re.search(r"margin-(top|block-start)\s*:", body):
            fail(
                "css/custom.css",
                f"{' '.join(selector.split())} offsets items with a top margin; "
                "blocks side by side share a top edge (docs/DESIGN-GUIDE.md \u00a77)",
            )

    for sheet in ("css/custom.css", "css/fonts.css"):
        with open(os.path.join(ROOT, sheet), encoding="utf-8") as fh:
            body = fh.read()
        # A data URI is a document of its own, and a url() inside one points
        # within that document, not at a file here. Drop them before looking
        # for targets to resolve.
        body = re.sub(r'url\(\s*"data:[^"]*"\s*\)', "", body)
        body = re.sub(r"url\(\s*'data:[^']*'\s*\)", "", body)
        body = re.sub(r"url\(\s*data:[^)]*\)", "", body)
        for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", body):
            if url.startswith(("data:", "http", "#")):
                continue
            target = os.path.normpath(os.path.join(ROOT, os.path.dirname(sheet), url))
            if not os.path.exists(target):
                fail(sheet, f"url() target does not exist: {url}")


BUZZWORDS = (
    "leverage", "cutting-edge", "cutting edge", "seamless", "seamlessly",
    "revolutionise", "revolutionize", "unlock the power", "game-changing",
    "best-in-class", "state-of-the-art solution", "synergy", "paradigm shift",
)


# Presentation belongs in the stylesheet. An attribute that paints, sizes or
# positions something cannot be restyled, cannot respond to a media query or a
# colour scheme, and is invisible to anyone reading the CSS to find out how a
# thing looks. Geometry is not presentation: a path's `d`, a circle's `cx`, a
# `viewBox` and `preserveAspectRatio` describe *what the shape is*, and stay in
# the markup.
SVG_PRESENTATION = (
    "fill", "fill-opacity", "fill-rule", "stroke", "stroke-width",
    "stroke-opacity", "stroke-linecap", "stroke-linejoin", "stroke-dasharray",
    "opacity", "stop-color", "stop-opacity", "color", "font-family",
    "font-size", "font-weight", "text-anchor", "dominant-baseline",
    "letter-spacing",
)

# Presentational HTML attributes. All were removed from the language; browsers
# still honour them, which is what makes them worth failing on.
HTML_PRESENTATION = (
    "align", "valign", "bgcolor", "background", "border", "cellpadding",
    "cellspacing", "hspace", "vspace", "nowrap", "face", "bordercolor",
)


def check_markup_presentation(names: list[str]) -> None:
    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            page = fh.read()
        body = re.sub(r"<!--.*?-->", "", page, flags=re.S)

        for match in re.finditer(r"\sstyle\s*=", body, re.I):
            fail(name, f"inline style attribute at line {body[:match.start()].count(chr(10)) + 1}; "
                       "move the declarations into css/custom.css")

        if re.search(r"<style[\s>]", body, re.I):
            fail(name, "embedded <style> element; the site has one stylesheet")

        # Scan inside tags only, with quoted values blanked out first. An
        # attribute is a name at a whitespace boundary, so this catches the
        # unquoted form (align=center) and the boolean form (nowrap) as well
        # as the quoted one, and does not fire on the word "align" in a
        # sentence or on a class named align-left.
        for match in re.finditer(r"<[a-zA-Z][^>]*>", body):
            tag = re.sub(r"=\s*\"[^\"]*\"", '=""', match.group(0))
            tag = re.sub(r"=\s*'[^']*'", "=''", tag)
            line = body[:match.start()].count(chr(10)) + 1
            for attr in SVG_PRESENTATION + HTML_PRESENTATION:
                if re.search(rf"\s{re.escape(attr)}\s*(?==|\s|/?>)", tag, re.I):
                    fail(name, f"presentation attribute {attr} at line {line}; "
                               "give the element a class and style it in "
                               "css/custom.css")


def check_language(names: list[str]) -> None:
    """The mechanical half of the language rules in docs/DESIGN-GUIDE.md.

    Only what a script can judge: em dashes, and a short list of words that
    have no place in a research lab's copy. Everything else in that section
    needs a person.
    """
    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            raw = fh.read()
        visible = strip_comments(raw)
        visible = re.sub(r"<script.*?</script>", "", visible, flags=re.S)

        dashes = len(re.findall(r"&mdash;|\u2014", visible))
        if dashes:
            fail(
                name,
                f"{dashes} em dash(es) in published copy; use a comma, a colon, "
                "parentheses or two sentences (docs/DESIGN-GUIDE.md \u00a72)",
            )

        lowered = re.sub(r"<[^>]+>", " ", visible).lower()
        for word in BUZZWORDS:
            if word in lowered:
                fail(name, f"buzzword in published copy: {word!r}")


def check_publications() -> None:
    """Every listed publication must carry a resolving DOI.

    The page lists peer-reviewed publications only. A title without an
    identifier is exactly the entry that gets copied into a reference manager
    and never corrected, so the absence of a DOI fails the build. Whether the
    DOI points at the right paper is a human's job.
    """
    path = os.path.join(ROOT, "publications.html")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        html = strip_comments(fh.read())

    for entry in re.findall(r'<li class="pub\b.*?</li>', html, re.S):
        title = re.search(r"<h4[^>]*>(.*?)</h4>", entry, re.S)
        label = " ".join(re.sub(r"<[^>]+>", " ", title.group(1)).split()) if title else "?"
        if "doi.org/" not in entry:
            fail("publications.html", f"publication entry without a DOI: {label!r}")
        for marker in ("is-pending", "is-forthcoming"):
            if marker in entry:
                fail(
                    "publications.html",
                    f"entry {label!r} is marked {marker}; the page lists "
                    "peer-reviewed publications with a DOI only",
                )


def check_humans() -> None:
    """humans.txt, per https://humanstxt.org, plus this site's own additions."""
    path = os.path.join(ROOT, "humans.txt")
    if not os.path.exists(path):
        fail("humans.txt", "missing (see https://humanstxt.org)")
        return
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    for section in ("/* TEAM */", "/* THANKS */", "/* SITE */", "/* GENERATIVE TOOLS */"):
        if section not in text:
            fail("humans.txt", f"missing the {section} section")


def check_generated_assets(names: list[str]) -> None:
    """Every generated image should be reachable from a page or a stylesheet.

    An orphan is not broken, but it is dead weight in the repository and a sign
    that a reference was renamed or removed without the build being updated.
    Matching is a plain substring search rather than attribute parsing, because
    some of these are referenced from meta content and from CSS url().
    """
    haystack = ""
    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            haystack += fh.read()
    for sheet in ("css/custom.css", "css/fonts.css"):
        with open(os.path.join(ROOT, sheet), encoding="utf-8") as fh:
            haystack += fh.read()
    with open(os.path.join(ROOT, "site.webmanifest"), encoding="utf-8") as fh:
        haystack += fh.read()

    generated = os.path.join(ROOT, "img")
    for filename in sorted(os.listdir(generated)):
        if os.path.isdir(os.path.join(generated, filename)):
            continue  # img/original and img/logos hold sources, not output
        if filename not in haystack:
            warn(
                "img",
                f"{filename} is generated but nothing references it; "
                "drop it from tools/build_assets.py or start using it",
            )


def _relative_luminance(hex_colour: str) -> float:
    def channel(value: int) -> float:
        v = value / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast(a: str, b: str) -> float:
    high, low = sorted((_relative_luminance(a), _relative_luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def check_contrast_comments() -> None:
    """Each colour token documents its contrast ratio. Verify the arithmetic.

    A stale ratio is worse than none: it is exactly the number someone will
    quote in an accessibility statement without re-deriving it. The comment
    says which background the pair is measured against, so this reads that
    rather than guessing.
    """
    with open(os.path.join(ROOT, "css", "custom.css"), encoding="utf-8") as fh:
        css = fh.read()

    # The site may ship one scheme or two; only check the ones that exist.
    marker = "@media (prefers-color-scheme: dark)"
    root_start = css.index(":root {")
    if marker in css:
        dark_at = css.index(marker)
        blocks = {"light": css[root_start:dark_at], "dark": css[dark_at:dark_at + 2000]}
    else:
        blocks = {"light": css[root_start:]}

    for scheme, block in blocks.items():
        def value(token: str) -> str | None:
            found = re.search(rf"{re.escape(token)}:\s*(#[0-9a-f]{{6}})", block)
            return found.group(1) if found else None

        for token, colour, comment in re.findall(
            r"(--[a-z0-9-]+):\s*(#[0-9a-f]{6});\s*/\*(.*?)\*/", block
        ):
            claimed = re.search(r"([0-9]+\.[0-9])\s*:\s*1", comment)
            if not claimed:
                continue
            background = value("--inverse-bg") if "--inverse-bg" in comment else value("--page-paper")
            if not background:
                continue
            actual = contrast(colour, background)
            if abs(actual - float(claimed.group(1))) >= 0.06:
                fail(
                    "css/custom.css",
                    f"{scheme} {token} is documented at {claimed.group(1)}:1 on "
                    f"{background} but measures {actual:.2f}:1",
                )
            elif actual < 4.5:
                fail(
                    "css/custom.css",
                    f"{scheme} {token} is {actual:.2f}:1 on {background}, below WCAG AA",
                )


def check_design_guide() -> None:
    """Every colour the design guide quotes must be the one the CSS declares.

    Documentation drifts from code silently, and a palette table that is subtly
    wrong is worse than no table: someone will copy a value out of it. Only the
    hex values are checked, because they are the part that is mechanically
    checkable — the prose still needs a human.
    """
    guide_path = os.path.join(ROOT, "docs", "DESIGN-GUIDE.md")
    if not os.path.exists(guide_path):
        fail("docs/DESIGN-GUIDE.md", "missing")
        return
    with open(guide_path, encoding="utf-8") as fh:
        guide = fh.read()
    with open(os.path.join(ROOT, "css", "custom.css"), encoding="utf-8") as fh:
        css = fh.read()

    # Only the light-scheme block: that is what the guide's table documents.
    marker = "@media (prefers-color-scheme: dark)"
    start = css.index(":root {")
    root = css[start:css.index(marker)] if marker in css else css[start:]

    # Every token the table names has to exist, including the ones whose value
    # is derived from another and so has no hex of its own.
    for token in re.findall(r"\| `(--[a-z0-9-]+)` \|", guide):
        if not re.search(rf"{re.escape(token)}:", root):
            fail("docs/DESIGN-GUIDE.md", f"documents {token}, which css/custom.css does not declare")

    # Where the table gives a hex, it has to be the hex the stylesheet gives.
    for token, quoted in re.findall(r"\| `(--[a-z0-9-]+)` \| `(#[0-9a-f]{6})` \|", guide):
        declared = re.search(rf"{re.escape(token)}:\s*(#[0-9a-f]{{6}})", root)
        if not declared:
            continue
        if declared.group(1) != quoted:
            fail(
                "docs/DESIGN-GUIDE.md",
                f"says {token} is {quoted} but css/custom.css declares {declared.group(1)}",
            )


def check_sitemap(names: list[str]) -> None:
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        fail("sitemap.xml", "missing")
        return
    with open(path, encoding="utf-8") as fh:
        listed = set(re.findall(r"<loc>([^<]+)</loc>", fh.read()))
    expected = {
        f"{SITE_ORIGIN}/" if n == "index.html" else f"{SITE_ORIGIN}/{n}" for n in names
    }
    for missing in sorted(expected - listed):
        fail("sitemap.xml", f"does not list {missing} (run: python3 tools/build_assets.py --sitemap)")
    for extra in sorted(listed - expected):
        fail("sitemap.xml", f"lists {extra}, which is not a page in this repository")


def check_external(names: list[str]) -> None:
    import urllib.error
    import urllib.request

    urls: set[str] = set()
    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            html = strip_comments(fh.read())
        urls |= set(re.findall(r'href="(https?://[^"]+)"', html))

    for url in sorted(urls):
        # This site's own URLs are checked against the working tree by
        # check_links. Asking the network about them only reports whether the
        # last deploy has happened yet, which is not a defect in the source.
        if url.startswith(SITE_ORIGIN):
            continue

        clean = url.replace("&amp;", "&")

        def request(method: str) -> int:
            req = urllib.request.Request(
                clean,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (compatible; via-systems-lab-linkcheck/1.0; "
                        "+https://viasystemslab.github.io/)"
                    )
                },
                method=method,
            )
            with urllib.request.urlopen(req, timeout=25) as response:
                return response.status

        try:
            code = request("HEAD")
            # Plenty of servers refuse HEAD but serve the page perfectly well.
            if code >= 400:
                code = request("GET")
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 405, 501, 503):
                try:
                    code = request("GET")
                except Exception:
                    code = exc.code
            else:
                code = exc.code
        except Exception as exc:  # network trouble is not a content defect
            warn("external", f"{url} could not be checked: {exc}")
            continue

        # 403, 429 and 503 mean "this server will not answer a script", not
        # "this link is broken" — several university and publisher sites refuse
        # any non-browser request. Report them, but do not fail a build over a
        # link that works perfectly well for a reader.
        if code in (403, 429, 503):
            warn("external", f"{url} refused an automated request (HTTP {code}); check it by hand")
        elif code >= 400:
            fail("external", f"{url} returned HTTP {code}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--external",
        action="store_true",
        help="also resolve every outbound URL (needs network access)",
    )
    args = parser.parse_args()

    names = pages()
    all_ids = {name: page_ids(name) for name in names}
    site_ids = collect_site_ids(names)

    for name in names:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            raw = fh.read()
        html = strip_comments(raw)
        check_head(name, html)
        check_structure(name, html)
        check_links(name, html, all_ids)
        check_jsonld(name, raw, site_ids)

    check_css()
    check_markup_presentation(names)
    check_language(names)
    check_publications()
    check_humans()
    check_contrast_comments()
    check_design_guide()
    check_generated_assets(names)
    check_sitemap(names)
    if args.external:
        check_external(names)

    print(f"checked {len(names)} page(s): {', '.join(names)}")
    for message in warnings:
        print(f"  warning  {message}")
    for message in errors:
        print(f"  ERROR    {message}")
    if errors:
        print(f"\n{len(errors)} error(s)")
        return 1
    print(f"\nno errors ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
