#!/usr/bin/env python3
"""Run every check the deploy runs, before pushing.

The deploy workflow refuses to publish a site whose links are malformed or
whose files do not exist. Finding that out from a red cross on GitHub is slow
and, worse, the previous version stays live while you think you shipped. This
script runs the same checks locally, so a broken build is caught in seconds.

    python check.py          # rebuild the pages, then check the working tree
    python check.py --site _site   # check an assembled site directory (CI)
    python check.py --no-build     # check what is on disk, do not regenerate

CI calls this too, so there is one implementation of "is this publishable"
rather than a copy in the workflow that can drift from the copy here.

Exit code is 0 when everything passes and 1 when anything fails.
"""
import argparse
import pathlib
import re
import subprocess
import sys
from urllib.parse import unquote, urlparse

HERE = pathlib.Path(__file__).parent

# Files the site needs that are not reached by a link from a page. Missing
# these does not break a link check but does break the site.
REQUIRED = ["index.html", "styles.css", "script.js"]

REF = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']')
EXTERNAL = ("http://", "https://", "mailto:", "tel:", "data:", "#", "//")


def say(ok, label, detail=""):
    print("  %s %s%s" % ("PASS" if ok else "FAIL", label, (" — " + detail) if detail else ""))
    return ok


def run_build():
    """Regenerate the pages, and fail loudly if build.py itself errors."""
    r = subprocess.run([sys.executable, "build.py"], cwd=str(HERE),
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        return say(False, "build.py runs", "it exited %d" % r.returncode)
    return say(True, "build.py runs")


def check_links(site):
    """Delegate to check_links.py so there is one link grammar, not two."""
    r = subprocess.run([sys.executable, str(HERE / "check_links.py"), str(site)],
                       capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        print(out)
        return say(False, "every link is well-formed")
    return say(True, "every link is well-formed", out.splitlines()[-1].strip() if out else "")


def check_assets(site):
    """Every local href/src resolves to a file that exists.

    Paths are matched the way the host serves them: "" is the homepage and an
    extensionless path is its .html file. They are also percent-decoded, since
    a filename with a space in it is encoded in the href but not on disk.
    """
    site = pathlib.Path(site)
    missing = []
    for page in sorted(site.glob("*.html")):
        for ref in REF.findall(page.read_text(encoding="utf-8")):
            if ref.startswith(EXTERNAL):
                continue
            path = unquote(urlparse(ref).path).lstrip("/")
            if not path:
                path = "index.html"
            elif not pathlib.PurePosixPath(path).suffix:
                path += ".html"
            if not (site / path).exists():
                missing.append("%s: %s" % (page.name, ref))
    if missing:
        for m in missing:
            print("      " + m)
        return say(False, "every local file referenced exists",
                   "%d missing" % len(missing))
    return say(True, "every local file referenced exists")


def check_reproducible():
    """Building twice produces byte-identical files.

    A build that varies run to run — a date stamped at build time, a dict
    iterated in a different order — means the pages you commit are not the
    pages CI publishes, and every push looks like the whole site changed.
    Two builds a second apart will not catch a value that changes daily, so
    this also fails on any generated file that contains today's date, which
    is what a build-time stamp looks like.
    """
    import datetime
    import hashlib

    def digest():
        out = {}
        for f in sorted(HERE.glob("*.html")) + [HERE / "sitemap.xml", HERE / "robots.txt"]:
            if f.exists():
                out[f.name] = hashlib.md5(f.read_bytes()).hexdigest()
        return out

    first = digest()
    r = subprocess.run([sys.executable, "build.py"], cwd=str(HERE),
                       capture_output=True, text=True)
    if r.returncode != 0:
        return say(False, "building twice gives the same bytes", "the second build failed")
    second = digest()
    moved = sorted(k for k in first if first[k] != second[k])
    if moved:
        return say(False, "building twice gives the same bytes", ", ".join(moved))

    # Today's date in a generated page is what a build-time stamp looks
    # like, and two builds a second apart will never catch one. But a post
    # written today legitimately carries today's date, so the date only
    # counts as a stamp when it appears nowhere in the sources - if it is
    # in a source file, somebody typed it rather than the clock.
    #
    # Every .py in the folder and in pages/, not build.py alone: the posts
    # moved out to posts.py when the generator was split up, and a check
    # that still read only build.py called a note written today a build
    # stamp and stopped the push.
    today = datetime.date.today().isoformat()
    sources = ""
    srcs = sorted(HERE.glob("*.py")) + sorted((HERE / "pages").glob("*.py"))
    for src in srcs + [HERE / "leetcode.json"]:
        if src.exists():
            sources += src.read_text(encoding="utf-8")
    if today not in sources:
        stamped = sorted(f.name for f in HERE.glob("*.html")
                         if today in f.read_text(encoding="utf-8"))
        sm = HERE / "sitemap.xml"
        if sm.exists() and today in sm.read_text(encoding="utf-8"):
            stamped.append("sitemap.xml")
        if stamped:
            return say(False, "no generated file stamps the build date",
                       ", ".join(stamped))
    return say(True, "building twice gives the same bytes")


def check_placeholders(site):
    """No template placeholder or build marker survived into a page.

    A `{{desc}}` in the shell renders as a literal "{desc}" rather than the
    description, and an unreplaced <!--CITE:c1--> leaves a citation missing.
    Neither breaks a link or a file reference, so nothing else here notices;
    the og:description tag shipped as the literal text "{desc}" for weeks.
    """
    site = pathlib.Path(site)
    # {desc}, {title} and friends — a brace around a bare identifier. CSS and
    # JS braces are always followed by whitespace, a newline or another rule,
    # so a word tightly wrapped in braces is a leftover format field.
    field = re.compile(r"\{[a-z_][a-z0-9_]*\}")
    marker = re.compile(
        r"<!--\s*(CITE:[^>]*|LEETCODE|CVACTIONS|PUBGROUPS|"
        r"BLOGPOSTS|CATCOLOURS|CATTILES|NOTECARDS|NOTECOUNT|NOTEDATA|NOTESTALLY|NOTESEND|"
        r"LIFESTYLEPOSTS|CAMPUSPOSTS)\s*-->"
    )
    found = []
    for page in sorted(site.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for m in set(field.findall(text)) | set(m.group(0) for m in marker.finditer(text)):
            found.append("%s: %s" % (page.name, m))
    if found:
        for f in sorted(found):
            print("      " + f)
        return say(False, "no placeholder survived into a page",
                   "%d left" % len(found))
    return say(True, "no placeholder survived into a page")


def check_line_endings(site):
    """Generated files use LF.

    Python's text mode writes CRLF on Windows, so the same build.py produced
    different bytes there than in CI, and git reported every line of every
    page as changed. build.py writes LF explicitly now; this catches a
    regression.
    """
    site = pathlib.Path(site)
    bad = []
    for f in sorted(list(site.glob("*.html")) + [site / "sitemap.xml", site / "robots.txt"]):
        if f.exists() and b"\r\n" in f.read_bytes():
            bad.append(f.name)
    if bad:
        return say(False, "generated files use Unix line endings", ", ".join(bad))
    return say(True, "generated files use Unix line endings")


def check_required(site):
    site = pathlib.Path(site)
    gone = [f for f in REQUIRED if not (site / f).exists()]
    if gone:
        return say(False, "the files the site cannot do without are present",
                   ", ".join(gone))
    return say(True, "the files the site cannot do without are present")


def check_js(site):
    """Parse script.js. A syntax error there breaks every page silently —
    nothing in the link or asset checks would notice."""
    js = pathlib.Path(site) / "script.js"
    if not js.exists():
        return say(False, "script.js parses", "it is not there")
    node = subprocess.run(["node", "--version"], capture_output=True, text=True)
    if node.returncode != 0:
        print("  SKIP script.js parses — node is not installed")
        return True
    r = subprocess.run(["node", "--check", str(js)], capture_output=True, text=True)
    if r.returncode != 0:
        print("      " + r.stderr.strip().splitlines()[0])
        return say(False, "script.js parses")
    return say(True, "script.js parses")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--site", default=None,
                    help="an assembled site directory to check instead of the working tree")
    ap.add_argument("--no-build", action="store_true",
                    help="do not regenerate the pages first")
    args = ap.parse_args()

    site = args.site or str(HERE)
    building = args.site is None and not args.no_build

    print("Checking %s" % ("the working tree" if args.site is None else site))
    results = []
    if building:
        results.append(run_build())
        if not results[-1]:
            print("\nFAILED — the pages could not be generated.")
            return 1
    if building:
        results.append(check_reproducible())
    results.append(check_required(site))
    results.append(check_links(site))
    results.append(check_assets(site))
    results.append(check_placeholders(site))
    results.append(check_line_endings(site))
    results.append(check_js(site))

    if all(results):
        print("\nAll checks passed. Safe to push.")
        return 0
    print("\nFAILED — fix the above before pushing, or the deploy will stop "
          "and the old site will stay live.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
