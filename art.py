#!/usr/bin/env python3
"""Two drawings, shared by the home page and the projects page.

Inline SVG rather than image files: they are a handful of shapes, they
have to follow the theme, and a file each would cost two requests to
say less. They are decoration, so they carry role="presentation" and
no title - the card's own heading is what a screen reader reads.

They live here rather than in either page because both pages use them,
and a copy in each is a copy that will drift.
"""
ART_PERFORMANCE = """<svg viewBox="0 0 400 150" role="presentation">
              <g stroke="currentColor" opacity=".10" stroke-width="1">
                <line x1="0" y1="38" x2="400" y2="38"/><line x1="0" y1="75" x2="400" y2="75"/><line x1="0" y1="112" x2="400" y2="112"/>
              </g>
              <polyline points="30,118 90,100 150,106 210,66 270,56 330,32 372,38" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
              <g fill="currentColor">
                <circle cx="90" cy="100" r="4"/><circle cx="210" cy="66" r="4"/><circle cx="330" cy="32" r="5.5"/>
              </g>
            </svg>"""

ART_COACH = """<svg viewBox="0 0 400 150" role="presentation">
              <g stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".85">
                <path d="M104 75 L192 42"/><path d="M104 75 L192 75"/><path d="M104 75 L192 108"/>
                <path d="M192 42 L286 42"/><path d="M192 75 L286 75"/><path d="M192 108 L286 108"/>
              </g>
              <circle cx="104" cy="75" r="10" fill="currentColor"/>
              <g fill="none" stroke="currentColor" stroke-width="1.8">
                <circle cx="192" cy="42" r="6"/><circle cx="192" cy="75" r="6"/><circle cx="192" cy="108" r="6"/>
              </g>
              <g fill="currentColor" opacity=".16">
                <rect x="286" y="34" width="48" height="16" rx="3"/><rect x="286" y="67" width="64" height="16" rx="3"/><rect x="286" y="100" width="40" height="16" rx="3"/>
              </g>
            </svg>"""


# One page now, so there is nothing to navigate between. The header
# still shows the "Exit the blog" brand, which is the only way out.
