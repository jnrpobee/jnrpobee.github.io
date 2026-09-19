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

  /* ── current year ────────────────────────────────────────── */
  $$('[data-year]').forEach(function (el) {
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

  /* ── publication filters (publications page) ─────────────── */
  var chips = $$('.chip');
  var pubs = $$('.pub');
  var countEl = $('#pub-count');
  var emptyEl = $('#pub-empty');
  function applyFilter(f) {
    var shown = 0;
    pubs.forEach(function (p) {
      var match = (f === 'all') || (p.getAttribute('data-topic') === f);
      p.hidden = !match;
      if (match) shown++;
    });
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
  $$('[data-copy-bib]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pre = $('pre', document.getElementById(btn.getAttribute('data-copy-bib')));
      copyText(pre.textContent, 'BibTeX copied');
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
})();
