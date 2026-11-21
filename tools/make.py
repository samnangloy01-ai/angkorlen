import json,re,html,os
from urllib.parse import quote
# Run from anywhere:  python3 tools/make.py
# Reads tools/*.json, writes temple-*.html, temples.html and sitemap.xml into the repo root.
S=os.path.dirname(os.path.abspath(__file__))+'/'
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
d=json.load(open(S+'temples.json'))
def eng_name(t,s):
    s=s.strip()
    parts=[p.strip() for p in re.split(r'\s+[-–—]\s+',s)]
    if len(parts)>1 and re.search(r'(Century|Period|Possibly|Late|Early|\d)',parts[0]): name=parts[1]
    else: name=parts[0]
    return name.split(' / ')[0].strip()
def slug(n):
    n=re.sub(r'\(.*?\)','',n); n=n.replace('’',"").replace("'","")
    return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
def plain(h): 
    t=re.sub(r'<br\s*/?>',' ',h); t=re.sub(r'<[^>]+>','',t); return html.unescape(re.sub(r'\s+',' ',t)).strip()
def eng_desc(h):
    p=plain(h)
    sents=re.findall(r'[A-Z][^.!?]{40,}?[.!?]',p)
    for x in sents:
        if sum(c.isascii() for c in x)/len(x)>0.95 and not re.search(r'History|English|Khmer:',x[:20]): return x
    return ''
def img(src,w): 
    u='/'+src.lstrip('/'); return 'https://wsrv.nl/?url='+quote('https://www.angkorlens.com'+u,safe='')+'&w=%d&q=75&output=jpg'%w, u
pages={}
for x in d:
    n=eng_name(x['t'],x['s']); sl=slug(n)
    if not sl or not x['i']: continue
    if sl in pages and len(pages[sl]['h'])>=len(x['h']): continue
    x['name']=n; pages[sl]=x
COVER={'preah-khan-kampong-svay':'IMG_0018.JPG'}
EX=json.load(open(S+'extra.json'))
for key,slug_ in (('bakong','bakong-temple'),('banteaysrei','banteay-srei')):
    e=EX[key]
    facts=' · '.join(f'<strong>{html.escape(k)}:</strong> {html.escape(v)}' for k,v in e['f'])
    body=facts+'<br><br>'+'<br><br>'.join(html.escape(x) for x in e['d'])+'<br><br><strong>Look for:</strong> '+html.escape(e['l'])
    sub=next((v for k,v in e['f'] if k in('Where',)),'Cambodia')
    pages[slug_]={'t':e['km'],'s':sub,'name':e['t'],'h':body,'i':[f"sf-{key}-{i}.jpg" for i in range(1,e['n']+1)]}
NEW=json.load(open(S+'new_temples.json'))
for e in NEW:
    pages[e['slug']]={'t':e['km'],'s':e['sub'],'name':e['name'],'h':e['h'],'i':e['i'],'gps':e.get('gps')}
for k,c in COVER.items():
    if k in pages: pages[k]['i']=[c]+[i for i in pages[k]['i'] if i!=c]
