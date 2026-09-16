# VIA Systems Lab — website

Source of <https://viasystemslab.github.io/>, the site of the VIA Systems Lab
(Verona Intelligent Analytics Systems) at the University of Verona.

Static HTML and CSS. No build step, no framework, no JavaScript, no tracking,
and no third-party request at page load — the fonts and the stylesheets are
served from this repository. Editing a page means editing an HTML file.

## Preview it locally

Open a terminal in this directory and serve it over HTTP:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000/>. Serve it rather than opening the file
directly: `file://` URLs break the manifest, the JSON-LD tooling and some
relative paths, so what you see would not be what visitors get.

Before you commit, run the checks:

```sh
python3 tools/lint.py
```

## What is where

### Content — the pages and what is written on them

| Path | What it holds |
| --- | --- |
| `index.html` | The homepage, in navigation order: hero, about, research themes, project highlights, people, footer. |
| `projects.html` | Every project, in full. The homepage carries highlights only. |
| `publications.html` | Every output, grouped by kind. |
| `ai-statement.html` | The lab's statement on AI and scientific research: principles, example guidelines, and the sources it adapts, including how the document itself was written. Linked from About, from the publications practice section and from the open-practice notes. |
| `img/original/` | The lab's master artwork. Edited by hand. |
| `img/logos/` | Third-party marks — the university, the EU emblem, partner projects. Reproduced as supplied: read [`img/logos/README.md`](img/logos/README.md) before touching them. |

### Style — how it looks

| Path | What it holds |
| --- | --- |
| `css/custom.css` | The whole design: colour and type tokens, then one section per component. The only stylesheet you should edit. |
| `css/pure.css`, `css/grids-responsive.css` | Pure CSS 3.0.0, vendored unmodified. Do not edit; replace by re-downloading a release. |
| `css/fonts.css` | `@font-face` rules. Generated to match `fonts/` — see "Fonts" below. |
| `fonts/` | Source Serif 4 and Source Sans 3, variable, `latin` and `latin-ext` subsets. |
| `icons/favicon.svg` | The favicon, hand-drawn. Every PNG icon beside it is generated from it or from the seal. |
| `img/` | Everything directly in here is generated from `img/original/` and `img/logos/`. Do not edit. |

**All presentation lives in `css/custom.css`.** The pages carry no `style`
attribute, no `<style>` element, no SVG presentation attribute (`fill`,
`stroke`, `stop-color`, …) and no presentational HTML attribute (`align`,
`bgcolor`, …). To change how something looks, give it a class and style the
class. `tools/lint.py` fails the build on any of them.

Geometry is not presentation: a path's `d`, a circle's `cx`, a `viewBox` and
`preserveAspectRatio` describe the shape itself and belong in the markup.

### Metadata, tooling and checks

