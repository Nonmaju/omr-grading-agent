"""OMR 엑셀 + 정답 → 채점 결과와 통계. 모든 숫자는 여기서 pandas로 계산한다(LLM은 계산하지 않음)."""
import re
from dataclasses import dataclass

import pandas as pd

_QCOL = re.compile(r"(?:Q|문항)?\s*0*(\d+)\s*번?", re.I)   # Q01, q1, 1, 1번, 문항1 모두 허용
_NAME_HINT = re.compile(r"학생|이름|성명|name", re.I)


@dataclass
class Result:
    names: list[str]            # 데이터 순서의 학생명
    marked: pd.DataFrame        # 학생 × 문항 제출 답 (index=학생명, columns=문항번호 int)
    correct: pd.DataFrame       # 학생 × 문항 정오(bool)
    scores: pd.Series           # 학생별 점수
    key: dict[int, tuple[int, int]]  # 문항 -> (정답, 배점)
    blank: int = 0              # 빈칸 수(오답 처리)
    invalid: int = 0            # 인식할 수 없는 값 수(1~5 밖의 값, 문자 등; 오답 처리)


def _qcols(df: pd.DataFrame) -> dict[int, object]:
    return {int(m.group(1)): c for c in df.columns if (m := _QCOL.fullmatch(str(c).strip()))}


def _clean_name(n, i: int) -> str:
    """학생명을 한 줄·40자로 정리한다(엑셀 시트/LLM 입력에 긴 문자열이나 줄바꿈이 들어가는 것을 막음)."""
    s = re.sub(r"\s+", " ", str(n)).strip()[:40]
    return s if s and s.lower() != "nan" else f"학생{i}"


def grade(omr_file, key) -> Result:
    sheets = pd.read_excel(omr_file, sheet_name=None)  # 시트가 여러 개면 문항 열이 가장 많은 시트를 쓴다
    df = max(sheets.values(), key=lambda d: len(_qcols(d)))
    qcols = _qcols(df)
    missing = sorted(q for q in key if q not in qcols)
    if missing:
        raise ValueError(f"OMR 파일에 없는 문항: {missing}")
    others = [c for c in df.columns if c not in qcols.values()]  # 첫 열이 '번호'여도 '학생명/이름' 열을 우선 사용
    name_col = next((c for c in others if _NAME_HINT.search(str(c))), others[0] if others else df.columns[0])
    qs = sorted(key)
    seen: dict[str, int] = {}
    names = []
    for i, n in enumerate(df[name_col], 1):  # 학생명이 중복이면 '이름(2)'처럼 구분한다(인덱스 중복으로 인한 오류 방지)
        n = _clean_name(n, i)
        seen[n] = seen.get(n, 0) + 1
        names.append(n if seen[n] == 1 else f"{n}({seen[n]})")
    raw = df[[qcols[q] for q in qs]].set_axis(qs, axis=1).set_axis(names, axis=0)
    raw = raw.replace({"①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5})
    marked = raw.apply(pd.to_numeric, errors="coerce")  # 빈칸/이상값은 NaN → 오답
    blank = int(raw.isna().sum().sum())
    invalid = int((marked.isna() & raw.notna()).sum().sum() + (marked.notna() & ~marked.isin(range(1, 6))).sum().sum())
    answers = pd.Series({q: key[q][0] for q in qs})
    points = pd.Series({q: key[q][1] for q in qs})
    correct = marked.eq(answers, axis=1)
    return Result(list(marked.index), marked, correct, (correct * points).sum(axis=1), key, blank, invalid)


def summary(r: Result) -> dict:
    s = r.scores
    return {"학생 수": len(s), "평균": round(float(s.mean()), 2), "중앙값": float(s.median()),
            "표준편차(표본)": round(float(s.std()), 2), "최고점": float(s.max()), "최저점": float(s.min())}


def wrong_counts(r: Result) -> pd.DataFrame:
    """문항별 오답 수. 정렬: 오답 많은 순 → 배점 높은 순 → 문항 번호 순."""
    wc = (~r.correct).sum()
    df = pd.DataFrame({"문항": wc.index, "오답 수": wc.values, "배점": [r.key[q][1] for q in wc.index],
                       "정답": [r.key[q][0] for q in wc.index]})
    return df.sort_values(["오답 수", "배점", "문항"], ascending=[False, False, True]).reset_index(drop=True)


def hardest(r: Result, n: int = 3) -> pd.DataFrame:
    return wrong_counts(r).head(n)


def top_ties(r: Result, n: int = 3) -> list[int]:
    """TOP n 밖에 있지만 n위와 오답 수가 같은 문항 번호(경계 동점 표시용)."""
    wc = wrong_counts(r)
    if len(wc) <= n:
        return []
    edge = wc.iloc[n - 1]["오답 수"]
    return [int(q) for q in wc.iloc[n:][wc.iloc[n:]["오답 수"] == edge]["문항"]]


def lowest_students(r: Result) -> list[tuple[int, str, float]]:
    """최저점 학생(동점이면 모두): (순번, 학생명, 점수)."""
    low = r.scores.min()
    return [(i + 1, n, float(s)) for i, (n, s) in enumerate(r.scores.items()) if s == low]


def find_student(r: Result, num: int) -> tuple[int, str, float] | None:
    """'N번 학생' 해석: ① 학생명 속 숫자가 N인 학생 ② 없으면 데이터 순서의 N번째."""
    for i, n in enumerate(r.names):
        if re.search(rf"(?<!\d){num}(?!\d)", n):
            return i + 1, n, float(r.scores[n])
    if 1 <= num <= len(r.names):
        n = r.names[num - 1]
        return num, n, float(r.scores[n])
    return None
