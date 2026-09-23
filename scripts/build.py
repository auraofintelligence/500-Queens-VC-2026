"""Build the static, accessible 500 Queens site without third-party dependencies."""
import json, html, re, argparse
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://auraofintelligence.github.io/500-Queens-VC-2026/'
e = html.escape
def read(name, default=None):
    p = ROOT / 'data' / name
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
def image(name, alt, cls='', eager=False):
    path=ROOT/'assets/images'/f'{name}.webp'
    if not path.exists(): name='home-hero'
    return f'<picture class="{cls}"><source media="(max-width: 760px)" srcset="assets/images/{name}-mobile.webp"><img src="assets/images/{name}.webp" alt="{e(alt)}" width="1536" height="1024" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async"></picture>'
def card(title,text,href=None,art=None,tag=None):
    heading=f'<a class="card-title" href="{e(href)}">{title}</a>' if href else f'<h3>{title}</h3>'
    return f'<article class="card">{image(art,title,"card-image") if art else ""}<div class="card-inner">{f"<span class=tag>{tag}</span>" if tag else ""}{heading}<p>{text}</p></div></article>'
def section(heading,body,cls='',intro=None):
    return f'<section class="section {cls}"><div class="wrap"><div class="section-head"><h2>{heading}</h2>{f"<p>{intro}</p>" if intro else ""}</div>{body}</div></section>'
def feature(title,text,art,link=None,label='Explore the idea'):
    return f'<section class="section"><div class="wrap split"><div><h2>{title}</h2>{text}{f"<a class=text-link href={link}>{label} →</a>" if link else ""}</div><figure class="feature-image">{image(art,"AI-generated concept illustration: "+title)}<figcaption>AI-generated concept illustration.</figcaption></figure></div></section>'
