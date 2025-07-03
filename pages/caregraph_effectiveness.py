import streamlit as st
import json
import datetime
import joblib
import os

from pages.tool import CareGraph, MemoryAgent, _4oMiniClient, UserProfile
from my_switch import switch_page

# --- Helper functions ---
def save_graph(graph: CareGraph, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(graph, path)

def load_graph(path: str) -> CareGraph:
    graph = joblib.load(path)
    graph.llm = _4oMiniClient()
    return graph

# --- Session initialization ---
if 'graph' not in st.session_state:
    # Initialize or load CareGraph and profile
    if os.path.exists("../caregraph_full.pkl"):
        st.session_state.graph = load_graph("../caregraph_full.pkl")
    else:
        st.session_state.graph = CareGraph()
        profile = UserProfile(
            user_id="A123",
            sensory_profile={'sound':'high','light':'medium'},
            communication_preferences={"visual": "high", "verbal": "low"},
            stress_signals=['hand flapping', 'aggressive behavior']
        )
        st.session_state.graph.add_profile(profile)
        save_graph(st.session_state.graph, "caregraph_full.pkl")
    st.session_state.llm = _4oMiniClient()
    st.session_state.agent = MemoryAgent(st.session_state.llm, st.session_state.graph)

# --- page-specific session state (state2) ---
if 'state2' not in st.session_state:
    st.session_state.state2 = "feedback_loop"
    st.session_state.situation2 = (
        "할머니 생신 잔치에 ... 감각 과부하를 나타내고 있음"
    )
    st.session_state.strategy2 = {
        'cause': '혼잡한 환경에서 발생하는 소음,...',
        'intervention': [
            {
                'strategy': '안전한 피난처 제공',
                'purpose': '감각 과부하를 완화...',
                'example': {
                    'immediate': '문제가 발생했을 때 즉시...',
                    'standard': '가족 모임 전 미리...'
                }
            }
        ]
    }
    st.session_state.history2 = []

# --- ensure expert_id ---
if 'expert_id' not in st.session_state or not st.session_state.expert_id:
    st.warning("홈에서 먼저 응답자 ID를 입력해주세요.")
    st.stop()

st.title("자폐 행동 중재 전략 개선 시스템 (2차 피드백)")

# --- Feedback loop (state2) ---
if st.session_state.state2 == "feedback_loop":
    st.subheader("📝 문제 상황")
    st.markdown(st.session_state.situation2)

    st.subheader("🤖 GPT의 전략 제안")
    st.markdown(f"```json\n{json.dumps(st.session_state.strategy2, ensure_ascii=False, indent=2)}\n```")

    feedback = st.chat_input("피드백을 입력해주세요 (완료 시 'Complete')")
    if feedback:
        if feedback.strip().lower() == "complete":
            st.session_state.state2 = "survey"
            st.success("✅ 'Complete' 입력됨 — 설문으로 이동합니다.")
            st.experimental_rerun()
        else:
            prompt = f"""이전 전략:\n{json.dumps(st.session_state.strategy2, ensure_ascii=False)}\n\n돌봄 교사의 피드백: {feedback}\n\n이 피드백을 반영하여 전략을 개선해 주세요.\nJSON 형식: {{\n  \"cause\": \"...\",\n  \"intervention\": [\"...\"]\n}}"""
            response = st.session_state.agent.call_as_llm(prompt)
            try:
                parsed = json.loads(response)
                st.session_state.strategy2 = parsed
            except Exception:
                st.session_state.strategy2 = {'cause':'', 'intervention':[]}
            st.session_state.history2.append({'feedback': feedback, 'result': st.session_state.strategy2})
            st.experimental_rerun()

# --- Survey (state2) ---
elif st.session_state.state2 == "survey":
    st.subheader("📋 2차 피드백 전략 설문조사")
    q1 = st.slider("1. 최종 전략이 문제 해결에 적절했습니까?", 0, 5)
    q2 = st.slider("2. 추가 피드백 후 전략이 개선되었다고 느끼셨습니까?", 0, 5)
    q3 = st.slider("3. 이번 세션의 피로도는 어떠셨습니까?", 0, 5)
    comment = st.text_area("4. 기타 의견이 있다면 자유롭게 작성해주세요.")

    if st.button("설문 제출"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = st.session_state.expert_id
        user_dir = f"responses/{uid}"
        os.makedirs(user_dir, exist_ok=True)
        path = os.path.join(user_dir, "feedback_loop_2.csv")
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{now},{uid},{q1},{q2},{q3},\"{comment}\"\n")
        st.success("설문이 저장되었습니다. 감사합니다!")

# --- Navigation ---
col1, = st.columns([1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/improve_survey.py")
