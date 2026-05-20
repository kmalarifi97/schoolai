#!/usr/bin/env python3
"""Generate the library website: one self-contained Arabic-RTL static page
that combines the book pages, concept videos, projects, and PhET playground.

Reads structure.json, concept_library_beats_v2.json, concepts/INDEX.json,
and the 6 project JSONs. Emits site/index.html with video src as relative
paths to the existing mp4s (no copying). Re-run anytime to resync.
"""
import json, glob, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = ROOT / "scripts"
OUT = ROOT / "site"
OUT.mkdir(exist_ok=True)

struct = json.load(open(S / "structure.json"))
v2 = json.load(open(S / "concept_library_beats_v2.json"))
idx = {c["slug"]: c for c in json.load(open(S / "concepts/INDEX.json"))["concepts"]}

PHET = {
    "skatepark": "https://phet.colorado.edu/en/simulations/energy-skate-park-basics",
    "collisionlab": "https://phet.colorado.edu/en/simulations/collision-lab",
    "orbitlab": "https://phet.colorado.edu/en/simulations/gravity-and-orbits",
    "balancerig": "https://phet.colorado.edu/en/simulations/balancing-act",
    "springdrop": "https://phet.colorado.edu/en/simulations/masses-and-springs",
    "thermalbudget": "https://phet.colorado.edu/en/simulations/energy-forms-and-changes",
}

def esc(x): return html.escape(str(x), quote=True)

def vid(p):
    """relative path from site/ to an mp4, or '' if missing"""
    f = sorted(glob.glob(str(p)))
    return ("../" + str(pathlib.Path(f[0]).relative_to(ROOT))) if f else ""

# ---- concepts grouped by chapter/lesson ----
concepts = {}
for c in v2["concepts"]:
    slug = c["slug"]
    nn = idx.get(slug, {})
    d = nn.get("dir", "")
    mp4 = vid(S / "concepts" / pathlib.Path(d).name / f"{slug}_full_voiced_subs.mp4") if d else ""
    handoff = c["beats"][-1]["text"] if c.get("beats") else ""
    concepts.setdefault(c["chapter"], {}).setdefault(c["lesson"], []).append({
        "slug": slug, "ar": c["concept_ar"], "en": c["concept_en"],
        "pages": nn.get("book_pages", ""), "mp4": mp4, "status": c["status"],
        "handoff": handoff,
    })

# ---- projects ----
projects = []
for pj in sorted(glob.glob(str(S / "projects/*/*.json"))):
    d = json.load(open(pj))
    slug = d["slug"]
    mp4 = vid(pathlib.Path(pj).parent / f"{slug}_full_voiced_subs.mp4")
    projects.append({
        "slug": slug, "ar": d.get("project_ar", ""), "en": d.get("project_en", ""),
        "persona": d.get("persona", ""), "sim": d.get("phet_sim", "").split("(")[0].strip(),
        "phet": PHET.get(slug, "https://phet.colorado.edu"),
        "combines": d.get("concepts_combined", []), "mp4": mp4,
    })

lessons_meta = {}
for ch in struct["chapters"]:
    for ls in ch.get("lessons", []):
        lessons_meta[ls["id"]] = ls
book = struct["book"]

# ---------------- HTML ----------------
def card(c):
    pg = f'<span class="chip">ص {esc(c["pages"])}</span>' if c["pages"] else ""
    if c["mp4"]:
        play = f'<button class="play" data-src="{esc(c["mp4"])}" data-title="{esc(c["ar"])}" aria-label="تشغيل">▶</button>'
        cls = "card"
    else:
        play = '<span class="ext">مؤرشَف خارجيًّا</span>'
        cls = "card card--ext"
    quote = f'<p class="handoff">{esc(c["handoff"])}</p>' if c["handoff"] else ""
    return f'''<article class="{cls}">
      <div class="card__top">{play}<div class="card__id">{esc(c["en"])}</div></div>
      <h4>{esc(c["ar"])}</h4>{quote}
      <div class="card__foot">{pg}</div>
    </article>'''

