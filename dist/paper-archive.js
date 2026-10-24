// Whole-paper archive stays separate from question-level practice.
export function archivePapers(archive, {stage, year='', month='', query=''}={}) {
  const term=query.trim().toLowerCase();
  return archive.papers.filter(p=>p.stage===stage&&(!year||p.year===+year)&&(!month||p.month===+month)&&(!term||`${p.id} ${p.title}`.toLowerCase().includes(term)))
    .sort((a,b)=>b.year-a.year||b.month-a.month||a.variant.localeCompare(b.variant));
}
export function validateArchive(archive) {
  if(!Array.isArray(archive?.papers)||!archive.papers.length)throw Error('整卷档案不可用');
  const ids=new Set();
  for(const p of archive.papers){
    if(ids.has(p.id)||!['P1','P2','P3'].includes(p.stage)||![1,6,10].includes(p.month)||!['','A','R'].includes(p.variant)||(p.year>2025||(p.year===2025&&p.month>6)))throw Error('整卷档案资料不一致');
    for(const key of ['pdf','markScheme'])if(!/^assets\/past-papers\/[a-z0-9-]+\.pdf$/.test(p[key]))throw Error('整卷文件地址无效');
    ids.add(p.id);
  }
  return archive;
}
