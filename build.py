"""Build the SignalFeed site from src/*.json articles + the landing page. Run: python3 build.py"""
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
import hashlib
def ver(f): return hashlib.sha1((ROOT / f).read_bytes()).hexdigest()[:8]
BASE = "https://signalfeed.dev/"
UPWORK = "https://www.upwork.com/freelancers/~019a97d6c06c1b0e74"
EMAIL = "aaron.signalfeed@gmail.com"
GUIDES = [  # slug, short title, kind
    ("title-ii-pdf-guide.html", "ADA Title II and your PDFs", "Regulation"),
    ("public-universities-title-ii-pdfs.html", "Public universities and the 2027 Title II deadline", "Regulation"),
    ("state-agencies-title-ii-pdfs.html", "State agencies and the 2027 Title II deadline", "Regulation"),
    ("special-districts-title-ii-pdfs.html", "Special districts and the 2028 Title II deadline", "Regulation"),
    ("section-504-patient-pdfs.html", "HHS Section 504 and patient PDFs", "Regulation"),
    ("pdf-inventory-title-ii.html", "How to inventory your PDFs before Title II", "How-to"),
    ("accessible-word-to-pdf.html", "Word to accessible PDF, step by step", "How-to"),
    ("accessible-meeting-agendas.html", "Accessible meeting agendas and minutes", "How-to"),
    ("accessible-budget-tables.html", "Accessible budget tables", "How-to"),
    ("scanned-minutes-accessible.html", "Making scanned minutes accessible", "How-to"),
    ("verapdf-pdf-ua-errors.html", "veraPDF PDF/UA errors, explained", "How-to"),
    ("title-ii-accessibility-training.html", "ADA Title II training for staff", "Training"),
    ("pdf-remediation-before-after.html", "PDF remediation before and after", "Samples"),
    ("remediation-partners.html", "White-label remediation for agencies", "Partners"),
    ("online-store-accessibility-checklist.html", "Online store accessibility checklist", "Checklist"),
    ("title-ii-pdf-findings.html", "Title II PDF findings across five kinds of public entities", "Data"),
    ("title-ii-pdf-backlog-index.html", "Title II PDF Backlog Index: 657 US cities", "Data"),
    ("pdf-remediation-cost.html", "How much PDF remediation costs", "Data"),
    ("pdf-remediation-cost-estimator.html", "PDF remediation cost estimator", "Tool"),
    ("pdf-remediation-quote-check.html", "Checking a PDF remediation quote", "How-to"),
    ("tutoring-invoice-tracker-excel.html", "Tutoring sessions and invoices in Excel", "How-to"),
    ("local-government-website-platforms.html", "Website platforms of US cities and counties", "Data"),
    ("k12-district-platforms.html", "K-12 district website and board platforms", "Data"),
    ("pdf-backlog-sizing.html", "PDF backlog sizing for remediation bids", "Data"),
    ("mn-title-ii-pdf-readiness.html", "Minnesota Title II PDF readiness", "Data"),
    ("book-formatting-sample.html", "Ebook and paperback formatting sample", "Samples"),
]
for _s, _t in (("title-ii-pdf-backlog-counties.html", "Title II PDF Backlog Index: US counties"),
               ("title-ii-pdf-backlog-universities.html", "Title II PDF Backlog Index: public universities"),
               ("title-ii-pdf-backlog-state-government.html", "Title II PDF Backlog Index: state government websites"),
               ("title-ii-pdf-backlog-special-districts.html", "Title II PDF Backlog Index: special district websites")):
    if (ROOT / "src" / _s.replace(".html", ".json")).exists():  # appear only once the edition is published
        GUIDES.insert(next(i for i, g in enumerate(GUIDES) if g[0] == "title-ii-pdf-backlog-index.html") + 1, (_s, _t, "Data"))
LOGO = '''<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fb0ff"/><stop offset="1" stop-color="#6ff0d2"/></linearGradient></defs><rect x="1" y="1" width="30" height="30" rx="9" fill="none" stroke="url(#lg)" stroke-width="2"/><path d="M7 20c3-6 5-6 8 0s5 6 10-8" fill="none" stroke="url(#lg)" stroke-width="2.4" stroke-linecap="round"/></svg>'''

