import streamlit as st

st.set_page_config(page_title="홈", layout="wide")
st.title("초보 자폐인 보호자를 위한 지원 AI 시스템에 대한 설문조사에 오신 것을 환영합니다.")

# --- 설문 목적 및 개요 ---
st.markdown("## 설문조사의 목적")
st.write("""
- 초보 자폐인 보호자를 보조할 수 있는 AI 시스템의 실효성을 측정하기 위한 설문조사입니다.
- 해당 지원 AI 시스템은 초보 자폐인 보호자를 위한 시스템으로 자폐인이 공격적인 성향 및 자해를 하는 경우 그 원인을 파악하고 중재 방안을 제시해주는 시스템입니다.
- 각 페이지 별로 제시 된 자폐인의 Meltdown 원인과 중재 방안은 GPT-o3로 생성된 모든 답변입니다. GPT-o3의 환각 문제로 엉뚱한 중재방안이 있을 수 있는데 그럴 경우 0점을 주시면 됩니다.
- 각 페이지 별로 제시된 유튜브 영상은 AI로 자폐인의 Meltdown 순간과 그 이전에 발생한 자폐인의 Meltdown의 원인이 될 만한 순간을 디텍션해서 생성된 클립입니다. (ex. 자폐인이 자해를 하는 행위가 2:34초에 있었고 낯선 사람이 자폐인의 방으로 들어온 것이 1:20초에 있었다면 해당 클립은 원본 유튜브의 1:20~2:34초 구간입니다)
- 해당 클립의 원본 링크는 각 페이지 상단에 따로 제공해드릴 것입니다.
- 설문은 총 8 페이지로 이루어져있습니다.
- 1-5 페이지의 설문은 제시된 중재방안에 대해서 얼마나 적절한지에 따라 0~5점을 주시면 됩니다.
- 6-7 페이지는 GPT-o3에게 중재 방안에 대한 피드백을 주고 해당 피드백을 반영한 답변을 얻으실 수 있습니다. 원하시는 만큼 피드백을 주시면 되며 그에 따른 설문을 해주시면 됩니다.
- 마지막 페이지에는 자폐인의 관찰 일지를 GPT-o3가 참고하여 답변을 생성할 것입니다. 역시 원하시는 만큼 피드백을 주시면 되며 그에 따른 설문을 해주시면 됩니다.
- 6-8 페이지는 GPT-o3 모델의 특성상 답변이 조금 느립니다. 3-4초 정도 생각하시면 될 것 같습니다.
""")

# expert_id 초기화
if "expert_id" not in st.session_state:
    st.session_state.expert_id = ""

# ID 입력
expert_id = st.text_input("응답자 ID를 입력해주세요:", st.session_state.expert_id)
if expert_id:
    st.session_state.expert_id = expert_id
    st.success(f"{expert_id} 님, 좌측에서 설문을 선택해 주세요.")

col_next, = st.columns([1])

# 3) 다음 페이지 버튼 (언제나 보입니다)
with col_next:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/1_survey_1.py")
