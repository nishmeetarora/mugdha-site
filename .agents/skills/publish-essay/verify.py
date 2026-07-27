#!/usr/bin/env python3
"""
Fidelity gate for essay pages.

Walks the markdown source and the built page in parallel and proves the page
carries the source text unchanged. Formatting is allowed to split a source
paragraph across display blocks; it is never allowed to drop words, reword
them, reorder them, or merge two source paragraphs into one block.

    python3 verify.py <slug>
    python3 verify.py thinking/foo.md thinking/foo.html

Exit 0 = safe to commit. Exit 1 = do not commit.
"""

import html
import os
import re
import sys
import difflib

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))


def norm(t):
    """Collapse to comparable words: quotes, punctuation and case are noise."""
    t = t.replace('’', "'").replace('‘', "'")
    t = t.replace('“', '"').replace('”', '"')
    return re.sub(r'[^a-zA-Z0-9]+', ' ', t).lower().strip()


def strip_tags(fragment):
    fragment = re.sub(r'<br\s*/?>', ' ', fragment)
    return html.unescape(re.sub(r'<[^>]+>', ' ', fragment))


def source_units(md):
    """Each non-blank markdown line is one authored unit (paragraph or heading).

    A '#'-prefixed line is the essay's own H1/divider scaffolding, not body
    text, so it is skipped -- bold '**...**' section headings are NOT skipped,
    because they must appear on the page verbatim as chapter titles.
    """
    out = []
    for line in md.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        u = norm(line)
        if u:
            out.append((u, line.strip()))
    return out


def page_units(page):
    """Every <p>/<h2> inside the essay body, in reading order.

    chapter-label paragraphs ('Chapter IV') are template ornament, not content.
    """
    try:
        body = page[page.index('<main class="story-body"'):page.index('<!-- BIO -->')]
    except ValueError:
        sys.exit('FAIL: could not locate <main class="story-body"> ... <!-- BIO --> in page')
    out = []
    for m in re.finditer(r'<(p|h2)([^>]*)>(.*?)</\1>', body, re.S):
        attrs, inner = m.group(2), m.group(3)
        if 'chapter-label' in attrs:
            continue
        t = norm(strip_tags(inner))
        if t:
            out.append(t)
    return out, body


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        slug = args[0].replace('.md', '').replace('.html', '')
        slug = os.path.basename(slug)
        md_path = os.path.join(REPO, 'thinking', slug + '.md')
        html_path = os.path.join(REPO, 'thinking', slug + '.html')
    elif len(args) == 2:
        md_path, html_path = args
    else:
        sys.exit(__doc__)

    for p in (md_path, html_path):
        if not os.path.exists(p):
            sys.exit('FAIL: missing %s' % p)

    md = open(md_path).read()
    page = open(html_path).read()
    src = source_units(md)
    units, body = page_units(page)

    failures = []

    # ---- 1. word level: nothing dropped, nothing invented -------------------
    sw = norm(' '.join(raw for _, raw in src)).split()
    bw = norm(strip_tags(body)).split()
    sm = difflib.SequenceMatcher(None, sw, bw, autojunk=False)
    dropped, added = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ('delete', 'replace') and i2 > i1:
            dropped.append(' '.join(sw[i1:i2]))
        if tag in ('insert', 'replace') and j2 > j1:
            added.append(' '.join(bw[j1:j2]))

    ORNAMENT = re.compile(r'^chapter [ivx]+$')
    added_real = [a for a in added if not ORNAMENT.match(a)]

    print('WORDS         source %d / page %d' % (len(sw), len(bw)))
    if dropped:
        failures.append('%d passage(s) dropped from the source' % len(dropped))
        for d in dropped:
            print('  DROPPED     %s' % d[:100])
    else:
        print('  dropped     none')
    if added_real:
        failures.append('%d passage(s) on the page are not in the source' % len(added_real))
        for a in added_real:
            print('  INVENTED    %s' % a[:100])
    else:
        print('  invented    none (chapter ornaments ignored)')

    # ---- 2. unit level: no merged paragraphs, headings verbatim -------------
    si, cur, buf, splits, desync = 0, (src[0][0] if src else ''), [], [], None
    for u in units:
        if cur.startswith(u):
            buf.append(u)
            cur = cur[len(u):].strip()
            if not cur:
                if len(buf) > 1:
                    splits.append((src[si][1], list(buf)))
                buf, si = [], si + 1
                cur = src[si][0] if si < len(src) else '\x00END'
        else:
            desync = (src[si][1] if si < len(src) else '<past end>', u)
            break

    print('UNITS         source %d / page %d' % (len(src), len(units)))
    if desync:
        failures.append('page diverges from the source paragraph order')
        print('  DESYNC      expected: %s' % desync[0][:90])
        print('              page had: %s' % desync[1][:90])
    elif si < len(src):
        failures.append('page ends %d source unit(s) early' % (len(src) - si))
        print('  TRUNCATED   first missing: %s' % src[si][1][:90])
    else:
        print('  consumed    %d/%d in order, no merges' % (si, len(src)))

    # ---- 3. report the formatting liberties (allowed, but disclose them) ----
    print('FORMATTING    %d paragraph split(s) for emphasis' % len(splits))
    for whole, parts in splits:
        print('  split       %s' % whole[:88])
        for p in parts:
            print('      ->      %s' % p[:84])
    ems = [strip_tags(e).strip() for e in re.findall(r'<em>(.*?)</em>', body, re.S)]
    print('              %d italicised phrase(s)' % len(ems))
    for e in ems:
        print('  em          %s' % e[:88])

    print()
    if failures:
        print('FAIL - DO NOT COMMIT')
        for f in failures:
            print('  * %s' % f)
        return 1
    print('PASS - source text is intact')
    return 0


if __name__ == '__main__':
    sys.exit(main())
