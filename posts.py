#!/usr/bin/env python3
"""What is on the blog: the categories, and the posts themselves.

This is the file to open to write something. Everything that arranges
these - the board, the list, the filters, the tiles - is in notes.py,
and you should not need to look at it.
"""

# ─── HOW TO ADD A POST ─────────────────────────────────────────────────
#
# Newest first. Add an entry at the top of POSTS:
#
#     {
#         "date": "2026-10-04",          # ISO; shown in the reader's format
#         "title": "What I learned watching coaches ignore dashboards",
#         "image": {
#             "src": "assets/blog/whiteboard.jpg",
#             "alt": "A whiteboard covered in a session plan",
#             "caption": "Optional line under the picture.",
#         },
#         "body": """
#           <p>First paragraph.</p>
#           <p>Second paragraph. Links look like
#              <a class="text-link" href="https://example.org/">this</a>.</p>
# """,
#     },
#
# The body is HTML so a post can hold a list or a quote. Keep it to the
# tags already styled on the site: p, a.text-link, strong, em, ul, li,
# blockquote. Then run `python build.py` and `python check.py`.
#======== Test Posts =========


#==========================

# ─── HOW TO ADD A CATEGORY ─────────────────────────────────────────────
#
# The key on the left is what a post's "category" must say. The right side
# is either just the name readers see:
#
#     "campus": "Campus Life",
#
# or that name plus a line for its tile at the foot of the blog:
#
#     "campus": {"label": "Campus Life",
#                "blurb": "Graduate school at BYU: the work and the pace."},
#
# Both forms work, so adding one in a hurry never breaks the build. A
# category with no blurb still gets a tile; the tile just has nothing to
# say under its name.
#
# Colour is not set here. Each category takes the next hue in the order
# this dict declares them, which means a category keeps its colour when
# you add another below it. There are six hues; the seventh category and
# everything after it gets a pair of them in a diagonal stripe, which is
# worth 21 categories before anything repeats. See _cat_slots().
BLOG_CATEGORIES = {
    "lifestyle": {
        "label": "Lifestyle",
        "blurb": "The ordinary hours outside the lab — what I notice, "
                 "and what I decide to keep.",
    },
    "campus": {
        "label": "Campus Life",
        "blurb": "Graduate school at BYU: the work, the people, and the "
                 "pace of the place.",
    },
    "Pod": {
        "label": "Inside The Pod",
        "blurb": "Notes from the research pod — what we are building, and "
                 "why it is built that way.",
    },
    "The Movies": {
        "label": "The Movies",
        "blurb": "Films and shows that shaped how I see things, watched "
                 "again with older eyes.",
    },
}

