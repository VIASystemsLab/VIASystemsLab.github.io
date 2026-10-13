#!/bin/sh
#
# Refuse a commit that adds a machine-local absolute path: where this clone
# lives, the committer's home directory, or anyone's home on macOS or Windows
# (a name under the Users directory). The path exists on one machine only, so
# to everyone else it is a dangling reference, and it publishes the account
# name it contains besides. Only added lines are checked, so a file that
# already carries such a path can still be edited.
#
# Run by pre-commit; see .pre-commit-config.yaml.

set -e

root=$(git rev-parse --show-toplevel) || exit 1

# A home of / (some containers) would match every line, so it is skipped.
home=${HOME:-}
[ "$home" = / ] && home=

found=$(git diff --cached --no-color --no-ext-diff -U0 --diff-filter=ACMR |
    awk -v root="$root" -v home="$home" '
        /^\+\+\+ / { file = substr($0, 7); next }
        /^\+/ {
            line = substr($0, 2)
            if (index(line, root) || (home != "" && index(line, home)) ||
                line ~ /\/Users\/[A-Za-z0-9._-]+/ || line ~ /[A-Za-z]:\\+Users\\+[A-Za-z0-9._-]+/)
                printf "  %s: %s\n", file, substr(line, 1, 100)
        }')

if [ -n "$found" ]; then
    echo "pre-commit: staged lines add a machine-local absolute path" >&2
    printf '%s\n' "$found" >&2
    echo "Write it relative to the repository root instead." >&2
    exit 1
fi
