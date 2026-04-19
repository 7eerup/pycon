# 5부터 1까지 카운트다운
count = 10

while count > 0:
    print(count)
    count -= 1


# 사용자 입력
while True:
    user_input = input("명령을 입력하세요(quit 입력 시 종료): ")
    if user_input == "q":
        print("프로그램 종료")
        break
    else:
        print(f"입력: {user_input}")


# 올바른 비밀번호 입력할 때까지 반복
correct_password = "1234"
attempts = 0

while attempts < 3:
    password = input("비밀번호를 입력하세요: ")
    attempts += 1
    
    if password == correct_password:
        print("로그인 성공!")
        break
    else:
        print(f"틀렸습니다 ({3 - attempts}회 남음)")

if attempts == 3:
    print("비밀번호 입력 횟수 초과")