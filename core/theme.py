"""화면 공통 스타일. 레이아웃(와이어프레임)과 세부 디자인(시안)을 분리하기 위해 CSS를 한곳에 둔다.

시안 선택(임시): 주소 끝에 ?theme=A|B|C 를 붙이거나 화면의 '시안' 버튼으로 바꾼다. 선택은 세션에 유지된다.
최종 시안이 정해지면 DEFAULT만 남기고 나머지와 picker()는 지운다.
"""
import streamlit as st

DEFAULT = "A"

# 시안별 색·모양 값. 아래 템플릿(_css)이 이 값으로 모든 요소를 칠한다.
THEMES = {
    "A": dict(  # 가천 블루: 깔끔한 대학 서비스 느낌
        name="가천 블루", bg="#F4F8FD", side="#FFFFFF", card="#FFFFFF", line="#D6E2F2", text="#0E2342", muted="#5B6F8C",
        accent="#0B5DAE", accent_text="#FFFFFF", user="#E6F0FB", radius="14px", shadow="0 2px 10px rgba(11,93,174,.08)",
        font="'Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif", head_font="inherit", head_weight="800",
        logo="190px", hero_gap="2.2rem"),
    "B": dict(  # 다크 대시보드: 어두운 배경, 청록 포인트
        name="다크 대시보드", bg="#0B1220", side="#101A2E", card="#131E36", line="#243455", text="#E7EEF9", muted="#8FA2C2",
        accent="#2DD4BF", accent_text="#06201C", user="#1A2A4A", radius="10px", shadow="none",
        font="'Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif", head_font="inherit", head_weight="700",
        logo="170px", hero_gap="2.6rem"),
    "C": dict(  # 웜 에디토리얼: 따뜻한 종이 느낌, 세리프 제목, 테라코타 포인트
        name="웜 에디토리얼", bg="#FBF6EC", side="#F3EAD9", card="#FFFDF8", line="#DCCDB3", text="#2A2018", muted="#7A6A55",
        accent="#C8552B", accent_text="#FFFFFF", user="#F4E6CF", radius="4px", shadow="none",
        font="'Pretendard','Noto Sans KR','Malgun Gothic',system-ui,sans-serif",
        head_font="'Noto Serif KR','Nanum Myeongjo',Georgia,'Times New Roman',serif", head_weight="700",
        logo="150px", hero_gap="1.6rem"),
}

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


