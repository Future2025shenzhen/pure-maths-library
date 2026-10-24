import * as pdfjs from './assets/pdfjs/pdf.mjs';
pdfjs.GlobalWorkerOptions.workerSrc=new URL('./assets/pdfjs/pdf.worker.mjs',import.meta.url).href;
const $=id=>document.getElementById(id),params=new URLSearchParams(location.search),names={qp:'题卷',ms:'评分标准',er:'考官报告',gt:'分数线',ci:'实验说明',pm:'预发布材料'},seasons={m:'2–3月',s:'5–6月',w:'10–11月'};
document.body.classList.toggle('embedded',window.self!==window.top);
let files=[],byName=new Map(),current=null,documentPdf=null,loadingTask=null,renderTask=null,pageNumber=1,zoom=1,loadSerial=0,renderSerial=0;
function showMessage(text,error=false){$('message').textContent=text;$('message').classList.toggle('error',error);$('message').hidden=!text}
function matching(file,type){return ['qp','ms'].includes(file.type)?byName.get(file.filename.replace(/_(qp|ms)_/,'_'+type+'_')):null}
async function draw(){
 if(!documentPdf)return;
 const serial=++renderSerial,previous=renderTask;previous?.cancel();if(previous)try{await previous.promise}catch{}
 if(serial!==renderSerial||!documentPdf)return;
 const pdfPage=await documentPdf.getPage(pageNumber);if(serial!==renderSerial)return;
 const natural=pdfPage.getViewport({scale:1}),available=Math.max(230,$('viewport').clientWidth-28),scale=Math.min(1100,available)/natural.width*zoom,viewport=pdfPage.getViewport({scale});
 let ratio=Math.min(devicePixelRatio||1,2);ratio=Math.min(ratio,Math.sqrt(16000000/(viewport.width*viewport.height)));
 const canvas=$('canvas');canvas.width=Math.floor(viewport.width*ratio);canvas.height=Math.floor(viewport.height*ratio);canvas.style.width=viewport.width+'px';canvas.style.height=viewport.height+'px';canvas.hidden=false;showMessage('');
 $('page').value=String(pageNumber);$('prev').disabled=pageNumber<=1;$('next').disabled=pageNumber>=documentPdf.numPages;$('zoom').textContent=zoom===1?'适合宽度':Math.round(zoom*100)+'%';
 const task=pdfPage.render({canvasContext:canvas.getContext('2d'),viewport,transform:ratio===1?null:[ratio,0,0,ratio,0,0]});renderTask=task;
 try{await task.promise;if(serial===renderSerial)$('viewport').scrollTo(0,0)}catch(error){if(error.name!=='RenderingCancelledException'&&serial===renderSerial){showMessage('此页暂未显示，请点击重试。',true);$('retry').hidden=false;console.error(error)}}
}
async function open(file){
 const serial=++loadSerial;++renderSerial;renderTask?.cancel();if(loadingTask)try{await loadingTask.destroy()}catch{};if(documentPdf)try{await documentPdf.destroy()}catch{};documentPdf=null;current=file;pageNumber=1;zoom=1;
 $('canvas').hidden=true;$('attachment').hidden=true;$('retry').hidden=true;showMessage('正在载入原卷…');
 const title=(file.subject==='physics'?'Physics 0625':'Computer Science 0478')+' · '+file.year+' '+seasons[file.session]+(file.paper?' · '+file.paper:'')+' · '+names[file.type];$('document-title').textContent=title;document.title=title+' · Pure Practice';
 const relative=new URL(file.path,location.href);if(relative.origin!==location.origin)throw Error('PDF must be hosted on this website');
 $('download').href=relative.href;$('download').download=file.filename;$('download').textContent=file.filename.endsWith('.pdf')?'下载 PDF':'下载附件';$('download').hidden=false;
 $('back').href='igcse.html?'+new URLSearchParams({subject:file.subject,file:file.filename});
 $('filename').textContent=file.filename+' · '+Math.round(file.bytes/1024)+' KB';$('source').textContent='来源存档：'+file.repository+'；核验日期：2026-10-24。';
 for(const type of ['qp','ms']){const target=matching(file,type);$(type).disabled=!target;$(type).classList.toggle('active',file.type===type);$(type).onclick=()=>open(target).catch(fail)}
 const query=new URLSearchParams({subject:file.subject,file:file.filename});history.replaceState(null,'','?'+query);if(window.parent!==window)window.parent.postMessage({type:'igcse-selected',filename:file.filename},location.origin);
 if(!file.filename.endsWith('.pdf')){showMessage('');$('attachment').hidden=false;$('attachment-link').href=relative.href;$('attachment-link').download=file.filename;return}
 try{
  loadingTask=pdfjs.getDocument({url:relative.href,isEvalSupported:false});const next=await loadingTask.promise;if(serial!==loadSerial){await next.destroy();return}documentPdf=next;$('total').textContent='/ '+next.numPages;$('page').max=String(next.numPages);await draw();
 }catch(error){if(serial===loadSerial)fail(error)}
}
function fail(error){showMessage('试卷暂未载入，请点击重试；无需进入第三方网站。',true);$('retry').hidden=false;console.error(error)}
$('prev').onclick=()=>{if(documentPdf&&pageNumber>1){pageNumber--;draw().catch(fail)}};
$('next').onclick=()=>{if(documentPdf&&pageNumber<documentPdf.numPages){pageNumber++;draw().catch(fail)}};
$('page').onchange=()=>{if(documentPdf){pageNumber=Math.max(1,Math.min(documentPdf.numPages,Number.parseInt($('page').value,10)||1));draw().catch(fail)}};
$('zoom-in').onclick=()=>{zoom=Math.min(2.5,Math.round((zoom+.2)*10)/10);draw().catch(fail)};
$('zoom-out').onclick=()=>{zoom=Math.max(.6,Math.round((zoom-.2)*10)/10);draw().catch(fail)};
$('retry').onclick=()=>current?open(current).catch(fail):location.reload();
let resize;window.addEventListener('resize',()=>{clearTimeout(resize);resize=setTimeout(()=>draw().catch(fail),160)});
async function start(){
 const response=await fetch('data/igcse-online-files.json');if(!response.ok)throw Error('HTTP '+response.status);files=(await response.json()).files;byName=new Map(files.map(file=>[file.filename,file]));
 let requested=params.get('file');if(!requested&&params.get('pdf')){try{requested=decodeURIComponent(new URL(params.get('pdf')).pathname.split('/').pop())}catch{}}
 let file=byName.get(requested);const subject=params.get('subject')==='cs'?'cs':'physics';
 if(!file&&!requested)file=byName.get(subject==='physics'?'0625_w24_qp_42.pdf':'0478_w24_qp_12.pdf');
 if(!file){showMessage('未找到这份已收集的试卷，请返回列表选择。',true);$('back').href='igcse.html?subject='+subject;return}
 await open(file);
}
start().catch(fail);
