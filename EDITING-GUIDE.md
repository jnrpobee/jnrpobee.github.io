# Website editing guide

This guide explains how this website is organized, where to make changes, how
to add content, and how to check a change before publishing it. For a shorter
project overview, see [README.md](README.md).

## The one rule to remember

**Edit `build.py`, not the generated `.html` pages.**

`build.py` contains the page content and shared layout. Running it generates
`index.html`, `research.html`, `projects.html`, and the other HTML files. A
direct edit to one of those generated files will be erased by the next build
and by the deployment workflow.

The normal flow is:

```text
build.py + styles.css + script.js + assets/
                    |
                    |  python build.py
                    v
       generated HTML, sitemap.xml, robots.txt
                    |
                    |  push to main
                    v
                GitHub Pages
```

## Quick start

The site has no package manager or third-party dependencies. You only need
Python 3 and a web browser.

On Windows PowerShell:

```powershell
py build.py
py check.py
.\start-local.bat
```

On macOS or Linux:

```bash
python3 build.py
python3 check.py
./start-local.sh
```

Open <http://localhost:8000> to preview the site. Press `Ctrl+C` in the server
window to stop it. If port 8000 is already in use, run `python serve.py 8001`
and open <http://localhost:8001>.

`check.py` runs the build itself, so it is the most important command before a
commit. Running `build.py` separately is still useful when you want to preview
immediately.

## Project map

| File or folder | Purpose | Edit directly? |
|---|---|---|
| `build.py` | Page content, navigation, metadata, citations, posts, and the shared HTML shell | Yes |
| `styles.css` | Light and dark themes, layout, typography, responsive rules, and print styles | Yes |
| `script.js` | Menus, theme switching, search, citations, copy buttons, and other interactions | Yes |
| `assets/` | Portraits, logos, icons, social image, and the downloadable CV | Yes |
| `leetcode.json` | Last known LeetCode figures, normally refreshed by automation | Usually no |
| `index.html`, `about.html`, etc. | Generated pages | **No** |
| `sitemap.xml`, `robots.txt` | Generated search-engine files | **No** |
| `serve.py` and `start-local.*` | Local preview server | Only when changing the development setup |
| `check.py` and `check_links.py` | Pre-publish validation | Only when changing validation rules |
| `.github/workflows/deploy.yml` | GitHub Pages deployment | Only when changing deployment |
| `GITHUB.md` | Initial GitHub Pages and domain setup notes | Reference |
| `DEPLOY.md` | Alternative Cloudflare Pages setup notes | Reference |

## How to read `build.py`

The file is long, but it is arranged in sections. Use your editor's search to
jump to one of these names:

1. `BASE_URL`, `NAV`, and `UNLISTED` define the domain and page structure.
2. `CITATIONS`, `PUB_GROUPS`, and `PUBS` build the publications page.
3. `POSTS` contains entries for the unlisted notes page.
4. `SOCIALS` supplies the social links in the shared footer.
5. `PAGES` maps each output filename to a content key, page title, and search
   description.
6. `SHELL` is the shared document structure used by every page.
7. `BODY["home"]`, `BODY["research"]`, and the other `BODY` entries contain
   the visible page content.
8. The loop near the bottom combines `SHELL` and `BODY`, then writes all of the
   generated files.

Most routine content updates happen inside a `BODY[...]` block. These blocks
are HTML stored inside Python triple-quoted strings, so preserve the opening
and closing `"""` markers.

## Edit text on an existing page

1. Copy a distinctive sentence from the website.
2. Search for it in `build.py`.
3. Make the change in the matching `BODY[...]` section.
4. Run `py check.py` or `python3 check.py`.
5. Refresh the local preview and inspect the result.

For example, homepage content is in `BODY["home"]`, contact information is in
`BODY["about"]`, and the web CV is in `BODY["cv"]`.

The content uses HTML. Common patterns are:

```html
<h2>A section heading</h2>
<p>A paragraph with <strong>important text</strong>.</p>
<a class="text-link" href="https://example.com/">A link</a>
<ul>
  <li>A list item</li>
</ul>
```

Use `&amp;` for a literal ampersand in HTML text. When adding an external link
that opens a new tab, keep `target="_blank" rel="noopener"` together.

