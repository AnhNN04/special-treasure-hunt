import streamlit as st
import requests
import time

# 1. Hàm load hiệu ứng Lottie từ URL
@st.cache_data(show_spinner=False)
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# 2. Hàm hiển thị lời chúc (Hiện toàn bộ chữ rực rỡ)
def show_wish(text):
    st.markdown(f"""
        <div class="wish-container">
            {text}
        </div>
    """, unsafe_allow_html=True)

# 3. Hàm hiển thị thông báo lỗi rung lắc
def shake_error(msg):
    st.markdown(f"""
        <div class="shake-container">
            ⚠️ {msg}
        </div>
    """, unsafe_allow_html=True)

# 4. Hàm Custom CSS (Xử lý triệt để lỗi đè giao diện và tối ưu Mobile)
def set_design():
    st.markdown("""
        <style>
        /* Ẩn các thành phần thừa của Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        div[data-testid="stStatusWidget"] {display: none;}
        
        /* Khử lỗi mờ màn hình khi chuyển cảnh */
        [data-testid="stAppViewContainer"] {
            opacity: 1 !important;
            filter: none !important;
        }

        /* Nền Gradient di động */
        .stApp {
            background: linear-gradient(180deg, #1A0A2E 0%, #4A0E4E 50%, #880E4F 100%);
            background-attachment: fixed;
        }

        /* HIỆU ỨNG FADE-IN MƯỢT MÀ (1.5s) */
        @keyframes fadeEffect {
            0% { opacity: 0; transform: translateY(25px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* CONTAINER CHÍNH CĂN GIỮA TUYỆT ĐỐI */
        .main .block-container {
            max-width: 500px;
            padding-top: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            text-align: center;
            animation: fadeEffect 1.5s ease-in-out;
        }

        /* FIX LỖI ĐÈ NHAU: Tăng Gap giữa các phần tử */
        [data-testid="stVerticalBlock"] > div {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            gap: 35px !important;
        }

        /* TÙY CHỈNH Ô NHẬP LIỆU */
        .stTextInput { 
            width: 100% !important; 
            margin-bottom: 15px !important;
            overflow: visible !important; 
        }
        
        [data-testid="stTextInputRootElement"] {
            overflow: visible !important;
            background: transparent !important;
        }

        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.1);
            color: white !important;
            border-radius: 18px;
            border: 2px solid #FF4B4B !important;
            text-align: center;
            height: 3.8em;
            font-size: 16px;
            box-sizing: border-box;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #FFD700 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
        }

        /* KHUNG LỜI CHÚC SANG TRỌNG */
        .wish-container {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px;
            border: 2px dashed #FFD700;
            color: #FFD700;
            font-size: 20px;
            font-weight: bold;
            line-height: 1.6;
            text-align: left;    /* Đổi thành left để căn lề trái */
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.3);
            animation: fadeEffect 1s ease-in;
            margin: 20px 0;
            white-space: pre-line;
        }

        /* HIỆU ỨNG NÚT BẤM (PULSE) */
        @keyframes pulseBtn {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.5); }
            70% { transform: scale(1.04); box-shadow: 0 0 0 15px rgba(255, 75, 75, 0); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
        }

        div.stButton > button {
            display: block;
            margin: 15px auto !important;
            width: 100%;
            max-width: 280px;
            border-radius: 50px;
            height: 3.8em;
            background: linear-gradient(90deg, #FF4B4B 0%, #FF8E53 100%);
            color: white !important;
            font-weight: bold;
            font-size: 18px !important;
            border: none;
            box-shadow: 0px 5px 20px rgba(255, 75, 75, 0.4);
            animation: pulseBtn 1s infinite;
        }

        /* Nút Wobble nhanh cho Call To Action */
        @keyframes superWobble {
            0% { transform: rotate(0); }
            20% { transform: rotate(-3deg) scale(1.05); }
            40% { transform: rotate(3deg) scale(1.05); }
            60% { transform: rotate(-3deg) scale(1.05); }
            80% { transform: rotate(3deg) scale(1.05); }
            100% { transform: rotate(0); }
        }
        .wobble-btn > button {
            animation: superWobble 0.8s infinite ease-in-out !important;
            background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%) !important;
            color: #1A0A2E !important;
            box-shadow: 0px 0px 25px rgba(255, 215, 0, 0.6) !important;
        }
        
        /* Hiệu ứng Shake thông báo lỗi */
        @keyframes shakeAction {
            0%, 100% { transform: translateX(0); }
            20%, 60% { transform: translateX(-8px); }
            40%, 80% { transform: translateX(8px); }
        }
        .shake-container {
            background-color: rgba(255, 75, 75, 0.2);
            color: #FF7575;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #FF4B4B;
            margin: 10px 0;
            animation: shakeAction 0.5s ease-in-out;
            width: 100%;
            font-weight: bold;
            text-align: center;
        }

        iframe { background-color: transparent !important; }
        
        </style>
    """, unsafe_allow_html=True)
