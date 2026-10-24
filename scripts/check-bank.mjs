import fs from 'node:fs';import vm from 'node:vm';import {validateBank} from '../dist/core.js';
const data=validateBank(JSON.parse(fs.readFileSync(new URL('../dist/data/bank.json',import.meta.url))));const box={};vm.runInNewContext(fs.readFileSync(new URL('../dist/assets/katex/katex.min.js',import.meta.url),'utf8'),box);let formulae=0;
function scan(t){for(const m of t.matchAll(/\$([^$]+)\$/g)){box.katex.renderToString(m[1],{throwOnError:true,strict:'ignore'});formulae++;}}
function part(p){scan(p.text);if(p.subparts)p.subparts.forEach(part);else{scan(p.answer);scan(p.explanation);p.scheme.forEach(r=>scan(r.text));}}
for(const q of data.questions){scan(q.stem);q.parts.forEach(part);}for(const [s,cs] of Object.entries(data.chapters))for(const c of cs){const n=data.questions.filter(q=>q.stage===s&&q.chapters[0]===c.id).length;const expected=s==='P1'&&[4,7,9].includes(c.id)?36:s==='P3'&&c.id===6?40:['P2','P3'].includes(s)&&c.id===7?35:30;if(n!==expected)throw Error(s+' chapter '+c.id+' count '+n);}
if(data.questions.length!==788)throw Error('Total count');console.log(`PASS 788 historical questions; V14/V15 add 18 reviewed items; nested marks, IDs and ${formulae} formulas`);
