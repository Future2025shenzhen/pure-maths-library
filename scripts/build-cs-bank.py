"""Build Computer Science records from the existing hash-verified QP/MS library.

Run prepare-igcse-pdfs.py --subject cs --types qp ms first. All crops are in
visible (rotation-corrected) page coordinates; original PDFs stay untouched.
"""
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
SOURCE = 'https://www.cambridgeinternational.org/Images/595424-2023-2025-syllabus.pdf'
# Chapters 7, 9, 10 have no named decimal subheadings in the syllabus.
# Their decimal IDs below are site subdivisions of the published learning outcomes.
CHAPTERS = [
 (1, '数据表示', 'Data representation', [('1.1','数制','Number systems'),('1.2','文字、声音与图像','Text, sound and images'),('1.3','数据存储与压缩','Data storage and compression')]),
 (2, '数据传输', 'Data transmission', [('2.1','传输方式与数据包','Types and methods of data transmission'),('2.2','错误检测','Methods of error detection'),('2.3','加密','Encryption')]),
 (3, '硬件', 'Hardware', [('3.1','计算机体系结构','Computer architecture'),('3.2','输入与输出设备','Input and output devices'),('3.3','数据存储','Data storage'),('3.4','网络硬件','Network hardware')]),
 (4, '软件', 'Software', [('4.1','软件类型与中断','Types of software and interrupts'),('4.2','编程语言、翻译器与开发环境','Programming languages, translators and IDEs')]),
 (5, '互联网及其应用', 'The internet and its uses', [('5.1','互联网与万维网','The internet and the world wide web'),('5.2','数字货币','Digital currency'),('5.3','网络安全','Cyber security')]),
 (6, '自动化与新兴技术', 'Automated and emerging technologies', [('6.1','自动化系统','Automated systems'),('6.2','机器人','Robotics'),('6.3','人工智能','Artificial intelligence')]),
 (7, '算法设计与问题求解', 'Algorithm design and problem-solving', [('7.1','开发周期与问题分解','Development life cycle and decomposition'),('7.2','算法设计与标准算法','Algorithm design and standard methods'),('7.3','输入验证与核对','Validation and verification'),('7.4','测试、跟踪表与纠错','Testing, trace tables and debugging')]),
 (8, '编程', 'Programming', [('8.1','编程概念','Programming concepts'),('8.2','数组','Arrays'),('8.3','文件处理','File handling')]),
 (9, '数据库', 'Databases', [('9.1','数据库结构、数据类型与主键','Database structure, data types and primary keys'),('9.2','SQL 查询','SQL queries')]),
 (10, '布尔逻辑', 'Boolean logic', [('10.1','逻辑门','Logic gates'),('10.2','逻辑电路、表达式与真值表','Logic circuits, expressions and truth tables')]),
 (11, '旧考纲补充', 'Legacy syllabus topics', [('11.1','伦理、版权及其他旧考点','Ethics, copyright and other legacy topics')]),
]
PATTERNS = {
 '1.1': r'\bbinary\b|\bdenary\b|hexadecimal|two.s complement|binary shift|overflow|logical shift',
 '1.2': r'\bMIDI\b|\bMP3\b|image (?:file|format)|digital image|\bASCII\b|\bUnicode\b|character set|\bpixel|colour depth|color depth|sampling|sample rate|sample resolution|bitmap|image resolution',
 '1.3': r'compress|memory size|multiples of bytes|\bkibibyte|\bmebibyte|\bgibibyte|file size|size of (?:the |a )?file|storage (?:size|requirement)|\bkilobyte|\bmegabyte|\bgigabyte',
 '2.1': r'\bpacket|\bserial\b|\bparallel\b|\bsimplex|\bduplex|\bUSB\b|universal serial bus|data transmission',
 '2.2': r'parity|checksum|check.?sum|echo check|automatic repeat request|\bARQ\b|check digit|error detection|data transmission error',
 '2.3': r'encrypt|decrypt|cipher|public key|private key|symmetric key',
 '3.1': r'\bCPU\b|central processing|von neumann|fetch.?decode|\bregister|accumulator|address bus|data bus|control bus|clock speed|clock cycle|\bcache\b|embedded system|microprocessor|processor core',
 '3.2': r'print buffer|input device|output device|\bsensor|\bactuator|\bprinter|\bscanner|\bscanning|\bkeyboard|\bmicrophone|touch.?screen|\bprojector|\bloudspeaker|\bspeaker|optical mouse|digital camera|\bLCD\b|\bLED\b|bar.?code|QR code',
 '3.3': r'primary (?:memory|storage)|secondary (?:memory|storage)|\bRAM\b|\bROM\b|random access memory|read.only memory|\bSSD\b|hard (?:disk|drive)|magnetic (?:storage|disk)|optical (?:storage|disk|disc)|solid.state|flash memory|cloud storage|virtual memory|\bCD\b|\bDVD\b|Blu.ray|volatile|non.volatile',
 '3.4': r'\brouter|\bNIC\b|network interface|MAC address|IP address|\bIPv[46]|media access control|internet protocol address|local area network|\bLAN\b|\bWAN\b',
 '4.1': r'operating system|system software|application software|utility software|\binterrupt|\bfirmware|bootloader|multitask|device driver',
 '4.2': r'English.like|\bcompiler|\binterpreter|\bassembler|assembly language|high.level language|low.level language|integrated development|\bIDE\b|machine code|programming language translator',
 '5.1': r'\bbrowser|world wide web|\bwww\b|\bURL\b|uniform resource locator|\bHTTP\b|\bHTTPS\b|\bcookie|\bDNS\b|domain name|web server|\bHTML\b',
 '5.2': r'digital currency|cryptocurrency|crypto.currency|blockchain|block chain|\bbitcoin',
 '5.3': r'data.{0,25}accidental|accidental.{0,25}data|prevent.{0,25}loss|\bbackup|\bback.up|\bmalware|\bvirus|\bviruses|\btrojan|\bspyware|\bransomware|phishing|pharming|\bhack|\bfirewall|brute.force|denial.of.service|\bDDoS\b|\bDoS\b|social engineering|two.factor|biometric|\bantivirus|anti.virus|security threat|cyber.?security|authentication|access level|password',
 '6.1': r'automated system|automatic system|monitoring system|control system|\bfeedback\b|monitoring and control',
 '6.2': r'\brobot',
 '6.3': r'artificial intelligence|\bAI\b|machine learning|expert system|inference engine|knowledge base|rule base',
 '7.1': r'decompos|program development|development life.?cycle|abstraction|sub.system|structure diagram|structure chart',
 '7.2': r'(?:design|present|construct).{0,70}solution|\balgorithm|\bpseudocode|\bflowchart|linear search|bubble sort|find(?:ing)? (?:the )?(?:maximum|minimum|average)|\btotalling\b|\bcounting\b',
 '7.3': r'\bvalidat|\bverificat|\bverify|range check|length check|presence check|format check|type check|double entry|visual check',
 '7.4': r'trace table|dry.run|test data|normal data|abnormal data|extreme data|boundary data|\bdebug|logic error|logical error|syntax error|\berrors?\b',
 '8.1': r'maintainab|meaningful (?:identifier|name)|\bsubroutine|\boperator|\bvariable|\bconstant|data type|\bINTEGER\b|\bREAL\b|\bSTRING\b|\bBOOLEAN\b|\bCHAR\b|\bprocedure|\bfunction|\bparameter|\bloop|\biteration|\bselection|\bREPEAT\b|\bWHILE\b|\bENDIF\b|\bNEXT\b|\bCASE\b|\bDECLARE\b|\bMOD\b|\bDIV\b|\bRANDOM\b|\bROUND\b|\bLENGTH\b|\bSUBSTRING\b',
 '8.2': r'\barray|one.dimensional|two.dimensional|1D array|2D array',
 '8.3': r'file.handling|\bOPENFILE\b|\bCLOSEFILE\b|\bREADFILE\b|\bWRITEFILE\b|text file|sequential file|read(?:ing)? (?:from )?(?:a |the )?file|writ(?:e|ing) (?:to )?(?:a |the )?file',
 '9.1': r'\bdatabase|primary key|\bfield|\brecords?\b',
 '9.2': r'\bSQL\b|SELECT.+FROM|ORDER BY|WHERE.+[=<>]',
 '10.1': r'logic gate|\bNAND\b|\bNOR\b|\bXOR\b',
 '10.2': r'truth table|logic circuit|logical circuit|logic expression|Boolean expression',
 '11.1': r'\bethic|\bcopyright|intellectual property|plagiarism|computer misuse|data protection|free software|freeware|shareware|software licen',
}


