# VIA Systems Lab Website Design Plan

> [!NOTE]
> **Historical. This is the original brief, not the current design.**
>
> The site has been built, and several decisions here were superseded along the
> way — the custom 15-column grid, the staggered compositions, the one-page
> structure. **[DESIGN-GUIDE.md](DESIGN-GUIDE.md) is the authority on how the
> site is designed now**, and its final section lists exactly what changed and
> why.
>
> This document is kept because the reasoning behind the brief is still worth
> reading: the audience, the objectives, the non-goals, and the metadata and
> accessibility requirements, which carried over intact. Do not implement from
> this page without checking the guide first.

**Status:** First draft, superseded  
**Audience:** Research collaborators, students, practitioners, and open-source communities  
**Platform:** GitHub Pages, static HTML/CSS, progressive enhancement  
**Primary language:** English, with a future path to Italian content

## 1. Product Direction

VIA Systems Lab should present a small, serious research organization with a clear point of view:

> Old scientific discipline, carried forward with modern data systems.

The site should feel modern, minimal, reliable, and open without looking like a generic technology startup. Its character should come from editorial typography, precise spacing, visible evidence of research activity, and a restrained visual system rather than decorative effects.

### Core objectives

1. Explain what the lab studies within the first viewport.
2. Make people, research areas, projects, and publications easy to discover.
3. Show that the lab values verification, reproducibility, and open source.
4. Work well on a phone before adding larger-screen composition.
5. Publish machine-readable information that search engines and research tools can understand.
6. Keep the site maintainable as a small static repository.

### Non-goals for the first release

- No custom JavaScript application shell.
- No CMS or server-side dependency.
- No artificial dashboard, animated data visualization, or speculative metrics.
- No attempt to publish complete publication metadata until the underlying records are verified.

## 2. Current Repository Assessment

The existing page is a useful content draft, but it needs structural cleanup before visual refinement.

- `via.html` already contains the essential narrative: the lab description, principal investigator, research areas, VIA interpretations, and contact information.
- The current markup uses Pure grid classes and custom `g-*` classes, but the stylesheet links point to `css/pure.css` and `css/custom.css` while those files currently live at repository root. The asset paths must be made consistent.
- The vendored stylesheet is Pure CSS `1.0.0`. The current upstream release is Pure CSS `3.0.0`.
- The wave SVG and older layout rules create a strong visual identity, but they also introduce fixed heights, negative offsets, wide-screen assumptions, and unnecessary layout fragility.
- The current page has no reliable navigation, project/publication structure, skip link, explicit landmark strategy, or machine-readable research metadata.
- The image/logo assets already present in the repository should be reused before introducing new artwork.

## 3. Information Architecture

The first version should remain a focused one-page site with stable anchors. A later version can split content into dedicated pages without changing the conceptual model.

### Primary navigation

- **About** - mission, approach, and institutional context
- **Research** - research themes and methods
- **Projects** - selected open-source or data projects
- **People** - principal investigator and future members
- **Publications** - selected papers, datasets, and software
- **Contact** - affiliation, email, profiles, and repository links

On small screens, the navigation should be a compact native disclosure or a simple stacked list. Do not require JavaScript for access to any section.

### Page sequence

1. **Header / masthead**
   - VIA Systems Lab wordmark or logo
   - short descriptor: `Verona Intelligent Analytics Systems`
   - anchor navigation
2. **Hero statement**
   - one precise sentence about trustworthy, interactive information analytics
   - primary actions: `Explore research` and `View open source`
   - one small fact line: University of Verona, Italy
3. **Research signal**
   - three or five concise themes, arranged as an odd-column grid
4. **About the lab**
   - mission, working style, and connection to digital archives / data systems
5. **Selected work**
   - project records with status, technologies, links, and maintenance state
6. **People and affiliation**
   - person record, institutional link, ORCID, GitHub, and email where verified
7. **Publications and outputs**
   - selected publications, datasets, software, and teaching material
8. **Open practice**
   - source repositories, licenses, reproducibility, and contribution links
9. **Footer**
   - contact, University of Verona, privacy/accessibility note, metadata links

## 4. Layout System

### Grid decision

Use Pure CSS as the base utility layer, but define the lab's composition in a small custom layer. Pure's default 5-column mental model is not sufficient for the desired editorial rhythm.

Use a semantic **15-column conceptual grid** on medium and large screens. Fifteen is intentionally odd and supports balanced asymmetric compositions:

- full width: `15 / 15`
- wide content: `9 / 15`
- supporting content: `5 / 15`
- gap or alignment rail: `1 / 15`
- three feature items: `5 / 15` each
- five research themes: `3 / 15` each

The implementation may use CSS Grid for the custom compositions while retaining Pure for reset, forms, buttons, and basic utilities. This avoids forcing meaningful content into arbitrary class names such as `g-3-5`.

### Mobile-first rules

