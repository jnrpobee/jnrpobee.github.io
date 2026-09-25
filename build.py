#!/usr/bin/env python3
"""Generate the static pages from one shared shell."""
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


# ── LeetCode panel ────────────────────────────────────────────────
# The numbers live in leetcode.json, refreshed by update_leetcode.py during
# the deploy. If that file is missing or unreadable the panel is left out
# rather than rendered empty.
#
# Difficulty colours: the conventional green/amber/red fails accessibility
# checks badly — green/amber collide under deuteranopia (ΔE 3.8) and
# amber/red sit below the normal-vision floor (ΔE 13.0). These three clear
# every all-pairs gate on a dark surface, and each row is labelled in text
# so colour is never the only thing carrying identity.
import html as _html
import json as _json
import math as _math
from urllib.parse import quote as _quote

# ── citations ────────────────────────────────────────────────────────────
# One entry per publication. The styles below are written out by hand rather
# than generated from a template, because the conventions differ in ways a
# formatter gets wrong: APA sentence-cases the article title, MLA shortens
# the closing page number and collapses four authors to "et al.", IEEE
# abbreviates both given names and the journal. They are plain text so that
# copying gives something clean to paste; italics do not survive a copy
# anyway.
#
# Each key here is a publication id — "c1", "c2", and the next one is
# "c3". The id ties three things together: the entry in PUBS below, the
# Cite button's data-cite attribute, and the <!--CITE:id--> comment that
# cite_panel() replaces with the panel. See HOW TO ADD A PUBLICATION under
# "publications" further down.
#
# A format you leave out simply has no tab, so it is fine to add an entry
# with only BibTeX at first and fill in the rest later.
CITE_STYLES = [("bibtex", "BibTeX"), ("apa", "APA"), ("mla", "MLA"),
               ("chicago", "Chicago"), ("ieee", "IEEE")]

CITATIONS = {
    "c1": {
        "bibtex": """@article{jones2025nature,
  author  = {Jones, Michael and Kari, Tuomas and Reich, Daniel and
             Ens, Barrett and Liu, Siyi and Pobee, Solomon B. and
             Mueller, Florian},
  title   = {Toward a Framework for the Design of Interactive
             Technology for Nature Recreation},
  journal = {International Journal of Human--Computer Interaction},
  volume  = {41},
  number  = {18},
  pages   = {11691--11711},
  year    = {2025},
  doi     = {10.1080/10447318.2024.2443808},
  url     = {https://doi.org/10.1080/10447318.2024.2443808}
}""",
        "apa": "Jones, M., Kari, T., Reich, D., Ens, B., Liu, S., Pobee, S. B., "
               "& Mueller, F. (2025). Toward a framework for the design of "
               "interactive technology for nature recreation. International "
               "Journal of Human–Computer Interaction, 41(18), "
               "11691–11711. https://doi.org/10.1080/10447318.2024.2443808",
        "mla": "Jones, Michael, et al. “Toward a Framework for the Design of "
               "Interactive Technology for Nature Recreation.” International "
               "Journal of Human–Computer Interaction, vol. 41, no. 18, 2025, "
               "pp. 11691–711. https://doi.org/10.1080/10447318.2024.2443808.",
        "chicago": "Jones, Michael, Tuomas Kari, Daniel Reich, Barrett Ens, Siyi Liu, "
                   "Solomon B. Pobee, and Florian Mueller. “Toward a Framework for "
                   "the Design of Interactive Technology for Nature Recreation.” "
                   "International Journal of Human–Computer Interaction 41, no. 18 "
                   "(2025): 11691–11711. "
                   "https://doi.org/10.1080/10447318.2024.2443808.",
        "ieee": "M. Jones, T. Kari, D. Reich, B. Ens, S. Liu, S. B. Pobee, and "
                "F. Mueller, “Toward a framework for the design of interactive "
                "technology for nature recreation,” Int. J. Human–Computer "
                "Interaction, vol. 41, no. 18, pp. 11691–11711, 2025, "
                "doi: 10.1080/10447318.2024.2443808.",
    },
    "c2": {
        "bibtex": """@incollection{iqbal2026mathbuddy,
  author    = {Iqbal, Saba and Pobee, Solomon and
               Adhikari, Akriti and Schooley, Benjamin},
  title     = {MathBuddy: An LLM-Based Chatbot for Elementary
               Math Education},
  booktitle = {HCI International 2025 -- Late Breaking Papers},
  series    = {Lecture Notes in Computer Science},
  publisher = {Springer Nature Switzerland},
  pages     = {392--403},
  year      = {2026},
  doi       = {10.1007/978-3-032-13174-4_25},
  url       = {https://doi.org/10.1007/978-3-032-13174-4_25}
}""",
        "apa": "Iqbal, S., Pobee, S., Adhikari, A., & Schooley, B. (2026). "
               "MathBuddy: An LLM-based chatbot for elementary math education. "
               "In HCI International 2025 – Late breaking papers (Lecture Notes "
               "in Computer Science, pp. 392–403). Springer Nature Switzerland. "
               "https://doi.org/10.1007/978-3-032-13174-4_25",
        "mla": "Iqbal, Saba, et al. “MathBuddy: An LLM-Based Chatbot for "
               "Elementary Math Education.” HCI International 2025 – Late "
               "Breaking Papers, Lecture Notes in Computer Science, Springer "
               "Nature Switzerland, 2026, pp. 392–403. "
               "https://doi.org/10.1007/978-3-032-13174-4_25.",
        "chicago": "Iqbal, Saba, Solomon Pobee, Akriti Adhikari, and Benjamin Schooley. "
                   "“MathBuddy: An LLM-Based Chatbot for Elementary Math "
                   "Education.” In HCI International 2025 – Late Breaking "
                   "Papers, 392–403. Lecture Notes in Computer Science. Springer "
                   "Nature Switzerland, 2026. "
                   "https://doi.org/10.1007/978-3-032-13174-4_25.",
        "ieee": "S. Iqbal, S. Pobee, A. Adhikari, and B. Schooley, “MathBuddy: "
                "An LLM-based chatbot for elementary math education,” in HCI "
                "International 2025 – Late Breaking Papers, ser. Lecture Notes in "
                "Computer Science. Springer Nature Switzerland, 2026, pp. 392–403, "
                "doi: 10.1007/978-3-032-13174-4_25.",
    },
}


def cite_panel(pid):
    """The citation block for one publication: a format switcher and one
    <pre> per format, all but the first hidden."""
    entry = CITATIONS[pid]
    # Only the formats this entry actually has, in CITE_STYLES order, so a
    # publication can go up with BibTeX alone and gain the others later.
    # The first one present is the tab that opens.
    styles = [(k, l) for k, l in CITE_STYLES if entry.get(k)]
    if not styles:
        raise ValueError(
            "CITATIONS[%r] has no citation formats — the Cite button would "
            "open an empty panel. Give it at least a bibtex entry." % pid)
    tabs, blocks = [], []
    for i, (key, label) in enumerate(styles):
        first = (i == 0)
        tabs.append(
            '          <button type="button" class="cite-tab" role="tab" '
            'id="%s-%s-tab" aria-controls="%s-%s" aria-selected="%s" '
            'data-cite-style="%s" data-cite-panel="%s">%s</button>'
            % (pid, key, pid, key, "true" if first else "false", key, pid, label))
        blocks.append(
            '<pre id="%s-%s" role="tabpanel" aria-labelledby="%s-%s" '
            'data-cite-style="%s"%s%s>%s</pre>'
            % (pid, key, pid, key, key,
               "" if key == "bibtex" else ' class="cite-prose"',
               "" if first else " hidden",
               _html.escape(entry[key])))
    return (
        '              <div class="cite-panel" id="%s" hidden>\n'
        '        <div class="cite-tabs" role="tablist" aria-label="Citation format">\n'
        '%s\n'
        '        </div>\n'
        '%s\n'
        '                <div class="copy-wrap"><button type="button" class="btn-s" '
        'data-copy-bib="%s">Copy citation</button></div>\n'
        '              </div>'
        % (pid, "\n".join(tabs), "\n".join(blocks), pid))


# ── publications ────────────────────────────────────────────────────────
# The kinds of publication the page can show, in the order they appear on
# it. A kind with nothing in it is not rendered at all: an empty "Posters"
# heading would read as a gap rather than a section waiting to be filled.
# The heading, the count beside it and the topic filter all follow from
# whatever is in PUBS below, so adding an entry is the only step.
#
# ─── HOW TO ADD A PUBLICATION ───────────────────────────────────────────
#
# 1. Add its citation to CITATIONS above, under a new id: "c3", then "c4",
#    and so on. Give it whichever of the five formats you have; the tabs
#    are generated from the keys that are present.
#
# 2. Copy the template below into the list for its kind in PUBS, and fill
#    in the parts in CAPITALS. The three places that carry the id must all
#    say the same thing: data-cite, aria-controls and the CITE comment.
#
# 3. Run `python build.py`, then `python check.py` before pushing.
#
#     """\
#       <article class="pub" data-topic="TOPIC">
#         <div class="pub-kind">KIND<br>YEAR</div>
#         <div>
#           <a class="pub-title" href="DOI-URL" target="_blank" rel="noopener">TITLE</a>
#           <p class="pub-authors">Co Author, <strong>Solomon B. Pobee</strong>, Another Author</p>
#           <p class="pub-venue">VENUE &middot; PAGES</p>
#           <p class="pub-desc">A sentence or two on what the work found.</p>
#           <div class="cite-row">
#             <a class="btn-s btn-go" href="DOI-URL" target="_blank" rel="noopener">Read paper <span aria-hidden="true">&#8599;</span></a>
#             <button type="button" class="btn-s" data-cite="c3" aria-expanded="false" aria-controls="c3">Cite</button>
#             <button type="button" class="btn-s" data-copy-doi="10.XXXX/YYYYY">Copy DOI</button>
#           </div>
#           <!--CITE:c3-->
#         </div>
#       </article>
# """,
#
#   KIND is the small label down the left: Journal, Conference, Chapter,
#   Workshop, Poster. It is free text, so it can read "Late Breaking" or
#   anything else that fits.
#
#   TOPIC must match one of the filter chips on the page — "nature" or
#   "learning" today. If the work is about something else, add a chip in
#   BODY["publications"] first, or the entry will disappear whenever a
#   visitor uses the filter.
#
#   data-copy-doi takes the bare DOI with no https://doi.org/ in front of
#   it; the Copy DOI button adds that itself.
# ────────────────────────────────────────────────────────────────────────
PUB_GROUPS = [
    ("journal", "Journal Articles"),
    ("conference", "Conference Papers"),
    ("chapter", "Book Chapters"),
    ("workshop", "Workshop Papers"),
    ("poster", "Posters &amp; Extended Abstracts"),
]
PUB_MARK = "<!--PUBGROUPS-->"

