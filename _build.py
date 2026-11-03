#!/usr/bin/env python3
"""Builds the YCBC static site into ./site. Edit content here, then run: python3 build.py"""
import os, json, html, re

OUT = os.path.join(os.path.dirname(__file__), "site")
DOMAIN = "https://yakimacbc.org"
BOOK = "https://book.carepatron.com/Yakima-Center-for-Biblical-Counseling/David?p=CPYr9o-GQtWvPU1mG8IbVg&s=7IHqQZRP"
PHONE = "(509) 731-4772"
TEL = "tel:+15097314772"
EMAIL = "david.jamison@yakimacbc.org"
SUBSTACK = "https://ycbc.substack.com"
CHURCH = "https://www.saintandrewsyakima.org/"
GIVE = "https://standrewsyakima.churchcenter.com/giving/to/biblical-counseling-center"
BOOK_ATTR = f'href="{BOOK}" target="_blank" rel="noopener"'

HELP = [
    ("marriage.html", "Marriage", "Conflict, distance, broken trust, and preparing well for marriage."),
    ("anxiety.html", "Anxiety, worry & stress", "Fear, overwhelm, discouragement, and depression."),
    ("men.html", "Counseling for men", "Pornography, anger, discipline, and leading a family."),
    ("family.html", "Family & parenting", "Defiant kids, divided parents, and homes in conflict."),
]
NAV = [
    ("biblical-counseling.html", "Biblical counseling"),
    ("fees.html", "Sessions & fees"),
    ("about.html", "Meet the counselor"),
    ("churches.html", "For churches"),
    ("faq.html", "FAQ"),
    ("contact.html", "Contact"),
]
ABOUT = [
    ("biblical-counseling.html", "Biblical counseling", "What it is, and how we approach it.", "book"),
    ("about.html", "Meet the counselor", "David Jamison, director.", "people"),
    ("faq.html", "FAQs", "Common questions, answered plainly.", "chat"),
    ("contact.html", "Contact", "Phone, email, and our office.", "pin"),
]
TAGLINE = "Trusting the Word of Christ to help you walk with Christ and become like Christ."

CHEV = '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
ARROW = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M4 2l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
BURGER = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18M3 12h18M3 17h18" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'
PHONE_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z" fill="currentColor"/></svg>'


# Custom icon set in the logo's style: slate line work with one gold detail.
def _ic(body):
    return f'<svg class="ic" viewBox="0 0 40 40" aria-hidden="true">{body}</svg>'
ICONS = {
    "marriage": _ic('<circle cx="15" cy="21" r="9" class="s"/><circle cx="25" cy="21" r="9" class="g"/>'),
    "anxiety": _ic('<path class="s" d="M4 30h32M9 35h22M20 8v5M9.4 13.4l3.2 3.2M30.6 13.4l-3.2 3.2M4 24h4.5M31.5 24H36"/><path class="g" d="M11 30a9 9 0 0118 0"/>'),
    "men": _ic('<path class="s" d="M20 4l13 5v9c0 9-5.5 15-13 18C12.5 33 7 27 7 18V9z"/><path class="g" d="M20 12v14M14.5 17.5h11"/>'),
    "family": _ic('<path class="s" d="M5 19L20 6l15 13M9 16v18h22V16"/><path class="g" d="M17 34v-9h6v9"/>'),
    "foundation": _ic('<path class="s" d="M4 34h32M7 28h26v6H7zM10 22h20v6H10z"/><path class="g" d="M13 16h14v6H13z"/>'),
    "framework": _ic('<path class="s" d="M6 34V16h28v18M6 25h28M15 16v18M25 16v18"/><path class="g" d="M4 17L20 6l16 11"/>'),
    "phone": _ic('<path class="s" d="M12 6h6l2 8-4 2c1.5 3.5 4.5 6.5 8 8l2-4 8 2v6c0 1.5-1.2 2.5-2.8 2.4C18 29.5 10.5 22 10 9 10 7.2 10.8 6 12 6z"/>'),
    "mail": _ic('<rect class="s" x="5" y="10" width="30" height="21" rx="1.5"/><path class="g" d="M6 11l14 11 14-11"/>'),
    "book": _ic('<path class="s" d="M20 11c-4-3-9-3-14-2v21c5-1 10-1 14 2 4-3 9-3 14-2V9c-5-1-10-1-14 2zM20 11v21"/><path class="g" d="M25 7.5v8l2.5-1.8 2.5 1.8v-8.6"/>'),
    "paths": _ic('<path class="s" d="M20 36V23M20 23L9.5 11.5M20 23l10.5-11.5"/><path class="g" d="M6 15V8h7M34 15V8h-7"/>'),
    "church": _ic('<path class="s" d="M8 36V20l12-8 12 8v16M5 36h30M17 36v-6a3 3 0 016 0v6"/><path class="g" d="M20 3v9M16.5 6.5h7"/>'),
    "compass": _ic('<circle class="s" cx="20" cy="20" r="14.5"/><path class="s" d="M20 3v3M20 34v3M3 20h3M34 20h3"/><path class="g" d="M20 9.5l3.6 10.5L20 30.5 16.4 20z"/>'),
    "door": _ic('<path class="s" d="M9 36V5h17v31M5 36h30"/><path class="g" d="M26 5l7 4v26l-7 1z"/>'),
    "chat": _ic('<path class="s" d="M6 8h22v15H14l-6 5v-5H6z"/><path class="g" d="M30 14h4v14h-2v4l-5-4H17v-3"/>'),
    "clock": _ic('<circle class="s" cx="20" cy="20" r="14.5"/><path class="g" d="M20 11v9l6 4"/>'),
    "screen": _ic('<rect class="s" x="5" y="8" width="30" height="20" rx="1.5"/><path class="s" d="M14 34h12M20 28v6"/><circle class="g" cx="20" cy="17" r="3.2"/><path class="g" d="M14.5 25c1-3 3-4.4 5.5-4.4s4.5 1.4 5.5 4.4"/>'),
    "hand": _ic('<path class="s" d="M6 27h5l7 3h9l8-6c1-1 0-3-1.6-2.6L26 24h-7"/><path class="s" d="M11 24l5-3h6c2 0 2 3 0 3h-3"/><path class="g" d="M23 6l2.2 4.4 4.8.7-3.5 3.4.8 4.8-4.3-2.3-4.3 2.3.8-4.8-3.5-3.4 4.8-.7z"/>'),
    "card": _ic('<rect class="s" x="5" y="10" width="30" height="20" rx="1.5"/><path class="s" d="M5 16h30"/><path class="g" d="M10 24h8"/>'),
    "arrow": _ic('<path class="s" d="M6 20h24M23 12l8 8-8 8"/><circle class="g" cx="8" cy="20" r="3"/>'),
    "tag": _ic('<path class="s" d="M6 6h13l15 15-13 13L6 19z"/><circle class="g" cx="13" cy="13" r="2.6"/>'),
    "people": _ic('<circle class="s" cx="14" cy="13" r="5"/><path class="s" d="M5 33c0-6 4-10 9-10s9 4 9 10"/><circle class="g" cx="27" cy="15" r="4"/><path class="g" d="M24 23.5c1-.4 2-.5 3-.5 4.4 0 8 3.4 8 9"/>'),
    "layers": _ic('<path class="s" d="M20 6l15 7-15 7-15-7z"/><path class="s" d="M5 20l15 7 15-7"/><path class="g" d="M5 27l15 7 15-7"/>'),
    "turn": _ic('<path class="s" d="M8 34V20a8 8 0 018-8h14"/><path class="g" d="M25 6l6 6-6 6"/>'),
    "chain": _ic('<rect class="s" x="5" y="15" width="16" height="10" rx="5"/><rect class="g" x="19" y="15" width="16" height="10" rx="5"/>'),
    "flame": _ic('<path class="s" d="M20 35c-6.5 0-10.5-4.3-10.5-10 0-6.5 6-10 7-17 4 3 10 8.5 10 17"/><path class="g" d="M20 35c3.6 0 6-2.4 6-5.8 0-3.6-3-5.6-4.2-9.2-2.5 2-7.8 4.8-7.8 9.2 0 3.4 2.4 5.8 6 5.8z"/>'),
    "check": _ic('<circle class="s" cx="20" cy="20" r="14.5"/><path class="g" d="M13.5 20.5l4.5 4.5 8.5-9"/>'),
    "not": _ic('<circle class="s" cx="20" cy="20" r="14.5"/><path class="g" d="M10 30L30 10"/>'),
    "pin": _ic('<path class="s" d="M20 35s11-10.5 11-19a11 11 0 00-22 0c0 8.5 11 19 11 19z"/><circle class="g" cx="20" cy="16" r="4"/>'),
}
ICONS = {k: v.replace('<svg class="ic"', f'<svg class="ic ic-{k}"', 1) for k, v in ICONS.items()}
HELP_ICON = {"marriage.html": "marriage", "anxiety.html": "anxiety", "men.html": "men", "family.html": "family"}
MENU_PREVIEW = {
    "marriage.html": ("“They shall become one flesh.”", "Genesis 2:24", ["Communication and conflict", "Infidelity and rebuilding trust", "Pre-marital counseling"]),
    "anxiety.html": ("“He cares for you.”", "1 Peter 5:7", ["Worry and fear", "Depression and low moods", "Feeling overwhelmed"]),
    "men.html": ("“Stand firm in the faith.”", "1 Corinthians 16:13", ["Sexual sin and pornography", "Anger", "Leading a family well"]),
    "family.html": ("“Teach them diligently to your children.”", "Deuteronomy 6:7", ["Discipline and teenage rebellion", "Blended families", "Adult children"]),
}


