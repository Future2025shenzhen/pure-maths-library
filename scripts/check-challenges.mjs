import fs from 'node:fs';import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url),bank=JSON.parse(fs.readFileSync(new URL('dist/data/bank.json',root))),base=JSON.parse(fs.readFileSync(new URL('editorial/v8/base-fingerprints.json',root))),extra=bank.questions.filter(q=>q.difficulty==='challenge');
const {createHash}=await import('node:crypto');
for(const q of bank.questions.filter(q=>q.difficulty!=='challenge'))assert.equal(createHash('sha256').update(JSON.stringify(q)).digest('hex'),base[q.id],q.id+' base content changed');
assert.equal(Object.keys(base).length,750);assert.equal(extra.length,20);
for(const q of extra){assert(!JSON.stringify(q).includes(String.fromCharCode(92).repeat(4)),'repeated TeX escapes '+q.id);assert(q.parts.length>=3&&q.parts.length<=4,q.id);assert(q.marks>=10&&q.marks<=15,q.id);assert(q.sourceReferences.length>0);assert(q.adaptationNote.length>=30,q.id);assert.equal(new Set(q.chapters).size,q.chapters.length);assert.equal(q.chapters[0],Number(q.id.slice(4,6)));assert(Number(q.id.slice(-2))>=31);}
const app=fs.readFileSync(new URL('dist/app.js',root),'utf8');assert(app.includes('[...linkedChapters(q)].sort((a,b)=>a-b).join("、")'),'all-original chapter header');
const sql=fs.readFileSync(new URL('backend/004-challenge-catalog.sql',root),'utf8');for(const q of extra)assert(sql.includes("'"+q.id+"'"));
console.log('PASS 750 base fingerprints unchanged;20 challenge IDs/structures/marks/source notes, full coverage header and catalog migration');
