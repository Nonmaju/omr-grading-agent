"""화면 공통 스타일. 레이아웃(와이어프레임)과 세부 디자인(시안)을 분리하기 위해 CSS를 한곳에 둔다."""
import streamlit as st

_BASE = """
<style>
[data-testid="stSidebarNav"] {display: none;}            /* 기본 페이지 목록 대신 직접 만든 페이지 버튼을 쓴다 */
</style>
"""
_HIDE_SIDEBAR = """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"] {display: none;}  /* 1페이지는 사이드바 없음 */
</style>
"""


def apply(hide_sidebar: bool = False) -> None:
    st.markdown(_BASE + (_HIDE_SIDEBAR if hide_sidebar else ""), unsafe_allow_html=True)
