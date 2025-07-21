import streamlit as st
import json
import datetime
import joblib
import os
from json_repair import repair_json
import re

from pages.tool import CareGraph, MemoryAgent, _4oMiniClient, UserProfile
from my_switch import switch_page

if not st.session_state.get("caregraph_effectiveness_4_init"):
    # 최초 진입 시에만 이전 페이지 키 삭제
    for key in ['state2','situation2','strategy2','history2','loop_count2']:
        st.session_state.pop(key, None)
    st.session_state.caregraph_effectiveness_4_init = True

# --- Helper functions ---
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
        "학교 공개 수업 날, 평소와 달리 교실 뒷자리에 여러 명의 낯선 학부모들이 조용히 앉아 있었고, 교실 전체가 평소와 다른 분위기가 형성되자, A는 점점 손을 흔들며 불안 신호를 보이다가 갑자기 귀를 막고 자리 밑으로 웅크리며 멜트다운을 일으켰다."
    )
    st.session_state.strategy2 = {
        'cause': '학교 공개 수업 날 형성된 낯선 사람들의 정적인 존재와 교실의 비일상적인 분위기 변화가 A에게 심리적 압박과 예측 불가능한 긴장감을 유발하여 감각 과부하 및 멜트다운으로 이어짐',
        'intervention': [
            {'strategy': '예고된 변화 시각화 및 사전 시뮬레이션',
             'purpose': '낯선 사람의 존재와 환경 변화에 대한 불안을 사전에 인지하고 준비할 수 있도록 하여 예측 가능성을 높이고 감각적·심리적 안정 확보',
             'example': {'immediate': '멜트다운 징후(손 흔들기)가 나타날 시, 교사는 A에게 눈높이를 맞추고 미리 준비된 ‘안심 시각카드’(“지켜보기만 해요”, “곧 끝나요”)를 조용히 보여주며 말 없이 고개를 끄덕여 안정감을 전달',
                         'standard': '공개 수업 전날과 당일 아침, A와 함께 교실 내 낯선 사람 등장 상황을 담은 그림카드 또는 짧은 역할극을 통해 예측 가능한 시나리오로 시뮬레이션을 반복하여 노출 적응 훈련 진행'}}
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

**GPT의 답변에 대하여 판단 하실 때 위에서 제시 된 자폐인의 프로파일과 관찰일지를 참고해주시면 감사드리겠습니다.**

이 설문의 주 목적은 개인화된 자폐인 정보를 이용하는 GPT와의 대화를 통한 중재 방안의 개선이 얼마나 유용한지를 측정하는 것입니다.
따라서 최소한 3번 정도의 피드백을 주시면 감사드리겠습니다.
피드백의 형식은 없으며 자유롭게 GPT가 처음 제시한 중재방안에 대해서 지적을 해주시거나 혹은 새로운 상황을 가정하여 피드백을 주시면 됩니다.
(ex. 자폐아가 특정 사물에 집착하여 위험한 행동을 함 --> 부모가 자폐아의 관심 유도를 위하여 손에 들고 있던 간식을 제시함 --> 자폐아가 간식에 관심을 주지 않고 계속해서 특정 사물에 집착하며 점차적으로 Meltdown 현상을 보이기 시작함)

전략 개선이 완료되었다고 판단되면 "Complete"를 입력하면 설문으로 이동합니다.

각 항목에 대하여 0 = 전혀 부적절, 1 = 대체로 부적절, 2 = 보통 이하, 3 = 보통 이상, 4 = 대체로 적절, 5 = 매우 적절 로 판단해주시면 감사드리겠습니다.
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
            st.session_state.state2 = "survey"
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
                
                st.header("🔄 업데이트된 중재 전략")
                for item in parsed:
                    if not isinstance(item, dict):
                        continue
                    strategies = item.get("intervention_strategies", [])
                    for intr_raw in strategies:
                        if isinstance(intr_raw, str):
                            try:
                                intr = json.loads(intr_raw)
                            except json.JSONDecodeError:
                                intr = json.loads(repair_json(intr_raw))
                        else:
                            intr = intr_raw
                        name = intr.get("strategy_name", "전략명 없음")
                        st.subheader(f"• {name}")
                        steps = intr.get("steps", {})
                        if isinstance(steps, dict):
                            st.markdown("단계별 절차:")
                            for k in sorted(steps, key=lambda x: int(x)):
                                st.markdown(f"- {steps[k]}")
                            elif isinstance(steps, list):
                                st.markdown("단계별 절차:")
                                for s in steps:
                                    st.markdown(f"- {s}")
                            st.markdown("---")
                        
            except Exception as e:
                st.error(f"JSON 파싱 오류: {e}")

# --- Survey ---
elif st.session_state.state2 == "survey":
    st.subheader("📋 설문조사")
    st.markdown("시스템의 유용성 및 개선 가능성에 대한 의견을 남겨주세요.")

    q1 = st.slider("1. 자폐인의 개별 특성(감각/소통/스트레스 신호 등)이 전략에 반영되었다고 느끼셨습니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q1")
    q2 = st.slider("2. 과거 상황(메모리) 기록이 실제 전략 제안에 도움이 되었습니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q2")
    q3 = st.slider("3. 피드백을 반복할수록 전략이 개선되었다고 느끼셨습니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q3")
    q4 = st.slider("4. 시스템의 사용 흐름(전략 제시 - 피드백 - 반복)은 직관적이었습니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q4")
    q5 = st.slider("5. 전체적으로 문제 상황 해결에 실질적인 기여를 했다고 생각하십니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q5")
    q6 = st.slider("6. 이 시스템을 실제 교실/상담/일반 가정 환경에 적용할 수 있다고 생각하십니까? (0=전혀 아니다, 5=매우 그렇다)", 0, 5, key="q6")
    comment = st.text_area("7. 기타 의견 또는 개선 제안이 있다면 자유롭게 적어주세요")

    if st.button("설문 제출"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expert_id = st.session_state.expert_id
        user_dir = f"responses/{expert_id}"
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, "caregraph_effectiveness.csv")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"{now},{expert_id},{q1},{q2},{q3},{q4},{q5},{q6},\"{comment}\"")
        st.success("모든 설문이 완료 되었습니다. 고생하셨습니다!")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("◀ 이전 페이지"):
        st.switch_page("pages/8_caregraph_effectiveness_3.py")       # pages/home.py (확장자 제외)