| Path | What it holds |
| --- | --- |
| `docs/DESIGN-GUIDE.md` | What the site looks like and why — colour, type, layout, composition, imagery. The authority on design decisions. |
| `docs/METADATA.md` | How the structured data works and how to extend it. Read it before adding a person, project or publication. |
| `docs/DESIGN-PLAN.md` | The original brief. Historical; superseded by the design guide, which lists what changed. |
| `humans.txt` | Who made the site, per [humanstxt.org](https://humanstxt.org), including what was machine-generated. |
| `sitemap.xml`, `robots.txt` | Generated and hand-written respectively. Never edit the sitemap. |
| `site.webmanifest` | Name, icons and theme colours for installed/bookmarked use. |
| `tools/lint.py` | All the static checks. |
| `tools/build_assets.py` | Regenerates every derived image, icon and the sitemap. |
| `assets.lock.json` | Hashes of the artwork the generated files came from. CI compares against it. |
| `.githooks/` | Optional pre-commit and commit-msg hooks. |
| `.gitidentity.example` | Template for the per-person commit identity and signing key. |
| `.github/workflows/` | CI validation, and the job that rebuilds derived images when artwork changes. |

## Layout

Composition uses **Pure's own grid**: `.pure-g` on the row, `.pure-u-*` classes
on the children, at Pure's `md` (48em) and `lg` (64em) breakpoints. So a block
that is full width on a phone, half width on a tablet and a little over half on
a desktop is written in the markup:

```html
<div class="prose pure-u-1 pure-u-md-1-2 pure-u-lg-13-24">
```

`css/custom.css` deliberately does **not** define a grid. It adds only the two
things Pure leaves to the page:

- `.shell` centres a row and caps its width
- `.pure-g` gets gutters, which Pure omits so its units stay exact percentages

Everything else in that file styles components. Where a block is offset — the
second project highlight steps down slightly, the emblem hangs past the hero —
it is a `margin` on top of a Pure unit, never a second grid system.

### Surfaces are positional, never per-section

Sections alternate between the page surface and the travertine band through
`.section:nth-of-type(even)`. **Do not add a `section--about`-style modifier to
tint one.** Tying a colour to a named piece of content is what once left a
mismatched wedge under the hero when the sections were reordered; the linter now
rejects those modifiers.

For the same reason, a panel that sits *inside* a section — the project rail,
the "working with the lab" box — is tinted with
`color-mix(in srgb, var(--ink) 5%, transparent)` rather than filled with
`var(--paper)` or `var(--field)`. It then reads correctly whichever surface it
lands on, in either colour scheme.

### Adding a section

1. Give it a `<section>` with an `id`, a heading, and `aria-labelledby`
   pointing at that heading's `id`.
2. Put a `<div class="shell pure-g">` inside it.
3. Give each child a `pure-u-*` class for each breakpoint you care about.
4. If it should be reachable from the menu, add it to the navigation in **all
   three** pages, in the same order everywhere, and keep the page's own section
   order matching that navigation.

## Editing content

### A research theme

In `index.html`, inside `<ol class="themes pure-g">`. Copy a `<li class="theme">`
block, keep its `id` stable — the JSON-LD `DefinedTerm` for that theme points at
it — and add a matching `DefinedTerm` to the graph in `<head>`. The blocks are
unnumbered, so order is the only thing that changes when you add one.

### A project

In `projects.html`, inside the "Funded projects" section. Copy an
`<article class="project pure-g">` and give it a stable `id`. Every record has
the same shape — description on the left, rail on the right holding the logo,
the links and the facts — and they are deliberately not alternated or offset.

Add the matching `ResearchProject` object to the JSON-LD graph in that page's
`<head>`. If the project should also appear on the homepage, add a short
`<li class="highlight">` to `index.html` — the homepage carries highlights
only, never the full record. Add the grant to the funding column in the footer
of all three pages.

**Publish a figure only once it appears in the project's CORDIS record or on
its own site.** Grant numbers, durations, consortium sizes and contributions
are all public there; none of them should come from memory.

**Confirm a repository really belongs to the project before linking it.** A
plausible-looking account name is not evidence: `github.com/DataGems` is an
unrelated personal account, while the project's actual organisation is
`github.com/datagems-eosc`. Check the organisation's name, description and
repositories, then record it in the project's `sameAs`.

### A publication

In `publications.html`. There is a filled-in template in an HTML comment at the
end of the list — copy that.

Groups and tags are two different axes, and it is worth keeping them apart:

- **The group** says what kind of contribution the paper makes: a journal
  article, a research paper, a vision or position paper, a demonstration, a
  poster. Put the entry in the matching group, newest first.
- **The tags** say where it was published and who paid for it: the type of
  publication, then the venue, then the funding project.

So a vision paper that appeared at a conference is filed under **Vision and
position papers** and tagged **Conference**. The two do not have to agree
because they are not answering the same question.

The tag classes are:

```
tag--journal  tag--conference  tag--workshop  tag--demo  tag--poster
tag--dataset  tag--software                 (project outputs)
tag--armada   tag--datagems                 (funding project)
tag--venue                                  (venue label)
```

Types are distinguished by border style as well as by colour, so they still
read in greyscale and to a colour-blind reader. Keep that property if you add a
new type.

**Every entry has a resolving DOI.** No DOI, no entry: not a preprint, not a
paper in preparation, not a placeholder. The page lists peer-reviewed
publications only, so there is no forthcoming section. Data and software are
published with the project that produced them.

Resolve the DOI and check the title, authors, year and venue against what it
resolves to before adding anything. `tools/lint.py` fails the build if a
published entry has no `doi.org` link, and if the structured data asserts an
ORCID iD or an email address the page never shows. It cannot tell you the DOI
points at the right paper.

### A person

In `index.html`, in the People section. The roster has four groups —
**Principal investigator**, **Members**, **External members** and
**Collaborators** — and ships with one real record and four `is-pending` slots
so the shape is obvious. Copy a `<li class="person">`, drop `is-pending`, and
fill it in.

Which group: Members are appointed at the University of Verona, External
members work with the lab from another institution, Collaborators are named on
a shared output.

For a member of the lab, add the matching `Person` node to the JSON-LD graph
and list it under the organisation's `member`. The RDFa attributes (`typeof`,
`property`, `resource`) must keep matching that node, and `resource` must be the
person's ORCID URL, or the two descriptions become two separate entities. The
ORCID iD has to be visible in the card — the linter enforces it. See
[docs/METADATA.md](docs/METADATA.md).

