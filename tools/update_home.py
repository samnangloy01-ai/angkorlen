# python3 tools/update_home.py
# Rebuilds the homepage "New Temples" row from tools/new_temples.json (newest first)
# and sets the temple count in index.html to the number of temple pages.
import json,html,os,re,glob
from urllib.parse import quote
T=os.path.dirname(os.path.abspath(__file__))+'/'; R=os.path.dirname(T[:-1])+'/'
d=json.load(open(T+'new_temples.json'))
def im(f,w): return 'https://wsrv.nl/?url='+quote('https://www.angkorlens.com/'+f,safe='')+'&w=%d&q=75&output=jpg'%w
cards=''.join(f'<a class="alrow-c" href="/temple-{e["slug"]}.html"><span class="alrow-i"><img loading="lazy" decoding="async" src="{im(e["i"][0],600)}" alt="{html.escape(e["name"])}"></span><small>New temple</small><b>{html.escape(e["name"])}</b><i>{html.escape(e["km"])}</i></a>' for e in reversed(d))
f=R+'index.html'; s=open(f).read()
i=s.index('<!--NEWCARDS-->')+15; j=s.index('<!--/NEWCARDS-->'); s=s[:i]+cards+s[j:]
n=len(glob.glob(R+'temple-*.html'))
s=re.sub(r'Explore \d+ Khmer',f'Explore {n} Khmer',s)
s=re.sub(r'All temple guides \(\d+\)',f'All temple guides ({n})',s)
s=re.sub(r'See all \d+ temple',f'See all {n} temple',s)
open(f,'w').write(s); print('index.html updated, count =',n)
