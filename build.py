#!/usr/bin/env python3
"""Generate the static pages from one shared shell.

This file does the assembling and nothing else. What goes into a page
lives beside it:

    core.py       where the site lives, the nav, clean URLs
    shell.py      the frame every page is poured into
    pages/        one module per page, holding that page's markup
    notes.py      the blog - posts, board, filters, tiles, colours
    pubs.py       publications and their citation panels
    leetcode.py   the LeetCode panel on the projects page
    art.py        the two drawings the home and projects pages share

Run it the same way as always: python build.py
"""
from core import (BASE_URL, BLOG_NAME, NAV, OUT, UNLISTED, clean_links,
                  public_path, write)
from shell import (JSONLD, PAGES, SCHOLAR_LD, SHELL, SOCIALS, header_brand,
                   nav_links, pager)
from pages import BODY, CV_MARK, cv_actions
from pubs import CITATIONS, PUB_MARK, cite_panel, pub_groups
from leetcode import LC_MARK, lc_section
from notes import (BLOG_POSTS_MARK, CAT_COLOURS_MARK, CAT_TILES_MARK,
                   NOTES_END_MARK, NOTES_TALLY_MARK, NOTE_CARDS_MARK,
                   NOTE_COUNT_MARK, NOTE_DATA_MARK, blog_posts, cat_colours,
                   cat_tiles, note_cards, note_data, notes_end, notes_tally,
                   playground_attrs)

# The footer's profile links, built once: every page carries the same set,
# so there is nothing per-page to work out inside the loop.
socials_html = "\n".join(
    '          <a href="%s" target="_blank" rel="noopener">%s</a>' % (u, n) for u, n in SOCIALS
)

# 404 is the one page with no module of its own. It is a few lines, it is
# not in PAGES, and it is written after the loop with its own SHELL.format
# call - a page/ module for it would be a file to maintain for something
# nobody navigates to on purpose.
NOT_FOUND_BODY = """      <section class="pad">
        <p class="eyebrow enter-1">404 <span>&times;</span> NOT FOUND</p>
        <h1 class="enter-1">This page doesn\u2019t exist.</h1>
        <p class="lead enter-2">The link may be out of date, or the page may have moved.</p>
        <div class="hero-actions" style="margin-top:34px;">
          <a class="button button-primary" href="index.html">Back to home <span aria-hidden="true">&rarr;</span></a>
          <a class="button button-secondary" href="publications.html">Publications <span aria-hidden="true">&rarr;</span></a>
        </div>
      </section>"""


# Read once, not once per page. lc_section() opens leetcode.json, and the
# same panel is dropped into whichever page asks for it.
_LC = lc_section()


# ── one page at a time ────────────────────────────────────────────────
# Every page is the same shell with different fillings. First the shell is
# formatted, which settles the head, the nav and the footer; then each
# mark left in the markup is replaced by whatever module owns it.
for filename, key, title, desc in PAGES:
    html = SHELL.format(
        blogname=BLOG_NAME,
        desc=desc,
        title=title,
        canonical=BASE_URL + public_path(filename),
        ogtitle=title,
        ogtype=("profile" if key in ("home", "about") else "website"),
        base=BASE_URL,
        key=key,
        brand=header_brand(filename),
        nav=nav_links(filename),
        socials=socials_html,
        body=BODY[key],
        pager=pager(filename),
        jsonld=(JSONLD if key == "home" else (SCHOLAR_LD if key == "publications" else "")),
        robots=('  <meta name="robots" content="noindex, nofollow">'
                if filename in UNLISTED else ""),
    )
    # The marks, each replaced by the module that owns it. Order does not
    # matter - no generated block contains another block's mark - but a
    # mark that survives to the end fails check.py rather than shipping a
    # comment into a finished page.
    page = html.replace(LC_MARK, _LC).replace(CV_MARK, cv_actions())
    page = page.replace(PUB_MARK, pub_groups())
    page = page.replace(BLOG_POSTS_MARK, blog_posts())
    page = page.replace(NOTES_TALLY_MARK, notes_tally())
    page = page.replace(NOTES_END_MARK, notes_end())
    page = page.replace(NOTE_CARDS_MARK, note_cards())
    page = page.replace(NOTE_COUNT_MARK, playground_attrs())
    page = page.replace(NOTE_DATA_MARK, note_data())
    page = page.replace(CAT_COLOURS_MARK, cat_colours())
    page = page.replace(CAT_TILES_MARK, cat_tiles())
    for _pid in CITATIONS:
        page = page.replace("<!--CITE:%s-->" % _pid, cite_panel(_pid))
    # Last, so it catches links written anywhere above - in a page module,
    # in a generated block, or in the shell. Filenames become the clean
    # addresses visitors see: research.html -> /research.
    page = clean_links(page)
    write(OUT / filename, page)
    print("wrote", filename, len(page), "bytes")

# ── sitemap.xml, robots.txt and a 404 page ────────────────────────
# No <lastmod>. It used to be today's date, stamped afresh on every build,
# which made the file differ every time it was generated on a different day
# from the one it was committed on — and told search engines that every page
# had changed on every deploy, which was never true. Google ignores a lastmod
# it cannot trust, so an inaccurate one buys nothing and costs a build that is
# not reproducible. The sitemap is valid without it.
_urls = "\n".join(
    '  <url><loc>%s%s</loc><priority>%s</priority></url>'
    % (BASE_URL, public_path(f), "1.0" if f == "index.html" else "0.8")
    for f, _ in NAV
)
write(OUT / "sitemap.xml",
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + _urls + '\n</urlset>\n')
print("wrote sitemap.xml")

write(OUT / "robots.txt",
    "User-agent: *\nAllow: /\n\nSitemap: " + BASE_URL + "/sitemap.xml\n")
print("wrote robots.txt")

_nf = SHELL.format(
    blogname=BLOG_NAME,
    desc="That page doesn't exist.",
    title="Page not found \u2014 Solomon B. Pobee",
    key="notfound",
    brand=header_brand("404.html"),
    canonical=BASE_URL + "/404.html",
    ogtitle="Page not found \u2014 Solomon B. Pobee",
    ogtype="website",
    base=BASE_URL,
    nav=nav_links("404.html"),
    socials=socials_html,
    body=NOT_FOUND_BODY,
    pager="",
    jsonld="",
    robots='  <meta name="robots" content="noindex">',
)
write(OUT / "404.html", clean_links(_nf))
print("wrote 404.html")
