"""Combine the original and expansion artwork registers without private source paths."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'assets/images'
register=root/'provenance.json'
main=json.loads(register.read_text(encoding='utf-8'))
assets={a['slug']:a for a in main['assets']}
for path in sorted(root.glob('*provenance*.json')):
    if path==register:continue
    data=json.loads(path.read_text(encoding='utf-8-sig'))
    for a in data.get('assets',[]):assets[a['slug']]=a
    for a in data.get('images',[]):
        files=[a[k].removeprefix('assets/images/') for k in ['asset','mobile']]
        name=files[0].removesuffix('.webp')
        assets[name]={'slug':name,'files':files,'prompt':a['prompt'],'tool':a.get('method','Built-in image_gen'),'review':a.get('review',''),'disclosure':'GenAI concept artwork depicting fictional people and proposed environments.'}
main['assets']=list(assets.values())
main['updated']='2026-09-23'
register.write_text(json.dumps(main,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Registered {len(assets)} original artworks and their phone versions')
