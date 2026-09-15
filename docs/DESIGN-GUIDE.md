# Design guide

What the VIA Systems Lab site looks like and why, as built. This is the
authority on design decisions; change the site and change this page with it.

It grew out of [DESIGN-PLAN.md](DESIGN-PLAN.md), which is the original brief and
is now historical. Where the two disagree, this page wins — §12 lists what
changed and why, so nobody re-derives a decision that has already been made and
reversed.

Related: [README](../README.md) for how to edit the site,
[METADATA.md](METADATA.md) for the structured data.

---

## 1. Character

> An old scientific discipline, carried forward with modern data systems.

Quietly technical, editorial, civic. The identity comes from typography,
precise spacing, and evidence of real research activity — not from effects.
Colour marks actions and signals; it does not decorate surfaces.

The test for any addition: **would a reader trust this page more, or less?**
Anything that makes the site look like a product launch is wrong for it.

---

## 2. Colour

Sampled from the lab emblem: travertine, petrol, terracotta, ink. Every value
is a token at the top of `css/custom.css`. **Never write a colour in a
component rule.**

### Light

| Token | Value | Role | Contrast |
| --- | --- | --- | --- |
| `--page-paper` | `#f7f3eb` | The page surface, as a fixed value | — |
| `--paper` | → `--page-paper` | The *current* surface; re-pointed inside dark bands | — |
| `--field` | `#ede5d7` | Travertine band for alternate sections | — |
| `--ink` | `#1b2a31` | Body text | 13.3:1 on paper |
| `--ink-soft` | `#4a5b63` | Metadata, secondary text | 6.4:1 |
| `--accent-2` | `#22434f` | Petrol used as *ink*: rules, tags | 9.6:1 |
| `--petrol` | `#22434f` | Petrol used as a *surface* | — |
| `--signal` | `#9c4f38` | Terracotta: links, emphasis | 5.3:1 |
| `--signal-strong` | `#7e3e2c` | Hover | 7.3:1 |
| `--rule` | `#c6b9a4` | Hairlines (decorative) | — |

### Inverse bands (hero, page header, footer)

| Token | Value | Contrast on `--inverse-bg` |
| --- | --- | --- |
| `--inverse-bg` | `#22434f` | — |
| `--inverse-text` | `#f1ebe0` | 8.9:1 |
| `--inverse-soft` | `#bccad0` | 6.3:1 |
| `--inverse-signal` | `#eba98f` | 5.4:1 |

Dark mode re-points the same token names under
`@media (prefers-color-scheme: dark)`. Every pair passes AA there too.

### Rules

- **Every text pair meets WCAG AA.** Each token carries its measured ratio in a
  comment. Change a colour, re-check every pair it appears in.
- **`--petrol` and `--accent-2` are the same value in light mode and different
  in dark.** That is deliberate: one is a surface, one is ink. In dark mode a
  near-black surface and readable ink cannot be the same colour. Use the one
  that matches your intent, not the one that happens to look right today.
- **Filled elements name both sides.** A tag with a coloured background gets
  its own `--tag-*-bg` / `--tag-*-fg` pair rather than inheriting a surface
  token, because the surface token flips between schemes and the pairing would
  break silently.
- **The focus ring is `--focus`**, re-pointed inside inverse bands. It is never
  removed.

---

## 3. Surfaces

Two rules, both learned the hard way.

### Section tinting is positional, never per-section

```css
.section:nth-of-type(even) { background: var(--field); }
```

Sections alternate between the page surface and the travertine band according
to **where they sit**, not what they are. `section--about`-style modifiers are
forbidden and the linter rejects them.

The reason: tinting used to be keyed to named sections. When the sections were
reordered, the pattern became arbitrary and the band under the hero silently
changed colour, leaving a mismatched wedge. A colour that belongs to a name has
to be kept in step by hand; a colour that belongs to a position does not.

The hero and the page header are `<section>` elements too, so they count as the
first item and the alternation starts beneath them.

### Panels tint their surface, they do not name it

A panel that sits *inside* a section — the project rail, the "working with the
lab" box — uses:

```css
background: color-mix(in srgb, var(--ink) 5%, transparent);
```

not `var(--paper)` or `var(--field)`. It then reads correctly on whichever
surface it lands on, in either colour scheme, and survives the section being
re-tinted.

---

## 4. Typography

Two families, both variable, both SIL Open Font Licence, both served from this
repository so the page makes no third-party request.

