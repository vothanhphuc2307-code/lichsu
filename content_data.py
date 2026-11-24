# -*- coding: utf-8 -*-
"""Master verified content & question bank for:
Lịch sử 12 (Kết nối tri thức với cuộc sống) — Bài 6: Cách mạng tháng Tám năm 1945.
Used as single source of truth for both the interactive Web App (data.js)
and the printable A4 Study Guide & Mock Exam PDF (build_pdf.py).
"""

META = {
    "subject": "Lịch sử 12",
    "book": "Kết nối tri thức với cuộc sống (GDPT 2018)",
    "topic": "Chủ đề 3: Cách mạng tháng Tám năm 1945, chiến tranh giải phóng dân tộc và chiến tranh bảo vệ Tổ quốc trong lịch sử Việt Nam (từ tháng 8 năm 1945 đến nay)",
    "lesson_num": 6,
    "lesson_title": "Bài 6: Cách mạng tháng Tám năm 1945",
    "exam_duration_min": 15,
    "exam_structure": "12 câu Trắc nghiệm nhiều lựa chọn (6,0 điểm) + 2 câu Trắc nghiệm Đúng/Sai (4,0 điểm)",
}

CATEGORIES = [
    {"id": "boi-canh", "label": "1. Bối cảnh & Thời cơ", "short": "Bối cảnh", "color": "#b91c1c"},
    {"id": "dien-bien", "label": "2. Diễn biến Tổng khởi nghĩa", "short": "Diễn biến", "color": "#c2410c"},
    {"id": "nguyen-nhan-y-nghia", "label": "3. Nguyên nhân & Ý nghĩa", "short": "Nguyên nhân - Ý nghĩa", "color": "#0f766e"},
    {"id": "bai-hoc-tinh-chat", "label": "4. Bài học, Tính chất & Vận dụng", "short": "Bài học & Vận dụng", "color": "#4338ca"},
]

# ============================================================================
# 1. STRUCTURED THEORY (Bám sát 100% SGK Lịch sử 12 KNTT Bài 6)
# ============================================================================
THEORY_SECTIONS = [
    {
        "id": "sec-1",
        "num": "1",
        "title": "Bối cảnh lịch sử & Thời cơ \"ngàn năm có một\"",
        "subtitle": "Tình hình thế giới, trong nước và chủ trương kịp thời của Đảng",
        "blocks": [
            {
                "heading": "a) Bối cảnh thế giới (Khách quan thuận lợi)",
                "points": [
                    "Đầu tháng 8/1945, Chiến tranh thế giới thứ hai bước vào giai đoạn kết thúc (phát xít Đức đã đầu hàng ở châu Âu từ tháng 5/1945).",
                    "Ở châu Á – Thái Bình Dương, quân Đồng minh dồn dập tấn công Nhật Bản: Mỹ ném hai quả bom nguyên tử xuống Hi-rô-si-ma (6/8) và Na-ga-xa-ki (9/8); Hồng quân Liên Xô tuyên chiến (8/8) và tấn công tiêu diệt đạo quân Quan Đông của Nhật ở Đông Bắc Trung Quốc (9/8).",
                    "Ngày 15/8/1945, Nhật hoàng tuyên bố đầu hàng Đồng minh không điều kiện. Chiến tranh thế giới thứ hai chấm dứt."
                ]
            },
            {
                "heading": "b) Bối cảnh trong nước & Thời cơ \"ngàn năm có một\"",
                "points": [
                    "Kẻ thù tê liệt: Quân Nhật ở Đông Dương rệu rã, mất hết tinh thần chiến đấu; chính phủ thân Nhật Trần Trọng Kim hoang mang, dao động cực độ.",
                    "Lực lượng cách mạng sẵn sàng: Trải qua 15 năm chuẩn bị (1930–1945) và trực tiếp là Cao trào kháng Nhật cứu nước (từ tháng 3 đến giữa tháng 8/1945, sau sự kiện Nhật đảo chính Pháp 9/3 và Chỉ thị \"Nhật - Pháp bắn nhau và hành động của chúng ta\" ngày 12/3/1945), lực lượng chính trị, vũ trang và khí thế quần chúng đã sẵn sàng; tầng lớp trung gian ngả hẳn về phía cách mạng.",
                    "Thời cơ vàng (rất ngắn ngủi): Chỉ tồn tại từ khi Nhật Bản đầu hàng Đồng minh (15/8/1945) đến TRƯỚC KHI quân Đồng minh (Anh, Trung Hoa Dân quốc) kéo vào Đông Dương giải giáp quân Nhật (đầu tháng 9/1945). Kẻ thù cũ đã gục ngã, kẻ thù mới chưa kịp đến!"
                ]
            },
            {
                "heading": "c) Chủ trương kịp thời của Đảng và Hồ Chí Minh (13 – 17/8/1945)",
                "points": [
                    "Ngày 13/8/1945: Ngay khi nhận tin Nhật sắp đầu hàng, Trung ương Đảng và Tổng bộ Việt Minh lập Ủy ban Khởi nghĩa toàn quốc, ban bố Quân lệnh số 1 (23 giờ ngày 13/8), chính thức phát lệnh Tổng khởi nghĩa trong cả nước.",
                    "Ngày 14 – 15/8/1945: Hội nghị toàn quốc của Đảng họp tại Tân Trào (Tuyên Quang), thông qua kế hoạch lãnh đạo toàn dân Tổng khởi nghĩa giành chính quyền trước khi quân Đồng minh vào; quyết định những vấn đề quan trọng về đối nội, đối ngoại sau khi giành chính quyền.",
                    "Ngày 16 – 17/8/1945: Đại hội Quốc dân họp tại Tân Trào, tán thành chủ trương Tổng khởi nghĩa của Đảng, thông qua 10 chính sách lớn của Việt Minh, quy định Quốc kì (cờ đỏ sao vàng), Quốc ca (Tiến quân ca) và cử ra Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch.",
                    "Ngày 18/8/1945: Chủ tịch Hồ Chí Minh gửi Thư kêu gọi Tổng khởi nghĩa: \"Giờ quyết định cho vận mệnh dân tộc ta đã đến. Toàn quốc đồng bào hãy đứng dậy đem sức ta mà tự giải phóng cho ta.\""
                ]
            }
        ]
    },
    {
        "id": "sec-2",
        "num": "2",
        "title": "Diễn biến chính của Cách mạng tháng Tám năm 1945",
        "subtitle": "15 ngày sục sôi (14/8 → 28/8/1945) và mốc son khai sinh nước Việt Nam mới (2/9/1945)",
        "blocks": [
            {
                "heading": "a) Khởi nghĩa bùng nổ và giành chính quyền sớm ở các địa phương",
                "points": [
                    "Từ ngày 14/8/1945: Nhiều cấp bộ Đảng và Việt Minh ở cơ sở (một số xã, huyện thuộc đồng bằng sông Hồng, Thanh Hóa, Nghệ An, Hà Tĩnh, Thừa Thiên Huế, Quảng Ngãi, Khánh Hòa...) dù chưa nhận được Quân lệnh số 1 vẫn chủ động căn cứ vào Chỉ thị 12/3/1945 phát động nhân dân nổi dậy giành chính quyền.",
                    "Chiều 16/8/1945: Một đơn vị Giải phóng quân do Võ Nguyên Giáp chỉ huy xuất phát từ Tân Trào tiến về bao vây, đánh chiếm thị xã Thái Nguyên, mở đầu cuộc Tổng khởi nghĩa bằng lực lượng vũ trang.",
                    "Ngày 18/8/1945: Nhân dân 4 tỉnh Bắc Giang, Hải Dương, Hà Tĩnh và Quảng Nam giành được chính quyền ở tỉnh lị SỚM NHẤT cả nước."
                ]
            },
            {
                "heading": "b) Thắng lợi quyết định tại 3 trung tâm đô thị lớn",
                "points": [
                    "Hà Nội (19/8/1945): Cuộc mít tinh lớn tại Nhà hát Lớn biến thành biểu tình vũ trang, quần chúng chiếm Phủ Khâm sai, Tòa Thị chính, Trại Bảo an binh... Tối 19/8, khởi nghĩa thắng lợi hoàn toàn tại Thủ đô, cổ vũ mạnh mẽ cả nước.",
                    "Huế (23/8/1945): Hàng vạn nhân dân nội, ngoại thành kéo về trung tâm thành phố chiếm các công sở, giành chính quyền tại kinh đô triều Nguyễn.",
                    "Sài Gòn (25/8/1945): Hơn 1 triệu quần chúng Sài Gòn – Chợ Lớn và các tỉnh lân cận biểu tình rầm rộ, giành chính quyền ở trung tâm lớn nhất Nam Bộ."
                ]
            },
            {
                "heading": "c) Hoàn thành trên cả nước & Khai sinh nước Việt Nam Dân chủ Cộng hòa",
                "points": [
                    "Ngày 28/8/1945: Hai tỉnh cuối cùng trên đất liền là Đồng Nai Thượng và Hà Tiên giành được chính quyền → Tổng khởi nghĩa thắng lợi trên phạm vi cả nước chỉ trong 15 ngày (14–28/8/1945). Cùng ngày, Ủy ban Dân tộc giải phóng Việt Nam cải tổ thành Chính phủ lâm thời nước Việt Nam Dân chủ Cộng hòa.",
                    "Ngày 30/8/1945: Tại Ngọ Môn (Huế), vua Bảo Đại đọc chiếu thoái vị và trao ấn kiếm cho đại diện Chính phủ lâm thời → Chế độ quân chủ phong kiến Việt Nam hơn 1000 năm hoàn toàn sụp đổ.",
                    "Ngày 2/9/1945: Tại Quảng trường Ba Đình (Hà Nội), Chủ tịch Hồ Chí Minh thay mặt Chính phủ lâm thời đọc bản Tuyên ngôn Độc lập, trịnh trọng tuyên bố sự ra đời của nước Việt Nam Dân chủ Cộng hòa."
                ]
            }
        ]
    },
    {
        "id": "sec-3",
        "num": "3",
        "title": "Nguyên nhân thắng lợi, Ý nghĩa lịch sử & Bài học kinh nghiệm",
        "subtitle": "Trọng tâm ăn điểm câu Thông hiểu – Vận dụng – Đúng/Sai",
        "blocks": [
            {
                "heading": "a) Nguyên nhân thắng lợi (Chủ quan QUYẾT ĐỊNH — Khách quan THUẬN LỢI)",
                "points": [
                    "Chủ quan (Quyết định nhất): (1) Sự lãnh đạo đúng đắn, sáng suốt, tài tình của Đảng Cộng sản Đông Dương, đứng đầu là Chủ tịch Hồ Chí Minh (NHÂN TỐ QUYẾT ĐỊNH HÀNG ĐẦU); (2) Quá trình chuẩn bị chu đáo suốt 15 năm (1930–1945) qua 3 phong trào cách mạng (1930–1931, 1936–1939, 1939–1945); (3) Truyền thống yêu nước nồng nàn, tinh thần đoàn kết, ý chí đấu tranh bất khuất của toàn dân tộc dưới ngọn cờ Mặt trận Việt Minh.",
                    "Khách quan (Điều kiện thuận lợi): Chiến thắng của Hồng quân Liên Xô và các lực lượng Đồng minh trong cuộc chiến tranh chống phát xít (đặc biệt là đánh bại quân phiệt Nhật Bản), làm kẻ thù trực tiếp ở Đông Dương suy sụp, tạo thời cơ khách quan thuận lợi."
                ]
            },
            {
                "heading": "b) Ý nghĩa lịch sử (Đối với Việt Nam & Thế giới)",
                "points": [
                    "Đối với dân tộc Việt Nam: Lật đổ ách cai trị của thực dân Pháp hơn 80 năm, quân phiệt Nhật gần 5 năm; chấm dứt chế độ quân chủ hơn 1000 năm; lập nên nước Việt Nam Dân chủ Cộng hòa — nhà nước dân chủ nhân dân đầu tiên ở Đông Nam Á.",
                    "Bước ngoặt nhảy vọt: Mở ra kỷ nguyên mới — kỷ nguyên độc lập, tự do và phát triển dưới chế độ dân chủ cộng hòa; nhân dân từ thân phận nô lệ trở thành người làm chủ đất nước; Đảng Cộng sản Đông Dương từ đảng hoạt động bí mật trở thành ĐẢNG CẦM QUYỀN; chuẩn bị tiền đề cho các thắng lợi tiếp theo.",
                    "Đối với thế giới: Góp phần vào thắng lợi chung của các lực lượng hòa bình, dân chủ, tiến bộ chống chủ nghĩa phát xít; góp phần làm tan rã hệ thống thuộc địa của chủ nghĩa thực dân (chọc thủng khâu yếu nhất); cổ vũ mạnh mẽ phong trào giải phóng dân tộc trên thế giới."
                ]
            },
            {
                "heading": "c) Bài học kinh nghiệm & Đặc điểm – Tính chất cần nhớ",
                "points": [
                    "4 Bài học kinh nghiệm: (1) Về sự lãnh đạo của Đảng (đường lối đúng đắn, vận dụng sáng tạo chủ nghĩa Mác - Lênin, chủ động linh hoạt); (2) Về xây dựng và phát huy khối đại đoàn kết toàn dân tộc (qua Mặt trận Việt Minh và các hình thức tập hợp quần chúng phong phú); (3) Về nắm bắt thời cơ (xác định đúng, chủ động, mau lẹ chớp thời cơ hành động); (4) Về kết hợp sức mạnh dân tộc với sức mạnh thời đại (nội lực giữ vai trò quyết định).",
                    "Tính chất: Là cuộc cách mạng giải phóng dân tộc điển hình, mang tính chất dân chủ mới (chưa phải cách mạng XHCN, chưa giải quyết triệt để vấn đề ruộng đất/tàn dư phong kiến).",
                    "Đặc điểm nghệ thuật khởi nghĩa: Kết hợp đấu tranh chính trị với vũ trang (LỰC LƯỢNG CHÍNH TRỊ QUYẾT ĐỊNH, lực lượng vũ trang làm nòng cốt); kết hợp nông thôn và thành thị (thắng lợi ở đô thị lớn có ý nghĩa quyết định); đi từ khởi nghĩa từng phần lên tổng khởi nghĩa; giành chính quyền nhanh chóng (15 ngày), ít đổ máu."
                ]
            }
        ]
    }
]