Publish a name, a photograph or an email address only with that person's
agreement.

## Design tokens

**[docs/DESIGN-GUIDE.md](docs/DESIGN-GUIDE.md) is the full design guide** —
palette, type scale, layout, composition rules and what is deliberately absent.
Read it before changing how anything looks.

All colour and type decisions live at the top of `css/custom.css`, in `:root`.
Change them there, never in a component.

The palette is sampled from the lab emblem: travertine, oxblood brick and ink,
with the node-graph's teal raised to an instrument cyan and used only as a
signal. There is one scheme; the site does not follow `prefers-color-scheme`,
and [docs/DESIGN-GUIDE.md](docs/DESIGN-GUIDE.md) says why. Every text pair
meets WCAG AA; body text on paper is 14.5:1. **If you change a colour,
re-check the pairs it appears in** — the tokens carry their measured ratio in a
comment, and `tools/lint.py` checks the arithmetic.

A component that needs a value to vary exposes it as a custom property with a
default, rather than being copied and edited. `.graph`, the node figure on the
hero band, is the worked example.

Two typefaces, both variable, both under the SIL Open Font Licence:
Source Serif 4 for headings, Source Sans 3 for everything else.

### Fonts

`fonts/` and `css/fonts.css` were generated from the Google Fonts CSS2 API and
then vendored, so the site makes no third-party request. To change a weight
range or add a subset, fetch the new CSS from that API with a browser user
agent, download the `.woff2` files it points at, and rewrite `css/fonts.css` to
match. Keep `font-display: swap` and keep the `unicode-range` values — they are
what stops a reader downloading `latin-ext` they will never see.

## Images and icons

Everything in `img/` except `img/original/`, and every PNG in `icons/`, is
generated. After changing the artwork or `icons/favicon.svg`:

```sh
python3 tools/build_assets.py
```

This rewrites the derivatives, the social card, the icons and `sitemap.xml`,
and records a hash of each source in `assets.lock.json`. CI compares those
hashes, so forgetting to rebuild fails the build rather than shipping a stale
logo.

Prerequisites, on macOS:

```sh
brew install webp librsvg
```

on Debian or Ubuntu:

```sh
sudo apt-get install webp librsvg2-bin imagemagick
```

You do not have to install them to change text or CSS — only to change
artwork. If you push artwork without rebuilding, the `Assets` workflow rebuilds
and commits the derivatives for you.

## Metadata

Each page carries one JSON-LD graph in `<head>`, plus RDFa on the visible
person and organisation records. **[docs/METADATA.md](docs/METADATA.md) is the
full guide** — the entity model, the vocabularies, copy-paste recipes and how
to validate. In short:

- One canonical URL per page, and `og:url` matches it.
- Every node has a stable `@id`, preferably one someone else maintains: ORCID
  for a person, CORDIS for a project, ROR for an institution, a DOI for an
  output.
