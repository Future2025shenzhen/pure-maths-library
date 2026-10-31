export function applyCsPastScope(bank,scope,taxonomy){
 const valid=new Set(taxonomy.chapters.flatMap(c=>c.sections.map(s=>s.id)));
 for(const q of bank.questions){
  const required=scope?.questions?.[q.id]?.requiredSections;
  if(!Array.isArray(required)||!required.length||new Set(required).size!==required.length||!required.every(s=>valid.has(s)))throw Error('计算机科学题目章节范围缺失：'+q.id);
  q.requiredSections=[...required];q.sections=[...required];q.chapters=[...new Set(required.map(s=>Number(s.split('.')[0])))];q.topics=[...required];
 }
 return bank;
}
export function csScopeMatches(question,selected,allowCross=false){
 const required=question.requiredSections;
 if(!selected.length||!Array.isArray(required)||!required.length)return false;
 return allowCross?required.some(s=>selected.includes(s)):required.every(s=>selected.includes(s));
}
