"""Validate the built public files and unchanged reference archive."""
import hashlib,json,re,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
errors=[]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.altless=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1':self.h1+=1
        if 'id' in attrs:self.ids.add(attrs['id'])
        if tag=='img' and 'alt' not in attrs:self.altless+=1
        for attr in ['href','src','srcset']:
            if attrs.get(attr):self.links.append(attrs[attr].split()[0])
pages={}
for path in ROOT.glob('*.html'):
    text=path.read_text(encoding='utf-8');p=Parser();p.feed(text);pages[path.name]=p
    if p.h1!=1:errors.append(f'{path.name}: {p.h1} H1 headings')
    if p.altless:errors.append(f'{path.name}: missing alt text')
    if not path.name.startswith('source-') and re.search(r'[\u2013\u2014]',text):errors.append(f'{path.name}: long dash punctuation')
    if 'Previous page' not in text or 'Next page' not in text:errors.append(f'{path.name}: missing page sequence')
    if 'Back to top' not in text:errors.append(f'{path.name}: missing top control')
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=ROOT/unquote(u.path) if u.path else path
        if not target.exists():errors.append(f'{path.name}: missing {link}')
for name,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if not u.scheme and u.fragment:
            target=unquote(u.path) or name
            if target in pages and u.fragment not in pages[target].ids:errors.append(f'{name}: missing anchor {link}')
lib=json.loads((ROOT/'data/reference-library.json').read_text())
for doc in lib['documents']:
    path=ROOT/doc['href']
    if hashlib.sha256(path.read_bytes()).hexdigest()!=doc['sha256']:errors.append(f'Reference changed: {path.name}')
catalogue=json.loads((ROOT/'data/enterprise-catalogue.json').read_text())
if len(catalogue['enterprises'])!=120:errors.append('Expected 120 original enterprise ideas')
if len(lib['documents'])!=27:errors.append('Expected 27 original documents')
if len(lib['websites'])!=15:errors.append('Expected 15 supplied sites')
for path in (ROOT/'data').glob('*.json'):
    if re.search(r'C:[/\\]|file://',path.read_text(encoding='utf-8')):errors.append(f'Local path exposed: {path.name}')
main_pages=[name for name in pages if name in ['index.html','vision.html','community.html','leadership.html','ai-queens.html','ventures.html','catalogue.html','shared-intelligence.html','care.html','capital.html','brisbane.html','global.html','join.html','references.html','licence.html']]
if len(main_pages)>=15:
    hero_paths=[]
    for name in main_pages:
        text=(ROOT/name).read_text(encoding='utf-8')
        match=re.search(r'class="hero-bg".*?<img src="([^"]+)"',text)
        if not match:errors.append(f'{name}: missing generated full-width hero')
        else:hero_paths.append(match.group(1))
    if len(set(hero_paths))!=15:errors.append('Expected a distinct GenAI hero for each of the 15 main pages')
    provenance=json.loads((ROOT/'assets/images/provenance.json').read_text(encoding='utf-8'))
    if len(provenance['assets'])<15:errors.append('Expected provenance for at least the 15 original artworks')
    for asset in provenance['assets']:
        for name in asset['files']:
            if not (ROOT/'assets/images'/name).exists():errors.append(f'Missing artwork file: {name}')
font_css=(ROOT/'assets/fonts/fonts.css')
if font_css.exists():
    for name in re.findall(r'url\(([^)]+)\)',font_css.read_text(encoding='utf-8')):
        if not (font_css.parent/name).exists():errors.append(f'Missing bundled font: {name}')
if errors:print('\n'.join(errors));sys.exit(1)
print(f'PASS: {len(pages)} pages; local links and anchors; image alt text; page navigation; 27 original checksums; 120 concepts; 15 supplied websites.')
