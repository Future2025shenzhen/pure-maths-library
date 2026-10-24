const $=id=>document.getElementById(id), params=new URLSearchParams(location.search);
const names={qp:'题卷',ms:'评分标准',er:'考官报告',gt:'分数线',ci:'实验说明',pm:'预发布材料'};
const seasons={m:'2–3月',s:'5–6月',w:'10–11月'};
let subject=params.get('subject')==='cs'?'cs':'physics',files=[],pairs=[],index=new Map(),selected=null;
for(let y=2024;y>=2019;y--){const option=new Option(String(y),String(y));$('year').add(option)}
function sameExam(a,b){return a&&b&&a.subject===b.subject&&a.year===b.year&&a.session===b.session&&a.paper===b.paper&&['qp','ms'].includes(a.type)&&['qp','ms'].includes(b.type)}
function pair(file,type){return ['qp','ms'].includes(file.type)?index.get(file.filename.replace(/_(qp|ms)_/,'_'+type+'_')):null}
function selectedStyle(){for(const card of document.querySelectorAll('.paper'))card.classList.toggle('selected',card.dataset.file===selected?.filename||sameExam(index.get(card.dataset.file),selected))}
function select(file){
 if(!file)return;selected=file;
 const url=new URL('igcse-reader.html',location.href);url.search=new URLSearchParams({subject:file.subject,file:file.filename});
 $('reader-frame').hidden=false;$('reader-empty').hidden=true;$('reader-frame').src=url.href;
 $('direct').href=url.href;$('direct').removeAttribute('aria-disabled');
 $('title').textContent=(subject==='physics'?'物理':'计算机')+' · '+file.year+' '+seasons[file.session]+(file.paper?' · Paper '+file.paper:'')+' · '+names[file.type];
 const query=new URLSearchParams(location.search);query.set('subject',subject);query.set('file',file.filename);history.replaceState(null,'','?'+query);
 selectedStyle();if(matchMedia('(max-width:760px)').matches)$('workspace').classList.add('reading');
}
function clearReader(){selected=null;$('reader-frame').hidden=true;$('reader-frame').removeAttribute('src');$('reader-empty').hidden=false;$('reader-empty').querySelector('h2').textContent='当前筛选没有资料';$('reader-empty').querySelector('p').textContent='请更换年份、考季、资料类型或搜索内容。';$('title').textContent='暂无试卷';$('direct').removeAttribute('href');$('direct').setAttribute('aria-disabled','true')}
function list(){
 document.querySelectorAll('[data-subject]').forEach(b=>b.classList.toggle('active',b.dataset.subject===subject));
 $('practice').href='igcse-practice.html?subject='+subject;
 document.title=(subject==='physics'?'Physics 0625':'Computer Science 0478')+' · Pure Practice';
 const year=$('year').value,session=$('session').value,kind=$('kind').value,q=$('search').value.trim().toLowerCase();
 const rows=pairs.filter(f=>f.subject===subject&&(year==='all'||String(f.year)===year)&&(session==='all'||f.session===session)&&(kind==='all'||(kind==='papers'?['qp','ms'].includes(f.type):f.type===kind))&&(!q||(f.filename+' '+f.paper+' '+f.year+' '+names[f.type]).toLowerCase().includes(q)));
 $('papers').replaceChildren();$('count').textContent=rows.length+' 项';
 for(const file of rows){const card=document.createElement('article');card.className='paper';card.dataset.file=file.filename;const title=document.createElement('div');title.className='paper-title';title.textContent=file.year+' '+seasons[file.session]+(file.paper?' · Paper '+file.paper[0]+' / '+file.paper.slice(1):'');const meta=document.createElement('div');meta.className='paper-meta';meta.textContent=(subject==='physics'?'Physics 0625':'Computer Science 0478')+(file.year===2020&&file.session==='s'?' · 当季编制材料':'');const actions=document.createElement('div');actions.className='paper-actions';
 for(const type of ['qp','ms']){const f=pair(file,type);if(f){const button=document.createElement('button');button.textContent=names[type];button.onclick=()=>select(f);actions.append(button)}}
 if(!actions.childNodes.length){const button=document.createElement('button');button.textContent=names[file.type]||file.type;button.onclick=()=>select(file);actions.append(button)}card.append(title,meta,actions);$('papers').append(card)}
 if(!rows.length){const message=document.createElement('p');message.textContent='没有匹配的资料。';$('papers').append(message);clearReader();return}
 if(!selected||!rows.some(f=>f.filename===selected.filename||sameExam(f,selected)))select(rows.find(f=>f.type==='qp'&&f.paper==='42')||rows.find(f=>f.type==='qp')||rows[0]);else selectedStyle();
}
function changeSubject(next){subject=next;selected=null;$('year').value='2024';$('session').value='all';$('kind').value='papers';$('search').value='';list()}
for(const button of document.querySelectorAll('[data-subject]'))button.onclick=()=>changeSubject(button.dataset.subject);
for(const id of ['year','session','kind'])$(id).onchange=list;$('search').oninput=list;
$('list-toggle').onclick=()=>$('workspace').classList.toggle('reading');
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('reader').requestFullscreen()}catch{$('direct').click()}};
window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==$('reader-frame').contentWindow||event.data?.type!=='igcse-selected')return;const file=index.get(event.data.filename);if(file&&file.subject===subject){selected=file;const url=new URL('igcse-reader.html',location.href);url.search=new URLSearchParams({subject,file:file.filename});$('direct').href=url.href;const query=new URLSearchParams(location.search);query.set('file',file.filename);history.replaceState(null,'','?'+query);$('title').textContent=(subject==='physics'?'物理':'计算机')+' · '+file.year+' '+seasons[file.session]+(file.paper?' · Paper '+file.paper:'')+' · '+names[file.type];selectedStyle()}});
async function start(){try{
 const response=await fetch('data/igcse-online-files.json');if(!response.ok)throw Error('HTTP '+response.status);const data=await response.json();files=data.files;index=new Map(files.map(f=>[f.filename,f]));pairs=files.filter(f=>f.type!=='ms'||!index.has(f.filename.replace('_ms_','_qp_')));pairs.sort((a,b)=>b.year-a.year||({w:3,s:2,m:1}[b.session]-{w:3,s:2,m:1}[a.session])||Number(a.paper||0)-Number(b.paper||0)||a.filename.localeCompare(b.filename));
 const requested=index.get(params.get('file'));$('year').value=requested&&requested.subject===subject?String(requested.year):'2024';if(requested&&requested.subject===subject){selected=requested;if(!['qp','ms'].includes(requested.type))$('kind').value=requested.type}list();if(requested&&requested.subject===subject)select(requested);
 }catch(error){$('count').textContent='试卷目录暂未载入';$('reader-empty').querySelector('p').textContent='请点击重新载入。';$('retry').hidden=false;$('retry').onclick=()=>location.reload();console.error(error)}}
start();