LB='<style>.photo-membership-overlay{position:fixed;inset:0;z-index:10001;background:rgba(15,23,42,.72);backdrop-filter:blur(5px);display:flex;align-items:center;justify-content:center;padding:18px}.photo-membership-overlay.hidden{display:none}.photo-membership-card{width:min(560px,100%);max-height:92vh;overflow-y:auto;background:#fff;border:1px solid #e5e7eb;border-radius:28px;box-shadow:0 25px 80px rgba(0,0,0,.35);padding:28px}.photo-membership-top{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}.photo-membership-badge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border-radius:999px;background:#ecfeff;color:#0e7490;font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.photo-membership-close{border:0;background:transparent;color:#737373;font-size:30px;line-height:1;cursor:pointer;padding:2px 7px}.photo-membership-card h2{margin:12px 0 8px;color:#171717;font-size:25px;font-weight:800}.photo-membership-subtitle{margin:0;color:#525252;font-size:14px;line-height:1.6}.photo-membership-preview{margin:20px 0;border-radius:18px;overflow:hidden;background:#f5f5f5;position:relative}.photo-membership-preview img{width:100%;height:220px;object-fit:cover;display:block;filter:blur(3px);transform:scale(1.02);opacity:.72}.photo-membership-preview-lock{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.18)}.photo-membership-lock-circle{width:58px;height:58px;border-radius:50%;background:rgba(17,24,39,.86);color:#fff;display:flex;align-items:center;justify-content:center;font-size:22px}.photo-plan-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}.photo-plan{border:1px solid #e5e7eb;border-radius:18px;padding:18px;background:#fff}.photo-plan.yearly{border-color:#0891b2;box-shadow:0 5px 20px rgba(8,145,178,.10)}.photo-plan h3{margin:0;color:#171717;font-size:15px;font-weight:800}.photo-plan-price{margin:7px 0 12px;color:#0891b2;font-size:25px;font-weight:900}.photo-plan-price span{font-size:12px;color:#737373;font-weight:600}.photo-plan ul{margin:0;padding-left:18px;color:#525252;font-size:12px;line-height:1.75}.photo-pay-btn{width:100%;margin-top:14px;border:0;border-radius:12px;padding:11px 14px;background:#171717;color:#fff;font-size:12px;font-weight:800;letter-spacing:.04em;cursor:pointer}.photo-plan.yearly .photo-pay-btn{background:#0891b2}.photo-pay-btn:hover{opacity:.9}.photo-membership-note{margin:16px 0 0;text-align:center;color:#737373;font-size:11px;line-height:1.5}.photo-membership-note strong{color:#525252}@media(max-width:640px){.photo-membership-card{padding:20px;border-radius:22px}.photo-plan-grid{grid-template-columns:1fr}.photo-membership-preview img{height:180px}}.hidden{display:none!important}</style>\n    <div id="photoMembershipModal" class="photo-membership-overlay hidden" role="dialog" aria-modal="true" aria-labelledby="photoMembershipTitle">\n        <div class="photo-membership-card">\n            <div class="photo-membership-top">\n                <div>\n                    <span class="photo-membership-badge">🔒 Photo Membership</span>\n                    <h2 id="photoMembershipTitle">Unlock Original Temple Photos</h2>\n                    <p class="photo-membership-subtitle">Support AngkorLens and unlock access to original-resolution temple photographs. Your membership supports heritage documentation and research.</p>\n                </div>\n                <button class="photo-membership-close" onclick="closePhotoMembership()" aria-label="Close">&times;</button>\n            </div>\n            <div class="photo-membership-preview">\n                <img id="photoMembershipPreview" src="" alt="Membership photo preview" loading="lazy" decoding="async">\n                <div class="photo-membership-preview-lock"><div class="photo-membership-lock-circle">🔒</div></div>\n            </div>\n            <div id="photoComingSoon" style="display:none;margin:0 0 16px;padding:16px 18px;border-radius:14px;background:#fff7e6;border:1px solid #e2c98f;color:#5a4316;font-size:15px;line-height:1.5"><strong>Coming soon ✨</strong><br>Online payment for original photos will open soon. Thank you for supporting AngkorLens and Khmer heritage!</div>\n            <div class="photo-plan-grid">\n<div class="photo-plan">\n                    <h3>Buy One Picture</h3>\n                    <div class="photo-plan-price">$4.99 <span>/ picture</span></div>\n                    <ul><li>One original-resolution photograph</li><li>Purchase this picture only</li></ul>\n                    <button class="photo-pay-btn" onclick="startMembershipCheckout(\'single\')">Buy This Picture — $4.99</button>\n                </div>\n<div class="photo-plan">\n                    <h3>Monthly Membership</h3>\n                    <div class="photo-plan-price">$14.99 <span>/ month</span></div>\n                    <ul><li>Unlimited photo access</li><li>Original-resolution photographs</li><li>Support Khmer heritage documentation</li></ul>\n                    <button class="photo-pay-btn" onclick="startMembershipCheckout(\'monthly\')">Continue — $14.99/month</button>\n                </div>\n<div class="photo-plan yearly">\n                    <h3>Yearly Membership</h3>\n                    <div class="photo-plan-price">$100.00 <span>/ year</span></div>\n                    <ul><li>Unlimited photo access</li><li>Original-resolution photographs</li><li>Support Khmer heritage documentation</li></ul>\n                    <button class="photo-pay-btn" onclick="startMembershipCheckout(\'yearly\')">Continue — $100.00/year</button>\n                </div>\n        </div>\n            <p class="photo-membership-note"><strong>Payment setup:</strong> Stripe Checkout will be connected in the next step. This page does not collect or store card or bank information.</p>\n        </div>\n<script>\n(function(){var m=document.getElementById(\'photoMembershipModal\');\nwindow.openPhotoMembership=function(src){document.getElementById(\'photoMembershipPreview\').src=src||\'\';var n=document.getElementById(\'photoComingSoon\');if(n)n.style.display=\'none\';m.classList.remove(\'hidden\');document.body.style.overflow=\'hidden\';};\nwindow.closePhotoMembership=function(){m.classList.add(\'hidden\');document.body.style.overflow=\'\';};\nwindow.startMembershipCheckout=function(){var n=document.getElementById(\'photoComingSoon\');if(n){n.style.display=\'block\';n.scrollIntoView({behavior:\'smooth\',block:\'nearest\'});}};\nm.addEventListener(\'click\',function(e){if(e.target===m)closePhotoMembership();});\ndocument.addEventListener(\'keydown\',function(e){if(e.key===\'Escape\')closePhotoMembership();});\ndocument.querySelectorAll(\'.ph\').forEach(function(el){el.addEventListener(\'click\',function(){var i=el.querySelector(\'img\');openPhotoMembership(i?i.currentSrc||i.src:\'\');});});\ndocument.addEventListener(\'contextmenu\',function(e){if(e.target.closest(\'.ph\'))e.preventDefault();});\ndocument.addEventListener(\'dragstart\',function(e){if(e.target.tagName===\'IMG\')e.preventDefault();});\n})();\n</script>'
CSS='''*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans Khmer",sans-serif;background:#F6F1E7;color:#221F1C;line-height:1.7}
a{color:#7A5A1E}header{background:#221F1C;padding:14px 16px}header a{color:#C9A55A;text-decoration:none;font-family:Georgia,serif;letter-spacing:.18em;text-transform:uppercase;font-size:18px}
main{max-width:960px;margin:0 auto;padding:28px 16px 60px}.crumb{font-size:14px;margin:0 0 10px}h1{font-family:Georgia,serif;font-size:clamp(28px,5vw,42px);line-height:1.15;margin:0 0 6px}
.km{color:#7A5A1E;font-size:20px;margin:0 0 4px}.sub{color:#6b625a;margin:0 0 22px}.hero{width:100%;max-height:70vh;object-fit:contain;background:#e8e0d2;border-radius:18px;display:block}
.story{background:#fff;border-radius:18px;padding:22px 20px;margin:24px 0;font-size:16px;overflow-wrap:anywhere}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px}
.grid img{width:100%;height:200px;object-fit:cover;border-radius:12px;display:block;background:#e8e0d2}.by{color:#6b625a;font-size:14px;margin:8px 0 0}.cta{display:inline-block;margin-top:26px;background:#C9A55A;color:#221F1C;font-weight:700;text-decoration:none;padding:12px 22px;border-radius:999px}
.more{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.more a{border:1px solid #d6cbb8;border-radius:999px;padding:6px 12px;text-decoration:none;font-size:14px}
footer{text-align:center;color:#6b625a;font-size:14px;padding:24px 16px}
.ph{position:relative;margin:0;cursor:pointer;-webkit-touch-callout:none;user-select:none;-webkit-user-select:none}.ph img{pointer-events:none}
.ph::after{content:"";position:absolute;inset:0}.wm{position:absolute;right:10px;bottom:8px;color:rgba(255,255,255,.85);font-size:12px;text-shadow:0 1px 3px rgba(0,0,0,.7);pointer-events:none;z-index:1}
.lk img{filter:blur(6px) saturate(.8);transform:scale(1.08)}.lk{overflow:hidden;border-radius:12px}.lock{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:30px;z-index:1;background:rgba(34,31,28,.25)}
.lockmsg{background:#fff;border-radius:12px;padding:10px 14px;color:#5a4316}.lbbox{background:#fff;color:#221F1C;border-radius:20px;max-width:560px;width:100%;padding:26px 22px;position:relative;text-align:left}
.lbbox h2{font-family:Georgia,serif;margin:4px 0 8px}.lbk{color:#7A5A1E;font-weight:800;letter-spacing:.12em;font-size:12px;margin:0}.lbbox .lbx{color:#221F1C;font-size:32px;top:8px;right:12px}
@media print{.ph img{display:none}}
.lb{position:fixed;inset:0;background:rgba(15,13,11,.94);z-index:50;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px}.lb[hidden]{display:none}
.lb img{max-width:100%;max-height:68vh;object-fit:contain;border-radius:10px}.lbx{position:absolute;top:10px;right:14px;background:none;border:0;color:#fff;font-size:40px;cursor:pointer;line-height:1}
.lbt{margin:0 0 14px;font-size:15px;color:#4E4740}.plans{display:flex;flex-direction:column;gap:8px}
.plans button{background:#C9A55A;color:#221F1C;border:0;border-radius:999px;padding:10px 16px;font-weight:700;cursor:pointer;font-size:14px}.plans button:hover{background:#E2C98F}
.soon{background:#fff7e6;color:#5a4316;border-radius:12px;padding:12px 14px;margin:12px 0 0;font-size:14px;text-align:left}.soon[hidden]{display:none}.soon a{color:#7A5A1E}'''

