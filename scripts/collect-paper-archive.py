"""Collect the explicitly listed current-specification P1/P2/P3 paper PDFs.

Run locally with PyMuPDF installed. Existing 2020-2023 files remain untouched.
The published archive intentionally stops at the June 2025 session.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, time, urllib.request
import fitz

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://alevelclouds.com/past-papers/Edexcel/maths/'
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://alevelclouds.com/'}
MONTHS = {1: 'jan', 6: 'jun', 10: 'oct'}

def download(url):
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=45) as r:
                return r.read()
        except Exception as e:
            last = e
            if attempt < 2:
                time.sleep(attempt + 1)
    raise last

def main():
    html = download(SOURCE).decode()
    names = sorted(set(re.findall(r'https://edemat\.alevelclouds\.com/(\d{2}_\d{2}_(?:QP|MS)_P[123][AR]?\.pdf)', html)))
    names = [x for x in names if 19 <= int(x[:2]) and (2000 + int(x[:2]), int(x[3:5])) <= (2025, 6)]
    target = ROOT / 'dist/assets/past-papers'
    target.mkdir(parents=True, exist_ok=True)
    def collect(name):
        yy, mm, kind, unit = name[:-4].split('_')
        year, month, stage, variant = 2000 + int(yy), int(mm), unit[:2], unit[2:]
        identity = f'{stage.lower()}-{MONTHS[month]}-{year}' + (f'-{variant.lower()}' if variant else '')
        path = target / (identity + ('-ms' if kind == 'MS' else '') + '.pdf')
        url = 'https://edemat.alevelclouds.com/' + name
        try:
            existing = path.exists()
            content = path.read_bytes() if existing else download(url)
            doc = fitz.open(stream=content, filetype='pdf')
            cover = '\n'.join(doc[i].get_text() for i in range(min(2, len(doc))))
            code = f'WMA1{stage[-1]}'
            if code not in re.sub(r'\s+', '', cover).upper():
                raise ValueError(f'Cover does not identify {code}')
            if kind == 'MS' and str(year) not in cover:
                raise ValueError('Mark scheme cover year does not match catalog')
            if not existing:
                path.write_bytes(content)
            return dict(id=identity, stage=stage, year=year, month=month, variant=variant,
                        kind=kind, path=path.relative_to(ROOT / 'dist').as_posix(), source=url,
                        pages=len(doc), bytes=len(content), sha256=hashlib.sha256(content).hexdigest(),
                        gitBlobSha=hashlib.sha1(f'blob {len(content)}\0'.encode()+content).hexdigest(),
                        existing=existing, coverYearPresent=str(year) in cover,
                        paperLogNumber=next(iter(re.findall(r'P[0-9]{5}A',cover)),None),
                        status='verified-pdf-cover')
        except Exception as e:
            return dict(id=identity, kind=kind, source=url, status='failed', error=str(e))
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(collect, names))
    evidence = ROOT / 'editorial/paper-archive'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'download-audit.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
    failed = [x for x in results if x['status'] == 'failed']
    print(json.dumps({'files':len(results),'new':sum(not x.get('existing',True) for x in results),'failed':failed},ensure_ascii=False),flush=True)
    if failed:
        raise SystemExit('Some source files could not be verified; archive not generated.')
    practice_ids = {p['id'] for p in json.loads((ROOT/'dist/data/past-bank.json').read_text())['papers']}
    exceptions = json.loads((evidence/'reviewed-cover-exceptions.json').read_text())
    papers = []
    for identity in sorted({x['id'] for x in results}):
        qp = next(x for x in results if x['id']==identity and x['kind']=='QP')
        ms = next(x for x in results if x['id']==identity and x['kind']=='MS')
        if qp['paperLogNumber'] and ms['paperLogNumber'] and qp['paperLogNumber'] != ms['paperLogNumber']:
            review = exceptions.get(identity,{})
            if review.get('questionPaperSha256') != qp['sha256'] or review.get('markSchemeSha256') != ms['sha256']:
                raise ValueError(f'{identity}: question paper and mark scheme log numbers differ')
        if not qp['coverYearPresent'] and not (qp['paperLogNumber'] and qp['paperLogNumber']==ms['paperLogNumber']):
            raise ValueError(f'{identity}: missing year and no matching mark-scheme log number')
        papers.append(dict(id=identity,stage=qp['stage'],year=qp['year'],month=qp['month'],variant=qp['variant'],
                           title=f"{qp['stage']} · {qp['year']}年{qp['month']}月"+(f" · {qp['variant']}卷" if qp['variant'] else ''),
                           pdf=qp['path'],markScheme=ms['path'],source=qp['source'],markSchemeSource=ms['source'],
                           sha256=qp['sha256'],markSchemeSha256=ms['sha256'],pages=qp['pages'],markSchemePages=ms['pages'],
                           questionPracticeAvailable=identity in practice_ids,
                           verification='PDF可读取；卷别及年份已核对，原卷缺少日期时用官方评分标准年份与试卷编号交叉核对。未作逐题数学审核。'))
    archive=dict(version=1,updatedAt='2026-10-24',catalogSource=SOURCE,
                 note='整卷档案独立于逐题练习；收录范围截至2025年6月。A/R卷按来源标识分别保存。',papers=papers)
    (ROOT/'dist/data/paper-archive.json').write_text(json.dumps(archive,ensure_ascii=False,indent=2)+'\n')
    (evidence/'catalog.html').write_text(html)
    print(f'Archive ready: {len(papers)} paper/mark-scheme pairs through June 2025.',flush=True)

if __name__ == '__main__':
    main()
