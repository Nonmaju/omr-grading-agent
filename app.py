"""페이지 1: 서비스 소개(랜딩).

와이어프레임(README.pdf 6쪽): 좌상단 '페이지 버튼' / 화면 중앙 '가천대 로고' / 그 아래 서비스명.
첫 화면은 와이어프레임 그대로 두고, 서비스 소개(벤토 카드)는 아래로 스크롤하면 나온다.
"""
import logging
from pathlib import Path

import streamlit as st

from core import theme

st.set_page_config(page_title="영어 학원 평가 도우미", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
theme.apply(hide_sidebar=True)

_ICO = {  # 가는 선(1.4) 아이콘
    "grade": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="3" width="15" height="18" rx="3"/><path d="M8.5 8.5h7M8.5 12.5h4M9 17l1.8 1.8L15 15"/></svg>',
    "excel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v10m0 0-4-4m4 4 4-4M5 19h14"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5.5 5.5h13a1.5 1.5 0 0 1 1.5 1.5v8a1.5 1.5 0 0 1-1.5 1.5H12l-4.2 3v-3H5.5A1.5 1.5 0 0 1 4 15V7a1.5 1.5 0 0 1 1.5-1.5Z"/></svg>',
}

# ---- 페이지 버튼 (좌상단) ----
nav = st.columns([1.2, 1.2, 5.6])
for col, (path, label, icon) in zip(nav, [("app.py", "서비스 소개", ":material/home:"), ("pages/analysis.py", "채점·분석", ":material/bar_chart:")]):
    try:
        col.page_link(path, label=label, icon=icon)
    except Exception as e:  # 배포 오류가 가려지지 않게 로그를 남긴다
        logging.getLogger(__name__).warning("page_link 실패(%s): %r", path, e)
        col.caption(f"{label} (준비 중)")

# ---- 로고(중앙) + 서비스명 ----
st.write("")
_, mid, _ = st.columns([2, 1, 2])
mid.image(str(Path(__file__).parent / "assets" / "gachon_logo.png"), width="stretch")
st.markdown(
    '<div class="eyebrow">OMR 자동 채점 · AI 성적 분석</div>'
    '<h1 class="hero-title">영어 학원 <span>평가 도우미</span></h1>'
    '<p class="hero-sub">문제지·OMR·정답지를 올리면 채점부터 엑셀 정리, 성적 질문까지 한 번에 끝냅니다.</p>',
    unsafe_allow_html=True,
)
with st.container(key="cta"):
    st.page_link("pages/analysis.py", label="채점 시작하기", icon=":material/arrow_outward:")

# ---- 서비스 소개 (스크롤): 비대칭 벤토 ----
st.markdown(
    '<div class="bento">'
    '<div class="bz big"><div class="core">'
    f'<div class="ico">{_ICO["chat"]}</div><h4>성적 질문 챗봇</h4>'
    '<p>데이터 분석을 몰라도 괜찮아요. 궁금한 걸 그대로 물어보면 채점 결과를 바탕으로 답하고, 많이 틀린 유형의 문제도 새로 만들어 줍니다.</p>'
    '<div class="demo">'
    '<div class="q">가장 성적이 저조한 학생은 누구야?</div>'
    '<div class="a">가장 성적이 저조한 학생은 10번째 909학생으로, 점수는 31점입니다.</div>'
    '<div class="q">가장 많이 틀린 문제와 비슷한 문제 만들어줘</div>'
    '<div class="a">21번(오답 9명)과 같은 유형으로 새 문제를 만들었어요.</div>'
    '</div></div></div>'
    '<div class="bz"><div class="core">'
    f'<div class="ico">{_ICO["grade"]}</div><h4>정답지에서 바로 채점</h4>'
    '<p>정답과 배점을 정답 PDF에서 직접 읽어 채점해요. 시험이 바뀌어도 파일만 올리면 됩니다.</p>'
    '</div></div>'
    '<div class="bz"><div class="core">'
    f'<div class="ico">{_ICO["excel"]}</div><h4>엑셀로 정리</h4>'
    '<p>평균·중앙값·표준편차, 가장 많이 틀린 문항, 학생별 점수와 문항별 정오답을 한 파일로 내려받아요.</p>'
    '</div></div>'
    '</div>'
    '<div class="foot">가천대학교 생성형 AI 활용 부트캠프 최종평가 프로젝트</div>',
    unsafe_allow_html=True,
)
