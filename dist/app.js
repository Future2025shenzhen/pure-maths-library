import {STORE_KEY,shuffle,validateBank,cleanState,filterQuestions,composePaper} from './core.js';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)],main=$('#main-view');
const icons={search:'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke-width="1.5"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></svg>'};
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
// Escape TeX angle brackets before HTML parsing; preserve authored tables.
const format=v=>String(v).replace(/\$[^$]*\$/g,m=>esc(m));
let data,state,ids,view='library',stage='P1',chapters=[],kind='',status='all',search='',page=1,order=[],paper=null,answersOpen=false;
const opened=new Set();const PAGE_SIZE=6;
function toast(message){const el=$('#toast');el.textContent=message;el.classList.add('visible');clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove('visible'),3500);}
function math(el=main){if(window.renderMathInElement)window.renderMathInElement(el,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false,strict:'ignore',trust:false});}
function safeRead(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback;}catch{return fallback;}}
function saveState(){try{localStorage.setItem(STORE_KEY,JSON.stringify(state));}catch{toast('浏览器未允许保存记录，请导出备份。');}$('#saved-count').textContent=state.saved.length;}
function savePaper(){try{localStorage.setItem('pure-practice-paper-v1',JSON.stringify(paper));}catch{toast('当前试卷无法保存，建议打印留存。');}}
function resetOrder(){order=data.questions.filter(q=>q.stage===stage).map(q=>q.id);page=1;}
function chapterName(id){return data.chapters[stage].find(c=>c.id===id);}
function setStage(value){if(!data.chapters[value])return;stage=value;chapters=data.chapters[stage].map(c=>c.id);kind='';resetOrder();renderSidebar();render();}
function renderSidebar(){
 $$('#stage-switch button').forEach(b=>b.classList.toggle('selected',b.dataset.stage===stage));
 $('#chapters').innerHTML=data.chapters[stage].map(c=>`<label class="chapter" title="${esc(c.scope)}"><input type="checkbox" value="${c.id}" ${chapters.includes(c.id)?'checked':''}><span><b>${c.id.toString().padStart(2,'0')} · ${esc(c.zh)}</b><small>${esc(c.title)}</small></span><span class="count">${data.questions.filter(q=>q.stage===stage&&q.chapters.includes(c.id)).length||'待重写'}</span></label>`).join('');
 $('#kind').innerHTML='<option value="">全部知识点</option>'+[...new Set(data.questions.filter(q=>q.stage===stage).flatMap(q=>q.topics))].map(t=>`<option ${kind===t?'selected':''} value="${esc(t)}">${esc(t)}</option>`).join('');
 $('#status').value=status;
}
function foot(){return '<footer class="page-foot"><span>原创练习 · English questions / 中文解析 · 非 Pearson 官方产品</span><button data-action="quality">资料与质量记录 ↗</button></footer>';}
function top(label,title,description){return `<div class="heading-line"><div class="breadcrumb">学习空间 <span>/ ${label}</span></div><span class="stage-pill">PURE MATHEMATICS · ${stage}</span></div><section class="intro"><div class="intro-label">A LITTLE PRACTICE. A CLEARER MIND.</div><h1>${title}</h1><p>${description}</p><span class="math-decoration" aria-hidden="true">f(x)</span><div class="intro-bottom"><strong>${stage}</strong><span>${data.questions.filter(q=>q.stage===stage).length} 道重写题</span><span class="sep">/</span><span>${data.chapters[stage].length} 个教材章节 · 每章30题</span><span class="sep">/</span><span>纸上演算 · 自主核对</span><button data-action="quality">质量记录</button></div></section>`;}
function roman(i){return ['i','ii','iii','iv','v'][i]||String(i+1);}
function questionPart(p,i,sub=false){return `<div class="${sub?'subpart':'part'}"><span class="part-label">(${sub?roman(i):String.fromCharCode(97+i)})</span><div class="part-body">${format(p.text)}${p.subparts?`<div class="subparts">${p.subparts.map((s,j)=>questionPart(s,j,true)).join('')}</div>`:''}</div>${p.subparts?'':`<span class="marks">(${p.marks})</span>`}</div>`;}
function answerPart(p,i,sub=false){const label=`(${sub?roman(i):String.fromCharCode(97+i)})`;if(p.subparts)return `<section class="answer-group"><h4>${label} ${format(p.text)}</h4>${p.subparts.map((s,j)=>answerPart(s,j,true)).join('')}</section>`;return `<section class="answer-part ${sub?'answer-subpart':''}"><div class="answer-title"><span>${label}</span><div class="final">${format(p.answer)}</div><span class="leaf-marks">${p.marks} marks</span></div><p class="explanation">${format(p.explanation)}</p><div class="mark-scheme">${p.scheme.map(r=>`<div class="mark-row"><span class="mark-code">${r.code}</span><span>${format(r.text)}</span></div>`).join('')}</div></section>`;}
function makeAnswer(q){return `<div class="answer-panel" id="answer-${q.id}" ${opened.has(q.id)?'':'hidden'}><h3>标准答案 · 中文解析 · 评分细则</h3>${q.parts.map((p,i)=>answerPart(p,i)).join('')}${q.answerFigure||''}<p class="scheme-note">M：方法分 · A：准确分（通常依赖相应方法）· B：独立得分点。等价正确解法应予认可。评分点为原创建议，非官方评分细则。</p></div>`;}
function makeCard(q,n,{exam=false}={}){
 const done=state.done.includes(q.id),saved=state.saved.includes(q.id),cs=data.chapters[q.stage];
 return `<article class="question-card" id="card-${q.id}" data-qid="${q.id}" aria-label="${q.id} ${esc(q.type)}"><div class="card-head"><div class="card-meta"><span class="q-number">Question ${String(exam?n:(q.originalNumber??n)).padStart(2,'0')}</span><span class="tag">${esc(cs.find(c=>c.id===q.chapters[0]).zh)}</span><span class="q-id">${q.id}</span>${q.editorialRevision===4?'<span class="tag">本轮修订</span>':''}</div><div class="card-actions"><button class="small-action done-label ${done?'on':''}" data-action="done" data-id="${q.id}" aria-pressed="${done}" title="手动切换已做状态">${done?'✓ 已做':'○ 未做'}</button><button class="small-action star ${saved?'on':''}" data-action="save" data-id="${q.id}" aria-pressed="${saved}" aria-label="${saved?'取消收藏':'收藏'} ${q.id}">${saved?'★':'☆'}</button><button class="small-action" data-action="refresh" data-id="${q.id}" aria-label="刷新整道题 ${q.id}" title="在当前筛选范围内换一道完整题">↻</button></div></div><div class="exam-text" lang="en"><div class="stem">${format(q.stem)}</div>${q.parts.map((p,i)=>questionPart(p,i)).join('')}</div><div class="card-footer"><button class="answer-toggle" data-action="answer" data-id="${q.id}" aria-expanded="${opened.has(q.id)}" aria-controls="answer-${q.id}">${opened.has(q.id)?'收起答案与解析 −':'查看答案与解析 ＋'}</button><span class="total-marks">Total <strong>${q.marks}</strong> marks</span></div>${exam?'':makeAnswer(q)}</article>`;
}
function matches(){return filterQuestions(data,{stage,chapters,type:kind,status,search,savedOnly:view==='saved'},state).sort((a,b)=>order.indexOf(a.id)-order.indexOf(b.id));}
function renderLibrary(){
 const saved=view==='saved';main.innerHTML=top(saved?'收藏夹':'原创题库',saved?'留给下一次的好问题。':'把时间留给思考。',saved?'把值得回顾的题目放在这里。收藏与已做互相独立，随时回来继续。':'选一个章节，找一道完整的题。在纸上推演，再用清楚的解析核对每一步。')+`<section class="batch-notice"><div><b>全章节重写 · 共750题</b><p>P1共9章，P2、P3各8章，每章30题。本轮修订68题，另校正措辞与精度。修订题保留原编号，旧的已做标记请自行核对。</p></div><div class="batch-links"><a href="assets/rewrite-books/${stage}.pdf" target="_blank" rel="noopener">下载本阶段完整题册 ↗</a><details class="chapter-downloads"><summary>按章节下载题册</summary>${data.chapters[stage].map(c=>`<a href="assets/rewrite-books/${stage}-C${String(c.id).padStart(2,'0')}.pdf" target="_blank" rel="noopener">第${c.id}章 · ${esc(c.zh)}（30题）</a>`).join('')}</details></div></section><div class="search-row"><div class="search-box">${icons.search}<input id="search" type="search" value="${esc(search)}" placeholder="搜索知识点、英文题干或题目 ID…" aria-label="搜索当前阶段题目"></div><button class="secondary mobile-only" id="show-filters">☰ 筛选</button><button class="secondary" data-action="shuffle">↻ 打乱顺序</button><button class="primary" data-action="go-paper">＋ 生成练习卷</button></div><div id="results"></div>`+foot();
 $('#search').addEventListener('input',e=>{search=e.target.value;page=1;renderResults();});
 $('#show-filters')?.addEventListener('click',openFilters);
 renderResults();
}
function renderResults(){
 const pool=matches(),pages=Math.max(1,Math.ceil(pool.length/PAGE_SIZE));page=Math.min(page,pages);const current=pool.slice((page-1)*PAGE_SIZE,page*PAGE_SIZE);
 const active=chapters.length===data.chapters[stage].length?`<span class="filter-chip">${stage} · 全部章节</span>`:chapters.length?chapters.map(c=>`<span class="filter-chip">${esc(chapterName(c).zh)}</span>`).join(''):'<span class="filter-chip">未选择章节</span>';
 $('#results').innerHTML=`<div class="result-row"><div class="active-filters">${active}${kind?`<span class="filter-chip">${esc(kind)}</span>`:''}</div><span>找到 <strong>${pool.length}</strong> 道题 ${pool.length?`· ${(page-1)*PAGE_SIZE+1}–${Math.min(page*PAGE_SIZE,pool.length)}`:''}</span></div>${current.length?current.map((q,i)=>makeCard(q,(page-1)*PAGE_SIZE+i+1)).join(''):`<div class="empty"><span class="empty-icon">∅</span><h2>${view==='saved'?'这个范围还没有收藏':'没有找到符合条件的题目'}</h2><p>可以尝试其他章节、关键词或做题状态。</p><button class="secondary" data-action="reset">重置筛选</button></div>`}<div class="pagination"><button class="secondary" data-action="prev" ${page===1?'disabled':''}>← 上一页</button><span>第 ${page} / ${pages} 页</span><button class="secondary" data-action="next" ${page===pages?'disabled':''}>下一页 →</button></div>`;
 math($('#results'));
}
function renderBooks(){main.innerHTML=top('教材','回到知识的起点。','三本教材原文件，在这里按页阅读。可切换全屏，也可在新窗口打开 PDF。')+`<div class="book-grid">${['P1','P2','P3'].map((u,i)=>`<article class="book-card"><div class="book-cover ${['blue','tan',''][i]}"><span class="book-label">PEARSON EDEXCEL IAL</span><b>${u}</b><span>Pure Mathematics ${i+1}</span></div><div class="book-content"><h2>${u} · Pure Mathematics ${i+1}</h2><p>${[235,217,233][i]} 页 · ${data.chapters[u].length} 章<br>用户提供的扫描版教材</p><button class="primary" data-action="book" data-stage="${u}">打开教材 ↗</button></div></article>`).join('')}</div><div class="notice">三个教材文件保持上传原样。同名的三份 P3 文件经 SHA-256 比对一致，仅保留一份。2023年及以前的用户上传试卷与评分细则另收录在“历年真题”区。</div>`+foot();}
function renderPapers(){
 if(paper){renderPaper();return;}
 const available=data.questions.filter(q=>q.stage===stage&&!state.done.includes(q.id)&&q.chapters.every(c=>chapters.includes(c))).length;
 main.innerHTML=top('组卷','为一次专注的练习准备。','按当前章节范围组合完整题目。只抽取未标记已做的题目，附整卷答案与中文评分说明。')+`<div class="form-panel"><h2>${stage} · 组卷设置</h2><p class="tiny">范围由左侧阶段及章节选择决定。手机请点击“调整范围”。题型与搜索关键词不影响组卷。</p><div class="notice">当前范围：${chapters.length===data.chapters[stage].length?'全部章节':chapters.length?chapters.map(c=>esc(chapterName(c).zh)).join('、'):'未选择章节'}<br>可用未做题：<strong>${available}</strong> 道</div><label class="choice"><input type="radio" name="paper-mode" value="practice" checked><span><b>章节练习卷</b><small>按章节覆盖与题型多样性抽取，总分依题目计算。</small></span></label><div class="field-row"><label>章节练习卷题数<select id="paper-count"><option value="3">3 道题</option><option value="5" selected>5 道题</option><option value="10">10 道题</option><option value="15">15 道题</option></select></label></div><div class="button-row"><button class="primary" data-action="compose">生成新试卷 →</button><button class="secondary" data-action="adjust-scope">调整范围</button></div><div id="paper-error" role="alert"></div></div>`+foot();
}
function renderPaper(){
 const questions=paper.ids.map(id=>data.questions.find(q=>q.id===id));
 if(questions.some(q=>!q)){paper=null;savePaper();renderPapers();return;}
 const total=questions.reduce((a,q)=>a+q.marks,0);
 main.innerHTML=`<div class="heading-line"><div class="breadcrumb">学习空间 <span>/ 已生成试卷</span></div><span class="stage-pill">${esc(paper.stage)} · ORIGINAL PRACTICE</span></div><div class="paper-heading"><div class="paper-label">PURE PRACTICE · ORIGINAL QUESTIONS</div><h2>Pure Mathematics ${paper.stage.slice(1)}<br>${paper.full?'Practice Examination':'Chapter Practice'}</h2><p>${paper.full?'Time allowed: 1 hour 30 minutes · ':''}Answer all questions. Show sufficient working.<br>${questions.length} questions · Total ${total} marks · ${esc(paper.date)}</p></div><div class="paper-tools"><div class="button-row"><button class="primary" data-action="paper-answers">${answersOpen?'收起整卷答案':'查看整卷答案与解析'}</button><button class="secondary" data-action="print">打印 / 存为 PDF</button></div><div class="button-row"><button class="secondary" data-action="paper-done">整卷标记已做</button><button class="secondary" data-action="new-paper">重新组卷</button></div></div><div class="paper">${questions.map((q,i)=>makeCard(q,i+1,{exam:true})).join('')}</div>${answersOpen?`<section class="paper-answers"><div class="paper-title">Answers and Suggested Mark Scheme</div>${questions.map((q,i)=>`<section class="question-card"><div class="card-head"><span class="q-number">Question ${i+1} · ${q.id} · ${q.marks} marks</span></div>${makeAnswer(q).replace(' hidden','')}</section>`).join('')}</section>`:''}`+foot();math();
}
function render(){
 $$('.topbar .nav').forEach(b=>b.classList.toggle('active',b.dataset.view===view));
 if(view==='library'||view==='saved')renderLibrary();else if(view==='books')renderBooks();else renderPapers();
 $('#saved-count').textContent=state.saved.length;
}
function navigate(v){view=v;page=1;history.replaceState(null,'',`#${v}`);render();window.scrollTo({top:0,behavior:'instant'});}
function openFilters(){$('#sidebar').classList.add('open');$('#close-filters').focus();}
function closeFilters(){$('#sidebar').classList.remove('open');}
function resetFilters(){chapters=data.chapters[stage].map(c=>c.id);kind='';status='all';search='';page=1;renderSidebar();render();}
function showQuality(){
 $('#quality-content').innerHTML=`<h3>全章节重写 · 750题内部复核稿</h3><p>P1共9章270题，P2共8章240题，P3共8章240题；每章30题。</p><p>本轮对全部750题作编辑扫描，实质重写68题，另校正歧义、精度与重复考法；按实际依赖关系设置(a)、(b)(i)(ii)等层级，题图和答案图分别展示。题库不提供在线作答或自动判分。</p><p>每题含至少两项主设问、标准答案、中文解析及建议评分细则。已检查题量、ID、逐级分值和公式渲染，并对可计算结果进行符号、数值及人工内部复核。</p><p>未完成外部教师逐题审阅。当前材料为原创练习稿，并非Pearson官方试题。真题区另有33套、323道2020—2023年原题，保留原图原页，附中文解答与官方评分标准。</p><p>收藏与已做记录保存在当前浏览器。</p>`;$('#report-dialog').showModal();
}
let pdfDoc=null,pdfPage=1,pdfScale=1,pdfLoading=0,pdfRenderTask=null,pdfSerial=0;
async function openBook(u){
 const token=++pdfLoading;const dialog=$('#pdf-dialog');if(!dialog.open)dialog.showModal();$('#pdf-title').textContent=`${u} · Pure Mathematics ${u.slice(1)}`;$('#pdf-original').href=`assets/${u.toLowerCase()}.pdf`;$('#pdf-message').textContent='教材较大，首次加载请稍候…';$('#pdf-canvas').hidden=true;pdfScale=1;pdfPage=1;
 try{
  const pdfjs=await import('./assets/pdfjs/pdf.mjs');pdfjs.GlobalWorkerOptions.workerSrc=new URL('./assets/pdfjs/pdf.worker.mjs',import.meta.url).href;
  const doc=await pdfjs.getDocument({url:`assets/${u.toLowerCase()}.pdf`,isEvalSupported:false}).promise;
  if(token!==pdfLoading){doc.destroy();return;}
  if(pdfDoc)pdfDoc.destroy();pdfDoc=doc;$('#pdf-total').textContent=`/ ${doc.numPages}`;$('#pdf-page').max=doc.numPages;$('#pdf-message').textContent='';await renderPdf();
 }catch(e){if(token!==pdfLoading)return;$('#pdf-message').textContent='内嵌阅读器暂时无法加载，请点击上方“原文件”在新窗口阅读。';console.error('PDF loading failed',e);}
}
async function renderPdf(){
 if(!pdfDoc)return;const serial=++pdfSerial;
 if(pdfRenderTask){try{pdfRenderTask.cancel();await pdfRenderTask.promise;}catch{}pdfRenderTask=null;}
 try{
  const p=await pdfDoc.getPage(pdfPage);if(serial!==pdfSerial)return;
  const base=p.getViewport({scale:1}),width=Math.max(180,$('#pdf-scroll').clientWidth-32),fit=Math.min(width,950)/base.width,css=p.getViewport({scale:fit*pdfScale}),dpr=Math.min(window.devicePixelRatio||1,2);
  const canvas=$('#pdf-canvas'),v=p.getViewport({scale:fit*pdfScale*dpr});canvas.width=v.width;canvas.height=v.height;canvas.style.width=`${css.width}px`;canvas.style.height=`${css.height}px`;canvas.hidden=false;
  pdfRenderTask=p.render({canvasContext:canvas.getContext('2d'),viewport:v});await pdfRenderTask.promise;
  if(serial!==pdfSerial)return;$('#pdf-page').value=pdfPage;$('#pdf-prev').disabled=pdfPage===1;$('#pdf-next').disabled=pdfPage===pdfDoc.numPages;$('#pdf-zoom').textContent=pdfScale===1?'适合宽度':`${Math.round(pdfScale*100)}%`;$('#pdf-scroll').scrollTo({top:0,left:0});
 }catch(e){if(e?.name!=='RenderingCancelledException'){$('#pdf-message').textContent='此页渲染失败，可打开原文件阅读。';console.error(e);}}
}
async function fullscreenPdf(){
 const dialog=$('#pdf-dialog'),expand=!dialog.classList.contains('expanded');
 dialog.classList.toggle('expanded',expand);$('#pdf-fullscreen').textContent=expand?'退出全屏':'全屏阅读';
 try{if(expand&&document.documentElement.requestFullscreen)await document.documentElement.requestFullscreen();else if(!expand&&document.fullscreenElement)await document.exitFullscreen();}catch{/* Viewport fullscreen remains available when native fullscreen is unsupported. */}
 await renderPdf();
}
async function handleAction(action,el){
 const id=el.dataset.id;
 if(action==='answer'){if(opened.has(id))opened.delete(id);else opened.add(id);const panel=$(`#answer-${id}`);panel.hidden=!opened.has(id);el.setAttribute('aria-expanded',String(opened.has(id)));el.textContent=opened.has(id)?'收起答案与解析 −':'查看答案与解析 ＋';if(opened.has(id))math(panel);return;}
 if(action==='save'||action==='done'){
  const key=action==='save'?'saved':'done';state[key]=state[key].includes(id)?state[key].filter(a=>a!==id):[...state[key],id];saveState();renderResults();return;
 }
 if(action==='refresh'){
  const pool=matches(),visible=$$('#results article[data-qid]').map(a=>a.dataset.qid),options=pool.filter(q=>!visible.includes(q.id));
  if(!options.length){toast('当前筛选范围没有其他题目可替换，请扩大范围。');return;}
  const next=shuffle(options)[0],at=order.indexOf(id),other=order.indexOf(next.id);[order[at],order[other]]=[order[other],order[at]];opened.delete(next.id);renderResults();toast('已换成另一道完整题目');return;
 }
 if(action==='shuffle'){order=shuffle(data.questions.filter(q=>q.stage===stage).map(q=>q.id));page=1;renderResults();toast('题目顺序已打乱');return;}
 if(action==='reset'){resetFilters();return;}
 if(action==='prev'||action==='next'){page+=action==='next'?1:-1;renderResults();$('#results').scrollIntoView({block:'start',behavior:'smooth'});return;}
 if(action==='quality'){showQuality();return;}
 if(action==='go-paper'){navigate('papers');return;}
 if(action==='adjust-scope'){if(innerWidth<=760)openFilters();else{const el=$('#chapters input');el?.focus();$('#sidebar').scrollTo({top:0,behavior:'smooth'});}return;}
 if(action==='compose'){
  const err=$('#paper-error');if(!chapters.length){err.innerHTML='<div class="error-box">请至少选择一个章节。</div>';return;}
  el.disabled=true;el.textContent='正在检查组合…';await new Promise(r=>setTimeout(r,30));
  const result=composePaper(data,{stage,chapters,count:Number($('#paper-count').value),full:$('input[name="paper-mode"]:checked').value==='full'},state);
  if(result.error){err.innerHTML=`<div class="error-box">${esc(result.error)}</div>`;el.disabled=false;el.textContent='生成新试卷 →';return;}
  paper={stage,ids:result.questions.map(q=>q.id),full:result.full,date:new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date())};answersOpen=false;savePaper();renderPaper();window.scrollTo({top:0,behavior:'smooth'});return;
 }
 if(action==='paper-answers'){answersOpen=!answersOpen;renderPaper();return;}
 if(action==='new-paper'){paper=null;answersOpen=false;savePaper();renderPapers();return;}
 if(action==='paper-done'){state.done=[...new Set([...state.done,...paper.ids])];saveState();toast('整卷已标记为已做；不会被后续组卷抽取');return;}
 if(action==='print'){window.print();return;}
 if(action==='book'){await openBook(el.dataset.stage);return;}
}
async function init(){
 try{
  const res=await fetch('data/bank.json?v=editorial-v4');if(!res.ok)throw Error(`HTTP ${res.status}`);data=validateBank(await res.json());ids=new Set(data.questions.map(q=>q.id));state=cleanState(safeRead(STORE_KEY,{}),ids);
  const old=safeRead('pure-practice-paper-v1',null);if(old&&data.chapters[old.stage]&&Array.isArray(old.ids)&&old.ids.length&&old.ids.every(id=>ids.has(id)&&id.startsWith(old.stage))&&new Set(old.ids).size===old.ids.length&&typeof old.date==='string')paper=old;
  const params=new URLSearchParams(location.search);if(data.chapters[params.get('stage')])stage=params.get('stage');search=params.get('q')||'';const hash=location.hash.slice(1);if(['library','saved','papers','books'].includes(hash))view=hash;
  chapters=data.chapters[stage].map(c=>c.id);resetOrder();renderSidebar();render();
  $$('.topbar .nav').forEach(b=>b.addEventListener('click',()=>navigate(b.dataset.view)));
  $$('#stage-switch button').forEach(b=>b.addEventListener('click',()=>setStage(b.dataset.stage)));
  $('#chapters').addEventListener('change',()=>{chapters=$$('#chapters input:checked').map(x=>Number(x.value));page=1;render();});
  $('#all-chapters').addEventListener('click',()=>{chapters=data.chapters[stage].map(c=>c.id);page=1;renderSidebar();render();});
  $('#kind').addEventListener('change',e=>{kind=e.target.value;page=1;render();});$('#status').addEventListener('change',e=>{status=e.target.value;page=1;render();});$('#reset').addEventListener('click',resetFilters);
  $('#sidebar-book').addEventListener('click',()=>openBook(stage));$('#close-filters').addEventListener('click',closeFilters);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')closeFilters();});
  document.addEventListener('click',e=>{const a=e.target.closest('[data-action]');if(a)handleAction(a.dataset.action,a).catch(err=>{console.error(err);toast('操作未完成，请稍后重试。');});const c=e.target.closest('[data-close]');if(c)$(`#${c.dataset.close}`).close();});
  $('#settings').addEventListener('click',()=>{$('#personal-stats').innerHTML=`<span><b>${state.saved.length}</b>收藏</span><span><b>${state.done.length}</b>已做 / ${data.questions.length} 道</span><span>完成进度 ${Math.round(state.done.length/data.questions.length*100)}%</span>`;$('#personal-dialog').showModal();});
  $('#export-state').addEventListener('click',()=>{const blob=new Blob([JSON.stringify({...state,exportedAt:new Date().toISOString()},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='pure-practice-backup.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  $('#import-file').addEventListener('change',async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>1024*1024)throw Error('备份文件过大');const raw=JSON.parse(await file.text());if(raw.version!==1||!Array.isArray(raw.done)||!Array.isArray(raw.saved))throw Error('不是有效的题库备份');const incoming=cleanState(raw,ids);state=cleanState({saved:[...state.saved,...incoming.saved],done:[...state.done,...incoming.done]},ids);saveState();$('#personal-dialog').close();render();toast('备份已合并');}catch(err){toast(err.message||'无法读取备份');}finally{e.target.value='';}});
  $('#pdf-prev').addEventListener('click',()=>{if(pdfPage>1){pdfPage--;renderPdf();}});$('#pdf-next').addEventListener('click',()=>{if(pdfDoc&&pdfPage<pdfDoc.numPages){pdfPage++;renderPdf();}});$('#pdf-page').addEventListener('change',e=>{if(pdfDoc){const value=Number(e.target.value);if(!Number.isInteger(value)||value<1||value>pdfDoc.numPages){e.target.value=pdfPage;return;}pdfPage=value;renderPdf();}});
  $('#pdf-in').addEventListener('click',()=>{pdfScale=Math.min(3,pdfScale+.25);renderPdf();});$('#pdf-out').addEventListener('click',()=>{pdfScale=Math.max(.5,pdfScale-.25);renderPdf();});$('#pdf-fullscreen').addEventListener('click',fullscreenPdf);
  $('#pdf-dialog').addEventListener('close',()=>{pdfLoading++;$('#pdf-dialog').classList.remove('expanded');$('#pdf-fullscreen').textContent='全屏阅读';if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});});
  document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement){$('#pdf-dialog').classList.remove('expanded');$('#pdf-fullscreen').textContent='全屏阅读';if($('#pdf-dialog').open)renderPdf();}});
  let resize;window.addEventListener('resize',()=>{clearTimeout(resize);resize=setTimeout(()=>{if($('#pdf-dialog').open)renderPdf();},160);});
 }catch(err){console.error(err);main.innerHTML=`<div class="empty"><h1>题库暂时无法载入</h1><p>请通过 HTTP 服务运行完整项目，并确认 data/bank.json 可访问。</p><button class="primary" onclick="location.reload()">重新加载</button></div>`;}
}
init();
