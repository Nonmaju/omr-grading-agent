"""페이지 2: 데이터 입력 · 자동 채점 · 엑셀 추출 · 채팅."""
import streamlit as st
from dotenv import load_dotenv

from core.answer_key import parse_answer_pdf
from core.chat import answer
from core.export import to_excel
from core.grading import grade, summary
from core.problems import parse_problems_pdf

load_dotenv()
st.set_page_config(page_title="데이터 분석 · 영어 학원 평가 도우미", page_icon="📝", layout="wide")

st.markdown(
    """
<style>
[data-testid="stSidebarNav"] {display: none;}
.block-container {max-width: 1000px; padding-top: 4rem;}
.logo {text-align: center; padding: .9rem; border: 2px dashed rgba(128,128,128,.4);
  border-radius: 12px; opacity: .75; font-weight: 600; margin-bottom: .5rem;}
.logo small {font-weight: 400; font-size: .8rem;}
.page-head h1 {margin: 0; padding: 0; font-size: 2rem;}
.page-head p {opacity: .7; margin: .3rem 0 1.2rem;}
.guide {display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));}
.guide div {padding: 1.2rem; border-radius: 14px; border: 1px solid rgba(128,128,128,.25);
  background: var(--secondary-background-color, rgba(128,128,128,.06)); line-height: 1.6;
  word-break: keep-all;}
.guide b {display: inline-flex; width: 1.8rem; height: 1.8rem; align-items: center;
  justify-content: center; border-radius: 50%; background: #4f46e5; color: #fff; margin-right: .4rem;}
[data-testid="stMetric"] {padding: .9rem 1rem; border-radius: 14px;
  border: 1px solid rgba(128,128,128,.25);
  background: var(--secondary-background-color, rgba(128,128,128,.06));}
</style>
""",
    unsafe_allow_html=True,
)

ss = st.session_state
ss.setdefault("messages", [])
done = "result" in ss

# ---------------------------------------------------------------- 사이드바
with st.sidebar:
    st.markdown('<div class="logo">가천대학교<br><small>로고 위치</small></div>', unsafe_allow_html=True)
    st.page_link("app.py", label="서비스 소개", icon="🏠")
    st.page_link("pages/analysis.py", label="채점·분석", icon="📊")
    history = st.container()  # 채팅 내역: 대화가 갱신된 뒤 아래쪽에서 채움
    st.divider()
    st.subheader("데이터 업로드")
    prob_f = st.file_uploader("문제지 (PDF)", type="pdf", key="prob")
    omr_f = st.file_uploader("OMR 결과 (Excel)", type=["xlsx", "xls"], key="omr")
    ans_f = st.file_uploader("정답지 (PDF)", type="pdf", key="ans")
    start = st.button("🚀 분석 시작", type="primary", use_container_width=True,
                      disabled=not (prob_f and omr_f and ans_f))
    st.download_button("📥 엑셀 추출", data=ss.get("excel", b""), file_name="채점_결과.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True, disabled=not done)

# ---------------------------------------------------------------- 분석 시작
if start:
    with st.spinner("정답을 추출하고 채점하는 중입니다..."):
        try:
            key = parse_answer_pdf(ans_f)
            result = grade(omr_f, key)
            try:
                problems = parse_problems_pdf(prob_f)
            except Exception:
                problems = {}  # 문제 본문은 유사 문제 생성에만 쓰이므로 실패해도 채점은 계속
            ss.update(result=result, problems=problems, excel=to_excel(result), messages=[])
            done = True
        except Exception as e:
            ss.pop("result", None)
            ss.pop("excel", None)
            done = False
            st.error(f"분석에 실패했습니다: {e}")

# ---------------------------------------------------------------- 본문
st.markdown(
    '<div class="page-head"><h1>📝 영어 학원 평가 도우미</h1>'
    '<p>OMR 자동 채점 · 성적 분석 · 질문 챗봇</p></div>',
    unsafe_allow_html=True,
)
if not done:
    st.markdown(
        '<div class="guide">'
        '<div><b>1</b>왼쪽 사이드바에 <b style="all:unset">문제지·OMR·정답지</b>를 올려 주세요.</div>'
        '<div><b>2</b><b style="all:unset">분석 시작</b> 버튼을 누르면 자동으로 채점합니다.</div>'
        '<div><b>3</b>채점이 끝나면 <b style="all:unset">엑셀 추출</b>과 채팅을 쓸 수 있어요.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
else:
    s = summary(ss.result)
    c = st.columns(4)
    c[0].metric("학생 수", f"{s['학생 수']}명")
    c[1].metric("평균", f"{s['평균']}점")
    c[2].metric("중앙값", f"{s['중앙값']:g}점")
    c[3].metric("표준편차(표본)", f"{s['표준편차(표본)']}")
    st.caption("채점이 끝났어요. 아래 채팅으로 성적에 대해 물어보세요. 예: 평균이랑 중앙값이 뭐야? / 가장 많이 틀린 문제와 유사한 문제 만들어줘")

for m in ss.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if q := st.chat_input("채점 결과에 대해 질문하세요" if done else "분석을 시작하면 질문할 수 있어요", disabled=not done):
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        with st.spinner("답변을 만드는 중..."):
            text, _ = answer(q, ss.messages, ss.result, ss.problems)
        st.markdown(text)
    ss.messages += [{"role": "user", "content": q}, {"role": "assistant", "content": text}]

with history:
    st.subheader("채팅 내역")
    qs = [m["content"] for m in ss.messages if m["role"] == "user"]
    if qs:
        for q_ in qs:
            st.caption("💬 " + (q_ if len(q_) <= 30 else q_[:30] + "…"))
    else:
        st.caption("아직 대화가 없어요.")