def table(headers,rows,caption=''):
    return '<div class="table-scroll"><table>'+ (f'<caption>{caption}</caption>' if caption else '') +'<thead><tr>'+''.join(f'<th scope="col">{c}</th>' for c in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'

def home():
    body='''<div class="intro-band"><div class="wrap"><p><span class="status-dot"></span>A bold proposal. A community to build. A future to lead.</p><a href="references.html">Explore the planning material →</a></div></div>'''
    body+=feature('If equality were<br><em>being designed now...</em>','<p class="statement">What would women want and need from the places, workplaces and systems around them?</p><p>Begin with women\'s own experiences. From the outback to the city, across cultures, body types, ages and ways of living, the answers can shape what we build together.</p>','equality-community','designing-equality.html','Explore the big question')
    body+=section('Talent is everywhere.<br><em>Opportunity should be too.</em>', '''<div class="split top"><p class="statement">More women shaping what gets built, what gets funded, and what comes next.</p><div><p>500 Queens Venture Capital is a proposal to connect women with the capital, practical experience and relationships to become CEOs, enterprise leaders and decision makers.</p><p>Start with something useful. Build a business, take an existing one forward, lead a research team or help a community thrive. You do not need to arrive with a startup. You need room to begin.</p><a class="text-link" href="vision.html">Discover the vision →</a></div></div><div class="stat-row"><div class="stat"><strong>500+</strong><p>Women developing leadership in the Australian starting ambition.</p></div><div class="stat"><strong>120</strong><p>Original enterprise ideas to explore, question and develop.</p></div><div class="stat"><strong>24</strong><p>AI Queen mentor concepts, alongside experienced people.</p></div></div>''','light')
    body+=section('Your ambition belongs here.','<div class="grid">'+card('Become the decision maker','Learn to lead through real projects, customers, teams and budgets. Bring your curiosity; develop your judgement.','leadership.html','leadership-hero')+card('Build something that matters','Explore enterprise ideas spanning care, energy, intelligent tools, culture and the biggest scientific questions.','ventures.html','ventures-hero')+card('Help opportunity grow','Contribute mentoring, a place to work, a practical project or backing for a clear result.','capital.html','capital-hero')+'</div>',intro='An invitation to future founders, returning workers, experienced leaders, researchers, mentors and backers.')
    body+=feature('A different kind<br>of royal ambition.','<p class="statement">Joyful Responsible Abundance.</p><p>A rewarding life. Responsibility for consequences. Prosperity that reaches more people.</p><p>Here, being a Queen is about the confidence and capability to lead. The ambition extends from a first paid leadership role to resilient communities, shared intelligence and civilisation-scale challenges.</p>','commons-hero','vision.html','Meet the bigger vision')
    body+=section('From a first spark<br>to real responsibility.','<div class="journey">'+''.join(f'<article><span class="number">0{i}</span><h3>{t}</h3><p>{p}</p></article>' for i,(t,p) in enumerate([('Find your people','Meet others through learning, culture and a useful problem.'),('Explore your direction','Choose an enterprise idea and work with mentors to test it.'),('Practise leadership','Make decisions about customers, money, people and delivery.'),('Build the next chapter','Pursue paid responsibility, grants, ownership or business succession.')],1))+'</div><a class="text-link" href="leadership.html">See how leadership develops →</a>','plum')
    body+=section('A funding gap.<br>A leadership opportunity.','''<div class="split top"><div class="funding-bars"><div><div class="bar-label"><span>Female-only founding teams</span><strong>2%</strong></div><div class="bar"><span style="width:2%"></span></div></div><div><div class="bar-label"><span>At least one female founder</span><strong>24%</strong></div><div class="bar"><span style="width:24%"></span></div></div><p class="notice">Share of Australian startup funding in 2025. The 24% includes the 2%. <a href="https://www.australianstartupfunding.com/" target="_blank" rel="noopener">State of Australian Startup Funding 2025 ↗</a></p></div><div><p>These figures describe founding teams. Our ambition goes further: women with meaningful authority over strategy, budgets, hiring, ownership and investment.</p><p>The original vision seeks a 50/50 funding balance. The practical work begins with leadership development, useful enterprises and a delivery community.</p><a class="text-link" href="capital.html">Explore the proposed funding model →</a></div></div>''')
    body+=feature('Brisbane beginnings.<br>Open horizons.','<p>Born in Brisbane, imagined for Australia and connected to a wider world. The starting vision grows from at least 500 women in Australia to international ambitions of 10,000 and 50,000.</p><p>Local people shape local programmes. Knowledge, mentoring and useful tools travel between them.</p>','horizons-hero','global.html','Follow the wider horizon')
    body+='''<section class="cta-section"><h2>The future needs<br><em>your kind of ambition.</em></h2><p>Bring something you want to learn, a problem worth solving or experience to share. Find a place in the idea and help shape what happens next.</p><div class="actions"><a class="button" href="join.html">Find your place <span>↗</span></a><a class="button secondary" href="references.html">Read the plan <span>→</span></a></div></section>'''
    return body

def references():
    lib=read('reference-library.json',{})
    docs=lib.get('documents',[]); sites=lib.get('websites',[]); repos=lib.get('repositories',[])
    readers={r['id']:r for r in read('reference-readers.json',[])}
    reader_intro='Read each document online, or choose to download the original. ' if len(readers)==len(docs) else ''
    body=section('The ideas, in their own words.',f'<p class="narrow">Read the current planning document, trace an idea to the original presentations, or follow a connected public project. This library contains {len(docs)} supplied documents and all 15 supplied website links. {reader_intro}Original files are preserved without rewriting their contents.</p><div class="reading-links"><a href="#documents">Documents</a><a href="#websites">Websites</a><a href="#provenance">How to read the sources</a></div>','light')
    body+='<section class="section" id="documents"><div class="wrap" data-filter-group="documents"><h2>The document library</h2><div class="filter-bar"><div class="field"><label for="document-search">Search the documents</label><input type="search" id="document-search" placeholder="Try leadership, Queens, care or space"></div></div><p class="filter-count" data-result-count aria-live="polite"></p><div class="reference-list">'
    for doc in docs:
        href=doc.get('href'); title=doc['title']; ext=Path(href or doc.get('originalFilename','')).suffix.removeprefix('.').upper(); size=doc.get('sizeBytes',doc.get('size',0))
        if not isinstance(size,(float,int)): size=0
        size_text=f'{size/1024/1024:.1f} MB' if size>=1024*1024 else f'{size/1024:.0f} KB'
        reader=readers.get(doc['id']);online=f'<a class="read-source" href="{reader["slug"]}.html#read">Read online →</a>' if reader else ''
        body+=f'<article class="reference-item" data-search="{e(title+" "+doc.get("category",""))}"><div><h3>{e(title)}</h3><p>{e(doc.get("category","Original reference"))} · {ext} · {size_text}</p></div><div class="reference-actions">{online}{f"<a href={e(href)} download>Download {ext} ↓</a>" if href else "<span>Source unavailable</span>"}</div></article>'
    body+='</div><p class="no-results" hidden>No documents match this search. Try a shorter phrase.</p></div></section>'
    links=''.join(f'<article class="reference-item"><div><h3>{e(s["title"])}</h3><p>{e(s.get("description","Supplied public reference"))}</p></div><a href="{e(s["url"])}" target="_blank" rel="noopener">Visit source ↗</a></article>' for s in sites+repos)
    body+='<section class="section plum" id="websites"><div class="wrap"><h2>Follow the connections.</h2><p>Public websites and the additional Extreme Matter Atlas repository supplied with the brief.</p><div class="reference-list">'+links+'</div></div></section>'
    body+=section('Read the source. Keep the context.','''<div id="provenance" class="grid two">'''+card('Present-day plan','The planning document dated 23 September 2026 guides this website. Earlier files show the evolution of the idea, including historical dates, numbers and terminology.')+card('Ambition and evidence','The funding and scale figures are proposed or historical guides. Original presentations include long-horizon concepts that need research and testing.')+card('Original files','The 27 document downloads retain the supplied bytes. The public <a href="data/reference-library.json">reference register</a> records file sizes and SHA-256 checksums for verification.')+card('Artwork and rights','Site illustrations are original GenAI concept artwork, not photographs of an established team, occupied premises or delivered infrastructure. <a href="licence.html">Read the licence and credits</a>.')+'</div>','light')
    body+=feature('The beginning<br>of a conversation.','<p>Use these materials to ask better questions, develop an enterprise brief or bring a useful contribution to the next conversation.</p><p>A source library keeps the history visible while new people help shape what follows.</p>','licence-hero','join.html','Find your place')
    return body

def licence():
    raw=(ROOT/'LICENSE').read_text(encoding='utf-8'); parts=[]; in_list=False
    for line in raw.splitlines():
        if line.startswith('- '):
            if not in_list: parts.append('<ul>');in_list=True
            parts.append(f'<li>{e(line[2:])}</li>');continue
        if in_list:parts.append('</ul>');in_list=False
        if line.startswith('# '):continue
        if line.startswith('## '):parts.append(f'<h2>{e(line[3:])}</h2>')
        elif line.strip():parts.append(f'<p>{e(line)}</p>')
    if in_list:parts.append('</ul>')
    return section('The Strange But True<br>Public Source Licence.','<div class="prose">'+''.join(parts)+'</div>','light')+section('The original mark. New worlds of possibility.','<div class="split"><img src="assets/brand/500-queens-original.png" alt="Original 500 Queens Venture Capital logo: a queen holding a golden orbital form above a 500 lotus" width="642" height="577"><div><p>The logo and favicon use the original 500 Queens artwork from <a href="https://auraofintelligence.com/alpha-infinity-foundation/">Aura of Intelligence, Alpha Infinity Foundation</a>.</p><p>The site artwork was created with the built-in image generation tool for this project. It depicts possible futures and fictional people. <a href="assets/images/provenance.json">View the artwork prompts and provenance</a>.</p><p>Typography uses Playfair Display and Manrope, bundled locally under their open font licences. Third-party references retain their own rights.</p></div></div>')

def generic(chapter):
    result=''
    for i,s in enumerate(chapter['sections']):
        content=''.join(f'<p>{p}</p>' for p in s.get('paragraphs',[]))
        if s.get('cards'): content+='<div class="grid '+('two' if len(s['cards'])%2==0 else '')+'">'+''.join(card(c['title'],c['text']) for c in s['cards'])+'</div>'
        if s.get('steps'): content+='<div class="journey">'+''.join(f'<article><span class="number">{n:02d}</span><h3>{st["title"]}</h3><p>{st["text"]}</p></article>' for n,st in enumerate(s['steps'],1))+'</div>'
        if s.get('table'): content+=table(s['table']['headers'],s['table']['rows'])
        if s.get('image'):content+='<figure class="feature-image">'+image(s['image'],s.get('caption','AI-generated concept illustration'))+'<figcaption>'+s.get('caption','AI-generated concept illustration.')+'</figcaption></figure>'
        result+=section(s['heading'],content,'light' if i%3==0 else ('plum' if i%3==2 else ''))
        if i==0 and not s.get('image'):
            supporting={'vision':'horizons-hero','community':'care-hero','leadership':'capital-hero','ai-queens':'intelligence-hero','shared-intelligence':'council-hero','care':'commons-hero','capital':'leadership-hero','brisbane':'commons-hero','global':'ventures-hero'}
            result+='<div>'+image(supporting.get(chapter['slug'],chapter['hero']),'AI-generated concept illustration for '+chapter['title'],'wide-art')+'<p class="wrap image-caption">AI-generated concept illustration.</p></div>'
    if chapter['slug']=='capital':result+=budget()
    if chapter.get('sources'):result+=section('Explore the source material.','<div class="reading-links">'+''.join(f'<a href="{e(s["href"])}">{e(s["title"])}</a>' for s in chapter['sources'])+'</div>','section-tight')
    return result

def budget():
    fields=[('intake','Enterprise grants each year',100,1),('grant','Amount per grant (A$)',50000,1000),('operations','Annual operations (A$)',1000000,10000),('years','Years of funded operation',5,1),('setup','One-off setup (A$)',0,1000)]
    form='<form id="budget-form"><div class="budget-fields">'+''.join(f'<div class="field"><label for="budget-{n}">{label}</label><input id="budget-{n}" type="number" name="{n}" value="{value}" min="{1 if n=="years" else 0}" step="{1 if n in ("intake","years") else "any"}" required></div>' for n,label,value,step in fields)+'</div><button type="reset" class="button secondary" style="margin-top:25px">Restore the 2021 guide</button></form>'
    return section('Shape a funding scenario.','<p class="narrow">Start with the rounded 2021 planning guide, then explore different inputs. These are calculations, not a funding offer, current quote or confirmed backing. All amounts are Australian dollars.</p><div class="budget-layout">'+form+'<div class="budget-result" aria-live="polite"><p>Combined programme guide</p><output id="budget-output">A$30,000,000</output><p id="budget-detail">A$25,000,000 enterprise grants + A$5,000,000 operations over five years.</p><p id="budget-enterprises">500 enterprise grants in this scenario.</p></div></div><p class="notice" style="margin-top:25px">Formula: (annual grants × amount per grant + annual operations) × years + setup. Changing yearly costs, inflation and financing are not modelled. Leadership participation is counted separately from enterprise grants.</p>','plum')

def ventures():
    items=read('ventures.json',[]); sectors=sorted({v['sector'] for v in items})
    body=section('Useful work.<br>Extraordinary possibilities.','<p class="narrow">These public project concepts are starting points for women to develop and lead. They connect the wider vision with local services, making, culture, resilience and scientific discovery. Each suggested next step is an experiment to develop, not an advertised placement or funded portfolio company.</p><div class="actions"><a class="button" href="catalogue.html">Explore all 120 original ideas →</a></div>','light')
    body+='<section class="section"><div class="wrap" data-filter-group="project connections"><h2>Find a direction that moves you.</h2><div class="filter-bar"><div class="field"><label for="venture-search">Search the ideas</label><input type="search" id="venture-search" placeholder="Try energy, care, film or intelligence"></div><div class="field"><label for="venture-sector">Choose a field</label><select id="venture-sector"><option value="">Every field</option>'+''.join(f'<option>{e(s)}</option>' for s in sectors)+'</select></div></div><p class="filter-count" data-result-count aria-live="polite"></p><div class="grid two">'
    arts=['ventures-hero','commons-hero','horizons-hero','leadership-hero']
    for i,v in enumerate(items):
        body+=f'<article class="card" data-category="{e(v["sector"])}" data-search="{e(v["title"]+" "+v["summary"]+" "+v["sector"])}">'+image(arts[i%4],'AI-generated conceptual setting for '+v['sector'],'card-image')+f'<div class="card-inner"><span class="tag">{e(v["sector"])}</span><h3>{e(v["title"])}</h3><p>{e(v["summary"])}</p><p><strong>A possible first test</strong><br>{e(v["opportunity"])}</p><p class="notice">{e(v["evidenceNote"])}</p><a class="text-link" href="{e(v["href"])}" target="_blank" rel="noopener">Explore the public project ↗</a></div></article>'
    body+='</div><p class="no-results" hidden>No projects match. Try another field or a shorter search.</p></div></section>'
    body+=feature('From a possibility<br>to an enterprise brief.','<p>Name the people who need it. Describe the smallest useful result. Estimate the time, skills and money required. Decide what evidence would make you continue, change direction or stop.</p><p>For research ideas, record the mechanism, nearest working technology, measurement and cost of the next test. Boldness and honest evidence can belong together.</p>','capital-hero','leadership.html','Build your leadership pathway')
    return body

def catalogue():
    data=read('enterprise-catalogue.json',{}); items=data.get('enterprises',[]); categories=list(dict.fromkeys(v['category'] for v in items))
    body=section('An invitation to think bigger.','<p class="narrow">The original 500 Queens presentation offered 120 startup suggestions, across systems for life, matter and intelligence. They remain a starting library: some connect to available technologies; others are far-horizon research ideas.</p><p class="narrow">Explore the original titles, then turn an interesting question into a practical brief. Inclusion records the original ambition, not technical feasibility or investment readiness.</p>','light')
    body+='<section class="section"><div class="wrap" data-filter-group="original ideas"><h2>Find your spark.</h2><div class="filter-bar"><div class="field"><label for="catalogue-search">Search 120 original ideas</label><input type="search" id="catalogue-search" placeholder="Try water, care, robots or space"></div><div class="field"><label for="catalogue-sector">Explore a theme</label><select id="catalogue-sector"><option value="">All eleven themes</option>'+''.join(f'<option>{e(c)}</option>' for c in categories)+'</select></div></div><p class="filter-count" data-result-count aria-live="polite"></p><div class="catalogue-grid">'
    for v in items:
        title=v.get('planningTitle') or v['title']; queen=v.get('pillarQueen',''); queen=', '.join(queen) if isinstance(queen,list) else queen
        body+=f'<article class="card" data-search="{e(title+" "+v["category"]+" "+queen)}" data-category="{e(v["category"])}"><div class="card-inner"><span class="tag">{e(v["category"])}</span><h3>{e(title)}</h3><p>Explore with {e(queen)}.</p></div></article>'
    body+='</div><p class="no-results" hidden>No ideas match. Try a broader phrase or a different theme.</p></div></section>'
    body+=feature('A brave idea deserves<br>a clear next question.','<p>Choose one concept. Ask what would need to be true for it to work. Find the closest demonstrated technology. Plan a small test with someone who understands the field.</p><p>AI Queens can help organise the questions. Human experience, measurements and community needs guide the decisions.</p>','council-hero','ai-queens.html','Meet the AI Queens')
    body+=section('Trace the original catalogue.','<p>The original titles come from <em>500 Queens VC NEW Long</em>, slides 15-18. The current planning document connects them with mentor pairings and practical activities. Obvious spelling updates appear in the display; the <a href="data/enterprise-catalogue.json">catalogue data</a> retains the original titles and provenance.</p><a class="text-link" href="references.html">Read the original documents →</a>','light')
    return body

def join():
    body=section('You do not need<br>to have it all figured out.','<p class="narrow">Bring something you want to learn, a problem worth solving or experience to share. Future founders, returning workers, students, researchers and established leaders all have a place in the proposed community.</p>','light')
    body+=section('Where would you like to begin?','''<p>Choose a starting point. You can change direction as you explore.</p><div class="choice-buttons">'''+''.join(f'<button type="button" data-pathway="{k}" aria-pressed="{str(k=="learn").lower()}">{v}</button>' for k,v in [('learn','Learn to lead'),('build','Build an enterprise'),('mentor','Share my experience'),('back','Back the work'),('host','Host or connect')])+'''</div><div class="pathway-result" aria-live="polite"><h3 id="path-title">Begin with a useful question</h3><p id="path-text">You can start without a company or a polished pitch. Choose an enterprise theme, write down a problem you have seen, and explore which leadership skills you would like to develop.</p><a class="text-link" id="path-link" href="leadership.html">Explore the leadership pathway →</a></div>''')
    body+=feature('A first conversation<br>can change a direction.','<p>The next establishment step is gathering people who can help deliver: organisers, teachers, experienced executives, project partners and backers.</p><p>Useful offers are specific. A workshop you could host. A business problem you could share. A prototype you could test. A paid placement you could support.</p>','commons-hero')
    body+=section('Make a starting note.','''<p class="narrow">Write a short note for your own use. Keep it on your device, then choose whether to share it through the existing Aura of Intelligence contact page. This website does not collect or submit your note.</p><div class="field narrow"><label for="interest-note">What would you like to learn, build or contribute?</label><textarea id="interest-note" rows="5" placeholder="A problem I care about, experience I can share, or something I would like to learn..."></textarea></div><div class="actions"><button type="button" class="button" id="download-note">Download my note ↓</button><a class="button secondary" href="https://auraofintelligence.com/contact/" target="_blank" rel="noopener">Open the Aura contact page ↗</a></div><p id="note-status" class="notice" aria-live="polite" style="margin-top:20px">Your words stay in this page until you download them. No account is required.</p>''','plum')
    body+=section('What happens from here?','<div class="grid two">'+card('Shape the delivery community','Interested people can help define the first gathering, practical briefs and mentoring offers. No intake dates or funded places have been announced.')+card('Turn offers into a programme','An operating host or delivery group, current budget and confirmed backing are needed to open funded activity. Luke has contributed the vision and public material voluntarily.')+'</div>','light')
    return body

ORDER=['index','vision','designing-equality','community','leadership','ai-queens','ventures','catalogue','network','shared-intelligence','care','capital','brisbane','global','join','references','licence']
META={
'index':('Home','Female ambition deserves<br><em>a bigger stage.</em>','A new generation of women leading enterprise, shaping investment and building a more abundant world. Beginning in Brisbane. Open to possibility.','home-hero'),
'ventures':('Venture ideas','Build the world<br><em>you want to lead.</em>','Explore enterprise directions connecting local needs with bold ideas in science, culture, care and shared prosperity.','ventures-hero'),
'catalogue':('120 startup ideas','One idea can<br><em>open a world.</em>','120 original startup suggestions. Eleven fields of possibility. A starting point for your curiosity.','ventures-hero'),
'join':('Find your place','Bring your<br><em>kind of brilliance.</em>','An idea. A useful skill. A question you cannot leave alone. There are many ways to begin.','leadership-hero'),
'references':('Source library','Big ideas.<br><em>Open sources.</em>','Explore the plan, the original archive and the public projects behind 500 Queens.','library-hero'),
'licence':('Licence and credits','Learn. Explore.<br><em>Give credit.</em>','The Strange But True Public Source Licence and the creative provenance of this website.','library-hero')}

def render(slug,meta,body,pages):
    title,heading,dek,art=meta; idx=pages.index(slug); prev=pages[(idx-1)%len(pages)]; nxt=pages[(idx+1)%len(pages)]
    link=lambda s:f'{s}.html'
    visible_pages=globals().get('NAV_PAGES',pages)
    nav=''.join(f'<a href="{link(s)}" {"aria-current=page" if s==slug else ""}>{META[s][0]}</a>' for s in visible_pages)
    actions='<div class="actions"><a class="button" href="join.html">Find your place <span>↗</span></a><a class="button secondary" href="vision.html">Explore the vision <span>→</span></a></div>' if slug=='index' else ''
    if len(pages)<10: actions='<div class="actions"><a class="button" href="references.html">Explore the source library <span>→</span></a></div>' if slug=='index' else ''
    seo_heading=re.sub('<[^>]+>',' ',heading).strip()
    return f'''<!doctype html>
<html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#21132b"><title>{e(title)} | 500 Queens Venture Capital</title><meta name="description" content="{e(dek)}"><link rel="canonical" href="{BASE+('' if slug=='index' else link(slug))}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)} | 500 Queens Venture Capital"><meta property="og:description" content="{e(dek)}"><meta property="og:url" content="{BASE+('' if slug=='index' else link(slug))}"><meta property="og:image" content="{BASE}assets/images/home-hero.webp"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/brand/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="assets/brand/favicon.png"><link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png"><link rel="stylesheet" href="assets/site.css?v=20260923-network-2"><link rel="stylesheet" href="assets/network.css?v=20260923-network-2"><link rel="stylesheet" href="assets/readers.css?v=20260923-network-2"><link rel="stylesheet" href="assets/heroes.css?v=20260923-network-2"><script defer src="assets/site.js?v=20260923-network-2"></script><script defer src="assets/network.js?v=20260923-network-2"></script></head>
<body id="top"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="index.html" aria-label="500 Queens Venture Capital home"><img src="assets/brand/500-queens-original.png" width="62" height="62" alt=""><span class="brand-name">500 Queens<span>Venture Capital</span></span></a><nav class="header-links" aria-label="Main navigation">{''.join(f'<a href="{link(s)}">{META[s][0]}</a>' for s in ['vision','ai-queens','catalogue','network'] if s in visible_pages)}</nav><button class="menu-toggle" aria-expanded="false" aria-controls="explore-menu" type="button">Explore ☰</button></div></header><nav class="menu-panel" id="explore-menu" aria-label="Explore every page" hidden><div class="wrap"><h2>A world of possibility.</h2><p>Follow a chapter, or choose your own direction.</p><div class="menu-grid">{nav}</div></div></nav>
<main id="main"><section class="hero {'home' if slug=='index' else 'detail-hero' if slug.startswith(('queen-','startup-','category-','source-')) else ''}">{image(art,'AI-generated concept artwork for '+title,'hero-bg',True)}<div class="wrap"><div class="hero-copy">{f'<div class="hero-crumb"><a href="index.html">500 Queens</a> / {e(title)}</div>' if slug!='index' else ''}<h1>{heading}</h1><p>{dek}</p>{actions}</div></div><span class="hero-meta">GenAI concept artwork</span></section>{body}</main>
<nav class="page-turn" aria-label="Previous and next page"><a href="{link(prev)}"><span>← Previous page</span><strong>{META[prev][0]}</strong></a><a href="{link(nxt)}"><span>Next page →</span><strong>{META[nxt][0]}</strong></a></nav><footer><div class="wrap"><div class="footer-top"><div><a class="brand" href="index.html"><img src="assets/brand/500-queens-original.png" width="62" height="62" alt="Original 500 Queens logo"><span class="brand-name">500 Queens<span>Venture Capital</span></span></a><p>Women leading enterprise and investment.<br>Joyful Responsible Abundance.</p></div><nav class="footer-links" aria-label="Footer chapters">{''.join(f'<a href="{link(s)}">{META[s][0]}</a>' for s in ['vision','leadership','ventures','join'] if s in visible_pages)}</nav><nav class="footer-links" aria-label="Sources and rights"><a href="references.html">Source library</a><a href="licence.html">Licence and credits</a><a href="https://github.com/auraofintelligence/500-Queens-VC-2026" target="_blank" rel="noopener">Project on GitHub ↗</a></nav></div><div class="footer-bottom"><p>500 Queens is a proposal in development. Funding, premises, programmes and partnerships are to be established. The planning material records no committed funding. GenAI illustrations depict possible futures.</p><p>© 2026 Luke Nathan Hayes / Strange But True / Aura of Intelligence.<br><a href="licence.html">Strange But True Public Source Licence</a>. Commercial rights reserved.</p></div></div></footer><a class="to-top" href="#top" aria-label="Back to top">↑</a></body></html>'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--batch',choices=['first','full'],default='full');args=parser.parse_args()
    chapters=read('chapters.json',[])
    dedicated_heroes={'vision':'vision-hero','shared-intelligence':'intelligence-hero','care':'care-hero','brisbane':'brisbane-hero'}
    for chapter in chapters:
        if chapter['slug'] in dedicated_heroes:chapter['hero']=dedicated_heroes[chapter['slug']]
    META['catalogue']=(*META['catalogue'][:3],'catalogue-hero')
    META['join']=(*META['join'][:3],'invitation-hero')
    META['licence']=(*META['licence'][:3],'licence-hero')
    page_headings={
        'vision':'A future shaped<br><em>by more of us.</em>',
        'community':'Find your people.<br><em>Build your next chapter.</em>',
        'leadership':'Learn to lead.<br><em>Lead to change.</em>',
        'ai-queens':'Meet your<br><em>Council of Queens.</em>',
        'shared-intelligence':'Intelligence<br><em>we can share.</em>',
        'care':'Care counts.<br><em>People matter.</em>',
        'capital':'Back the work.<br><em>Grow the possibility.</em>',
        'brisbane':'A shared home.<br><em>A bigger beginning.</em>',
        'global':'Local roots.<br><em>Open horizons.</em>'
    }
    content={'index':home(),'references':references(),'licence':licence(),'ventures':ventures(),'catalogue':catalogue(),'join':join()}
    for c in chapters:
        META[c['slug']]=(c['title'],page_headings.get(c['slug'],c['heading']),c['dek'],c['hero']);content[c['slug']]=generic(c)
    if 'vision' not in content:
        META['vision']=('The vision','Women leading.<br><em>Possibility growing.</em>','A plan for women to build useful enterprises, exercise real leadership and share in a more abundant future.','home-hero')
        content['vision']=section('Build the community.<br>Fund the work.<br>Develop the leaders.','<p class="narrow">500 Queens Venture Capital connects women with practical enterprise experience, experienced mentors and the resources to lead. Its Australian starting ambition is at least 500 women, growing through international communities and useful work.</p><p class="narrow">The purpose is Joyful Responsible Abundance: a rewarding life, responsibility for consequences and prosperity that reaches more people. The full planning document sets out leadership development, 120 original enterprise concepts, AI Queens mentorship, community care and the funding model.</p><a class="button" href="references.html">Read the planning material →</a>','light')
    from network import Network
    from equality import build_equality
    helpers={'image':image,'section':section,'card':card,'table':table,'feature':feature}
    network_builder=Network(ROOT,helpers)
    network=network_builder.generate() if args.batch=='full' else None
    if network:
        content['ai-queens']=network['queens'];content['catalogue']=network['catalogue'];content['network']=network['network']
        META['network']=('Explore the network','A world of ideas.<br><em>Your own direction.</em>','Connect Queens, enterprise fields and startup ideas. Shape a pathway around what matters to you.','equality-community')
        for key,value in network['pages'].items():META[key]=value['meta']
        featured_ids=['spark-queen','shield-queen','seed-queen']
        featured=[network_builder.qmap[i] for i in featured_ids if i in network_builder.qmap]
        council_preview=section('Many kinds of women.<br><em>Many ways to lead.</em>','<p>Meet a Council of individual AI Queen characters, with different bodies, ages, backgrounds and ways of seeing the world. Follow each one into her work, learning sessions and connected enterprise ideas.</p><div class="queen-feature-strip">'+''.join(network_builder.queen_card(q) for q in featured)+'</div><div class="actions"><a class="button" href="ai-queens.html">Meet all 24 Queens →</a><a class="button secondary" href="network.html">Build my pathway →</a></div>')
        content['index']=content['index'].replace('<section class="cta-section">',council_preview+'<section class="cta-section">')
    content['designing-equality']=build_equality(helpers,bool(network))
    META['designing-equality']=('Designing equality','What would you<br><em>design differently?</em>','If equality were being designed now, what would women want and need from their environments and systems?','equality-community')
    pages=[s for s in ORDER if s in content and (args.batch=='full' or s in ['index','vision','references','licence'])]
    from readers import build_readers
    reader_pages=build_readers(ROOT,section) if args.batch=='full' else {}
    for key,value in reader_pages.items():META[key]=value['meta']
    globals()['NAV_PAGES']=pages
    for slug in pages:
        body=content[slug]
        if args.batch=='first':
            for target in ORDER:
                if target not in pages:body=body.replace(f'href="{target}.html"','href="references.html"').replace(f'href={target}.html','href=references.html')
        (ROOT/f'{slug}.html').write_text(render(slug,META[slug],body,pages),encoding='utf-8')
    if network:
        for key,value in network['pages'].items():
            (ROOT/f'{key}.html').write_text(render(key,value['meta'],value['body'],value['sequence']),encoding='utf-8')
    for key,value in reader_pages.items():
        (ROOT/f'{key}.html').write_text(render(key,value['meta'],value['body'],value['sequence']),encoding='utf-8')
    META['404']=('Find your way','A new direction<br><em>starts here.</em>','This address does not lead to a current page. Choose a chapter and keep exploring.','library-hero')
    if args.batch=='full':
        lost=render('404',META['404'],section('Where would you like to go?','<div class="actions"><a class="button" href="index.html">Back to the beginning →</a><a class="button secondary" href="references.html">Explore the source library →</a></div>'),pages+['404'])
        lost=lost.replace('<head>','<head><base href="'+BASE+'"><meta name="robots" content="noindex">')
        (ROOT/'404.html').write_text(lost,encoding='utf-8')
    (ROOT/'.nojekyll').touch()
    sitemap_pages=pages+(list(network['pages']) if network else [])+list(reader_pages)
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE+("" if s=="index" else s+".html")}</loc><lastmod>2026-09-23</lastmod></url>' for s in sitemap_pages)+'</urlset>',encoding='utf-8')
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'sitemap.xml\n',encoding='utf-8')
    print(f'Built {len(sitemap_pages)} public pages ({len(pages)} main chapters, {len(network["pages"]) if network else 0} network profiles)')
if __name__=='__main__':main()
