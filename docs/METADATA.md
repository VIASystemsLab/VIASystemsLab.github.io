# Metadata guide

How this site publishes machine-readable information about the lab, and what
you have to do to keep it correct when you edit a page.

Read this before adding a person, a project or a publication. Most of it is one
rule applied repeatedly: **the page and its metadata must say the same thing,
and both must be checkable.**

---

## 1. Why the site carries structured data at all

A research lab's site is read by more than people. Search engines, ORCID, EU
reporting tools, OpenAIRE-style harvesters and other researchers' scripts all
want to know who the lab is, who works in it, what it is funded by, and what it
has produced. Prose cannot tell them. Structured data can.

The site uses **JSON-LD 1.1** as its primary representation, with a small
amount of **RDFa** on the visible person and organisation records. JSON-LD is
an RDF serialisation, a W3C Recommendation, easy to validate, and understood by
search engines and research tooling. RDFa is added only where it binds visible
text to the same entity, so the two descriptions merge into one graph instead
of contradicting each other.

There is no separate metadata file to keep in sync. Everything lives in the
page it describes.

---

## 2. The entity model

Six kinds of thing, and one stable identifier each.

| Entity | `@id` | Described on |
| --- | --- | --- |
| The lab | `https://viasystemslab.github.io/#organization` | every page |
| The university | `https://ror.org/039bp8j42` | every page |
| A person | their ORCID URL | `index.html` only |
| A project | its CORDIS URL | `projects.html` only |
| A research theme | `…/#theme-<slug>` | `index.html` only |
| An output | its DOI URL | `publications.html` only |

Plus the site furniture: `#website`, each page's `#webpage`, the emblem
(`#emblem`), and the source repository.

### Describe once, reference everywhere

An entity is **described** on exactly one page — the page a reader would go to
for it. Every other page **references** it by `@id` and says nothing more:

```jsonc
// index.html — describes the person
{ "@id": "https://orcid.org/0000-0001-7922-5998",
  "@type": "Person", "name": "Matteo Lissandrini", "jobTitle": "…" }

// projects.html — references the same person, adds no claims
{ "@id": "https://cordis.europa.eu/project/id/101168951",
  "member": { "@id": "https://orcid.org/0000-0001-7922-5998" } }
```

This matters for more than tidiness. A description repeated on every page
becomes as many descriptions as there are pages, and they drift apart; the
one on the page nobody remembers to update is the one a harvester reads.

### Choosing an `@id`

Prefer an identifier someone else maintains and that resolves:

- a person → their **ORCID** URL
- a project → its **CORDIS** URL
- an institution → its **ROR** URL
- a paper, dataset or software release → its **DOI** URL
- anything with no external identifier → a fragment on this site's canonical
  URL, e.g. `https://viasystemslab.github.io/#organization`

Never invent an `@id`, never use a `mailto:` or a search URL, and never let one
change once it is published — a changed `@id` is a different entity as far as
every consumer is concerned.

---

## 3. Vocabularies

### Declared, because a term from them appears

| Prefix | IRI | Used for | On |
| --- | --- | --- | --- |
| *(default)* | `https://schema.org/` | Everything structural: `ResearchOrganization`, `Person`, `ResearchProject`, `ScholarlyArticle`, `Dataset`, `SoftwareSourceCode`, `DefinedTerm`, `MonetaryGrant`. | every page |
| `iptcExt` | `http://iptc.org/std/Iptc4xmpExt/2008-02-29/` | `DigitalSourceType`, for AI provenance. Reached through the `digitalSourceType` term definition rather than written as a prefixed name. | `index.html` |

**Declare a prefix only where a term from it is used.** An unused declaration
is not free: it reads as a promise that the page says something in that
vocabulary, so the next person to touch the graph has to read it to find out
that the page does not. `dcterms`, `foaf` and `org` were all declared with not
one term between them, and were removed rather than left as decoration.

### Available, not currently declared

The other namespaces the linter will accept an `http:` IRI from. Declare one on
the page that starts using it, and not before:

