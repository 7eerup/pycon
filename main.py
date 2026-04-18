import json
import os

# ============= 입력 검증 함수 =============

def get_integer_input(prompt, min_value, max_value):
    """정수 입력을 받고 검증하는 함수"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input:
                print("오류: 입력이 비어있습니다. 다시 입력하세요.")
                continue
            
            try:
                value = int(user_input)
            except ValueError:
                print(f"오류: 숫자를 입력하세요. (입력값: '{user_input}')")
                continue
            
            if value < min_value or value > max_value:
                print(f"오류: {min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                continue
            
            return value
        
        except (KeyboardInterrupt, EOFError):
            return None


def get_string_input(prompt, allow_empty=False):
    """문자열 입력을 받고 검증하는 함수"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and not allow_empty:
                print("오류: 입력이 비어있습니다. 다시 입력하세요.")
                continue
            
            return user_input
        
        except (KeyboardInterrupt, EOFError):
            return None


# ============= 메뉴 함수 =============

def display_menu():
    """메뉴를 출력하는 함수"""
    print("\n" + "="*40)
    print("퀴즈 프로그램에 오신 것을 환영합니다!")
    print("="*40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("="*40)


def get_menu_choice():
    """메뉴 선택을 받는 함수"""
    while True:
        try:
            choice = input("원하는 기능을 선택하세요 (1-5): ").strip()
            
            if not choice:
                print("오류: 입력이 비어있습니다. 다시 입력하세요.")
                continue
            
            if choice not in ['1', '2', '3', '4', '5']:
                print("오류: 1부터 5 사이의 숫자를 입력하세요.")
                continue
            
            return choice
        
        except (KeyboardInterrupt, EOFError):
            return None


# ============= Quiz 클래스 =============

class Quiz:
    """개별 퀴즈를 표현하는 클래스"""
    def __init__(self, question, choices, answer, qid=None):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어있을 수 없습니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 정확히 4개여야 합니다.")
        if not isinstance(answer, int) or not (1 <= answer <= 4):
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        self.id = qid
        self.question = question.strip()
        self.choices = [c.strip() for c in choices]
        self.answer = answer

    def display(self):
        """문제와 선택지를 출력"""
        print(f"\n[문제] {self.question}")
        for i, ch in enumerate(self.choices, start=1):
            print(f"  {i}) {ch}")

    def is_correct(self, user_choice):
        """사용자 선택이 정답인지 확인"""
        return user_choice == self.answer

    def get_correct_text(self):
        """정답 텍스트 반환"""
        return self.choices[self.answer - 1]
    
    def summary(self):
        """퀴즈 목록용 한 줄 출력"""
        return f"id={self.id}: {self.question}"

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["question"], d["choices"], d["answer"], d.get("id"))


# ============= 기본 퀴즈 데이터 =============

def get_default_quizzes():
    """기본 퀴즈 데이터를 반환합니다."""
    return [
        Quiz("파이썬의 창시자는?", ["귀도 반 로섐", "라이너스 토르발즈", "데니스 리치", "비야네 스트롭스트룹"], 1, 1),
        Quiz("파이썬이 처음 출시된 연도는?", ["1989년", "1991년", "1995년", "2000년"], 2, 2),
        Quiz("파이썬의 특징이 아닌 것은?", ["동적 타입", "인터프리터 언어", "컴파일 필수", "간단한 문법"], 3, 3),
        Quiz("리스트 인덱스 시작 값은?", ["0", "1", "-1", "없음"], 1, 4),
        Quiz("함수 정의 키워드는?", ["func", "define", "def", "function"], 3, 5)
    ]


# ============= 데이터 관리 =============

def load_quiz_data(filename="data.json"):
    try:
        if not os.path.exists(filename):
            quizzes = get_default_quizzes()
            save_quiz_data(quizzes, filename)
            return quizzes
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Quiz.from_dict(q) for q in data]
    
    except Exception:
        return get_default_quizzes()


