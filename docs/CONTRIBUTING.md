# Contributing

How to change the site and get the change committed. What the site looks like
and why is in [DESIGN-GUIDE.md](DESIGN-GUIDE.md); how the structured data works
is in [METADATA.md](METADATA.md).

## Set up once per clone

Install [pre-commit](https://pre-commit.com) and enable the hooks, which run
the checks before each commit and check the message format:

```sh
uv tool install pre-commit
git config --local --unset-all core.hooksPath 2>/dev/null || :
pre-commit install
```

`.pre-commit-config.yaml` lists what runs.

Set up your commit identity in this clone's own config, so entries in the
history are attributed explicitly and signed, rather than picking up whatever
global identity the machine has:

```sh
git config --local user.name "Your Name"
git config --local user.email "you@example.org"
git config --local user.signingkey <your-key-id>
git config --local commit.gpgsign true
```

If you have no signing key yet, GitHub's guide shows how to create one and add
it to your account:
<https://docs.github.com/en/authentication/managing-commit-signature-verification>.
After your first commit, check that it took:

```sh
git log -1 --show-signature                       # expect "Good signature"
```

If signing fails, fix it rather than committing unsigned. A misattributed or
unsigned entry cannot be corrected without rewriting history.

## Before you commit

```sh
python3 tools/lint.py
python3 tools/build_assets.py --check
```

The pre-commit hooks run both. CI runs them again, plus the Nu Html Checker.

## Rules for changes

- **Style the class, never the element.** No `style` attribute, no `<style>`
  element, no SVG presentation attribute, no presentational HTML attribute.
  Give the element a class and style it in `css/custom.css`. The linter fails
  on all of these.
- **Never edit a generated file.** Images directly in `img/`, the PNG icons and
  `sitemap.xml` come from `tools/build_assets.py`. Change the source and
  rebuild.
- **Every publication has a resolving DOI**, or, where the venue issues none, a
  link to its record in the venue's official archive. The page lists
  peer-reviewed work only. Before adding an entry, confirm the title, authors,
  year and venue against what the link resolves to. The linter checks that the
  link is there, not that it points at the right paper.
- **Write copy by the Language section of
  [DESIGN-GUIDE.md](DESIGN-GUIDE.md#2-language).** It applies to commit
  messages and comments too.
- **Leave the lab's marks, the partner logos and the icons to the
  maintainer.** They live in `img/original/`, `img/logos/` and `icons/`, and
  every change to them goes through `tools/build_assets.py`, which needs image
  tools installed (see the README). Images for page content go in
  `img/content/` instead, as below.

## Adding an image or a PDF

Both are served exactly as you commit them, with no build step.

**An image inside a page** goes in `img/content/`:

1. Export it ready to serve: WebP (or PNG or JPEG), no wider than it is shown,
   under **500 KB**. 1600 pixels wide is plenty for a full-width figure.
2. Name it for what it shows, lowercase with hyphens:
   `img/content/armada-kickoff-2026.webp`.
3. Reference it with `alt`, `width` and `height`, and `loading="lazy"` below
   the fold:

   ```html
   <img src="img/content/armada-kickoff-2026.webp"
        alt="The ARMADA doctoral candidates at the kick-off meeting in Verona"
        width="1600" height="900" loading="lazy">
   ```

   `alt` says what the image shows, for someone who cannot see it. Leave it
   empty (`alt=""`) only for an image that adds nothing to the text.
4. If the image was made or altered with a generative image tool, say so in
   its caption. The caption is enough: a content image needs no structured
   data.

Publish a photograph of a person only with their agreement.

**A PDF** goes in `files/`, under **10 MB**, named the same way:
`files/armada-summer-school-2026-programme.pdf`. Link it from the page with its
size, so a reader knows before downloading:

```html
<a href="files/armada-summer-school-2026-programme.pdf">Programme (PDF, 1.2 MB)</a>
```

Host a PDF here only when it has no other public home. A paper is linked by its
DOI or its official archive record, and a dataset or a deliverable by its
Zenodo or CORDIS record.

`tools/lint.py` fails on a file over the limit or of another type, and warns
about a file that no page links to.

## Commits

```
<type>(<scope>): <subject>
```

- **type**: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci`
  `chore` `content`
- **scope**: optional, lowercase letters, digits and `. _ / -`, naming a real
  part of the site: `nav`, `theme`, `seo`, `assets`, `publications`
- **subject**: imperative ("add", not "added"), lowercase first letter, no
  trailing full stop, and saying what changed: not `update`, `wip` or `fix`
- 72 characters or fewer for the whole subject line
- a body, if any, after one blank line

```
fix(nav): keep the current page marked on the projects page
content(publications): add the EDBT vision paper
build(assets): regenerate the emblem derivatives
```

One topic per commit: do not mix a content change with a styling change, or a
refactor with a behaviour change. Stage files by name rather than with
`git add -A`, so a stray file never rides along.

Commits written by a coding agent end their subject line with ` [BOT]`, so they
can be told apart from hand-written ones. Do not add it to your own.

## Proposing a change

Every change reaches the site through a pull request. `main` accepts nothing
else, and merging into it publishes the site within a minute or two.

1. **Make a branch.** Members of the VIASystemsLab organisation push branches
   to this repository; anyone else forks it.

   ```sh
   git switch main
   git pull
   git switch -c profile/your-name
   ```

2. **Make the change and preview it** with `python3 -m http.server 8000`, as
   the README describes.
3. **Commit** as above. The hooks run the checks.
4. **Push and open a pull request** against `main`. Keep it to one topic, such
   as one new person or one publication.
5. **Wait for CI.** It runs the same checks, plus the HTML validator. A red
   check means something to fix on your branch: push the fix and CI runs again.
6. **Ask someone else to review it.** They merge it when CI is green. Do not
   merge your own.

If `main` moves on while you wait, press **Update branch** on the pull request.
If GitHub reports a conflict, ask for help rather than resolving it by guesswork,
then open **Files changed** and check that it shows only your change.
