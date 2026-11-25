# San Francisco hub + place pages. Run from make.py (uses CSS, LB, img, out, html, json, quote, S).
SF=json.load(open(S+'sf_places.json'))
_t=out['temples.html']; COOKIE=_t[_t.find('<script>/* Google tag'):_t.find('</script></head>')+9]
SFCSS='''.facts{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px}.facts span{background:#fff;border:1px solid #E6DCCB;border-radius:999px;padding:5px 12px;font-size:14px}
.look{background:#fff7e6;border-radius:14px;padding:12px 16px;margin-top:14px}.kmtxt{font-size:16px;line-height:1.9}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}.c{background:#fff;border-radius:16px;overflow:hidden;text-decoration:none;color:#221F1C;box-shadow:0 2px 10px rgba(0,0,0,.05)}
.c img{width:100%;height:170px;object-fit:cover;display:block;background:#e8e0d2}.c b{display:block;padding:10px 12px 0;font-family:Georgia,serif;font-size:17px}.c i{display:block;padding:0 12px;color:#7A5A1E;font-style:normal;font-size:14px}.c span{display:block;padding:2px 12px 12px;color:#6b625a;font-size:13px}'''
def head(title,desc,url,ogi,ld):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{ogi}"><meta property="og:url" content="{url}"><meta property="og:type" content="article">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script><style>{CSS}
{SFCSS}</style>{COOKIE}</head><body>
<header><a href="/">AngkorLens</a></header><main>'''
SF_URLS=['https://www.angkorlens.com/san-francisco.html']
for j,p in enumerate(SF):
    k=p['key']; n=p['name']; ims=[f"sf-{k}-{i}.jpg" for i in range(1,p['n']+1)]
    url=f"https://www.angkorlens.com/san-francisco-{p['slug']}.html"; SF_URLS.append(url)
    desc=(p['d'][0][:150].rsplit(' ',1)[0]+'…') if len(p['d'][0])>155 else p['d'][0]
    ogi=img(ims[0],1200)[0]
    ld={"@context":"https://schema.org","@type":"TouristAttraction","name":n,"alternateName":p['km'],"description":desc,"url":url,"image":ogi,
        "containedInPlace":{"@type":"City","name":"San Francisco","containedInPlace":{"@type":"State","name":"California"}}}
    facts=''.join(f'<span><strong>{html.escape(a)}:</strong> {html.escape(b)}</span>' for a,b in p['facts'])
    en=''.join(f'<p>{html.escape(x)}</p>' for x in p['d'])
    km=''.join(f'<p>{html.escape(x)}</p>' for x in p['dk'])
    thumbs=''.join(f'<figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{img(s0,480)[0]}" alt="{html.escape(n)}, San Francisco – photo {i+2}"><span class="wm">© AngkorLens</span></figure>' for i,s0 in enumerate(ims[1:]))
    others=[SF[(j+m)%len(SF)] for m in range(1,len(SF))]
    more=''.join(f'<a href="/san-francisco-{o["slug"]}.html">{html.escape(o["name"])}</a>' for o in others)
    maps='https://www.google.com/maps/search/?api=1&query='+quote(n+', San Francisco, CA')
    out[f"san-francisco-{p['slug']}.html"]=head(f"{n}, San Francisco ({p['km']}) – Photos | AngkorLens",desc,url,ogi,ld)+f'''
<p class="crumb"><a href="/">Home</a> › <a href="/san-francisco.html">San Francisco</a> › {html.escape(n)}</p>
<h1>{html.escape(n)}</h1><p class="km">{html.escape(p['km'])}</p><p class="sub">{html.escape(p['sub'])}</p>
<figure class="ph hero-w"><img class="hero" draggable="false" src="{img(ims[0],900)[0]}" alt="{html.escape(n)}, San Francisco"><span class="wm">© AngkorLens · Samnang Loy</span></figure>
<p class="by">Photographs by Samnang Loy · AngkorLens</p>
<div class="mapbox" style="margin:6px 0 18px;padding:12px 16px;background:#fff;border:1px solid #E6DCCB;border-radius:14px;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px"><span>📍 <strong>{html.escape(n)}</strong>, San Francisco, California</span><a href="{maps}" target="_blank" rel="noopener" style="display:inline-block;padding:7px 14px;border-radius:999px;background:#8A5A2B;color:#fff;text-decoration:none;font-weight:700;font-size:14px">Open in Google Maps · បើកផែនទី</a></div>
<section class="story"><div class="facts">{facts}</div>{en}<p class="look"><strong>Look closely:</strong> {html.escape(p['look'])}</p>
<hr><div class="kmtxt">{km}<p class="look"><strong>សូមសង្កេតមើល៖</strong> {html.escape(p['lk'])}</p></div></section>
<h2 style="font-family:Georgia,serif">More photos · រូបថតបន្ថែម</h2><p class="lockmsg">🔒 Tap any photo to see it full size or buy the original. · ចុចលើរូប ដើម្បីមើលទំហំធំ ឬទិញរូបដើម។</p><div class="grid">{thumbs}</div>
<a class="cta" href="/san-francisco.html">← All San Francisco places</a>
<h2 style="font-family:Georgia,serif;margin-top:34px">More in San Francisco</h2><nav class="more">{more}</nav>
</main><footer>© AngkorLens · Samnang Loy</footer>'''+LB+'</body></html>'
cards=''.join(f'<a class="c" href="/san-francisco-{p["slug"]}.html"><img loading="lazy" src="{img(f"sf-{p["key"]}-1.jpg",480)[0]}" alt="{html.escape(p["name"])}, San Francisco"><b>{html.escape(p["name"])}</b><i>{html.escape(p["km"])}</i><span>{html.escape(p["sub"])} · {p["n"]} photos</span></a>' for p in SF)
hd='Photographs of San Francisco by Samnang Loy: Golden Gate Bridge, Painted Ladies, Lombard Street, Chinatown, City Hall, Palace of Fine Arts and more, in English and Khmer.'
ld={"@context":"https://schema.org","@type":"CollectionPage","name":"San Francisco Through My Lens","description":hd,"url":SF_URLS[0],
    "hasPart":[{"@type":"TouristAttraction","name":p['name'],"url":f"https://www.angkorlens.com/san-francisco-{p['slug']}.html"} for p in SF]}
out['san-francisco.html']=head('San Francisco Through My Lens – Photos of 15 Places | AngkorLens',hd,SF_URLS[0],img('sf-goldengate-1.jpg',1200)[0],ld)+f'''
<style>main{{max-width:1500px}}.list{{grid-template-columns:repeat(4,1fr);gap:18px}}.c img{{height:auto;aspect-ratio:4/3}}.c b{{font-size:19px}}
@media(max-width:900px){{.list{{grid-template-columns:repeat(2,1fr);gap:12px}}.c b{{font-size:16px}}}}</style>
<p class="crumb"><a href="/">Home</a> › San Francisco</p>
<h1>San Francisco Through My Lens</h1><p class="km">សាន់ហ្វ្រាន់ស៊ីស្កូ តាមកែវថតរបស់ខ្ញុំ</p>
<p class="sub">{len(SF)} places in San Francisco, California, photographed by Samnang Loy. Tap a place to see its photos and story in English and Khmer.<br>ចុចលើកន្លែងណាមួយ ដើម្បីមើលរូបថត និងរឿងរ៉ាវជាភាសាអង់គ្លេស និងខ្មែរ។</p>
<div class="list">{cards}</div>
<a class="cta" href="/">← Back to AngkorLens</a></main><footer>© AngkorLens · Samnang Loy</footer></body></html>'''