- **Source Serif 4** — `--font-display` — headings and the wordmark.
- **Source Sans 3** — `--font-text` — body, metadata, navigation, labels.
- System monospace — `--font-mono` — repository and code labels only.

### Scale

Fluid, `--step--2` through `--step-5`, each a `clamp()`. **Use a step; never
write a font size.** Body is `--step-0` (1–1.1rem) at line height 1.62.

### Rules

- Uppercase is for short labels only: eyebrows, tags, column titles, the
  wordmark. Never for a sentence.
- `text-wrap: balance` on headings, `pretty` on pull quotes.
- Measure is capped per component (`--measure`, or a `ch` value). Long lines are
  a legibility bug, not a layout preference.
- Numbers in metadata use `font-variant-numeric: lining-nums tabular-nums` so
  columns of grant numbers and dates align.

---

## 5. Layout

**Pure CSS 3.0.0 provides the grid.** `css/custom.css` defines none of its own.

```html
<div class="shell pure-g">
  <div class="prose pure-u-1 pure-u-md-1-2 pure-u-lg-13-24">…</div>
</div>
```

Widths live in the markup, as `pure-u-*` classes, at Pure's own breakpoints:

| Breakpoint | Width | Behaviour |
| --- | --- | --- |
| base | below `48em` | One column. No offsets, no overlap. |
| `md` | `48em`+ | Units take effect. |
| `lg` | `64em`+ | Widest measure. |

The stylesheet adds only the two things Pure deliberately leaves to the page:

1. `.shell` centres the row and caps its measure at `--shell-max` (82rem).
2. `.pure-g > [class*="pure-u"]` gets half a gutter of padding each side.

Because each unit is padded, the row must be one `--col-gap` wider than the
content measure — that is what `--shell-edge` and `--shell-outer` express. There
are **no negative margins** anywhere in the gutter system; a negative
`margin-inline` on `.shell` would override the `auto` that centres it.

### Rules

- **Do not introduce a second grid.** No `grid-template-columns` for page
  composition. Component internals may use Grid or Flexbox freely.
- **A token read by two elements lives in `:root`.** Siblings inherit nothing
  from each other: `--hero-skew` sits at the root precisely because both the
  hero and the section after it need it.
- **Blocks side by side share a top edge.** See §6.

---

## 6. Composition

### Alignment, not stagger

Earlier versions offset alternate rows and stepped the second card down. That
is gone. Research themes are a plain grid — three across, then two, with the
short row centred — and the two project highlights share a top edge.

The rule: **two things side by side are read as a pair, and a staggered top
edge reads as a mistake rather than as composition.** Asymmetry is fine when it
is structural (a wide body beside a narrow rail); it is not fine as decoration.

### The dark bands and the diagonal

The hero and each page header are inverse bands whose lower edge is a shallow
diagonal, deepest on the left, rising to the right.

It is a real cut, not a painted one. The band is a clipped `::before` layer, and
the band's element overlaps the section beneath it by `--hero-skew` /
`--pagehead-skew`, so what shows through the diagonal **is that section**, in
whatever colour it has. There is no second colour to keep in step.

The emblem hangs past the hero's content row into that overlap, crossing the
diagonal. That is the one deliberate piece of dynamism on the site, and it is a
margin on an ordinary Pure unit — it reflows, wraps and zooms like anything
else. The offset is always smaller than the hero's bottom padding, so the
emblem can never reach the section below however the text grows.

### Rhythm

Section padding is `--section-pad`; the section after a band adds the skew back
so its content clears the overlap. Row gaps are `--row-gap`. Hairlines are
`--rule`. That is the whole vocabulary — a component that needs a new spacing
value probably wants an existing one.

---

## 7. Components

| Component | Purpose |
| --- | --- |
| `.masthead` | Seal, wordmark, six-item nav. Sticky from `md`. |
| `.hero` / `.pagehead` | Inverse band opening a page. |
| `.section__head` | Eyebrow (number + label), title, standfirst. |
| `.theme` | One research theme: rule, name, description, methods. |
| `.highlight` | A project in brief, on the homepage. |
| `.project` | A full project record: body plus rail. |
| `.project__rail` | Logo, the three links, then the facts. |
| `.person` | A roster card. `.person--lead` marks the PI by its rule colour, not by size. |
| `.pub` | One output, tagged by kind and funding project. |
| `.tag` | Kind, project or status. Distinguished by **colour and border style**, so it survives greyscale and colour-vision deficiency. |
| `.smallnote` | A one-paragraph aside where a section would be out of proportion. |
| `.footer` | Three matching columns, the marks, the fine print. |

