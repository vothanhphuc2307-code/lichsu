# -*- coding: utf-8 -*-
"""Build the printable A4 Study Guide + 2 Mock 15-Minute Exams + Detailed Solutions
+ 60-Second Cheat Sheet PDF for Lịch sử 12 (KNTT) — Bài 6: Cách mạng tháng Tám năm 1945.
"""

import html
import os
import re
import shutil
import subprocess
import time

from content_data import (
    EXAMS,
    MC_QUESTIONS,
    META,
    SOURCES,
    TF_QUESTIONS,
    THEORY_SECTIONS,
    TIMELINE,
    TRAPS,
    validate_data,
)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(OUT_DIR, "On_Tap_Va_De_Kiem_Tra_15_Phut_Lich_Su_12_Bai_6_KNTT.html")
PDF_PATH = os.path.join(OUT_DIR, "On_Tap_Va_De_Kiem_Tra_15_Phut_Lich_Su_12_Bai_6_KNTT.pdf")
CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE_DIR = os.path.join(OUT_DIR, "_chrome_pdf_profile")

MC_BY_ID = {q["id"]: q for q in MC_QUESTIONS}
TF_BY_ID = {t["id"]: t for t in TF_QUESTIONS}
LETTERS = ["A", "B", "C", "D"]


def esc(s):
    return html.escape(str(s), quote=True)


def build_svg_timeline():
    """Crisp vector SVG 2-row timeline of August Revolution (13/8 -> 2/9/1945)."""
    row1 = [
        ("13/8", "Quân lệnh số 1", "Ủy ban KN toàn quốc", "#991b1b"),
        ("14–15/8", "Hội nghị Đảng", "Tân Trào • Tổng KN", "#b91c1c"),
        ("15/8", "Nhật đầu hàng", "Thời cơ vàng mở ra", "#b45309"),
        ("16–17/8", "ĐH Quốc dân", "UB DT Giải phóng VN", "#b91c1c"),
        ("18/8", "4 tỉnh lị sớm nhất", "BG • HD • HT • QN", "#047857"),
    ]
    row2 = [
        ("19/8", "Hà Nội thắng lợi", "Đô thị lớn 1 • Cổ vũ", "#991b1b"),
        ("23/8", "Huế thắng lợi", "Đô thị lớn 2 • Kinh đô", "#c2410c"),
        ("25/8", "Sài Gòn thắng lợi", "Đô thị lớn 3 • Nam Bộ", "#c2410c"),
        ("28/8", "Thắng lợi cả nước", "ĐN Thượng & Hà Tiên", "#047857"),
        ("30/8 & 2/9", "Thoái vị & Độc lập", "Khai sinh VNDCCH", "#1e3a8a"),
    ]

    nodes_svg = []
    # Connecting lines Row 1
    nodes_svg.append('<line x1="72" y1="34" x2="668" y2="34" stroke="#fca5a5" stroke-width="3" stroke-linecap="round"/>')
    # Connecting curved turn from Row 1 end to Row 2 start
    nodes_svg.append('<path d="M 668 34 L 705 34 Q 722 34 722 52 L 722 108 Q 722 126 705 126 L 35 126 Q 18 126 18 144 L 18 156 Q 18 172 35 172 L 72 172" fill="none" stroke="#fed7aa" stroke-width="2.5" stroke-dasharray="5,4"/>')
    # Connecting lines Row 2
    nodes_svg.append('<line x1="72" y1="172" x2="668" y2="172" stroke="#fdba74" stroke-width="3" stroke-linecap="round"/>')

    xs = [72, 221, 370, 519, 668]
    for i, (date, title, sub, col) in enumerate(row1):
        x = xs[i]
        nodes_svg.append(f'''
          <g transform="translate({x}, 34)">
            <circle cx="0" cy="0" r="10" fill="{col}" stroke="#fff" stroke-width="2.5"/>
            <text x="0" y="3.5" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">{i+1}</text>
            <rect x="-66" y="16" width="132" height="58" rx="7" fill="#ffffff" stroke="{col}" stroke-width="1.2"/>
            <rect x="-66" y="16" width="132" height="19" rx="7" fill="{col}"/>
            <rect x="-66" y="28" width="132" height="7" fill="{col}"/>
            <text x="0" y="29" text-anchor="middle" font-size="10" font-weight="700" fill="#ffffff">{esc(date)}</text>
            <text x="0" y="49" text-anchor="middle" font-size="10.2" font-weight="700" fill="#111827">{esc(title)}</text>
            <text x="0" y="64" text-anchor="middle" font-size="8.8" fill="#4b5563">{esc(sub)}</text>
          </g>
        ''')

    for i, (date, title, sub, col) in enumerate(row2):
        x = xs[i]
        nodes_svg.append(f'''
          <g transform="translate({x}, 172)">
            <circle cx="0" cy="0" r="10" fill="{col}" stroke="#fff" stroke-width="2.5"/>
            <text x="0" y="3.5" text-anchor="middle" font-size="9.5" font-weight="700" fill="#fff">{i+6}</text>
            <rect x="-66" y="16" width="132" height="58" rx="7" fill="#ffffff" stroke="{col}" stroke-width="1.2"/>
            <rect x="-66" y="16" width="132" height="19" rx="7" fill="{col}"/>
            <rect x="-66" y="28" width="132" height="7" fill="{col}"/>
            <text x="0" y="29" text-anchor="middle" font-size="10" font-weight="700" fill="#ffffff">{esc(date)}</text>
            <text x="0" y="49" text-anchor="middle" font-size="10.2" font-weight="700" fill="#111827">{esc(title)}</text>
            <text x="0" y="64" text-anchor="middle" font-size="8.8" fill="#4b5563">{esc(sub)}</text>
          </g>
        ''')

    return f'''
    <div class="svg-card">
      <div class="svg-caption">SƠ ĐỒ TRỤC THỜI GIAN 10 MỐC SỐNG CÒN: CÁCH MẠNG THÁNG TÁM NĂM 1945 (13/8 → 2/9/1945)</div>
      <svg viewBox="0 0 740 256" width="100%" xmlns="http://www.w3.org/2000/svg" style="display:block;font-family:'Segoe UI',Arial,sans-serif;">
        <rect x="0" y="0" width="740" height="256" rx="10" fill="#fffaf7"/>
        {''.join(nodes_svg)}
      </svg>
    </div>
    '''


