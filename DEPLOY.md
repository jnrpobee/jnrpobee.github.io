# Publishing solomonbpobee.com on Cloudflare Pages

This folder is a plain static site. There is no build step, no framework and no
dependencies — the HTML that is here is the HTML that gets served. Any static
host will serve it; these instructions are for Cloudflare Pages.

Everything below except the Cloudflare account steps has already been done for
you. What remains is roughly twenty minutes, most of it waiting for DNS.

---

## Before you start: three gaps in the content

The site is technically ready. The writing is not quite, and these will be
visible to anyone who visits:

- **CV page** — Education and Experience are honest "To add" blocks. Anyone
  reading will see the site is unfinished there.
- **About page** — the "Beyond the lab" section says "Your words go here".
- **LinkedIn** — the site links to `linkedin.com/in/jnrpobee`. That is my
  inference from your username elsewhere; the old site had an invalid URL.
  Open it and confirm it is really yours before you launch.

None of these block deployment. You may prefer to fill them first, or to
publish now and edit after — a redeploy takes about a minute.

---

## What to upload

The deploy bundle is `solomonbpobee-cloudflare.zip`. It contains only the files
that should be public:

```
index.html  research.html  projects.html  publications.html
about.html  cv.html  404.html
styles.css  script.js
assets/          icons, portrait, Open Graph image, web manifest
sitemap.xml  robots.txt
_headers         caching and security headers
_redirects       sends the bare domain to www
```

The build scripts (`build.py`, `check_links.py`) and the local-preview helpers
are deliberately **not** in the bundle. They stay here in your working folder.

---

## Step 1 — Find out where your DNS lives

You own the domain, but the records currently point at Google Sites, and the
steps below depend on who controls them. I could not look this up from here, so
check it yourself:

Go to <https://who.is/whois/solomonbpobee.com> and read the **Registrar** line
and the **Name Servers** list. Registrars bought alongside Google Sites usually
show Squarespace (Google sold that business to them); you may also see
Namecheap, GoDaddy, or Cloudflare if you are already there.

Write down what it says. You will need to sign in to that registrar in Step 3.

---

## Step 2 — Put the site on Cloudflare Pages

1. Create a free account at <https://dash.cloudflare.com/sign-up> if you do not
   have one, and verify the email.
2. In the left sidebar choose **Workers & Pages**, then **Create** →
   **Pages** → **Upload assets**.
3. Name the project `solomonbpobee`. This name becomes a free
   `solomonbpobee.pages.dev` address, which stays available forever as a
   fallback and is handy for checking your work before the real domain points
   at it.
4. Unzip `solomonbpobee-cloudflare.zip` and drag the **contents** onto the
   upload area — the individual files and the `assets` folder, not a folder
   containing them. If you drop a wrapping folder, the site will end up at
   `/solomon-portfolio/index.html` and the root will 404.
5. Click **Deploy site**.

It goes live at `solomonbpobee.pages.dev` within a minute or so. **Open it and
click through every page before going further.** If something looks wrong, it is
much easier to fix now than after the domain is switched.

---

## Step 3 — Point the domain at it

Cloudflare Pages handles the apex domain (`solomonbpobee.com`, with no `www`)
cleanly only when Cloudflare is also running your DNS. That means moving the
domain's nameservers. The domain stays registered where it is — you are only
changing who answers DNS queries for it.

1. In the Cloudflare dashboard, go to **Websites** → **Add a site**, enter
   `solomonbpobee.com`, and choose the **Free** plan.
2. Cloudflare scans your existing records and shows you what it found.
   **Read this list carefully.** If you have email on this domain — anything at
   `@solomonbpobee.com` — the MX and TXT records must all be there. If any are
   missing, add them by hand before continuing, or your mail will stop
   arriving. This is the one step in this process that can break something you
   are already relying on.
3. Cloudflare gives you two nameservers, something like `amy.ns.cloudflare.com`
   and `rick.ns.cloudflare.com`. Sign in to the registrar you identified in
   Step 1, find the nameserver setting, and replace the existing ones with
   Cloudflare's.
4. Wait. Nameserver changes usually take a few minutes to a couple of hours,
   occasionally up to 24. Cloudflare emails you when the domain is active.

Once the domain shows **Active** in Cloudflare:

5. Go back to **Workers & Pages** → your `solomonbpobee` project → **Custom
   domains** → **Set up a custom domain**.
6. Add `www.solomonbpobee.com`. Cloudflare creates the DNS record for you.
7. Add `solomonbpobee.com` as well, so the bare domain resolves too.

HTTPS certificates are issued automatically and usually take a few minutes.
Until they are ready you may see a certificate warning; that is expected and
resolves itself.

---

## Step 4 — Retire the Google Sites version

Once the new site is serving, open Google Sites, find the old site's settings,
and remove the custom domain mapping for `solomonbpobee.com`. Leaving it mapped
does not break anything now that DNS has moved, but it will confuse you in a
year when you have forgotten this afternoon.

Do not delete the old Google site outright until you are sure you have not lost
anything from it.

---

## Step 5 — Check the launch

With the domain live, confirm each of these:

- `https://www.solomonbpobee.com` loads the new site.
- `https://solomonbpobee.com` redirects to the `www` version.
- All six pages load, and the navigation works on a phone.
- A made-up URL such as `/nonsense` shows the styled 404 page.
- The favicon appears in the browser tab.
- Paste the URL into a Slack or WhatsApp message and confirm the preview card
  shows your portrait and name — that is the Open Graph image working.

Then tell Google the site changed: submit `https://www.solomonbpobee.com/sitemap.xml`
at <https://search.google.com/search-console>. Without this, search results will
keep pointing at the Google Sites version for a while.

---

## Redeploying after an edit

The site is generated by `build.py` in this folder. After editing it:

```bash
python3 build.py          # regenerate the HTML pages
python3 check_links.py .  # confirm no malformed links
```

Then in Cloudflare: **Workers & Pages** → `solomonbpobee` → **Create
deployment** → drag the files again. The previous deployment stays in the
project's history, so if a change goes wrong you can roll back with one click.

If you would rather not drag files each time, connect the folder to a GitHub
repo and point the Pages project at it under **Settings** → **Builds &
deployments**. Then a `git push` publishes. Leave the build command empty —
there is nothing to build. Worth doing if you expect to edit often; not worth
it for a site you touch twice a year.

---

## The two config files, in case you wonder later

**`_headers`** sets cache lifetimes and a few security headers. Images and
icons are cached for a year, CSS and JS for an hour, HTML not at all — so a
redeploy is visible immediately rather than after a stale cache expires.

**`_redirects`** sends `solomonbpobee.com` to `www.solomonbpobee.com`, matching
the canonical URLs in the pages' `<head>`. If it does not take effect, do it in
the dashboard instead: **Rules** → **Redirect Rules** → create a rule matching
hostname `solomonbpobee.com` and redirecting to
`https://www.solomonbpobee.com/${http.request.uri.path}` with status 301.

---

## If you get stuck

The likeliest failure is DNS, and the symptom is the domain showing the old
Google site, or nothing at all. Check <https://dnschecker.org> for
`www.solomonbpobee.com` — it shows what DNS servers around the world currently
answer. If they still show Google's addresses, the nameserver change has not
propagated yet and the answer is to wait rather than to change anything.
