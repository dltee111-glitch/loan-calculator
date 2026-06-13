import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="Karis의 스마트 대출이자 계산기",
    page_icon="💰",
    layout="centered"
)

# 커스텀 스타일링 (고급스러운 다크 테마 느낌 반영)
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stNumberInput div div input {
        color: #ffffff !important;
    }
    .stSelectbox div div div {
        color: #ffffff !important;
    }
    div[data-testid="metric-container"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏦 Karis의 스마트 대출이자 계산기")
st.write("상환 방식별 매달 내는 원금과 이자를 정밀하게 계산하고 비교해 드립니다.")
st.markdown("---")

# 입력 영역
st.header("💵 대출 조건 입력")
col1, col2 = st.columns(2)

with col1:
    loan_amount = st.number_input("대출 금액 (원)", min_value=0, value=50000000, step=1000000, format="%d")
    loan_rate = st.number_input("연 이자율 (%)", min_value=0.0, max_value=100.0, value=5.5, step=0.1, format="%.2f")

with col2:
    loan_term_years = st.number_input("대출 기간 (년)", min_value=1, max_value=50, value=3, step=1)
    repayment_method = st.selectbox(
        "상환 방식 선택",
        ["원리금균등상환", "원금균등상환", "만기일시상환"]
    )

# 계산 기본 변수 설정
principal = loan_amount
annual_rate = loan_rate / 100
monthly_rate = annual_rate / 12
total_months = int(loan_term_years * 12)

# 상환 방식별 연산 로직
schedule = []

if repayment_method == "원리금균등상환":
    # 월 상환액 (원금 + 이자) 공식
    if monthly_rate > 0:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_months) / (((1 + monthly_rate) ** total_months) - 1)
    else:
        monthly_payment = principal / total_months
        
    balance = principal
    for month in range(1, total_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        if balance < 0: balance = 0
        schedule.append({
            "회차": f"{month}회차",
            "납부원금": round(principal_payment),
            "대출이자": round(interest_payment),
            "월상환액": round(monthly_payment),
            "대출잔액": round(balance)
        })

elif repayment_method == "원금균등상환":
    # 매달 동일하게 상환할 원금
    monthly_principal_payment = principal / total_months
    balance = principal
    for month in range(1, total_months + 1):
        interest_payment = balance * monthly_rate
        monthly_payment = monthly_principal_payment + interest_payment
        balance -= monthly_principal_payment
        if balance < 0: balance = 0
        schedule.append({
            "회차": f"{month}회차",
            "납부원금": round(monthly_principal_payment),
            "대출이자": round(interest_payment),
            "월상환액": round(monthly_payment),
            "대출잔액": round(balance)
        })

elif repayment_method == "만기일시상환":
    # 매달 이자만 내다가 마지막 달에 원금 전액 상환
    balance = principal
    for month in range(1, total_months + 1):
        interest_payment = balance * monthly_rate
        if month == total_months:
            principal_payment = principal
            monthly_payment = principal + interest_payment
            balance = 0
        else:
            principal_payment = 0
            monthly_payment = interest_payment
            balance = principal
            
        schedule.append({
            "회차": f"{month}회차",
            "납부원금": principal_payment,
            "대출이자": round(interest_payment),
            "월상환액": round(monthly_payment),
            "대출잔액": round(balance)
        })

# 데이터프레임 변환
df_schedule = pd.DataFrame(schedule)

# 결과 요약 지표 연산
total_interest = df_schedule["대출이자"].sum()
total_repayment = principal + total_interest
avg_monthly_payment = df_schedule["월상환액"].mean()

# 결과 대시보드 출력
st.markdown("---")
st.header("📊 대출이자 분석 결과")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="총 대출 이자", value=f"{total_interest:,.0f} 원")
with m2:
    st.metric(label="총 상환 금액 (원금+이자)", value=f"{total_repayment:,.0f} 원")
with m3:
    st.metric(label="평균 월 상환액", value=f"{avg_monthly_payment:,.0f} 원")

# 시각화 (상환 회차별 원금 및 이자 변화 추이)
st.markdown("### 📈 회차별 상환 구성 추이")
chart_data = df_schedule.set_index("회차")[["납부원금", "대출이자"]]
st.area_chart(chart_data)

# 상세 납부 일정 표 출력
st.markdown("### 📋 상세 납부 일정표")
st.dataframe(
    df_schedule.style.format({
        "납부원금": "{:,.0f}원",
        "대출이자": "{:,.0f}원",
        "월상환액": "{:,.0f}원",
        "대출잔액": "{:,.0f}원"
    }),
    use_container_width=True
)

st.markdown("---")
st.caption("본 계산기는 수수료 및 기타 세부 우대 금리 조항이 제외된 표준 상환 방식을 적용한 모의 계산 결과입니다.")
