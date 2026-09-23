"""Read-only public deployment verification, including original download bytes."""
import concurrent.futures,hashlib,json,sys
from pathlib import Path
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1]
BASE='https://auraofintelligence.github.io/500-Queens-VC-2026/'
def fetch(path):
    request=Request(BASE+path,headers={'User-Agent':'500Queens-public-site-check/1.0','Cache-Control':'no-cache'})
    with urlopen(request,timeout=60) as response:return response.status,response.read()
def check_page(path):
    status,body=fetch(path)
    if status!=200 or b'<h1>' not in body:raise ValueError(f'Page failed: {path}')
    if body.replace(b'\r\n',b'\n')!=(ROOT/path).read_bytes().replace(b'\r\n',b'\n'):raise ValueError(f'Page is not the latest local build: {path}')
    return path
def check_document(doc):
    status,body=fetch(doc['href'])
    if status!=200 or hashlib.sha256(body).hexdigest()!=doc['sha256']:raise ValueError(f'Original download mismatch: {doc["title"]}')
    return doc['title']
def check_asset(path):
    status,body=fetch(path)
    if status!=200 or not body:raise ValueError(f'Asset failed: {path}')
    return path
def main():
    pages=[p.name for p in ROOT.glob('*.html') if p.name!='404.html']
    lib=json.loads((ROOT/'data/reference-library.json').read_text(encoding='utf-8'))
    arts=json.loads((ROOT/'assets/images/provenance.json').read_text(encoding='utf-8'))
    assets=['assets/images/'+f for a in arts['assets'] for f in a['files']]
    assets+=['assets/brand/favicon.ico','assets/brand/500-queens-original.png','assets/site.css?v=20260923-network-3','assets/site.js?v=20260923-network-3','assets/network.css?v=20260923-network-3','assets/network.js?v=20260923-network-3','assets/readers.css?v=20260923-network-3','assets/heroes.css?v=20260923-network-3','assets/site-map.css?v=20260923-network-3','data/network.json']
    readers=ROOT/'data/reference-readers.json'
    if readers.exists():
        assets += list(dict.fromkeys(f for r in json.loads(readers.read_text(encoding='utf-8')) for f in r['files']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(check_page,pages));print(f'PASS: {len(pages)} public pages return HTTP 200')
        list(pool.map(check_document,lib['documents']));print(f'PASS: all {len(lib["documents"])} public downloads match supplied original SHA-256 checksums')
        list(pool.map(check_asset,assets));print(f'PASS: {len(assets)} public image and interface assets return HTTP 200')
    print('Public deployment verified')
if __name__=='__main__':main()
