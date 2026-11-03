(function () {
  // Always land at the top of a new page (unless the link points to a section on it)
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function toTop() { if (!location.hash) window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  toTop();
  document.addEventListener('DOMContentLoaded', toTop);
  window.addEventListener('load', toTop);
  window.addEventListener('pageshow', function (e) { if (e.persisted) toTop(); });
  var userMoved = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) { window.addEventListener(ev, function () { userMoved = true; }, { passive: true, once: true }); });
  document.querySelectorAll('iframe').forEach(function (f) { f.addEventListener('load', function () { if (!userMoved && !location.hash) window.scrollTo(0, 0); }); });
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Hero entrance
  requestAnimationFrame(function () {
  // Always land at the top of a new page (unless the link points to a section on it)
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  function toTop() { if (!location.hash) window.scrollTo({ top: 0, left: 0, behavior: 'instant' }); }
  toTop();
  document.addEventListener('DOMContentLoaded', toTop);
  window.addEventListener('load', toTop);
  window.addEventListener('pageshow', function (e) { if (e.persisted) toTop(); });
  var userMoved = false;
  ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) { window.addEventListener(ev, function () { userMoved = true; }, { passive: true, once: true }); });
  document.querySelectorAll('iframe').forEach(function (f) { f.addEventListener('load', function () { if (!userMoved && !location.hash) window.scrollTo(0, 0); }); });
    requestAnimationFrame(function () { document.body.classList.add('loaded'); });
  });

  // Header condenses after scrolling
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.mobile-bar');
  var lastY = window.scrollY;
  function onScrollHeader() {
    var y = window.scrollY;
    if (header) {
      if (y > 140) header.classList.add('condensed'); else if (y < 16) header.classList.remove('condensed');
      var menuOpen = document.querySelector('.nav .drop.open');
      if (y > 420 && y > lastY + 4 && !menuOpen) header.classList.add('tucked');
      else if (y < lastY - 4 || y <= 420) header.classList.remove('tucked');
    }
    lastY = y;
    if (bar) {
      var end = document.querySelector('.cta-band') || document.querySelector('.site-footer');
      var endTop = end ? end.getBoundingClientRect().top : 1e9;
      bar.classList.toggle('show', window.scrollY > 320 && endTop > window.innerHeight - 10);
    }
  }
  window.addEventListener('scroll', onScrollHeader, { passive: true });
  onScrollHeader();

  // Bevel frames: drawn to match the logo's mitred panel
  var NS = 'http://www.w3.org/2000/svg';
  function drawFrame(el) {
    var svg = el.querySelector('svg.frame');
    if (!svg) { svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'frame'); svg.setAttribute('aria-hidden', 'true'); el.appendChild(svg); }
    var w = el.offsetWidth, h = el.offsetHeight;
    var p = parseFloat(getComputedStyle(el).paddingTop) || 24;
    var o = 2.5, i = p - 1.5;
    if (!w || !h) return;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('preserveAspectRatio', 'none');
    var shapes = [
      ['rect', { x: o, y: o, width: w - 2 * o, height: h - 2 * o, rx: 4 }, 'outer'],
      ['rect', { x: i, y: i, width: w - 2 * i, height: h - 2 * i }, ''],
      ['path', { d: 'M' + o + ' ' + o + 'L' + i + ' ' + i + 'M' + (w - o) + ' ' + o + 'L' + (w - i) + ' ' + i + 'M' + o + ' ' + (h - o) + 'L' + i + ' ' + (h - i) + 'M' + (w - o) + ' ' + (h - o) + 'L' + (w - i) + ' ' + (h - i) }, 'diag'],
      ['path', { d: 'M' + w / 2 + ' ' + o + 'V' + i + 'M' + w / 2 + ' ' + (h - o) + 'V' + (h - i) + 'M' + o + ' ' + h / 2 + 'H' + i + 'M' + (w - o) + ' ' + h / 2 + 'H' + (w - i) }, 'diag']
    ];
    svg.innerHTML = '';
    shapes.forEach(function (s) {
      var n = document.createElementNS(NS, s[0]);
      for (var k in s[1]) n.setAttribute(k, s[1][k]);
      n.setAttribute('pathLength', '1');
      if (s[2]) n.setAttribute('class', s[2]);
      svg.appendChild(n);
    });
  }
  var bevels = document.querySelectorAll('.bevel');
  bevels.forEach(function (b) {
    var img = b.querySelector('img');
    drawFrame(b);
    if (img && !img.complete) img.addEventListener('load', function () { drawFrame(b); });
  });
  if ('ResizeObserver' in window) {
    var ro = new ResizeObserver(function (entries) { entries.forEach(function (e) { drawFrame(e.target); }); });
    bevels.forEach(function (b) { ro.observe(b); });
  } else {
    window.addEventListener('resize', function () { bevels.forEach(drawFrame); });
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { bevels.forEach(drawFrame); });

  // Headings sign themselves off as they come into view
  var heads = document.querySelectorAll('main .section h2');
  if ('IntersectionObserver' in window && !reduce) {
    var hio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('signed'); hio.unobserve(e.target); } }); }, { rootMargin: '0px 0px -15% 0px' });
    heads.forEach(function (h) { hio.observe(h); });
  } else { heads.forEach(function (h) { h.classList.add('signed'); }); }

  // The logo draws in on the first page of a visit only
  try { if (!sessionStorage.getItem('ycbc-intro')) { doc.classList.add('intro'); sessionStorage.setItem('ycbc-intro', '1'); } } catch (e) {}

  // Reveal on scroll
  var targets = document.querySelectorAll('[data-reveal],[data-stagger],.bevel');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add('in'); });
  }

  // ---------- pinned scroll scenes ----------
  function clamp(x) { return Math.max(0, Math.min(1, x)); }
  function ease(x) { return 1 - Math.pow(1 - x, 3); }
  var scenes = [].slice.call(document.querySelectorAll('.scene'));
  if (reduce) doc.classList.add('no-scene');

  var handlers = {
    words: function (el) {
      var w = el.querySelectorAll('.w');
      return function (p) { var n = Math.round(clamp(p * 1.15) * w.length); for (var i = 0; i < w.length; i++) w[i].classList.toggle('lit', i < n); };
    },
    converge: function (el) {
      var a = el.querySelector('.a'), b = el.querySelector('.b'), c = el.querySelector('.c'), dot = el.querySelector('.dot'), after = el.querySelector('.after');
      return function (p) {
        var t1 = ease(clamp(p / 0.55)), t2 = ease(clamp((p - 0.5) / 0.3)), t3 = clamp((p - 0.72) / 0.18);
        a.style.strokeDashoffset = 1 - t1; b.style.strokeDashoffset = 1 - t1; c.style.strokeDashoffset = 1 - t2;
        dot.style.opacity = t1 > 0.98 ? 1 : 0;
        after.style.opacity = t3; after.style.transform = 'translateY(' + (12 * (1 - t3)) + 'px)';
      };
    },
    settle: function (el) {
      var w = [].slice.call(el.querySelectorAll('.sw'));
      var seed = 7; function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280 - 0.5; }
      var off = w.map(function () { return [rnd() * 260, rnd() * 180, rnd() * 40]; });
      return function (p) {
        w.forEach(function (n, i) {
          var e = ease(clamp(p * 1.35 - i * 0.025));
          var k = 1 - e, o = off[i];
          n.style.transform = 'translate(' + (o[0] * k) + 'px,' + (o[1] * k) + 'px) rotate(' + (o[2] * k) + 'deg)';
          n.style.opacity = 0.2 + 0.8 * e;
        });
      };
    },
    stamp: function (el) {
      var items = el.querySelectorAll('.stamps li'), soft = el.querySelector('.soft');
      return function (p) {
        for (var i = 0; i < items.length; i++) items[i].classList.toggle('on', p > 0.08 + i * 0.17);
        if (soft) soft.classList.toggle('on', p > 0.82);
      };
    },
    thread: function (el) {
      var ol = el.querySelector('ol'), li = el.querySelectorAll('li');
      return function (p) {
        var q = clamp(p * 1.15);
        ol.style.setProperty('--p', q);
        for (var i = 0; i < li.length; i++) li[i].classList.toggle('on', q >= i / (li.length - 1) - 0.001 && q > 0.02);
      };
    },
    split: function (el) {
      var l = el.querySelector('.card.l'), r = el.querySelector('.card.r'), one = el.querySelector('.one'), bodies = el.querySelectorAll('.card .body');
      var mobile = function () { return window.innerWidth <= 700; };
      return function (p) {
        var e = ease(clamp((p - 0.1) / 0.55)), t = clamp((p - 0.5) / 0.3);
        if (mobile()) { l.style.transform = 'translateY(' + (50 * (1 - e)) + '%)'; r.style.transform = 'translateY(' + (-50 * (1 - e)) + '%)'; }
        else { var k = 1 - e; l.style.transform = 'translateX(calc(' + (50 * k) + '% + ' + k + 'rem))'; r.style.transform = 'translateX(calc(' + (-50 * k) + '% - ' + k + 'rem))'; }
        one.style.opacity = 1 - clamp(p / 0.3);
        for (var i = 0; i < bodies.length; i++) bodies[i].style.opacity = t;
      };
    },
    hub: function (el) {
      var lines = el.querySelectorAll('line'), nodes = el.querySelectorAll('.node');
      return function (p) {
        for (var i = 0; i < lines.length; i++) {
          var t = ease(clamp(p * 1.4 - i * 0.09));
          lines[i].style.strokeDashoffset = 1 - t;
          nodes[i].style.opacity = clamp((t - 0.8) / 0.2);
        }
      };
    }
  };

  var running = scenes.map(function (el) {
    var f = handlers[el.getAttribute('data-scene')];
    return f ? { el: el, fn: f(el), target: 0, shown: -1 } : null;
  }).filter(Boolean);

  // Each scene holds in the center of the screen while it plays.
  // Progress runs from the moment the stage pins to the moment it releases.
  function measure() {
    var vh = window.innerHeight;
    running.forEach(function (s) {
      var r = s.el.getBoundingClientRect();
      var span = s.el.offsetHeight - vh;
      s.target = reduce ? 1 : (span > 0 ? clamp(-r.top / span) : clamp((vh * 0.6 - r.top) / (vh * 0.5)));
    });
  }
  var raf = null;
  function frame() {
    raf = null;
    var again = false;
    running.forEach(function (s) {
      if (s.shown < 0) s.shown = s.target;
      var d = s.target - s.shown;
      if (Math.abs(d) > 0.0015) { s.shown += d * 0.16; again = true; } else { s.shown = s.target; }
      s.fn(s.shown);
      s.el.style.setProperty('--glow', s.shown.toFixed(3));
    });
    if (again) raf = requestAnimationFrame(frame);
  }
  function kick() { measure(); if (!raf) raf = requestAnimationFrame(frame); }
  window.addEventListener('scroll', kick, { passive: true });
  window.addEventListener('resize', kick);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(kick);
  kick();

  // Gentle parallax on the hero mark
  var mark = null;
  if (mark && !reduce) {
    window.addEventListener('scroll', function () {
      var y = Math.min(window.scrollY, 800);
      mark.style.transform = 'translateY(' + (y * 0.12) + 'px)';
    }, { passive: true });
  }

  // Accordions (FAQ answers and phone-menu groups) open and close on the same curve.
  // The panel animates grid-template-rows between 0fr and 1fr, so heights are never measured.
  function smoothDetails(d, panelSel, guard) {
    var sum = d.querySelector('summary'), panel = d.querySelector(panelSel);
    if (!sum || !panel || reduce) return;
    sum.addEventListener('click', function (e) {
      e.preventDefault();
      if (guard && !guard()) return;
      if (d.open && !d.classList.contains('shut')) {
        d.classList.add('shut');
        var done = function (ev) {
          if (ev && (ev.target !== panel || ev.propertyName !== 'grid-template-rows')) return;
          panel.removeEventListener('transitionend', done);
          if (d.classList.contains('shut')) { d.open = false; d.classList.remove('shut'); }
        };
        panel.addEventListener('transitionend', done);
        setTimeout(done, 650);
      } else {
        d.classList.add('shut');
        d.open = true;
        requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.remove('shut'); }); });
      }
    });
  }
  document.querySelectorAll('.faq details, .dist-more').forEach(function (d) { smoothDetails(d, '.answer'); });
  document.querySelectorAll('.mobile-nav details').forEach(function (d) { smoothDetails(d, '.m-body'); });
  // Home's extra areas: open on wide screens, tidy accordions on phones
  var minis = document.querySelectorAll('details.mini');
  var mq = window.matchMedia('(max-width: 860px)');
  function setMinis() { minis.forEach(function (d) { d.open = !mq.matches; }); }
  setMinis(); if (mq.addEventListener) mq.addEventListener('change', setMinis);
  minis.forEach(function (d) {
    smoothDetails(d, '.answer', function () { return mq.matches; });
  });

  // Desktop dropdown
  document.querySelectorAll('.nav .drop').forEach(function (d) {
    var btn = d.querySelector('button');
    var close = function () { d.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !d.classList.contains('open');
      d.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    d.addEventListener('mouseenter', function () { d.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); });
    var t = null;
    d.addEventListener('mouseleave', function () { t = setTimeout(close, 220); });
    d.addEventListener('mouseenter', function () { clearTimeout(t); });
    document.addEventListener('click', close);
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') { close(); btn.focus(); } });
  });

  // Mobile menu
  var panel = document.querySelector('.mobile-nav');
  var openBtn = document.querySelector('.menu-toggle');
  if (panel && openBtn) {
    var closeBtn = panel.querySelector('.close');
    var setOpen = function (o) {
      panel.classList.toggle('open', o);
      openBtn.setAttribute('aria-expanded', String(o));
      document.body.style.overflow = o ? 'hidden' : '';
      if (bar) bar.style.visibility = o ? 'hidden' : '';
      if (o) closeBtn.focus(); else openBtn.focus();
    };
    openBtn.addEventListener('click', function () { setOpen(true); });
    closeBtn.addEventListener('click', function () { setOpen(false); });
    panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
  }
})();
