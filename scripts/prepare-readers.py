"""Publish faithful, complete local reading copies without changing source files.

Run with the bundled Python runtime. Office documents use Luke's authorised
desktop LibreOffice in normal-profile headless mode. Markdown is parsed as data,
then reduced to safe semantic HTML. No embedded source instructions are executed.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote, urlparse
import zipfile

from PIL import Image
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
NODE = RUNTIME / 'node/bin/node.exe'
MARKED = RUNTIME / 'node/node_modules/marked/lib/marked.esm.js'
POPPLER = RUNTIME / 'native/poppler/Library/bin/pdftoppm.exe'
SOFFICE = Path('C:/Program Files/LibreOffice/program/soffice.com')
CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
WIDTH = 1400


def run(args, **kwargs):
    result = subprocess.run([str(x) for x in args], check=True, capture_output=True,
                            creationflags=CREATE_NO_WINDOW, **kwargs)
    return result.stdout


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


class SafeHTML(HTMLParser):
    """A narrow allow-list, including tables and code, with no executable HTML."""
    allowed = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li',
               'blockquote', 'pre', 'code', 'strong', 'em', 'del', 's', 'br',
               'hr', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'a', 'sup', 'sub'}
    blocked = {'script', 'style', 'iframe', 'object', 'embed', 'svg', 'math'}
    void = {'br', 'hr'}

    def __init__(self, known_sources):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.stack = []
        self.block_depth = 0
        self.known_sources = known_sources
        self.missing_images = 0

    def safe_url(self, value):
        value = html.unescape(value or '').strip()
        parsed = urlparse(value)
        if parsed.scheme.lower() in {'https', 'http', 'mailto'}:
            return value
        # Only retain relative links when the referenced source exists.
        name = Path(unquote(parsed.path).replace('\\', '/')).name.lower()
        return self.known_sources.get(name)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in self.blocked:
            self.block_depth += 1
            return
        if self.block_depth:
            return
        if tag == 'img':
            target = self.safe_url(attrs.get('src', ''))
            alt = attrs.get('alt', 'Image')
            if target:
                self.parts.append('<p class="source-image-link"><a href="' + html.escape(target, quote=True)
                                  + '">View source image: ' + html.escape(alt) + '</a></p>')
            else:
                self.missing_images += 1
                self.parts.append('<p class="source-placeholder">[Image placeholder in the supplied Markdown source]</p>')
            return
        if tag not in self.allowed:
            return
        rendered = 'h2' if tag == 'h1' else tag
        extra = ''
        if tag == 'a':
            target = self.safe_url(attrs.get('href', ''))
            if target:
                extra = ' href="' + html.escape(target, quote=True) + '" rel="noopener noreferrer"'
            else:
                rendered = 'span'
        if tag == 'ol' and str(attrs.get('start', '')).isdigit():
            extra = ' start="' + attrs['start'] + '"'
        if tag in {'td', 'th'}:
            for key in ('colspan', 'rowspan'):
                if str(attrs.get(key, '')).isdigit():
                    extra += ' ' + key + '="' + attrs[key] + '"'
        if tag == 'code' and re.fullmatch(r'language-[a-zA-Z0-9_-]+', attrs.get('class', '')):
            extra = ' class="' + attrs['class'] + '"'
        self.parts.append('<' + rendered + extra + '>')
        if tag not in self.void:
            self.stack.append((tag, rendered))

    def handle_endtag(self, tag):
        if tag in self.blocked:
            self.block_depth = max(0, self.block_depth - 1)
            return
        if self.block_depth or tag not in self.allowed or tag in self.void:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, rendered in reversed(self.stack[i:]):
                    self.parts.append('</' + rendered + '>')
                del self.stack[i:]
                break

    def handle_data(self, data):
        if not self.block_depth:
            self.parts.append(html.escape(data))

    def result(self):
        for _, tag in reversed(self.stack):
            self.parts.append('</' + tag + '>')
        self.stack.clear()
        return ''.join(self.parts)


def markdown_reader(doc, dest, known_sources):
    source = ROOT / doc['href']
    script = "import {marked} from " + json.dumps(MARKED.as_uri()) + ";import fs from 'node:fs';process.stdout.write(marked.parse(fs.readFileSync(process.argv[1],'utf8'),{gfm:true,breaks:false}));"
    parsed = run([NODE, '--input-type=module', '-e', script, source], timeout=60).decode('utf-8')
    safe = SafeHTML(known_sources)
    safe.feed(parsed)
    rendered = safe.result()
    note = ''
    if safe.missing_images:
        note = '<p class="notice">This source includes image placeholders; all supplied text is shown.</p>'
    fragment = dest / 'index-fragment.html'
    fragment.write_text(note + '<article class="source-markdown">' + rendered + '</article>', encoding='utf-8')
    return {'previewType': 'html', 'pageCount': 1, 'fragment': relative(fragment),
            'files': [relative(fragment)], 'missingSourceImages': safe.missing_images}


def office_pdf(doc, dest):
    source = ROOT / doc['href']
    pdf = dest / 'source.pdf'
    if pdf.exists():
        return pdf
    converted = dest / (source.stem + '.pdf')
    if converted.exists():
        converted.replace(pdf)
        return pdf
    filter_name = 'impress_pdf_Export' if doc['format'] == 'PPTX' else 'writer_pdf_Export'
    options = {'ExportHiddenSlides': {'type': 'boolean', 'value': 'true'}} if doc['format'] == 'PPTX' else {}
    conversion = 'pdf:' + filter_name + (':' + json.dumps(options, separators=(',', ':')) if options else '')
    output = run([SOFFICE, '--headless', '--convert-to', conversion, '--outdir', dest, source], timeout=180)
    if not converted.exists():
        raise RuntimeError('LibreOffice did not create ' + str(converted) + ': ' + output.decode('utf-8', errors='replace'))
    converted.replace(pdf)
    return pdf


def pdf_reader(doc, dest, pdf):
    reader = PdfReader(pdf)
    count = len(reader.pages)
    if doc['format'] == 'PPTX':
        with zipfile.ZipFile(ROOT / doc['href']) as package:
            slides = [n for n in package.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]
        if count != len(slides):
            raise RuntimeError(f'{doc["id"]}: {count} rendered pages for {len(slides)} original slides')
    scratch = ROOT / 'work/readers' / doc['id']
    scratch.mkdir(parents=True, exist_ok=True)
    images = [dest / f'page-{i:03d}.webp' for i in range(1, count + 1)]
    if not all(p.exists() for p in images):
        run([POPPLER, '-scale-to-x', WIDTH, '-scale-to-y', '-1', '-png', pdf, scratch / 'page'], timeout=600)
        pngs = sorted(scratch.glob('page-*.png'), key=lambda p: int(p.stem.split('-')[-1]))
        if len(pngs) != count:
            raise RuntimeError(f'{doc["id"]}: rendered image count differs from PDF')
        for png, target in zip(pngs, images):
            with Image.open(png) as image:
                image.convert('RGB').save(target, 'WEBP', quality=92, method=6)
    word = 'Slide' if doc['format'] == 'PPTX' else 'Page'
    pdf_href = relative(pdf)
    parts = ['<details class="source-page-navigation"><summary>Jump to a ' + word.lower() + '</summary>'
             '<p><a class="button secondary" href="' + html.escape(pdf_href, quote=True) + '">Open PDF reading copy</a></p>'
             '<nav class="source-page-jump" aria-label="Document pages">' + ''.join(
                 f'<a href="#source-page-{i}">{word} {i}</a>' for i in range(1, count + 1)) + '</nav></details>',
             '<div class="source-pages">']
    files = [pdf_href] if doc['format'] != 'PDF' else []
    all_text = []
    for index, (page, image) in enumerate(zip(reader.pages, images), 1):
        path = relative(image)
        files.append(path)
        with Image.open(image) as bitmap:
            width, height = bitmap.size
        if width != WIDTH:
            raise RuntimeError('Unexpected page preview width: ' + path)
        text = page.extract_text() or ''
        all_text.append(f'{word} {index}\n\n{text}')
        parts.append(f'<section class="source-page" id="source-page-{index}"><h2>{word} {index} of {count}</h2>')
        parts.append('<figure><a href="' + path + '" aria-label="Open ' + word.lower() + f' {index} at full size">'
                     '<img src="' + path + '" alt="' + html.escape(f'{word} {index} of {doc["title"]}', quote=True)
                     + f'" width="{width}" height="{height}" loading="lazy" decoding="async"></a>'
                     f'<figcaption><a href="{path}">Open {word.lower()} {index} at full size</a></figcaption></figure>')
        if text.strip():
            parts.append(f'<details class="source-page-text"><summary>Read selectable text for {word.lower()} {index}</summary>'
                         '<p class="notice">Text extracted from this page. Use the page image for its original layout, tables and figures.</p>'
                         '<div class="source-extracted-text">' + html.escape(text).replace('\n', '<br>') + '</div></details>')
        parts.append('</section>')
    parts.append('</div>')
    fragment = dest / 'index-fragment.html'
    fragment.write_text('\n'.join(parts), encoding='utf-8')
    text_path = dest / 'readable-text.txt'
    text_path.write_text('\n\n'.join(all_text), encoding='utf-8')
    files.extend([relative(fragment), relative(text_path)])
    return {'previewType': 'pages', 'pageCount': count, 'fragment': relative(fragment),
            'files': files, 'pdfHref': pdf_href, 'pageWidth': WIDTH}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--only', nargs='*', help='Optional document IDs for a targeted rebuild')
    args = parser.parse_args()
    library = json.loads((ROOT / 'data/reference-library.json').read_text(encoding='utf-8-sig'))
    docs = library['documents']
    known_sources = {}
    for doc in docs:
        for filename in [Path(doc['href']).name, doc['originalFilename']]:
            known_sources[filename.lower()] = 'source-' + doc['id'] + '.html'
    originals = {doc['id']: sha(ROOT / doc['href']) for doc in docs}
    for doc in docs:
        if originals[doc['id']] != doc['sha256']:
            raise RuntimeError('Source hash differs from original archive: ' + doc['id'])
    manifest_path = ROOT / 'data/reference-readers.json'
    existing = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    results = {d['id']: d for d in existing}
    jobs = []
    # LibreOffice conversion is sequential because it shares the normal profile.
    for doc in docs:
        if args.only and doc['id'] not in args.only:
            continue
        dest = ROOT / 'references/previews' / doc['id']
        dest.mkdir(parents=True, exist_ok=True)
        base = {'id': doc['id'], 'slug': 'source-' + doc['id'], 'title': doc['title'].strip(),
                'sourceHref': doc['href'], 'format': doc['format'], 'sourceSha256': originals[doc['id']]}
        if doc['format'] == 'MD':
            results[doc['id']] = {**base, **markdown_reader(doc, dest, known_sources)}
            print(doc['id'] + ': full Markdown reader prepared', flush=True)
        else:
            pdf = ROOT / doc['href'] if doc['format'] == 'PDF' else office_pdf(doc, dest)
            jobs.append((doc, dest, pdf, base))
            print(doc['id'] + ': PDF reading copy ready', flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(pdf_reader, doc, dest, pdf): (doc, base) for doc, dest, pdf, base in jobs}
        for future in concurrent.futures.as_completed(futures):
            doc, base = futures[future]
            results[doc['id']] = {**base, **future.result()}
            print(doc['id'] + ': ' + str(results[doc['id']]['pageCount']) + ' full pages/slides ready', flush=True)
    for doc in docs:
        if sha(ROOT / doc['href']) != originals[doc['id']]:
            raise RuntimeError('An original was changed: ' + doc['id'])
    ordered = [results[d['id']] for d in docs if d['id'] in results]
    manifest_path.write_text(json.dumps(ordered, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Prepared {len(ordered)} complete readers; all {len(docs)} source hashes unchanged.', flush=True)


if __name__ == '__main__':
    main()
