#!/usr/bin/env python3
"""Validate every href/src in the built pages. Catches malformed values —
unevaluated template fragments, empty hrefs, stray quotes, spaces."""
import pathlib, re, sys
from html.parser import HTMLParser

class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.found = []
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for attr in ('href', 'src'):
            if attr in d:
                self.found.append((tag, attr, d[attr]))

VALID = re.compile(
    r'^(https?://[^\s"\'<>]+'          # absolute
    r'|mailto:[^\s"\'<>]+'             # mail
    r'|#[\w/\-]*'                      # in-page / route
    r'|data:[a-z]+/[a-z.+\-]+;base64,[A-Za-z0-9+/=]+'   # embedded asset
    # The formats a page on this site may legitimately point at. It is a
    # list rather than a wildcard so that a stray word still reads as
    # malformed - but it has to hold every extension actually in use, or
    # a real image fails the deploy. jpeg, webp, avif and gif were all
    # missing until a post used a .jpeg and the build stopped.
    r'|[\w\-./%]+\.(html|css|js|svg|jpe?g|png|gif|webp|avif|ico|xml|txt'
    r'|pdf|woff2?|mp4|webm|webmanifest)(\?[\w=&\-]*)?'
    r'|/(?:[\w\-]+(?:/[\w\-]+)*)?(?:[#?][^\s"\'<>]*)?'  # clean path: / or /research
    r')$'
)

def check(path):
    s = pathlib.Path(path).read_text(encoding='utf-8')
    p = Links(); p.feed(s)
    bad = []
    for tag, attr, val in p.found:
        v = val.strip()
        if not v:
            bad.append((tag, attr, '(empty)')); continue
        if any(t in v for t in ('+ ', ' + ', '{', '}', '%s', 'SCHOLAR_URL', 'undefined')):
            bad.append((tag, attr, v)); continue
        if not VALID.match(v):
            bad.append((tag, attr, v))
    return len(p.found), bad

# With arguments, check those files or directories. With none, check the
# builds and single-file previews that live beside this script.
if len(sys.argv) > 1:
    targets = []
    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        targets += sorted(p.glob('*.html')) if p.is_dir() else [p]
else:
    targets = []
    for d in ('dark', 'topnav'):
        targets += sorted(pathlib.Path(d).glob('*.html'))
    targets += [pathlib.Path(f) for f in
                ('pobee-dark.html', 'pobee-topnav.html', 'solomon-pobee.html')]

total, failures = 0, 0
for t in targets:
    n, bad = check(t)
    total += n
    if bad:
        failures += len(bad)
        print('%s — %d malformed' % (t, len(bad)))
        for tag, attr, v in bad[:6]:
            print('    <%s %s="%s">' % (tag, attr, v[:90]))
print('\n%d links checked across %d files — %s'
      % (total, len(targets), 'all well-formed' if not failures else '%d MALFORMED' % failures))
sys.exit(1 if failures else 0)