def render_theory_html():
    parts = []
    for sec in THEORY_SECTIONS:
        blocks_html = []
        for blk in sec["blocks"]:
            li_items = "".join(f"<li>{esc(p)}</li>" for p in blk["points"])
            blocks_html.append(f'''
              <div class="theory-block">
                <div class="theory-subhead">{esc(blk["heading"])}</div>
                <ul class="theory-list">{li_items}</ul>
              </div>
            ''')
        parts.append(f'''
          <div class="theory-sec">
            <div class="sec-head">
              <span class="sec-num">{esc(sec["num"])}</span>
              <div>
                <div class="sec-title">{esc(sec["title"])}</div>
                <div class="sec-sub">{esc(sec["subtitle"])}</div>
              </div>
            </div>
            {''.join(blocks_html)}
          </div>
        ''')
    return "".join(parts)


def render_compare_table():
    return '''
    <div class="compare-box">
      <div class="box-title">BẢNG PHÂN BIỆT NHANH 3 SỰ KIỆN LÃNH ĐẠO CÁCH MẠNG (13 – 17/8/1945) — CỰC HAY RA TRẮC NGHIỆM!</div>
      <table class="std-table">
        <thead>
          <tr>
            <th style="width:15%">Thời gian</th>
            <th style="width:27%">Sự kiện / Cơ quan</th>
            <th style="width:36%">Quyết định trọng tâm</th>
            <th style="width:22%">Từ khóa chốt đáp án</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>13/8/1945</strong></td>
            <td><strong>Ủy ban Khởi nghĩa toàn quốc</strong> (Trung ương Đảng &amp; Tổng bộ Việt Minh lập)</td>
            <td>Ban bố <strong>Quân lệnh số 1</strong> (23 giờ ngày 13/8), chính thức phát lệnh Tổng khởi nghĩa trong cả nước.</td>
            <td><span class="pill red">Quân lệnh số 1</span></td>
          </tr>
          <tr>
            <td><strong>14 – 15/8/1945</strong></td>
            <td><strong>Hội nghị toàn quốc của Đảng</strong> (Tân Trào, Tuyên Quang)</td>
            <td>Thông qua kế hoạch lãnh đạo toàn dân Tổng khởi nghĩa trước khi quân Đồng minh vào; quyết định đối nội, đối ngoại.</td>
            <td><span class="pill amber">Kế hoạch Đảng • Đối nội/ngoại</span></td>
          </tr>
          <tr>
            <td><strong>16 – 17/8/1945</strong></td>
            <td><strong>Đại hội Quốc dân Tân Trào</strong> (Tuyên Quang)</td>
            <td>Tán thành Tổng khởi nghĩa, thông qua 10 chính sách Việt Minh, quy định Quốc kì &amp; Quốc ca, cử <strong>Ủy ban Dân tộc giải phóng VN</strong> (Hồ Chí Minh làm Chủ tịch).</td>
            <td><span class="pill green">10 chính sách • UB DT Giải phóng</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    '''


def render_traps_html():
    rows = []
    for tr in TRAPS:
        rows.append(f'''
          <div class="trap-card">
            <div class="trap-hdr"><span class="trap-num">Bẫy {tr["num"]}</span> {esc(tr["title"])}</div>
            <div class="trap-grid">
              <div class="trap-bad"><strong>✗ Dễ dính bẫy:</strong> {esc(tr["wrong"])}</div>
              <div class="trap-good"><strong>✓ Chuẩn SGK:</strong> {esc(tr["right"])}</div>
            </div>
            <div class="trap-why"><em>Giải thích nhanh:</em> {esc(tr["why"])}</div>
          </div>
        ''')
    return f'''
      <div class="section-banner amber-banner">
        <span>⚠</span> 10 BẪY KINH ĐIỂN HAY RA TRONG ĐỀ KIỂM TRA 15 PHÚT BÀI 6
      </div>
      <div class="traps-wrap">{''.join(rows)}</div>
    '''


def render_sources_html():
    cards = []
    for s in SOURCES:
        cards.append(f'''
          <div class="source-card">
            <div class="source-title">{esc(s["title"])} <span class="source-meta">— {esc(s["meta"])}</span></div>
            <blockquote class="source-quote">{esc(s["quote"])}</blockquote>
            <div class="source-take"><strong>Trọng tâm khai thác câu Đúng/Sai:</strong> {esc(s["takeaway"])}</div>
          </div>
        ''')
    return f'''
      <div class="section-banner navy-banner">
        <span>📜</span> 4 ĐOẠN TƯ LIỆU VÀNG THƯỜNG DÙNG CHO PHẦN TRẮC NGHIỆM ĐÚNG / SAI
      </div>
      {''.join(cards)}
    '''


