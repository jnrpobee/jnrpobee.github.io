# Publishing solomonbpobee.com with GitHub Pages

Written against your actual setup, looked up on 18 September 2026:

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
address stops arriving. Nothing in this guide touches them, and Namecheap's
Advanced DNS screen lists MX records in a separate section from the host
records you *will* edit — but it is worth knowing before you start deleting
rows.

The good news: the bare domain has no A record at all right now, so adding
GitHub's is purely additive. The only existing record you remove is the single
`www` CNAME pointing at Google.

---

## Step 1 — Create the repository

Go to <https://github.com/new>.

- **Repository name:** `jnrpobee.github.io` — this exact name. A repo named
  after your account serves from the root of your GitHub domain.
- **Visibility:** Public. GitHub Pages needs this on the Free plan; private
  repos require Pro.
- **Do not** tick "Add a README", a `.gitignore`, or a licence. Your folder
  already has what it needs, and an initial commit on GitHub's side turns your
  first push into a merge conflict.

Click **Create repository**.

## Step 2 — Install Git if you have not

Check first — open PowerShell and run `git --version`. If you get a version
number, skip ahead.

Otherwise install [Git for Windows](https://git-scm.com/download/win), accept
the defaults, and close and reopen PowerShell afterwards so it picks up the new
command.

## Step 3 — Push the folder

In PowerShell:

```powershell
cd C:\Users\jnrpo\Documents\website_design\v2-dark

git init -b main
git add .
git commit -m "Personal site"
git remote add origin https://github.com/jnrpobee/jnrpobee.github.io.git
git push -u origin main
```

A browser window will open asking you to authorise Git. If instead it asks for
a password in the terminal, it wants a personal access token, not your account
password — GitHub stopped accepting passwords over HTTPS years ago. Generate
one at **Settings → Developer settings → Personal access tokens → Fine-grained
tokens**, give it read and write access to this repository, and paste it at the
password prompt.

Refresh the repository page. Your files should be there.

## Step 4 — Turn Pages on

In the repository: **Settings** → **Pages** → under *Build and deployment*, set
**Source** to **GitHub Actions**.

That is the whole configuration. The workflow file already in your folder does
the rest.

## Step 5 — Watch the first deploy and check it

Open the **Actions** tab. A run called *Deploy to GitHub Pages* should be going.
It takes a minute or two.

The workflow does not simply publish the repository. It assembles a folder of
only the public files, then runs two checks against it — every link is
well-formed, and every image and stylesheet the pages reference actually
exists. If either fails the deploy stops rather than shipping a broken site.
A red run means one of those caught something; open it and read the failing
step.

Green run: your site is live at **https://jnrpobee.github.io**.

**Click through all six pages there before you touch DNS.** Check the portrait
loads, the navigation works, the publications list renders. Fixing things now
is far easier than after the domain points here.

## Step 6 — Change the DNS at Namecheap

Sign in to Namecheap → **Domain List** → **Manage** next to `solomonbpobee.com`
→ the **Advanced DNS** tab.

**First, delete one record.** In the *Host Records* table, find the row:

```
CNAME    www    ghs.googlehosted.com
```

Delete that row, and only that row. It is what currently sends visitors to
Google Sites.

**Then add five records.** Use the **Add New Record** button for each.

Four A records, all with host `@`:

| Type | Host | Value |
|---|---|---|
| A Record | @ | 185.199.108.153 |
| A Record | @ | 185.199.109.153 |
| A Record | @ | 185.199.110.153 |
| A Record | @ | 185.199.111.153 |

And one CNAME:

| Type | Host | Value |
|---|---|---|
| CNAME Record | www | jnrpobee.github.io |

Leave TTL on Automatic. Save with the green tick on each row.

**Leave everything else alone** — the MX records (your email forwarding), the
SPF TXT record, and the Google verification TXT. None of them conflict with
GitHub.

If you want IPv6 as well, you can add four AAAA records on `@` pointing at
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153` and
`2606:50c0:8003::153`. Optional — the site works without them.

## Step 7 — Tell GitHub about the domain

Back in the repository: **Settings** → **Pages** → **Custom domain**. Enter
`www.solomonbpobee.com` and click **Save**.

GitHub checks the DNS. Namecheap usually propagates in under thirty minutes,
sometimes a couple of hours. If it says the domain is not correctly configured,
that normally means the records have not spread yet — wait rather than change
anything. <https://dnschecker.org> for `www.solomonbpobee.com` shows you what
the world currently sees; when it shows `jnrpobee.github.io` you are there.

Once it validates, tick **Enforce HTTPS**. The certificate takes up to an hour
and a warning before then is normal.

Your `CNAME` file already contains `www.solomonbpobee.com`, so this step may
already be filled in for you.

## Step 8 — Check the launch, then retire the old site

Confirm each of these:

- `https://www.solomonbpobee.com` loads the new site
- `https://solomonbpobee.com` redirects to the `www` version — GitHub does this
  for you
- All six pages work, including on a phone
- A made-up URL like `/nonsense` shows the styled 404 page
- **Send yourself an email at your `@solomonbpobee.com` address and confirm it
  still arrives.** Two minutes, and it is the one thing here that could have
  gone quietly wrong.
- Paste the URL into WhatsApp or Slack and check the preview card shows your
  portrait

Then, in Google Sites, remove the custom domain mapping from the old site.
Do not delete the old site outright until you are sure nothing on it is lost.

Finally, submit `https://www.solomonbpobee.com/sitemap.xml` at
<https://search.google.com/search-console>. Without this, Google will keep
serving the old Google Sites version in results for a while.

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

The push is the deploy — about a minute. Every version stays in the repository
history, so a bad change is one `git revert` away.

---

## Still outstanding

The CV page's Education and Experience sections say "To add", the About page's
"Beyond the lab" says "Your words go here", and the LinkedIn URL
(`linkedin.com/in/jnrpobee`) is my inference rather than something I confirmed.
None block the deploy; all three are a one-minute redeploy to fix.

## If you would rather use Cloudflare later

`DEPLOY.md` covers that route. The same repository connects to Cloudflare Pages
in a few minutes — you would turn GitHub Pages off at that point so the two are
not both claiming the domain.