# ============================================================================
# 2. TIMELINE MILESTONES (12 mốc sống còn)
# ============================================================================
TIMELINE = [
    {
        "date": "9 & 12/3/1945",
        "short": "Nhật đảo chính Pháp & Chỉ thị 12/3",
        "tag": "Bước đệm",
        "detail": "Đêm 9/3/1945, Nhật đảo chính lật đổ Pháp độc chiếm Đông Dương. Ngày 12/3/1945, Ban Thường vụ Trung ương Đảng ra Chỉ thị \"Nhật - Pháp bắn nhau và hành động của chúng ta\", phát động Cao trào kháng Nhật cứu nước và khởi nghĩa từng phần.",
        "trap": "Thời điểm này thời cơ TỔNG khởi nghĩa CHƯA chín muồi (quân Nhật còn mạnh), mới chỉ là khởi nghĩa từng phần!"
    },
    {
        "date": "6 – 9/8/1945",
        "short": "Mỹ ném bom nguyên tử & Liên Xô đánh Nhật",
        "tag": "Thế giới",
        "detail": "Mỹ ném 2 quả bom nguyên tử xuống Hi-rô-si-ma (6/8) và Na-ga-xa-ki (9/8). Ngày 8–9/8, Hồng quân Liên Xô tuyên chiến và tấn công tiêu diệt đạo quân Quan Đông của Nhật ở Đông Bắc Trung Quốc.",
        "trap": "Đây là nhân tố KHÁCH QUAN đẩy Nhật đến bờ vực đầu hàng, không phải nguyên nhân quyết định thắng lợi của ta."
    },
    {
        "date": "13/8/1945",
        "short": "Ủy ban Khởi nghĩa ra Quân lệnh số 1",
        "tag": "Phát lệnh",
        "detail": "Trung ương Đảng và Tổng bộ Việt Minh thành lập Ủy ban Khởi nghĩa toàn quốc. Lúc 23 giờ cùng ngày, Ủy ban ban bố Quân lệnh số 1, chính thức phát lệnh Tổng khởi nghĩa trên cả nước.",
        "trap": "Đừng nhầm! Cơ quan ra Quân lệnh số 1 là ỦY BAN KHỞI NGHĨA TOÀN QUỐC (ra trước cả khi Nhật tuyên bố đầu hàng ngày 15/8)."
    },
    {
        "date": "14 – 15/8/1945",
        "short": "Hội nghị toàn quốc của Đảng (Tân Trào)",
        "tag": "Chủ trương",
        "detail": "Hội nghị toàn quốc của Đảng họp ở Tân Trào (Tuyên Quang), thông qua kế hoạch lãnh đạo toàn dân Tổng khởi nghĩa giành chính quyền trước khi quân Đồng minh vào; quyết định chính sách đối nội, đối ngoại.",
        "trap": "Hội nghị của ĐẢNG họp 14–15/8, còn ĐẠI HỘI QUỐC DÂN họp ngay sau đó 16–17/8!"
    },
    {
        "date": "15/8/1945",
        "short": "Nhật Bản đầu hàng Đồng minh vô điều kiện",
        "tag": "Thời cơ mở ra",
        "detail": "Nhật hoàng tuyên bố đầu hàng Đồng minh không điều kiện. Quân Nhật ở Đông Dương rệu rã, chính phủ Trần Trọng Kim hoang mang. Thời cơ \"ngàn năm có một\" chính thức xuất hiện.",
        "trap": "Thời cơ chỉ kéo dài từ 15/8 đến TRƯỚC KHI quân Đồng minh vào giải giáp quân Nhật (đầu tháng 9/1945)."
    },
    {
        "date": "16 – 17/8/1945",
        "short": "Đại hội Quốc dân Tân Trào & Giải phóng Thái Nguyên",
        "tag": "Đoàn kết",
        "detail": "Đại hội Quốc dân tán thành Tổng khởi nghĩa, thông qua 10 chính sách của Việt Minh, cử Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch. Chiều 16/8, Giải phóng quân do Võ Nguyên Giáp chỉ huy tiến về đánh chiếm thị xã Thái Nguyên.",
        "trap": "Ủy ban Dân tộc giải phóng Việt Nam (bầu tại Đại hội Quốc dân) là tiền thân của Chính phủ lâm thời."
    },
    {
        "date": "18/8/1945",
        "short": "4 tỉnh lị giành chính quyền SỚM NHẤT",
        "tag": "Mốc vàng",
        "detail": "Nhân dân 4 tỉnh Bắc Giang, Hải Dương, Hà Tĩnh và Quảng Nam giành được chính quyền ở tỉnh lị sớm nhất cả nước. Cùng ngày, Hồ Chí Minh viết Thư kêu gọi Tổng khởi nghĩa.",
        "trap": "Mẹo nhớ 4 tỉnh: BẮC - HẢI - HÀ - QUẢNG (Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam). Chú ý: đây là 4 TỈNH LỊ sớm nhất, còn ở cấp xã/huyện thì từ 14/8 đã có nơi giành chính quyền!"
    },
    {
        "date": "19/8/1945",
        "short": "Khởi nghĩa thắng lợi ở Hà Nội",
        "tag": "Đô thị 1",
        "detail": "Cuộc mít tinh lớn tại Nhà hát Lớn biến thành biểu tình vũ trang đánh chiếm Phủ Khâm sai, Tòa Thị chính, Trại Bảo an binh. Tối 19/8, khởi nghĩa thắng lợi hoàn toàn tại Thủ đô.",
        "trap": "19/8 là ngày kỷ niệm Cách mạng tháng Tám thành công, mang ý nghĩa cổ vũ và tác động quyết định tới các địa phương."
    },
    {
        "date": "23/8/1945",
        "short": "Khởi nghĩa thắng lợi ở Huế",
        "tag": "Đô thị 2",
        "detail": "Hàng vạn quần chúng nội, ngoại thành Huế tiến vào thành phố chiếm các công sở, giành chính quyền ngay tại kinh đô của triều đình phong kiến nhà Nguyễn.",
        "trap": "23/8 là giành chính quyền ở Huế, nhưng phải đến 30/8 vua Bảo Đại mới chính thức tuyên bố thoái vị!"
    },
    {
        "date": "25/8/1945",
        "short": "Khởi nghĩa thắng lợi ở Sài Gòn",
        "tag": "Đô thị 3",
        "detail": "Hơn 1 triệu quần chúng Sài Gòn – Chợ Lớn và các vùng phụ cận xuống đường biểu dương lực lượng, giành chính quyền thắng lợi ở trung tâm lớn nhất Nam Bộ.",
        "trap": "Nhớ chuỗi 3 đô thị lớn cách đều nhau: Hà Nội (19/8) → +4 ngày → Huế (23/8) → +2 ngày → Sài Gòn (25/8)!"
    },
    {
        "date": "28/8/1945",
        "short": "Đồng Nai Thượng & Hà Tiên — Thắng lợi cả nước",
        "tag": "Về đích",
        "detail": "Hai tỉnh cuối cùng trên đất liền là Đồng Nai Thượng và Hà Tiên giành chính quyền. Tổng khởi nghĩa hoàn thành trên phạm vi cả nước sau 15 ngày (14–28/8). Ủy ban Dân tộc giải phóng cải tổ thành Chính phủ lâm thời.",
        "trap": "Nhớ 2 tỉnh cuối: ĐỒNG NAI THƯỢNG & HÀ TIÊN (28/8). Tổng thời gian Tổng khởi nghĩa: 15 ngày!"
    },
    {
        "date": "30/8 & 2/9/1945",
        "short": "Bảo Đại thoái vị (30/8) & Tuyên ngôn Độc lập (2/9)",
        "tag": "Kỷ nguyên mới",
        "detail": "30/8: Vua Bảo Đại đọc chiếu thoái vị tại Huế, chấm dứt vĩnh viễn chế độ quân chủ hơn 1000 năm. 2/9: Chủ tịch Hồ Chí Minh đọc Tuyên ngôn Độc lập tại Quảng trường Ba Đình, khai sinh nước Việt Nam Dân chủ Cộng hòa.",
        "trap": "Hỏi mốc chấm dứt chế độ phong kiến → 30/8/1945! Hỏi mốc khai sinh nước VNDCCH / hoàn thành trọn vẹn CM tháng Tám → 2/9/1945!"
    }
]

# ============================================================================
# 3. 10 CLASSIC EXAM TRAPS
# ============================================================================
TRAPS = [
    {
        "num": 1,
        "title": "Kẻ thù trực tiếp bị đánh đổ trong tháng 8/1945",
        "wrong": "Giành chính quyền từ tay thực dân Pháp và phát xít Nhật.",
        "right": "Giành chính quyền từ tay PHÁT XÍT NHẬT và chính quyền tay sai thân Nhật (Trần Trọng Kim).",
        "why": "Thực dân Pháp đã bị Nhật đảo chính lật đổ từ đêm 9/3/1945 nên tháng 8/1945 ta giành chính quyền trực tiếp từ tay Nhật (dù ý nghĩa lịch sử là lật đổ ách thống trị hơn 80 năm của Pháp và gần 5 năm của Nhật)."
    },
    {
        "num": 2,
        "title": "Ai ban bố \"Quân lệnh số 1\" ngày 13/8/1945?",
        "wrong": "Hội nghị toàn quốc của Đảng hoặc Đại hội Quốc dân Tân Trào.",
        "right": "ỦY BAN KHỞI NGHĨA TOÀN QUỐC (do Trung ương Đảng và Tổng bộ Việt Minh lập ra ngày 13/8).",
        "why": "Mốc ngày rất rõ: 13/8 lập Ủy ban Khởi nghĩa & ra Quân lệnh số 1 → 14–15/8 Hội nghị toàn quốc của Đảng → 16–17/8 Đại hội Quốc dân."
    },
    {
        "num": 3,
        "title": "Khoảng thời gian của \"Thời cơ ngàn năm có một\"",
        "wrong": "Từ khi Nhật đảo chính Pháp (9/3/1945) hoặc kéo dài đến cuối năm 1945.",
        "right": "Từ khi Nhật đầu hàng Đồng minh (15/8/1945) đến TRƯỚC KHI quân Đồng minh kéo vào Đông Dương (đầu 9/1945).",
        "why": "Nếu khởi nghĩa trước 15/8 khi Nhật chưa thua hẳn thì địch còn mạnh; nếu để sau khi quân Đồng minh (Anh, Tưởng) kéo vào thì sẽ vấp phải kẻ thù mới."
    },
    {
        "num": 4,
        "title": "Nơi giành chính quyền sớm nhất vs 4 tỉnh lị sớm nhất",
        "wrong": "Ngày 18/8 mới bắt đầu nổ ra khởi nghĩa giành chính quyền ở Việt Nam.",
        "right": "Từ 14/8 đã có nhiều xã, huyện giành chính quyền; còn 18/8 là 4 TỈNH LỊ sớm nhất (Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam).",
        "why": "Đọc kỹ đề: hỏi 'bắt đầu nổ ra ở cơ sở' → 14/8; hỏi '4 tỉnh giành chính quyền ở tỉnh lị sớm nhất' → 18/8."
    },
    {
        "num": 5,
        "title": "Mốc chấm dứt hoàn toàn chế độ quân chủ (phong kiến)",
        "wrong": "Ngày 19/8 (Hà Nội), ngày 23/8 (Huế) hoặc ngày 2/9 (Tuyên ngôn Độc lập).",
        "right": "Ngày 30/8/1945 — sự kiện vua Bảo Đại tuyên bố thoái vị, trao ấn kiếm tại Huế.",
        "why": "Huế giành chính quyền 23/8, nhưng phải đến chiều 30/8 vua Bảo Đại mới chính thức đọc chiếu thoái vị, đặt dấu chấm hết cho chế độ quân chủ hơn 1000 năm."
    },
    {
        "num": 6,
        "title": "Lực lượng giữ vai trò QUYẾT ĐỊNH trong Tổng khởi nghĩa",
        "wrong": "Lực lượng vũ trang (Giải phóng quân) quyết định, lực lượng chính trị hỗ trợ.",
        "right": "LỰC LƯỢNG CHÍNH TRỊ của quần chúng nhân dân quyết định; lực lượng vũ trang làm nòng cốt, xung kích.",
        "why": "Quần chúng đông đảo (hàng chục vạn, hàng triệu người) xuống đường mít tinh, biểu tình làm tê liệt quân địch là nhân tố tạo nên thắng lợi nhanh chóng, ít đổ máu."
    },
    {
        "num": 7,
        "title": "Nguyên nhân QUYẾT ĐỊNH nhất dẫn đến thắng lợi",
        "wrong": "Chiến thắng của Hồng quân Liên Xô và quân Đồng minh đánh bại phát xít Nhật.",
        "right": "Nguyên nhân CHỦ QUAN — đứng đầu là sự lãnh đạo đúng đắn, sáng suốt của Đảng Cộng sản Đông Dương và Chủ tịch Hồ Chí Minh.",
        "why": "Chiến thắng của Liên Xô và Đồng minh là nguyên nhân KHÁCH QUAN tạo điều kiện/thời cơ thuận lợi. Ở Đông Nam Á lúc đó nhiều nước cùng có điều kiện khách quan này nhưng chỉ Việt Nam, In-đô-nê-xi-a, Lào giành độc lập kịp thời!"
    },
    {
        "num": 8,
        "title": "Xóa bỏ chế độ quân chủ ≠ Xóa bỏ hết tàn dư phong kiến",
        "wrong": "Cách mạng tháng Tám đã xóa bỏ hoàn toàn mọi tàn dư phong kiến và hoàn thành cách mạng ruộng đất.",
        "right": "Mới chấm dứt chế độ QUÂN CHỦ (nhà nước phong kiến), CHƯA xóa bỏ hoàn toàn tàn dư phong kiến (vấn đề ruộng đất chưa giải quyết triệt để).",
        "why": "Đảng tạm gác khẩu hiệu cách mạng ruộng đất để tập trung tối đa cho nhiệm vụ giải phóng dân tộc và mở rộng khối đại đoàn kết trong Mặt trận Việt Minh."
    },
    {
        "num": 9,
        "title": "Tính chất của Cách mạng tháng Tám năm 1945",
        "wrong": "Cách mạng xã hội chủ nghĩa hoặc cách mạng tư sản kiểu cũ.",
        "right": "Cách mạng GIẢI PHÓNG DÂN TỘC (điển hình) mang tính chất DÂN CHỦ MỚI.",
        "why": "Mục tiêu hàng đầu là đánh đổ đế quốc, phát xít, giành độc lập dân tộc; đồng thời lập chế độ dân chủ cộng hòa, mang lại quyền làm chủ cho nhân dân."
    },
    {
        "num": 10,
        "title": "Nhật đầu hàng Đồng minh ≠ Quân Nhật bị tiêu diệt hết ngay lập tức",
        "wrong": "Ngày 15/8, quân Nhật ở Đông Dương bị tiêu diệt hoàn toàn nên ta chỉ việc tiếp quản.",
        "right": "Quân Nhật ở Đông Dương RỆU RÃ, hoang mang nhưng vẫn còn vũ khí và lực lượng; ta vẫn phải kiên quyết chớp thời cơ khởi nghĩa giành chính quyền.",
        "why": "Nhiều câu Đúng/Sai cố tình đổi từ 'rệu rã, hoang mang' thành 'bị tiêu diệt hoàn toàn' hoặc 'tự động trao trả chính quyền cho Việt Minh' — gặp là chọn SAI ngay!"
    }
]

# ============================================================================
# 4. PRIMARY HISTORICAL SOURCES (4 đoạn tư liệu vàng chuẩn SGK)
# ============================================================================
SOURCES = [
    {
        "id": "src-1",
        "title": "Tư liệu 1 • Quân lệnh số 1 (13/8/1945)",
        "meta": "Ủy ban Khởi nghĩa toàn quốc — 23 giờ ngày 13/8/1945",
        "quote": "“Giờ tổng khởi nghĩa đã đánh! Cơ hội có một cho quân dân Việt Nam vùng dậy giành lấy quyền độc lập của nước nhà!... Chúng ta phải hành động cho nhanh, với một tinh thần vô cùng quả cảm, vô cùng thận trọng! Cuộc thắng lợi hoàn toàn nhất định sẽ về ta!”",
        "takeaway": "Thể hiện sự nhạy bén, quyết đoán tuyệt vời của Trung ương Đảng và Tổng bộ Việt Minh trong việc phát động Tổng khởi nghĩa kịp thời."
    },
    {
        "id": "src-2",
        "title": "Tư liệu 2 • Thư kêu gọi Tổng khởi nghĩa (18/8/1945)",
        "meta": "Chủ tịch Hồ Chí Minh — Tháng 8 năm 1945",
        "quote": "“Hỡi đồng bào yêu quý! Giờ quyết định cho vận mệnh dân tộc ta đã đến. Toàn quốc đồng bào hãy đứng dậy đem sức ta mà tự giải phóng cho ta... Chúng ta không thể chậm trễ. Tiến lên! Tiến lên! Dưới lá cờ Việt Minh, đồng bào hãy dũng cảm tiến lên!”",
        "takeaway": "Nhấn mạnh tinh thần tự lực tự cường ('đem sức ta mà tự giải phóng cho ta'), khối đại đoàn kết dưới ngọn cờ Mặt trận Việt Minh và tính khẩn trương chớp thời cơ."
    },
    {
        "id": "src-3",
        "title": "Tư liệu 3 • Tuyên ngôn Độc lập (2/9/1945)",
        "meta": "Chủ tịch Hồ Chí Minh đọc tại Quảng trường Ba Đình, Hà Nội",
        "quote": "“Nước Việt Nam có quyền hưởng tự do và độc lập, và sự thật đã thành một nước tự do độc lập. Toàn thể dân tộc Việt Nam quyết đem tất cả tinh thần và lực lượng, tính mạng và của cải để giữ vững quyền tự do, độc lập ấy.”",
        "takeaway": "Khai sinh nước Việt Nam Dân chủ Cộng hòa — nhà nước dân chủ nhân dân đầu tiên ở Đông Nam Á, mở ra kỷ nguyên độc lập, tự do."
    },
    {
        "id": "src-4",
        "title": "Tư liệu 4 • Đánh giá tầm vóc Cách mạng tháng Tám",
        "meta": "Chủ tịch Hồ Chí Minh (Báo cáo Chính trị tại Đại hội II của Đảng, 1951 — trích SGK KNTT)",
        "quote": "“Chẳng những giai cấp lao động và nhân dân Việt Nam ta có thể tự hào, mà giai cấp lao động và những dân tộc bị áp bức nơi khác cũng có thể tự hào rằng: Lần này là lần đầu tiên trong lịch sử cách mạng của các dân tộc thuộc địa và nửa thuộc địa, một Đảng mới 15 tuổi đã lãnh đạo cách mạng thành công, đã nắm chính quyền toàn quốc.”",
        "takeaway": "Khẳng định 2 ý lớn: (1) Năng lực lãnh đạo tài tình của Đảng Cộng sản Đông Dương (1930–1945: 15 tuổi); (2) Tầm vóc và sức cổ vũ quốc tế to lớn đối với các dân tộc thuộc địa."
    }
]

