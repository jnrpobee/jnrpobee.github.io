# Website editing guide

This guide explains how this website is organized, where to make changes, how
to add content, and how to check a change before publishing it. For a shorter
project overview, see [README.md](README.md).

**Keep this file current.** It is the documentation for the site, and it is
only useful while it matches the code. When you add a feature, change where
something lives, or rename a file, update the matching section here in the
same commit. A guide that sends you to the wrong file is worse than no guide.

## The one rule to remember

**Edit the Python source, not the generated `.html` pages.**

Running `build.py` generates `index.html`, `research.html`, `blog.html` and
the rest. A direct edit to one of those generated files will be erased by the
next build and by the deployment workflow.

The normal flow is:

```text
build.py + core.py + shell.py + pages/ + notes.py + posts.py
       + pubs.py + leetcode.py + art.py + styles.css + script.js + assets/
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

Open <http://localhost:8001> to preview the site. Press `Ctrl+C` in the server
window to stop it. If port 8001 is already in use, run `python serve.py 8002`
and open <http://localhost:8002>.

`check.py` runs the build itself, so it is the most important command before a
commit. Running `build.py` separately is still useful when you want to preview
immediately.

## Project map

The generator used to be one 2,376-line `build.py`. It is now split by
subject, so each file is short enough to read in one sitting.

| File or folder | Purpose | Edit directly? |
|---|---|---|
| `posts.py` | The blog: your categories and your posts. **The file to open to write something.** | Yes |
| `pages/` | One module per page, holding that page's markup — `home.py`, `research.py`, `projects.py`, `publications.py`, `about.py`, `blog.py`, `cv.py` | Yes |
| `pubs.py` | Publications and the citation panel under each one | Yes |
| `core.py` | Where the site lives (`BASE_URL`), the nav order, clean URLs | Occasionally |
| `shell.py` | The frame every page is poured into: head, nav, footer, pager, structured data | Occasionally |
| `notes.py` | The blog's machinery — board, list, filters, calendar, tiles, colours | Rarely |
| `leetcode.py` | The LeetCode panel on the projects page | Rarely |
| `art.py` | The two drawings the home and projects pages share | Rarely |
| `build.py` | Assembles everything and writes the files. Holds no content. | Rarely |
| `styles.css` | Light and dark themes, layout, typography, responsive rules, print styles | Yes |
| `script.js` | Menus, theme switching, search, citations, blog filters, copy buttons | Yes |
| `assets/` | Portraits, logos, icons, social image, blog images, the downloadable CV | Yes |
| `leetcode.json` | Last known LeetCode figures, normally refreshed by automation | Usually no |
| `index.html`, `about.html`, etc. | Generated pages | **No** |
| `sitemap.xml`, `robots.txt` | Generated search-engine files | **No** |
| `serve.py` and `start-local.*` | Local preview server | Only when changing the development setup |
| `check.py` and `check_links.py` | Pre-publish validation | Only when changing validation rules |
| `.github/workflows/deploy.yml` | GitHub Pages deployment | Only when changing deployment |
| `GITHUB.md` | Initial GitHub Pages and domain setup notes | Reference |
| `DEPLOY.md` | Alternative Cloudflare Pages setup notes | Reference |

## Where things live

Start from what you want to change:

| I want to… | Open |
|---|---|
| Write a blog post | `posts.py` |
| Add a blog category | `posts.py` (`BLOG_CATEGORIES`) |
| Change the words on a page | `pages/<name>.py` |
| Add a publication | `pubs.py` |
| Add a project card | `pages/projects.py` |
| Update the web CV | `pages/cv.py` |
| Change the nav order or the domain | `core.py` |
| Change page titles, search descriptions, footer links | `shell.py` |
| Change a colour, spacing, or a breakpoint | `styles.css` |
| Change something that happens on click | `script.js` |

Page markup lives in HTML stored inside Python triple-quoted strings, so
preserve the opening and closing `"""` markers.

## Edit text on an existing page

Every page has its own file:

| Page | File |
|---|---|
| Home | `pages/home.py` |
| Research | `pages/research.py` |
| Projects | `pages/projects.py` |
| Publications | `pages/publications.py` (the list itself is in `pubs.py`) |
| About | `pages/about.py` |
| CV | `pages/cv.py` |
| Blog | `pages/blog.py` (the writing is in `posts.py`) |
| 404 | `build.py`, as `NOT_FOUND_BODY` |

1. Copy a distinctive sentence from the website.
2. Search for it in `pages/`.
3. Make the change in the matching module.
4. Run `py check.py` or `python3 check.py`.
5. Refresh the local preview and inspect the result.

Research and About are the simple ones: prose and headings, nothing generated,
no marks. Editing the file is the whole job.

**The home page duplicates two project cards** that also live in
`pages/projects.py` — the same drawings, a shorter description. Rename a
project or change its link and there are two files to edit. Nothing checks
that they still agree, so it is worth searching for the project's name across
`pages/` rather than trusting memory.

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

Internal links in the page modules use filenames:

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
2. Reference it from the page module:

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

Nothing resizes an image for you. Anything wider than about 1600px is wasted
on this layout, and a phone photo dropped in unedited can be several megabytes.

## Add a project

The complete project list is in `pages/projects.py`.

1. Find an existing `<article class="project-card">...</article>` block.
2. Copy the entire block inside the same `project-grid`.
3. Change its label, heading, description, artwork or image, and link.
4. If it should also be featured on the homepage, add or update the matching
   card in `pages/home.py`.
5. Build, check, and preview at both desktop and phone widths.

Repository cards use `<a class="repo" ...>` blocks in the same file. Their
`data-repo="owner/name"` value lets `script.js` request current GitHub
information when the page loads. Keep a written description in the HTML so
the card remains useful if that request is unavailable.

## Add a publication

`pubs.py` includes a copyable template under `HOW TO ADD A PUBLICATION`,
immediately above `PUB_GROUPS`. The required steps are:

1. Add a new entry to `CITATIONS` using the next ID (`c3`, `c4`, and so on).
   BibTeX is enough to begin; the other supported formats can be added later,
   and the tabs are generated from whichever keys are present.
2. Copy the publication template into the correct list in `PUBS`: `journal`,
   `conference`, `chapter`, `workshop`, `poster`, or `abstract`.
3. Use the same citation ID in all three places — `data-cite`,
   `aria-controls`, and `<!--CITE:...-->`. A mismatch is the usual cause of a
   Cite button that opens nothing.
4. The filter chips above the list are generated from the kinds in use, so
   there is nothing to add for them: put the entry in the right list in `PUBS`
   and its chip appears. A kind with no publications gets no chip, and with
   only one kind on the page no chips are written at all — there would be
   nothing to choose between.

   The page used to filter by subject area instead, with hand-written chips
   in `pages/publications.py`. With two papers each chip narrowed the list to
   exactly one entry, which is a table of contents wearing a filter's clothes.
   `data-topic` on a publication is now unused; leaving one in does no harm.
5. Update the initial publication total in `pages/publications.py` — the
   `id="pub-count"` span. JavaScript updates it after a search or filter, but
   the HTML should start with the correct number.
6. Update `SCHOLAR_LD` in `shell.py` so search engines receive the new
   scholarly record.
7. Review any summary that mentions the publication count or selected work,
   especially `pages/home.py` and `pages/cv.py`.
8. Run `check.py`, then test the topic filter, citation tabs, copy button, and
   DOI link in the preview.

Keep newest publications first within their group.

## The blog

The blog is an unlisted page: it is not in the navigation or the sitemap and
it carries a `noindex` tag, but anyone given the address can read it. Unlisted
is not private. Do not put anything there you would mind a stranger reading.

It is reached by the small dot beside the header note, and by the copyright
line in the footer on a phone.

### Add a post

Open `posts.py` and add a dictionary at the top of `POSTS`:

```python
    {
        "date": "2026-10-04",
        "category": "lifestyle",
        "title": "Post title",
        "body": """
          <p>First paragraph.</p>
          <p>Second paragraph with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
