#!/usr/bin/env python3
"""The CV page, and the buttons that offer the PDF.

The web CV is the HTML below. The downloadable PDF is whatever sits in
assets/cv/ - cv_actions() finds it and builds the two buttons at
<!--CVACTIONS-->. The two do not update each other, so a change to your
history means editing both.
"""
import html as _html
from urllib.parse import quote as _quote

from core import OUT

BODY = {}

# ── the CV download ──────────────────────────────────────────────────────
# Drop a PDF into assets/cv/ and both buttons on the CV page point at it:
# Download saves it, Print sends that file to the printer rather than the web
# page. Leave the folder empty and the Download button is left out entirely
# rather than linking to a file that is not there — a dead reference fails
# the deploy's asset check and stops the whole site publishing — and Print
# falls back to printing the page, so the button is never dead. The filename
# is yours to choose; if there is more than one PDF the last by name wins, so
# dated names like cv-2026-09.pdf sort the newest to the end.
CV_DIR = OUT / "assets" / "cv"
CV_MARK = "<!--CVACTIONS-->"


def cv_actions():
    """The Download and Print buttons under the CV heading.

    Download points at whatever PDF is in assets/cv/; with more than one,
    the last by name wins, so a dated name like cv-2026-10.pdf sorts the
    newest to the end. With no PDF the Download button is left out
    entirely rather than pointing at a file that is not there - a dead
    reference fails the deploy's asset check and stops the whole site
    publishing. Print falls back to printing the page, so it is never
    dead.
    """
    pdfs = sorted(p.name for p in CV_DIR.glob("*.pdf")) if CV_DIR.is_dir() else []
    out = []
    if pdfs:
        # Percent-encode the filename. Real CV files are called things like
        # "Solo-Resume-Aug 2026.pdf", and a raw space in an href is not a
        # valid URL — it broke the deploy's link check once already.
        href = "assets/cv/%s" % _quote(pdfs[-1])
        out.append('<a class="button button-primary" href="%s" download>'
                   'Download PDF <span aria-hidden="true">&darr;</span></a>' % href)
        out.append('<button type="button" class="button button-secondary" '
                   'data-print="%s">Print CV</button>' % href)
    else:
        out.append('<button type="button" class="button button-secondary" '
                   'data-print="">Print this page</button>')
    return "\n          " + "\n          ".join(out)


