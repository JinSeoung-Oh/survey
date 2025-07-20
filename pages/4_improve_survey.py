import streamlit as st
import datetime
from my_switch import switch_page
from pages.tool import O3MiniClient
import os

agent = O3MiniClient()

# ─── 초기 세션 상태 설정 ─────────────────────────────
if "state" not in st.session_state:
    st.session_state.state = "feedback_loop"
    st.session_state.problem = "할머니 생신 잔치에 참석한 자폐인이 친척들과 이웃들로 붐빈 낯선 환경에서 불안 증상을 보이다가, 결국 울음을 터뜨리며 가구 뒤에 숨거나 귀를 막는 등의 감각 과부하 행동을 나타냈음"
    st.session_state.strategy = {
        'cause': '낯선 사람들(친척 및 이웃)의 밀집된 환경, 익숙하지 않은 분위기, 많은 말소리와 움직임이 동시에 자폐인의 감각 시스템을 압도하여 감각 과부하 및 불안을 유발함. 이로 인해 자폐인은 울음, 숨기, 귀 막기 등 자극 회피 행동을 나타냄.',
        'intervention': [
            {'strategy': '감각 차단 휴식 공간 제공 (Sensory Retreat)',
             'purpose': '과도한 감각 자극으로부터 자폐인을 일시적으로 보호하여 안정감을 회복하고 환경 적응을 유도',
             'example': {'immediate': '자폐인이 울음을 터뜨릴 때 즉시 조용하고 인적이 드문 방이나 공간(예: 안방, 베란다 등)으로 동행하여 귀를 막지 않아도 되는 수준으로 감각 자극을 차단하고, 시각·청각 자극을 최소화한 공간에서 편안히 쉴 수 있도록 함',
                         'standard': '잔치 등 군중이 많은 상황에서는 사전에 \'감각 휴식 공간\'을 확보하고, 자폐인이 해당 공간의 위치와 사용 방식을 미리 익히도록 연습하며, 필요 시 언제든 해당 공간으로 이동할 수 있다는 신호와 루틴을 정해 안정감을 줄 수 있도록 함'}}
        ]
    }
    st.session_state.history = [("GPT", st.session_state.strategy)]

# ─── 응답자 ID 확인 ───────────────────────────────
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("홈에서 먼저 응답자 ID를 입력해주세요.")
    st.stop()

# ─── 타이틀 및 설명 표시 ───────────────────────────
st.title("자폐 행동 중재 전략 개선 시스템")

st.markdown("""
이 페이지에서는 설문을 진행하시고 계시는 분의 피드백을 바탕으로 GPT가 중재 전략을 반복적으로 개선하는 시스템을 체험해보실 수 있습니다. 
아래의 문제 상황과 GPT가 제안한 전략을 확인하고, 피드백을 제공해 주세요. 

이 설문의 주 목적은 유저 피드백을 통한 GPT와의 대화가 중재 방안의 개선이 얼마나 유용한지 그리고 사용자의 피로도는 얼마나 되는지를 측정하는 것입니다.
따라서 최소한 3번 정도의 피드백을 주시면 감사드리겠습니다.
피드백의 형식은 없으며 자유롭게 GPT가 처음 제시한 중재방안에 대해서 지적을 해주시거나 혹은 새로운 상황을 가정하여 피드백을 주시면 됩니다.
(ex. 자폐아가 특정 사물에 집착하여 위험한 행동을 함 --> 부모가 자폐아의 관심 유도를 위하여 손에 들고 있던 간식을 제시함 --> 자폐아가 간식에 관심을 주지 않고 계속해서 특정 사물에 집착하며 점차적으로 Meltdown 현상을 보이기 시작함)

전략 개선이 완료되었다고 판단되면 `"Complete"`를 입력하면 설문으로 이동합니다.

각 항목에 대하여 0 = 전혀 부적절, 1 = 대체로 부적절, 2 = 보통 이하, 3 = 보통 이상, 4 = 대체로 적절, 5 = 매우 적절 로 판단해주시면 감사드리겠습니다.
""")

# ─── GPT 피드백 루프 ───────────────────────────────
if st.session_state.state == "feedback_loop":
    strategy = st.session_state.strategy
    intervention = strategy['intervention'][0]  # 리스트 안 하나의 전략
    example = intervention['example']
    st.subheader("📝 문제 상황")
    st.markdown(f"{st.session_state.problem}")

    st.subheader("🤖 GPT의 전략 제안")
    st.markdown(f"""
**Cause:**  
{strategy['cause']}

**중재 전략:**  
- Strategy: {intervention['strategy']}  
- Purpose: {intervention['purpose']}  
- Immediate: {example['immediate']}  
- Standard: {example['standard']}
""")

    feedback = st.chat_input("전략에 대한 피드백을 입력해주세요. (완성되었다고 판단되면 'Complete'를 입력)")

    if feedback:
        if feedback.strip().lower() == "complete":
            st.session_state.state = "survey"
            st.success("✅ 'Complete'가 입력되었습니다. 설문으로 이동합니다.")
            st.rerun()
        else:
            prompt = f"""이전 전략:
{st.session_state.strategy}

돌봄 교사의 피드백: {feedback}

이 피드백을 반영하여 전략을 개선해 주세요.
JSON 형식: {{
  "cause": "...",
  "intervention": ["...", "..."]
}}
"""
            response = agent.call_as_llm(prompt)  # GPT 호출
            st.session_state.strategy = response
            st.session_state.history.append(("GPT", response))
            st.rerun()

# ─── 설문조사 단계 ────────────────────────────────
elif st.session_state.state == "survey":
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
        filepath = os.path.join(user_dir, "feedback_gpt_loop_1.csv")
        
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{now},{expert_id},{q1},{q2},{q3},\"{comment}\"\n")
        st.success("설문이 저장되었습니다. 감사합니다!")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/3_survey_3.py")       # pages/home.py (확장자 제외)
with col2:
    if st.button("다음 페이지 ▶"):
        st.switch_page("pages/5_improve_survey_2.py")    # pages/survey2.py (확장자 제외)
