#!/usr/bin/env python3
"""The pieces every other module needs: where the site lives, what is in
the nav, and how a file on disk becomes an address a visitor sees.

Nothing here knows about any one page. Everything here is imported by
something that does."""
import io
import pathlib

OUT = pathlib.Path(__file__).parent

# Where the site will live. Change this one line if you host it elsewhere —
# canonical URLs, Open Graph tags and sitemap.xml all follow from it.
BASE_URL = "https://www.solomonbpobee.com"


# Nav order drives the header, the prev/next pager at the foot of each page
# and the order of sitemap.xml, so changing it here changes all three.
NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("publications.html", "Publications"),
    ("about.html", "About"),
    ("cv.html", "CV"),
    ("projects.html", "Projects"),
]

# Pages are written to disk as .html files, because that is what a static host
# serves from. They are *linked* without the extension: GitHub Pages resolves
# /research to research.html on its own, and a visitor should never see a
# filename in the address bar. clean_links() below does the rewriting, so the
# page templates can go on referring to plain filenames.
import re

def write(path, text):
    """Write a generated file with Unix line endings on every platform.

    Python's text mode turns "\n" into "\r\n" on Windows, so the same
    build.py produced CRLF files there and LF files in CI. Git then saw
    every line of every page as changed, and the pre-push check read that
    as the pages being out of date. newline="" stops the translation.
    """
    with io.open(str(path), "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def public_path(filename):
    """The address a visitor sees for a given file on disk."""
    return "/" if filename == "index.html" else "/" + filename[:-len(".html")]

# Unlisted pages: generated and linked with clean URLs like everything
# else, but kept out of the nav, the pager and sitemap.xml.
UNLISTED = ["blog.html"]

# What the blog is called. It appears in the browser tab, in the blog's own
# nav, and in the labels a screen reader reads out on the two doors into it
# (the status dot in the header, the copyright line in the footer). The
# masthead in BODY["blog"] carries it too and is written out in full there,
# since it is set as display type rather than a label.
BLOG_NAME = "The Margin"

_LINK = re.compile(r'(href|action)="(' + "|".join([f for f, _ in NAV] + UNLISTED) + r')((?:#|\?)[^"]*)?"')

def clean_links(html):
    """Rewrite internal links from filenames to the addresses visitors see."""
    return _LINK.sub(
        lambda m: '%s="%s%s"' % (m.group(1), public_path(m.group(2)), m.group(3) or ""),
        html,
    )

import html as _html
import json as _json
import math as _math
from urllib.parse import quote as _quote
