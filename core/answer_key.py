"""정답 PDF → {문항번호: (정답, 배점)}. 정답/배점은 항상 업로드된 PDF에서 읽는다(하드코딩 금지)."""
import re

import pdfplumber

CIRCLED = "①②③④⑤"


def parse_answer_pdf(file) -> dict[int, tuple[int, int]]:
    with pdfplumber.open(file) as pdf:
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)
    key: dict[int, tuple[int, int]] = {}
    for n, a, s in re.findall(r"(\d{1,2})\s*([①-⑤])\s*(\d)", text):
        key.setdefault(int(n), (CIRCLED.index(a) + 1, int(s)))  # 홀수형/짝수형이 함께 있으면 먼저 나온 표(첫 쪽)를 쓴다
    if not key or sorted(key) != list(range(1, max(key) + 1)):
        raise ValueError(f"정답표를 읽지 못했습니다(추출된 문항: {sorted(key)}). 정답 PDF가 맞는지 확인해 주세요.")
    return key
