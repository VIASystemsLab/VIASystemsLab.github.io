# AGENTS.md: VIA Systems Lab website

The public website of VIA Systems Lab at the University of Verona: a static HTML/CSS site on Pure CSS, served through GitHub Pages.

## Core rules

These are binding. They override any general default behaviour.

1. **Never touch anything outside this repository.** Not sibling repositories,
   not `$HOME` dotfiles, not system paths, not global installs. 
   Reading outside it is not allowed either without asking first.
2. **Never `git commit` without explicit permission**, every time. 
   "The change is finished" is not permission.
3. **Never switch branch on your own.** By default work on whatever branch HEAD is on, you can ask to switch if there are reasons to do so.
4. **Never stage in bulk.** No `git add -A`, `git add .`, `git add -u`,
   `git commit -a`. Enumerate paths.
5. **One commit per topic**, and every commit an agent authors ends its subject line with `[BOT]`. Never a commit called "update".
6. **`.temp/` is gitignored scratch space.** Read it, ask before writing, never
   overwrite without a named yes, never commit it, and never name its paths in a committed file.
7. **Size-check before reading any file.** A large generated file saturates the
   context window and blocks the user's work.
8. **Never start a long-running or destructive operation on your own initiative.** 
   Describe the command and let the user run it.
9. **Ask instead of investigating, when asking is cheaper**, and be brief.

## Commits

The commit format, the checks to run first and the setup for hooks and signing are in [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). 
Follow it, with one difference: for an agent the ` [BOT]` suffix is mandatory, not optional. 
The `commit-msg` hook accepts a subject without it only because it also checks hand-written commits, which must not carry the marker. Passing the hook does not make an unmarked agent commit acceptable.

## Further rules

A clone may also carry a fuller, machine-local rule set for your tool, covering the git workflow, commit identity, secrets, working style and language in more detail. 
**When one is present, follow it.** The rules in this file are the floor, not the whole of it, and nothing local may contradict them.
