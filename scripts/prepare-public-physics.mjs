import { readFileSync, writeFileSync, rmSync } from 'node:fs';
import { isPublishedExamFile, limitPhysicsBank, physicsPapers } from '../dist/physics-scope.js';

const dist = new URL('../dist/', import.meta.url);
const manifestPath = new URL('data/igcse-online-files.json', dist);
const bankPath = new URL('data/physics-question-bank.json', dist);
const manifest = JSON.parse(readFileSync(manifestPath));
const kept = manifest.files.filter(isPublishedExamFile);
for (const file of manifest.files.filter(file => !isPublishedExamFile(file))) {
  if (!/^assets\/igcse\/0625_[a-z0-9_]+\.pdf$/.test(file.path)) {
    throw new Error(`Unexpected Physics asset path: ${file.path}`);
  }
  rmSync(new URL(file.path, dist), { force: true });
}
manifest.files = kept;
manifest.knownGaps = manifest.knownGaps.filter(name => {
  const number = /^0625_[a-z0-9]+_[a-z]+_([1-6])\d\.pdf$/.exec(name)?.[1];
  return !number || physicsPapers.includes(Number(number));
});
const bank = limitPhysicsBank(JSON.parse(readFileSync(bankPath)));
writeFileSync(manifestPath, JSON.stringify(manifest));
writeFileSync(bankPath, JSON.stringify(bank));
console.log(`Published Physics papers 2, 4 and 6: ${bank.papers.length} papers, ${bank.questions.length} questions.`);
