import streamlit as st
import datetime
from my_switch import switch_page
from pages.tool import O3MiniClient
import os
import json

agent = O3MiniClient()

if not st.session_state.get("improve_survey_2_init"):
    # 최초 진입 시에만 이전 페이지 키 삭제
    for key in ['state1','situation1','strategy1','history1','loop_count1']:
        st.session_state.pop(key, None)
    st.session_state.improve_survey_2_init = True

# ─── 초기 세션 상태 설정 ─────────────────────────────
if "state1" not in st.session_state:
    st.session_state.state1 = "feedback_loop"
    st.session_state.problem1 = "학교 복도에서 급식실로 이동 중, 천장 형광등이 전력 불안정으로 불규칙하게 연속적으로 깜빡이며 이를 바라보던 A가 눈을 가린 채 멜트다운을 일으킴. "
    st.session_state.strategy1 = {
        'cause': '자폐인은 시각적 민감성이 높아 예측 불가능한 깜빡임(형광등 플리커)에 의해 혼란과 불안을 겪을 수 있으며, 이러한 반복적이고 강렬한 자극이 멜트다운을 유발함.',
        'intervention': [
            {'strategy': '시각 자극 완충 (Visual Buffering)',
             'purpose': '강한 시각 자극으로부터 자폐인을 보호하여 멜트다운을 예방하고 안정적인 환경을 유지',
             'example': {'immediate': '즉시 자폐인의 시선을 차단할 수 있도록 부드러운 후드나 챙 달린 모자, 선글라스, 안면 차폐용 패브릭 등을 제공하고, 밝기 자극이 적은 복도 측면(창문 쪽 또는 벽 쪽)으로 이동 경로를 변경하며, 가능한 빠르게 안정된 조도 환경으로 이동함',
                         'standard': '학교 이동 경로 중 조도가 불안정하거나 깜빡임 위험이 있는 구간을 사전 조사하고, 해당 구간에서는 시각 자극을 줄일 수 있는 보조 도구(모자, 차광 안경 등)를 착용하는 것을 일상 루틴으로 정착시키며, 사전에 조도 변화에 대한 경고 신호나 예고를 제공함'}}
        ]
    }
    st.session_state.history1 = [("GPT", st.session_state.strategy1)]

# ─── 응답자 ID 확인 ───────────────────────────────
if "expert_id" not in st.session_state or not st.session_state.expert_id:
    st.warning("홈에서 먼저 응답자 ID를 입력해주세요.")
    st.stop()

if 'survey5_submitted' not in st.session_state:
    st.session_state.survey5_submitted = False

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
설문 조사 완료 후 제출 버튼을 누르셔야지만 다음 페이지로 이동이 가능하십니다.
""")

# ─── GPT 피드백 루프 ───────────────────────────────
if st.session_state.state1 == "feedback_loop":
    strategy = st.session_state.strategy1
    if isinstance(strategy, dict) and "error" in strategy:
        st.error(strategy["error"])
        st.stop()

    # 안전하게 intervention 리스트 구성
    raw = strategy.get('intervention')
    if isinstance(raw, dict):
        interventions = [raw]
    elif isinstance(raw, list):
        interventions = raw
    else:
        # 문자열 혹은 기타 타입인 경우
        interventions = [{
            'strategy': str(raw),
            'purpose': '',
            'example': {'immediate': '', 'standard': ''}
        }]

    # 이제 첫 번째 전략을 꺼냅니다
    intervention = interventions[0]
    example = intervention.get('example', {})

    st.subheader("📝 문제 상황")
    st.markdown(st.session_state.problem1)

    st.subheader("🤖 GPT의 전략 제안")
    st.markdown(f"""
**Cause:**  
{strategy.get('cause','')}

