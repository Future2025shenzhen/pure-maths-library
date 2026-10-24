"""Build exact Cambridge IGCSE resource links from publisher index HTML.

Third-party links remain on their original hosts. This script never downloads,
commits, or republishes Cambridge PDF bytes. Network failures retain existing
manifest with a clear status rather than claiming a verified paper.
"""
import json
import re
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "dist/data/igcse-paper-manifest.json"
SOURCES = {
    "physics": ("0625", "physics-0625"),
    "cs": ("0478", "computer-science-0478"),
}
BASE = "https://qualifiedquest.com/past-papers/igcse-o-level/"
FILE_RE = re.compile(r"^(0625|0478)_([msw])(19|20|21|22|23|24)_(qp|ms|gt|er|ci|pm)(?:_([1-6][1-3]))?\.pdf$",re.I)

class PDFLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
    def handle_starttag(self, tag, attrs):
        if tag != "a": return
        href = dict(attrs).get("href","")
        if href: self.links.add(href)

def parse_links(html, base, code, slug):
    p = PDFLinks()
    p.feed(html)
    found = {}
    for href in p.links:
        url = urljoin(base,href)
        parsed = urlparse(url)
        if parsed.scheme!="https" or parsed.hostname!="qualifiedquest.com": continue
        if not parsed.path.startswith("/papers/igcse-o-level/"+slug+"/"): continue
        filename = parsed.path.rsplit("/",1)[-1]
        m = FILE_RE.fullmatch(filename)
        if not m or m.group(1)!=code: continue
        year = 2000+int(m.group(3))
        if "/"+str(year)+"/" not in parsed.path: continue
        session,kind,component = m.group(2),m.group(4),m.group(5)
        if kind in ("qp","ms","ci","pm") and not component: continue
        if kind in ("er","gt") and component: continue
        found[(session,year,kind,component)] = url
    return found

def get_html(url):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; educational-index-catalog/1.0)"})
    with urlopen(req, timeout=22,context=ssl.create_default_context()) as res:
        if res.status != 200: raise RuntimeError("HTTP "+str(res.status))
        html=res.read(2_400_000).decode("utf-8","replace")
    if len(html)<1000:raise RuntimeError("short index page")
    return html

def probe_pdf(url):
    """Verify PDF header only; do not save copyrighted file bytes."""
    req=Request(url,headers={"User-Agent":"Mozilla/5.0","Range":"bytes=0-15"})
    try:
        with urlopen(req,timeout=7,context=ssl.create_default_context()) as response:
            if not response.geturl().startswith("https://"):
                return "insecure-redirect"
            return "pdf-signature-confirmed" if response.read(16).startswith(b"%PDF-") else "not-a-pdf"
    except Exception:
        return "source-unavailable"