def cur(page, href):
    return ' aria-current="page"' if page == href else ""


def header(page):
    items = "".join(
        f'<a class="mini-item" href="{h}"{cur(page,h)}>{ICONS[HELP_ICON[h]]}<span><b>{n}</b><small>{d}</small></span></a>' for h, n, d in HELP)
    previews = "".join(
        f'''<div class="mega-panel" data-panel="{h}"><blockquote>{MENU_PREVIEW[h][0]}<cite>{MENU_PREVIEW[h][1]}</cite></blockquote><p>{d}</p><ul>{"".join(f"<li>{c}</li>" for c in MENU_PREVIEW[h][2])}</ul><a class="more" href="{h}">Explore {n.lower() if h!="men.html" else "counseling for men"}</a></div>'''
        for h, n, d in HELP)
    about = "".join(f'<a class="mini-item" href="{h}"{cur(page,h)}>{ICONS[ic]}<span><b>{n}</b><small>{d}</small></span></a>' for h, n, d, ic in ABOUT)
    help_cur = ' class="is-current"' if page in HELP_ICON else ""
    about_cur = ' class="is-current"' if page in [a[0] for a in ABOUT] else ""
    m_help = "".join(f'<a class="m-item" href="{h}">{ICONS[HELP_ICON[h]]}<span>{n}</span>{CHEV_R}</a>' for h, n, _ in HELP)
    m_about = "".join(f'<a class="m-item" href="{h}">{ICONS[ic]}<span>{n}</span>{CHEV_R}</a>' for h, n, d, ic in ABOUT)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/logo.png" alt="Yakima Center for Biblical Counseling" width="1253" height="408"></a>
    <nav class="nav" aria-label="Main">
      <div class="drop"><button type="button" aria-expanded="false" aria-haspopup="true"{help_cur}>How we help {CHEV}</button>
        <div class="menu mega">
          <div class="mega-grid">{items}</div>
          <div class="mega-foot"><span>Not sure where you fit? Every new client starts with a free 20-minute consultation.</span><a class="btn btn-primary btn-sm" {BOOK_ATTR}>Book a consultation</a></div>
        </div>
      </div>
      <div class="drop"><button type="button" aria-expanded="false" aria-haspopup="true"{about_cur}>About {CHEV}</button>
        <div class="menu mini">{about}</div>
      </div>
      <a href="fees.html"{cur(page,"fees.html")}>Sessions &amp; fees</a>
      <a href="churches.html"{cur(page,"churches.html")}>For churches</a>
    </nav>
    <a class="btn btn-primary" {BOOK_ATTR}>Book a free consultation</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-label="Open menu">{BURGER}</button>
  </div>
</header>
<div class="mobile-nav" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="top"><img src="assets/logo-light.png" alt=""><button class="close" type="button" aria-label="Close menu">{CLOSE}</button></div>
  <div class="m-groups">
    <details class="m-group" open><summary class="m-label">How we help{CHEV}</summary><div class="m-body"><div class="m-in"><div class="m-list">{m_help}</div></div></div></details>
    <details class="m-group"><summary class="m-label">About{CHEV}</summary><div class="m-body"><div class="m-in"><div class="m-list">{m_about}</div></div></div></details>
    <details class="m-group"><summary class="m-label">Next steps{CHEV}</summary><div class="m-body"><div class="m-in">
      <div class="m-list"><a class="m-item" href="fees.html">{ICONS["card"]}<span>Sessions &amp; fees</span>{CHEV_R}</a>
      <a class="m-item" href="churches.html">{ICONS["church"]}<span>For pastors &amp; churches</span>{CHEV_R}</a></div>
    </div></div></details>
  </div>
  <div class="m-foot">
    <a class="btn btn-gold" {BOOK_ATTR}>Book a free consultation</a>
    <a class="m-tel" href="{TEL}">or call {PHONE}</a>
    <p class="mob-tag">{TAGLINE}</p>
  </div>
</div>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="assets/logo-light.png" alt="Yakima Center for Biblical Counseling" width="1253" height="408">
        <p class="foot-tag"><b>Truth that transforms.</b>{TAGLINE}</p>
      </div>
      <div>
        <h4>How we help</h4>
        <ul>{"".join(f'<li><a href="{h}">{n}</a></li>' for h, n, _ in HELP)}</ul>
      </div>
      <div>
        <h4>The center</h4>
        <ul><li><a href="biblical-counseling.html">Biblical counseling</a></li><li><a href="about.html">Meet the counselor</a></li><li><a href="fees.html">Sessions &amp; fees</a></li><li><a href="churches.html">For churches</a></li><li><a href="faq.html">FAQs</a></li></ul>
      </div>
      <div>
        <h4>Visit or call</h4>
        <ul class="foot-contact"><li>Upper floor, 32 N Front St<br>Yakima, WA 98901</li><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a {BOOK_ATTR}>Schedule an appointment</a></li><li><a href="{GIVE}">Support the ministry</a></li></ul>
      </div>
    </div>
    <div class="crisis-bar">
      <p><strong>Crisis resources</strong>For immediate safety concerns, call 911 or the Suicide &amp; Crisis Lifeline. We provide spiritual guidance, not emergency mental health services.</p>
      <div class="crisis-links"><a href="tel:911">Call 911</a><a href="tel:988">Call or text 988</a></div>
    </div>
    <div class="legal">
      <p><b>Religious ministry:</b> This ministry operates under Washington State religious exemption RCW 18.19.040(6). Our biblical counselors are not Washington state licensed mental health professionals and do not provide psychotherapy, psychological treatment, or mental health diagnosis. Biblical counseling is religious ministry, not professional therapy. <b>Church ministry:</b> Biblical counseling services are provided as ministry of <a href="{CHURCH}">Saint Andrew's Presbyterian Church</a> (PCA) and are based on biblical principles and theological teachings.</p>
      <p class="copy"><span>© 2026 Yakima Center for Biblical Counseling</span><a href="privacy.html">Privacy</a><a href="contact.html">Contact</a></p>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick actions">
  <a class="call" href="{TEL}">{PHONE_ICON}<span>Call</span></a>
  <a class="book" {BOOK_ATTR}>Book a free consultation</a>
</div>'''


NEXT = {
    "index.html": ("biblical-counseling.html", "Biblical counseling", "What it is, and how we approach it."),
    "marriage.html": ("biblical-counseling.html", "Biblical counseling", "How Scripture shapes the way we counsel."),
    "anxiety.html": ("biblical-counseling.html", "Biblical counseling", "How Scripture shapes the way we counsel."),
    "men.html": ("biblical-counseling.html", "Biblical counseling", "How Scripture shapes the way we counsel."),
    "family.html": ("biblical-counseling.html", "Biblical counseling", "How Scripture shapes the way we counsel."),
    "biblical-counseling.html": ("fees.html", "Sessions &amp; fees", "What to expect, and what it costs."),
    "fees.html": ("about.html", "Meet the counselor", "Get to know David."),
    "about.html": ("contact.html", "Schedule an appointment", "Start with a free 20-minute consultation."),
    "faq.html": ("contact.html", "Schedule an appointment", "Start with a free 20-minute consultation."),
    "churches.html": ("biblical-counseling.html", "Biblical counseling", "What your members can expect from us."),
    "privacy.html": ("index.html", "Home", "Back to the beginning."),
}


def next_band(fn):
    if fn not in NEXT:
        return ""
    h, t, d = NEXT[fn]
    return f'''<nav class="next-band" aria-label="Next page"><div class="wrap"><a href="{h}"><span class="lbl">Next</span><b>{t}</b><span class="d">{d}</span><span class="go">{ARROW}</span></a></div></nav>'''


def page(filename, title, description, body, extra_head=""):
    canon = DOMAIN + "/" + ("" if filename == "index.html" else filename.replace(".html", ""))
    return f'''<!DOCTYPE html>
