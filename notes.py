#!/usr/bin/env python3
"""Everything that arranges the blog. The writing itself is in posts.py.

This is the one page with enough machinery to deserve a module of its
own: the board in the hero and the notes that rotate through it, the
list below, the filters, the month calendar, the category tiles and the
colours they carry.

Nothing here needs editing to publish a post."""
import re
import html as _html
import json as _json

from core import BLOG_NAME, OUT
from posts import BLOG_CATEGORIES, POSTS

# ── the blog ──────────────────────────────────────────────────────────────
# An unlisted page. It is not in the nav, not in sitemap.xml, and carries
# a noindex tag, so it will not turn up in a search. It is reached by the
# little dot beside the header note. That makes it unlisted rather than
# private: anyone given the address, or reading the page source, can open
# it. Do not put anything on it you would mind a stranger reading.
#



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
