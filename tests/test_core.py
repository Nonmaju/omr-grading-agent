import io
import re
from pathlib import Path

import openpyxl
import pandas as pd

from core.answer_key import parse_answer_pdf
from core.export import to_excel
from core.grading import find_student, grade, hardest, lowest_students, summary
from core.problems import parse_problems_pdf

ROOT = Path(__file__).resolve().parent.parent
ANS = ROOT / "samples" / "2026학년도-대학수학능력시험-영어-정답.pdf"
PROB = ROOT / "samples" / "2026학년도-대학수학능력시험-영어-문제.pdf"
OMR = ROOT / "samples" / "sample_data.xlsx"


def test_answer_key():
    key = parse_answer_pdf(ANS)
    assert len(key) == 45 and sum(p for _, p in key.values()) == 100
    assert key[1] == (3, 2) and key[30] == (5, 3) and key[45] == (5, 2)


def test_problems_split():
    p = parse_problems_pdf(PROB)
    assert sorted(p) == list(range(1, 46)) and p[8].startswith("8.")


def test_grade_matches_manual():
    key = parse_answer_pdf(ANS)
    r = grade(OMR, key)
    ws = openpyxl.load_workbook(OMR).active
    rows = list(ws.iter_rows(values_only=True))
    name, *ans = rows[1]  # 첫 학생을 손으로(루프로) 채점
    manual = sum(key[q][1] for q in range(1, 46) if ans[q - 1] == key[q][0])
    assert r.scores[name] == manual
    assert len(r.names) == 10 and 0 <= r.scores.min() <= r.scores.max() <= 100


def test_stats_and_lookup():
    r = grade(OMR, parse_answer_pdf(ANS))
    s = summary(r)
    assert s["평균"] == round(r.scores.mean(), 2) and s["중앙값"] == r.scores.median()
    assert len(hardest(r, 3)) == 3
    assert all(sc == r.scores.min() for _, _, sc in lowest_students(r))
    assert find_student(r, 905)[1] == "905학생"      # 학생명 숫자 일치
    assert find_student(r, 3)[1] == r.names[2]        # 없으면 N번째
    assert find_student(r, 87) is None


def test_excel():
    r = grade(OMR, parse_answer_pdf(ANS))
    wb = openpyxl.load_workbook(io.BytesIO(to_excel(r)))
    assert wb.sheetnames[0] == "전체 학생 성적 개요" and len(wb.sheetnames) == 2 + 10
    assert "10번 학생 점수 및 각 문제별 정답 여부" in wb.sheetnames


def _omr(rows, cols):
    buf = io.BytesIO()
    pd.DataFrame(rows, columns=["학생명", *cols]).to_excel(buf, index=False)
    buf.seek(0)
    return buf


def test_robust_omr_input():
    key = {1: (3, 2), 2: (1, 3)}
    # 열 이름 변형(q01, 2번), 원문자 마킹(③), 빈칸, 중복 학생명
    r = grade(_omr([["홍길동", "③", 1], ["홍길동", 3, None]], ["q01", "2번"]), key)
    assert r.names == ["홍길동", "홍길동(2)"]
    assert list(r.scores) == [5, 2]
    assert len(to_excel(r)) > 0  # 중복 이름에서도 엑셀 생성이 터지지 않음


def test_missing_columns_listed_sorted():
    try:
        grade(_omr([["a", 1]], ["Q01"]), {1: (1, 2), 3: (1, 2), 2: (1, 2)})
    except ValueError as e:
        assert "[2, 3]" in str(e)
    else:
        raise AssertionError("누락 문항 오류가 나야 함")


def test_excel_sheet_order():
    r = grade(OMR, parse_answer_pdf(ANS))
    names = openpyxl.load_workbook(io.BytesIO(to_excel(r))).sheetnames
    assert names[0] == "전체 학생 성적 개요" and names[1].startswith("1번 학생") and names[-1] == "전체 학생 결과"
