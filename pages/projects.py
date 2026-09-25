#!/usr/bin/env python3
"""The projects page.

Two kinds of card. A project card is written by hand and carries one of
the drawings from art.py. A repo card carries data-repo="owner/name",
and script.js fills in the live GitHub figures when the page loads -
so keep a written description in the HTML, because that request fails
whenever GitHub is slow, rate-limited or blocked.

<!--LEETCODE--> is where leetcode.py's panel goes. Leave it alone
unless you are moving the panel; a mark that survives into a finished
page fails check.py.
"""
from art import ART_COACH, ART_PERFORMANCE

BODY = {}

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
