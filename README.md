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

### Other branches

`coursework` holds earlier project work from BYU-Idaho, kept for reference.