## Add or change a link

Internal links in `build.py` use filenames:

```html
<a href="research.html">Research</a>
```

The generator changes that to `/research` in the finished page. Do not change
the source link to a local computer path such as `C:\...`.

Other useful link formats are:

```html
<a href="https://example.com/">External website</a>
<a href="mailto:jnrpobee@byu.edu">Send email</a>
<a href="assets/cv/example.pdf">Local file</a>
```

After adding a link, run the full `check.py` command. It catches malformed
links and references to local files that do not exist.

## Add or replace an image

1. Put the image in `assets/`. Use a short, lowercase, hyphenated filename.
2. Reference it from a `BODY[...]` block:

   ```html
   <img src="assets/project-photo.jpg"
        alt="A concise description of the image"
        loading="lazy" decoding="async">
   ```

3. Give informative images meaningful `alt` text. Use `alt=""` only for an
   image that is entirely decorative.
4. Run `check.py` to confirm the path is correct.

The current portraits are `assets/portrait.jpg` and
`assets/portrait-square.jpg`. The link-preview image is
`assets/og-image.jpg`. Replacing a file while keeping the same filename updates
every place that already uses it.

## Add a project

The complete project list is inside `BODY["projects"]` in `build.py`.

1. Find an existing `<article class="project-card">...</article>` block.
2. Copy the entire block inside the same `project-grid`.
3. Change its label, heading, description, artwork or image, and link.
4. If it should also be featured on the homepage, add or update the matching
   card in `BODY["home"]`.
5. Build, check, and preview at both desktop and phone widths.

Repository cards use `<a class="repo" ...>` blocks in `BODY["projects"]`.
Their `data-repo="owner/name"` value lets `script.js` request current GitHub
information when the page loads. Keep a written description in the HTML so
the card remains useful if that request is unavailable.

## Add a publication

`build.py` includes a copyable publication template immediately above
`PUB_GROUPS`. The required steps are:

1. Add a new entry to `CITATIONS` using the next ID (`c3`, `c4`, and so on).
   BibTeX is enough to begin; the other supported formats can be added later.
2. Copy the publication template into the correct list in `PUBS`: `journal`,
   `conference`, `chapter`, `workshop`, or `poster`.
3. Use the same citation ID in `data-cite`, `aria-controls`, and
   `<!--CITE:...-->`.
4. Set `data-topic` to an existing filter value such as `nature` or
   `learning`. For a new topic, also add a matching filter button in
   `BODY["publications"]`.
5. Update the initial publication total in `BODY["publications"]`. JavaScript
   updates it after a search or filter is used, but the HTML should start with
   the correct number.
6. Update `SCHOLAR_LD` so search engines receive the new scholarly record.
7. Review any summary that mentions the publication count or selected work,
   especially `BODY["home"]` and `BODY["cv"]`.
8. Run `check.py`, then test the topic filter, citation tabs, copy button, and
   DOI link in the preview.

Keep newest publications first within their group.

## Add a note or blog post

The notes page is intentionally unlisted: it is not in the main navigation or
sitemap, but anyone with its address can read it. Do not use it for private
information.

Add a dictionary inside the `POSTS = [...]` list in `build.py`:

```python
POSTS = [
    {
        "date": "2026-10-04",
        "title": "Post title",
        "body": """
          <p>First paragraph.</p>
          <p>Second paragraph with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
]
```

Use an ISO date in `YYYY-MM-DD` form. Posts are sorted newest first during the
build. The post body may use the HTML elements already styled for notes:
`p`, `a.text-link`, `strong`, `em`, `ul`, `li`, and `blockquote`.

## Update the CV

There are two related CVs:

- The visible web CV is in `BODY["cv"]` in `build.py`.
- The downloadable PDF is in `assets/cv/`.

They do not update each other, so revise both when the underlying information
changes. If the folder contains more than one PDF, the filename that sorts
last alphabetically is used. A dated filename such as `cv-2026-10.pdf` makes
that rule predictable.

If there is no PDF, the download button is omitted and the print button prints
the web page instead.

## Change navigation, metadata, or shared content

- Change navigation order and labels in `NAV`.
- Change the browser title and search description in `PAGES`.
- Change footer profile links in `SOCIALS`.
- Change the canonical domain in `BASE_URL`.
- Change shared header, footer, command-palette markup, or document metadata in
  `SHELL`.
