import streamlit as st
import datetime
from my_switch import switch_page
import os

st.title("설문 2: 마트에서의 자폐인 Meltdown")

st.markdown("""
해당 영상은 자폐인이 가족과 함께 마트에 간 유튜브입니다. 
낯선 사람들이 많이 지나다니는 마트에서 자폐인이 소리를 지르고 있으며 아버지로 보이는 사람이 자폐인을 달래는 모습을 보이고 있는 유튜브입니다.
중재 방안 후보들은 각각 strategy, purpose, immediate, standard라는 요소를 가지고 있습니다.
여기서 strategy는 중재 전략의 이름이며 purpose는 해당 중재 전략의 목적입니다.
immediate는 그 순간에 당장 조치 할 수 있는 중재 전략이며 standard는 일반적인 수행 할 수 있는 중재 전략을 의미합니다.

Survey_2의 목적은 중재 전략이 얼마나 적절하게 제시 되었는지를 측정하는 것에 목적이 있습니다.

전체 내용을 보시고자 한다면 아래 링크를 확인해주시면 감사드리겠습니다..
해당 클립의 원본 링크 : https://www.youtube.com/watch?v=hQ3F49XHHTE
""")

# ID가 없으면 작성하라고 유도
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("먼저 홈에서 응답자 ID를 입력해 주세요.")
    st.stop()

# 비디오
st.video("https://youtu.be/ABGADcUeI8c")

# 해결 방안 후보들
interventions = [
    """1. **strategy**: 감각 조절을 통한 안정화  \n**purpose**: 자폐인이 주변 자극을 완화시켜 심리적 안정을 찾도록 지원하기 위함  \n**immediate**: 분노 발작이 시작되면 즉시 조용한 목소리로 진정 명령을 하며, 아이를 시끄러운 소리나 밝은 빛에서 멀리 떨어뜨림  \n**standard**: 쇼핑 센터 내에서 미리 정해진 조용한 공간이나 대기실로 이동하여 소음 차단 헤드폰, 어둡거나 차분한 조명 등을 활용해 감각 자극을 줄이는 방안을 실행""",
    """2. **strategy**: 일관된 시간 관리 및 신체 접촉 최소화  \n**purpose**: 보호자와의 과도한 신체 접촉을 줄이고 명확한 예측 가능성을 제공하여 아이의 안정감을 높이기 위함  \n**immediate**: 아이의 감정이 격해질 때 신체적 제지 대신 부드럽고 일관된 음성으로 간단하고 명료한 지시를 제공  \n**standard**: 일관된 일과표와 행동 규칙을 사전에 설명하고, 불안 요소를 줄이기 위해 구체적인 예시와 시각 자료를 활용하여 상황 대처 방법을 지도""",
    """3. **strategy**: 경계 설정 및 사회적 규칙 안내  \n**purpose**: 타인과의 안전한 상호작용을 위해 개인의 신체적 경계를 명확히 하고, 사회적 규칙을 이해시키기 위함  \n**immediate**: 즉각적으로 부드러운 어조로 아이에게 타인의 개인 공간을 존중하도록 간단한 언어로 설명  \n**standard**: 사진이나 그림 카드 등 시각 자료를 활용해 사회적 규칙과 개인 경계에 대해 정기적으로 교육하며, 반복 학습을 통해 이해도를 높임""",
    """4. **strategy**: 비언어적 신호 활용  \n**purpose**: 아이에게 부적절한 신체 접촉 행동을 인식시키고, 대안을 제시하기 위해 비언어적 소통 기법을 활용  \n**immediate**: 아이의 행동이 시작되면 즉시 미소나 손짓과 같은 긍정적 제스처를 사용하여 올바른 신체 접촉 방식을 유도  \n**standard**: 정기적인 비언어적 커뮤니케이션 교육을 실시하여, 구체적인 제스처와 상황별 피드백을 통해 아이가 자신의 행동을 조절할 수 있도록 지도"""
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

    filepath = os.path.join(user_dir, "survey2.csv")

    # 응답 저장
    with open(filepath, "a", encoding="utf-8") as f:
        for intervention, rating in ratings.items():
            f.write(f"{now},{expert_id},\"{intervention}\",{rating},\"{comments}\",\"\",{overall_helpfulness}\n")

    st.success("응답이 저장되었습니다. 감사합니다!")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/1_survey_1.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/3_survey_3.py")    # pages/survey2.py (확장자 제외)
        
