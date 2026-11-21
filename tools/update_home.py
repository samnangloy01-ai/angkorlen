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
rows=STYLE
for k in range(len(books)-1,-1,-1):
    b=books[k]; no=FIRST_BOOK+k; n=len(b)
    sid='new-temples' if k==len(books)-1 else f'new-temples-book{no}'
    t=TITLES[len(books)-1-k] if len(books)-1-k < len(TITLES) else 'More temples · ប្រាសាទផ្សេងទៀត'
    rows+=(f'<div style="background:#fafafa;width:100%;padding:1px 0 30px"><section class="alrow" id="{sid}" aria-label="{html.escape(t.split(" · ")[0])}">\n'
           f' <div class="alrow-h"><h2>{html.escape(t)} ({n})</h2><a href="/temples.html">View all</a></div>\n'
           ' <div class="alrow-w">\n  <button type="button" class="alrow-b l" aria-label="Scroll left" disabled>‹</button>\n'
           '  <div class="alrow-s">'+''.join(card(e) for e in reversed(b))+'</div>\n'
           '  <button type="button" class="alrow-b r" aria-label="Scroll right">›</button>\n </div>\n</section></div>\n')
rows+='''<script>
document.querySelectorAll('.alrow-w').forEach(function(w){var s=w.querySelector('.alrow-s'),l=w.querySelector('.l'),r=w.querySelector('.r');
function pos(){var img=s.querySelector('.alrow-i');if(img){var t=img.offsetHeight/2-28+'px';l.style.top=t;r.style.top=t;}l.disabled=s.scrollLeft<5;r.disabled=s.scrollLeft+s.clientWidth>=s.scrollWidth-5;}
l.onclick=function(){s.scrollBy({left:-s.clientWidth*0.9,behavior:'smooth'});};r.onclick=function(){s.scrollBy({left:s.clientWidth*0.9,behavior:'smooth'});};
s.addEventListener('scroll',pos,{passive:true});window.addEventListener('resize',pos);setTimeout(pos,300);pos();});
</script>'''
f=R+'index.html'; s=open(f).read()
i=s.index('<!--NEWROWS-->')+14; j=s.index('<!--/NEWROWS-->'); s=s[:i]+rows+s[j:]
n=len(glob.glob(R+'temple-*.html'))
s=re.sub(r'Explore \d+ Khmer',f'Explore {n} Khmer',s)
s=re.sub(r'All temple guides \(\d+\)',f'All temple guides ({n})',s)
s=re.sub(r'See all \d+ temple',f'See all {n} temple',s)
open(f,'w').write(s); print('index.html updated, count =',n,'new temples =',len(d),'rows =',len(books))