# ============================================================================
# 5. 24 SPEED FLASHCARDS
# ============================================================================
FLASHCARDS = [
    {"id": "fc-1", "cat": "boi-canh", "front": "Ngày 15/8/1945 xảy ra sự kiện quốc tế quyết định nào?", "back": "Nhật Bản tuyên bố đầu hàng Đồng minh không điều kiện → Chiến tranh thế giới thứ hai kết thúc, thời cơ ngàn năm có một xuất hiện."},
    {"id": "fc-2", "cat": "boi-canh", "front": "Hai đòn giáng quyết định đầu tháng 8/1945 buộc Nhật phải đầu hàng?", "back": "Mỹ ném 2 quả bom nguyên tử xuống Hi-rô-si-ma (6/8) và Na-ga-xa-ki (9/8); Hồng quân Liên Xô đánh tan đạo quân Quan Đông (8–9/8)."},
    {"id": "fc-3", "cat": "boi-canh", "front": "Thời cơ \"ngàn năm có một\" tồn tại trong khoảng thời gian nào?", "back": "Từ khi Nhật đầu hàng Đồng minh (15/8/1945) đến TRƯỚC KHI quân Đồng minh vào Đông Dương giải giáp quân Nhật (đầu 9/1945)."},
    {"id": "fc-4", "cat": "boi-canh", "front": "Cơ quan nào thành lập ngày 13/8/1945 và ban bố Quân lệnh số 1?", "back": "Ủy ban Khởi nghĩa toàn quốc (do Trung ương Đảng và Tổng bộ Việt Minh thành lập)."},
    {"id": "fc-5", "cat": "boi-canh", "front": "Hội nghị toàn quốc của Đảng (14–15/8/1945) họp ở đâu và quyết định gì?", "back": "Họp tại Tân Trào (Tuyên Quang): phát động Tổng khởi nghĩa giành chính quyền trước khi quân Đồng minh vào; quyết định chính sách đối nội, đối ngoại."},
    {"id": "fc-6", "cat": "boi-canh", "front": "Đại hội Quốc dân Tân Trào (16–17/8/1945) đã bầu ra cơ quan nào?", "back": "Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch (cùng việc tán thành Tổng khởi nghĩa, thông qua 10 chính sách của Việt Minh)."},
    {"id": "fc-7", "cat": "boi-canh", "front": "Câu nói \"Đem sức ta mà tự giải phóng cho ta\" nằm trong văn kiện nào?", "back": "Thư kêu gọi Tổng khởi nghĩa của Chủ tịch Hồ Chí Minh (tháng 8/1945 — ngày 18/8/1945)."},
    {"id": "fc-8", "cat": "boi-canh", "front": "Bước tập dượt trực tiếp cho Tổng khởi nghĩa diễn ra từ tháng 3 đến 8/1945 là gì?", "back": "Cao trào kháng Nhật cứu nước (khởi đầu sau sự kiện Nhật đảo chính Pháp 9/3 và Chỉ thị \"Nhật - Pháp bắn nhau...\" 12/3/1945)."},
    {"id": "fc-9", "cat": "dien-bien", "front": "Chiều 16/8/1945, Giải phóng quân do Võ Nguyên Giáp chỉ huy tiến về đánh chiếm nơi nào?", "back": "Thị xã Thái Nguyên (xuất phát từ Tân Trào, mở đầu cuộc Tổng khởi nghĩa bằng lực lượng vũ trang)."},
    {"id": "fc-10", "cat": "dien-bien", "front": "4 tỉnh giành chính quyền ở tỉnh lị SỚM NHẤT cả nước (18/8/1945)?", "back": "Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam (Mẹo nhớ: BẮC - HẢI - HÀ - QUẢNG)."},
    {"id": "fc-11", "cat": "dien-bien", "front": "Mốc giành chính quyền tại 3 đô thị lớn: Hà Nội, Huế, Sài Gòn?", "back": "Hà Nội: 19/8/1945 → Huế: 23/8/1945 → Sài Gòn: 25/8/1945."},
    {"id": "fc-12", "cat": "dien-bien", "front": "2 tỉnh cuối cùng trên đất liền giành chính quyền ngày 28/8/1945?", "back": "Đồng Nai Thượng và Hà Tiên → Đánh dấu Tổng khởi nghĩa thắng lợi trên phạm vi cả nước sau 15 ngày (14–28/8)."},
    {"id": "fc-13", "cat": "dien-bien", "front": "Sự kiện nào ngày 30/8/1945 chấm dứt hoàn toàn chế độ quân chủ Việt Nam?", "back": "Vua Bảo Đại đọc chiếu thoái vị và trao ấn kiếm cho đại diện Chính phủ lâm thời tại Ngọ Môn (Huế)."},
    {"id": "fc-14", "cat": "dien-bien", "front": "Sự kiện ngày 2/9/1945 tại Quảng trường Ba Đình (Hà Nội)?", "back": "Chủ tịch Hồ Chí Minh đọc bản Tuyên ngôn Độc lập, khai sinh nước Việt Nam Dân chủ Cộng hòa."},
    {"id": "fc-15", "cat": "nguyen-nhan-y-nghia", "front": "Nhân tố QUYẾT ĐỊNH HÀNG ĐẦU đưa đến thắng lợi Cách mạng tháng Tám?", "back": "Sự lãnh đạo đúng đắn, sáng suốt, tài tình của Đảng Cộng sản Đông Dương, đứng đầu là Chủ tịch Hồ Chí Minh."},
    {"id": "fc-16", "cat": "nguyen-nhan-y-nghia", "front": "Nguyên nhân KHÁCH QUAN của Cách mạng tháng Tám là gì? Vai trò của nó?", "back": "Chiến thắng của Hồng quân Liên Xô và Đồng minh chống phát xít Nhật → Chỉ tạo điều kiện/thời cơ thuận lợi, KHÔNG quyết định thay nội lực."},
    {"id": "fc-17", "cat": "nguyen-nhan-y-nghia", "front": "Cách mạng tháng Tám lật đổ ách cai trị của những thế lực nào (và bao lâu)?", "back": "Thực dân Pháp (hơn 80 năm), quân phiệt Nhật (gần 5 năm), chế độ quân chủ phong kiến (hơn 1000 năm)."},
    {"id": "fc-18", "cat": "nguyen-nhan-y-nghia", "front": "Địa vị của Đảng và nhân dân thay đổi thế nào sau Cách mạng tháng Tám?", "back": "Đảng: từ đảng bí mật → ĐẢNG CẦM QUYỀN. Nhân dân: từ thân phận nô lệ → NGƯỜI LÀM CHỦ đất nước."},
    {"id": "fc-19", "cat": "nguyen-nhan-y-nghia", "front": "Ý nghĩa quốc tế cốt lõi của Cách mạng tháng Tám năm 1945?", "back": "Góp phần đánh bại chủ nghĩa phát xít, làm tan rã hệ thống thuộc địa của chủ nghĩa thực dân và cổ vũ phong trào giải phóng dân tộc thế giới."},
    {"id": "fc-20", "cat": "nguyen-nhan-y-nghia", "front": "Nhà nước Việt Nam Dân chủ Cộng hòa có vị thế gì ở Đông Nam Á?", "back": "Là nhà nước dân chủ nhân dân (công nông) ĐẦU TIÊN ở khu vực Đông Nam Á."},
    {"id": "fc-21", "cat": "bai-hoc-tinh-chat", "front": "4 bài học kinh nghiệm lớn của Cách mạng tháng Tám năm 1945?", "back": "(1) Sự lãnh đạo của Đảng; (2) Xây dựng, phát huy khối đại đoàn kết dân tộc; (3) Nắm bắt, chớp thời cơ; (4) Kết hợp sức mạnh dân tộc với sức mạnh thời đại."},
    {"id": "fc-22", "cat": "bai-hoc-tinh-chat", "front": "Tính chất điển hình của Cách mạng tháng Tám năm 1945?", "back": "Cách mạng giải phóng dân tộc mang tính chất dân chủ mới (KHÔNG phải cách mạng XHCN, chưa xóa bỏ hết tàn dư ruộng đất phong kiến)."},
    {"id": "fc-23", "cat": "bai-hoc-tinh-chat", "front": "Trong Tổng khởi nghĩa tháng Tám, lực lượng nào giữ vai trò QUYẾT ĐỊNH?", "back": "Lực lượng CHÍNH TRỊ của quần chúng nhân dân giữ vai trò quyết định; lực lượng vũ trang giữ vai trò nòng cốt, xung kích."},
    {"id": "fc-24", "cat": "bai-hoc-tinh-chat", "front": "Kẻ thù TRỰC TIẾP mà nhân dân ta giành chính quyền trong tháng 8/1945 là ai?", "back": "Phát xít Nhật và chính quyền tay sai thân Nhật (Trần Trọng Kim) — vì Pháp đã bị Nhật đảo chính lật đổ từ 9/3/1945!"}
]

