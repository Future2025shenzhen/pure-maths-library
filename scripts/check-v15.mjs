import fs from 'node:fs';
import assert from 'node:assert/strict';
import {filterQuestions,composePaper} from '../dist/core.js';

const root=new URL('../',import.meta.url);
const bank=JSON.parse(fs.readFileSync(new URL('dist/data/bank.json',root)));
const classification=JSON.parse(fs.readFileSync(new URL('dist/data/classification.json',root)));
const chapter4=bank.questions.filter(q=>q.stage==='P1'&&q.id.startsWith('P1-C04-'));
const chapter9=bank.questions.filter(q=>q.stage==='P1'&&q.id.startsWith('P1-C09-'));
const active=[...chapter4,...chapter9].filter(q=>!q.withdrawn);
const deleted4=new Set(['P1-C04-R02','P1-C04-R05','P1-C04-R07','P1-C04-R08','P1-C04-R12','P1-C04-R13','P1-C04-R14','P1-C04-R16','P1-C04-R19','P1-C04-R23','P1-C04-R26','P1-C04-R27','P1-C04-R29']);
const deleted9=new Set(['P1-C09-R04','P1-C09-R07','P1-C09-R11','P1-C09-R12','P1-C09-R14','P1-C09-R15','P1-C09-R20','P1-C09-R21','P1-C09-R24','P1-C09-R26','P1-C09-R27','P1-C09-R28','P1-C09-R29']);
const cross=new Set(['P1-C06-R12','P1-C06-R17','P1-C06-R26','P1-C06-R30']);
const additions=new Set([...Array.from({length:6},(_,i)=>`P1-C04-R${31+i}`),...Array.from({length:6},(_,i)=>`P1-C09-R${31+i}`)]);

assert.equal(bank.version,16);
assert.equal(classification.version,16);
assert.equal(bank.questions.length,790);
assert.equal(bank.questions.filter(q=>!q.withdrawn).length,738);
assert.equal(bank.questions.filter(q=>q.withdrawn).length,52);
assert.equal(chapter4.length,36);assert.equal(chapter9.length,36);
assert.equal(chapter4.filter(q=>!q.withdrawn).length,23);
assert.equal(chapter9.filter(q=>!q.withdrawn).length,23);
assert.deepEqual(new Set(chapter4.filter(q=>q.withdrawn).map(q=>q.id)),deleted4);
assert.deepEqual(new Set(chapter9.filter(q=>q.withdrawn).map(q=>q.id)),deleted9);
for(const id of cross)assert(bank.questions.find(q=>q.id===id)?.withdrawn,id);
for(const id of additions)assert(active.some(q=>q.id===id),id);

const leaves=parts=>parts.flatMap(p=>p.subparts?leaves(p.subparts):[p]);
const sources=new Map();
for(const q of active){
  assert.equal(q.editorialRevision,15,q.id);
  assert.deepEqual(q.chapters,[Number(q.id.slice(4,6))],q.id+' primary chapter');
  assert(q.sourceReferences?.length===1,q.id+' exact source');
  assert(q.sourceSummary?.length>=10,q.id+' source summary');
  assert(q.adaptationDimensions?.length>=3,q.id+' adaptation dimensions');
  assert(q.examEssence?.length>=10,q.id+' exam essence');
  assert(q.difficultyPosition?.startsWith('略难于'),q.id+' difficulty');
  assert(q.errorNotes?.length>=2,q.id+' errors');
  assert(q.designNote?.length>=10,q.id+' design');
  assert(!JSON.stringify(q).includes('采用解析所述方法'),q.id+' generic solution');
  assert.equal(q.parts.reduce((n,p)=>n+p.marks,0),q.marks,q.id+' total marks');
  for(const p of leaves(q.parts)){
    assert(p.approach&&p.solutionSteps?.length>=1,q.id+' steps');
    assert(/[\u4e00-\u9fff]/.test(p.approach+p.solutionSteps.join('')),q.id+' Chinese solution');
    assert.equal(p.scheme.reduce((n,r)=>n+r.marks,0),p.marks,q.id+' scheme marks');
    assert(p.scheme.every(r=>/^[MAB]\d+$/.test(r.code)&&r.marks>=0),q.id+' scheme codes');
  }
  const source=q.sourceReferences[0].questionId;
  sources.set(source,(sources.get(source)||0)+1);
  assert(q.sourceReferences[0].year>=2019&&q.sourceReferences[0].year<=2025,q.id+' source year');
}
assert(Math.max(...sources.values())<=3,'source reuse cap within reviewed chapters');
for(const chapter of [chapter4,chapter9]){
  const live=chapter.filter(q=>!q.withdrawn);
  const long=live.filter(q=>q.marks>=8||q.parts.length>=3);
  assert(long.length<=Math.floor(live.length/4),'long-question cap');
}

for(const q of bank.questions.filter(q=>q.stage==='P1'&&!q.id.startsWith('P1-C04-'))){
  assert(!q.chapters.includes(4),q.id+' stale secondary Chapter 4 tag');
}
for(const q of bank.questions){
  assert.deepEqual(classification.questions[q.id],{stage:q.stage,chapters:q.chapters},q.id+' classification');
}

const state={saved:[],done:[]};
for(const chapter of [4,9]){
  const filters={stage:'P1',chapters:[chapter],status:'all',search:'',type:'',savedOnly:false};
  const pool=filterQuestions(bank,filters,state);
  assert.equal(pool.length,23,`chapter ${chapter} practice pool`);
  assert(pool.every(q=>q.chapters.length===1&&q.chapters[0]===chapter));
  const paper=composePaper(bank,{stage:'P1',chapters:[chapter],count:10,full:false},state,()=>0.37);
  assert(!paper.error);assert(paper.questions.every(q=>!q.withdrawn));
}
console.log('PASS v15: C04/C09 each 23 active, 30 withdrawals, 12 additions, exact sources, Chinese solutions, source cap 3 and clean chapter placement');
