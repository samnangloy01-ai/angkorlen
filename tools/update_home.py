# python3 tools/update_home.py
# Rebuilds the homepage "New Temples" rows from tools/new_temples.json and sets the temple count.
# Every 40 new temples make one book and one row: temples 1-40 = Book 3, 41-80 = Book 4, ...
# The newest book's row is on top; inside each row the newest temple is first.
import json,html,os,re,glob
from urllib.parse import quote
T=os.path.dirname(os.path.abspath(__file__))+'/'; R=os.path.dirname(T[:-1])+'/'
PER_BOOK=40; FIRST_BOOK=3
KM='០១២៣៤៥៦៧៨៩'
def kmn(n): return ''.join(KM[int(c)] for c in str(n))
d=json.load(open(T+'new_temples.json'))
def im(f,w): return 'https://wsrv.nl/?url='+quote('https://www.angkorlens.com/'+f,safe='')+'&w=%d&q=75&output=jpg'%w
def loc(e):
    return e['sub'].split(' · ')[-1]
PIN='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>'
def card(e): return f'<a class="alrow-c" href="/temple-{e["slug"]}.html"><span class="alrow-i"><img loading="lazy" decoding="async" src="{im(e["i"][0],600)}" alt="{html.escape(e["name"])}"></span><b>{html.escape(e["name"])}</b><i>{html.escape(e["km"])}</i><span class="alrow-p">{PIN}{html.escape(loc(e))}</span></a>'
TITLES=['Explore our temple collection · ស្វែងរកបណ្តុំប្រាសាទរបស់យើង','My favorite temple collection · បណ្តុំប្រាសាទដែលខ្ញុំចូលចិត្ត']
STYLE='''<style>
.alrow-c b{margin-top:14px;font-weight:700;letter-spacing:-.01em;white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
.alrow-i{border-radius:14px}
.alrow-p{display:inline-flex;align-items:center;gap:6px;margin-top:12px;padding:6px 12px;border:1.5px solid #7A5A1E;border-radius:8px;color:#5b4314;font-size:14px;font-weight:600;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.alrow-p svg{flex:0 0 auto}
</style>
'''
books=[d[i:i+PER_BOOK] for i in range(0,len(d),PER_BOOK)]
COLL=['collection-explore.html','collection-favorite.html']
def collpage(k):  # newest book first: 0 = explore, 1 = favorite, 2+ = more
    j=len(books)-1-k
    return COLL[j] if j<len(COLL) else f'collection-book{FIRST_BOOK+k}.html'
def blurb(e):
    t=re.sub(r'<[^>]+>',' ',e['h'].split('<hr')[0]); t=re.sub(r'\s+',' ',t).strip()
    t=t[len(e['name']):].strip() if t.startswith(e['name']) else t
    t=re.sub(r'^\([^)]*\)\s*','',t)  # drop a "(Other name)" left over from the heading
    m=re.match(r'(.{40,170}?[.!?])\s',t+' '); t=m.group(1) if m else t[:150].rsplit(' ',1)[0]+'…'
    return t
def fcard(e): return (f'<a class="alfx-c" href="/temple-{e["slug"]}.html"><span class="alfx-i"><img loading="lazy" decoding="async" src="{im(e["i"][0],700)}" alt="{html.escape(e["name"])}"></span>'
    f'<b>{html.escape(e["name"])}</b><i>{html.escape(e["km"])}</i><span class="alrow-p">{PIN}{html.escape(loc(e))}</span><p>{html.escape(blurb(e))}</p></a>')
