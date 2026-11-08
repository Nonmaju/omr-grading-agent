"""화면 스타일: 확정 시안 B(다크). 그라데이션·글로우·알약 모양 없이 평평하고 단정하게 간다.

색 값은 .streamlit/config.toml의 [theme]와 맞춰 두었다(기본 위젯이 어두운 색으로 그려지도록).
외부 자원은 폰트(Pretendard, jsDelivr CDN) 하나뿐이며, 로드되지 않으면 시스템 한글 글꼴로 대체된다.
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
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css");
:root {
  --bg:#0B1220; --side:#0F1830; --card:#131E36; --line:#22304F; --text:#E7EEF9; --muted:#8FA2C2;
  --accent:#2DD4BF; --accent-text:#06201C; --user:#1A2A4A; --r:10px;
  --ease:cubic-bezier(0.32,0.72,0,1);
  --font:'Pretendard Variable',Pretendard,'Noto Sans KR','Malgun Gothic',system-ui,sans-serif;
}

/* ---------- 바탕·타이포 ---------- */
html, body, .stApp, .stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
.stApp button, .stApp textarea, .stApp input, .stApp div[data-testid="stMarkdownContainer"] { font-family: var(--font); }
.stApp { background: var(--bg); font-variant-numeric: tabular-nums; }
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div[data-testid="stMarkdownContainer"] { color: var(--text); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 { color: var(--text); font-weight: 700; letter-spacing: -.02em; text-wrap: balance; }
.stApp p { text-wrap: pretty; line-height: 1.65; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stHeader"] * { color: var(--muted); }
[data-testid="stSidebar"] { background: var(--side); border-right: 1px solid var(--line); }
[data-testid="stSidebar"] * { color: var(--text); }

/* ---------- 카드 ---------- */
[data-testid="stVerticalBlockBorderWrapper"] { background: var(--card); border: 1px solid var(--line) !important; border-radius: 12px; }

/* ---------- 버튼 ---------- */
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {
  border-radius: 8px; padding: .55rem 1rem;
  transition: background .25s var(--ease), border-color .25s var(--ease), transform .25s var(--ease);
}
[data-testid="stBaseButton-primary"] { background: var(--accent); border: 1px solid var(--accent); }
[data-testid="stBaseButton-primary"] * { color: var(--accent-text) !important; font-weight: 700; }
[data-testid="stBaseButton-primary"]:hover:not(:disabled) { background: #5EEAD4; border-color: #5EEAD4; }
[data-testid="stBaseButton-secondary"] { background: transparent; border: 1px solid var(--line); }
[data-testid="stBaseButton-secondary"] * { color: var(--text) !important; }
[data-testid="stBaseButton-secondary"]:hover:not(:disabled) { border-color: var(--accent); }
[data-testid="stBaseButton-primary"]:active:not(:disabled), [data-testid="stBaseButton-secondary"]:active:not(:disabled) { transform: scale(.98); }
[data-testid="stBaseButton-primary"]:disabled { background: var(--card); border-color: var(--line); }   /* 비활성: 밝은 글자가 보이게 */
[data-testid="stBaseButton-primary"]:disabled * { color: var(--muted) !important; }
button:disabled { opacity: .6; }
:focus-visible { outline: 2px solid var(--accent) !important; outline-offset: 2px; }
[data-testid="stChatInput"] textarea:focus-visible { outline: none !important; }   /* 입력창 테두리가 이미 포커스를 보여 준다 */

/* ---------- 파일 업로드 ---------- */
[data-testid="stFileUploaderDropzone"] { background: var(--bg); border: 1px dashed var(--line); border-radius: 8px; transition: border-color .25s var(--ease); }
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--accent); }
[data-testid="stFileUploaderDropzone"] * { color: var(--muted) !important; }
[data-testid="stFileUploaderDropzone"] button { background: transparent; border: 1px solid var(--line); border-radius: 6px; }
[data-testid="stFileUploaderDropzone"] button * { color: var(--text) !important; }
[data-testid="stFileChip"] { background: var(--bg) !important; border: 1px solid var(--line); border-radius: 6px; }
[data-testid="stFileChip"] * { color: var(--text) !important; }
[data-testid="stFileChip"] > div:first-child { background: #1B2A4A !important; border-radius: 6px; }   /* 파일 아이콘 칸(기본값이 글자색이라 아이콘이 안 보였음) */
[data-testid="stFileChip"] > div:first-child * { color: var(--accent) !important; }

/* ---------- 채팅 ---------- */
[data-testid="stChatMessage"] { background: transparent; border-radius: 10px; padding: .8rem 1rem; }
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: var(--user); }
[data-testid="stChatMessageAvatarUser"] { background: #2B3C61 !important; border-radius: 8px; }
[data-testid="stChatMessageAvatarAssistant"] { background: var(--accent) !important; border-radius: 8px; }
[data-testid="stChatMessageAvatarUser"] * { color: #fff !important; }
[data-testid="stChatMessageAvatarAssistant"] * { color: var(--accent-text) !important; }
[data-testid="stChatInput"] { background: var(--card); border: 1px solid var(--line) !important; border-radius: 10px; transition: border-color .25s var(--ease); }
[data-testid="stChatInput"]:focus-within { border-color: var(--accent) !important; }
[data-testid="stChatInput"] div { background: transparent !important; }
[data-testid="stChatInput"] textarea { color: var(--text); background: transparent; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted); }
[data-testid="stChatInputSubmitButton"] { background: var(--accent) !important; border-radius: 8px; }
[data-testid="stChatInput"] button, [data-testid="stChatInput"] button * { color: var(--accent-text) !important; }
[data-testid="stBottom"], [data-testid="stBottom"] > div { background: transparent; }
[data-testid="stAlert"] { border-radius: 10px; }
.stApp hr { border-color: var(--line); }
*::-webkit-scrollbar { width: 8px; height: 8px; }
*::-webkit-scrollbar-thumb { background: rgba(255,255,255,.12); border-radius: 8px; }

/* ---------- 페이지 버튼 ---------- */
[data-testid="stPageLink-NavLink"] { border-radius: 8px; transition: background .25s var(--ease); }
[data-testid="stPageLink-NavLink"]:hover { background: rgba(255,255,255,.05); }
[data-testid="stPageLink-NavLink"][aria-current="page"] { background: rgba(45,212,191,.12); }
[data-testid="stPageLink-NavLink"][aria-current="page"] * { color: var(--accent) !important; }

/* ---------- 랜딩 ---------- */
[data-testid="stImage"] img { max-width: 168px; margin: 0 auto; display: block; border-radius: 50%; }
.eyebrow { text-align: center; margin: 1.6rem 0 .7rem; font-size: .8rem; font-weight: 600; letter-spacing: .08em; color: var(--accent); }
.hero-title { text-align: center; font-size: clamp(2.1rem, 5vw, 3.2rem); line-height: 1.15; margin: 0 0 .9rem; }
.hero-title span { color: var(--accent); }
.hero-sub { text-align: center !important; color: var(--muted) !important; max-width: 34rem; margin: 0 auto 1.6rem !important; font-size: 1.04rem; }
.st-key-cta { display: flex; flex-direction: column; align-items: center !important; }
.st-key-cta a { border-radius: 8px; padding: .7rem 1.4rem; background: var(--accent); transition: background .25s var(--ease), transform .25s var(--ease); }
.st-key-cta a:hover { background: #5EEAD4; }
.st-key-cta a:active { transform: scale(.98); }
.st-key-cta a * { color: var(--accent-text) !important; font-weight: 700; }

.bento { display: grid; grid-template-columns: 1.35fr 1fr; gap: 16px; margin: 3.2rem 0 1.5rem; }
.bz { animation: rise .7s var(--ease) both; }
.bz.big { grid-row: span 2; animation-delay: .05s; }
.bz:nth-child(2) { animation-delay: .12s; }
.bz:nth-child(3) { animation-delay: .2s; }
.core { height: 100%; padding: 1.5rem 1.6rem; border-radius: 12px; box-sizing: border-box; background: var(--card); border: 1px solid var(--line); transition: border-color .25s var(--ease); }
.core:hover { border-color: rgba(45,212,191,.45); }
.core .ico { width: 38px; height: 38px; border-radius: 8px; display: grid; place-items: center; margin-bottom: 1rem; color: var(--accent); border: 1px solid var(--line); background: var(--bg); }
.core .ico svg { width: 21px; height: 21px; }
.core h4 { margin: 0 0 .4rem; font-size: 1.12rem; }
.core p { margin: 0; color: var(--muted) !important; font-size: .95rem; }
.demo { margin-top: 1.4rem; display: grid; gap: .5rem; }
.demo div { padding: .65rem .95rem; border-radius: 8px; font-size: .92rem; line-height: 1.5; max-width: 90%; }
.demo .q { justify-self: end; background: var(--user); }
.demo .a { justify-self: start; background: var(--bg); border: 1px solid var(--line); }
.foot { text-align: center; color: var(--muted); font-size: .8rem; padding: 2rem 0 1rem; }

/* ---------- 2페이지 빈 화면(단계 안내) ---------- */
.steps { display: grid; gap: .7rem; max-width: 34rem; margin: 1.4rem auto 0; }
.step { display: flex; gap: .9rem; align-items: center; padding: .9rem 1.1rem; border-radius: 10px; background: var(--bg); border: 1px solid var(--line); animation: rise .7s var(--ease) both; }
.step:nth-child(2) { animation-delay: .08s; } .step:nth-child(3) { animation-delay: .16s; }
.step i { flex: none; width: 30px; height: 30px; border-radius: 8px; display: grid; place-items: center; font-style: normal; font-weight: 700; color: var(--accent); border: 1px solid var(--line); }
.step b { display: block; } .step span { color: var(--muted) !important; font-size: .9rem; }
.empty-title { text-align: center; margin-top: 2.2rem; }
.empty-title small { color: var(--muted); }

@keyframes rise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@media (max-width: 760px) { .bento { grid-template-columns: 1fr; } .bz.big { grid-row: auto; } .demo div { max-width: 100%; } }
@media (prefers-reduced-motion: reduce) { .bz, .step { animation: none; } * { transition: none !important; } }
</style>
"""


def apply(hide_sidebar: bool = False) -> None:
    st.markdown(_BASE + _CSS + (_HIDE_SIDEBAR if hide_sidebar else ""), unsafe_allow_html=True)