| Prefix | IRI | For |
| --- | --- | --- |
| `dcterms` | `http://purl.org/dc/terms/` | [Bibliographic terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) schema.org lacks. |
| `foaf` | `http://xmlns.com/foaf/0.1/` | [Person and group relations](http://xmlns.com/foaf/spec/). Prefer the schema.org equivalent where there is one, so the graph keeps to one vocabulary for one job. |
| `org` | `http://www.w3.org/ns/org#` | The [W3C Organization Ontology](https://www.w3.org/TR/vocab-org/), for organisational structure a `ResearchOrganization` cannot express. |

### `http:` is not a typo

Namespace IRIs use `http:`, not `https:`, because that is what the IRI *is*.
"Fixing" one to `https:` silently creates a different, undefined term.

`tools/lint.py` accepts an `http:` URL under these prefixes and rejects it
everywhere else, so the list above is also the list of vocabularies the build
will let you reach for:

```
http://purl.org/    http://xmlns.com/    http://www.w3.org/
http://iptc.org/    http://cv.iptc.org/
```

---

## 4. What each page carries

### `index.html`

The canonical graph. `WebSite`, `WebPage`, the `ResearchOrganization`, the
university, the principal investigator, the five research themes as
`DefinedTerm`s, brief `ResearchProject` stubs pointing at `projects.html`, the
emblem as an `ImageObject`, and the repository as `SoftwareSourceCode`.

The project stubs deliberately carry **no `description`** — the homepage shows
only highlights, so asserting the full description there would claim something
the page does not show.

### `projects.html`

A `CollectionPage` with a `BreadcrumbList` and an `ItemList`, plus the full
`ResearchProject` node for each project with its `MonetaryGrant`. References
the organisation and the university by `@id`.

### `publications.html`

A `CollectionPage` with a `BreadcrumbList` and an `ItemList`, plus a
`ScholarlyArticle` for every listed publication, each with its DOI as `@id` and
a `funding` reference to the project that paid for it. See §6.

### `ai-statement.html`

One node typed `["WebPage", "DigitalDocument"]`, because the page both *is* a
page and *carries* a document that other work can cite. It names the lab as
`author` and the principal investigator as `editor`, and it declares where its
text comes from:

- **`isBasedOn`** the statement it adapts, by DOI.
- **`citation`** the lab's own work that informed it, by DOI.
- **`dateModified`**, which the visible "Last update" line must match.

Both sources are described on this page, since it is the page a reader would
go to for them: a `CreativeWork` for the statement and a `ScholarlyArticle` for
the paper. Neither is a lab output, so neither belongs on `publications.html`.

Change the text materially and `dateModified` and the visible date change with
it. A statement whose recorded date predates its content is worse than an
undated one.

---

## 5. Recipes

### Add a person

1. Add the visible `<li class="person">` to the People section of
   `index.html`, in the right group.
2. Add the RDFa attributes, with `resource` set to their ORCID URL:

   ```html
   <li class="person …" vocab="https://schema.org/" typeof="Person"
       resource="https://orcid.org/0000-0000-0000-0000">
     <h4 class="person__name">
       <a property="url" href="https://example.org/"><span property="name">Name</span></a>
     </h4>
     <p class="person__title" property="jobTitle">Title</p>
   </li>
   ```

3. Add the `Person` node to the JSON-LD graph with the **same** `@id`, and list
   it under the organisation's `member`.
4. Make the ORCID iD **visible in the card**. This is enforced: the linter
   fails if the graph asserts an ORCID iD the page never prints.

Publish a name, photograph or email address only with that person's agreement.
For a collaborator you are naming but not describing, a bare reference is
enough — do not create a `Person` node for someone whose details you have not
checked with them.

### Add a project

1. Add the `<article class="project">` to `projects.html` with a stable `id`.
2. Add the `ResearchProject` node, `@id` = the CORDIS URL:

   ```jsonc
   {
     "@id": "https://cordis.europa.eu/project/id/000000000",
     "@type": "ResearchProject",
     "name": "ACRONYM",
     "alternateName": "Full title as CORDIS records it",
     "url": "https://project-site.example/",
     "startDate": "2025-01-01",
     "endDate": "2027-12-31",
     "member": { "@id": "https://viasystemslab.github.io/#organization" },
     "sameAs": ["https://cordis.europa.eu/project/id/000000000"],
     "funding": {
       "@type": "MonetaryGrant",
       "identifier": "000000000",
       "name": "Call identifier, as CORDIS writes it",
       "url": "https://cordis.europa.eu/project/id/000000000",
       "funder": { "@id": "https://ror.org/00k4n6c32" }
     }
   }
   ```

3. Add it to the page's `ItemList` and bump `numberOfItems`.
4. If it belongs on the homepage, add a **highlight** there and a matching stub
   node — name, dates, `mainEntityOfPage`, nothing more.
5. Add the grant to the funding disclaimer in the footer of every page.

Every date, grant number and figure comes from the project's CORDIS record.

### Add a publication

1. Put the visible entry in the right group in `publications.html`.
2. Add the output node, `@id` = the DOI URL:

   ```jsonc
   {
     "@id": "https://doi.org/10.0000/xxxxx",
     "@type": "ScholarlyArticle",
     "name": "Verified title",
     "author": [{ "@id": "https://orcid.org/0000-0001-7922-5998" }],
     "datePublished": "2026",
     "publication": { "@type": "PublicationEvent", "name": "EDBT 2026" },
     "identifier": "https://doi.org/10.0000/xxxxx",
     "url": "https://doi.org/10.0000/xxxxx",
     "funding": { "@id": "https://cordis.europa.eu/project/id/101168951" },
     "creativeWorkStatus": "Published"
   }
   ```

3. Reference it from the page's `CollectionPage` via `mainEntity`.

Use `Dataset` for data and `SoftwareSourceCode` (with `codeRepository`) for
tools. `funding` is what links an output back to the grant that paid for it —
it is the property EU reporting cares about, so do not omit it.

---

## 6. The verification rule

**Every entry on the publications page has a resolving DOI, and its record has
been checked against that DOI.** Not against a memory of it, not against a
citation in another paper, not against a preprint's metadata.

No DOI means no entry. The page lists peer-reviewed publications only: there is
no forthcoming section, no work in preparation, and no placeholder marked
pending. Data and software are published with the project that produced them.

A wrong DOI in structured data is copied into reference managers and aggregator
databases within days, and is very hard to retract. Leaving a paper off the list
until its DOI exists costs a reader nothing by comparison.

The same applies to ORCID iDs, ROR IDs, grant numbers and affiliations.

---

## 7. AI provenance

The lab emblem was generated with a model and then edited by hand. That is
declared in three places that must agree:

1. **Visibly**, in the footer provenance note on every page.
2. **In prose**, in `humans.txt`.
3. **Machine-readably**, on the `ImageObject` in `index.html`, using IPTC's
   controlled vocabulary — the interoperable way to state this:

   ```jsonc
   "digitalSourceType": {
     "@id": "http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia"
   }
   ```

Values you may need, from
<http://cv.iptc.org/newscodes/digitalsourcetype/>:

| Term | Means |
| --- | --- |
| `trainedAlgorithmicMedia` | Created by a generative model, used as generated. |
| `compositeWithTrainedAlgorithmicMedia` | Model output combined with human or non-AI work. **What this site's emblem uses.** |
| `algorithmicallyEnhanced` | Human-authored, with a model used to enhance it. |
| `digitalCapture` | A photograph. No model involved. |

If you add an image, declare its source type. If you replace the emblem with
something drawn by a person, change the value — do not leave the old one.

**The third-party marks are excluded from all of this.** The University of
Verona lockup, the EU emblem and the ARMADA and DataGEMS logos were supplied
by their owners and are reproduced unaltered. They carry no
`digitalSourceType`, and the provenance note is worded so it cannot be read as
covering them. See `img/logos/README.md`.

The code has its own acknowledgement: `creditText` on the `SoftwareSourceCode`
node, the `/* GENERATIVE TOOLS */` section of `humans.txt`, and a `[BOT]`
marker on agent-authored commits.

---

## 8. Non-RDF metadata

Also per page, and also checked:

- **`<link rel="canonical">`** — one per page. `og:url` must match it exactly.
- **Open Graph and Twitter card** — presentation only. They are never a
  substitute for the JSON-LD, and they must not contradict it.
- **`sitemap.xml`** — generated by `tools/build_assets.py`; never edited by
  hand. The linter fails if it and the set of pages disagree.
- **`robots.txt`** — points at the sitemap.
- **`humans.txt`** — per [humanstxt.org](https://humanstxt.org), linked from
  every page with `<link rel="author" type="text/plain">`.

---

## 9. Validating

```sh
python3 tools/lint.py
```

checks, among other things:

- the JSON-LD parses, every node has an `@id`, and no `@id` is duplicated
- every `@id` reference resolves — in this page's graph, in another page's
  graph, or into a declared controlled vocabulary
- the canonical URL is right and `og:url` agrees with it
- no ORCID iD or email address is asserted that the page does not show
- `humans.txt` exists, has its sections, and is linked

For the things a script cannot judge, use:

- **Schema Markup Validator** — <https://validator.schema.org/> — paste the
  page source and read the **expanded** graph, not just the summary. Check that
  entities you expected to merge actually merged into one node.
- **Google Rich Results Test** — <https://search.google.com/test/rich-results>
  — for how a search engine will read it.
- **W3C Nu Html Checker** — run in CI on every push.

Reading the expanded graph is the step people skip, and it is the one that
catches a `Person` that silently became two entities because an RDFa `resource`
and a JSON-LD `@id` did not match.
