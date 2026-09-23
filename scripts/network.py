"""Connected Queen, enterprise and category pages, built from explicit content records."""
import json, re, html, unicodedata
from pathlib import Path
e=html.escape

def slug(value):
    value=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',value).strip('-')

class Network:
    def __init__(self,root,helpers):
        self.root=root;self.h=helpers
        self.queens=self.load('queens.json',{}).get('queens',[])
        self.enterprises=self.load('enterprise-details-a.json',[])+self.load('enterprise-details-b.json',[])
        self.enterprises.sort(key=lambda x:x['catalogueIndex'])
        self.categories=self.load('category-details-a.json',[])+self.load('category-details-b.json',[])
        self.original=self.load('enterprise-catalogue.json',{})
        cat_order={c['id']:i for i,c in enumerate(self.original.get('categories',[]))}
        self.categories.sort(key=lambda x:cat_order.get(x['id'],99))
        self.projects={p['slug']:p for p in self.load('ventures.json',[])}
        self.qmap={q['id']:q for q in self.queens};self.cmap={c['id']:c for c in self.categories}
        self.by_index={s['catalogueIndex']:s for s in self.enterprises}
        self.pages={};self.records=[]
        for s in self.enterprises:
            s['queenIds']=[self.queen_id(q) for q in s.get('queenIds',[]) if self.queen_id(q) in self.qmap]
        for c in self.categories:
            c['queenIds']=[self.queen_id(q) for q in c.get('queenIds',[]) if self.queen_id(q) in self.qmap]
            c['hero']='categories/'+c['id']
        for q in self.queens:
            q['hero']='queens/'+q['id']
            q['collaborators']=[self.queen_id(i) for i in q.get('collaborators',[]) if self.queen_id(i) in self.qmap and self.queen_id(i)!=q['id']]

    def load(self,name,default):
        path=self.root/'data'/name
        return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default
    def queen_id(self,value):
        value=slug(value)
        if value in ['super-aura','super-queen-aura','super','aura']:return 'super-queen'
        if value in self.qmap:return value
        return value if value.endswith('-queen') else value+'-queen'
    def path(self,kind,item):return f'{kind}-{item["id"]}.html'
    def picture(self,art,alt,cls='card-image'):
        # Category and Council artwork provide honest interim imagery in review batches.
        if not (self.root/'assets/images'/f'{art}.webp').exists():
            art='council-hero' if art.startswith('queens/') else 'ventures-hero'
        return self.h['image'](art,alt,cls)
    def section(self,title,body,style=''):return self.h['section'](title,body,style)
    def paragraphs(self,texts):
        if isinstance(texts,str):texts=[texts]
        return ''.join(f'<p>{e(t)}</p>' for t in texts)
    def bullet(self,items):return '<ul class="useful-list">'+''.join(f'<li>{e(i)}</li>' for i in items)+'</ul>'
    def save(self,kind,item):
        name=item.get('name',item.get('title',''))
        return f'<button class="save-item" type="button" data-save-id="{kind}:{e(item["id"])}" data-save-title="{e(name)}" data-save-href="{self.path(kind,item)}" data-save-kind="{kind}" aria-pressed="false">Add to my pathway +</button>'
    def crumbs(self,items):return '<nav class="context-nav wrap" aria-label="Within the network">'+''.join(f'<a href="{e(href)}">{e(label)}</a><span aria-hidden="true">/</span>' for label,href in items)+'<a href="network.html#my-pathway">My pathway</a></nav>'
    def queen_card(self,q):
        return f'<article class="card queen-card" data-search="{e(q["name"]+" "+q["summary"]+" "+q["tagline"])}" data-category="{e(q["group"])}">'+self.picture(q['hero'],'Fictional AI Queen character: '+q['name'])+f'<div class="card-inner"><span class="tag">{"Civilisation Pillar" if q["group"]=="pillar" else "Cultural Anchor"}</span><a class="card-title" href="{self.path("queen",q)}">{e(q["name"])}</a><p>{e(q["tagline"])}</p>{self.save("queen",q)}</div></article>'
    def startup_card(self,s,art=False):
        c=self.cmap[s['categoryId']]
        return f'<article class="card enterprise-card" data-search="{e(s["title"]+" "+s["oneLine"]+" "+c["title"])}" data-category="{e(c["title"])}">'+(self.picture(c['hero'],'GenAI concept illustration for '+c['title']) if art else '')+f'<div class="card-inner"><a class="tag" href="{self.path("category",c)}">{e(c["title"])}</a><a class="card-title" href="{self.path("startup",s)}">{e(s["title"])}</a><p>{e(s["oneLine"])}</p><p class="stage-label">{e(s["evidence"]["stage"])}</p>{self.save("startup",s)}</div></article>'
    def category_card(self,c):
        count=sum(s['categoryId']==c['id'] for s in self.enterprises)
        return '<article class="card">'+self.picture(c['hero'],'GenAI illustration of '+c['title'])+f'<div class="card-inner"><span class="tag">{count} enterprise directions</span><a class="card-title" href="{self.path("category",c)}">{e(c["title"])}</a><p>{e(c["summary"])}</p>{self.save("category",c)}</div></article>'
    def queen_links(self,ids):return '<div class="grid">'+''.join(self.queen_card(self.qmap[i]) for i in dict.fromkeys(ids) if i in self.qmap)+'</div>'
    def category_links(self,ids):return '<div class="reading-links">'+''.join(f'<a href="{self.path("category",self.cmap[i])}">{e(self.cmap[i]["title"])}</a>' for i in dict.fromkeys(ids) if i in self.cmap)+'</div>'
    def source_links(self,sources):return '<div class="reading-links">'+''.join(f'<a href="{e(s["href"])}">{e(s["title"])}</a>' for s in sources)+'</div>'
    def project_links(self,slugs):
        return '<div class="grid two">'+''.join(self.h['card'](e(self.projects[i]['title']),e(self.projects[i]['summary']),self.projects[i]['href'],tag='Connected public concept') for i in dict.fromkeys(slugs) if i in self.projects)+'</div>'
    def equality_questions(self,category_id):
        questions={
            'simulations-and-robots':['Which tasks do women want help with, and which decisions or human relationships should remain in their hands?','How would women of different bodies, ages, abilities and working conditions test the equipment and service?'],
            'clean-power-systems':['Whose priorities shape reliable energy for homes, care, small businesses and remote work?','How would women share ownership, skilled jobs and decisions about siting, pricing and maintenance?'],
            'closed-loop-food':['What would affordable, nourishing food and a workable caring day look like for the women involved?','Who controls the growing system, land, income and decisions, including in regional or remote communities?'],
            'waste-reclamation':['Whose unpaid work currently keeps materials moving, and how could value and responsibility be shared more fairly?','Would the collection, sorting and workshop design fit different bodies, caring schedules and transport options?'],
            'subterranean-cities':['What would women want to control about light, privacy, movement, public space and caring facilities in a new settlement?','Who can leave, change the design or challenge a decision, and how would that power work in practice?'],
            'extreme-metamaterials':['Who defines the problem this material should solve, and whose exposure or workload needs to be considered?','How would women working in production, using the product and managing its end of life shape the test plan?'],
            'space-industry':['Whose bodies, caring lives and ambitions are considered when designing equipment, teams and time away?','How could women influence mission priorities, work conditions, safety decisions and ownership from the beginning?'],
            'micro-architectures':['Whose everyday experience should shape the research question, intended use and acceptable trade-offs?','How would access to research tools, training, paid work and decisions be shared across the proposed team?'],
            'humanities-and-fun':['What kinds of enjoyment, creativity and connection do the women involved want more room for?','Who controls the story, the platform and the income, and who can participate across different places and bodies?'],
            'market-analysis':['Whose needs are missing from the market data, and how would those women describe value in their own words?','Who can challenge an assumption about women as customers, workers or investors before it shapes a decision?'],
            'aura-of-intelligence':['What work do women want an intelligent tool to support, and what authority should remain with them?','Who controls the data, corrects the system and receives the productivity benefits across languages and locations?']
        }
        return questions.get(category_id,['Which women would use, work in, maintain or live beside this system, and what do they say they want?','What design, ownership or decision-making power would make a meaningful difference to those women?'])
    def equality_section(self,item,category_id):
        return self.section('If equality were being designed now...',self.bullet(item.get('equalityQuestions') or self.equality_questions(category_id))+'<p>Begin with women\'s own experiences across bodies, ages, cultures and places. Invite disagreement and choose a practical change together.</p><a class="text-link" href="designing-equality.html">Create a women-led design brief →</a>','plum')
    def action_band(self,kind,item):
        return '<div class="intro-band"><div class="wrap"><p>Follow the connections. Choose your direction.</p><div class="inline-actions">'+self.save(kind,item)+'<a href="network.html#my-pathway">Open my pathway →</a></div></div></div>'
    def add_page(self,kind,item,heading,dek,hero,body,sequence):
        name=item.get('name',item.get('title'));key=f'{kind}-{item["id"]}'
        self.pages[key]={'meta':(name,heading,dek,hero),'body':body,'sequence':sequence}
        self.records.append({'id':f'{kind}:{item["id"]}','kind':kind,'title':name,'href':key+'.html','summary':dek,'categoryIds':item.get('categoryIds',[item['categoryId']] if item.get('categoryId') else [item['id']] if kind=='category' else []),'queenIds':item.get('queenIds',[]),'art':hero})

    def build_queen(self,q,sequence):
        body=self.crumbs([('AI Queens','ai-queens.html')])+self.action_band('queen',q)
        body+=self.section(q['tagline'],self.paragraphs(q['summary'])+f'<div class="mentor-voice"><p>{e(q["voice"])}</p><span>{e(q["name"])} · fictional AI mentor character</span></div>','light')
        body+=self.section('The perspective she brings.',self.paragraphs([q['role']]+q['approach']))
        body+=self.section('Work through a real decision.','<div class="grid">'+''.join(self.h['card'](e(x['title']),e(x['text'])) for x in q['helpsWith'])+'</div>','plum')
        session=q['session'];steps=''.join(f'<article><span class="number">{i:02d}</span><p>{e(s)}</p></article>' for i,s in enumerate(session['steps'],1))
        body+=self.section(e(session['title']),self.paragraphs(session['context'])+'<div class="journey">'+steps+'</div><div class="callout"><h3>Leave with something useful.</h3>'+self.paragraphs(session['deliverable'])+'</div>'+self.paragraphs(session['review']),'light')
        body+=self.section('Questions to take into the room.',self.bullet(q['questions'])+f'<div class="session-download"><a class="button" href="sessions/{e(q["id"])}.md" download>Download her session guide ↓</a><p>A written preparation guide for your own use with a human mentor or AI assistant.</p></div>')
        body+=self.section('Whose future are we designing?','<p>Ask what the women involved want and need from this environment or system. Bring the Queen\'s perspective to that conversation, with women from the relevant places, backgrounds and ways of living shaping the answers.</p><a class="text-link" href="designing-equality.html">Explore the central equality question →</a>','light')
        related=[s for s in self.enterprises if q['id'] in s.get('queenIds',[])]
        if not related:related=[s for s in self.enterprises if s['categoryId'] in q.get('categoryIds',[])][:6]
        body+=self.section('Ideas she can help you explore.','<p>These are proposed learning connections. Choose a brief, follow its evidence questions and bring the people affected into the work.</p><div class="grid">'+''.join(self.startup_card(s) for s in related[:6])+'</div>'+self.category_links(q.get('categoryIds',[])),'plum')
        body+=self.section('Bring another perspective.',self.queen_links(q.get('collaborators',[])))
        body+=self.section('Keep the judgement human.',self.bullet(q.get('limits',[]))+self.paragraphs(q['sourceNote'])+self.source_links(q.get('sourceLinks',[])),'light')
        self.add_page('queen',q,e(q['name']).replace(' Queen','<br><em>Queen</em>'),q['tagline'],q['hero'],body,sequence)
        session_dir=self.root/'sessions';session_dir.mkdir(exist_ok=True)
        text=f'# A working session with {q["name"]}\n\nFictional AI mentor concept. This is a preparation guide, not a live mentoring service.\n\n## Your starting point\n\nThe decision I need to make:\n\nPeople affected:\n\nEvidence I have:\n\n## {session["title"]}\n\n{session["context"]}\n\n'+ '\n'.join(f'{i}. {s}' for i,s in enumerate(session['steps'],1))+f'\n\n## A useful result\n\n{session["deliverable"]}\n\n## Human review\n\n{session["review"]}\n\n## Questions\n\n'+'\n'.join('- '+t for t in q['questions'])+f'\n\n## Source and role\n\n{q["sourceNote"]}\n\nhttps://auraofintelligence.github.io/500-Queens-VC-2026/{self.path("queen",q)}\n'
        (session_dir/f'{q["id"]}.md').write_text(text,encoding='utf-8')

    def build_startup(self,s,sequence):
        c=self.cmap[s['categoryId']];body=self.crumbs([('All startup ideas','catalogue.html'),(c['title'],self.path('category',c))])+self.action_band('startup',s)
        body+=self.section('The need worth working on.',self.paragraphs(s['need']),'light')
        body+=self.section('What the enterprise could offer.',self.paragraphs(s['offer'])+'<div class="audience-box"><h3>People to build with</h3>'+self.bullet(s['users'])+'</div>')
        pilot=s['firstPilot'];body+=self.section(e(pilot['title']),'<div class="journey">'+''.join(f'<article><span class="number">{i:02d}</span><p>{e(t)}</p></article>' for i,t in enumerate(pilot['steps'],1))+'</div><div class="callout"><h3>The first result</h3>'+self.paragraphs(pilot['deliverable'])+'</div>','plum')
        evidence=s['evidence'];body+=self.section('What needs to be demonstrated.','<p class="stage-label">'+e(evidence['stage'])+'</p><div class="grid">'+self.h['card']('The starting evidence',e(evidence['known']))+self.h['card']('The open question',e(evidence['unknown']))+self.h['card']('The next measurement',e(evidence['nextMeasurement']))+'</div>','light')
        body+=self.section('Build the means to deliver.','<div class="split top"><div><h3>Useful capabilities and resources</h3>'+self.bullet(s['resources'])+'</div><div><h3>A possible business model</h3>'+self.paragraphs(s['businessModel'])+'<h3>A leadership decision to practise</h3>'+self.paragraphs(s['leadershipDecision'])+'</div></div>')
        body+=self.section('People, consequences and decisions.',self.bullet(s['risks']),'plum')
        body+=self.equality_section(s,c['id'])
        body+=self.section('Build your learning council.',self.queen_links(s.get('queenIds',[])))
        related=[self.by_index[i] for i in s.get('relatedIndices',[]) if i in self.by_index and i!=s['catalogueIndex']]
        body+=self.section('Build alongside these ideas.','<div class="grid">'+''.join(self.startup_card(r) for r in related)+'</div>','light')
        if s.get('projectSlugs'):body+=self.section('Follow existing public concept work.',self.project_links(s['projectSlugs']))
        original=self.original['enterprises'][s['catalogueIndex']];source=original.get('source',{})
        body+=self.section('From the original suggestion to a working brief.',self.paragraphs(s['sourceNote'])+f'<p>Original title: <em>{e(original["title"])}</em>. The pilot, business model and learning connections on this page are proposed developments of that original idea.</p>'+self.source_links([{'title':'Original 500 Queens presentation','href':source.get('document','references/documents/500-queens-vc-new-long.pptx')},{'title':'Current planning document','href':'references/documents/queens-venture-capital-planning-document.pdf'}]+s.get('sources',[])),'light')
        self.add_page('startup',s,e(s['title']),s['oneLine'],c['hero'],body,sequence)

    def build_category(self,c,sequence):
        items=[s for s in self.enterprises if s['categoryId']==c['id']]
        body=self.crumbs([('All startup ideas','catalogue.html')])+self.action_band('category',c)
        body+=self.section('A field of work. A shared direction.',self.paragraphs([c['summary'],c['opportunity']]),'light')
        body+=self.section('Start with a useful result.','<div class="journey">'+''.join(f'<article><span class="number">{i:02d}</span><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></article>' for i,t in enumerate(c['startingPath'],1))+'</div>')
        body+=self.section('Explore every enterprise in this field.','<div class="grid two">'+''.join(self.startup_card(s) for s in items)+'</div>','plum')
        body+=self.section('Share capability. Strengthen the whole field.','<div class="split top"><div><h3>What these enterprises can share</h3>'+self.bullet(c['sharedInfrastructure'])+'</div><div><h3>Questions worth bringing together</h3>'+self.bullet(c['questions'])+'</div></div>','light')
        body+=self.equality_section(c,c['id'])
        body+=self.section('Meet the mentors for this direction.',self.queen_links(c.get('queenIds',[])))
        if c.get('projectSlugs'):body+=self.section('Connect the field to public project work.',self.project_links(c['projectSlugs']),'plum')
        body+=self.section('Follow the source.',self.paragraphs(c['sourceNote'])+self.source_links([{'title':'The original startup catalogue','href':'references/documents/500-queens-vc-new-long.pptx'},{'title':'The full source library','href':'references.html'}]+c.get('sources',[])),'light')
        self.add_page('category',c,e(c['title']),c['summary'],c['hero'],body,sequence)

    def queen_hub(self):
        body=self.section('Twenty-four Queens.<br>Many ways to lead.','<p>Each Queen is a distinct fictional AI mentor with her own perspective, working style and place in the enterprise network. Explore her profile, follow the ideas she connects with, and use her session guide to prepare a real decision.</p><p>The Council includes women of different ages, body sizes, appearances and styles. Glamour, practicality, curiosity and authority can belong to any of them. Their role is to support your judgement alongside experienced people.</p><div class="actions"><a class="button" href="network.html">Explore the connections →</a><a class="button secondary" href="network.html#my-pathway">Build my pathway →</a></div>','light')
        body+='<section class="section"><div class="wrap" data-filter-group="Queens"><h2>Find a perspective that speaks to you.</h2><div class="filter-bar"><div class="field"><label for="queen-search">Search expertise, character or name</label><input type="search" id="queen-search" placeholder="Try prototypes, storytelling or governance"></div><div class="field"><label for="queen-group">Explore the Council</label><select id="queen-group"><option value="">All 24 Queens</option><option value="pillar">Civilisation Pillar Queens</option><option value="cultural">Cultural Anchor Queens</option></select></div></div><p class="filter-count" data-result-count aria-live="polite"></p><div class="grid">'+''.join(self.queen_card(q) for q in self.queens)+'</div><p class="no-results" hidden>No Queens match. Try a broader search.</p></div></section>'
        body+=self.section('Different roles. Shared responsibility.','<div class="grid two">'+self.h['card']('Civilisation Pillar Queens','Twelve practical perspectives on enterprise, from energy and water to law, manufacturing, culture and long-term strategy.')+self.h['card']('Cultural Anchor Queens','Twelve creative perspectives on identity, belonging and working across differences. Cultural authority and knowledge remain with the people involved.')+'</div><p>The profiles expand the original brief into proposed character and learning designs. They introduce a mentoring system to develop, with downloadable preparation guides. A live AI conversation service is not connected to this website.</p>','light')
        return body
    def catalogue_hub(self):
        body=self.section('Every idea has<br>a place to begin.','<p>Explore eleven connected fields and all 120 original startup suggestions. Every idea now has a practical concept brief: people it could help, a first pilot, evidence questions, resources, leadership decisions and connections to other enterprises and Queens.</p><p>The original catalogue mixes possible near-term businesses with engineering challenges and speculative research. The evidence section on each page makes that distinction visible.</p>','light')
        body+=self.section('Choose a field of possibility.','<div class="grid">'+''.join(self.category_card(c) for c in self.categories)+'</div>')
        body+='<section class="section plum"><div class="wrap" data-filter-group="original ideas"><h2>Explore all 120 directions.</h2><div class="filter-bar"><div class="field"><label for="catalogue-search">Search the startup ideas</label><input type="search" id="catalogue-search" placeholder="Try care, water, space or materials"></div><div class="field"><label for="catalogue-sector">Choose a category</label><select id="catalogue-sector"><option value="">All eleven categories</option>'+''.join(f'<option>{e(c["title"])}</option>' for c in self.categories)+'</select></div></div><p class="filter-count" data-result-count aria-live="polite"></p><div class="catalogue-grid">'+''.join(self.startup_card(s) for s in self.enterprises)+'</div><p class="no-results" hidden>No ideas match. Try another category or a shorter phrase.</p></div></section>'
        return body
    def network_hub(self):
        body=self.section('Follow an idea.<br>Find your people and your next step.','<p>Queens, enterprise categories and startup ideas belong to one connected learning network. Choose a field to see relevant mentors and enterprise briefs. Add anything that interests you to your own pathway below.</p><p>Your pathway stays in this browser. Download a copy when you want to keep it or share it. There are no member accounts or public profiles in this planning tool.</p>','light')
        body+='<section class="section"><div class="wrap"><h2>Find the connections.</h2><div class="field narrow"><label for="network-category">Choose a field to explore</label><select id="network-category"><option value="">Choose a category</option>'+''.join(f'<option value="{e(c["id"])}">{e(c["title"])}</option>' for c in self.categories)+'</select></div><div class="network-layout" id="network-explorer" aria-live="polite"><p class="network-empty">Choose a field to reveal its Queens, shared capabilities and startup ideas.</p></div><noscript><p>Explore the same connections through the <a href="ai-queens.html">Queen profiles</a> and <a href="catalogue.html">category pages</a>.</p></noscript></div></section>'
        body+='<section class="section plum" id="my-pathway"><div class="wrap"><h2>Your pathway. Your choices.</h2><p>Add Queens, categories and startup ideas as you explore. Nothing is chosen for you.</p><p id="pathway-storage-status" class="notice" role="status"></p><div class="pathway-saved" id="pathway-saved"><p>Your pathway is empty. Visit a Queen or enterprise page and choose “Add to my pathway”.</p></div><form id="network-plan" class="plan-form"><div class="field"><label for="plan-problem">The problem or possibility I care about</label><textarea id="plan-problem" name="problem" rows="3"></textarea></div><div class="field"><label for="plan-people">People I would want to learn from or work with</label><textarea id="plan-people" name="people" rows="3"></textarea></div><div class="field"><label for="plan-test">The smallest useful first test</label><textarea id="plan-test" name="test" rows="3"></textarea></div><div class="field"><label for="plan-support">Skills, resources and support I would need</label><textarea id="plan-support" name="support" rows="3"></textarea></div><div class="field"><label for="plan-decision">The next decision and evidence I need</label><textarea id="plan-decision" name="decision" rows="3"></textarea></div></form><div class="actions"><button class="button" id="export-pathway" type="button">Download my pathway ↓</button><button class="button secondary" id="clear-pathway" type="button">Clear this pathway</button></div><p class="notice" id="pathway-export-status" role="status"></p></div></section>'
        body+=self.section('A useful next conversation.','<p>Take your pathway to someone with relevant experience. Agree a first result, who needs to be involved, what it will cost and when to review it. The site helps you prepare; the relationships and decisions are yours.</p><a class="button" href="join.html">Find your way into the proposal →</a>','light')
        return body
    def generate(self):
        if not self.queens or len(self.enterprises)!=120 or len(self.categories)!=11:return None
        qseq=['queen-'+q['id'] for q in self.queens];cseq=['category-'+c['id'] for c in self.categories]
        for q in self.queens:self.build_queen(q,qseq)
        for c in self.categories:self.build_category(c,cseq)
        for s in self.enterprises:
            seq=['startup-'+i['id'] for i in self.enterprises if i['categoryId']==s['categoryId']]
            self.build_startup(s,seq)
        network={'records':self.records,'categories':[{'id':c['id'],'title':c['title'],'summary':c['summary'],'href':self.path('category',c),'queenIds':c['queenIds'],'sharedInfrastructure':c['sharedInfrastructure']} for c in self.categories],'queens':[{'id':q['id'],'title':q['name'],'summary':q['tagline'],'href':self.path('queen',q),'categoryIds':q['categoryIds'],'group':q['group']} for q in self.queens],'startups':[{'id':s['id'],'title':s['title'],'summary':s['oneLine'],'href':self.path('startup',s),'categoryId':s['categoryId'],'queenIds':s['queenIds'],'stage':s['evidence']['stage']} for s in self.enterprises]}
        (self.root/'data/network.json').write_text(json.dumps(network,ensure_ascii=False,indent=2),encoding='utf-8')
        return {'pages':self.pages,'queens':self.queen_hub(),'catalogue':self.catalogue_hub(),'network':self.network_hub(),'data':network}