PUBS = {
    # ── JOURNAL ARTICLES ────────────────────────────────────────────────
    # A peer-reviewed article in a journal.
    "journal": [
        """\
          <article class="pub" data-topic="nature">
            <div class="pub-kind">Journal<br>2025</div>
            <div>
              <a class="pub-title" href="https://doi.org/10.1080/10447318.2024.2443808" target="_blank" rel="noopener">Toward a Framework for the Design of Interactive Technology for Nature Recreation</a>
              <p class="pub-authors">Michael Jones, Tuomas Kari, Daniel Reich, Barrett Ens, Siyi Liu, <strong>Solomon B. Pobee</strong>, Florian Mueller</p>
              <p class="pub-venue">Int. Journal of Human&ndash;Computer Interaction &middot; 41(18), 11691&ndash;11711</p>
              <p class="pub-desc">A framework for building technology that enhances rather than diminishes the wellness benefits of outdoor recreation, decomposing engagement into nine facets tied to place, time, and community, and grounded in philosophy-of-technology perspectives.</p>
              <div class="cite-row">
                <a class="btn-s btn-go" href="https://doi.org/10.1080/10447318.2024.2443808" target="_blank" rel="noopener">Read paper <span aria-hidden="true">&#8599;</span></a>
                <button type="button" class="btn-s" data-cite="c1" aria-expanded="false" aria-controls="c1">Cite</button>
                <button type="button" class="btn-s" data-copy-doi="10.1080/10447318.2024.2443808">Copy DOI</button>
              </div>
<!--CITE:c1-->
            </div>
          </article>
""",
    ],
    # ── CONFERENCE PAPERS ───────────────────────────────────────────────
    # A full paper presented at a conference: CHI, CSCW, UIST, IEEE VR,
    # ASSETS and the like. Not the same as a Book Chapter below, even when
    # the proceedings are published as a book — file it by how you would
    # cite it. Paste the template from the comment above between these
    # brackets.
    "conference": [],
    # ── BOOK CHAPTERS ───────────────────────────────────────────────────
    # A chapter in an edited volume. The MathBuddy paper sits here because
    # it is published as an LNCS chapter; if you would rather cite it as a
    # conference paper, move it to "conference" and change its pub-kind
    # label from "Chapter" to "Conference".
    "chapter": [
        """\
          <article class="pub" data-topic="learning">
            <div class="pub-kind">Chapter<br>2026</div>
            <div>
              <a class="pub-title" href="https://doi.org/10.1007/978-3-032-13174-4_25" target="_blank" rel="noopener">MathBuddy: An LLM-Based Chatbot for Elementary Math Education</a>
              <p class="pub-authors">Saba Iqbal, <strong>Solomon Pobee</strong>, Akriti Adhikari, Benjamin Schooley</p>
              <p class="pub-venue">HCI International 2025 &ndash; Late Breaking Papers &middot; LNCS, Springer &middot; 392&ndash;403</p>
              <p class="pub-desc">A chatbot that gives students in grades 5&ndash;7 step-by-step guidance as they work through math problems. Testing found it made practice more engaging, while surfacing real questions about AI accuracy for young learners.</p>
              <div class="cite-row">
                <a class="btn-s btn-go" href="https://doi.org/10.1007/978-3-032-13174-4_25" target="_blank" rel="noopener">Read paper <span aria-hidden="true">&#8599;</span></a>
                <button type="button" class="btn-s" data-cite="c2" aria-expanded="false" aria-controls="c2">Cite</button>
                <button type="button" class="btn-s" data-copy-doi="10.1007/978-3-032-13174-4_25">Copy DOI</button>
              </div>
<!--CITE:c2-->
            </div>
          </article>
""",
    ],
    # ── WORKSHOP PAPERS ─────────────────────────────────────────────────
    # A paper at a workshop attached to a conference, usually shorter and
    # not in the main proceedings.
    "workshop": [],
    # ── POSTERS AND EXTENDED ABSTRACTS ──────────────────────────────────
    # Short-format contributions: posters, late-breaking work, extended
    # abstracts, demos.
    "poster": [],
}


def pub_groups():
    out = []
    for key, label in PUB_GROUPS:
        items = PUBS.get(key) or []
        if not items:
            continue
        out.append('        <section class="pub-group" data-group="%s">' % key)
        out.append('          <h3 class="group-head">%s <span class="group-count" '
                   'data-group-count>%d</span></h3>' % (label, len(items)))
        out.append('          <div class="pubs">')
        out.extend(a.rstrip("\n") for a in items)
        out.append('          </div>')
        out.append('        </section>')
        out.append('')
    return "\n".join(out).rstrip("\n")


# ── the blog ──────────────────────────────────────────────────────────────
# An unlisted page. It is not in the nav, not in sitemap.xml, and carries
# a noindex tag, so it will not turn up in a search. It is reached by the
# little dot beside the header note. That makes it unlisted rather than
# private: anyone given the address, or reading the page source, can open
# it. Do not put anything on it you would mind a stranger reading.
#
# ─── HOW TO ADD A POST ─────────────────────────────────────────────────
#
# Newest first. Add an entry at the top of POSTS:
#
#     {
#         "date": "2026-10-04",          # ISO; shown in the reader's format
#         "title": "What I learned watching coaches ignore dashboards",
#         "image": {
#             "src": "assets/blog/whiteboard.jpg",
#             "alt": "A whiteboard covered in a session plan",
#             "caption": "Optional line under the picture.",
#         },
#         "body": """
#           <p>First paragraph.</p>
#           <p>Second paragraph. Links look like
#              <a class="text-link" href="https://example.org/">this</a>.</p>
# """,
#     },
#
# The body is HTML so a post can hold a list or a quote. Keep it to the
# tags already styled on the site: p, a.text-link, strong, em, ul, li,
# blockquote. Then run `python build.py` and `python check.py`.
#======== Test Posts =========


#==========================
# ─── HOW TO ADD A CATEGORY ─────────────────────────────────────────────
#
# The key on the left is what a post's "category" must say. The right side
# is either just the name readers see:
#
#     "campus": "Campus Life",
#
# or that name plus a line for its tile at the foot of the blog:
#
#     "campus": {"label": "Campus Life",
#                "blurb": "Graduate school at BYU: the work and the pace."},
#
# Both forms work, so adding one in a hurry never breaks the build. A
# category with no blurb still gets a tile; the tile just has nothing to
# say under its name.
#
# Colour is not set here. Each category takes the next hue in the order
# this dict declares them, which means a category keeps its colour when
# you add another below it. There are six hues; the seventh category and
# everything after it gets a pair of them in a diagonal stripe, which is
# worth 21 categories before anything repeats. See _cat_slots().
BLOG_CATEGORIES = {
    "lifestyle": {
        "label": "Lifestyle",
        "blurb": "The ordinary hours outside the lab — what I notice, "
                 "and what I decide to keep.",
    },
    "campus": {
        "label": "Campus Life",
        "blurb": "Graduate school at BYU: the work, the people, and the "
                 "pace of the place.",
    },
    "Pod": {
        "label": "Inside The Pod",
        "blurb": "Notes from the research pod — what we are building, and "
                 "why it is built that way.",
    },
    "The Movies": {
        "label": "The Movies",
        "blurb": "Films and shows that shaped how I see things, watched "
                 "again with older eyes.",
    },
}


def _cat_label(key):
    """The name readers see, whichever form the category was written in."""
    v = BLOG_CATEGORIES.get(key)
    if isinstance(v, dict):
        return v.get("label") or key
    return v or "Notes"


def _cat_blurb(key):
    """The line under the name on the category's tile, if it has one."""
    v = BLOG_CATEGORIES.get(key)
    return (v.get("blurb") or "").strip() if isinstance(v, dict) else ""


# How many distinct hues there are to hand out. Not a free dial: the six
# were picked by search and then measured - every one clears 3:1 against
# all nine surfaces the site puts them on, and every pair of them stays
# apart under colour-blind vision with all six on screen at once, which
# is what the tiles do. A seventh hue cannot be added without one of the
# pairs failing. The values themselves live in styles.css, as --cat-1 to
# --cat-6, stepped separately for each theme.
CAT_HUES = 6


def _cat_slots():
    """Which hue, or which two, each category wears.

    The first six take a hue each. After that a category takes a pair and
    wears them as a diagonal stripe, because a seventh hue that nobody
    can tell from the second one is worse than no seventh hue. The pairs
    are generated in a fixed order, so category eleven keeps its stripe
    when category five is renamed.

    Returns {key: (primary, secondary or None)}, one-based to match the
    --cat-N custom properties.
    """
    import itertools
    pairs = itertools.combinations(range(1, CAT_HUES + 1), 2)
    out = {}
    for i, key in enumerate(BLOG_CATEGORIES):
        if i < CAT_HUES:
            out[key] = (i + 1, None)
        else:
            try:
                out[key] = next(pairs)
            except StopIteration:
                # 21 categories in. Whatever this is, it is not a category
                # scheme any more, so the rest share the last stripe
                # rather than the build falling over.
                out[key] = (CAT_HUES - 1, CAT_HUES)
    return out

