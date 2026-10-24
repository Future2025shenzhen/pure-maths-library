import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root=new URL('../dist/',import.meta.url);
for(const file of ['igcse.html','igcse-reader.html','igcse-practice.html']){
 const html=fs.readFileSync(new URL(file,root),'utf8');
 assert(html.includes('<!doctype html>'),file);
 const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)];
 assert(scripts.length,file+' missing script');
 for(const [i,m] of scripts.entries())new vm.Script(m[1],{filename:file+'#'+i});
}
const original=JSON.parse(fs.readFileSync(new URL('data/igcse-original.json',root),'utf8'));
assert.equal(original.questions.filter(q=>q.subject==='physics').length,3);
assert.equal(original.questions.filter(q=>q.subject==='cs').length,3);
for(const q of original.questions){assert(q.stem&&q.answer&&q.marks>0&&q.id);}
const paper=JSON.parse(fs.readFileSync(new URL('data/igcse-paper-manifest.json',root),'utf8'));
assert(paper.records.length>0);
for(const x of paper.records){
 assert.equal(x.fileStatus,'not-checked');
 if(x.sourceStatus==='source-listing-confirmed')assert(x.sourceEvidenceUrl?.startsWith('https://'));
}
console.log('PASS IGCSE HTML JavaScript syntax, original questions and transparent source states');
