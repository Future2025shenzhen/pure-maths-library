import fs from 'node:fs';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';

const root=new URL('../dist/',import.meta.url);
const bank=JSON.parse(fs.readFileSync(new URL('data/physics-question-bank.json',root),'utf8'));
assert.equal(bank.papers.length,251);
assert.equal(bank.questions.length,4590);
assert.equal(new Set(bank.papers.map(p=>p.id)).size,251);
assert.equal(new Set(bank.questions.map(q=>q.id)).size,4590);
assert.equal(bank.questions.filter(q=>q.group==='mcq-theory').length,4254);
assert.equal(bank.questions.filter(q=>q.group==='practical').length,336);
assert.equal(bank.questions.filter(q=>[1,2].includes(q.paperType)).length,3360);
assert.equal(bank.questions.filter(q=>q.answer==='Question Discounted').length,1);
for(const question of bank.questions){
 assert(question.pages.length&&question.markSchemePages.length,question.id);
 assert(question.officialMarkScheme&&question.verification.includes('不添加自创解析'),question.id);
 assert(question.pages.every(page=>page.pdf.includes('_qp_')&&page.crop.length===4),question.id);
 assert(question.markSchemePages.every(page=>page.pdf.includes('_ms_')&&page.crop.length===4),question.id);
 assert(question.chapters.length&&question.sections.length,question.id);
 if([1,2].includes(question.paperType))assert(['A','B','C','D','Question Discounted'].includes(question.answer),question.id);
 else assert.equal(question.answer,null,question.id);
}
const html=fs.readFileSync(new URL('igcse.html',root),'utf8');
const app=fs.readFileSync(new URL('igcse-online.js',root),'utf8');
const bankHtml=fs.readFileSync(new URL('physics-bank.html',root),'utf8');
const bankApp=fs.readFileSync(new URL('physics-bank.js',root),'utf8');
assert(html.includes('id="practice"')&&html.includes('hidden>原创练习'));
assert(app.includes("$('practice').hidden=subject==='physics'"));
assert(bankHtml.includes('允许跨章节')&&bankHtml.includes('真题收藏')&&bankHtml.includes('上下连续滑动'));
assert(bankApp.includes('IntersectionObserver')&&bankApp.includes('pure-physics-notes-v1'));
for(const source of [bankApp]){
 const check=spawnSync(process.execPath,['--check','--input-type=module'],{input:source,encoding:'utf8'});
 assert.equal(check.status,0,check.stderr);
}
console.log('PASS Physics official bank: 251 papers, 4590 questions, official MS crops, no Physics mock entry');
