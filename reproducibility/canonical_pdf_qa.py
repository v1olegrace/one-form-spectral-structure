"""Inspect a compiled canonical paper; requires optional PyMuPDF.

This records structural checks and source hashes, and optionally renders every
page. A PASS is not a visual review and does not verify the scientific claims.
The historical pdf_qa.py instead checks the non-canonical Quarto draft.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

import fitz

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(pdf, log, report, render_dir=None):
    doc = fitz.open(pdf)
    text = '\n'.join(page.get_text() for page in doc)
    paper_source = (ROOT/'paper/paper.tex').read_text(encoding='utf-8')
    version = re.search(r'Draft (v[\d.]+)', paper_source).group(1)
    issues = []
    if f'Draft {version}' not in text:
        issues.append('Missing current draft version in PDF')
    if 'Spectral structure of approximate one-form' not in text:
        issues.append('Missing canonical title')
    if '??' in text:
        issues.append('Possible unresolved reference (??)')
    font_types = sorted({font[2] for page in doc for font in page.get_fonts(full=True)})
    if 'Type3' in font_types or 'Type 3' in font_types:
        issues.append('Bitmap Type 3 font')
    for number, page in enumerate(doc, 1):
        if len(page.get_text().strip()) < 40:
            issues.append(f'Empty or nearly empty page {number}')
        for block in page.get_text('blocks'):
            x0, y0, x1, y1 = block[:4]
            if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                issues.append(f'Text outside page {number}: {block[:4]}')
    log_text = log.read_text(encoding='utf-8', errors='replace')
    log_issues = re.findall(r'^(?:LaTeX|Package \w+) Warning.*$|^Overfull.*$|^!.*$',
                           log_text, re.M)
    issues.extend(log_issues)
    bibliography_log = log.with_suffix('.blg')
    if not bibliography_log.exists():
        issues.append('Missing BibTeX log')
    elif 'Warning--' in bibliography_log.read_text(errors='replace'):
        issues.append('BibTeX warning')
    if render_dir is not None:
        render_dir.mkdir(parents=True, exist_ok=True)
        for number, page in enumerate(doc, 1):
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(render_dir/f'page-{number:02}.png')
    sources = [ROOT/'paper'/name for name in
               ['paper.tex', 'appendix.tex', 'references.bib', 'physofall.bst']]
    sources.extend(sorted((ROOT/'paper/figures').glob('*.dat')))
    result = {
        'status': 'PASS' if not issues else 'FAIL', 'draft': version,
        'pages': len(doc), 'pdf': str(pdf.resolve()), 'pdf_sha256': digest(pdf),
        'log_sha256': digest(log), 'font_types': font_types, 'issues': issues,
        'source_sha256': {str(p.relative_to(ROOT)): digest(p) for p in sources},
        'visual_review': 'NOT_ASSESSED_BY_SCRIPT',
        'scope': 'PDF structure and current source inventory; not scientific validation',
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if not issues else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, default=ROOT/'paper/paper.pdf')
    parser.add_argument('--log', type=Path, default=ROOT/'paper/paper.log')
    parser.add_argument('--report', type=Path, default=ROOT/'output/data/canonical_pdf_qa.json')
    parser.add_argument('--render-dir', type=Path)
    args = parser.parse_args()
    raise SystemExit(inspect(args.pdf, args.log, args.report, args.render_dir))
