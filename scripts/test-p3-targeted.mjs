import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {chapterMatches} from '../dist/core.js';
import {applyClassification} from '../dist/classification.js';
import {applyP3PastScope} from '../dist/p3-past-scope.js';
const read=path=>JSON.parse(fs.readFileSync(new URL('../'+path,import.meta.url),'utf8'));
const source=read('dist/data/past-bank.json'),scope=read('dist/data/p3-past-scope.json'),audit=read('editorial/p3-targeted/source-audit.json');
const raw=structuredClone(source),before=JSON.stringify(raw.questions.filter(q=>q.stage!=='P3'));
const bank=applyClassification(raw,read('dist/data/classification.json'));
const otherBefore=JSON.stringify(bank.questions.filter(q=>q.stage!=='P3'));
applyP3PastScope(bank,scope);
assert.equal(JSON.stringify(bank.questions.filter(q=>q.stage!=='P3')),otherBefore);
const questions=bank.questions.filter(q=>q.stage==='P3');
assert.equal(questions.length,161);assert.equal(scope.questionCount,161);
assert.deepEqual(Object.keys(scope.questions).sort(),questions.map(q=>q.id).sort());
assert.deepEqual(Object.keys(audit.questions).sort(),questions.map(q=>q.id).sort());
function canonical(x){if(Array.isArray(x))return '['+x.map(canonical).join(',')+']';if(x&&typeof x==='object')return '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canonical(x[k])).join(',')+'}';return JSON.stringify(x);}
const digest=x=>crypto.createHash('sha256').update(canonical(x)).digest('hex');
for(const q of questions){
 const original=source.questions.find(x=>x.id===q.id),entry=scope.questions[q.id];
 assert.equal(audit.questions[q.id].questionFingerprint,digest({searchText:original.searchText,sourcePages:original.sourcePages,marks:original.marks}),q.id);
 assert.equal(audit.questions[q.id].answerFingerprint,digest(original.markSchemePages),q.id);
 assert.deepEqual(q.requiredChapters,q.chapterLinks);
 assert.deepEqual([...entry.requirements.map(r=>r.chapter)].sort((a,b)=>a-b),q.requiredChapters);
 assert(entry.requirements.every(r=>r.skills.length));
}
// All 256 chapter combinations: targeted permits selected-to-selected mixtures,
// while cross mode also admits a question with any selected chapter.
for(let mask=0;mask<256;mask++){
 const selected=Array.from({length:8},(_,i)=>i+1).filter(n=>mask&(1<<(n-1)));
 for(const q of questions){
  const required=new Set(scope.questions[q.id].requiredChapters);
  const expectedStrict=selected.length>0&&[...required].every(n=>selected.includes(n));
  const expectedCross=selected.length>0&&selected.some(n=>required.has(n));
  assert.equal(chapterMatches(q,selected,false),expectedStrict,q.id+' strict '+selected);
  assert.equal(chapterMatches(q,selected,true),expectedCross,q.id+' cross '+selected);
 }
}
const requirements={
 'P3-2020-10-Q08':[6],
 'P3-2021-01-Q10':[3,6],
 'P3-2021-06-Q07':[6],
 'P3-2021-10-Q06':[4,6],
 'P3-2022-10-Q02':[2],
 'P3-2023-01-Q07':[3,6],
 'P3-2023-01-Q08':[4,7],
 'P3-2024-01-Q04':[1,2,5,6],
 'P3-2024-01-Q06':[6],
 'P3-2024-06-Q02':[1,7],
 'P3-2024-06-Q08':[5,6,8],
 'P3-2024-06-Q09':[6],
 'P3-2024-10-Q09':[1,6,7],
 'P3-2025-01-Q02':[5],
 'P3-2025-01-Q10':[6],
 'P3-2025-06-Q05':[4,7],
 'P3-2025-06-Q07':[6,8],
 'P3-2025-06A-Q04':[1,7],
 'P3-2025-06A-Q05':[4,6]
};
for(const[id,expected]of Object.entries(requirements))assert.deepEqual(scope.questions[id].requiredChapters,expected,id);
for(const id of ['P3-2020-01-Q05','P3-2023-06-Q05','P3-2024-01-Q09']){
 const q=questions.find(q=>q.id===id);assert(chapterMatches(q,[3,4],false));assert(!chapterMatches(q,[3],false));
}
for(const id of ['P3-2021-10-Q06','P3-2025-06A-Q05']){
 const q=questions.find(q=>q.id===id);assert(!chapterMatches(q,[6],false));assert(chapterMatches(q,[4,6],false));assert(chapterMatches(q,[6],true));
}
const partial=structuredClone(scope);delete partial.questions['P3-2025-01-Q10'];
assert.throws(()=>applyP3PastScope(structuredClone(source),partial),/章节范围缺失/);
const invalid=structuredClone(scope);invalid.questions['P3-2025-01-Q10'].requirements=[];
assert.throws(()=>applyP3PastScope(structuredClone(source),invalid),/章节范围缺失/);
assert.equal(JSON.stringify(source.questions.filter(q=>q.stage!=='P3')),before);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(new URL('../editorial/p3-targeted/requirements.txt',import.meta.url))).digest('hex'),audit.sourceFileSha256);
console.log('PASS 161 source-linked P3 scopes, 256 chapter selections, identity vs differentiation cases, whole-question coverage and P1/P2 preservation');