def render_exam_paper(exam):
    """Render a clean, printable 15-minute test paper (without answers)."""
    mc_blocks = []
    for idx, qid in enumerate(exam["mc_ids"], 1):
        q = MC_BY_ID[qid]
        # Check if short options -> 2-column grid, else 1-column
        max_len = max(len(o) for o in q["options"])
        grid_cls = "opt-grid-2" if max_len <= 52 else "opt-grid-1"
        opts_html = "".join(
            f'<div class="opt-item"><span class="opt-lbl">{LETTERS[i]}.</span> <span>{esc(opt)}</span></div>'
            for i, opt in enumerate(q["options"])
        )
        mc_blocks.append(f'''
          <div class="q-block">
            <div class="q-stem"><strong>Câu {idx}.</strong> {esc(q["question"])}</div>
            <div class="{grid_cls}">{opts_html}</div>
          </div>
        ''')

    tf_blocks = []
    for idx, tid in enumerate(exam["tf_ids"], 1):
        t = TF_BY_ID[tid]
        stmts_html = "".join(
            f'''
            <tr>
              <td class="tf-key"><strong>{s["key"]})</strong></td>
              <td class="tf-text">{esc(s["text"])}</td>
              <td class="tf-box">☐ Đ &nbsp; ☐ S</td>
            </tr>
            '''
            for s in t["statements"]
        )
        tf_blocks.append(f'''
          <div class="tf-block">
            <div class="q-stem"><strong>Câu {idx}.</strong> Đọc đoạn tư liệu sau đây và xác định tính Đúng/Sai của các nhận định bên dưới:</div>
            <div class="tf-passage">
              <div>{esc(t["passage"])}</div>
              <div class="tf-src">({esc(t["source"])})</div>
            </div>
            <table class="tf-table">
              <tbody>{stmts_html}</tbody>
            </table>
          </div>
        ''')

    return f'''
      <div class="page-break"></div>
      <div class="exam-header">
        <div class="exam-top-row">
          <div class="exam-left">
            <div class="exam-school">ÔN TẬP KIỂM TRA THƯỜNG XUYÊN 15 PHÚT</div>
            <div class="exam-subj">MÔN: LỊCH SỬ 12 — SÁCH KẾT NỐI TRI THỨC</div>
            <div class="exam-lesson">Nội dung: Bài 6 — Cách mạng tháng Tám năm 1945</div>
          </div>
          <div class="exam-right">
            <div class="exam-code">{esc(exam["code"])}</div>
            <div class="exam-time">Thời gian làm bài: 15 phút</div>
            <div class="exam-note">(Không kể thời gian phát đề)</div>
          </div>
        </div>
        <div class="student-bar">
          <span>Họ và tên: .................................................................</span>
          <span>Lớp: 12.......</span>
          <span>Điểm: ............. / 10</span>
        </div>
      </div>

      <div class="part-hdr">
        PHẦN I. TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN <span>(6,0 điểm — 12 câu × 0,5 điểm/câu)</span>
      </div>
      <div class="part-guide">Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi thí sinh chỉ chọn một phương án đúng nhất.</div>
      {''.join(mc_blocks)}

      <div class="part-hdr" style="margin-top:10px;">
        PHẦN II. TRẮC NGHIỆM ĐÚNG / SAI <span>(4,0 điểm — 2 câu × 2,0 điểm/câu)</span>
      </div>
      <div class="part-guide">Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn Đúng (Đ) hoặc Sai (S). Thang điểm chuẩn Bộ GD&amp;ĐT: đúng 1 ý được 0,2đ; đúng 2 ý được 0,5đ; đúng 3 ý được 1,0đ; đúng cả 4 ý được 2,0đ.</div>
      {''.join(tf_blocks)}
      <div class="exam-end">— HẾT {esc(exam["code"])} —</div>
    '''


def render_exam_solutions(exam):
    """Render quick answer key + detailed explanations for an exam."""
    # Quick MC table
    mc_cells_h = "".join(f"<th>C{i}</th>" for i in range(1, 13))
    mc_cells_a = "".join(f"<td><strong>{LETTERS[MC_BY_ID[qid]['answer']]}</strong></td>" for qid in exam["mc_ids"])

    tf_summary = []
    for idx, tid in enumerate(exam["tf_ids"], 1):
        t = TF_BY_ID[tid]
        seq = " &nbsp;•&nbsp; ".join(f'{s["key"]}) <strong>{"Đ" if s["answer"] else "S"}</strong>' for s in t["statements"])
        tf_summary.append(f'<span><strong>Câu {idx} (Đ/S):</strong> {seq}</span>')

    mc_details = []
    for idx, qid in enumerate(exam["mc_ids"], 1):
        q = MC_BY_ID[qid]
        ans_letter = LETTERS[q["answer"]]
        ans_text = q["options"][q["answer"]]
        trap_badge = '<span class="pill red" style="margin-left:5px;">CÂU BẪY</span>' if q["trap"] else ""
        mc_details.append(f'''
          <div class="sol-item">
            <div class="sol-head">
              <span class="sol-qnum">Câu {idx}</span>
              <span class="sol-ans">Chọn {ans_letter}</span>
              {trap_badge}
              <span class="sol-opt-preview">{esc(ans_text)}</span>
            </div>
            <div class="sol-body">{esc(q["explanation"])}</div>
            <div class="sol-tip"><strong>Mẹo nhớ nhanh:</strong> {esc(q["tip"])}</div>
          </div>
        ''')

    tf_details = []
    for idx, tid in enumerate(exam["tf_ids"], 1):
        t = TF_BY_ID[tid]
        stmt_rows = []
        for s in t["statements"]:
            badge = '<span class="tf-badge ok">ĐÚNG</span>' if s["answer"] else '<span class="tf-badge no">SAI</span>'
            stmt_rows.append(f'''
              <div class="tf-sol-row">
                <div class="tf-sol-top"><strong>Ý {s["key"]})</strong> {badge} <span class="tf-sol-stmt">{esc(s["text"])}</span></div>
                <div class="tf-sol-exp">{esc(s["explanation"])}</div>
              </div>
            ''')
        tf_details.append(f'''
          <div class="tf-sol-box">
            <div class="tf-sol-title">Phần II — Câu {idx}: {esc(t["title"])}</div>
            {''.join(stmt_rows)}
          </div>
        ''')

    return f'''
      <div class="sol-exam-block">
        <div class="section-banner green-banner">
          <span>✓</span> ĐÁP ÁN &amp; GIẢI THÍCH CHI TIẾT — {esc(exam["name"].upper())}
        </div>
        <div class="key-card">
          <div class="key-label">BẢNG TRA ĐÁP ÁN NHANH {esc(exam["code"])}</div>
          <table class="key-table">
            <thead><tr><th>Phần I</th>{mc_cells_h}</tr></thead>
            <tbody><tr><td><strong>Đáp án</strong></td>{mc_cells_a}</tr></tbody>
          </table>
          <div class="key-tf-row">{' &nbsp;&nbsp;|&nbsp;&nbsp; '.join(tf_summary)}</div>
        </div>
        <div class="sol-subhdr">I. Giải thích chi tiết 12 câu Trắc nghiệm nhiều phương án lựa chọn</div>
        {''.join(mc_details)}
        <div class="sol-subhdr" style="margin-top:8px;">II. Giải thích chi tiết 2 câu Trắc nghiệm Đúng / Sai</div>
        {''.join(tf_details)}
      </div>
    '''