<html lang="en" class="js seam-a">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/og.jpg">
<meta name="theme-color" content="#18241F">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/favicon.png">
<link rel="preload" href="assets/fonts/alegreya-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/styles.css">
{extra_head}
</head>
<body>
{header(filename)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="assets/site.js"></script>
</body>
</html>'''


DEFAULT_ACTIONS = f'<a class="btn btn-primary" {BOOK_ATTR}>Book a free consultation</a><a class="tel" href="{TEL}">or call <b>{PHONE}</b></a>'
PARTNER_ACTIONS = f'<a class="btn btn-primary" href="mailto:{EMAIL}?subject=Ministry%20partnership%20inquiry">Inquire about a ministry partnership</a><a class="tel" href="{TEL}">or call <b>{PHONE}</b></a>'


def cta(title="The first conversation is free.", text="All new clients begin with a free 20-minute consultation. Tell us what's going on, and we'll tell you honestly whether we can help.", actions=None):
    return f'''<section class="cta-band">
  <div class="wrap">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="actions">{(actions or DEFAULT_ACTIONS).replace("btn-primary","btn-light")}</div>
  </div>
</section>'''


def page_hero(h1, lede, crumb=None, facts=False, actions=None, icon=None, aside=None, variant="", top="", below=""):
    c = f'<p class="crumb">{ICONS[icon] if icon else ""}<a href="{crumb[0]}">{crumb[1]}</a></p>' if crumb else ""
    f = f'''<aside class="facts" aria-label="At a glance">
      <ul><li><b>Free</b><span>20-minute first consultation</span></li><li><b>$100</b><span>per 50–60 minute session</span></li><li><b>In person or video</b><span>Downtown Yakima or secure video</span></li></ul>
      <a class="tel" href="{TEL}">Call <b>{PHONE}</b></a>
    </aside>''' if facts else (aside or "")
    acts = "" if actions == "" else f'<div class="actions">{actions or DEFAULT_ACTIONS}</div>'
    return f'''<section class="page-hero{' has-facts' if (facts or aside) else ''} {variant}">
  <div class="wrap">
    <div class="ph-main">
    {top}
    {c}
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    {acts}
    </div>
    {f}
  </div>
  {below}
</section>'''


def concerns(intro_h, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'''<section class="section">
  <div class="wrap split">
    <div><h2>{intro_h}</h2><p class="lede" style="margin-top:1rem">If you see yourself here, you're in the right place.</p></div>
    <div class="concern-panel"><ul class="topic-list two">{lis}</ul></div>
  </div>
</section>'''


def verse_block(r):
    m = re.match(r"“(.*)”\s*(.+)$", r)
    if not m:
        return f"<blockquote class='pt-q'><p>{r}</p></blockquote>"
    return f"<blockquote class='pt-q'><p>{m.group(1)}</p><cite>{m.group(2)}</cite></blockquote>"


def points(h, intro, pts, note=""):
    cards = "".join(
        f'<article class="pt"><h3>{t}</h3><p>{d}</p>{verse_block(r) if r else ""}</article>'
        for t, d, r in pts)
    n = f'<p class="note">{note}</p>' if note else ""
    return f'''<section class="section tint">
  <div class="wrap">
    <div class="section-head"><h2>{h}</h2>{f"<p class=lede>{intro}</p>" if intro else ""}</div>
    <div class="pts swipe pts-{len(pts)}">{cards}</div>
    {n}
  </div>
</section>'''


def faq(items, heading="Questions"):
    ds = "".join(f'<details><summary>{q}</summary><div class="answer"><div class="answer-in">{a if a.lstrip().startswith("<") else "<p>"+a+"</p>"}</div></div></details>' for q, a in items)
    return f'''<section class="section">
  <div class="wrap split">
    <div><h2>{heading}</h2></div>
    <div class="faq">{ds}</div>
  </div>
</section>'''


def faq_groups(groups):
    out = ""
    for gid, title, items in groups:
        ds = "".join(f'<details><summary>{q}</summary><div class="answer"><div class="answer-in">{a if a.lstrip().startswith("<") else "<p>"+a+"</p>"}</div></div></details>' for q, a in items)
        out += f'''<section class="section faq-sec" id="{gid}"><div class="wrap split"><div><h2>{title}</h2></div><div class="faq">{ds}</div></div></section>'''
    return out


def expect_short():
    return f'''<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>How it works</h2></div>
    <ol class="steps">
      <li><h3>Free consultation</h3><p>A 20-minute call to hear what's going on, answer your questions, and decide together whether we're a good fit.</p></li>
      <li><h3>Weekly sessions</h3><p>50 to 60 minutes, in person downtown or by secure video. $100 per session.</p></li>
      <li><h3>Real change</h3><p>Every session ends with clear next steps, and we review your progress together as we go.</p></li>
    </ol>
  </div>
</section>'''


def cross(exclude):
    links = "".join(
        f'<a href="{h}">{ICONS[HELP_ICON[h]]}<b>{n}</b><span>{blurb}</span></a>'
        for h, n, blurb in [
            ("marriage.html", "Marriage", "Conflict, distance, broken trust"),
            ("anxiety.html", "Anxiety, worry & stress", "Fear, overwhelm, discouragement"),
            ("men.html", "Counseling for men", "Porn, anger, leading at home"),
            ("family.html", "Family & parenting", "Teens, discipline, home conflict"),
        ] if h != exclude)
    return f'''<section class="section tight tint">
  <div class="wrap">
    <div class="section-head"><h2 style="font-size:clamp(1.6rem,2.6vw,2.1rem)">Other ways we help</h2></div>
    <div class="cross">{links}</div>
  </div>
</section>'''


def faq_jsonld(items):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": html.unescape(q),
                            "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", " ", html.unescape(a)).strip()}} for q, a in items]}
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'



def scene_marriage():
    return """<section class="scene" data-scene="converge" aria-label="Genesis 2:24">
  <div class="stage"><div class="wrap">
    <svg class="converge" viewBox="0 0 1000 260" aria-hidden="true">
      <path class="a" pathLength="1" d="M0 30 C 260 30, 380 130, 560 130"/>
      <path class="b" pathLength="1" d="M0 230 C 260 230, 380 130, 560 130"/>
      <path class="c" pathLength="1" d="M560 130 L1000 130"/>
      <circle class="dot" cx="560" cy="130" r="8"/>
    </svg>
    <div class="after" style="margin-top:2.5rem"><p>“Therefore a man shall leave his father and his mother and hold fast to his wife, and they shall become one flesh.”</p><cite>Genesis 2:24</cite></div>
  </div></div>
</section>"""


def scene_anxiety():
    words = "Casting all your anxieties on him, because he cares for you.".split()
    w = " ".join(f'<span class="sw">{x}</span>' for x in words)
    return f"""<section class="scene" data-scene="settle" aria-label="1 Peter 5:7">
  <div class="stage"><div class="wrap">
    <p class="settle">{w}</p><cite>1 Peter 5:7</cite>
  </div></div>
</section>"""


def scene_men():
    return """<section class="scene" data-scene="stamp" aria-label="1 Corinthians 16:13-14">
  <div class="stage"><div class="wrap">
    <ul class="stamps"><li>Be watchful.</li><li>Stand firm in the faith.</li><li>Act like men.</li><li>Be strong.</li></ul>
    <span class="stamps"><span class="soft">Let all that you do be done in love.</span></span>
    <cite>1 Corinthians 16:13–14</cite>
  </div></div>
</section>"""


def scene_family():
    return """<section class="scene" data-scene="thread" aria-label="Deuteronomy 6:6-7">
  <div class="stage"><div class="wrap thread">
    <div><p class="verse">“These words that I command you today shall be on your heart. You shall teach them diligently to your children, and shall talk of them…”</p><cite>Deuteronomy 6:6–7</cite></div>
    <ol><li>when you sit in your house,</li><li>when you walk by the way,</li><li>when you lie down,</li><li>and when you rise.</li></ol>
  </div></div>
</section>"""


def scene_approach():
    return """<section class="scene" data-scene="split" aria-label="Sin and suffering">
  <div class="stage"><div class="wrap split-scene">
    <div class="pair">
      <div class="card l"><div class="body"><h3>Sin</h3><p>requires</p><ul><li>Confession</li><li>Confrontation</li><li>Conformity to Christ</li><li>Commitment to change</li></ul></div></div>
      <div class="card r"><div class="body"><h3>Suffering</h3><p>calls for</p><ul><li>Moving toward Christ</li><li>Mourning with Him</li><li>Maturing through trials</li><li>Ministering comfort to others</li></ul></div></div>
      <div class="one"><p>We counsel sin and suffering differently.</p></div>
    </div>
  </div></div>
</section>"""


def scene_hub():
    nodes = [(80, 90), (300, 28), (520, 90), (540, 320), (300, 392), (60, 320)]
    lines = "".join(f'<line pathLength="1" x1="300" y1="210" x2="{x}" y2="{y}"/>' for x, y in nodes)
    ns = "".join(f'<g class="node"><circle cx="{x}" cy="{y}" r="22"/><path d="M{x} {y-11}V{y+11}M{x-8} {y-3}H{x+8}"/></g>' for x, y in nodes)
    return f"""<section class="scene" data-scene="hub" aria-label="Church partnerships">
  <div class="stage"><div class="wrap hub">
    <div><h2>One center, many churches.</h2><p>Our hope is to serve congregations across the Yakima Valley, giving pastors a trusted place to send people who need more time than a pastor can give.</p></div>
    <svg viewBox="0 0 600 420" aria-hidden="true">{lines}{ns}<image href="assets/mark-large.png" x="262" y="152" width="76" height="116"/></svg>
  </div></div>
</section>"""


def hub_graphic():
    nodes = [(70, 95), (300, 28), (530, 95), (550, 315), (300, 392), (50, 315)]
    lines = "".join(f'<line style="--i:{i}" x1="300" y1="210" x2="{x}" y2="{y}"/>' for i, (x, y) in enumerate(nodes))
    ns = "".join(f'<g class="node" style="--i:{i}"><circle cx="{x}" cy="{y}" r="24"/><path d="M{x} {y-12}V{y+12}M{x-8} {y-4}H{x+8}"/></g>' for i, (x, y) in enumerate(nodes))
    ring = '<circle class="ring" cx="300" cy="210" r="150"/>'
    return f'''<div class="hub-hero" aria-hidden="true"><svg viewBox="0 0 600 420">{ring}{lines}{ns}<image href="assets/mark-large.png" x="260" y="149" width="80" height="123"/></svg></div>'''


def window_graphic():
    """A lancet window in the logo's style; lead lines draw, then panes fill in."""
    panes = [
        ("M60 150V95a40 40 0 0180 0v55z", "sage"), ("M60 150h40v70H60z", "gold"), ("M100 150h40v70h-40z", "slate"),
        ("M60 220h40v70H60z", "slate"), ("M100 220h40v70h-40z", "sage"), ("M60 290h80v40H60z", "gold"),
    ]
    p = "".join(f'<path class="pane {c}" style="--i:{i}" d="{d}"/>' for i, (d, c) in enumerate(panes))
    lead = '<path class="lead" pathLength="1" d="M60 330V95a40 40 0 0180 0v235zM60 150h80M60 220h80M60 290h80M100 150v140"/>'
    frame = '<path class="frame" pathLength="1" d="M48 342V93a52 52 0 01104 0v249z"/>'
    sill = '<path class="sill" d="M36 342h128v10H36z"/>'
    ray = '<circle class="glow" cx="100" cy="100" r="22"/>'
    return f'<div class="window-graphic" aria-hidden="true"><svg viewBox="0 0 200 360">{ray}{p}{lead}{frame}{sill}</svg></div>'


def door_graphic():
    """An arched doorway in the logo's style: the frame draws, then the door swings open to warm light."""
    opening = "M60 330V95a40 40 0 0180 0v235z"
    door = (f'<g class="leaf"><path class="pane slate" style="--i:0" d="{opening}"/>'
            '<path class="lead" pathLength="1" d="M70 320V150h60v170M70 140v-40a30 30 0 0160 0v40z"/>'
            '<circle class="knob" cx="126" cy="230" r="4"/></g>')
    return ('<div class="hgfx door-graphic" aria-hidden="true"><svg viewBox="0 0 200 360">'
            f'<path class="light" d="{opening}"/><circle class="glow" cx="100" cy="210" r="34"/>'
            f'{door}'
            '<path class="frame" pathLength="1" d="M48 342V93a52 52 0 01104 0v249z"/>'
            '<path class="lead" pathLength="1" d="M60 330V95a40 40 0 0180 0v235z"/>'
            '<path class="sill" d="M34 342h132v10H34z"/><path class="sill" d="M46 352h108v8H46z"/>'
            '</svg></div>')


def lamp_graphic():
    """An oil lamp (Psalm 119:105): the outline draws, the body fills, then the flame catches."""
    body = "M28 238c0-26 30-36 74-36 34 0 58 10 70 22l26-10c-4 18-18 28-34 32-18 14-40 20-66 20-46 0-70-10-70-28z"
    return ('<div class="hgfx lamp-graphic" aria-hidden="true"><svg viewBox="0 0 230 300">'
            '<circle class="glow" cx="192" cy="168" r="40"/>'
            f'<path class="pane slate" style="--i:0" d="{body}"/>'
            '<path class="pane sage" style="--i:1" d="M78 206c8-10 40-10 48 0z"/>'
            f'<path class="frame" pathLength="1" d="{body}"/>'
            '<path class="lead" pathLength="1" d="M70 266l-6 16h84l-6-14"/>'
            '<path class="sill" d="M56 282h104v8H56z"/>'
            '<path class="flame" d="M194 206c-12-8-14-24-4-38 3-4 4-10 3-16 10 8 18 22 14 36-2 9-7 15-13 18z"/>'
            '<path class="flame-in" d="M195 204c-5-4-6-11-2-17 1 4 4 6 6 9 2 4 0 7-4 8z"/>'
            '</svg></div>')


def path_404_graphic():
    """A winding path and a signpost, for the page-not-found page."""
    return ('<div class="hgfx path404-graphic" aria-hidden="true"><svg viewBox="0 0 340 230">'
            '<path class="lead hills" pathLength="1" d="M0 96c40-16 70-20 110-8s70 10 110-6 80-14 120 0"/>'
            '<path class="frame trail" pathLength="1" d="M70 226c40-24 70-30 60-58s-60-28-30-54 70-14 90-26"/>'
            '<path class="lead" pathLength="1" d="M262 214V92"/>'
            '<path class="pane gold" style="--i:0" d="M262 104h52l12 12-12 12h-52z"/>'
            '<path class="pane sage" style="--i:1" d="M262 140h-52l-12 12 12 12h52z"/>'
            '<path class="lead" pathLength="1" d="M262 104h52l12 12-12 12h-52M262 140h-52l-12 12 12 12h52"/>'
            '<path class="sill" d="M246 214h32v6h-32z"/>'
            '</svg></div>')


def path_graphic():
    """Three-step path for the fees page: consultation, sessions, change."""
    steps = [("Free", "20-minute consultation"), ("$100", "per 50–60 minute session"), ("Lasting change", "transformation, not simply relief")]
    nodes = "".join(f'<li style="--i:{i}"><span class="dot"></span><b>{a}</b><small>{b}</small></li>' for i, (a, b) in enumerate(steps))
    return f'<div class="path-graphic" aria-label="How counseling begins"><div class="wrap"><div class="path-line"><span></span></div><ol>{nodes}</ol></div></div>'


def contact_card():
    return f'''<aside class="contact-card" aria-label="Contact details">
      <a href="{TEL}">{ICONS["phone"]}<span><small>Call</small>{PHONE}</span></a>
      <a href="mailto:{EMAIL}">{ICONS["mail"]}<span><small>Email</small>{EMAIL}</span></a>
      <div>{ICONS["pin"]}<span><small>Office</small>Upper floor, 32 N Front Street<br>Yakima, WA 98901</span></div>
    </aside>'''


def icon_cards(items, cls=""):
    cards = "".join(f'<article class="dist">{ICONS[ic]}<h3>{t}</h3><p>{d}</p></article>' for ic, t, d in items)
    return f'<div class="dist-grid swipe {cls}">{cards}</div>'


def give_block(tint=True):
    return f"""<section class="section{' tint' if tint else ''}">
  <div class="wrap split">
    <div><h2>Support the ministry</h2></div>
    <div>
      <p class="lede">The center is a ministry of Saint Andrew's Presbyterian Church. Gifts help sustain its work of bringing God's Word to hurting people in Yakima.</p>
      <div class="actions" style="margin-top:1.5rem"><a class="btn btn-ghost" href="{GIVE}">Give to the center</a></div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- VETTED LISTS (from the current church-site page)
L_DEP = ["Clinical depression and mood disorders", "Anxiety and panic disorders", "Seasonal depression (SAD)", "Post-partum depression",
         "Social anxiety and phobias", "Obsessive-compulsive patterns", "Anxiety after frightening or painful events", "Fear and worry management"]
L_TRANS = ["Job loss and career changes", "Retirement adjustments", "Empty nest syndrome", "Moving and relocation stress",
           "Health crises and chronic illness", "Financial hardship and debt", "Death of spouse or family member", "Major life disappointments"]
L_ADDICT = ["Substance abuse (alcohol, drugs)", "Sexual addiction and pornography", "Gambling and financial addiction", "Food addiction and eating disorders",
            "Technology and social media addiction", "Anger and rage patterns", "Lying and deception habits", "Work addiction and perfectionism"]
L_MAR = ["Pre-marital counseling and preparation", "Communication skills and conflict resolution", "Sexual intimacy and purity issues", "Infidelity recovery and rebuilding trust",
         "Blended family dynamics", "In-law and extended family conflicts", "Separation and divorce recovery", "Single adult relationship concerns"]
L_FAM = ["Child discipline and behavioral issues", "Teenage rebellion and communication", "Adoption and foster care challenges", "Sibling rivalry and family dynamics",
         "Single parenting struggles", "Blended family integration", "Adult children relationships", "Grandparenting guidance"]
L_SPIRIT = ["Doubt and faith crises", "Spiritual dryness and disconnection", "Legalism and performance-based faith", "Spiritual disciplines",
            "Church hurt and disappointment", "Backsliding and spiritual restoration", "Calling and purpose questions", "Suffering and theodicy issues", "Recovering from harsh or controlling church experiences"]

PHILOSOPHY = """<p>Scripture is both our source and our system; the foundation that informs our understanding and the framework that guides our methodology. We don't just use Bible verses, we use biblical categories to understand your struggles and biblical solutions to address them.</p>
<p>Our goal extends beyond symptom relief to worldview formation and heart transformation, helping you see and respond to life through God's eyes rather than the world's categories.</p>"""


def what_is(home=False):
    link = f'<div class="link-row">{link_card("biblical-counseling.html", "book", "Learn more", "Biblical counseling")}{link_card("faq.html", "chat", "Have questions?", "Read the FAQs")}</div>' if home else ""
    head = 'What is biblical counseling?' if home else 'In short'
    cells = [("check", "What it is", "Personal ministry of God's Word: honest conversation, prayer, and practical homework, shaped by Scripture rather than psychological techniques."),
             ("not", "What it isn't", "Licensed therapy. We don't provide psychotherapy or mental health diagnosis, and sessions aren't billed to insurance."),
             ("people", "Who it's for", "Christians from any church, and anyone willing to engage with Scripture's wisdom for their struggles."),
             ("compass", "Where it leads", "Transformation, not simply relief: a changed heart and a life ordered under Christ's lordship.")]
    grid = "".join(f'<div class="wi-cell">{ICONS[ic]}<h3>{t}</h3><p>{d}</p></div>' for ic, t, d in cells)
    return f'''<section class="section sage" id="what">
  <div class="wrap wi">
    <div class="wi-intro">
      <h2>{head}</h2>
      <p class="lede">Biblical counseling is personal ministry of God's Word. A trained counselor helps you understand what you're facing and respond to it through Scripture, with Christ at the center.</p>
      {link}
    </div>
    <div class="wi-grid">{grid}</div>
  </div>
</section>'''


def philosophy_cards():
    return f'''<div class="ff">
      <div class="ff-card">
        {ICONS["foundation"]}
        <h3>Foundation</h3><p class="ff-sub">Scripture informs our understanding.</p>
        <ul><li>God's Word speaks with authority and sufficiency to all of life's challenges.</li><li>We use biblical categories (the heart, sin, suffering, and grace) to understand your struggles.</li><li>Scripture interprets everything, including our own experiences.</li></ul>
      </div>
      <div class="ff-card">
        {ICONS["framework"]}
        <h3>Framework</h3><p class="ff-sub">Scripture guides our methodology.</p>
        <ul><li>We address root issues at the level of the heart, not just surface behaviors.</li><li>We counsel struggles rooted in sin and struggles rooted in suffering differently.</li><li>Change happens through the ordinary means of grace: God's Word, prayer, and community.</li></ul>
      </div>
    </div>'''


def link_card(href, ic, small, label, extra=""):
    return f'<a class="ask-link" href="{href}"{extra}>{ICONS[ic]}<span><small>{small}</small>{label}</span><span class="arr">{ARROW}</span></a>'


def tag_card(ic, title, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<article class="tag-card"><div class="tc-head">{ICONS[ic]}<h3>{title}</h3></div><ul class="topic-list">{lis}</ul></article>'


def mini_list(title, items):
    return f'<details class="mini" open><summary><h3>{title}</h3>{CHEV}</summary><div class="answer"><div class="answer-in"><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div></div></details>'


pages = {}

# ---------------------------------------------------------------- HOME
verse = "The purpose in a man's heart is like deep water, but a man of understanding will draw it out."
verse_html = " ".join(f'<span class="w">{w}</span>' for w in verse.split())
org = {
    "@context": "https://schema.org", "@type": "ProfessionalService",
    "name": "Yakima Center for Biblical Counseling", "url": DOMAIN,
    "telephone": "+1-509-731-4772", "email": EMAIL,
    "address": {"@type": "PostalAddress", "streetAddress": "32 N Front Street, Upper Floor",
                "addressLocality": "Yakima", "addressRegion": "WA", "postalCode": "98901", "addressCountry": "US"},
    "areaServed": "Yakima, Washington",
    "description": "Biblical counseling for individuals, couples, and families. A ministry of Saint Andrew's Presbyterian Church.",
    "priceRange": "$100 per session; free initial consultation",
}
pages["index.html"] = (
    "Biblical & Christian Counseling in Yakima, WA | Yakima Center for Biblical Counseling",
    "Biblical counseling in Yakima for marriages, men, families, anxiety, and depression. The sufficiency of God's Word applied to your actual struggles. Free 20-minute consultation.",
    f'''<section class="hero">
  <div class="hero-glow"></div>
  <div class="wrap">
    <div>
      <p class="kicker">{TAGLINE}</p>
      <h1><span class="line"><span>Truth that</span></span><span class="line"><span>transforms.</span></span></h1>
      <p class="lede">Marriage falling apart. Kids rebelling. Depression settling in like fog and indwelling sin you just can't seem to defeat. Life has a way of serving up challenges that leave us scrambling for answers. At YCBC we don't offer quick fixes or shallow optimism, we offer something better: the sufficiency, authority and wisdom of God's Word applied to your actual struggles.</p>
      <div class="actions"><a class="btn btn-primary" {BOOK_ATTR}>Book a free consultation</a><a class="tel" href="{TEL}">or call <b>{PHONE}</b></a></div>
    </div>
    <figure class="hero-photo"><div class="bevel"><img src="assets/bible.jpg" alt="An open Bible" width="960" height="1200"></div></figure>
  </div>
</section>

<section class="section" id="help">
  <div class="wrap">
    <div class="section-head">
      <h2>How we help</h2>
      <p class="lede">Biblical counseling in Yakima for individuals, couples, and families.</p>
    </div>
    <div class="tiles">
      <a class="tile" href="marriage.html">{ICONS["marriage"]}<h3>Marriage</h3><p>Conflict, communication, infidelity, intimacy, blended families, and pre-marital counseling.</p><span class="go">{ARROW}</span></a>
      <a class="tile" href="anxiety.html">{ICONS["anxiety"]}<h3>Anxiety, worry &amp; stress</h3><p>Fear, panic, worry, and the depression that so often comes with them.</p><span class="go">{ARROW}</span></a>
      <a class="tile" href="men.html">{ICONS["men"]}<h3>Counseling for men</h3><p>Pornography, anger, discipline, and the weight of leading a family well.</p><span class="go">{ARROW}</span></a>
      <a class="tile" href="family.html">{ICONS["family"]}<h3>Family &amp; parenting</h3><p>Discipline, teenage rebellion, adoption and foster care, and relationships with adult children.</p><span class="go">{ARROW}</span></a>
    </div>
    <div class="also-wrap">
      <div class="also-head"><h3 class="also-h">We also walk with people through</h3>{link_card("contact.html", "chat", "Not listed?", "Just ask")}</div>
      <div class="also-grid">
        {tag_card("turn", "Life transitions", L_TRANS)}
        {tag_card("chain", "Addiction &amp; habitual sin", L_ADDICT)}
        {tag_card("flame", "Spiritual growth", L_SPIRIT)}
      </div>
    </div>
  </div>
</section>

{what_is(home=True)}

<section class="scene" data-scene="words" aria-label="Proverbs 20:5">
  <div class="stage"><div class="wrap">
    <blockquote style="margin:0"><p class="words">{verse_html}</p><cite>Proverbs 20:5</cite></blockquote>
  </div></div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Our philosophy</h2></div>
    {philosophy_cards()}
    <div class="link-row">{link_card("biblical-counseling.html", "book", "Our approach", "More about biblical counseling")}</div>
  </div>
</section>

<section class="section tint">
  <div class="wrap">
    <div class="section-head"><h2>What to expect</h2></div>
    <ol class="steps timeline">
      <li><h3>A free consultation</h3><p>All new clients begin with a free 20-minute initial consultation to understand your concerns, discuss our approach, answer your questions, and see whether we're a good fit.</p></li>
      <li><h3>Weekly sessions</h3><p>Sessions run 50–60 minutes, in person or by secure video, and are $100. Most people meet weekly. <a href="fees.html">Sessions &amp; fees</a></p></li>
      <li><h3>Lasting change</h3><p>Early sessions focus on understanding your story and establishing biblical hope. Later sessions apply Scripture to your struggle, then send you forward with encouragement.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap person">
    <div class="bevel"><img src="assets/david.jpg" alt="David Jamison, director of the Yakima Center for Biblical Counseling" width="960" height="1200" loading="lazy"></div>
    <div>
      <h2>Meet the counselor</h2>
      <p class="creds">David Jamison, MA in Counseling, Westminster Theological Seminary</p>
      <p>With several years of counseling experience specializing in individual and marriage counseling, David integrates his pastoral heart with his commitment to the sufficiency of God's Word for genuine life transformation.</p>
      <div class="link-row">{link_card("about.html", "people", "Meet the counselor", "More about David")}</div>
    </div>
  </div>
</section>



{cta()}''',
    f'<script type="application/ld+json">{json.dumps(org)}</script>',
)

# ---------------------------------------------------------------- MARRIAGE
marriage_faq = [
    ("What if my spouse won't come?", "Come anyway. God often begins changing a marriage by changing one person. You'll learn to love your spouse faithfully whether or not they join you, and many reluctant spouses come later."),
    ("Do you offer pre-marital counseling?", "Yes. We work through expectations, communication, conflict, finances, intimacy, and what Scripture says marriage is for, so you build on the right foundation from the start."),
    ("Can we meet virtually?", "Yes. Virtual sessions are conducted via the secure client portal and follow the same format, duration, and fees as in-person sessions."),
    ("What if there's abuse in our marriage?", "Tell us right away. Safety comes first. Joint counseling isn't appropriate where there is abuse, and we'll help you find the right protection and support, including your church's leaders and, where needed, the authorities."),
]
pages["marriage.html"] = (
    "Christian Marriage Counseling in Yakima, WA | YCBC",
    "Biblical marriage counseling in Yakima for couples facing conflict, broken trust, or distance, and pre-marital counseling. Free 20-minute initial consultation.",
    page_hero("Christian marriage counseling in Yakima",
              "Constant conflict. Cold distance. Trust that's been broken. We don't offer quick fixes or shallow optimism for your marriage. We offer the wisdom of God's Word applied to your actual struggles.",
              ("index.html#help", "How we help"), facts=True, icon="marriage") +
    concerns("Marriage and relationship challenges", L_MAR) + scene_marriage() +
    points("How we help couples", "Most marriage conflict isn't really about the dishes or the budget. It's about the heart.", [
        ("Root issues, not just surface behaviors", "We explore the heart-level dynamics, your deepest desires, fears, and worship, that drive the patterns in your marriage.", "“What causes quarrels and what causes fights among you? Is it not this, that your passions are at war within you?” James 4:1"),
        ("Sin and suffering, rightly distinguished", "Some of what you're facing calls for confession and change. Some calls for comfort. Usually it's both, and we counsel each differently.", ""),
        ("Change between sessions", "Expect homework: Scripture, prayer, and new rhythms of speaking, listening, repenting, and forgiving that carry into everyday life.", ""),
    ]) +
    faq(marriage_faq) + cross("marriage.html") + cta(),
    faq_jsonld(marriage_faq),
)

# ---------------------------------------------------------------- ANXIETY
anx_faq = [
    ("Does struggling with anxiety mean my faith is weak?", "No. Scripture is full of faithful people who were afraid, overwhelmed, and downcast. Your struggle is an invitation to bring your fears to God, not proof that He has given up on you."),
    ("I take medication. Should I stop?", "No. Please don't change any medication without talking to your doctor. You're welcome here whether or not you take medication, and we're glad to work alongside your physician."),
    ("Is this therapy?", "No. We apply Scripture to life's challenges rather than psychological techniques. Our counselors are not licensed mental health professionals and do not provide psychotherapy or mental health diagnosis."),
    ("What if I'm in crisis right now?", "For immediate safety concerns, call 911 or the Suicide & Crisis Lifeline (988). We provide spiritual guidance, not emergency mental health services."),
]
pages["anxiety.html"] = (
    "Biblical Counseling for Anxiety, Worry & Stress in Yakima | YCBC",
    "Christian counseling in Yakima for anxiety, worry, stress, fear, and depression, grounded in God's Word. Free 20-minute initial consultation.",
    page_hero("Biblical counseling for anxiety, worry &amp; stress",
              "Depression settling in like fog. Worry that won't let go. Scripture speaks to fear and sorrow with more honesty than you might expect, and it speaks to the whole person.",
              ("index.html#help", "How we help"), facts=True, icon="anxiety") +
    concerns("Depression and anxiety", L_DEP) + scene_anxiety() +
    points("How we help with anxiety and depression", "", [
        ("Body and soul", "Anxiety and depression affect the whole person, body and soul. We take your experience seriously and care for you as a whole person, not a set of symptoms.", ""),
        ("What you're carrying", "Fear always has an object. Together we'll explore what you're afraid of losing, what you're trying to control, and where you're looking for security.", ""),
        ("Moving toward Christ", "Suffering calls for moving toward Christ, mourning with Him, and maturing through trials. You'll learn to bring specific fears to God and take the next faithful step.", "“Do not be anxious about anything, but in everything by prayer and supplication with thanksgiving let your requests be made known to God.” Philippians 4:6"),
    ]) +
    faq(anx_faq) + cross("anxiety.html") + cta(),
    faq_jsonld(anx_faq),
)

# ---------------------------------------------------------------- MEN
men_faq = [
    ("I've tried to quit porn many times. Why would this be different?", "Willpower alone rarely holds, because the problem runs deeper than behavior. We'll get to the root, build real accountability, and fight from grace rather than shame. Change takes time, but it's real."),
    ("Will you tell my wife or my pastor?", "Not without your permission. Confidentiality has biblical and legal limits, mainly safety concerns and legal requirements, which our consent form explains. Bringing others in, when it helps, is something we decide together."),
    ("I'm not sure I even need counseling.", "That's what the free 20-minute consultation is for. No pressure. If you don't need us, we'll tell you."),
    ("Do you counsel women and couples too?", "Yes. We serve men, women, couples, and families. We just know that many men assume counseling isn't for them, and we want them to know it is."),
]
pages["men.html"] = (
    "Biblical Counseling for Men in Yakima, WA | YCBC",
    "Christian counseling for men in Yakima: pornography, anger, marriage, discipline, and leading your family, grounded in Scripture. Free 20-minute initial consultation.",
    page_hero("Biblical counseling for men",
              "Indwelling sin you just can't seem to defeat. Anger that scares your kids. A marriage gone cold. Many men carry these things for years without saying them out loud. You don't have to.",
              ("index.html#help", "How we help"), facts=True, icon="men") +
    concerns("Men come to us about",
             ["Sexual sin and pornography", "Anger and rage patterns", "A struggling marriage", "Leading their family well",
              "Discipline, drift, and wasted time", "Work addiction and perfectionism", "Isolation and no real friends", "Fatherhood"]) + scene_men() +
    points("What to expect", "Straight talk, grounded in Scripture. Not a lecture, and not a pat on the back.", [
        ("Honest conversation", "You can say the real thing here. Nothing you bring will shock us, and you won't be talked down to.", ""),
        ("Root issues", "Lust, anger, and drift are usually symptoms. We go after the heart: what you love, what you fear, and what you worship.", ""),
        ("A plan and real accountability", "Expect homework and follow-through. With your permission, we'll bring trusted men from your church alongside you.", ""),
        ("Grace that changes you", "Real change flows from what Christ has accomplished for you, not from willpower and effort. The gospel doesn't excuse sin; it gives you the power to fight it.", "“For the grace of God has appeared… training us to renounce ungodliness and worldly passions.” Titus 2:11–12"),
    ], note="<strong>We have a particular burden for men.</strong> Many never thought counseling was for them. We want them to know it is.") +
    faq(men_faq) + cross("men.html") + cta("Take the first step.", "All new clients begin with a free, confidential 20-minute consultation. No pressure, and no obligation."),
    faq_jsonld(men_faq),
)

# ---------------------------------------------------------------- FAMILY
fam_faq = [
    ("Do you counsel children and teens?", "Yes, when parents want us to. Because parents shape the home, we'll usually involve you along the way. Tell us about your family in the free consultation and we'll talk through what makes sense."),
    ("My spouse and I don't agree on parenting. Can we still come?", "Yes. It's one of the most common reasons parents come, and getting on the same page is often the most important first step."),
    ("Can you help with an adult child?", "Yes. Parenting changes when children grow up, and so do the heartaches. We help parents navigate strained relationships, prodigals, and boundaries with adult children."),
]
pages["family.html"] = (
    "Christian Family & Parenting Counseling in Yakima, WA | YCBC",
    "Biblical counseling for families and parents in Yakima: discipline, teenage rebellion, blended families, adoption and foster care. Free 20-minute initial consultation.",
    page_hero("Christian family &amp; parenting counseling",
              "Kids rebelling. Parents divided. A home that feels more like a battlefield than a refuge. God's Word speaks to the whole household, and there's hope for yours.",
              ("index.html#help", "How we help"), facts=True, icon="family") +
    concerns("Family and parenting issues", L_FAM) + scene_family() +
    points("How we help families", "", [
        ("Parents shape the home", "We counsel parents, children, and teens. Because parents set the tone of a household, we'll usually involve you, even when it's your child we're counseling.", ""),
        ("Hearts, not just behavior", "Rewards and consequences have their place, but real change happens at the level of the heart, for children and parents alike.", "“Fathers, do not provoke your children to anger, but bring them up in the discipline and instruction of the Lord.” Ephesians 6:4"),
        ("A plan for your home", "Expect clear, workable next steps: how to talk, how to correct, how to repair, and how to keep going when it's hard.", ""),
    ]) +
    faq(fam_faq) + cross("family.html") + cta(),
    faq_jsonld(fam_faq),
)

# ---------------------------------------------------------------- APPROACH
pages["biblical-counseling.html"] = (
    "What Is Biblical Counseling? | Yakima Center for Biblical Counseling",
    "What biblical counseling is, how it differs from therapy, and our philosophy, commitments, and distinctives. Biblical counseling in Yakima, WA.",
    page_hero("What is biblical counseling?", TAGLINE, variant="ph-center", top=window_graphic()) +
    f'''{what_is()}
<section class="section">
  <div class="wrap split">
    <div><h2>Biblical counseling and therapy</h2></div>
    <div>
      <p class="lede">We apply Scripture to life's challenges rather than psychological techniques. Our counselors are trained in biblical counseling methodology, not licensed as mental health professionals.</p>
      <p>Our goal is transformation, not simply relief. Rather than managing symptoms, we go to the heart: what you love, fear, and worship, and to Christ, who changes people from the inside out.</p>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap">
    <div class="section-head"><h2>Our philosophy</h2></div>
    {philosophy_cards()}
    <div class="ff-body">
      {PHILOSOPHY}
      <blockquote class="pull"><p>All Scripture is breathed out by God and profitable for teaching, for reproof, for correction, and for training in righteousness, that the man of God may be complete, equipped for every good work.</p><cite>2 Timothy 3:16–17</cite></blockquote>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Our commitments</h2><p class="lede">Five commitments that hold up everything we do.</p></div>
    <ul class="pillars swipe"><li><span class="pillar-cap"></span><h3>Scripture-driven</h3><p>God's Word defines everything about our counseling. We believe the Bible speaks with authority and sufficiency to all of life's challenges, providing both the lens to understand your struggles and the resources to address them.</p></li><li><span class="pillar-cap"></span><h3>Heart-focused</h3><p>We deal with the real issues, not just surface behaviors. Our goal is transformation of the inner person: your thoughts, desires, beliefs, and motives. Expect deep work that doesn't settle for quick fixes or shallow optimism.</p></li><li><span class="pillar-cap"></span><h3>Christ-centered</h3><p>All lasting change flows from the gospel of Jesus Christ. He has made us more than conquerors. Not through techniques or formulas, but through knowing Christ and being transformed by Him. The gospel reshapes everything.</p></li><li><span class="pillar-cap"></span><h3>Wisdom-guided</h3><p>No two situations are identical. We apply Scripture's permanent principles with discernment to your unique circumstances, pursuing what's truly loving and helpful for you. No cookie-cutter solutions or formulas.</p></li><li><span class="pillar-cap"></span><h3>Church-connected</h3><p>Biblical counseling works best when integrated into the local church, not separated from it. We're an aid to your church, not a replacement. With your permission, we coordinate with pastors to ensure consistent biblical care.</p></li></ul>
  </div>
</section>''' + scene_approach() + f'''
<section class="section sage">
  <div class="wrap">
    <div class="section-head"><h2>Our distinctives</h2><p class="lede">What sets YCBC apart.</p></div>
    <div class="dist-grid swipe"><article class="dist">{ICONS["book"]}<h3>Theologically grounded care</h3><p class="dist-sum">Seminary-level training in theology and biblical interpretation, so Scripture is handled rightly.</p><details class="dist-more"><summary><span class="o">Read more</span><span class="c">Show less</span>{CHEV}</summary><div class="answer"><div class="answer-in"><p>Our counselor brings seminary-level training in theology and biblical interpretation. This isn't just good intentions, it's rigorous theological grounding that equips us to handle Scripture rightly and apply it to life's complexity.</p></div></div></details></article><article class="dist">{ICONS["paths"]}<h3>Tailored to specific issues</h3><p class="dist-sum">We counsel struggles rooted in sin and struggles rooted in suffering differently.</p><details class="dist-more"><summary><span class="o">Read more</span><span class="c">Show less</span>{CHEV}</summary><div class="answer"><div class="answer-in"><p>We distinguish between struggles rooted primarily in sin and those rooted primarily in suffering, counseling each differently. Sin requires confession, confrontation, conformity to Christ, and commitment to change. Suffering calls for moving toward Christ, mourning with Him, maturing through trials, and eventually ministering comfort to others.</p></div></div></details></article><article class="dist">{ICONS["church"]}<h3>Church-integrated ministry</h3><p class="dist-sum">We work alongside your pastors and elders, never in place of them.</p><details class="dist-more"><summary><span class="o">Read more</span><span class="c">Show less</span>{CHEV}</summary><div class="answer"><div class="answer-in"><p>YCBC is part of the local church. With your permission, we coordinate with your pastors to ensure consistent care. When conflicts arise between our guidance and your church leadership, we defer to your elders or conclude counseling. We believe transformation happens through the ordinary means of grace (God's Word, prayer, sacraments, and community) pursued together, not in isolation.</p></div></div></details></article><article class="dist">{ICONS["compass"]}<h3>Whole-life transformation</h3><p class="dist-sum">Not coping strategies, but a whole life ordered under Christ's lordship.</p><details class="dist-more"><summary><span class="o">Read more</span><span class="c">Show less</span>{CHEV}</summary><div class="answer"><div class="answer-in"><p>We don't just address symptoms or offer coping strategies. We help you develop a comprehensive Christian worldview, cultivate spiritual disciplines (including Scripture memory, meditation, and prayer), and order your entire life under Christ's lordship. The goal is Christlikeness and participation in His mission.</p></div></div></details></article><article class="dist">{ICONS["door"]}<h3>Conviction with openness</h3><p class="dist-sum">Clear convictions, gladly serving believers across denominational lines.</p><details class="dist-more"><summary><span class="o">Read more</span><span class="c">Show less</span>{CHEV}</summary><div class="answer"><div class="answer-in"><p>We hold clear theological convictions while serving believers across denominational lines. God's Word is for Christians of all stripes. Likewise, while we're grounded in Scripture's authority we also recognize God's good gifts through common grace, including the real benefits that medicine and science can provide. This means we can appreciate medical interventions while maintaining that Scripture interprets everything and that ultimate transformation comes through Christ alone.</p></div></div></details></article><article class="dist dist-cta"><h3>See it for yourself</h3><p class="dist-sum">All new clients begin with a free 20-minute consultation, with no cost and no commitment.</p><a class="btn btn-gold" {BOOK_ATTR}>Book a free consultation</a></article></div>
  </div>
