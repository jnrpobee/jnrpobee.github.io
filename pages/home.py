#!/usr/bin/env python3
"""The front page.

Five sections: the hero, the three focus lines, the selected work, the
research strip and the closing call to action.

The two project cards here are deliberate duplicates of cards on the
projects page - the same drawings from art.py, a shorter description.
Change a project's name or link and you have two places to change it;
nothing checks that they agree.
"""
from art import ART_COACH, ART_PERFORMANCE

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