def render_cheatsheet_page():
    """Standalone final 1-page A4 60-second cram sheet before entering the classroom."""
    return '''
      <div class="page-break"></div>
      <div class="cheat-page">
        <div class="cheat-banner">
          <div class="cheat-kicker">TỜ GHI NHỚ SIÊU TỐC — ĐỌC LẠI 60 GIÂY TRƯỚC KHI PHÁT ĐỀ</div>
          <div class="cheat-title">PHAO NHỚ NHANH BÀI 6: CÁCH MẠNG THÁNG TÁM NĂM 1945</div>
          <div class="cheat-sub">Sách giáo khoa Lịch sử 12 — Bộ Kết nối tri thức với cuộc sống</div>
        </div>

        <div class="cheat-grid-2">
          <div class="cheat-box red-top">
            <div class="cheat-h">1. MỐC NGÀY SỐNG CÒN (ĐỌC THUỘC LÒNG)</div>
            <ul class="cheat-list">
              <li><strong>9/3 &amp; 12/3/1945:</strong> Nhật đảo chính Pháp → Chỉ thị <em>"Nhật - Pháp bắn nhau..."</em> → Cao trào kháng Nhật &amp; khởi nghĩa từng phần.</li>
              <li><strong>6 &amp; 9/8/1945:</strong> Mỹ ném 2 bom nguyên tử; <strong>8–9/8:</strong> Liên Xô đánh tan đạo quân Quan Đông.</li>
              <li><strong>13/8/1945 (23h):</strong> Lập <strong>Ủy ban Khởi nghĩa toàn quốc</strong> → Ban bố <strong>Quân lệnh số 1</strong>.</li>
              <li><strong>14–15/8/1945:</strong> <strong>Hội nghị toàn quốc của Đảng</strong> (Tân Trào) → Kế hoạch Tổng KN + đối nội, đối ngoại.</li>
              <li><strong>15/8/1945:</strong> Nhật hoàng đầu hàng Đồng minh vô điều kiện → <strong>Thời cơ vàng mở ra</strong>.</li>
              <li><strong>16–17/8/1945:</strong> <strong>Đại hội Quốc dân Tân Trào</strong> → 10 chính sách Việt Minh + bầu <strong>UB DT Giải phóng VN</strong> (HCM Chủ tịch). Chiều 16/8: Võ Nguyên Giáp đánh thị xã Thái Nguyên.</li>
              <li><strong>18/8/1945:</strong> <strong>4 tỉnh lị sớm nhất:</strong> Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam + Thư kêu gọi của HCM.</li>
              <li><strong>19/8 → 23/8 → 25/8:</strong> <strong>3 đô thị lớn:</strong> Hà Nội → Huế → Sài Gòn (ý nghĩa quyết định!).</li>
              <li><strong>28/8/1945:</strong> <strong>2 tỉnh cuối cùng:</strong> Đồng Nai Thượng &amp; Hà Tiên → Xong cả nước trong <strong>15 ngày</strong> (14–28/8). Cải tổ thành Chính phủ lâm thời.</li>
              <li><strong>30/8/1945:</strong> Vua Bảo Đại thoái vị tại Huế → <strong>Chấm dứt chế độ quân chủ</strong> (&gt;1000 năm).</li>
              <li><strong>2/9/1945:</strong> Tuyên ngôn Độc lập (Ba Đình) → <strong>Khai sinh nước Việt Nam Dân chủ Cộng hòa</strong>.</li>
            </ul>
          </div>

          <div class="cheat-col">
            <div class="cheat-box amber-top">
              <div class="cheat-h">2. CÁC BỘ TỪ KHÓA "ĂN ĐIỂM CHẮC 100%"</div>
              <ul class="cheat-list">
                <li><strong>Mẹo nhớ 4 tỉnh đầu (18/8):</strong> <strong>BẮC - HẢI - HÀ - QUẢNG</strong> (Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam).</li>
                <li><strong>Mẹo nhớ 2 tỉnh cuối (28/8):</strong> <strong>ĐỒNG NAI THƯỢNG &amp; HÀ TIÊN</strong>.</li>
                <li><strong>Thời cơ ngàn năm có một:</strong> Từ <strong>15/8</strong> (Nhật đầu hàng) đến <strong>TRƯỚC KHI Đồng minh vào</strong> (đầu 9/1945).</li>
                <li><strong>3 con số lật đổ:</strong> Pháp <strong>&gt;80 năm</strong> • Nhật <strong>gần 5 năm</strong> • Quân chủ <strong>&gt;1000 năm</strong>.</li>
                <li><strong>Chuyển biến địa vị:</strong> Đảng (bí mật → <strong>cầm quyền</strong>); Nhân dân (nô lệ → <strong>làm chủ</strong>); Nhà nước dân chủ nhân dân <strong>đầu tiên ở Đông Nam Á</strong>.</li>
                <li><strong>Kỷ nguyên mới:</strong> Độc lập, tự do và phát triển dưới chế độ dân chủ cộng hòa.</li>
              </ul>
            </div>

            <div class="cheat-box green-top" style="margin-top:8px;">
              <div class="cheat-h">3. NGUYÊN NHÂN • TÍNH CHẤT • 4 BÀI HỌC</div>
              <ul class="cheat-list">
                <li><strong>Nguyên nhân QUYẾT ĐỊNH nhất:</strong> Chủ quan — đứng đầu là <strong>sự lãnh đạo của Đảng</strong> (15 năm chuẩn bị 1930–1945 + truyền thống yêu nước, Mặt trận Việt Minh).</li>
                <li><strong>Nguyên nhân KHÁCH QUAN:</strong> Chiến thắng của Liên Xô &amp; Đồng minh → <em>tạo điều kiện thuận lợi</em> (KHÔNG quyết định!).</li>
                <li><strong>Tính chất:</strong> Cách mạng <strong>giải phóng dân tộc</strong> điển hình mang tính <strong>dân chủ mới</strong>.</li>
                <li><strong>Phương thức:</strong> Khởi nghĩa từng phần → Tổng KN; kết hợp nông thôn &amp; thành thị; <strong>lực lượng chính trị quyết định</strong>, vũ trang làm nòng cốt; nhanh gọn (15 ngày), ít đổ máu.</li>
                <li><strong>4 Bài học vàng:</strong> (1) Lãnh đạo của Đảng; (2) Đại đoàn kết dân tộc (Việt Minh); (3) Nắm bắt, chớp thời cơ; (4) Kết hợp sức mạnh dân tộc với thời đại (nội lực quyết định).</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="cheat-box navy-top" style="margin-top:8px;">
          <div class="cheat-h">4. 6 BẪY PHẢI CẢNH GIÁC KHI ĐỌC ĐỀ (THẤY LÀ PHÁT HIỆN NGAY!)</div>
          <div class="cheat-traps-grid">
            <div><strong>①</strong> Giành chính quyền trực tiếp từ tay <strong>NHẬT &amp; tay sai</strong> (KHÔNG phải Pháp — Pháp bị đảo chính từ 9/3).</div>
            <div><strong>②</strong> <strong>13/8</strong> lập UB Khởi nghĩa ra Quân lệnh số 1 ≠ <strong>16–17/8</strong> ĐH Quốc dân bầu UB Dân tộc giải phóng VN.</div>
            <div><strong>③</strong> Chấm dứt chế độ phong kiến là <strong>30/8</strong> (Bảo Đại thoái vị), KHÔNG phải 19/8, 23/8 hay 2/9.</div>
            <div><strong>④</strong> Mới chấm dứt chế độ <strong>quân chủ</strong>, <strong>CHƯA</strong> xóa bỏ hết tàn dư phong kiến / cách mạng ruộng đất triệt để.</div>
            <div><strong>⑤</strong> <strong>Lực lượng CHÍNH TRỊ</strong> giữ vai trò quyết định, lực lượng vũ trang là nòng cốt (thấy đảo ngược → chọn SAI!).</div>
            <div><strong>⑥</strong> Ngày 15/8 quân Nhật <strong>rệu rã, hoang mang</strong> chứ <strong>KHÔNG</strong> bị tiêu diệt hết ngay hay tự trao chính quyền.</div>
          </div>
        </div>
      </div>
    '''