</section>''' + cta(),
)

# ---------------------------------------------------------------- FEES
pages["fees.html"] = (
    "Sessions & Fees | Yakima Center for Biblical Counseling",
    "Biblical counseling in Yakima: free 20-minute initial consultation, $100 per 50–60 minute session, in person or virtual. Reduced rates for partner churches.",
    page_hero("Sessions &amp; fees", "Our counselors have invested years in theological training and biblical counseling methodology. This fee reflects that preparation and ensures we can provide consistent, quality care.",
              variant="ph-wide", below=path_graphic()) +
    f'''<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What to expect</h2></div>
    {icon_cards([
        ("chat", "Initial consultation", "All new clients begin with a free 20-minute initial consultation. It allows us to understand your concerns, discuss our biblical counseling approach, answer your questions, and determine if our services are a good fit for your needs."),
        ("clock", "Sessions", "Sessions typically run 50–60 minutes. We'll start by understanding your situation, then work together to apply Scripture's wisdom to your specific challenges. Most people meet weekly, though we adjust based on your needs."),
        ("screen", "Virtual counseling", "Virtual sessions are conducted via the client portal, a secure and confidential environment, and follow the same format, duration, and fees as in-person sessions. All you need is a private space, a reliable internet connection, and a device with a camera and microphone."),
        ("hand", "Financial considerations", "If the fee presents a genuine hardship, please talk with us. We believe God's people should be able to access biblical guidance when they need it most."),
        ("card", "Insurance", "Because biblical counseling is religious ministry rather than licensed therapy, insurance doesn't cover sessions."),
        ("church", "Partner churches", "Members of churches that partner with the center receive reduced session rates. <a href='churches.html'>Learn about partnerships</a>."),
    ], "even")}
  </div>
