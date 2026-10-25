import fs from 'node:fs';
import assert from 'node:assert/strict';

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
 if([1,2].includes(question.paperType))assert(['A','B','C','D','Question Discounted'].includes(question.answer),question.id);
 else assert.equal(question.answer,null,question.id);
}
const html=fs.readFileSync(new URL('igcse.html',root),'utf8');
const app=fs.readFileSync(new URL('igcse-online.js',root),'utf8');
assert(html.includes('id="practice"')&&html.includes('hidden>原创练习'));
assert(app.includes("$('practice').hidden=subject==='physics'"));
console.log('PASS Physics official bank: 251 papers, 4590 questions, official MS crops, no Physics mock entry');
