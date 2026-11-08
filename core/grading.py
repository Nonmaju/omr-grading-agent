"""OMR 엑셀 + 정답 → 채점 결과와 통계. 모든 숫자는 여기서 pandas로 계산한다(LLM은 계산하지 않음)."""
import re
from dataclasses import dataclass

import pandas as pd


@dataclass
class Result:
    names: list[str]            # 데이터 순서의 학생명
    marked: pd.DataFrame        # 학생 × 문항 제출 답 (index=학생명, columns=문항번호 int)
    correct: pd.DataFrame       # 학생 × 문항 정오(bool)
    scores: pd.Series           # 학생별 점수
    key: dict[int, tuple[int, int]]  # 문항 -> (정답, 배점)


def grade(omr_file, key) -> Result:
    df = pd.read_excel(omr_file)
    name_col = df.columns[0]
    qcols = {int(m.group(1)): c for c in df.columns[1:] if (m := re.fullmatch(r"Q(\d+)", str(c).strip()))}
    missing = [q for q in key if q not in qcols]
    if missing:
        raise ValueError(f"OMR 파일에 없는 문항: {missing}")
    qs = sorted(key)
    marked = df[[qcols[q] for q in qs]].set_axis(qs, axis=1).set_axis(df[name_col].astype(str), axis=0)
    marked = marked.apply(pd.to_numeric, errors="coerce")  # 빈칸/이상값은 NaN → 오답
    answers = pd.Series({q: key[q][0] for q in qs})
    points = pd.Series({q: key[q][1] for q in qs})
    correct = marked.eq(answers, axis=1)
    return Result(list(marked.index), marked, correct, (correct * points).sum(axis=1), key)


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
