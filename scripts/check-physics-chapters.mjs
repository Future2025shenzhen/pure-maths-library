import fs from 'node:fs';
import assert from 'node:assert/strict';

const data=JSON.parse(fs.readFileSync(new URL('../dist/data/physics-chapters.json',import.meta.url),'utf8'));
assert.equal(data.subject,'Cambridge IGCSE Physics 0625');
assert.deepEqual(data.paperGroups.map(group=>group.papers),[[1,2,3,4],[5,6]]);
assert.equal(data.chapters.length,6);
assert.equal(data.chapters.flatMap(chapter=>chapter.sections).length,24);
assert.deepEqual(data.chapters.map(chapter=>chapter.sections.length),[8,3,4,5,2,2]);

const ids=data.chapters.flatMap(chapter=>chapter.sections.map(section=>section.id));
assert.equal(new Set(ids).size,ids.length);
for(const chapter of data.chapters){
  assert(chapter.title&&chapter.zh&&chapter.page>0);
  for(const section of chapter.sections){
    assert(section.id.startsWith(chapter.id+'.'));
    assert(section.title&&section.zh&&section.page>=chapter.page);
  }
}

console.log('PASS Physics taxonomy: 6 chapters, 24 sections, combined MCQ/theory and separate practical banks');
