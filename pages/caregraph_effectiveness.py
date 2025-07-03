import streamlit as st
import json
import datetime
import joblib
import os
from json_repair import repair_json

from pages.tool import CareGraph, MemoryAgent, _4oMiniClient, UserProfile
from my_switch import switch_page

# --- Helper functions ---
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

if 'llm' not in st.session_state:
    st.session_state.llm = _4oMiniClient()

if 'agent' not in st.session_state:
    st.session_state.agent = MemoryAgent(st.session_state.llm, st.session_state.graph)
    
# --- Page‐specific state (state2) initialization ---
if 'state2' not in st.session_state:
    st.session_state.state2 = "feedback_loop"
    st.session_state.situation2 = (
        "할머니 생신 잔치에 참석한 자폐인이 친척들과 이웃들로 붐빈 낯선 환경에서 불안 증상을 보이다가, 결국 울음을 터뜨리며 가구 뒤에 숨거나 귀를 막는 등의 감각 과부하 행동을 나타냈음"
    )
    st.session_state.strategy2 = {
        'cause': '혼잡한 환경에서 발생하는 소음, 낯선 얼굴들과 과도한 움직임으로 인한 감각 과부하와 불안감이 자폐인이 긍정적인 대처를 하지 못하고 극도의 스트레스 반응을 보이게 만듭니다',
        'intervention': [
            {'strategy': '안전한 피난처 제공',
             'purpose': '감각 과부하를 완화하고 자폐인이 안정감을 되찾을 수 있도록 조용한 개인 공간을 마련',
             'example': {'immediate': '문제가 발생했을 때 즉시 조용한 방이나 지정된 휴식 공간으로 안내하여 불안을 줄임',
                         'standard': '가족 모임 전 미리 조용한 휴식 공간을 사전에 마련하고, 자폐인에게 그 공간 이용 방법을 시각적 자료와 함께 안내'}}
        ]
    }
    st.session_state.history2 = []
    st.session_state.loop_count2 = 0

# 관리자 정의 초기 안내
st.title("가상의 자폐인의 프로파일과 관찰 일지가 적용된 GraphDB와 O3-mini를 통한 시스템 관련 설문")

st.markdown("""
이 페이지에서는 가상의 자폐인 A의 프로파일과 관찰 일지로 구축된 GraphDB와 O3-mini를 이용한 시스템에 관한 유용성에 대한 설문을 진행하시게 됩니다.
아래에 제시 되어 있는 관찰 일지의 중재는 해당 상황에서 자폐인을 중재하는데 성공한 중재방안입니다.

**자폐인 A의 프로파일**  \n가상의 자폐인 A는 소리에 매우 민감하며 광반응에는 그렇게까지 민감하지 않고 의사소통 시에는 대화만 하는 것보다는 바디 랭귀지를 섞는 것을 더 선호하는 것으로 세팅했습니다. 스트레스를 받을 시에 손을 흔들거나 혹은 공격적인 성향을 보이는 것으로 설정했습니다.

**자폐인 A의 관찰 일지**  \n**상황_1** : 붐비고 시끄러운 슈퍼마켓 환경, 즉 많은 사람들과 소음, 낯선 자극들로 인한 감각 과부하가 원인으로 작용하여 자폐인이 불편함을 느끼고, 부모에게 향하는 항의 및 신체적 저항 행동(짜증 행동)을 나타냄  \n**중재_1** : 부모가 가능한 한 조용하고 밝기가 낮은 구역으로 즉시 이동시켜 감각 자극을 줄임

**상황_2** : 계곡에서 가족들과 즐거운 시간을 보내고 있었으나 갑자기 낯선 가족들이 자폐인의 가족이 있는 곳으로 오면서 자폐인이 분노와 공포 반응을 보였음  \n**중재_2** : 부모나 돌봄자가 부드럽게 다가가서 가볍게 어깨를 감싸거나 손을 잡으며 '괜찮아, 안전해'라는 짧은 시각적 메시지를 전달함

이 설문의 주 목적은 개인화된 자폐인 정보를 이용하는 GPT와의 대화를 통한 중재 방안의 개선이 얼마나 유용한지를 측정하는 것입니다.
따라서 최소한 3번 정도의 피드백을 주시면 감사드리겠습니다.
피드백의 형식은 없으며 자유롭게 GPT가 처음 제시한 중재방안에 대해서 지적을 해주시거나 혹은 새로운 상황을 가정하여 피드백을 주시면 됩니다.
(ex. 자폐아가 특정 사물에 집착하여 위험한 행동을 함 --> 부모가 자폐아의 관심 유도를 위하여 손에 들고 있던 간식을 제시함 --> 자폐아가 간식에 관심을 주지 않고 계속해서 특정 사물에 집착하며 점차적으로 Meltdown 현상을 보이기 시작함)

전략 개선이 완료되었다고 판단되면 "Complete"를 입력하면 설문으로 이동합니다.
""")

