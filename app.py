import streamlit as st
import pandas as pd

st.set_page_config(page_title="신용대출 이자 계산기", layout="centered")

st.title("💳 신용대출 이자 계산기")
st.markdown("대출 원금과 금리, 기간을 입력하여 상환액을 계산합니다.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    principal = st.number_input("대출 원금 (원)", min_value=100000, value=10000000, step=100000)
    rate = st.number_input("연 금리 (%)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
with col2:
    period = st.number_input("대출 기간 (개월)", min_value=1, max_value=360, value=12)
    method = st.selectbox("상환 방식", ["원리금 균등 상환", "원금 균등 상환"])

def calculate_loan(p, r, m, method):
    monthly_rate = (r / 100) / 12
    months = m
    
    if method == "원리금 균등 상환":
        # 월 상환액 = 대출금 * [이자율*(1+이자율)^기간] / [(1+이자율)^기간 - 1]
        monthly_payment = p * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
        total_payment = monthly_payment * months
        return monthly_payment, total_payment - p
    else:
        # 원금 균등은 매달 원금이 동일하게 상환됨
        principal_payment = p / months
        # 첫 달 이자가 가장 높음
        interest = p * monthly_rate
        return principal_payment + interest, (p * monthly_rate * (months + 1)) / 2

if st.button("계산하기"):
    monthly_pay, total_interest = calculate_loan(principal, rate, period, method)
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric("월 예상 상환액", f"{int(monthly_pay):,} 원")
    col_r2.metric("총 이자 비용", f"{int(total_interest):,} 원")
    
    st.info(f"선택하신 '{method}' 방식으로 {period}개월 동안 상환 시 결과입니다.")

st.markdown("---")
st.caption("※ 본 계산 결과는 단순 참고용이며, 실제 금융기관의 대출 조건에 따라 달라질 수 있습니다.")

# 블로그 링크 배너 추가
st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h4 style="color: #333; margin-bottom: 10px;">✍️ Karis의 테크 & 재테크 블로그</h4>
        <p style="color: #555; margin-bottom: 15px;">최신 공모주 상세 분석, IPO 청약 일정 및 재테크 꿀팁을 놓치지 마세요!</p>
        <a href="https://blog.naver.com/karis_official" target="_blank" style="text-decoration: none; color: #ffffff; background-color: #00c73c; padding: 10px 20px; border-radius: 5px; font-weight: bold;">블로그 바로가기</a>
    </div>
""", unsafe_allow_html=True)
