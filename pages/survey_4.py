import streamlit as st
import datetime
from my_switch import switch_page
import os

st.title("설문 4: 자해 행동을 하고 있는 자폐인")

st.markdown("""
해당 영상은 자폐인이 의자에 가만히 있는 모습을 담은 유튜브입니다. 
자폐인이 의자 위에 가만히 앉아 있지만 주먹으로 자신의 머리를 계속해서 가격하고 있습니다.
중재 방안 후보들은 각각 strategy, purpose, immediate, standard라는 요소를 가지고 있습니다.
여기서 strategy는 중재 전략의 이름이며 purpose는 해당 중재 전략의 목적입니다.
immediate는 그 순간에 당장 조치 할 수 있는 중재 전략이며 standard는 일반적인 수행 할 수 있는 중재 전략을 의미합니다.

Survey_4의 목적은 중재 전략이 얼마나 적절하게 제시 되었는지를 측정하는 것에 목적이 있습니다.

전체 내용을 보시고자 한다면 아래 링크를 확인해주시면 감사드리겠습니다..
해당 클립의 원본 링크 : https://www.youtube.com/watch?v=3D8Y0wM-fkU
""")

# ID가 없으면 작성하라고 유도
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("먼저 홈에서 응답자 ID를 입력해 주세요.")
    st.stop()

# 비디오
st.video("https://youtu.be/i9zi6Sqc_FY")

# 해결 방안 후보들
interventions = [
    """1. **strategy**: 즉각적인 감각 조절 제공  \n**purpose**: 자해 행동 발생 시 부정적인 감각 과부하를 줄이고 안정감을 제공하기 위해 즉각적인 센서리 조절을 돕는 것이 목적입니다  \n**immediate**: 자해 행동이 시작되면 조용히 아이에게 접근하여 부드러운 촉감의 센서리 토이나 촉각 도구(예: 촉감 볼)를 제공하여 감각 입력을 조절하도록 유도합니다  \n**standard**: 평상시 수업 전 센서리 도구 상자를 준비하고, 아이와 함께 도구 사용법을 연습하여 필요할 때 즉각적으로 사용할 수 있도록 교육합니다. """,
    """2. **strategy**: 환경 변경 및 관심 분산  \n**purpose**: 자해 행동에 몰입하지 않도록 환경이나 활동을 조정하여 아이의 주의를 안전한 방향으로 전환시키는 것이 목적입니다  \n**immediate**: 문제가 발생하면 조용히 아이의 주변을 정리하고, 시각적으로 흥미로운 안전한 물건(예: 그림, 퍼즐 등)을 제시하여 주의를 분산시킵니다  \n**standard**: 사전에 구성된 야외 활동 계획 내에서 규칙적이고 구조화된 일정과 활동(예: 짧은 산책, 조용한 놀이 시간)을 마련하여 아이가 안정감을 느끼며 주의를 다른 곳으로 돌릴 수 있도록 합니다.
"""
]

st.subheader("💡 제안된 해결 방안들에 대해 각각 평가해 주세요.")

ratings = {}
for i, intervention in enumerate(interventions):
    st.markdown(intervention.strip())
    rating = st.slider(f"→ 이 방안의 적절성 (0~5)", 0, 5, key=f"rating_{i}")
    ratings[intervention] = rating
    st.markdown("---")

overall_helpfulness = st.slider("→ 전반적 도움 정도 (0~5)", 0, 5, key="overall_helpfulness")

# 추가 의견
comments = st.text_area("전체적인 의견 또는 설명 (선택사항)")

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
        st.switch_page("pages/survey_3.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/survey_5.py")    # pages/survey2.py (확장자 제외)