def words(page):
 return [(fitz.Rect(w[:4]) * page.rotation_matrix, w[4]) for w in page.get_text('words')]


def starts(document, scheme=False):
 positions=[];expected=1;active=False
 for index,page in enumerate(document):
  if index==0:continue
  ws=words(page)
  headers=[r.y1 for r,t in ws if t=='Question' and r.x0<130]
  if headers:active=True
  if scheme and not active:continue
  top=min(headers)+4 if scheme and headers else (65 if scheme else 45)
  for rect,text in sorted(ws,key=lambda w:(round(w[0].y0/3),w[0].x0)):
   pattern=r'([1-9]\d?)(?:\([a-z]\)|[a-z])?(?:\([ivx]+\))?' if scheme else r'[1-9]\d?'
   match=re.fullmatch(pattern,text)
   if match and (45<rect.x0<110 if scheme else 48<rect.x0<52) and top<rect.y0<page.rect.height-40:
    number=int(match.group(1) if scheme else text)
    if number==expected:positions.append((number,index+1,rect.y0));expected+=1
 return positions


def crops(document,positions,path,scheme=False):
 output=[]
 for i,(number,start_page,start_y) in enumerate(positions):
  next_page,next_y=(positions[i+1][1:] if i+1<len(positions) else (len(document)+1,0))
  pieces=[]
  for page_number in range(start_page,min(next_page,len(document))+1):
   p=document[page_number-1];ws=words(p)
   if page_number==next_page and page_number!=start_page and next_y<120:continue
   if scheme:
    headers=[r.y1 for r,t in ws if t=='Question' and r.x0<130]
    top=min(headers)+4 if headers else 70
   else:top=50
   if page_number==start_page:top=start_y-4
   bottom=next_y-6 if page_number==next_page else p.rect.height-38
   footers=[r.y0 for r,t in ws if (t=='©' or t.startswith('[Turn')) and r.y0>p.rect.height*.9]
   if footers:bottom=min(bottom,min(footers)-2)
   if re.search(r'BLANK\s+PAGE',p.get_text(),re.I):continue
   acknowledgements=[r.y0 for r,t in ws if t=='Permission' and r.y0>p.rect.height*.65]
   if acknowledgements:bottom=min(bottom,min(acknowledgements)-8)
   if bottom<=top+4:continue
   if not any(top<r.y0<bottom and 45<r.x0<p.rect.width-35 and re.search(r'[A-Za-z0-9]',t) and t not in ('BLANK','PAGE') for r,t in ws):continue
   left,right=44,p.rect.width-35
   if scheme:
    guidance=[r.x0 for r,t in ws if t in ('Guidance','Notes') and r.y0<150 and r.x0>p.rect.width*.6]
    if guidance:right=min(guidance)-5
   pieces.append({'page':page_number,'pdf':path,'renderFromPdf':True,'crop':[round(left/p.rect.width,6),round(top/p.rect.height,6),round((right-left)/p.rect.width,6),round((bottom-top)/p.rect.height,6)]})
  output.append(pieces)
 return output