- Change command-palette destinations in the `commands` list in `script.js`.

Because these values are shared, always inspect more than one page after a
change.

## Add a new page

Adding a page touches several connected lists:

1. Add `BODY["newkey"] = """..."""` in `build.py`.
2. Add a row to `PAGES` with the output filename, the same content key, its
   browser title, and its search description.
3. Add the filename and label to `NAV` if it should be a normal public page.
   This automatically adds it to the header, page-to-page pager, and sitemap.
4. If it should behave like the notes page instead, add it to `UNLISTED`. An
   unlisted page receives `noindex` and is omitted from navigation and the
   sitemap; unlisted does not mean private.
5. Add it to the command-palette `commands` in `script.js` if visitors should
   be able to find it there.
6. Add any page-specific styles to `styles.css`.
7. Run the build and checks, then test the clean URL such as `/newpage`.

Every generated page must appear in either `NAV` or `UNLISTED` so its internal
filename links can be converted to clean URLs.

## Change colors, typography, or layout

Theme colors and fonts are CSS custom properties near the top of `styles.css`.

- The first `:root` block defines the light theme.
- The `@media (prefers-color-scheme:dark)` block defines automatic dark mode.
- The `:root[data-theme="dark"]` block defines dark mode chosen with the theme
  switch.

When changing a dark-theme variable, update it in both dark blocks or automatic
and manually selected dark mode will look different. Reuse existing variables
such as `--text`, `--accent`, `--bg`, and `--border` instead of scattering new
literal colors through later rules.

The rest of the stylesheet is labeled by component: header, hero, project
cards, publications, CV, footer, responsive rules, print rules, and the
LeetCode panel. Place a new rule beside the component it affects and check both
themes, narrow screens, and reduced-motion behavior.

## Change interactive behavior

All browser behavior is in `script.js`, using plain JavaScript with no build
step. The file is divided by labeled comments. Shared values such as `EMAIL`
and `GH_USER` are near the top.

When changing JavaScript:

1. Keep the page usable when JavaScript is unavailable.
2. Preserve keyboard access and the existing ARIA attributes.
3. Test at least the desktop menu, mobile menu, theme switch, command palette,
   and the feature you changed.
4. Check the browser console for errors.

## Validate before committing

Run:

```powershell
py check.py
```

or:

```bash
python3 check.py
```

The check rebuilds the site and verifies links, referenced assets, leftover
template markers, repeatable output, line endings, required files, and
JavaScript syntax. A passing run is the best indication that GitHub Pages will
accept the same build.

Also inspect the preview manually:

- Check the edited page in light and dark themes.
- Resize to a phone width and confirm nothing is cut off.
- Follow every new link.
- Confirm images have useful alternative text.
- Navigate interactive controls with the keyboard.
- Review the generated files in `git diff`; source and generated output should
  be committed together.

Optional: run `python install-hooks.py` once in a clone. It installs the
included pre-push hook, which runs the same checks before allowing a push.

## Publish the change

Pushing a commit to `main` starts `.github/workflows/deploy.yml`. The workflow
refreshes LeetCode data when possible, rebuilds the site from `build.py`, runs
the checks, and publishes the assembled public files to GitHub Pages.

If a check fails, the workflow stops and the previously published version
remains live. Open the repository's **Actions** tab to read the error. Do not
edit the live generated HTML as a workaround; correct the source, rebuild, and
push another commit.

## Common problems

### My change disappeared

You probably edited a generated `.html` file. Make the same change in
`build.py`, then rebuild.

### The build reports a Python syntax error

Check the area you just edited for an unclosed `"""` string, a missing comma
in a list or dictionary, or unmatched brackets.

### A local link works poorly when I double-click an HTML file

Use `start-local.bat`, `start-local.sh`, or `python serve.py`. The preview
server supports the same extensionless URLs as the deployed site.

### A referenced file is missing

Check its spelling, capitalization, and path. Web hosts are case-sensitive
even when a Windows development machine is not.

### The page looks right in one dark mode but not the other

The automatic and explicit dark-theme variables are separate blocks near the
top of `styles.css`. Keep their corresponding values in sync.