**중재 전략:**  
- Strategy: {intervention.get('strategy','')}  
- Purpose: {intervention.get('purpose','')}  
- Immediate: {example.get('immediate','')}  
- Standard: {example.get('standard','')}
""")

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
**반드시 순수 JSON** (dict) 형태로만 응답해 주세요. 
예시:
{{
  "cause": "…",
  "intervention": [
    {{
      "strategy": "…",
      "purpose": "…",
      "example": {{
        "immediate": "…",
        "standard": "…"
      }}
    }}
  ]
}}
"""
            raw = agent.call_as_llm(prompt)
            new_strategy = None
            if isinstance(raw, dict):
                new_strategy = raw
            else:
                try:
                    parsed = json.loads(raw)
                except Exception as e:
                    parsed = None
                if isinstance(parsed, dict):
                    new_strategy = parsed
                else:
                    redo_prompt = (
    "이전 GPT 응답이 올바른 JSON dict가 아니었습니다.\n"
    "아래 이전 응답과 사용된 프롬프트를 참고하여,\n"
    "오직 JSON dict 형태로만, 추가 설명 없이 순수하게 다시 보내주세요.\n\n"
    "=== 이전 응답 ===\n"
    "%s\n\n"
    "=== 사용된 프롬프트 ===\n"
    "%s\n\n"
    "반드시 JSON dict 포맷:\n"
    "{\n"
    '  "cause": "...",\n'
    '  "intervention": [\n'
    '    {\n'
    '      "strategy": "...",\n'
    '      "purpose": "...",\n'
    '      "example": {\n'
    '        "immediate": "...",\n'
    '        "standard": "..." \n'
    '      }\n'
    '    }\n'
    '  ]\n'
    "}\n"
) % (raw, prompt)
                    raw2 = agent.call_as_llm(redo_prompt)
                    try:
                        parsed2 = json.loads(raw2)
                    except Exception:
                        parsed2 = None
                    if isinstance(parsed2, dict):
                        new_strategy = parsed2
                    else:
                        new_strategy = {
                                        "error" : "심각한 Error가 발생했습니다. 관리자에게 연락 부탁드립니다"
                                       }
            st.session_state.strategy1 = new_strategy
            st.session_state.history1.append(("GPT", new_strategy))
            st.rerun()

# ─── 설문조사 단계 ────────────────────────────────
elif st.session_state.state1 == "survey":
    st.subheader("📝 GPT 피드백 반복 전략에 대한 설문조사")

    q1 = st.slider("1. LLM 기반 중재 전략이 반복 피드백 후 자폐인 중재 효과를 실질적으로 개선했다고 느끼십니까? (0=전혀 아니다, 5=매우 그렇다)",0, 5, key="q1")
    q2 = st.slider("2. 각 피드백이 실제로 전략 개선에 반영되어 체감할 수 있었다고 느끼셨습니까? (0=전혀 아니다, 5=매우 그렇다)",0, 5, key="q2")
    q3 = st.slider("3. 반복적인 피드백·수정 과정에서 심리적·작업적 피로감을 느끼셨습니까? (0=전혀 아니다, 5=매우 그렇다)",0, 5, key="q3")
    q4 = st.slider("4. 최종 전략 결과를 전문가로서 신뢰할 수 있다고 생각하십니까? (0=전혀 아니다, 5=매우 그렇다)",0, 5, key="q4")
    q5 = st.slider("5. LLM의 피드백 적용 결과가 이해하기 쉽고 명료했다고 느끼셨습니까? (0=전혀 아니다, 5=매우 그렇다)",0, 5, key="q5")
    comment = st.text_area("6. 추가 의견이 있다면 자유롭게 작성해 주세요.")

    if st.button("설문 제출"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expert_id = st.session_state.expert_id
        user_dir = f"responses/{expert_id}"
        
        os.makedirs(user_dir, exist_ok=True)
        filepath = os.path.join(user_dir, "feedback_gpt_loop_2.csv")
        
        if not os.path.exists(FILEPATH):
            with open(FILEPATH, "w", encoding="utf-8") as f:
                f.write("timestamp","expert_id","intervention_effectiveness","feedback_reflection","fatigue","trust_in_strategy","clarity","additional_comments\n")

        with open(FILEPATH, "a", encoding="utf-8") as f:
            f.write(f"{now},{expert_id}",f"{q1},{q2},{q3},{q4},{q5}",f"\"{comment}\"\n")

        st.session_state.survey5_submitted = True
        st.success("설문이 저장되었습니다. 감사합니다!")

if st.session_state.survey5_submitted:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("◀ 이전 페이지"):
            st.switch_page("pages/4_improve_survey.py")       # pages/home.py (확장자 제외)
    with col2:
        if st.button("다음 페이지 ▶"):
            st.switch_page("pages/6_caregraph_effectiveness.py")    # pages/survey2.py (확장자 제외)
