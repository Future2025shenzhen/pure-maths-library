import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {shuffle,chapterMatches,filterQuestions} from '../dist/core.js';
import {applyClassification,linkedChapters} from '../dist/classification.js';
import {archivePapers,validateArchive} from '../dist/paper-archive.js';
import {Stopwatch} from '../dist/stopwatch.js';
const root=new URL('../dist/',import.meta.url),read=p=>fs.readFileSync(new URL(p,root),'utf8');
const bank=applyClassification(JSON.parse(read('data/bank.json')),JSON.parse(read('data/classification.json')));
for(const stage of ['P1','P2','P3'])for(const c of bank.chapters[stage]){
 const filters={stage,chapters:[c.id],allowCrossChapter:false,type:'',status:'all',search:''};
 const strict=filterQuestions(bank,filters,{saved:[],done:[]});
 assert(strict.every(q=>(q.requiredChapters||q.chapterLinks||q.chapters).every(n=>n===c.id)));
 const cross=filterQuestions(bank,{...filters,allowCrossChapter:true},{saved:[],done:[]});assert(cross.length>=strict.length);
}
assert(!chapterMatches({chapters:[2,6]},[2],false));assert(chapterMatches({chapters:[2,6]},[2],true));
assert(chapterMatches({chapters:[2,6]},[2,6],false));assert(!chapterMatches({chapters:[2]},[],true));
const input=Array.from({length:40},(_,i)=>i),randomized=shuffle(input,()=>0.25);assert.notDeepEqual(randomized,input);assert.deepEqual([...randomized].sort((a,b)=>a-b),input);assert.deepEqual(input,Array.from({length:40},(_,i)=>i));
// Initialization regression: use the real current HTML and an authenticated account stub.
// Removed optional prose must never prevent PDF reader controls from binding.
const html=read('past.html'),nodes=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],{value:'',textContent:'',innerHTML:'',hidden:false,listeners:{},addEventListener(type,fn){this.listeners[type]=fn;},classList:{toggle(){},remove(){}},close(){},open:false}]));
let errors=[];
const fakeAccount={enabled:true,user:{nickname:'test'},ready:Promise.resolve(),getState:()=>({saved:[],done:[]}),addEventListener(){},activity:async()=>{}};
class ContinuousPdfViewerStub{constructor(){this.current=1;}open(){}go(){}setZoom(){}resize(){}destroyDocument(){}}
const context={console:{error:e=>errors.push(e)},account:fakeAccount,mountAccountLink:async()=>{},archivePapers,validateArchive,shuffle,chapterMatches,Stopwatch,ContinuousPdfViewer:ContinuousPdfViewerStub,applyClassification,linkedChapters,improveMath:x=>x,renderMath(){},notePlaceholder:()=>'',mountNotes(){},localStorage:{getItem:()=>null},sessionStorage:{getItem:()=>null,setItem(){}},innerWidth:1000,URLSearchParams,location:{search:''},document:{body:{classList:{toggle(){}}},querySelector:s=>s.startsWith('#')?nodes.get(s.slice(1))||null:null,addEventListener(){}},window:{addEventListener(){}},setInterval,clearInterval,setTimeout,clearTimeout,fetch:async url=>({ok:true,json:async()=>JSON.parse(read(url.split('?')[0]))})};
vm.createContext(context);let src=read('past.js').replace(/^import .*;\n/gm,'').replaceAll('import.meta.url',JSON.stringify(new URL('../dist/past.js',import.meta.url).href));src=src.replace(/init\(\);\s*$/,'globalThis.initialized=init();');vm.runInContext(src,context);await context.initialized;
assert.deepEqual(errors,[]);assert.equal(typeof nodes.get('reader-close').listeners.click,'function');assert.equal(typeof nodes.get('reader-full').listeners.click,'function');assert.equal(typeof nodes.get('timer-start').listeners.click,'function');assert(nodes.get('past-results').innerHTML.includes('question-card'));
assert(nodes.get('paper-directory').innerHTML.includes('2019'));assert(nodes.get('paper-directory').innerHTML.includes('2025'));assert(!nodes.get('paper-directory').innerHTML.includes('2026'));assert(!html.includes('reserve-directory'));
await nodes.get('past-year').listeners.change({target:{value:'2025'}});assert(nodes.get('paper-directory').innerHTML.includes('2025'));assert(nodes.get('past-results').innerHTML.includes('question-card'));assert(nodes.get('past-results').innerHTML.includes('查看官方答案'));
assert(html.includes('past-shuffle'));assert.equal(typeof nodes.get('past-shuffle').listeners.click,'function');assert(!read('app.js').includes('data-action="shuffle"'));
assert(!read('past.js').includes('account.requireUser()'));assert(!read('past.js').includes('data-copy-question'));assert(read('past.js').includes('guest-mode'));
console.log('PASS strict/cross chapter scope, unbiased shuffle integrity, authenticated past initialization and PDF/timer control binding');
