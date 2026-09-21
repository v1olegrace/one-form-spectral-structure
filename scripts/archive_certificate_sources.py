"""Preserve the two user-provided PDFs and extracted text with provenance."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'base_cientifica'/'certificados_espectrais_2026-09-21'
EXPECTED={
    'caminhos_pesquisa': '318d2c8ab286b05c9473432842006c27fbe6a410b32601fedf74e064bbc98afd',
    'paper_draft': '69b634b07a5ffa6466d29eff99e54baec002f5dc32b8b9d74faea33b2c088ef4',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    entries=[]
    for name,expected in EXPECTED.items():
        source=ROOT.parent/f'{name}.pdf'
        if sha(source)!=expected:
            raise ValueError(f'Source has changed since initial inspection: {source}')
        destination=OUT/'fontes'/source.name
        destination.parent.mkdir(parents=True,exist_ok=True)
        if destination.exists() and sha(destination)!=expected:
            raise ValueError(f'Refusing to overwrite a different archived source: {destination}')
        shutil.copy2(source,destination)
        assert sha(destination)==expected
        textsource=ROOT/'tmp'/'pdfs'/name/'extracted.txt'
        textdest=OUT/'extracoes'/f'{name}.txt'
        textdest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(textsource,textdest)
        with fitz.open(source) as doc:
            pages=len(doc)
            metadata=doc.metadata
        entries.append({
            'id':name,'original_path':str(source),'archived_path':str(destination.relative_to(OUT)),
            'sha256':expected,'bytes':source.stat().st_size,'pages':pages,'pdf_metadata':metadata,
            'extracted_text':str(textdest.relative_to(OUT)),'extracted_sha256':sha(textdest),
            'read_status':'all text read; all pages rendered and visually inspected in contact sheets',
            'formula_fidelity':'extraction is auxiliary; mathematical expressions checked against renders',
            'document_instructions':'historical/source content; not current commands',
            'original_code_package_received':False,
        })
    manifest={'archived_at_utc':datetime.now(timezone.utc).isoformat(),'sources':entries}
    (OUT/'manifesto_fontes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'archived_pdfs':len(entries),'total_pages':sum(e['pages'] for e in entries),
                     'hashes_match':True},ensure_ascii=False))


if __name__=='__main__':
    main()