chapters_html = []
for ch in struct["chapters"]:
    cid = ch["id"]
    if cid not in concepts:
        continue
    les_html = []
    for lid, items in sorted(concepts[cid].items()):
        lm = lessons_meta.get(lid, {})
        cards = "".join(card(c) for c in items)
        les_html.append(f'''<div class="lesson">
          <div class="lesson__head">
            <span class="lesson__id">{esc(lid)}</span>
            <div><h3>{esc(lm.get("title_ar",""))}</h3>
            <span class="lesson__en">{esc(lm.get("title_en",""))} · ص {esc(lm.get("start_page",""))}–{esc(lm.get("end_page",""))}</span></div>
          </div>
          <div class="grid">{cards}</div>
        </div>''')
    chapters_html.append(f'''<section class="chapter reveal" id="ch{cid}">
      <header class="chapter__h">
        <span class="chapter__n">{esc(["","١","٢","٣","٤","٥","٦"][cid])}</span>
        <div><h2>{esc(ch["title_ar"])}</h2><span class="chapter__en">{esc(ch["title_en"])}</span></div>
      </header>
      {"".join(les_html)}
    </section>''')

# project cards
def pcard(p):
    chips = "".join(f'<span class="chip chip--c">{esc(x.split("(")[0].split("_",1)[-1])}</span>'
                     for x in p["combines"])
    play = (f'<button class="play play--lg" data-src="{esc(p["mp4"])}" data-title="{esc(p["ar"])}">▶ القصّة</button>'
            if p["mp4"] else "")
    return f'''<article class="pcard reveal">
      <div class="pcard__sim">{esc(p["sim"])}</div>
      <h3>{esc(p["ar"])}</h3>
      <p class="pcard__persona">{esc(p["persona"])}</p>
      <div class="pcard__chips">{chips}</div>
      <div class="pcard__act">
        {play}
        <a class="phet" href="{esc(p["phet"])}" target="_blank" rel="noopener">افتح مِحاكاة PhET ↗</a>
      </div>
    </article>'''

projects_html = "".join(pcard(p) for p in projects)
nconc = sum(len(i) for ch in concepts.values() for i in ch.values())

