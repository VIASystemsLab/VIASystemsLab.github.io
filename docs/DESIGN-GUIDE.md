# Design guide

What the VIA Systems Lab site looks like and why, as built. This is the
authority on design decisions; change the site and change this page with it.

[DESIGN-PLAN.md](DESIGN-PLAN.md) is the original brief and is kept as a
historical document. Where the two disagree, this page wins. §13 states the
decisions most often reopened, so nobody re-derives one that is already made.

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

## 2. Language

The site's voice is the same as its design: precise, unhurried, and short of
anything that sounds like it is selling. These rules govern copy written *for*
the site. They do not license rewriting text the lab authored, or text quoted
from a source. The AI statement, a project abstract taken from CORDIS, a paper
title: those are someone else's words, and they stay as written even where they
break the rules below.

### No em dashes unless the sentence needs one and no alternative exists

Try a comma, a colon, parentheses, or two sentences first. One of them almost
always works, and reads faster. The bar is not "a dash reads well here", it is
"nothing else will do". An em dash invites a clause the sentence did not need.

> Outputs are grouped by kind — vision, journal, conference — and each one
> carries the project that funded it.

becomes

> Outputs are grouped by kind (vision, journal, conference), and each one
> carries the project that funded it.

### Name the specific thing

Prefer the technical term to the general one. "A large language model", "a
coding agent", "a generative image tool" rather than "AI". The general word is
acceptable only where the breadth is the point, or where it is the term the
source itself uses, which is why the lab's statement uses it and the pages
around it mostly do not.

The same applies everywhere else: "Horizon Europe grant 101168951" beats
"EU funding", and "the ARMADA repository" beats "our code".

### The lab is a group, not a person

The VIA Systems Lab is several researchers with shared goals. It has no mind of
its own: it does not believe, think, care about, want or ask. An opinion, a
decision or a piece of work belongs to the people who had it or did it, and the
copy names them. A reader is here to work out whether to join the lab or work
with it, and a lab written as a single actor reads as one person's project.

The test is to give the lab exactly one member. If the sentence still reads
correctly, it is describing a person rather than a group.

> The lab believes an answer is only useful if it can be checked.

becomes

> Researchers in the lab argue that an answer is only useful if it can be
> checked.

A possessive with one owner does the same thing more quietly. "The lab's view"
is somebody's view: say whose, or name the people who hold it.

### "We" is the lab, all of it

"We" is the site's voice and is right far more often than not. The
open-science pledge is written in it, because a commitment every member makes
is exactly what the word is for. It goes wrong in two ways.

It is the wrong word when it excludes people the same page counts as members:

> We work with doctoral candidates, postdoctoral researchers and collaborators
> in Verona and beyond.

becomes

> The lab brings together doctoral candidates, postdoctoral researchers and
> scientists in Verona, and works with collaborators beyond it.

It is also the wrong word when the claim belongs to more people than the lab. A
paper with fifteen authors from eight institutions is not something "we
published"; it is a paper by members of the lab and their co-authors. Claim
membership of the work, not ownership of it, and let the author list say the
rest.

### No buzzwords, no marketing register

No "leverage", "cutting-edge", "seamless", "powerful", "unlock",
"revolutionise". If a sentence would be at home in a product launch, it is
wrong for a research lab. The test in §1 applies to prose as much as to
colour: would a reader trust this page more, or less?

### Favour the source

Link the authority rather than restating it. Quote a figure only where it is
published, and link the record it came from. Between paraphrasing a CORDIS
entry and linking it, link it. This is the same rule the metadata follows: see
[METADATA.md](METADATA.md) on publishing nothing that has not been checked
against its own identifier.

### Say it once

If a fact belongs in two places, put it where a reader will look for it and
link from the other. Duplicated prose is how one copy goes stale while the
other does not. It is why the homepage carries project highlights and not full
records, and why the design guide links the metadata guide instead of
summarising it.

### Be brief

