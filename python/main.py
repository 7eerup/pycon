import json

class Quiz:
    def __init__(self, question, options, answer_idx):
        self.question = question
        self.options = options
        self.answer_idx = answer_idx

    def to_dict(self):
        return {
            "question":self.question, 
            "options":self.options, 
            "answer_idx":self.answer_idx
            }
            
    @classmethod
    def from_dict(cls, data):
        return cls(data['question'], data["options"], data["answer_idx"])

def create_default_quizzes():
    return [
        Quiz("스트라이크 3번은?",["아웃","안타","홈런","도루"], 1),
        Quiz("볼을 네번 던지면?",["볼카운트","볼쓰리","볼아웃","볼넷"], 4),
        Quiz("직선으로 가장 빠른 구종은?",["직구","커터","슬라이더","싱커"], 2),
        Quiz("공이 인플레이 된 상황에서 타자가 홈까지 들어오는것을 뭐라고 할까요",["그라운드 홈런","홈런","쓰리런","투런포"], 1),
        Quiz("야구공이 아닌거는?",["코크볼","하드볼","소프트볼","퍽"], 4)
    ]

class QuizGame:
    def __init__(self, file_path="state.json"):
        self.file_path = file_path
        self.quizzes, self.best_score = self.load_state()

    def load_state(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                loaded_quizzes = [Quiz.from_dict(d) for d in data["quizzes"]]
                loaded_best_score = data["best_score"]

                return loaded_quizzes, loaded_best_score
            
        except (FileNotFoundError, json.JSONDecodeError):
            #파일 없음 / JSON오류
            default_quizzes = create_default_quizzes()
            self.quizzes = default_quizzes
            self.best_score = 0

            self.save_state()
            return default_quizzes, 0


    def save_state(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                #Quiz객체를 -> dict로 변경
                json_data = {
                    "quizzes": [q.to_dict() for q in self.quizzes], 
                    "best_score": self.best_score         
                }
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print("\n저장 완료")
        except Exception as e:
            print(f"save error: {e}")


    def Display_menu(self):
        print("\n" + "="*40)
        print("    🎯 나만의 퀴즈 게임 🎯")
        print("="*40)
        print("\n1. 퀴즈 풀기")
        print("\n2. 퀴즈 추가")
        print("\n3. 퀴즈 목록")
        print("\n4. 점수 확인")
        print("\n5. 종료")

    def list_quiz(self):
        print("\n등록된 퀴즈 목록 (총 {}개)".format(len(self.quizzes)))
        print("\n"+"-"*40)

        if len(self.quizzes) == 0:
            print("등록된 퀴즈가 없습니다. 퀴즈를 추가해주세요.")
            print("\n"+ "-"*40)
            return
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-"*40)
    
    def max_score(self):
        if self.best_score == 0:
            print("아직 퀴즈를 풀지 않았습니다 풀어보세요!")
        else:
            print(f"최고 점수는 {self.best_score}점 입니다!")

    def play_quiz(self):
        correct_count = 0
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{i}번 문제] {quiz.question}\n")
            for n, option in enumerate(quiz.options, start=1):
                print(f"[{n}] {option}")
            
            while True:
                user_answer = input("정답 입력 1-4 : ").strip()

                if user_answer.isdigit() and 1 <= int(user_answer) <= 4:
                    user_answer = int(user_answer)
                    break
                else:
                    print("잘못된 입력입니다. 1부터 4사이의 숫자를 입력하세요.")
            if user_answer == quiz.answer_idx:
                print("정답입니다!")
                correct_count += 1
            else:
                print(f"오답입니다! (정답 : {quiz.answer_idx}번)")
        
        if correct_count > self.best_score:
            print(f"새로운 최고 점수 달성 {correct_count}점!")
            self.best_score = correct_count
            self.save_state()
    
    def add_quiz(self):
        i = 0
        new_quiz_options = []
        new_quiz_question = input("문제를 입력해주세요 : ").strip()
    
        for i in range(4):
            new_quiz_options.append(input(f"\n[{i+1}] 번째 보기를 입력해주세요 : "))
        
        while True:
            new_quiz_answer_idx = input("\n해당 문제에 정답을 알려주세요(1 ~ 4) : ")
            if new_quiz_answer_idx.isdigit() and 1 <= int(new_quiz_answer_idx) <= 4:
                answer_idx = int(new_quiz_answer_idx)
                new_quiz = Quiz(new_quiz_question, new_quiz_options, answer_idx)
                self.quizzes.append(new_quiz)
                self.save_state()
                print("퀴즈가 성공적으로 추가되었습니다!")
                break
            else:
                print("입력이 옳바르지 않습니다 다시 입력해주세요!")
            
        

    def run(self):
        try:
            while True:
                self.Display_menu()
                choice = input("\n선택: ").strip()

                if choice == "1":
                    self.play_quiz()
                    
                    pass
                elif choice == "2":
                    self.add_quiz() 
                    pass
                elif choice == "3":
                    self.list_quiz()

                elif  choice == "4":
                    self.max_score()
                    pass
                elif choice == "5":
                    print("프로그램을 종료합니다. 안녕히 가세요!")
                    self.save_state()
                    break
                else:
                    print("잘못된 입력입니다. 1-5 사이의 숫자를 입력해주세요")    

        except KeyboardInterrupt:
            print("\n\nCtrl + C 프로그램을 종료합니다")
            print("저장 후 종료 됩니다")
            self.save_state()

        except EOFError:
            print("\n\n에러로 입력이 종료 되었습니다")
            print("저장 후 종료 됩니다")
            self.save_state()
            

# branch test
# 코드 동작 테스트
if __name__ == "__main__":
    game = QuizGame()
    game.run()
