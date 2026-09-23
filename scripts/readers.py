"""Wrap full source previews in the public site's navigation and optional downloads."""
import html,json
e=html.escape

def build_readers(root,section):
    register=root/'data/reference-readers.json'
    if not register.exists():return {}
    records=json.loads(register.read_text(encoding='utf-8-sig'))
    pages={};sequence=[r['slug'] for r in records]
    for r in records:
        fragment=(root/r['fragment']).read_text(encoding='utf-8')
        count=r.get('pageCount',0)
        detail=f'{count} slides' if r['format']=='PPTX' else f'{count} pages' if r['format']!='MD' and count else 'Full document'
        body='<nav class="context-nav wrap" aria-label="Source library"><a href="references.html#documents">All references</a><span aria-hidden="true">/</span><a href="#read">Read online</a></nav>'
        body+='<section class="section light" id="read"><div class="wrap"><div class="reader-toolbar"><div><h2>Read the source.</h2><p>'+e(r['format'])+' original · '+detail+'</p></div><a class="button" href="'+e(r['sourceHref'])+'" download>Download original '+e(r['format'])+' ↓</a></div><p class="notice">Original source material, including its historical dates and proposals.</p>'
        body+='<div class="source-reader">'+fragment+'</div></div></section>'
        body+=section('Keep exploring.','<div class="actions"><a class="button" href="references.html#documents">Back to the library →</a><a class="button secondary" href="'+e(r['sourceHref'])+'" download>Download original '+e(r['format'])+' ↓</a></div>')
        title=r['title'].strip()
        pages[r['slug']]={'meta':(title,e(title),'Read the complete supplied reference online, or download the original file.','library-hero'),'body':body,'sequence':sequence}
    return pages