FSTYLE='''<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
<style>
.alfx{max-width:1280px;margin:0 auto;padding:56px 24px 40px;display:grid;grid-template-columns:minmax(260px,.9fr) 2.1fr;gap:40px;align-items:start}
.alfx-l .eb{font-size:14px;font-weight:800;letter-spacing:.18em;color:#3f7a3a;text-transform:uppercase;margin:6px 0 10px}
.alfx-l h2{margin:0;line-height:1.02}
.alfx-l h2 .t1{display:block;font-size:clamp(40px,4.6vw,64px);font-weight:900;color:#1d1b19;letter-spacing:-.02em}
.alfx-l h2 .t2{display:block;font-family:Pacifico,'Brush Script MT',cursive;font-weight:400;font-size:clamp(36px,4.2vw,58px);color:#c8452c;margin-top:4px}
.alfx-l .kmt{font-family:'Noto Serif Khmer','Khmer OS',serif;color:#7A5A1E;font-size:18px;margin:12px 0 0}
.alfx-l .ds{font-size:18px;line-height:1.65;color:#3a3633;margin:18px 0 24px}
.alfx-btn{display:inline-block;background:#24485c;color:#fff;font-weight:800;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;padding:16px 30px;border-radius:4px}
.alfx-btn:hover{background:#1a3747}
.alfx-r{position:relative;min-width:0}
.alfx-s{display:flex;gap:28px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding:6px 4px 10px}
.alfx-s::-webkit-scrollbar{display:none}
.alfx-c{flex:0 0 min(320px,78vw);scroll-snap-align:start;text-decoration:none;color:#221F1C}
.alfx-i{display:block;aspect-ratio:1/1;overflow:hidden;background:#e8e0d2;position:relative}
.alfx-i img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.alfx-i:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(255,170,120,.10),rgba(140,60,40,.12))}
.alfx-c:first-child .alfx-i{transform:rotate(-3deg);margin:8px 6px 4px}
.alfx-c:hover .alfx-i img{transform:scale(1.04)}
.alfx-c b{display:block;font-size:26px;font-weight:900;line-height:1.15;margin-top:18px;letter-spacing:-.01em}
.alfx-c:hover b{color:#c8452c;text-decoration:underline}
.alfx-c i{display:block;font-style:normal;font-family:'Noto Serif Khmer','Khmer OS',serif;color:#7A5A1E;font-size:15px;margin-top:4px}
.alfx-c p{font-size:16px;line-height:1.6;color:#3a3633;margin:12px 0 0}
.alfx-a{position:absolute;left:-26px;top:40px;display:flex;flex-direction:column;gap:6px;z-index:3}
.alfx-a button{width:52px;height:52px;border:0;background:#b9d7e6;color:#24485c;font-size:22px;cursor:pointer;border-radius:2px}
.alfx-a button:disabled{opacity:.45;cursor:default}
@media(max-width:860px){.alfx{grid-template-columns:1fr;gap:24px;padding-top:36px}.alfx-a{display:none}.alfx-c:first-child .alfx-i{transform:none;margin:0}}
</style>
'''
rows=STYLE+FSTYLE
for k in range(len(books)-1,-1,-1):
    b=books[k]; no=FIRST_BOOK+k; n=len(b)
    sid='new-temples' if k==len(books)-1 else f'new-temples-book{no}'
    t=TITLES[len(books)-1-k] if len(books)-1-k < len(TITLES) else 'More temples · ប្រាសាទផ្សេងទៀត'
    cp=collpage(k)
    if k==len(books)-1:
        rows+=(f'<div style="background:#fff;width:100%"><section class="alfx" id="{sid}" aria-label="Explore our temple collection">\n'
               ' <div class="alfx-l"><p class="eb">The collection · ទើបបន្ថែមថ្មី</p>'
               '<h2><span class="t1">Explore our</span><span class="t2">Temple Collection</span></h2>'
               '<p class="kmt">ស្វែងរកបណ្តុំប្រាសាទរបស់យើង</p>'
               '<p class="ds">From hidden brick towers in the forest to bridges and gates of the Khmer Empire, these are the newest temples I have photographed and written about. Each one has its history in English and Khmer, photos and a GPS map.</p>'
               f'<a class="alfx-btn" href="/{cp}">See all ({n}) · មើលទាំងអស់</a></div>\n'
               ' <div class="alfx-r"><div class="alfx-a"><button type="button" class="r" aria-label="Next">→</button><button type="button" class="l" aria-label="Previous" disabled>←</button></div>\n'
               '  <div class="alfx-s">'+''.join(fcard(e) for e in reversed(b))+'</div></div>\n</section></div>\n')
        continue
    rows+=(f'<div style="background:#fafafa;width:100%;padding:1px 0 30px"><section class="alrow" id="{sid}" aria-label="{html.escape(t.split(" · ")[0])}">\n'
           f' <div class="alrow-h"><h2>{html.escape(t)} ({n})</h2><a href="/{cp}">View all</a></div>\n'
           ' <div class="alrow-w">\n  <button type="button" class="alrow-b l" aria-label="Scroll left" disabled>‹</button>\n'
           '  <div class="alrow-s">'+''.join(card(e) for e in reversed(b))+'</div>\n'
           '  <button type="button" class="alrow-b r" aria-label="Scroll right">›</button>\n </div>\n</section></div>\n')