DOC = f'''<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>مكتبة الفيزياء ٢ — شاهد الفكرة، ثمّ حُلّ بنفسك</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;600;700&family=Noto+Naskh+Arabic:wght@400;500;700&family=Amiri:ital@0;1&display=swap" rel="stylesheet">
<style>
:root{{--void:#000;--ink:#ECE6DA;--dim:#8C8576;--line:rgba(236,230,218,.10);
--amber:#E2A86A;--amber-2:#caa06a;--blue:#6E97B8;--card:#0a0a0a;}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{background:var(--void);color:var(--ink);font-family:"Noto Naskh Arabic",serif;
line-height:1.85;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
body::before{{content:"";position:fixed;inset:0;z-index:1;pointer-events:none;opacity:.035;
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E")}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 28px;position:relative;z-index:2}}
h1,h2,h3,h4,.chapter__n,.lesson__id{{font-family:"Reem Kufi",sans-serif;font-weight:600;line-height:1.3}}
/* hero */
.hero{{min-height:96vh;display:flex;flex-direction:column;justify-content:center;
padding:120px 0 80px;position:relative}}
.hero::after{{content:"";position:absolute;inset-inline:0;bottom:14vh;height:1px;
background:linear-gradient(90deg,transparent,var(--line) 30%,var(--line) 70%,transparent)}}
.kicker{{font-family:"Reem Kufi";letter-spacing:.35em;color:var(--amber);font-size:.78rem;
margin-bottom:30px;opacity:0;animation:up .9s .1s forwards}}
.hero h1{{font-size:clamp(2.8rem,8vw,6.2rem);font-weight:700;letter-spacing:-.01em;
opacity:0;animation:up 1s .25s forwards}}
.hero h1 .am{{font-family:"Amiri",serif;font-style:italic;color:var(--amber)}}
.hero p{{max-width:48ch;margin-top:30px;color:var(--dim);font-size:1.12rem;
opacity:0;animation:up 1s .5s forwards}}
.hero .meta{{margin-top:46px;display:flex;gap:34px;flex-wrap:wrap;color:var(--dim);
font-size:.85rem;font-family:"Reem Kufi";letter-spacing:.04em;
opacity:0;animation:up 1s .7s forwards}}
.hero .meta b{{color:var(--ink);font-size:1.5rem;display:block;font-weight:700}}
@keyframes up{{from{{opacity:0;transform:translateY(26px)}}to{{opacity:1;transform:none}}}}
/* chapter */
.chapter{{padding:88px 0;border-top:1px solid var(--line)}}
.chapter__h{{display:flex;align-items:flex-start;gap:26px;margin-bottom:54px}}
.chapter__n{{font-size:3.2rem;color:var(--amber);line-height:1;opacity:.85;
font-variant-numeric:tabular-nums}}
.chapter__h h2{{font-size:clamp(1.8rem,4vw,2.7rem)}}
.chapter__en{{color:var(--dim);font-family:"Reem Kufi";letter-spacing:.16em;
font-size:.74rem;text-transform:uppercase}}
.lesson{{margin:0 0 56px}}
.lesson__head{{display:flex;align-items:center;gap:18px;margin:0 0 26px;
padding-bottom:14px;border-bottom:1px solid var(--line)}}
.lesson__id{{font-size:.92rem;color:var(--void);background:var(--amber);
padding:5px 12px;border-radius:2px;letter-spacing:.05em}}
.lesson__head h3{{font-size:1.4rem}}
.lesson__en{{color:var(--dim);font-size:.78rem;font-family:"Reem Kufi";letter-spacing:.05em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:18px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:4px;
padding:22px;display:flex;flex-direction:column;gap:13px;min-height:208px;
transition:border-color .4s,transform .4s,background .4s}}
.card:hover{{border-color:rgba(226,168,106,.5);transform:translateY(-3px);background:#0d0c0a}}
.card--ext{{opacity:.5}}
.card__top{{display:flex;align-items:center;justify-content:space-between;gap:12px}}
.card__id{{font-family:"Reem Kufi";font-size:.66rem;letter-spacing:.12em;
text-transform:uppercase;color:var(--dim);text-align:left}}
.card h4{{font-size:1.3rem;color:var(--ink)}}
.handoff{{font-family:"Amiri",serif;font-style:italic;color:var(--amber-2);
font-size:.95rem;line-height:1.7;opacity:.82;flex:1}}
.card__foot{{display:flex;gap:8px;align-items:center}}
.chip{{font-family:"Reem Kufi";font-size:.68rem;letter-spacing:.05em;color:var(--dim);
border:1px solid var(--line);padding:3px 10px;border-radius:999px}}
.chip--c{{color:var(--amber-2);border-color:rgba(226,168,106,.28)}}
.ext{{font-family:"Reem Kufi";font-size:.7rem;color:var(--dim)}}
.play{{width:46px;height:46px;border-radius:50%;border:1px solid rgba(226,168,106,.45);
background:transparent;color:var(--amber);font-size:.8rem;cursor:pointer;
display:grid;place-items:center;transition:all .35s;flex:none}}
.play:hover{{background:var(--amber);color:var(--void);transform:scale(1.08)}}
.play--lg{{width:auto;height:auto;border-radius:999px;padding:11px 22px;
font-family:"Reem Kufi";font-size:.84rem;letter-spacing:.04em}}
/* projects */
.lab{{padding:96px 0;border-top:1px solid var(--line)}}
.lab__h{{text-align:center;margin-bottom:60px}}
.lab__h h2{{font-size:clamp(2rem,5vw,3rem)}}
.lab__h .am{{font-family:"Amiri",serif;font-style:italic;color:var(--amber)}}
.lab__h p{{color:var(--dim);margin-top:14px}}
.plist{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}}
.pcard{{background:linear-gradient(180deg,#0c0b09,#070707);border:1px solid var(--line);
border-radius:5px;padding:30px;display:flex;flex-direction:column;gap:14px;
transition:border-color .4s,transform .4s}}
.pcard:hover{{border-color:rgba(110,151,184,.45);transform:translateY(-3px)}}
.pcard__sim{{font-family:"Reem Kufi";font-size:.7rem;letter-spacing:.14em;
text-transform:uppercase;color:var(--blue)}}
.pcard h3{{font-size:1.42rem;line-height:1.45}}
.pcard__persona{{color:var(--dim);font-size:.92rem}}
.pcard__chips{{display:flex;flex-wrap:wrap;gap:7px;margin-top:4px}}
.pcard__act{{display:flex;gap:12px;align-items:center;margin-top:14px;flex-wrap:wrap}}
.phet{{font-family:"Reem Kufi";font-size:.84rem;letter-spacing:.03em;color:var(--blue);
border:1px solid rgba(110,151,184,.45);padding:11px 20px;border-radius:999px;
text-decoration:none;transition:all .35s}}
.phet:hover{{background:var(--blue);color:var(--void)}}
footer{{border-top:1px solid var(--line);padding:60px 0 90px;color:var(--dim);
font-size:.84rem;text-align:center;font-family:"Reem Kufi";letter-spacing:.04em}}
footer .am{{font-family:"Amiri",serif;font-style:italic;color:var(--amber);font-size:1rem}}
/* lightbox */
.lb{{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.94);
display:none;place-items:center;padding:30px;backdrop-filter:blur(6px)}}
.lb.on{{display:grid}}
.lb__in{{width:min(960px,94vw)}}
.lb__t{{font-family:"Reem Kufi";color:var(--amber);margin-bottom:14px;font-size:1.1rem}}
.lb video{{width:100%;border-radius:5px;background:#000;display:block}}
.lb__x{{position:absolute;top:24px;left:30px;background:none;border:1px solid var(--line);
color:var(--ink);width:44px;height:44px;border-radius:50%;cursor:pointer;font-size:1.1rem}}
.lb__x:hover{{border-color:var(--amber);color:var(--amber)}}
.reveal{{opacity:0;transform:translateY(34px);transition:opacity 1s,transform 1s}}
.reveal.in{{opacity:1;transform:none}}
@media(max-width:640px){{.chapter__h{{gap:16px}}.wrap{{padding:0 18px}}}}
</style></head><body>
<div class="wrap">
  <header class="hero">
    <div class="kicker">الفيزياء ٢ · نظام المسارات · السنة الثانية</div>
    <h1>شاهِد الفكرة.<br>ثمّ <span class="am">حُلَّ بنفسك.</span></h1>
    <p>مكتبةٌ تُشعِل الفهم ثمّ تتنحّى. كلُّ مفهومٍ مقطعٌ قصيرٌ يبني الحدس ويتوقّف قبل المعادلة — لأنّ الحلّ مهمّتُك أنت. ثمّ ستةُ مشاريع تجمع المفاهيم معًا على مِحاكيات PhET.</p>
    <div class="meta">
      <span><b>{nconc}</b>مقطع مفهوم</span>
      <span><b>{len(projects)}</b>مشروع تطبيقي</span>
      <span><b>٦</b>فصول · {esc(book["total_pdf_pages"])} صفحة</span>
      <span><b>AR</b>ترجمة فصحى مدمجة</span>
    </div>
  </header>

  {"".join(chapters_html)}

  <section class="lab reveal" id="lab">
    <div class="lab__h">
      <h2>المختبر — <span class="am">مشاريع PhET</span></h2>
      <p>شخصيّةٌ تحاول، فتتعثّر — حتى تبني نموذجًا. تنبّأ قبل أن تضغط «تشغيل».</p>
    </div>
    <div class="plist">{projects_html}</div>
  </section>

  <footer>
    {esc(book["title_ar"])} — {esc(book["publisher"])} · {esc(book["edition"])}<br>
    <span class="am">الصمتُ محتوى. شاهِد، ثمّ فكِّر.</span>
  </footer>
</div>

<div class="lb" id="lb">
  <button class="lb__x" id="lbx" aria-label="إغلاق">✕</button>
  <div class="lb__in"><div class="lb__t" id="lbt"></div>
  <video id="lbv" controls preload="metadata"></video></div>
</div>
<script>
const lb=document.getElementById('lb'),lv=document.getElementById('lbv'),lt=document.getElementById('lbt');
function close(){{lb.classList.remove('on');lv.pause();lv.removeAttribute('src');lv.load();}}
document.querySelectorAll('.play').forEach(b=>b.addEventListener('click',()=>{{
  lv.src=b.dataset.src;lt.textContent=b.dataset.title;lb.classList.add('on');lv.play().catch(()=>{{}});
}}));
document.getElementById('lbx').addEventListener('click',close);
lb.addEventListener('click',e=>{{if(e.target===lb)close();}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')close();}});
const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target);}}}}),{{threshold:.08}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body></html>'''

(OUT / "index.html").write_text(DOC, encoding="utf-8")
print(f"site -> {OUT/'index.html'}  ({len(DOC)//1024} KB)  "
      f"concepts={nconc} projects={len(projects)} chapters={len(chapters_html)}")