# ============================================================================
# 6. 52 MULTIPLE CHOICE QUESTIONS (Phần I — 4 lựa chọn)
#    Fields: id, cat, level ('NB'|'TH'|'VD'), trap (bool), question, options[4], answer (0..3), explanation, tip
# ============================================================================
MC_QUESTIONS = [
    # ---- CHỦ ĐỀ 1: BỐI CẢNH & THỜI CƠ (14 câu: mc-01 .. mc-14) ----
    {
        "id": "mc-01", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Sự kiện nào sau đây đã tạo ra thời cơ khách quan thuận lợi nhất cho nhân dân Việt Nam đứng lên Tổng khởi nghĩa tháng Tám năm 1945?",
        "options": [
            "Phát xít Đức đầu hàng Đồng minh không điều kiện (5/1945).",
            "Nhật Bản tuyên bố đầu hàng Đồng minh không điều kiện (15/8/1945).",
            "Quân phiệt Nhật đảo chính lật đổ thực dân Pháp ở Đông Dương (9/3/1945).",
            "Liên Xô và Mỹ thỏa thuận chấm dứt Chiến tranh lạnh."
        ],
        "answer": 1,
        "explanation": "Ngày 15/8/1945, Nhật Bản tuyên bố đầu hàng Đồng minh không điều kiện khiến quân Nhật ở Đông Dương rệu rã, chính phủ thân Nhật Trần Trọng Kim hoang mang. Đây là thời cơ khách quan thuận lợi nhất cho cuộc Tổng khởi nghĩa.",
        "tip": "Nhớ mốc 15/8/1945: Nhật đầu hàng vô điều kiện = thời cơ Tổng khởi nghĩa mở ra!"
    },
    {
        "id": "mc-02", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Đầu tháng 8 năm 1945, hai đòn tấn công quyết định của lực lượng Đồng minh buộc quân phiệt Nhật Bản phải đầu hàng không điều kiện là",
        "options": [
            "Mỹ ném bom nguyên tử xuống Nhật Bản và Hồng quân Liên Xô đánh tan đạo quân Quan Đông.",
            "quân Anh đổ bộ vào Đông Dương và quân Pháp phản công giải phóng Pa-ri.",
            "Mỹ đổ bộ lên Bắc Phi và Hồng quân Liên Xô giải phóng Béc-lin.",
            "quân Trung Hoa Dân quốc tổng phản công và quân Anh giải phóng Miến Điện."
        ],
        "answer": 0,
        "explanation": "Ngày 6 và 9/8/1945, Mỹ ném hai quả bom nguyên tử xuống Hi-rô-si-ma và Na-ga-xa-ki; ngày 8–9/8/1945, Hồng quân Liên Xô tuyên chiến và tấn công tiêu diệt đạo quân Quan Đông của Nhật ở Đông Bắc Trung Quốc, buộc Nhật đầu hàng ngày 15/8/1945.",
        "tip": "Cặp sự kiện đầu tháng 8/1945: Mỹ (2 bom nguyên tử 6 & 9/8) + Liên Xô (đạo quân Quan Đông 8–9/8)."
    },
    {
        "id": "mc-03", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Ngay sau khi Nhật Bản tuyên bố đầu hàng Đồng minh (15/8/1945), tình hình kẻ thù của cách mạng ở Đông Dương như thế nào?",
        "options": [
            "Quân Nhật vẫn giữ nguyên sức mạnh và mở cuộc càn quét lớn vào Việt Bắc.",
            "Thực dân Pháp lập tức khôi phục lại hoàn toàn bộ máy cai trị trên cả nước.",
            "Quân Nhật ở Đông Dương rệu rã, chính phủ thân Nhật Trần Trọng Kim hoang mang, tê liệt.",
            "Quân Đồng minh đã kịp thời tiến vào giải giáp toàn bộ quân Nhật ở Hà Nội."
        ],
        "answer": 2,
        "explanation": "Khi Nhật Hoàng tuyên bố đầu hàng Đồng minh (15/8/1945), quân đội Nhật ở Đông Dương rệu rã, mất tinh thần chiến đấu, còn chính phủ thân Nhật Trần Trọng Kim hoang mang, dao động cực độ.",
        "tip": "Từ khóa chuẩn SGK: quân Nhật 'rệu rã', chính phủ Trần Trọng Kim 'hoang mang'."
    },
    {
        "id": "mc-04", "cat": "boi-canh", "level": "TH", "trap": True,
        "question": "Thời cơ \"ngàn năm có một\" của Cách mạng tháng Tám năm 1945 chỉ tồn tại trong khoảng thời gian nào sau đây?",
        "options": [
            "Từ khi Nhật đảo chính Pháp (9/3/1945) đến khi Nhật đầu hàng Đồng minh (15/8/1945).",
            "Từ khi Chiến tranh thế giới thứ hai bùng nổ (9/1939) đến khi kết thúc (8/1945).",
            "Từ khi phát xít Đức đầu hàng (5/1945) đến khi Cách mạng tháng Tám thành công.",
            "Từ khi Nhật đầu hàng Đồng minh (15/8/1945) đến trước khi quân Đồng minh vào Đông Dương."
        ],
        "answer": 3,
        "explanation": "Thời cơ vàng xuất hiện cực kỳ ngắn ngủi: kẻ thù trực tiếp (Nhật) đã đầu hàng và rệu rã (15/8/1945), trong khi kẻ thù mới (quân Đồng minh: Anh, Trung Hoa Dân quốc, đằng sau là Pháp) chưa kịp kéo vào Đông Dương (đầu tháng 9/1945).",
        "tip": "BẪY KINH ĐIỂN: Thời cơ KHÔNG bắt đầu từ 9/3/1945 mà chỉ từ 15/8 đến TRƯỚC KHI quân Đồng minh vào!"
    },
    {
        "id": "mc-05", "cat": "boi-canh", "level": "TH", "trap": False,
        "question": "Vì sao Đảng Cộng sản Đông Dương xác định phải tiến hành Tổng khởi nghĩa giành chính quyền trước khi quân Đồng minh tiến vào Đông Dương?",
        "options": [
            "Để kịp thời tranh thủ viện trợ vũ khí trực tiếp từ quân đội Nhật Bản.",
            "Để tránh phải đối đầu với những thế lực đế quốc mới và đón quân Đồng minh với tư cách người chủ đất nước.",
            "Vì theo thỏa thuận của Hội nghị I-an-ta, quân Đồng minh sẽ trao trả độc lập ngay nếu ta khởi nghĩa sớm.",
            "Vì sau tháng 8/1945, lực lượng vũ trang của Việt Minh sẽ bị giải thể theo yêu cầu của Liên Hợp Quốc."
        ],
        "answer": 1,
        "explanation": "Nếu giành được chính quyền từ tay Nhật trước khi quân Đồng minh kéo vào, nhân dân Việt Nam sẽ đứng ở vị thế chủ nhân của một nước độc lập để đón quân Đồng minh vào giải giáp quân Nhật, tránh nguy cơ Pháp núp bóng Đồng minh tái chiếm ngay lập tức.",
        "tip": "Kẻ thù cũ đã gục, kẻ thù mới chưa kịp đến → giành chính quyền để làm chủ nhà trước khi Đồng minh vào!"
    },
    {
        "id": "mc-06", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Trong khoảng thời gian từ tháng 3 đến giữa tháng 8 năm 1945, phong trào đấu tranh nào ở Việt Nam đã trực tiếp chuẩn bị lực lượng và tập dượt cho Tổng khởi nghĩa tháng Tám?",
        "options": [
            "Phong trào dân chủ 1936 – 1939.",
            "Cao trào kháng Nhật cứu nước.",
            "Phong trào Xô viết Nghệ - Tĩnh.",
            "Phong trào \"Phá kho thóc giải quyết nạn đói\" sau ngày 2/9/1945."
        ],
        "answer": 1,
        "explanation": "Sau khi Nhật đảo chính Pháp (9/3/1945) và Ban Thường vụ Trung ương Đảng ra Chỉ thị \"Nhật - Pháp bắn nhau và hành động của chúng ta\" (12/3/1945), Cao trào kháng Nhật cứu nước diễn ra sôi nổi từ tháng 3 đến giữa tháng 8/1945, là cuộc tập dượt trực tiếp cho Tổng khởi nghĩa.",
        "tip": "Tháng 3 → 8/1945 = Cao trào kháng Nhật cứu nước (khởi nghĩa từng phần)."
    },
    {
        "id": "mc-07", "cat": "boi-canh", "level": "NB", "trap": True,
        "question": "Ngày 13 tháng 8 năm 1945, ngay khi nhận được những thông tin về việc Nhật Bản sắp đầu hàng Đồng minh, Trung ương Đảng và Tổng bộ Việt Minh đã thành lập cơ quan nào và ban bố văn kiện gì?",
        "options": [
            "Ủy ban Dân tộc giải phóng Việt Nam và ban bố Tuyên ngôn Độc lập.",
            "Chính phủ lâm thời và ban bố 10 chính sách lớn của Việt Minh.",
            "Ủy ban Khởi nghĩa toàn quốc và ban bố Quân lệnh số 1.",
            "Hội nghị toàn quốc của Đảng và ban bố Chỉ thị Nhật - Pháp bắn nhau."
        ],
        "answer": 2,
        "explanation": "Đêm 13/8/1945, Trung ương Đảng và Tổng bộ Việt Minh thành lập Ủy ban Khởi nghĩa toàn quốc; đến 23 giờ cùng ngày, Ủy ban Khởi nghĩa toàn quốc ban bố Quân lệnh số 1, chính thức phát lệnh Tổng khởi nghĩa trong cả nước.",
        "tip": "BẪY HAY NHẦM: 13/8 = Ủy ban Khởi nghĩa toàn quốc + Quân lệnh số 1 (KHÔNG phải Ủy ban Dân tộc giải phóng!)."
    },
    {
        "id": "mc-08", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Hội nghị toàn quốc của Đảng Cộng sản Đông Dương họp tại Tân Trào (Tuyên Quang) từ ngày 14 đến ngày 15 tháng 8 năm 1945 đã thông qua quyết định trọng đại nào?",
        "options": [
            "Phát động Tổng khởi nghĩa giành chính quyền trong cả nước trước khi quân Đồng minh vào.",
            "Thành lập Mặt trận Việt Nam Độc lập Đồng minh (Việt Minh).",
            "Phát động cuộc kháng chiến toàn quốc chống thực dân Pháp xâm lược.",
            "Thành lập Đội Việt Nam Tuyên truyền Giải phóng quân."
        ],
        "answer": 0,
        "explanation": "Hội nghị toàn quốc của Đảng (14–15/8/1945) tại Tân Trào đã thông qua kế hoạch lãnh đạo toàn dân Tổng khởi nghĩa giành chính quyền trước khi quân Đồng minh vào Đông Dương và quyết định những vấn đề quan trọng về đối nội, đối ngoại sau khi giành chính quyền.",
        "tip": "14–15/8 = Hội nghị toàn quốc của Đảng (kế hoạch Tổng khởi nghĩa + đối nội, đối ngoại)."
    },
    {
        "id": "mc-09", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Đại hội Quốc dân họp tại Tân Trào (16 – 17/8/1945) KHÔNG thông qua nội dung nào dưới đây?",
        "options": [
            "Tán thành chủ trương Tổng khởi nghĩa của Đảng.",
            "Thông qua 10 chính sách lớn của Mặt trận Việt Minh.",
            "Cử ra Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch.",
            "Thông qua Hiến pháp đầu tiên của nước Việt Nam Dân chủ Cộng hòa."
        ],
        "answer": 3,
        "explanation": "Đại hội Quốc dân Tân Trào (16–17/8/1945) tán thành chủ trương Tổng khởi nghĩa, thông qua 10 chính sách của Việt Minh, quy định Quốc kì, Quốc ca và bầu Ủy ban Dân tộc giải phóng Việt Nam. Hiến pháp đầu tiên được Quốc hội khóa I thông qua sau này (11/1946).",
        "tip": "Đọc kỹ chữ KHÔNG! Hiến pháp đầu tiên là năm 1946, không phải ở Tân Trào 8/1945."
    },
    {
        "id": "mc-10", "cat": "boi-canh", "level": "NB", "trap": True,
        "question": "Cơ quan nào được bầu ra tại Đại hội Quốc dân Tân Trào (16 – 17/8/1945) và đóng vai trò tiền thân của Chính phủ lâm thời nước Việt Nam Dân chủ Cộng hòa?",
        "options": [
            "Ủy ban Khởi nghĩa toàn quốc.",
            "Ủy ban Dân tộc giải phóng Việt Nam.",
            "Tổng bộ Việt Minh.",
            "Ủy ban Quân sự cách mạng Bắc Kỳ."
        ],
        "answer": 1,
        "explanation": "Đại hội Quốc dân Tân Trào đã cử ra Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch. Đến ngày 28/8/1945, cơ quan này được cải tổ thành Chính phủ lâm thời nước Việt Nam Dân chủ Cộng hòa.",
        "tip": "Phân biệt 2 Ủy ban: 13/8 = Ủy ban Khởi nghĩa toàn quốc (phát lệnh); 16–17/8 = Ủy ban Dân tộc giải phóng VN (tiền thân Chính phủ)."
    },
    {
        "id": "mc-11", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Lời kêu gọi lịch sử: \"Giờ quyết định cho vận mệnh dân tộc ta đã đến. Toàn quốc đồng bào hãy đứng dậy đem sức ta mà tự giải phóng cho ta\" được Chủ tịch Hồ Chí Minh viết trong văn kiện nào?",
        "options": [
            "Bản Tuyên ngôn Độc lập (2/9/1945).",
            "Lời kêu gọi toàn quốc kháng chiến (19/12/1946).",
            "Thư kêu gọi Tổng khởi nghĩa (tháng 8/1945).",
            "Chỉ thị Nhật - Pháp bắn nhau và hành động của chúng ta (12/3/1945)."
        ],
        "answer": 2,
        "explanation": "Ngày 18/8/1945, Chủ tịch Hồ Chí Minh gửi Thư kêu gọi Tổng khởi nghĩa tới đồng bào cả nước với câu nói bất hủ: \"Giờ quyết định cho vận mệnh dân tộc ta đã đến. Toàn quốc đồng bào hãy đứng dậy đem sức ta mà tự giải phóng cho ta\".",
        "tip": "Gặp câu 'đem sức ta mà tự giải phóng cho ta' → Thư kêu gọi Tổng khởi nghĩa (tháng 8/1945)."
    },
    {
        "id": "mc-12", "cat": "boi-canh", "level": "TH", "trap": True,
        "question": "Vì sao khi Nhật đảo chính Pháp (9/3/1945), Đảng Cộng sản Đông Dương chưa phát động Tổng khởi nghĩa mà chỉ phát động cao trào kháng Nhật cứu nước và khởi nghĩa từng phần?",
        "options": [
            "Vì thực dân Pháp vẫn còn nắm giữ phần lớn quân đội mạnh ở Bắc Bộ.",
            "Vì quân phiệt Nhật còn mạnh, lực lượng trung gian chưa ngả hẳn về phía cách mạng, điều kiện Tổng khởi nghĩa chưa chín muồi.",
            "Vì Mặt trận Việt Minh chưa được thành lập nên chưa tập hợp được lực lượng quần chúng.",
            "Vì Hồng quân Liên Xô yêu cầu Việt Nam chờ quân Đồng minh vào mới được khởi nghĩa."
        ],
        "answer": 1,
        "explanation": "Tháng 3/1945, Nhật vừa đảo chính lật đổ Pháp nên quân Nhật vẫn còn rất mạnh, chính quyền địch chưa tê liệt, lực lượng trung gian còn dao động. Vì thế điều kiện Tổng khởi nghĩa chưa chín muồi — Đảng chỉ phát động cao trào kháng Nhật và khởi nghĩa từng phần để chuẩn bị thời cơ.",
        "tip": "So sánh 9/3 vs 15/8: 9/3 Nhật còn MẠNH → khởi nghĩa từng phần; 15/8 Nhật ĐẦU HÀNG, RỆU RÃ → Tổng khởi nghĩa!"
    },
    {
        "id": "mc-13", "cat": "boi-canh", "level": "NB", "trap": False,
        "question": "Thắng lợi của Cách mạng tháng Tám năm 1945 là kết quả trực tiếp của quá trình chuẩn bị chu đáo về đường lối và lực lượng của Đảng Cộng sản Đông Dương trong suốt bao nhiêu năm?",
        "options": [
            "5 năm (1940 – 1945).",
            "10 năm (1935 – 1945).",
            "15 năm (1930 – 1945).",
            "20 năm (1925 – 1945)."
        ],
        "answer": 2,
        "explanation": "Từ khi thành lập (1930) đến tháng 8/1945 là tròn 15 năm Đảng lãnh đạo chuẩn bị chu đáo qua 3 phong trào cách mạng lớn (1930–1931, 1936–1939 và 1939–1945).",
        "tip": "Nhớ mốc 15 năm (1930–1945) — trùng câu của Bác Hồ: 'một Đảng mới 15 tuổi đã lãnh đạo cách mạng thành công'!"
    },
    {
        "id": "mc-14", "cat": "boi-canh", "level": "TH", "trap": False,
        "question": "Sự kiện Trung ương Đảng và Tổng bộ Việt Minh phát lệnh Tổng khởi nghĩa (đêm 13/8/1945) — ngay cả trước khi Nhật hoàng chính thức đọc tuyên bố đầu hàng (trưa 15/8/1945) — chứng tỏ điều gì?",
        "options": [
            "Sự nóng vội, chủ quan khi chưa đánh giá kỹ tương quan lực lượng.",
            "Sự nhạy bén, quyết đoán và bản lĩnh chủ động chớp thời cơ của Đảng.",
            "Sự phụ thuộc hoàn toàn vào chỉ đạo từ bên ngoài của các nước Đồng minh.",
            "Quân Nhật ở Việt Nam đã bí mật ký thỏa thuận đầu hàng riêng với Việt Minh từ 13/8."
        ],
        "answer": 1,
        "explanation": "Vừa nắm được tin Nhật chuẩn bị đầu hàng (sau khi Mỹ ném bom nguyên tử và Liên Xô đánh tan đạo quân Quan Đông), Đảng lập tức thành lập Ủy ban Khởi nghĩa và ban bố Quân lệnh số 1 ngay đêm 13/8. Điều này thể hiện tầm nhìn sắc bén, sự quyết đoán và nghệ thuật chớp thời cơ tuyệt vời.",
        "tip": "Phát lệnh 13/8 (trước 15/8) = minh chứng đỉnh cao của tính chủ động, nhạy bén chớp thời cơ!"
    },

    # ---- CHỦ ĐỀ 2: DIỄN BIẾN TỔNG KHỞI NGHĨA (14 câu: mc-15 .. mc-28) ----
    {
        "id": "mc-15", "cat": "dien-bien", "level": "NB", "trap": True,
        "question": "Trong Cách mạng tháng Tám năm 1945, nhân dân 4 tỉnh nào sau đây đã giành được chính quyền ở tỉnh lị sớm nhất cả nước (ngày 18/8/1945)?",
        "options": [
            "Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam.",
            "Cao Bằng, Bắc Kạn, Lạng Sơn, Thái Nguyên.",
            "Hà Nội, Hải Phòng, Huế, Sài Gòn.",
            "Bắc Ninh, Nam Định, Nghệ An, Quảng Ngãi."
        ],
        "answer": 0,
        "explanation": "Ngày 18/8/1945, nhân dân 4 tỉnh Bắc Giang, Hải Dương, Hà Tĩnh và Quảng Nam đã giành được chính quyền ở tỉnh lị sớm nhất trong cả nước.",
        "tip": "Mẹo nhớ 4 tỉnh sớm nhất (18/8): BẮC - HẢI - HÀ - QUẢNG (Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam)!"
    },
    {
        "id": "mc-16", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Chiều 16 tháng 8 năm 1945, theo lệnh của Ủy ban Khởi nghĩa, một đơn vị Giải phóng quân do Võ Nguyên Giáp chỉ huy xuất phát từ Tân Trào tiến về bao vây, đánh chiếm địa phương nào?",
        "options": [
            "Thị xã Tuyên Quang.",
            "Thị xã Thái Nguyên.",
            "Thị xã Bắc Giang.",
            "Thành phố Hà Nội."
        ],
        "answer": 1,
        "explanation": "Chiều 16/8/1945, một đơn vị Giải phóng quân do Võ Nguyên Giáp chỉ huy xuất phát từ Tân Trào tiến về giải phóng thị xã Thái Nguyên, mở đầu cuộc Tổng khởi nghĩa bằng lực lượng vũ trang.",
        "tip": "16/8 + Võ Nguyên Giáp + Giải phóng quân từ Tân Trào → Thị xã THÁI NGUYÊN."
    },
    {
        "id": "mc-17", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Thứ tự thời gian giành chính quyền thắng lợi tại 3 đô thị lớn nhất cả nước trong Cách mạng tháng Tám năm 1945 là",
        "options": [
            "Hà Nội (19/8) → Sài Gòn (23/8) → Huế (25/8).",
            "Huế (19/8) → Hà Nội (23/8) → Sài Gòn (25/8).",
            "Hà Nội (19/8) → Huế (23/8) → Sài Gòn (25/8).",
            "Sài Gòn (19/8) → Huế (23/8) → Hà Nội (25/8)."
        ],
        "answer": 2,
        "explanation": "Khởi nghĩa thắng lợi lần lượt theo chiều Bắc → Trung → Nam tại 3 trung tâm lớn: Hà Nội (19/8/1945), Huế (23/8/1945) và Sài Gòn (25/8/1945).",
        "tip": "Nhớ đúng trục Bắc → Trung → Nam: Hà Nội (19) → Huế (23) → Sài Gòn (25)."
    },
    {
        "id": "mc-18", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Đến ngày 28 tháng 8 năm 1945, hai địa phương nào sau đây giành được chính quyền cuối cùng trên đất liền, đánh dấu Tổng khởi nghĩa thắng lợi trên phạm vi cả nước?",
        "options": [
            "Đồng Nai Thượng và Hà Tiên.",
            "Cà Mau và Rạch Giá.",
            "Hà Giang và Lai Châu.",
            "Quảng Trị và Bình Thuận."
        ],
        "answer": 0,
        "explanation": "Ngày 28/8/1945, Đồng Nai Thượng và Hà Tiên là hai tỉnh cuối cùng trên đất liền giành được chính quyền, khép lại 15 ngày Tổng khởi nghĩa (14–28/8/1945) thắng lợi trên phạm vi cả nước.",
        "tip": "4 tỉnh đầu (18/8): Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam. 2 tỉnh cuối (28/8): Đồng Nai Thượng, Hà Tiên!"
    },
    {
        "id": "mc-19", "cat": "dien-bien", "level": "NB", "trap": True,
        "question": "Sự kiện nào sau đây ngày 30 tháng 8 năm 1945 đánh dấu chế độ quân chủ (phong kiến) kéo dài hơn 1000 năm ở Việt Nam hoàn toàn sụp đổ?",
        "options": [
            "Quần chúng nhân dân giành chính quyền thắng lợi tại kinh đô Huế.",
            "Chủ tịch Hồ Chí Minh đọc bản Tuyên ngôn Độc lập tại Quảng trường Ba Đình.",
            "Vua Bảo Đại đọc chiếu thoái vị và trao ấn kiếm cho đại diện Chính phủ lâm thời.",
            "Ủy ban Dân tộc giải phóng Việt Nam cải tổ thành Chính phủ lâm thời."
        ],
        "answer": 2,
        "explanation": "Chiều 30/8/1945, trước hàng vạn nhân dân tại Ngọ Môn (Huế), vua Bảo Đại đọc chiếu thoái vị và trao ấn kiếm cho phái đoàn Chính phủ lâm thời, chính thức chấm dứt vĩnh viễn chế độ quân chủ ở Việt Nam.",
        "tip": "BẪY MỐC NGÀY: Huế giành chính quyền = 23/8; Bảo Đại thoái vị (chế độ phong kiến sụp đổ) = 30/8!"
    },
    {
        "id": "mc-20", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Ngày 2 tháng 9 năm 1945, tại Quảng trường Ba Đình (Hà Nội), Chủ tịch Hồ Chí Minh thay mặt Chính phủ lâm thời đọc bản Tuyên ngôn Độc lập, trịnh trọng tuyên bố sự ra đời của",
        "options": [
            "nước Cộng hòa Xã hội Chủ nghĩa Việt Nam.",
            "nước Việt Nam Dân chủ Cộng hòa.",
            "Liên bang Đông Dương dân chủ.",
            "Chính phủ Cách mạng lâm thời Cộng hòa miền Nam Việt Nam."
        ],
        "answer": 1,
        "explanation": "Ngày 2/9/1945, Chủ tịch Hồ Chí Minh đọc Tuyên ngôn Độc lập, khai sinh nước Việt Nam Dân chủ Cộng hòa — nhà nước dân chủ nhân dân đầu tiên ở Đông Nam Á.",
        "tip": "Quốc hiệu năm 1945 là Việt Nam Dân chủ Cộng hòa (đến năm 1976 mới đổi thành CHXHCN Việt Nam)."
    },
    {
        "id": "mc-21", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Tổng khởi nghĩa giành chính quyền trong Cách mạng tháng Tám năm 1945 đã diễn ra và giành thắng lợi trên phạm vi cả nước trong khoảng thời gian bao lâu?",
        "options": [
            "5 ngày (từ 14/8 đến 19/8/1945).",
            "10 ngày (từ 18/8 đến 28/8/1945).",
            "15 ngày (từ 14/8 đến 28/8/1945).",
            "30 ngày (từ 2/8 đến 2/9/1945)."
        ],
        "answer": 2,
        "explanation": "Từ những địa phương cơ sở đầu tiên vùng lên ngày 14/8 đến khi Đồng Nai Thượng và Hà Tiên giành chính quyền ngày 28/8/1945, cuộc Tổng khởi nghĩa giành thắng lợi trên cả nước chỉ trong vòng 15 ngày.",
        "tip": "Con số chuẩn: 15 NGÀY (14/8 → 28/8/1945) — nhanh chóng và ít đổ máu!"
    },
    {
        "id": "mc-22", "cat": "dien-bien", "level": "TH", "trap": True,
        "question": "Vì sao ngay từ ngày 14 tháng 8 năm 1945, nhiều cấp bộ Đảng và tổ chức Việt Minh ở các địa phương dù chưa nhận được Quân lệnh số 1 nhưng vẫn chủ động phát động nhân dân khởi nghĩa giành chính quyền thắng lợi?",
        "options": [
            "Do quân đội Nhật đã tự động bàn giao toàn bộ vũ khí cho các địa phương.",
            "Do đã thấm nhuần tinh thần Chỉ thị \"Nhật - Pháp bắn nhau và hành động của chúng ta\" (12/3/1945) và chủ động nắm bắt thời cơ thực tiễn.",
            "Do nhận được sự chi viện trực tiếp bằng không quân của lực lượng Đồng minh.",
            "Do chính phủ Trần Trọng Kim ra lệnh giải tán chính quyền ở toàn bộ cấp xã, huyện."
        ],
        "answer": 1,
        "explanation": "Chỉ thị 12/3/1945 đã dự kiến trước tình huống Nhật đầu hàng và nêu rõ phương châm chủ động nắm thời cơ. Nhờ vậy, khi nghe tin Nhật đầu hàng, từ 14/8 nhiều địa phương chưa kịp nhận Quân lệnh số 1 vẫn linh hoạt, chủ động lãnh đạo nhân dân khởi nghĩa thắng lợi.",
        "tip": "Từ khóa: thấm nhuần Chỉ thị 12/3/1945 + tính chủ động, sáng tạo của địa phương!"
    },
    {
        "id": "mc-23", "cat": "dien-bien", "level": "TH", "trap": False,
        "question": "Thắng lợi của cuộc khởi nghĩa tại ba đô thị lớn Hà Nội (19/8), Huế (23/8) và Sài Gòn (25/8) có tác động như thế nào đối với tiến trình Cách mạng tháng Tám năm 1945?",
        "options": [
            "Chấm dứt ngay lập tức sự có mặt của quân Đồng minh tại Đông Dương.",
            "Làm tê liệt các cơ quan đầu não của kẻ thù, cổ vũ mạnh mẽ và tạo bước ngoặt quyết định cho thắng lợi trên cả nước.",
            "Chỉ mang ý nghĩa biểu tượng ở thành thị, không ảnh hưởng tới các vùng nông thôn.",
            "Mở đầu cho phong trào khởi nghĩa từng phần ở vùng căn cứ địa Việt Bắc."
        ],
        "answer": 1,
        "explanation": "Hà Nội, Huế, Sài Gòn là 3 trung tâm chính trị, kinh tế, quân sự lớn nhất của kẻ thù ở Bắc – Trung – Nam. Thắng lợi nhanh chóng tại 3 nơi này đã đánh sập đầu não chính quyền địch, tạo hiệu ứng lan tỏa quyết định đưa cả nước đến thắng lợi.",
        "tip": "3 đô thị lớn = 3 đầu não Bắc – Trung – Nam → thắng lợi ở đây có ý nghĩa QUYẾT ĐỊNH toàn cục!"
    },
    {
        "id": "mc-24", "cat": "dien-bien", "level": "NB", "trap": False,
        "question": "Ngày 28 tháng 8 năm 1945, Ủy ban Dân tộc giải phóng Việt Nam đã được cải tổ thành cơ quan nào sau đây?",
        "options": [
            "Ủy ban Khởi nghĩa toàn quốc.",
            "Chính phủ lâm thời nước Việt Nam Dân chủ Cộng hòa.",
            "Quốc hội khóa I nước Việt Nam Dân chủ Cộng hòa.",
            "Mặt trận Liên hiệp quốc dân Việt Nam."
        ],
        "answer": 1,
        "explanation": "Ngày 28/8/1945, Ủy ban Dân tộc giải phóng Việt Nam được cải tổ thành Chính phủ lâm thời nước Việt Nam Dân chủ Cộng hòa do Hồ Chí Minh làm Chủ tịch, chuẩn bị ra mắt quốc dân đồng bào vào ngày 2/9/1945.",
        "tip": "Chuỗi tiến hóa: Ủy ban Dân tộc giải phóng VN (16–17/8) → Chính phủ lâm thời nước VNDCCH (28/8) → Ra mắt quốc dân (2/9)."
    },
    {
        "id": "mc-25", "cat": "dien-bien", "level": "TH", "trap": False,
        "question": "Điểm nổi bật về hình thái (địa bàn) diễn ra cuộc Tổng khởi nghĩa giành chính quyền trong Cách mạng tháng Tám năm 1945 là",
        "options": [
            "chỉ diễn ra ở các tỉnh đồng bằng và đô thị lớn, không diễn ra ở miền núi.",
            "diễn ra ở nông thôn trước, kết thúc hoàn toàn ở nông thôn rồi mới đánh vào thành thị.",
            "kết hợp hài hòa cả nông thôn và thành thị, trong đó thắng lợi ở các đô thị lớn có ý nghĩa quyết định.",
            "chỉ diễn ra ở 3 thành phố lớn là Hà Nội, Huế, Sài Gòn rồi các tỉnh khác tự sáp nhập."
        ],
        "answer": 2,
        "explanation": "Cách mạng tháng Tám đi từ khởi nghĩa từng phần ở nông thôn tiến lên Tổng khởi nghĩa đồng loạt kết hợp cả nông thôn và thành thị, trong đó thắng lợi tại các đô thị lớn (Hà Nội, Huế, Sài Gòn) đóng vai trò quyết định đối với cả nước.",
        "tip": "Hình thái CM tháng Tám = Kết hợp NÔNG THÔN + THÀNH THỊ (thắng lợi ở đô thị quyết định)."
    },
    {
        "id": "mc-26", "cat": "dien-bien", "level": "TH", "trap": True,
        "question": "Nhận định nào sau đây phản ánh ĐÚNG vai trò của các lực lượng trong cuộc Tổng khởi nghĩa tháng Tám năm 1945?",
        "options": [
            "Lực lượng vũ trang giữ vai trò quyết định, lực lượng chính trị chỉ hỗ trợ phía sau.",
            "Lực lượng chính trị của quần chúng giữ vai trò quyết định, lực lượng vũ trang giữ vai trò nòng cốt, xung kích.",
            "Quân đội Đồng minh giữ vai trò quyết định giải phóng các thành phố lớn.",
            "Chỉ sử dụng lực lượng chính trị hoàn toàn, không có sự tham gia của lực lượng vũ trang."
        ],
        "answer": 1,
        "explanation": "Trong Cách mạng tháng Tám năm 1945, Đảng kết hợp chặt chẽ đấu tranh chính trị với đấu tranh vũ trang, trong đó lực lượng chính trị đông đảo của quần chúng giữ vai trò quyết định, còn lực lượng vũ trang đóng vai trò nòng cốt, xung kích hỗ trợ.",
        "tip": "BẪY CỰC HAY RA: Lực lượng CHÍNH TRỊ quyết định, lực lượng VŨ TRANG làm nòng cốt/xung kích!"
    },
    {
        "id": "mc-27", "cat": "dien-bien", "level": "TH", "trap": False,
        "question": "Trong cuộc khởi nghĩa giành chính quyền ở Hà Nội (19/8/1945), thắng lợi diễn ra nhanh chóng và ít đổ máu chủ yếu nhờ yếu tố nào?",
        "options": [
            "Sức mạnh áp đảo của hàng vạn quần chúng biểu tình có vũ trang hỗ trợ, kết hợp khôn khéo việc trung lập hóa quân Nhật.",
            "Quân đội Nhật ở Hà Nội đã rút hết về nước từ trước ngày 15/8/1945.",
            "Chính phủ Trần Trọng Kim tự nguyện trao lại toàn bộ công sở từ ngày 14/8.",
            "Có sự đổ bộ hỗ trợ của quân đội Mỹ và Anh vào trung tâm Hà Nội."
        ],
        "answer": 0,
        "explanation": "Tại Hà Nội ngày 19/8, khí thế áp đảo của hàng chục vạn quần chúng cách mạng kết hợp lực lượng tự vệ chiến đấu cùng sách lược mềm dẻo, khôn khéo (không khiêu khích quân Nhật vô ích mà cô lập, trung lập hóa chúng) đã buộc quân Nhật án binh bất động, giúp ta thắng lợi trọn vẹn và ít đổ máu.",
        "tip": "Khí thế quần chúng áp đảo + nghệ thuật phân hóa, trung lập hóa quân Nhật → thắng nhanh, ít đổ máu!"
    },
    {
        "id": "mc-28", "cat": "dien-bien", "level": "TH", "trap": True,
        "question": "Trong Cách mạng tháng Tám năm 1945, nhân dân Việt Nam đã giành chính quyền trực tiếp từ tay kẻ thù nào?",
        "options": [
            "Thực dân Pháp và chính quyền tay sai thân Pháp.",
            "Phát xít Nhật và chính quyền tay sai thân Nhật.",
            "Quân đội Trung Hoa Dân quốc và quân đội Anh.",
            "Liên quân thực dân Pháp – Nhật đang cùng cai trị Đông Dương."
        ],
        "answer": 1,
        "explanation": "Đêm 9/3/1945, phát xít Nhật đã đảo chính lật đổ thực dân Pháp để độc chiếm Đông Dương. Vì vậy, đến tháng 8/1945, nhân dân ta giành chính quyền trực tiếp từ tay phát xít Nhật và chính quyền tay sai thân Nhật (Chính phủ Trần Trọng Kim).",
        "tip": "BẪY SỐ 1: Pháp bị Nhật đảo chính từ 9/3/1945 rồi! Tháng 8/1945 ta giành chính quyền TRỰC TIẾP từ tay NHẬT!"
    },

    # ---- CHỦ ĐỀ 3: NGUYÊN NHÂN & Ý NGHĨA (13 câu: mc-29 .. mc-41) ----
    {
        "id": "mc-29", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": True,
        "question": "Nhân tố giữ vai trò quyết định hàng đầu đưa đến thắng lợi của Cách mạng tháng Tám năm 1945 là",
        "options": [
            "chiến thắng của Hồng quân Liên Xô và các lực lượng Đồng minh chống phát xít.",
            "sự lãnh đạo đúng đắn, sáng suốt của Đảng Cộng sản Đông Dương, đứng đầu là Chủ tịch Hồ Chí Minh.",
            "mâu thuẫn nội bộ sâu sắc giữa phát xít Nhật và thực dân Pháp ở Đông Dương.",
            "sự ủng hộ về tài chính và vũ khí của các nước xã hội chủ nghĩa Đông Âu."
        ],
        "answer": 1,
        "explanation": "Trong các nguyên nhân thắng lợi, nguyên nhân chủ quan giữ vai trò quyết định — mà đứng đầu là sự lãnh đạo đúng đắn, sáng suốt, tài tình của Đảng Cộng sản Đông Dương và Chủ tịch Hồ Chí Minh.",
        "tip": "Luôn nhớ: Nguyên nhân CHỦ QUAN quyết định (đứng đầu là sự lãnh đạo của Đảng); Liên Xô/Đồng minh là KHÁCH QUAN!"
    },
    {
        "id": "mc-30", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Nội dung nào sau đây là nguyên nhân KHÁCH QUAN góp phần đưa đến thắng lợi của Cách mạng tháng Tám năm 1945?",
        "options": [
            "Truyền thống yêu nước nồng nàn và tinh thần đoàn kết của nhân dân Việt Nam.",
            "Quá trình chuẩn bị lực lượng chu đáo suốt 15 năm (1930 – 1945) của Đảng.",
            "Chiến thắng của Hồng quân Liên Xô và lực lượng Đồng minh trong cuộc chiến tranh chống phát xít.",
            "Sự sáng tạo, linh hoạt trong chớp thời cơ của các cấp bộ Đảng ở địa phương."
        ],
        "answer": 2,
        "explanation": "Chiến thắng của Hồng quân Liên Xô và lực lượng Đồng minh đánh bại chủ nghĩa phát xít (đặc biệt là quân phiệt Nhật) là nhân tố từ bên ngoài (khách quan) làm kẻ thù trực tiếp của ta gục ngã, tạo thời cơ thuận lợi cho Tổng khởi nghĩa.",
        "tip": "Khách quan = yếu tố bên ngoài (Liên Xô + Đồng minh đánh bại phát xít). 3 đáp án còn lại đều là nội lực bên trong (chủ quan)."
    },
    {
        "id": "mc-31", "cat": "nguyen-nhan-y-nghia", "level": "TH", "trap": False,
        "question": "Nhân tố khách quan (chiến thắng của Hồng quân Liên Xô và quân Đồng minh chống phát xít) có vai trò như thế nào đối với thắng lợi của Cách mạng tháng Tám năm 1945?",
        "options": [
            "Giữ vai trò quyết định trực tiếp, thay thế cho quá trình chuẩn bị lực lượng trong nước.",
            "Tạo ra điều kiện và thời cơ thuận lợi để nhân dân Việt Nam đứng lên giành chính quyền.",
            "Trực tiếp giải phóng các đô thị lớn Hà Nội, Huế, Sài Gòn giúp nhân dân Việt Nam.",
            "Không có bất kỳ tác động nào đến diễn biến Cách mạng tháng Tám năm 1945."
        ],
        "answer": 1,
        "explanation": "Chiến thắng của Liên Xô và Đồng minh trước phát xít Nhật tạo ra thời cơ khách quan cực kỳ thuận lợi (làm kẻ thù trực tiếp rệu rã), nhưng muốn biến thời cơ thành thắng lợi thì nhân tố chủ quan (sự chuẩn bị 15 năm và lãnh đạo của Đảng) mới mang tính quyết định.",
        "tip": "Khách quan = tạo thời cơ thuận lợi; Chủ quan = quyết định biến thời cơ thành thắng lợi!"
    },
    {
        "id": "mc-32", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Thắng lợi của Cách mạng tháng Tám năm 1945 đã lật đổ ách thống trị của những thế lực nào trên đất nước Việt Nam?",
        "options": [
            "Thực dân Pháp (hơn 80 năm), quân phiệt Nhật (gần 5 năm) và chế độ quân chủ (hơn 1000 năm).",
            "Thực dân Pháp (hơn 50 năm), đế quốc Mỹ (gần 20 năm) và chế độ quân chủ.",
            "Chỉ lật đổ quân phiệt Nhật Bản, vẫn duy trì thể chế quân chủ lập hiến của triều Nguyễn.",
            "Chủ nghĩa thực dân mới của Mỹ và chính quyền Sài Gòn."
        ],
        "answer": 0,
        "explanation": "Theo SGK Lịch sử 12 KNTT: Cách mạng tháng Tám đã lật đổ ách cai trị của thực dân Pháp trong hơn 80 năm (1858–1945), quân phiệt Nhật Bản gần 5 năm (9/1940–8/1945) và chấm dứt thời kì quân chủ hơn 1000 năm.",
        "tip": "Bộ 3 con số chuẩn SGK KNTT: Pháp (>80 năm) • Nhật (gần 5 năm) • Quân chủ (>1000 năm)."
    },
    {
        "id": "mc-33", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Thắng lợi của Cách mạng tháng Tám năm 1945 đã làm thay đổi địa vị của Đảng Cộng sản Đông Dương như thế nào?",
        "options": [
            "Từ một tổ chức quần chúng trở thành Mặt trận dân tộc thống nhất.",
            "Từ một đảng hoạt động bí mật trở thành đảng cầm quyền trong cả nước.",
            "Từ đảng cầm quyền ở miền Bắc mở rộng lãnh đạo ra toàn khu vực Đông Nam Á.",
            "Từ một tổ chức yêu nước tự phát trở thành chính đảng hợp pháp của chế độ thuộc địa."
        ],
        "answer": 1,
        "explanation": "Trước tháng 8/1945, Đảng Cộng sản Đông Dương phải hoạt động bí mật (bị đế quốc khủng bố). Sau thắng lợi của Cách mạng tháng Tám, Đảng trở thành đảng cầm quyền, lãnh đạo Nhà nước Việt Nam Dân chủ Cộng hòa.",
        "tip": "Đảng: bí mật → CẦM QUYỀN. Nhân dân: nô lệ → LÀM CHỦ đất nước."
    },
    {
        "id": "mc-34", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Cách mạng tháng Tám năm 1945 đánh dấu một bước tiến nhảy vọt trong lịch sử dân tộc Việt Nam vì đã mở ra",
        "options": [
            "kỷ nguyên cả nước thống nhất cùng đi lên chủ nghĩa xã hội.",
            "kỷ nguyên độc lập, tự do và phát triển dưới chế độ dân chủ cộng hòa.",
            "kỷ nguyên đổi mới, hội nhập kinh tế quốc tế sâu rộng.",
            "kỷ nguyên công nghiệp hóa, hiện đại hóa đất nước."
        ],
        "answer": 1,
        "explanation": "Cách mạng tháng Tám mở ra kỷ nguyên mới trong lịch sử dân tộc: kỷ nguyên độc lập, tự do và phát triển dưới chế độ dân chủ cộng hòa; nhân dân lao động từ thân phận nô lệ trở thành người làm chủ đất nước.",
        "tip": "Đừng nhầm với mốc 1975 (cả nước thống nhất đi lên CNXH) hay 1986 (Đổi mới)! 1945 = Kỷ nguyên ĐỘC LẬP, TỰ DO!"
    },
    {
        "id": "mc-35", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Sự ra đời của nước Việt Nam Dân chủ Cộng hòa (2/9/1945) mang ý nghĩa lịch sử đặc biệt nào đối với khu vực Đông Nam Á?",
        "options": [
            "Là quốc gia đầu tiên ở châu Á hoàn thành công nghiệp hóa.",
            "Là nhà nước dân chủ nhân dân (công nông) đầu tiên ở Đông Nam Á.",
            "Là nước sáng lập Hiệp hội các quốc gia Đông Nam Á (ASEAN).",
            "Là nước duy nhất ở Đông Nam Á tuyên bố độc lập trong năm 1945."
        ],
        "answer": 1,
        "explanation": "Nước Việt Nam Dân chủ Cộng hòa ra đời là nhà nước dân chủ nhân dân đầu tiên ở Đông Nam Á (lưu ý: năm 1945 còn có In-đô-nê-xi-a ngày 17/8 và Lào ngày 12/10 tuyên bố độc lập nên nhận định 'nước duy nhất tuyên bố độc lập năm 1945' là sai!).",
        "tip": "Nhà nước dân chủ nhân dân ĐẦU TIÊN ở Đông Nam Á! (Tránh bẫy 'nước duy nhất tuyên bố độc lập 1945' vì còn In-đô-nê-xi-a và Lào)."
    },
    {
        "id": "mc-36", "cat": "nguyen-nhan-y-nghia", "level": "NB", "trap": False,
        "question": "Nội dung nào sau đây phản ánh ĐÚNG ý nghĩa quốc tế của Cách mạng tháng Tám năm 1945 ở Việt Nam?",
        "options": [
            "Buộc thực dân Pháp phải ký Hiệp định Giơ-ne-vơ công nhận độc lập của Đông Dương.",
            "Làm sụp đổ hoàn toàn hệ thống chủ nghĩa thực dân kiểu mới của đế quốc Mỹ.",
            "Góp phần vào thắng lợi chống phát xít, làm tan rã hệ thống thuộc địa và cổ vũ phong trào giải phóng dân tộc thế giới.",
            "Chấm dứt hoàn toàn tình trạng đối đầu Đông – Tây trong Chiến tranh lạnh."
        ],
        "answer": 2,
        "explanation": "Về mặt quốc tế, Cách mạng tháng Tám góp phần vào thắng lợi của các lực lượng hòa bình, dân chủ, tiến bộ chống chủ nghĩa phát xít, góp phần làm tan rã hệ thống thuộc địa của chủ nghĩa thực dân (chọc thủng khâu yếu nhất) và cổ vũ mạnh mẽ phong trào giải phóng dân tộc trên thế giới.",
        "tip": "3 ý nghĩa quốc tế: (1) Góp phần chống phát xít; (2) Làm tan rã hệ thống thuộc địa; (3) Cổ vũ phong trào GPDT thế giới."
    },
    {
        "id": "mc-37", "cat": "nguyen-nhan-y-nghia", "level": "TH", "trap": True,
        "question": "Nhận định nào sau đây KHÔNG ĐÚNG về ý nghĩa lịch sử của Cách mạng tháng Tám năm 1945?",
        "options": [
            "Chấm dứt vĩnh viễn chế độ quân chủ kéo dài hơn 1000 năm ở Việt Nam.",
            "Đưa nhân dân Việt Nam từ thân phận nô lệ trở thành người làm chủ đất nước.",
            "Đã xóa bỏ hoàn toàn mọi tàn dư phong kiến và giải quyết triệt để vấn đề ruộng đất cho nông dân.",
            "Góp phần cổ vũ mạnh mẽ tinh thần đấu tranh của các dân tộc thuộc địa và phụ thuộc trên thế giới."
        ],
        "answer": 2,
        "explanation": "Cách mạng tháng Tám đã xóa bỏ chế độ QUÂN CHỦ (nhà nước phong kiến), nhưng CHƯA xóa bỏ hoàn toàn mọi tàn dư phong kiến và chưa giải quyết triệt để vấn đề ruộng đất (cải cách ruộng đất diễn ra trong giai đoạn sau).",
        "tip": "BẪY QUEN THUỘC: 'chấm dứt chế độ quân chủ' = ĐÚNG; 'xóa bỏ hoàn toàn tàn dư phong kiến / triệt để ruộng đất' = SAI!"
    },
    {
        "id": "mc-38", "cat": "nguyen-nhan-y-nghia", "level": "VD", "trap": False,
        "question": "Một số học giả nước ngoài cho rằng thắng lợi của Cách mạng tháng Tám năm 1945 là do sự \"ăn may\" khi Việt Minh lợi dụng \"khoảng trống quyền lực\" sau khi Nhật đầu hàng. Luận điểm nào sau đây bác bỏ thuyết phục nhất quan điểm sai trái đó?",
        "options": [
            "Mọi quốc gia ở Đông Nam Á năm 1945 đều giành được độc lập dễ dàng như nhau.",
            "Thắng lợi đó là kết quả của quá trình chuẩn bị chu đáo suốt 15 năm (1930–1945) của Đảng và sự chủ động, kịp thời chớp thời cơ của toàn dân tộc.",
            "Quân đội Nhật Bản ở Việt Nam đã tự nguyện rút toàn bộ binh lính về nước trước ngày 15/8/1945.",
            "Nhân dân Việt Nam nhận được sự đổ bộ giải phóng trực tiếp từ quân đội Mỹ và Anh."
        ],
        "answer": 1,
        "explanation": "Thời cơ khách quan xuất hiện chung ở nhiều nước Đông Nam Á khi Nhật đầu hàng, nhưng không phải nước nào cũng giành được chính quyền. Việt Nam thành công nhanh chóng chính nhờ sự chuẩn bị nội lực chu đáo trong 15 năm (đường lối, lực lượng, căn cứ địa, tập dượt) cùng bản lĩnh chủ động chớp thời cơ của Đảng.",
        "tip": "Bác bỏ luận điệu 'ăn may / khoảng trống quyền lực' → nhấn mạnh 15 năm chuẩn bị nội lực + chủ động chớp thời cơ!"
    },
    {
        "id": "mc-39", "cat": "nguyen-nhan-y-nghia", "level": "TH", "trap": False,
        "question": "Trong Báo cáo Chính trị năm 1951, Chủ tịch Hồ Chí Minh viết: \"Lần đầu tiên trong lịch sử cách mạng của các dân tộc thuộc địa và nửa thuộc địa, một Đảng mới 15 tuổi đã lãnh đạo cách mạng thành công, đã nắm chính quyền toàn quốc\". Nhận định này khẳng định điều gì?",
        "options": [
            "Cách mạng tháng Tám chỉ có ý nghĩa trong phạm vi nội bộ của giai cấp công nhân Việt Nam.",
            "Năng lực lãnh đạo tài tình của Đảng Cộng sản Đông Dương và tầm vóc cổ vũ quốc tế to lớn của Cách mạng tháng Tám.",
            "Đảng Cộng sản Đông Dương là chính đảng duy nhất được thành lập ở khu vực châu Á thế kỉ XX.",
            "Thắng lợi của Cách mạng tháng Tám hoàn toàn không cần tới vai trò của các tầng lớp nhân dân khác."
        ],
        "answer": 1,
        "explanation": "Lời đánh giá của Chủ tịch Hồ Chí Minh tôn vinh bản lĩnh, năng lực lãnh đạo xuất sắc của Đảng Cộng sản Đông Dương (ra đời 1930 → 1945 mới 15 tuổi) đồng thời khẳng định niềm tự hào và sức cổ vũ lớn lao đối với các dân tộc bị áp bức trên toàn thế giới.",
        "tip": "Tư liệu 'Đảng mới 15 tuổi' = 2 vế: Năng lực lãnh đạo của Đảng + Ý nghĩa cổ vũ quốc tế!"
    },
    {
        "id": "mc-40", "cat": "nguyen-nhan-y-nghia", "level": "TH", "trap": False,
        "question": "Điều kiện nào sau đây thuộc nhóm NGUYÊN NHÂN CHỦ QUAN tạo nên sức mạnh tổng hợp của nhân dân Việt Nam trong Cách mạng tháng Tám năm 1945?",
        "options": [
            "Liên Xô tuyên chiến với quân phiệt Nhật Bản ngày 8/8/1945.",
            "Mỹ ném hai quả bom nguyên tử xuống Hi-rô-si-ma và Na-ga-xa-ki.",
            "Truyền thống yêu nước nồng nàn, khối đại đoàn kết toàn dân được tập hợp trong Mặt trận Việt Minh.",
            "Sự sụp đổ của chủ nghĩa phát xít Đức tại chiến trường châu Âu."
        ],
        "answer": 2,
        "explanation": "Truyền thống yêu nước nồng nàn, tinh thần đoàn kết toàn dân trong Mặt trận Việt Minh là sức mạnh nội lực bên trong (nguyên nhân chủ quan). Các sự kiện về Liên Xô, Mỹ hay phát xít Đức đều là diễn biến từ bên ngoài (nguyên nhân khách quan).",
        "tip": "Nội lực trong nước (Đảng + 15 năm chuẩn bị + truyền thống yêu nước, Việt Minh) = Chủ quan."
    },
    {
        "id": "mc-41", "cat": "nguyen-nhan-y-nghia", "level": "TH", "trap": False,
        "question": "Thắng lợi của Cách mạng tháng Tám năm 1945 đã tạo ra tiền đề quan trọng nào cho các giai đoạn lịch sử tiếp theo của cách mạng Việt Nam?",
        "options": [
            "Giúp Việt Nam không còn phải đối mặt với bất kỳ cuộc chiến tranh xâm lược nào nữa.",
            "Xây dựng được chính quyền cách mạng làm cơ sở vững chắc cho cuộc kháng chiến chống Pháp, chống Mỹ và công cuộc xây dựng đất nước sau này.",
            "Đưa Việt Nam trở thành ủy viên thường trực Hội đồng Bảo an Liên Hợp Quốc.",
            "Thiết lập ngay quan hệ ngoại giao chính thức với tất cả các nước tư bản phương Tây."
        ],
        "answer": 1,
        "explanation": "Cách mạng tháng Tám lập nên nước Việt Nam Dân chủ Cộng hòa, đưa Đảng thành đảng cầm quyền và nhân dân làm chủ đất nước — tạo nền tảng chính trị, pháp lý và tinh thần vô giá cho các thắng lợi tiếp theo (kháng chiến chống Pháp, chống Mỹ và bảo vệ Tổ quốc).",
        "tip": "Tạo tiền đề = có chính quyền cách mạng, vị thế độc lập, sức mạnh toàn dân cho các thắng lợi tiếp theo."
    },

    # ---- CHỦ ĐỀ 4: BÀI HỌC, TÍNH CHẤT & VẬN DỤNG (11 câu: mc-42 .. mc-52) ----
    {
        "id": "mc-42", "cat": "bai-hoc-tinh-chat", "level": "NB", "trap": False,
        "question": "Bài học kinh nghiệm hàng đầu, có ý nghĩa quyết định đối với mọi thắng lợi của cách mạng Việt Nam được rút ra từ Cách mạng tháng Tám năm 1945 là",
        "options": [
            "bài học về sự lãnh đạo đúng đắn, sáng tạo của Đảng.",
            "bài học về việc tranh thủ sự viện trợ quân sự từ bên ngoài.",
            "bài học về tập trung toàn bộ lực lượng cho đấu tranh nghị trường.",
            "bài học về giải phóng thành thị trước rồi mới tiến về nông thôn."
        ],
        "answer": 0,
        "explanation": "Theo SGK Lịch sử 12 KNTT, bài học về sự lãnh đạo của Đảng là nhân tố quyết định: Đảng phải có đường lối đúng đắn trên cơ sở vận dụng sáng tạo chủ nghĩa Mác - Lênin vào thực tiễn Việt Nam, chủ động và linh hoạt trong lãnh đạo.",
        "tip": "Bài học hàng đầu / quyết định nhất luôn là: Sự lãnh đạo đúng đắn, sáng tạo của Đảng!"
    },
    {
        "id": "mc-43", "cat": "bai-hoc-tinh-chat", "level": "NB", "trap": False,
        "question": "Trong Cách mạng tháng Tám năm 1945, bài học về xây dựng và phát huy sức mạnh khối đại đoàn kết toàn dân tộc gắn liền trực tiếp với vai trò của tổ chức nào?",
        "options": [
            "Hội Việt Nam Cách mạng Thanh niên.",
            "Mặt trận Dân chủ Đông Dương.",
            "Mặt trận Việt Minh (Việt Nam Độc lập Đồng minh).",
            "Mặt trận Dân tộc giải phóng miền Nam Việt Nam."
        ],
        "answer": 2,
        "explanation": "Mặt trận Việt Minh (thành lập 19/5/1941) với các hội Cứu quốc phong phú đã tập hợp, tổ chức và đoàn kết mọi tầng lớp nhân dân yêu nước không phân biệt giai cấp, tôn giáo, dân tộc dưới lá cờ đỏ sao vàng.",
        "tip": "Cách mạng tháng Tám + khối đại đoàn kết = MẶT TRẬN VIỆT MINH!"
    },
    {
        "id": "mc-44", "cat": "bai-hoc-tinh-chat", "level": "TH", "trap": False,
        "question": "Nghệ thuật chỉ đạo khởi nghĩa đặc sắc nhất được thể hiện qua việc phát động và giành thắng lợi trọn vẹn chỉ trong 15 ngày (14 – 28/8/1945) là bài học nào sau đây?",
        "options": [
            "Bài học về xây dựng quân đội chính quy, hiện đại.",
            "Bài học về xác định đúng, chủ động và mau lẹ nắm bắt, chớp thời cơ.",
            "Bài học về đàm phán ngoại giao song phương với các cường quốc.",
            "Bài học về vừa đánh vừa đàm trên chiến trường chính quy."
        ],
        "answer": 1,
        "explanation": "Đảng đã phân tích chính xác tình hình thế giới và trong nước, dự báo sớm sự thất bại của Nhật, kiên quyết phát lệnh ngay khi thời cơ \"ngàn năm có một\" xuất hiện và hoàn thành trước khi quân Đồng minh vào.",
        "tip": "15 ngày thắng lợi gọn gàng trước khi Đồng minh vào = đỉnh cao nghệ thuật CHỚP THỜI CƠ!"
    },
    {
        "id": "mc-45", "cat": "bai-hoc-tinh-chat", "level": "TH", "trap": False,
        "question": "Trong bài học về \"kết hợp sức mạnh dân tộc với sức mạnh thời đại\" rút ra từ Cách mạng tháng Tám năm 1945, yếu tố nào giữ vai trò quyết định?",
        "options": [
            "Sức mạnh thời đại (bối cảnh quốc tế thuận lợi).",
            "Sức mạnh dân tộc (nội lực bên trong đất nước).",
            "Sức mạnh quân sự của các nước Đồng minh chống phát xít.",
            "Tài chính viện trợ từ phong trào cộng sản quốc tế."
        ],
        "answer": 1,
        "explanation": "Cách mạng tháng Tám cho thấy cần biết tranh thủ điều kiện quốc tế thuận lợi (sức mạnh thời đại), nhưng sức mạnh dân tộc (nội lực bên trong: đường lối của Đảng, lực lượng toàn dân) luôn đóng vai trò quyết định.",
        "tip": "Kết hợp dân tộc + thời đại → SỨC MẠNH DÂN TỘC (nội lực) luôn giữ vai trò quyết định!"
    },
    {
        "id": "mc-46", "cat": "bai-hoc-tinh-chat", "level": "TH", "trap": True,
        "question": "Tính chất điển hình, nổi bật nhất của Cách mạng tháng Tám năm 1945 ở Việt Nam là",
        "options": [
            "một cuộc cách mạng tư sản dân quyền kiểu cũ.",
            "một cuộc cách mạng xã hội chủ nghĩa hoàn chỉnh.",
            "một cuộc cách mạng giải phóng dân tộc mang tính chất dân chủ mới.",
            "một cuộc cải cách dân chủ ôn hòa trong khuôn khổ chế độ thuộc địa."
        ],
        "answer": 2,
        "explanation": "Cách mạng tháng Tám năm 1945 là cuộc cách mạng giải phóng dân tộc điển hình (nhiệm vụ trung tâm là đánh đổ đế quốc, phát xít giành độc lập cho dân tộc) đồng thời mang tính chất dân chủ mới (lập chính quyền của dân, xóa bỏ chế độ quân chủ, góp phần đánh bại phát xít).",
        "tip": "BẪY TÍNH CHẤT: Giải phóng dân tộc + Dân chủ mới (KHÔNG phải CM XHCN, KHÔNG phải tư sản kiểu cũ!)."
    },
    {
        "id": "mc-47", "cat": "bai-hoc-tinh-chat", "level": "TH", "trap": False,
        "question": "Biểu hiện nào sau đây chứng tỏ Cách mạng tháng Tám năm 1945 mang tính chất DÂN CHỦ MỚI?",
        "options": [
            "Đã chia đều toàn bộ ruộng đất của địa chủ cho nông dân nghèo ngay trong tháng 8/1945.",
            "Đã xóa bỏ chế độ quân chủ chuyên chế, lập nên nhà nước dân chủ cộng hòa, mang lại quyền làm chủ và các quyền dân chủ cho nhân dân.",
            "Đã hoàn thành việc quốc hữu hóa toàn bộ các cơ sở công nghiệp tư bản.",
            "Đã xóa bỏ hoàn toàn sự tồn tại của mọi giai cấp trong xã hội Việt Nam."
        ],
        "answer": 1,
        "explanation": "Tính chất dân chủ mới thể hiện ở chỗ: Cách mạng tháng Tám là một bộ phận của phe dân chủ chống phát xít; lật đổ chế độ quân chủ chuyên chế; thiết lập Nhà nước Việt Nam Dân chủ Cộng hòa của nhân dân và bước đầu đem lại quyền tự do, dân chủ, giảm tô thuế cho nhân dân lao động.",
        "tip": "Tính dân chủ mới = chống phát xít + xóa bỏ quân chủ + lập nhà nước dân chủ cộng hòa + mang lại quyền làm chủ."
    },
    {
        "id": "mc-48", "cat": "bai-hoc-tinh-chat", "level": "VD", "trap": False,
        "question": "Điểm độc đáo, sáng tạo nhất trong phương pháp tiến hành khởi nghĩa của Cách mạng tháng Tám năm 1945 là gì?",
        "options": [
            "Chỉ sử dụng chiến tranh du kích kéo dài nhiều năm ở vùng rừng núi.",
            "Đi từ khởi nghĩa từng phần tiến lên tổng khởi nghĩa, kết hợp đấu tranh chính trị với vũ trang, kết hợp nông thôn và thành thị.",
            "Dựa hoàn toàn vào cuộc tổng bãi công của công nhân ở các khu công nghiệp lớn.",
            "Chờ quân đội nước ngoài đánh bại hoàn toàn địch rồi tổ chức bầu cử nghị viện."
        ],
        "answer": 1,
        "explanation": "Sáng tạo lớn của Đảng là không rập khuôn mô hình nước ngoài: đi từ khởi nghĩa từng phần (tháng 3–8/1945) tiến lên tổng khởi nghĩa đồng loạt khi thời cơ chín muồi; kết hợp linh hoạt đấu tranh chính trị với vũ trang, kết hợp nông thôn và thành thị.",
        "tip": "Bộ 3 kết hợp sáng tạo: Khởi nghĩa từng phần → Tổng khởi nghĩa | Chính trị + Vũ trang | Nông thôn + Thành thị."
    },
    {
        "id": "mc-49", "cat": "bai-hoc-tinh-chat", "level": "VD", "trap": False,
        "question": "Trong công cuộc xây dựng và bảo vệ Tổ quốc Việt Nam hiện nay, bài học về \"xây dựng và phát huy sức mạnh khối đại đoàn kết dân tộc\" của Cách mạng tháng Tám được vận dụng trực tiếp nhất qua hoạt động nào?",
        "options": [
            "Tập hợp rộng rãi mọi tầng lớp nhân dân trong Mặt trận Tổ quốc Việt Nam và đẩy mạnh các phong trào thi đua yêu nước.",
            "Chỉ tập trung phát triển các lực lượng vũ trang mà không cần mở rộng các tổ chức xã hội.",
            "Thực hiện chính sách đóng cửa, hạn chế giao lưu hợp tác với bên ngoài.",
            "Chỉ phát huy vai trò của giai cấp công nhân ở các khu đô thị lớn."
        ],
        "answer": 0,
        "explanation": "Kế thừa bài học từ Mặt trận Việt Minh, ngày nay Đảng và Nhà nước tiếp tục mở rộng, củng cố khối đại đoàn kết toàn dân tộc qua Mặt trận Tổ quốc Việt Nam và các tổ chức chính trị - xã hội với nhiều hình thức phong phú, khơi dậy tinh thần yêu nước và thi đua phát triển đất nước.",
        "tip": "Vận dụng bài học đại đoàn kết hôm nay = Mặt trận Tổ quốc VN + phong trào thi đua + đoàn kết toàn dân."
    },
    {
        "id": "mc-50", "cat": "bai-hoc-tinh-chat", "level": "VD", "trap": False,
        "question": "Bài học kinh nghiệm về \"nắm bắt thời cơ\" từ Cách mạng tháng Tám năm 1945 có ý nghĩa thực tiễn nào đối với Việt Nam trong bối cảnh hội nhập quốc tế hiện nay?",
        "options": [
            "Chờ đợi các nước lớn giải quyết xong mọi biến động toàn cầu mới đưa ra chính sách.",
            "Chủ động dự báo tình hình thế giới, kịp thời tận dụng cơ hội từ hội nhập và khoa học – công nghệ để phát triển, đồng thời ứng phó hiệu quả với thách thức.",
            "Tránh tham gia các tổ chức kinh tế khu vực để bảo toàn nguyên trạng nền kinh tế.",
            "Chỉ tập trung vào lĩnh vực quân sự, xem nhẹ phát triển kinh tế và ngoại giao."
        ],
        "answer": 1,
        "explanation": "Trong bối cảnh toàn cầu hóa và Cách mạng công nghiệp 4.0 biến động nhanh, bài học chớp thời cơ đòi hỏi Việt Nam phải nhạy bén phân tích tình hình quốc tế, chủ động nắm bắt cơ hội phát triển kinh tế – công nghệ – đối ngoại và hóa giải kịp thời các nguy cơ.",
        "tip": "Chớp thời cơ hôm nay = chủ động phân tích, tận dụng cơ hội hội nhập & công nghệ, ứng phó kịp thời thách thức."
    },
    {
        "id": "mc-51", "cat": "bai-hoc-tinh-chat", "level": "VD", "trap": True,
        "question": "Nhận định nào sau đây là SAI khi tổng kết những đặc điểm nổi bật của Cách mạng tháng Tám năm 1945?",
        "options": [
            "Diễn ra nhanh chóng (15 ngày), gọn gàng và ít đổ máu.",
            "Kết hợp chặt chẽ giữa đấu tranh chính trị của quần chúng với đấu tranh vũ trang.",
            "Lực lượng vũ trang nhân dân đóng vai trò quyết định trực tiếp, còn lực lượng chính trị chỉ hỗ trợ.",
            "Có sự kết hợp hài hòa giữa điều kiện khách quan thuận lợi và sự chuẩn bị chu đáo về nhân tố chủ quan."
        ],
        "answer": 2,
        "explanation": "Nhận định 'lực lượng vũ trang quyết định trực tiếp, lực lượng chính trị chỉ hỗ trợ' đã đảo ngược vai trò hai lực lượng! Thực tế trong Cách mạng tháng Tám năm 1945, LỰC LƯỢNG CHÍNH TRỊ của quần chúng mới đóng vai trò quyết định, còn lực lượng vũ trang giữ vai trò nòng cốt, xung kích.",
        "tip": "BẪY ĐẢO VAI TRÒ: Cứ thấy 'vũ trang quyết định, chính trị hỗ trợ' là SAI ngay!"
    },
    {
        "id": "mc-52", "cat": "bai-hoc-tinh-chat", "level": "VD", "trap": False,
        "question": "Điểm khác biệt căn bản của Nhà nước Việt Nam Dân chủ Cộng hòa ra đời sau Cách mạng tháng Tám năm 1945 so với các triều đại phong kiến trước đó trong lịch sử dân tộc là",
        "options": [
            "lần đầu tiên đất nước ta giành được nền độc lập dân tộc.",
            "lần đầu tiên thiết lập chế độ dân chủ cộng hòa, nhân dân lao động đứng lên làm chủ đất nước.",
            "lần đầu tiên Việt Nam có bộ máy hành chính thống nhất từ trung ương tới địa phương.",
            "lần đầu tiên lãnh thổ Việt Nam có đường biên giới ổn định trên đất liền."
        ],
        "answer": 1,
        "explanation": "Trong lịch sử dựng nước và giữ nước, dân tộc ta từng nhiều lần giành lại độc lập dưới các triều đại Ngô, Lý, Trần, Lê... nhưng đó vẫn là chế độ quân chủ (vua nắm quyền). Điểm khác biệt căn bản nhất của năm 1945 là lần đầu tiên thiết lập chế độ DÂN CHỦ CỘNG HÒA, nhân dân lao động trở thành người làm chủ đất nước.",
        "tip": "Khác biệt căn bản của 1945 so với lịch sử trước đó = Lần đầu tiên thiết lập CHẾ ĐỘ DÂN CHỦ CỘNG HÒA (nhân dân làm chủ)!"
    },
]

