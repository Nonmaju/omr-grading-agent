"""문제지 PDF → {문항번호: 본문 텍스트}. 2단 편집이라 페이지를 좌/우로 잘라 읽고, 문항 번호 순서대로 분할한다."""
import re

import pdfplumber


def parse_problems_pdf(file, max_q: int = 45) -> dict[int, str]:
    lines: list[str] = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            w, h = page.width, page.height
            for box in ((0, 0, w / 2, h), (w / 2, 0, w, h)):  # 왼쪽 단 → 오른쪽 단
                lines += (page.crop(box).extract_text() or "").splitlines()
    out: dict[int, list[str]] = {}
    cur = 0
    for ln in lines:
        m = re.match(rf"\s*{cur + 1}\s*\.(\s|$)", ln)  # 다음에 올 번호만 시작으로 인정(본문 속 숫자 오탐 방지)
        if m and cur < max_q:
            cur += 1
            out[cur] = []
        if cur:
            out[cur].append(ln)
    return {q: "\n".join(v).strip() for q, v in out.items()}
