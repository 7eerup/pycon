## 프로젝트 개요
- Python 활용한 CLI 기반 퀴즈 프로그램
- 사용자는 퀴즈를 풀고, 직접 퀴즈를 추가하며, 점수를 확인하고, 프로그램 종료 후에도 데이터가 유지되도록 JSON 파일 기반의 상태 저장 기능을 포함하고 있습니다.

## 퀴즈 주제 선정 이유
- Python 기초 및 프로그래밍 지식 학습 환경 구성

## 실행 환경 및 방법
python3 main.py
python3.13.7
표준 라이브러리 사용


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


## 데이터 파일 설명(state.json 등)
- 퀴즈 데이터 저장
- 최고 점수 및 마지막 점수 저장
- 프로그램 실행 시 데이터 복원