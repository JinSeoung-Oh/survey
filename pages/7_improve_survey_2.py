import streamlit as st
import datetime
from my_switch import switch_page
from pages.tool import O3MiniClient
import os

agent = O3MiniClient()

# ─── 초기 세션 상태 설정 ─────────────────────────────
if "state1" not in st.session_state:
    st.session_state.state1 = "feedback_loop"
    st.session_state.problem1 = "외출을 위해 자폐인에게 옷을 입히려고 하는데 자폐인이 그 옷을 입지 않으려고 저항하는 상황"
    st.session_state.strategy1 = """{
  "cause": "특정 옷에 대한 감각 민감성 또는 예측되지 않은 변화로 인해 스트레스가 유발됨",
  "intervention": [
    "아이가 선호하는 옷을 먼저 보여주며 선택권을 주고, 상황을 시각적으로 설명하며 천천히 옷 입기를 유도함"
  ]
}"""
    st.session_state.history1 = [("GPT", st.session_state.strategy)]

# ─── 응답자 ID 확인 ───────────────────────────────
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("홈에서 먼저 응답자 ID를 입력해주세요.")
    st.stop()

# ─── 타이틀 및 설명 표시 ───────────────────────────
st.title("자폐 행동 중재 전략 개선 시스템")

st.markdown("""
이 페이지에서는 설문을 진행하시고 계시는 분의 피드백을 바탕으로 GPT가 중재 전략을 반복적으로 개선하는 시스템을 체험해보실 수 있습니다. 
아래의 문제 상황과 GPT가 제안한 전략을 확인하고, 피드백을 제공해 주세요. 

이 설문의 주 목적은 GPT와의 대화를 통한 중재 방안의 개선이 얼마나 유용한지 그리고 사용자의 피로도는 얼마나 되는지를 측정하는 것입니다.
따라서 최소한 3번 정도의 피드백을 주시면 감사드리겠습니다.
피드백의 형식은 없으며 자유롭게 GPT가 처음 제시한 중재방안에 대해서 지적을 해주시거나 혹은 새로운 상황을 가정하여 피드백을 주시면 됩니다.
(ex. 자폐아가 특정 사물에 집착하여 위험한 행동을 함 --> 부모가 자폐아의 관심 유도를 위하여 손에 들고 있던 간식을 제시함 --> 자폐아가 간식에 관심을 주지 않고 계속해서 특정 사물에 집착하며 점차적으로 Meltdown 현상을 보이기 시작함)

전략 개선이 완료되었다고 판단되면 `"Complete"`를 입력하면 설문으로 이동합니다.
""")

# ─── GPT 피드백 루프 ───────────────────────────────
if st.session_state.state1 == "feedback_loop":
    st.subheader("📝 문제 상황")
    st.markdown(f"{st.session_state.problem}")

    st.subheader("🤖 GPT의 전략 제안")
    st.markdown(f"```\n{st.session_state.strategy}\n```")

    feedback = st.chat_input("전략에 대한 피드백을 입력해주세요. (완성되었다고 판단되면 'Complete'를 입력)")

    if feedback:
        if feedback.strip().lower() == "complete":
            st.session_state.state1 = "survey"
            st.success("✅ 'Complete'가 입력되었습니다. 설문으로 이동합니다.")
            st.rerun()
        else:
            prompt = f"""이전 전략:
{st.session_state.strategy1}

돌봄 교사의 피드백: {feedback}

이 피드백을 반영하여 전략을 개선해 주세요.
JSON 형식: {{
  "cause": "...",
  "intervention": ["...", "..."]
}}
"""
            response = agent.call_as_llm(prompt)  # GPT 호출
            st.session_state.strategy1 = response
            st.session_state.history1.append(("GPT", response))
            st.rerun()

# ─── 설문조사 단계 ────────────────────────────────
elif st.session_state.state1 == "survey":
    st.subheader("📝 GPT 피드백 반복 전략에 대한 설문조사")

    q1 = st.slider("1. 최종 전략이 문제 해결에 적절했다고 느끼십니까?", 0, 5)
    q2 = st.slider("2. 피드백을 반영할수록 전략이 개선되었다고 느끼셨습니까?", 0, 5)
    q3 = st.slider("3. 반복 과정에서 피로감을 느끼셨습니까?", 0, 5)
    comment = st.text_area("4. 추가 의견이 있다면 자유롭게 작성해 주세요.")

    if st.button("설문 제출"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expert_id = st.session_state.expert_id
        user_dir = f"responses/{expert_id}"
        
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, "feedback_gpt_loop_2.csv")
        
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{now},{expert_id},{q1},{q2},{q3},\"{comment}\"\n")
        st.success("설문이 저장되었습니다. 감사합니다!")


col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/7_improve_survey.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/caregraph_effectiveness.py")    # pages/survey2.py (확장자 제외)
