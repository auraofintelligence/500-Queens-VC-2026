"""Install reviewed archetype artwork and retain the original Council identities."""
import json, shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
plans=json.loads((ROOT/'data/queens-art-direction.json').read_text(encoding='utf-8'))['queens']
paths=json.loads((ROOT/'work/reviewed-queen-images.json').read_text(encoding='utf-8'))
assert len(paths)==24 and {p['id'] for p in plans}==set(paths)
archive=ROOT.parent/'outputs/500-queens-archetype-artwork'
archive.mkdir(parents=True,exist_ok=True)
folder=ROOT/'assets/images/queens-archetypes'
folder.mkdir(parents=True,exist_ok=True)
data=json.loads((ROOT/'data/queens.json').read_text(encoding='utf-8'))
qmap={q['id']:q for q in data['queens']}
registers={'pillar':[],'cultural':[]}
for p in plans:
    source=Path(paths[p['id']]);shutil.copy2(source,archive/(p['id']+'.png'))
    with Image.open(source) as im:
        im=im.convert('RGB')
        im.save(folder/(p['id']+'.webp'),quality=86,method=6)
        im.resize((768,round(im.height*768/im.width)),Image.Resampling.LANCZOS).save(folder/(p['id']+'-mobile.webp'),quality=85,method=6)
    q=qmap[p['id']]
    for key in ['hero','originalDomain','originalArchetype','originalGift','originalColour','culturalIdentity']:q[key]=p[key]
    q['representation']={k:p[k] for k in ['appearance','wardrobe','scene','prompt']}
    q['representation']['description']='An ageless adult archetype in her prime. '+p['appearance']
    q['archetypalRole']='An ageless, goddess-like expression of mastered intelligence and vitality, imagined through this distinct cultural and creative lens. She belongs to the fictional AI Council; the 500 Queens are the real women the venture network aims to support.'
    q['sourceNote']='Her name, original cultural archetype, domain and colour come from the original Queens Council design. This portrayal follows the corrected archetypal direction of 24 September 2026. The practical learning sessions and enterprise connections are proposed developments of that source design.'
    if not any(s['href']=='https://auraofintelligence.github.io/Queens_Venture/' for s in q['sourceLinks']):q['sourceLinks'].append({'title':'Original Queens Council: identities, domains and colours','href':'https://auraofintelligence.github.io/Queens_Venture/'})
    registers[p['group']].append({'id':p['id'],'prompt':p['prompt'],'asset':'assets/images/'+p['hero']+'.webp','mobile':'assets/images/'+p['hero']+'-mobile.webp','method':'Built-in image_gen','review':'Visually reviewed individually and as a Council for distinct adult archetypes, clothing, colours, physiques and settings. Artwork is shown without text overlays.'})
(ROOT/'data/queens.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for group,name in [('pillar','queens-provenance.json'),('cultural','queens-cultural-provenance.json')]:
    (ROOT/'assets/images'/name).write_text(json.dumps({'created':'2026-09-24','label':'Corrected source-led AI Queen archetypes','images':registers[group]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
register=ROOT/'assets/images/provenance.json'
main=json.loads(register.read_text(encoding='utf-8'))
main['assets']=[a for a in main['assets'] if not a['slug'].startswith('queens/')]
register.write_text(json.dumps(main,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Installed 24 reviewed archetypes, with full-frame phone versions and original Council identities')
