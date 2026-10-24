import fs from 'node:fs';
import assert from 'node:assert/strict';
import {filterQuestions,composePaper} from '../dist/core.js';

const root=new URL('../',import.meta.url);
const read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const bank=read('dist/data/bank.json');
const past=read('dist/data/past-bank.json');
const layout=read('dist/data/past-layout.json').questions;
const chapter=bank.questions.filter(q=>q.stage==='P1'&&q.id.startsWith('P1-C07-'));
const active=chapter.filter(q=>!q.withdrawn);
const deleted=new Set(['P1-C07-R04','P1-C07-R05','P1-C07-R06','P1-C07-R09','P1-C07-R12','P1-C07-R14','P1-C07-R16','P1-C07-R17','P1-C07-R18','P1-C07-R19','P1-C07-R22','P1-C07-R26','P1-C07-R29','P1-C07-R15','P1-C07-R27','P1-C07-R35','P1-C07-R36']);

assert.equal(bank.questions.length,790);
assert.equal(bank.questions.filter(q=>!q.withdrawn).length,738);
assert.equal(chapter.length,38);
assert.equal(active.length,21);
assert.deepEqual(new Set(chapter.filter(q=>q.withdrawn).map(q=>q.id)),deleted);
for(const id of ['P1-C07-R31','P1-C07-R32','P1-C07-R33','P1-C07-R34','P1-C07-R37','P1-C07-R38'])assert(active.some(q=>q.id===id),id);

const sources=new Map(),partCounts=new Map();
for(const q of active){
  assert.equal(q.editorialRevision,16,q.id);
  assert(q.sourceReferences?.length,q.id+' source');
  assert(q.sourceSummary?.length>=10,q.id+' source summary');
  assert(q.adaptationDimensions?.length>=3,q.id+' dimensions');
  assert(q.examEssence?.length>=10,q.id+' essence');
  assert(q.difficultyPosition?.startsWith('略难于'),q.id+' difficulty');
  assert(q.errorNotes?.length>=2,q.id+' errors');
  assert(q.designNote?.length>=10,q.id+' design');
  assert(!JSON.stringify(q).includes('采用解析所述方法'),q.id+' generic explanation');
  assert.equal(q.parts.reduce((n,p)=>n+p.marks,0),q.marks,q.id+' marks');
  for(const p of q.parts){
    assert(p.approach&&p.solutionSteps?.length>=2,q.id+' steps');
    assert(/[\u4e00-\u9fff]/.test(p.approach)&&/[\u4e00-\u9fff]/.test(p.solutionSteps.join('')),q.id+' Chinese solution');
    assert.equal(p.scheme.reduce((n,r)=>n+r.marks,0),p.marks,q.id+' scheme');
    assert(p.scheme.every(r=>/^[MAB]\d+$/.test(r.code)&&r.marks>0),q.id+' codes');
  }
  const source=q.sourceReferences[0].questionId;
  sources.set(source,(sources.get(source)||0)+1);
  partCounts.set(q.parts.length,(partCounts.get(q.parts.length)||0)+1);
}
assert(Math.max(...sources.values())<=3,'source reuse cap');
assert.deepEqual(Object.fromEntries([...partCounts].sort()),{'1':1,'2':12,'3':8});

const state={saved:[...deleted],done:[]};
const filters={stage:'P1',chapters:bank.chapters.P1.map(c=>c.id),status:'all',search:'',type:''};
assert(!filterQuestions(bank,filters,state).some(q=>deleted.has(q.id)));
assert([...deleted].every(id=>filterQuestions(bank,{...filters,savedOnly:true},state).some(q=>q.id===id)));
const composed=composePaper(bank,{stage:'P1',chapters:filters.chapters,count:6,full:false},state);
assert(!composed.error);assert(composed.questions.every(q=>!q.withdrawn));

assert.deepEqual(Object.keys(layout).sort(),past.questions.map(q=>q.id).sort());
for(const q of past.questions)for(const v of layout[q.id]){
  assert(q.sourcePages.includes(v.page));assert(fs.existsSync(new URL('dist/'+v.image,root)));
  const [x,y,w,h]=v.crop;assert([x,y,w,h].every(Number.isFinite));assert(x>=0&&y>=0&&w>0&&h>0&&x+w<=1.00001&&y+h<=1.00001);
}
console.log('PASS Radians: 21 active, 17 withdrawals, 8 historical additions, source cap 3, detailed solutions and valid past-paper layouts');