Controls are square-cornered (1px radius). Buttons are uppercase, letterspaced,
and come in four variants: `--primary` / `--ghost` for inverse bands,
`--solid` / `--outline` for light surfaces.

---

## 8. Motion

One reveal, and only where the browser can do it without script:

```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: view()) { … }
}
```

Both guards are required. The `@supports` guard means a browser that cannot run
the animation never sees the zero-opacity start state, so motion can never hide
content. Hover and focus transitions are 120–140ms. Nothing animates that a
reader must wait for.

---

## 9. Imagery

### The lab's own artwork

`img/original/` holds the masters. Everything served from `img/` is generated by
`tools/build_assets.py` — never edit a generated file. WebP with a PNG fallback,
`width`/`height` on every `<img>`, `loading="lazy"` below the fold.

The emblem was generated with a model and refined by hand. That is declared
visibly in the footer, in prose in `humans.txt`, and machine-readably as an IPTC
digital source type. **If you add an image, declare its source type** — see
[METADATA.md §7](METADATA.md).

### Third-party marks

`img/logos/` holds the university lockup, the EU emblem and partner project
logos. They belong to their owners, are reproduced as supplied, and are **not**
covered by the AI provenance statement.

The only permitted adjustment is inverting a **flat monochrome** mark so it
reads against the opposite background — the university lockup on the dark
footer, the project logos on a light page. Both are a single ink on
transparency, so inverting reproduces the other cut exactly. **Never invert a
mark that carries more than one colour**, and never invert the EU emblem, which
keeps its own blue field and 3:2 proportions. See
[`img/logos/README.md`](../img/logos/README.md).

---

## 10. Accessibility

Requirements, not preferences. Several are enforced by `tools/lint.py`.

- One `<h1>` per page; heading levels never skip.
- A skip link to `#main` on every page.
- Landmarks: `header`, `nav`, `main`, `footer`, with section headings.
- Every image has `alt` (empty when decorative) and `width`/`height`.
- Keyboard focus is always visible. Never remove an outline without replacing it.
- External-link markers are drawn shapes with empty `content`, so a screen
  reader does not announce them.
- The page works with CSS disabled and with JavaScript unavailable.
- Test at 320px, at 200% zoom, and with the keyboard alone before shipping a
  layout change.

---

## 11. Things that are deliberately absent

Worth stating, so they are not proposed again as improvements:

- No JavaScript, no framework, no build step for the pages themselves.
- No analytics, no cookies, no third-party request at page load.
- No carousel, no accordion, no modal, no scroll-jacking.
- No decorative photography. The emblem and the partner marks are the images.
- No dashboard, animated chart or invented metric.

---

## 12. What changed since the design plan

| The plan said | The site does | Why |
| --- | --- | --- |
| A custom 15-column CSS Grid, because Pure's 5-column model is too coarse | Pure's own grid, `.pure-g` / `.pure-u-*` | Not reimplementing a grid that ships with the framework. Pure's `md`/`lg` are `48em`/`64em` — exactly the breakpoints the design already used. The 24ths cover the asymmetric splits the plan wanted. |
| Asymmetric, staggered compositions on an odd grid | Aligned grids; no offsets | Staggering read as a mistake rather than as composition. Asymmetry survives where it is structural — a wide body beside a narrow rail. |
| Decide whether to keep the wave motif | Retired | Replaced by one shallow diagonal on the dark bands. No fixed heights, no negative offsets, nothing to clip. |
| A focused one-page site | Three pages | Projects and publications outgrew a section each; the homepage carries highlights and links out. |
| Display serif + text sans, family unspecified | Source Serif 4 + Source Sans 3, self-hosted | Both OFL, variable, designed to pair. Self-hosting removes a third-party request. |
| Palette described in words ("pale cool blue", "restrained vermilion") | Sampled from the emblem | The artwork already was a palette. |
| — | Section tinting is positional | Content-keyed tints broke on reorder. See §3. |
| — | AI provenance declared in four places | Not in scope when the plan was written. |
| JSON-LD as primary RDF, verified facts only | Unchanged | Still right. See [METADATA.md](METADATA.md). |

---

## 13. Before you ship a design change

```sh
python3 tools/lint.py          # structure, links, metadata, CSS tokens
```

Then look at it: 320px, 768px, 1440px; light and dark; 200% zoom; keyboard
only. The linter checks that the rules here are *followed*; it cannot tell you
whether the result is any good.