</section>''' + cta(),
)

# ---------------------------------------------------------------- ABOUT
pages["about.html"] = (
    "Meet the Counselor: David Jamison | Yakima Center for Biblical Counseling",
    "Meet David Jamison, director of the Yakima Center for Biblical Counseling. MA in Counseling, Westminster Theological Seminary.",
    f'''<section class="page-hero ph-person">
  <div class="wrap">
    <div class="bevel"><img src="assets/david.jpg" alt="David Jamison" width="960" height="1200"></div>
    <div class="ph-main">
      <p class="crumb">Meet the counselor</p>
      <h1>David Jamison</h1>
      <p class="lede">Director of Discipleship and Counseling at Saint Andrew's Presbyterian Church, with several years of experience in individual and marriage counseling.</p>
      <ul class="cred-list">
        <li>{ICONS["book"]}<span>MA in Counseling, Westminster Theological Seminary</span></li>
        <li>{ICONS["people"]}<span>Individuals, couples, and families</span></li>
        <li>{ICONS["church"]}<span>Ruling elder, Saint Andrew's Presbyterian Church</span></li>
      </ul>
      <div class="actions"><a class="btn btn-primary" {BOOK_ATTR}>Book a free consultation with David</a></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div><h2>About David</h2></div>
    <div class="prose-lg">
      <p>David holds a Master of Arts in Counseling from Westminster Theological Seminary and has also pursued graduate theological study at Redemption Seminary. With several years of counseling experience specializing in individual and marriage counseling, he serves as Director of Discipleship and Counseling at Saint Andrew's, integrating his pastoral heart with his commitment to the sufficiency of God's Word for genuine life transformation.</p>
      <p>David counsels individuals and couples facing challenges ranging from anxiety, anger, and relational difficulties to complex issues like suicidal ideation and scrupulosity. His approach centers on utilizing Scripture to help believers walk more faithfully with Christ, believing that God's Word provides both the framework for understanding life's struggles and the divine resources for change. Additionally, his ministerial and theological training equips him to serve believers across denominational lines with both biblical depth and pastoral care.</p>
      <p>David and his wife, Lauren, have two young sons. In his spare time David likes to read, play games, and spend time with friends.</p>
    </div>
  </div>
