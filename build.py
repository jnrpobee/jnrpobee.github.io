#!/usr/bin/env python3
"""Generate the static pages from one shared shell."""
import pathlib

OUT = pathlib.Path(__file__).parent

# Where the site will live. Change this one line if you host it elsewhere —
# canonical URLs, Open Graph tags and sitemap.xml all follow from it.
BASE_URL = "https://www.solomonbpobee.com"


NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("projects.html", "Projects"),
    ("publications.html", "Publications"),
    ("about.html", "About"),
    ("cv.html", "CV"),
]

# Pages are written to disk as .html files, because that is what a static host
# serves from. They are *linked* without the extension: GitHub Pages resolves
# /research to research.html on its own, and a visitor should never see a
# filename in the address bar. clean_links() below does the rewriting, so the
# page templates can go on referring to plain filenames.
import re

def public_path(filename):
    """The address a visitor sees for a given file on disk."""
    return "/" if filename == "index.html" else "/" + filename[:-len(".html")]

_LINK = re.compile(r'(href|action)="(' + "|".join(f for f, _ in NAV) + r')((?:#|\?)[^"]*)?"')

def clean_links(html):
    """Rewrite internal links from filenames to the addresses visitors see."""
    return _LINK.sub(
        lambda m: '%s="%s%s"' % (m.group(1), public_path(m.group(2)), m.group(3) or ""),
        html,
    )


# ── LeetCode panel ────────────────────────────────────────────────
# The numbers live in leetcode.json, refreshed by update_leetcode.py during
# the deploy. If that file is missing or unreadable the panel is simply left
# out rather than rendered with nothing in it.
import html as _html
import json as _json

LC_MARK = "<!--LEETCODE-->"
LC_TIERS = [("advanced", "Advanced"), ("intermediate", "Intermediate"),
            ("fundamental", "Fundamental")]


