import streamlit as st
import time
from streamlit_lottie import st_lottie
from functions import set_design, load_lottieurl, show_wish, shake_error

# 1. Khởi tạo giao diện và CSS
set_design()

# 2. Khởi tạo Session State (Trạng thái ứng dụng)
if 'step' not in st.session_state: st.session_state.step = 1
if 'auth_sub_step' not in st.session_state: st.session_state.auth_sub_step = 0
if 'greeting_sub_step' not in st.session_state: st.session_state.greeting_sub_step = 0
if 'confirm_choice' not in st.session_state: st.session_state.confirm_choice = False
if 'result_shown' not in st.session_state: st.session_state.result_shown = False
if 'final_gift_id' not in st.session_state: st.session_state.final_gift_id = None
if 'error_msg' not in st.session_state: st.session_state.error_msg = None

# Quản lý 2 lượt chơi và quà tặng
if 'turns_played' not in st.session_state: st.session_state.turns_played = 0
if 'chosen_gift_ids' not in st.session_state: st.session_state.chosen_gift_ids = []

# Ngân hàng quà tặng (4 QR và 1 hộp troll)
GIFTS = {
    1: {
        "name": "Lì xì May mắn 🧧\n\nCap màn hình lại ngayyy nha...",
        "type": "qr",
        "image": "assets/qr1.jpg",
        "caption": "Quét cái này là nhận may mắn cả năm ✨\nCòn nếu muốn may mắn cả đời thì nhắn mìn để hỏi nhé... 💌"
    },
    2: {
        "name": "Giải Độc đắc 💎\n\nCap màn hình lại ngayyy nha...",
        "type": "qr",
        "image": "assets/qr1.jpg",
        "caption": "Chúc mừng em trúng giải độc đắc nhaa 💎\nNhưng độc đắc là gì thì từ từ rồi sẽ bít. 😉"
    },
    3: {
        "name": "Trà sữa Full Topping 🧋\n\nCap màn hình lại ngayyy nha...",
        "type": "qr",
        "image": "assets/qr1.jpg",
        "caption": "Trà sữa full topping cho người ngọt ngào nhất hôm nay 🧋😌"
    },
    4: {
        "name": "Chúc em may mắn lần sau 😅",
        "type": "troll",
        "image": None,
        "caption": "Đen thì phải gì ạ...😅\n\nNhưng thui không sao vì, em vẫn sẽ là ưu tiên mà 💛"
    },
    5: {
        "name": "Cốc nước dừa (Bị Trộm) 🕯️\n\nCap màn hình lại ngayyy nha...",
        "type": "qr",
        "image": "assets/qr1.jpg",
        "caption": "Anh đã tìm được cốc nước dừa em bị uống mất rồi nhaa 🕯️"
    }
}

main_container = st.container()

