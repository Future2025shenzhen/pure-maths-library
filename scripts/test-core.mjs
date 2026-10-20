import assert from 'node:assert/strict';import fs from 'node:fs';
import {validateBank,composePaper,filterQuestions,cleanState} from '../dist/core.js';
const data=validateBank(JSON.parse(fs.readFileSync(new URL('../dist/data/bank.json',import.meta.url))));const state={saved:[],done:[]};const ids=new Set(data.questions.map(q=>q.id));
let seed=157;function random(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
for(const stage of ['P1','P2','P3']){
 const chapters=data.chapters[stage].map(c=>c.id),f={stage,chapters,type:'',status:'all',search:'',savedOnly:false};
 assert.equal(filterQuestions(data,f,state).length,data.questions.filter(q=>q.stage===stage).length);assert.equal(filterQuestions(data,{...f,chapters:[]},state).length,0);
 const doneId=data.questions.find(q=>q.stage===stage).id,st={done:[doneId],saved:[doneId]};assert(filterQuestions(data,f,st).some(q=>q.id===doneId));assert.equal(filterQuestions(data,{...f,savedOnly:true},st).length,1);
 const paper=composePaper(data,{stage,chapters,count:10,full:false},st,random);assert(!paper.error);assert.equal(paper.questions.length,10);assert(!paper.questions.some(q=>q.id===doneId));assert.equal(new Set(paper.questions.map(q=>q.id)).size,10);assert.equal(paper.marks,paper.questions.reduce((s,q)=>s+q.marks,0));
 const full=composePaper(data,{stage,chapters,full:true},st,random);assert(!full.error,full.error);assert.equal(full.marks,75);assert(full.questions.length>=9&&full.questions.length<=(stage==='P3'?10:11));assert(!full.questions.some(q=>q.id===doneId));assert.equal(new Set(full.questions.map(q=>q.id)).size,full.questions.length);assert(chapters.every(c=>full.questions.some(q=>q.chapters.includes(c))));for(const q of full.questions){assert.equal(q.stage,stage);assert(full.questions.filter(a=>a.chapters[0]===q.chapters[0]).length<=2);assert(full.questions.filter(a=>a.type===q.type).length<=3);}
 const one=composePaper(data,{stage,chapters:[1],count:5,full:false},state,random);assert(!one.error);assert(one.questions.every(q=>q.chapters.length===1&&q.chapters[0]===1));assert(composePaper(data,{stage,chapters,count:5,full:false},{done:data.questions.filter(q=>q.stage===stage).map(q=>q.id)},random).error);
}
const valid=[...ids][0];assert.deepEqual(cleanState({done:['invalid',1,valid,valid],saved:[valid]},ids),{version:1,done:[valid],saved:[valid]});
const q=data.questions.find(q=>q.stage==='P1'&&q.parts.some(p=>p.subparts));const topic=q.topics[0];assert(filterQuestions(data,{stage:'P1',chapters:data.chapters.P1.map(c=>c.id),type:topic,status:'all',search:'',savedOnly:false},state).some(v=>v.id===q.id));
console.log('PASS 770-question filtering, chapter practice, score sums, uniqueness, done exclusion, insufficient pools, topic filter and saved-state validation');
