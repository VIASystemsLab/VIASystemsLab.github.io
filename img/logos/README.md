# Third-party logos

These are **not** the lab's marks and **not** covered by the generative-AI
provenance statement in `humans.txt`. They are the trademarks and official
emblems of their owners, reproduced here to acknowledge funding and
affiliation, which Horizon Europe grant agreements require.

| File | Owner | Used for |
| --- | --- | --- |
| `uvrdlls.png` | University of Verona | Institutional affiliation, shown in the site footer. |
| `euflag.png` | European Union | Funding acknowledgement, shown in the site footer beside "Funded by the European Union". |
| `armada-logo-w-h.png` | ARMADA project | The ARMADA record on `projects.html`. Flat white, horizontal: used as supplied on a dark page, inverted to black on a light one. |
| `datagems-logo-w.png` | DataGEMS project | The DataGEMS record on `projects.html`. Flat white, horizontal, same treatment. Only 387px wide, so it is never scaled up past that. |
| `armada-logo-b-v.png` | ARMADA project | Flat black, vertical. Unused — the horizontal cut suits the record better. |
| `armada-logo-c-v.png` | ARMADA project | Full colour, vertical. Unused: a gradient mark cannot follow the page's colour scheme without being put in a box. |
| `armada-logo-c-disc.png` | ARMADA project | Logo plus the full funding disclaimer and EU emblem. Unused: the disclaimer is set as live text in the footer instead, so it stays readable, selectable and translatable. |
| `armada-bg-gradient.png`, `armada-bg-lines.png` | ARMADA project | Brand backgrounds. Unused: they belong to ARMADA's visual identity, not the lab's. |

Web-sized derivatives are generated into `img/` by `tools/build_assets.py`.
Do not edit the generated files.

## Rules when using them

- Reproduce them as supplied. Do not recolour, redraw, stretch or crop them.
  The one permitted adjustment is inverting a **flat monochrome** mark so it
  reads against the opposite background: `uvrdlls.png` (black) on the dark
  footer, and `armada-logo-w-h.png` (white) on a light page. Both are a single
  ink on transparency, so inverting reproduces the other cut exactly. Never
  invert a mark that carries more than one colour.
- The EU emblem must keep its own blue field and its 3:2 proportions, and must
  never be inverted or tinted. It always appears next to the words "Funded by
  the European Union".
- Give every one of them real alternative text naming the owner.