def build_html():
    de1, de2 = EXAMS[0], EXAMS[1]
    return f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<title>Ôn tập &amp; Đề Kiểm Tra 15 Phút Lịch Sử 12 (KNTT) — Bài 6: Cách mạng tháng Tám năm 1945</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10.5mm 12.5mm 13mm 12.5mm;
    @top-left {{ content: none; }}
    @top-center {{ content: none; }}
    @top-right {{ content: none; }}
    @bottom-left {{
      content: "Lịch sử 12 (KNTT) • Bài 6: Cách mạng tháng Tám năm 1945";
      font-family: "Segoe UI", Arial, sans-serif;
      font-size: 7.5pt;
      color: #6b7280;
    }}
    @bottom-right {{
      content: "Trang " counter(page) " / " counter(pages);
      font-family: "Segoe UI", Arial, sans-serif;
      font-size: 7.5pt;
      font-weight: 600;
      color: #4b5563;
    }}
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 9.4pt;
    line-height: 1.44;
    color: #1f2937;
    background: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}
  .page-break {{ page-break-before: always; break-before: page; }}

  /* Hero Cover Strip */
  .hero {{
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 55%, #b45309 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 10px;
    margin-bottom: 12px;
    position: relative;
  }}
  .hero-kicker {{
    font-size: 8pt;
    letter-spacing: 0.9px;
    text-transform: uppercase;
    color: #fde68a;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .hero-title {{
    font-family: "Times New Roman", Cambria, serif;
    font-size: 18.5pt;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 5px;
  }}
  .hero-sub {{
    font-size: 9.2pt;
    color: #fef3c7;
  }}
  .hero-pills {{
    margin-top: 9px;
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .hero-pill {{
    background: rgba(255,255,255,0.16);
    border: 1px solid rgba(255,255,255,0.28);
    color: #fff;
    padding: 2.5px 9px;
    border-radius: 99px;
    font-size: 8pt;
    font-weight: 600;
  }}

  /* Section Banners */
  .section-banner {{
    padding: 7px 12px;
    border-radius: 7px;
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin: 12px 0 8px 0;
    display: flex;
    align-items: center;
    gap: 7px;
    break-after: avoid;
    page-break-after: avoid;
  }}
  .red-banner {{ background: #fef2f2; color: #991b1b; border-left: 4px solid #b91c1c; }}
  .amber-banner {{ background: #fffbeb; color: #92400e; border-left: 4px solid #d97706; }}
  .navy-banner {{ background: #eff6ff; color: #1e3a8a; border-left: 4px solid #1d4ed8; }}
  .green-banner {{ background: #ecfdf5; color: #065f46; border-left: 4px solid #059669; }}

  /* SVG Card */
  .svg-card {{
    border: 1px solid #fed7aa;
    border-radius: 9px;
    padding: 8px 10px 6px 10px;
    background: #fffaf7;
    margin-bottom: 11px;
    break-inside: avoid;
  }}
  .svg-caption {{
    font-size: 8.2pt;
    font-weight: 700;
    color: #9a3412;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: 0.3px;
  }}

  /* Theory Sections */
  .theory-sec {{
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 9px;
    background: #ffffff;
  }}
  .sec-head {{
    display: flex;
    align-items: center;
    gap: 9px;
    border-bottom: 1.5px solid #fee2e2;
    padding-bottom: 6px;
    margin-bottom: 7px;
    break-after: avoid;
  }}
  .sec-num {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #991b1b;
    color: #fff;
    font-weight: 700;
    font-size: 10.5pt;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }}
  .sec-title {{
    font-size: 10.6pt;
    font-weight: 700;
    color: #7f1d1d;
  }}
  .sec-sub {{
    font-size: 8.2pt;
    color: #6b7280;
  }}
  .theory-block {{
    margin-bottom: 6px;
    break-inside: avoid;
  }}
  .theory-block:last-child {{ margin-bottom: 0; }}
  .theory-subhead {{
    font-weight: 700;
    font-size: 9.2pt;
    color: #111827;
    margin-bottom: 2.5px;
  }}
  .theory-list {{
    padding-left: 16px;
  }}
  .theory-list li {{
    margin-bottom: 2.5px;
    text-align: justify;
  }}

  /* Comparison Table */
  .compare-box {{
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 8px 10px;
    background: #fafafa;
    margin: 9px 0;
    break-inside: avoid;
  }}
  .box-title {{
    font-size: 8.6pt;
    font-weight: 700;
    color: #991b1b;
    margin-bottom: 6px;
  }}
  .std-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.6pt;
  }}
  .std-table th {{
    background: #991b1b;
    color: #fff;
    text-align: left;
    padding: 5px 7px;
    font-weight: 700;
  }}
  .std-table td {{
    border: 1px solid #e5e7eb;
    padding: 5px 7px;
    vertical-align: top;
    background: #fff;
  }}
  .pill {{
    display: inline-block;
    padding: 1.5px 6px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
  }}
  .pill.red {{ background: #fee2e2; color: #991b1b; }}
  .pill.amber {{ background: #fef3c7; color: #92400e; }}
  .pill.green {{ background: #d1fae5; color: #065f46; }}

  /* Traps Grid */
  .traps-wrap {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
  }}
  .trap-card {{
    border: 1px solid #fde68a;
    border-radius: 7px;
    padding: 6.5px 8px;
    background: #fffdf7;
    break-inside: avoid;
    font-size: 8.3pt;
  }}
  .trap-hdr {{
    font-weight: 700;
    color: #78350f;
    margin-bottom: 4px;
    font-size: 8.6pt;
  }}
  .trap-num {{
    display: inline-block;
    background: #d97706;
    color: #fff;
    border-radius: 4px;
    padding: 0.5px 5px;
    font-size: 7.4pt;
    margin-right: 3px;
  }}
  .trap-grid {{
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-bottom: 3.5px;
  }}
  .trap-bad {{
    background: #fef2f2;
    color: #991b1b;
    padding: 3px 6px;
    border-radius: 4px;
    border-left: 2.5px solid #dc2626;
  }}
  .trap-good {{
    background: #ecfdf5;
    color: #065f46;
    padding: 3px 6px;
    border-radius: 4px;
    border-left: 2.5px solid #059669;
  }}
  .trap-why {{
    color: #4b5563;
    font-size: 7.9pt;
    line-height: 1.35;
  }}

  /* Sources */
  .source-card {{
    border: 1px solid #bfdbfe;
    border-radius: 7px;
    padding: 7px 10px;
    background: #f8fbff;
    margin-bottom: 7px;
    break-inside: avoid;
  }}
  .source-title {{
    font-weight: 700;
    font-size: 8.9pt;
    color: #1e3a8a;
    margin-bottom: 3px;
  }}
  .source-meta {{
    font-weight: 400;
    color: #4b5563;
    font-size: 8.1pt;
  }}
  .source-quote {{
    font-family: "Times New Roman", Cambria, serif;
    font-style: italic;
    font-size: 9.4pt;
    line-height: 1.42;
    color: #111827;
    border-left: 3px solid #2563eb;
    padding-left: 9px;
    margin: 4px 0;
  }}
  .source-take {{
    font-size: 8.2pt;
    color: #1f2937;
  }}

  /* Exam Paper Styling — tuned so each 15-min exam fits cleanly on exactly 2 A4 pages (1 double-sided sheet!) */
  .exam-header {{
    border: 1.5px solid #1f2937;
    border-radius: 6px;
    padding: 7px 11px;
    margin-bottom: 7px;
    background: #fafafa;
    break-inside: avoid;
  }}
  .exam-top-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    border-bottom: 1px dashed #9ca3af;
    padding-bottom: 4px;
    margin-bottom: 4.5px;
  }}
  .exam-school {{ font-size: 8pt; font-weight: 700; color: #4b5563; }}
  .exam-subj {{ font-size: 10.5pt; font-weight: 800; color: #991b1b; }}
  .exam-lesson {{ font-size: 8.4pt; font-weight: 600; color: #111827; }}
  .exam-right {{ text-align: right; }}
  .exam-code {{
    display: inline-block;
    background: #991b1b;
    color: #fff;
    font-weight: 800;
    font-size: 9.4pt;
    padding: 1.5px 9px;
    border-radius: 5px;
    margin-bottom: 2px;
  }}
  .exam-time {{ font-size: 8.4pt; font-weight: 700; color: #111827; }}
  .exam-note {{ font-size: 7.4pt; font-style: italic; color: #6b7280; }}
  .student-bar {{
    display: flex;
    justify-content: space-between;
    font-size: 8.4pt;
    font-weight: 600;
    color: #111827;
  }}
  .part-hdr {{
    font-size: 9.1pt;
    font-weight: 800;
    color: #991b1b;
    border-bottom: 1.5px solid #991b1b;
    padding-bottom: 1.5px;
    margin-bottom: 2px;
    break-after: avoid;
  }}
  .part-hdr span {{ font-weight: 600; font-size: 8.1pt; color: #4b5563; }}
  .part-guide {{
    font-size: 7.7pt;
    font-style: italic;
    color: #4b5563;
    margin-bottom: 5px;
    break-after: avoid;
  }}
  .q-block {{
    margin-bottom: 4.2px;
    break-inside: avoid;
  }}
  .q-stem {{
    font-size: 8.55pt;
    line-height: 1.33;
    color: #111827;
    margin-bottom: 1.8px;
    text-align: justify;
  }}
  .opt-grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5px 12px;
    padding-left: 8px;
  }}
  .opt-grid-1 {{
    display: flex;
    flex-direction: column;
    gap: 1px;
    padding-left: 8px;
  }}
  .opt-item {{
    font-size: 8.35pt;
    line-height: 1.3;
    display: flex;
    gap: 4px;
    align-items: baseline;
  }}
  .opt-lbl {{ font-weight: 700; color: #7f1d1d; flex-shrink: 0; }}

  .tf-block {{
    margin-bottom: 6px;
    break-inside: avoid;
  }}
  .tf-passage {{
    background: #f9fafb;
    border: 1px solid #d1d5db;
    border-left: 3px solid #991b1b;
    border-radius: 5px;
    padding: 4.5px 8px;
    font-family: "Times New Roman", Cambria, serif;
    font-size: 8.9pt;
    line-height: 1.32;
    font-style: italic;
    margin: 3px 0 4px 0;
    text-align: justify;
  }}
  .tf-src {{
    text-align: right;
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 7.4pt;
    font-style: normal;
    color: #4b5563;
    margin-top: 2px;
  }}
  .tf-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.35pt;
    line-height: 1.3;
  }}
  .tf-table td {{
    border: 1px solid #e5e7eb;
    padding: 3px 5.5px;
    vertical-align: top;
  }}
  .tf-key {{ width: 25px; text-align: center; color: #7f1d1d; background: #fef2f2; }}
  .tf-box {{ width: 70px; text-align: center; white-space: nowrap; font-weight: 600; color: #374151; background: #fafafa; }}
  .exam-end {{
    text-align: center;
    font-weight: 700;
    font-size: 8.3pt;
    letter-spacing: 1px;
    color: #4b5563;
    margin-top: 5px;
  }}

  /* Solutions — tuned so each exam's solutions fit cleanly on exactly 2 A4 pages */
  .sol-exam-block {{ margin-bottom: 6px; }}
  .key-card {{
    border: 1px solid #a7f3d0;
    background: #f0fdf4;
    border-radius: 7px;
    padding: 5px 8px;
    margin-bottom: 6px;
    break-inside: avoid;
  }}
  .key-label {{
    font-size: 8pt;
    font-weight: 800;
    color: #065f46;
    margin-bottom: 3px;
  }}
  .key-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.1pt;
    text-align: center;
    background: #fff;
  }}
  .key-table th {{
    background: #047857;
    color: #fff;
    padding: 2.5px 4px;
    border: 1px solid #047857;
  }}
  .key-table td {{
    padding: 2.5px 4px;
    border: 1px solid #a7f3d0;
    color: #065f46;
  }}
  .key-tf-row {{
    margin-top: 4px;
    font-size: 8pt;
    color: #064e3b;
  }}
  .sol-subhdr {{
    font-size: 8.8pt;
    font-weight: 700;
    color: #111827;
    margin: 4px 0 4px 0;
    break-after: avoid;
  }}
  .sol-item {{
    border: 1px solid #e5e7eb;
    border-left: 3px solid #059669;
    border-radius: 5px;
    padding: 4px 7px;
    margin-bottom: 3.8px;
    background: #fff;
    break-inside: avoid;
    font-size: 8pt;
    line-height: 1.32;
  }}
  .sol-head {{
    margin-bottom: 1.5px;
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 4px;
  }}
  .sol-qnum {{ font-weight: 800; color: #111827; }}
  .sol-ans {{
    background: #047857;
    color: #fff;
    font-weight: 700;
    font-size: 7.3pt;
    padding: 0.5px 5px;
    border-radius: 4px;
  }}
  .sol-opt-preview {{ font-weight: 600; color: #065f46; }}
  .sol-body {{ color: #374151; text-align: justify; margin-bottom: 1.5px; }}
  .sol-tip {{ color: #92400e; background: #fffbeb; padding: 1.5px 5px; border-radius: 4px; font-size: 7.6pt; }}

  .tf-sol-box {{
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 5px;
    background: #fafafa;
    break-inside: avoid;
  }}
  .tf-sol-title {{
    font-weight: 700;
    color: #1e3a8a;
    font-size: 8.3pt;
    margin-bottom: 3px;
  }}
  .tf-sol-row {{
    padding: 2.5px 0;
    border-top: 1px dashed #e5e7eb;
    font-size: 7.9pt;
    line-height: 1.3;
  }}
  .tf-sol-top {{ margin-bottom: 1px; }}
  .tf-badge {{
    display: inline-block;
    padding: 0.5px 5px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 7.1pt;
    margin: 0 3px;
  }}
  .tf-badge.ok {{ background: #d1fae5; color: #065f46; }}
  .tf-badge.no {{ background: #fee2e2; color: #991b1b; }}
  .tf-sol-stmt {{ font-weight: 600; color: #111827; }}
  .tf-sol-exp {{ color: #374151; padding-left: 6px; text-align: justify; }}

  /* Final 1-page 60s Cheat Sheet */
  .cheat-page {{ font-size: 8.15pt; line-height: 1.36; }}
  .cheat-banner {{
    background: linear-gradient(135deg, #1e293b 0%, #7f1d1d 100%);
    color: #fff;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 9px;
    text-align: center;
  }}
  .cheat-kicker {{ font-size: 7.4pt; letter-spacing: 0.8px; color: #fde68a; font-weight: 700; }}
  .cheat-title {{ font-family: "Times New Roman", Cambria, serif; font-size: 14pt; font-weight: 700; margin: 2px 0; }}
  .cheat-sub {{ font-size: 8pt; color: #e2e8f0; }}
  .cheat-grid-2 {{
    display: grid;
    grid-template-columns: 1.06fr 0.94fr;
    gap: 8px;
    align-items: start;
  }}
  .cheat-box {{
    border: 1px solid #e5e7eb;
    border-radius: 7px;
    padding: 7px 9px;
    background: #fff;
  }}
  .red-top {{ border-top: 3.5px solid #b91c1c; }}
  .amber-top {{ border-top: 3.5px solid #d97706; }}
  .green-top {{ border-top: 3.5px solid #059669; }}
  .navy-top {{ border-top: 3.5px solid #1d4ed8; background: #f8fbff; }}
  .cheat-h {{
    font-weight: 800;
    font-size: 8.5pt;
    color: #111827;
    margin-bottom: 4.5px;
    letter-spacing: 0.2px;
  }}
  .cheat-list {{ padding-left: 14px; }}
  .cheat-list li {{ margin-bottom: 3px; text-align: justify; }}
  .cheat-traps-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 12px;
    font-size: 8pt;
  }}
</style>
</head>
<body>
  <!-- COVER / HERO -->
  <div class="hero">
    <div class="hero-kicker">{esc(META["subject"])} • SÁCH GIÁO KHOA {esc(META["book"])}</div>
    <div class="hero-title">BÀI 6: CÁCH MẠNG THÁNG TÁM NĂM 1945</div>
    <div class="hero-sub">Cẩm nang ôn cấp tốc kiểm tra 15 phút • Sơ đồ mốc thời gian • 10 bẫy kinh điển • 2 Đề thi thử chuẩn Bộ GD&amp;ĐT kèm giải chi tiết</div>
    <div class="hero-pills">
      <span class="hero-pill">Bám sát 100% SGK KNTT</span>
      <span class="hero-pill">2 Đề 15 phút (12 TN + 2 Đúng/Sai)</span>
      <span class="hero-pill">Giải thích từng ý a–d</span>
      <span class="hero-pill">Kèm Tờ Phao Nhớ Nhanh 60 Giây</span>
    </div>
  </div>

  <!-- SECTION A: THEORY & TIMELINE -->
  <div class="section-banner red-banner">
    <span>★</span> PHẦN A. HỆ THỐNG LÝ THUYẾT TRỌNG TÂM &amp; TRỤC THỜI GIAN BÀI 6
  </div>
  {build_svg_timeline()}
  {render_theory_html()}
  {render_compare_table()}

  <!-- TRAPS & SOURCES -->
  <div class="page-break"></div>
  {render_traps_html()}
  {render_sources_html()}

  <!-- SECTION B: ĐỀ 01 -->
  {render_exam_paper(de1)}

  <!-- SECTION C: ĐỀ 02 -->
  {render_exam_paper(de2)}

  <!-- SECTION D: SOLUTIONS -->
  <div class="page-break"></div>
  {render_exam_solutions(de1)}
  <div class="page-break"></div>
  {render_exam_solutions(de2)}

  <!-- FINAL BONUS 1-PAGE CHEAT SHEET -->
  {render_cheatsheet_page()}
</body>
</html>
'''


def export_pdf():
    validate_data()
    html_str = build_html()
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(f"[OK] Wrote HTML: {HTML_PATH} ({len(html_str):,} chars)")

    if os.path.exists(PDF_PATH):
        os.remove(PDF_PATH)
    if os.path.exists(PROFILE_DIR):
        shutil.rmtree(PROFILE_DIR, ignore_errors=True)
    os.makedirs(PROFILE_DIR, exist_ok=True)

    file_url = "file:///" + HTML_PATH.replace("\\", "/")
    cmd = [
        CHROME_EXE,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-crash-reporter",
        "--disable-extensions",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        "--no-pdf-header-footer",
        f"--user-data-dir={PROFILE_DIR}",
        f"--print-to-pdf={PDF_PATH}",
        file_url,
    ]
    t0 = time.time()
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    last_size = -1
    stable_ticks = 0
    while True:
        rc = proc.poll()
        if rc is not None:
            print(f"[OK] Chrome exited rc={rc} in {time.time() - t0:.1f}s")
            break
        if os.path.exists(PDF_PATH):
            sz = os.path.getsize(PDF_PATH)
            if sz > 10000 and sz == last_size:
                with open(PDF_PATH, "rb") as pf:
                    pf.seek(max(0, sz - 64))
                    tail = pf.read()
                if b"%%EOF" in tail:
                    stable_ticks += 1
                    if stable_ticks >= 3:
                        proc.terminate()
                        print(f"[OK] PDF stabilized ({sz:,} bytes) in {time.time() - t0:.1f}s")
                        break
            else:
                last_size = sz
                stable_ticks = 0
        if time.time() - t0 > 60:
            proc.kill()
            raise RuntimeError("Chrome timed out exporting PDF")
        time.sleep(0.4)

    shutil.rmtree(PROFILE_DIR, ignore_errors=True)

    if not os.path.exists(PDF_PATH):
        raise RuntimeError("PDF was not generated!")

    pdf_bytes = open(PDF_PATH, "rb").read()
    pg_count = len(re.findall(rb"/Type\s*/Page\b(?!s)", pdf_bytes))
    print(f"[OK] Final PDF: {PDF_PATH} ({len(pdf_bytes):,} bytes, {pg_count} pages)")


if __name__ == "__main__":
    export_pdf()
