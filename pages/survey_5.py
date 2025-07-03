import streamlit as st
import datetime
from my_switch import switch_page
import os

st.title("설문 5: 병원에서의 자폐인 Meltdown")

st.markdown("""
해당 영상은 자폐인이 병원 침대 위에서 Meltdown을 경험하고 있는 모습을 담은 유튜브입니다. 
자폐인이 병원 의자에 누워 있는 상태에서 격렬하게 몸부림을 치고 있고 주변에서는 이러한 자폐인을 물리적으로 제제하고 있습니다.
중재 방안 후보들은 각각 strategy, purpose, immediate, standard라는 요소를 가지고 있습니다.
여기서 strategy는 중재 전략의 이름이며 purpose는 해당 중재 전략의 목적입니다.
immediate는 그 순간에 당장 조치 할 수 있는 중재 전략이며 standard는 일반적인 수행 할 수 있는 중재 전략을 의미합니다.

Survey_5의 목적은 중재 전략이 얼마나 적절하게 제시 되었는지를 측정하는 것에 목적이 있습니다.

전체 내용을 보시고자 한다면 아래 링크를 확인해주시면 감사드리겠습니다..
해당 클립의 원본 링크 : https://www.youtube.com/watch?v=EAGe9cgI5e0
""")

# ID가 없으면 작성하라고 유도
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("먼저 홈에서 응답자 ID를 입력해 주세요.")
    st.stop()

# 비디오
st.video("https://youtu.be/QcGVHFlke9o")

# 해결 방안 후보들
interventions = [
    """1. **strategy**: 감각 안정 지원  \n**purpose**: 환경의 감각 자극을 줄여 자폐인의 불안을 완화하고 안정된 상태를 유도하기 위함  \n**immediate**: 문제가 발생했을 때 즉시 조용하고 부드러운 목소리로 '안전해'라고 말하며 과도한 신체 접촉을 피하고 거리를 두기  \n**standard**: 정기적으로 시각 자료(예: 일정표, 감각 도구 사진)를 활용하여 예측 가능한 환경을 제공하고, 귀마개나 조절 가능한 빛 등 감각 도구를 이용하여 감각 과부하를 줄이는 방법 적용""", 
    """2. **strategy**: 안전한 신체적 경계 설정  \n**purpose**: 불필요한 신체적 접촉을 최소화하며, 자폐인이 안전하다고 느낄 수 있는 물리적 공간을 마련하기 위함  \n**immediate**: 즉시 부드러운 몸짓으로 물리적 거리를 확보하며, 주변 성인을 차분하게 재배치하여 자폐인 주위의 지나친 접촉을 제한  \n**standard**: 예측 가능한 신체적 경계를 위해 바닥에 표시된 테이프, 의자 배치 등을 활용하고 사전에 행동 지침을 설명하여 안정된 환경을 조성""",
    """3. **strategy**: 비폭력적 언어 사용  \n**purpose**: 자폐인이 안전하다고 느끼도록 차분한 의사소통을 통해 불안을 완화하고 신뢰를 구축하기 위함  \n**immediate**: 즉각적으로 부드러운 어조로 '괜찮아, 내가 도와줄게'라고 말하며, 자폐인의 감정을 인정하는 반응 보이기  \n**standard**: 정기적인 의사소통 훈련 세션에서 시각 보조 자료와 함께 감정을 조절하는 방법, 대체 의사소통 도구(예: 카드 또는 그림)를 활용하여 일정한 패턴의 의사소통 기법을 교육""",
    """4. **strategy**: 감각 자극 최소화  \n**purpose**: 과도한 감각 자극으로 인한 불안과 스트레스를 줄여 자폐인이 더 차분하게 환경을 받아들일 수 있도록 하기 위함  \n**immediate**: 즉각적으로 조명과 소음을 최소화하여 자폐인이 느끼는 감각적 부담을 경감시킴  \n**standard**: 클래스룸 내 별도의 휴식 공간을 마련하고, 정해진 시간에 감각 완화 활동(예: 심호흡, 부드러운 음악 듣기) 프로그램을 운영""",
    """5. **strategy**: 예측 가능한 환경 제공  \n**purpose**: 일관된 시간표와 시각 자료를 통해 자폐인에게 환경의 예측 가능성을 부여하여 불안을 감소시키기 위함  \n**immediate**: 즉시 현재 상황을 간단한 그림이나 짧은 설명으로 전달하여 자폐인이 상황을 이해하도록 도움  \n**standard**: 정규 수업 또는 치료 시간에 시각적 일정표와 구체적 설명을 제공하고, 환경 변화 시 사전 공지를 통해 예측 가능하도록 체계화""",
    """6. **strategy**: 사회적 상호작용 기술 지도  \n**purpose**: 자폐인이 사회적 상황에서 적절한 신체 접촉과 대처 방법을 학습, 내면의 불안을 완화하면서 올바른 상호작용을 유도하기 위함  \n**immediate**: 즉각적으로 긍정적인 사회적 접촉의 예시(예: 가볍게 손을 잡는 등)를 보여주며 올바른 행동 유도  \n**standard**: 정기적으로 역할극 및 사회적 기술 훈련을 진행하며, 시각 자료와 함께 사회적 신호와 적절한 반응을 교육하는 시간을 마련"""
]

st.subheader("💡 제안된 해결 방안들에 대해 각각 평가해 주세요.")

ratings = {}
for i, intervention in enumerate(interventions):
    st.markdown(intervention.strip())
    rating = st.slider(f"→ 이 방안의 적절성 (0~5)", 0, 5, key=f"rating_{i}")
    ratings[intervention] = rating
    st.markdown("---")

# 추가 의견
comments = st.text_area("전체적인 의견 또는 설명 (선택사항)")

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
        st.switch_page("pages/survey_4.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/improve_survey.py")    # pages/survey2.py (확장자 제외)
