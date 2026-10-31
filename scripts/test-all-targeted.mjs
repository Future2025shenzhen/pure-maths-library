import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {applyPastScope} from '../dist/past-scope.js';
import {applyCsPastScope,csScopeMatches} from '../dist/cs-past-scope.js';
import {chapterMatches} from '../dist/core.js';
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url)));
const stable=v=>Array.isArray(v)?v.map(stable):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,stable(v[k])])):v;
const digest=v=>createHash('sha256').update(JSON.stringify(stable(v))).digest('hex');
const raw=read('dist/data/past-bank.json'),csRaw=read('dist/data/cs-question-bank.json'),taxonomy=read('dist/data/cs-chapters.json');
const scopes=Object.fromEntries(['P1','P2','P3'].map(s=>[s,read(`dist/data/${s.toLowerCase()}-past-scope.json`)]));
const audit=read('editorial/all-targeted/source-audit.json');
for(const q of [...raw.questions.filter(q=>q.stage!=='P3'),...csRaw.questions]){
 const a=audit.questions[q.id];assert(a,q.id);
 const keys=q.stage?['searchText','sourcePages','marks']:['searchText','pages','marks'];
 assert.equal(digest(Object.fromEntries(keys.map(k=>[k,q[k]]))),a.questionFingerprint,q.id+' changed question');
 assert.equal(digest(q.markSchemePages),a.answerFingerprint,q.id+' changed answer');
}
for(const s of ['P1','P2','CS'])assert.equal(createHash('sha256').update(fs.readFileSync(new URL(`../editorial/all-targeted/${s}-requirements.txt`,import.meta.url))).digest('hex'),audit.annotationSha256[s]);
const bank=applyPastScope(structuredClone(raw),scopes);
for(const stage of ['P1','P2','P3']){
 const qs=bank.questions.filter(q=>q.stage===stage),max=stage==='P1'?9:8;
 assert.equal(qs.length,scopes[stage].questionCount);
 for(let mask=0;mask<1<<max;mask++){
  const selected=Array.from({length:max},(_,i)=>i+1).filter(n=>mask&(1<<(n-1)));
  for(const q of qs){const required=q.requiredChapters;
   assert.equal(chapterMatches(q,selected,false),required.every(n=>selected.includes(n))&&selected.length>0);
   assert.equal(chapterMatches(q,selected,true),required.some(n=>selected.includes(n)));
  }
 }
}
for(const [id,expected] of Object.entries({'P1-2019-01-Q12':[8,9],'P1-2024-01-Q06':[6],'P1-2025-06-Q02':[8],'P2-2019-06-Q06':[1,6],'P2-2025-01-Q07':[3,8],'P2-2025-06A-Q08':[1,7,8]}))assert.deepEqual(bank.questions.find(q=>q.id===id).requiredChapters,expected,id);
const csScope=read('dist/data/cs-past-scope.json'),cs=applyCsPastScope(structuredClone(csRaw),csScope,taxonomy);
assert.equal(cs.questions.length,692);assert.equal(Object.keys(csScope.questions).length,692);
for(let mask=0;mask<1<<11;mask++){
 const selected=taxonomy.chapters.filter(c=>mask&(1<<(c.id-1))).flatMap(c=>c.sections.map(s=>s.id));
 for(const q of cs.questions){assert.equal(csScopeMatches(q,selected),q.requiredSections.every(s=>selected.includes(s))&&selected.length>0);assert.equal(csScopeMatches(q,selected,true),q.requiredSections.some(s=>selected.includes(s)));}
}
for(const q of cs.questions){
 assert(csScopeMatches(q,q.requiredSections));assert(!csScopeMatches(q,[]));
 for(const omitted of q.requiredSections)assert(!csScopeMatches(q,q.requiredSections.filter(s=>s!==omitted)));
}
for(const [id,expected] of Object.entries({'CS-2024-S-11-Q05':['3.1','3.3'],'CS-2024-S-12-Q05':['3.1'],'CS-2024-S-13-Q04':['3.3'],'CS-2024-W-23-Q11':['9.2'],'CS-2020-W-13-Q10':['10.2'],'CS-2019-W-21-Q05':['9.1','9.2']}))assert.deepEqual(cs.questions.find(q=>q.id===id).requiredSections,expected,id);
assert.throws(()=>applyPastScope(structuredClone(raw),{...scopes,P1:{questions:{}}}));
assert.throws(()=>applyCsPastScope(structuredClone(csRaw),{questions:{}},taxonomy));
assert(!csScopeMatches({sections:['3.1']},['3.1']));
// Overlay keeps source crops, answers, marks and persistent record IDs intact.
for(const [before,after] of [[raw,bank],[csRaw,cs]])for(let i=0;i<before.questions.length;i++)for(const key of ['id','paper','marks','pages','sourcePages','markSchemePages','answer'])assert.deepEqual(after.questions[i][key],before.questions[i][key]);
console.log('PASS all P1/P2/CS source fingerprints, complete scope coverage, exhaustive chapter unions, section omissions, corrected examples and fail-closed metadata');