- An entity is *described* on one page and *referenced* by `@id` from the
  others. Do not restate it.
- `sameAs` points at an authoritative profile, never at a search result.
- What the structured data claims, the page shows. The linter fails the build
  if the graph asserts an ORCID iD or an email address the page never prints.

## Accessibility

These are requirements, not preferences, and several are enforced by the
linter:

- One `<h1>` per page, and heading levels never skip.
- A skip link to `#main` on every page.
- Every image has `alt` (empty when decorative) and `width`/`height`.
- Keyboard focus is always visible; never remove an outline without replacing it.
- The page works with CSS disabled and with JavaScript unavailable.
- Motion is confined to one reveal, behind both `prefers-reduced-motion` and an
  `@supports` guard, so it can never hide content.

Test at 320px, at 200% zoom, and with the keyboard alone before shipping a
layout change.

## Checks

`tools/lint.py` verifies structure, links, metadata and CSS:

```sh
python3 tools/lint.py              # fast, no network
python3 tools/lint.py --external   # also resolves every outbound URL
```

Install the git hooks once per clone, to run the checks before each commit and
to check the commit message format:

```sh
git config core.hooksPath .githooks
```

### Commit identity

Entries in the history are attributed explicitly and signed, rather than
picking up whatever global git identity happens to be configured on the
machine. Set yours up once per clone:

```sh
cp .gitidentity.example .gitidentity
$EDITOR .gitidentity                              # your name, address, key id
git config --local include.path ../.gitidentity
```

`.gitidentity` is a git config file that `.git/config` includes, so git reads
it natively — there is no script in between. It is gitignored, because it is a
per-person setting: cloning the repository must not hand you somebody else's
address or signing key.

Check that it took:

```sh
git config --get user.email
git log -1 --show-signature
```

A signed entry reports `Good signature`. If signing fails, fix it rather than
going ahead unsigned — a misattributed or unsigned entry cannot be corrected
without rewriting history.

Commit messages follow `<type>(<scope>): <subject>`, imperative, lowercase,
no trailing full stop, 72 characters or fewer:

```
fix(nav): keep the current page marked on the projects page
content(publications): add the EDBT vision paper
build(assets): regenerate the emblem derivatives
```

Types: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci`
`chore` `content`.

On GitHub, `.github/workflows/ci.yml` runs the linter, validates every page
with the Nu Html Checker, and confirms the derived assets match their sources.
It re-checks outbound links weekly. `.github/workflows/assets.yml` rebuilds and
commits derived images when the artwork changes.

## Provenance and acknowledgements

The site is explicit about what was machine-generated, in the footer of every
page, in `humans.txt`, and in the page metadata.

- **The lab emblem** was created with OpenAI's ChatGPT image generation tool
  from prompts developed for the lab, then refined by hand. It is declared
  machine-readably with the IPTC digital source type
  `compositeWithTrainedAlgorithmicMedia`.
- **The markup, styles, tooling and documentation** were drafted with Claude
  Opus 5 and reviewed by the authors. Agent-authored commits carry `[BOT]` in
  the subject line.
- **The content** — research descriptions, project summaries, publication
  records — is written and verified by people.
- **Third-party marks are not covered by any of that.** The University of
  Verona lockup, the EU emblem and the ARMADA logo belong to their owners and
  are reproduced as supplied. If you touch them, read
  [`img/logos/README.md`](img/logos/README.md) first: the EU emblem in
  particular must keep its own blue field and its 3:2 proportions, and must
  never be inverted or tinted.

If you add an image, declare its source type. If you add a funded project, add
its grant to the funding acknowledgement in the footer of all three pages.

## Deployment

The site is an organisation GitHub Pages site served from the default branch.
Pushing to `main` publishes it; there is no deployment workflow and there
should not be one. `.nojekyll` is present so the files are served exactly as
committed.

## Licence

Site source: see [LICENSE](LICENSE). The lab emblem and wordmark in
`img/original/` are the lab's own marks. Source Serif 4 and Source Sans 3 are
used under the SIL Open Font Licence 1.1; Pure CSS under the BSD Licence.