Cut any sentence that exists only to soften another. No preamble, no restating
the heading, no summary of what was just said.

### Inclusive terminology

Follow the ACM's *Words Matter* guidance:
<https://www.acm.org/diversity-inclusion/words-matter>. Prefer the neutral term
where one exists — allowlist and blocklist, primary and replica, a placeholder
name rather than "dummy" — and prefer they/them where a person's pronouns are
not known.

## 3. Colour

Sampled from the lab emblem: travertine, oxblood brick and ink, with the
node-graph’s teal raised to an instrument cyan and used only as a signal.
Every value
is a token at the top of `css/custom.css`. **Never write a colour in a
component rule.**

### Light

| Token | Value | Role | Contrast |
| --- | --- | --- | --- |
| `--page-paper` | `#f6f1e8` | The page surface, as a fixed value | — |
| `--paper` | → `--page-paper` | The *current* surface; re-pointed inside dark bands | — |
| `--field` | `#ebe1d2` | Travertine band for alternate sections | — |
| `--ink` | `#2a1d19` | Body text | 14.5:1 on paper |
| `--ink-soft` | `#4a3831` | Metadata, secondary text | 9.8:1 |
| `--accent-2` | `#085059` | Instrument cyan used as *ink*: section titles, rules, tags | 8.1:1 on paper, 7.1:1 on travertine |
| `--petrol` | `#4a2118` | Oxblood used as a *surface* | — |
| `--signal` | `#8c3a2b` | Brick: links, emphasis | 6.8:1 |
| `--signal-strong` | `#6e2c20` | Hover | 9.1:1 |
| `--rule` | `#d2c3ae` | Hairlines (decorative) | — |

### Inverse bands (hero, page header, footer)

| Token | Value | Contrast on `--inverse-bg` |
| --- | --- | --- |
| `--inverse-bg` | `#4a2118`, an alias of `--petrol` | — |
| `--inverse-text` | `#f4eadf` | 11.6:1 |
| `--inverse-soft` | `#d7b9ab` | 7.5:1 |
| `--inverse-signal` | `#5fd4e3` | 7.9:1 |
| `--graph-ink` | derived: half `--inverse-signal` in `--inverse-soft`, which lands on #9bc6c7 | decorative, never text |

### There is one scheme

The site does **not** follow `prefers-color-scheme`. The palette is designed
and reviewed on a travertine page, and a scheme nobody has reviewed is worse
than none: it ships a second design that no one signed off.

If a dark scheme is wanted, derive it, review it on real pages, and only then
add the media query. `img/original/` holds the white cuts of the seal and the
plaque for that case.

### Rules

- **Every text pair meets WCAG AA.** Each token carries its measured ratio in a
  comment, and `tools/lint.py` recomputes those ratios from the hex values on
  every run — a stale figure fails the build.
- **`--petrol` is a surface, `--accent-2` is ink.** Different hues as well as
  different roles: the oxblood grounds the dark bands, the instrument cyan
  marks rules and tags. Use the one that matches your intent.
- **The cyan is the whole technical register.** `#085059` is the emblem's own
  teal at 91% saturation instead of 68%: the chroma of an indicator lamp
  rather than a patina, with the brightness pulled down from 47% to 35% so it
  can carry a heading at 8.1:1. It makes the "technology" reading almost
  single handed, which is also why it stays confined to section titles, rules
  and small tags. Spread across a surface it would read as a dashboard.
- **Filled elements name both sides.** A tag with a coloured background gets
  its own `--tag-*-bg` / `--tag-*-fg` pair rather than inheriting a surface
  token. `--paper` is re-pointed to the band colour inside the dark bands, so a
  filled element that took its foreground from it would pair that background
  against the wrong ink, silently. Where you mean the real page colour
  regardless of context, name `--page-paper`.
- **The focus ring is `--focus`**, re-pointed inside inverse bands. It is never
  removed.

---

## 4. Surfaces