```

`date` is ISO `YYYY-MM-DD`; the page rewrites it into the reader's own format.
`category` must be one of the keys in `BLOG_CATEGORIES`. The body may use the
elements already styled for notes: `p`, `a.text-link`, `strong`, `em`, `ul`,
`li`, and `blockquote`.

Posts are sorted newest first during the build. There is only one blog page —
categories are filters on it, not separate pages.

Optional keys:

- `"summary"` — the teaser shown before a note is opened. Without it, the
  first sentence is used.
- `"image"` — a picture at the top of the post body. See below.
- `"pin": True` — keeps the post on the board in the hero, and stops that
  board slot rotating away from it.
- `"fasten"` — what holds the note to the page: `pin`, `tape`, `clip`,
  `bulldog` or `dot`. Left out, they rotate so no two notes in a row match.

### Put a picture in a post

Put the file in `assets/blog/`, then:

```python
        "image": {
            "src": "assets/blog/whiteboard.jpg",
            "alt": "A whiteboard covered in a session plan",
            "caption": "Optional line under the picture.",
        },
```

`alt` is **required** — the build stops without it, rather than shipping a
picture that is invisible to anyone using a screen reader. If the image really
is decorative, write `"alt": ""` on purpose. A `src` that does not exist fails
`check.py`. Drop `caption` and you simply get the image.

The short form `"image": "assets/blog/whiteboard.jpg"` gives the picture empty
alt text, so use it only for something genuinely decorative.

### Add a category

In `posts.py`, add an entry to `BLOG_CATEGORIES`. Either form works:

```python
    "campus": "Campus Life",

    "campus": {"label": "Campus Life",
               "blurb": "Graduate school at BYU: the work and the pace."},