</section>''' + cta(),
)

# ---------------------------------------------------------------- CHURCHES
pages["churches.html"] = (
    "Ministry Partnerships for Churches | Yakima Center for Biblical Counseling",
    "Pastors and churches in the Yakima Valley: partner with YCBC for trusted biblical counseling referrals, reduced member rates, and care under your elders' oversight.",
    page_hero("For pastors &amp; churches", "Most pastors don't have the hours for long-term counseling. A ministry partnership gives your congregation a trusted place for biblical care, under your oversight.", actions=PARTNER_ACTIONS, aside=hub_graphic()) +
    f'''<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What a partnership can look like</h2><p class="lede">Every church is different, so every partnership is shaped around your congregation. Most include some of the following.</p></div>
    {icon_cards([
        ("arrow", "A trusted referral", "When someone in your care needs more time than you can give, you know exactly where to send them, and that they'll receive counsel grounded in Scripture."),
        ("tag", "Reduced member rates", "Members of partner churches receive reduced session fees, so cost is less of a barrier for your people."),
        ("church", "Coordination with your elders", "With the counselee's permission, we keep you informed and coordinate care. When conflicts arise, we defer to your elders or conclude counseling."),
        ("people", "Strengthening your church's care", "Counseling is meant to send people back into the life of the church: its preaching, sacraments, and fellowship. We're an aid to your church, not a replacement."),
        ("book", "Equipping your people", "We're glad to talk about ways to help your leaders and members grow in caring for one another with God's Word."),
        ("layers", "Levels that fit", "Partnerships come in several levels to fit churches of different sizes and needs."),
    ], "even")}
    <p class="note">We serve churches across denominational lines that share a commitment to the authority and sufficiency of Scripture.</p>
  </div>