# Expert ID input
if 'expert_id' not in st.session_state:
    st.session_state.expert_id = st.text_input("응답자 ID를 입력해주세요.")
    if not st.session_state.expert_id:
        st.stop()

# --- Feedback loop ---
if st.session_state.state2 == "feedback_loop":
    strat = st.session_state.strategy2
    st.subheader("🤖 중재 전략 피드백")
    st.write(f"**문제 상황:** {st.session_state.situation2}")
    st.write(f"**원인:** {strat.get('cause')}")
    st.write("**중재 후보:**")
    for i, intr in enumerate(strat.get('intervention', []), 1):
        st.write(f"{i}. {intr.get('strategy')} - {intr.get('purpose')}")
        st.write(f"   - 즉시 적용: {intr.get('example', {}).get('immediate')}")
        st.write(f"   - 표준 상황: {intr.get('example', {}).get('standard')}")

    feedback = st.chat_input(
        "피드백을 입력하세요 (완료 시 'Complete' 입력):"
    )
    if feedback:
        if feedback.strip().lower() == "complete":
            st.session_state.agent.finalize(st.session_state.expert_id)
            st.session_state.state = "survey"
            st.success("전략 개선 완료. 설문으로 이동합니다.")
            st.rerun()
        else:
            # 루프 진행
            st.session_state.history2.append({
                'loop': st.session_state.loop_count2 + 1,
                'strategy': strat,
                'feedback': feedback
            })
            st.session_state.loop_count2 += 1
            retry_resp = st.session_state.agent.alt_ask(
                "A123",
                feedback,
                strat.get('event')
            )

            try:
                repaired = repair_json(retry_resp)
                parsed = json.loads(repaired)

                st.session_state.strategy_list = []

                if isinstance(parsed, list):
                    for item in parsed:
                        st.session_state.strategy_list.append({
                                   'event': item.get('event', ''),
                                   'observed_behavior': item.get('observed_behavior', []),
                                   'intervention': item.get('intervention_strategies', [])
                                    })
                    
                elif isinstance(parsed, dict) and 'action_input' in parsed:
                    for evt, detail in parsed['action_input'].items():
                        st.session_state.strategy_list.append({
                                    'event': evt,
                                    'cause': detail.get('cause', ''),
                                    'intervention': detail.get('intervention', [])
                            })
                    
                else:
                    raise ValueError("지원되지 않는 JSON 구조입니다.")

                if st.session_state.strategy_list:
                    st.markdown("---")
                    st.header("🔄 업데이트된 중재 전략")
                    for idx, strat in enumerate(st.session_state.strategy_list, start=1):
                        with st.expander(f"{idx}. 이벤트: {strat['event']}", expanded=(idx==1)):
                            obs = strat.get('observed_behavior', [])
                            if obs:
                                st.markdown(f"**관찰된 행동:** {', '.join(obs)}")
                            intervs = strat.get('intervention', [])
                            if intervs:
                                st.markdown("**중재 전략:**")
                                for jdx, iv in enumerate(intervs, start=1):
                                    title = (iv.get('description')
                                             or iv.get('strategy_name')
                                             or iv.get('name')
                                             or iv.get('strategy', '')
                                             )
                                    st.markdown(f"**{j}. {title}**")
                                    for step in iv.get('steps', []):
                                        clean = re.sub(r'^\s*\d+\.\s*', '', step)
                                        st.markdown(f"- {clean}")

            except Exception as e:
                st.error(f"JSON 파싱 오류: {e}")

# --- Survey ---
elif st.session_state.state2 == "survey":
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
            f.write(f"{now},{expert_id},{q1},{q2},{q3},{q4},{q5},{q6},\"{comment}\"")
        st.success("응답이 저장되었습니다. 감사합니다!")

col1,= st.columns([1])
with col1:
    if st.button("◀ 이전 페이지"):
       st.switch_page("pages/improve_survey_2.py")