```

The `blurb` is the line under the name on that category's tile at the foot of
the blog. A category with no blurb still gets a tile.

**Colour is not set here.** Each category takes the next hue in the order this
dictionary declares them, so a category keeps its colour when you add another
below it. The hue shows on the note's border, on the dot beside its label, and
on the tile's top rule.

There are six hues. The seventh category and everything after it gets a pair
of them in a diagonal stripe, which is worth 21 categories before anything
repeats. That happens automatically.

The six are `--cat-1` to `--cat-6` in `styles.css`. They were not chosen by
eye: they were searched for and then measured, so every one clears 3:1 against
all nine surfaces the site puts them on, and every pair stays apart under
colour-blind vision with all six on screen at once, which is what the tiles do.
Swapping one by eye will quietly break a pair.

### What the reader gets, without you doing anything

- **Reading time.** Counted from the words. Under a minute it shows seconds to
  the nearest ten; at a minute and over, whole minutes.
- **A permanent link.** Built from the date and the title, so retitling a post
  does not break a link somebody saved.
- **The board.** The three cards in the hero carry notes, the highlight moves
  between them, and once there are more notes than slots the cards turn over so
  everything gets its turn up there. A pinned note holds its slot.
- **Filters, paging and a month calendar.** All generated from the posts. No
  control needs adding when you write something.

All of that lives in `notes.py`. You should not need to open it.

## Update the CV

There are two related CVs:

- The visible web CV is in `pages/cv.py`.
- The downloadable PDF is in `assets/cv/`.

They do not update each other, so revise both when the underlying information
changes. If the folder contains more than one PDF, the filename that sorts
last alphabetically is used. A dated filename such as `cv-2026-10.pdf` makes
that rule predictable.

If there is no PDF, the download button is omitted and the print button prints
the web page instead.

## Change navigation, metadata, or shared content

- Change navigation order and labels in `NAV`, in `core.py`.
- Change the canonical domain in `BASE_URL`, in `core.py`.
- Change the browser title and search description in `PAGES`, in `shell.py`.
- Change footer profile links in `SOCIALS`, in `shell.py`.
- Change shared header, footer, command-palette markup, or document metadata in
  `SHELL`, in `shell.py`.
- Change what the blog is called in `BLOG_NAME`, in `core.py`. It appears in
  the browser tab, the blog's own nav, and the labels a screen reader reads on
  the two doors into it.
- Change command-palette destinations in the `commands` list in `script.js`.

Because these values are shared, always inspect more than one page after a
change.

## Add a new page

Adding a page touches several connected files:

1. Create `pages/newkey.py` holding `BODY = {}` and
   `BODY["newkey"] = """..."""`.
2. Register it in `pages/__init__.py` — one `from . import newkey as _newkey`
   line and one `BODY.update(_newkey.BODY)` line, following the pattern there.
3. Add a row to `PAGES` in `shell.py` with the output filename, the same
   content key, its browser title, and its search description.
4. Add the filename and label to `NAV` in `core.py` if it should be a normal
   public page. This automatically adds it to the header, the page-to-page
   pager, and the sitemap.
5. If it should behave like the blog instead, add it to `UNLISTED` in
   `core.py`. An unlisted page receives `noindex` and is omitted from
   navigation and the sitemap; unlisted does not mean private.
6. Add it to the command-palette `commands` in `script.js` if visitors should
   be able to find it there.
7. Add any page-specific styles to `styles.css`.
8. Run the build and checks, then test the clean URL such as `/newpage`.

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

The six category hues (`--cat-1` to `--cat-6`) sit in the same three blocks.
Read the comment above them before changing one — they are a measured set, not
a palette picked by eye.

The rest of the stylesheet is labeled by component: header, hero, project
cards, publications, the blog's board and notes, CV, footer, responsive rules,
print rules, and the LeetCode panel. Place a new rule beside the component it
affects and check both themes, narrow screens, and reduced-motion behavior.

## Change interactive behavior

All browser behavior is in `script.js`, using plain JavaScript with no build
step. The file is divided by labeled comments. Shared values such as `EMAIL`
and `GH_USER` are near the top.

When changing JavaScript:

1. Keep the page usable when JavaScript is unavailable. The blog is the test
   case: with scripts off the notes all render, the board still animates in
   CSS, and every control that needs script stays hidden.
2. Preserve keyboard access and the existing ARIA attributes.
3. Test at least the desktop menu, mobile menu, theme switch, command palette,
   and the feature you changed.
4. Check the browser console for errors.

Selectors are easy to get wrong across pages. The blog filters and the
publications filters both use `.chip`, so a selector written as `$$('.chip')`
will reach across pages and quietly break one of them. Scope them.

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
refreshes LeetCode data when possible, rebuilds the site from source, runs the
checks, and publishes the assembled public files to GitHub Pages.

If a check fails, the workflow stops and the previously published version
remains live. Open the repository's **Actions** tab to read the error. Do not
edit the live generated HTML as a workaround; correct the source, rebuild, and
push another commit.

## Common problems

### My change disappeared

You probably edited a generated `.html` file. Make the same change in the
matching source module, then rebuild.

### The build reports a Python syntax error

Check the area you just edited for an unclosed `"""` string, a missing comma
in a list or dictionary, or unmatched brackets.

### `Unknown blog category 'Inside The Pod'`

You used a category's display label where its key belongs. In
`BLOG_CATEGORIES` the left side is the key a post refers to and the right side
is what readers see. The post's `"category"` needs the key.

### The push is refused because a generated file "differs from what you committed"

You committed a source change without its regenerated HTML, or the reverse.
CI rebuilds from source, so a mismatch means GitHub would publish something
other than what you previewed. Run `python build.py`, then `git add -A` and
commit again.

### `Unable to create '.git/index.lock': File exists`

A previous git command did not finish. Check nothing is running
(`tasklist | grep -i git`), confirm the lock file is zero bytes and older than
your last command (`ls -la .git/*.lock`), then remove it and retry.

### A local link works poorly when I double-click an HTML file

Use `start-local.bat`, `start-local.sh`, or `python serve.py`. The preview
server supports the same extensionless URLs as the deployed site.

### A referenced file is missing

Check its spelling, capitalization, and path. Web hosts are case-sensitive
even when a Windows development machine is not.

### The page looks right in one dark mode but not the other

The automatic and explicit dark-theme variables are separate blocks near the
top of `styles.css`. Keep their corresponding values in sync.

### A lit control turns unreadable when the cursor is on it

A hover rule is beating the rule that fills the control with the accent.
`--accent-ink` is the only colour that is legible on the accent in both
themes; a hover rule that sets `--text` instead will measure about 1.15:1.
Write the hover variant explicitly so it out-ranks the plain `:hover`.