with main_container:
    # --- GIAI ĐOẠN 1: GIẢI MÃ (3 CÂU HỎI) ---
    if st.session_state.step == 1:
        # Cổng chào
        if st.session_state.auth_sub_step == 0:
            st.markdown("<h2 style='text-align: center;'>🔐 Khởi động vài câu hỏi ikk</h2>", unsafe_allow_html=True)
            lottie_gate = load_lottieurl("https://lottie.host/ceea23a6-3887-4b76-911e-51537b4e391b/KzOudZKZmY.json")
            if lottie_gate:
                st_lottie(lottie_gate, height=280, key="gate_animation")
            st.markdown("<p style='text-align: center;'>Hi Ngừi Đệpppp! Giải mã để nhận quà nhaaa!</p>", unsafe_allow_html=True)
            st.markdown('<div class="wobble-btn">', unsafe_allow_html=True)
            if st.button("🚀 LẸT GOOO..."):
                st.session_state.auth_sub_step = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Logic 3 câu hỏi
        elif 1 <= st.session_state.auth_sub_step <= 3:
            current_q = st.session_state.auth_sub_step
            st.markdown(f"<p style='text-align: center; color: #FFD700; font-weight: bold;'>Thử thách {current_q} / 3</p>", unsafe_allow_html=True)
            st.progress(current_q / 3)
            
            questions = {
                1: {
                    "q": "Trong suy nghĩ của mìn, điều gì khiến bạn trở nên đặc biệt? ✨💌✨",
                    "options": {
                        "a": "Nụ cười",
                        "b": "Sự khác biệt",
                        "c": "Phong cách",
                        "d": "Sự dịu dàng"
                    },
                    "a": "b"
                },
                2: {
                    "q": "Trong buổi tất niên hôm đó, điều gì 'đáng tiếc' nhất xảy ra với elm? 😅😅😅",
                    "options": {
                        "a": "Bị chôm chôm chìa khoá",
                        "b": "Về quá trễ",
                        "c": "Bị uống mất cốc nước dừa",
                        "d": "Uống nước lọc thay rượu (lừa thầy dối bạn)"
                    },
                    "a": "c"
                },
                3: {
                    "q": "Nếu năm mới này có thêm một người luôn sẵn sàng lắng nghe và ủng hộ bạn, em có sẵn sang mở lòng không? 😊",
                    "a": "có"
                }
            }

            question_data = questions[current_q]

            st.markdown(f"<h3 style='text-align: center;'>{question_data['q']}</h3>", unsafe_allow_html=True)

            # Nếu có options → dùng radio
            if "options" in question_data:
                user_ans = st.radio(
                    "Chọn đáp án:",
                    options=list(question_data["options"].keys()),
                    format_func=lambda x: f"{x.upper()}. {question_data['options'][x]}",
                    key=f"radio_{current_q}"
                )
            else:
                user_ans = st.text_input(
                    "Nhập câu trả lời...",
                    key=f"q_input_{current_q}"
                ).lower().strip()
            
            if st.session_state.error_msg:
                shake_error(st.session_state.error_msg)
                st.session_state.error_msg = None

            if st.button("KIỂM TRA ✅", key=f"btn_{current_q}"):
                correct_answer = question_data["a"]

                if user_ans == correct_answer:
                    st.balloons()
                    st.success("Chính xác luôn! Giọiiiii quá!")
                    time.sleep(2.0) 
                    if current_q < 3:
                        st.session_state.auth_sub_step += 1
                    else:
                        st.session_state.auth_sub_step = 6
                    st.rerun()
                else:
                    st.session_state.error_msg = "Chưa juan rồi, thử lại ngayyyy ❤️"
                    st.rerun()

        # Màn chuyển tiếp 1 -> 2
        elif st.session_state.auth_sub_step == 6:
            st.markdown("<h2 style='text-align: center;'>🎊 XỊN HÉEEEEE! 🎊</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Em đã vượt qua tất cả thử thách. Bây giờ là lúc nhận phần thưởng!</p>", unsafe_allow_html=True)
            st.markdown('<div class="wobble-btn">', unsafe_allow_html=True)
            if st.button("🎁 XEM QUÀ NGAY ĐI"):
                st.session_state.step = 2
                st.session_state.greeting_sub_step = 0
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- GIAI ĐOẠN 2: NGHI THỨC MỞ QUÀ ---
    elif st.session_state.step == 2:
        # 2.0: Hộp quà lắc lư
        if st.session_state.greeting_sub_step == 0:
            st.markdown("<h2 style='text-align: center;'>✨ MÓN QUÀ BÍ MẬT ✨</h2>", unsafe_allow_html=True)
            lottie_gift_big = load_lottieurl("https://lottie.host/6a567954-207d-4b53-911d-283e15545232/vB8NOf3mP6.json")
            if lottie_gift_big:
                st_lottie(lottie_gift_big, height=350, key="gift_big_shaking")
            
            st.markdown('<div class="wobble-btn">', unsafe_allow_html=True)
            if st.button("🧧 MỞ NGAY ĐIIII"):
                st.session_state.greeting_sub_step = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # 2.1: Bung lời chúc ngay lập tức
        elif st.session_state.greeting_sub_step == 1:
            lottie_firework = load_lottieurl("https://lottie.host/3888fa0a-809b-424e-8dee-d3086f49a270/KWFTtoyVas.json")
            if lottie_firework:
                st_lottie(lottie_firework, height=220, key="fireworks_reveal")
            st.balloons()
            
            wish_text = (
                "Chúc mừng năm mới Ất Tỵ 2026! 🐍✨🎉\n\n"
                "Chúc em một năm thật rực rỡ 🌸, luôn giữ được sự cá tính và đặc biệt theo cách rất riêng của chính bản thân elm 💫.\n"
                "Mong mọi điều tốt đẹp, may mắn và bình an 🍀🌿 sẽ luôn đồng hành cùng em trong từng chặng đường.\n"
                "Hy vọng năm mới này anh sẽ có thêm nhiều cơ hội được hiểu em nhiều hơn một chút 😊😊😊"
            )           
            show_wish(wish_text)
            
            if st.button("TIẾP TỤC 👉"):
                st.session_state.greeting_sub_step = 2
                st.rerun()

        # 2.2: Màn chuyển tiếp 2 -> 3
        elif st.session_state.greeting_sub_step == 2:
            st.markdown("<h2 style='text-align: center;'>💝 TIẾP THEO LÀ... 💝</h2>", unsafe_allow_html=True)
            lottie_ready = load_lottieurl("https://lottie.host/57530e9d-773a-446a-8b36-541575f0a0e9/yT51WkX6Ld.json")
            if lottie_ready:
                st_lottie(lottie_ready, height=250, key="ready_gacha")
            st.markdown("<p style='text-align: center;'>Anh gửi bạn <b>2 lượt chọn</b> hộp quà may mắn henggg!</p>", unsafe_allow_html=True)
            st.markdown('<div class="wobble-btn">', unsafe_allow_html=True)
            if st.button("🕹 NHANH CHO NÓNG..."):
                st.session_state.step = 3
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # --- GIAI ĐOẠN 3: KHO BÁU LÌ XÌ (2 LƯỢT) ---
    elif st.session_state.step == 3:
        # A. Màn hình Kết thúc (Byee Byee)
        if st.session_state.turns_played >= 2:
            st.markdown("<h1 style='text-align: center;'>✨ BYEE BYEE ✨</h1>", unsafe_allow_html=True)
            lottie_bye = load_lottieurl("https://lottie.host/9327e366-512c-4999-a477-88d4001a1c31/z0L2RjYgIe.json")
            if lottie_bye:
                st_lottie(lottie_bye, height=300, key="bye_animation")
            st.markdown("<h3 style='text-align: center; color: #FFD700;'>Thật sự là a mới nghĩ ra code đến đoạn này thui ý. Ỏ...</h3>", unsafe_allow_html=True)
            # st.write("<p style='text-align: left;'>Anh cảm ơn bạn đã chịu xem đến cuối. Hẹn gặp lại em (cô gái đặc biệt) ở những thứ 'lỏ lỏ, odds and ends' tiếp nhé. <br> Nhưng vẫn mong năm mới thật nhiều ý nghĩa và luôn mỉm cười với elm. 😊</p>", unsafe_allow_html=True)
            st.write("<p style='text-align: left;'>Anh cảm ơn em vì đã dành thời gian xem đến cuối.\n\nHẹn gặp lại em (cô gái đặc biệt) ở những điều nho nhỏ, “lỏ lỏ”, những odds and ends thú vị phía trước nhé.\n\nVà vẫn mong năm mới của em sẽ thật nhiều ý nghĩa, luôn mỉm cười thật tươi. 😊</p>", unsafe_allow_html=True)

        # B. Màn hình chọn hộp quà
        elif not st.session_state.confirm_choice:
            st.markdown(f"<h2 style='text-align: center;'>🧧 Lượt {st.session_state.turns_played + 1} / 2</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Hãy chọn một hộp quà may mắn nhe!</p>", unsafe_allow_html=True)
            
            # Phóng to hộp quà bằng wrapper CSS
            st.markdown('<div class="gift-box-container">', unsafe_allow_html=True)
            cols = st.columns(3)
            box_idx = 0
            for i in range(1, 6):
                # Chỉ hiện những hộp chưa bị chọn ở lượt trước
                if i not in st.session_state.chosen_gift_ids:
                    with cols[box_idx % 3]:
                        if st.button(f"🎁", key=f"box_{i}"):
                            st.session_state.final_gift_id = i
                            st.session_state.confirm_choice = True
                            st.rerun()
                    box_idx += 1
            st.markdown('</div>', unsafe_allow_html=True)
        
        # C. Màn hình Xác nhận & Kết quả
        else:
            selected_id = st.session_state.final_gift_id
            gift_data = GIFTS[selected_id]
            
            if not st.session_state.result_shown:
                # 1. Xác nhận
                st.warning(f"⚠️ Em đã chọn hộp quà số {selected_id}!")
                st.write("<p style='text-align: center;'>Chắc chắn chưa Nàngggg? Chọn sai phải chịu nha.</p>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("CHỐT LUÔN! ✅"):
                        st.session_state.result_shown = True
                        st.rerun()
                with c2:
                    if st.button("CHỌN LẠI... 🔄"):
                        st.session_state.confirm_choice = False
                        st.rerun()
            else:
                # 2. Hiển thị quà
                st.balloons()
                if gift_data["type"] == "qr":
                    st.success(f"🎉 TRÚNG RỒI: {gift_data['name']}")
                    st.image(gift_data["image"], width='stretch')
                    st.info(gift_data["caption"])
                else:
                    st.error(f"😅 {gift_data['name']}")
                    st.info(gift_data["caption"])
                
                # Logic chuyển lượt hoặc kết thúc
                if st.session_state.turns_played + 1 < 2:
                    if st.button("CHỌN TIẾP LƯỢT 2 🧧"):
                        st.session_state.chosen_gift_ids.append(selected_id)
                        st.session_state.turns_played += 1
                        st.session_state.confirm_choice = False
                        st.session_state.result_shown = False
                        st.rerun()
                else:
                    if st.button("XEM KẾT THÚC ✨"):
                        st.session_state.chosen_gift_ids.append(selected_id)
                        st.session_state.turns_played += 1
                        st.rerun()
