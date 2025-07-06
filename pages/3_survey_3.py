import streamlit as st
import datetime
from my_switch import switch_page
import os

st.title("설문 3: 자폐인의 공격적인 모습")

st.markdown("""
해당 영상은 자폐인이 집에서 가족과 함께 있는 모습을 담은 유튜브입니다. 
자폐인이 어머니에게 안겨 있지만 자폐인은 자신의 뒷통수로 어머니를 연속해서 가격하는 모습을 보이고 있습니다.
중재 방안 후보들은 각각 strategy, purpose, immediate, standard라는 요소를 가지고 있습니다.
여기서 strategy는 중재 전략의 이름이며 purpose는 해당 중재 전략의 목적입니다.
immediate는 그 순간에 당장 조치 할 수 있는 중재 전략이며 standard는 일반적인 수행 할 수 있는 중재 전략을 의미합니다.

Survey_3의 목적은 LLM이 중재 전략을 얼마나 적절하게 제시 할 수 있는지 그 능력을 측정하는 것에 목적이 있습니다.

전체 내용을 보시고자 한다면 아래 링크를 확인해주시면 감사드리겠습니다..
해당 클립의 원본 링크 : https://www.youtube.com/watch?v=C-0dUcJE6hg
""")

# ID가 없으면 작성하라고 유도
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("먼저 홈에서 응답자 ID를 입력해 주세요.")
    st.stop()

# 비디오
st.video("https://youtu.be/5Cfc2oGZAbI")

# 해결 방안 후보들
interventions = [
    """1. **strategy**: 감각 자극 조절  \n**purpose**: 과도한 감각 자극을 완화하여 불안감을 줄이고 안정된 행동을 유도  \n**immediate**: 즉시 조용한 공간으로 이동하여 목소리 톤을 낮추고 부드럽게 대화하며 감각 자극을 줄인다.  \n**standard**: 교실 내 조용한 구역을 마련하고, 조명 및 소리 조절 도구(소음 차단 헤드폰, 간접 조명 등)를 활용하여 일상적인 감각 환경을 조절한다.""",
    """2. **strategy**: 비폭력적 의사소통 지원  \n**purpose**: 자폐 아동이 자신의 감정을 말이나 다른 수단으로 표현할 수 있도록 돕고, 물리적 행동 대신 적절한 의사소통 방법을 사용할 수 있도록 지도  \n**immediate**: 상황 발생 시, 부드럽고 침착한 어조로 아이에게 '말로 표현해봐'라며 유도한다.  \n**standard**: 시각 자료(예: 그림 카드, 사진 일람표)와 함께 정기적으로 의사소통 교육을 실시하여 감정 표현과 요구 전달 방법을 연습시킨다""",
    """3. **strategy**: 심리적 안정 제공  \n**purpose**: 아동이 심리적으로 안정감을 회복하고 감정을 조절할 수 있도록 지원  \n**immediate**: 아동이 울거나 소리칠 때 부드럽게 안아주거나, 차분한 목소리로 '괜찮아'라고 말하며 즉각적 안정을 도모한다  \n**standard**: 정기적인 휴식 시간과 안정 영역(안전 구역, 쿠션 코너 등)을 마련해 아동이 자율적으로 휴식을 취할 수 있도록 환경을 조성한다""",
    """4. **strategy**: 시각적 지원 활용  \n**purpose**: 어려운 감정 상황에서 아동에게 명확한 시각 자료를 통해 상황을 해석하고 예측할 수 있도록 도움  \n**immediate**: 문제가 발생할 때 즉시 시각 자료(예: 감정 카드, 행동 차트)를 보여주어 아동이 현재 상태를 인식하도록 유도한다.  \n**standard**: 일상 수업에 시각 지원 도구(타임 타이블, 일과표 등)를 포함시켜, 아동이 예측 가능한 일상 패턴을 인식하고 전반적인 불안을 감소시킨다""",
    """5. **strategy**: 사회적 상호작용 교육  \n**purpose**: 아동들이 서로의 신체적 경계를 이해하고 존중할 수 있도록 사회적 기술을 향상시키기 위함  \n**immediate**: 즉각 상황 발생 시, 부드럽게 아동들에게 서로의 거리를 유지하도록 안내하고 차분하게 설명한다  \n**standard**: 정기적으로 역할 놀이 및 모형 활동을 통해 ‘적절한 신체 접촉’에 대한 시각 자료와 함께 교육을 실시한다.""",
    """6. **strategy**: 구조화된 환경 설정  \n**purpose**: 신체 접촉으로 인한 오해를 방지하고, 아동들이 안전하게 상호작용할 수 있는 체계적인 환경을 조성하기 위함  \n**immediate**: 문제가 발생할 경우, 즉시 물리적 거리를 두도록 성인이 중재하며 안전한 공간으로 유도한다  \n**standard**: '교실 배치를 변경하여 아동들 간 거리를 자연스럽게 확보하고, 소그룹 활동을 통해 상대방과의 상호작용 규칙을 명확히 한다."""
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

    filepath = os.path.join(user_dir, "survey3.csv")

    # 응답 저장
    with open(filepath, "a", encoding="utf-8") as f:
        for intervention, rating in ratings.items():
            f.write(f"{now},{expert_id},\"{intervention}\",{rating},\"{comments}\",\"\",{overall_helpfulness}\n")

    st.success("응답이 저장되었습니다. 감사합니다!")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/2_survey_2.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/4_improve_survey.py")    # pages/survey2.py (확장자 제외)
    