rows+='''<script>
document.querySelectorAll('.alrow-w').forEach(function(w){var s=w.querySelector('.alrow-s'),l=w.querySelector('.l'),r=w.querySelector('.r');
function pos(){var img=s.querySelector('.alrow-i');if(img){var t=img.offsetHeight/2-28+'px';l.style.top=t;r.style.top=t;}l.disabled=s.scrollLeft<5;r.disabled=s.scrollLeft+s.clientWidth>=s.scrollWidth-5;}
l.onclick=function(){s.scrollBy({left:-s.clientWidth*0.9,behavior:'smooth'});};r.onclick=function(){s.scrollBy({left:s.clientWidth*0.9,behavior:'smooth'});};
s.addEventListener('scroll',pos,{passive:true});window.addEventListener('resize',pos);setTimeout(pos,300);pos();});
document.querySelectorAll('.alfx-r').forEach(function(w){var s=w.querySelector('.alfx-s'),l=w.querySelector('.l'),r=w.querySelector('.r');
function pos(){l.disabled=s.scrollLeft<5;r.disabled=s.scrollLeft+s.clientWidth>=s.scrollWidth-5;}
l.onclick=function(){s.scrollBy({left:-s.clientWidth*0.8,behavior:'smooth'});};r.onclick=function(){s.scrollBy({left:s.clientWidth*0.8,behavior:'smooth'});};
s.addEventListener('scroll',pos,{passive:true});window.addEventListener('resize',pos);setTimeout(pos,300);pos();});
</script>'''
# collection pages: built from temples.html (same look), only that collection's temples
tp=open(R+'temples.html').read()
allc={m.group(1):m.group(0) for m in re.finditer(r'<a class="c" href="/temple-([a-z0-9-]+)\.html">.*?</a>',tp)}
CT=[('Explore our temple collection','ស្វែងរកបណ្តុំប្រាសាទរបស់យើង'),('My favorite temple collection','បណ្តុំប្រាសាទដែលខ្ញុំចូលចិត្ត')]
for k in range(len(books)):
    b=books[k]; j=len(books)-1-k; en,kmT=CT[j] if j<len(CT) else ('More temples','ប្រាសាទផ្សេងទៀត')
    cards=''.join(allc[e['slug']] for e in reversed(b) if e['slug'] in allc)
    pg=tp
    pg=re.sub(r'<title>.*?</title>',f'<title>{en} – {len(b)} Khmer Temples | AngkorLens</title>',pg,1)
    pg=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="https://www.angkorlens.com/{collpage(k)}">',pg,1)
    pg=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{en}: {len(b)} Khmer temples photographed by AngkorLens, with history in English and Khmer.">',pg,1)
    pg=re.sub(r'<p class="crumb">.*?</p>',f'<p class="crumb"><a href="/">Home</a> › <a href="/temples.html">Temple guides</a> › {en}</p>',pg,1)
    pg=re.sub(r'<h1>.*?</h1><p class="km">.*?</p><p class="sub">.*?</p>',f'<h1>{en}</h1><p class="km">{kmT}</p><p class="sub">{len(b)} temples · <a href="/temples.html">See all temples</a></p>',pg,1)
    pg=re.sub(r'<div class="list">.*?</div></main>','<div class="list">'+cards.replace('\\','\\\\')+'</div></main>',pg,1,flags=re.S)
    open(R+collpage(k),'w').write(pg)
f=R+'index.html'; s=open(f).read()
i=s.index('<!--NEWROWS-->')+14; j=s.index('<!--/NEWROWS-->'); s=s[:i]+rows+s[j:]
n=len([p for p in glob.glob(R+'temple-*.html') if 'http-equiv="refresh"' not in open(p).read()])
s=re.sub(r'Explore \d+ Khmer',f'Explore {n} Khmer',s)
s=re.sub(r'All temple guides \(\d+\)',f'All temple guides ({n})',s)
s=re.sub(r'See all \d+ temple',f'See all {n} temple',s)
open(f,'w').write(s); print('index.html updated, count =',n,'new temples =',len(d),'rows =',len(books))

# ---- homepage search: index of ALL temple pages (English + Khmer), shown as a dropdown under the search box ----
idx=[]
thumbs={m.group(1):m.group(2) for m in re.finditer(r'<a class="c" href="/temple-([a-z0-9-]+)\.html"><img[^>]*?src="([^"]+)"',tp)}
for p in sorted(glob.glob(R+'temple-*.html')):
    slug=p.split('/temple-')[1][:-5]; t=open(p).read()
    if 'http-equiv="refresh"' in t: continue
    g=lambda rx:(re.search(rx,t,re.S).group(1) if re.search(rx,t,re.S) else '')
    name=html.unescape(g(r'<h1>(.*?)</h1>')); km=html.unescape(g(r'<p class="km">(.*?)</p>')); sub=html.unescape(g(r'<p class="sub">(.*?)</p>'))
    story=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',g(r'<section class="story">(.*?)</section>'))))[:260]
    idx.append({'u':'/temple-'+slug+'.html','n':name,'k':km,'s':sub if sub!=name else '','t':thumbs.get(slug,''),'x':(slug.replace('-',' ')+' '+story).lower()})