# ============================================================================
# 7. 8 TRUE/FALSE PASSAGE QUESTIONS (Phần II — chuẩn form Bộ GD&ĐT, mỗi câu 4 ý)
# ============================================================================
TF_QUESTIONS = [
    {
        "id": "tf-01",
        "cat": "boi-canh",
        "title": "Bối cảnh tháng 8/1945 & Thời cơ \"ngàn năm có một\"",
        "passage": "“Đến ngày 15 - 8 - 1945, Nhật Bản tuyên bố đầu hàng Đồng minh không điều kiện. Ngay sau khi Nhật Bản tuyên bố đầu hàng Đồng minh, quân Nhật ở Đông Dương rệu rã, Chính phủ thân Nhật Trần Trọng Kim hoang mang. Điều kiện khách quan thuận lợi cho cuộc Tổng khởi nghĩa đã đến... Trước đó, từ tháng 3 đến tháng 8/1945, cao trào kháng Nhật, cứu nước đã diễn ra trong cả nước, góp phần chuẩn bị lực lượng, tập dượt cho quần chúng đấu tranh, sẵn sàng tổng khởi nghĩa giành chính quyền khi thời cơ đến.”",
        "source": "Sách giáo khoa Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Sự kiện Nhật Bản đầu hàng Đồng minh không điều kiện (15/8/1945) đã tạo ra điều kiện khách quan thuận lợi cho cuộc Tổng khởi nghĩa ở Việt Nam.",
                "answer": True,
                "explanation": "ĐÚNG. Tư liệu nêu rõ: sau khi Nhật Bản đầu hàng Đồng minh (15/8/1945), quân Nhật ở Đông Dương rệu rã, chính phủ Trần Trọng Kim hoang mang — điều kiện khách quan thuận lợi cho Tổng khởi nghĩa đã đến."
            },
            {
                "key": "b",
                "text": "Ngay khi Nhật Bản tuyên bố đầu hàng, quân đội Nhật ở Đông Dương đã bị tiêu diệt hoàn toàn và tự động trao trả chính quyền cho Việt Minh.",
                "answer": False,
                "explanation": "SAI (BẪY!). Quân Nhật ở Đông Dương lúc đó 'rệu rã, mất tinh thần' chứ chưa bị tiêu diệt hoàn toàn và cũng không tự động trao trả chính quyền; nhân dân ta vẫn phải kiên quyết chớp thời cơ vùng lên khởi nghĩa giành chính quyền."
            },
            {
                "key": "c",
                "text": "Cao trào kháng Nhật cứu nước (từ tháng 3 đến tháng 8/1945) đóng vai trò chuẩn bị lực lượng và tập dượt trực tiếp cho thắng lợi của Tổng khởi nghĩa.",
                "answer": True,
                "explanation": "ĐÚNG. Trực tiếp từ đoạn tư liệu và kiến thức SGK: cao trào kháng Nhật cứu nước chuẩn bị lực lượng, tập dượt quần chúng sẵn sàng tổng khởi nghĩa khi thời cơ đến."
            },
            {
                "key": "d",
                "text": "Thời cơ \"ngàn năm có một\" của Cách mạng tháng Tám xuất hiện từ khi Nhật đảo chính Pháp (9/3/1945) và kéo dài liên tục đến hết năm 1945.",
                "answer": False,
                "explanation": "SAI (BẪY!). Thời cơ ngàn năm có một rất ngắn ngủi, chỉ tồn tại từ khi Nhật đầu hàng Đồng minh (15/8/1945) đến TRƯỚC KHI quân Đồng minh kéo vào Đông Dương giải giáp quân Nhật (đầu tháng 9/1945)."
            }
        ]
    },
    {
        "id": "tf-02",
        "cat": "boi-canh",
        "title": "Chủ trương phát lệnh Tổng khởi nghĩa (13 – 18/8/1945)",
        "passage": "“Ngày 13 - 8 - 1945, ngay khi nhận được những thông tin về việc Nhật Bản sắp đầu hàng Đồng minh, Trung ương Đảng và Tổng bộ Việt Minh lập tức thành lập Ủy ban Khởi nghĩa toàn quốc, ban bố Quân lệnh số 1, chính thức phát lệnh Tổng khởi nghĩa trong cả nước. Từ ngày 14 đến ngày 15 - 8 - 1945, Hội nghị toàn quốc của Đảng họp ở Tân Trào (Tuyên Quang) thông qua kế hoạch lãnh đạo toàn dân Tổng khởi nghĩa... Từ ngày 16 đến ngày 17 - 8 - 1945, Đại hội Quốc dân được triệu tập ở Tân Trào, tán thành chủ trương Tổng khởi nghĩa của Đảng, thông qua 10 chính sách của Việt Minh, cử ra Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch.”",
        "source": "Tổng hợp theo SGK Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Ủy ban Khởi nghĩa toàn quốc đã ban bố Quân lệnh số 1 vào ngày 13/8/1945, chính thức phát lệnh Tổng khởi nghĩa trên phạm vi cả nước.",
                "answer": True,
                "explanation": "ĐÚNG. Đêm 13/8/1945, Trung ương Đảng và Tổng bộ Việt Minh thành lập Ủy ban Khởi nghĩa toàn quốc và ban bố Quân lệnh số 1 (23 giờ cùng ngày)."
            },
            {
                "key": "b",
                "text": "Hội nghị toàn quốc của Đảng (14 – 15/8/1945) đã bầu ra Ủy ban Dân tộc giải phóng Việt Nam do Hồ Chí Minh làm Chủ tịch.",
                "answer": False,
                "explanation": "SAI (BẪY ĐỔI SỰ KIỆN!). Ủy ban Dân tộc giải phóng Việt Nam do ĐẠI HỘI QUỐC DÂN TÂN TRÀO (16 – 17/8/1945) bầu ra, không phải Hội nghị toàn quốc của Đảng!"
            },
            {
                "key": "c",
                "text": "Việc Đảng phát lệnh Tổng khởi nghĩa trước cả khi Nhật hoàng chính thức tuyên bố đầu hàng (15/8) thể hiện sự nhạy bén, quyết đoán và chủ động nắm bắt thời cơ.",
                "answer": True,
                "explanation": "ĐÚNG. Khi vừa nắm chắc dấu hiệu Nhật sắp đầu hàng, Đảng lập tức ra Quân lệnh số 1 (13/8) để kịp thời huy động toàn dân giành chính quyền trước khi quân Đồng minh kéo vào."
            },
            {
                "key": "d",
                "text": "Đại hội Quốc dân Tân Trào thể hiện tinh thần đoàn kết và sự đồng lòng của toàn thể dân tộc Việt Nam trước giờ Tổng khởi nghĩa.",
                "answer": True,
                "explanation": "ĐÚNG. Đại hội Quốc dân quy tụ đại biểu các đảng phái, đoàn thể, dân tộc, tôn giáo... nhất trí tán thành chủ trương Tổng khởi nghĩa và thông qua 10 chính sách của Việt Minh."
            }
        ]
    },
    {
        "id": "tf-03",
        "cat": "dien-bien",
        "title": "Diễn biến 15 ngày Tổng khởi nghĩa (14/8 – 2/9/1945)",
        "passage": "“Từ ngày 14 - 8 - 1945, một số cấp bộ Đảng và tổ chức Việt Minh đã căn cứ vào tình hình cụ thể của địa phương phát động nhân dân khởi nghĩa giành chính quyền. Chiều 16 - 8 - 1945, một đơn vị Giải phóng quân do Võ Nguyên Giáp chỉ huy xuất phát từ Tân Trào tiến về giải phóng thị xã Thái Nguyên. Ngày 18 - 8 - 1945, nhân dân Bắc Giang, Hải Dương, Hà Tĩnh và Quảng Nam giành được chính quyền ở tỉnh lị sớm nhất cả nước. Tiếp đó, khởi nghĩa thắng lợi ở Hà Nội (19/8), Huế (23/8), Sài Gòn (25/8). Đến ngày 28/8, Đồng Nai Thượng và Hà Tiên là hai tỉnh cuối cùng giành được chính quyền. Ngày 30/8, vua Bảo Đại thoái vị. Ngày 2/9/1945, Chủ tịch Hồ Chí Minh đọc Tuyên ngôn Độc lập.”",
        "source": "Tóm lược diễn biến theo SGK Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Ngày 18/8/1945 là thời điểm đầu tiên nổ ra khởi nghĩa giành chính quyền ở Việt Nam trong Cách mạng tháng Tám.",
                "answer": False,
                "explanation": "SAI (BẪY!). Từ ngày 14/8/1945 đã có nhiều xã, huyện ở cơ sở chủ động khởi nghĩa giành chính quyền; ngày 18/8 là mốc 4 TỈNH LỊ giành chính quyền sớm nhất (Bắc Giang, Hải Dương, Hà Tĩnh, Quảng Nam)."
            },
            {
                "key": "b",
                "text": "Thắng lợi của khởi nghĩa ở ba đô thị lớn Hà Nội (19/8), Huế (23/8) và Sài Gòn (25/8) đã làm tê liệt đầu não của kẻ thù, quyết định thắng lợi trên cả nước.",
                "answer": True,
                "explanation": "ĐÚNG. Hà Nội, Huế, Sài Gòn là 3 trung tâm chính trị, kinh tế, quân sự lớn nhất 3 miền; giành được 3 nơi này tạo hiệu ứng lan tỏa quyết định toàn cục."
            },
            {
                "key": "c",
                "text": "Tổng khởi nghĩa tháng Tám năm 1945 giành thắng lợi trên phạm vi cả nước trong vòng 15 ngày (từ 14/8 đến 28/8/1945).",
                "answer": True,
                "explanation": "ĐÚNG. Bắt đầu từ 14/8 ở các địa phương cơ sở cho đến ngày 28/8 khi hai tỉnh cuối cùng (Đồng Nai Thượng và Hà Tiên) giành chính quyền = tròn 15 ngày."
            },
            {
                "key": "d",
                "text": "Sự kiện khởi nghĩa thắng lợi ở kinh đô Huế (23/8/1945) đã chính thức chấm dứt vĩnh viễn chế độ quân chủ phong kiến Việt Nam.",
                "answer": False,
                "explanation": "SAI (BẪY MỐC NGÀY!). Phải đến ngày 30/8/1945, khi vua Bảo Đại đọc chiếu thoái vị và trao ấn kiếm cho đại diện Chính phủ lâm thời thì chế độ quân chủ Việt Nam mới chính thức sụp đổ hoàn toàn."
            }
        ]
    },
    {
        "id": "tf-04",
        "cat": "nguyen-nhan-y-nghia",
        "title": "Ý nghĩa lịch sử & Bước ngoặt vĩ đại của dân tộc",
        "passage": "“Cách mạng tháng Tám năm 1945 là sự kiện lịch sử vĩ đại, đã lật đổ ách cai trị của thực dân Pháp trong hơn 80 năm, của quân phiệt Nhật Bản gần 5 năm; chấm dứt thời kì quân chủ hơn 1000 năm; lập nên nước Việt Nam Dân chủ Cộng hòa... Đảng Cộng sản Đông Dương từ một đảng bí mật trở thành đảng cầm quyền, nhân dân Việt Nam từ thân phận nô lệ trở thành người làm chủ đất nước. Cách mạng tháng Tám đã đánh dấu một bước tiến nhảy vọt trong lịch sử dân tộc: mở ra kỉ nguyên độc lập, tự do và phát triển dưới chế độ dân chủ cộng hòa.”",
        "source": "Sách giáo khoa Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Cách mạng tháng Tám năm 1945 đã chấm dứt đồng thời ách thống trị của chủ nghĩa thực dân, quân phiệt phát xít và chế độ quân chủ ở Việt Nam.",
                "answer": True,
                "explanation": "ĐÚNG. Tư liệu khẳng định rõ: lật đổ ách cai trị của thực dân Pháp (>80 năm), quân phiệt Nhật (gần 5 năm) và chấm dứt thời kì quân chủ (>1000 năm)."
            },
            {
                "key": "b",
                "text": "Thắng lợi của Cách mạng tháng Tám đã đưa Đảng Cộng sản Đông Dương từ một đảng hoạt động bí mật trở thành đảng cầm quyền.",
                "answer": True,
                "explanation": "ĐÚNG. Đây là chuyển biến lịch sử về địa vị chính trị của Đảng Cộng sản Đông Dương ngay sau khi Nhà nước Việt Nam Dân chủ Cộng hòa ra đời."
            },
            {
                "key": "c",
                "text": "Cách mạng tháng Tám đã xóa bỏ hoàn toàn mọi tàn dư của chế độ phong kiến và đưa cả nước Việt Nam bước ngay vào thời kì quá độ lên chủ nghĩa xã hội.",
                "answer": False,
                "explanation": "SAI (BẪY KÉP!). Cách mạng tháng Tám mới xóa bỏ chế độ quân chủ chứ chưa xóa bỏ hết tàn dư phong kiến (ruộng đất chưa giải quyết triệt để); và năm 1945 mở ra kỷ nguyên độc lập, tự do dưới chế độ dân chủ cộng hòa (đến sau năm 1975 cả nước mới cùng đi lên CNXH)."
            },
            {
                "key": "d",
                "text": "Nước Việt Nam Dân chủ Cộng hòa ra đời là nhà nước dân chủ nhân dân đầu tiên ở khu vực Đông Nam Á.",
                "answer": True,
                "explanation": "ĐÚNG. Sự ra đời của nước Việt Nam Dân chủ Cộng hòa (2/9/1945) đánh dấu nhà nước công nông / dân chủ nhân dân đầu tiên tại Đông Nam Á."
            }
        ]
    },
    {
        "id": "tf-05",
        "cat": "nguyen-nhan-y-nghia",
        "title": "Đánh giá của Chủ tịch Hồ Chí Minh & Tầm vóc quốc tế",
        "passage": "“Chẳng những giai cấp lao động và nhân dân Việt Nam ta có thể tự hào, mà giai cấp lao động và những dân tộc bị áp bức nơi khác cũng có thể tự hào rằng: Lần này là lần đầu tiên trong lịch sử cách mạng của các dân tộc thuộc địa và nửa thuộc địa, một Đảng mới 15 tuổi đã lãnh đạo cách mạng thành công, đã nắm chính quyền toàn quốc.”",
        "source": "Hồ Chí Minh Toàn tập, Tập 7 — trích trong SGK Lịch sử 12, bộ Kết nối tri thức với cuộc sống",
        "statements": [
            {
                "key": "a",
                "text": "Đoạn tư liệu khẳng định vai trò lãnh đạo đúng đắn, tài tình của Đảng Cộng sản Đông Dương là nhân tố quyết định hàng đầu đưa Cách mạng tháng Tám tới thắng lợi.",
                "answer": True,
                "explanation": "ĐÚNG. Chủ tịch Hồ Chí Minh nhấn mạnh mốc son 'một Đảng mới 15 tuổi đã lãnh đạo cách mạng thành công, đã nắm chính quyền toàn quốc' — khẳng định vai trò quyết định hàng đầu của Đảng."
            },
            {
                "key": "b",
                "text": "Thắng lợi của Cách mạng tháng Tám không chỉ có ý nghĩa với dân tộc Việt Nam mà còn cổ vũ mạnh mẽ phong trào giải phóng dân tộc trên thế giới.",
                "answer": True,
                "explanation": "ĐÚNG. Tư liệu chỉ rõ 'những dân tộc bị áp bức nơi khác cũng có thể tự hào' — thể hiện sức cổ vũ to lớn đối với phong trào giải phóng dân tộc thuộc địa và phụ thuộc."
            },
            {
                "key": "c",
                "text": "Chiến thắng của Hồng quân Liên Xô và lực lượng Đồng minh là nguyên nhân quyết định nhất, thay thế cho vai trò lãnh đạo của Đảng trong Cách mạng tháng Tám.",
                "answer": False,
                "explanation": "SAI (BẪY KINH ĐIỂN!). Chiến thắng của Liên Xô và Đồng minh là nguyên nhân KHÁCH QUAN tạo điều kiện thuận lợi, tuyệt đối không thể thay thế nguyên nhân chủ quan quyết định là sự lãnh đạo của Đảng và sức mạnh toàn dân."
            },
            {
                "key": "d",
                "text": "Con số \"15 tuổi\" trong đoạn tư liệu phản ánh quá trình chuẩn bị lực lượng bền bỉ của Đảng Cộng sản Đông Dương từ năm 1930 đến năm 1945.",
                "answer": True,
                "explanation": "ĐÚNG. Đảng thành lập đầu năm 1930 đến tháng 8/1945 là tròn 15 năm chuẩn bị chu đáo qua ba phong trào cách mạng (1930–1931, 1936–1939, 1939–1945)."
            }
        ]
    },
    {
        "id": "tf-06",
        "cat": "bai-hoc-tinh-chat",
        "title": "Nghệ thuật khởi nghĩa, Phương pháp & Tính chất",
        "passage": "“Cách mạng tháng Tám năm 1945 diễn ra trong bối cảnh thời cơ cách mạng xuất hiện nhanh chóng nhưng cũng có nguy cơ qua đi rất nhanh. Dưới sự lãnh đạo của Đảng và Chủ tịch Hồ Chí Minh, toàn dân tộc đã triệu người như một vùng lên giành chính quyền từ tay phát xít Nhật và tay sai, kết hợp chặt chẽ giữa nông thôn với thành thị, giữa lực lượng chính trị của quần chúng với lực lượng vũ trang cách mạng, giành thắng lợi nhanh chóng và ít đổ máu.”",
        "source": "Tổng hợp kiến thức trọng tâm Bài 6, SGK Lịch sử 12 Kết nối tri thức",
        "statements": [
            {
                "key": "a",
                "text": "Trong Cách mạng tháng Tám năm 1945, nhân dân ta đã giành chính quyền trực tiếp từ tay phát xít Nhật và chính quyền tay sai thân Nhật.",
                "answer": True,
                "explanation": "ĐÚNG. Thực dân Pháp đã bị Nhật đảo chính lật đổ từ đêm 9/3/1945 nên tháng 8/1945 kẻ thù trực tiếp bị ta đánh đổ để giành chính quyền là phát xít Nhật và tay sai."
            },
            {
                "key": "b",
                "text": "Lực lượng vũ trang cách mạng giữ vai trò quyết định trực tiếp, còn lực lượng chính trị của quần chúng chỉ đóng vai trò hỗ trợ.",
                "answer": False,
                "explanation": "SAI (BẪY ĐẢO VAI TRÒ!). Ngược lại: LỰC LƯỢNG CHÍNH TRỊ của quần chúng nhân dân giữ vai trò quyết định, còn lực lượng vũ trang giữ vai trò nòng cốt, xung kích hỗ trợ."
            },
            {
                "key": "c",
                "text": "Cách mạng tháng Tám năm 1945 là cuộc cách mạng giải phóng dân tộc điển hình, đồng thời mang tính chất dân chủ mới.",
                "answer": True,
                "explanation": "ĐÚNG. Đây là tính chất chuẩn xác của Cách mạng tháng Tám: đặt nhiệm vụ giải phóng dân tộc lên hàng đầu và lập nên nhà nước dân chủ cộng hòa của nhân dân."
            },
            {
                "key": "d",
                "text": "Cuộc Tổng khởi nghĩa kết hợp hài hòa địa bàn nông thôn và thành thị, đi từ khởi nghĩa từng phần tiến lên tổng khởi nghĩa.",
                "answer": True,
                "explanation": "ĐÚNG. Từ tháng 3 đến giữa tháng 8/1945 là khởi nghĩa từng phần chủ yếu ở nông thôn; giữa tháng 8 bùng nổ tổng khởi nghĩa kết hợp cả nông thôn và thành thị."
            }
        ]
    },
    {
        "id": "tf-07",
        "cat": "nguyen-nhan-y-nghia",
        "title": "Nguyên nhân chủ quan & Bác bỏ luận điệu \"ăn may\"",
        "passage": "“Thắng lợi của Cách mạng tháng Tám năm 1945 là kết quả tổng hợp của nhiều nguyên nhân chủ quan và khách quan. Nhân dân Việt Nam có truyền thống yêu nước nồng nàn, tinh thần đoàn kết, ý chí đấu tranh kiên cường bất khuất vì độc lập, tự do. Dưới sự lãnh đạo của Đảng Cộng sản Đông Dương đứng đầu là Chủ tịch Hồ Chí Minh, lực lượng cách mạng đã được chuẩn bị chu đáo qua 15 năm đấu tranh. Đồng thời, chiến thắng của Hồng quân Liên Xô và các nước Đồng minh trong cuộc chiến tranh chống phát xít đã tạo ra thời cơ khách quan thuận lợi.”",
        "source": "Theo SGK Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Truyền thống yêu nước nồng nàn và tinh thần đoàn kết của nhân dân Việt Nam là một trong những nguyên nhân chủ quan dẫn tới thắng lợi.",
                "answer": True,
                "explanation": "ĐÚNG. Đây là nền tảng tinh thần quý báu thuộc nhóm nguyên nhân chủ quan tạo nên sức mạnh toàn dân."
            },
            {
                "key": "b",
                "text": "Cách mạng tháng Tám thành công chủ yếu do sự \"ăn may\" khi lợi dụng \"khoảng trống quyền lực\" sau khi Nhật đầu hàng.",
                "answer": False,
                "explanation": "SAI. Luận điệu 'ăn may' là hoàn toàn sai trái; thắng lợi có được nhờ 15 năm chuẩn bị chu đáo về đường lối, lực lượng, căn cứ địa và nghệ thuật chớp thời cơ chủ động của Đảng."
            },
            {
                "key": "c",
                "text": "Mối quan hệ giữa nguyên nhân chủ quan và khách quan trong Cách mạng tháng Tám cho thấy nội lực bên trong giữ vai trò quyết định, còn điều kiện bên ngoài tạo thời cơ thuận lợi.",
                "answer": True,
                "explanation": "ĐÚNG. Có thời cơ khách quan nhưng nếu không chuẩn bị sẵn nội lực chủ quan thì không thể chớp được thời cơ và giành thắng lợi nhanh chóng."
            },
            {
                "key": "d",
                "text": "Chỉ có riêng Việt Nam ở Đông Nam Á có điều kiện khách quan phát xít Nhật đầu hàng trong tháng 8 năm 1945.",
                "answer": False,
                "explanation": "SAI. Toàn bộ khu vực Đông Nam Á bị Nhật chiếm đóng đều có chung điều kiện khách quan là Nhật đầu hàng Đồng minh (15/8/1945), nhưng chỉ Việt Nam, In-đô-nê-xi-a và Lào chớp thời cơ tuyên bố độc lập kịp thời trong năm 1945."
            }
        ]
    },
    {
        "id": "tf-08",
        "cat": "bai-hoc-tinh-chat",
        "title": "Bài học kinh nghiệm & Giá trị vận dụng hiện nay",
        "passage": "“Thắng lợi của Cách mạng tháng Tám năm 1945 để lại nhiều bài học kinh nghiệm quý báu đối với sự nghiệp xây dựng và bảo vệ Tổ quốc: bài học về sự lãnh đạo của Đảng với đường lối đúng đắn, chủ động, linh hoạt, sáng tạo; bài học về xây dựng và phát huy sức mạnh khối đại đoàn kết toàn dân tộc gắn liền với vai trò của Mặt trận Việt Minh; bài học về xác định đúng và mau lẹ nắm bắt thời cơ; bài học về kết hợp sức mạnh dân tộc với sức mạnh thời đại.”",
        "source": "Theo SGK Lịch sử 12, bộ Kết nối tri thức với cuộc sống, Bài 6",
        "statements": [
            {
                "key": "a",
                "text": "Bài học về sự lãnh đạo đúng đắn, sáng tạo của Đảng trên cơ sở vận dụng chủ nghĩa Mác - Lênin vào thực tiễn Việt Nam vẫn giữ nguyên giá trị trong thời kì Đổi mới hiện nay.",
                "answer": True,
                "explanation": "ĐÚNG. Sự lãnh đạo đúng đắn, linh hoạt, sáng tạo của Đảng là bài học hàng đầu xuyên suốt từ Cách mạng tháng Tám đến sự nghiệp xây dựng và bảo vệ Tổ quốc hôm nay."
            },
            {
                "key": "b",
                "text": "Trong Cách mạng tháng Tám năm 1945, khối đại đoàn kết toàn dân tộc được tập hợp rộng rãi thông qua Mặt trận Tổ quốc Việt Nam.",
                "answer": False,
                "explanation": "SAI (BẪY TÊN MẶT TRẬN!). Năm 1945 là MẶT TRẬN VIỆT MINH! Còn Mặt trận Tổ quốc Việt Nam được thành lập sau này (năm 1955) và hoạt động hiện nay."
            },
            {
                "key": "c",
                "text": "Bài học về nắm bắt thời cơ gợi mở cho Việt Nam ngày nay cần chủ động phân tích tình hình quốc tế, tận dụng cơ hội từ hội nhập và khoa học – công nghệ để phát triển đất nước.",
                "answer": True,
                "explanation": "ĐÚNG. Vận dụng sáng tạo bài học chớp thời cơ giúp đất nước chủ động hội nhập, phát triển kinh tế – công nghệ và ứng phó kịp thời với thách thức."
            },
            {
                "key": "d",
                "text": "Trong bài học kết hợp sức mạnh dân tộc với sức mạnh thời đại, tranh thủ nguồn lực bên ngoài luôn giữ vai trò quyết định hơn sức mạnh nội lực.",
                "answer": False,
                "explanation": "SAI (BẪY ĐẢO VAI TRÒ!). Sức mạnh dân tộc (nội lực bên trong) luôn giữ vai trò QUYẾT ĐỊNH; sức mạnh thời đại (nguồn lực, điều kiện quốc tế) là nhân tố quan trọng để kết hợp, cộng hưởng."
            }
        ]
    }
]

