import streamlit as st
import datetime
from my_switch import switch_page
import os

st.title("설문 1: 그랜드 케니언에서의 자폐인 Meltdown")
st.markdown(""" 해당 영상은 자폐인이 가족과 함께 그랜드 케니언으로 여행을 간 유튜브입니다. 
영상 속에서 자폐인의 Meltdown이 나타나는 부분은 처음 주차장에서입니다.
주차장에서 자폐인은 빨간 자동차에서 떨어지지 않으려는 모습을 보이며 그의 형으로 보이는 사람이 자폐인을 달래는 모습을 보이고 있습니다.
중재 방안 후보들은 각각 strategy, purpose, immediate, standard라는 요소를 가지고 있습니다.
여기서 strategy는 중재 전략의 이름이며 purpose는 해당 중재 전략의 목적입니다.
immediate는 그 순간에 당장 조치 할 수 있는 중재 전략이며 standard는 일반적인 수행 할 수 있는 중재 전략을 의미합니다.

Survey_1의 목적은 중재 전략이 얼마나 적절하게 제시 되었는지를 측정하는 것에 목적이 있습니다.

전체 내용을 보시고자 한다면 아래 링크를 확인해주시면 감사드리겠습니다.
해당 클립의 원본 링크 : https://www.youtube.com/watch?v=3B42Sev56xo
""")


# ID가 없으면 작성하라고 유도
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("먼저 홈에서 응답자 ID를 입력해 주세요.")
    st.stop()

# 비디오
st.video("https://youtu.be/kBL3zx4MTHA")

# 해결 방안 후보들
interventions = [
    """1. strategy: 환경적 자극 조절
          purpose: 감각 과부하를 예방하고 자폐인이 보다 안정된 환경에서 상황을 받아들일 수 있도록 돕기 위함
          immediate: 문제가 발생하면 빨간 밴이나 기타 시각적 자극 요소로부터 거리를 두도록 유도하며, 조용한 구역으로 천천히 이동시킴
          standard: 야외 활동 전 또는 활동 중에 불필요한 자극(강한 빛, 소음 등)을 줄일 수 있는 도구(예: 선글라스, 귀마개)와 함께, 미리 정해진 조용한 휴식 구역을 안내""",
    """2. strategy: 시각적 지원 제공,
          purpose: 자폐인의 시각 의사소통 선호를 활용하여 상황 예측 가능성을 높이고, 안정감을 제공하기 위함
          immediate: 불안 징후가 보이면 간단한 그림 카드나 사진을 보여주며 현재 상황과 앞으로의 행동을 간략히 설명
          standard: 사전에 야외 활동 스케줄이나 사회 이야기를 준비해 상황 전개를 시각적으로 안내하고, 자폐인이 이해할 수 있도록 반복적으로 활용"""
]

st.subheader("💡 제안된 해결 방안들에 대해 각각 평가해 주세요.")

ratings = {}
for i, intervention in enumerate(interventions):
    st.markdown(f"**{intervention}**")
    rating = st.slider(f"→ 이 방안의 적절성 (0~5)", 0, 5, key=f"rating_{i}")
    ratings[intervention] = rating
    st.markdown("---")

overall_helpfulness = st.slider("→ 전반적 도움 정도 (0~5)", 0, 5, key="overall_helpfulness")

# 제출
if st.button("제출"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expert_id = st.session_state.expert_id
    user_dir = f"responses/{expert_id}"

    # 디렉터리 없으면 생성
    os.makedirs(user_dir, exist_ok=True)

    filepath = os.path.join(user_dir, "survey1.csv")

    # 응답 저장
    with open(filepath, "a", encoding="utf-8") as f:
        for intervention, rating in ratings.items():
            f.write(f"{now},{expert_id},\"{intervention}\",{rating},\"{comments}\",\"\",{overall_helpfulness}\n")

    st.success("응답이 저장되었습니다. 감사합니다!")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        switch_page("home")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        switch_page("survey2")    # pages/survey2.py (확장자 제외)
        