SJS=('<!--ALSEARCH--><style>#alSR{position:absolute;left:0;right:0;top:100%;margin-top:8px;background:#fff;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.25);'
 'text-align:left;max-height:420px;overflow:auto;z-index:60;display:none}#alSR a{display:flex;gap:12px;align-items:center;padding:9px 12px;color:#221F1C;text-decoration:none;border-bottom:1px solid #f1ece4}'
 '#alSR a:hover,#alSR a.on{background:#FBF7F0}#alSR img{width:56px;height:42px;object-fit:cover;border-radius:8px;flex:none;background:#eee}#alSR b{display:block;font-size:15px}'
 '#alSR i{display:block;font-style:normal;font-size:13px;color:#8A5A2B}#alSR small{display:block;font-size:12px;color:#8c8478}#alSR .none{padding:14px;color:#8c8478;font-size:14px}'
 '#alSR .all{display:block;text-align:center;font-weight:600;color:#8A5A2B}</style>'
 '<script>window.AL_SEARCH='+json.dumps(idx,ensure_ascii=False).replace('</','<\\/')+';'
 '(function(){var inp=document.getElementById("searchInput");if(!inp)return;var box=inp.parentNode;box.style.position="relative";'
 'var r=document.createElement("div");r.id="alSR";box.appendChild(r);var cur=-1,list=[];'
 'function norm(s){return(s||"").toLowerCase().replace(/[\\u200b\\u200c\\u200d]/g,"").replace(/\\s+/g," ").trim()}'
 'function esc(s){return s.replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}'
 'function score(e,q){var n=norm(e.n),k=norm(e.k),w=q.split(" "),s=0;for(var i=0;i<w.length;i++){var t=w[i];if(!t)continue;'
 'if(n.indexOf(t)==0||k.indexOf(t)==0)s+=5;else if(n.indexOf(t)>=0||k.indexOf(t)>=0)s+=3;else if(norm(e.s).indexOf(t)>=0)s+=2;else if(e.x.indexOf(t)>=0)s+=1;else return 0}return s}'
 'function show(){var q=norm(inp.value);cur=-1;if(q.length<1){r.style.display="none";return}'
 'list=AL_SEARCH.map(function(e){return[score(e,q),e]}).filter(function(a){return a[0]>0}).sort(function(a,b){return b[0]-a[0]}).map(function(a){return a[1]});'
 'var h=list.slice(0,8).map(function(e){return\'<a href="\'+e.u+\'">\'+(e.t?\'<img loading="lazy" src="\'+e.t+\'" alt="">\':"")+\'<span><b>\'+esc(e.n)+\'</b><i>\'+esc(e.k)+\'</i>\'+(e.s?\'<small>\'+esc(e.s)+\'</small>\':"")+\'</span></a>\'}).join("");'
 'if(!list.length)h=\'<div class="none">No temple found · រកមិនឃើញប្រាសាទ</div>\';'
 'h+=\'<a class="all" href="/temples.html">\'+(list.length>8?("See all "+list.length+" results · "):"")+\'All temples · ប្រាសាទទាំងអស់</a>\';r.innerHTML=h;r.style.display="block"}'
 'function mark(){var a=r.querySelectorAll("a");for(var i=0;i<a.length;i++)a[i].classList.toggle("on",i==cur)}'
 'inp.addEventListener("input",show);inp.addEventListener("focus",show);'
 'inp.addEventListener("keydown",function(ev){var a=r.querySelectorAll("a");if(ev.key=="ArrowDown"){cur=Math.min(cur+1,a.length-1);mark();ev.preventDefault()}'
 'else if(ev.key=="ArrowUp"){cur=Math.max(cur-1,0);mark();ev.preventDefault()}else if(ev.key=="Enter"){var t=a[cur>=0?cur:0];if(t&&list.length){location.href=t.href;ev.preventDefault()}}else if(ev.key=="Escape"){r.style.display="none"}});'
 'document.addEventListener("click",function(ev){if(!box.contains(ev.target))r.style.display="none"});'
 'var btn=box.querySelector("button");if(btn)btn.addEventListener("click",function(){show();if(list.length)location.href=list[0].u})})();</script><!--/ALSEARCH-->')
s=open(f).read()
if '<!--ALSEARCH-->' in s:
    s=s[:s.index('<!--ALSEARCH-->')]+SJS+s[s.index('<!--/ALSEARCH-->')+16:]
else:
    s=s.replace('</body>',SJS+'\n</body>',1)
s=s.replace('placeholder="Search temples, ruins, architecture..."','placeholder="Search a temple · ស្វែងរកប្រាសាទ (e.g. Kravan, ក្រវ៉ាន់, Koh Ker)"')
open(f,'w').write(s); print('search index:',len(idx),'temples')