Two rules.

### Section tinting is positional, never per-section

```css
.section:nth-of-type(even) { background: var(--field); }
```

Sections alternate between the page surface and the travertine band according
to **where they sit**, not what they are. `section--about`-style modifiers are
forbidden and the linter rejects them.

The reason: a tint keyed to a named section belongs to the content rather than
to the place. Reorder the sections and the pattern turns arbitrary, the band
under the hero changes colour with nothing announcing it, and a mismatched
wedge is left sitting on the section below. A colour that belongs to a name has
to be kept in step by hand; a colour that belongs to a position does not.

The hero and the page header are `<section>` elements too, so they count as the
first item and the alternation starts beneath them.

### Panels never name their own surface

A panel that sits *inside* a section takes its background from the section's
position, never from a surface token written into the panel's own rule. Two
treatments do that. The choice between them is how much the panel has to
separate from the page.

**Tint what it lands on.** The project rail:

```css
background: color-mix(in srgb, var(--ink) 5%, transparent);
```

A subordinate column inside a record only has to lift off the page. The tint
reads correctly on either surface, and there is nothing to keep in step.

**Swap to the opposite surface.** The "working with the lab" box, and every
other `.note`:

```css
.note { background: var(--note-bg); }

.section:nth-of-type(even) {
  background: var(--field);
  --note-bg: var(--page-paper);
}
```

`--note-bg` is travertine at the root and paper inside a tinted section, so a
note always lands on the surface its section is not. A block set aside from the
argument of its section has to read as a distinct panel, and a 5% wash lands on
both surfaces as the same small darkening, which reads as a box on neither.

What both avoid is `var(--paper)` or `var(--field)` in the component rule
itself. That is the version that breaks: the surface would be decided by the
panel rather than by where the panel sits, so a reorder would have to be
followed by hand. The declaration above sits inside the positional selector, so
it does not.

---

## 5. Typography

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
- Measure is capped per component: `--measure` for prose, `--measure-lead`
  (68ch) for the standfirst under a section heading, or a local `ch` value.
  **The cap is deliberately narrower than the column it sits in.** A standfirst
  block spans 17/24 of the shell, but its text stops around 56% — filling the
  column would give a ~95-character line. Long lines are a legibility bug, not
  a layout preference.
- Numbers in metadata use `font-variant-numeric: lining-nums tabular-nums` so
  columns of grant numbers and dates align.

---

## 6. Layout

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
- **Blocks side by side share a top edge.** See §7.
- **Never keep two things apart with two independent scales.** If a gap is
  maintained by one value growing on one curve and another growing on a
  different one, the gap is only correct at the width you happened to check.
  Two places here are arranged so that it cannot arise: the hero fade masks the
  element box rather than clearing text positioned in another coordinate space,
  and the pull quote's hanging mark is a block rather than a glyph growing on
  `9vw` against an indent growing on `4vw`. Prefer an arrangement that cannot
  collide over one that currently does not.

---

## 7. Composition

### Alignment, not stagger

Research themes are a plain grid, three across and then two with the short row
centred, and the two project highlights share a top edge. Alternate rows are
never offset and no card is stepped down.

The rule: **two things side by side are read as a pair, and a staggered top
edge reads as a mistake rather than as composition.** Asymmetry is fine when it
is structural (a wide body beside a narrow rail); it is not fine as decoration.

It is enforced: `tools/lint.py` fails the build on any `:nth-child` selector
that sets a top margin.

### The graph on the band

The hero band carries the lab's own node-and-link figure — the one the emblem
draws in the paving stones — as a single drawing, placed in the half of the
band that has no text.

It is not a tile. A small motif repeated edge to edge at uniform density is
what makes a background read as wallpaper, and it puts texture behind the
words. The figure is drawn once, at 36 nodes and 64 edges, hand-placed so it
stays irregular.

Three things about it are load-bearing:

- **The fade is a CSS mask on the element box, not a gradient inside the SVG.**
  The drawing is cropped to fill its box; a gradient in user space would be
  cropped with it and the fade would land somewhere unpredictable — possibly
  under the text.
- **First ink sits at 57% of the band.** The text column ends at 54%. That
  three-point margin is the only thing keeping the graph off the words, so
  re-derive it if you change the box width or the mask.
- **A wider box does not show more graph.** The drawing scales to fill its box,
  so widening it magnifies the figure and the fixed window then shows a
  *smaller* slice. To show more graph, make the box **narrower**. It is at 62%,
  which renders at roughly natural size with about 70% of the drawing in view.

Each node sits on a small disc of the band colour, drawn between the edges and
the dots, so an edge stops at its node instead of showing through it.

**It is hidden below Pure's `md` breakpoint.** A narrow band has no empty half
to put it in, so it would sit under the text and read as noise.

The component is `.graph`, named for what it is rather than for the hero, and
everything adjustable is a custom property with a default: `--graph-width`,
`--graph-stroke`, `--graph-edge-alpha`, `--graph-node-alpha`, `--graph-ink`,
`--graph-ground`, and the two fade stops. A second band can use it by
overriding a value; nothing needs copying.

The top-to-bottom shading is a second mask layer, not a gradient inside the
SVG, and it is inside `@supports (mask-composite: intersect)`. A gradient would
need a `url(#id)` paint reference from the stylesheet, which does not resolve
reliably from an external sheet. Where the two layers cannot be combined the
horizontal fade still applies, and that is the part that keeps ink off words.

### The dark bands and the diagonal

The hero and each page header are inverse bands whose lower edge is a shallow
diagonal, deepest on the left, rising to the right.

It is a real cut, not a painted one. The band is a clipped `::before` layer,
and the band's element overlaps the section beneath it, so what shows through
the diagonal **is that section**, in whatever colour it has. There is no second
colour to keep in step.

Three separate numbers, because they answer three separate questions:

| Token | Answers |
| --- | --- |
| `--hero-skew` / `--pagehead-skew` | How much higher does the right end of the edge finish than the left? |
| `--hero-overlap` | How far is the band pulled over the section below? |
| `--hero-band-lift` | How far are *both* ends raised off the band's own bottom edge? |

The first two are equal by default, and that equality is what makes the next
section show through the diagonal. They are two tokens because the mobile
layout needs them to differ: if you find a value doing two jobs, split it
before you change either.

Below `md` the hero stacks, the band is lifted so its edge crosses the emblem's
middle, and the overlap drops to zero. A lifted band has nothing of the next
section to show through, and overlapping anyway would put the join between two
surfaces in the open just under the emblem.

The emblem hangs past the hero's content row, crosses the diagonal and carries
on into the section below. That is the one deliberate piece of dynamism on the
site, and it is a margin on an ordinary Pure unit — it reflows, wraps and zooms
like anything else.

The offset is deliberately larger than the hero's own bottom padding: the
emblem is meant to leave the band, not stop at it. What keeps it safe is the
section underneath. That section is pulled up by the skew and adds the same
amount back as padding, so its first line of text always sits `--section-pad`
below the hero's bottom edge, whatever the viewport. **If you change the hero's
padding, the skew or the overhang, re-check that clearance** — it is the only
thing standing between the emblem and the text below it.

### Rhythm

Section padding is `--section-pad`; the section after a band adds the skew back
so its content clears the overlap. Row gaps are `--row-gap`. Hairlines are
`--rule`. That is the whole vocabulary — a component that needs a new spacing
value probably wants an existing one.

---

## 8. Components

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
| `.pub` | One output, tagged by type of publication, venue and funding project. |
| `.tag` | Type of publication, venue or project. Distinguished by **colour and border style**, so it survives greyscale and colour-vision deficiency. |
| `.note` | Anything set aside from the argument of its section: a caveat, an invitation to work with the lab, a disclosure. One frame for all of them, with an optional `.note__title` and `.note__links`. |
| `.statement-list` | A term and its rule, one per row. Used by the AI statement. |
| `.graph` | The node-and-link figure on a dark band. See §7. |
| `.footer` | Three matching columns, the marks, the fine print. |