def save_quiz_data(quizzes, filename="data.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([q.to_dict() for q in quizzes], f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# ============= 점수 관리 함수 =============

def load_score(filename="score.json"):
    """점수 데이터 로드"""
    try:
        if not os.path.exists(filename):
            return {"best": None, "last": None}
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                "best": data.get("best_score"),
                "last": data.get("last_score")
            }
    except Exception:
        return {"best": None, "last": None}


def save_score(best, last, filename="score.json"):
    """최고 점수를 저장하는 함수"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"best_score": best, "last_score": last}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 점수 저장 실패: {e}")

# ============= 기능 구현 =============

def solve_quiz(quizzes):
    if not quizzes:
        print("\n⚠️ 퀴즈가 없습니다.")
        return None

    score = 0

    for quiz in quizzes:
        quiz.display()
        choice = get_integer_input("답: ", 1, 4)

        if choice is None:
            return None

        if quiz.is_correct(choice):
            print("정답!")
            score += 1
        else:
            print(f"오답! 정답: {quiz.get_correct_text()}")

    print(f"\n점수: {score}/{len(quizzes)}")
    return score

def add_quiz(quizzes, filename="data.json"):
    """퀴즈를 추가하고 파일에 저장하는 함수"""
    print("\n=== 퀴즈 추가 ===")

    question = get_string_input("문제 내용을 입력하세요: ")
    if question is None:
        print("입력 취소")
        return

    choices = []
    for i in range(1, 5):
        choice = get_string_input(f"선택지 {i}: ")
        if choice is None or not choice.strip():
            print("선택지는 비어 있을 수 없습니다.")
            return
        choices.append(choice)

    answer = get_integer_input("정답 번호 (1-4): ", 1, 4)
    if answer is None:
        print("입력 취소")
        return

    new_id = max([q.id for q in quizzes if hasattr(q, 'id')], default=0) + 1

    quiz = Quiz(question, choices, answer, new_id)

    quizzes.append(quiz)
    save_quiz_data(quizzes, filename)

    print(f"✅ 퀴즈 추가 완료 (id={new_id})")

def show_quizzes(quizzes):
    """저장된 퀴즈 목록을 출력하는 함수"""
    print("\n=== 퀴즈 목록 ===")

    if not quizzes:
        print("⚠️ 등록된 퀴즈가 없습니다.")
        return

    for quiz in quizzes:
        print(quiz.summary())

def show_scores(score_data):
    """점수 출력"""
    print("\n=== 점수 정보 ===")

    best = score_data["best"]
    last = score_data["last"]

    if last is None:
        print("⚠️ 아직 퀴즈를 풀지 않았습니다.")
        return

    print(f"📌 이전 점수: {last}")
    
    if best is not None:
        print(f"🏆 최고 점수: {best}")

# ============= 메인 =============

def main():
    score_data = load_score()
    print("\n프로그램을 시작합니다...\n")
    
    quizzes = load_quiz_data()
    
    try:
        while True:
            display_menu()
            choice = get_menu_choice()
            
            if choice is None:
                break
            
            if choice == '1':
                result = solve_quiz(quizzes)

                if result is not None:
                    last = result
                    best = score_data["best"]

                    # 최고 점수 갱신
                    if best is None or result > best:
                        best = result
                        print("🎉 최고 점수 갱신!")

                    # 데이터 업데이트
                    score_data = {"best": best, "last": last}

                    # 파일 저장
                    save_score(best, last)
            
            elif choice == '2':
                add_quiz(quizzes)
            
            elif choice == '3':
                show_quizzes(quizzes)
            
            elif choice == '4':
                show_scores(score_data)
            
            elif choice == '5':
                print("\n프로그램을 종료합니다.")
                break
    
    except (KeyboardInterrupt, EOFError):
        pass
    
    finally:
        print("\n⚠️ 프로그램을 종료합니다.")
        save_quiz_data(quizzes)


if __name__ == "__main__":
    main()