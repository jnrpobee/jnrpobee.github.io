/* ─────────────────────────────────────────────────────────────
   Solomon B. Pobee — portfolio (dark research portfolio)
   Shared behaviour for every page. No dependencies, no build.
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var EMAIL = 'jnrpobee@byu.edu';
  var GH_USER = 'jnrpobee';
  var root = document.documentElement;

  function reduce() {
    return window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  }
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  }

  /* ── dates in the reader's own format ────────────────────── */
  /* Every real date on the site carries its ISO value in datetime="". The
     page ships with the month spelled out, which is unambiguous anywhere;
     here it becomes whatever the reader's machine uses — 9/19/2026 in the
     US, 19/09/2026 in most other places. If anything below fails the
     spelled-out text simply stays, which is why it is the fallback. */
  $$('time[datetime]').forEach(function (el) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(el.getAttribute('datetime') || '');
    if (!m) return;
    /* Built from the parts, not from the string: new Date('2026-09-19') is
       parsed as UTC midnight, which is still the 18th anywhere west of
       Greenwich — the date would read a day early across the Americas. */
    var d = new Date(+m[1], +m[2] - 1, +m[3]);
    if (isNaN(d.getTime())) return;
    try {
      /* Month spelled out, not numeric: "September 21, 2026" for a US reader
         and "21 September 2026" for a British one. The locale still decides
         the order, so it stays the reader's own convention, but nobody has to
         work out whether 9/21 means September or the 9th. The explicit
         options are used rather than dateStyle:'long' because they are
         supported further back and produce the same result. */
      el.textContent = d.toLocaleDateString(undefined, {
        year: 'numeric', month: 'long', day: 'numeric'
      });
    } catch (e) { /* keep the spelled-out date */ }
  });

  /* ── current year ────────────────────────────────────────── */
  /* Deliberately narrow. This used to match any [data-year], which meant
     the day a note carried a data-year of its own, every note on the blog
     had its contents replaced by the number 2026. The hook now names the
     one element it is for. */
  $$('[data-copyright-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ── toast ───────────────────────────────────────────────── */
  var toastEl = $('#toast');
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2200);
  }

  /* ── clipboard, with a fallback for older browsers ───────── */
  function copyText(text, okMsg) {
    function fallback() {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.top = '-1000px';
        document.body.appendChild(ta);
        ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        toast(ok ? okMsg : 'Could not copy automatically');
      } catch (err) {
        toast('Could not copy automatically');
      }
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { toast(okMsg); }, fallback);
    } else {
      fallback();
    }
  }

  /* ── mobile menu: a panel under the bar, page still visible ─ */
  var toggle = $('#menu-toggle');
  var drawer = $('#drawer');
  var scrim = $('#scrim');
  var topbar = $('.site-header');
  var trapKeys = null;

  function menuIsOpen() { return document.body.classList.contains('menu-open'); }

  function focusables() {
    return $$('a[href], button:not([disabled])', topbar).filter(function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0;
    });
  }

  function openMenu() {
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close navigation');
    document.body.classList.add('menu-open');
    if (scrim) scrim.hidden = false;

    var first = $('a[href]', drawer);
    if (first) first.focus();

    trapKeys = function (e) {
      if (e.key !== 'Tab') return;
      var f = focusables();
      if (!f.length) return;
      var a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    };
    document.addEventListener('keydown', trapKeys, true);
  }

  function closeMenu(opts) {
    if (!menuIsOpen()) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open navigation');
    document.body.classList.remove('menu-open');
    if (scrim) scrim.hidden = true;
    if (trapKeys) {
      document.removeEventListener('keydown', trapKeys, true);
      trapKeys = null;
    }
    if (!opts || opts.restoreFocus !== false) {
      if (topbar.contains(document.activeElement) || document.activeElement === document.body) {
        toggle.focus();
      }
    }
  }

  if (toggle && drawer) {
    toggle.addEventListener('click', function () {
      if (menuIsOpen()) { closeMenu(); } else { openMenu(); }
    });
    if (scrim) scrim.addEventListener('click', function () { closeMenu(); });
    $$('a', drawer).forEach(function (a) {
      a.addEventListener('click', function () { closeMenu({ restoreFocus: false }); });
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 980) closeMenu({ restoreFocus: false });
    });
  }


  /* ── reveal on scroll ─────────────────────────────────────────
     Blocks ease up into place as they come into view. Anything that
     can't be observed is simply shown, so nothing is ever stranded
     invisible. */
  var REVEAL_SELECTOR = '.hero-copy, .portrait-panel, .focus-strip > .kicker, .focus-list, .section-heading, .project-card, .pub-group, .repo, .detail-card, .value, .cv-row, .split > div, .research-question > *, .slot, .inprogress, .pager, .links, .mail-wrap, .filters';
  (function revealOnScroll() {
    if (!root.classList.contains('js-reveal')) return;
    var els = $$(REVEAL_SELECTOR);
    if (!els.length) return;

    function showAll() {
      els.forEach(function (el) { el.classList.add('is-in'); });
    }
    if (!('IntersectionObserver' in window)) { showAll(); return; }

    try {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.classList.add('is-in');
          obs.unobserve(en.target);
        });
      }, { threshold: 0.06, rootMargin: '0px 0px -40px 0px' });
      els.forEach(function (el) { io.observe(el); });
      window.revealPrime = function (scope) {
        $$(REVEAL_SELECTOR, scope || document).forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('is-in');
        });
      };
    } catch (e) { showAll(); }
  })();

  /* ── back to top ─────────────────────────────────────────── */
  var totop = $('#totop');
  var ticking = false;
  function onScroll() {
    if (totop) {
      if (window.scrollY > 500) { totop.classList.add('show'); }
      else { totop.classList.remove('show'); }
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();
  if (totop) {
    totop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce() ? 'auto' : 'smooth' });
    });
  }

  /* ── theme ───────────────────────────────────────────────── */
  (function () {
    var root = document.documentElement;
    var buttons = $$('[data-theme-toggle]');
    if (!buttons.length) return;
    var mq = null;
    try { mq = window.matchMedia('(prefers-color-scheme:dark)'); } catch (e) {}

    function current() {
      var chosen = root.getAttribute('data-theme');
      if (chosen === 'dark' || chosen === 'light') return chosen;
      return mq && mq.matches ? 'dark' : 'light';
    }
    function label() {
      var next = current() === 'dark' ? 'light' : 'dark';
      buttons.forEach(function (b) {
        b.setAttribute('aria-label', 'Switch to the ' + next + ' theme');
        var t = $('.theme-btn-t', b);
        if (t) t.textContent = 'Switch to ' + next;
      });
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var next = current() === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        try { localStorage.setItem('theme', next); } catch (e) {}
        label();
      });
    });
    /* With no stored choice the page follows the system, so the label has
       to keep up if the visitor changes that setting while reading. */
    if (mq && mq.addEventListener) mq.addEventListener('change', label);
    label();
  })();

  /* ── publication filters (publications page) ─────────────── */
  /* The publications filters, and only those. This used to be every
     .chip on whatever page had loaded, which was harmless while the
     publications page was the only one with chips - and stopped being
     harmless the moment the blog grew its own. Both sets write
     aria-pressed, so on the blog the two handlers fought: pressing the
     calendar button cleared whichever category was lit. */
  var chips = $$('.chip[data-filter]');
  var pubs = $$('.pub');
  var countEl = $('#pub-count');
  var emptyEl = $('#pub-empty');
  var searchEl = $('#pub-search');
  var activeTopic = 'all';

  /* The searchable text of each entry, gathered once. Title, authors and
     venue — not the description, so typing a common word like "design"
     does not match half the page through its prose. */
  var haystack = pubs.map(function (p) {
    return ['.pub-title', '.pub-authors', '.pub-venue'].map(function (sel) {
      var el = $(sel, p);
      return el ? el.textContent : '';
    }).join(' \u0001 ').toLowerCase();
  });

  /* Every whitespace-separated word has to appear somewhere, so "pobee
     nature" finds the paper that is both, in either order. */
  function matchesQuery(i, terms) {
    for (var t = 0; t < terms.length; t++) {
      if (haystack[i].indexOf(terms[t]) === -1) return false;
    }
    return true;
  }

  function applyFilter(f) {
    if (f) activeTopic = f;
    f = activeTopic;
    var q = searchEl ? searchEl.value.trim().toLowerCase() : '';
    var terms = q ? q.split(/\s+/) : [];
    var shown = 0;
    pubs.forEach(function (p, i) {
      var match = ((f === 'all') || (p.getAttribute('data-topic') === f))
                  && (!terms.length || matchesQuery(i, terms));
      p.hidden = !match;
      if (match) shown++;
    });
    if (emptyEl) {
      emptyEl.textContent = q
        ? 'Nothing matches “' + q + '”.'
        : 'No publications in this area yet.';
    }
    // a venue group with nothing left in it shouldn't sit there empty
    $$('.pub-group').forEach(function (g) {
      var visible = $$('.pub', g).filter(function (p) { return !p.hidden; }).length;
      g.hidden = visible === 0;
      var c = $('[data-group-count]', g);
      if (c) c.textContent = visible;
    });
    chips.forEach(function (c) {
      c.setAttribute('aria-pressed', String(c.getAttribute('data-filter') === f));
    });
    if (countEl) {
      countEl.textContent = shown + (shown === 1 ? ' publication' : ' publications');
    }
    if (emptyEl) emptyEl.hidden = shown !== 0;
  }
  chips.forEach(function (c) {
    c.addEventListener('click', function () { applyFilter(c.getAttribute('data-filter')); });
  });

  if (searchEl) {
    searchEl.addEventListener('input', function () { applyFilter(); });
    /* Escape clears rather than closing anything, which is what a search
       field inside a page is expected to do. */
    searchEl.addEventListener('keydown', function (e) {
      if ((e.key || '') !== 'Escape') return;
      e.stopPropagation();
      if (searchEl.value) { e.preventDefault(); searchEl.value = ''; applyFilter(); }
      else { searchEl.blur(); }
    });
    /* "/" jumps to the field, the way it does on GitHub — but not while
       the reader is already typing somewhere, or a slash could never be
       typed into any other field on the page. The command palette is on
       Cmd/Ctrl-K, so there is no clash. */
    document.addEventListener('keydown', function (e) {
      if ((e.key || '') !== '/' || e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target || {};
      var tag = (t.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select' || t.isContentEditable) return;
      e.preventDefault();
      searchEl.focus();
      searchEl.select();
    });
  }

  /* ── citations ───────────────────────────────────────────── */
  $$('[data-cite]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('data-cite'));
      var open = !panel.hidden;
      panel.hidden = open;
      btn.setAttribute('aria-expanded', String(!open));
      btn.textContent = open ? 'Cite' : 'Hide';
    });
  });
  /* Citation format switcher. Each panel holds one <pre> per style and shows
     one at a time; the copy button takes whichever is visible, so there is a
     single source of truth for what gets copied. */
  function showCiteStyle(panelId, style) {
    var panel = document.getElementById(panelId);
    if (!panel) return;
    $$('pre[data-cite-style]', panel).forEach(function (pre) {
      pre.hidden = pre.getAttribute('data-cite-style') !== style;
    });
    $$('[data-cite-style][data-cite-panel]', panel).forEach(function (tab) {
      tab.setAttribute('aria-selected',
        String(tab.getAttribute('data-cite-style') === style));
    });
  }
  $$('[data-cite-panel]').forEach(function (tab) {
    tab.addEventListener('click', function () {
      showCiteStyle(tab.getAttribute('data-cite-panel'),
                    tab.getAttribute('data-cite-style'));
    });
    tab.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      var tabs = $$('[data-cite-panel="' + tab.getAttribute('data-cite-panel') + '"]');
      var i = tabs.indexOf(tab);
      var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      if (!next) return;
      e.preventDefault();
      next.click();
      next.focus();
    });
  });

  $$('[data-copy-bib]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('data-copy-bib'));
      var pre = $$('pre[data-cite-style]', panel).filter(function (p) { return !p.hidden; })[0]
             || $('pre', panel);
      var label = pre.getAttribute('data-cite-style') === 'bibtex' ? 'BibTeX' : 'Citation';
      copyText(pre.textContent, label + ' copied');
    });
  });

  /* Print. With a CV PDF in assets/cv/ the button carries its path and that
     file is what gets printed, not the web page. The PDF goes into an
     offscreen iframe and we print that; Chrome, Edge and Firefox all handle
     it. Safari will not print a PDF in an iframe, so if the call throws, or
     the frame has not loaded after a moment, the file is opened in a tab
     instead and the reader prints from the viewer. An empty data-print means
     no PDF has been added yet, and the page itself is printed. */
  function printPdf(url) {
    var done = false;
    var frame = document.createElement('iframe');
    frame.setAttribute('aria-hidden', 'true');
    frame.style.cssText =
      'position:fixed;right:0;bottom:0;width:1px;height:1px;opacity:0;border:0;';
    function fallback() {
      if (done) return;
      done = true;
      if (frame.parentNode) frame.parentNode.removeChild(frame);
      window.open(url, '_blank', 'noopener');
    }
    var timer = setTimeout(fallback, 4000);
    frame.onload = function () {
      clearTimeout(timer);
      if (done) return;
      try {
        frame.contentWindow.focus();
        frame.contentWindow.print();
        done = true;
      } catch (e) {
        fallback();
      }
    };
    frame.onerror = fallback;
    frame.src = url;
    document.body.appendChild(frame);
  }

  $$('[data-print]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-print');
      if (url) printPdf(url); else window.print();
    });
  });
  $$('[data-copy-doi]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      copyText('https://doi.org/' + btn.getAttribute('data-copy-doi'), 'DOI link copied');
    });
  });
  $$('[data-copy-mail]').forEach(function (btn) {
    btn.addEventListener('click', function () { copyText(EMAIL, 'Email address copied'); });
  });

  /* ── command palette (⌘K / Ctrl-K) ───────────────────────── */
  var palette = $('#palette');
  var cmdInput = $('#cmd-input');
  var cmdList = $('#cmd-list');
  var openBtns = $$('.cmd-btn');
  var lastFocus = null, sel = 0, visible = [];

  var trapPalette = null;
  function paletteFocusables() {
    return $$('input, button:not([disabled])', palette).filter(function (el) {
      return el.offsetWidth > 0 || el.offsetHeight > 0;
    });
  }


  function nav(href) { window.location.href = href; }

  var ITEMS = [
    { kind: 'Page', label: 'Home', run: function () { nav('/'); } },
    { kind: 'Page', label: 'Research', run: function () { nav('/research'); } },
    { kind: 'Page', label: 'Projects', run: function () { nav('/projects'); } },
    { kind: 'Page', label: 'Publications', run: function () { nav('/publications'); } },
    { kind: 'Page', label: 'About', run: function () { nav('/about'); } },
    { kind: 'Page', label: 'CV', run: function () { nav('/cv'); } },
    { kind: 'Action', label: 'Copy email address', run: function () { copyText(EMAIL, 'Email address copied'); } },
    { kind: 'Action', label: 'Print this page', run: function () { window.print(); } },
    { kind: 'Link', label: 'GitHub profile', run: function () { window.open('https://github.com/jnrpobee', '_blank', 'noopener'); } },
    { kind: 'Link', label: 'Google Scholar', run: function () { window.open('https://scholar.google.com/citations?user=02WgxKoAAAAJ', '_blank', 'noopener'); } },
    { kind: 'Link', label: 'ORCID profile', run: function () { window.open('https://orcid.org/0009-0007-5172-0410', '_blank', 'noopener'); } },
    { kind: 'Link', label: 'ResearchGate profile', run: function () { window.open('https://www.researchgate.net/profile/Solomon-Pobee', '_blank', 'noopener'); } },
    { kind: 'Link', label: 'LeetCode', run: function () { window.open('https://leetcode.com/u/pobee/', '_blank', 'noopener'); } },
    { kind: 'Link', label: 'LinkedIn profile', run: function () { window.open('https://linkedin.com/in/jnrpobee', '_blank', 'noopener'); } },
    { kind: 'Paper', label: 'Nature recreation framework (IJHCI 2025)', run: function () { window.open('https://doi.org/10.1080/10447318.2024.2443808', '_blank', 'noopener'); } },
    { kind: 'Paper', label: 'MathBuddy chatbot (Springer 2026)', run: function () { window.open('https://doi.org/10.1007/978-3-032-13174-4_25', '_blank', 'noopener'); } }
  ];

  function render(q) {
    if (!cmdList) return;
    q = (q || '').trim().toLowerCase();
    visible = ITEMS.filter(function (it) {
      return !q || (it.label + ' ' + it.kind).toLowerCase().indexOf(q) !== -1;
    });
    sel = 0;
    cmdList.innerHTML = '';
    if (!visible.length) {
      var li0 = document.createElement('li');
      var b0 = document.createElement('button');
      b0.type = 'button';
      b0.disabled = true;
      b0.textContent = 'Nothing matches';
      li0.appendChild(b0);
      cmdList.appendChild(li0);
      return;
    }
    visible.forEach(function (it, i) {
      var li = document.createElement('li');
      if (i === 0) li.className = 'sel';
      var b = document.createElement('button');
      b.type = 'button';
      var s1 = document.createElement('span');
      s1.textContent = it.label;
      var s2 = document.createElement('span');
      s2.className = 'kind';
      s2.textContent = it.kind;
      b.appendChild(s1);
      b.appendChild(s2);
      b.addEventListener('click', function () { closeCmd(); it.run(); });
      li.appendChild(b);
      cmdList.appendChild(li);
    });
  }

  function move(d) {
    var lis = cmdList.querySelectorAll('li');
    if (!lis.length || !visible.length) return;
    if (lis[sel]) lis[sel].classList.remove('sel');
    sel = (sel + d + visible.length) % visible.length;
    lis[sel].classList.add('sel');
    lis[sel].scrollIntoView({ block: 'nearest' });
  }

  function openCmd() {
    if (!palette) return;
    lastFocus = document.activeElement;
    palette.hidden = false;
    cmdInput.value = '';
    render('');
    cmdInput.focus();
    trapPalette = function (e) {
      if (e.key !== 'Tab') return;
      var f = paletteFocusables();
      if (!f.length) return;
      var a = f[0], z = f[f.length - 1];
      if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
      else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
    };
    document.addEventListener('keydown', trapPalette, true);
  }
  function closeCmd() {
    if (!palette) return;
    palette.hidden = true;
    if (trapPalette) { document.removeEventListener('keydown', trapPalette, true); trapPalette = null; }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  openBtns.forEach(function (b) { b.addEventListener('click', openCmd); });
  if (cmdInput) cmdInput.addEventListener('input', function () { render(cmdInput.value); });
  if (palette) {
    palette.addEventListener('mousedown', function (e) { if (e.target === palette) closeCmd(); });
  }

  document.addEventListener('keydown', function (e) {
    var k = (e.key || '').toLowerCase();
    if ((e.metaKey || e.ctrlKey) && k === 'k') {
      e.preventDefault();
      if (palette && palette.hidden) { openCmd(); } else { closeCmd(); }
      return;
    }
    if (k === 'escape' && menuIsOpen()) { e.preventDefault(); closeMenu(); return; }
    if (!palette || palette.hidden) return;
    if (k === 'escape') { e.preventDefault(); closeCmd(); }
    else if (k === 'arrowdown') { e.preventDefault(); move(1); }
    else if (k === 'arrowup') { e.preventDefault(); move(-1); }
    else if (k === 'enter') {
      e.preventDefault();
      var it = visible[sel];
      if (it) { closeCmd(); it.run(); }
    }
  });

  /* show the right modifier key for the platform */
  try {
    if (!/Mac|iPhone|iPad/.test(navigator.platform || '')) {
      $$('.cmd-btn kbd').forEach(function (k) { k.textContent = 'Ctrl K'; });
    }
  } catch (e) {}

  /* ── GitHub refresh (projects page) ──────────────────────────
     Repo cards render from the values written into the HTML, so the
     page is complete with no network call. This then refreshes stars,
     descriptions and last-push dates from the GitHub API. If the
     request fails or is rate-limited, the written values stand.      */
  function relTime(iso) {
    var then = new Date(iso).getTime();
    if (isNaN(then)) return '';
    var days = Math.floor((Date.now() - then) / 86400000);
    if (days <= 0) return 'updated today';
    if (days === 1) return 'updated yesterday';
    if (days < 30) return 'updated ' + days + ' days ago';
    var months = Math.round(days / 30);
    if (months < 12) return 'updated ' + months + (months === 1 ? ' month ago' : ' months ago');
    var years = Math.round(days / 365);
    return 'updated ' + years + (years === 1 ? ' year ago' : ' years ago');
  }

  (function refreshRepos() {
    var rows = $$('[data-repo]');
    if (!rows.length || typeof fetch !== 'function') return;

    fetch('https://api.github.com/users/' + GH_USER + '/repos?per_page=100&sort=updated', {
      headers: { 'Accept': 'application/vnd.github+json' }
    })
      .then(function (res) { if (!res.ok) throw new Error('gh'); return res.json(); })
      .then(function (list) {
        if (!Array.isArray(list)) return;
        var byName = {};
        list.forEach(function (r) { if (r && r.full_name) byName[r.full_name.toLowerCase()] = r; });

        rows.forEach(function (el) {
          var repo = byName[(el.getAttribute('data-repo') || '').toLowerCase()];
          if (!repo) return;

          var desc = $('.repo-desc', el);
          if (desc && repo.description) desc.textContent = repo.description;

          var stars = $('[data-stars]', el);
          if (stars && repo.stargazers_count > 0) {
            stars.textContent = repo.stargazers_count + (repo.stargazers_count === 1 ? ' star' : ' stars');
            stars.hidden = false;
          }

          var updated = $('[data-updated]', el);
          var when = repo.pushed_at ? relTime(repo.pushed_at) : '';
          if (updated && when) { updated.textContent = when; updated.hidden = false; }
        });
      })
      .catch(function () { /* keep the values written into the page */ });
  })();
  /* ── the notes page ───────────────────────────────────────────────────
     Two things the markup cannot do on its own. Both are additions: with
     this file missing, the board's cards are still links that jump to
     their note, and the shuffle button is never shown at all rather than
     sitting there doing nothing. */
  (function () {
    var posts = [].slice.call(document.querySelectorAll('details.post'));
    if (!posts.length) return;

    /* A link to #post-3 lands on a note that is closed. Open it, so
       arriving from the board - or from a link someone shared - shows the
       writing rather than a heading to click a second time. */
    /* Find the note a link is asking for, forgiving two kinds of old link.
       Addresses used to be positions - #post-3 - so anything saved before
       they became permanent still has to land somewhere sensible; and an
       address built from a title stops matching if the title is ever
       edited, so the date at the front of it is accepted on its own. */
    function findNote(id) {
      var el = document.getElementById(id);
      if (el && el.tagName.toLowerCase() === 'details') return el;

      var old = /^post-(\d+)$/.exec(id);
      if (old) return posts[parseInt(old[1], 10) - 1] || null;

      var date = /^(\d{4}-\d{2}-\d{2})/.exec(id);
      if (date) {
        for (var i = 0; i < posts.length; i++) {
          if (posts[i].id.indexOf(date[1]) === 0) return posts[i];
        }
      }
      return null;
    }

    function openTarget(hash, flash) {
      if (!hash || hash.charAt(0) !== '#') return;
      var el = findNote(hash.slice(1));
      if (!el) return;
      /* A link from the board, or a link someone shared, can point at a
         note the current filter or page length is hiding. Reveal it
         rather than scrolling to nothing. */
      if (el.hidden) { el.hidden = false; }
      el.open = true;
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      if (flash) {
        el.classList.remove('post-lit');
        void el.offsetWidth;                 // restart the animation
        el.classList.add('post-lit');
      }
    }

    window.addEventListener('hashchange', function () { openTarget(location.hash, false); });
    openTarget(location.hash, false);

    /* ── filtering and paging ───────────────────────────────────────
       Everything here is an addition. Without it the page is the whole
       list, newest first, with its month headings - which is a perfectly
       good page, and the reason the controls carry `hidden` in the markup
       and are revealed from here rather than the other way round. */
    var STEP = 5;
    var filters = document.querySelector('[data-filters]');
    var counts = document.querySelector('[data-counts]');
    var moreWrap = document.querySelector('[data-more-wrap]');
    var moreBtn = moreWrap && moreWrap.querySelector('[data-more]');
    var countOut = filters && filters.querySelector('[data-filter-count]');
    var heads = [].slice.call(document.querySelectorAll('[data-month-head]'));
    var years = [].slice.call(document.querySelectorAll('[data-year-head]'));
    var picked = '';          /* '' means every category */
    var month = '';           /* '' means every month; set below */
    var perPage = STEP;       /* 0 means everything */
    var shown = perPage;

    function matching() {
      return posts.filter(function (p) {
        if (picked && p.getAttribute('data-blog-topic') !== picked) return false;
        if (month && p.getAttribute('data-month') !== month) return false;
        return true;
      });
    }

    function draw() {
      var hits = matching();
      var limit = perPage ? Math.min(shown, hits.length) : hits.length;

      posts.forEach(function (p) { p.hidden = true; });
      hits.slice(0, limit).forEach(function (p) { p.hidden = false; });

      /* A month heading belongs on the page only while one of its notes
         is still on it, and its own count has to follow the filter. */
      heads.forEach(function (h) {
        var month = h.getAttribute('data-month-head');
        var live = hits.slice(0, limit).filter(function (p) {
          return p.getAttribute('data-month') === month;
        }).length;
        h.hidden = live === 0;
        var n = h.querySelector('[data-month-count]');
        if (n) n.textContent = live + (live === 1 ? ' note' : ' notes');
      });

      /* The count at the right edge is only worth reading when the page
         is holding notes back. "5 of 18" says something; "3 notes" beside
         a chip that already reads 3 is the same number twice. */
      /* A year band goes when its last month goes, and it stays away
         entirely while there is only one year on the page - one band
         saying 2026 over everything says nothing. */
      var liveYears = 0;
      years.forEach(function (y) {
        var on = hits.slice(0, limit).filter(function (p) {
          return p.getAttribute('data-in-year') === y.getAttribute('data-year-head');
        }).length;
        if (on) liveYears++;
        y.hidden = on === 0;
        var n = y.querySelector('[data-year-count]');
        if (n) n.textContent = on + (on === 1 ? ' note' : ' notes');
      });
      if (liveYears < 2) years.forEach(function (y) { y.hidden = true; });

      if (countOut) {
        var trimmed = limit < hits.length;
        countOut.hidden = !trimmed;
        countOut.textContent = trimmed ? limit + ' of ' + hits.length : '';
      }
      if (moreWrap) {
        var left = hits.length - limit;
        moreWrap.hidden = left <= 0;
        if (moreBtn) {
          moreBtn.textContent = 'Show ' + Math.min(perPage || left, left) +
                                ' more \u2193';
        }
      }
    }

    /* Which chips a group owns has to be said explicitly. The calendar's
       own button is a .chip sitting inside the filter row, so a handler
       that reached for every .chip in there treated it as a category:
       picking a month quietly cleared the category filter and lit the
       calendar button as though it were one. */
    function press(group, sel, on) {
      [].forEach.call(group.querySelectorAll(sel), function (c) {
        c.setAttribute('aria-pressed', String(on(c)));
      });
    }

    if (filters) {
      filters.hidden = false;
      filters.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip[data-cat]');
        if (!chip) return;
        /* One at a time. Pressing the chip that is already on turns it
           off again, which lands back on all notes - so "All" is a
           shortcut rather than the only way out of a filter. */
        var cat = chip.getAttribute('data-cat');
        picked = (cat === 'all' || cat === picked) ? '' : cat;
        press(filters, '.chip[data-cat]', function (c) {
          var k = c.getAttribute('data-cat');
          return k === 'all' ? picked === '' : k === picked;
        });
        shown = perPage;      /* a new filter starts the count again */
        draw();
      });
    }

    /* ── the month calendar ─────────────────────────────────────────
       A year of months, one year on screen at a time, with the months
       that have writing in them pressable and the rest shown but dead.
       It narrows the list the same way the chips do and stacks with them,
       so "campus notes from August" is a thing a reader can ask for.

       Being a popover rather than a native menu, it has to close itself:
       on Escape, on a click elsewhere, and after a choice. */
    var monthPick = document.querySelector('[data-month-pick]');
    if (monthPick) {
      monthPick.hidden = false;
      var toggle = monthPick.querySelector('[data-cal-toggle]');
      var panel = monthPick.querySelector('[data-cal]');
      var yearOut = monthPick.querySelector('[data-cal-year]');
      var grids = [].slice.call(monthPick.querySelectorAll('[data-cal-grid]'));
      var steps = [].slice.call(monthPick.querySelectorAll('[data-cal-step]'));
      var current = monthPick.querySelector('[aria-current="true"]');

      /* The page opens on the newest month that has writing in it - the
         current edition - which the markup has already marked. */
      month = current ? current.getAttribute('data-month') : '';
      var atYear = grids.length ? grids.length - 1 : 0;   /* grids run newest first */
      atYear = 0;

      function showYear() {
        grids.forEach(function (g, i) { g.hidden = i !== atYear; });
        if (yearOut) yearOut.textContent = grids[atYear].getAttribute('data-cal-grid');
        steps.forEach(function (b) {
          var dir = parseInt(b.getAttribute('data-cal-step'), 10);
          b.disabled = atYear + dir < 0 || atYear + dir >= grids.length;
        });
      }

      function open(on) {
        panel.hidden = !on;
        toggle.setAttribute('aria-expanded', String(on));
        if (on) showYear();
      }

      toggle.addEventListener('click', function () {
        open(panel.hidden);
      });
      steps.forEach(function (b) {
        b.addEventListener('click', function () {
          atYear += parseInt(b.getAttribute('data-cal-step'), 10);
          atYear = Math.max(0, Math.min(grids.length - 1, atYear));
          showYear();
        });
      });
      monthPick.addEventListener('click', function (e) {
        var cell = e.target.closest('[data-month]');
        if (!cell) return;
        month = cell.getAttribute('data-month');
        monthPick.querySelectorAll('[aria-current]').forEach(function (el) {
          el.removeAttribute('aria-current');
        });
        if (month) cell.setAttribute('aria-current', 'true');
        toggle.textContent = month || 'Every month';
        /* Whichever year the chosen month lives in becomes the one the
           panel opens on next time. */
        grids.forEach(function (g, i) {
          if (g.contains(cell)) atYear = i;
        });
        shown = perPage;
        open(false);
        draw();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && !panel.hidden) { open(false); toggle.focus(); }
      });
      document.addEventListener('click', function (e) {
        if (!panel.hidden && !monthPick.contains(e.target)) open(false);
      });
      showYear();
    }

    if (counts) {
      counts.hidden = false;
      counts.addEventListener('click', function (e) {
        var chip = e.target.closest('.chip[data-count]');
        if (!chip) return;
        perPage = parseInt(chip.getAttribute('data-count'), 10) || 0;
        shown = perPage;
        press(counts, '.chip[data-count]', function (c) { return c === chip; });
        draw();
      });
    }

    if (moreBtn) {
      moreBtn.addEventListener('click', function () {
        shown += perPage || matching().length;
        draw();
      });
    }

    if (filters || counts || moreWrap || monthPick) draw();

    var btn = document.querySelector('[data-surprise]');
    if (btn && posts.length > 1) {
      btn.hidden = false;
      var last = null;
      btn.addEventListener('click', function () {
        /* Shuffle within what the reader has chosen to look at. Sending
           them to a note their own filter excludes would be a strange
           answer to pressing this. */
        var pool = matching();
        if (pool.length < 2) pool = posts;
        var pick;
        do { pick = pool[Math.floor(Math.random() * pool.length)]; }
        while (pick === last && pool.length > 1);
        last = pick;
        posts.forEach(function (p) { if (p !== pick) p.open = false; });
        openTarget('#' + pick.id, true);
      });
    }
  })();

  /* ── the board turns over ────────────────────────────────── */
  (function () {
    /* The hero board holds three cards and the site can hold any number
       of notes. Left alone, the fourth note and everything after it
       never reach the board at all: the three newest sit up there until
       something displaces them, and the rest live only in the list.

       So the cards themselves turn over. Each one changes at the moment
       the lime leaves it, to a note that was waiting off the board, and
       the note it was showing goes to the back of the queue. Given long
       enough, everything written gets its turn up there.

       build.py writes the notes into the page as JSON - see note_data()
       - and only when there are more of them than the board can hold.
       So the absence of that element is the signal that there is
       nothing to do here, and the page that ships without it keeps the
       CSS animation and the three cards it was built with. */
    var board = $('.notes-playground');
    if (!board || reduce()) return;

    var tag = $('[data-board-notes]', board);
    if (!tag) return;

    var all;
    try { all = JSON.parse(tag.textContent); } catch (e) { return; }
    if (!all || !all.length) return;

    var cards = $$('.note-paper', board);
    if (cards.length < 2 || all.length <= cards.length) return;

    var TURN = 5200;   /* how long a card holds the lime */
    var FADE = 1400;   /* how long the colour takes to travel - --fade in styles.css */

    /* Slot one holds. It carries the pinned note, or failing that the
       newest, and that is the one thing a visitor arriving should be
       able to count on finding. The other slots do the travelling. */
    var HELD = 0;

    var showing = all.slice(0, cards.length);
    var queue = all.slice(cards.length);

    /* Shuffled once, then taken in turn. Drawing at random each time
       would show the same note twice running and leave others never
       shown; a shuffled queue reads as unordered and still gives every
       note its turn. */
    for (var i = queue.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var swap = queue[i]; queue[i] = queue[j]; queue[j] = swap;
    }

    function paint(card, note, slot) {
      card.setAttribute('data-fasten', note.fasten);
      card.setAttribute('href', note.href);
      /* The card's own children, not a descendant search: the fastener
         is a span too, and so is the "Read" line, and neither of them
         carries writing that changes. */
      var label = null;
      [].forEach.call(card.children, function (el) {
        if (label || el.tagName !== 'SPAN') return;
        if (el.className.indexOf('fasten') !== -1) return;
        if (el.className.indexOf('note-open') !== -1) return;
        label = el;
      });
      if (label) {
        label.textContent = ('0' + (slot + 1)).slice(-2) + ' / ' + note.cat;
      }
      var title = $('strong', card);
      if (title) title.textContent = note.title;
      var when = $('p', card);
      if (when) when.textContent = note.date;
    }

    function turn(slot) {
      if (slot === HELD || !queue.length) return;
      var card = cards[slot];
      card.classList.add('turning');
      window.setTimeout(function () {
        /* Take the first note in the queue wearing a fastener that is
           not already on the board. build.py's no-repeats rule holds
           for the order it wrote; rotation breaks that order, and two
           red pins side by side is what it looks like when it does. */
        var worn = showing.map(function (n, k) {
          return k === slot ? null : n.fasten;
        });
        var pick = 0;
        while (pick < queue.length && worn.indexOf(queue[pick].fasten) !== -1) {
          pick++;
        }
        if (pick === queue.length) pick = 0;
        var arriving = queue.splice(pick, 1)[0];
        queue.push(showing[slot]);
        showing[slot] = arriving;
        paint(card, arriving, slot);
        card.classList.remove('turning');
      }, FADE * 0.45);
    }

    var at = 0, started = false;
    function step() {
      var leaving = (at - 1 + cards.length) % cards.length;
      cards.forEach(function (c, n) { c.classList.toggle('lit', n === at); });
      /* Not on the first pass: nothing has been lit yet, so nothing has
         earned the right to change. */
      if (started) turn(leaving);
      started = true;
      at = (at + 1) % cards.length;
    }

    /* Someone reading a card is not someone who wants it to change.
       mouseenter and mouseleave rather than mouseover and mouseout:
       these fire for the board alone and ignore the crossings between
       its own children, which would otherwise start it again the
       moment the cursor moved from one card to the next. */
    var paused = false;
    board.addEventListener('mouseenter', function () { paused = true; });
    board.addEventListener('mouseleave', function () { paused = false; });
    board.addEventListener('focusin', function () { paused = true; });
    board.addEventListener('focusout', function () { paused = false; });

    board.classList.add('is-turning');
    step();
    window.setInterval(function () { if (!paused) step(); }, TURN);
  })();
})();
