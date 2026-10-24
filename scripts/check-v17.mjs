import fs from 'node:fs';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const past=read('dist/data/past-bank.json'),archive=read('dist/data/paper-archive.json'),classes=read('dist/data/classification.json').questions;
assert.equal(past.version,17);assert.equal(past.papers.length,58);assert.equal(past.questions.length,572);
assert.deepEqual(Object.fromEntries(['P1','P2','P3'].map(s=>[s,past.questions.filter(q=>q.stage===s).length])),{P1:211,P2:200,P3:161});
const generated=past.questions.filter(q=>q.v17Added);
assert.equal(generated.length,249);assert.equal(past.questions.filter(q=>q.officialMarkScheme&&q.officialSchemeRevision===17).length,572);assert.equal(new Set(past.questions.map(q=>q.id)).size,572);
for(const paper of archive.papers){
 const qs=past.questions.filter(q=>q.paper===paper.id).sort((a,b)=>a.number-b.number);
 assert(qs.length,paper.id+' has no question practice');
 assert.deepEqual(qs.map(q=>q.number),Array.from({length:qs.length},(_,i)=>i+1),paper.id+' numbering');
 assert.equal(qs.reduce((n,q)=>n+q.marks,0),75,paper.id+' marks');
}
for(const q of generated){
 assert(q.year===2019||q.year===2024||q.year===2025,q.id+' target year');
 assert(q.year<2025||q.month<=6,q.id+' cutoff');
 assert.equal(q.solutionSections.length,0,q.id+' no authored solution');
 assert(q.verification.includes('官方评分标准')&&q.verification.includes('未另写自拟解法'),q.id);
 assert(q.pages.length&&q.markSchemePages.length,q.id+' page mappings');
 assert.deepEqual(classes[q.id],{stage:q.stage,chapters:q.chapters},q.id+' classification');
 for(const v of [...q.pages,...q.markSchemePages]){
  assert(v.renderFromPdf&&fs.existsSync(new URL('dist/'+v.pdf,root)),q.id+' '+v.pdf);
  const [x,y,w,h]=v.crop;assert([x,y,w,h].every(Number.isFinite)&&x>=0&&y>=0&&w>0&&h>0&&x+w<=1.00001&&y+h<=1.00001,q.id+' crop');
 }
 assert(q.markSchemePages.some(v=>v.highlights?.some(h=>h.kind==='accuracy')),q.id+' visible answer highlights');
}
for(const q of past.questions){
 assert(q.markSchemePages?.length,q.id+' official scheme mapping');
 assert(q.markSchemePages.some(v=>v.highlights?.some(h=>h.kind==='accuracy')),q.id+' visible answer highlights');
}
const sql=fs.readFileSync(new URL('backend/007-complete-past-catalog.sql',root),'utf8');
for(const q of generated)assert(sql.includes(`('${q.id}','past','${q.stage}')`),q.id+' catalog');
assert.equal((sql.match(/\('P[123]-/g)||[]).length,249);
console.log('PASS v17: 572 questions across all 58 papers through June 2025; 249 additions use full source crops and official mark-scheme crops only.');