def lc_section():
    try:
        d = _json.loads((OUT / "leetcode.json").read_text(encoding="utf-8"))
    except Exception:
        return ""

    total = (d.get("solved") or {}).get("all")
    if not isinstance(total, int):
        return ""

    lang = (d.get("language") or {}).get("name")
    tiers = d.get("tiers") or {}
    counts = [r.get("n", 0) for rows in tiers.values() for r in rows]
    top = max(counts) if counts else 1

    blocks = []
    for key, label in LC_TIERS:
        rows = [r for r in (tiers.get(key) or []) if isinstance(r.get("n"), int)]
        if not rows:
            continue
        items = "\n".join(
            '            <li style="--n:%d"><span>%s</span><b>%d</b></li>'
            % (r["n"], _html.escape(str(r.get("tag", ""))), r["n"])
            for r in rows)
        blocks.append(
            '          <div class="lc-tier">\n'
            '            <p class="lc-tier-k">%s</p>\n'
            '            <ul class="lc-tags">\n%s\n            </ul>\n'
            '          </div>' % (label, items))

    solved_line = "<strong>%d</strong> problems solved" % total
    if lang:
        solved_line += " <em>in %s</em>" % _html.escape(lang).replace(" ", "&nbsp;")

    note = ("Topic tags as shown on the profile &mdash; a single problem can carry "
            "several, so these don&rsquo;t sum to the total.")
    when = d.get("fetched")
    if when:
        try:
            import datetime as _dt
            note += " Last checked %s." % _dt.date.fromisoformat(when).strftime("%-d %B %Y")
        except Exception:
            pass

    return (
        '      <section class="lc">\n'
        '        <div class="lc-head">\n'
        '          <div>\n'
        '            <p class="lc-k">LeetCode</p>\n'
        '            <p class="lc-total">%s</p>\n'
        '          </div>\n'
        '          <a class="btn-s btn-go" href="https://leetcode.com/u/%s/" target="_blank" '
        'rel="noopener">View profile <span aria-hidden="true">&#8599;</span></a>\n'
        '        </div>\n'
        '        <div class="lc-tiers" style="--max:%d">\n%s\n        </div>\n'
        '        <p class="lc-note">%s</p>\n'
        '      </section>'
        % (solved_line, _html.escape(str(d.get("username") or "pobee")),
           top, "\n".join(blocks), note)
    )

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
              <g stroke="rgba(245,243,237,.10)" stroke-width="1">
                <line x1="0" y1="38" x2="400" y2="38"/><line x1="0" y1="75" x2="400" y2="75"/><line x1="0" y1="112" x2="400" y2="112"/>
              </g>
              <polyline points="30,118 90,100 150,106 210,66 270,56 330,32 372,38" fill="none" stroke="#8bff43" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
              <g fill="#8bff43">
                <circle cx="90" cy="100" r="4"/><circle cx="210" cy="66" r="4"/><circle cx="330" cy="32" r="5.5"/>
              </g>
            </svg>"""

ART_COACH = """<svg viewBox="0 0 400 150" role="presentation">
              <g stroke="#8bff43" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".85">
                <path d="M104 75 L192 42"/><path d="M104 75 L192 75"/><path d="M104 75 L192 108"/>
                <path d="M192 42 L286 42"/><path d="M192 75 L286 75"/><path d="M192 108 L286 108"/>
              </g>
              <circle cx="104" cy="75" r="10" fill="#8bff43"/>
              <g fill="none" stroke="#8bff43" stroke-width="1.8">
                <circle cx="192" cy="42" r="6"/><circle cx="192" cy="75" r="6"/><circle cx="192" cy="108" r="6"/>
              </g>
              <g fill="rgba(245,243,237,.16)">
                <rect x="286" y="34" width="48" height="16" rx="3"/><rect x="286" y="67" width="64" height="16" rx="3"/><rect x="286" y="100" width="40" height="16" rx="3"/>
              </g>
            </svg>"""


def nav_links(active):
    return "\n".join(
        '        <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", l)
        for h, l in NAV
    )


def pager(active):
    ids = [h for h, _ in NAV]
    i = ids.index(active)
    prev = NAV[i - 1] if i > 0 else None
    nxt = NAV[i + 1] if i < len(NAV) - 1 else None
    if not prev and not nxt:
        return ""
    out = ['      <nav class="pager" aria-label="Page navigation">']
    if prev:
        out.append('        <a class="pg prev" href="%s"><span>Previous</span><strong>%s</strong></a>' % prev)
    if nxt:
        out.append('        <a class="pg next" href="%s"><span>Next</span><strong>%s</strong></a>' % nxt)
    out.append("      </nav>")
    return "\n".join(out)


SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="description" content="{desc}" />
  <title>{title}</title>


  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="{ogtype}">
  <meta property="og:site_name" content="Solomon B. Pobee">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{{desc}}">
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
  <meta name="theme-color" content="#07100e">

  <script>
    /* only hide blocks for the scroll reveal when JS is running and the
       visitor hasn't asked for reduced motion */
    try {{
      if (!window.matchMedia('(prefers-reduced-motion:reduce)').matches) {{
        document.documentElement.classList.add('js-reveal');
      }}
    }} catch (e) {{}}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css" />
</head>
<body data-page="{key}">
  <a class="skip" href="#main">Skip to content</a>

  <div class="shell">
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="Solomon B. Pobee &mdash; home">
        <img class="logo-mark" src="assets/logo-mark.svg" alt="" width="44" height="44" fetchpriority="high">
        <span class="brand-text">
          <strong>Solomon B. Pobee</strong>
          <em>PhD Student &middot; HCI &middot; BYU</em>
        </span>
      </a>

      <nav class="site-nav" aria-label="Primary">
{nav}
      </nav>

      <p class="header-note"><span class="status-dot"></span>Building technology<br>for more human potential.</p>

      <button class="menu-toggle" id="menu-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open navigation">
        <i></i><i></i><i></i>
      </button>

      <div class="drawer" id="drawer">
        <nav class="site-nav" aria-label="Primary, mobile">
{nav}
        </nav>
        <p class="drawer-note"><span class="status-dot"></span>Building technology for more human potential.</p>
        <a class="drawer-mail" href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a>
        <div class="footer-links">
{socials}
        </div>
        <button type="button" class="btn-s cmd-btn">Search this site <span aria-hidden="true">&#8984;K</span></button>
      </div>
    </header>

    <div class="scrim" id="scrim" hidden></div>

    <main id="main">
{body}
      <div class="pad">
{pager}
      </div>
    </main>

    <footer class="site-footer" id="contact">
      <div class="footer-brand">
        <img class="logo-mark logo-mark-sm" src="assets/logo-mark.svg" alt="" width="34" height="34" loading="lazy">
        <span class="footer-divider"></span>
        <span>Solomon B. Pobee &middot; &copy; <span data-year>2026</span></span>
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

        <div class="filters" role="group" aria-label="Filter publications by topic">
          <button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>
          <button type="button" class="chip" data-filter="nature" aria-pressed="false">Nature Recreation</button>
          <button type="button" class="chip" data-filter="learning" aria-pressed="false">Learning Technology</button>
          <div class="counts">
            <span class="count" id="pub-count" role="status" aria-live="polite">2 publications</span>
            <span class="count count-note">Peer reviewer for 5 papers</span>
          </div>
        </div>

        <section class="pub-group" data-group="journal">
          <h3 class="group-head">Journal Articles <span class="group-count" data-group-count>1</span></h3>
          <div class="pubs">
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
              <div class="cite-panel" id="c1" hidden>
<pre>@article{jones2025nature,
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
}</pre>
                <div class="copy-wrap"><button type="button" class="btn-s" data-copy-bib="c1">Copy BibTeX</button></div>
              </div>
            </div>
          </article>
          </div>
        </section>

        <section class="pub-group" data-group="conference">
          <h3 class="group-head">Conference Papers &amp; Chapters <span class="group-count" data-group-count>1</span></h3>
          <div class="pubs">
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
              <div class="cite-panel" id="c2" hidden>
<pre>@incollection{iqbal2026mathbuddy,
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
}</pre>
                <div class="copy-wrap"><button type="button" class="btn-s" data-copy-bib="c2">Copy BibTeX</button></div>
              </div>
            </div>
          </article>
          </div>
        </section>

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
        <div class="slot">
          <span class="tag">Your words go here</span>
          <p>A few lines in your own voice &mdash; where you&rsquo;re from, how you came to this work, what you do when you&rsquo;re not doing research.</p>
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
          <ul class="links">
            <li><a href="https://github.com/jnrpobee" target="_blank" rel="noopener"><span>GitHub</span><span class="h">jnrpobee</span></a></li>
            <li><a href="https://scholar.google.com/citations?user=02WgxKoAAAAJ" target="_blank" rel="noopener"><span>Google Scholar</span><span class="h">Publications</span></a></li>
            <li><a href="https://orcid.org/0009-0007-5172-0410" target="_blank" rel="noopener"><span>ORCID</span><span class="h">0009-0007-5172-0410</span></a></li>
            <li><a href="https://www.researchgate.net/profile/Solomon-Pobee" target="_blank" rel="noopener"><span>ResearchGate</span><span class="h">Solomon-Pobee</span></a></li>
            <li><a href="https://linkedin.com/in/jnrpobee" target="_blank" rel="noopener"><span>LinkedIn</span><span class="h">in/jnrpobee</span></a></li>
            <li><a href="https://leetcode.com/u/pobee/" target="_blank" rel="noopener"><span>LeetCode</span><span class="h">pobee</span></a></li>
            <li><a href="https://twitter.com/jnrpobee" target="_blank" rel="noopener"><span>X / Twitter</span><span class="h">@jnrpobee</span></a></li>
          </ul>
        </div>
      </section>"""

