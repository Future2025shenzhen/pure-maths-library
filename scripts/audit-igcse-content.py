"""Audit every locally available IGCSE PDF without republishing its contents.

Writes only structured verification evidence, not extracted copyright text.
A cryptographic hash match and readable PDF are separate from content identity.
"""
from pathlib import Path
import argparse
import json
import zipfile
import re
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
MANIFEST=DIST/'data/igcse-online-files.json'
OUTPUT=DIST/'data/igcse-content-audit.json'

def compact_text(reader, pages):
    snippets=[]
    for i in sorted(set(pages)):
        if 0<=i<len(reader.pages):
            try:
                text=reader.pages[i].extract_text() or ''
                snippets.append(text[:12000])
            except Exception:
                pass
    return '\n'.join(snippets)

def audit(entry, PdfReader):
    p=DIST/entry['path']
    result={'filename':entry['filename'],'subject':entry['subject'],
            'year':entry['year'],'session':entry['session'],'type':entry['type'],
            'paper':entry.get('paper'),'expectedPages':entry.get('pages'),
            'fileSize':entry.get('bytes'),'sha256':entry.get('sha256')}
    if not p.is_file():
        result.update(status='missing',notes=['file-not-found'])
        return result
    if p.suffix.lower()=='.zip':
        try:
            with zipfile.ZipFile(p) as archive:
                members=archive.infolist()
                corrupted=archive.testzip()
                result['archiveEntries']=len(members)
                result['uncompressedBytes']=sum(f.file_size for f in members)
                if corrupted is not None:
                    result.update(status='archive-discrepancy',notes=['CRC-error-in-archive-member'])
                elif not members:
                    result.update(status='archive-discrepancy',notes=['empty-ZIP'])
                else:
                    result.update(status='archive-consistent',notes=[])
        except Exception as err:
            result.update(status='archive-discrepancy',notes=[type(err).__name__[:80]])
        return result
    try:
        reader=PdfReader(str(p),strict=False)
        num=len(reader.pages)
        result['observedPages']=num
        result['encrypted']=bool(reader.is_encrypted)
        if reader.is_encrypted:
            result.update(status='manual-review',notes=['encrypted'])
            return result
        text=compact_text(reader,[0,1,min(2,num-1),num-1])
        clean=re.sub(r'\s+',' ',text).upper()
        result['extractedCharacters']=len(clean)
        subject=entry['filename'][:4]
        code_found=bool(re.search(r'(?<!\d)'+subject+r'(?!\d)',clean))
        result['syllabusCodeOnPages']=code_found
        other='0478' if subject=='0625' else '0625'
        other_found=bool(re.search(r'(?<!\d)'+other+r'(?!\d)',clean))
        result['otherSubjectCodePresent']=other_found
        kind=entry['type']
        kind_patterns={
          'qp':r'QUESTION PAPER|CAMBRIDGE IGCSE|INTERNATIONAL GENERAL CERTIFICATE',
          'ms':r'MARK SCHEME|MARKING SCHEME',
          'er':r'EXAMINER REPORT|PRINCIPAL EXAMINER',
          'gt':r'GRADE THRESHOLD|GRADE BOUNDAR',
          'ci':r'CONFIDENTIAL INSTRUCTIONS',
          'pm':r'PRE.RELEASE|PRE.RELEASE MATERIAL|PREPARATORY MATERIAL'
        }
        result['documentTypeTextMatched']=bool(re.search(kind_patterns.get(kind,r'\b'+kind.upper()+r'\b'),clean))
        # Printed dates are not always on the first two pages, or may be
        # copyright dates. This is only a possible match, never conclusive.
        result['yearMentionedOnPages']=bool(re.search(r'(?<!\d)'+str(entry['year'])+r'(?!\d)',clean))
        result['pagesMatchManifest']=num==entry.get('pages')
        notes=[]
        if num<1: notes.append('no-pages')
        if not result['pagesMatchManifest']: notes.append('page-count-disagrees-with-manifest')
        if not clean: notes.append('no-readable-text-in-sampled-pages')
        if not code_found: notes.append('subject-code-not-found-in-sampled-pages')
        if not result['documentTypeTextMatched']: notes.append('document-type-not-confirmed-from-sampled-text')
        if other_found and not code_found: notes.append('potential-other-syllabus-document')
        result['notes']=notes
        if num<1 or not result['pagesMatchManifest']:
            result['status']='discrepancy'
        elif code_found and result['documentTypeTextMatched']:
            result['status']='sampled-content-consistent'
        else:
            result['status']='manual-review'
    except Exception as err:
        result.update(status='unreadable',notes=[type(err).__name__[:80]])
    return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sample',type=int,default=0,help='Optional bounded local diagnostic')
    args=parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit('pypdf missing: install via python3 -m pip install pypdf')
    data=json.loads(MANIFEST.read_text())
    entries=data['files'][:args.sample] if args.sample else data['files']
    rows=[audit(f,PdfReader) for f in entries]
    counts={status:sum(x['status']==status for x in rows)
            for status in ['sampled-content-consistent','archive-consistent','manual-review','discrepancy','archive-discrepancy','unreadable','missing']}
    report={'version':1,'generatedAt':datetime.now(timezone.utc).isoformat(),
            'scope':'PDF: sampled page text and page counts; ZIP: archive member CRC. Not complete human page-by-page review',
            'sourceManifest':'data/igcse-online-files.json',
            'auditedFiles':len(rows),'totalManifestFiles':len(data['files']),
            'counts':counts,'records':rows}
    report['fileFormats']={'pdf':sum(f['filename'].endswith('.pdf') for f in entries),'zip':sum(f['filename'].endswith('.zip') for f in entries)}
    OUTPUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('IGCSE content audit:',json.dumps(counts,sort_keys=True),
          'scanned',len(rows),'/',len(data['files']),flush=True)
    if counts['missing'] or counts['unreadable'] or counts['discrepancy'] or counts['archive-discrepancy']:
        print('WARNING: flagged items require investigation; see audit JSON')
        for item in rows:
            if item['status'] in ('missing','unreadable','discrepancy','archive-discrepancy'):
                print('REVIEW: '+item['filename']+' | '+item['status']+' | '+','.join(item.get('notes',[])),flush=True)
    if not args.sample and len(rows)!=len(data['files']):
        raise SystemExit('Incomplete audit')

if __name__=='__main__':
    main()