BODY["cv"] = """      <section class="pad">
        <p class="eyebrow enter-1">CURRICULUM <span>&times;</span> VITAE</p>
        <h1 class="enter-1">Solomon B. Pobee</h1>
        <p class="lead enter-2">Computer Science PhD student &middot; Human&ndash;Computer Interaction &middot; Brigham Young University</p>
        <div class="cv-actions enter-2"><!--CVACTIONS-->
        </div>
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
            <p>Human&ndash;Computer Interaction &middot; Sports Technology &middot; Youth Athletics &middot; Outdoor Recreation &middot; Injury Prevention</p>
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
            <p><a class="text-link" href="mailto:jnrpobee@byu.edu">jnrpobee@byu.edu</a> &middot; <a class="text-link" href="mailto:jnrpobee@outlook.fr">jnrpobee@outlook.fr</a></p>
          </div>
        </div>

        <p class="sub">Education</p>
        <div class="cv-row">
          <p class="kicker">2024 &mdash; PRESENT</p>
          <div>
            <h3>Brigham Young University</h3>
            <p><strong>PhD, Computer Science</strong> &mdash; emphasis in Human&ndash;Computer Interaction. Provo, Utah.<br>
            Academic Scholarship. Member of the Graduate Studies Association. Coursework in human&ndash;computer interaction, privacy, outdoor and recreation HCI, algorithm design and analysis, software engineering, and agentic AI systems.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2012 &mdash; 2020</p>
          <div>
            <h3>Brigham Young University &ndash; Idaho</h3>
            <p><strong>BSc, Computer Science</strong> &mdash; emphasis in Web Design and Development, minor in Information Technology. Rexburg, Idaho.<br>
            Coursework in system security, cyber security, software applications, and web engineering. Member of the BYU Management Society.</p>
          </div>
        </div>

        <p class="sub">Experience</p>
        <div class="cv-row">
          <p class="kicker">2024 &mdash; PRESENT</p>
          <div>
            <h3>Research Assistant &middot; Brigham Young University</h3>
            <p>Provo, Utah. Lead a team of student researchers in the lab, supporting them in carrying out and presenting research. Ran a study on how technology affordances shape engagement with nature during a day hike, and what that implies for designing technology that supports wellbeing rather than competing with it. Lead a toe-sensor project prototyping hands-free interaction that keeps attention on the activity rather than the device.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2021 &mdash; 2023</p>
          <div>
            <h3>Reconciliation Officer &middot; Soci&eacute;t&eacute; G&eacute;n&eacute;rale, Head Office</h3>
            <p>Accra, Ghana. Reconciled daily transactions across internal ledgers, the central bank and correspondent banks. Investigated breaks in suspense and clearing accounts with branch teams, cutting outstanding items by 30% in six months, and worked with treasury, operations and IT to shorten exception-handling turnaround by 20%. Monitored unusual entries and escalated high-risk items for fraud prevention and regulatory compliance, and introduced process controls and automation that removed hours of manual checking each week.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">2018 &mdash; 2019</p>
          <div>
            <h3>Instructor &middot; Missionary Training Center</h3>
            <p>Accra, Ghana. Trained missionaries in teaching skills and in their assigned mission language, running role plays, practice lessons and feedback sessions. Used immersion and conversation practice to accelerate language learning, and adjusted instruction to different learning speeds. Coached individuals one to one, and maintained lesson plans, schedules and progress reporting.</p>
          </div>
        </div>

        <p class="sub">Service</p>
        <div class="cv-row">
          <p class="kicker">ONGOING</p>
          <div>
            <h3>Peer review</h3>
            <p>Reviewer for five papers, including submissions to the ACM Conference on Human&ndash;Computer Interaction and Sports.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">OCT 2026</p>
          <div>
            <h3>Student Volunteer &middot; CSCW 2026</h3>
            <p>ACM Conference on Computer-Supported Cooperative Work and Social Computing. Salt Lake City, Utah.</p>
          </div>
        </div>

        <p class="sub">Awards</p>
        <div class="cv-row">
          <p class="kicker">2025</p>
          <div>
            <h3>BYU Professional Presentation Award</h3>
            <p>Brigham Young University.</p>
          </div>
        </div>

        <p class="sub">Invited &amp; upcoming</p>
        <div class="cv-row">
          <p class="kicker">JUL 2025</p>
          <div>
            <h3>NatureHCI: Towards Designing Computer-Enriched Nature Experiences</h3>
            <p>Schloss Dagstuhl &ndash; Leibniz-Zentrum f&uuml;r Informatik, Germany.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">MAY 2026</p>
          <div>
            <h3>American College of Sports Medicine Annual Meeting</h3>
            <p>Salt Lake City, Utah.</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">OCT 2026</p>
          <div>
            <h3>CSCW 2026</h3>
            <p>ACM Conference on Computer-Supported Cooperative Work and Social Computing. Salt Lake City, Utah.</p>
          </div>
        </div>

        <p class="sub">Certifications</p>
        <div class="cv-row">
          <p class="kicker">RESEARCH</p>
          <div>
            <h3>Research ethics</h3>
            <p>Responsible Conduct of Research &mdash; Faculty and Student Researchers.<br>
            Social and Behavioral Research Investigators and Mentors.</p>
          </div>
        </div>

        <p class="sub">Skills &amp; languages</p>
        <div class="cv-row">
          <p class="kicker">TECHNICAL</p>
          <div>
            <h3>Tools and methods</h3>
            <p>Python, C++, MATLAB, PHP &middot; Java, MySQL<br>
            SciPy, pandas, Seaborn<br>
            Quantitative and qualitative research methods</p>
          </div>
        </div>
        <div class="cv-row">
          <p class="kicker">LANGUAGES</p>
          <div>
            <h3>English and French</h3>
            <p>English, native. French, professional working proficiency.</p>
          </div>
        </div>
      </section>"""
