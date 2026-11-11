window.LS12_DB = (function () {
  const lessons = window.LS12_LESSONS || [];
  const allQuestions = [];
  const byId = Object.create(null);

  lessons.forEach((lesson) => {
    lesson.mc.forEach((q) => {
      const normalized = {
        ...q,
        type: 'mc',
        lessonId: lesson.id,
        lessonShort: lesson.shortTitle,
        lessonTitle: lesson.title,
        topic: lesson.topic,
        partLabel: 'Phần I • Trắc nghiệm'
      };
      allQuestions.push(normalized);
      byId[normalized.id] = normalized;
    });

    lesson.tf.forEach((q) => {
      const normalized = {
        ...q,
        type: 'tf',
        lessonId: lesson.id,
        lessonShort: lesson.shortTitle,
        lessonTitle: lesson.title,
        topic: lesson.topic,
        partLabel: 'Phần II • Đúng / Sai'
      };
      allQuestions.push(normalized);
      byId[normalized.id] = normalized;
    });
  });

  return {
    title: 'Đề cương Kiểm tra Giữa kì I — Lịch sử 12 (2025 - 2026)',
    lessons,
    allQuestions,
    byId,
    counts: {
      total: allQuestions.length,
      mc: allQuestions.filter((q) => q.type === 'mc').length,
      tf: allQuestions.filter((q) => q.type === 'tf').length
    }
  };
})();
