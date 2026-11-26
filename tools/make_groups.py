# python3 tools/make_groups.py   (run AFTER tools/make.py and BEFORE tools/update_home.py)
# Temple groups (tools/groups.json): several nearby temples shown as ONE card on the homepage.
# Clicking the card opens group-{slug}.html, which tells the group story and shows a small card for each temple.
# Each member temple keeps its own page (temple-{slug}.html); this script adds a "← group / next →" bar to it.
# A temple joins a group with  "group": "<group slug>"  in tools/new_temples.json.
import json, html, os, re
from urllib.parse import quote
T = os.path.dirname(os.path.abspath(__file__)) + '/'; R = os.path.dirname(T[:-1]) + '/'
G = json.load(open(T + 'groups.json'))
NEW = {e['slug']: e for e in json.load(open(T + 'new_temples.json'))}
def im(f, w): return 'https://wsrv.nl/?url=' + quote('https://www.angkorlens.com/' + f, safe='') + '&w=%d&q=75&output=jpg' % w
def esc(s): return html.escape(s)

for gs, g in G.items():
    mem = [m for m in g['members'] if m in NEW]
    gurl = f'/group-{gs}.html'
    # 1) "group / previous / next" bar on every member page
    for i, m in enumerate(mem):
        p = R + f'temple-{m}.html'; t = open(p).read()
        t = re.sub(r'<nav class="grpbar".*?</nav>\n?', '', t, flags=re.S)
        prv = mem[i - 1] if i > 0 else None; nxt = mem[i + 1] if i + 1 < len(mem) else None
        a = 'style="border:1px solid #d6cbb8;border-radius:999px;padding:6px 12px;text-decoration:none;font-size:14px;background:#fff"'
        bar = (f'<nav class="grpbar" style="display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px">'
               f'<a {a} href="{gurl}">← {esc(g["name"])} · {esc(g["km"])} ({i + 1}/{len(mem)})</a>'
               + (f'<a {a} href="/temple-{prv}.html">‹ {esc(NEW[prv]["name"])}</a>' if prv else '')
               + (f'<a {a} href="/temple-{nxt}.html">{esc(NEW[nxt]["name"])} ›</a>' if nxt else '') + '</nav>\n')
        t = t.replace('<figure class="ph hero-w">', bar + '<figure class="ph hero-w">', 1)
        crumb_old = '<a href="/temples.html">Temple guides</a> › '
        crumb_new = crumb_old + f'<a href="{gurl}">{esc(g["name"])}</a> › '
        if crumb_new not in t:
            t = t.replace(crumb_old, crumb_new, 1)
        open(p, 'w').write(t)
    # 2) the group page, built from the first member page so it has the same look, cookie bar and photo popup
    base = open(R + f'temple-{mem[0]}.html').read()
    base = re.sub(r'<div id="mapPayModal".*?</script>', '', base, count=1, flags=re.S)
    url = f'https://www.angkorlens.com/group-{gs}.html'
    desc = f'{g["name"]}: {len(mem)} Khmer linga temples photographed by Samnang Loy, with history in English and Khmer.'[:155]
    head = (f'<title>{esc(g["name"])} ({esc(g["km"])}) – Photos &amp; History | AngkorLens</title>\n'
            f'<meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico">\n'
            f'<meta property="og:title" content="{esc(g["name"])} – AngkorLens"><meta property="og:description" content="{esc(desc)}"><meta property="og:image" content="{im(g["cover"], 1200)}"><meta property="og:url" content="{url}"><meta property="og:type" content="article">\n')
    base = re.sub(r'<title>.*?<meta property="og:type" content="article">\n?', lambda _: head, base, count=1, flags=re.S)
    base = re.sub(r'<script type="application/ld\+json">.*?</script>', '', base, count=1, flags=re.S)
    # small north-south line drawing of the members (no outside map)
    pts = [(NEW[m]['gps']['lat'], NEW[m]['gps']['lon']) for m in mem if NEW[m].get('gps')]
    svg = ''
    if len(pts) == len(mem) and len(mem) > 1:
        la = [p[0] for p in pts]; lo = [p[1] for p in pts]
        sp = max(max(la) - min(la), max(lo) - min(lo)) or 1
        Hh = 60 + 70 * (len(mem) - 1)
        c = ''
        for k, (m, (y, x)) in enumerate(zip(mem, pts)):
            cy = 30 + (max(la) - y) / sp * (Hh - 60); cx = 150 + (x - (min(lo) + max(lo)) / 2) / sp * (Hh - 60)
            c += (f'<a href="/temple-{m}.html"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="#8A5A2B"/>'
                  f'<text x="{cx + 18:.0f}" y="{cy + 5:.0f}" font-size="14" fill="#221F1C">{esc(NEW[m]["name"])} · {esc(g["codes"].get(m, ""))}</text></a>')
        svg = (f'<figure style="margin:0 0 22px;background:#fff;border-radius:18px;padding:14px"><svg viewBox="0 0 520 {Hh}" width="100%" style="max-width:520px;display:block" role="img" aria-label="Order of the temples from north to south">'
               f'<text x="20" y="24" font-size="13" fill="#7A5A1E">N ↑</text>{c}</svg>'
               f'<figcaption style="color:#6b625a;font-size:13px">From north to south · ពីជើងទៅត្បូង</figcaption></figure>')
    cards = ''.join(
        f'<a class="gc" href="/temple-{m}.html"><img loading="lazy" src="{im(NEW[m]["i"][0], 600)}" alt="{esc(NEW[m]["name"])}">'
        f'<b>{k + 1}. {esc(NEW[m]["name"])}</b><span>{esc(NEW[m]["km"])} · {esc(g["codes"].get(m, ""))}</span></a>' for k, m in enumerate(mem))
    style = ('<style>.glist{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin:6px 0 24px}'
             '.gc{background:#fff;border-radius:16px;overflow:hidden;text-decoration:none;color:#221F1C}.gc img{width:100%;height:170px;object-fit:cover;display:block;background:#e8e0d2}'
             '.gc b{display:block;padding:10px 12px 0;font-family:Georgia,serif}.gc span{display:block;padding:2px 12px 12px;color:#7A5A1E;font-size:14px}.gc:hover b{color:#c8452c;text-decoration:underline}</style>')
    main = (f'<main>{style}<p class="crumb"><a href="/">Home</a> › <a href="/temples.html">Temple guides</a> › {esc(g["name"])}</p>\n'
            f'<h1>{esc(g["name"])}</h1><p class="km">{esc(g["km"])}</p><p class="sub">{esc(g["sub"])}</p>\n'
            f'<figure class="ph hero-w"><img class="hero" draggable="false" src="{im(g["cover"], 900)}" alt="{esc(g["name"])}, Cambodia"><span class="wm">© AngkorLens · Samnang Loy</span></figure>\n'
            f'<p class="by">Photographs by Samnang Loy · AngkorLens</p>\n'
            f'<h2 style="font-family:Georgia,serif">{len(mem)} temples · ប្រាសាទ {len(mem)}</h2><div class="glist">{cards}</div>\n'
            f'{svg}<section class="story">{g["h"]}</section>\n'
            + (f'<h2 style="font-family:Georgia,serif">On site · នៅនឹងកន្លែង</h2><div class="grid"><figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{im(g["sign"], 480)}" alt="Information sign of the {esc(g["name"])}"><span class="wm">© AngkorLens</span></figure></div>\n' if g.get('sign') else '')
            + '<a class="cta" href="/">← Explore all of AngkorLens</a>\n</main>')
    base = re.sub(r'<main>.*?</main>', lambda _: main, base, count=1, flags=re.S)
    open(R + f'group-{gs}.html', 'w').write(base)
    # 3) sitemap
    sm = open(R + 'sitemap.xml').read()
    if url not in sm:
        day = re.search(r'<lastmod>([^<]+)</lastmod>', sm).group(1)
        sm = sm.replace('</urlset>', f'  <url><loc>{url}</loc><lastmod>{day}</lastmod></url>\n</urlset>')
        open(R + 'sitemap.xml', 'w').write(sm)
    print('group page:', f'group-{gs}.html', len(mem), 'temples')
