export function applyClassification(data,index){
 for(const q of data.questions){const entry=index.questions?.[q.id];if(!entry||entry.stage!==q.stage||!Array.isArray(entry.chapters)||!entry.chapters.length)throw Error('章节索引缺失：'+q.id);q.chapterLinks=[...new Set(entry.chapters)];}
 return data;
}
export const linkedChapters=q=>q.chapterLinks||q.chapters;
