#!/usr/bin/env python3
"""The blog's page.

Almost nothing is written here. The masthead and the board's frame are,
and everything else arrives at a mark:

    NOTECARDS / NOTECOUNT / NOTEDATA   the three cards in the hero
    CATCOLOURS                         a hue for each category
    NOTESTALLY                         filters, calendar, per-page picker
    BLOGPOSTS                          the notes themselves
    NOTESEND                           the "show more" button and the closer
    CATTILES                           the category tiles at the foot

All of them are filled by notes.py, from the writing in posts.py. To
publish something you want posts.py, not this file.
"""
BODY = {}

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