POSTS = [
        {
        "date": "2026-09-24",
        "category": "The Movies",
        "title": "Going back in time to the movies",
        "summary": "I could sit back and watch the movies I loved as a young man, but I wanted to see them in the way they were meant to be seen.",
        "body": """
          <p> Homeland, the 100, breaking bad, and a few other shows that defined my youth. these are the shows that shaped my perspective on life and the world around me. </p>
          <p>Second paragraph, with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
        {
        "date": "2026-09-24",
        "category": "lifestyle",
        "title": "The unexpected long trip home",
        "summary": "A long trip home, and the multiple stops along the way.",
        "body": """
          <p>First paragraph.</p>
          <p>Second paragraph, with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
    {
        "date": "2026-09-24",
        "category": "Pod",
        "title": "The Smart Intruder: Invasion of the Open Territory",
        "summary": "Smart intruders has moved into the open territory. What happens next?",
        "body": """
          <p>In the wilderness are different pods belonging to different groups who have established their own territories.</p>
          <p>Second paragraph, with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
    {
        "date": "2026-09-21",
        "category": "lifestyle",
        "title": "Why I am keeping these notes",
        "body": """
          <p>Research usually reaches people after the questions have been narrowed, the methods have been settled, and the writing has been polished. A great deal of useful thinking happens before that point. I want this page to hold some of it.</p>
          <p>My work sits at the intersection of human&ndash;computer interaction, youth sport, and coaching. These settings make a people-first approach essential. Athletes and coaches do not simply need more data or another dashboard; a tool has to earn its place by reducing friction, clarifying a decision, or making limited time more useful.</p>
          <p>I will use these notes for ideas from building and studying systems, connections from things I am reading, and lessons that may not belong in a formal paper. The ideas will sometimes be provisional. The goal is to make the process more visible and give the thinking room to develop.</p>
""",
    },
    {
        "date": "2026-09-15",
        "category": "campus",
        "title": "Useful technology should reduce the work",
        "body": """
          <p>A system can present accurate information and still fail the people it was designed to help. This often happens when getting the insight requires more recording, organizing, and reviewing than a coach or athlete can reasonably sustain.</p>
          <p>Before adding a feature, I find it useful to ask a smaller set of questions: What decision will this support? What information already exists? Who has to do extra work? What happens when the data is incomplete?</p>
          <p>The most useful system may not be the one that collects the most data. It may be the one that asks for the minimum useful input, communicates uncertainty clearly, and fits into a routine that is already under pressure. Usability is not only whether someone can operate a tool; it is also whether using it remains worthwhile.</p>
""",
    },
    {
        "date": "2026-09-23",
        "category": "lifestyle",
        "fasten": "tape",
        "title": "A poem I keep coming back to",
        "summary": "Norma Cornett Marek\u2019s \u201cTomorrow Never Comes,\u201d and the habit it left me with.",
        "body": """
          <p>I read this years ago and it has not left me since. It is called <em>Tomorrow Never Comes</em>, by Norma Cornett Marek, and the whole of it turns on one repeated phrase:</p>
          <blockquote>If I knew this would be the last time&hellip;</blockquote>
          <p>The poem runs that sentence through ordinary things. Watching someone sleep. Hearing their voice in prayer. A door closing behind them on an unremarkable morning. Each time it asks what you would have done differently had you known, and each time the answer is almost nothing: a minute longer, one more word, the thing said out loud instead of assumed to be understood.</p>
          <p>That is what makes it land. It does not ask for grand gestures, and it does not really warn you about death. It warns you about deferral &mdash; about the quiet confidence that there will be another chance to say it.</p>
          <p>The ending turns from regret to instruction. It stops describing what you would have done and starts telling you what to do now &mdash; hold the people you love, and spend your words on them while there are words to spend. What struck me is how ordinary the words it asks for are. Not declarations. Four short things most of us can manage and routinely do not:</p>
          <blockquote>&ldquo;I&rsquo;m sorry.&rdquo; &ldquo;Please.&rdquo; &ldquo;Forgive me.&rdquo; &ldquo;Thank you.&rdquo;</blockquote>
          <p>It closes on the line I think about most:</p>
          <blockquote>The past doesn&rsquo;t come back, and the future might not come.</blockquote>
          <p>What it changed in me is unremarkable from the outside. I call home more than I used to. I have mostly stopped saving things to say. <a class="text-link" href="http://www.heartwhispers.net/poetry/00040.html" target="_blank" rel="noopener">The full poem is at Heart Whispers</a>, where it is published with the author&rsquo;s name on it &mdash; worth reading whole, and worth reading there rather than here.</p>
""",
    },
]
BLOG_POSTS_MARK = "<!--BLOGPOSTS-->"
NOTES_TALLY_MARK = "<!--NOTESTALLY-->"
NOTES_END_MARK = "<!--NOTESEND-->"

# What holds each note to the page. A post may name its own with
# "fasten": "tape"; anything that does not gets the next one in this
# order, so a board of notes never wears the same fastener twice running.
# The art for each lives in styles.css, keyed on data-fasten.
FASTENERS = ("pin", "tape", "clip", "bulldog", "dot")

# Roughly what an adult reads in a minute of prose. The figure only has to
# be honest enough to set an expectation, so it is rounded up to a whole
# minute and never shown as zero.
WORDS_PER_MINUTE = 220


_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December")


def _one_line(post):
    """The line under the title.

    Prefer an explicit "summary" on the post. Failing that, take the first
    sentence of the body, so an entry written before this existed still
    reads properly instead of showing nothing.
    """
    given = (post.get("summary") or "").strip()
    if given:
        return given
    text = re.sub(r"<[^>]+>", " ", post.get("body", ""))
    text = _html.unescape(text)
    text = " ".join(text.split())
    if not text:
        return ""
    m = re.search(r"^(.+?[.!?])(\s|$)", text)
    line = m.group(1) if m else text
    # Roughly two lines at the card's width. The CSS clamps to two lines
    # as well, so this only decides where the ellipsis falls.
    if len(line) > 150:
        line = line[:149].rsplit(" ", 1)[0] + "\u2026"
    return line


def _ordered_posts():
    """Newest first. Everything that numbers or links a post counts from
    this order, so the board, the list and the anchors agree."""
    return sorted(POSTS, key=lambda x: x.get("date", ""), reverse=True)


# How many notes the board holds. Two and three have their own keyframes
# and their own card positions, so this is not a free dial - see
# "the papers take turns" in styles.css before changing it.
BOARD_SLOTS = 3


def _board_order():
    """Every note, in the order the board would hang them.

    Pinned notes come first, oldest pin first so adding one does not
    reshuffle the board, and the rest follow newest first. A post with
    "pin": True keeps its place whatever its date, so something worth
    keeping up there - a piece you are proud of, a poem - does not slide
    off the board the week you write two other things.

    The first BOARD_SLOTS of this are what the page ships with. The
    remainder is the queue the cards turn over through once script is
    running - see the board rotation in script.js.
    """
    order = _ordered_posts()
    pinned = [p for p in order if p.get("pin")][::-1]
    rest = [p for p in order if not p.get("pin")]
    return pinned + rest


def _board_posts():
    """The notes the page ships with on the board."""
    return _board_order()[:BOARD_SLOTS]


def _slug(text):
    """A title reduced to something that can live in a URL."""
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text)


def _anchors():
    """A permanent address for every note, in _ordered_posts() order.

    The old ids were positions - the newest note was post-1 - so writing
    anything renumbered every note below it and quietly repointed every
    link anyone had saved. An address has to be a property of the note,
    not of where it currently sits, so it is built from the date and the
    title: 2026-09-21-why-i-am-keeping-these-notes.

    The date comes first because it is the part that never changes. Retitle
    a note and the old link still carries the right date, which script.js
    uses to find it again.
    """
    seen, out = {}, []
    for post in _ordered_posts():
        stem = post.get("date", "") or "undated"
        tail = _slug(post.get("title", ""))
        base = ("%s-%s" % (stem, tail)).strip("-")
        seen[base] = seen.get(base, 0) + 1
        out.append(base if seen[base] == 1 else "%s-%d" % (base, seen[base]))
    return out


def _fasteners():
    """What each note wears, newest first.

    A post names its own with "fasten"; everything else takes its turn
    through FASTENERS. The rotation steps past anything worn by the two
    notes above, so a reader scrolling never sees the same fastener twice
    close together - including when a named choice lands on the turn the
    rotation was about to take. With five fasteners and a memory of two
    there is always one free, so the search always ends.
    """
    out, turn = [], 0
    for post in _ordered_posts():
        named = (post.get("fasten") or "").strip().lower()
        if named:
            if named not in FASTENERS:
                raise ValueError(
                    "Unknown fastener %r. Use one of: %s"
                    % (named, ", ".join(FASTENERS))
                )
            chosen = named
        else:
            recent = out[-2:]
            for _ in range(len(FASTENERS)):
                chosen = FASTENERS[turn % len(FASTENERS)]
                turn += 1
                if chosen not in recent:
                    break
        out.append(chosen)
    return out


def _reading_time(post):
    """How long this note takes to read, as the line the card carries.

    Whole minutes alone said nothing here. Every note written so far came
    out as "1 min read", so a two-sentence thought and a page of prose
    wore the same label and the number stopped being information.

    Under a minute this counts seconds instead, to the nearest ten, which
    is a difference a reader can actually feel. At a minute and over it
    goes back to whole minutes: reading speed varies by more than a
    factor of two between people, so "3 min 40 sec" would be claiming an
    accuracy that is not there. Ten seconds is the floor, because "4 sec
    read" reads as a joke about the post.
    """
    text = re.sub(r"<[^>]+>", " ", post.get("body", ""))
    words = len(_html.unescape(text).split())
    seconds = words * 60.0 / WORDS_PER_MINUTE
    if seconds < 60:
        ten = max(10, int(round(seconds / 10.0)) * 10)
        # 55 seconds rounds to 60, and "60 sec read" is a minute said badly.
        if ten < 60:
            return "%d sec read" % ten
    return "%d min read" % max(1, int(round(seconds / 60.0)))


_TALLY = ("no", "one", "two", "three", "four", "five", "six", "seven",
          "eight", "nine", "ten")


def _spelled(n):
    """Small numbers read better as words in a line of running text."""
    return _TALLY[n] if n < len(_TALLY) else str(n)


def _post_figure(post):
    """An optional image on a post.

    Written as:

        "image": {
            "src": "assets/blog/lab-whiteboard.jpg",
            "alt": "A whiteboard covered in a session plan",
            "caption": "Optional line under the picture.",
        },

    alt is required and must describe the picture, because a reader using
    a screen reader gets nothing else. Pass "alt": "" deliberately if the
    image is purely decorative. The deploy's asset check will catch a src
    that does not exist, so a typo stops the build rather than shipping a
    broken image.
    """
    img = post.get("image")
    if not img:
        return ""
    if isinstance(img, str):                      # "image": "assets/blog/x.jpg"
        img = {"src": img, "alt": ""}
    src = (img.get("src") or "").strip()
    if not src:
        return ""
    if "alt" not in img:
        raise ValueError(
            "The image on %r has no alt text. Describe it, or set "
            '"alt": "" if it is decorative.' % post.get("title", "a post"))
    cap = (img.get("caption") or "").strip()
    out = ['          <figure class="post-figure">']
    out.append('            <img src="%s" alt="%s" loading="lazy" decoding="async">'
               % (_html.escape(src), _html.escape(img["alt"])))
    if cap:
        out.append('            <figcaption>%s</figcaption>' % _html.escape(cap))
    out.append('          </figure>')
    return "\n".join(out)


NOTE_CARDS_MARK = "<!--NOTECARDS-->"
NOTE_COUNT_MARK = "<!--NOTECOUNT-->"
NOTE_DATA_MARK = "<!--NOTEDATA-->"
CAT_COLOURS_MARK = "<!--CATCOLOURS-->"
CAT_TILES_MARK = "<!--CATTILES-->"

# Shown when there are no posts yet, so the hero still looks designed
# rather than empty.
NOTE_CARDS_FALLBACK = [
    ("NOTICE", "Look closer.", "Start with the ordinary details."),
    ("RESET", "Make room.", "Rest belongs in the process."),
    ("CARRY", "Keep what matters.", "Less noise. More intention."),
]
_NOTE_SLOTS = ("one", "two", "three")


def _card_rows(posts):
    """What a board card says about each of these notes.

    One place, because the cards the page ships with and the list script
    rotates through have to agree about every note down to the fastener -
    a card that changed its writing but kept the last note's pin would be
    wearing someone else's.
    """
    import datetime as _dt
    worn = _fasteners()
    slugs = _anchors()
    where = dict((id(q), n) for n, q in enumerate(_ordered_posts()))
    out = []
    for post in posts:
        label = _cat_label(post.get("category", "lifestyle"))
        when = post.get("date", "")
        try:
            d = _dt.date.fromisoformat(when)
            sub = "%d %s %d" % (d.day, _MONTHS[d.month - 1], d.year)
        except Exception:
            sub = ""
        n = where[id(post)]
        out.append((label.upper(), post.get("title", "Untitled"), sub,
                    worn[n], "#" + slugs[n]))
    return out


def note_data():
    """Every note the board can show, for the rotation in script.js.

    Only written when there is something to rotate in: with three notes
    or fewer the board already holds all of them and the cards have
    nowhere to turn to.

    JSON in a script tag the browser will not execute, rather than an
    attribute format invented for the occasion. The order is
    _board_order()'s, so script can take the first three as the ones
    already on the board and the rest as the queue without working
    anything out for itself.
    """
    if len(POSTS) <= BOARD_SLOTS:
        return ""
    import json
    rows = [{"cat": a, "title": b, "date": c, "fasten": d, "href": e}
            for (a, b, c, d, e) in _card_rows(_board_order())]
    blob = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    # The one sequence that cannot appear inside a script element, whatever
    # the type says: it would end the element early.
    blob = blob.replace("</", "<\\/")
    return ('          <script type="application/json" data-board-notes>'
            '%s</script>' % blob)


def note_cards():
    """The three papers pinned in the hero, carrying the newest posts.

    Which notes hang here is _board_posts()'s decision; each card wears
    the same fastener as its own note below, so a reader following a card
    down the page lands on something that looks like what they clicked.

    The highlight moves from one card to the next on a timer. Without
    script that is the CSS animation below the papers in styles.css, so
    the board still works with nothing loaded; with script it becomes a
    class, which is what lets a card change what it says at the moment
    the colour leaves it - see note_data() and the board rotation in
    script.js. Either way it stops for anyone who has asked for reduced
    motion.
    """
    rows = _card_rows(_board_posts())
    if not rows:
        # Nothing written yet, so the cards are placeholders. They lead
        # nowhere, so they stay plain <div>s and the board stays hidden
        # from screen readers - see playground_attrs().
        rows = [(a, b, c, FASTENERS[i % len(FASTENERS)], "")
                for i, (a, b, c) in enumerate(NOTE_CARDS_FALLBACK)]

    out = []
    for i, (label, title, sub, fasten, href) in enumerate(rows):
        tag = "a" if href else "div"
        out.append('          <%s class="note-paper note-paper-%s" style="--i:%d"'
                   ' data-fasten="%s"%s>'
                   % (tag, _NOTE_SLOTS[i], i, fasten,
                      (' href="%s"' % href) if href else ""))
        # Four pieces, because tape uses two and a later fastener might
        # want four. The ones this fastener does not use stay invisible.
        out.append('            <span class="fasten" aria-hidden="true">'
                   '<i></i><i></i><i></i><i></i></span>')
        out.append('            <span>%02d / %s</span>' % (i + 1, _html.escape(label)))
        out.append('            <strong>%s</strong>' % _html.escape(title))
        if href:
            out.append('            <span class="note-open">Read &rarr;</span>')
        if sub:
            out.append('            <p>%s</p>' % _html.escape(sub))
        out.append('          </%s>' % tag)
    return "\n".join(out)


def playground_attrs():
    """How many cards the board is holding, and - when there is nothing
    written yet - that it is decoration.

    With posts, the cards are links to them, so the board is real content
    and hiding it would take those links away from a screen reader. The
    placeholder cards lead nowhere, so that board stays hidden and the
    empty-state line below speaks for it."""
    n = min(len(POSTS), 3) or len(NOTE_CARDS_FALLBACK)
    hidden = "" if POSTS else ' aria-hidden="true"'
    return ' data-cards="%d"%s' % (n, hidden)


def blog_posts():
    """Every post, newest first, each one collapsed to its title and a
    single line until the reader opens it.

    <details> rather than a script: it opens on click and on Enter or
    Space, it is announced as expandable, the browser's find-in-page can
    open it to reveal a match, and it still works if the JavaScript fails.
    """
    if not POSTS:
        return ('        <div class="empty">Nothing here yet. This is where '
                'the writing will go.</div>')
    import datetime as _dt
    out = []
    worn = _fasteners()
    slugs = _anchors()
    seen_month = seen_year = None
    for i, post in enumerate(_ordered_posts()):
        when, shown = post.get("date", ""), ""
        category = post.get("category", "lifestyle")
        if category not in BLOG_CATEGORIES:
            raise ValueError(
                "Unknown blog category %r. Use one of: %s"
                % (category, ", ".join(sorted(BLOG_CATEGORIES)))
            )
        try:
            d = _dt.date.fromisoformat(when)
            # Spelled out as the fallback; script.js rewrites it to the
            # reader's own format, the same as the LeetCode date.
            shown = ('<time datetime="%s">%d %s %d</time>'
                     % (_html.escape(when), d.day, _MONTHS[d.month - 1], d.year))
        except Exception:
            when = ""
        line = _one_line(post)
        # A heading at each new month, so the list reads as an archive
        # rather than one long column. They sit inside .posts with the
        # notes rather than wrapping them, which keeps one counter running
        # down the whole page and lets the filter hide a month by hiding
        # its heading, without either having to know about the other.
        month = year = ""
        if when:
            year = "%d" % d.year
            # A year band above the months, so two years of writing reads
            # as two years rather than one long run of month headings.
            # Like the month heading it is a sibling of the notes, not a
            # wrapper, which keeps one number running down the page and
            # lets the filter hide a whole year by hiding its band.
            if year != seen_year:
                out.append('        <div class="year" data-year-head="%s">' % year)
                out.append('          <h3>%s</h3>' % year)
                out.append('          <span class="rule" aria-hidden="true"></span>')
                out.append('          <span class="n" data-year-count></span>')
                out.append('        </div>')
                seen_year = year
            month = "%s %d" % (_MONTHS[d.month - 1], d.year)
            if month != seen_month:
                out.append('        <div class="month" data-month-head="%s">'
                           % _html.escape(month))
                out.append('          <h3>%s</h3>' % _html.escape(month))
                out.append('          <span class="rule" aria-hidden="true"></span>')
                out.append('          <span class="n" data-month-count></span>')
                out.append('        </div>')
                seen_month = month
        # The id is what the board card links to, and what the shuffle
        # sends the reader to.
        out.append('        <details class="post" id="%s" data-blog-topic="%s"'
                   ' data-fasten="%s" data-month="%s" data-in-year="%s"'
                   ' data-n="%d"%s>'
                   % (slugs[i], _html.escape(category), worn[i],
                      _html.escape(month), _html.escape(year), i + 1,
                      ' data-stripe' if _cat_slots().get(category, (0, None))[1]
                      else ''))
        out.append('          <summary class="post-head">')
        # The fastener lives inside the summary because anything else
        # inside a closed <details> is hidden.
        out.append('            <span class="fasten" aria-hidden="true">'
                   '<i></i><i></i><i></i><i></i></span>')
        out.append('            <div class="post-meta">')
        if shown:
            out.append('              <p class="post-date">%s</p>' % shown)
        out.append('              <p class="post-read">%s</p>'
                   % _reading_time(post))
        out.append('              <p class="post-category">%s</p>'
                   % _html.escape(_cat_label(category)))
        out.append('            </div>')
        out.append('            <h2 class="post-title">%s</h2>'
                   % _html.escape(post.get("title", "Untitled")))
        if line:
            out.append('            <p class="post-summary">%s</p>' % _html.escape(line))
        out.append('            <span class="post-chevron" aria-hidden="true"></span>')
        out.append('          </summary>')
        out.append('          <div class="post-body">')
        fig = _post_figure(post)
        if fig:
            out.append(fig)
        out.append(post.get("body", "").rstrip("\n"))
        out.append('          </div>')
        out.append('        </details>')
    return "\n".join(out)



# How many notes the list shows before a reader asks for more, and the
# lengths the picker offers. The controls only appear once there is enough
# written to need them - see notes_tally() - so an early page stays quiet.
PAGE_STEP = 5
PAGE_STEPS = (5, 10, 15)


def _category_counts():
    """Every category in use, in the order BLOG_CATEGORIES declares them,
    with how many notes each holds. A category nobody has written in yet
    gets no chip."""
    out = []
    for key in BLOG_CATEGORIES:
        n = len([p for p in POSTS if p.get("category", "lifestyle") == key])
        if n:
            out.append((key, _cat_label(key), n))
    return out


def cat_colours():
    """One small stylesheet handing each category its hue.

    Written here rather than in styles.css because the mapping is a
    property of the category list, not of the design: add a category and
    it takes the next hue without anybody editing CSS. It names tokens
    rather than colours, so the theme still decides what --cat-3 is.

    A stripe carries two, which is what --cat-b is for; everything with a
    single hue leaves it unset, and the rule that draws the stripe checks
    for data-stripe rather than for the property.
    """
    slots = _cat_slots()
    if not slots:
        return ""
    out = ['        <style>']
    for key, (a, b) in slots.items():
        sel = '[data-blog-topic="%s"]' % _html.escape(key, quote=True)
        if b is None:
            out.append('          %s{--cat:var(--cat-%d);}' % (sel, a))
        else:
            out.append('          %s{--cat:var(--cat-%d);--cat-b:var(--cat-%d);}'
                       % (sel, a, b))
    out.append('        </style>')
    return "\n".join(out)


def cat_tiles():
    """The tiles at the foot of the blog: what is in here, and how much.

    The page used to stop at the last note and leave a screen of empty
    board above the footer. This fills it with the one thing a reader who
    got that far might want, which is what else there is - and each tile
    is the filter for its own category, so it answers the question and
    then acts on it.

    Only categories that have been written in appear. A tile for an empty
    one would be a promise the list cannot keep.
    """
    rows = _category_counts()
    if not rows:
        return ""
    slots = _cat_slots()
    out = ['      <section class="cat-tiles pad" aria-labelledby="cat-tiles-title">']
    out.append('        <div class="section-heading">')
    out.append('          <p class="kicker" id="cat-tiles-title">WHAT IS IN HERE</p>')
    out.append('          <p class="notes-order">%s &middot; TAP TO FILTER</p>'
               % _html.escape(_spelled(len(rows)).upper() +
                              (" CORNERS" if len(rows) != 1 else " CORNER") +
                              " OF THE BOARD"))
    out.append('        </div>')
    out.append('        <div class="cat-grid">')
    for key, label, n in rows:
        stripe = ' data-stripe' if slots.get(key, (0, None))[1] else ''
        out.append('          <button type="button" class="cat-tile" '
                   'data-blog-topic="%s" data-cat-tile aria-pressed="false"%s>'
                   % (_html.escape(key, quote=True), stripe))
        out.append('            <h3>%s</h3>' % _html.escape(label))
        blurb = _cat_blurb(key)
        if blurb:
            out.append('            <p>%s</p>' % _html.escape(blurb))
        out.append('            <span class="n">%s note%s</span>'
                   % (_spelled(n), "" if n == 1 else "s"))
        out.append('          </button>')
    out.append('        </div>')
    out.append('      </section>')
    return "\n".join(out)


def _months_in_use():
    """Every month that has a note in it, newest first, with its count.

    A chip each would be fine for a year and unreadable after three, so
    the months go in a select rather than the chip row. It is also the
    honest control for a list that only grows: a select scrolls, a row of
    chips wraps until it owns half the page.
    """
    import datetime as _dt
    out, seen = [], {}
    for post in _ordered_posts():
        try:
            d = _dt.date.fromisoformat(post.get("date", ""))
        except Exception:
            continue
        key = "%s %d" % (_MONTHS[d.month - 1], d.year)
        if key not in seen:
            seen[key] = len(out)
            out.append([key, 0])
        out[seen[key]][1] += 1
    return out


_MONTH_SHORT = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def _month_select():
    """The month picker, drawn as a calendar rather than a menu.

    A year of months is a shape people already know, and it says something
    a list cannot: which months have writing in them and which are empty.
    Every month of every year appears; the ones with nothing in them are
    there but unpressable, so the gaps in a year are visible rather than
    silently absent.

    The whole grid is built here rather than in script.js, so the counts
    come from the same place as everything else and the markup can be read
    in the page source. script.js only shows one year at a time.
    """
    months = _months_in_use()
    if not months:
        return ""
    have = dict(months)                       # "September 2026" -> count
    years = sorted({k.rsplit(" ", 1)[-1] for k, _ in months}, reverse=True)
    opening = months[0][0]                    # newest month with writing

    out = ['          <div class="month-pick" data-month-pick hidden>']
    out.append('            <button type="button" class="chip cal-toggle" '
               'data-cal-toggle aria-expanded="false">%s</button>'
               % _html.escape(opening))
    out.append('            <div class="cal" data-cal hidden>')
    out.append('              <div class="cal-head">')
    out.append('                <button type="button" class="cal-step" data-cal-step="-1" '
               'aria-label="Later year">&lsaquo;</button>')
    out.append('                <span class="cal-year" data-cal-year></span>')
    out.append('                <button type="button" class="cal-step" data-cal-step="1" '
               'aria-label="Earlier year">&rsaquo;</button>')
    out.append('              </div>')
    for year in years:
        out.append('              <div class="cal-grid" data-cal-grid="%s" hidden>' % year)
        for n, short in enumerate(_MONTH_SHORT, start=1):
            key = "%s %s" % (_MONTHS[n - 1], year)
            count = have.get(key)
            if count:
                out.append('                <button type="button" class="cal-m has" '
                           'data-month="%s"%s><em>%s</em><i>%d</i></button>'
                           % (_html.escape(key),
                              ' aria-current="true"' if key == opening else "",
                              short, count))
            else:
                out.append('                <button type="button" class="cal-m" '
                           'disabled><em>%s</em><i></i></button>' % short)
        out.append('              </div>')
    out.append('              <button type="button" class="cal-all" data-month="">'
               'Every month <span>%d</span></button>' % len(POSTS))
    out.append('            </div>')
    out.append('          </div>')
    return "\n".join(out)


def notes_tally():
    """Everything above the list: the filters, the count, the length
    picker and the shuffle.

    Each control ships with `hidden` and script.js removes it, so a reader
    without JavaScript is never shown a control that cannot work - the
    same reason the topic words lost their pill.

    They also only exist when they are worth having. One category means no
    filter to speak of, and five notes need no paging, so a page early in
    its life shows a count and nothing else and grows its controls as the
    writing arrives.
    """
    n = len(POSTS)
    if not n:
        return ""
    out = []

    cats = _category_counts()
    if len(cats) > 1:
        out.append('        <div class="notes-filters" data-filters hidden>')
        out.append('          <p class="filter-label" id="filter-label">Show</p>')
        out.append('          <div class="filter-chips" role="group" aria-labelledby="filter-label">')
        out.append('            <button type="button" class="chip" data-cat="all" '
                   'aria-pressed="true">All notes <span>%d</span></button>' % n)
        for key, label, count in cats:
            out.append('            <button type="button" class="chip" data-cat="%s" '
                       'aria-pressed="false">%s <span>%d</span></button>'
                       % (_html.escape(key), _html.escape(label), count))
        out.append('          </div>')
        out.append(_month_select())
        out.append('          <p class="filter-count" data-filter-count></p>')
        out.append('        </div>')

    out.append('        <div class="notes-toolbar">')
    out.append('          <p class="notes-count">%s note%s so far</p>'
               % (_spelled(n).capitalize(), "" if n == 1 else "s"))
    # Every length, always. An earlier version hid a step that was larger
    # than the list, and hid the whole row below six notes, on the grounds
    # that a page with three notes has no use for paging. True, but it
    # also meant the controls only appeared once there was enough written
    # to need them, which made the page look like it had lost them. They
    # stay put now; with a short list they simply have nothing to do.
    out.append('          <span class="count-picker" data-counts hidden>')
    out.append('            <span class="count-label">Per page</span>')
    for step in PAGE_STEPS:
        out.append('            <button type="button" class="chip" data-count="%d" '
                   'aria-pressed="%s">%d</button>'
                   % (step, "true" if step == PAGE_STEP else "false", step))
    out.append('            <button type="button" class="chip" data-count="0" '
               'aria-pressed="false">All</button>')
    out.append('          </span>')
    out.append('          <button class="surprise" type="button" data-surprise hidden>'
               'Surprise me</button>')
    out.append('        </div>')
    return "\n".join(out)


def notes_end():
    """The foot of the list: the button that reveals the next few notes,
    and a line so the page finishes rather than running out."""
    if not POSTS:
        return ""
    out = []
    # Rendered whichever way; script.js hides it the moment there is
    # nothing further to show, which on a short list is immediately.
    out.append('        <div class="notes-more" data-more-wrap hidden>')
    out.append('          <button class="surprise" type="button" data-more></button>')
    out.append('        </div>')
    out.append('        <div class="notes-end">')
    out.append('          <p>That is everything pinned so far</p>')
    out.append('          <span class="again">More when there is more.</span>')
    out.append('        </div>')
    return "\n".join(out)

# ── the CV download ──────────────────────────────────────────────────────
# Drop a PDF into assets/cv/ and both buttons on the CV page point at it:
# Download saves it, Print sends that file to the printer rather than the web
# page. Leave the folder empty and the Download button is left out entirely
# rather than linking to a file that is not there — a dead reference fails
# the deploy's asset check and stops the whole site publishing — and Print
# falls back to printing the page, so the button is never dead. The filename
# is yours to choose; if there is more than one PDF the last by name wins, so
# dated names like cv-2026-09.pdf sort the newest to the end.
CV_DIR = OUT / "assets" / "cv"
CV_MARK = "<!--CVACTIONS-->"


def cv_actions():
    pdfs = sorted(p.name for p in CV_DIR.glob("*.pdf")) if CV_DIR.is_dir() else []
    out = []
    if pdfs:
        # Percent-encode the filename. Real CV files are called things like
        # "Solo-Resume-Aug 2026.pdf", and a raw space in an href is not a
        # valid URL — it broke the deploy's link check once already.
        href = "assets/cv/%s" % _quote(pdfs[-1])
        out.append('<a class="button button-primary" href="%s" download>'
                   'Download PDF <span aria-hidden="true">&darr;</span></a>' % href)
        out.append('<button type="button" class="button button-secondary" '
                   'data-print="%s">Print CV</button>' % href)
    else:
        out.append('<button type="button" class="button button-secondary" '
                   'data-print="">Print this page</button>')
    return "\n          " + "\n          ".join(out)


LC_MARK = "<!--LEETCODE-->"
# The colours live in styles.css so they can follow the theme; these
# are the class suffixes that select them.
LC_DIFF = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]

_R, _CX, _GAP = 54.0, 64.0, 3.0          # donut radius, centre, arc gap in px
_C = 2 * _math.pi * _R


def _donut(solved, total):
    """Composition of the solved problems, as one arc per difficulty."""
    arcs, at = [], 0.0
    for key, label in LC_DIFF:
        n = solved.get(key)
        if not isinstance(n, int) or n <= 0:
            continue
        span = (n / total) * _C
        drawn = max(span - _GAP, 1.0)
        arcs.append(
            '          <circle class="lc-arc lc-%s" cx="%g" cy="%g" r="%g" '
            'stroke-dasharray="%.2f %.2f" stroke-dashoffset="%.2f">'
            '<title>%s: %d of %d solved</title></circle>'
            % (key, _CX, _CX, _R, drawn, _C - drawn, -at, label, n, total))
        at += span
    return "\n".join(arcs)


def lc_section():
    try:
        d = _json.loads((OUT / "leetcode.json").read_text(encoding="utf-8"))
    except Exception:
        return ""

    solved = d.get("solved") or {}
    total = solved.get("all")
    if not isinstance(total, int) or total <= 0:
        return ""

    totals = d.get("totals") or {}
    lang = (d.get("language") or {}).get("name")
    user = _html.escape(str(d.get("username") or "pobee"))

    # Bars compare the difficulties against each other — scaled to the
    # largest of them — because a bar against LeetCode's whole catalogue
    # would be an invisible sliver at every difficulty. The catalogue size
    # is given as text beside it instead.
    counts = [solved.get(k) for k, _ in LC_DIFF if isinstance(solved.get(k), int)]
    peak = max(counts) if counts else 1

    rows = []
    for key, label in LC_DIFF:
        n = solved.get(key)
        if not isinstance(n, int):
            continue
        pool = totals.get(key)
        of = ' <span class="lc-of">of %s</span>' % format(pool, ",") if isinstance(pool, int) else ""
        rows.append(
            '            <li class="lc-row lc-%s">\n'
            '              <p class="lc-row-k"><i></i>%s</p>\n'
            '              <p class="lc-row-n"><strong>%d</strong>%s</p>\n'
            '              <span class="lc-bar" style="--p:%.1f%%"></span>\n'
            '            </li>' % (key, label, n, of, 100.0 * n / peak))

    parts = [
        '      <section class="lc">',
        '        <div class="lc-head">',
        '          <div>',
        '            <p class="lc-k">LeetCode</p>',
        '            <p class="lc-sub">%s%s</p>' % (
            "Problems solved on ", "@" + user),
        '          </div>',
        '          <a class="btn-s btn-go" href="https://leetcode.com/u/%s/" target="_blank" '
        'rel="noopener">View profile <span aria-hidden="true">&#8599;</span></a>' % user,
        '        </div>',
        '        <div class="lc-split">',
        '          <figure class="lc-donut">',
        '            <svg viewBox="0 0 128 128" role="img" aria-label="%s">' % _html.escape(
            "%d problems solved: %s" % (total, ", ".join(
                "%d %s" % (solved[k], l.lower()) for k, l in LC_DIFF
                if isinstance(solved.get(k), int) and solved[k] > 0))),
        '              <g transform="rotate(-90 64 64)">',
        '          <circle class="lc-track" cx="64" cy="64" r="54"/>',
        _donut(solved, total),
        '              </g>',
        '            </svg>',
        '            <figcaption class="lc-donut-n"><strong>%d</strong><span>solved</span></figcaption>' % total,
        '          </figure>',
        '          <ul class="lc-diff">',
        "\n".join(rows),
        '          </ul>',
        '        </div>',
    ]

    bits = []
    if lang:
        bits.append("Solved in %s." % _html.escape(lang).replace(" ", "&nbsp;"))
    when = d.get("fetched")
    if when:
        try:
            import datetime as _dt
            _d = _dt.date.fromisoformat(when)
            # Built by hand rather than with strftime. "%-d" (no leading zero)
            # is a glibc extension: it raises on Windows, the except below
            # swallowed it, and this whole line silently vanished from the
            # page — so a Windows build and a CI build produced different
            # HTML. Month names are spelled out for the same reason, since
            # "%B" follows the machine's locale.
            _months = ("January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November",
                       "December")
            # The ISO date goes in datetime="" and script.js rewrites the text
            # to however the reader's own machine writes dates — 9/19/2026 in
            # the US, 19/09/2026 in most of the rest of the world. That has to
            # happen in the browser: one file is served to every visitor, so
            # the build cannot know whose convention to use. The spelled-out
            # form below is what stays if scripting is off, and it reads the
            # same either way round.
            bits.append('Last checked <time datetime="%s">%d %s %d</time>.'
                        % (_html.escape(when), _d.day,
                           _months[_d.month - 1], _d.year))
        except Exception:
            pass
    if bits:
        parts.append('        <p class="lc-note">%s</p>' % " ".join(bits))
    parts.append('      </section>')
    return "\n".join(parts)

# Google Scholar profile.
SCHOLAR_URL = "https://scholar.google.com/citations?user=02WgxKoAAAAJ"

SOCIALS = [
    ("https://github.com/jnrpobee", "GitHub"),
    (SCHOLAR_URL, "Google Scholar"),
    ("https://orcid.org/0009-0007-5172-0410", "ORCID"),
    ("https://www.researchgate.net/profile/Solomon-Pobee", "ResearchGate"),
    ("https://linkedin.com/in/jnrpobee", "LinkedIn"),
]

PAGES = [
    ("index.html", "home", "Solomon B. Pobee — HCI Researcher",
     "Solomon B. Pobee — PhD researcher in human–computer interaction, sports technology, and human performance."),
    ("research.html", "research", "Research — Solomon B. Pobee",
     "Research by Solomon B. Pobee in human–computer interaction, sports technology, and youth athletics."),
    ("projects.html", "projects", "Projects — Solomon B. Pobee",
     "Projects and open-source work by Solomon B. Pobee in HCI, sports technology, and human performance."),
    ("publications.html", "publications", "Publications — Solomon B. Pobee",
     "Peer-reviewed publications by Solomon B. Pobee."),
    ("about.html", "about", "About — Solomon B. Pobee",
     "About Solomon B. Pobee, Computer Science PhD student and human–computer interaction researcher."),
    ("cv.html", "cv", "CV — Solomon B. Pobee",
     "Curriculum vitae for Solomon B. Pobee, Computer Science PhD student and HCI researcher."),
    # Unlisted — see UNLISTED above. Generated like any other page, but
    # absent from the nav, the pager and sitemap.xml, and marked noindex.
    ("blog.html", "blog", BLOG_NAME + " — Solomon B. Pobee",
     "The Margin: notes on lifestyle, campus and the PhD, kept by Solomon B. Pobee."),
]

SCHOLAR_LD = """<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"ItemList",
  "name":"Publications by Solomon B. Pobee",
  "itemListElement":[
    {
      "@type":"ListItem","position":1,
      "item":{
        "@type":"ScholarlyArticle",
        "name":"MathBuddy: An LLM-Based Chatbot for Elementary Math Education",
        "author":[
          {"@type":"Person","name":"Saba Iqbal"},
          {"@type":"Person","name":"Solomon Pobee"},
          {"@type":"Person","name":"Akriti Adhikari"},
          {"@type":"Person","name":"Benjamin Schooley"}
        ],
        "datePublished":"2026",
        "isPartOf":{"@type":"PublicationVolume","name":"HCI International 2025 \u2013 Late Breaking Papers"},
        "publisher":{"@type":"Organization","name":"Springer Nature Switzerland"},
        "pagination":"392-403",
        "identifier":"https://doi.org/10.1007/978-3-032-13174-4_25",
        "url":"https://doi.org/10.1007/978-3-032-13174-4_25"
      }
    },
    {
      "@type":"ListItem","position":2,
      "item":{
        "@type":"ScholarlyArticle",
        "name":"Toward a Framework for the Design of Interactive Technology for Nature Recreation",
        "author":[
          {"@type":"Person","name":"Michael Jones"},
          {"@type":"Person","name":"Tuomas Kari"},
          {"@type":"Person","name":"Daniel Reich"},
          {"@type":"Person","name":"Barrett Ens"},
          {"@type":"Person","name":"Siyi Liu"},
          {"@type":"Person","name":"Solomon B. Pobee"},
          {"@type":"Person","name":"Florian Mueller"}
        ],
        "datePublished":"2025",
        "isPartOf":{"@type":"Periodical","name":"International Journal of Human\u2013Computer Interaction"},
        "volumeNumber":"41","issueNumber":"18","pagination":"11691-11711",
        "identifier":"https://doi.org/10.1080/10447318.2024.2443808",
        "url":"https://doi.org/10.1080/10447318.2024.2443808"
      }
    }
  ]
}
</script>"""

JSONLD = """<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"Person",
  "name":"Solomon B. Pobee",
  "jobTitle":"PhD Student, Computer Science",
  "email":"mailto:jnrpobee@byu.edu",
  "affiliation":{"@type":"CollegeOrUniversity","name":"Brigham Young University"},
  "knowsAbout":["Human-Computer Interaction","Youth Sports Technology","Injury Prevention","Nature Recreation","Learning Technology"],
  "identifier":"https://orcid.org/0009-0007-5172-0410",
  "sameAs":[
    "https://orcid.org/0009-0007-5172-0410",
    "https://scholar.google.com/citations?user=02WgxKoAAAAJ",
    "https://www.researchgate.net/profile/Solomon-Pobee",
    "https://github.com/jnrpobee",
    "https://linkedin.com/in/jnrpobee",
    "https://twitter.com/jnrpobee"
  ]
}
</script>"""

ART_PERFORMANCE = """<svg viewBox="0 0 400 150" role="presentation">
              <g stroke="currentColor" opacity=".10" stroke-width="1">
                <line x1="0" y1="38" x2="400" y2="38"/><line x1="0" y1="75" x2="400" y2="75"/><line x1="0" y1="112" x2="400" y2="112"/>
              </g>
              <polyline points="30,118 90,100 150,106 210,66 270,56 330,32 372,38" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
              <g fill="currentColor">
                <circle cx="90" cy="100" r="4"/><circle cx="210" cy="66" r="4"/><circle cx="330" cy="32" r="5.5"/>
              </g>
            </svg>"""

ART_COACH = """<svg viewBox="0 0 400 150" role="presentation">
              <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".85">
                <path d="M104 75 L192 42"/><path d="M104 75 L192 75"/><path d="M104 75 L192 108"/>
                <path d="M192 42 L286 42"/><path d="M192 75 L286 75"/><path d="M192 108 L286 108"/>
              </g>
              <circle cx="104" cy="75" r="10" fill="currentColor"/>
              <g fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="192" cy="42" r="6"/><circle cx="192" cy="75" r="6"/><circle cx="192" cy="108" r="6"/>
              </g>
              <g fill="currentColor" opacity=".16">
                <rect x="286" y="34" width="48" height="16" rx="3"/><rect x="286" y="67" width="64" height="16" rx="3"/><rect x="286" y="100" width="40" height="16" rx="3"/>
              </g>
            </svg>"""


# One page now, so there is nothing to navigate between. The header
# still shows the "Exit the blog" brand, which is the only way out.
BLOG_NAV = [
    ("blog.html", BLOG_NAME),
]


def nav_links(active):
    links = BLOG_NAV if active in (h for h, _ in BLOG_NAV) else NAV
    return "\n".join(
        '        <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", l)
        for h, l in links
    )


def header_brand(active):
    if active in (h for h, _ in BLOG_NAV):
        return """      <a class="brand blog-home-brand" href="index.html" aria-label="Exit the blog and return to the main homepage">
        <span class="blog-home-mark" aria-hidden="true">&larr;</span>
        <span class="brand-text">
          <strong>Home</strong>
          <em>Exit the blog</em>
        </span>
      </a>"""
    return """      <a class="brand" href="index.html" aria-label="Solomon B. Pobee &mdash; home">
        <img class="logo-mark" src="assets/logo-mark.svg" alt="" width="44" height="44" fetchpriority="high">
        <span class="brand-text">
          <strong>Solomon B. Pobee</strong>
          <em>PhD Student &middot; HCI &middot; BYU</em>
        </span>
      </a>"""


def pager(active):
    ids = [h for h, _ in NAV]
    # A page that is deliberately not in the nav — the blog — gets no
    # prev/next footer, because it sits outside the sequence.
    if active not in ids:
        return ""
    i = ids.index(active)
    prev = NAV[i - 1] if i > 0 else None
    nxt = NAV[i + 1] if i < len(NAV) - 1 else None
    if not prev and not nxt:
        return ""
    # The padded wrapper belongs to the pager, not to the shell. It used
    # to sit in the shell around {pager}, which meant a page that has no
    # pager still carried an empty .pad - 128px of nothing above the
    # footer on the blog and on 404.
    out = ['      <div class="pad">',
           '      <nav class="pager" aria-label="Page navigation">']
    if prev:
        out.append('        <a class="pg prev" href="%s"><span>Previous</span><strong>%s</strong></a>' % prev)
    if nxt:
        out.append('        <a class="pg next" href="%s"><span>Next</span><strong>%s</strong></a>' % nxt)
    out.append("      </nav>")
    out.append("      </div>")
    return "\n".join(out)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="description" content="{desc}" />
  <title>{title}</title>
{robots}


  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:site_name" content="Solomon B. Pobee">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{base}/assets/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Solomon B. Pobee, PhD student in human-computer interaction at Brigham Young University">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@jnrpobee">
  <meta name="twitter:creator" content="@jnrpobee">

  <link rel="icon" href="assets/favicon.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
  <link rel="manifest" href="assets/site.webmanifest">
  <meta name="theme-color" content="#f1efe9" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#07100e" media="(prefers-color-scheme: dark)">

  <script>
    /* only hide blocks for the scroll reveal when JS is running and the
       visitor hasn't asked for reduced motion */
    try {{
      if (!window.matchMedia('(prefers-reduced-motion:reduce)').matches) {{
        document.documentElement.classList.add('js-reveal');
      }}
    }} catch (e) {{}}
    /* An explicit theme choice, applied before first paint so the page
       never flashes the other one. No stored choice means the CSS decides,
       which keeps the site following the visitor's system setting. */
    try {{
      var t = localStorage.getItem('theme');
      if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t);
    }} catch (e) {{}}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
</head>
<body data-page="{key}">
  <a class="skip" href="#main">Skip to content</a>

  <div class="shell">
    <header class="site-header">
{brand}

      <nav class="site-nav" aria-label="Primary">
{nav}
      </nav>

      <div class="header-end">
        <button type="button" class="theme-toggle" data-theme-toggle aria-label="Switch theme"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><g class="i-sun"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6M17 17l1.6 1.6M18.6 5.4L17 7M7 17l-1.6 1.6"/></g><path class="i-moon" d="M20 14.2A8.2 8.2 0 0 1 9.8 4a8.4 8.4 0 1 0 10.2 10.2z"/></svg></button>
        <p class="header-note"><a class="status-dot" href="blog.html" aria-label="{blogname}"></a><span class="header-note-text">Building technology<br>for more human potential.</span></p>
      </div>

      <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open navigation">
        <i></i><i></i><i></i>
      </button>

      <div class="drawer" id="drawer">
        <nav class="site-nav" aria-label="Primary, mobile">
{nav}
        </nav>
        <p class="drawer-note"><span class="status-dot"></span>Building technology for more human potential.</p>
        <!-- The address and the profile links used to sit here as well.
             They are in the footer of every page, two taps away, and in a
             drawer that only has to get somebody to a page they were
             clutter between the navigation and the search. -->
        <button type="button" class="btn-s cmd-btn">Search this site <span aria-hidden="true">&#8984;K</span></button>
      </div>
    </header>

    <div class="scrim" id="scrim" hidden></div>

    <main id="main">
{body}
{pager}
    </main>

    <footer class="site-footer" id="contact">
      <div class="footer-brand">
        <img class="logo-mark logo-mark-sm" src="assets/logo-mark.svg" alt="" width="34" height="34" loading="lazy">
        <span class="footer-divider"></span>
        <a class="footer-copy" href="blog.html" aria-label="{blogname}">Solomon B. Pobee &middot; &copy; <span data-copyright-year>2026</span></a>
      </div>
      <div class="footer-links">
        <a href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a>
{socials}
      </div>
      <p class="footer-tagline">A more active tomorrow.</p>
    </footer>
  </div>

  <div class="palette" id="palette" role="dialog" aria-modal="true" aria-label="Command palette" hidden>
    <div class="palette-box">
      <input id="cmd-input" type="text" placeholder="Go to a page, copy an address, open a paper&hellip;" autocomplete="off" spellcheck="false">
      <ul id="cmd-list"></ul>
      <div class="palette-foot"><span>&#8593;&#8595; navigate</span><span>&#8629; select</span><span>esc close</span></div>
    </div>
  </div>

  <button type="button" class="totop" id="totop" aria-label="Back to top">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
  </button>

  <div class="toast" id="toast" role="status" aria-live="polite"></div>

{jsonld}
  <!-- Cloudflare Web Analytics -->
  <script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "533b27c2f1324a9ca8154b9de9fa3d2e"}}'></script>
  <!-- End Cloudflare Web Analytics -->
  <script src="script.js"></script>
</body>
</html>
"""

BODY = {}

BODY["home"] = """      <section class="hero pad" aria-labelledby="hero-title">
        <div class="hero-copy enter-1">
          <p class="eyebrow">RESEARCH <span>&times;</span> PEOPLE <span>&times;</span> PERFORMANCE</p>
          <h1 id="hero-title">Solomon B. Pobee</h1>
          <p class="hero-statement">I design and study technology<br>for human performance.</p>
          <p class="hero-summary">PhD researcher in human&ndash;computer interaction at Brigham Young University, exploring how interactive systems can support youth athletes, coaches, performance, and injury prevention &mdash; in clubs that operate without a support staff.</p>
          <div class="hero-actions">
            <a class="button button-primary" href="research.html">Explore research <span aria-hidden="true">&rarr;</span></a>
            <a class="button button-secondary" href="cv.html">View CV <span aria-hidden="true">&#8599;</span></a>
          </div>
        </div>

        <div class="portrait-panel enter-2" aria-label="Portrait of Solomon B. Pobee">
          <img class="portrait-photo" src="assets/portrait.jpg" alt="Solomon B. Pobee" width="900" height="1349" fetchpriority="high" decoding="async">
          <div class="portrait-copy">
            <p>People</p>
            <p>Technology</p>
            <p>Healthier athletes</p>
            <p>Brighter futures</p>
            <span></span>
          </div>
        </div>
      </section>

      <section class="focus-strip pad" aria-labelledby="focus-title">
        <p class="kicker" id="focus-title">FOCUS AREAS</p>
        <div class="focus-list">
          <p>Human&ndash;Computer Interaction</p>
          <p>Sports Technology</p>
          <p>Youth Athletics</p>
        </div>
      </section>

      <section class="projects pad" aria-labelledby="work-title">
        <div class="section-heading">
          <p class="kicker" id="work-title">SELECTED WORK</p>
          <a href="projects.html">View all projects <span aria-hidden="true">&rarr;</span></a>
        </div>

        <div class="project-grid">
          <article class="project-card">
            <div class="project-art" aria-hidden="true">""" + ART_PERFORMANCE + """</div>
            <div class="project-body">
              <p class="project-meta">HCI &middot; Data &middot; Systems</p>
              <h2>Youth Sports Performance System</h2>
              <p>A data-driven system to help young athletes and coaches track, understand, and improve performance &mdash; without overwhelming the people using it.</p>
              <a class="go" href="projects.html">View project <span aria-hidden="true">&rarr;</span></a>
            </div>
          </article>

          <article class="project-card">
            <div class="project-art" aria-hidden="true">""" + ART_COACH + """</div>
            <div class="project-body">
              <p class="project-meta">HCI &middot; Research &middot; Coaching</p>
              <h2>Coach Decision Support Tools</h2>
              <p>Interactive tools that help coaches make evidence-informed decisions about training, development, and athlete well-being.</p>
              <a class="go" href="projects.html">View project <span aria-hidden="true">&rarr;</span></a>
            </div>
          </article>
        </div>
      </section>

      <section class="projects pad" aria-labelledby="pubs-title" style="padding-bottom:64px;">
        <div class="section-heading">
          <p class="kicker" id="pubs-title">RECENT PUBLICATIONS</p>
          <a href="publications.html">All publications <span aria-hidden="true">&rarr;</span></a>
        </div>

        <div class="pubs">
          <article class="pub">
            <div class="pub-kind">Chapter &middot; 2026</div>
            <div>
              <a class="pub-title" href="https://doi.org/10.1007/978-3-032-13174-4_25" target="_blank" rel="noopener">MathBuddy: An LLM-Based Chatbot for Elementary Math Education</a>
              <p class="pub-authors">Saba Iqbal, <strong>Solomon Pobee</strong>, Akriti Adhikari, Benjamin Schooley</p>
              <p class="pub-venue">HCI International 2025 &ndash; Late Breaking Papers &middot; LNCS, Springer &middot; 392&ndash;403</p>
            </div>
          </article>
          <article class="pub">
            <div class="pub-kind">Journal &middot; 2025</div>
            <div>
              <a class="pub-title" href="https://doi.org/10.1080/10447318.2024.2443808" target="_blank" rel="noopener">Toward a Framework for the Design of Interactive Technology for Nature Recreation</a>
              <p class="pub-authors">Michael Jones, Tuomas Kari, Daniel Reich, Barrett Ens, Siyi Liu, <strong>Solomon B. Pobee</strong>, Florian Mueller</p>
              <p class="pub-venue">Int. Journal of Human&ndash;Computer Interaction &middot; 41(18), 11691&ndash;11711</p>
            </div>
          </article>
        </div>
      </section>

      <section class="split pad" aria-labelledby="about-title">
        <div class="split-intro">
          <p class="kicker">ABOUT</p>
          <h2 id="about-title">Technology is most interesting to me when it meets the real world.</h2>
          <span class="accent-line" style="margin-top:22px;"></span>
        </div>
        <div class="body-copy">
          <p>I&rsquo;m Solomon B. Pobee, a PhD student in Computer Science at Brigham Young University, working at the intersection of human&ndash;computer interaction, sport, and human performance.</p>
          <p>I&rsquo;m interested in designing and studying technologies that support young athletes, coaches, and communities &mdash; helping more people stay active, healthy, and reach their potential.</p>
          <p>I care about tools that hold up in practice, not systems that only look good in a lab.</p>
        </div>
      </section>"""

BODY["research"] = """      <section class="pad">
        <p class="eyebrow enter-1">RESEARCH <span>&times;</span> HCI <span>&times;</span> SPORT</p>
        <h1 class="enter-1">Research</h1>
        <p class="lead enter-2">I study how interactive systems can support youth athletes and coaches in settings where time, staffing, and access to specialised resources are limited.</p>
      </section>

      <section class="split pad">
        <div class="split-intro">
          <p class="kicker">CURRENTLY</p>
          <h2>Human&ndash;computer interaction for real-world sports environments.</h2>
        </div>
        <div class="body-copy">
          <p>I&rsquo;m a PhD student in Computer Science at Brigham Young University. My work focuses on adolescent sub-elite youth sports and the role technology can play in <strong>performance</strong>, <strong>club coordination</strong>, and <strong>injury prevention</strong>.</p>
          <p>The through-line is designing for contexts where the usual assumptions don&rsquo;t hold: no expert operator, no dedicated staff, no budget for the thing that would obviously solve the problem. I&rsquo;m particularly interested in systems that fit into existing coaching and athlete workflows rather than adding complexity to them.</p>
        </div>
      </section>

      <section class="pad" style="border-top:1px solid var(--border);">
        <div class="section-heading"><p class="kicker">FOCUS AREAS</p></div>
        <div class="detail-grid">
          <article class="detail-card">
            <span class="n">01</span>
            <h3>Human&ndash;Computer Interaction</h3>
            <p>Designing and evaluating interactive systems around the needs, constraints, and behaviours of real users.</p>
          </article>
          <article class="detail-card">
            <span class="n">02</span>
            <h3>Sports Technology</h3>
            <p>Exploring how digital tools can help athletes and coaches understand training, performance, and development.</p>
          </article>
          <article class="detail-card">
            <span class="n">03</span>
            <h3>Youth Athletics</h3>
            <p>Studying technology in sub-elite environments, where teams often operate with far fewer specialised resources.</p>
          </article>
          <article class="detail-card">
            <span class="n">04</span>
            <h3>Injury Prevention</h3>
            <p>Investigating how interactive tools and useful data representations can support healthier participation in sport.</p>
          </article>
        </div>
      </section>

      <section class="research-question pad">
        <p class="kicker">GUIDING QUESTION</p>
        <p>How can we build technology that gives athletes and coaches useful insight without making their work harder?</p>
      </section>

      <section class="pad" style="padding-top:0;">
        <p class="note">Published work across these areas is on the <a href="publications.html">Publications</a> page; systems in development are under <a href="projects.html">Projects</a>.</p>
      </section>"""

BODY["projects"] = """      <section class="pad">
        <p class="eyebrow enter-1">SELECTED <span>&times;</span> WORK</p>
        <h1 class="enter-1">Projects</h1>
        <p class="lead enter-2">Research and engineering work around HCI, sports technology, data, and human performance.</p>
      </section>

      <section class="projects pad" style="padding-top:44px;">
        <div class="project-grid">
          <article class="project-card">
            <div class="project-art" aria-hidden="true">""" + ART_PERFORMANCE + """</div>
            <div class="project-body">
              <p class="project-meta">HCI &middot; Data &middot; Systems</p>
              <h2>Youth Sports Performance System</h2>
              <p>A data-driven concept for helping young athletes and coaches track, understand, and improve performance without overwhelming the people using it.</p>
              <a class="go" href="mailto:jnrpobee@byu.edu?subject=Youth%20Sports%20Performance%20System">Ask about this project <span aria-hidden="true">&rarr;</span></a>
            </div>
          </article>

          <article class="project-card">
            <div class="project-art" aria-hidden="true">""" + ART_COACH + """</div>
            <div class="project-body">
              <p class="project-meta">HCI &middot; Research &middot; Coaching</p>
              <h2>Coach Decision Support Tools</h2>
              <p>Interactive concepts for presenting evidence in ways that help coaches make decisions around training, development, and athlete well-being.</p>
              <a class="go" href="mailto:jnrpobee@byu.edu?subject=Coach%20Decision%20Support%20Tools">Ask about this project <span aria-hidden="true">&rarr;</span></a>
            </div>
          </article>
        </div>
      </section>

      <section class="pad" style="border-top:1px solid var(--border);">
        <div class="section-heading">
          <p class="kicker">CODE</p>
          <a href="https://github.com/jnrpobee" target="_blank" rel="noopener">View all on GitHub <span aria-hidden="true">&#8599;</span></a>
          <a href="https://leetcode.com/u/pobee/" target="_blank" rel="noopener" style="margin-left:22px;">LeetCode <span aria-hidden="true">&#8599;</span></a>
        </div>
        <p class="note" style="margin-top:14px;">Open-source work &mdash; research tooling, data analysis, and systems built along the way.</p>

        <div class="repos">
          <a class="repo" style="--lang:#3572A5" data-repo="kennionblack/ai-audio-transcriber" href="https://github.com/kennionblack/ai-audio-transcriber" target="_blank" rel="noopener">
            <span class="repo-name"><em>kennionblack /</em> ai-audio-transcriber</span>
            <p class="repo-desc">An end-to-end, multi-agent pipeline that turns raw interview audio into structured qualitative insights.</p>
            <span class="repo-meta">
              <span class="repo-lang"><i></i>Python</span>
              <span class="repo-role">Contributor</span>
              <span data-stars hidden></span><span data-updated hidden></span>
            </span>
          </a>

          <a class="repo" style="--lang:#3572A5" data-repo="jnrpobee/Research-paper-retrieval" href="https://github.com/jnrpobee/Research-paper-retrieval" target="_blank" rel="noopener">
            <span class="repo-name">Research-paper-retrieval</span>
            <p class="repo-desc">An agentic system to retrieve research papers from journals and conferences.</p>
            <span class="repo-meta">
              <span class="repo-lang"><i></i>Python</span>
              <span data-stars hidden></span><span data-updated hidden></span>
            </span>
          </a>

          <a class="repo" style="--lang:#3572A5" data-repo="jnrpobee/hiking" href="https://github.com/jnrpobee/hiking" target="_blank" rel="noopener">
            <span class="repo-name">hiking</span>
            <p class="repo-desc">Recreational survey project analysing outdoor-recreation survey data with pandas &mdash; groundwork adjacent to the nature recreation framework paper.</p>
            <span class="repo-meta">
              <span class="repo-lang"><i></i>Python</span>
              <span data-stars hidden></span><span data-updated hidden></span>
            </span>
          </a>

          <a class="repo" style="--lang:#3572A5" data-repo="jnrpobee/AI-audio-text-1.0" href="https://github.com/jnrpobee/AI-audio-text-1.0" target="_blank" rel="noopener">
            <span class="repo-name">AI-audio-text-1.0</span>
            <p class="repo-desc">A multi-agent system that transcribes interview and podcast audio into text &mdash; the first version of the transcription pipeline.</p>
            <span class="repo-meta">
              <span class="repo-lang"><i></i>Python</span>
              <span data-stars hidden></span><span data-updated hidden></span>
            </span>
          </a>

          <a class="repo" style="--lang:#B07219" data-repo="jnrpobee/chess" href="https://github.com/jnrpobee/chess" target="_blank" rel="noopener">
            <span class="repo-name">chess</span>
            <p class="repo-desc">Full-stack chess application with server, client, and game logic, built for BYU CS 240.</p>
            <span class="repo-meta">
              <span class="repo-lang"><i></i>Java</span>
              <span data-stars hidden></span><span data-updated hidden></span>
            </span>
          </a>
        </div>
      </section>

      <!--LEETCODE-->

      <section class="split pad">
        <div class="split-intro">
          <p class="kicker">IN PROGRESS</p>
          <h2>More case studies will live here.</h2>
        </div>
        <div class="body-copy">
          <p>As projects mature, this page can expand into full case studies with the problem, methods, system design, findings, publications, and implementation details.</p>
        </div>
      </section>"""

BODY["publications"] = """      <section class="pad">
        <p class="eyebrow enter-1">PEER-REVIEWED <span>&times;</span> WORK</p>
        <h1 class="enter-1">Publications</h1>
        <p class="lead enter-2">Newest first. Every entry carries a formatted citation you can copy.</p>

        <div class="pub-search">
          <input type="search" id="pub-search" placeholder="Search titles, authors, venues&hellip;"
                 autocomplete="off" spellcheck="false" aria-label="Search publications"
                 aria-describedby="pub-search-hint">
          <kbd aria-hidden="true">/</kbd>
          <span id="pub-search-hint" class="sr-only">Press the slash key to search from anywhere on this page. Results are counted above the list.</span>
        </div>

        <div class="filters" role="group" aria-label="Filter publications by topic">
          <button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>
          <button type="button" class="chip" data-filter="nature" aria-pressed="false">Nature Recreation</button>
          <button type="button" class="chip" data-filter="learning" aria-pressed="false">Learning Technology</button>
          <div class="counts">
            <span class="count" id="pub-count" role="status" aria-live="polite">2 publications</span>
            <span class="count count-note">Peer reviewer for 5 papers</span>
          </div>
        </div>

        <!--PUBGROUPS-->

        <div class="empty" id="pub-empty" hidden>No publications in this area yet.</div>

        <p class="note">Full record on <a href="https://orcid.org/0009-0007-5172-0410" target="_blank" rel="noopener">ORCID</a> and <a href="https://www.researchgate.net/profile/Solomon-Pobee" target="_blank" rel="noopener">ResearchGate</a>.</p>
      </section>"""

BODY["about"] = """      <section class="pad">
        <p class="eyebrow enter-1">ABOUT <span>&times;</span> SOLOMON</p>
        <h1 class="enter-1" style="font-family:var(--serif);font-weight:400;font-size:clamp(2.4rem,5.4vw,5rem);line-height:1.02;letter-spacing:-.02em;">Technology is most interesting to me when it meets the real world.</h1>
      </section>

      <section class="split pad">
        <div class="portrait-panel" style="min-height:520px;">
          <img class="portrait-photo" src="assets/portrait.jpg" alt="Solomon B. Pobee" width="900" height="1349" loading="lazy" decoding="async">
        </div>
        <div class="body-copy" style="align-self:center;">
          <p class="kicker">HELLO</p>
          <p style="font-family:var(--serif);font-size:clamp(1.8rem,3.2vw,2.8rem);line-height:1.08;color:var(--text);margin:18px 0 22px;max-width:none;">I&rsquo;m Solomon B. Pobee, a PhD student in Computer Science at Brigham Young University.</p>
          <p>My work sits at the intersection of human&ndash;computer interaction, sport, and human performance. I&rsquo;m interested in technology that helps people make better decisions in environments where resources, staffing, and technical infrastructure may be limited.</p>
          <p>A major focus of my research is adolescent sub-elite youth sports: understanding the needs of athletes and coaches, then designing interactive systems that can support performance, development, and injury prevention.</p>
          <p>I care about tools that work in practice &mdash; not just systems that look good in a lab.</p>
        </div>
      </section>

      <section class="pad" style="border-top:1px solid var(--border);">
        <p class="kicker">HOW I THINK ABOUT THE WORK</p>
        <div class="values-grid">
          <article class="value">
            <h3>People first.</h3>
            <p>Start with the people, constraints, and routines already present in the environment.</p>
          </article>
          <article class="value">
            <h3>Useful over flashy.</h3>
            <p>Good technology should clarify decisions rather than create another layer of work.</p>
          </article>
          <article class="value">
            <h3>Research in context.</h3>
            <p>Real-world settings reveal needs and tradeoffs that controlled environments can miss.</p>
          </article>
        </div>

        <p class="sub">Beyond the lab</p>
        <div class="body-copy">
          <p>I came to research by a longer route than most. I served three years in Abidjan, taught language and teaching skills at the Missionary Training Center in Accra, and spent two years at Soci&eacute;t&eacute; G&eacute;n&eacute;rale reconciling transactions across internal ledgers, the central bank and correspondent banks.</p>
          <p>That last one was better preparation than it sounds. Reconciliation is largely the work of finding where the records stop agreeing with reality and establishing why &mdash; which is not so far from running a study. I work in English and French.</p>
        </div>
      </section>

      <section class="split pad">
        <div class="split-intro">
          <p class="kicker">CONTACT</p>
          <h2>Get in touch.</h2>
          <span class="accent-line" style="margin-top:22px;"></span>
        </div>
        <div>
          <p class="body-copy" style="margin:0;">Happy to talk research, collaboration, or anything at the intersection of HCI and youth sport. If you&rsquo;re a coach, club, or researcher working with under-resourced teams, I&rsquo;d particularly like to hear from you.</p>
          <div class="mail-wrap">
            <a class="mail-big" href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a>
            <button type="button" class="btn-s" data-copy-mail>Copy</button>
          </div>
          <p class="mail-alt">or <a class="text-link" href="mailto:jnrpobee@outlook.fr">jnrpobee@outlook.fr</a></p>
          <ul class="links">
            <li><a href="https://github.com/jnrpobee" target="_blank" rel="noopener"><span>GitHub</span><span class="h">jnrpobee</span></a></li>
            <li><a href="https://scholar.google.com/citations?user=02WgxKoAAAAJ" target="_blank" rel="noopener"><span>Google Scholar</span><span class="h">Publications</span></a></li>
            <li><a href="https://orcid.org/0009-0007-5172-0410" target="_blank" rel="noopener"><span>ORCID</span><span class="h">Solomon B Pobee</span></a></li>
            <li><a href="https://www.researchgate.net/profile/Solomon-Pobee" target="_blank" rel="noopener"><span>ResearchGate</span><span class="h">Solomon-Pobee</span></a></li>
            <li><a href="https://linkedin.com/in/jnrpobee" target="_blank" rel="noopener"><span>LinkedIn</span><span class="h">in/jnrpobee</span></a></li>
            <li><a href="https://leetcode.com/u/pobee/" target="_blank" rel="noopener"><span>LeetCode</span><span class="h">pobee</span></a></li>
            <li><a href="https://twitter.com/jnrpobee" target="_blank" rel="noopener"><span>X / Twitter</span><span class="h">@jnrpobee</span></a></li>
          </ul>
        </div>
      </section>"""

BODY["blog"] = """      <section class="notes-hero pad" aria-labelledby="notes-title">
        <div class="notes-hero-copy enter-1">
          <!-- The masthead. The name is set in the serif at display size over
               a hairline rule, with a dateline above it and the standfirst
               below, the way a magazine opens a section. Change the name in
               one place and the nav label, the <title> and the two secret
               doors follow — see BLOG_NAME near the top of this file. -->
          <p class="eyebrow">OFF THE CLOCK</p>
          <h1 id="notes-title" class="masthead-name">The Margin</h1>
          <p class="masthead-standfirst">Small reflections on work, routines, curiosity, and the parts of life that shape how I think.</p>
          <div class="notes-topics" aria-label="Topics covered">
            <span>Lifestyle</span>
            <span>Campus life</span>
            <span>PhD life</span>
            <span>BYU</span>
            <span>Field notes</span>
          </div>
        </div>

        <div class="notes-playground enter-2"<!--NOTECOUNT-->>
          <p class="notes-board-label">FIELD NOTES / LIFE IN MOTION</p>
          <svg class="notes-thread" viewBox="0 0 440 390" role="presentation">
            <path d="M72 104 C162 26 224 178 352 92 S384 262 248 286 S106 246 76 326"/>
          </svg>
<!--NOTECARDS-->
          <span class="notes-spark notes-spark-one" aria-hidden="true">&#10022;</span>
          <span class="notes-spark notes-spark-two" aria-hidden="true">&#10022;</span>
          <p class="notes-mantra">notice <i>&rarr;</i> pause <i>&rarr;</i> learn <i>&rarr;</i> repeat</p>
<!--NOTEDATA-->
        </div>
      </section>

      <section class="focus-strip notes-focus pad" aria-labelledby="notes-focus-title">
        <p class="kicker" id="notes-focus-title">A FEW GUIDING IDEAS</p>
        <div class="focus-list">
          <p>Stay curious.</p>
          <p>Make room.</p>
          <p>Notice the ordinary.</p>
        </div>
      </section>

      <section class="notes-feed pad" aria-labelledby="recent-notes-title">
        <div class="section-heading">
          <p class="kicker" id="recent-notes-title">ALL NOTES</p>
          <p class="notes-order">NEWEST FIRST &middot; TAP TO READ</p>
        </div>
<!--CATCOLOURS-->
<!--NOTESTALLY-->
        <div class="posts" id="blog-posts">
<!--BLOGPOSTS-->
        </div>
<!--NOTESEND-->
      </section>

<!--CATTILES-->

      <section class="notes-return pad">
        <p class="note">You found this by clicking the dot. <a class="text-link" href="index.html">Back to the front</a>.</p>
      </section>"""

BODY["cv"] = """      <section class="pad">
        <p class="eyebrow enter-1">CURRICULUM <span>&times;</span> VITAE</p>
        <h1 class="enter-1">Solomon B. Pobee</h1>
        <p class="lead enter-2">Computer Science PhD student &middot; Human&ndash;Computer Interaction &middot; Brigham Young University</p>
        <div class="cv-actions enter-2"><!--CVACTIONS-->
        </div>
      </section>

      <section class="pad" style="padding-top:20px;">
        <div class="cv-row">
          <p class="kicker">CURRENTLY</p>
          <div>
            <h3>Brigham Young University</h3>
            <p>PhD student in Computer Science, studying human&ndash;computer interaction with a focus on adolescent sub-elite youth sports.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">RESEARCH</p>
          <div>
            <h3>Research areas</h3>
            <p>Human&ndash;Computer Interaction &middot; Sports Technology &middot; Youth Athletics &middot; Outdoor Recreation &middot; Injury Prevention</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">PUBLICATIONS</p>
          <div>
            <h3>Two peer-reviewed publications</h3>
            <p>A journal article in the <em>International Journal of Human&ndash;Computer Interaction</em> (2025) and a Springer book chapter (2026). Full details on the <a class="text-link" href="publications.html">Publications</a> page.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">CONTACT</p>
          <div>
            <h3>Email</h3>
            <p><a class="text-link" href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a> &middot; <a class="text-link" href="mailto:jnrpobee@outlook.fr">jnrpobee@outlook.fr</a></p>
          </div>
        </div>

        <p class="sub">Education</p>
        <div class="cv-row">
          <p class="kicker">2024 &mdash; PRESENT</p>
          <div>
            <h3>Brigham Young University</h3>
            <p><strong>PhD, Computer Science</strong> &mdash; emphasis in Human&ndash;Computer Interaction. Provo, Utah.<br>
            Academic Scholarship. Member of the Graduate Studies Association. Coursework in human&ndash;computer interaction, privacy, outdoor and recreation HCI, algorithm design and analysis, software engineering, and agentic AI systems.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2012 &mdash; 2020</p>
          <div>
            <h3>Brigham Young University &ndash; Idaho</h3>
            <p><strong>BSc, Computer Science</strong> &mdash; emphasis in Web Design and Development, minor in Information Technology. Rexburg, Idaho.<br>
            Coursework in system security, cyber security, software applications, and web engineering. Member of the BYU Management Society.</p>
          </div>
        </div>

        <p class="sub">Experience</p>
        <div class="cv-row">
          <p class="kicker">2024 &mdash; PRESENT</p>
          <div>
            <h3>Research Assistant &middot; Brigham Young University</h3>
            <p>Provo, Utah. Lead a team of student researchers in the lab, supporting them in carrying out and presenting research. Ran a study on how technology affordances shape engagement with nature during a day hike, and what that implies for designing technology that supports wellbeing rather than competing with it. Lead a toe-sensor project prototyping hands-free interaction that keeps attention on the activity rather than the device.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2021 &mdash; 2023</p>
          <div>
            <h3>Reconciliation Officer &middot; Soci&eacute;t&eacute; G&eacute;n&eacute;rale, Head Office</h3>
            <p>Accra, Ghana. Reconciled daily transactions across internal ledgers, the central bank and correspondent banks. Investigated breaks in suspense and clearing accounts with branch teams, cutting outstanding items by 30% in six months, and worked with treasury, operations and IT to shorten exception-handling turnaround by 20%. Monitored unusual entries and escalated high-risk items for fraud prevention and regulatory compliance, and introduced process controls and automation that removed hours of manual checking each week.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2018 &mdash; 2019</p>
          <div>
            <h3>Instructor &middot; Missionary Training Center</h3>
            <p>Accra, Ghana. Trained missionaries in teaching skills and in their assigned mission language, running role plays, practice lessons and feedback sessions. Used immersion and conversation practice to accelerate language learning, and adjusted instruction to different learning speeds. Coached individuals one to one, and maintained lesson plans, schedules and progress reporting.</p>
          </div>
        </div>

        <p class="sub">Service</p>
        <div class="cv-row">
          <p class="kicker">ONGOING</p>
          <div>
            <h3>Peer review</h3>
            <p>Reviewer for five papers, including submissions to the ACM Conference on Human&ndash;Computer Interaction and Sports.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">OCT 2026</p>
          <div>
            <h3>Student Volunteer &middot; CSCW 2026</h3>
            <p>ACM Conference on Computer-Supported Cooperative Work and Social Computing. Salt Lake City, Utah.</p>
          </div>
        </div>

        <p class="sub">Awards</p>
        <div class="cv-row">
          <p class="kicker">2025</p>
          <div>
            <h3>BYU Professional Presentation Award</h3>
            <p>Brigham Young University.</p>
          </div>
        </div>

        <p class="sub">Invited &amp; upcoming</p>
        <div class="cv-row">
          <p class="kicker">JUL 2025</p>
          <div>
            <h3>NatureHCI: Towards Designing Computer-Enriched Nature Experiences</h3>
            <p>Schloss Dagstuhl &ndash; Leibniz-Zentrum f&uuml;r Informatik, Germany.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">MAY 2026</p>
          <div>
            <h3>American College of Sports Medicine Annual Meeting</h3>
            <p>Salt Lake City, Utah.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">OCT 2026</p>
          <div>
            <h3>CSCW 2026</h3>
            <p>ACM Conference on Computer-Supported Cooperative Work and Social Computing. Salt Lake City, Utah.</p>
          </div>
        </div>

        <p class="sub">Certifications</p>
        <div class="cv-row">
          <p class="kicker">RESEARCH</p>
          <div>
            <h3>Research ethics</h3>
            <p>Responsible Conduct of Research &mdash; Faculty and Student Researchers.<br>
            Social and Behavioral Research Investigators and Mentors.</p>
          </div>
        </div>

        <p class="sub">Skills &amp; languages</p>
        <div class="cv-row">
          <p class="kicker">TECHNICAL</p>
          <div>
            <h3>Tools and methods</h3>
            <p>Python, C++, MATLAB, PHP &middot; Java, MySQL<br>
            SciPy, pandas, Seaborn<br>
            Quantitative and qualitative research methods</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">LANGUAGES</p>
          <div>
            <h3>English and French</h3>
            <p>English, native. French, professional working proficiency.</p>
          </div>
        </div>
      </section>"""


socials_html = "\n".join(
    '          <a href="%s" target="_blank" rel="noopener">%s</a>' % (u, n) for u, n in SOCIALS
)

NOT_FOUND_BODY = """      <section class="pad">
        <p class="eyebrow enter-1">404 <span>&times;</span> NOT FOUND</p>
        <h1 class="enter-1">This page doesn\u2019t exist.</h1>
        <p class="lead enter-2">The link may be out of date, or the page may have moved.</p>
        <div class="hero-actions" style="margin-top:34px;">
          <a class="button button-primary" href="index.html">Back to home <span aria-hidden="true">&rarr;</span></a>
          <a class="button button-secondary" href="publications.html">Publications <span aria-hidden="true">&rarr;</span></a>
        </div>
      </section>"""


_LC = lc_section()

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