Controls are square-cornered (1px radius). Buttons are uppercase, letterspaced,
and come in four variants: `--primary` / `--ghost` for inverse bands,
`--solid` / `--outline` for light surfaces.

### Nothing is styled from the markup

No `style` attribute, no `<style>` element, no SVG presentation attribute
(`fill`, `stroke`, `stroke-width`, `stop-color`, `opacity`, …), no
presentational HTML attribute (`align`, `bgcolor`, `border`, …). Give the
element a class and style the class. `tools/lint.py` fails on all of them.

An attribute that paints cannot be restyled, cannot answer a media query, and
is invisible to anyone reading the stylesheet to find out how something looks.
The last two matter here: the hero figure disappears below `md`, and that is
one line in the stylesheet only because nothing about its appearance is in the
page.

**Geometry is not presentation.** A path's `d`, a circle's `cx` and `r`, a
`viewBox` and `preserveAspectRatio` say what the shape *is*. They stay in the
markup.

### A component exposes knobs, not copies

What varies is a custom property with a default, so a second use overrides a
value instead of duplicating the rule. `.graph` is the worked example: one rule
set, nine defaults, reusable on any dark band.

Name a component for what it is, not for where it first appeared. `.hero__art`
became `.graph` for that reason.

---

## 9. Motion

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

## 10. Imagery

### The lab's own artwork

`img/original/` holds the lab's masters and `img/logos/` the supplied
third-party marks. Everything else served from `img/` is generated by
`tools/build_assets.py`; never edit a generated file. WebP with a PNG fallback,
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

## 11. Accessibility

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

## 12. Things that are deliberately absent

Worth stating, so they are not proposed again as improvements:

- No JavaScript, no framework, no build step for the pages themselves.
- No dark scheme. See §3.
- No analytics, no cookies, no third-party request at page load.
- No carousel, no accordion, no modal, no scroll-jacking.
- No decorative photography. The emblem and the partner marks are the images.
- No dashboard, animated chart or invented metric.

---

## 13. Settled decisions

Each of these gets proposed the other way about once a year, and the reason is
not readable off the CSS.

- **Pure's grid, and none of our own.** Pure ships one; its `md` and `lg`
  breakpoints are the `48em` and `64em` the design works at, and its 24ths
  cover every asymmetric split on the site. See §6.
- **Oxblood is the ground, instrument cyan is the signal.** Both are sampled
  from the emblem, which is already a palette. Making the warm colour the
  surface rather than the accent puts about 200° of hue between this site and
  the neighbouring lab site it would otherwise resemble, and reverses the
  warm/cool relationship. See §3.
- **Source Serif 4 and Source Sans 3, self-hosted.** Both are OFL, both are
  variable, and they are designed to pair. Self-hosting removes a third-party
  request at page load. See §5.
- **One shallow diagonal on the dark bands, and no other motif.** It is a
  clip-path on the band's own layer: no fixed heights, no negative offsets,
  nothing to keep in step. See §4.
- **Four pages, not one.** Projects and publications each need more room than a
  section; the homepage carries highlights and links out to the records. See
  [METADATA.md](METADATA.md) §2 for which page describes what.
- **Provenance is declared wherever a generated asset appears**, not once in a
  colophon. See §10 and [METADATA.md](METADATA.md) §7.

---

## 14. Before you ship a design change

```sh
python3 tools/lint.py          # structure, links, metadata, CSS tokens
```

Then look at it: 320px, 768px, 1440px; 200% zoom; keyboard only. There is one
colour scheme, so there is one to look at. The linter checks that the rules here are *followed*; it cannot tell you
whether the result is any good.
