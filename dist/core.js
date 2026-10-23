export const STORE_KEY='pure-practice-state-v1';
export function shuffle(items,random=Math.random){const a=[...items];for(let i=a.length-1;i>0;i--){const j=Math.floor(random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
export function validateBank(data){
 const ids=new Set();
 if(!data.chapters||!Array.isArray(data.questions))throw Error('题库格式无效');
 for(const q of data.questions){
  if(ids.has(q.id))throw Error(`题目ID重复：${q.id}`);ids.add(q.id);
  if(!data.chapters[q.stage]||!q.chapters.length||!q.chapters.every(id=>data.chapters[q.stage].some(c=>c.id===id)))throw Error(`章节无效：${q.id}`);
  if(q.parts.length<2||!q.stem)throw Error(`题目不完整：${q.id}`);
  function checkPart(p){if(!p.text)throw Error(`小问缺少设问：${q.id}`);if(p.subparts){if(p.subparts.length<2||p.subparts.reduce((s,a)=>s+a.marks,0)!==p.marks)throw Error(`分层小问分值无效：${q.id}`);p.subparts.forEach(checkPart);}else if(!p.answer||!p.explanation||!p.scheme?.length||p.scheme.reduce((s,a)=>s+a.marks,0)!==p.marks)throw Error(`小问或评分点无效：${q.id}`);}q.parts.forEach(checkPart);
  if(q.parts.reduce((s,p)=>s+p.marks,0)!==q.marks)throw Error(`总分无效：${q.id}`);
 }
 return data;
}
export function cleanState(data,ids){const result={version:1,saved:[],done:[]};for(const kind of ['saved','done'])if(Array.isArray(data?.[kind]))result[kind]=[...new Set(data[kind].filter(v=>typeof v==='string'&&ids.has(v)))];return result;}
// Strict mode requires every taught dependency to be inside the selected scope.
export function chapterMatches(q,selected,allowCrossChapter=false){
 const required=q.requiredChapters||q.chapterLinks||q.chapters||[];
 return selected.length>0&&required.length>0&&(allowCrossChapter?required.some(c=>selected.includes(c)):required.every(c=>selected.includes(c)));
}
export function filterQuestions(data,filters,state){
 const needle=filters.search.trim().toLowerCase();
 return data.questions.filter(q=>{
  if(q.stage!==filters.stage||q.withdrawn&&!filters.savedOnly)return false;
  if(!chapterMatches(q,filters.chapters,filters.allowCrossChapter??true))return false;
  if(filters.type&&q.type!==filters.type&&!q.topics.includes(filters.type))return false;
  if(filters.status==='done'&&!state.done.includes(q.id))return false;
  if(filters.status==='undone'&&state.done.includes(q.id))return false;
  if(filters.savedOnly&&!state.saved.includes(q.id))return false;
  if(needle){const cs=data.chapters[q.stage].filter(c=>(q.chapterLinks||q.chapters).includes(c.id));const hay=[q.id,q.type,q.difficulty==='challenge'?'提高题 challenge':'',q.stem,...q.parts.flatMap(p=>[p.text,...(p.subparts||[]).map(s=>s.text)]),...cs.flatMap(c=>[c.title,c.zh,c.scope]),...q.topics].join(' ').toLowerCase();if(!hay.includes(needle))return false;}
  return true;
 });
}
// Constrained selection: exact mark sum, no done/duplicate questions, bounded
// chapter/type repetition, and stage-specific question-count ranges seen in sources.
export function composePaper(data,{stage,chapters=[],count=5,full=false},state,random=Math.random){
 const all=data.chapters[stage].map(c=>c.id),selected=chapters.length?chapters:all;
 const pool=shuffle(data.questions.filter(q=>q.stage===stage&&!q.withdrawn&&['internal-review','internal-review-only'].includes(q.review)&&!state.done.includes(q.id)&&chapterMatches(q,selected,false)),random);
 if(full&&selected.length!==all.length)return {error:'完整模拟卷需要选择本阶段全部章节。局部范围请生成章节练习卷。'};
 if(pool.length<(full?9:count))return {error:`当前范围只有 ${pool.length} 道可用未做题，数量不足。请扩大章节范围，或按实际情况在题库取消已做标记。`};
 if(!full){
  const picked=[],groups=new Map(),types=new Map(),covered=new Set();
  while(picked.length<count){
   const choices=pool.filter(q=>!picked.includes(q));
   choices.sort((a,b)=>{const score=q=>q.chapters.filter(c=>!covered.has(c)).length*100-(groups.get(q.chapters[0])||0)*10-(types.get(q.type)||0)*3;return score(b)-score(a);});
   const q=choices[0];if(!q)break;picked.push(q);q.chapters.forEach(c=>covered.add(c));groups.set(q.chapters[0],(groups.get(q.chapters[0])||0)+1);types.set(q.type,(types.get(q.type)||0)+1);
  }
  return {questions:shuffle(picked,random),marks:picked.reduce((s,q)=>s+q.marks,0),full:false,coverage:[...covered]};
 }
 const limits=stage==='P3'?[9,10]:[9,11];
 let nodes=0;const maxNodes=180000;
 const dfs=(idx,picked,sum,groups,types,covered)=>{
  nodes++;if(nodes>maxNodes)return null;
  if(sum===75){if(picked.length>=limits[0]&&picked.length<=limits[1]&&selected.every(c=>covered.has(c)))return picked;return null;}
  if(sum>75||picked.length>=limits[1]||pool.length-idx<limits[0]-picked.length)return null;
  const remaining=limits[1]-picked.length;if(sum+remaining*Math.max(...pool.map(q=>q.marks))<75)return null;
  for(let i=idx;i<pool.length;i++){
   const q=pool[i],primary=q.chapters[0];
   if(sum+q.marks>75||(groups.get(primary)||0)>=2||(types.get(q.type)||0)>=3)continue;
   const ng=new Map(groups),nt=new Map(types),nc=new Set(covered);ng.set(primary,(ng.get(primary)||0)+1);nt.set(q.type,(nt.get(q.type)||0)+1);q.chapters.forEach(c=>nc.add(c));
   const unCovered=selected.filter(c=>!nc.has(c));
   const slots=limits[1]-picked.length-1;
   if(unCovered.length>slots*2||unCovered.some(c=>!pool.slice(i+1).some(a=>a.chapters.includes(c))))continue;
   const found=dfs(i+1,[...picked,q],sum+q.marks,ng,nt,nc);if(found)return found;
  }
  return null;
 };
 // Prioritize stronger integrated questions, while retaining random order within a mark band.
 pool.sort((a,b)=>b.marks-a.marks);
 // Cover each primary chapter once before filling the remaining mark total.
 // This avoids exhausting the search on many equivalent high-mark combinations.
 let sums=new Map([[0,[]]]);
 for(const chapter of selected){
  const next=new Map();
  for(const [sum,chosen] of sums)for(const q of pool.filter(q=>q.chapters[0]===chapter)){
   const total=sum+q.marks;if(total>75||next.has(total)||chosen.filter(a=>a.type===q.type).length>=3)continue;
   next.set(total,[...chosen,q]);
  }
  sums=next;
 }
 function fill(chosen,needed,slots,start=0){
  if(!slots)return needed===0?chosen:null;
  if(needed<=0)return null;
  for(let i=start;i<pool.length;i++){
   const q=pool[i];if(q.marks>needed||chosen.includes(q)||chosen.filter(a=>a.chapters[0]===q.chapters[0]).length>=2||chosen.filter(a=>a.type===q.type).length>=3)continue;
   const found=fill([...chosen,q],needed-q.marks,slots-1,i+1);if(found)return found;
  }
  return null;
 }
 let result=null;
 for(let count=limits[0];count<=limits[1]&&!result;count++)for(const [sum,chosen] of sums){
  result=fill(chosen,75-sum,count-chosen.length);if(result)break;
 }
 result ||= dfs(0,[],0,new Map(),new Map(),new Set());
 if(!result)return {error:'当前未做题无法同时满足75分、题数、全章节覆盖及重复限制。请改用章节练习卷；系统不会用已做题或重复题填补。'};
 return {questions:shuffle(result,random),marks:75,full:true,coverage:selected};
}
