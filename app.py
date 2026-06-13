import streamlit as st

# 사이드바 메뉴 설정
menu = st.sidebar.radio("계산기 선택", ["대출", "마통", "공모주"])

# 각 계산기별 기능 함수화
def loan_calculator():
    # 여기에 [기존 대출 계산기 코드] 복사 붙여넣기
    st.write("대출 계산 로직...")

def minus_account_calculator():
    # 여기에 [기존 마통 계산기 코드] 복사 붙여넣기
    st.write("마통 계산 로직...")

def ipo_calculator():
    # 여기에 [기존 공모주 계산기 코드] 복사 붙여넣기
    st.write("공모주 계산 로직...")

# 메뉴 선택에 따른 화면 출력
if menu == "대출":
    loan_calculator()
elif menu == "마통":
    minus_account_calculator()
elif menu == "공모주":
    ipo_calculator()
