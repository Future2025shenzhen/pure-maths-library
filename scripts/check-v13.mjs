import fs from 'node:fs';
import assert from 'node:assert/strict';
import {filterQuestions,composePaper} from '../dist/core.js';
const root=new URL('../',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const bank=read('dist/data/bank.json'),past=read('dist/data/past-bank.json'),layout=read('dist/data/past-layout.json').questions,withdrawals=read('editorial/v13/withdrawals.json').records;
assert.equal(bank.questions.filter(q=>!q.withdrawn).length,753);
assert.equal(withdrawals.length,6);
const state={saved:withdrawals.map(r=>r.id),done:[]},filters={stage:'P1',chapters:bank.chapters.P1.map(c=>c.id),status:'all',search:'',type:''};
const daily=filterQuestions(bank,filters,state),saved=filterQuestions(bank,{...filters,savedOnly:true},state);
for(const row of withdrawals){assert(!daily.some(q=>q.id===row.id));assert(saved.some(q=>q.id===row.id));assert(bank.questions.some(q=>q.id===row.retained&&!q.withdrawn));}
const composed=composePaper(bank,{stage:'P1',chapters:filters.chapters,count:6,full:false},state);
assert(!composed.error);assert(composed.questions.every(q=>!q.withdrawn));
assert.deepEqual(Object.keys(layout).sort(),past.questions.map(q=>q.id).sort());
for(const q of past.questions){
 const slices=layout[q.id];assert(slices.length);
 for(const v of slices){assert(q.sourcePages.includes(v.page));assert(fs.existsSync(new URL('dist/'+v.image,root)));assert.equal(v.crop.length,4);const [x,y,w,h]=v.crop;assert([x,y,w,h].every(Number.isFinite));assert(x>=0&&y>=0&&w>0&&h>0&&x+w<=1.00001&&y+h<=1.00001);}
 for(const v of q.pages)assert(slices.some(s=>s.page===v.page),q.id+' lost a previously shown content page');
}
assert(layout['P1-2021-06-Q09'].some(v=>v.page===31),'continuation sketch diagram');
assert(layout['P3-2022-10-Q07'].some(v=>v.page===21),'continuation sketch diagram');
const first=layout['P1-2020-01-Q01'];assert(first.reduce((n,s)=>n+s.crop[3],0)<.2,'short question must not include answer stationery');
console.log('PASS v13: 6 reviewed withdrawals excluded from practice/new papers, saved IDs preserved; 323 compact question layouts, both continuation diagrams, valid source crops and no lost existing content pages');
