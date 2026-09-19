# Publishing solomonbpobee.com with GitHub Pages

## Where you are now

The push worked — 42 objects, `main` created and tracking `origin/main`.

One surprise: `jnrpobee.github.io` was not an empty repository. It already held
your BYU-Idaho coursework (`assignments/`, `term-website/`, `The MONOMYTH.pdf`,
an `index.html` that redirects to `jnrpobee.html`) on a branch called
**`master`**, and GitHub Pages was already serving it at
<https://jnrpobee.github.io>.

Nothing collided and nothing was overwritten. Your site went onto a **new**
branch, `main`, with a history entirely separate from `master` — which is why
Git offered you a pull-request link instead of just updating things. The two
branches coexist.

So the coursework is *already* on its own branch. The steps below rename that
branch to something you will recognise in a year, promote `main` to default, and
publish from it.

**About those 2 moderate vulnerabilities GitHub flagged:** they are on the
default branch, which is currently `master` — so they are in the old
coursework, almost certainly a bundled jQuery or Bootstrap under
`term-website/`. Your new site has no dependencies of any kind. Once `main` is
the default branch, Dependabot rescans and stops reporting them.

---

## Your DNS, looked up 18 September 2026

| | |
|---|---|
| Registrar and DNS | Namecheap (BasicDNS: `dns1`/`dns2.registrar-servers.com`) |
| Domain registered | 31 March 2026, expires 31 March 2028 |
| `www.solomonbpobee.com` | CNAME → `ghs.googlehosted.com` (the Google Sites site) |
| `solomonbpobee.com` (bare) | no A record — the bare domain resolves to nothing today |
| Mail | **live email forwarding** via `eforward1`–`eforward5.registrar-servers.com` |
| Also present | an SPF record and a Google site-verification TXT |

**The one thing to be careful about:** those `eforward` MX records are working
email forwarding for `@solomonbpobee.com`. If you delete them, mail to that
address stops arriving. Nothing here touches them, and Namecheap lists MX
records separately from the host records you *will* edit — but know it before
you start deleting rows.

The bare domain has no A record at all right now, so adding GitHub's is purely
additive. The only existing record you remove is the single `www` CNAME
pointing at Google.

---

## Step 1 — Rename `master` to `coursework`

Go to <https://github.com/jnrpobee/jnrpobee.github.io/branches>.

Find the `master` row and click the pencil (rename) icon at the right. Change
the name to `coursework` and confirm.

This moves nothing and deletes nothing — it relabels the branch your coursework
already lives on, so that a year from now the repository explains itself.

## Step 2 — Make `main` the default branch

**Settings** → **General** → scroll to *Default branch* → click the ⇄ switch
icon → choose **`main`** → **Update**, and confirm.

GitHub will warn that changing the default branch can affect open pull requests
and forks. You have neither, so it is safe. It is also reversible — switching
back is the same two clicks.

From this point the repository's front page shows your site rather than the
coursework, which stays one branch-selector click away.

## Step 3 — Point Pages at the workflow

**Settings** → **Pages** → under *Build and deployment*, change **Source** from
*Deploy from a branch* to **GitHub Actions**.

This is the step that stops the old coursework being published and hands
publishing to the workflow already sitting in your repo.

## Step 4 — Run the deploy

**Actions** tab → **Deploy to GitHub Pages** in the left sidebar → **Run
workflow** → **Run workflow**.

(You can trigger it by hand because the workflow declares `workflow_dispatch`.
No dummy commit needed.)

It takes a minute or two. The workflow does not simply publish the repository —
it assembles a folder of only the public files, then checks that every link is
well-formed and that every image and stylesheet the pages reference actually
exists. If either check fails the deploy stops rather than shipping something
broken, so a red run means a real problem: open it and read the failing step.

Green run: open <https://jnrpobee.github.io>. It should now be your site, not
the coursework redirect.

**Click through all six pages before touching DNS.** Check the portrait loads,
the navigation works on a narrow window, the publications render. Far easier to
fix now than once the domain points here.

## Step 5 — Change the DNS at Namecheap

Sign in → **Domain List** → **Manage** next to `solomonbpobee.com` → the
**Advanced DNS** tab.

**Delete one record.** In *Host Records*, find and remove:

```
CNAME    www    ghs.googlehosted.com
```

That row, and only that row. It is what currently sends visitors to Google Sites.

**Add five records** with **Add New Record**.

| Type | Host | Value |
|---|---|---|
| A Record | @ | 185.199.108.153 |
| A Record | @ | 185.199.109.153 |
| A Record | @ | 185.199.110.153 |
| A Record | @ | 185.199.111.153 |
| CNAME Record | www | jnrpobee.github.io |

TTL stays Automatic. Save each row with the green tick.

**Leave everything else alone** — the MX records (your email forwarding), the
SPF TXT, and the Google verification TXT. None conflict with GitHub.

Optional IPv6: four AAAA records on `@` pointing at `2606:50c0:8000::153`,
`2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

## Step 6 — Attach the domain

**Settings** → **Pages** → **Custom domain** → enter `www.solomonbpobee.com` →
**Save**. Your `CNAME` file already contains this, so it may be pre-filled.

GitHub verifies the DNS. Namecheap usually propagates within thirty minutes,
sometimes a couple of hours. "Domain not correctly configured" almost always
means the records have not spread yet — wait rather than change anything.
<https://dnschecker.org> for `www.solomonbpobee.com` shows what the world sees;
when it shows `jnrpobee.github.io`, you are there.

Then tick **Enforce HTTPS**. The certificate can take up to an hour, and a
warning before then is normal.

## Step 7 — Check the launch, then retire the old site

- `https://www.solomonbpobee.com` loads the new site
- `https://solomonbpobee.com` redirects to `www` — GitHub does this for you
- All six pages work, including on a phone
- A made-up URL like `/nonsense` shows the styled 404
- **Email yourself at your `@solomonbpobee.com` address and confirm it still
  arrives.** Two minutes, and it is the one thing that could have gone quietly
  wrong.
- Paste the URL into WhatsApp or Slack; the preview card should show your
  portrait

Then remove the custom domain mapping from the old site in Google Sites, and
submit `https://www.solomonbpobee.com/sitemap.xml` at
<https://search.google.com/search-console> so results stop pointing at the
Google Sites version. Do not delete the old Google site until you are sure
nothing on it is lost.

---

## Making changes later

```powershell
cd C:\Users\jnrpo\Documents\website_design\v2-dark
python build.py
python check_links.py .
git add -A
git commit -m "what changed"
git push
```

The push is the deploy — about a minute. Every version stays in history, so a
bad change is one `git revert` away.

To look at the old coursework again: `git checkout coursework`, or use the
branch dropdown on GitHub.

---

## Still outstanding

The CV page's Education and Experience sections say "To add", the About page's
"Beyond the lab" says "Your words go here", and the LinkedIn URL
(`linkedin.com/in/jnrpobee`) is my inference rather than something I confirmed.
None block the deploy; all three are a one-minute redeploy to fix.

## If you would rather use Cloudflare later

`DEPLOY.md` covers that route. The same repository connects to Cloudflare Pages
in a few minutes — you would turn GitHub Pages off then, so the two are not both
claiming the domain.
