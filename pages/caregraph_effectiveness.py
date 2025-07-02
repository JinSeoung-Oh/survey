import streamlit as st
import json
import datetime
import joblib
import os

from tool import CareGraph, MemoryAgent, _4oMiniClient 
from streamlit_extras.switch_page_button import switch_page

# --- Helper functions ---
def save_graph(graph: CareGraph, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(graph, path)

def load_graph(path: str) -> CareGraph:
    graph = joblib.load(path)
    graph.llm = _4oMiniClient()

# --- Session initialization ---
if 'graph' not in st.session_state:
    # Initialize or load CareGraph and profile
    if os.path.exists("../caregraph_full.pkl"):
        st.session_state.graph = load_graph("../caregraph_full.pkl")
    else:
        st.session_state.graph = CareGraph()
        # 관리자 정의 초기 사용자 프로필
        profile = UserProfile(
            user_id="A123",
            sensory_profile={'sound':'high','light':'medium'},
            communication_preferences={"visual": "high", "verbal": "low"},
            stress_signals=['hand flapping', 'aggressive behavior']
        )
        st.session_state.graph.add_profile(profile)
        save_graph(st.session_state.graph, "caregraph_full.pkl")
    # Initialize agent with admin-defined defaults
    st.session_state.llm = O3MiniClient()
    st.session_state.agent = MemoryAgent(st.session_state.llm, st.session_state.graph)
    # 관리자 정의 초기 상황 및 초기 전략
    st.session_state.state = "feedback_loop"
    st.session_state.situation = (
        "할머니 생신 잔치에 자폐인 가족이 참석하였음. 할머니 댁에는 친척들과 할머니의 이웃들로 붐비고 있음. 낯선 사람들이 가득한 환경에서 자폐인이 불안 증상을 보이다가 결국 울음을 터뜨리며 다른 사람과 상호작용하거나 행사에 참여하도록 유도하는 언어나 신체적 시도에 대해 거부 반응을 보임. 가구 뒤에 숨거나 귀를 막는 등의 행동을 보이며 감각 과부하를 나타내고 있음"
    )
    st.session_state.strategy = {
        'cause': '혼잡한 환경에서 발생하는 소음, 낯선 얼굴들과 과도한 움직임으로 인한 감각 과부하와 불안감이 자폐인이 긍정적인 대처를 하지 못하고 극도의 스트레스 반응을 보이게 만듭니다',
        'intervention': [
            {'strategy': '안전한 피난처 제공',
             'purpose': '감각 과부하를 완화하고 자폐인이 안정감을 되찾을 수 있도록 조용한 개인 공간을 마련',
             'example': {'immediate': '문제가 발생했을 때 즉시 조용한 방이나 지정된 휴식 공간으로 안내하여 불안을 줄임',
                         'standard': '가족 모임 전 미리 조용한 휴식 공간을 사전에 마련하고, 자폐인에게 그 공간 이용 방법을 시각적 자료와 함께 안내'}}
        ]
    }
    st.session_state.history = []
    st.session_state.loop_count = 0

# 관리자 정의 초기 안내
st.title("가상의 자폐인의 프로파일과 관찰 일지가 적용된 GraphDB와 O3-mini를 통한 시스템 관련 설문")

st.markdown("""
이 페이지에서는 가상의 자폐인 A의 프로파일과 관찰 일지로 구축된 GraphDB와 O3-mini를 이용한 시스템에 관한 유용성에 대한 설문을 진행하시게 됩니다.
아래에 제시 되어 있는 관찰 일지의 중재는 해당 상황에서 자폐인을 중재하는데 성공한 중재방안입니다.

- 자폐인 A의 프로파일
가상의 자폐인 A는 소리에 매우 민감하며 광반응에는 그렇게까지 민감하지 않고 의사소통 시에는 대화만 하는 것보다는 바디 랭귀지를 섞는 것을 더 선호하는 것으로 세팅했습니다. 스트레스를 받을 시에 손을 흔들거나 혹은 공격적인 성향을 보이는 것으로 설정했습니다.

- 자폐인 A의 관찰 일지
상황_1 : 붐비고 시끄러운 슈퍼마켓 환경, 즉 많은 사람들과 소음, 낯선 자극들로 인한 감각 과부하가 원인으로 작용하여 자폐인이 불편함을 느끼고, 부모에게 향하는 항의 및 신체적 저항 행동(짜증 행동)을 나타냄
중재_1 : 부모가 가능한 한 조용하고 밝기가 낮은 구역으로 즉시 이동시켜 감각 자극을 줄임

상황_2 : 계곡에서 가족들과 즐거운 시간을 보내고 있었으나 갑자기 낯선 가족들이 자폐인의 가족이 있는 곳으로 오면서 자폐인이 분노와 공포 반응을 보였음
중재_2 : 부모나 돌봄자가 부드럽게 다가가서 가볍게 어깨를 감싸거나 손을 잡으며 '괜찮아, 안전해'라는 짧은 시각적 메시지를 전달함

상황_3 : 자폐인에게 간식을 주던 부모가 간식 주는 것을 멈추자 자폐인이 더 달라는 신호를 보냄. 하지만 부모가 이를 무시하였고 자폐인이 이에 화를 내기 시작함
중재_3 : 아이의 제스처가 관찰되면 시각적 소통 도구(예: 그림 카드, 소통 게시판)를 즉시 제시하여 아이가 요구하는 바를 구체적으로 표현할 수 있도록 도와줌

상황_4 : 부모와 함께 차를 타고 이동 중이던 자폐인이 밖에서 빠르게 휙휙 바뀌는 풍경을 바라보다가 갑자기 몸부림을 치며 부모를 손으로 치기 시작함
중재_4 : 부모가 차분한 목소리로 아이에게 '안전해'라는 말을 반복하며, 손짓 등 부드러운 신체 언어로 안정감을 줌

이 설문의 주 목적은 개인화된 자폐인 정보를 이용하는 GPT와의 대화를 통한 중재 방안의 개선이 얼마나 유용한지를 측정하는 것입니다.
따라서 최소한 3번 정도의 피드백을 주시면 감사드리겠습니다.
피드백의 형식은 없으며 자유롭게 GPT가 처음 제시한 중재방안에 대해서 지적을 해주시거나 혹은 새로운 상황을 가정하여 피드백을 주시면 됩니다.
(ex. 자폐아가 특정 사물에 집착하여 위험한 행동을 함 --> 부모가 자폐아의 관심 유도를 위하여 손에 들고 있던 간식을 제시함 --> 자폐아가 간식에 관심을 주지 않고 계속해서 특정 사물에 집착하며 점차적으로 Meltdown 현상을 보이기 시작함)

전략 개선이 완료되었다고 판단되면 `"Complete"`를 입력하면 설문으로 이동합니다.
""")

# Expert ID input
if 'expert_id' not in st.session_state:
    st.session_state.expert_id = st.text_input("응답자 ID를 입력해주세요.")
    if not st.session_state.expert_id:
        st.stop()

# --- Feedback loop ---
if st.session_state.state == "feedback_loop":
    strat = st.session_state.strategy
    st.subheader("🤖 중재 전략 피드백 (반복)")
    st.markdown(f"**문제 상황:** {st.session_state.situation}")
    st.markdown(f"**행동 유형:** {strat.get('event')}")
    st.markdown(f"**원인:** {strat.get('cause')}")
    st.markdown("**중재 후보:**")
    for i, intr in enumerate(strat.get('intervention', []), 1):
        st.markdown(f"{i}. {intr.get('strategy')} - {intr.get('purpose')}")
        st.markdown(f"   - 즉시 적용: {intr.get('example', {}).get('immediate')}")
        st.markdown(f"   - 표준 상황: {intr.get('example', {}).get('standard')}")

    feedback = st.chat_input(
        "피드백을 입력하세요 (완료 시 'Complete' 입력):"
    )
    if feedback:
        if feedback.strip().lower() == "complete":
            st.session_state.agent.finalize(st.session_state.expert_id)
            save_graph(st.session_state.graph, "caregraph_full.pkl")
            st.session_state.state = "survey"
            st.success("전략 개선 완료. 설문으로 이동합니다.")
            st.rerun()
        else:
            # 루프 진행
            st.session_state.history.append({
                'loop': st.session_state.loop_count + 1,
                'strategy': strat,
                'feedback': feedback
            })
            st.session_state.loop_count += 1
            retry_resp = st.session_state.agent.alt_ask(
                st.session_state.expert_id,
                feedback,
                strat.get('event')
            )
            try:
                parsed = json.loads(retry_resp)
                for evt, detail in parsed.get('action_input', {}).items():
                    st.session_state.strategy = {
                        'event': evt,
                        'cause': detail.get('cause', ''),
                        'intervention': detail.get('intervention', [])
                    }
                    break
                save_graph(st.session_state.graph, "caregraph_full.pkl")
                st.rerun()
            except Exception as e:
                st.error(f"JSON 파싱 오류: {e}")

# --- Survey ---
elif st.session_state.state == "survey":
    st.subheader("📋 설문조사")
    st.markdown("시스템의 유용성 및 개선 가능성에 대한 의견을 남겨주세요.")

    q1 = st.slider("1. 자폐인의 개별 특성(감각/소통/스트레스 신호 등)이 전략에 반영되었다고 느끼셨습니까?", 0, 5)
    q2 = st.slider("2. 과거 상황(메모리) 기록이 실제 전략 제안에 도움이 되었습니까?", 0, 5)
    q3 = st.slider("3. 피드백을 반복할수록 전략이 개선되었다고 느끼셨습니까?", 0, 5)
    q4 = st.slider("4. 시스템의 사용 흐름(전략 제시 - 피드백 - 반복)은 직관적이었습니까?", 0, 5)
    q5 = st.slider("5. 전체적으로 문제 상황 해결에 실질적인 기여를 했다고 생각하십니까?", 0, 5)
    q6 = st.slider("6. 이 시스템을 실제 교실/상담 환경에 적용할 수 있다고 생각하십니까?", 0, 5)
    comment = st.text_area("7. 기타 의견 또는 개선 제안이 있다면 자유롭게 적어주세요")

    if st.button("설문 제출"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expert_id = st.session_state.expert_id
        user_dir = f"responses/{expert_id}"
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, "caregraph_effectiveness.csv")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{now},{expert_id},{q1},{q2},{q3},{q4},{q5},{q6},\"{comment}\"
")
        st.success("응답이 저장되었습니다. 감사합니다!")

col1,= st.columns([1])
with col1:
    if st.button("◀ 이전 페이지"):
       switch_page("improve_survey2")
