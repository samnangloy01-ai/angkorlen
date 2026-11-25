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

# ---- On the way to Reno (photo-card page, like the sftravel "Top 10" row) ----
ROAD=[('road-1.jpg','On the way','High desert hills','ភ្នំវាលខ្សាច់ខ្ពង់រាប','Brown hills, a green golf course, and snowy peaks peeking through the gap.'),
('road-2.jpg','On the way','Wetlands and a wide sky','វាលភក់ និងមេឃធំទូលាយ','Flat marsh with pools of water, yellow wildflowers and low hills far away.'),
('road-3.jpg','On the way','A winding mountain road','ផ្លូវភ្នំកោងៗ','Sagebrush slopes, a 35 mph sign and mountains under white clouds.'),
('road-4.jpg','On the way','Snow-capped mountains','ភ្នំគ្របដោយព្រិល','A long white ridge rising above the town, seen from the highway.'),
('road-5.jpg','On the way','Ranch land below the peaks','ដីកសិដ្ឋាន ក្រោមកំពូលភ្នំ','Wooden barns, juniper trees and a bright snowy summit.'),
('road-6.jpg','On the way','City below the mountains','ទីក្រុងនៅជើងភ្នំ','Green neighborhoods spreading out to the foot of the hills.'),
('road-7.jpg','On the way','Exit 65','ច្រកចេញលេខ ៦៥','A quiet off-ramp lined with pine and eucalyptus trees.'),
('road-8.jpg','On the way','Down the hill','ចុះពីលើភ្នំ','A 15 mph curve sign, power poles and snowy peaks in the distance.'),
('road-9.jpg','On the way','Toward Lake Tahoe','ឆ្ពោះទៅបឹង Tahoe','A road sign for South Lake Tahoe below jagged snowy mountains.'),
('road-10.jpg','On the way','Rolling green hills','ភ្នំបៃតងរលកៗ','Oak trees scattered over grassy hills beside the freeway.'),
('road-11.jpg','On the way','Green hills over the street','ភ្នំបៃតងពីលើផ្លូវ','Lamp posts, a gas station sign and grassy hills under puffy clouds.'),
('road-12.jpg','On the way','A row of tall palms','ជួរដើមដូងខ្ពស់ៗ','Skinny palm trees standing high above a green park.'),
('road-13.jpg','On the way','Golden hills by the freeway','ភ្នំពណ៌មាសក្បែរផ្លូវធំ','Dry golden grass and dark oak trees along the highway.'),
('road-14.jpg','On the way','Marsh and wind turbines','វាលភក់ និងម៉ាស៊ីនខ្យល់','Wide green wetlands, a strip of water and white wind turbines far away.'),
('road-15.jpg','On the way','Junction U.S. 50','ផ្លូវប្រសព្វ U.S. 50','A green highway sign, sagebrush and a line of snowy peaks.'),
('road-16.jpg','On the way','Down into the valley','ចុះទៅជ្រលងភ្នំ','The freeway dropping toward layers of rolling hills and a glimpse of water.'),
('road-17.jpg','On the way','Pine-covered hills','ភ្នំគ្របដោយដើមស្រល់','Dark green pines dotted over dry golden slopes.')]
_o=[f'road-{n}.jpg' for n in (10,16,13,11,12,2,14,7,1,3,17,8,4,5,6,9,15)]
ROAD=sorted(ROAD,key=lambda r:_o.index(r[0]))
CITY=[('reno-1.jpg','The Reno Arch','ខ្លោងទ្វារ Reno','The famous sign over the street: “The Biggest Little City in the World.”'),
('reno-city-1.jpg','Downtown at night','ទីក្រុងពេលយប់','Towers glowing green and red against the dark blue sky.'),
('reno-city-2.jpg','The Truckee River','ទន្លេ Truckee','The river rushes under a bridge right through downtown.'),
('reno-city-3.jpg','Riverwalk gardens','សួនតាមមាត់ទន្លេ','Stone terraces and black pyramid-roofed shelters along the water.'),
('reno-city-4.jpg','A shelter by the river','រោងតូចមាត់ទន្លេ','Looking out from a riverside shelter toward the bridge.'),
('reno-city-5.jpg','The glass whale','ត្រីបាឡែនកញ្ចក់','A giant whale sculpture made of colored glass panels, standing in the city plaza.'),
('reno-city-6.jpg','Whale and little whale','ត្រីបាឡែនធំ និងតូច','Seen from below, a smaller whale swims under the big one.'),
('reno-city-7.jpg','A giant mining machine','ម៉ាស៊ីនរ៉ែយក្ស','A huge old-style mining rig with wheels and lights, under a painted sky dome indoors.'),
('reno-city-8.jpg','The sea-god fountain','ក្បាលទឹកព្រះសមុទ្រ','A sea god, mermen and sea monsters around an indoor fountain.'),
('reno-city-9.jpg','The white dome','ដំបូលមូលពណ៌ស','A huge white dome on the rooftops under storm clouds.'),
('reno-city-10.jpg','Eldorado at dusk','Eldorado ពេលព្រលប់','The Eldorado tower with its neon lines just turning on.'),
('reno-city-11.jpg','Eldorado at night','Eldorado ពេលយប់','The whole tower outlined in red neon.'),
('reno-city-12.jpg','The camera mural','គំនូរជញ្ជាំងអ្នកថតរូប','A rainbow mural of a photographer standing on a boombox, on The Virginian.'),
('reno-city-13.jpg','A bird of metal','បក្សីលោហៈ','A bird sculpture made of curved metal strips, set into a stone wall.'),
('reno-city-14.jpg','Morning over West Street','ពេលព្រឹកលើផ្លូវ West','Snowy peaks above a blue-and-white tower and the Bonanza Inn sign.'),
('reno-city-15.jpg','Maple Street crossing','ផ្លូវប្រសព្វ Maple','Red lights, an I-80 West sign and an old taco shop sign.'),
('reno-city-16.jpg','The freeway through town','ផ្លូវធំកាត់ទីក្រុង','Traffic winding between green neighborhoods below a snowy ridge.'),
('reno-city-17.jpg','The whole valley','ជ្រលងភ្នំទាំងមូល','From a hillside, the city towers look small in the middle of the valley.')]
def _card(f,lab,t,k,d): return f'<article class="rc"><figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{img(f,640)[0]}" alt="{html.escape(t)}, Reno, Nevada – photo by Samnang Loy"><span class="wm">© AngkorLens</span></figure><div class="rb"><small>{html.escape(lab)}</small><b>{html.escape(t)}</b><i>{html.escape(k)}</i><p>{html.escape(d)}</p></div></article>'
cc=''.join(_card(f,'In Reno',t,k,d) for f,t,k,d in CITY)
RURL='https://www.angkorlens.com/reno-lake-tahoe.html'; SF_URLS.append(RURL)
rc=''.join(f'<article class="rc"><figure class="ph"><img loading="lazy" decoding="async" draggable="false" src="{img(f,640)[0]}" alt="{html.escape(t)} – on the way to Reno, photo by Samnang Loy"><span class="wm">© AngkorLens</span></figure><div class="rb"><small>{html.escape(lab)}</small><b>{html.escape(t)}</b><i>{html.escape(k)}</i><p>{html.escape(d)}</p></div></article>' for f,lab,t,k,d in ROAD)
rd='Photos of Reno, Nevada by Samnang Loy: the Reno Arch, the Truckee River, neon casinos, the glass whale and the drive there through hills and snowy mountains.'
rld={"@context":"https://schema.org","@type":"ImageGallery","name":"Reno, Nevada & the road there","description":rd,"url":RURL,"author":{"@type":"Person","name":"Samnang Loy"}}
out['reno-lake-tahoe.html']=head('Reno, Nevada – Photos of the City & the Road There | AngkorLens',rd,RURL,img('reno-1.jpg',1200)[0],rld).replace('<main>','<div class="band"><div class="bi"><p class="crumb"><a href="/">Home</a> › Reno &amp; Lake Tahoe</p><small>ON THE ROAD · តាមផ្លូវ</small><h1>Reno, Nevada <em>&amp; the road there</em></h1><p class="km2">ទីក្រុង Reno រដ្ឋ Nevada និងផ្លូវទៅដល់ទីនោះ</p><p class="bd">Photos from Reno, “The Biggest Little City in the World,” and from my drive there: the river, neon lights, public art, green and golden hills, open wetlands, high desert and snow-capped mountains. Tap a photo to see it full size.<br>រូបថតក្នុងទីក្រុង Reno និងតាមផ្លូវ៖ ទន្លេ ភ្លើងនីអុង សិល្បៈសាធារណៈ វាលភក់ ភ្នំបៃតង វាលខ្សាច់ និងភ្នំគ្របដោយព្រិល។</p></div></div><main class="rm">',1)+f'''
<style>.band{{background:#B9532F;color:#fff;padding:34px 16px 120px}}.bi{{max-width:1500px;margin:0 auto}}.band .crumb a{{color:#FBE7C6}}.band small{{letter-spacing:.2em;font-weight:800;font-size:14px}}
.band h1{{font-family:Georgia,serif;font-size:clamp(34px,6vw,64px);margin:6px 0 4px;color:#fff}}.band h1 em{{display:block;color:#FBE7C6;font-style:italic}}.km2{{color:#FBE7C6;font-size:20px;margin:0 0 10px}}.bd{{max-width:900px;font-size:17px;margin:0}}
h2.rh{{font-family:Georgia,serif;margin:0 0 14px;padding:10px 16px;background:#fff;border-radius:12px;display:inline-block;box-shadow:0 4px 14px rgba(0,0,0,.08)}}main.rm{{max-width:1500px;margin-top:-100px;padding-top:0}}.rg{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}.rc{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 6px 22px rgba(0,0,0,.12)}}
.rc img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:#e8e0d2}}.rb{{padding:12px 16px 18px}}.rb small{{color:#6b625a;letter-spacing:.08em;text-transform:uppercase;font-size:12px;font-weight:700}}
.rb b{{display:block;font-family:Georgia,serif;font-size:20px;margin:4px 0 0;color:#1f2a44}}.rb i{{display:block;font-style:normal;color:#7A5A1E;font-size:14px}}.rb p{{margin:6px 0 0;color:#4E4740;font-size:15px;line-height:1.5}}
@media(max-width:900px){{.rg{{grid-template-columns:repeat(2,1fr);gap:12px}}.rb b{{font-size:16px}}.rb p{{font-size:13px}}}}</style>
<h2 class="rh">In Reno · ក្នុងទីក្រុង Reno</h2><div class="rg">{cc}</div><h2 class="rh" style="margin-top:40px">On the way · តាមផ្លូវ</h2><div class="rg">{rc}</div>
<p class="by" style="margin-top:18px">Photographs by Samnang Loy · AngkorLens. Lake Tahoe photos coming soon.</p>
<a class="cta" href="/">← Back to AngkorLens</a></main><footer>© AngkorLens · Samnang Loy</footer>'''+LB+'</body></html>'
