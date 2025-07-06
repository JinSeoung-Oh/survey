import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import datetime
import os

# 설문 대상자의 경력 입력 페이지
st.title("설문 대상자의 경력 입력")

# Home에서 입력된 응답자 ID 표시
expert_id = st.session_state.get("expert_id", "")
st.write(f"응답자 ID: **{expert_id}** 님")

# 1) 기본 정보 입력
name = st.text_input("이름", key="expert_name")
education = st.selectbox(
    "최종 학력",
    ["중졸 이하", "고졸", "전문대졸", "학사(대학 졸업)", "석사", "박사"],
    key="expert_education"
)
major = st.text_input("전공", key="expert_major")

# 2) 경력 및 경험 입력
years_experience = st.number_input(
    "관련 분야 경력 (년)", min_value=0, max_value=50, step=1, key="expert_years"
)
description = st.text_area(
    "경력 및 전문 분야 설명",
    placeholder="예) 자폐 돌봄 3년, ABA 훈련 2년 등",
    key="expert_desc",
    height=120
)

# 3) 제출 버튼 및 저장 로직
if st.button("제출"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_dir = f"responses/{expert_id}"
    os.makedirs(user_dir, exist_ok=True)
    filepath = os.path.join(user_dir, "career_info.csv")
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"{now},{expert_id},{name},{education},{major},{years_experience},\"{description}\"\n")
    st.success("경력 정보가 저장되었습니다.")

# 4) 이전/다음 페이지 이동
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("Home.py")
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/1_survey_1.py")
