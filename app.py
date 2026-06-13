import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="Karis 금융 계산기 포털", layout="centered")

# 2. 각 계산기별 실제 배포 URL (배포 후 주소를 여기에 입력하세요)
URL_LOAN = "https://your-loan-calculator-app-url.streamlit.app"
URL_MINUS = "https://your-minus-calculator-app-url.streamlit.app"
URL_IPO = "https://your-ipo-calculator-app-url.streamlit.app"

# 3. 메인 화면 구성 (대시보드 방식)
st.title("💰 Karis 금융 계산기 포털")
st.markdown("---")

st.subheader("원하시는 계산기를 선택하세요")

# 카드형 UI 구현 및 각 URL로 연결
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="background-color:#1e2229; padding:20px; border-radius:10px; text-align:center;">
        <h4 style="color:#00e65a;">대출 이자 계산기</h4>
        <p style="color:#ffffff; font-size:12px;">원리금 / 원금 균등계산기</p>
        <a href="{URL_LOAN}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#00e65a; color:#000000; font-weight:bold; padding:10px; border-radius:5px;">실시간 계산기 켜기</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color:#1e2229; padding:20px; border-radius:10px; text-align:center;">
        <h4 style="color:#00e65a;">마통 이자 계산기</h4>
        <p style="color:#ffffff; font-size:12px;">사용금액 일할 계산기</p>
        <a href="{URL_MINUS}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#00e65a; color:#000000; font-weight:bold; padding:10px; border-radius:5px;">실시간 계산기 켜기</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color:#1e2229; padding:20px; border-radius:10px; text-align:center;">
        <h4 style="color:#00e65a;">공모주 청약</h4>
        <p style="color:#ffffff; font-size:12px;">증거금 및 배정 수량</p>
        <a href="{URL_IPO}" target="_blank" style="text-decoration:none;">
            <div style="background-color:#00e65a; color:#000000; font-weight:bold; padding:10px; border-radius:5px;">실시간 계산기 켜기</div>
        </a>
    </div>
    """, unsafe_allow_html=True)