def head(title, desc, slug, extra="", og=None):
    og = og or slug.replace(".html", "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{BASE}{'' if slug == 'index.html' else slug}">
<meta property="og:site_name" content="SignalFeed.dev">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="{'website' if slug == 'index.html' else 'article'}">
<meta property="og:url" content="{BASE}{'' if slug == 'index.html' else slug}">
<meta property="og:image" content="{BASE}assets/og/{og}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(title)}: SignalFeed.dev card over a printing press">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{BASE}assets/og/{og}.jpg">
<meta name="theme-color" content="#05070d">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/site.css?v={ver('assets/site.css')}">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="./" aria-label="SignalFeed.dev home">{LOGO}<span>SignalFeed.dev</span></a>
<nav class="nav" aria-label="Main">
<a class="hide-sm" href="./#services">Services</a>
<a class="hide-sm" href="./#checker">Free checker</a>
<a class="hide-sm" href="./#guides">Guides</a>
<a class="hide-sm" href="jobs/">Job data</a>
<a class="btn btn-primary" href="mailto:{EMAIL}?subject=Free%202-page%20sample">Free sample</a>
</nav></div></header>
'''

FOOT = f'''<footer class="site-footer"><div class="wrap">
<div><a class="brand" href="./">{LOGO}<span>SignalFeed.dev</span></a><p>Document accessibility and clean data. Careful human review, honest reports.</p></div>
<nav aria-label="Footer">
<a href="./#services">Services</a><a href="./#checker">Free PDF checker</a><a href="./#guides">Guides</a><a href="jobs/">Job data</a>
<a href="{UPWORK}">Hire on Upwork</a><a href="accessibility.html">Accessibility</a><a href="mailto:{EMAIL}">Email</a><span>Hero footage: Everett Bumstead via Pexels</span>
</nav>
<p style="flex-basis:100%;margin:0">General information, not legal advice. We don&#39;t issue compliance certificates; we report exactly what was checked.</p>
</div></footer>
<script src="assets/fx.js?v={ver('assets/fx.js')}" defer></script>
</body>
</html>
'''

def article(a):
    kind = a.get("kind") or next((k for s, _, k in GUIDES if s == a["slug"]), "Guide")
    others = "".join(f'<li><a href="{s}">{html.escape(t)}</a></li>' for s, t, _ in GUIDES if s != a["slug"])
    return head(a["title"], a["description"], a["slug"], extra=a.get("head_extra", ""), og=a.get("og")) + f'''<main id="main">
<div class="article-head cine">
<video class="hero-video" id="heroVideo" autoplay muted loop playsinline preload="metadata" aria-hidden="true" poster="https://images.unsplash.com/photo-1461958508236-9a742665a0d5?w=1600&q=70&auto=format"><source src="https://videos.pexels.com/video-files/29906414/12837346_960_540_24fps.mp4" type="video/mp4"></video>
<canvas id="field" aria-hidden="true"></canvas>
<button class="vid-toggle" id="vidToggle" type="button" aria-label="Pause background video"><svg class="i-pause" viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="2.5" width="3" height="11" rx="1"/><rect x="9.5" y="2.5" width="3" height="11" rx="1"/></svg><svg class="i-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4c0 .6.7 1 1.2.6l8-5.2a.7.7 0 0 0 0-1.2l-8-5.2c-.5-.4-1.2 0-1.2.6z"/></svg></button>
<div class="wrap">
<p class="crumbs"><a href="./">SignalFeed.dev</a> / <a href="./#guides">Guides</a> / {kind}</p>
<h1>{a["h1"]}</h1>
<p class="article-meta">{kind} · Last reviewed November 2026 · Sources linked inline</p>
</div></div>
<div class="wrap article">
<article class="prose">
{a["body"]}
</article>
<aside class="aside" aria-label="Related">
<div class="card"><h2>Free tool</h2><p>Check any PDF for basic structural warning signs. It runs in your browser; nothing is uploaded.</p><a class="btn btn-ghost" href="./#checker">Open the checker</a></div>
<div class="card"><h2>More guides</h2><ul>{others}</ul></div>
</aside>
</div>
</main>
''' + FOOT

def index():
    checker = (ROOT / "src/checker-script.html").read_text()
    cards = "".join(f'<a class="card reveal" href="{s}"><span class="tag">{k}</span><h3>{html.escape(t)}</h3><span class="more">Read the guide →</span></a>' for s, t, k in GUIDES)
    ribbon = '<div class="ribbon" aria-hidden="true"><svg viewBox="0 0 1600 200" preserveAspectRatio="none"><path fill="none" stroke="#8fb0ff" stroke-opacity=".35" stroke-width="1.2"/><path fill="none" stroke="#6ff0d2" stroke-opacity=".3" stroke-width="1.2"/><path fill="none" stroke="#8fb0ff" stroke-opacity=".2" stroke-width="1"/></svg></div>'
    return head("SignalFeed.dev: Accessible PDFs, WCAG Audits and Clean Data",
                "SignalFeed.dev rebuilds public documents as accessible, tagged PDFs and web pages, audits websites against WCAG 2.2 AA, and cleans messy data. Free in-browser PDF checker and plain-English guides.",
                "index.html") + f'''<main id="main">
<section class="hero-x" aria-labelledby="hero-title">
<video class="hero-video" id="heroVideo" autoplay muted loop playsinline preload="auto" aria-hidden="true"
  poster="https://images.unsplash.com/photo-1461958508236-9a742665a0d5?w=1600&q=70&auto=format">
  <source src="https://videos.pexels.com/video-files/29906414/12837347_1280_720_24fps.mp4" type="video/mp4">
</video>
<canvas id="field" aria-hidden="true"></canvas>
<button class="vid-toggle" id="vidToggle" type="button" aria-label="Pause background video"><svg class="i-pause" viewBox="0 0 16 16" aria-hidden="true"><rect x="3.5" y="2.5" width="3" height="11" rx="1"/><rect x="9.5" y="2.5" width="3" height="11" rx="1"/></svg><svg class="i-play" viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 2.8v10.4c0 .6.7 1 1.2.6l8-5.2a.7.7 0 0 0 0-1.2l-8-5.2c-.5-.4-1.2 0-1.2.6z"/></svg></button>
<div class="scan" aria-hidden="true"></div>
<div class="hud" aria-hidden="true"><i></i>
<span class="tl mono"><span class="dot"></span>SignalFeed.dev // Document systems</span>
<span class="tr mono">Standards · WCAG 2.1 AA (Title II) · 2.2 AA (audits)</span>
<span class="bl mono">Checker · local only · 0 uploads</span>
<span class="br mono" id="utc">UTC --:--:--</span>
</div>
<div class="wrap">
<p class="eyebrow reveal">Document accessibility · WCAG 2.1 / 2.2 AA</p>
<h1 id="hero-title" class="reveal">Every document, <span class="grad">readable by everyone.</span></h1>
<p class="lede reveal">We rebuild agendas, notices, budgets, reports and patient handouts as tagged PDFs and accessible web pages, audit websites against WCAG, and clean the data behind them. Built for public bodies and online stores facing real deadlines.</p>
<div class="cta-row reveal"><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Free%202-page%20sample">Request a free 2-page sample</a><a class="btn btn-ghost" href="#checker">Check a PDF now</a></div><p class="email-alt">or email <span class="email-copy">{EMAIL}</span></p>
</div>

</section>

<div class="wrap"><div class="statbar reveal" role="list">
<div role="listitem"><b>Apr 26, 2027</b><span>ADA Title II date for governments serving 50,000+</span></div>
<div role="listitem"><b>Apr 26, 2028</b><span>Smaller governments and special districts</span></div>
<div role="listitem"><b>2 of 907</b><span>sampled city PDFs passed a PDF/UA-1 check</span></div>
<div role="listitem"><b>0 uploads</b><span>Our PDF checker runs entirely in your browser</span></div>
</div></div>


<section class="story" id="how-it-works" aria-labelledby="story-title">
<div class="story-sticky">
<div class="stage3d" aria-hidden="true">
<div class="laptop"><div class="lid"><div class="screen">
<div class="ui-bar"><i></i><i></i><i></i><b>SIGNALFEED // ANALYZE · agenda-2027-01-12.pdf</b></div>
<div class="ui">
<div class="doc">
<div class="sweep"></div>
<div class="ln h"></div><span class="chip" style="--i:0;left:8px;top:6px">H1</span><span class="outline" style="--i:0;left:12px;top:12px;width:72%;height:18px"></span>
<div class="ln"></div><div class="ln"></div><div class="ln s"></div><span class="chip b" style="--i:1;right:10px;top:34px">P</span>
<div class="tbl"><span class="th"></span><span class="th"></span><span class="th"></span><span></span><span></span><span></span><span></span><span></span><span></span></div><span class="chip" style="--i:2;right:10px;top:76px">TABLE · TH</span><span class="outline" style="--i:2;left:12px;top:80px;width:88%;height:42px"></span>
<div class="fig"></div><span class="chip b" style="--i:3;left:20px;top:132px">FIGURE · ALT</span>
<div class="ln"></div><div class="ln s"></div><span class="chip" style="--i:4;right:10px;bottom:16px">L · LI</span>
</div>
<div class="panel">
<span class="t">Verification</span>
<div class="row" style="--i:0">Structure tags <em>found</em></div>
<div class="row" style="--i:1">Language <em>en-US</em></div>
<div class="row" style="--i:2">Title <em>set</em></div>
<div class="row" style="--i:3">Headings <em>H1 → H2</em></div>
<div class="row" style="--i:4">Table headers <em>3 / 3</em></div>
<div class="row" style="--i:5">Alt text <em>1 / 1</em></div>
<div class="row" style="--i:6">Reading order <em class="r">manual ✓</em></div>
<div class="score">Report ready · manual checks listed</div>
</div>
</div>
</div></div><div class="base"></div></div>
</div>
<div>
<p class="eyebrow">How it works</p>
<h2 id="story-title" style="font-size:clamp(28px,3.4vw,44px);line-height:1.05;letter-spacing:-.03em;margin:8px 0 26px">From unreadable to checked and reported.</h2>
<ol class="captions">
<li class="on" data-step="0"><span class="k">01 · Intake</span><strong>Your document, opened up.</strong>We read the source PDF or Word file and map every element on every page.</li>
<li data-step="1"><span class="k">02 · Structure</span><strong>Every element tagged.</strong>Headings, paragraphs, lists, tables with header cells, figures with real descriptions, in the right reading order.</li>
<li data-step="2"><span class="k">03 · Verify</span><strong>Checked, then reported.</strong>Automated checks plus an AI-assisted WCAG checklist review. You get a report of exactly what passed.</li>
</ol>
</div>
</div>
</section>

<section class="block" id="services" aria-labelledby="svc-title">
{ribbon}
<div class="wrap">
<div class="section-head reveal"><p class="eyebrow">Services</p><h2 id="svc-title">From backlog to accessible, without the guesswork.</h2><p>Fixed quotes, a free sample first, and a report that says exactly what was checked and what wasn&#39;t.</p></div>
<div class="grid">
<div class="card reveal"><span class="num">01</span><h3>Accessible PDFs</h3><p>Documents rebuilt with real headings, reading order, table headers, alt text, title and language, as a tagged PDF plus an accessible web version.</p><p class="price">From $45 for 10 pages</p></div>
<div class="card reveal"><span class="num">02</span><h3>Website WCAG audits</h3><p>Automated axe-core scans plus scripted browser checks for what scanners miss: keyboard, focus, zoom and reflow, and forms (no screen-reader testing). One prioritized fix list.</p><p class="price">From $60 for 5 key pages</p></div>
<div class="card reveal"><span class="num">03</span><h3>Templates and clean data</h3><p>Word templates that export better PDFs by default, and messy spreadsheets deduplicated and standardized with a full change log.</p><p class="price">From $30</p></div>
</div>
</div>
</section>

<section class="block alt" id="checker" aria-labelledby="chk-title">
<div class="wrap split" style="align-items:start">
<div class="reveal"><p class="eyebrow">Free tool</p><h2 id="chk-title" style="font-size:clamp(30px,4vw,48px);line-height:1.05;letter-spacing:-.03em;margin:8px 0 14px">PDF accessibility quick check</h2>
<p class="lede" style="font-size:18px">Look for basic structural warning signs in seconds: missing tags, language, title, headings, alt text and table headers, and pages that may be scans. Your file is read by your own browser and never uploaded.</p>
<p class="note">These are basic signals, not a conformance test. Reading order, tag correctness and descriptions need a person and a screen reader.</p></div>
<div class="tool reveal">
<div class="drop">
<input type="file" id="file" accept="application/pdf,.pdf">
<label class="btn btn-primary" for="file">Choose a PDF</label>
<p class="status" id="status" role="status" aria-live="polite">No file chosen.</p>
</div>
<div id="results" class="result-wrap" aria-live="polite"></div>
</div>
</div>
</section>

<section class="block" aria-labelledby="how-title">
{ribbon}
<div class="wrap split">
<div class="reveal"><p class="eyebrow">How we work</p><h2 id="how-title" style="font-size:clamp(30px,4vw,48px);line-height:1.05;letter-spacing:-.03em;margin:8px 0 14px">Careful work, honestly reported.</h2>
<p class="lede" style="font-size:18px">We use AI-assisted tools, and a person checks every delivery before it goes out. We never sell overlays or &ldquo;compliance certificates&rdquo;.</p></div>
<ol class="steps reveal">
<li><strong>Free 2-page sample</strong>Send your hardest public document (no personal, student or medical information). Check our result in your own checker before you pay.</li>
<li><strong>Fixed quote</strong>Priced by pages and complexity, agreed up front.</li>
<li><strong>Rebuild and validate</strong>Every PDF is validated against PDF/UA-1 with veraPDF (you get the report), then reviewed against a WCAG checklist with AI-assisted tools.</li>
<li><strong>Clear report</strong>What passed, what needs your input, and anything we couldn&#39;t fix.</li>
</ol>
</div>
</section>

<section class="block alt" id="guides" aria-labelledby="g-title">
<div class="wrap">
<div class="section-head reveal"><p class="eyebrow">Guides</p><h2 id="g-title">Plain-English guides, with sources.</h2><p>Deadlines, exceptions and step-by-step fixes for the documents public bodies and clinics post most.</p></div>
<div class="grid">{cards}</div>
</div>
</section>

<section class="block" aria-labelledby="cta-title">
<div class="wrap"><div class="cta-card reveal" style="padding:44px">
<h2 id="cta-title" style="font-size:clamp(26px,3.4vw,40px);letter-spacing:-.02em">Have a backlog of PDFs?</h2>
<p style="font-size:18px;margin:10px 0 22px">Send one document and get two pages back, rebuilt and checked, free. Then decide.</p>
<div class="cta-row"><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Free%202-page%20sample">Email us a document</a><a class="btn btn-ghost" href="{UPWORK}">Hire us on Upwork</a></div><p class="email-alt">or email <span class="email-copy">{EMAIL}</span></p>
</div></div>
</section>
</main>
{checker.replace("class='bad'", "class='bad'").replace("<table>", "<table class='result-table'>")}
''' + FOOT

import readiness
for f in sorted((ROOT / "src").glob("*.json")):
    if f.name == "mn-readiness.json":
        continue
    a = json.loads(f.read_text())
    (ROOT / a["slug"]).write_text(article(a))
(ROOT / "index.html").write_text(index())
for a in readiness.pages(ROOT / "src/mn-readiness.json", EMAIL):
    (ROOT / a["slug"]).write_text(article(a))
print("built", len(list((ROOT / "src").glob("*.json"))), "articles + index")
# QA guard: refuse to finish if any page has an empty or placeholder link (caught a live bug on 2026-11-27).
import re as _re
_bad = []
for _p in ROOT.glob("*.html"):
    _t = _p.read_text()
    for _m in _re.finditer(r'href="(|#|None|\{[^}]*\})"', _t):
        _bad.append(f"{_p.name}: href={_m.group(1)!r}")
    for _u in _re.findall(r'href="([a-z0-9][a-z0-9\-/\.]*\.(?:html|csv|docx|pdf|xlsx))"', _t):
        if not (ROOT / _u).exists():
            _bad.append(f"{_p.name}: missing target {_u}")
if _bad:
    raise SystemExit("QA guard: empty/placeholder links found:\n  " + "\n  ".join(_bad[:20]))
print("QA guard: no empty links")