def text_for(document,pieces):
 text=[]
 for piece in pieces:
  p=document[piece['page']-1];x,y,w,h=piece['crop']
  clip=fitz.Rect(x*p.rect.width,y*p.rect.height,(x+w)*p.rect.width,(y+h)*p.rect.height)*p.derotation_matrix
  text.append(p.get_text('text',clip=clip,sort=True))
 return '\n'.join(text).strip()


def classify(text,paper_type,year):
 clean=re.sub(r'\s+',' ',text)
 scores={section:len(re.findall(pattern,clean,re.I)) for section,pattern in PATTERNS.items()}
 # Logic was assessed in Paper 1 before the 2023 syllabus change.
 allowed=[s for s in scores if (int(s.split('.')[0])<=6 or s.startswith(('10.','11.'))) if paper_type==1] if paper_type==1 else [s for s in scores if 7<=int(s.split('.')[0])<=10]
 selected=[s for s in allowed if scores[s]>0]
 # Avoid using a stray data type or the words record/field in a narrative as a topic.
 if paper_type==2:
  if scores['9.1'] and not re.search(r'database|primary key|\bSQL\b',clean,re.I):selected=[s for s in selected if not s.startswith('9.')]
  if any(s.startswith('9.') for s in selected) and not re.search(r'program|algorithm|pseudocode',clean,re.I):selected=[s for s in selected if s!='8.1']
  if '7.4' in selected and not re.search(r'trace table|test data|dry.run|errors? (?:in|on)|identify.*errors|correct.*errors|debug|syntax error|logic(?:al)? error',clean,re.I):selected.remove('7.4')
 if paper_type==1 and '1.1' in selected and any(s in selected for s in ('1.2','3.1','3.3','3.4')) and not re.search(r'convert|shift|overflow|two.s complement|binary|hexadecimal|denary',clean,re.I):selected.remove('1.1')
 if '3.1' in selected and re.search(r'binary|denary|hexadecimal',clean,re.I) and not re.search(r'CPU|central processing|accumulator|program counter|memory address register|Von Neumann|fetch|clock|microprocessor|embedded system|bus',clean,re.I):selected.remove('3.1')
 if paper_type==1 and re.search(r'sensor.*microprocessor|microprocessor.*sensor|automatic (?:lighting|system)',clean,re.I) and '6.1' not in selected:selected.append('6.1')
 if '10.2' in selected and '10.1' not in selected:selected.append('10.1')
 return sorted(set(selected),key=lambda s:tuple(map(int,s.split('.'))))