# Map box + "5 free temple maps" limit (only for pages that have a 'gps' field in new_temples.json)
def mapbox(k,g):
    note=f' <span style="color:#7a6a55;font-size:13px">({html.escape(g["note"])})</span>' if g.get('note') else ''
    return (f'<div class="mapbox" style="margin:6px 0 18px;padding:12px 16px;background:#fff;border:1px solid #E6DCCB;border-radius:14px;">'
            f'<div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;">'
            f'<span>📍 <strong>GPS · ទីតាំង:</strong> {html.escape(g["dms"])}{note}</span>'
            f'<a class="mapbtn" data-slug="{k}" href="https://www.google.com/maps?q={g["lat"]},{g["lon"]}" target="_blank" rel="noopener" '
            f'style="display:inline-block;padding:7px 14px;border-radius:999px;background:#8A5A2B;color:#fff;text-decoration:none;font-weight:700;font-size:14px;">Open in Google Maps · បើកផែនទី</a></div>'
            f'<div id="mapLeft" style="margin-top:6px;color:#7a6a55;font-size:12px"></div></div>')
MAPGATE = """<div id="mapPayModal" class="photo-membership-overlay hidden" role="dialog" aria-modal="true" aria-labelledby="mapPayTitle"><div class="photo-membership-card">
<div class="photo-membership-top"><div><span class="photo-membership-badge">🗺️ Temple Maps</span><h2 id="mapPayTitle">Unlock all temple maps</h2>
<p class="photo-membership-subtitle">You have used your 5 free temple maps. Unlock the GPS map for every AngkorLens temple with one payment.<br>អ្នកបានប្រើផែនទីឥតគិតថ្លៃគ្រប់ ៥ ប្រាសាទហើយ។ បង់ម្តង ដើម្បីប្រើផែនទីប្រាសាទទាំងអស់។</p></div>
<button class="photo-membership-close" onclick="closeMapPay()" aria-label="Close">&times;</button></div>
<div id="mapComingSoon" style="display:none;margin:16px 0;padding:16px 18px;border-radius:14px;background:#fff7e6;border:1px solid #e2c98f;color:#5a4316;font-size:15px;line-height:1.5"><strong>Coming soon ✨</strong><br>Online payment will open soon. Thank you for supporting AngkorLens and Khmer heritage!<br>ការបង់ប្រាក់តាមអនឡាញ នឹងបើកឆាប់ៗនេះ។</div>
<div class="photo-plan yearly" style="margin-top:18px"><h3>All Temple Maps</h3><div class="photo-plan-price">$10.99 <span>/ one time</span></div>
<ul><li>GPS map for every temple</li><li>Use as many times as you like</li><li>Support Khmer heritage documentation</li></ul>
<button class="photo-pay-btn" onclick="document.getElementById('mapComingSoon').style.display='block'">Unlock all maps — $10.99</button></div>
<p class="photo-membership-note"><strong>Payment setup:</strong> Stripe Checkout will be connected in the next step. This page does not collect or store card or bank information.</p></div></div>
<script>(function(){var K='al_maps_v1',U='al_maps_unlocked',F=5,m=document.getElementById('mapPayModal'),b=document.querySelector('.mapbtn'),L=document.getElementById('mapLeft');
function get(){try{var a=JSON.parse(localStorage.getItem(K)||'[]');return Array.isArray(a)?a:[]}catch(e){return []}}
function save(a){try{localStorage.setItem(K,JSON.stringify(a))}catch(e){}}
function un(){try{return localStorage.getItem(U)==='1'}catch(e){return false}}
window.closeMapPay=function(){m.classList.add('hidden');document.body.style.overflow='';};
function openPay(){document.getElementById('mapComingSoon').style.display='none';m.classList.remove('hidden');document.body.style.overflow='hidden';}
if(!b)return;var s=b.getAttribute('data-slug');
function upd(){var a=get();if(un()||a.indexOf(s)>=0){L.textContent='';return}var r=Math.max(0,F-a.length);L.textContent=r>0?(r+' of '+F+' free temple maps left · នៅសល់ផែនទីឥតគិតថ្លៃ '+r+'/'+F):'Your 5 free temple maps are used · ផែនទីឥតគិតថ្លៃ ៥ អស់ហើយ';}
b.addEventListener('click',function(e){var a=get();if(un()||a.indexOf(s)>=0)return;if(a.length<F){a.push(s);save(a);setTimeout(upd,300);return}e.preventDefault();openPay();});
m.addEventListener('click',function(e){if(e.target===m)closeMapPay();});document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMapPay();});upd();})();</script>"""
FB="onerror=\"if(!this.dataset.f){this.dataset.f=1;this.src=this.dataset.o}\""
out={}
keys=sorted(pages)
for k in keys:
    x=pages[k]; n=x['name']; km=x['t'].strip(); sub=x['s'].strip()
    desc=eng_desc(x['h']) or f"Photographs and history of {n}, a Khmer temple site in Cambodia, by Samnang Loy."
    desc=desc[:155]
    url=f'https://www.angkorlens.com/temple-{k}.html'
    h0,o0=img(x['i'][0],900)
    ogi=img(x['i'][0],1200)[0]
    def lockurl(s0): return 'https://wsrv.nl/?url='+quote('https://www.angkorlens.com/'+s0.lstrip('/'),safe='')+'&w=60&blur=8&q=40&output=jpg'
    rest=x['i'][1:]
    thumbs=''
    if rest: thumbs+=f'<figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{img(rest[0],480)[0]}" alt="{html.escape(n)} photo 2"><span class="wm">© AngkorLens</span></figure>'
    thumbs+=''.join(f'<figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{img(s0,480)[0]}" alt="{html.escape(n)} photo {i+3}"><span class="wm">© AngkorLens</span></figure>' for i,s0 in enumerate(rest[1:]))
    nlock=max(0,len(rest)-1)
    idx=keys.index(k); others=[keys[(idx+j)%len(keys)] for j in range(1,7)]
    more=''.join(f'<a href="/temple-{o}.html">{html.escape(pages[o]["name"])}</a>' for o in others)
    ld={"@context":"https://schema.org","@type":"TouristAttraction","name":n,"alternateName":km,"description":desc,"url":url,"image":ogi,"isAccessibleForFree":True,"touristType":"Cultural heritage","containedInPlace":{"@type":"Country","name":"Cambodia"}}
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(n)} ({html.escape(km)}) – Photos &amp; History | AngkorLens</title>
<meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}"><link rel="icon" href="/favicon.ico">
<meta property="og:title" content="{html.escape(n)} – AngkorLens"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:image" content="{ogi}"><meta property="og:url" content="{url}"><meta property="og:type" content="article">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script><style>{CSS}</style></head><body>
<header><a href="/">AngkorLens</a></header><main>
<p class="crumb"><a href="/">Home</a> › <a href="/temples.html">Temple guides</a> › {html.escape(n)}</p>
<h1>{html.escape(n)}</h1><p class="km">{html.escape(km)}</p><p class="sub">{html.escape(sub)}</p>
<figure class="ph hero-w"><img class="hero" draggable="false" src="{h0}" alt="{html.escape(n)}, Cambodia"><span class="wm">© AngkorLens · Samnang Loy</span></figure>
<p class="by">Photographs by Samnang Loy · AngkorLens</p>
{mapbox(k,x['gps']) if x.get('gps') else ''}<section class="story">{x['h']}</section>
<h2 style="font-family:Georgia,serif">More photos · រូបថតបន្ថែម</h2><p class="lockmsg">🔒 Tap any photo to see it full size or buy the original. · ចុចលើរូប ដើម្បីមើលទំហំធំ ឬទិញរូបដើម។</p><div class="grid">{thumbs}</div>
<a class="cta" href="/">← Explore all of AngkorLens</a>
<h2 style="font-family:Georgia,serif;margin-top:34px">More temples</h2><nav class="more">{more}</nav>
</main><footer>© AngkorLens · Samnang Loy</footer>'''+(MAPGATE if x.get('gps') else '')+LB+'''</body></html>'''
    out[f'temple-{k}.html']=page
# index page
cards=''.join(f'<a class="c" href="/temple-{k}.html"><img loading="lazy" src="{img(pages[k]["i"][0],480)[0]}" data-o="{img(pages[k]["i"][0],480)[1]}" {FB} alt="{html.escape(pages[k]["name"])}"><b>{html.escape(pages[k]["name"])}</b><span>{html.escape(pages[k]["t"].strip())}</span></a>' for k in keys)
out['temples.html']=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Khmer Temple Guides – {len(keys)} Temples in Cambodia | AngkorLens</title>
<meta name="description" content="Photo guides to {len(keys)} ancient Khmer temples across Cambodia, from Preah Vihear and Koh Ker to Preah Khan Kampong Svay, photographed by Samnang Loy.">
<link rel="canonical" href="https://www.angkorlens.com/temples.html"><link rel="icon" href="/favicon.ico"><style>{CSS}
.list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}}.c{{background:#fff;border-radius:16px;overflow:hidden;text-decoration:none;color:#221F1C}}.c img{{width:100%;height:160px;object-fit:cover;display:block;background:#e8e0d2}}.c b{{display:block;padding:10px 12px 0;font-family:Georgia,serif}}.c span{{display:block;padding:0 12px 12px;color:#7A5A1E;font-size:14px}}</style></head><body>
<header><a href="/">AngkorLens</a></header><main><p class="crumb"><a href="/">Home</a> › Temple guides</p>
<h1>Khmer Temple Guides</h1><p class="km">មគ្គុទ្ទេសក៍ប្រាសាទខ្មែរ</p><p class="sub">{len(keys)} temples photographed by Samnang Loy, each with history in English and Khmer.</p>
<div class="list">{cards}</div></main><footer>© AngkorLens · Samnang Loy</footer></body></html>'''
for f,c in out.items(): open(R+f,'w').write(c)
sm=['https://www.angkorlens.com/','https://www.angkorlens.com/temples.html']+[f'https://www.angkorlens.com/temple-{k}.html' for k in keys]
open(R+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>2026-11-18</lastmod></url>\n' for u in sm)+'</urlset>\n')
print(len(out),'pages written')
