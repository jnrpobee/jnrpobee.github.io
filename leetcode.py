#!/usr/bin/env python3
"""The LeetCode panel on the projects page."""
import html as _html
import json as _json
import math as _math

from core import OUT

LC_MARK = "<!--LEETCODE-->"
# The colours live in styles.css so they can follow the theme; these
# are the class suffixes that select them.
LC_DIFF = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]

_R, _CX, _GAP = 54.0, 64.0, 3.0          # donut radius, centre, arc gap in px
_C = 2 * _math.pi * _R


def _donut(solved, total):
    """Composition of the solved problems, as one arc per difficulty.

    One circle per difficulty, each drawn as a dash the length of its
    share of the ring and pushed round by everything before it - which
    is how you draw a donut with no library. _GAP is subtracted from
    every arc so neighbouring segments do not touch: abutting arcs read
    as one continuous ring, and the eye stops being able to tell where
    a difficulty ends.

    Each arc carries a <title>, so hovering names the slice and a screen
    reader gets the figure. A difficulty with nothing solved is left out
    rather than drawn as a zero-length arc.
    """
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
    """The whole panel, or "" if there is nothing trustworthy to show.

    The figures come from leetcode.json, which update_leetcode.py
    refreshes during the deploy. Every way that can go wrong ends the
    same way - no file, unreadable JSON, a missing or nonsensical total -
    and the answer is always to leave the panel out rather than render
    an empty one. A panel showing nothing looks broken; no panel just
    looks like a page without a panel.
    """
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
