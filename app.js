/* ==========================================================================
   Sử 12 (KNTT) — Bài 6: Cách Mạng Tháng Tám 1945 — Interactive Study App
   Zero external dependencies • Works 100% offline via file:///
   ========================================================================== */
(function () {
  'use strict';

  const DB = window.SU12_B6;
  if (!DB) {
    document.getElementById('mainContent').innerHTML =
      '<div class="container"><div class="card" style="padding:24px;">Không tải được dữ liệu <code>data.js</code>. Vui lòng kiểm tra lại thư mục.</div></div>';
    return;
  }

  const LETTERS = ['A', 'B', 'C', 'D'];
  const STORAGE_KEY = 'su12_bai6_kntt_v1';
  const CAT_MAP = Object.fromEntries(DB.categories.map((c) => [c.id, c]));
  const MC_MAP = Object.fromEntries(DB.mc.map((q) => [q.id, q]));
  const TF_MAP = Object.fromEntries(DB.tf.map((t) => [t.id, t]));

  // Normalized combined bank (52 MC + 8 TF = 60 items)
  const ALL_ITEMS = [
    ...DB.mc.map((q, i) => ({ ...q, kind: 'mc', bankNum: i + 1 })),
    ...DB.tf.map((t, i) => ({ ...t, kind: 'tf', bankNum: i + 1 })),
  ];

  // =========================================================================
  // Persistent User State
  // =========================================================================
  function loadStore() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) throw new Error('empty');
      const parsed = JSON.parse(raw);
      return {
        theme: parsed.theme || 'light',
        mastered: parsed.mastered || {},
        wrong: parsed.wrong || {},
        fcMastered: parsed.fcMastered || {},
        history: Array.isArray(parsed.history) ? parsed.history : [],
        bestMatchSec: typeof parsed.bestMatchSec === 'number' ? parsed.bestMatchSec : null,
      };
    } catch (_) {
      return {
        theme: 'light',
        mastered: {},
        wrong: {},
        fcMastered: {},
        history: [],
        bestMatchSec: null,
      };
    }
  }

  const store = loadStore();
  function saveStore() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch (_) {}
  }

  // =========================================================================
  // Runtime UI State
  // =========================================================================
  const ui = {
    tab: 'exam', // 'exam' | 'practice' | 'games' | 'theory' | 'stats'
    shuffleExam: false,

    // Active exam session
    examSession: null, // { examId, name, code, mcItems[], tfItems[], answersMc:{}, answersTf:{}, flags:{}, remainingSec, totalSec, paused, submitted, reviewFilter:'all', timerId }

    // Practice state
    practice: {
      cat: 'all',
      kind: 'all', // 'all' | 'mc' | 'tf'
      onlyTrap: false,
      onlyWrong: false,
      query: '',
      mode: 'focus', // 'focus' | 'list'
      order: ALL_ITEMS.map((it) => it.id),
      focusIdx: 0,
      answersMc: {}, // qid -> chosen index
      answersTf: {}, // tid -> { a:bool, ... }
      checkedTf: {}, // tid -> true
    },

    // Games state
    games: {
      sub: 'flashcard', // 'flashcard' | 'match' | 'chrono'
      fcCat: 'all',
      fcOrder: DB.flashcards.map((f) => f.id),
      fcIdx: 0,
      fcFlipped: false,

      // Match game
      matchRound: 0,
      matchPairs: [],
      matchLeft: [],
      matchRight: [],
      matchSelLeft: null,
      matchSelRight: null,
      matchMatchedIds: {},
      matchWrongPair: null,
      matchMistakes: 0,
      matchElapsed: 0,
      matchTimerId: null,
      matchDone: false,

      // Chrono sort
      chronoItems: [], // 5 timeline items with correctRank
      chronoPool: [],
      chronoPicked: [],
      chronoChecked: false,
    },

    // Theory state
    theory: {
      activeTlIdx: 4, // Default highlight 15/8
      hideTraps: false,
      revealedTraps: {},
    },
  };

  // =========================================================================
  // Helpers
  // =========================================================================
  function esc(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function shuffleArr(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function normText(s) {
    return String(s)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd');
  }

  function formatTime(sec) {
    const s = Math.max(0, Math.floor(sec));
    const m = Math.floor(s / 60);
    const r = s % 60;
    return `${String(m).padStart(2, '0')}:${String(r).padStart(2, '0')}`;
  }

  function tfScoreFromRight(rightCount) {
    // Chuẩn tỷ lệ Bộ GD&ĐT trên thang 2.0 điểm/câu:
    // 1 ý = 10% (0.2), 2 ý = 25% (0.5), 3 ý = 50% (1.0), 4 ý = 100% (2.0)
    return [0, 0.2, 0.5, 1.0, 2.0][rightCount] || 0;
  }

  function toast(msg) {
    const box = document.getElementById('toastContainer');
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = msg;
    box.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.25s ease';
      setTimeout(() => el.remove(), 260);
    }, 2400);
  }

  function openModal(title, bodyHtml, buttons) {
    const backdrop = document.getElementById('modalBackdrop');
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalBody').innerHTML = bodyHtml;
    const foot = document.getElementById('modalFooter');
    foot.innerHTML = '';
    buttons.forEach((b) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `btn ${b.cls || ''}`;
      btn.textContent = b.label;
      btn.addEventListener('click', () => {
        closeModal();
        if (b.onClick) b.onClick();
      });
      foot.appendChild(btn);
    });
    backdrop.hidden = false;
  }

  function closeModal() {
    document.getElementById('modalBackdrop').hidden = true;
  }

  function stopAllTimers() {
    if (ui.examSession && ui.examSession.timerId) {
      clearInterval(ui.examSession.timerId);
      ui.examSession.timerId = null;
    }
    if (ui.games.matchTimerId) {
      clearInterval(ui.games.matchTimerId);
      ui.games.matchTimerId = null;
    }
  }

  // =========================================================================
  // Theme & Global Navigation
  // =========================================================================
  function applyTheme() {
    document.documentElement.setAttribute('data-theme', store.theme);
  }

  function setTab(nextTab) {
    if (ui.examSession && !ui.examSession.submitted && nextTab !== 'exam') {
      openModal(
        'Đang làm bài thi thử 15 phút',
        '<p>Bạn đang làm dở <strong>' + esc(ui.examSession.name) + '</strong>. Nếu rời sang mục khác, đồng hồ sẽ tạm dừng và bài thi vẫn được giữ lại để bạn quay về làm tiếp.</p>',
        [
          { label: 'Ở lại làm tiếp', cls: 'btn-primary' },
          {
            label: 'Tạm dừng & chuyển mục',
            onClick: () => {
              ui.examSession.paused = true;
              if (ui.examSession.timerId) {
                clearInterval(ui.examSession.timerId);
                ui.examSession.timerId = null;
              }
              ui.tab = nextTab;
              syncNavAndRender();
            },
          },
        ]
      );
      return;
    }
    if (ui.games.matchTimerId && nextTab !== 'games') {
      clearInterval(ui.games.matchTimerId);
      ui.games.matchTimerId = null;
    }
    ui.tab = nextTab;
    syncNavAndRender();
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  function syncNavAndRender() {
    document.querySelectorAll('.nav-tab').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.tab === ui.tab);
    });
    document.getElementById('navCountPractice').textContent = String(ALL_ITEMS.length);
    render();
  }

  // =========================================================================
  // EXAM LOGIC
  // =========================================================================
  function prepareMcItem(q, doShuffle) {
    if (!doShuffle) {
      return { ...q, options: q.options.slice(), answer: q.answer };
    }
    const pairs = q.options.map((text, idx) => ({ text, isAns: idx === q.answer }));
    const sh = shuffleArr(pairs);
    return {
      ...q,
      options: sh.map((p) => p.text),
      answer: sh.findIndex((p) => p.isAns),
    };
  }

  function startCuratedExam(examId) {
    stopAllTimers();
    const ex = DB.exams.find((e) => e.id === examId);
    if (!ex) return;
    const doShuf = ui.shuffleExam;
    let mcList = ex.mc_ids.map((id) => prepareMcItem(MC_MAP[id], doShuf));
    let tfList = ex.tf_ids.map((id) => ({ ...TF_MAP[id] }));
    if (doShuf) {
      mcList = shuffleArr(mcList);
      tfList = shuffleArr(tfList);
    }
    launchExamSession({
      examId: ex.id,
      code: ex.code,
      name: ex.name,
      durationSec: ex.duration_min * 60,
      mcItems: mcList,
      tfItems: tfList,
    });
  }

  function startRandomExam() {
    stopAllTimers();
    // Pick balanced 3 questions per category (4 * 3 = 12 MC) + 2 random TF
    const pickedMc = [];
    DB.categories.forEach((cat) => {
      const pool = shuffleArr(DB.mc.filter((q) => q.cat === cat.id));
      pickedMc.push(...pool.slice(0, 3));
    });
    const mcList = shuffleArr(pickedMc).map((q) => prepareMcItem(q, true));
    const tfList = shuffleArr(DB.tf).slice(0, 2).map((t) => ({ ...t }));
    launchExamSession({
      examId: 'random-' + Date.now(),
      code: 'ĐỀ NGẪU NHIÊN',
      name: 'Đề Ngẫu Nhiên 15 Phút (Cân bằng 4 mảng)',
      durationSec: 15 * 60,
      mcItems: mcList,
      tfItems: tfList,
    });
  }

  function launchExamSession({ examId, code, name, durationSec, mcItems, tfItems }) {
    ui.examSession = {
      examId,
      code,
      name,
      mcItems,
      tfItems,
      answersMc: {},
      answersTf: {},
      flags: {},
      totalSec: durationSec,
      remainingSec: durationSec,
      paused: false,
      submitted: false,
      reviewFilter: 'all',
      result: null,
      timerId: null,
    };
    ui.tab = 'exam';
    startExamTimer();
    syncNavAndRender();
    window.scrollTo({ top: 0, behavior: 'instant' });
  }

  function startExamTimer() {
    const ses = ui.examSession;
    if (!ses || ses.submitted || ses.paused) return;
    if (ses.timerId) clearInterval(ses.timerId);
    ses.timerId = setInterval(() => {
      if (!ui.examSession || ui.examSession.submitted || ui.examSession.paused) return;
      ui.examSession.remainingSec -= 1;
      const el = document.getElementById('examTimerDisplay');
      if (el) {
        el.textContent = formatTime(ui.examSession.remainingSec);
        const pill = document.getElementById('examTimerPill');
        if (pill) {
          pill.classList.toggle('warn', ui.examSession.remainingSec <= 180 && ui.examSession.remainingSec > 60);
          pill.classList.toggle('danger', ui.examSession.remainingSec <= 60);
        }
      }
      if (ui.examSession.remainingSec <= 0) {
        clearInterval(ui.examSession.timerId);
        ui.examSession.timerId = null;
        toast('Hết 15 phút! Hệ thống tự động nộp bài và chấm điểm.');
        finalizeExam();
      }
    }, 1000);
  }

  function countExamAnswered(ses) {
    let mcDone = 0;
    ses.mcItems.forEach((q) => {
      if (typeof ses.answersMc[q.id] === 'number') mcDone++;
    });
    let tfDone = 0;
    ses.tfItems.forEach((t) => {
      const ans = ses.answersTf[t.id] || {};
      if (t.statements.every((s) => typeof ans[s.key] === 'boolean')) tfDone++;
    });
    return { mcDone, tfDone, totalDone: mcDone + tfDone, total: ses.mcItems.length + ses.tfItems.length };
  }

  function requestSubmitExam() {
    const ses = ui.examSession;
    if (!ses || ses.submitted) return;
    const prog = countExamAnswered(ses);
    const missing = prog.total - prog.totalDone;
    const msg =
      missing > 0
        ? `<p>Bạn còn <strong>${missing} câu chưa làm đủ</strong> (đã xong ${prog.totalDone}/${prog.total} câu). Bạn vẫn muốn nộp bài ngay chứ?</p>`
        : `<p>Bạn đã hoàn thành đủ <strong>${prog.total}/${prog.total} câu</strong>! Xác nhận nộp bài để chấm điểm chuẩn Bộ GD&amp;ĐT?</p>`;
    openModal('Xác nhận nộp bài', msg, [
      { label: 'Kiểm tra lại', cls: '' },
      { label: 'Nộp bài & Chấm điểm', cls: 'btn-primary', onClick: () => finalizeExam() },
    ]);
  }

  function finalizeExam() {
    const ses = ui.examSession;
    if (!ses || ses.submitted) return;
    if (ses.timerId) {
      clearInterval(ses.timerId);
      ses.timerId = null;
    }
    ses.submitted = true;
    ses.paused = false;

    let mcRight = 0;
    const wrongIds = [];
    const catStats = {};
    DB.categories.forEach((c) => {
      catStats[c.id] = { right: 0, total: 0 };
    });

    ses.mcItems.forEach((q) => {
      catStats[q.cat].total += 1;
      const picked = ses.answersMc[q.id];
      if (picked === q.answer) {
        mcRight++;
        catStats[q.cat].right += 1;
        store.mastered[q.id] = true;
        delete store.wrong[q.id];
      } else {
        wrongIds.push(q.id);
        store.wrong[q.id] = true;
      }
    });

    let tfScore = 0;
    let tfRightItems = 0;
    ses.tfItems.forEach((t) => {
      const ans = ses.answersTf[t.id] || {};
      let subRight = 0;
      t.statements.forEach((s) => {
        catStats[t.cat].total += 1;
        if (ans[s.key] === s.answer) {
          subRight++;
          tfRightItems++;
          catStats[t.cat].right += 1;
        }
      });
      tfScore += tfScoreFromRight(subRight);
      if (subRight === 4) {
        store.mastered[t.id] = true;
        delete store.wrong[t.id];
      } else {
        wrongIds.push(t.id);
        store.wrong[t.id] = true;
      }
    });

    const mcScore = mcRight * 0.5;
    const totalScore = Math.round((mcScore + tfScore) * 100) / 100;
    const elapsedSec = ses.totalSec - Math.max(0, ses.remainingSec);

    ses.result = {
      mcRight,
      mcScore,
      tfRightItems,
      tfTotalItems: ses.tfItems.length * 4,
      tfScore: Math.round(tfScore * 100) / 100,
      totalScore,
      elapsedSec,
      wrongIds,
      catStats,
    };

    const now = new Date();
    const dateStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')} • ${now.getDate()}/${now.getMonth() + 1}`;
    store.history.unshift({
      examId: ses.examId,
      code: ses.code,
      name: ses.name,
      score: totalScore,
      mcRight,
      tfRightItems,
      elapsedSec,
      dateStr,
    });
    if (store.history.length > 30) store.history.length = 30;
    saveStore();
    render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function drillWrongIds(ids) {
    if (!ids.length) {
      toast('Tuyệt vời! Bạn không có câu sai nào để làm lại.');
      return;
    }
    ids.forEach((id) => {
      store.wrong[id] = true;
      delete ui.practice.answersMc[id];
      delete ui.practice.answersTf[id];
      delete ui.practice.checkedTf[id];
    });
    saveStore();
    ui.examSession = null;
    ui.practice.cat = 'all';
    ui.practice.kind = 'all';
    ui.practice.onlyTrap = false;
    ui.practice.onlyWrong = true;
    ui.practice.query = '';
    ui.practice.mode = 'focus';
    ui.practice.focusIdx = 0;
    ui.tab = 'practice';
    syncNavAndRender();
    toast(`Đã lọc ${ids.length} câu cần làm lại!`);
  }

  // =========================================================================
  // RENDER: TAB 1 — EXAM HUB / ACTIVE EXAM / RESULT
  // =========================================================================
  function renderExamTab() {
    if (!ui.examSession) return renderExamHub();
    return renderActiveExam(ui.examSession);
  }

  function renderExamHub() {
    const masteredCount = Object.keys(store.mastered).length;
    const wrongCount = Object.keys(store.wrong).length;
    const bestScore = store.history.length ? Math.max(...store.history.map((h) => h.score)) : null;

    const examCards = DB.exams
      .map((ex) => {
        const past = store.history.filter((h) => h.examId === ex.id);
        const best = past.length ? Math.max(...past.map((h) => h.score)) : null;
        return `
          <article class="card exam-card">
            <div>
              <div class="exam-card-top">
                <span class="badge badge-red">${esc(ex.code)}</span>
                <span class="badge ${ex.badge.includes('PDF') ? 'badge-gold' : 'badge-info'}">${esc(ex.badge)}</span>
              </div>
              <h3 class="exam-card-title">${esc(ex.name)}</h3>
              <p class="exam-card-desc">${esc(ex.subtitle)}</p>
            </div>
            <div>
              <div class="exam-meta-row" style="margin-bottom:12px;">
                <span class="exam-meta-pill">⏱ 15 phút</span>
                <span class="exam-meta-pill">12 Trắc nghiệm (6đ)</span>
                <span class="exam-meta-pill">2 Đúng/Sai (4đ)</span>
              </div>
              <div class="exam-card-foot">
                <span class="exam-best">${best !== null ? `Cao nhất: <strong>${best.toFixed(1)}/10</strong> (${past.length} lần)` : 'Chưa thi thử'}</span>
                <button class="btn btn-primary btn-sm" data-start-exam="${ex.id}" type="button">Bắt đầu thi →</button>
              </div>
            </div>
          </article>
        `;
      })
      .join('');

    const recentHtml = store.history.length
      ? `
        <div class="card" style="padding:18px 20px; margin-top:20px;">
          <div class="section-header-row" style="margin-bottom:10px;">
            <div>
              <h3 class="section-title" style="font-size:16px;">Lịch sử làm đề gần đây</h3>
            </div>
            <button class="btn btn-sm" id="goStatsBtn" type="button">Xem phân tích chi tiết →</button>
          </div>
          <div style="overflow-x:auto;">
            <table class="history-table">
              <thead><tr><th>Đề thi</th><th>Điểm</th><th>Phần I (TN)</th><th>Phần II (Đ/S)</th><th>Thời gian</th><th>Lúc</th></tr></thead>
              <tbody>
                ${store.history
                  .slice(0, 5)
                  .map(
                    (h) => `
                  <tr>
                    <td><strong>${esc(h.code)}</strong> — ${esc(h.name)}</td>
                    <td><span class="badge ${h.score >= 8.5 ? 'badge-green' : h.score >= 6.5 ? 'badge-gold' : 'badge-red'}">${h.score.toFixed(2)} / 10</span></td>
                    <td>${h.mcRight}/12 câu</td>
                    <td>${h.tfRightItems}/8 ý</td>
                    <td>${formatTime(h.elapsedSec)}</td>
                    <td style="color:var(--text-muted)">${esc(h.dateStr)}</td>
                  </tr>
                `
                  )
                  .join('')}
              </tbody>
            </table>
          </div>
        </div>
      `
      : '';

    return `
      <div class="container">
        <section class="hero-banner">
          <div>
            <div class="hero-kicker">LỊCH SỬ 12 • KẾT NỐI TRI THỨC • CHỦ ĐỀ 3</div>
            <h1 class="hero-title">Bài 6: Cách Mạng Tháng Tám Năm 1945</h1>
            <p class="hero-desc">Trọn bộ ôn kiểm tra 15 phút chuẩn form Bộ GD&amp;ĐT (12 Trắc nghiệm + 2 Đúng/Sai). Làm đề bấm giờ thực chiến, luyện kho 60 câu giải thích siêu kỹ, lật Flashcard &amp; cày game mốc thời gian!</p>
            <div class="hero-cta-row">
              <button class="hero-btn-white" id="heroQuickExam" type="button">⚡ Làm ngay Đề 01 (15 phút)</button>
              <button class="hero-btn-ghost" id="heroQuickTheory" type="button">📖 Đọc 10 Bẫy Kinh Điển</button>
              ${wrongCount > 0 ? `<button class="hero-btn-ghost" id="heroDrillWrong" type="button">❌ Xử lại ${wrongCount} câu sai</button>` : ''}
            </div>
          </div>
          <div class="hero-stats-grid">
            <div class="hero-stat">
              <div class="hero-stat-val">${bestScore !== null ? bestScore.toFixed(1) : '—'}<span style="font-size:13px;font-weight:600;opacity:0.8"> /10</span></div>
              <div class="hero-stat-lbl">Điểm 15 phút cao nhất</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${masteredCount}<span style="font-size:13px;font-weight:600;opacity:0.8"> /${ALL_ITEMS.length}</span></div>
              <div class="hero-stat-lbl">Câu đã nắm chắc</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${Object.keys(store.fcMastered).length}<span style="font-size:13px;font-weight:600;opacity:0.8"> /${DB.flashcards.length}</span></div>
              <div class="hero-stat-lbl">Flashcard đã thuộc</div>
            </div>
            <div class="hero-stat">
              <div class="hero-stat-val">${wrongCount}</div>
              <div class="hero-stat-lbl">Câu từng sai cần ôn</div>
            </div>
          </div>
        </section>

        <div class="section-header-row">
          <div>
            <h2 class="section-title">Chọn Đề Thi Thử 15 Phút</h2>
            <p class="section-sub">Đề 01 &amp; Đề 02 trùng khớp 100% với file PDF để bạn vừa in giấy vừa chấm tự động trên máy.</p>
          </div>
          <label class="toggle-label">
            <input type="checkbox" id="shuffleExamToggle" ${ui.shuffleExam ? 'checked' : ''} />
            <span>Trộn câu &amp; đảo đáp án A–D</span>
          </label>
        </div>

        <div class="exam-grid">
          ${examCards}
          <article class="card exam-card" style="background:linear-gradient(155deg, var(--surface) 0%, var(--gold-soft) 100%); border-color:var(--gold-border);">
            <div>
              <div class="exam-card-top">
                <span class="badge badge-gold">ĐỀ NGẪU NHIÊN</span>
                <span class="badge badge-green">Vô hạn đề mới</span>
              </div>
              <h3 class="exam-card-title">Đề Trộn Ngẫu Nhiên 15 Phút</h3>
              <p class="exam-card-desc">Tự động rút 12 câu Trắc nghiệm cân bằng đều 4 mảng kiến thức + 2 câu Đúng/Sai từ kho 60 câu, tự đảo đáp án A–D chống học vẹt.</p>
            </div>
            <div>
              <div class="exam-meta-row" style="margin-bottom:12px;">
                <span class="exam-meta-pill">⏱ 15 phút</span>
                <span class="exam-meta-pill">3 câu/chủ đề</span>
                <span class="exam-meta-pill">Đảo A–D tự động</span>
              </div>
              <div class="exam-card-foot">
                <span class="exam-best">Luyện phản xạ thật trước giờ thi</span>
                <button class="btn btn-gold btn-sm" id="startRandomExamBtn" type="button">Tạo đề mới →</button>
              </div>
            </div>
          </article>
        </div>

        ${recentHtml}
      </div>
    `;
  }

  function renderActiveExam(ses) {
    const prog = countExamAnswered(ses);
    const isSub = ses.submitted;
    const timerCls = ses.remainingSec <= 60 ? 'danger' : ses.remainingSec <= 180 ? 'warn' : '';

    // Result Banner if submitted
    let resultBannerHtml = '';
    if (isSub && ses.result) {
      const r = ses.result;
      const pct = Math.min(100, Math.round((r.totalScore / 10) * 100));
      let verdict = 'Cần ôn thêm lý thuyết & 10 bẫy kinh điển nhé!';
      if (r.totalScore >= 9.5) verdict = 'Đỉnh nóc kịch trần! Mai vào lớp auto 10 điểm!';
      else if (r.totalScore >= 8.5) verdict = 'Quá chắc tay rồi! Soi kỹ lại 1–2 câu sai là trọn vẹn 10/10!';
      else if (r.totalScore >= 7.0) verdict = 'Khá ổn rồi đó! Xem kỹ giải thích câu bẫy để bật lên 9–10 điểm!';

      const catBarsHtml = DB.categories
        .map((c) => {
          const st = r.catStats[c.id];
          const p = st.total ? Math.round((st.right / st.total) * 100) : 0;
          return `
            <div>
              <div class="cat-bar-top">
                <span>${esc(c.short)}</span>
                <span style="color:${p >= 80 ? 'var(--success)' : p >= 50 ? 'var(--gold)' : 'var(--danger)'}">${st.right}/${st.total} (${p}%)</span>
              </div>
              <div class="bar-track"><div class="bar-fill" style="width:${p}%; background:${c.color}"></div></div>
            </div>
          `;
        })
        .join('');

      resultBannerHtml = `
        <div class="card result-hero">
          <div class="score-circle" style="--pct:${pct}">
            <div class="score-circle-inner">
              <div class="score-num">${r.totalScore.toFixed(2).replace(/\.00$/, '.0')}</div>
              <div class="score-max">trên 10 điểm</div>
            </div>
          </div>
          <div style="width:100%">
            <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px;">
              <span class="badge badge-green">ĐÃ CHẤM ĐIỂM CHUẨN BỘ GD&amp;ĐT</span>
              <span class="badge badge-neutral">Thời gian làm: ${formatTime(r.elapsedSec)}</span>
            </div>
            <h2 style="margin:0 0 4px 0;font-size:20px;">${esc(verdict)}</h2>
            <div class="result-breakdown">
              <div class="rb-box"><div class="rb-val">${r.mcRight} / 12 câu</div><div class="rb-lbl">Phần I • +${r.mcScore.toFixed(1)} điểm</div></div>
              <div class="rb-box"><div class="rb-val">${r.tfRightItems} / ${r.tfTotalItems} ý</div><div class="rb-lbl">Phần II • +${r.tfScore.toFixed(1)} điểm</div></div>
              <div class="rb-box"><div class="rb-val" style="color:${r.wrongIds.length ? 'var(--danger)' : 'var(--success)'}">${r.wrongIds.length} câu</div><div class="rb-lbl">Câu sai / chưa trọn điểm</div></div>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:8px;">
              ${r.wrongIds.length > 0 ? `<button class="btn btn-soft-danger btn-sm" id="drillExamWrongBtn" type="button">🔥 Làm lại ${r.wrongIds.length} câu sai ngay</button>` : ''}
              <button class="btn btn-primary btn-sm" id="retakeExamBtn" type="button">↻ Thi lại đề này</button>
              <button class="btn btn-sm" id="exitExamBtn" type="button">← Chọn đề khác</button>
              <button class="btn btn-sm" id="toggleReviewWrongBtn" type="button">${ses.reviewFilter === 'wrong' ? 'Hiện tất cả 14 câu' : 'Chỉ lọc các câu sai'}</button>
            </div>
            <div class="cat-bars">${catBarsHtml}</div>
          </div>
        </div>
      `;
    }

    // Build MC cards
    const mcCardsHtml = ses.mcItems
      .map((q, idx) => {
        const picked = ses.answersMc[q.id];
        const isCorrect = isSub && picked === q.answer;
        if (isSub && ses.reviewFilter === 'wrong' && isCorrect) return '';
        const cat = CAT_MAP[q.cat];
        const optsHtml = q.options
          .map((opt, oi) => {
            let cls = '';
            if (!isSub && picked === oi) cls = 'selected';
            else if (isSub) {
              if (oi === q.answer) cls = 'correct';
              else if (picked === oi && oi !== q.answer) cls = 'wrong';
            }
            return `
              <button class="opt-btn ${cls}" type="button" data-exam-mc="${q.id}" data-opt="${oi}" ${isSub ? 'disabled' : ''}>
                <span class="opt-key">${LETTERS[oi]}</span>
                <span>${esc(opt)}</span>
              </button>
            `;
          })
          .join('');

        const expHtml = isSub
          ? `
            <div class="exp-box ${isCorrect ? '' : 'is-wrong'}">
              <div class="exp-title ${isCorrect ? 'ok' : 'bad'}">
                ${isCorrect ? '✓ Chính xác! (+0,5 điểm)' : picked === undefined ? `✗ Bạn bỏ trống — Đáp án đúng là ${LETTERS[q.answer]}` : `✗ Chưa đúng (bạn chọn ${LETTERS[picked]}) — Đáp án đúng là ${LETTERS[q.answer]}`}
              </div>
              <div>${esc(q.explanation)}</div>
              <div class="exp-tip">💡 Mẹo nhớ nhanh: ${esc(q.tip)}</div>
            </div>
          `
          : '';

        return `
          <article class="card q-card" id="ex-mc-${idx + 1}">
            <div class="q-card-head">
              <div class="q-badges">
                <span class="badge badge-red">Câu ${idx + 1}</span>
                <span class="badge badge-neutral">${esc(cat.short)}</span>
                ${isSub && q.trap ? '<span class="badge badge-gold">⚠ Câu bẫy</span>' : ''}
              </div>
              ${!isSub ? `<button class="flag-btn ${ses.flags[q.id] ? 'active' : ''}" data-flag="${q.id}" type="button">${ses.flags[q.id] ? '⚑ Đã đánh dấu' : '⚐ Đánh dấu'}</button>` : ''}
            </div>
            <p class="q-stem">${esc(q.question)}</p>
            <div class="options-list">${optsHtml}</div>
            ${expHtml}
          </article>
        `;
      })
      .join('');

    // Build TF cards
    const tfCardsHtml = ses.tfItems
      .map((t, idx) => {
        const ans = ses.answersTf[t.id] || {};
        const subRight = t.statements.filter((s) => ans[s.key] === s.answer).length;
        if (isSub && ses.reviewFilter === 'wrong' && subRight === 4) return '';
        const pts = tfScoreFromRight(subRight);

        const stmtsHtml = t.statements
          .map((s) => {
            const val = ans[s.key];
            const ok = isSub && val === s.answer;
            const bad = isSub && val !== s.answer;
            return `
              <div class="tf-row ${ok ? 'ok' : bad ? 'bad' : ''}">
                <div class="tf-row-main">
                  <div class="tf-stmt"><strong>${s.key})</strong> ${esc(s.text)}</div>
                  <div class="tf-toggles">
                    <button class="tf-pill ${!isSub && val === true ? 'picked-true' : ''} ${isSub && s.answer === true ? 'reveal-ok' : isSub && val === true && !s.answer ? 'reveal-bad' : ''}"
                            type="button" data-exam-tf="${t.id}" data-key="${s.key}" data-val="true" ${isSub ? 'disabled' : ''}>Đúng</button>
                    <button class="tf-pill ${!isSub && val === false ? 'picked-false' : ''} ${isSub && s.answer === false ? 'reveal-ok' : isSub && val === false && s.answer ? 'reveal-bad' : ''}"
                            type="button" data-exam-tf="${t.id}" data-key="${s.key}" data-val="false" ${isSub ? 'disabled' : ''}>Sai</button>
                  </div>
                </div>
                ${isSub ? `<div class="tf-row-exp"><strong>${ok ? '✓ Đúng' : '✗ Sai'} (Đáp án: ${s.answer ? 'ĐÚNG' : 'SAI'}):</strong> ${esc(s.explanation)}</div>` : ''}
              </div>
            `;
          })
          .join('');

        return `
          <article class="card q-card" id="ex-tf-${idx + 1}">
            <div class="q-card-head">
              <div class="q-badges">
                <span class="badge badge-info">Phần II • Câu ${idx + 1}</span>
                <span class="badge badge-neutral">${esc(t.title)}</span>
                ${isSub ? `<span class="badge ${subRight === 4 ? 'badge-green' : 'badge-gold'}">Đúng ${subRight}/4 ý (+${pts.toFixed(1)}đ)</span>` : ''}
              </div>
              ${!isSub ? `<button class="flag-btn ${ses.flags[t.id] ? 'active' : ''}" data-flag="${t.id}" type="button">${ses.flags[t.id] ? '⚑ Đã đánh dấu' : '⚐ Đánh dấu'}</button>` : ''}
            </div>
            <p class="q-stem">Đọc đoạn tư liệu sau và chọn <strong>Đúng</strong> hoặc <strong>Sai</strong> cho từng nhận định a), b), c), d):</p>
            <div class="passage-box">
              <div>${esc(t.passage)}</div>
              <div class="passage-src">(${esc(t.source)})</div>
            </div>
            <div class="tf-list">${stmtsHtml}</div>
          </article>
        `;
      })
      .join('');

    // Palette buttons
    const mcPal = ses.mcItems
      .map((q, idx) => {
        const picked = ses.answersMc[q.id];
        let cls = '';
        if (isSub) cls = picked === q.answer ? 'correct' : 'wrong';
        else if (typeof picked === 'number') cls = 'answered';
        if (!isSub && ses.flags[q.id]) cls += ' flagged';
        return `<button class="pal-btn ${cls}" type="button" data-jump="ex-mc-${idx + 1}">${idx + 1}</button>`;
      })
      .join('');

    const tfPal = ses.tfItems
      .map((t, idx) => {
        const ans = ses.answersTf[t.id] || {};
        const cnt = Object.keys(ans).length;
        const subRight = t.statements.filter((s) => ans[s.key] === s.answer).length;
        let cls = '';
        if (isSub) cls = subRight === 4 ? 'correct' : subRight > 0 ? 'partial' : 'wrong';
        else if (cnt === 4) cls = 'answered';
        else if (cnt > 0) cls = 'partial';
        if (!isSub && ses.flags[t.id]) cls += ' flagged';
        return `<button class="pal-btn ${cls}" type="button" data-jump="ex-tf-${idx + 1}">ĐS${idx + 1}</button>`;
      })
      .join('');

    return `
      <div class="container">
        <div class="exam-sticky-bar">
          <div class="exam-bar-left">
            <span class="badge badge-red">${esc(ses.code)}</span>
            <span class="exam-bar-title">${esc(ses.name)}</span>
            <span class="exam-progress-pill">${isSub ? 'Đã nộp bài' : `Đã làm ${prog.totalDone}/${prog.total} câu`}</span>
          </div>
          <div class="exam-bar-right">
            ${
              !isSub
                ? `
              <div class="timer-pill ${timerCls}" id="examTimerPill">
                <span>⏱</span>
                <span id="examTimerDisplay">${formatTime(ses.remainingSec)}</span>
              </div>
              <button class="btn btn-sm" id="pauseExamBtn" type="button">${ses.paused ? '▶ Tiếp tục' : '⏸ Tạm dừng'}</button>
              <button class="btn btn-primary btn-sm" id="submitExamBtn" type="button">Nộp bài</button>
              <button class="btn btn-sm" id="cancelExamBtn" type="button" title="Thoát đề thi">✕</button>
            `
                : `
              <button class="btn btn-sm" id="exitExamBtnTop" type="button">← Về danh sách đề</button>
            `
            }
          </div>
        </div>

        ${resultBannerHtml}

        <div class="exam-workspace">
          <div>
            <div class="part-divider">
              <h3>PHẦN I. TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (6,0 điểm)</h3>
              <p>12 câu × 0,5 điểm/câu — Chọn một phương án đúng nhất cho mỗi câu hỏi.</p>
            </div>
            ${mcCardsHtml || '<div class="card" style="padding:18px;margin-bottom:14px;color:var(--success);font-weight:700;">🎉 Không có câu sai nào ở Phần I!</div>'}

            <div class="part-divider" style="margin-top:20px;">
              <h3>PHẦN II. TRẮC NGHIỆM ĐÚNG / SAI (4,0 điểm)</h3>
              <p>2 câu × 2,0 điểm/câu — Thang điểm chuẩn Bộ GD&amp;ĐT: 1 ý 0,2đ • 2 ý 0,5đ • 3 ý 1,0đ • 4 ý 2,0đ.</p>
            </div>
            ${tfCardsHtml || '<div class="card" style="padding:18px;margin-bottom:14px;color:var(--success);font-weight:700;">🎉 Đạt trọn 4/4 điểm Phần II!</div>'}
          </div>

          <aside class="card exam-sidebar">
            <div class="palette-title">
              <span>Bảng câu hỏi</span>
              <span style="font-size:12px;color:var(--text-muted)">${prog.totalDone}/${prog.total}</span>
            </div>
            <div style="font-size:11.5px;font-weight:700;color:var(--text-muted);margin-bottom:6px;">Phần I • Trắc nghiệm</div>
            <div class="palette-grid">${mcPal}</div>
            <div style="font-size:11.5px;font-weight:700;color:var(--text-muted);margin-bottom:6px;">Phần II • Đúng / Sai</div>
            <div class="palette-grid" style="grid-template-columns:repeat(2,1fr);">${tfPal}</div>
            <div class="palette-legend">
              ${
                !isSub
                  ? `
                <span><i class="leg-dot" style="background:var(--primary)"></i>Đã làm</span>
                <span><i class="leg-dot" style="background:var(--surface-alt);border:1px solid var(--border-strong)"></i>Chưa làm</span>
                <span><i class="leg-dot" style="background:#f59e0b;border-radius:50%"></i>Đánh dấu</span>
              `
                  : `
                <span><i class="leg-dot" style="background:var(--success)"></i>Đúng trọn</span>
                <span><i class="leg-dot" style="background:var(--danger)"></i>Sai</span>
              `
              }
            </div>
            ${!isSub ? `<button class="btn btn-primary" id="submitExamSideBtn" type="button" style="width:100%;margin-top:12px;">Nộp bài ngay</button>` : ''}
          </aside>
        </div>
      </div>
    `;
  }

  // =========================================================================
  // RENDER: TAB 2 — PRACTICE & FULL 60-QUESTION BANK
  // =========================================================================
  function getFilteredPracticeItems() {
    const p = ui.practice;
    const qNorm = normText(p.query.trim());
    const mapById = Object.fromEntries(ALL_ITEMS.map((it) => [it.id, it]));
    const ordered = p.order.map((id) => mapById[id]).filter(Boolean);
    return ordered.filter((it) => {
      if (p.cat !== 'all' && it.cat !== p.cat) return false;
      if (p.kind !== 'all' && it.kind !== p.kind) return false;
      if (p.onlyTrap && !(it.kind === 'mc' && it.trap)) return false;
      if (p.onlyWrong && !store.wrong[it.id] && p.answersMc[it.id] === undefined && !p.checkedTf[it.id]) return false;
      if (qNorm) {
        const hay =
          it.kind === 'mc'
            ? normText(it.question + ' ' + it.options.join(' ') + ' ' + it.explanation)
            : normText(it.title + ' ' + it.passage + ' ' + it.statements.map((s) => s.text).join(' '));
        if (!hay.includes(qNorm)) return false;
      }
      return true;
    });
  }

  function renderPracticeCard(it, displayIdx) {
    const p = ui.practice;
    const cat = CAT_MAP[it.cat];
    if (it.kind === 'mc') {
      const picked = p.answersMc[it.id];
      const answered = typeof picked === 'number';
      const isCorrect = answered && picked === it.answer;

      const optsHtml = it.options
        .map((opt, oi) => {
          let cls = '';
          if (answered) {
            if (oi === it.answer) cls = 'correct';
            else if (picked === oi) cls = 'wrong';
          }
          return `
            <button class="opt-btn ${cls}" type="button" data-prac-mc="${it.id}" data-opt="${oi}" ${answered ? 'disabled' : ''}>
              <span class="opt-key">${LETTERS[oi]}</span>
              <span>${esc(opt)}</span>
            </button>
          `;
        })
        .join('');

      return `
        <article class="card q-card">
          <div class="q-card-head">
            <div class="q-badges">
              <span class="badge badge-red">Câu ${displayIdx}</span>
              <span class="badge badge-neutral">${esc(cat.short)}</span>
              <span class="badge badge-info">${it.level === 'NB' ? 'Nhận biết' : it.level === 'TH' ? 'Thông hiểu' : 'Vận dụng'}</span>
              ${it.trap ? '<span class="badge badge-gold">⚠ Câu dễ bẫy</span>' : ''}
              ${store.wrong[it.id] ? '<span class="badge badge-red">Từng sai</span>' : store.mastered[it.id] ? '<span class="badge badge-green">✓ Đã nắm</span>' : ''}
            </div>
            ${answered ? `<button class="btn btn-sm" data-prac-reset="${it.id}" type="button">↻ Làm lại</button>` : ''}
          </div>
          <p class="q-stem">${esc(it.question)}</p>
          <div class="options-list">${optsHtml}</div>
          ${
            answered
              ? `
            <div class="exp-box ${isCorrect ? '' : 'is-wrong'}">
              <div class="exp-title ${isCorrect ? 'ok' : 'bad'}">
                ${isCorrect ? '✓ Chuẩn xác! Đáp án ' + LETTERS[it.answer] : '✗ Tiếc quá! Đáp án đúng là ' + LETTERS[it.answer]}
              </div>
              <div>${esc(it.explanation)}</div>
              <div class="exp-tip">💡 Mẹo nhớ nhanh: ${esc(it.tip)}</div>
            </div>
          `
              : ''
          }
        </article>
      `;
    } else {
      const ans = p.answersTf[it.id] || {};
      const checked = !!p.checkedTf[it.id];
      const filledCount = Object.keys(ans).length;
      const rightCount = it.statements.filter((s) => ans[s.key] === s.answer).length;

      const stmtsHtml = it.statements
        .map((s) => {
          const val = ans[s.key];
          const ok = checked && val === s.answer;
          const bad = checked && val !== s.answer;
          return `
            <div class="tf-row ${ok ? 'ok' : bad ? 'bad' : ''}">
              <div class="tf-row-main">
                <div class="tf-stmt"><strong>${s.key})</strong> ${esc(s.text)}</div>
                <div class="tf-toggles">
                  <button class="tf-pill ${!checked && val === true ? 'picked-true' : ''} ${checked && s.answer === true ? 'reveal-ok' : checked && val === true && !s.answer ? 'reveal-bad' : ''}"
                          type="button" data-prac-tf="${it.id}" data-key="${s.key}" data-val="true" ${checked ? 'disabled' : ''}>Đúng</button>
                  <button class="tf-pill ${!checked && val === false ? 'picked-false' : ''} ${checked && s.answer === false ? 'reveal-ok' : checked && val === false && s.answer ? 'reveal-bad' : ''}"
                          type="button" data-prac-tf="${it.id}" data-key="${s.key}" data-val="false" ${checked ? 'disabled' : ''}>Sai</button>
                </div>
              </div>
              ${checked ? `<div class="tf-row-exp"><strong>${ok ? '✓ Đúng' : '✗ Sai'} (Chuẩn: ${s.answer ? 'ĐÚNG' : 'SAI'}):</strong> ${esc(s.explanation)}</div>` : ''}
            </div>
          `;
        })
        .join('');

      return `
        <article class="card q-card">
          <div class="q-card-head">
            <div class="q-badges">
              <span class="badge badge-info">Đúng / Sai #${it.bankNum}</span>
              <span class="badge badge-neutral">${esc(cat.short)}</span>
              ${checked ? `<span class="badge ${rightCount === 4 ? 'badge-green' : 'badge-gold'}">Đúng ${rightCount}/4 ý (+${tfScoreFromRight(rightCount).toFixed(1)}đ)</span>` : ''}
            </div>
            <div style="display:flex;gap:6px;">
              ${!checked ? `<button class="btn btn-primary btn-sm" data-prac-check-tf="${it.id}" type="button" ${filledCount < 4 ? 'disabled' : ''}>Kiểm tra (${filledCount}/4)</button>` : `<button class="btn btn-sm" data-prac-reset-tf="${it.id}" type="button">↻ Làm lại</button>`}
            </div>
          </div>
          <p class="q-stem">${esc(it.title)} — Đọc đoạn tư liệu và chọn Đúng / Sai:</p>
          <div class="passage-box">
            <div>${esc(it.passage)}</div>
            <div class="passage-src">(${esc(it.source)})</div>
          </div>
          <div class="tf-list">${stmtsHtml}</div>
        </article>
      `;
    }
  }

  function renderPracticeTab() {
    const p = ui.practice;
    const items = getFilteredPracticeItems();
    if (p.focusIdx >= items.length) p.focusIdx = Math.max(0, items.length - 1);
    const wrongCount = Object.keys(store.wrong).length;
    const trapCount = DB.mc.filter((q) => q.trap).length;

    let bodyHtml = '';
    if (!items.length) {
      bodyHtml = `
        <div class="card" style="padding:32px;text-align:center;">
          <p style="font-size:16px;font-weight:700;margin:0 0 8px 0;">Không tìm thấy câu hỏi nào khớp bộ lọc!</p>
          <button class="btn btn-primary btn-sm" id="clearFiltersBtn" type="button">Xóa bộ lọc</button>
        </div>
      `;
    } else if (p.mode === 'focus') {
      const cur = items[p.focusIdx];
      bodyHtml = `
        <div class="focus-nav-bar">
          <button class="btn btn-sm" id="pracPrevBtn" type="button" ${p.focusIdx === 0 ? 'disabled' : ''}>← Câu trước</button>
          <span class="focus-counter">Câu ${p.focusIdx + 1} / ${items.length} <span style="font-weight:500;font-size:12.5px;color:var(--text-muted)">(Phím tắt: 1–4 chọn đáp án, ← / → chuyển câu)</span></span>
          <button class="btn btn-primary btn-sm" id="pracNextBtn" type="button" ${p.focusIdx >= items.length - 1 ? 'disabled' : ''}>Câu tiếp →</button>
        </div>
        ${renderPracticeCard(cur, p.focusIdx + 1)}
      `;
    } else {
      bodyHtml = items.map((it, i) => renderPracticeCard(it, i + 1)).join('');
    }

    return `
      <div class="container">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Luyện Tập Chấm Tức Thì &amp; Kho 60 Câu (84 ý hỏi)</h2>
            <p class="section-sub">52 câu Trắc nghiệm 4 lựa chọn + 8 câu Tư liệu Đúng/Sai (32 ý nhỏ) bám sát 100% SGK KNTT Bài 6.</p>
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">
            <button class="btn btn-sm ${p.mode === 'focus' ? 'btn-primary' : ''}" data-prac-mode="focus" type="button">Từng câu</button>
            <button class="btn btn-sm ${p.mode === 'list' ? 'btn-primary' : ''}" data-prac-mode="list" type="button">Danh sách</button>
            <button class="btn btn-sm" id="pracShuffleBtn" type="button">🔀 Trộn thứ tự</button>
          </div>
        </div>

        <div class="card filter-panel">
          <div class="filter-row">
            <button class="chip ${p.cat === 'all' ? 'active' : ''}" data-f-cat="all" type="button">Tất cả (${ALL_ITEMS.length})</button>
            ${DB.categories
              .map(
                (c) =>
                  `<button class="chip ${p.cat === c.id ? 'active' : ''}" data-f-cat="${c.id}" type="button">${esc(c.label)}</button>`
              )
              .join('')}
          </div>
          <div class="filter-row">
            <button class="chip ${p.kind === 'all' && !p.onlyTrap && !p.onlyWrong ? 'active' : ''}" data-f-kind="all" type="button">Mọi dạng</button>
            <button class="chip ${p.kind === 'mc' ? 'active' : ''}" data-f-kind="mc" type="button">Trắc nghiệm (${DB.mc.length})</button>
            <button class="chip ${p.kind === 'tf' ? 'active' : ''}" data-f-kind="tf" type="button">Đúng / Sai (${DB.tf.length})</button>
            <button class="chip ${p.onlyTrap ? 'active' : ''}" id="filterTrapBtn" type="button">⚠ Chỉ câu bẫy (${trapCount})</button>
            <button class="chip ${p.onlyWrong ? 'active' : ''}" id="filterWrongBtn" type="button">❌ Câu từng sai (${wrongCount})</button>
            <input class="search-input" id="pracSearchInput" type="search" value="${esc(p.query)}" placeholder="Tìm từ khóa (vd: 18/8, Bảo Đại, Quân lệnh, Đồng Nai...)" />
          </div>
        </div>

        ${bodyHtml}
      </div>
    `;
  }

  // =========================================================================
  // RENDER: TAB 3 — FLASHCARD & TIMELINE MINIGAMES
  // =========================================================================
  function initMatchGame(roundIdx) {
    if (ui.games.matchTimerId) {
      clearInterval(ui.games.matchTimerId);
      ui.games.matchTimerId = null;
    }
    const g = ui.games;
    g.matchRound = roundIdx;
    // Slice 6 pairs from the 12 milestones (Round even: 0..5, odd: 6..11, random >1: random 6)
    let source;
    if (roundIdx % 3 === 0) source = DB.timeline.slice(6, 12); // Most tested Aug 18 -> Sep 2!
    else if (roundIdx % 3 === 1) source = DB.timeline.slice(0, 6); // Mar 9 -> Aug 17
    else source = shuffleArr(DB.timeline).slice(0, 6);

    const pairs = source.map((m, i) => ({ id: 'm-' + i, date: m.date, event: m.short }));
    g.matchPairs = pairs;
    g.matchLeft = shuffleArr(pairs);
    g.matchRight = shuffleArr(pairs);
    g.matchSelLeft = null;
    g.matchSelRight = null;
    g.matchMatchedIds = {};
    g.matchWrongPair = null;
    g.matchMistakes = 0;
    g.matchElapsed = 0;
    g.matchDone = false;

    g.matchTimerId = setInterval(() => {
      if (ui.tab !== 'games' || ui.games.sub !== 'match' || ui.games.matchDone) return;
      ui.games.matchElapsed += 1;
      const el = document.getElementById('matchTimerVal');
      if (el) el.textContent = formatTime(ui.games.matchElapsed);
    }, 1000);
  }

  function initChronoGame() {
    // Pick 5 distinct chronological milestones from DB.timeline
    const idxs = shuffleArr(DB.timeline.map((_, i) => i))
      .slice(0, 5)
      .sort((a, b) => a - b);
    const selected = idxs.map((origIdx, rank) => ({
      id: 'c-' + origIdx,
      rank,
      date: DB.timeline[origIdx].date,
      short: DB.timeline[origIdx].short,
    }));
    ui.games.chronoItems = selected;
    ui.games.chronoPool = shuffleArr(selected);
    ui.games.chronoPicked = [];
    ui.games.chronoChecked = false;
  }

  function renderGamesTab() {
    const g = ui.games;
    let content = '';

    if (g.sub === 'flashcard') {
      const fcById = Object.fromEntries(DB.flashcards.map((f) => [f.id, f]));
      const list = g.fcOrder
        .map((id) => fcById[id])
        .filter((f) => f && (g.fcCat === 'all' || f.cat === g.fcCat));
      if (g.fcIdx >= list.length) g.fcIdx = 0;
      const card = list[g.fcIdx];
      const masteredInList = list.filter((f) => store.fcMastered[f.id]).length;
      const cat = card ? CAT_MAP[card.cat] : null;

      content = `
        <div class="fc-stage">
          <div class="filter-row" style="justify-content:center;margin-bottom:12px;">
            <button class="chip ${g.fcCat === 'all' ? 'active' : ''}" data-fc-cat="all" type="button">Tất cả (${DB.flashcards.length})</button>
            ${DB.categories.map((c) => `<button class="chip ${g.fcCat === c.id ? 'active' : ''}" data-fc-cat="${c.id}" type="button">${esc(c.short)}</button>`).join('')}
          </div>

          <div style="display:flex;justify-content:space-between;align-items:center;font-size:13.5px;font-weight:700;color:var(--text-secondary);">
            <span>Thẻ ${g.fcIdx + 1} / ${list.length}</span>
            <span style="color:var(--success)">Đã thuộc: ${masteredInList} / ${list.length} thẻ</span>
          </div>
          <div class="bar-track" style="margin-top:6px;">
            <div class="bar-fill" style="width:${Math.round((masteredInList / Math.max(1, list.length)) * 100)}%;background:var(--success);"></div>
          </div>

          <div class="fc-card-wrap">
            <div class="fc-card ${g.fcFlipped ? 'flipped' : ''}" id="fcFlipBox">
              <div class="fc-face fc-front">
                <div style="display:flex;gap:8px;align-items:center;">
                  <span class="badge badge-red">${esc(cat.short)}</span>
                  ${store.fcMastered[card.id] ? '<span class="badge badge-green">✓ Đã thuộc</span>' : '<span class="badge badge-neutral">Chưa thuộc</span>'}
                </div>
                <div class="fc-q">${esc(card.front)}</div>
                <div class="fc-hint">Nhấn vào thẻ hoặc phím <strong>Space</strong> để lật đáp án</div>
              </div>
              <div class="fc-face fc-back">
                <span class="badge badge-gold">ĐÁP ÁN CHUẨN SGK KNTT</span>
                <div class="fc-a">${esc(card.back)}</div>
                <div class="fc-hint">Đánh giá mức độ ghi nhớ của bạn bên dưới ↓</div>
              </div>
            </div>
          </div>

          <div class="fc-controls">
            <button class="btn btn-sm" id="fcPrevBtn" type="button">← Trước</button>
            <button class="btn btn-soft-danger btn-sm" id="fcNeedReviewBtn" type="button">↻ Chưa thuộc (ôn tiếp)</button>
            <button class="btn btn-success btn-sm" id="fcMasterBtn" type="button">✓ Đã thuộc thẻ này</button>
            <button class="btn btn-sm" id="fcNextBtn" type="button">Tiếp →</button>
            <button class="btn btn-sm" id="fcShuffleBtn" type="button">🔀 Trộn thẻ</button>
          </div>
        </div>
      `;
    } else if (g.sub === 'match') {
      if (!g.matchPairs.length) initMatchGame(0);
      const matchedCount = Object.keys(g.matchMatchedIds).length;
      const roundLabel =
        g.matchRound % 3 === 0
          ? 'Bộ 1: Cao trào Tổng khởi nghĩa (18/8 → 2/9)'
          : g.matchRound % 3 === 1
          ? 'Bộ 2: Chuẩn bị & Tân Trào (9/3 → 17/8)'
          : 'Bộ 3: Trộn ngẫu nhiên 6 mốc';

      content = `
        <div class="card" style="padding:20px;">
          <div class="section-header-row" style="margin-bottom:8px;">
            <div>
              <h3 style="margin:0;font-size:17px;">⚡ Ghép Cặp Mốc Thời Gian Siêu Tốc</h3>
              <p class="section-sub">${esc(roundLabel)} — Chọn 1 mốc bên trái rồi chọn sự kiện tương ứng bên phải.</p>
            </div>
            <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
              <span class="badge badge-info">⏱ <span id="matchTimerVal">${formatTime(g.matchElapsed)}</span></span>
              <span class="badge badge-green">Khớp: ${matchedCount}/6</span>
              <span class="badge badge-red">Lỗi: ${g.matchMistakes}</span>
              ${store.bestMatchSec !== null ? `<span class="badge badge-gold">🏆 Kỷ lục: ${store.bestMatchSec}s</span>` : ''}
              <button class="btn btn-primary btn-sm" id="matchNewRoundBtn" type="button">↻ Đổi bộ mốc mới</button>
            </div>
          </div>

          ${
            g.matchDone
              ? `
            <div style="padding:18px;border-radius:12px;background:var(--success-soft);border:1px solid var(--success-border);text-align:center;margin:10px 0;">
              <h3 style="margin:0 0 6px 0;color:var(--success);">🎉 Xuất sắc! Bạn ghép xong 6/6 mốc trong ${g.matchElapsed} giây (${g.matchMistakes} lỗi)!</h3>
              <button class="btn btn-success btn-sm" id="matchNextSetBtn" type="button">Chơi tiếp bộ mốc kế tiếp →</button>
            </div>
          `
              : ''
          }

          <div class="match-board">
            <div class="match-col">
              <div class="match-col-hdr">Mốc thời gian</div>
              ${g.matchLeft
                .map((p) => {
                  const isM = !!g.matchMatchedIds[p.id];
                  const isSel = g.matchSelLeft === p.id;
                  const isBad = g.matchWrongPair && g.matchWrongPair.l === p.id;
                  return `<button class="match-tile ${isM ? 'matched' : isSel ? 'selected' : ''} ${isBad ? 'shake' : ''}" type="button" data-match-l="${p.id}" ${isM ? 'disabled' : ''}>📅 ${esc(p.date)}</button>`;
                })
                .join('')}
            </div>
            <div class="match-col">
              <div class="match-col-hdr">Sự kiện lịch sử tương ứng</div>
              ${g.matchRight
                .map((p) => {
                  const isM = !!g.matchMatchedIds[p.id];
                  const isSel = g.matchSelRight === p.id;
                  const isBad = g.matchWrongPair && g.matchWrongPair.r === p.id;
                  return `<button class="match-tile ${isM ? 'matched' : isSel ? 'selected' : ''} ${isBad ? 'shake' : ''}" type="button" data-match-r="${p.id}" ${isM ? 'disabled' : ''}>${esc(p.event)}</button>`;
                })
                .join('')}
            </div>
          </div>
        </div>
      `;
    } else {
      if (!g.chronoItems.length) initChronoGame();
      const pickedSet = new Set(g.chronoPicked.map((x) => x.id));
      const slotsHtml = [0, 1, 2, 3, 4]
        .map((i) => {
          const item = g.chronoPicked[i];
          const ok = g.chronoChecked && item && item.rank === i;
          const bad = g.chronoChecked && item && item.rank !== i;
          return `
            <div class="chrono-slot ${item ? 'filled' : ''} ${ok ? 'ok' : bad ? 'bad' : ''}">
              <span class="chrono-num">${i + 1}</span>
              ${
                item
                  ? `<div style="flex:1;font-weight:600;font-size:14px;">${esc(item.short)} ${g.chronoChecked ? `<span class="badge ${ok ? 'badge-green' : 'badge-red'}" style="margin-left:6px;">${esc(item.date)}</span>` : ''}</div>
                     ${!g.chronoChecked ? `<button class="btn btn-sm" data-chrono-remove="${item.id}" type="button">Bỏ</button>` : ''}`
                  : `<span style="color:var(--text-muted);font-size:13.5px;">Chọn sự kiện thứ ${i + 1} từ cột bên trái...</span>`
              }
            </div>
          `;
        })
        .join('');

      const rightCount = g.chronoChecked ? g.chronoPicked.filter((x, i) => x.rank === i).length : 0;

      content = `
        <div class="card" style="padding:20px;">
          <div class="section-header-row">
            <div>
              <h3 style="margin:0;font-size:17px;">🧭 Xếp Thứ Tự Lịch Sử (Từ Sớm → Muộn)</h3>
              <p class="section-sub">Nhấn lần lượt 5 sự kiện theo đúng trình tự thời gian từ sớm nhất đến muộn nhất.</p>
            </div>
            <div style="display:flex;gap:8px;">
              ${!g.chronoChecked ? `<button class="btn btn-primary btn-sm" id="chronoCheckBtn" type="button" ${g.chronoPicked.length < 5 ? 'disabled' : ''}>Kiểm tra thứ tự (${g.chronoPicked.length}/5)</button>` : ''}
              <button class="btn btn-sm" id="chronoNewBtn" type="button">↻ Bộ 5 sự kiện mới</button>
            </div>
          </div>

          ${
            g.chronoChecked
              ? `<div style="padding:12px 16px;border-radius:10px;margin-bottom:12px;background:${rightCount === 5 ? 'var(--success-soft)' : 'var(--gold-soft)'};border:1px solid ${rightCount === 5 ? 'var(--success-border)' : 'var(--gold-border)'};font-weight:700;">
                  ${rightCount === 5 ? '🎉 Đúng tuyệt đối 5/5 vị trí! Bạn đã thuộc làu mạch diễn biến!' : `Bạn xếp đúng ${rightCount}/5 vị trí. Thứ tự chuẩn: ${g.chronoItems.map((x) => `${x.date} (${x.short})`).join(' → ')}`}
                </div>`
              : ''
          }

          <div class="chrono-grid">
            <div>
              <div class="match-col-hdr" style="margin-bottom:8px;">5 sự kiện đang bị xáo trộn</div>
              <div class="match-col">
                ${g.chronoPool
                  .map((item) => {
                    const used = pickedSet.has(item.id);
                    return `<button class="match-tile ${used ? 'matched' : ''}" type="button" data-chrono-pick="${item.id}" ${used || g.chronoChecked ? 'disabled' : ''}>${esc(item.short)}</button>`;
                  })
                  .join('')}
              </div>
            </div>
            <div>
              <div class="match-col-hdr" style="margin-bottom:8px;">Trình tự của bạn (Sớm → Muộn)</div>
              ${slotsHtml}
            </div>
          </div>
        </div>
      `;
    }

    return `
      <div class="container">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Flashcard Lật Thẻ &amp; Game Học Nhanh Mốc Thời Gian</h2>
            <p class="section-sub">Ghi nhớ sạch toàn bộ mốc ngày 13/8 → 2/9 và từ khóa ăn điểm chỉ trong 5 phút!</p>
          </div>
        </div>
        <div class="subtabs">
          <button class="subtab-btn ${g.sub === 'flashcard' ? 'active' : ''}" data-game-sub="flashcard" type="button">🃏 Flashcard (24 thẻ)</button>
          <button class="subtab-btn ${g.sub === 'match' ? 'active' : ''}" data-game-sub="match" type="button">⚡ Ghép Cặp Mốc Thời Gian</button>
          <button class="subtab-btn ${g.sub === 'chrono' ? 'active' : ''}" data-game-sub="chrono" type="button">🧭 Xếp Thứ Tự Lịch Sử</button>
        </div>
        ${content}
      </div>
    `;
  }

  // =========================================================================
  // RENDER: TAB 4 — THEORY, INTERACTIVE TIMELINE, 10 TRAPS & SOURCES
  // =========================================================================
  function renderTheoryTab() {
    const t = ui.theory;
    const activeTl = DB.timeline[t.activeTlIdx] || DB.timeline[0];

    const tlNodes = DB.timeline
      .map(
        (m, i) => `
      <button class="tl-node ${i === t.activeTlIdx ? 'active' : ''}" type="button" data-tl-idx="${i}">
        <div class="tl-date">${esc(m.date)}</div>
        <div class="tl-short">${esc(m.short)}</div>
      </button>
    `
      )
      .join('');

    const theoryHtml = DB.theory
      .map(
        (sec) => `
      <section class="card theory-card">
        <div class="theory-card-hdr">
          <span class="theory-num">${esc(sec.num)}</span>
          <div>
            <h3 style="margin:0;font-size:17.5px;">${esc(sec.title)}</h3>
            <p class="section-sub">${esc(sec.subtitle)}</p>
          </div>
        </div>
        ${sec.blocks
          .map(
            (b) => `
          <div class="theory-sub">
            <h4>${esc(b.heading)}</h4>
            <ul>${b.points.map((pt) => `<li>${esc(pt)}</li>`).join('')}</ul>
          </div>
        `
          )
          .join('')}
      </section>
    `
      )
      .join('');

    const trapsHtml = DB.traps
      .map((tr) => {
        const masked = t.hideTraps && !t.revealedTraps[tr.num];
        return `
          <article class="card trap-card">
            <div class="trap-title"><span class="badge badge-gold">Bẫy ${tr.num}</span> ${esc(tr.title)}</div>
            <div class="trap-wrong"><strong>✗ Dễ dính bẫy:</strong> ${esc(tr.wrong)}</div>
            <div class="trap-right ${masked ? 'masked' : ''}" data-reveal-trap="${tr.num}" title="${masked ? 'Nhấn để mở đáp án chuẩn SGK' : ''}">
              <strong>✓ Chuẩn SGK KNTT:</strong> ${esc(tr.right)}
            </div>
            <div class="trap-why ${masked ? 'masked' : ''}" data-reveal-trap="${tr.num}" style="${masked ? 'filter:blur(6px);user-select:none;cursor:pointer;' : ''}">${esc(tr.why)}</div>
          </article>
        `;
      })
      .join('');

    const sourcesHtml = DB.sources
      .map(
        (s) => `
      <article class="card" style="padding:18px 20px;margin-bottom:12px;">
        <div style="font-weight:800;color:var(--info);margin-bottom:4px;">${esc(s.title)} <span style="font-weight:500;color:var(--text-muted);font-size:13px;">— ${esc(s.meta)}</span></div>
        <div class="passage-box" style="margin:8px 0;">${esc(s.quote)}</div>
        <div style="font-size:13.8px;"><strong>Trọng tâm ra đề Đúng/Sai:</strong> ${esc(s.takeaway)}</div>
      </article>
    `
      )
      .join('');

    return `
      <div class="container">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Trục Thời Gian Tương Tác (12 Mốc Sống Còn)</h2>
            <p class="section-sub">Nhấn vào từng mốc ngày để xem diễn biến chi tiết &amp; cảnh báo bẫy đi kèm.</p>
          </div>
        </div>

        <div class="timeline-strip">${tlNodes}</div>

        <div class="card tl-detail-card">
          <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px;">
            <span class="badge badge-red">${esc(activeTl.date)}</span>
            <span class="badge badge-gold">${esc(activeTl.tag)}</span>
            <strong style="font-size:16.5px;">${esc(activeTl.short)}</strong>
          </div>
          <p style="margin:0 0 10px 0;">${esc(activeTl.detail)}</p>
          <div class="exp-tip" style="margin-top:0;">⚠ Cảnh báo bẫy mốc này: ${esc(activeTl.trap)}</div>
        </div>

        <div class="section-header-row" style="margin-top:26px;">
          <div>
            <h2 class="section-title">⚠ 10 Bẫy Kinh Điển Kiểm Tra 15 Phút</h2>
            <p class="section-sub">Bật chế độ che đáp án để tự nhẩm lại trước khi nhấn mở kiểm tra trí nhớ!</p>
          </div>
          <label class="toggle-label">
            <input type="checkbox" id="hideTrapsToggle" ${t.hideTraps ? 'checked' : ''} />
            <span>Che đáp án chuẩn SGK để tự ôn</span>
          </label>
        </div>
        <div class="traps-grid">${trapsHtml}</div>

        <h2 class="section-title" style="margin:24px 0 12px 0;">📖 Lý Thuyết Trọng Tâm SGK KNTT Bài 6</h2>
        ${theoryHtml}

        <h2 class="section-title" style="margin:24px 0 12px 0;">📜 4 Đoạn Tư Liệu Vàng Hay Ra Phần Đúng / Sai</h2>
        ${sourcesHtml}
      </div>
    `;
  }

  // =========================================================================
  // RENDER: TAB 5 — STATS & WRONG BANK
  // =========================================================================
  function renderStatsTab() {
    const masteredCount = Object.keys(store.mastered).length;
    const wrongIds = Object.keys(store.wrong);
    const pct = Math.round((masteredCount / ALL_ITEMS.length) * 100);

    const catBars = DB.categories
      .map((c) => {
        const items = ALL_ITEMS.filter((it) => it.cat === c.id);
        const done = items.filter((it) => store.mastered[it.id]).length;
        const p = Math.round((done / items.length) * 100);
        return `
          <div>
            <div class="cat-bar-top">
              <span>${esc(c.label)}</span>
              <span>${done}/${items.length} (${p}%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width:${p}%;background:${c.color}"></div></div>
          </div>
        `;
      })
      .join('');

    return `
      <div class="container">
        <div class="section-header-row">
          <div>
            <h2 class="section-title">Tiến Độ Ôn Thi &amp; Kho Câu Hay Sai</h2>
            <p class="section-sub">Dữ liệu lưu tự động trên trình duyệt của bạn.</p>
          </div>
          <button class="btn btn-soft-danger btn-sm" id="resetAllProgressBtn" type="button">Xóa toàn bộ tiến độ</button>
        </div>

        <div class="card result-hero">
          <div class="score-circle" style="--pct:${pct}">
            <div class="score-circle-inner">
              <div class="score-num">${pct}%</div>
              <div class="score-max">đã nắm chắc</div>
            </div>
          </div>
          <div style="width:100%">
            <h3 style="margin:0 0 8px 0;">Mức độ sẵn sàng kiểm tra 15 phút ngày mai</h3>
            <div class="result-breakdown">
              <div class="rb-box"><div class="rb-val">${masteredCount} / ${ALL_ITEMS.length}</div><div class="rb-lbl">Câu đã làm đúng</div></div>
              <div class="rb-box"><div class="rb-val" style="color:var(--danger)">${wrongIds.length} câu</div><div class="rb-lbl">Câu từng làm sai</div></div>
              <div class="rb-box"><div class="rb-val">${store.history.length} lượt</div><div class="rb-lbl">Số đề 15 phút đã thi</div></div>
            </div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              ${wrongIds.length > 0 ? `<button class="btn btn-primary btn-sm" id="statsDrillWrongBtn" type="button">🔥 Xử gọn ${wrongIds.length} câu từng sai ngay</button>` : '<span class="badge badge-green">✓ Hiện không có câu sai tồn đọng!</span>'}
            </div>
            <div class="cat-bars">${catBars}</div>
          </div>
        </div>

        <div class="card" style="padding:20px;">
          <h3 style="margin:0 0 12px 0;font-size:16.5px;">Toàn bộ lịch sử thi thử 15 phút (${store.history.length})</h3>
          ${
            store.history.length
              ? `
            <div style="overflow-x:auto;">
              <table class="history-table">
                <thead><tr><th>#</th><th>Đề thi</th><th>Điểm</th><th>Phần I</th><th>Phần II</th><th>Thời gian</th><th>Thời điểm</th></tr></thead>
                <tbody>
                  ${store.history
                    .map(
                      (h, idx) => `
                    <tr>
                      <td>${idx + 1}</td>
                      <td><strong>${esc(h.code)}</strong> — ${esc(h.name)}</td>
                      <td><span class="badge ${h.score >= 8.5 ? 'badge-green' : h.score >= 6.5 ? 'badge-gold' : 'badge-red'}">${h.score.toFixed(2)} / 10</span></td>
                      <td>${h.mcRight}/12</td>
                      <td>${h.tfRightItems}/8 ý</td>
                      <td>${formatTime(h.elapsedSec)}</td>
                      <td style="color:var(--text-muted)">${esc(h.dateStr)}</td>
                    </tr>
                  `
                    )
                    .join('')}
                </tbody>
              </table>
            </div>
          `
              : '<p style="color:var(--text-muted);margin:0;">Bạn chưa hoàn thành bài thi thử 15 phút nào. Chuyển sang mục <strong>Thi thử 15p</strong> để bắt đầu nhé!</p>'
          }
        </div>
      </div>
    `;
  }

  // =========================================================================
  // Master Render & Event Binding
  // =========================================================================
  function render() {
    const main = document.getElementById('mainContent');
    if (ui.tab === 'exam') main.innerHTML = renderExamTab();
    else if (ui.tab === 'practice') main.innerHTML = renderPracticeTab();
    else if (ui.tab === 'games') main.innerHTML = renderGamesTab();
    else if (ui.tab === 'theory') main.innerHTML = renderTheoryTab();
    else if (ui.tab === 'stats') main.innerHTML = renderStatsTab();
    bindViewEvents();
  }

  function bindViewEvents() {
    const main = document.getElementById('mainContent');

    // Exam Hub
    main.querySelectorAll('[data-start-exam]').forEach((btn) =>
      btn.addEventListener('click', () => startCuratedExam(btn.dataset.startExam))
    );
    const randBtn = main.querySelector('#startRandomExamBtn');
    if (randBtn) randBtn.addEventListener('click', startRandomExam);
    const heroQuick = main.querySelector('#heroQuickExam');
    if (heroQuick) heroQuick.addEventListener('click', () => startCuratedExam('de-01'));
    const heroTheory = main.querySelector('#heroQuickTheory');
    if (heroTheory) heroTheory.addEventListener('click', () => setTab('theory'));
    const heroWrong = main.querySelector('#heroDrillWrong');
    if (heroWrong) heroWrong.addEventListener('click', () => drillWrongIds(Object.keys(store.wrong)));
    const goStats = main.querySelector('#goStatsBtn');
    if (goStats) goStats.addEventListener('click', () => setTab('stats'));
    const shufToggle = main.querySelector('#shuffleExamToggle');
    if (shufToggle) {
      shufToggle.addEventListener('change', (e) => {
        ui.shuffleExam = e.target.checked;
      });
    }

    // Active Exam Events
    if (ui.tab === 'exam' && ui.examSession) {
      const ses = ui.examSession;
      main.querySelectorAll('[data-exam-mc]').forEach((btn) => {
        btn.addEventListener('click', () => {
          if (ses.submitted) return;
          ses.answersMc[btn.dataset.examMc] = Number(btn.dataset.opt);
          render();
        });
      });
      main.querySelectorAll('[data-exam-tf]').forEach((btn) => {
        btn.addEventListener('click', () => {
          if (ses.submitted) return;
          const tid = btn.dataset.examTf;
          ses.answersTf[tid] = ses.answersTf[tid] || {};
          ses.answersTf[tid][btn.dataset.key] = btn.dataset.val === 'true';
          render();
        });
      });
      main.querySelectorAll('[data-flag]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const id = btn.dataset.flag;
          ses.flags[id] = !ses.flags[id];
          render();
        });
      });
      main.querySelectorAll('[data-jump]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const target = document.getElementById(btn.dataset.jump);
          if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
      });
      const pauseBtn = main.querySelector('#pauseExamBtn');
      if (pauseBtn) {
        pauseBtn.addEventListener('click', () => {
          ses.paused = !ses.paused;
          if (ses.paused && ses.timerId) {
            clearInterval(ses.timerId);
            ses.timerId = null;
            toast('Đã tạm dừng đồng hồ.');
          } else {
            startExamTimer();
            toast('Tiếp tục đếm giờ!');
          }
          render();
        });
      }
      ['#submitExamBtn', '#submitExamSideBtn'].forEach((sel) => {
        const b = main.querySelector(sel);
        if (b) b.addEventListener('click', requestSubmitExam);
      });
      const cancelBtn = main.querySelector('#cancelExamBtn');
      if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
          openModal('Thoát bài thi?', '<p>Bạn có chắc muốn hủy bài thi thử hiện tại để quay về chọn đề khác?</p>', [
            { label: 'Tiếp tục làm bài', cls: 'btn-primary' },
            {
              label: 'Thoát đề',
              cls: 'btn-soft-danger',
              onClick: () => {
                stopAllTimers();
                ui.examSession = null;
                render();
              },
            },
          ]);
        });
      }
      ['#exitExamBtn', '#exitExamBtnTop'].forEach((sel) => {
        const b = main.querySelector(sel);
        if (b) {
          b.addEventListener('click', () => {
            ui.examSession = null;
            render();
          });
        }
      });
      const retake = main.querySelector('#retakeExamBtn');
      if (retake) {
        retake.addEventListener('click', () => {
          if (ses.examId.startsWith('random-')) startRandomExam();
          else startCuratedExam(ses.examId);
        });
      }
      const toggleRev = main.querySelector('#toggleReviewWrongBtn');
      if (toggleRev) {
        toggleRev.addEventListener('click', () => {
          ses.reviewFilter = ses.reviewFilter === 'wrong' ? 'all' : 'wrong';
          render();
        });
      }
      const drillBtn = main.querySelector('#drillExamWrongBtn');
      if (drillBtn && ses.result) {
        drillBtn.addEventListener('click', () => drillWrongIds(ses.result.wrongIds));
      }
    }

    // Practice Tab Events
    if (ui.tab === 'practice') {
      const p = ui.practice;
      main.querySelectorAll('[data-prac-mode]').forEach((b) =>
        b.addEventListener('click', () => {
          p.mode = b.dataset.pracMode;
          render();
        })
      );
      main.querySelectorAll('[data-f-cat]').forEach((b) =>
        b.addEventListener('click', () => {
          p.cat = b.dataset.fCat;
          p.focusIdx = 0;
          render();
        })
      );
      main.querySelectorAll('[data-f-kind]').forEach((b) =>
        b.addEventListener('click', () => {
          p.kind = b.dataset.fKind;
          if (p.kind === 'all') {
            p.onlyTrap = false;
            p.onlyWrong = false;
          }
          p.focusIdx = 0;
          render();
        })
      );
      const fTrap = main.querySelector('#filterTrapBtn');
      if (fTrap) {
        fTrap.addEventListener('click', () => {
          p.onlyTrap = !p.onlyTrap;
          if (p.onlyTrap) p.kind = 'mc';
          p.focusIdx = 0;
          render();
        });
      }
      const fWrong = main.querySelector('#filterWrongBtn');
      if (fWrong) {
        fWrong.addEventListener('click', () => {
          p.onlyWrong = !p.onlyWrong;
          p.focusIdx = 0;
          render();
        });
      }
      const searchIn = main.querySelector('#pracSearchInput');
      if (searchIn) {
        searchIn.addEventListener('input', (e) => {
          p.query = e.target.value;
          p.focusIdx = 0;
          render();
          const refreshed = document.getElementById('pracSearchInput');
          if (refreshed) {
            refreshed.focus();
            refreshed.setSelectionRange(refreshed.value.length, refreshed.value.length);
          }
        });
      }
      const shufBtn = main.querySelector('#pracShuffleBtn');
      if (shufBtn) {
        shufBtn.addEventListener('click', () => {
          p.order = shuffleArr(p.order);
          p.focusIdx = 0;
          toast('Đã trộn thứ tự kho 60 câu!');
          render();
        });
      }
      const clearBtn = main.querySelector('#clearFiltersBtn');
      if (clearBtn) {
        clearBtn.addEventListener('click', () => {
          p.cat = 'all';
          p.kind = 'all';
          p.onlyTrap = false;
          p.onlyWrong = false;
          p.query = '';
          p.focusIdx = 0;
          render();
        });
      }
      const prevBtn = main.querySelector('#pracPrevBtn');
      if (prevBtn) prevBtn.addEventListener('click', () => { p.focusIdx = Math.max(0, p.focusIdx - 1); render(); });
      const nextBtn = main.querySelector('#pracNextBtn');
      if (nextBtn) nextBtn.addEventListener('click', () => { p.focusIdx += 1; render(); });

      main.querySelectorAll('[data-prac-mc]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const qid = btn.dataset.pracMc;
          const opt = Number(btn.dataset.opt);
          p.answersMc[qid] = opt;
          const q = MC_MAP[qid];
          if (opt === q.answer) {
            store.mastered[qid] = true;
            delete store.wrong[qid];
          } else {
            store.wrong[qid] = true;
          }
          saveStore();
          render();
        });
      });
      main.querySelectorAll('[data-prac-reset]').forEach((btn) => {
        btn.addEventListener('click', () => {
          delete p.answersMc[btn.dataset.pracReset];
          render();
        });
      });
      main.querySelectorAll('[data-prac-tf]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const tid = btn.dataset.pracTf;
          p.answersTf[tid] = p.answersTf[tid] || {};
          p.answersTf[tid][btn.dataset.key] = btn.dataset.val === 'true';
          render();
        });
      });
      main.querySelectorAll('[data-prac-check-tf]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const tid = btn.dataset.pracCheckTf;
          p.checkedTf[tid] = true;
          const t = TF_MAP[tid];
          const ans = p.answersTf[tid] || {};
          const right = t.statements.filter((s) => ans[s.key] === s.answer).length;
          if (right === 4) {
            store.mastered[tid] = true;
            delete store.wrong[tid];
          } else {
            store.wrong[tid] = true;
          }
          saveStore();
          render();
        });
      });
      main.querySelectorAll('[data-prac-reset-tf]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const tid = btn.dataset.pracResetTf;
          delete p.answersTf[tid];
          delete p.checkedTf[tid];
          render();
        });
      });
    }

    // Games Tab Events
    if (ui.tab === 'games') {
      const g = ui.games;
      main.querySelectorAll('[data-game-sub]').forEach((btn) => {
        btn.addEventListener('click', () => {
          if (g.matchTimerId && btn.dataset.gameSub !== 'match') {
            clearInterval(g.matchTimerId);
            g.matchTimerId = null;
          }
          g.sub = btn.dataset.gameSub;
          if (g.sub === 'match' && (!g.matchPairs.length || g.matchDone)) initMatchGame(g.matchRound);
          if (g.sub === 'chrono' && !g.chronoItems.length) initChronoGame();
          render();
        });
      });

      // Flashcards
      main.querySelectorAll('[data-fc-cat]').forEach((b) =>
        b.addEventListener('click', () => {
          g.fcCat = b.dataset.fcCat;
          g.fcIdx = 0;
          g.fcFlipped = false;
          render();
        })
      );
      const flipBox = main.querySelector('#fcFlipBox');
      if (flipBox) {
        flipBox.addEventListener('click', () => {
          g.fcFlipped = !g.fcFlipped;
          flipBox.classList.toggle('flipped', g.fcFlipped);
        });
      }
      const fcList = g.fcOrder
        .map((id) => DB.flashcards.find((f) => f.id === id))
        .filter((f) => f && (g.fcCat === 'all' || f.cat === g.fcCat));
      const curFc = fcList[g.fcIdx];

      const fcPrev = main.querySelector('#fcPrevBtn');
      if (fcPrev) fcPrev.addEventListener('click', () => { g.fcIdx = (g.fcIdx - 1 + fcList.length) % fcList.length; g.fcFlipped = false; render(); });
      const fcNext = main.querySelector('#fcNextBtn');
      if (fcNext) fcNext.addEventListener('click', () => { g.fcIdx = (g.fcIdx + 1) % fcList.length; g.fcFlipped = false; render(); });
      const fcMaster = main.querySelector('#fcMasterBtn');
      if (fcMaster && curFc) {
        fcMaster.addEventListener('click', () => {
          store.fcMastered[curFc.id] = true;
          saveStore();
          g.fcIdx = (g.fcIdx + 1) % fcList.length;
          g.fcFlipped = false;
          toast('✓ Đã đánh dấu thuộc thẻ!');
          render();
        });
      }
      const fcReview = main.querySelector('#fcNeedReviewBtn');
      if (fcReview && curFc) {
        fcReview.addEventListener('click', () => {
          delete store.fcMastered[curFc.id];
          saveStore();
          g.fcIdx = (g.fcIdx + 1) % fcList.length;
          g.fcFlipped = false;
          render();
        });
      }
      const fcShuf = main.querySelector('#fcShuffleBtn');
      if (fcShuf) {
        fcShuf.addEventListener('click', () => {
          g.fcOrder = shuffleArr(g.fcOrder);
          g.fcIdx = 0;
          g.fcFlipped = false;
          toast('Đã trộn 24 thẻ Flashcard!');
          render();
        });
      }

      // Match Game
      const checkMatch = () => {
        if (!g.matchSelLeft || !g.matchSelRight) return;
        if (g.matchSelLeft === g.matchSelRight) {
          g.matchMatchedIds[g.matchSelLeft] = true;
          g.matchSelLeft = null;
          g.matchSelRight = null;
          if (Object.keys(g.matchMatchedIds).length === g.matchPairs.length) {
            g.matchDone = true;
            if (g.matchTimerId) {
              clearInterval(g.matchTimerId);
              g.matchTimerId = null;
            }
            if (store.bestMatchSec === null || g.matchElapsed < store.bestMatchSec) {
              store.bestMatchSec = g.matchElapsed;
              saveStore();
              toast(`🏆 Kỷ lục mới: ${g.matchElapsed} giây!`);
            }
          }
          render();
        } else {
          g.matchMistakes += 1;
          g.matchWrongPair = { l: g.matchSelLeft, r: g.matchSelRight };
          g.matchSelLeft = null;
          g.matchSelRight = null;
          render();
          setTimeout(() => {
            g.matchWrongPair = null;
            if (ui.tab === 'games' && ui.games.sub === 'match') render();
          }, 420);
        }
      };

      main.querySelectorAll('[data-match-l]').forEach((b) =>
        b.addEventListener('click', () => {
          g.matchSelLeft = b.dataset.matchL;
          if (g.matchSelRight) checkMatch();
          else render();
        })
      );
      main.querySelectorAll('[data-match-r]').forEach((b) =>
        b.addEventListener('click', () => {
          g.matchSelRight = b.dataset.matchR;
          if (g.matchSelLeft) checkMatch();
          else render();
        })
      );
      ['#matchNewRoundBtn', '#matchNextSetBtn'].forEach((sel) => {
        const b = main.querySelector(sel);
        if (b) {
          b.addEventListener('click', () => {
            initMatchGame(g.matchRound + 1);
            render();
          });
        }
      });

      // Chrono Game
      main.querySelectorAll('[data-chrono-pick]').forEach((b) =>
        b.addEventListener('click', () => {
          const item = g.chronoPool.find((x) => x.id === b.dataset.chronoPick);
          if (item && g.chronoPicked.length < 5) {
            g.chronoPicked.push(item);
            render();
          }
        })
      );
      main.querySelectorAll('[data-chrono-remove]').forEach((b) =>
        b.addEventListener('click', () => {
          g.chronoPicked = g.chronoPicked.filter((x) => x.id !== b.dataset.chronoRemove);
          render();
        })
      );
      const chCheck = main.querySelector('#chronoCheckBtn');
      if (chCheck) {
        chCheck.addEventListener('click', () => {
          g.chronoChecked = true;
          render();
        });
      }
      const chNew = main.querySelector('#chronoNewBtn');
      if (chNew) {
        chNew.addEventListener('click', () => {
          initChronoGame();
          render();
        });
      }
    }

    // Theory Tab Events
    if (ui.tab === 'theory') {
      main.querySelectorAll('[data-tl-idx]').forEach((b) =>
        b.addEventListener('click', () => {
          ui.theory.activeTlIdx = Number(b.dataset.tlIdx);
          render();
        })
      );
      const hideToggle = main.querySelector('#hideTrapsToggle');
      if (hideToggle) {
        hideToggle.addEventListener('change', (e) => {
          ui.theory.hideTraps = e.target.checked;
          ui.theory.revealedTraps = {};
          render();
        });
      }
      main.querySelectorAll('[data-reveal-trap]').forEach((el) => {
        el.addEventListener('click', () => {
          if (!ui.theory.hideTraps) return;
          ui.theory.revealedTraps[el.dataset.revealTrap] = true;
          render();
        });
      });
    }

    // Stats Tab Events
    if (ui.tab === 'stats') {
      const drill = main.querySelector('#statsDrillWrongBtn');
      if (drill) drill.addEventListener('click', () => drillWrongIds(Object.keys(store.wrong)));
      const reset = main.querySelector('#resetAllProgressBtn');
      if (reset) {
        reset.addEventListener('click', () => {
          openModal(
            'Xóa toàn bộ tiến độ?',
            '<p>Hành động này sẽ xóa lịch sử thi thử, danh sách câu đã nắm chắc, câu hay sai và thẻ Flashcard đã thuộc.</p>',
            [
              { label: 'Hủy' },
              {
                label: 'Xóa sạch',
                cls: 'btn-soft-danger',
                onClick: () => {
                  store.mastered = {};
                  store.wrong = {};
                  store.fcMastered = {};
                  store.history = [];
                  store.bestMatchSec = null;
                  saveStore();
                  toast('Đã đặt lại toàn bộ tiến độ.');
                  render();
                },
              },
            ]
          );
        });
      }
    }
  }

  // =========================================================================
  // Keyboard Shortcuts (Focus Practice & Flashcards)
  // =========================================================================
  document.addEventListener('keydown', (e) => {
    const tag = (e.target && e.target.tagName) || '';
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    if (!document.getElementById('modalBackdrop').hidden) {
      if (e.key === 'Escape') closeModal();
      return;
    }

    if (ui.tab === 'games' && ui.games.sub === 'flashcard') {
      if (e.code === 'Space') {
        e.preventDefault();
        ui.games.fcFlipped = !ui.games.fcFlipped;
        const box = document.getElementById('fcFlipBox');
        if (box) box.classList.toggle('flipped', ui.games.fcFlipped);
      } else if (e.key === 'ArrowRight') {
        const b = document.getElementById('fcNextBtn');
        if (b) b.click();
      } else if (e.key === 'ArrowLeft') {
        const b = document.getElementById('fcPrevBtn');
        if (b) b.click();
      }
    } else if (ui.tab === 'practice' && ui.practice.mode === 'focus') {
      if (e.key === 'ArrowRight') {
        const b = document.getElementById('pracNextBtn');
        if (b && !b.disabled) b.click();
      } else if (e.key === 'ArrowLeft') {
        const b = document.getElementById('pracPrevBtn');
        if (b && !b.disabled) b.click();
      } else if (['1', '2', '3', '4', 'a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'].includes(e.key)) {
        const idxMap = { '1': 0, '2': 1, '3': 2, '4': 3, a: 0, b: 1, c: 2, d: 3 };
        const idx = idxMap[e.key.toLowerCase()];
        const btn = document.querySelector(`[data-prac-mc][data-opt="${idx}"]:not(:disabled)`);
        if (btn) btn.click();
      }
    }
  });

  // =========================================================================
  // Boot
  // =========================================================================
  applyTheme();
  document.getElementById('themeToggle').addEventListener('click', () => {
    store.theme = store.theme === 'light' ? 'dark' : 'light';
    saveStore();
    applyTheme();
  });
  document.getElementById('brandBtn').addEventListener('click', () => setTab('exam'));
  document.querySelectorAll('.nav-tab').forEach((btn) =>
    btn.addEventListener('click', () => setTab(btn.dataset.tab))
  );
  document.getElementById('modalCloseBtn').addEventListener('click', closeModal);
  document.getElementById('modalBackdrop').addEventListener('click', (e) => {
    if (e.target.id === 'modalBackdrop') closeModal();
  });

  syncNavAndRender();
})();