- Base layout is one column with a readable measure of approximately 35-45rem.
- No negative margins or visual overlap below the medium breakpoint.
- Hero content, navigation, headings, and buttons must wrap without clipping.
- Research themes stack as a vertical list or two-column list only when the viewport allows it.
- Images use intrinsic dimensions and `max-width: 100%`.
- Decorative waves, if retained, are optional background accents and never contain essential text.
- Medium and large layouts introduce the 15-column composition progressively, rather than switching the entire page at once.

### Suggested responsive breakpoints

Use content-driven breakpoints, documented in CSS variables or comments:

- base: under `48rem`
- medium: `48rem` and above
- large: `64rem` and above

The exact values can follow Pure CSS conventions, but the layout should be validated at 320px, 375px, 768px, 1024px, and 1440px widths.

## 5. Visual Direction

### Tone

Quietly technical, editorial, and civic. The design should communicate care and longevity: archival references, clear typographic hierarchy, and strong contrast paired with a small amount of contemporary color.

### Palette

Define tokens in `custom.css` rather than scattering values:

- ink: deep blue-black for text and primary headings
- paper: warm near-white for the main reading surface
- field: pale cool blue for secondary bands
- signal: restrained vermilion or coral for emphasis and links
- rule: muted blue-gray for borders and dividers
- inverse: paper text on ink backgrounds

Avoid a page dominated by gradients or one hue family. Color should identify actions, active links, and research signals, not decorate every surface.

### Typography

Use one expressive display family and one highly legible text family, loaded with a performance-conscious strategy. Recommended direction:

- display: a contemporary serif or humanist grotesk for section titles
- text: a readable sans-serif for body copy, metadata, and navigation
- code / repository labels: system monospace or a local monospace fallback

Keep body text between roughly 1rem and 1.15rem with generous line height. Avoid all-caps paragraphs. Reserve uppercase labels for short metadata only.

### Shape and motion

- Use square or lightly rounded controls, no excessive pill shapes.
- Use rules, offsets, and numbered labels to create identity.
- Add one page-load reveal for major sections and a restrained hover/focus transition for links.
- Respect `prefers-reduced-motion: reduce`.
- Do not make animation necessary to understand the content.

## 6. Content Model

Use consistent records so the page can grow without redesigning each section.

### Research theme

- `name`
- `short description`
- `methods or technologies`
- `related projects`
- `related publications`

Initial themes can be derived from the existing draft:

- Intelligent data analytics
- Knowledge graphs and data exploration
- Human-centered analytics
- Validated and trustworthy data systems
- Open data and digital archives

### Project

- title
- one-sentence purpose
- status: active, maintained, archived, or experimental
- repository URL
- documentation URL
- license
- technology tags
- related people

### Scholarly output

- title
- authors
- publication date
- venue
- DOI or stable URL
- abstract or short contribution statement
- related dataset/software URL

Do not invent publication, DOI, ORCID, license, or project facts. Use placeholders in the draft and replace them only after verification.

## 7. Semantic Web and RDF Metadata

### Recommendation

Use **JSON-LD 1.1** in a `<script type="application/ld+json">` block as the primary embedded RDF representation. JSON-LD is an RDF-compatible W3C standard, is easy to validate, and is supported by search engines and research tooling. Add visible semantic HTML and selected RDFa attributes where they improve the relationship between visible content and metadata.

The metadata should describe the lab as an organization, not claim that every page element is a publication or dataset.

### Vocabulary strategy

Use a small, explicit context:

- `schema.org` for `ResearchOrganization`, `Person`, `ScholarlyArticle`, `Dataset`, and `SoftwareSourceCode`
- `foaf` for person identity relationships where useful
- `dcterms` for titles, dates, subjects, and licenses
- `org` for organizational membership if a richer people model is needed
- `skos` only if research themes become a controlled vocabulary

Prefer stable identifiers and URLs over repeated literal text.

### Organization entity

Create one canonical organization entity with:

- `@id`: the canonical site URL plus a fragment, for example `https://<verified-domain>/#organization`
- `@type`: `ResearchOrganization`
- `name`: VIA Systems Lab
- `alternateName`: Verona Intelligent Analytics Systems
- `url`: canonical homepage
- `description`: concise verified description
- `parentOrganization`: University of Verona, if appropriate and verified
- `address`: Verona, Italy, only to the level the lab wants public
- `sameAs`: official university, GitHub organization, ORCID, and other authoritative profiles
- `member`: verified people only
- `knowsAbout`: the research themes

### Person entity

Create a linked `Person` entity for the principal investigator and later lab members:

- stable `@id`
- `name`
- `jobTitle`
- `affiliation`
- `worksFor`
- `sameAs`: ORCID, university profile, GitHub, and personal site when verified
- `email`: include only if intentionally public

### Output entities

Represent selected outputs as linked records:

- papers: `ScholarlyArticle`
- datasets: `Dataset`
- repositories or tools: `SoftwareSourceCode`

Each output should link back to the organization or person through `creator`, `author`, `funder`, `maintainer`, or `provider` as appropriate. Use DOI, repository, and dataset URLs as identifiers where available.

