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
```eof
```html:widget.html
<table width="170" bgcolor="#1e2229" cellpadding="15" cellspacing="0" style="border-collapse:collapse; border-radius:8px; text-align:center; font-family:'나눔고딕',sans-serif;">
  <tr>
    <td align="center" style="padding-top:20px; padding-bottom:5px;">
      <span style="color:#00e65a; font-weight:bold; font-size:16px; letter-spacing:-0.5px;">대출 이자 계산기</span>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding-top:0px; padding-bottom:15px;">
      <span style="color:#ffffff; font-size:12px; line-height:1.4; opacity:0.8;">Karis가 직접 개발한<br>원리금 / 원금 균등계산기</span>
    </td>
  </tr>
  <tr>
    <td align="center" style="padding-top:0px; padding-bottom:20px;">
      <a href="https://본인의_스트림릿_배포_주소/" target="_blank" style="text-decoration:none;">
        <div style="background-color:#00e65a; color:#ffffff; font-weight:bold; font-size:13px; padding:10px 0px; width:140px; border-radius:6px;">
          실시간 계산기 켜기
        </div>
      </a>
    </td>
  </tr>
</table>
```eof

---

### 🚀 대출이자 계산기 최종 빌드 및 연동 순서

1. **GitHub 새 저장소 생성**:
   * GitHub에 접속하여 새 저장소(Repository)를 만듭니다. 이름은 대출이자 계산기 직관성을 주기 위해 `general-loan-calculator` 정도로 지어주시면 좋습니다.
   * 저장소 안에 위 생성된 `app.py`를 그대로 올립니다.
   * `requirements.txt` 파일을 새로 만들어 내부에 `streamlit`만 입력하여 저장해 둡니다.

2. **Streamlit Cloud에 배포**:
   * Streamlit Cloud 대시보드에서 **[Create app]**을 클릭해 방금 만든 `general-loan-calculator` 저장소와 연결한 뒤 배포합니다.
   * 배포가 성공하면 나오는 **최종 URL 주소**를 복사해 둡니다.

3. **블로그 위젯 연동**:
   * 생성된 `widget.html` 파일 본문을 복사합니다.
   st.markdown("---")
   st.caption("본 계산기는 수수료 및 기타 세부 우대 금리 조항이 제외된 표준 상환 방식을 적용한 모의 계산 결과입니다.")
