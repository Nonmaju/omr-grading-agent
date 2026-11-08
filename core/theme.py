"""화면 스타일: 확정 시안 B(다크 대시보드). 레이아웃은 와이어프레임 그대로 두고 색·모양만 여기서 바꾼다.

색 값은 .streamlit/config.toml의 [theme]와 맞춰 두었다(기본 위젯이 어두운 색으로 그려지도록).
"""
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
_CSS = """
<style>
:root { --bg:#0B1220; --side:#101A2E; --card:#131E36; --line:#243455; --text:#E7EEF9; --muted:#8FA2C2;
        --accent:#2DD4BF; --accent-text:#06201C; --user:#1A2A4A; --r:10px; }
.stApp { background: var(--bg); font-family: 'Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif; }
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 { color: var(--text); font-family: inherit; font-weight: 700; letter-spacing: -.01em; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] * { color: var(--muted); }
[data-testid="stSidebar"] { background: var(--side); border-right: 1px solid var(--line); }
[data-testid="stSidebar"] * { color: var(--text); }

/* 카드(테두리 컨테이너: 업로드 박스, 채팅 내역) */
[data-testid="stVerticalBlockBorderWrapper"] { background: var(--card); border: 1px solid var(--line) !important; border-radius: var(--r); box-shadow: none; }
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] { box-shadow: none; }

/* 버튼 */
[data-testid="stBaseButton-primary"] { background: var(--accent); border: 1px solid var(--accent); border-radius: var(--r); }
[data-testid="stBaseButton-primary"] * { color: var(--accent-text) !important; font-weight: 700; }
[data-testid="stBaseButton-primary"]:hover { filter: brightness(1.08); }
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] { background: var(--card); border: 1px solid var(--line); border-radius: var(--r); }
[data-testid="stBaseButton-secondary"] * { color: var(--text) !important; }
button:disabled { opacity: .45; }

/* 파일 업로드 */
[data-testid="stFileUploaderDropzone"] { background: var(--bg); border: 1.5px dashed var(--line); border-radius: var(--r); }
[data-testid="stFileUploaderDropzone"] * { color: var(--muted) !important; }
[data-testid="stFileUploaderDropzone"] button { background: var(--card); border: 1px solid var(--line); }
[data-testid="stFileUploaderDropzone"] button * { color: var(--text) !important; }
[data-testid="stFileUploaderFile"] { background: var(--card); border-radius: var(--r); }

/* 채팅 */
[data-testid="stChatMessage"] { background: transparent; border-radius: var(--r); }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: var(--user); }
[data-testid="stChatInput"] { background: var(--card); border: 1px solid var(--line) !important; border-radius: var(--r); box-shadow: none; }
[data-testid="stChatInput"]:focus-within { border-color: var(--accent) !important; }
[data-testid="stChatInput"] textarea { color: var(--text); background: transparent; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted); }
[data-testid="stChatInput"] button { background: var(--accent); }
[data-testid="stChatInput"] button, [data-testid="stChatInput"] button * { color: var(--accent-text) !important; }
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: transparent; }
[data-testid="stAlert"] { border-radius: var(--r); }
.stApp hr { border-color: var(--line); }

/* Streamlit이 내부 요소에 따로 주는 밝은 배경을 시안 색으로 덮어쓴다 */
[data-testid="stChatInput"] div { background: transparent !important; }
[data-testid="stChatInputSubmitButton"] { background: var(--accent) !important; border-radius: var(--r); }
[data-testid="stFileChip"] { background: var(--bg) !important; border: 1px solid var(--line); border-radius: var(--r); }
[data-testid="stFileChip"] * { color: var(--text) !important; }
[data-testid="stButtonGroup"] button { background: var(--card) !important; border: 1px solid var(--line); border-radius: var(--r); }
[data-testid="stButtonGroup"] button * { color: var(--text) !important; }
[data-testid="stButtonGroup"] button[aria-checked="true"] { background: var(--accent) !important; border-color: var(--accent); }
[data-testid="stButtonGroup"] button[aria-checked="true"] * { color: var(--accent-text) !important; font-weight: 700; }

/* 페이지 버튼 */
[data-testid="stPageLink-NavLink"] { border-radius: var(--r); }
[data-testid="stPageLink-NavLink"][aria-current="page"] { background: var(--user); }

/* 랜딩 */
[data-testid="stImage"] img { max-width: 170px; margin: 0 auto; display: block; }
.hero-gap { height: 2.6rem; }
</style>
"""


def apply(hide_sidebar: bool = False) -> None:
    st.markdown(_BASE + _CSS + (_HIDE_SIDEBAR if hide_sidebar else ""), unsafe_allow_html=True)