BODY["cv"] = """      <section class="pad">
        <p class="eyebrow enter-1">CURRICULUM <span>&times;</span> VITAE</p>
        <h1 class="enter-1">Solomon B. Pobee</h1>
        <p class="lead enter-2">Computer Science PhD student &middot; Human&ndash;Computer Interaction &middot; Brigham Young University</p>
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
            <p>Human&ndash;Computer Interaction &middot; Sports Technology &middot; Youth Athletics &middot; Data Visualisation &middot; Injury Prevention</p>
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
            <p><a class="text-link" href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a></p>
          </div>
        </div>

        <p class="sub">Education</p>
        <div class="slot">
          <span class="tag">To add</span>
          <p>Degrees, institutions, and dates &mdash; including your prior degree before BYU.</p>
        </div>

        <p class="sub">Experience</p>
        <div class="slot">
          <span class="tag">To add</span>
          <p>Research, teaching, or industry roles: title, organisation, dates, and a line on what you worked on.</p>
        </div>

        <p class="sub">Service &amp; teaching</p>
        <div class="slot">
          <span class="tag">Optional</span>
          <p>Reviewing, mentoring, courses taught or assisted. Skip it if you have none yet.</p>
        </div>

        <p class="note"><strong>Temporary web CV.</strong> When your full CV is ready, this page can either carry it in full or offer a prominent PDF download while keeping this short web version.</p>
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
        desc=desc,
        title=title,
        canonical=BASE_URL + public_path(filename),
        ogtitle=title,
        ogtype=("profile" if key in ("home", "about") else "website"),
        base=BASE_URL,
        key=key,
        nav=nav_links(filename),
        socials=socials_html,
        body=BODY[key],
        pager=pager(filename),
        jsonld=(JSONLD if key == "home" else (SCHOLAR_LD if key == "publications" else "")),
    )
    (OUT / filename).write_text(clean_links(html.replace(LC_MARK, _LC)), encoding="utf-8")
    print("wrote", filename, len(html), "bytes")

# ── sitemap.xml, robots.txt and a 404 page ────────────────────────
import datetime
_today = datetime.date.today().isoformat()
_urls = "\n".join(
    '  <url><loc>%s%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>'
    % (BASE_URL, public_path(f), _today, "1.0" if f == "index.html" else "0.8")
    for f, _ in NAV
)
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + _urls + '\n</urlset>\n', encoding="utf-8")
print("wrote sitemap.xml")

(OUT / "robots.txt").write_text(
    "User-agent: *\nAllow: /\n\nSitemap: " + BASE_URL + "/sitemap.xml\n", encoding="utf-8")
print("wrote robots.txt")

_nf = SHELL.format(
    desc="That page doesn't exist.",
    title="Page not found \u2014 Solomon B. Pobee",
    key="notfound",
    canonical=BASE_URL + "/404.html",
    ogtitle="Page not found \u2014 Solomon B. Pobee",
    ogtype="website",
    base=BASE_URL,
    nav=nav_links("404.html"),
    socials=socials_html,
    body=NOT_FOUND_BODY,
    pager="",
    jsonld="",
)
(OUT / "404.html").write_text(clean_links(_nf), encoding="utf-8")
print("wrote 404.html")