def main():
    doc=json.loads(MANIFEST.read_text())
    by_id={r["id"]:r for r in doc["records"]}
    session_files={}
    source_state={}
    probe_candidates=[]
    year_sampled=set()
    direct_counts={"qp":0,"ms":0,"er":0,"gt":0,"ci":0,"pm":0}
    for subject,(code,slug) in SOURCES.items():
        index_url=BASE+slug+"/"
        try:
            links=parse_links(get_html(index_url),index_url,code,slug)
            if len(links)<20:raise RuntimeError("too few parsed PDF links: "+str(len(links)))
            source_state[subject]={"status":"index-parsed","indexUrl":index_url,"pdfLinksListed":len(links)}
        except Exception as error:
            source_state[subject]={"status":"index-unavailable","indexUrl":index_url,"reason":str(error)[:180]}
            print("WARN "+subject+" index unavailable: "+str(error)[:150])
            continue
        # Remove speculative inherited source-confidence states when this primary
        # evidence index was successfully parsed.
        for rec in doc["records"]:
            if rec["subject"]!=subject:continue
            for kind in ("qp","ms"):
                rec.pop(kind+"Url",None)
                rec[kind+"Status"]="not-listed-on-selected-index"
            rec["sourceStatus"]="not-listed-on-selected-index"
            rec.pop("sourceEvidenceUrl",None)
            rec["fileStatus"]="not-checked"
        for (session,year,kind,component),url in links.items():
            if kind in ("qp","ms","ci","pm") and component:
                id_=f"{code}_{session}{str(year)[-2:]}_{component}"
                rec=by_id.get(id_)
                if not rec:continue
                rec[kind+"Url"]=url
                rec[kind+"Status"]="filename-and-link-present-on-source-index"
                rec["sourceStatus"]="component-named-in-source-index"
                rec["sourceEvidenceUrl"]=index_url
                rec["linkVerification"]="source-html-href-observed;pdf-bytes-not-checked"
                direct_counts[kind]+=1
                if kind in ("qp","ms") and (subject,year,kind) not in year_sampled:
                    year_sampled.add((subject,year,kind))
                    probe_candidates.append((subject,rec,kind,url))
            else:
                key=f"{code}_{session}{str(year)[-2:]}"
                entry=session_files.setdefault(key,{"subject":subject,"year":year,"session":session,"sourceIndex":index_url})
                entry[kind+"Url"]=url
                entry[kind+"Status"]="filename-and-link-present-on-source-index;pdf-bytes-not-checked"
                direct_counts[kind]+=1
    probe_results={}
    with ThreadPoolExecutor(max_workers=8) as executor:
        tasks={executor.submit(probe_pdf,url):(subject,rec,kind,url) for subject,rec,kind,url in probe_candidates}
        for future in as_completed(tasks):
            subject,rec,kind,url=tasks[future]
            try: status=future.result()
            except Exception: status="source-unavailable"
            rec[kind+"ProbeStatus"]=status
            if status=="pdf-signature-confirmed":
                rec[kind+"Status"]="pdf-signature-confirmed"
            probe_results[status]=probe_results.get(status,0)+1
    doc["pdfProbeSummary"]={"attempted":len(probe_candidates),"results":probe_results,
      "scope":"HTTP PDF signature only; not a complete contents or copyright verification"}
    # Clearly report pair completeness from observed source hrefs only.
    coverage={}
    for subject in SOURCES:
        rows=[r for r in doc["records"] if r["subject"]==subject]
        both=sum(bool(r.get("qpUrl") and r.get("msUrl")) for r in rows)
        only_qp=sum(bool(r.get("qpUrl")) and not r.get("msUrl") for r in rows)
        only_ms=sum(bool(r.get("msUrl")) and not r.get("qpUrl") for r in rows)
        by_year={}
        for year in range(2019,2025):
            yr=[r for r in rows if r["year"]==year]
            by_year[str(year)]={"qp":sum(bool(r.get("qpUrl")) for r in yr),"ms":sum(bool(r.get("msUrl")) for r in yr),
             "pairs":sum(bool(r.get("qpUrl") and r.get("msUrl")) for r in yr)}
        coverage[subject]={"paired":both,"qpOnly":only_qp,"msOnly":only_ms,"byYear":by_year}
    doc["pairCoverage"]=coverage
    doc["version"]=10
    doc["description"]="Live-build index of exact source HTML hrefs. URL presence was verified on the source index page, NOT by downloading PDF content. A third-party host may refuse access. No copyrighted PDF bytes are stored."
    doc["indexedSessionResources"]=sorted(session_files.values(),key=lambda x:(x["subject"],x["year"],x["session"]))
    doc["lastIndexAudit"]=source_state
    doc["verifiedPdfCount"]=0
    MANIFEST.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+"\n")
    print("IGCSE source index build: "+json.dumps(direct_counts,sort_keys=True))
    print("IGCSE source statuses: "+json.dumps(source_state,sort_keys=True))
    print("IGCSE PDF probe: "+json.dumps(doc["pdfProbeSummary"],sort_keys=True))
    print("IGCSE QP/MS pair coverage: "+json.dumps(coverage,sort_keys=True))
    assert all(r.get("fileStatus")!="verified" for r in doc["records"])

if __name__=="__main__":
    main()
