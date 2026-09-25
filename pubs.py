#!/usr/bin/env python3
"""Publications, and the citation panel that opens under each one."""
import html as _html

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
    """The publications, grouped, in PUB_GROUPS order.

    A group with nothing in it is left out rather than rendered as an
    empty heading, so the page never announces "Posters" above nothing.
    The count beside each heading is the figure the page ships with;
    script.js recounts it whenever a filter or search narrows the list.
    """
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