### Metadata quality rules

- One canonical URL per page.
- Every `@id` must be stable and dereferenceable when practical.
- `sameAs` must point to an authoritative external identity, not a search result.
- Visible names, affiliations, dates, and links must agree with JSON-LD.
- Validate JSON-LD syntax and inspect the expanded graph before publishing.
- Add `og:*` and Twitter card metadata as social presentation metadata, but do not use it as a replacement for JSON-LD.
- Consider a `sitemap.xml` and `robots.txt` when the page structure stabilizes.

## 8. Accessibility and Reliability Requirements

- Use one `h1`, followed by logical heading levels.
- Include a visible-on-focus skip link to `main`.
- Use landmarks: `header`, `nav`, `main`, section headings, and `footer`.
- Every meaningful image needs accurate alternative text; decorative images use empty alt text.
- Maintain WCAG AA contrast for text, links, controls, and focus indicators.
- Use keyboard-visible focus states and never remove the default focus behavior without replacement.
- Make external links clear and avoid unnecessary `target="_blank"` behavior.
- Keep the page functional with CSS disabled and JavaScript unavailable.
- Use `lang="en"` now and plan for language alternates if Italian content is added.
- Test with keyboard navigation, reduced motion, zoom to 200%, and a screen reader spot check.

## 9. Pure CSS Migration Plan

1. Replace the local Pure `1.0.0` asset with the official Pure `3.0.0` distribution, or pin the official CDN asset with a documented fallback decision.
2. Correct the stylesheet paths so the deployed GitHub Pages site loads them from the repository root or move assets into a deliberate `css/` directory.
3. Keep Pure for base styles, buttons, forms, menus, and utilities.
4. Remove reliance on the old Pure grid font hack and replace the custom grid with CSS Grid where asymmetric layouts are required.
5. Rewrite `custom.css` around tokens, component sections, and mobile-first rules.
6. Remove fixed-height wave positioning and negative desktop offsets unless they survive mobile, zoom, and content growth tests.
7. Preserve existing logo assets and check their contrast on both paper and inverse backgrounds.
8. Keep HTML class names semantic and local to the component they style.

## 10. Delivery Phases

### Phase 1: Foundation

- Fix asset paths.
- Pin Pure CSS `3.0.0`.
- Establish HTML landmarks, skip link, navigation, canonical metadata, and CSS tokens.
- Replace the current hero structure with a content-first masthead.

**Exit condition:** the page renders correctly with CSS and without JavaScript at all target widths.

### Phase 2: Content and layout

- Convert research areas into five structured theme items.
- Add project, people, and publication sections with verified or clearly marked pending content.
- Implement the 15-column large-screen compositions and mobile stack.
- Reuse and test the existing logo assets.

**Exit condition:** a first-time visitor can identify the lab, its research, its people, and its open-source path within one scroll and the navigation reaches every section.

### Phase 3: Metadata and discoverability

- Add JSON-LD graph for the organization, principal investigator, and selected outputs.
- Add RDFa only to visible organization/person relationships that benefit from inline semantics.
- Add canonical, Open Graph, and social metadata.
- Validate the graph, links, and structured data.

**Exit condition:** all published metadata is syntactically valid, internally consistent, and based on verified facts.

### Phase 4: Quality pass

- Test keyboard and screen-reader navigation.
- Test at target viewport widths and 200% zoom.
- Test reduced motion and slow network loading.
- Check broken links, missing assets, console errors, and HTML validation.
- Review copy for precision, Italian institutional naming, and open-source claims.

**Exit condition:** no known accessibility, asset-path, or metadata errors remain for the first release.

## 11. Acceptance Checklist

- [ ] Pure CSS is pinned to `3.0.0` and its source is documented.
- [ ] All CSS and image paths work from the GitHub Pages deployment root.
- [ ] The first viewport clearly identifies VIA Systems Lab and its research focus.
- [ ] Mobile layout is usable at 320px without horizontal scrolling.
- [ ] Medium and large layouts use intentional odd-column compositions.
- [ ] Research, projects, people, publications, and contact have stable anchors.
- [ ] The page has a skip link, visible keyboard focus, logical headings, and accessible images.
- [ ] JSON-LD validates and uses stable identifiers.
- [ ] Visible facts and structured metadata agree.
- [ ] External identities and links are verified before publication.
- [ ] The site remains useful with JavaScript disabled.
- [ ] README documents local preview and deployment expectations.

## 12. Open Decisions Before Implementation

- Confirm the canonical public domain and final GitHub organization URL.
- Confirm the official spelling and capitalization of the lab and University of Verona affiliation.
- Decide which people, projects, publications, datasets, and repositories are ready for public listing.
- Confirm whether the public site should be English-only initially or launch with Italian language support.
- Choose a display typeface that is permitted for web embedding and performs well on GitHub Pages.
- Decide whether the wave motif remains as a small accent or is retired in favor of the logo and typographic system.
- Confirm the preferred public contact email and whether a physical address should be published.
