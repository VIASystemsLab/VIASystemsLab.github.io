# Contributing

How to change the site and get the change committed. What the site looks like
and why is in [DESIGN-GUIDE.md](DESIGN-GUIDE.md); how the structured data works
is in [METADATA.md](METADATA.md).

## Set up once per clone

Enable the hooks, which run the checks before each commit and check the
message format:

```sh
git config core.hooksPath .githooks
```

Set up your commit identity. Entries in the history are attributed explicitly
and signed, rather than picking up whatever global identity the machine has:

```sh
cp .gitidentity.example .gitidentity
$EDITOR .gitidentity                              # your name, address, key id
git config --local include.path ../.gitidentity
```

`.gitidentity` is a git config file that `.git/config` includes, so git reads
it natively. It is gitignored because it is per person: cloning the repository
must not hand you somebody else's address or signing key. Check that it took:

```sh
git config --get user.email
git log -1 --show-signature                       # expect "Good signature"
```

If signing fails, fix it rather than committing unsigned. A misattributed or
unsigned entry cannot be corrected without rewriting history.

## Before you commit

```sh
python3 tools/lint.py
python3 tools/build_assets.py --check
```

The `pre-commit` hook runs both. CI runs them again, plus the Nu Html Checker.

## Rules for changes

- **Style the class, never the element.** No `style` attribute, no `<style>`
  element, no SVG presentation attribute, no presentational HTML attribute.
  Give the element a class and style it in `css/custom.css`. The linter fails
  on all of these.
- **Never edit a generated file.** Images directly in `img/`, the PNG icons and
  `sitemap.xml` come from `tools/build_assets.py`. Change the source and
  rebuild.
- **Every publication has a resolving DOI.** The page lists peer-reviewed work
  only. Before adding an entry, confirm the title, authors, year and venue
  against what the DOI resolves to. The linter checks that the link is there,
  not that it points at the right paper.
- **Write copy by the Language section of
  [DESIGN-GUIDE.md](DESIGN-GUIDE.md#2-language).** It applies to commit
  messages and comments too.

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
