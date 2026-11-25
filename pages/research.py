#!/usr/bin/env python3
"""The research page.

Prose and headings only: no marks, no generated content. Editing this
file is the whole job.

ACTIVE RESEARCH is one <article class="project-entry"> per project. The
shape is fixed: an <h3> title, one paragraph of about 70-95 words, then
one <p class="meta"> row per attribute - the row's first <span> is the
label in the left rail and the <em> after it is the value. Add a second
project by copying the whole <article>.

One thing in the first entry is still a placeholder: the title
"Adolescent athletes and their data" was written here, not by you -
rename it to whatever the study is actually called.

The hiking entry has no METHODS row. Add one the same way when you know
what to put in it:
    <p class="meta"><span>Methods</span> <em>Interview study</em></p>
"""
BODY = {}

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
          <p>I&rsquo;m a PhD student in Computer Science at Brigham Young University, advised by <a class="text-link" href="https://cs.byu.edu/directory/michael-jones" target="_blank" rel="noopener">Michael D. Jones</a> in the Advanced Interactive Lab. My work focuses on adolescent sub-elite youth sports and the role technology can play in <strong>performance</strong>, <strong>club coordination</strong>, and <strong>injury prevention</strong>.</p>
          <p>The through-line is designing for contexts where the usual assumptions don&rsquo;t hold: no expert operator, no dedicated staff, no budget for the thing that would obviously solve the problem. I&rsquo;m particularly interested in systems that fit into existing coaching and athlete workflows rather than adding complexity to them.</p>
        </div>
      </section>

      <section class="pad" style="border-top:1px solid var(--border);">
        <div class="section-heading"><p class="kicker">ACTIVE RESEARCH</p></div>
        <article class="project-entry">
          <h3>Adolescent athletes and their data</h3>
          <p>This study explores adolescent athletes&rsquo; experiences, perceptions, and concerns regarding the collection, use, sharing, and management of their personal and performance data in U.S.&nbsp;organized youth sports. Where earlier work looked at how sub-elite coaches read and act on that data, this one puts the athletes themselves at the centre: what they know is being gathered, who they believe sees it, and what they would want to change about how it is handled.</p>
          <p class="meta"><span>Methods</span> <em>Interview study</em></p>
          <p class="meta"><span>Related work</span> <em><a class="text-link" href="publications.html">&ldquo;They don&rsquo;t tell the full story&rdquo;: Data, Perception, and Communication among Sub-Elite Youth Coaches in the United States</a> &middot; SportsHCI 2026</em></p>
        </article>

        <article class="project-entry">
          <h3>Technology use during a day hike</h3>
          <p>This study explores how people use technology during day hikes &mdash; phones, watches, cameras, navigation and tracking apps &mdash; and how that use mediates engagement with nature.</p>
          <p class="meta"><span>Related work</span> <em><a class="text-link" href="publications.html">Toward a Framework for the Design of Interactive Technology for Nature Recreation</a> &middot; IJHCI 2025</em></p>
        </article>
      </section>

      <section class="pad" style="border-top:1px solid var(--border);">
        <div class="section-heading"><p class="kicker">RESEARCH AREAS</p></div>
        <p class="areas">HCI &middot; Sports Technology &middot; Adolescent Athletes &middot; Youth Sports &middot; Injury Prevention &middot; Nature and Technology &middot; Privacy and data stewardship</p>
      </section>

      <section class="research-question pad">
        <p class="kicker">GUIDING QUESTION</p>
        <p>How can we build technology that gives athletes and coaches of Sub-elite youth sports useful insight without making their work harder?</p>
      </section>

      <section class="pad" style="padding-top:0;">
        <p class="note">Published work across these areas is on the <a href="publications.html">Publications</a> page; systems in development are under <a href="projects.html">Projects</a>.</p>
      </section>"""
