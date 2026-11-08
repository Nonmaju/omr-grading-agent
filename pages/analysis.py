"""페이지 2: 데이터 입력 · 자동 채점 · 엑셀 추출 · 채팅.

와이어프레임(README.pdf 6~9쪽): 왼쪽 '페이지 버튼' + 사이드바(데이터 업로드 Drag & Drop → 분석 시작 → 엑셀 추출),
오른쪽 큰 '채팅 내역' 영역과 아래 '채팅 입력'.
"""
import os

import streamlit as st

from core import theme
from core.answer_key import parse_answer_pdf
from core.chat import answer  # 이 import가 .env를 읽는다
from core.export import to_excel
from core.grading import grade, summary
from core.problems import parse_problems_pdf

st.set_page_config(page_title="채점·분석 · 영어 학원 평가 도우미", page_icon="📝", layout="wide")
theme.apply()


def _secret_key() -> str:
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return ""


ss = st.session_state
ss.setdefault("messages", [])
done = "result" in ss

# ---------------------------------------------------------------- 사이드바
with st.sidebar:
    st.page_link("app.py", label="서비스 소개", icon=":material/home:")
    st.page_link("pages/analysis.py", label="채점·분석", icon=":material/bar_chart:")
    with st.container(border=True):
        st.markdown("**데이터 업로드**")
        st.caption("Drag & Drop")
        prob_f = st.file_uploader("문제지 (PDF)", type="pdf", key="prob")
        omr_f = st.file_uploader("OMR 결과 (Excel)", type=["xlsx", "xls"], key="omr")
        ans_f = st.file_uploader("정답지 (PDF)", type="pdf", key="ans")
    start = st.button("분석 시작", icon=":material/play_arrow:", type="primary", width="stretch", disabled=not (prob_f and omr_f and ans_f))
    st.download_button("엑셀 추출", icon=":material/download:", data=ss.get("excel", b""), file_name="채점_결과.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       width="stretch", disabled=not done)

# ---------------------------------------------------------------- 분석 시작
ok = False
if start:
    with st.spinner("정답을 추출하고 채점하는 중입니다..."):
        try:
            key = parse_answer_pdf(ans_f)
            result = grade(omr_f, key)
            try:
                problems = parse_problems_pdf(prob_f)
            except Exception:
                problems = {}  # 문제 본문은 유사 문제 생성에만 쓰이므로 실패해도 채점은 계속
            warns = []
            if len(problems) < len(key):
                warns.append("문제지에서 문항 본문을 모두 읽지 못했어요(문제지와 정답지를 바꿔 올리지 않았는지 확인해 주세요). "
                             "채점은 정상이지만 유사 문제 생성의 품질이 떨어질 수 있어요.")
            if result.blank or result.invalid:
                warns.append(f"OMR에 빈칸 {result.blank}칸, 인식할 수 없는 값 {result.invalid}칸이 있어요. 이 칸은 오답으로 채점했어요.")
            ss.update(result=result, problems=problems, excel=to_excel(result), messages=[], warns=warns,
                      sig=tuple((f.name, f.size) for f in (prob_f, omr_f, ans_f)))
            ok = True
        except Exception as e:
            ss.pop("result", None)
            ss.pop("excel", None)
            done = False
            st.error(f"분석에 실패했습니다: {e}")
if ok:
    st.rerun()  # 사이드바의 엑셀 버튼은 위에서 이미 그려졌으므로, 채점 직후 활성 상태로 다시 그린다

# ---------------------------------------------------------------- 본문: 안내 + 채팅 내역 + 채팅 입력
if not (os.getenv("OPENAI_API_KEY") or _secret_key()):
    st.error("OpenAI API 키가 설정되지 않았어요. 관리자에게 문의해 주세요. (채점·엑셀은 가능하지만 채팅은 동작하지 않습니다)")
for w_ in ss.get("warns", []):
    st.warning(w_)
if done and all((prob_f, omr_f, ans_f)) and tuple((f.name, f.size) for f in (prob_f, omr_f, ans_f)) != ss.get("sig"):
    st.info("업로드한 파일이 바뀌었어요. 아래 결과는 이전 파일 기준이에요. **분석 시작**을 다시 눌러 주세요.")

chat_box = st.container(height=600, border=True)  # 채팅 내역
with chat_box:
    if not done:
        st.markdown(
            '<div class="empty-title"><h3>채팅 내역</h3><small>채점이 끝나면 여기서 성적에 대해 대화할 수 있어요</small></div>'
            '<div class="steps">'
            '<div class="step"><i>1</i><div><b>파일 올리기</b><span>왼쪽에 문제지, OMR 결과, 정답지를 올려 주세요</span></div></div>'
            '<div class="step"><i>2</i><div><b>분석 시작</b><span>버튼 한 번으로 정답 추출과 채점이 진행돼요</span></div></div>'
            '<div class="step"><i>3</i><div><b>엑셀 추출 · 질문하기</b><span>결과를 내려받거나 궁금한 점을 물어보세요</span></div></div>'
            '</div>',
            unsafe_allow_html=True)
    else:
        s = summary(ss.result)
        with st.chat_message("assistant"):  # 안내 메시지(대화 이력에는 넣지 않는다)
            st.markdown(
                f"채점이 끝났어요. 학생 **{s['학생 수']}명**, 평균 **{s['평균']}점**, 중앙값 **{s['중앙값']:g}점**, "
                f"표준편차(표본) **{s['표준편차(표본)']}**\n\n"
                "이렇게 물어보세요: *평균이랑 중앙값이 뭐야?* · *가장 성적이 저조한 학생은?* · *가장 많이 틀린 문제와 유사한 문제 만들어줘*")
    for m in ss.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

if q := st.chat_input("채점 결과에 대해 질문하세요" if done else "분석을 시작하면 질문할 수 있어요", disabled=not done):
    with chat_box:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            with st.spinner("답변을 만드는 중..."):
                text, _ = answer(q, ss.messages, ss.result, ss.problems)
            st.markdown(text)
    ss.messages += [{"role": "user", "content": q}, {"role": "assistant", "content": text}]
