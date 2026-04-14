import json
import os

# ============= 입력 검증 함수 =============

def get_integer_input(prompt, min_value, max_value):
    """정수 입력을 받고 검증하는 함수"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            # 1. 빈 입력 처리
            if not user_input:
                print("오류: 입력이 비어있습니다. 다시 입력하세요.")
                continue
            
            # 2. 숫자 변환 시도
            try:
                value = int(user_input)
            except ValueError:
                print(f"오류: 숫자를 입력하세요. (입력값: '{user_input}')")
                continue
            
            # 3. 범위 확인
            if value < min_value or value > max_value:
                print(f"오류: {min_value}부터 {max_value} 사이의 숫자를 입력하세요.")
                continue
            
            return value
        
        except (KeyboardInterrupt, EOFError):
            return None  # ✅ None 반환


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
            return None  # ✅ None 반환


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
            
            # 빈 입력 처리
            if not choice:
                print("오류: 입력이 비어있습니다. 다시 입력하세요.")
                continue
            
            # 범위 검증 (1-5)
            if choice not in ['1', '2', '3', '4', '5']:
                print("오류: 1부터 5 사이의 숫자를 입력하세요.")
                continue
            
            return choice
        
        except (KeyboardInterrupt, EOFError):
            return None  # ✅ None 반환으로 종료 신호


# ============= 데이터 관리 함수 =============

def get_default_quizzes():
    """기본 퀴즈 데이터를 반환합니다."""
    return [
        {
            "id": 1,
            "question": "파이썬의 창시자는?",
            "choices": ["귀도 반 로섐", "라이너스 토르발즈", "데니스 리치", "비야네 스트롭스트룹"],
            "answer": 1
        },
        {
            "id": 2,
            "question": "파이썬이 처음 출시된 연도는?",
            "choices": ["1989년", "1991년", "1995년", "2000년"],
            "answer": 2
        },
        {
            "id": 3,
            "question": "파이썬의 특징이 아닌 것은?",
            "choices": ["동적 타입", "인터프리터 언어", "컴파일 필수", "간단한 문법"],
            "answer": 3
        }
    ]


def load_quiz_data(filename="data.json"):
    """파일에서 퀴즈 데이터를 로드합니다."""
    try:
        # 파일이 없는 경우
        if not os.path.exists(filename):
            print(f"ℹ️ '{filename}' 파일이 없습니다. 기본 데이터를 사용합니다.")
            quizzes = get_default_quizzes()
            save_quiz_data(quizzes, filename)
            return quizzes
        
        # 파일 읽기
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # 데이터 유효성 검사
            if not isinstance(data, list) or len(data) == 0:
                raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")
            
            print(f"✅ '{filename}'에서 {len(data)}개의 퀴즈를 로드했습니다.")
            return data
    
    except json.JSONDecodeError:
        print(f"⚠️ '{filename}'이 손상되었습니다. 기본 데이터로 복구합니다.")
        quizzes = get_default_quizzes()
        save_quiz_data(quizzes, filename)
        return quizzes
    
    except (KeyError, ValueError) as e:
        print(f"⚠️ 데이터 형식 오류: {e}. 기본 데이터로 복구합니다.")
        quizzes = get_default_quizzes()
        save_quiz_data(quizzes, filename)
        return quizzes
    
    except Exception as e:
        print(f"⚠️ 예상치 못한 오류: {e}. 기본 데이터를 사용합니다.")
        return get_default_quizzes()


def save_quiz_data(quizzes, filename="data.json"):
    """현재 퀴즈 데이터를 파일에 저장합니다."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(quizzes, f, ensure_ascii=False, indent=2)
    
    except IOError as e:
        print(f"⚠️ 파일 저장 실패: {e}")
    except Exception as e:
        print(f"⚠️ 예상치 못한 오류: {e}")


# ============= Quiz 클래스 및 추가 기능 =============

