#!/usr/bin/env python3
"""The frame every page is poured into.

The head, the header and nav, the footer and the prev/next pager, plus
the structured data that describes the site to a search engine. Seven
pages share it, so one edit here shows on all of them.

SHELL is a format string. build.py fills these, and leaving one out is
a KeyError rather than a quiet blank:

    blogname   what the blog is called, for the tab and the two doors into it
    title      the browser title
    desc       the search description
    key        the page's content key, used as a hook in styles.css
    canonical  the page's own address, absolute
    base       the site root, for the Open Graph image
    ogtitle    the title a shared link shows
    ogtype     "profile" for the personal pages, "website" for the rest
    robots     a noindex tag, for the unlisted pages
    brand      the header's left-hand mark
    nav        the nav links, with this page marked current
    socials    the footer's profile links
    body       the page itself
    pager      the previous/next links, empty for a page outside the nav
    jsonld     structured data: the person on the home page, the
               scholarly record on the publications page, nothing elsewhere

A literal brace inside this string has to be doubled, or format() will
read it as a placeholder. That is why the CSS and JS inline here look
the way they do.
"""
import html as _html

from core import BASE_URL, BLOG_NAME, NAV, UNLISTED, public_path

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

BLOG_NAV = [
    ("blog.html", BLOG_NAME),
]


def nav_links(active):
    """The header links, with the current page marked.

    aria-current="page" is what says "you are here" to a screen reader;
    the underline in styles.css hangs off the same attribute, so the two
    can never disagree.
    """
    links = BLOG_NAV if active in (h for h, _ in BLOG_NAV) else NAV
    return "\n".join(
        '        <a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", l)
        for h, l in links
    )


def header_brand(active):
    """The mark at the left of the header, and the small status note.

    The note carries the dot that is one of the two ways into the blog -
    the other is the copyright line in the footer, which is what a phone
    gets, since the note is hidden at that width.
    """
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
    """Previous and next, in NAV order, or "" for a page outside it.

    The blog is unlisted, so it sits outside the sequence and gets no
    pager. The padded wrapper is part of what this returns rather than
    part of SHELL: when it lived in the shell, a page with no pager still
    carried an empty .pad and 128px of nothing above its footer.
    """
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
