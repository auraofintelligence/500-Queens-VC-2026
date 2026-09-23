"""Check the actual network records, connections, source fidelity and generated pages."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
def strings(v):
    if isinstance(v,str):yield v
    elif isinstance(v,list):
        for x in v:yield from strings(x)
    elif isinstance(v,dict):
        for x in v.values():yield from strings(x)
errors=[]
qs=load('queens.json')['queens'];es=load('enterprise-details-a.json')+load('enterprise-details-b.json');cs=load('category-details-a.json')+load('category-details-b.json');original=load('enterprise-catalogue.json');network=load('network.json')
projects={p['slug'] for p in load('ventures.json')}
qid={q['id'] for q in qs};cid={c['id'] for c in cs};sid={s['id'] for s in es};indices={s['catalogueIndex'] for s in es}
for actual,wanted,label in [(len(qs),24,'Queens'),(len(qid),24,'unique Queen IDs'),(len(es),120,'enterprise briefs'),(len(sid),120,'unique enterprise IDs'),(len(cs),11,'categories'),(len(cid),11,'unique category IDs')]:
    if actual!=wanted:errors.append(f'{label}: expected {wanted}, found {actual}')
if indices!=set(range(120)):errors.append('Original catalogue coverage is incomplete')
for item in es+cs:
    for q in item.get('queenIds',[]):
        if q not in qid:errors.append(f'Unknown raw Queen ID {q} in {item["id"]}')
    for p in item.get('projectSlugs',[]):
        if p not in projects:errors.append(f'Unknown connected project {p} in {item["id"]}')
for s in es:
    if len(s.get('equalityQuestions',[]))<2:errors.append(f'Missing venture-specific equality questions: {s["title"]}')
    original_record=original['enterprises'][s['catalogueIndex']]
    if s['title'] not in [original_record['title'],original_record.get('planningTitle')]:errors.append(f'Original title changed: {s["title"]}')
    if s['categoryId']!=original_record['categoryId']:errors.append(f'Original category changed: {s["title"]}')
    if len(s['firstPilot']['steps'])<3:errors.append(f'Insufficient pilot detail: {s["title"]}')
    if len(' '.join(strings({k:s[k] for k in ['need','offer','users','firstPilot','evidence','resources','businessModel','leadershipDecision','risks']})).split())<240:errors.append(f'Thin enterprise brief: {s["title"]}')
    for idx in s['relatedIndices']:
        if idx not in indices:errors.append(f'Unknown related enterprise: {idx}')
for q in qs:
    if len(q['helpsWith'])<2 or len(q['session']['steps'])<3:errors.append(f'Incomplete Queen learning profile: {q["id"]}')
    for c in q['categoryIds']:
        if c not in cid:errors.append(f'Unknown category {c} from {q["id"]}')
    if not (ROOT/'sessions'/f'{q["id"]}.md').exists():errors.append(f'Missing Queen session: {q["id"]}')
for c in cs:
    expected=next(x['count'] for x in original['categories'] if x['id']==c['id'])
    if sum(s['categoryId']==c['id'] for s in es)!=expected:errors.append(f'Category coverage changed: {c["id"]}')
if len(network['records'])!=155:errors.append('Expected 155 linked network records')
for r in network['records']:
    p=ROOT/r['href']
    if not p.exists():errors.append(f'Missing profile page: {r["href"]}');continue
    text=p.read_text(encoding='utf-8')
    if 'designing-equality.html' not in text:errors.append(f'Missing equality focus: {r["href"]}')
    if 'data-save-id' not in text:errors.append(f'Missing pathway action: {r["href"]}')
    for q in r['queenIds']:
        if q not in qid:errors.append(f'Unknown Queen link: {q}')
    if '--final-art' in sys.argv:
        for suffix in ['', '-mobile']:
            if not (ROOT/'assets/images'/f'{r["art"]}{suffix}.webp').exists():errors.append(f'Missing artwork: {r["art"]}{suffix}')
for path in (ROOT/'assets/images').glob('*provenance*.json'):
    if re.search(r'C:[/\\]|file://',path.read_text(encoding='utf-8')):errors.append(f'Private local path in public provenance: {path.name}')
if errors:print('\n'.join(errors));sys.exit(1)
print('PASS: 24 developed Queens; 11 complete categories; 120 substantive source-matched enterprise briefs; 155 connected pages; equality and planning links; session downloads'+('; all individual and category artwork' if '--final-art' in sys.argv else ''))