# ============================================================================
# 8. THREE CURATED 15-MINUTE MOCK EXAMS (12 MCQ + 2 TF = 10.0 điểm / 15 phút)
#    Đề 01 & Đề 02 appear verbatim in BOTH the PDF and the Web App!
#    Đề 03 is an extra advanced mock exam in the Web App!
# ============================================================================
EXAMS = [
    {
        "id": "de-01",
        "code": "ĐỀ SỐ 01",
        "name": "Đề 01 • Cơ Bản & Trọng Tâm SGK",
        "subtitle": "Bám sát 100% kiến thức cốt lõi Bài 6 KNTT • Chuẩn cấu trúc 15 phút",
        "badge": "Có trong PDF",
        "duration_min": 15,
        "mc_ids": [
            "mc-01", "mc-03", "mc-06", "mc-07",
            "mc-08", "mc-15", "mc-17", "mc-18",
            "mc-20", "mc-29", "mc-32", "mc-43"
        ],
        "tf_ids": ["tf-01", "tf-04"]
    },
    {
        "id": "de-02",
        "code": "ĐỀ SỐ 02",
        "name": "Đề 02 • Thông Hiểu & Chống Bẫy 10/10",
        "subtitle": "Chuyên trị các câu bẫy mốc ngày, bẫy vai trò lực lượng & từ khóa dễ nhầm",
        "badge": "Có trong PDF",
        "duration_min": 15,
        "mc_ids": [
            "mc-04", "mc-10", "mc-12", "mc-19",
            "mc-22", "mc-26", "mc-28", "mc-31",
            "mc-37", "mc-38", "mc-46", "mc-51"
        ],
        "tf_ids": ["tf-02", "tf-05"]
    },
    {
        "id": "de-03",
        "code": "ĐỀ SỐ 03",
        "name": "Đề 03 • Tổng Hợp Vận Dụng Cao",
        "subtitle": "Bộ câu hỏi mở rộng luyện phản xạ nhanh trước giờ vào lớp",
        "badge": "Đề Web nâng cao",
        "duration_min": 15,
        "mc_ids": [
            "mc-02", "mc-05", "mc-09", "mc-14",
            "mc-16", "mc-21", "mc-23", "mc-34",
            "mc-35", "mc-36", "mc-48", "mc-52"
        ],
        "tf_ids": ["tf-03", "tf-08"]
    }
]


