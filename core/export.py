"""채점 결과 → 엑셀 bytes (개요 시트 + 전체 결과 시트 + 학생별 시트)."""
import io

import pandas as pd

from core.grading import Result, hardest, summary, top_ties


def to_excel(r: Result) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as w:
        # 1) 전체 학생 성적 개요
        s = summary(r)
        ov = pd.DataFrame({"항목": list(s), "값": list(s.values())})
        ov.to_excel(w, sheet_name="전체 학생 성적 개요", index=False)
        top = hardest(r, 3).rename(columns={"문항": "가장 많이 틀린 문항 번호"})
        top.insert(0, "순위", range(1, len(top) + 1))
        top.to_excel(w, sheet_name="전체 학생 성적 개요", index=False, startrow=len(ov) + 2)
        ws = w.sheets["전체 학생 성적 개요"]
        ws.set_column(0, 4, 22)
        note = len(ov) + 2 + len(top) + 2
        if ties := top_ties(r, 3):  # 3위와 오답 수가 같은 문항이 더 있으면 알려 준다(정렬 기준: 오답 수 → 배점 → 문항 번호)
            ws.write(note, 0, f"※ 3위와 오답 수가 같은 문항: {', '.join(map(str, ties))}번")
            note += 1
        if r.blank or r.invalid:
            ws.write(note, 0, f"※ OMR 빈칸 {r.blank}칸, 인식할 수 없는 값 {r.invalid}칸은 오답으로 처리했습니다.")

        # 3) 학생별 시트: N번 학생 점수 및 각 문제별 정답 여부
        for i, name in enumerate(r.names, 1):
            d = pd.DataFrame({
                "문항": r.correct.columns,
                "제출 답": r.marked.loc[name].values,
                "정답": [r.key[q][0] for q in r.correct.columns],
                "배점": [r.key[q][1] for q in r.correct.columns],
                "정답 여부": ["O" if b else "X" for b in r.correct.loc[name]],
            })
            sheet = f"{i}번 학생 점수 및 각 문제별 정답 여부"
            pd.DataFrame({"학생명": [name], "점수": [r.scores[name]]}).to_excel(w, sheet_name=sheet, index=False)
            d.to_excel(w, sheet_name=sheet, index=False, startrow=3)
            w.sheets[sheet].set_column(0, 4, 12)

        # 2) 전체 학생 결과 (한눈에 보기) — 요구 그림의 시트 순서를 지키려고 맨 뒤에 둔다
        allr = r.correct.map(lambda b: "O" if b else "X")
        allr.columns = [f"Q{q:02d}" for q in allr.columns]
        allr.insert(0, "점수", r.scores)
        allr = allr.reset_index(names="학생명")
        allr.insert(0, "번호", range(1, len(allr) + 1))  # 학생별 시트의 'N번'과 같은 데이터 순서
        allr.to_excel(w, sheet_name="전체 학생 결과", index=False)
        w.sheets["전체 학생 결과"].set_column(0, 1, 14)
    return buf.getvalue()