def _css(v: dict) -> str:
    return f"""
<style>
:root {{ --bg:{v['bg']}; --side:{v['side']}; --card:{v['card']}; --line:{v['line']}; --text:{v['text']}; --muted:{v['muted']};
        --accent:{v['accent']}; --accent-text:{v['accent_text']}; --user:{v['user']}; --r:{v['radius']}; }}
.stApp {{ background: var(--bg); font-family: {v['font']}; }}
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div[data-testid="stMarkdownContainer"] {{ color: var(--text); }}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{ color: var(--text); font-family: {v['head_font']}; font-weight: {v['head_weight']}; letter-spacing: -.01em; }}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {{ color: var(--muted) !important; }}
[data-testid="stHeader"] {{ background: transparent; }}
[data-testid="stHeader"] * {{ color: var(--muted); }}
[data-testid="stSidebar"] {{ background: var(--side); border-right: 1px solid var(--line); }}
[data-testid="stSidebar"] * {{ color: var(--text); }}

/* 카드(테두리 컨테이너: 업로드 박스, 채팅 내역) */
[data-testid="stVerticalBlockBorderWrapper"] {{ background: var(--card); border: 1px solid var(--line) !important; border-radius: var(--r); box-shadow: {v['shadow']}; }}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{ box-shadow: none; }}

/* 버튼 */
[data-testid="stBaseButton-primary"] {{ background: var(--accent); border: 1px solid var(--accent); border-radius: var(--r); }}
[data-testid="stBaseButton-primary"] * {{ color: var(--accent-text) !important; font-weight: 700; }}
[data-testid="stBaseButton-primary"]:hover {{ filter: brightness(1.08); }}
[data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-secondaryFormSubmit"] {{ background: var(--card); border: 1px solid var(--line); border-radius: var(--r); }}
[data-testid="stBaseButton-secondary"] * {{ color: var(--text) !important; }}
button:disabled {{ opacity: .45; }}

/* 파일 업로드 */
[data-testid="stFileUploaderDropzone"] {{ background: var(--bg); border: 1.5px dashed var(--line); border-radius: var(--r); }}
[data-testid="stFileUploaderDropzone"] * {{ color: var(--muted) !important; }}
[data-testid="stFileUploaderDropzone"] button {{ background: var(--card); border: 1px solid var(--line); }}
[data-testid="stFileUploaderDropzone"] button * {{ color: var(--text) !important; }}
[data-testid="stFileUploaderFile"] {{ background: var(--card); border-radius: var(--r); }}

/* 채팅 */
[data-testid="stChatMessage"] {{ background: transparent; border-radius: var(--r); }}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{ background: var(--user); }}
[data-testid="stChatInput"] {{ background: var(--card); border: 1px solid var(--line) !important; border-radius: var(--r); box-shadow: {v['shadow']}; }}
[data-testid="stChatInput"]:focus-within {{ border-color: var(--accent) !important; }}
[data-testid="stChatInput"] textarea {{ color: var(--text); background: transparent; }}
[data-testid="stChatInput"] textarea::placeholder {{ color: var(--muted); }}
[data-testid="stChatInput"] button {{ background: var(--accent); }}
[data-testid="stChatInput"] button, [data-testid="stChatInput"] button * {{ color: var(--accent-text) !important; }}
[data-testid="stBottom"], [data-testid="stBottom"] > div {{ background: transparent; }}
[data-testid="stAlert"] {{ border-radius: var(--r); }}
.stApp hr {{ border-color: var(--line); }}

/* Streamlit이 내부 요소에 따로 주는 밝은 배경을 시안 색으로 덮어쓴다 */
[data-testid="stChatInput"] div {{ background: transparent !important; }}
[data-testid="stChatInputSubmitButton"] {{ background: var(--accent) !important; border-radius: var(--r); }}
[data-testid="stFileChip"] {{ background: var(--bg) !important; border: 1px solid var(--line); border-radius: var(--r); }}
[data-testid="stFileChip"] * {{ color: var(--text) !important; }}
[data-testid="stButtonGroup"] button {{ background: var(--card) !important; border: 1px solid var(--line); border-radius: var(--r); }}
[data-testid="stButtonGroup"] button * {{ color: var(--text) !important; }}
[data-testid="stButtonGroup"] button[aria-checked="true"] {{ background: var(--accent) !important; border-color: var(--accent); }}
[data-testid="stButtonGroup"] button[aria-checked="true"] * {{ color: var(--accent-text) !important; font-weight: 700; }}

/* 페이지 버튼 */
[data-testid="stPageLink-NavLink"] {{ border-radius: var(--r); }}
[data-testid="stPageLink-NavLink"][aria-current="page"] {{ background: var(--user); }}

/* 랜딩 */
[data-testid="stImage"] img {{ max-width: {v['logo']}; margin: 0 auto; display: block; }}
.hero-gap {{ height: {v['hero_gap']}; }}
</style>
"""


def apply(hide_sidebar: bool = False) -> str:
    qp = st.query_params.get("theme")
    if qp in THEMES:
        st.session_state["theme"] = qp  # 다른 페이지로 이동해도 유지(쿼리스트링은 이동 시 사라지므로 세션에 저장)
    name = st.session_state.get("theme", DEFAULT)
    st.markdown(_BASE + _css(THEMES[name]) + (_HIDE_SIDEBAR if hide_sidebar else ""), unsafe_allow_html=True)
    return name


def picker() -> None:
    """시안 선택(임시). 최종 시안 확정 후 제거."""
    cur = st.session_state.get("theme", DEFAULT)
    sel = st.segmented_control("시안", list(THEMES), default=cur, key="_theme_pick",
                               format_func=lambda k: f"{k} · {THEMES[k]['name']}", selection_mode="single")
    if sel and sel != cur:
        st.session_state["theme"] = sel
        st.rerun()
