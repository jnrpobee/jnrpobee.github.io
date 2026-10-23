#!/usr/bin/env python3
"""The recent-updates list on the home page.

One entry per thing worth announcing. Adding one means adding a dict to
NEWS below and running build.py - nothing else in the project needs
touching. The home page shows the newest HOME_COUNT of them; the rest
stay here, so there is no reason to delete an old entry when you add a
new one.

The layout is the publications pattern reused: the month in a mono rail
on the left, the item beside it, a hairline between entries. That reuse
is the point. The reader has already learned that shape on the
publications page, so a dated list needs no new vocabulary from them.
"""
import html as _html
import re as _re

# from notes import _IMAGE_KEYS

NEWS_MARK = "<!--NEWS-->"

# How many entries reach the home page. Three fills the space without
# pushing the About block too far down; raise it and the section grows.
HOME_COUNT = 3

# ─── the updates ──────────────────────────────────────────────────────
# date   "YYYY-MM". It sorts and it prints: "2026-10" becomes OCT 2026.
# title  one line, plain text. It is escaped, so no markup here.
# body   a list of paragraphs, one string each. Each one is HTML, the
#        same as a post's body, so a link is written out in full:
#        'See <a href="publications.html">the paper</a>.'
#
# Order does not matter - they are sorted newest-first on the way out.
NEWS = [
    {
        "date": "2026-10",
        "title": "CSCW 2026, Salt Lake City",
        "body": [
            "I attended the 2026 CSCW conference in Salt Lake City, Utah, where I "
            "served as a student volunteer (SV) and attended a workshop on "
            "&ldquo;Where does Privacy research go from here? Navigating the "
            "Challenges and Paths Forward&rdquo;.",
            "I met with several researchers in the HCI and CSCW communities, and I "
            "am looking forward to collaborating with them on future research "
            "projects.",
        ],
        "image": {                           
            "src": "assets/news/cscw-26.jpg",
            "alt": "Conference hall at CSCW 2026 in Salt Lake City",
            "caption": "Salt Lake City, October 2026",
        },
    },
]

# ─── a key nobody reads ────────────────────────────────────────────────
# Same guard as the blog's: an entry is a plain dictionary, so a
# misspelled key is valid Python that nothing ever looks at, and the
# build reports success while the page quietly lacks the thing. Listing
# the keys turns that into an error that says what you probably meant.
_NEWS_KEYS = frozenset(("date", "title", "body", "image"))
_IMAGE_KEYS = frozenset(("src", "alt", "caption")) 

def _reject_strays(where, given, allowed):
    """Raise on the first key that is not one this code reads."""
    import difflib
    for key in given:
        if not isinstance(key, str) or key.startswith("_") or key in allowed:
            continue
        near = difflib.get_close_matches(key.lower(), sorted(allowed), 1, 0.6)
        hint = ' Did you mean "%s"?' % near[0] if near else ""
        raise ValueError(
            '%s has an unknown key "%s".%s\n'
            "    Keys it may have: %s" % (where, key, hint, ", ".join(sorted(allowed)))
        )


def _check_shapes():
    """Run at import, so a typo fails on `python build.py` and not later."""
    for item in NEWS:
        name = item.get("title") or item.get("date") or "an update"
        _reject_strays("The update %r" % name, item, _NEWS_KEYS)
        for key in sorted(_NEWS_KEYS):
            if key not in item:
                raise ValueError('The update %r has no "%s".' % (name, key))
        if not _re.fullmatch(r"20\d\d-(0[1-9]|1[0-2])", str(item["date"])):
            raise ValueError(
                'The update %r has the date %r. It should read "YYYY-MM", '
                'like "2026-10".' % (name, item["date"])
            )
        if isinstance(item["body"], str):
            raise ValueError(
                "The update %r has its body written as one string. It should be a "
                'list of paragraphs, even for one: ["..."].' % name
            )
        img = item.get("image")
        if img is not None:
            if not isinstance(img, dict):
                raise ValueError(
                    'The update %r has its image written as %r. It should be a '
                    'dictionary: {"src": "assets/news/talk.jpg", "alt": "..."}.'
                    % (name, img))
            _reject_strays("The image on %r" % name, img, _IMAGE_KEYS)
            for key in ("src", "alt"):
                if not img.get(key):
                    raise ValueError(
                        'The image on %r has no "%s". Both are required: alt is '
                        "what a screen reader reads out." % (name, key))


_check_shapes()


# ─── rendering ─────────────────────────────────────────────────────────
# Spelled out rather than taken from strftime, which follows the machine's
# locale: the build has to produce the same bytes on any machine, and
# check.py compares two builds to prove it.
_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _label(date):
    """"2026-10" -> "Oct 2026". The CSS puts it in capitals."""
    year, month = date.split("-")
    return "%s %s" % (_MONTHS[int(month) - 1], year)


def news_section():
    """The whole section, or nothing at all if NEWS is empty.

    An empty list returns "" rather than a heading with no items under
    it - a section announcing updates and then showing none reads worse
    than no section.
    """
    if not NEWS:
        return ""
    out = [
        '      <section class="news pad" aria-labelledby="news-title">',
        '        <div class="section-heading">',
        '          <p class="kicker" id="news-title">RECENT UPDATES</p>',
        "        </div>",
        '        <div class="news-list">',
    ]
    newest = sorted(NEWS, key=lambda i: i["date"], reverse=True)[:HOME_COUNT]
    for item in newest:
        img = item.get("image")
        out.append('          <article class="news-item%s">'
                   % (" has-figure" if img else ""))
        out.append('            <p class="news-date">%s</p>' % _label(item["date"]))
        out.append("            <div>")
        out.append("              <h3>%s</h3>" % _html.escape(item["title"]))
        for para in item["body"]:
            out.append("              <p>%s</p>" % para.strip())
        out.append("            </div>")
        if img:
            out.append('            <figure class="news-figure">')
            out.append('              <img src="%s" alt="%s" loading="lazy" decoding="async">'
                       % (_html.escape(img["src"]), _html.escape(img["alt"])))
            if img.get("caption"):
                out.append("              <figcaption>%s</figcaption>"
                           % _html.escape(img["caption"]))
            out.append("            </figure>")
        out.append("          </article>")
    out.append("        </div>")
    out.append("      </section>")
    return "\n".join(out)
