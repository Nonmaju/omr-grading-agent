from core.chat import _student_number


def test_student_number_followup():
    hist = [{"role": "user", "content": "가장 성적이 저조한 학생은?"},
            {"role": "assistant", "content": "가장 성적이 저조한 학생은 10번째 909학생으로, 점수는 31점입니다."}]
    assert _student_number("그 학생 몇 점이야?", hist) == 10   # 직전 답변에서 찾기
    assert _student_number("87번 학생 몇 점이야?", hist) == 87  # 현재 질문 우선
    assert _student_number("그 학생 몇 점이야?", []) is None
