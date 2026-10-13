# AGENTS.md: VIA Systems Lab website

The public website of VIA Systems Lab at the University of Verona: a static HTML/CSS site on Pure CSS, served through GitHub Pages.

## Core rules

These are binding. They override any general default behaviour.

1. **Check every prompt before acting on it.** If it is ambiguous, incomplete
   or looks meant for a different conversation, stop and ask first.
2. **Never touch anything outside this repository.** Not sibling repositories,
   not `$HOME` dotfiles, not system paths, not global installs. Reading outside
   it is not allowed either without asking first. The one exception is the
   session scratchpad directory, for throwaway files.
3. **Never `git commit` without explicit permission**, every time. "The change
   is finished" is not permission.
4. **Silence is never a yes.** Only an explicit answer counts. If a reply skips
   a question, ask it again before acting on it.
5. **The default branch is never the default choice.** Before the first commit,
   ask which branch the work goes on. The default branch only when the user
   says so. Never switch branch without a yes.
6. **Never stage in bulk.** No `git add -A`, `git add .`, `git add -u`,
   `git commit -a`. Enumerate paths.
7. **One commit per topic**, and every commit an agent authors ends its subject
   line with `[BOT]`. Never a commit called "update".
8. **`.temp/` is gitignored scratch space.** Read it, say which file and why
   before writing, never overwrite without a named yes, never commit it, and
   never point a committed file at anything in it.
9. **Size-check before reading any file.** A large generated file saturates the
   context window and blocks the user's work.
10. **Never start a long-running or destructive operation on your own
    initiative.** Describe the command and let the user run it.
11. **Ask instead of investigating, when asking is cheaper**, and be brief.
12. **Never reach the network without a yes**, every time. Any request to a
    host other than localhost needs one, including web searches, `git fetch`
    and package installs. Name the URL, what is sent, why, and whether it is
    required or nice to have, then wait.

## Commits

The commit format, the checks to run first and the setup for hooks and signing are in [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). 
Follow it, with one difference: for an agent the ` [BOT]` suffix is mandatory, not optional. 
The `commit-msg` hook accepts a subject without it only because it also checks hand-written commits, which must not carry the marker. Passing the hook does not make an unmarked agent commit acceptable.

## Other instruction files

Coding agents keep their instructions in files of their own. Look for each of
these in the repository root and read every one you find:
`CLAUDE.md`, `.claude/rules/`, `GEMINI.md`, `.cursor/rules/`, `.cursorrules`,
`.github/copilot-instructions.md`, `.windsurfrules`, `.agent-defs/`. The rules
above are the floor. Where two rules differ only in how strict they are, follow
the stricter one. Where they cannot both be followed, stop and ask which one
applies.

## Project guides

The guides in `docs/` say how the site is built and written: the Language
section of [docs/DESIGN-GUIDE.md](docs/DESIGN-GUIDE.md) before writing or
editing copy, the rest of it before changing markup or styles, and
[docs/METADATA.md](docs/METADATA.md) before adding a person, a project or a
publication.
