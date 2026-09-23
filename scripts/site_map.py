"""Build the visual site map from the site's actual navigation records."""
import html
import json
from collections import defaultdict
from pathlib import Path


def build_site_map(root, helpers):
    root = Path(root)
    e = html.escape

    def read(name, default):
        path = root / 'data' / name
        return json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else default

    network = read('network.json', {})
    records = network.get('records', [])
    record_map = {record['id']: record for record in records}
    queens = network.get('queens', [])
    categories = network.get('categories', [])
    startups = network.get('startups', [])
    library = read('reference-library.json', {})
    documents = library.get('documents', [])
    readers = read('reference-readers.json', [])
    if isinstance(readers, dict):
        readers = readers.get('records', readers.get('documents', []))
    reader_map = {reader.get('sourceHref', ''): reader for reader in readers}
    image = helpers.get('image')

    def artwork(name, alt, css_class):
        if image:
            return image(name, alt, css_class)
        return ('<picture class="' + css_class + '"><img src="assets/images/' +
                e(name, quote=True) + '.webp" alt="' + e(alt, quote=True) +
                '" width="1536" height="1024" loading="lazy" decoding="async"></picture>')

    def count(value, label):
        return f'<span class="map-count"><strong>{value}</strong> {e(label)}</span>'

    def heading(anchor, title, description, count_text):
        return (f'<div class="map-branch-head"><span class="map-junction" aria-hidden="true"></span>'
                f'<div><h2 id="{anchor}-heading">{e(title)}</h2><p>{e(description)}</p></div>'
                f'<span class="map-branch-total">{e(count_text)}</span></div>')

    chapter_groups = [
        ('Begin with purpose', [
            ('index', 'Home', 'The opening invitation'),
            ('vision', 'The vision', 'The ambition and its purpose'),
            ('designing-equality', 'Designing equality', 'What women want to shape'),
            ('community', 'The community', 'Find people and useful work')]),
        ('Lead and learn', [
            ('leadership', 'Develop leadership', 'Practise real responsibility'),
            ('ai-queens', 'Meet the AI Queens', 'Individual mentors and learning routes'),
            ('shared-intelligence', 'Shared intelligence', 'Tools, learning and collaboration'),
            ('care', 'Care and reciprocity', 'Recognise contribution and connection')]),
        ('Build your direction', [
            ('ventures', 'Connected projects', '18 wider public concepts'),
            ('catalogue', 'The enterprise catalogue', 'Explore the original 120 ideas'),
            ('network', 'Explore the network', 'Keep your own pathway'),
            ('capital', 'Capital and opportunity', 'How backing could support the work')]),
        ('Connect and grow', [
            ('brisbane', 'Brisbane beginnings', 'A proposed shared home'),
            ('global', 'Wider horizons', 'Local leadership, global connections'),
            ('join', 'Find your place', 'Bring an interest or contribution'),
            ('references', 'The source library', 'Read the planning and source material'),
            ('licence', 'The licence', 'How this work can be used')])]

    chapter_cards = []
    for title, items in chapter_groups:
        links = ''.join(f'<li><a href="{slug}.html"><strong>{e(label)}</strong>'
                        f'<span>{e(description)}</span></a></li>' for slug, label, description in items)
        chapter_cards.append(f'<article class="map-chapter"><h3>{e(title)}</h3>'
                             f'<ul class="map-child-links">{links}</ul></article>')

    queen_groups = []
    for group, title, description in [
        ('pillar', 'The Civilisation Pillars', 'Archetypes of ideas, care, science, enterprise and leadership.'),
        ('cultural', 'The Cultural Anchor Queens', 'Twelve source-defined cultural archetypes, each with her own identity and presence.')]:
        members = [queen for queen in queens if queen.get('group') == group]
        faces = ''.join(artwork(record_map.get('queen:' + queen['id'], {}).get('art', 'queens/' + queen['id']),
                                '', 'map-peek-image') for queen in members[:3])
        cards = []
        for queen in members:
            art = record_map.get('queen:' + queen['id'], {}).get('art', 'queens/' + queen['id'])
            cards.append(f'<a class="map-queen" href="{e(queen["href"], quote=True)}">' +
                         artwork(art, 'GenAI portrait of ' + queen['title'], 'map-portrait') +
                         f'<span class="map-queen-copy"><strong>{e(queen["title"])}</strong>'
                         f'<span>{e(queen["summary"])}</span></span></a>')
        queen_groups.append(f'<details class="map-queen-group"><summary><span class="map-peek" aria-hidden="true">{faces}</span>'
                            f'<span class="map-summary-copy"><strong>{e(title)}</strong><span>{e(description)}</span></span>'
                            f'<span class="map-summary-count">{len(members)} Queens</span></summary>'
                            f'<div class="map-queen-grid">{"".join(cards)}</div></details>')

    category_cards = []
    for category in categories:
        members = [startup for startup in startups if startup.get('categoryId') == category['id']]
        art = record_map.get('category:' + category['id'], {}).get('art', 'categories/' + category['id'])
        children = ''.join(f'<li><a href="{e(startup["href"], quote=True)}">{e(startup["title"])}</a></li>' for startup in members)
        category_cards.append('<article class="map-category">' +
                              f'<a class="map-category-link" href="{e(category["href"], quote=True)}">' +
                              artwork(art, 'GenAI concept artwork for ' + category['title'], 'map-category-image') +
                              f'<h3>{e(category["title"])}</h3><span>Explore this field <span aria-hidden="true">→</span></span></a>'
                              f'<details class="map-startup-list"><summary>Show {len(members)} startup ideas</summary>'
                              f'<ul class="map-child-links">{children}</ul></details></article>')

    source_groups = defaultdict(list)
    for document in documents:
        reader = reader_map.get(document['href'])
        href = reader['slug'] + '.html#read' if reader else document['href']
        label = 'Read online' if reader else 'Open original'
        source_groups[document.get('category', 'Source material')].append(
            f'<li><a href="{e(href, quote=True)}"><strong>{e(document["title"].strip())}</strong>'
            f'<span>{label} · {e(document["format"])}</span></a></li>')
    sources = ''.join(f'<details class="map-source-group"><summary><span>{e(title)}</span>'
                      f'<span class="map-summary-count">{len(items)} references</span></summary>'
                      f'<ul class="map-child-links">{"".join(items)}</ul></details>' for title, items in source_groups.items())

    body = '<div class="visual-site-map">'
    body += ('<section class="map-overview section-tight" aria-labelledby="map-start"><div class="wrap">'
             '<div class="map-root"><a href="index.html"><img src="assets/brand/favicon.png" alt="" width="64" height="64">'
             '<span><strong id="map-start">500 Queens Venture Capital</strong><span>One shared beginning. Many possible paths.</span></span></a></div>'
             '<nav class="map-branches" aria-label="Site map branches">'
             '<a href="#map-chapters"><strong>The story</strong>' + count(17, 'main chapters') + '<span>Understand the vision and find your place.</span></a>'
             '<a href="#map-queens"><strong>The Queens</strong>' + count(len(queens), 'individual mentors') + '<span>Meet the characters and their work.</span></a>'
             '<a href="#map-enterprises"><strong>The enterprises</strong>' + count(len(startups), 'startup ideas') + '<span>Follow a field into its possibilities.</span></a>'
             '<a href="#map-sources"><strong>The source library</strong>' + count(len(documents), 'original references') + '<span>Read the material behind the proposal.</span></a>'
             '</nav><p class="map-instruction">Follow a branch, open a group, or choose a page. Each Queen and enterprise links onwards into the wider network.</p>'
             '</div></section>')
    body += ('<section class="map-section" id="map-chapters" aria-labelledby="map-chapters-heading"><div class="wrap map-section-inner">' +
             heading('map-chapters', 'The story', 'A connected introduction to the vision, people and practical work.', '17 chapters') +
             '<div class="map-chapter-grid">' + ''.join(chapter_cards) + '</div></div></section>')
    body += ('<section class="map-section" id="map-queens" aria-labelledby="map-queens-heading"><div class="wrap map-section-inner">' +
             heading('map-queens', 'The Queens', 'Open either council to see every individual portrait and profile.', f'{len(queens)} profiles') +
             '<div class="map-councils">' + ''.join(queen_groups) + '</div><p class="map-section-link"><a href="ai-queens.html">Meet the full Council <span aria-hidden="true">→</span></a></p></div></section>')
    body += ('<section class="map-section" id="map-enterprises" aria-labelledby="map-enterprises-heading"><div class="wrap map-section-inner">' +
             heading('map-enterprises', 'The enterprises', 'Each field has its own guide. Open a branch to find all its individual startup pages.', f'{len(categories)} fields · {len(startups)} ideas') +
             '<div class="map-category-grid">' + ''.join(category_cards) + '</div>'
             '<div class="map-network-bridge"><div><h3>Keep exploring the connections.</h3><p>Bring Queens and ideas together in your own pathway, or visit the 18 wider public project concepts.</p></div>'
             '<div class="actions"><a class="button" href="network.html">Explore the network →</a><a class="button secondary" href="ventures.html">Connected projects →</a></div></div></div></section>')
    body += ('<section class="map-section" id="map-sources" aria-labelledby="map-sources-heading"><div class="wrap map-section-inner">' +
             heading('map-sources', 'The source library', 'Open a collection to explore the complete supplied reference material.', f'{len(documents)} references') +
             '<div class="map-source-grid">' + sources + '</div><p class="map-section-link"><a href="references.html">Visit the full source library <span aria-hidden="true">→</span></a></p></div></section>')
    body += '<div class="map-return wrap"><a href="#map-start">Back to the map beginning ↑</a></div></div>'
    return body
