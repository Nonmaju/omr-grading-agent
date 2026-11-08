"""영어 학원 평가 도우미 - 페이지 1: 서비스 소개 (랜딩)."""
import streamlit as st

st.set_page_config(page_title="영어 학원 평가 도우미", page_icon="📝", layout="wide")

# 외부 폰트·이미지 없이 CSS만 사용. 색은 Streamlit 테마 변수를 써서 라이트/다크 모두 대응.
st.markdown(
    """
<style>
[data-testid="stSidebarNav"] {display: none;}
.block-container {max-width: 1080px; padding-top: 2.5rem;}
.hero {text-align: center; padding: 2.5rem 1rem 1rem;}
.hero .badge {display: inline-block; padding: .25rem .8rem; border-radius: 999px;
  background: rgba(79,70,229,.12); color: #4f46e5; font-size: .85rem; font-weight: 600;}
.hero h1 {font-size: clamp(2rem, 5vw, 3.2rem); line-height: 1.25; margin: 1rem 0 .8rem;
  word-break: keep-all;}
.hero h1 span {background: linear-gradient(90deg, #4f46e5, #0ea5e9);
  -webkit-background-clip: text; background-clip: text; color: transparent;}
.hero p {font-size: 1.1rem; opacity: .8; max-width: 640px; margin: 0 auto; word-break: keep-all;}
.sec-title {text-align: center; font-size: 1.6rem; font-weight: 700; margin: 3rem 0 .4rem;}
.sec-sub {text-align: center; opacity: .7; margin-bottom: 1.5rem; word-break: keep-all;}
.grid {display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));}
.card {padding: 1.4rem; border-radius: 16px; border: 1px solid rgba(128,128,128,.25);
  background: var(--secondary-background-color, rgba(128,128,128,.06));}
.card .ico {font-size: 1.8rem;}
.card h3 {font-size: 1.1rem; margin: .6rem 0 .4rem; padding: 0;}
.card p {margin: 0; font-size: .95rem; opacity: .8; line-height: 1.6; word-break: keep-all;}
.step .num {display: inline-flex; align-items: center; justify-content: center; width: 2rem;
  height: 2rem; border-radius: 50%; background: #4f46e5; color: #fff; font-weight: 700;}
.footer {text-align: center; opacity: .6; font-size: .85rem; margin-top: 3.5rem;
  padding-top: 1.2rem; border-top: 1px solid rgba(128,128,128,.25); line-height: 1.7;}
</style>
""",
    unsafe_allow_html=True,
)


def link(path, label, icon, **kw):
    # 페이지 파일이 아직 없거나 단독 실행이어도 랜딩이 깨지지 않도록 처리
    try:
        st.page_link(path, label=label, icon=icon, **kw)
    except Exception:
        st.caption(f"{label} (준비 중)")


# ---- 사이드바 ----
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1rem;border:2px dashed rgba(128,128,128,.4);'
        'border-radius:12px;opacity:.7;font-weight:600;">가천대학교<br>'
        '<span style="font-size:.8rem;font-weight:400;">로고 위치</span></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    link("app.py", "서비스 소개", "🏠")
    link("pages/analysis.py", "채점·분석", "📊")
    st.caption("영어 학원 평가 도우미 v1.0")

# ---- 히어로 ----
st.markdown(
    """
<div class="hero">
<span class="badge">영어 학원 선생님을 위한 채점 도구</span>
<h1>OMR 채점은 맡기고,<br><span>학생 지도에 집중하세요</span></h1>
<p>문제지와 OMR, 정답 PDF만 올리면 자동으로 채점하고 엑셀로 정리해 드립니다.
채점 결과는 챗봇에게 바로 물어볼 수 있어요.</p>
</div>
""",
    unsafe_allow_html=True,
)
_, mid, _ = st.columns([1, 1, 1])
with mid:
    link("pages/analysis.py", "시작하기", "🚀", use_container_width=True)

# ---- 핵심 기능 ----
st.markdown(
    '<div class="sec-title">핵심 기능</div>'
    '<div class="sec-sub">반복되는 채점 업무를 줄이고, 결과 해석까지 도와 드립니다.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="grid">
<div class="card"><div class="ico">✅</div><h3>OMR 자동 채점</h3>
<p>학생별 OMR 응답을 정답과 비교해 점수와 문항별 정오답, 전체 통계를 계산합니다.</p></div>
<div class="card"><div class="ico">📄</div><h3>정답 PDF 자동 인식</h3>
<p>정답 PDF에서 문항 번호, 정답, 배점을 알아서 읽어 옵니다. 직접 입력하지 않아도 됩니다.</p></div>
<div class="card"><div class="ico">📥</div><h3>엑셀로 내려받기</h3>
<p>채점 결과를 엑셀 파일로 정리해 드려요. 학부모 상담이나 기록 보관에 바로 쓸 수 있습니다.</p></div>
<div class="card"><div class="ico">💬</div><h3>성적 질문 챗봇</h3>
<p>"가장 많이 틀린 문항은?"처럼 물어보면 답해 주고, 틀린 유형의 유사 문제도 만들어 줍니다.</p></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---- 사용 방법 ----
st.markdown(
    '<div class="sec-title">사용 방법</div>'
    '<div class="sec-sub">복잡한 설정 없이 세 단계면 끝납니다.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
<div class="grid">
<div class="card step"><span class="num">1</span><h3>파일 업로드</h3>
<p>문제지 PDF, OMR 엑셀, 정답 PDF 세 가지를 올려 주세요.</p></div>
<div class="card step"><span class="num">2</span><h3>분석 시작</h3>
<p>버튼 한 번으로 채점과 통계 계산이 진행됩니다.</p></div>
<div class="card step"><span class="num">3</span><h3>엑셀 추출 · 질문하기</h3>
<p>결과를 엑셀로 받거나, 챗봇에게 궁금한 점을 물어보세요.</p></div>
</div>
""",
    unsafe_allow_html=True,
)
st.write("")
_, mid, _ = st.columns([1, 1, 1])
with mid:
    link("pages/analysis.py", "지금 채점해 보기", "📊", use_container_width=True)

# ---- 푸터 ----
st.markdown(
    '<div class="footer">영어 학원 평가 도우미 · 가천대학교 생성형 AI 활용 부트캠프 최종평가 프로젝트'
    '</div>',
    unsafe_allow_html=True,
)
