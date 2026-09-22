# Solomon B. Pobee

PhD student in Computer Science at Brigham Young University, working in
human–computer interaction. My research looks at how interactive systems can
support youth athletes and coaches — particularly in clubs that operate without
a support staff, where performance, development and injury prevention all
compete for the same limited attention.

**[www.solomonbpobee.com](https://www.solomonbpobee.com)** · [Google Scholar](https://scholar.google.com/citations?user=02WgxKoAAAAJ) · [ORCID](https://orcid.org/0009-0007-5172-0410)

## Publications

- **Toward a Framework for the Design of Interactive Technology for Nature
  Recreation** — Jones, Kari, Reich, Ens, Liu, **Pobee**, Mueller.
  *International Journal of Human–Computer Interaction*, 41(18), 11691–11711,
  2025. [doi:10.1080/10447318.2024.2443808](https://doi.org/10.1080/10447318.2024.2443808)
- **MathBuddy: An LLM-Based Chatbot for Elementary Math Education** — Iqbal,
  **Pobee**, Adhikari, Schooley. *HCI International 2025 Late Breaking Papers*,
  LNCS, Springer, 392–403, 2026.
  [doi:10.1007/978-3-032-13174-4_25](https://doi.org/10.1007/978-3-032-13174-4_25)

---

## About this repository

This repository is the source of the site above. It is plain HTML, CSS and
JavaScript — no framework, no build tooling, no dependencies.

| File | Page |
|---|---|
| `index.html` | Home |
| `research.html` | Research areas |
| `projects.html` | Projects and repositories |
| `publications.html` | Publications with citations |
| `about.html` | About and contact |
| `cv.html` | Short web CV |

`styles.css` holds all styling and `script.js` all behaviour. The pages
themselves are generated — see below.

### Working on it

```bash
python build.py          # regenerate the pages from build.py
python check_links.py .  # validate every href and src
./start-local.sh         # preview at localhost:8000 (start-local.bat on Windows)
```

`build.py` is the source of truth: it holds the page content and the shared
shell, and writes the `.html` files. Editing an `.html` file directly will work
until the next build, then be overwritten.

Pages are written as `.html` but linked without the extension — `/research`
rather than `/research.html` — which GitHub Pages resolves on its own. The
local preview server does the same, so it matches production.

### Deploying

Pushing to `main` runs `.github/workflows/deploy.yml`, which refreshes the
LeetCode figures, rebuilds the pages, checks that every link is well formed and
every referenced file exists, and publishes to GitHub Pages. If either check
fails the deploy stops and the previous version stays live. The workflow also
runs daily so the LeetCode numbers stay current without a push.

`leetcode.json` holds those figures and is refreshed by `update_leetcode.py`.
That script never blocks a deploy: if LeetCode is unreachable or answers oddly,
it warns and leaves the last known-good numbers in place.

### Adding a publication

Publications are grouped by kind on the page: Journal Articles, Conference
Papers, Book Chapters, Workshop Papers, and Posters & Extended Abstracts, in
that order. A kind with nothing in it is not shown at all, so the page never
carries an empty heading — add the first conference paper and the Conference
Papers section appears in the right place on the next build.

Both live in `build.py`, with a worked template in the comments:

1. Add the citation to `CITATIONS` under a new id (`"c3"`, then `"c4"`).
2. Copy the template from the comment above `PUB_GROUPS` into the matching
   list in `PUBS`, and fill in the parts in capitals.
3. `python build.py`, then `python check.py`.

The comments there say which kind is which, what `TOPIC` has to match, and
what to change if you would rather file the MathBuddy paper as a conference
paper than a book chapter.

### The CV download and print

Put a PDF in `assets/cv/` and both buttons on the CV page use it: **Download
PDF** saves it, and **Print CV** sends that file to the printer rather than
the web page.

Leave the folder empty and the Download button is left out, so the page never
links to a file that is not there — a dead reference fails the deploy's asset
check and stops the site publishing. Print then falls back to printing the CV
page itself, using the print rules in `styles.css`, so the button is never
dead.

The filename is yours to choose. If there is more than one PDF the last by
name wins, so dated names like `cv-2026-09.pdf` sort the newest to the end and
older versions can stay in the folder.

Printing the PDF loads it in an offscreen iframe and prints that. Safari will
not print a PDF in an iframe, so there it opens in a new tab instead and the
reader prints from the PDF viewer.

### Other branches

`coursework` holds earlier project work from BYU-Idaho, kept for reference.
