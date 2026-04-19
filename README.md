## 프로젝트 개요
- Python 활용한 CLI 기반 퀴즈 프로그램
- 사용자는 퀴즈를 풀고, 직접 퀴즈를 추가하며, 점수를 확인하고, 프로그램 종료 후에도 데이터가 유지되도록 JSON 파일 기반의 상태 저장 기능을 포함하고 있습니다.

## 퀴즈 주제 선정 이유
- Python 기초 및 프로그래밍 지식 학습 환경 구성

## 실행 환경 및 방법
- python3 main.py
- python3.13.7


## 기능 목록
1. 퀴즈 풀기
저장된 퀴즈를 순차적으로 출제
정답/오답 여부 즉시 피드백 제공
전체 문제 풀이 후 점수 출력
진행 상황 표시 ([현재 문제 / 전체 문제])
2. 퀴즈 추가
문제, 선택지(4개), 정답 입력
입력값 검증 처리 (빈 값, 범위 오류 등)
추가된 퀴즈는 파일에 자동 저장
3. 퀴즈 목록 확인
저장된 전체 퀴즈 목록 출력
퀴즈가 없는 경우 예외 처리
4. 점수 확인
이전 점수 확인
최고 점수 확인
5. 데이터 유지
프로그램 종료 후에도 데이터 유지
JSON 파일 기반 상태 저장
6. 예외 처리
KeyboardInterrupt (Ctrl+C)
EOFError
잘못된 입력 처리


## 파일 구조
```
.
├── README.md
├── main.py
├── screenshots
│   ├── branch_a.png
│   ├── branch_b.png
│   ├── branch_c.png
│   ├── class.png
│   ├── menu.png
│   ├── quiz.png
│   ├── quiz_add.png
│   ├── quiz_list.png
│   ├── quiz_score.png
│   └── user.png
└── state.json
```

## 데이터 파일 설명(state.json 등)
- 퀴즈 데이터 저장
- 최고 점수 및 마지막 점수 저장
- 프로그램 실행 시 데이터 복원



## 코드 구조 설계 & 데이터 구조 흐름
```
[사용자 입력]
   ↓
[input 함수]
   ↓
[QuizGame 로직]
   ↓
[Quiz 객체 활용]
   ↓
[state.json 저장]
```

```bash
Quiz 클래스 (도메인 객체)

역할:
퀴즈 하나를 표현
문제, 선택지, 정답 보관
정답 체크 (is_correct)
출력 (display)
직렬화 (to_dict, from_dict)


QuizGame 클래스 (애플리케이션 로직)

역할:
메뉴 관리
사용자 입력 흐름 제어
퀴즈 진행 (solve_quiz)
퀴즈 추가 (add_quiz)
점수 관리 (update_score)
파일 저장/불러오기 (load_data, save_data)
```

### “입력 처리(검증)”, “게임 진행”, “데이터 저장/불러오기” 로직
get_integer_input() / get_string_input()

solve_quiz() → add_quiz() → show_quizzes()

load_state() → save_state()


### state.json 읽기/쓰기 흐름
main() → QuizGame() → load_data() → load_state()


### Ctrl+C(KeyboardInterrupt) / EOFError 안전 처리
solve_quiz() → update_score() → save_data() → save_state()

### 커밋 단위

| 기능         | 브랜치                      |
| ---------- | ------------------------ |
| 기본 구조      | main                     |
| 퀴즈 풀기      | feature/quiz-fundamental |
| 퀴즈 추가      | feature/quiz-add         |
| 목록 기능      | feature/quiz-list        |
| 점수 기능      | feature/score            |
| state.json | feature/state            |


### 커밋 메시지
feat: 퀴즈 추가 기능 구현
feat: 퀴즈 목록 기능 구현
feat: 점수 저장 기능 구현
refactor: QuizGame 클래스 구조 개선
docs: README 작성


### 클래스
데이터 + 기능을 묶어서 재사용 가능하게 만든 구조

### 클래스 사용 이유
데이터 + 기능을 하나로 묶기 위해 (캡슐화)
상태(state)를 객체 단위로 관리하기 위해
구조화 확장성

### 함수만 사용할 경우
전역 변수 증가 → 상태 관리 어려움
데이터와 로직 분리 → 구조 복잡
유지보수 ↓

### JSON 저장 이유
파일 기반으로 데이터 영속성 유지
Python ↔ JSON 변환 쉬움 (dict ↔ JSON)

### JSON 특징
key-value 구조 (딕셔너리)
사람이 읽기 쉬움
언어 독립적 (호환성 좋음)

### try/except 필요한 이유
파일 입출력은 실패 가능성이 높음
파일 없음 (FileNotFoundError)
JSON 깨짐 (JSONDecodeError)
권한 문제 (PermissionError)

### 브랜치 분리 이유
- 기능별 독립 개발
- 기존 코드 안정성 유지
- 협업 시 충돌 최소화
- 안전한 기능 개발과 협업

### merge 의미
- 다른 브랜치의 변경사항을 main에 통합
- “기능 개발 → 검증 → 메인 반영” 흐름(구조화)

### state.json 구조 설계 이유
- 퀴즈 + 점수 → 하나의 상태로 관리
- 프로그램 재실행 시 전체 복원 가능
- state.json → 전체 상태를 한 번에 관리


### 퀴즈 데이터 1000개 이상 저장 JSON 저장 방식 한계점
- 전체 파일 재로드/재저장 비용 증가
- 메모리 사용량 증가
- 동시성 확장성 문제점 발생


### state.json 손상 시 대응 방법
- 백업 기반 복구 (권장) → 데이터 유실 최소화