POSTS = [
        {
        "date": "2026-09-24",
        "category": "The Movies",
        "title": "Going back in time to the movies",
        "summary": "I could sit back and watch the movies I loved as a young man, but I wanted to see them in the way they were meant to be seen.",
        "body": """
          <p> Homeland, the 100, breaking bad, and a few other shows that defined my youth. these are the shows that shaped my perspective on life and the world around me. </p>
          <p>Second paragraph, with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
        {
        "date": "2026-09-24",
        "category": "lifestyle",
        "title": "The unexpected long trip home",
        "summary": "A long trip home, and the multiple stops along the way.",
        "body": """
          <p>First paragraph.</p>
          <p>Second paragraph, with a
             <a class="text-link" href="https://example.org/">link</a>.</p>
""",
    },
    {
        "date": "2026-09-24",
        "category": "Pod",
        "title": "The Smart Intruder: Invasion of the Open Territory",
        "summary": "Smart intruders has moved into the open territory. What happens next?",
        "body": """
          <p>Just a Joke?

What is the true definition of a "joke"? Is there a boundary that decides what kind of joke is acceptable between people? Maybe there is, and maybe that boundary says something about the relationship between them. So what do you call someone who is told to stop acting strangely "in the name of joking," and then goes ahead and does it anyway?

..</p>
<p>A new member recently joined our pod: a know-it-all, self-proclaimed nerd I'll call Snake. He assumes everyone thinks and acts the way he does. He's odd and nosy, and he keeps trying to force his way in. It isn't working.</p>

<p> On a dry, sunny day with a deadline hanging over everyone, one of the pod members, Leo, stepped away from his desk. Snake quickly slipped into Leo's space, took his radio player, put in a cassette playing "The Witch Is Dead" as a joke, and then went back to his own desk to hide and wait for Leo to come back. </p>

<p>When Leo returned, he could tell something was off. Snake was delighted to watch him look confused. He said nothing and waited. A few days later, Leo told the others what had happened. He knew Snake was listening, so he played it smart and said the incident had been reported to the authorities. When Snake heard that, he got scared, went pale, and started begging and confessing. It was just a "joke," he said.</p>

<p>How is that a joke? How can someone who presents himself as so knowledgeable invade another person's privacy and then call it a joke? Could he ever be trusted? </p>

<p>I made a few small choices you might want to change. I added a title, swapped "territory" for "desk" and "space" so it reads more naturally, and wrote "said the incident had been reported" because the original didn't make clear who "they" were. If you'd like it to sound more formal, more personal, or shorter, I can adjust it</p>
""",
    },
    {
        "date": "2026-09-21",
        "category": "lifestyle",
        "title": "Why I am keeping these notes",
        "body": """
          <p>Research usually reaches people after the questions have been narrowed, the methods have been settled, and the writing has been polished. A great deal of useful thinking happens before that point. I want this page to hold some of it.</p>
          <p>My work sits at the intersection of human&ndash;computer interaction, youth sport, and coaching. These settings make a people-first approach essential. Athletes and coaches do not simply need more data or another dashboard; a tool has to earn its place by reducing friction, clarifying a decision, or making limited time more useful.</p>
          <p>I will use these notes for ideas from building and studying systems, connections from things I am reading, and lessons that may not belong in a formal paper. The ideas will sometimes be provisional. The goal is to make the process more visible and give the thinking room to develop.</p>
""",
    },
    {
        "date": "2026-09-15",
        "category": "campus",
        "title": "Useful technology should reduce the work",
        "body": """
          <p>A system can present accurate information and still fail the people it was designed to help. This often happens when getting the insight requires more recording, organizing, and reviewing than a coach or athlete can reasonably sustain.</p>
          <p>Before adding a feature, I find it useful to ask a smaller set of questions: What decision will this support? What information already exists? Who has to do extra work? What happens when the data is incomplete?</p>
          <p>The most useful system may not be the one that collects the most data. It may be the one that asks for the minimum useful input, communicates uncertainty clearly, and fits into a routine that is already under pressure. Usability is not only whether someone can operate a tool; it is also whether using it remains worthwhile.</p>
""",
    },
    {
        "date": "2026-09-23",
        "category": "lifestyle",
        "fasten": "tape",
        "title": "A poem I keep coming back to",
        "summary": "Norma Cornett Marek\u2019s \u201cTomorrow Never Comes,\u201d and the habit it left me with.",
        "body": """
          <p>I read this years ago and it has not left me since. It is called <em>Tomorrow Never Comes</em>, by Norma Cornett Marek, and the whole of it turns on one repeated phrase:</p>
          <blockquote>If I knew this would be the last time&hellip;</blockquote>
          <p>The poem runs that sentence through ordinary things. Watching someone sleep. Hearing their voice in prayer. A door closing behind them on an unremarkable morning. Each time it asks what you would have done differently had you known, and each time the answer is almost nothing: a minute longer, one more word, the thing said out loud instead of assumed to be understood.</p>
          <p>That is what makes it land. It does not ask for grand gestures, and it does not really warn you about death. It warns you about deferral &mdash; about the quiet confidence that there will be another chance to say it.</p>
          <p>The ending turns from regret to instruction. It stops describing what you would have done and starts telling you what to do now &mdash; hold the people you love, and spend your words on them while there are words to spend. What struck me is how ordinary the words it asks for are. Not declarations. Four short things most of us can manage and routinely do not:</p>
          <blockquote>&ldquo;I&rsquo;m sorry.&rdquo; &ldquo;Please.&rdquo; &ldquo;Forgive me.&rdquo; &ldquo;Thank you.&rdquo;</blockquote>
          <p>It closes on the line I think about most:</p>
          <blockquote>The past doesn&rsquo;t come back, and the future might not come.</blockquote>
          <p>What it changed in me is unremarkable from the outside. I call home more than I used to. I have mostly stopped saving things to say. <a class="text-link" href="http://www.heartwhispers.net/poetry/00040.html" target="_blank" rel="noopener">The full poem is at Heart Whispers</a>, where it is published with the author&rsquo;s name on it &mdash; worth reading whole, and worth reading there rather than here.</p>
""",
    },
]
