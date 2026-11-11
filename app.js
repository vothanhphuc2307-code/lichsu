/* ==========================================================================
   Sử 12 • Thi Thử & Chấm Đúng Sai — Application Logic
   ========================================================================== */
(function () {
  'use strict';

  const DB = window.LS12_DB;
  const MINDMAPS = window.LS12_MINDMAPS || [];
  const STORAGE_KEYS = {
    theme: 'ls12_theme',
    bookmarks: 'ls12_bookmarks',
    wrongIds: 'ls12_wrong_ids',
    history: 'ls12_history'
  };

  const LETTERS = ['A', 'B', 'C', 'D'];
  const PAGE_SIZE_QUIZ = 10;
  const PAGE_SIZE_BANK = 15;

  // Persistent User State
  const store = {
    theme: loadJSON(STORAGE_KEYS.theme, 'light'),
    bookmarks: new Set(loadJSON(STORAGE_KEYS.bookmarks, [])),
    wrongIds: new Set(loadJSON(STORAGE_KEYS.wrongIds, [])),
    history: loadJSON(STORAGE_KEYS.history, [])
  };

  // App Runtime State
  const state = {
    view: 'home', // 'home' | 'practice-setup' | 'mindmap' | 'workspace' | 'results' | 'bank'
    builder: {
      mode: 'exam', // 'exam' | 'practice'
      selectedLessons: DB.lessons.map((l) => l.id),
      typeFilter: 'all', // 'all' | 'mc' | 'tf'
      shuffleQuestions: false,
      shuffleOptions: false,
      durationMin: 45,
      autoCheckPractice: true
    },
    mindmap: {
      lessonId: (MINDMAPS[0] && MINDMAPS[0].id) || 'bai-1',
      layout: typeof window !== 'undefined' && window.innerWidth && window.innerWidth < 768 ? 'vertical' : 'tree',
      query: '',
      collapsed: {}
    },
    bank: {
      lessonId: 'all',
      type: 'all',
      query: '',
      showAnswers: true,
      page: 1
    },
    session: null,
    timerId: null
  };

  // DOM References
  const dom = {
    mainContent: document.getElementById('mainContent'),
    mainNav: document.getElementById('mainNav'),
    brandBtn: document.getElementById('brandBtn'),
    themeToggle: document.getElementById('themeToggle'),
    modalBackdrop: document.getElementById('modalBackdrop'),
    modalTitle: document.getElementById('modalTitle'),
    modalBody: document.getElementById('modalBody'),
    modalFooter: document.getElementById('modalFooter'),
    modalCloseBtn: document.getElementById('modalCloseBtn'),
    sheetBackdrop: document.getElementById('sheetBackdrop'),
    sheetSub: document.getElementById('sheetSub'),
    sheetBody: document.getElementById('sheetBody'),
    sheetCloseBtn: document.getElementById('sheetCloseBtn'),
    toastContainer: document.getElementById('toastContainer')
  };

  /* ------------------------------------------------------------------------
     Utilities
     ------------------------------------------------------------------------ */
  function loadJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function saveJSON(key, val) {
    try {
      localStorage.setItem(key, JSON.stringify(val));
    } catch {
      // Ignore quota errors
    }
  }

  function escapeHTML(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function stripVN(str) {
    return String(str)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd');
  }

  function shuffleArray(arr) {
    const copy = arr.slice();
    for (let i = copy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function formatTime(sec) {
    const s = Math.max(0, Math.floor(sec));
    const hrs = Math.floor(s / 3600);
    const mins = Math.floor((s % 3600) / 60);
    const rem = s % 60;
    const pad = (n) => String(n).padStart(2, '0');
    return hrs > 0 ? `${hrs}:${pad(mins)}:${pad(rem)}` : `${pad(mins)}:${pad(rem)}`;
  }

  function showToast(msg) {
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    dom.toastContainer.appendChild(el);
    setTimeout(() => {
      el.remove();
    }, 2400);
  }

  function applyTheme(theme) {
    store.theme = theme === 'dark' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', store.theme);
    saveJSON(STORAGE_KEYS.theme, store.theme);
  }

  function tfScoreFromCorrectCount(count) {
    if (count === 1) return 0.1;
    if (count === 2) return 0.25;
    if (count === 3) return 0.5;
    if (count === 4) return 1.0;
    return 0;
  }

  /* ------------------------------------------------------------------------
     Modal & Bottom Sheet
     ------------------------------------------------------------------------ */
  function openModal({ title, bodyHTML, buttons }) {
    dom.modalTitle.textContent = title;
    dom.modalBody.innerHTML = bodyHTML;
    dom.modalFooter.innerHTML = '';
    buttons.forEach((b) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = b.className || 'btn btn-outline';
      btn.textContent = b.label;
      btn.addEventListener('click', () => {
        closeModal();
        if (b.onClick) b.onClick();
      });
      dom.modalFooter.appendChild(btn);
    });
    dom.modalBackdrop.hidden = false;
  }

  function closeModal() {
    dom.modalBackdrop.hidden = true;
  }

  function openSheet() {
    if (!state.session) return;
    renderPaletteInto(dom.sheetBody, true);
    const done = countAnswered(state.session);
    dom.sheetSub.textContent = `Đã làm ${done}/${state.session.questions.length} câu`;
    dom.sheetBackdrop.hidden = false;
  }

  function closeSheet() {
    dom.sheetBackdrop.hidden = true;
  }

  /* ------------------------------------------------------------------------
     Session & Grading Helpers
     ------------------------------------------------------------------------ */
  function stopTimer() {
    if (state.timerId) {
      clearInterval(state.timerId);
      state.timerId = null;
    }
  }

  function startTimer() {
    stopTimer();
    if (!state.session || state.session.mode !== 'exam' || state.session.submitted) return;
    state.timerId = setInterval(() => {
      if (!state.session || state.session.submitted) {
        stopTimer();
        return;
      }
      state.session.remainingSec -= 1;
      state.session.elapsedSec += 1;
      const timerEl = document.getElementById('timerDisplay');
      if (timerEl) {
        timerEl.textContent = formatTime(state.session.remainingSec);
        timerEl.classList.remove('warning', 'danger');
        if (state.session.remainingSec <= 60) {
          timerEl.classList.add('danger');
        } else if (state.session.remainingSec <= 300) {
          timerEl.classList.add('warning');
        }
      }
      if (state.session.remainingSec <= 0) {
        stopTimer();
        showToast('Hết giờ làm bài! Hệ thống tự động nộp bài.');
        finalizeSubmission();
      }
    }, 1000);
  }

  function buildQuestionsFromFilter({ lessonIds, typeFilter, shuffleQuestions }) {
    let list = DB.allQuestions.filter((q) => {
      if (lessonIds && !lessonIds.includes(q.lessonId)) return false;
      if (typeFilter === 'mc' && q.type !== 'mc') return false;
      if (typeFilter === 'tf' && q.type !== 'tf') return false;
      return true;
    });
    if (shuffleQuestions) {
      list = shuffleArray(list);
    }
    return list;
  }

  function buildThpt2025Exam() {
    const mcPool = shuffleArray(DB.allQuestions.filter((q) => q.type === 'mc')).slice(0, 24);
    const tfPool = shuffleArray(DB.allQuestions.filter((q) => q.type === 'tf')).slice(0, 4);
    // Order by lesson for cleanliness inside each section
    const lessonOrder = new Map(DB.lessons.map((l, idx) => [l.id, idx]));
    mcPool.sort((a, b) => (lessonOrder.get(a.lessonId) - lessonOrder.get(b.lessonId)) || (a.num - b.num));
    tfPool.sort((a, b) => (lessonOrder.get(a.lessonId) - lessonOrder.get(b.lessonId)) || (a.num - b.num));
    return [...mcPool, ...tfPool];
  }

  function createSession({
    title,
    mode,
    questions,
    durationMin = 45,
    shuffleOptions = false,
    autoCheckPractice = true,
    isThptPreset = false
  }) {
    if (!questions.length) {
      showToast('Không có câu hỏi nào phù hợp với lựa chọn!');
      return;
    }

    const mcOrder = {};
    questions.forEach((q) => {
      if (q.type === 'mc') {
        mcOrder[q.id] = shuffleOptions ? shuffleArray([0, 1, 2, 3]) : [0, 1, 2, 3];
      }
    });

    stopTimer();
    state.session = {
      id: 'sess-' + Date.now(),
      title,
      mode, // 'exam' | 'practice'
      isThptPreset,
      questions,
      mcOrder,
      answers: {}, // mc: number (original option idx), tf: { a: bool, b: bool, ... }
      checked: {}, // practice mode per-question graded state
      submitted: false,
      autoCheckPractice,
      viewLayout: questions.length <= 1 ? 'focus' : 'paged', // 'paged' | 'focus'
      page: 1,
      focusIndex: 0,
      durationSec: durationMin * 60,
      remainingSec: durationMin * 60,
      elapsedSec: 0,
      startedAt: Date.now(),
      resultFilter: 'all', // 'all' | 'wrong' | 'correct' | 'bookmarked'
      resultPage: 1,
      resultShowAll: false
    };

    state.view = 'workspace';
    updateNavActive();
    render();
    window.scrollTo({ top: 0, behavior: 'instant' });
    if (mode === 'exam') {
      startTimer();
    }
  }

  function getQuestionState(session, q) {
    const ans = session.answers[q.id];
    const isGraded = session.submitted || Boolean(session.checked[q.id]);

    if (q.type === 'mc') {
      const hasAns = typeof ans === 'number';
      if (!isGraded) {
        return {
          status: hasAns ? 'answered' : 'unanswered',
          answeredItems: hasAns ? 1 : 0,
          totalItems: 1
        };
      }
      const isCorrect = hasAns && ans === q.answer;
      return {
        status: isCorrect ? 'correct' : 'wrong',
        isCorrect,
        earnedPts: isCorrect ? 0.25 : 0,
        maxPts: 0.25,
        answeredItems: hasAns ? 1 : 0,
        totalItems: 1
      };
    }

    // TF Question
    const tfAns = ans || {};
    const keys = q.items.map((it) => it.key);
    const chosenCount = keys.filter((k) => typeof tfAns[k] === 'boolean').length;

    if (!isGraded) {
      return {
        status: chosenCount === 0 ? 'unanswered' : chosenCount === keys.length ? 'answered' : 'partial',
        answeredItems: chosenCount,
        totalItems: keys.length
      };
    }

    let rightItems = 0;
    keys.forEach((k, idx) => {
      if (tfAns[k] === q.items[idx].answer) {
        rightItems += 1;
      }
    });
    const earnedPts = tfScoreFromCorrectCount(rightItems);
    return {
      status: rightItems === keys.length ? 'correct' : rightItems === 0 ? 'wrong' : 'partial',
      isCorrect: rightItems === keys.length,
      rightItems,
      totalItems: keys.length,
      earnedPts,
      maxPts: 1.0,
      answeredItems: chosenCount
    };
  }

  function countAnswered(session) {
    let count = 0;
    session.questions.forEach((q) => {
      const st = getQuestionState(session, q);
      if (st.answeredItems === st.totalItems) count += 1;
    });
    return count;
  }

  function computeResults(session) {
    let earnedPts = 0;
    let maxPts = 0;
    let mcTotal = 0;
    let mcCorrect = 0;
    let tfTotal = 0;
    let tfFullCorrect = 0;
    let tfItemTotal = 0;
    let tfItemCorrect = 0;

    const byLesson = {};
    DB.lessons.forEach((l) => {
      byLesson[l.id] = {
        id: l.id,
        shortTitle: l.shortTitle,
        earnedPts: 0,
        maxPts: 0,
        count: 0,
        fullCorrect: 0
      };
    });

    session.questions.forEach((q) => {
      const res = getQuestionState({ ...session, submitted: true }, q);
      earnedPts += res.earnedPts;
      maxPts += res.maxPts;

      const lStat = byLesson[q.lessonId];
      if (lStat) {
        lStat.earnedPts += res.earnedPts;
        lStat.maxPts += res.maxPts;
        lStat.count += 1;
        if (res.isCorrect) lStat.fullCorrect += 1;
      }

      if (q.type === 'mc') {
        mcTotal += 1;
        if (res.isCorrect) mcCorrect += 1;
      } else {
        tfTotal += 1;
        tfItemTotal += res.totalItems;
        tfItemCorrect += res.rightItems;
        if (res.isCorrect) tfFullCorrect += 1;
      }

      // Sync wrongIds in persistent store
      if (res.isCorrect) {
        store.wrongIds.delete(q.id);
      } else {
        store.wrongIds.add(q.id);
      }
    });

    saveJSON(STORAGE_KEYS.wrongIds, Array.from(store.wrongIds));

    const score10 = maxPts > 0 ? Math.round(((earnedPts / maxPts) * 10) * 100) / 100 : 0;
    const pct = maxPts > 0 ? Math.round((earnedPts / maxPts) * 100) : 0;

    return {
      score10,
      pct,
      earnedPts: Math.round(earnedPts * 100) / 100,
      maxPts: Math.round(maxPts * 100) / 100,
      mcTotal,
      mcCorrect,
      tfTotal,
      tfFullCorrect,
      tfItemTotal,
      tfItemCorrect,
      lessonBreakdown: Object.values(byLesson).filter((b) => b.count > 0)
    };
  }

  function finalizeSubmission() {
    if (!state.session || state.session.submitted) return;
    stopTimer();
    if (state.session.mode !== 'exam') {
      state.session.elapsedSec = Math.round((Date.now() - state.session.startedAt) / 1000);
    }
    state.session.submitted = true;
    const summary = computeResults(state.session);
    state.session.summary = summary;

    store.history.unshift({
      id: state.session.id,
      title: state.session.title,
      mode: state.session.mode,
      score10: summary.score10,
      pct: summary.pct,
      totalQ: state.session.questions.length,
      elapsedSec: state.session.elapsedSec,
      date: new Date().toLocaleString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit'
      })
    });
    store.history = store.history.slice(0, 12);
    saveJSON(STORAGE_KEYS.history, store.history);

    state.view = 'results';
    closeSheet();
    render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function promptSubmitExam() {
    if (!state.session) return;
    const total = state.session.questions.length;
    const done = countAnswered(state.session);
    const remaining = total - done;

    const msg =
      remaining > 0
        ? `<p>Bạn đã hoàn thành <strong>${done}/${total}</strong> câu. Còn <strong>${remaining} câu</strong> chưa làm đủ hoặc chưa chọn đáp án.</p><p>Bạn có chắc chắn muốn nộp bài ngay để xem điểm và lời giải chi tiết không?</p>`
        : `<p>Tuyệt vời! Bạn đã hoàn thành đủ <strong>${total}/${total}</strong> câu.</p><p>Bấm <strong>Nộp bài ngay</strong> để hệ thống chấm điểm và hiển thị giải thích chi tiết.</p>`;

    openModal({
      title: 'Xác nhận nộp bài',
      bodyHTML: msg,
      buttons: [
        { label: 'Làm tiếp', className: 'btn btn-outline' },
        {
          label: 'Nộp bài ngay',
          className: 'btn btn-success',
          onClick: finalizeSubmission
        }
      ]
    });
  }

  function confirmLeaveWorkspace(targetView) {
    if (state.view === 'workspace' && state.session && state.session.mode === 'exam' && !state.session.submitted) {
      openModal({
        title: 'Thoát khỏi bài thi thử?',
        bodyHTML: '<p>Bài thi thử hiện tại chưa được nộp. Nếu thoát ra ngoài, tiến độ làm bài này sẽ bị hủy.</p>',
        buttons: [
          { label: 'Ở lại làm tiếp', className: 'btn btn-outline' },
          {
            label: 'Thoát & Hủy bài',
            className: 'btn btn-danger-soft',
            onClick: () => {
              stopTimer();
              state.session = null;
              state.view = targetView;
              updateNavActive();
              render();
              window.scrollTo({ top: 0, behavior: 'instant' });
            }
          }
        ]
      });
      return;
    }
    stopTimer();
    state.view = targetView;
    updateNavActive();
    render();
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  /* ------------------------------------------------------------------------
     Render Helpers: Top Navigation
     ------------------------------------------------------------------------ */
  function updateNavActive() {
    const tabs = dom.mainNav.querySelectorAll('.nav-tab');
    tabs.forEach((t) => {
      const v = t.dataset.view;
      const isMatch =
        state.view === v ||
        (state.view === 'workspace' && state.session && state.session.mode === 'practice' && v === 'practice-setup') ||
        (state.view === 'workspace' && state.session && state.session.mode === 'exam' && v === 'home') ||
        (state.view === 'results' && v === 'home');
      t.classList.toggle('active', isMatch);
    });
  }

  /* ------------------------------------------------------------------------
     View 1: Home & Mock Exam Setup (and Practice Setup)
     ------------------------------------------------------------------------ */
  function renderHome(isPracticeDefault = false) {
    if (isPracticeDefault) {
      state.builder.mode = 'practice';
    } else if (state.view === 'home') {
      state.builder.mode = 'exam';
    }

    const wrongCount = store.wrongIds.size;
    const bookmarkCount = store.bookmarks.size;

    const presetsHTML = `
      <section class="preset-grid" aria-label="Đề xuất nhanh">
        <article class="preset-card">
          <div>
            <span class="preset-badge badge-blue">Chuẩn THPT 2025</span>
            <h3 class="preset-title">Thi Thử Đề 28 Câu</h3>
            <p class="preset-desc">24 câu Trắc nghiệm (0.25đ) + 4 câu Đúng/Sai (1.0đ lũy tiến). Thời gian 45 phút.</p>
          </div>
          <button class="btn btn-primary" type="button" data-preset="thpt">Thi thử ngay</button>
        </article>

        <article class="preset-card">
          <div>
            <span class="preset-badge badge-green">Full 100% Đề cương</span>
            <h3 class="preset-title">Thi Toàn Bộ ${DB.counts.total} Câu</h3>
            <p class="preset-desc">Đầy đủ ${DB.counts.mc} câu Phần I và ${DB.counts.tf} câu Phần II từ file đề cương. Thời gian 90 phút.</p>
          </div>
          <button class="btn btn-soft" type="button" data-preset="full-exam">Thi Full ${DB.counts.total} câu</button>
        </article>

        <article class="preset-card">
          <div>
            <span class="preset-badge badge-amber">Chuyên sâu Phần II</span>
            <h3 class="preset-title">Luyện Đúng / Sai (${DB.counts.tf} câu)</h3>
            <p class="preset-desc">Toàn bộ ${DB.counts.tf} câu đọc tư liệu lịch sử, chấm từng ý a, b, c, d kèm giải thích chi tiết.</p>
          </div>
          <button class="btn btn-outline" type="button" data-preset="tf-practice">Ôn Phần II ngay</button>
        </article>

        <article class="preset-card">
          <div>
            <span class="preset-badge badge-rose">Sửa lỗi sai</span>
            <h3 class="preset-title">Câu Làm Sai (${wrongCount})</h3>
            <p class="preset-desc">Ôn tập lại những câu hỏi bạn từng làm sai hoặc đánh dấu sao (${bookmarkCount} câu).</p>
          </div>
          <div style="display:flex; gap:6px;">
            <button class="btn btn-danger-soft" style="flex:1;" type="button" data-preset="wrong" ${wrongCount === 0 ? 'disabled' : ''}>Ôn câu sai</button>
            <button class="btn btn-outline" type="button" data-preset="bookmarks" title="Ôn câu đã đánh dấu sao" ${bookmarkCount === 0 ? 'disabled' : ''}>★ ${bookmarkCount}</button>
          </div>
        </article>
      </section>
    `;

    const builderHTML = `
      <section class="home-grid">
        <div class="card">
          <div class="section-header">
            <div>
              <h2 class="section-title">Tùy chỉnh đề thi &amp; ôn tập</h2>
              <p class="section-sub">Chọn bài học, hình thức chấm và trộn câu theo ý muốn</p>
            </div>
          </div>

          <div class="form-group">
            <span class="form-label">1. Chế độ làm bài</span>
            <div class="segmented" role="group" aria-label="Chế độ">
              <button type="button" class="seg-btn ${state.builder.mode === 'exam' ? 'active' : ''}" data-bmode="exam">Thi thử (Tính giờ &amp; Nộp bài)</button>
              <button type="button" class="seg-btn ${state.builder.mode === 'practice' ? 'active' : ''}" data-bmode="practice">Ôn tập (Chấm từng câu)</button>
            </div>
          </div>

          <div class="form-group">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <span class="form-label" style="margin:0;">2. Phạm vi bài học</span>
              <button type="button" class="btn btn-sm btn-outline" id="toggleAllLessonsBtn">Chọn / Bỏ tất cả</button>
            </div>
            <div class="chip-grid" id="lessonChips">
              ${DB.lessons
                .map((l) => {
                  const checked = state.builder.selectedLessons.includes(l.id);
                  const total = l.mc.length + l.tf.length;
                  return `
                    <label class="chip-toggle ${checked ? 'selected' : ''}">
                      <input type="checkbox" value="${l.id}" ${checked ? 'checked' : ''} />
                      <span>${escapeHTML(l.shortTitle)} (${total})</span>
                    </label>
                  `;
                })
                .join('')}
            </div>
          </div>

          <div class="form-group">
            <span class="form-label">3. Dạng câu hỏi</span>
            <div class="segmented" role="group" aria-label="Dạng câu hỏi">
              <button type="button" class="seg-btn ${state.builder.typeFilter === 'all' ? 'active' : ''}" data-btype="all">Tất cả (Phần I + II)</button>
              <button type="button" class="seg-btn ${state.builder.typeFilter === 'mc' ? 'active' : ''}" data-btype="mc">Phần I: Trắc nghiệm</button>
              <button type="button" class="seg-btn ${state.builder.typeFilter === 'tf' ? 'active' : ''}" data-btype="tf">Phần II: Đúng - Sai</button>
            </div>
          </div>

          <div class="form-group">
            <span class="form-label">4. Tùy chọn thêm</span>
            <div class="switch-row">
              <label for="optShuffleQ">Xáo trộn thứ tự câu hỏi</label>
              <input id="optShuffleQ" type="checkbox" ${state.builder.shuffleQuestions ? 'checked' : ''} />
            </div>
            <div class="switch-row">
              <label for="optShuffleOpt">Xáo trộn đáp án A, B, C, D (Phần I)</label>
              <input id="optShuffleOpt" type="checkbox" ${state.builder.shuffleOptions ? 'checked' : ''} />
            </div>
            ${
              state.builder.mode === 'exam'
                ? `
              <div class="switch-row">
                <label for="optDuration">Thời gian làm bài (phút)</label>
                <input id="optDuration" class="inline-input" type="number" min="5" max="180" step="5" value="${state.builder.durationMin}" style="width:92px;" />
              </div>`
                : `
              <div class="switch-row">
                <label for="optAutoCheck">Tự động chấm &amp; giải thích ngay khi chọn (Phần I)</label>
                <input id="optAutoCheck" type="checkbox" ${state.builder.autoCheckPractice ? 'checked' : ''} />
              </div>`
            }
          </div>

          <button type="button" class="btn btn-primary" style="width:100%;" id="startCustomBtn">
            Bắt đầu (<span id="customCountSpan">0</span> câu hỏi)
          </button>
        </div>

        <div class="card">
          <div class="section-header">
            <div>
              <h2 class="section-title">Cấu trúc 5 bài học trong đề cương</h2>
              <p class="section-sub">100% câu hỏi được trích chuẩn xác từ file PDF</p>
            </div>
          </div>
          <div class="lesson-list">
            ${DB.lessons
              .map(
                (l) => `
                <div class="lesson-item">
                  <div class="lesson-info">
                    <div class="lesson-topic">${escapeHTML(l.topic)}</div>
                    <div class="lesson-name">${escapeHTML(l.title)}</div>
                    <div class="lesson-meta">Phần I: ${l.mc.length} câu • Phần II: ${l.tf.length} câu (${l.tf.length * 4} ý)</div>
                  </div>
                  <div class="lesson-actions">
                    <button class="btn btn-sm btn-soft" type="button" data-lesson-practice="${l.id}">Ôn tập</button>
                    <button class="btn btn-sm btn-primary" type="button" data-lesson-exam="${l.id}">Thi thử</button>
                  </div>
                </div>`
              )
              .join('')}
          </div>
        </div>
      </section>
    `;

    const historyHTML =
      store.history.length > 0
        ? `
      <section class="card">
        <div class="section-header">
          <div>
            <h2 class="section-title">Lịch sử làm bài gần đây</h2>
            <p class="section-sub">Kết quả được lưu tự động trên thiết bị của bạn</p>
          </div>
          <button type="button" class="btn btn-sm btn-outline" id="clearHistoryBtn">Xóa lịch sử</button>
        </div>
        <div class="history-list">
          ${store.history
            .map(
              (h) => `
            <div class="history-card">
              <div style="min-width:0;">
                <div style="font-weight:700; font-size:0.9rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${escapeHTML(h.title)}</div>
                <div style="font-size:0.78rem; color:var(--text-muted);">${h.date} • ${h.totalQ} câu • ${formatTime(h.elapsedSec)}</div>
              </div>
              <div class="history-score">${h.score10.toFixed(2)}đ</div>
            </div>`
            )
            .join('')}
        </div>
      </section>`
        : '';

    dom.mainContent.innerHTML = `
      <div class="container">
        <section class="hero">
          <div>
            <div class="hero-tag">LỊCH SỬ 12 • CHƯƠNG TRÌNH GDPT 2018</div>
            <h1>Hệ thống Thi Thử &amp; Chấm Đúng Sai Kèm Giải Thích</h1>
            <p>Tổng hợp đầy đủ 100% <strong>${DB.counts.total} câu hỏi</strong> (${DB.counts.mc} câu Trắc nghiệm + ${DB.counts.tf} câu Đúng/Sai) từ đề cương Giữa kì I. Chấm điểm chuẩn thang Bộ GD&amp;ĐT 2025, giải thích từng ý a, b, c, d.</p>
            <div class="hero-actions">
              <button type="button" class="btn btn-sm hero-mindmap-btn" id="openMindmapFromHero">
                <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="3"/><circle cx="4.5" cy="6" r="2"/><circle cx="19.5" cy="6" r="2"/><circle cx="4.5" cy="18" r="2"/><circle cx="19.5" cy="18" r="2"/><path d="M9.7 10.2L6.1 7.4M14.3 10.2l3.6-2.8M9.7 13.8l-3.6 2.8M14.3 13.8l3.6 2.8"/></svg>
                <span>Xem Sơ đồ tư duy 5 bài (Không sót ý)</span>
              </button>
            </div>
          </div>
          <div class="hero-stats">
            <div class="hero-stat">
              <div class="hero-stat-val">${DB.counts.total}</div>
              <div class="hero-stat-lbl">Tổng số câu hỏi (100%)</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${DB.counts.mc} / ${DB.counts.tf}</div>
              <div class="hero-stat-lbl">Phần I / Phần II Đúng-Sai</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${store.history.length}</div>
              <div class="hero-stat-lbl">Lần làm bài đã lưu</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${store.wrongIds.size}</div>
              <div class="hero-stat-lbl">Câu cần ôn lại</div>
            </div>
          </div>
        </section>

        ${presetsHTML}
        ${builderHTML}
        ${historyHTML}
      </div>
    `;

    bindHomeEvents();
    updateCustomCount();
  }

  function updateCustomCount() {
    const span = document.getElementById('customCountSpan');
    const btn = document.getElementById('startCustomBtn');
    if (!span || !btn) return;
    const count = buildQuestionsFromFilter({
      lessonIds: state.builder.selectedLessons,
      typeFilter: state.builder.typeFilter,
      shuffleQuestions: false
    }).length;
    span.textContent = count;
    btn.disabled = count === 0;
  }

  function bindHomeEvents() {
    const heroMmBtn = document.getElementById('openMindmapFromHero');
    if (heroMmBtn) {
      heroMmBtn.addEventListener('click', () => confirmLeaveWorkspace('mindmap'));
    }

    // Quick presets
    dom.mainContent.querySelectorAll('[data-preset]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.dataset.preset;
        if (key === 'thpt') {
          createSession({
            title: 'Đề Thi Thử Chuẩn THPT 2025 (28 câu)',
            mode: 'exam',
            questions: buildThpt2025Exam(),
            durationMin: 45,
            shuffleOptions: false,
            isThptPreset: true
          });
        } else if (key === 'full-exam') {
          createSession({
            title: `Thi Full 100% Đề Cương (${DB.counts.total} câu)`,
            mode: 'exam',
            questions: DB.allQuestions.slice(),
            durationMin: 90,
            shuffleOptions: false
          });
        } else if (key === 'tf-practice') {
          createSession({
            title: `Ôn Tập Phần II — Đúng / Sai (${DB.counts.tf} câu)`,
            mode: 'practice',
            questions: DB.allQuestions.filter((q) => q.type === 'tf'),
            autoCheckPractice: true
          });
        } else if (key === 'wrong') {
          const qs = DB.allQuestions.filter((q) => store.wrongIds.has(q.id));
          createSession({
            title: `Ôn Lại Các Câu Làm Sai (${qs.length} câu)`,
            mode: 'practice',
            questions: qs,
            autoCheckPractice: true
          });
        } else if (key === 'bookmarks') {
          const qs = DB.allQuestions.filter((q) => store.bookmarks.has(q.id));
          createSession({
            title: `Ôn Các Câu Đánh Dấu Sao (${qs.length} câu)`,
            mode: 'practice',
            questions: qs,
            autoCheckPractice: true
          });
        }
      });
    });

    // Builder Mode toggle
    dom.mainContent.querySelectorAll('[data-bmode]').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.builder.mode = btn.dataset.bmode;
        state.view = state.builder.mode === 'practice' ? 'practice-setup' : 'home';
        updateNavActive();
        renderHome(state.builder.mode === 'practice');
      });
    });

    // Builder Type toggle
    dom.mainContent.querySelectorAll('[data-btype]').forEach((btn) => {
      btn.addEventListener('click', () => {
        state.builder.typeFilter = btn.dataset.btype;
        dom.mainContent.querySelectorAll('[data-btype]').forEach((b) => {
          b.classList.toggle('active', b.dataset.btype === state.builder.typeFilter);
        });
        updateCustomCount();
      });
    });

    // Lesson checkboxes
    const chipsWrap = document.getElementById('lessonChips');
    if (chipsWrap) {
      chipsWrap.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
        cb.addEventListener('change', () => {
          const id = cb.value;
          if (cb.checked) {
            if (!state.builder.selectedLessons.includes(id)) state.builder.selectedLessons.push(id);
          } else {
            state.builder.selectedLessons = state.builder.selectedLessons.filter((x) => x !== id);
          }
          cb.closest('.chip-toggle').classList.toggle('selected', cb.checked);
          updateCustomCount();
        });
      });
    }

    const toggleAllBtn = document.getElementById('toggleAllLessonsBtn');
    if (toggleAllBtn) {
      toggleAllBtn.addEventListener('click', () => {
        const allSelected = state.builder.selectedLessons.length === DB.lessons.length;
        state.builder.selectedLessons = allSelected ? [] : DB.lessons.map((l) => l.id);
        chipsWrap.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
          cb.checked = !allSelected;
          cb.closest('.chip-toggle').classList.toggle('selected', cb.checked);
        });
        updateCustomCount();
      });
    }

    // Options
    const optShuffleQ = document.getElementById('optShuffleQ');
    if (optShuffleQ) optShuffleQ.addEventListener('change', () => (state.builder.shuffleQuestions = optShuffleQ.checked));
    const optShuffleOpt = document.getElementById('optShuffleOpt');
    if (optShuffleOpt) optShuffleOpt.addEventListener('change', () => (state.builder.shuffleOptions = optShuffleOpt.checked));
    const optDuration = document.getElementById('optDuration');
    if (optDuration) {
      optDuration.addEventListener('change', () => {
        state.builder.durationMin = Math.min(180, Math.max(5, Number(optDuration.value) || 45));
      });
    }
    const optAutoCheck = document.getElementById('optAutoCheck');
    if (optAutoCheck) optAutoCheck.addEventListener('change', () => (state.builder.autoCheckPractice = optAutoCheck.checked));

    // Start custom button
    const startBtn = document.getElementById('startCustomBtn');
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        const qs = buildQuestionsFromFilter({
          lessonIds: state.builder.selectedLessons,
          typeFilter: state.builder.typeFilter,
          shuffleQuestions: state.builder.shuffleQuestions
        });
        const labelMode = state.builder.mode === 'exam' ? 'Thi thử' : 'Ôn tập';
        const lessonLabel =
          state.builder.selectedLessons.length === DB.lessons.length
            ? 'Tất cả 5 bài'
            : `${state.builder.selectedLessons.length} bài đã chọn`;
        createSession({
          title: `${labelMode}: ${lessonLabel} (${qs.length} câu)`,
          mode: state.builder.mode,
          questions: qs,
          durationMin: state.builder.durationMin,
          shuffleOptions: state.builder.shuffleOptions,
          autoCheckPractice: state.builder.autoCheckPractice
        });
      });
    }

    // Per-lesson quick buttons
    dom.mainContent.querySelectorAll('[data-lesson-practice]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const l = DB.lessons.find((x) => x.id === btn.dataset.lessonPractice);
        if (!l) return;
        const qs = buildQuestionsFromFilter({ lessonIds: [l.id], typeFilter: 'all', shuffleQuestions: false });
        createSession({
          title: `Ôn tập • ${l.shortTitle}`,
          mode: 'practice',
          questions: qs,
          autoCheckPractice: true
        });
      });
    });

    dom.mainContent.querySelectorAll('[data-lesson-exam]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const l = DB.lessons.find((x) => x.id === btn.dataset.lessonExam);
        if (!l) return;
        const qs = buildQuestionsFromFilter({ lessonIds: [l.id], typeFilter: 'all', shuffleQuestions: false });
        createSession({
          title: `Thi thử • ${l.shortTitle}`,
          mode: 'exam',
          questions: qs,
          durationMin: 35
        });
      });
    });

    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
      clearHistoryBtn.addEventListener('click', () => {
        store.history = [];
        saveJSON(STORAGE_KEYS.history, []);
        renderHome(state.builder.mode === 'practice');
        showToast('Đã xóa lịch sử làm bài.');
      });
    }
  }

  /* ------------------------------------------------------------------------
     Question Card HTML Builder (Shared by Workspace, Results, & Bank)
     ------------------------------------------------------------------------ */
  function buildQuestionCardInnerHTML(q, displayIdx, options = {}) {
    const {
      session = null,
      forceReveal = false,
      allowInteract = true
    } = options;

    const isBookmarked = store.bookmarks.has(q.id);
    const isGraded = forceReveal || (session && (session.submitted || Boolean(session.checked[q.id])));
    const qState = session ? getQuestionState(session, q) : null;

    let statusPill = '';
    if (isGraded && qState) {
      if (q.type === 'mc') {
        statusPill = qState.isCorrect
          ? `<span class="q-status-pill badge-green">Đúng (+0.25đ)</span>`
          : `<span class="q-status-pill badge-rose">${typeof session.answers[q.id] === 'number' ? 'Sai (0đ)' : 'Chưa chọn (0đ)'}</span>`;
      } else {
        const cls = qState.rightItems === 4 ? 'badge-green' : qState.rightItems === 0 ? 'badge-rose' : 'badge-amber';
        statusPill = `<span class="q-status-pill ${cls}">Đúng ${qState.rightItems}/4 ý (+${qState.earnedPts}đ)</span>`;
      }
    }

    const headerHTML = `
      <div class="q-head">
        <div class="q-tags">
          <span class="q-num-badge">Câu ${displayIdx + 1}</span>
          <span class="q-meta-pill">${escapeHTML(q.lessonShort)} • Câu ${q.num} (${q.type === 'mc' ? 'Phần I' : 'Phần II'})</span>
          ${statusPill}
        </div>
        <button type="button" class="bookmark-btn ${isBookmarked ? 'active' : ''}" data-action="bookmark" data-qid="${q.id}" title="Đánh dấu câu cần lưu ý">
          <svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          <span>${isBookmarked ? 'Đã lưu' : 'Đánh dấu'}</span>
        </button>
      </div>
    `;

    let bodyHTML = '';

    if (q.type === 'mc') {
      const order = session && session.mcOrder[q.id] ? session.mcOrder[q.id] : [0, 1, 2, 3];
      const userAns = session ? session.answers[q.id] : undefined;

      bodyHTML = `
        <p class="q-stem">${escapeHTML(q.question)}</p>
        <div class="mc-options">
          ${order
            .map((origIdx, dispPos) => {
              const isSelected = userAns === origIdx;
              const isTrueOpt = origIdx === q.answer;
              let cls = '';
              let badge = '';
              if (isGraded) {
                if (isTrueOpt) {
                  cls = 'correct';
                  badge = `<span class="mc-badge" style="color:var(--success);">✓ Đáp án đúng</span>`;
                } else if (isSelected) {
                  cls = 'wrong';
                  badge = `<span class="mc-badge" style="color:var(--danger);">✗ Bạn chọn</span>`;
                }
              } else if (isSelected) {
                cls = 'selected';
              }
              return `
                <button type="button" class="mc-opt ${cls}" data-action="mc-select" data-qid="${q.id}" data-orig="${origIdx}" ${!allowInteract || isGraded ? 'disabled' : ''}>
                  <span class="mc-letter">${LETTERS[dispPos]}</span>
                  <span class="mc-text">${escapeHTML(q.options[origIdx])}</span>
                  ${badge}
                </button>`;
            })
            .join('')}
        </div>
      `;

      // Practice check button if not yet graded
      if (allowInteract && session && session.mode === 'practice' && !session.submitted) {
        if (!isGraded) {
          bodyHTML += `
            <div class="q-actions-row">
              <span style="font-size:0.82rem; color:var(--text-muted);">${typeof userAns === 'number' ? 'Đã chọn phương án.' : 'Chọn 1 đáp án ở trên.'}</span>
              <button type="button" class="btn btn-sm btn-soft" data-action="check-one" data-qid="${q.id}">Kiểm tra &amp; Giải thích</button>
            </div>`;
        } else {
          bodyHTML += `
            <div class="q-actions-row">
              <span></span>
              <button type="button" class="btn btn-sm btn-outline" data-action="retry-one" data-qid="${q.id}">Làm lại câu này</button>
            </div>`;
        }
      }

      if (isGraded) {
        const correctDispPos = order.indexOf(q.answer);
        bodyHTML += `
          <div class="exp-box">
            <div class="exp-title">Giải thích chi tiết (Đáp án: ${LETTERS[correctDispPos]})</div>
            <div>${escapeHTML(q.explanation)}</div>
          </div>`;
      }
    } else {
      // TF Question
      const tfAns = session && session.answers[q.id] ? session.answers[q.id] : {};

      bodyHTML = `
        <p class="q-stem">${escapeHTML(q.prompt)}</p>
        <div class="quote-box">${escapeHTML(q.quote)}${q.source ? `<div class="quote-source">${escapeHTML(q.source)}</div>` : ''}</div>
        ${q.extraNote ? `<div class="extra-note">${escapeHTML(q.extraNote)}</div>` : ''}
        <div class="tf-list">
          ${q.items
            .map((item) => {
              const userVal = tfAns[item.key];
              const hasChoice = typeof userVal === 'boolean';
              const isRight = hasChoice && userVal === item.answer;

              let rowCls = '';
              let rightBtnCls = '';
              let wrongBtnCls = '';

              if (isGraded) {
                rowCls = forceReveal ? (item.answer ? 'correct' : '') : isRight ? 'correct' : 'wrong';
                if (item.answer === true) rightBtnCls = 'graded-right';
                else if (userVal === true) rightBtnCls = 'graded-wrong';

                if (item.answer === false) wrongBtnCls = 'graded-right';
                else if (userVal === false) wrongBtnCls = 'graded-wrong';
              } else {
                if (userVal === true) rightBtnCls = 'chosen';
                if (userVal === false) wrongBtnCls = 'chosen';
              }

              return `
                <div class="tf-row ${rowCls}">
                  <div class="tf-top">
                    <div class="tf-text">
                      <span class="tf-key">${item.key}.</span>
                      <span>${escapeHTML(item.text)}</span>
                    </div>
                    <div class="tf-controls">
                      <button type="button" class="tf-btn ${rightBtnCls}" data-action="tf-select" data-qid="${q.id}" data-key="${item.key}" data-val="true" ${!allowInteract || isGraded ? 'disabled' : ''}>Đúng</button>
                      <button type="button" class="tf-btn ${wrongBtnCls}" data-action="tf-select" data-qid="${q.id}" data-key="${item.key}" data-val="false" ${!allowInteract || isGraded ? 'disabled' : ''}>Sai</button>
                    </div>
                  </div>
                  ${
                    isGraded
                      ? `<div class="tf-item-exp"><strong>Đáp án chuẩn: ${item.answer ? 'Đúng (Đ)' : 'Sai (S)'}.</strong> ${escapeHTML(item.explanation)}</div>`
                      : ''
                  }
                </div>`;
            })
            .join('')}
        </div>
      `;

      if (allowInteract && session && session.mode === 'practice' && !session.submitted) {
        const chosenCnt = q.items.filter((it) => typeof tfAns[it.key] === 'boolean').length;
        if (!isGraded) {
          bodyHTML += `
            <div class="q-actions-row">
              <span style="font-size:0.82rem; color:var(--text-muted);">Đã chọn ${chosenCnt}/4 ý.</span>
              <button type="button" class="btn btn-sm btn-soft" data-action="check-one" data-qid="${q.id}">Chấm đúng sai &amp; Giải thích</button>
            </div>`;
        } else {
          bodyHTML += `
            <div class="q-actions-row">
              <span></span>
              <button type="button" class="btn btn-sm btn-outline" data-action="retry-one" data-qid="${q.id}">Làm lại câu này</button>
            </div>`;
        }
      }
    }

    return headerHTML + bodyHTML;
  }

  function getCardBorderClass(q, session) {
    if (!session) return '';
    const isGraded = session.submitted || Boolean(session.checked[q.id]);
    if (!isGraded) return '';
    const st = getQuestionState(session, q);
    if (st.status === 'correct') return 'graded-correct';
    if (st.status === 'wrong') return 'graded-wrong';
    if (st.status === 'partial') return 'graded-partial';
    return '';
  }

  /* ------------------------------------------------------------------------
     View 2: Active Workspace (Exam & Practice)
     ------------------------------------------------------------------------ */
  function renderPaletteInto(container, isMobileSheet = false) {
    const s = state.session;
    if (!s) return;

    const gridHTML = s.questions
      .map((q, idx) => {
        const st = getQuestionState(s, q);
        const bm = store.bookmarks.has(q.id) ? 'bookmarked' : '';
        const cur = s.viewLayout === 'focus' && s.focusIndex === idx ? 'current' : '';
        return `<button type="button" class="p-btn ${st.status} ${bm} ${cur}" data-pidx="${idx}">${idx + 1}</button>`;
      })
      .join('');

    container.innerHTML = `
      <div class="palette-legend">
        <span><i class="legend-dot" style="background:var(--surface-2); border:1px solid var(--border-strong);"></i>Chưa làm</span>
        <span><i class="legend-dot" style="background:var(--primary);"></i>Đã làm</span>
        ${
          s.mode === 'practice' || s.submitted
            ? `<span><i class="legend-dot" style="background:var(--success);"></i>Đúng</span>
               <span><i class="legend-dot" style="background:var(--danger);"></i>Sai</span>`
            : `<span><i class="legend-dot" style="background:var(--warning-soft); border:1px solid var(--warning);"></i>Đang làm dở</span>`
        }
        <span><i class="legend-dot" style="background:var(--amber-star); border-radius:50%;"></i>Lưu ý</span>
      </div>
      <div class="palette-grid">${gridHTML}</div>
    `;

    container.querySelectorAll('.p-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.dataset.pidx);
        jumpToQuestion(idx);
        if (isMobileSheet) closeSheet();
      });
    });
  }

  function jumpToQuestion(idx) {
    const s = state.session;
    if (!s) return;
    if (s.viewLayout === 'focus') {
      s.focusIndex = idx;
      renderWorkspace();
      window.scrollTo({ top: 0, behavior: 'instant' });
    } else {
      const targetPage = Math.floor(idx / PAGE_SIZE_QUIZ) + 1;
      const changedPage = targetPage !== s.page;
      s.page = targetPage;
      if (changedPage) renderWorkspace();
      const targetEl = document.querySelector(`.q-card[data-qid="${s.questions[idx].id}"]`);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }

  function getVisibleSlice(s) {
    if (s.viewLayout === 'focus') {
      const idx = Math.min(Math.max(0, s.focusIndex), s.questions.length - 1);
      return { start: idx, items: [s.questions[idx]], totalPages: s.questions.length, curPage: idx + 1 };
    }
    const totalPages = Math.max(1, Math.ceil(s.questions.length / PAGE_SIZE_QUIZ));
    s.page = Math.min(Math.max(1, s.page), totalPages);
    const start = (s.page - 1) * PAGE_SIZE_QUIZ;
    return {
      start,
      items: s.questions.slice(start, start + PAGE_SIZE_QUIZ),
      totalPages,
      curPage: s.page
    };
  }

  function renderWorkspace() {
    const s = state.session;
    if (!s) return;

    const doneCount = countAnswered(s);
    const total = s.questions.length;
    const slice = getVisibleSlice(s);

    const cardsHTML = slice.items
      .map((q, offset) => {
        const idx = slice.start + offset;
        const borderCls = getCardBorderClass(q, s);
        return `<article class="q-card ${borderCls}" data-qid="${q.id}" data-qidx="${idx}">${buildQuestionCardInnerHTML(q, idx, { session: s, allowInteract: true })}</article>`;
      })
      .join('');

    const pagerHTML =
      slice.totalPages > 1
        ? `
      <div class="pager-bar">
        <button type="button" class="btn btn-outline btn-sm" id="prevPageBtn" ${slice.curPage <= 1 ? 'disabled' : ''}>← ${s.viewLayout === 'focus' ? 'Câu trước' : 'Trang trước'}</button>
        <span style="font-size:0.86rem; font-weight:700; color:var(--text-secondary);">
          ${s.viewLayout === 'focus' ? `Câu ${slice.curPage} / ${total}` : `Trang ${slice.curPage} / ${slice.totalPages}`}
        </span>
        <button type="button" class="btn btn-primary btn-sm" id="nextPageBtn" ${slice.curPage >= slice.totalPages ? 'disabled' : ''}>${s.viewLayout === 'focus' ? 'Câu tiếp' : 'Trang sau'} →</button>
      </div>`
        : '';

    dom.mainContent.innerHTML = `
      <div class="has-mobile-bar">
        <div class="exam-bar">
          <div class="exam-bar-inner">
            <div class="exam-bar-left">
              <button type="button" class="btn btn-sm btn-outline" id="exitWorkspaceBtn">← Thoát</button>
              <div class="exam-title-wrap">
                <div class="exam-title">${escapeHTML(s.title)}</div>
                <div class="exam-progress-txt" id="progressTxt">Đã làm ${doneCount}/${total} câu</div>
              </div>
            </div>
            <div class="exam-bar-right">
              ${
                s.mode === 'exam'
                  ? `<div class="timer-pill ${s.remainingSec <= 60 ? 'danger' : s.remainingSec <= 300 ? 'warning' : ''}" id="timerDisplay">${formatTime(s.remainingSec)}</div>`
                  : `<button type="button" class="btn btn-sm btn-soft" id="checkPageBtn">Chấm trang này</button>`
              }
              <button type="button" class="btn btn-sm btn-outline" id="toggleLayoutBtn" title="Đổi kiểu hiển thị 1 câu hoặc nhiều câu">
                ${s.viewLayout === 'focus' ? 'Xem theo trang' : 'Xem 1 câu'}
              </button>
              <button type="button" class="btn btn-sm btn-success" id="submitTopBtn">Nộp bài</button>
            </div>
          </div>
        </div>

        <div class="container">
          <div class="workspace-layout">
            <div class="questions-col" id="questionsCol">
              ${cardsHTML}
              ${pagerHTML}
            </div>

            <aside class="sidebar-col">
              <div class="palette-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong style="font-size:0.95rem;">Bảng câu hỏi</strong>
                  <span style="font-size:0.8rem; color:var(--text-muted);" id="sidebarCountTxt">${doneCount}/${total}</span>
                </div>
                <div id="desktopPalette"></div>
                <button type="button" class="btn btn-success" style="width:100%; margin-top:14px;" id="submitSideBtn">Nộp bài &amp; Xem điểm</button>
              </div>
            </aside>
          </div>
        </div>

        <div class="mobile-bottom-bar">
          <button type="button" class="btn btn-outline" id="mobilePaletteBtn">Bảng câu (<span id="mobCountTxt">${doneCount}/${total}</span>)</button>
          ${
            slice.totalPages > 1
              ? `<button type="button" class="btn btn-soft" id="mobNextBtn" ${slice.curPage >= slice.totalPages ? 'disabled' : ''}>Tiếp →</button>`
              : ''
          }
          <button type="button" class="btn btn-success" id="submitMobBtn">Nộp bài</button>
        </div>
      </div>
    `;

    renderPaletteInto(document.getElementById('desktopPalette'), false);
    bindWorkspaceEvents();
  }

  function updateSingleQuestionDOM(qid) {
    const s = state.session;
    if (!s) return;
    const card = document.querySelector(`.q-card[data-qid="${qid}"]`);
    if (card) {
      const idx = Number(card.dataset.qidx);
      const q = s.questions[idx];
      card.className = `q-card ${getCardBorderClass(q, s)}`;
      card.innerHTML = buildQuestionCardInnerHTML(q, idx, { session: s, allowInteract: true });
    }

    // Update progress text & palette cell without full re-render
    const done = countAnswered(s);
    const total = s.questions.length;
    const progressTxt = document.getElementById('progressTxt');
    if (progressTxt) progressTxt.textContent = `Đã làm ${done}/${total} câu`;
    const sideCount = document.getElementById('sidebarCountTxt');
    if (sideCount) sideCount.textContent = `${done}/${total}`;
    const mobCount = document.getElementById('mobCountTxt');
    if (mobCount) mobCount.textContent = `${done}/${total}`;

    const qIdx = s.questions.findIndex((x) => x.id === qid);
    if (qIdx !== -1) {
      const st = getQuestionState(s, s.questions[qIdx]);
      const bm = store.bookmarks.has(qid) ? 'bookmarked' : '';
      const cur = s.viewLayout === 'focus' && s.focusIndex === qIdx ? 'current' : '';
      document.querySelectorAll(`.p-btn[data-pidx="${qIdx}"]`).forEach((pBtn) => {
        pBtn.className = `p-btn ${st.status} ${bm} ${cur}`;
      });
    }
  }

  function handleQuestionInteraction(e) {
    const btn = e.target.closest('button[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    const qid = btn.dataset.qid;
    const q = DB.byId[qid];
    if (!q) return;

    if (action === 'bookmark') {
      if (store.bookmarks.has(qid)) {
        store.bookmarks.delete(qid);
        showToast('Đã bỏ đánh dấu câu hỏi.');
      } else {
        store.bookmarks.add(qid);
        showToast('Đã đánh dấu sao câu hỏi.');
      }
      saveJSON(STORAGE_KEYS.bookmarks, Array.from(store.bookmarks));
      if (state.view === 'workspace') {
        updateSingleQuestionDOM(qid);
      } else {
        // Update bookmark button directly in results or bank
        const active = store.bookmarks.has(qid);
        btn.classList.toggle('active', active);
        const span = btn.querySelector('span');
        if (span) span.textContent = active ? 'Đã lưu' : 'Đánh dấu';
      }
      return;
    }

    const s = state.session;
    if (!s || s.submitted) return;

    if (action === 'mc-select') {
      const origIdx = Number(btn.dataset.orig);
      s.answers[qid] = origIdx;
      if (s.mode === 'practice' && s.autoCheckPractice) {
        s.checked[qid] = true;
      }
      updateSingleQuestionDOM(qid);
    } else if (action === 'tf-select') {
      const key = btn.dataset.key;
      const val = btn.dataset.val === 'true';
      if (!s.answers[qid]) s.answers[qid] = {};
      s.answers[qid][key] = val;
      updateSingleQuestionDOM(qid);
    } else if (action === 'check-one') {
      s.checked[qid] = true;
      updateSingleQuestionDOM(qid);
    } else if (action === 'retry-one') {
      delete s.checked[qid];
      delete s.answers[qid];
      updateSingleQuestionDOM(qid);
    }
  }

  function bindWorkspaceEvents() {
    const s = state.session;
    const qCol = document.getElementById('questionsCol');
    if (qCol) {
      qCol.addEventListener('click', handleQuestionInteraction);
    }

    const exitBtn = document.getElementById('exitWorkspaceBtn');
    if (exitBtn) exitBtn.addEventListener('click', () => confirmLeaveWorkspace(s.mode === 'practice' ? 'practice-setup' : 'home'));

    const submitTop = document.getElementById('submitTopBtn');
    const submitSide = document.getElementById('submitSideBtn');
    const submitMob = document.getElementById('submitMobBtn');
    [submitTop, submitSide, submitMob].forEach((b) => {
      if (b) b.addEventListener('click', promptSubmitExam);
    });

    const toggleLayoutBtn = document.getElementById('toggleLayoutBtn');
    if (toggleLayoutBtn) {
      toggleLayoutBtn.addEventListener('click', () => {
        s.viewLayout = s.viewLayout === 'focus' ? 'paged' : 'focus';
        if (s.viewLayout === 'focus') {
          s.focusIndex = (s.page - 1) * PAGE_SIZE_QUIZ;
        } else {
          s.page = Math.floor(s.focusIndex / PAGE_SIZE_QUIZ) + 1;
        }
        renderWorkspace();
        window.scrollTo({ top: 0, behavior: 'instant' });
      });
    }

    const checkPageBtn = document.getElementById('checkPageBtn');
    if (checkPageBtn) {
      checkPageBtn.addEventListener('click', () => {
        const slice = getVisibleSlice(s);
        slice.items.forEach((q) => {
          s.checked[q.id] = true;
        });
        renderWorkspace();
        showToast('Đã chấm tất cả câu hỏi đang hiển thị!');
      });
    }

    const prevBtn = document.getElementById('prevPageBtn');
    const nextBtn = document.getElementById('nextPageBtn');
    const mobNextBtn = document.getElementById('mobNextBtn');

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (s.viewLayout === 'focus') s.focusIndex = Math.max(0, s.focusIndex - 1);
        else s.page = Math.max(1, s.page - 1);
        renderWorkspace();
        window.scrollTo({ top: 0, behavior: 'instant' });
      });
    }
    const goNext = () => {
      const totalPages = s.viewLayout === 'focus' ? s.questions.length : Math.ceil(s.questions.length / PAGE_SIZE_QUIZ);
      if (s.viewLayout === 'focus') s.focusIndex = Math.min(totalPages - 1, s.focusIndex + 1);
      else s.page = Math.min(totalPages, s.page + 1);
      renderWorkspace();
      window.scrollTo({ top: 0, behavior: 'instant' });
    };
    if (nextBtn) nextBtn.addEventListener('click', goNext);
    if (mobNextBtn) mobNextBtn.addEventListener('click', goNext);

    const mobilePaletteBtn = document.getElementById('mobilePaletteBtn');
    if (mobilePaletteBtn) mobilePaletteBtn.addEventListener('click', openSheet);
  }

  /* ------------------------------------------------------------------------
     View 3: Results & Explanations Review
     ------------------------------------------------------------------------ */
  function renderResults() {
    const s = state.session;
    if (!s || !s.summary) {
      state.view = 'home';
      renderHome();
      return;
    }

    const r = s.summary;
    const wrongQuestions = s.questions.filter((q) => !getQuestionState(s, q).isCorrect);

    const filtered = s.questions
      .map((q, idx) => ({ q, idx, st: getQuestionState(s, q) }))
      .filter(({ q, st }) => {
        if (s.resultFilter === 'wrong') return !st.isCorrect;
        if (s.resultFilter === 'correct') return st.isCorrect;
        if (s.resultFilter === 'bookmarked') return store.bookmarks.has(q.id);
        return true;
      });

    const PAGE_SIZE_RES = 20;
    const usePaging = !s.resultShowAll && filtered.length > 25;
    const totalResPages = usePaging ? Math.max(1, Math.ceil(filtered.length / PAGE_SIZE_RES)) : 1;
    s.resultPage = Math.min(Math.max(1, s.resultPage || 1), totalResPages);
    const resStart = usePaging ? (s.resultPage - 1) * PAGE_SIZE_RES : 0;
    const visibleFiltered = usePaging ? filtered.slice(resStart, resStart + PAGE_SIZE_RES) : filtered;

    dom.mainContent.innerHTML = `
      <div class="container">
        <div class="result-hero">
          <div class="score-circle" style="--pct:${r.pct}%;">
            <div class="score-circle-inner">
              <div class="score-num">${r.score10.toFixed(2)}</div>
              <div class="score-scale">Thang 10 (${r.pct}%)</div>
            </div>
          </div>

          <div>
            <span class="preset-badge badge-blue">${escapeHTML(s.title)}</span>
            <h2 style="margin:0 0 6px; font-size:1.35rem;">Kết quả chấm điểm chi tiết</h2>
            <p style="margin:0; font-size:0.88rem; color:var(--text-muted);">
              Tổng điểm đạt được: <strong>${r.earnedPts}/${r.maxPts} điểm</strong> (tính theo thang chuẩn: Trắc nghiệm 0.25đ/câu; Đúng-Sai 1 ý = 0.1đ, 2 ý = 0.25đ, 3 ý = 0.5đ, 4 ý = 1.0đ).
            </p>

            <div class="result-stats-grid">
              <div class="r-stat">
                <div class="r-stat-val" style="color:var(--success);">${r.mcCorrect}/${r.mcTotal}</div>
                <div class="r-stat-lbl">Câu Phần I đúng</div>
              </div>
              <div class="r-stat">
                <div class="r-stat-val" style="color:var(--primary);">${r.tfItemCorrect}/${r.tfItemTotal}</div>
                <div class="r-stat-lbl">Ý Đúng/Sai chuẩn (${r.tfFullCorrect}/${r.tfTotal} câu trọn điểm)</div>
              </div>
              <div class="r-stat">
                <div class="r-stat-val" style="color:var(--danger);">${wrongQuestions.length}</div>
                <div class="r-stat-lbl">Câu cần xem lại</div>
              </div>
              <div class="r-stat">
                <div class="r-stat-val">${formatTime(s.elapsedSec)}</div>
                <div class="r-stat-lbl">Thời gian làm bài</div>
              </div>
            </div>

            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              ${
                wrongQuestions.length > 0
                  ? `<button type="button" class="btn btn-danger-soft" id="retryWrongBtn">Làm lại ${wrongQuestions.length} câu chưa đúng</button>`
                  : `<span class="preset-badge badge-green" style="padding:10px 14px; font-size:0.88rem;">Xuất sắc! Bạn đúng 100% toàn bộ bài!</span>`
              }
              <button type="button" class="btn btn-primary" id="retakeSameBtn">Thi lại đề này</button>
              <button type="button" class="btn btn-outline" id="backHomeBtn">Về trang chủ</button>
            </div>
          </div>
        </div>

        <section class="breakdown-grid">
          ${r.lessonBreakdown
            .map((b) => {
              const p = b.maxPts > 0 ? Math.round((b.earnedPts / b.maxPts) * 100) : 0;
              return `
              <div class="bd-card">
                <div style="display:flex; justify-content:space-between; gap:8px; font-weight:700; font-size:0.88rem;">
                  <span>${escapeHTML(b.shortTitle)}</span>
                  <span style="color:var(--primary);">${p}%</span>
                </div>
                <div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">Đúng trọn ${b.fullCorrect}/${b.count} câu (${Math.round(b.earnedPts * 100) / 100}/${Math.round(b.maxPts * 100) / 100}đ)</div>
                <div class="progress-track"><div class="progress-fill" style="width:${p}%;"></div></div>
              </div>`;
            })
            .join('')}
        </section>

        <div class="filter-bar">
          <strong style="font-size:0.94rem;">Xem lại đáp án &amp; giải thích (${filtered.length} câu):</strong>
          <div class="segmented" style="width:auto; flex:1 1 auto;">
            <button type="button" class="seg-btn ${s.resultFilter === 'all' ? 'active' : ''}" data-rfilter="all">Tất cả (${s.questions.length})</button>
            <button type="button" class="seg-btn ${s.resultFilter === 'wrong' ? 'active' : ''}" data-rfilter="wrong">Chưa đúng (${wrongQuestions.length})</button>
            <button type="button" class="seg-btn ${s.resultFilter === 'correct' ? 'active' : ''}" data-rfilter="correct">Đúng (${s.questions.length - wrongQuestions.length})</button>
            <button type="button" class="seg-btn ${s.resultFilter === 'bookmarked' ? 'active' : ''}" data-rfilter="bookmarked">Đánh dấu ★</button>
          </div>
          ${
            filtered.length > 25
              ? `<button type="button" class="btn btn-sm btn-outline" id="toggleResAllBtn">${s.resultShowAll ? 'Chia trang (20 câu)' : `Hiện cả ${filtered.length} câu`}</button>`
              : ''
          }
        </div>

        <div class="questions-col" id="resultQuestionsCol">
          ${
            visibleFiltered.length > 0
              ? visibleFiltered
                  .map(({ q, idx }) => `<article class="q-card ${getCardBorderClass(q, s)}" data-qid="${q.id}">${buildQuestionCardInnerHTML(q, idx, { session: s, allowInteract: false })}</article>`)
                  .join('')
              : `<div class="card" style="text-align:center; color:var(--text-muted);">Không có câu hỏi nào trong bộ lọc này.</div>`
          }
        </div>

        ${
          totalResPages > 1
            ? `
          <div class="pager-bar" style="margin-top:16px;">
            <button type="button" class="btn btn-outline btn-sm" id="resPrevBtn" ${s.resultPage <= 1 ? 'disabled' : ''}>← Trang trước</button>
            <span style="font-size:0.86rem; font-weight:700;">Trang ${s.resultPage} / ${totalResPages}</span>
            <button type="button" class="btn btn-primary btn-sm" id="resNextBtn" ${s.resultPage >= totalResPages ? 'disabled' : ''}>Trang sau →</button>
          </div>`
            : ''
        }
      </div>
    `;

    // Bind events
    document.getElementById('resultQuestionsCol').addEventListener('click', handleQuestionInteraction);

    dom.mainContent.querySelectorAll('[data-rfilter]').forEach((btn) => {
      btn.addEventListener('click', () => {
        s.resultFilter = btn.dataset.rfilter;
        s.resultPage = 1;
        renderResults();
      });
    });

    const toggleResAllBtn = document.getElementById('toggleResAllBtn');
    if (toggleResAllBtn) {
      toggleResAllBtn.addEventListener('click', () => {
        s.resultShowAll = !s.resultShowAll;
        s.resultPage = 1;
        renderResults();
      });
    }

    const resPrevBtn = document.getElementById('resPrevBtn');
    const resNextBtn = document.getElementById('resNextBtn');
    if (resPrevBtn) {
      resPrevBtn.addEventListener('click', () => {
        s.resultPage -= 1;
        renderResults();
        document.getElementById('resultQuestionsCol')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }
    if (resNextBtn) {
      resNextBtn.addEventListener('click', () => {
        s.resultPage += 1;
        renderResults();
        document.getElementById('resultQuestionsCol')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    }

    const retryWrongBtn = document.getElementById('retryWrongBtn');
    if (retryWrongBtn) {
      retryWrongBtn.addEventListener('click', () => {
        createSession({
          title: `Ôn Lại Câu Sai (${wrongQuestions.length} câu)`,
          mode: 'practice',
          questions: wrongQuestions,
          autoCheckPractice: true
        });
      });
    }

    document.getElementById('retakeSameBtn').addEventListener('click', () => {
      createSession({
        title: s.title,
        mode: s.mode,
        questions: s.questions.slice(),
        durationMin: Math.round(s.durationSec / 60),
        shuffleOptions: false,
        autoCheckPractice: s.autoCheckPractice,
        isThptPreset: s.isThptPreset
      });
    });

    document.getElementById('backHomeBtn').addEventListener('click', () => {
      state.session = null;
      state.view = 'home';
      updateNavActive();
      render();
      window.scrollTo({ top: 0, behavior: 'instant' });
    });
  }

  /* ------------------------------------------------------------------------
     View 4: Question Bank (All 177 Questions Lookup)
     ------------------------------------------------------------------------ */
  function getFilteredBankQuestions() {
    const qNorm = stripVN(state.bank.query.trim());
    return DB.allQuestions.filter((q) => {
      if (state.bank.lessonId !== 'all' && q.lessonId !== state.bank.lessonId) return false;
      if (state.bank.type !== 'all' && q.type !== state.bank.type) return false;
      if (qNorm) {
        const hay =
          q.type === 'mc'
            ? `${q.question} ${q.options.join(' ')} ${q.explanation}`
            : `${q.prompt} ${q.quote} ${q.items.map((i) => `${i.text} ${i.explanation}`).join(' ')}`;
        if (!stripVN(hay).includes(qNorm)) return false;
      }
      return true;
    });
  }

  function renderBankListOnly() {
    const filtered = getFilteredBankQuestions();
    const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE_BANK));
    state.bank.page = Math.min(Math.max(1, state.bank.page), totalPages);
    const start = (state.bank.page - 1) * PAGE_SIZE_BANK;
    const slice = filtered.slice(start, start + PAGE_SIZE_BANK);

    const countEl = document.getElementById('bankCountInfo');
    const colEl = document.getElementById('bankQuestionsCol');
    const pagerEl = document.getElementById('bankPagerRegion');

    if (countEl) {
      countEl.innerHTML = `Tìm thấy <strong>${filtered.length}</strong> câu hỏi • Trang ${state.bank.page}/${totalPages}`;
    }
    if (colEl) {
      colEl.innerHTML =
        slice.length > 0
          ? slice
              .map(
                (q, offset) =>
                  `<article class="q-card" data-qid="${q.id}">${buildQuestionCardInnerHTML(q, start + offset, {
                    forceReveal: state.bank.showAnswers,
                    allowInteract: false
                  })}</article>`
              )
              .join('')
          : `<div class="card" style="text-align:center; color:var(--text-muted);">Không tìm thấy câu hỏi phù hợp. Hãy thử từ khóa khác.</div>`;
    }
    if (pagerEl) {
      pagerEl.innerHTML =
        totalPages > 1
          ? `
          <div class="pager-bar" style="margin-top:16px;">
            <button type="button" class="btn btn-outline btn-sm" id="bankPrevBtn" ${state.bank.page <= 1 ? 'disabled' : ''}>← Trang trước</button>
            <span style="font-size:0.86rem; font-weight:700;">Trang ${state.bank.page} / ${totalPages}</span>
            <button type="button" class="btn btn-primary btn-sm" id="bankNextBtn" ${state.bank.page >= totalPages ? 'disabled' : ''}>Trang sau →</button>
          </div>`
          : '';
      const prev = document.getElementById('bankPrevBtn');
      const next = document.getElementById('bankNextBtn');
      if (prev) {
        prev.addEventListener('click', () => {
          state.bank.page -= 1;
          renderBankListOnly();
          window.scrollTo({ top: 0, behavior: 'instant' });
        });
      }
      if (next) {
        next.addEventListener('click', () => {
          state.bank.page += 1;
          renderBankListOnly();
          window.scrollTo({ top: 0, behavior: 'instant' });
        });
      }
    }
  }

  function renderBank() {
    dom.mainContent.innerHTML = `
      <div class="container">
        <div class="section-header">
          <div>
            <h1 class="section-title" style="font-size:1.3rem;">Kho toàn bộ ${DB.counts.total} câu hỏi trong đề cương</h1>
            <p class="section-sub">Tra cứu nhanh câu hỏi, đáp án chuẩn và giải thích chi tiết (100% từ file PDF)</p>
          </div>
          <button type="button" class="btn btn-sm ${state.bank.showAnswers ? 'btn-primary' : 'btn-outline'}" id="bankToggleAnsBtn">
            ${state.bank.showAnswers ? 'Đang hiện đáp án &amp; giải thích' : 'Đang ẩn đáp án (tự nhẩm)'}
          </button>
        </div>

        <div class="filter-bar">
          <input type="search" class="search-input" id="bankSearchInput" placeholder="Tìm câu hỏi, tư liệu, từ khóa (vd: I-an-ta, ASEAN, 1945)..." value="${escapeHTML(state.bank.query)}" />
          <select class="inline-select" id="bankLessonSelect" aria-label="Lọc theo bài">
            <option value="all" ${state.bank.lessonId === 'all' ? 'selected' : ''}>Tất cả 5 bài (${DB.counts.total})</option>
            ${DB.lessons
              .map(
                (l) =>
                  `<option value="${l.id}" ${state.bank.lessonId === l.id ? 'selected' : ''}>${escapeHTML(l.shortTitle)} (${l.mc.length + l.tf.length})</option>`
              )
              .join('')}
          </select>
          <select class="inline-select" id="bankTypeSelect" aria-label="Lọc theo dạng câu">
            <option value="all" ${state.bank.type === 'all' ? 'selected' : ''}>Phần I + II</option>
            <option value="mc" ${state.bank.type === 'mc' ? 'selected' : ''}>Chỉ Phần I (${DB.counts.mc})</option>
            <option value="tf" ${state.bank.type === 'tf' ? 'selected' : ''}>Chỉ Phần II (${DB.counts.tf})</option>
          </select>
        </div>

        <div id="bankCountInfo" style="font-size:0.84rem; color:var(--text-muted); margin-bottom:12px;"></div>
        <div class="questions-col" id="bankQuestionsCol"></div>
        <div id="bankPagerRegion"></div>
      </div>
    `;

    renderBankListOnly();

    // Bind Bank events once (search input stays mounted!)
    const bankCol = document.getElementById('bankQuestionsCol');
    if (bankCol) bankCol.addEventListener('click', handleQuestionInteraction);

    const searchInput = document.getElementById('bankSearchInput');
    let searchDebounce = null;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchDebounce);
      searchDebounce = setTimeout(() => {
        state.bank.query = searchInput.value;
        state.bank.page = 1;
        renderBankListOnly();
      }, 180);
    });

    document.getElementById('bankLessonSelect').addEventListener('change', (e) => {
      state.bank.lessonId = e.target.value;
      state.bank.page = 1;
      renderBankListOnly();
    });

    document.getElementById('bankTypeSelect').addEventListener('change', (e) => {
      state.bank.type = e.target.value;
      state.bank.page = 1;
      renderBankListOnly();
    });

    const toggleAnsBtn = document.getElementById('bankToggleAnsBtn');
    toggleAnsBtn.addEventListener('click', () => {
      state.bank.showAnswers = !state.bank.showAnswers;
      toggleAnsBtn.className = `btn btn-sm ${state.bank.showAnswers ? 'btn-primary' : 'btn-outline'}`;
      toggleAnsBtn.innerHTML = state.bank.showAnswers ? 'Đang hiện đáp án &amp; giải thích' : 'Đang ẩn đáp án (tự nhẩm)';
      renderBankListOnly();
    });
  }

  /* ------------------------------------------------------------------------
     View 5: Sơ đồ tư duy (Mind Map) — Full 5 Bài
     ------------------------------------------------------------------------ */
  function getActiveMindMap() {
    return MINDMAPS.find((m) => m.id === state.mindmap.lessonId) || MINDMAPS[0] || null;
  }

  function countMindMapMetrics(mm) {
    let nodes = 0;
    let items = 0;
    for (const b of mm.branches) {
      nodes += b.children.length;
      for (const c of b.children) {
        items += c.points.length + (c.traps ? c.traps.length : 0);
      }
    }
    return { branches: mm.branches.length, nodes, items };
  }

  function highlightTextHTML(rawText, query) {
    const text = String(rawText == null ? '' : rawText).normalize('NFC');
    const qNorm = stripVN((query || '').trim());
    if (!qNorm) return escapeHTML(text);

    let norm = '';
    const map = [];
    let offset = 0;
    for (const ch of Array.from(text)) {
      const s = stripVN(ch);
      if (s.length === 0) {
        if (map.length > 0) map[map.length - 1].end = offset + ch.length;
      } else {
        for (let k = 0; k < s.length; k++) {
          map.push({ start: offset, end: offset + ch.length });
        }
        norm += s;
      }
      offset += ch.length;
    }

    const ranges = [];
    let pos = 0;
    while (pos <= norm.length - qNorm.length) {
      const idx = norm.indexOf(qNorm, pos);
      if (idx === -1) break;
      const origStart = map[idx].start;
      const origEnd = map[idx + qNorm.length - 1].end;
      if (ranges.length && ranges[ranges.length - 1][1] >= origStart) {
        ranges[ranges.length - 1][1] = Math.max(ranges[ranges.length - 1][1], origEnd);
      } else {
        ranges.push([origStart, origEnd]);
      }
      pos = idx + qNorm.length;
    }

    if (ranges.length === 0) return escapeHTML(text);
    let out = '';
    let cursor = 0;
    for (const [start, end] of ranges) {
      if (start > cursor) out += escapeHTML(text.slice(cursor, start));
      out += `<mark class="mm-hit">${escapeHTML(text.slice(start, end))}</mark>`;
      cursor = end;
    }
    if (cursor < text.length) out += escapeHTML(text.slice(cursor));
    return out;
  }

  function formatMindMapPointHTML(rawText, query) {
    const text = String(rawText || '');
    const m = text.match(/^([^:\n]{2,46}:)\s+(.+)$/);
    if (m) {
      return `<span class="mm-lead">${highlightTextHTML(m[1], query)}</span> ${highlightTextHTML(m[2], query)}`;
    }
    return highlightTextHTML(text, query);
  }

  function filterMindMapBranches(mm, query) {
    const qNorm = stripVN((query || '').trim());
    if (!qNorm) return mm.branches;
    const out = [];
    for (const b of mm.branches) {
      if (stripVN(b.title).includes(qNorm)) {
        out.push(b);
        continue;
      }
      const matchedChildren = b.children.filter((c) => {
        if (stripVN(c.title).includes(qNorm)) return true;
        if (c.points.some((p) => stripVN(p).includes(qNorm))) return true;
        if (c.traps && c.traps.some((t) => stripVN(t).includes(qNorm))) return true;
        return false;
      });
      if (matchedChildren.length > 0) {
        out.push(Object.assign({}, b, { children: matchedChildren }));
      }
    }
    return out;
  }

  function renderMindMapLeafCardHTML(child, query, branchColor) {
    const trapsHTML =
      child.traps && child.traps.length > 0
        ? `
          <div class="mm-traps-box">
            <div class="mm-traps-title">Lưu ý bẫy đề thi</div>
            <ul class="mm-traps-list">
              ${child.traps.map((t) => `<li>${highlightTextHTML(t, query)}</li>`).join('')}
            </ul>
          </div>`
        : '';

    return `
      <article class="mm-leaf-card" style="--branch-color:${escapeHTML(branchColor)};">
        <h3 class="mm-leaf-title">${highlightTextHTML(child.title, query)}</h3>
        <ul class="mm-points-list">
          ${child.points.map((p) => `<li class="mm-point">${formatMindMapPointHTML(p, query)}</li>`).join('')}
        </ul>
        ${trapsHTML}
      </article>
    `;
  }

  function renderMindMapCanvasOnly() {
    const mm = getActiveMindMap();
    const statusLine = document.getElementById('mmStatusLine');
    const canvasRegion = document.getElementById('mmCanvasRegion');
    const clearBtn = document.getElementById('mmClearSearchBtn');
    const treeBtn = document.getElementById('mmLayoutTreeBtn');
    const vertBtn = document.getElementById('mmLayoutVertBtn');
    if (!mm || !canvasRegion) return;

    const query = state.mindmap.query.trim();
    const isSearching = query.length > 0;
    const branches = filterMindMapBranches(mm, query);
    const totalMetrics = countMindMapMetrics(mm);

    if (clearBtn) clearBtn.hidden = !isSearching;
    if (treeBtn) treeBtn.classList.toggle('active', state.mindmap.layout === 'tree');
    if (vertBtn) vertBtn.classList.toggle('active', state.mindmap.layout === 'vertical');

    if (statusLine) {
      const visiblePoints = branches.reduce(
        (acc, b) => acc + b.children.reduce((ca, c) => ca + c.points.length + (c.traps ? c.traps.length : 0), 0),
        0
      );
      statusLine.innerHTML = isSearching
        ? `<span>Đang lọc theo <strong>"${escapeHTML(query)}"</strong>: thấy <strong>${branches.length}</strong>/${mm.branches.length} nhánh (${visiblePoints} ý liên quan).</span>`
        : `<span><strong>${escapeHTML(mm.title)}</strong> • ${totalMetrics.branches} nhánh chính • ${totalMetrics.nodes} cụm kiến thức • ${totalMetrics.items} ý trọng tâm &amp; bẫy đề thi.</span><span>${state.mindmap.layout === 'tree' ? 'Mẹo: Cuộn ngang hoặc nhấn vào tên nhánh để thu gọn/mở rộng.' : 'Mẹo: Nhấn từng nhánh để mở rộng hoặc chuyển sang Sơ đồ nhánh ngang.'}</span>`;
    }

    if (branches.length === 0) {
      canvasRegion.innerHTML = `
        <div class="empty-state card">
          <p style="margin:0 0 10px; font-weight:600; color:var(--text);">Không tìm thấy ý kiến thức nào khớp với "${escapeHTML(query)}" trong ${escapeHTML(mm.shortTitle)}.</p>
          <button type="button" class="btn btn-sm btn-primary" data-mm-clear="1">Xóa từ khóa tìm kiếm</button>
        </div>
      `;
      return;
    }

    const isBranchCollapsed = (branchId) => !isSearching && Boolean(state.mindmap.collapsed[branchId]);

    if (state.mindmap.layout === 'tree') {
      canvasRegion.innerHTML = `
        <div class="mm-tree-scroll" style="--mm-accent:${escapeHTML(mm.accent)}; --mm-accent-soft:${escapeHTML(mm.accentSoft)};">
          <div class="mm-tree">
            <div class="mm-root-col">
              <div class="mm-root-node">
                <div class="mm-root-kicker">${escapeHTML(mm.shortTitle)}</div>
                <h2 class="mm-root-title">${escapeHTML(mm.center.title)}</h2>
                <p class="mm-root-desc">${escapeHTML(mm.center.desc)}</p>
              </div>
            </div>
            <div class="mm-root-link" aria-hidden="true"></div>
            <div class="mm-branches-col">
              ${branches
                .map((b) => {
                  const collapsed = isBranchCollapsed(b.id);
                  const branchColor = b.color || mm.accent;
                  const leafCount = b.children.length;
                  const childrenHTML = !collapsed
                    ? `
                      <div class="mm-branch-arm" aria-hidden="true"></div>
                      <div class="mm-children-col">
                        ${b.children
                          .map(
                            (child) => `
                            <div class="mm-leaf-wrap">
                              ${renderMindMapLeafCardHTML(child, query, branchColor)}
                            </div>`
                          )
                          .join('')}
                      </div>`
                    : '';

                  return `
                    <div class="mm-branch-row" style="--branch-color:${escapeHTML(branchColor)};">
                      <button type="button" class="mm-branch-node" data-mm-toggle="${b.id}" aria-expanded="${!collapsed}">
                        <div class="mm-branch-head">
                          <span class="mm-branch-title">${highlightTextHTML(b.title, query)}</span>
                          <span class="mm-branch-toggle">${collapsed ? '+' : '−'}</span>
                        </div>
                        <div class="mm-branch-meta">${leafCount} cụm ý • ${collapsed ? 'Nhấn để mở' : 'Đang mở'}</div>
                      </button>
                      ${childrenHTML}
                    </div>`;
                })
                .join('')}
            </div>
          </div>
        </div>
      `;
    } else {
      canvasRegion.innerHTML = `
        <div class="mm-vertical" style="--mm-accent:${escapeHTML(mm.accent)}; --mm-accent-soft:${escapeHTML(mm.accentSoft)};">
          <div class="mm-root-node">
            <div class="mm-root-kicker">${escapeHTML(mm.shortTitle)}</div>
            <h2 class="mm-root-title">${escapeHTML(mm.center.title)}</h2>
            <p class="mm-root-desc">${escapeHTML(mm.center.desc)}</p>
          </div>
          ${branches
            .map((b) => {
              const collapsed = isBranchCollapsed(b.id);
              const branchColor = b.color || mm.accent;
              return `
                <section class="mm-vbranch" style="--branch-color:${escapeHTML(branchColor)};">
                  <button type="button" class="mm-vbranch-head" data-mm-toggle="${b.id}" aria-expanded="${!collapsed}">
                    <div>
                      <div class="mm-branch-title">${highlightTextHTML(b.title, query)}</div>
                      <div class="mm-branch-meta">${b.children.length} cụm ý trọng tâm</div>
                    </div>
                    <span class="mm-branch-toggle">${collapsed ? '+' : '−'}</span>
                  </button>
                  ${
                    !collapsed
                      ? `<div class="mm-vbranch-body">
                          ${b.children.map((child) => renderMindMapLeafCardHTML(child, query, branchColor)).join('')}
                        </div>`
                      : ''
                  }
                </section>`;
            })
            .join('')}
        </div>
      `;
    }
  }

  function renderMindMap() {
    const mm = getActiveMindMap();
    if (!mm) {
      dom.mainContent.innerHTML = '<div class="container"><div class="card">Chưa có dữ liệu sơ đồ tư duy.</div></div>';
      return;
    }

    const tabsHTML = MINDMAPS.map((item, idx) => {
      const metrics = countMindMapMetrics(item);
      const isActive = item.id === mm.id;
      const cleanName = item.shortTitle.replace(/^Bài\s+\d+:\s*/i, '');
      return `
        <button
          type="button"
          class="mm-lesson-pill ${isActive ? 'active' : ''}"
          data-mm-lesson="${item.id}"
          style="--mm-accent:${escapeHTML(item.accent)}; --mm-accent-soft:${escapeHTML(item.accentSoft)};"
        >
          <span class="mm-pill-num">Bài ${idx + 1}</span>
          <span class="mm-pill-name">${escapeHTML(cleanName)}</span>
          <span class="mm-pill-meta">${metrics.branches} nhánh • ${metrics.items} ý</span>
        </button>
      `;
    }).join('');

    dom.mainContent.innerHTML = `
      <div class="container">
        <div class="mm-page-header">
          <div>
            <h1>Sơ đồ tư duy Lịch sử 12 — Trọn bộ 5 bài</h1>
            <p class="section-sub">${escapeHTML(mm.subtitle)} • Tổng hợp 100% ý chính, mốc thời gian, tổ chức &amp; lưu ý bẫy trắc nghiệm</p>
          </div>
          <div class="mm-header-actions">
            <button type="button" class="btn btn-sm btn-soft" id="mmPracticeLessonBtn">Ôn câu hỏi ${escapeHTML(mm.shortTitle.split(':')[0])}</button>
            <button type="button" class="btn btn-sm btn-primary" id="mmExamLessonBtn">Thi thử ${escapeHTML(mm.shortTitle.split(':')[0])}</button>
          </div>
        </div>

        <div class="mm-lesson-tabs" role="tablist" aria-label="Chọn bài học sơ đồ tư duy">
          ${tabsHTML}
        </div>

        <div class="mm-toolbar">
          <div class="mm-search-wrap">
            <input
              type="search"
              class="search-input"
              id="mmSearchInput"
              placeholder="Lọc ý, năm, từ khóa trong ${escapeHTML(mm.shortTitle.split(':')[0])} (vd: 1945, I-an-ta, ASEAN, Biển Đông)..."
              value="${escapeHTML(state.mindmap.query)}"
            />
            <button type="button" class="mm-search-clear" id="mmClearSearchBtn" title="Xóa tìm kiếm" aria-label="Xóa tìm kiếm" ${state.mindmap.query.trim() ? '' : 'hidden'}>×</button>
          </div>

          <div class="mm-tool-group">
            <div class="mm-layout-seg" role="group" aria-label="Kiểu hiển thị sơ đồ">
              <button type="button" class="mm-layout-btn ${state.mindmap.layout === 'tree' ? 'active' : ''}" id="mmLayoutTreeBtn">Nhánh ngang</button>
              <button type="button" class="mm-layout-btn ${state.mindmap.layout === 'vertical' ? 'active' : ''}" id="mmLayoutVertBtn">Cây dọc</button>
            </div>
            <button type="button" class="btn btn-sm btn-outline" id="mmExpandAllBtn">Mở hết</button>
            <button type="button" class="btn btn-sm btn-outline" id="mmCollapseAllBtn">Thu gọn</button>
          </div>
        </div>

        <div class="mm-status-line" id="mmStatusLine"></div>
        <div id="mmCanvasRegion"></div>
      </div>
    `;

    renderMindMapCanvasOnly();

    // Lesson tab switch
    dom.mainContent.querySelectorAll('[data-mm-lesson]').forEach((btn) => {
      btn.addEventListener('click', () => {
        if (state.mindmap.lessonId === btn.dataset.mmLesson) return;
        state.mindmap.lessonId = btn.dataset.mmLesson;
        renderMindMap();
      });
    });

    // Quick practice / exam for current mind map lesson
    const practiceBtn = document.getElementById('mmPracticeLessonBtn');
    if (practiceBtn) {
      practiceBtn.addEventListener('click', () => {
        const l = DB.lessons.find((x) => x.id === state.mindmap.lessonId);
        if (!l) return;
        const qs = buildQuestionsFromFilter({ lessonIds: [l.id], typeFilter: 'all', shuffleQuestions: false });
        createSession({
          title: `Ôn tập • ${l.shortTitle}`,
          mode: 'practice',
          questions: qs,
          autoCheckPractice: true
        });
      });
    }

    const examBtn = document.getElementById('mmExamLessonBtn');
    if (examBtn) {
      examBtn.addEventListener('click', () => {
        const l = DB.lessons.find((x) => x.id === state.mindmap.lessonId);
        if (!l) return;
        const qs = buildQuestionsFromFilter({ lessonIds: [l.id], typeFilter: 'all', shuffleQuestions: false });
        createSession({
          title: `Thi thử • ${l.shortTitle}`,
          mode: 'exam',
          questions: qs,
          durationMin: 35
        });
      });
    }

    // Live search input (stays mounted so mobile keyboard stays open)
    const searchInput = document.getElementById('mmSearchInput');
    let mmSearchDebounce = null;
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(mmSearchDebounce);
        mmSearchDebounce = setTimeout(() => {
          state.mindmap.query = searchInput.value;
          renderMindMapCanvasOnly();
        }, 120);
      });
    }

    const clearBtn = document.getElementById('mmClearSearchBtn');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        state.mindmap.query = '';
        if (searchInput) {
          searchInput.value = '';
          searchInput.focus();
        }
        renderMindMapCanvasOnly();
      });
    }

    // Layout toggles
    const treeBtn = document.getElementById('mmLayoutTreeBtn');
    if (treeBtn) {
      treeBtn.addEventListener('click', () => {
        state.mindmap.layout = 'tree';
        renderMindMapCanvasOnly();
      });
    }
    const vertBtn = document.getElementById('mmLayoutVertBtn');
    if (vertBtn) {
      vertBtn.addEventListener('click', () => {
        state.mindmap.layout = 'vertical';
        renderMindMapCanvasOnly();
      });
    }

    // Expand / Collapse all branches in current lesson
    const expandAllBtn = document.getElementById('mmExpandAllBtn');
    if (expandAllBtn) {
      expandAllBtn.addEventListener('click', () => {
        mm.branches.forEach((b) => {
          state.mindmap.collapsed[b.id] = false;
        });
        renderMindMapCanvasOnly();
      });
    }
    const collapseAllBtn = document.getElementById('mmCollapseAllBtn');
    if (collapseAllBtn) {
      collapseAllBtn.addEventListener('click', () => {
        mm.branches.forEach((b) => {
          state.mindmap.collapsed[b.id] = true;
        });
        renderMindMapCanvasOnly();
      });
    }

    // Delegated branch toggle & empty-clear actions inside canvas
    const canvasRegion = document.getElementById('mmCanvasRegion');
    if (canvasRegion) {
      canvasRegion.addEventListener('click', (e) => {
        const toggleBtn = e.target.closest('[data-mm-toggle]');
        if (toggleBtn) {
          const bid = toggleBtn.dataset.mmToggle;
          state.mindmap.collapsed[bid] = !state.mindmap.collapsed[bid];
          renderMindMapCanvasOnly();
          return;
        }
        const clearEmpty = e.target.closest('[data-mm-clear]');
        if (clearEmpty) {
          state.mindmap.query = '';
          if (searchInput) searchInput.value = '';
          renderMindMapCanvasOnly();
        }
      });
    }
  }

  /* ------------------------------------------------------------------------
     Main Render Dispatcher & Global Listeners
     ------------------------------------------------------------------------ */
  function render() {
    if (state.view === 'home') renderHome(false);
    else if (state.view === 'practice-setup') renderHome(true);
    else if (state.view === 'mindmap') renderMindMap();
    else if (state.view === 'workspace') renderWorkspace();
    else if (state.view === 'results') renderResults();
    else if (state.view === 'bank') renderBank();
  }

  function init() {
    applyTheme(store.theme);

    dom.themeToggle.addEventListener('click', () => {
      applyTheme(store.theme === 'dark' ? 'light' : 'dark');
    });

    dom.brandBtn.addEventListener('click', () => confirmLeaveWorkspace('home'));
    dom.brandBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        confirmLeaveWorkspace('home');
      }
    });

    dom.mainNav.querySelectorAll('.nav-tab').forEach((tab) => {
      tab.addEventListener('click', () => {
        confirmLeaveWorkspace(tab.dataset.view);
      });
    });

    dom.modalCloseBtn.addEventListener('click', closeModal);
    dom.modalBackdrop.addEventListener('click', (e) => {
      if (e.target === dom.modalBackdrop) closeModal();
    });

    dom.sheetCloseBtn.addEventListener('click', closeSheet);
    dom.sheetBackdrop.addEventListener('click', (e) => {
      if (e.target === dom.sheetBackdrop) closeSheet();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeModal();
        closeSheet();
        return;
      }
      if (state.view === 'workspace' && state.session && !state.session.submitted) {
        const s = state.session;
        if (s.viewLayout === 'focus') {
          if (e.key === 'ArrowRight') {
            if (s.focusIndex < s.questions.length - 1) {
              s.focusIndex += 1;
              renderWorkspace();
            }
          } else if (e.key === 'ArrowLeft') {
            if (s.focusIndex > 0) {
              s.focusIndex -= 1;
              renderWorkspace();
            }
          }
        }
      }
    });

    window.addEventListener('beforeunload', (e) => {
      if (state.view === 'workspace' && state.session && state.session.mode === 'exam' && !state.session.submitted) {
        e.preventDefault();
        e.returnValue = '';
      }
    });

    render();
  }

  init();
})();
