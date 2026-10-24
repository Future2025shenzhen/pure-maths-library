import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const root=new URL('../dist/',import.meta.url);
for(const file of ['igcse.html','igcse-reader.html','igcse-practice.html','igcse-audit.html']){
 const html=fs.readFileSync(new URL(file,root),'utf8');
 assert(html.includes('<!doctype html>'),file);
 const scripts=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)];
 assert(scripts.length,file+' missing script');
 for(const [i,m] of scripts.entries()){
  const check=spawnSync(process.execPath,['--check','--input-type=module'],{input:m[1],encoding:'utf8'});
  assert.equal(check.status,0,file+' script '+i+': '+check.stderr);
 }
}
const original=JSON.parse(fs.readFileSync(new URL('data/igcse-original.json',root),'utf8'));
assert.equal(original.questions.filter(q=>q.subject==='physics').length,3);
assert.equal(original.questions.filter(q=>q.subject==='cs').length,3);
for(const q of original.questions){assert(q.stem&&q.answer&&q.marks>0&&q.id);}
const paper=JSON.parse(fs.readFileSync(new URL('data/igcse-paper-manifest.json',root),'utf8'));
assert(paper.records.length>0);
const seen=new Set();
for(const x of paper.records){
 assert(!seen.has(x.id), 'Duplicate paper variant '+x.id);seen.add(x.id);
 assert([2019,2020,2021,2022,2023,2024].includes(x.year));
 assert(['physics','cs'].includes(x.subject));
 for(const kind of ['qp','ms','ci','pm']){
  if(!x[kind+'Url'])continue;
  const uri=new URL(x[kind+'Url']);
  assert.equal(uri.protocol,'https:');
  assert.equal(decodeURIComponent(uri.pathname.split('/').pop()).toLowerCase(),(x.id.slice(0,4)+'_'+x.id.slice(5,8)+'_'+kind+'_'+x.component+'.pdf').toLowerCase(),x.id+' '+kind);
 }

 assert.equal(x.fileStatus,'not-checked');
 if(x.sourceStatus==='source-listing-confirmed')assert(x.sourceEvidenceUrl?.startsWith('https://'));
}
if(paper.pairCoverage){
 for(const subject of ['physics','cs']){
  const rows=paper.records.filter(r=>r.subject===subject), c=paper.pairCoverage[subject];
  assert.equal(c.paired,rows.filter(r=>r.qpUrl&&r.msUrl).length);
  assert.equal(c.qpOnly,rows.filter(r=>r.qpUrl&&!r.msUrl).length);
  assert.equal(c.msOnly,rows.filter(r=>r.msUrl&&!r.qpUrl).length);
 }
}
console.log('PASS IGCSE HTML JavaScript syntax, original questions and transparent source states');

// The live browser uses only downloaded, byte-verified same-origin resources.
const online=JSON.parse(fs.readFileSync(new URL('data/igcse-online-files.json',root),'utf8'));
assert.equal(online.files.length,793);
const onlineNames=new Set();
for(const f of online.files){
 assert(!onlineNames.has(f.filename));onlineNames.add(f.filename);
 assert(['physics','cs'].includes(f.subject));assert(f.year>=2019&&f.year<=2024);
 assert.equal(f.path,'assets/igcse/'+f.filename);
 assert(/^[a-f0-9]{64}$/.test(f.sha256));assert(f.bytes>0);
 assert(f.url.startsWith('https://raw.githubusercontent.com/'));
 assert.equal(f.filename.slice(0,4),f.subject==='physics'?'0625':'0478');
}
for(const [subject,count] of [['physics',251],['cs',84]]){
 assert.equal(online.files.filter(f=>f.subject===subject&&f.type==='qp').length,count);
 assert.equal(online.files.filter(f=>f.subject===subject&&f.type==='ms').length,count);
}
for(const f of online.files.filter(f=>f.type==='qp'))assert(onlineNames.has(f.filename.replace('_qp_','_ms_')));
for(const file of ['igcse-online.js','igcse-reader.js']){
 const check=spawnSync(process.execPath,['--check',new URL(file,root).pathname],{encoding:'utf8'});assert.equal(check.status,0,check.stderr);
}
assert(!fs.readFileSync(new URL('igcse-online.js',root),'utf8').includes('papacambridge.com'));
assert(fs.readFileSync(new URL('igcse-reader.js',root),'utf8').includes('pdfjs.getDocument'));
console.log('PASS: 793 verified same-origin IGCSE files, 335 QP/MS pairs and PDF.js reader');