class Quiz:
    """개별 퀴즈를 표현하는 클래스"""
    def __init__(self, question, choices, answer, qid=None):
        # 기본 유효성 검사
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
        """사용자 선택이 정답인지 확인 (정수 1~4 기대)"""
        return user_choice == self.answer

    def get_correct_text(self):
        """정답 텍스트 반환"""
        return self.choices[self.answer - 1]

    def to_dict(self):
        """파일 저장용 딕셔너리 반환"""
        return {
            "id": self.id,
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

    @classmethod
    def from_dict(cls, d):
        """딕셔너리로부터 Quiz 객체 생성"""
        return cls(
            question=d["question"],
            choices=d["choices"],
            answer=d["answer"],
            qid=d.get("id")
        )


def next_id(quizzes):
    """현재 quizzes(dict 리스트)를 보고 다음 id 계산"""
    if not quizzes:
        return 1
    ids = []
    for q in quizzes:
        try:
            ids.append(int(q.get("id") or 0))
        except Exception:
            ids.append(0)
    return max(ids, default=0) + 1


def add_quiz(quizzes, filename="data.json"):
    """
    퀴즈를 입력받아 quizzes 리스트에 추가하고 파일에 저장.
    입력 도중 Ctrl+C/Ctrl+D 발생하면 작업을 취소하고 복귀합니다.
    """
    print("\n=== 퀴즈 추가 ===")
    # 문제 입력
    question = get_string_input("문제 내용을 입력하세요: ")
    if question is None:
        print("입력 취소: 프로그램으로 복귀합니다.")
        return False

    # 선택지 4개 입력
    choices = []
    for i in range(1, 5):
        ch = get_string_input(f"선택지 {i} 입력: ")
        if ch is None:
            print("입력 취소: 프로그램으로 복귀합니다.")
            return False
        choices.append(ch)

    # 정답 입력 (1-4)
    answer = get_integer_input("정답 번호를 입력하세요 (1-4): ", 1, 4)
    if answer is None:
        print("입력 취소: 프로그램으로 복귀합니다.")
        return False

    # id 부여 및 객체 생성
    qid = next_id(quizzes)
    try:
        quiz = Quiz(question=question, choices=choices, answer=answer, qid=qid)
    except ValueError as e:
        print(f"오류: {e}")
        return False

    # dict 형식으로 목록에 추가하고 저장
    quizzes.append(quiz.to_dict())
    save_quiz_data(quizzes, filename)
    print(f"✅ 퀴즈가 추가되었습니다. id={qid}")
    return True


# ============= 메뉴 처리 (quizzes 전달) =============

def handle_menu(choice, quizzes, filename="data.json"):
    """선택한 메뉴를 처리하는 함수 (quizzes 리스트를 직접 수정)"""
    if choice is None:
        return False

    if choice == '1':
        print("\n 퀴즈 풀기 기능 (준비 중)")
    elif choice == '2':
        add_quiz(quizzes, filename)
    elif choice == '3':
        print("\n=== 퀴즈 목록 ===")
        if not quizzes:
            print("퀴즈가 없습니다.")
        else:
            for q in quizzes:
                qid = q.get("id") if isinstance(q, dict) else getattr(q, "id", None)
                question = q.get("question") if isinstance(q, dict) else getattr(q, "question", "")
                print(f"id={qid}: {question}")
    elif choice == '4':
        print("\n 점수 확인 기능 (준비 중)")
    elif choice == '5':
        print("\n 프로그램을 종료합니다.")
        return False  # 프로그램 종료 신호
    
    return True  # 프로그램 계속 실행


# ============= 메인 함수 =============

def main():
    """메인 함수 - 프로그램 실행"""
    print("\n프로그램을 시작합니다...\n")
    
    # 데이터 로드
    filename = "data.json"
    quizzes = load_quiz_data(filename)
    
    try:
        while True:
            display_menu()
            choice = get_menu_choice()
            
            # Ctrl+C 또는 EOFError 처리
            if choice is None:  # ✅ None 감지
                break
            
            # 메뉴 처리 (quizzes 전달)
            if not handle_menu(choice, quizzes, filename):
                break
    
    except (KeyboardInterrupt, EOFError):
        # ✅ 추가 예외 처리 (혹시 모를 상황)
        pass
    
    finally:  # ✅ 항상 실행 - 안전한 종료 보장
        print("\n⚠️ 프로그램을 종료합니다.")
        save_quiz_data(quizzes, filename)
        print("데이터가 저장되었습니다.")


if __name__ == "__main__":
    main()