def balance_mc_options():
    """Deterministically rebalance A/B/C/D answer indices so every curated exam
    has an exact 3/3/3/3 distribution (no predictable pattern) and the full
    52-question bank has an exact 13/13/13/13 split."""
    mc_by_id = {q["id"]: q for q in MC_QUESTIONS}

    # Exact target patterns (no 3-in-a-row, exact 3x A/B/C/D per exam)
    exam_patterns = [
        [1, 3, 0, 2, 0, 3, 2, 1, 3, 0, 1, 2],  # Đề 01: 3A, 3B, 3C, 3D
        [3, 0, 2, 1, 0, 3, 1, 2, 2, 1, 3, 0],  # Đề 02: 3A, 3B, 3C, 3D
        [0, 2, 3, 1, 2, 0, 3, 1, 1, 3, 0, 2],  # Đề 03: 3A, 3B, 3C, 3D
    ]
    assigned = {}
    for ex, pat in zip(EXAMS, exam_patterns):
        for qid, target_idx in zip(ex["mc_ids"], pat):
            assigned[qid] = target_idx

    # Remaining 16 MCQs not in the 3 exams -> 4 each of 0, 1, 2, 3
    remaining = [q["id"] for q in MC_QUESTIONS if q["id"] not in assigned]
    rem_pat = [0, 2, 1, 3, 2, 0, 3, 1, 1, 3, 0, 2, 3, 1, 2, 0]
    for i, qid in enumerate(remaining):
        assigned[qid] = rem_pat[i % len(rem_pat)]

    for q in MC_QUESTIONS:
        target = assigned[q["id"]]
        cur = q["answer"]
        if cur != target:
            opts = list(q["options"])
            opts[cur], opts[target] = opts[target], opts[cur]
            q["options"] = opts
            q["answer"] = target


