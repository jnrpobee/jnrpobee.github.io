#!/usr/bin/env python3
"""Refresh leetcode.json from LeetCode's GraphQL endpoint.

LeetCode publishes no REST API, and its GraphQL endpoint sends no CORS headers,
so a browser on this site cannot read it. A build step can: there is no origin
to check server-side. This script runs in CI, writes the numbers into
leetcode.json, and build.py renders them into the page.

Design rule: this must never publish wrong numbers and must never block a
deploy. Every value is validated before it is written, and any failure leaves
leetcode.json exactly as it was and exits 0 with a warning. The site then keeps
showing the last figures known to be good.

Run it by hand the same way CI does:

    python update_leetcode.py            # refresh leetcode.json
    python update_leetcode.py --check    # fetch and report, write nothing
"""
import datetime
import json
import pathlib
import sys
import urllib.error
import urllib.request

HERE = pathlib.Path(__file__).parent
DATA = HERE / "leetcode.json"
ENDPOINT = "https://leetcode.com/graphql/"
TIMEOUT = 20

QUERY = """
query profile($u: String!) {
  allQuestionsCount { difficulty count }
  matchedUser(username: $u) {
    username
    submitStatsGlobal { acSubmissionNum { difficulty count } }
    languageProblemCount { languageName problemsSolved }
  }
}
"""


def warn(msg):
    """A GitHub Actions warning annotation, and a plain line elsewhere."""
    print("::warning title=LeetCode refresh::%s" % msg)


def fetch(username):
    body = json.dumps({"query": QUERY, "variables": {"u": username}}).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            # LeetCode rejects requests without a plausible browser origin.
            "Referer": "https://leetcode.com/u/%s/" % username,
            "User-Agent": "Mozilla/5.0 (compatible; solomonbpobee.com build)",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode())


def parse(payload, username):
    """Turn the GraphQL response into our shape, or raise ValueError."""
    if not isinstance(payload, dict):
        raise ValueError("response was not a JSON object")
    if payload.get("errors"):
        raise ValueError("GraphQL errors: %s" % payload["errors"])

    data = payload.get("data") or {}
    user = data.get("matchedUser")
    if not user:
        raise ValueError("no matchedUser for %r — has the username changed?" % username)

    # How many problems exist at each difficulty, for the "19 of 2,115" context.
    totals = {}
    for row in data.get("allQuestionsCount") or []:
        key = str(row.get("difficulty", "")).lower()
        count = row.get("count")
        if key in ("easy", "medium", "hard") and isinstance(count, int) and count > 0:
            totals[key] = count

    solved = {}
    for row in (user.get("submitStatsGlobal") or {}).get("acSubmissionNum") or []:
        key = str(row.get("difficulty", "")).lower()
        count = row.get("count")
        if key and isinstance(count, int):
            solved[key] = count
    if "all" not in solved:
        raise ValueError("no overall solved count in response")
    if solved["all"] < 0:
        raise ValueError("negative solved count")

    parts = [solved.get(k) for k in ("easy", "medium", "hard")]
    if all(isinstance(p, int) for p in parts) and sum(parts) != solved["all"]:
        raise ValueError(
            "easy+medium+hard (%d) does not equal all (%d)" % (sum(parts), solved["all"])
        )

    langs = [l for l in (user.get("languageProblemCount") or [])
             if isinstance(l.get("problemsSolved"), int)]
    langs.sort(key=lambda l: l["problemsSolved"], reverse=True)
    language = None
    if langs:
        name = str(langs[0].get("languageName") or "").strip()
        if name:
            # "Python3" reads better with a space on the page.
            label = "Python 3" if name.lower() in ("python3", "python 3") else name
            language = {"name": label, "solved": langs[0]["problemsSolved"]}

    return {
        "username": user.get("username") or username,
        "fetched": datetime.date.today().isoformat(),
        "note": ("Refreshed by update_leetcode.py, which the deploy workflow runs. "
                 "Edit by hand only to correct a bad fetch; the next run overwrites it."),
        "solved": {
            "all": solved["all"],
            "easy": solved.get("easy"),
            "medium": solved.get("medium"),
            "hard": solved.get("hard"),
        },
        "totals": totals or None,
        "language": language,
    }


def sane_against(new, old):
    """Refuse a result that looks like a broken response rather than progress."""
    if not old:
        return True
    was = ((old.get("solved") or {}).get("all")) or 0
    now = (new.get("solved") or {}).get("all") or 0
    if was and now == 0:
        raise ValueError("solved count dropped from %d to 0 — treating as a bad response" % was)
    if was and now < was:
        # Solved counts can fall if problems are removed from the site, but a
        # large drop is far more likely to be a partial response.
        if (was - now) > max(5, was * 0.25):
            raise ValueError("solved count fell from %d to %d — too large to trust" % (was, now))
    had = [k for k in ("easy", "medium", "hard") if isinstance((old.get("solved") or {}).get(k), int)]
    if had and not all(isinstance((new.get("solved") or {}).get(k), int) for k in had):
        raise ValueError("the difficulty breakdown went missing from the response")
    return True


def main():
    check_only = "--check" in sys.argv
    old = None
    if DATA.exists():
        try:
            old = json.loads(DATA.read_text(encoding="utf-8"))
        except Exception:
            old = None
    username = (old or {}).get("username") or "pobee"

    try:
        data = parse(fetch(username), username)
        sane_against(data, old)
    except urllib.error.URLError as e:
        warn("could not reach LeetCode (%s); keeping the existing numbers." % e.reason)
        return 0
    except Exception as e:
        warn("%s; keeping the existing numbers." % e)
        return 0

    total = data["solved"]["all"]
    lang = (data.get("language") or {}).get("name") or "unknown"
    print("  LeetCode: %d solved, most-used language %s" % (total, lang))
    s = data["solved"]
    print("    easy %s · medium %s · hard %s"
          % (s.get("easy"), s.get("medium"), s.get("hard")))

    if check_only:
        print("  --check given, leetcode.json not written")
        return 0

    if old and {k: v for k, v in old.items() if k != "fetched"} == \
               {k: v for k, v in data.items() if k != "fetched"}:
        print("  no change")
        return 0

    DATA.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("  wrote %s" % DATA.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
