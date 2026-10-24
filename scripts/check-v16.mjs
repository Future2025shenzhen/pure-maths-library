import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {validateBank,filterQuestions,cleanState,composePaper} from '../dist/core.js';
const read=p=>JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url)));
const bank=validateBank(read('dist/data/bank.json'));
const chapter=bank.questions.filter(q=>q.id.startsWith('P1-C07-'));
const live=chapter.filter(q=>!q.withdrawn);
assert.equal(chapter.length,38);assert.equal(live.length,21);
assert.equal(bank.questions.length,790);assert.equal(bank.questions.filter(q=>!q.withdrawn).length,738);
const additions=['P1-C07-R37','P1-C07-R38'];
assert(additions.every(id=>live.some(q=>q.id===id)));
assert(['15','27','35','36'].every(n=>chapter.find(q=>q.id===`P1-C07-R${n}`).withdrawn));
const families=new Map(),sources=new Map();
for(const q of bank.questions.filter(q=>!q.withdrawn))for(const s of q.sourceReferences||[])sources.set(s.questionId,(sources.get(s.questionId)||0)+1);
for(const q of live){
 assert.equal(q.editorialRevision,16);assert.deepEqual(q.chapters,[7]);
 assert.equal(q.sourceReferences.length,1);assert(q.questionTemplate&&q.examFamily);
 const s=q.sourceReferences[0];assert(sources.get(s.questionId)<=3,q.id+' source saturated across whole bank');
 for(const f of ['paperPdf','markSchemePdf'])assert(fs.existsSync(new URL('../dist/'+s[f].split('#')[0],import.meta.url)),q.id+' source file');
 assert(q.adaptationDimensions.filter(x=>['设问角度','求解目标','条件呈现','题目结构','参数化与分类讨论'].includes(x)).length>=2,q.id+' two angle/structure changes');
 assert(!q.adaptationNote.includes('真题固定套路'),q.id+' unsupported classic exemption');
 assert(q.errorNotes.length>=2&&q.errorNotes.length<=3);
 for(const p of q.parts)for(const value of [p.text,p.answer,...p.solutionSteps])assert(!/[\x00-\x1f]/.test(value),q.id+' accidental TeX escape');
 families.set(q.examFamily,[...(families.get(q.examFamily)||[]),q]);
}
assert.deepEqual([...families].sort().map(([f,qs])=>[f,qs.length]),[['G1',5],['G2',3],['G3',4],['G4',3],['G5',3],['G6',3]]);
for(const [f,qs] of families){assert(qs.length/21<=.25);assert(new Set(qs.map(q=>q.questionTemplate)).size>=3,f+' question-form coverage');}
assert(live.filter(q=>q.marks>=11||q.parts.length>=4).length<=Math.floor(21/4),'true long-chain cap, per observed P1 radians papers');
const state={saved:['P1-C07-R35','P1-C07-R37'],done:[]};
const filters={stage:'P1',chapters:[7],status:'all',search:'',type:'',allowCrossChapter:false};
assert.equal(filterQuestions(bank,filters,state).length,21);
assert(filterQuestions(bank,{...filters,savedOnly:true},state).some(q=>q.id==='P1-C07-R35'),'history still opens withdrawn ID');
assert.deepEqual(cleanState(state,new Set(bank.questions.map(q=>q.id))).saved,state.saved);
const paper=composePaper(bank,{stage:'P1',chapters:[7],count:10,full:false},state,()=>.37);
assert(!paper.error);assert(paper.questions.every(q=>!q.withdrawn&&q.chapters[0]===7));
// The newly legitimate one-part six-mark question must load; an empty question must still fail.
const single=live.find(q=>q.id==='P1-C07-R25');assert.equal(single.parts.length,1);
assert.doesNotThrow(()=>validateBank({chapters:bank.chapters,questions:[single]}));
assert.throws(()=>validateBank({chapters:bank.chapters,questions:[{...single,parts:[],marks:0}]}));
const marks=live.reduce((a,q)=>a+q.marks,0);assert.equal(marks,198);
console.log('PASS V16: all 21 questions, globally unsaturated sources, six-family quota, valid source links, history compatibility and single-part validation');