balance_mc_options()


def validate_data():
    """Run strict automated integrity checks on the entire content bank."""
    mc_by_id = {}
    ans_dist = {0: 0, 1: 0, 2: 0, 3: 0}
    cat_dist = {}
    for q in MC_QUESTIONS:
        assert q["id"] not in mc_by_id, f"Duplicate MC id: {q['id']}"
        assert len(q["options"]) == 4, f"{q['id']} must have 4 options"
        assert len(set(q["options"])) == 4, f"{q['id']} has duplicate options"
        assert q["answer"] in (0, 1, 2, 3), f"{q['id']} invalid answer index"
        assert q["explanation"].strip(), f"{q['id']} missing explanation"
        mc_by_id[q["id"]] = q
        ans_dist[q["answer"]] += 1
        cat_dist[q["cat"]] = cat_dist.get(q["cat"], 0) + 1

    tf_by_id = {}
    tf_bool_dist = {True: 0, False: 0}
    for t in TF_QUESTIONS:
        assert t["id"] not in tf_by_id, f"Duplicate TF id: {t['id']}"
        assert len(t["statements"]) == 4, f"{t['id']} must have 4 statements"
        keys = [s["key"] for s in t["statements"]]
        assert keys == ["a", "b", "c", "d"], f"{t['id']} keys mismatch"
        for s in t["statements"]:
            assert isinstance(s["answer"], bool)
            assert s["explanation"].strip()
            tf_bool_dist[s["answer"]] += 1
        tf_by_id[t["id"]] = t

    for ex in EXAMS:
        assert len(ex["mc_ids"]) == 12, f"{ex['id']} must have 12 MCs"
        assert len(set(ex["mc_ids"])) == 12, f"{ex['id']} duplicate MCs"
        assert len(ex["tf_ids"]) == 2, f"{ex['id']} must have 2 TFs"
        assert len(set(ex["tf_ids"])) == 2, f"{ex['id']} duplicate TFs"
        ex_dist = {0: 0, 1: 0, 2: 0, 3: 0}
        for mid in ex["mc_ids"]:
            assert mid in mc_by_id, f"{ex['id']} unknown MC {mid}"
            ex_dist[mc_by_id[mid]["answer"]] += 1
        for tid in ex["tf_ids"]:
            assert tid in tf_by_id, f"{ex['id']} unknown TF {tid}"
        print(f"     {ex['code']} A/B/C/D balance: {ex_dist}")

    # Check overlap between Đề 01, Đề 02, Đề 03 (0 overlap across all 3!)
    for i in range(len(EXAMS)):
        for j in range(i + 1, len(EXAMS)):
            ov_mc = set(EXAMS[i]["mc_ids"]) & set(EXAMS[j]["mc_ids"])
            ov_tf = set(EXAMS[i]["tf_ids"]) & set(EXAMS[j]["tf_ids"])
            assert not ov_mc, f"{EXAMS[i]['id']} & {EXAMS[j]['id']} share MC: {ov_mc}"
            assert not ov_tf, f"{EXAMS[i]['id']} & {EXAMS[j]['id']} share TF: {ov_tf}"

    print(f"[OK] Validated {len(MC_QUESTIONS)} MCQs, {len(TF_QUESTIONS)} TFs ({len(TF_QUESTIONS)*4} statements), {len(FLASHCARDS)} Flashcards, {len(TIMELINE)} Timeline milestones, {len(TRAPS)} Traps, {len(EXAMS)} Exams.")
    print(f"     MC answer distribution A/B/C/D: {ans_dist}")
    print(f"     MC category distribution: {cat_dist}")
    print(f"     TF statement True/False balance: {tf_bool_dist}")


def export_web_data(out_js_path):
    import json
    payload = {
        "meta": META,
        "categories": CATEGORIES,
        "theory": THEORY_SECTIONS,
        "timeline": TIMELINE,
        "traps": TRAPS,
        "sources": SOURCES,
        "flashcards": FLASHCARDS,
        "mc": MC_QUESTIONS,
        "tf": TF_QUESTIONS,
        "exams": EXAMS,
    }
    js_str = (
        "// Auto-generated from content_data.py — Single source of truth for Web & PDF\n"
        "window.SU12_B6 = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    )
    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write(js_str)
    print(f"[OK] Exported {out_js_path} ({len(js_str):,} chars)")


if __name__ == "__main__":
    import os
    validate_data()
    here = os.path.dirname(os.path.abspath(__file__))
    export_web_data(os.path.join(here, "data.js"))
