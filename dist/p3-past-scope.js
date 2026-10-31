// P3 scope is reviewed per complete question, including every subquestion.
export function applyP3PastScope(data,scope){
 if(scope?.stage!=='P3'||!scope.questions)throw Error('P3 针对练习章节索引不可用');
 for(const q of data.questions){
  if(q.stage!=='P3')continue;
  const entry=scope.questions[q.id],required=entry?.requiredChapters,requirements=entry?.requirements;
  if(!Array.isArray(required)||!required.length||new Set(required).size!==required.length||!required.every(n=>Number.isInteger(n)&&n>=1&&n<=8)||!Array.isArray(requirements)||requirements.length!==required.length||!required.every(n=>requirements.some(r=>r.chapter===n&&Array.isArray(r.skills)&&r.skills.length&&r.skills.every(s=>typeof s==='string'&&s.length))))throw Error('P3 题目章节范围缺失：'+q.id);
  q.requiredChapters=[...required];
  q.chapterLinks=[...required];
  q.scopeRequirements=requirements.map(r=>({chapter:r.chapter,skills:[...r.skills]}));
  q.topics=requirements.flatMap(r=>r.skills);
  q.titleZh=requirements.map(r=>r.skills[0]).join("、");
 }
 return data;
}
