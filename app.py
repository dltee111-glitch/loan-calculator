import streamlit as st
import pandas as pd

st.set_page_config(page_title="통합 대출이자 계산기", layout="centered")

st.title("💳 통합 대출이자 계산기")
st.markdown("대출 원금, 금리, 기간을 입력하여 상환액을 체계적으로 계산합니다.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    principal = st.number_input("대출 원금 (원)", min_value=100000, value=10000000, step=100000)
    rate = st.number_input("연 금리 (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
with col2:
    period = st.number_input("대출 기간 (개월)", min_value=1, max_value=360, value=12)
    method = st.selectbox("상환 방식", ["원리금 균등 상환", "원금 균등 상환"])

def get_schedule_df(p, r, m, method):
    monthly_rate = (r / 100) / 12
    schedule = []
    balance = p
    
    if method == "원리금 균등 상환":
        monthly_payment = p * (monthly_rate * (1 + monthly_rate) ** m) / ((1 + monthly_rate) ** m - 1)
        for i in range(1, m + 1):
            interest = balance * monthly_rate
            principal_pay = monthly_payment - interest
            balance -= principal_pay
            schedule.append([i, int(principal_pay), int(interest), int(max(0, balance))])
    else: # 원금 균등
        principal_pay = p / m
        for i in range(1, m + 1):
            interest = balance * monthly_rate
            balance -= principal_pay
            schedule.append([i, int(principal_pay), int(interest), int(max(0, balance))])
    
    return pd.DataFrame(schedule, columns=["회차", "상환 원금", "이자", "잔금"])

tab1, tab2, tab3 = st.tabs(["📊 기본 계산기", "📅 월별 상환 스케줄", "💡 이자 비교 분석"])

with tab1:
    st.subheader("계산 결과 요약")
    df_calc = get_schedule_df(principal, rate, period, method)
    monthly_avg = df_calc['상환 원금'].sum() / period + df_calc['이자'].sum() / period # 근사치
    if method == "원리금 균등 상환":
        monthly_payment = (principal * ( (rate/100/12) * (1+(rate/100/12))**period ) / ( (1+(rate/100/12))**period - 1 ))
        st.metric("월 예상 상환액", f"{int(monthly_payment):,} 원")
    else:
        st.info("원금 균등 상환은 매월 상환액이 달라집니다. (상세 탭 확인)")
    
    st.metric("총 이자 비용", f"{int(df_calc['이자'].sum()):,} 원")

with tab2:
    st.subheader("상세 상환 스케줄")
    st.dataframe(df_calc, use_container_width=True)

with tab3:
    st.subheader("금리별 이자 비교")
    col_a, col_b = st.columns(2)
    with col_a:
        rate1 = st.number_input("현재 금리 (%)", value=5.0, step=0.1)
    with col_b:
        rate2 = st.number_input("비교 금리 (%)", value=4.0, step=0.1)
    
    if st.button("비교 분석 시작"):
        total_int1 = get_schedule_df(principal, rate1, period, method)['이자'].sum()
        total_int2 = get_schedule_df(principal, rate2, period, method)['이자'].sum()
        diff = total_int1 - total_int2
        st.metric("총 이자 절감액", f"{int(diff):,} 원")
        st.success(f"금리를 {abs(rate1-rate2):.1f}% 낮추면 총 {int(diff):,}원을 절약할 수 있습니다.")

st.markdown("---")
st.caption("※ 본 계산 결과는 단순 참고용이며, 실제 금융기관의 대출 조건에 따라 달라질 수 있습니다.")

st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h4 style="color: #333; margin-bottom: 10px;">✍️ Karis의 테크 & 재테크 블로그</h4>
        <p style="color: #555; margin-bottom: 15px;">최신 공모주 상세 분석, IPO 청약 일정 및 재테크 꿀팁을 놓치지 마세요!</p>
        <a href="https://blog.naver.com/karis_official" target="_blank" style="text-decoration: none; color: #ffffff; background-color: #00c73c; padding: 10px 20px; border-radius: 5px; font-weight: bold;">블로그 바로가기</a>
    </div>
""", unsafe_allow_html=True)
