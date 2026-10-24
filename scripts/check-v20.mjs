import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
const preserved=JSON.parse(fs.readFileSync('editorial/v20/question-source-fingerprints.json'));
const sourceHash=q=>createHash('sha256').update(JSON.stringify(Object.fromEntries(Object.entries(q).filter(([k])=>!preserved.answerFields.includes(k))))).digest('hex');
const bank=JSON.parse(fs.readFileSync('dist/data/past-bank.json'));
const audit=JSON.parse(fs.readFileSync('editorial/v20/official-answer-audit.json'));
assert.equal(audit.length,572);
const byId=new Map(audit.map(q=>[q.id,q]));
for(const q of bank.questions){
 assert.equal(sourceHash(q),preserved.questions[q.id],q.id+' question and source data unchanged');
 assert.equal(q.officialSchemeRevision,20,q.id);
 assert.equal(q.officialMarkScheme,true,q.id);
 assert.deepEqual(q.solutionSections,[],q.id+' only official answers');
 assert(!q.quickCheckZh,q.id+' no authored answer summary');
 const paper=bank.papers.find(p=>p.id===q.paper),record=byId.get(q.id);
 assert.equal(record.sourcePdf,paper.markScheme,q.id+' exact matching paper');
 assert.equal(record.tables.length,q.markSchemePages.length,q.id);
 for(const [i,v] of q.markSchemePages.entries()){
  assert.equal(v.sourcePdf,paper.markScheme,q.id);
  assert.equal(v.sourcePage,record.tables[i].sourcePage,q.id);
  assert(fs.existsSync('dist/'+v.pdf),q.id+' extracted official PDF');
  assert.deepEqual(v.crop,[0,0,1,1]);
  assert(!v.highlights,q.id+' no annotations');
  assert(record.tables[i].marks.some(m=>/[MAB][123]/.test(m)),q.id+' official marks retained');
 }
}
const js=fs.readFileSync('dist/past.js','utf8');
assert(!js.includes('strokeRect'),'no drawn answer boxes');
assert(js.includes('v.sourcePage||v.page'),'original PDF links keep original page numbers');
console.log('PASS v20: all 572 answers use unannotated official Scheme/Marks extracts with original source references.');
