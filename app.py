"""페이지 1: 서비스 소개(랜딩).

와이어프레임(README.pdf 6쪽): 좌상단 '페이지 버튼' / 화면 중앙 '가천대 로고' / 그 아래 서비스명.
첫 화면은 와이어프레임 그대로 두고, 서비스 소개는 아래로 스크롤하면 나온다.
"""
from pathlib import Path

import streamlit as st

from core import theme

st.set_page_config(page_title="영어 학원 평가 도우미", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
theme.apply(hide_sidebar=True)

# ---- 페이지 버튼 (좌상단) ----
nav = st.columns([1.2, 1.2, 1.6, 4])
nav[0].page_link("app.py", label="서비스 소개", icon="🏠")
nav[1].page_link("pages/analysis.py", label="채점·분석", icon="📊")
with nav[3]:
    theme.picker()  # 시안 선택(임시)

# ---- 로고(중앙) + 서비스명 ----
st.write("")
_, mid, _ = st.columns([2, 1, 2])
mid.image(str(Path(__file__).parent / "assets" / "gachon_logo.png"), width="stretch")
st.markdown("<h1 style='text-align:center'>영어 학원 평가 도우미</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;opacity:.7'>OMR 자동 채점 · 성적 분석 · 질문 챗봇</p>", unsafe_allow_html=True)

# ---- 서비스 소개 (스크롤) ----
st.write("")
st.divider()
c = st.columns(3)
c[0].markdown("#### ✅ 자동 채점\n문제지·OMR·정답 PDF를 올리면 정답과 배점을 PDF에서 읽어 채점합니다.")
c[1].markdown("#### 📥 엑셀 추출\n전체 성적 개요와 학생별 점수·문항별 정오답을 엑셀로 내려받습니다.")
c[2].markdown("#### 💬 성적 챗봇\n평균, 최저 학생, 많이 틀린 문항을 묻고 유사 문제도 만들어 달라고 할 수 있습니다.")
st.caption("가천대학교 생성형 AI 활용 부트캠프 최종평가 프로젝트")