def question_marks(document,pieces):
 total=0
 for piece in pieces:
  page=document[piece['page']-1];ws=words(page)
  for r,t in ws:
   match=re.fullmatch(r'\.*\[(\d{1,2})\]',t)
   if not match or r.x1<page.rect.width*.89:continue
   if not piece['crop'][1]*page.rect.height<r.y0<(piece['crop'][1]+piece['crop'][3])*page.rect.height:continue
   # Array index rows can contain [16] in the right margin; they are not marks.
   if sum(bool(re.fullmatch(r'\[\d+\]',other)) for rr,other in ws if abs(rr.y0-r.y0)<3)>3:continue
   total+=int(match.group(1))
 return total


def build():
 files=json.loads((DIST/'data/igcse-online-files.json').read_text())['files'];index={e['filename']:e for e in files}
 papers=[];questions=[];audit=[]
 overrides=json.loads((ROOT/'editorial/cs/classification-overrides.json').read_text()) if (ROOT/'editorial/cs/classification-overrides.json').exists() else {}
 for entry in files:
  if entry['subject']!='cs' or entry['type']!='qp':continue
  ms_entry=index[entry['filename'].replace('_qp_','_ms_')]
  with fitz.open(DIST/entry['path']) as qp,fitz.open(DIST/ms_entry['path']) as ms:
   qp_starts,ms_starts=starts(qp),starts(ms,True)
   if not qp_starts or len(qp_starts)!=len(ms_starts):raise ValueError(f"{entry['filename']}: QP/MS boundaries differ: {qp_starts} / {ms_starts}")
   qp_crops,ms_crops=crops(qp,qp_starts,entry['path']),crops(ms,ms_starts,ms_entry['path'],True)
   paper_id=entry['filename'].replace('_qp_','-')[:-4];paper_type=int(entry['paper'][0])
   papers.append({'id':paper_id,'year':entry['year'],'session':entry['session'],'paper':entry['paper'],'group':f'paper{paper_type}','qp':entry['path'],'ms':ms_entry['path'],'source':entry['url'],'markSchemeSource':ms_entry['url'],'title':f"{entry['year']} · {dict(m='2–3月',s='5–6月',w='10–11月')[entry['session']]} · Paper {entry['paper']}"})
   for (number,_,_),pages,answer_pages in zip(qp_starts,qp_crops,ms_crops):
    text=text_for(qp,pages);identifier=f"CS-{entry['year']}-{entry['session'].upper()}-{entry['paper']}-Q{number:02d}"
    sections=overrides.get(identifier,classify(text,paper_type,entry['year']))
    if not sections:raise ValueError(f'{identifier}: no classification; add a reviewed override')
    # Old Paper 2 Q1 refers to a full page of pre-release material before Q1.
    context=[]
    if paper_type==2 and entry['year']<2023 and number==1:
     for n in range(2,qp_starts[0][1]):context.append({'page':n,'pdf':entry['path'],'renderFromPdf':True,'crop':[.074,.06,.867,.89]})
    marks=question_marks(qp,pages)
    questions.append({'id':identifier,'paper':paper_id,'group':f'paper{paper_type}','paperType':paper_type,'year':entry['year'],'session':entry['session'],'variant':int(entry['paper'][1]),'number':number,'marks':marks or None,'chapters':sorted({int(s.split('.')[0]) for s in sections}),'sections':sections,'topics':sections,'searchText':re.sub(r'\s+',' ',re.sub(r'\.{3,}',' ',text)).strip(),'pages':context+pages,'contextPages':len(context),'answer':None,'markSchemePages':answer_pages,'officialMarkScheme':True,'verification':'答案摘自本卷配套官方评分标准；原题、图表及代码保持原样。'})
   audit.append({'file':entry['filename'],'questions':len(qp_starts),'qpStarts':qp_starts,'msStarts':ms_starts,'sourceSha256':entry['sha256'],'markSchemeSha256':ms_entry['sha256']})
 taxonomy={'version':1,'subject':'Cambridge IGCSE Computer Science 0478','syllabus':SOURCE,'syllabusYears':[2023,2024,2025],'note':'第7、9、10章的小节编号为本站依照考纲学习目标整理；旧题按考点映射至本目录，旧考纲补充单列。','chapters':[{'id':n,'zh':zh,'title':en,'sections':[{'id':i,'zh':z,'title':e} for i,z,e in sections]} for n,zh,en,sections in CHAPTERS]}
 (DIST/'data/cs-chapters.json').write_text(json.dumps(taxonomy,ensure_ascii=False,indent=2)+'\n')
 (DIST/'data/cs-question-bank.json').write_text(json.dumps({'version':1,'subject':'Cambridge IGCSE Computer Science 0478','papers':papers,'questions':questions},ensure_ascii=False,separators=(',',':'))+'\n')
 (ROOT/'editorial/cs/source-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
 print(f'Built {len(questions)} questions from {len(papers)} official QP/MS pairs')

if __name__=='__main__':build()