</section>
<!-- PASTOR ENDORSEMENT: uncomment and fill in once you have a quote and permission.
<section class="section tint endorse">
  <div class="wrap">
    <blockquote><p>“Quote from a partner pastor goes here.”</p><cite><b>Pastor's name</b>Church name, Yakima</cite></blockquote>
  </div>
</section>
-->''' + cta("Let's talk about your church.", "We'll walk through what a ministry partnership could look like for your congregation.", actions=PARTNER_ACTIONS),
)

# ---------------------------------------------------------------- FAQ
gen_faq = [
    ("What makes biblical counseling different from other types of counseling?",
     """<ul class="faq-list"><li><b>Divine wisdom for life's complexities.</b> Scripture provides God's own perspective on your struggles, offering unchanging truth and reliable guidance that transcends human insight and cultural trends.</li>
<li><b>Heart transformation, not just relief or management.</b> We believe God's Word has power to create real change at the deepest level, transforming the desires, beliefs, and loves that shape your life.</li>
<li><b>Addressing root issues.</b> Rather than managing symptoms, we explore the heart-level dynamics (your deepest desires, fears, and worship) that drive patterns in your life.</li>
<li><b>Living from gospel truth.</b> Real change flows from understanding and embracing what Christ has accomplished for you, not from trying to improve yourself through willpower and effort.</li>
<li><b>Connected to your church community.</b> Biblical counseling strengthens your relationships within the body of Christ, fostering growth that continues beyond counseling sessions.</li></ul>"""),
    ("What makes biblical counseling different from therapy?", "We apply Scripture to life's challenges rather than psychological techniques. Our counselors are trained in biblical counseling methodology, not licensed as mental health professionals."),
    ("What does the counseling process look like?", """<p>Counseling unfolds in phases. Early sessions (2–4) focus on understanding your story and establishing biblical hope. Middle sessions involve interpreting your problem biblically and developing strategies for lasting change. Final sessions review what you've learned and send you forward with encouragement.</p>
<p>Each session includes prayer, homework review, focused work on your issue, and planning next steps. Between sessions, expect homework: Scripture memory, reading, prayer practices, or developing rhythms that support lasting change. We believe transformation happens through the ordinary means of grace (God's Word, prayer, and community) so our counseling deepens your engagement with these, rather than replacing them.</p>"""),
    ("How long does this take?", "Depends on the situation. Some find significant help in a handful of sessions. Others benefit from longer-term guidance. We'll work together to determine what serves you best."),
    ("Do I need to be a church member?", "Not at all. We're here to serve anyone willing to engage with Scripture's wisdom for their struggles."),
    ("Is this really confidential?", "Yes, with biblical and legal limits. Our consent form explains specific situations where confidentiality might be broken, mainly safety concerns and legal requirements."),
    ("Are your counselors actually qualified?", "Our counselors have extensive training in biblical counseling and theology. They're not state-licensed therapists, they're trained ministers of God's Word who specialize in applying Scripture to life's challenges."),
    ("What does it cost?", "The initial 20-minute consultation is free. Sessions are $100. Members of partner churches receive reduced rates, and if the fee presents a genuine hardship, please talk with us."),
    ("Do you take insurance?", "No. Because biblical counseling is religious ministry rather than licensed therapy, insurance doesn't cover sessions."),
    ("Can we meet virtually?", "Yes. Virtual sessions are conducted via the secure client portal and follow the same format, duration, and fees as in-person sessions."),
]
pages["faq.html"] = (
    "FAQs | Yakima Center for Biblical Counseling",
    "Answers about biblical counseling in Yakima: how it differs from therapy, the counseling process, confidentiality, cost, insurance, and virtual sessions.",
    page_hero("Questions, answered", "If you don't see your question here, call or email. We're glad to help.", actions="", top=lamp_graphic(), variant="ph-gfx",
              aside=f'''<nav class="jump" aria-label="Jump to a topic"><p>Jump to</p><a href="#about-bc">{ICONS["book"]}<span>About biblical counseling</span></a><a href="#process">{ICONS["clock"]}<span>The counseling process</span></a><a href="#practical">{ICONS["card"]}<span>Cost and practical details</span></a></nav>''') +
    faq_groups([("about-bc", "About biblical counseling", gen_faq[0:2] + gen_faq[6:7]),
                ("process", "The counseling process", gen_faq[2:6]),
                ("practical", "Cost and practical details", gen_faq[7:10])]) + cta(),
    faq_jsonld(gen_faq),
)

# ---------------------------------------------------------------- CONTACT
pages["contact.html"] = (
    "Contact & Book a Free Consultation | Yakima Center for Biblical Counseling",
    "Book a free 20-minute consultation with the Yakima Center for Biblical Counseling, or call (509) 731-4772. 32 N Front Street, Yakima, WA.",
    page_hero("Let's talk.", "All new clients begin with a free 20-minute initial consultation. Pick a time on the calendar below, or call or email and we'll get back to you.", actions="", top=door_graphic(), variant="ph-gfx", aside=contact_card()) +
    f"""<section class="section contact-first">
  <div class="wrap split">
    <div>
      <h2>Schedule an appointment</h2>
      <ol class="mini-steps"><li><b>Pick a time</b> for your free 20-minute consultation.</li><li><b>Talk it through</b> with David in person at our downtown office, or by video if you prefer.</li><li><b>Decide together</b> whether to begin regular sessions.</li></ol>
      <p class="note"><strong>Crisis resources.</strong> For immediate safety concerns, call 911 or the Suicide &amp; Crisis Lifeline (988). We provide spiritual guidance, not emergency mental health services.</p>
      <blockquote class="pull"><p>For the word of God is living and active, sharper than any two-edged sword, piercing to the division of soul and of spirit, of joints and of marrow, and discerning the thoughts and intentions of the heart.</p><cite>Hebrews 4:12</cite></blockquote>
    </div>
    <div>
      <div class="booking-frame"><iframe title="Carepatron Online Booking" src="{BOOK}&e=i" loading="lazy"></iframe></div>
      <p class="small" style="margin-top:1rem;color:var(--ink-soft)">Calendar not loading? <a {BOOK_ATTR}>Open it in a new tab</a>.</p>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="wrap map-wrap">
    <div>
      <h2>Finding us</h2>
      <p class="lede" style="margin-top:1.25rem">Our office is on the upper floor of 32 N Front Street, in downtown Yakima.</p>
      <div class="actions" style="margin-top:1.75rem"><a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&destination=32+N+Front+St,+Yakima,+WA+98901" target="_blank" rel="noopener">Get directions</a></div>
    </div>
    <div class="map-frame"><iframe title="Map to our office at 32 N Front Street, Yakima" src="https://maps.google.com/maps?q=32+N+Front+St,+Yakima,+WA+98901&z=16&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>""" + give_block(tint=False),
)

# ---------------------------------------------------------------- PRIVACY
pages["privacy.html"] = (
    "Privacy Policy | Yakima Center for Biblical Counseling",
    "How the Yakima Center for Biblical Counseling handles information on this website.",
    page_hero("Privacy policy", "Last updated November 2026.") +
    f"""<section class="section"><div class="wrap"><div class="prose">
  <h2>What this site collects</h2>
  <p>This website doesn't ask you to create an account or submit forms. If you call or email us, we receive the information you choose to share.</p>
  <h2>Booking and client records</h2>
  <p>Appointments and client records are handled through Carepatron, a secure practice-management platform. Information you enter there is governed by Carepatron's privacy policy and by the consent form you receive before counseling begins.</p>
  <h2>Analytics and advertising</h2>
  <p>We may use tools such as Google Analytics and Google Ads to understand how visitors find and use this site. These tools use cookies and collect general information like pages visited and the device used. They don't tell us who you are. You can limit this through your browser settings or at adssettings.google.com.</p>
  <h2>Maps</h2>
  <p>Our Contact page shows an embedded Google Map. Google may set cookies when the map loads, under Google's own privacy policy.</p>
  <h2>What we don't do</h2>
  <p>We don't sell or share your information with anyone for marketing.</p>
  <h2>Questions</h2>
  <p>Contact us at <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
</div></div></section>""",
)


# ---------------------------------------------------------------- 404
pages["404.html"] = (
    "Page not found | Yakima Center for Biblical Counseling",
    "Page not found.",
    page_hero("We can't find that page.", "It may have moved. Try the home page, or call us and we'll help you find what you need.", variant="ph-center", top=path_404_graphic()),
)

os.makedirs(OUT, exist_ok=True)
for fn, (title, desc, body, *extra) in pages.items():
    with open(os.path.join(OUT, fn), "w") as f:
        f.write(page(fn, title, desc, body, extra[0] if extra else ""))
urls = "".join(f"<url><loc>{DOMAIN}/{'' if fn=='index.html' else fn.replace('.html','')}</loc></url>" for fn in pages if fn != "404.html")
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
print("built", len(pages), "pages")
