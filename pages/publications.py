#!/usr/bin/env python3
"""The publications page.

Only the frame is here: the heading, the topic filter chips and the
count. The publications themselves are in pubs.py and arrive at
<!--PUBGROUPS-->.

Two things here have to agree with pubs.py. Every data-topic used by a
publication needs a chip here, or that entry vanishes the moment a
visitor filters. And the number in id="pub-count" is the figure the
page ships with - script.js corrects it after a search, but a stale
number is what a reader sees first.
"""
BODY = {}

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
