import fs from 'node:fs';import vm from 'node:vm';import assert from 'node:assert/strict';
import {improveMath} from '../dist/math-format.js';
import {applyClassification} from '../dist/classification.js';
const root=new URL('../dist/',import.meta.url).pathname,box={};vm.runInNewContext(fs.readFileSync(root+'assets/katex/katex.min.js','utf8'),box);
const index=JSON.parse(fs.readFileSync(root+'data/classification.json'));let count=0,changed=0;
function scan(v){if(typeof v==='string'){const t=improveMath(v);if(t!==v)changed++;for(const m of t.matchAll(/\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g)){box.katex.renderToString(m[1]??m[2],{throwOnError:true,strict:'ignore'});count++;}}else if(Array.isArray(v))v.forEach(scan);else if(v&&typeof v==='object')Object.values(v).forEach(scan);}
for(const name of ['bank','past-bank']){const d=applyClassification(JSON.parse(fs.readFileSync(root+'data/'+name+'.json')),index);scan(d.questions);for(const q of d.questions)assert(q.chapters.every(c=>q.chapterLinks.includes(c)));}
assert.equal(improveMath('$\\sqrt3/2$'),'$\\sqrt3/2$');
assert.equal(improveMath('$3/2$'),'$\\displaystyle \\frac{3}{2}$');
assert(improveMath('$\\sum_{r=1}^{N}r$').includes('\\displaystyle'));
assert(improveMath('$\\tfrac32$').includes('\\displaystyle \\frac32'));
assert.equal(improveMath('$3^2/2^3$'),'$3^2/2^3$');
assert.equal(improveMath('$x^a/b$'),'$x^a/b$');
assert.equal(Object.keys(index.questions).length,1111);
console.log(`PASS ${count} formulas render; ${changed} text fields improved; 1111 classification entries`);
