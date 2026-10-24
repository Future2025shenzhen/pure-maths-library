import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {archivePapers,validateArchive} from '../dist/paper-archive.js';
const root=new URL('../',import.meta.url),read=p=>JSON.parse(fs.readFileSync(new URL(p,root)));
const a=validateArchive(read('dist/data/paper-archive.json')),past=read('dist/data/past-bank.json');
assert.equal(a.papers.length,58);
assert.deepEqual(Object.fromEntries(['P1','P2','P3'].map(s=>[s,a.papers.filter(p=>p.stage===s).length])),{P1:21,P2:20,P3:17});
for(const p of a.papers){
  assert((p.year<2025)||(p.year===2025&&p.month<=6));
  for(const [key,hash] of [['pdf','sha256'],['markScheme','markSchemeSha256']]){
    const b=fs.readFileSync(new URL('dist/'+p[key],root));
    assert.equal(b.subarray(0,5).toString(),'%PDF-');
    assert.equal(createHash('sha256').update(b).digest('hex'),p[hash],p.id+' '+key);
  }
  assert.equal(p.questionPracticeAvailable,past.papers.some(old=>old.id===p.id));
}
assert.equal(archivePapers(a,{stage:'P1',year:'2025',month:'6'}).length,2);
assert.equal(archivePapers(a,{stage:'P1',year:'2026'}).length,0);
assert.equal(archivePapers(a,{stage:'P3',year:'2019'}).length,0);
assert.equal(past.questions.length,572);
assert(past.questions.every(q=>q.year<2025||(q.year===2025&&q.month<=6)));
assert.equal(past.questions.filter(q=>q.officialMarkScheme).length,572);
assert.equal(past.questions.filter(q=>q.v17Added).length,249);
console.log('PASS: 58 complete paper pairs through June 2025, 116 local PDFs and 572 question-by-question practice records.');
