import {applyP3PastScope} from './p3-past-scope.js?v=1';
// Chapter requirements describe every part of the complete question.
export function applyPastScope(data,scopes){
 applyP3PastScope(data,scopes.P3);
 for(const q of data.questions){
  if(q.stage==='P3')continue;
  const entry=scopes[q.stage]?.questions?.[q.id],required=entry?.requiredChapters,requirements=entry?.requirements,max=q.stage==='P1'?9:8;
  if(!Array.isArray(required)||!required.length||new Set(required).size!==required.length||!required.every(n=>Number.isInteger(n)&&n>=1&&n<=max)||!Array.isArray(requirements)||requirements.length!==required.length||!required.every(n=>requirements.some(r=>r.chapter===n&&Array.isArray(r.skills)&&r.skills.length&&r.skills.every(s=>typeof s==='string'&&s.length))))throw Error('真题章节范围缺失：'+q.id);
  q.requiredChapters=[...required];q.chapterLinks=[...required];q.scopeRequirements=requirements.map(r=>({chapter:r.chapter,skills:[...r.skills]}));q.topics=requirements.flatMap(r=>r.skills);q.titleZh=requirements.map(r=>r.skills[0]).join('、');
 }
 return data;
}
