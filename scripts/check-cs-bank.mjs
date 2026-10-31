import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=path=>JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'));
const bank=read('dist/data/cs-question-bank.json'),taxonomy=read('dist/data/cs-chapters.json'),manifest=read('dist/data/igcse-online-files.json');
const sources=manifest.files.filter(file=>file.subject==='cs'&&file.type==='qp');
assert.equal(bank.papers.length,sources.length);
assert.equal(bank.papers.length,84);
assert.equal(bank.questions.length,692);
const sections=new Set(taxonomy.chapters.flatMap(chapter=>chapter.sections.map(section=>section.id)));
assert.equal(sections.size,taxonomy.chapters.flatMap(chapter=>chapter.sections).length);
assert.equal(new Set(bank.questions.map(q=>q.id)).size,bank.questions.length);
for(const paper of bank.papers){
 const source=sources.find(file=>file.path===paper.qp),ms=manifest.files.find(file=>file.filename===source.filename.replace('_qp_','_ms_'));
 assert.equal(paper.ms,ms.path);
 const questions=bank.questions.filter(q=>q.paper===paper.id);
 assert.deepEqual(questions.map(q=>q.number),Array.from({length:questions.length},(_,i)=>i+1));
 assert.equal(questions.reduce((sum,q)=>sum+q.marks,0),paper.year<2023&&paper.group==='paper2'?50:75,paper.id+' must retain every mark');
 for(const q of questions){
  assert.equal(q.group,paper.group);assert.equal(q.year,paper.year);assert.equal(q.session,paper.session);
  assert(q.sections.length);assert(q.sections.every(id=>sections.has(id)),q.id);
  assert.deepEqual(q.chapters,[...new Set(q.sections.map(id=>Number(id.split('.')[0])))].sort((a,b)=>a-b));
  assert(q.marks>0&&q.searchText.length>15,q.id);
  assert(q.pages.length&&q.markSchemePages.length&&q.officialMarkScheme,q.id);
  assert.equal(q.contextPages>0,q.paperType===2&&q.year<2023&&q.number===1,q.id+' pre-release context');
  for(const [pieces,path] of [[q.pages,paper.qp],[q.markSchemePages,paper.ms]])for(const piece of pieces){
   assert.equal(piece.pdf,path);assert(piece.page>1&&piece.page<=manifest.files.find(file=>file.path===path).pages,q.id);
   const [x,y,w,h]=piece.crop;assert(x>=0&&y>=0&&w>0&&h>0&&x+w<=1.000001&&y+h<=1.000001,q.id);
  }
  assert(!/Permission to reproduce|copyright acknowledgements/i.test(q.searchText),q.id+' legal footer leaked into question');
 }
}
const question=id=>bank.questions.find(q=>q.id===id);
assert(question('CS-2024-M-12-Q02').sections.includes('3.1'),'CPU question must appear in computer architecture');
assert(question('CS-2021-M-12-Q03').sections.includes('3.2'),'device question must appear in input/output');
assert.deepEqual(question('CS-2024-M-22-Q10').sections,['8.1'],'maintainable programming is not a legacy topic');
assert(question('CS-2019-M-12-Q05').sections.includes('10.2'),'pre-2023 Paper 1 logic remains available');
assert(fs.readFileSync(new URL('../dist/index.html',import.meta.url),'utf8').includes('href="cs-bank.html"'));
const html=fs.readFileSync(new URL('../dist/cs-bank.html',import.meta.url),'utf8');
assert(html.includes('cs-cross-chapter')&&html.includes('cs-chapters')&&html.includes('igcse.html?subject=cs'));
console.log('PASS: 692 CS questions, 84 official QP/MS pairs, full paper marks, chapter/section tags and pre-release context.');
