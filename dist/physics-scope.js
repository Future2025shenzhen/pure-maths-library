export const physicsPapers = [2, 4, 6];
const groups = new Set(physicsPapers.map(number => `paper${number}`));

export function limitPhysicsBank(bank) {
  return {
    ...bank,
    papers: bank.papers.filter(paper => groups.has(paper.group)),
    questions: bank.questions.filter(question => groups.has(question.group))
  };
}

export function isPublishedExamFile(file) {
  return file.subject !== 'physics' || !file.paper || physicsPapers.includes(Number(file.paper[0]));
}
