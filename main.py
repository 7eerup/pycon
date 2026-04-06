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

def get_user_choice():
    """사용자 입력을 받는 함수"""
    while True:
        try:
            choice = input("원하는 기능을 선택하세요 (1-5): ").strip()
            
            # 입력값 검증
            if choice not in ['1', '2', '3', '4', '5']:
                print("오류: 1부터 5 사이의 숫자를 입력하세요.")
                continue
            
            return choice
        
        except Exception as e:
            print(f"오류 발생: {e}")

def handle_menu(choice):
    """선택한 메뉴를 처리하는 함수"""
    if choice == '1':
        print("\n 퀴즈 풀기 기능 (준비 중)")
    elif choice == '2':
        print("\n 퀴즈 추가 기능 (준비 중)")
    elif choice == '3':
        print("\n 퀴즈 목록 기능 (준비 중)")
    elif choice == '4':
        print("\n 점수 확인 기능 (준비 중)")
    elif choice == '5':
        print("\n 프로그램을 종료합니다.")
        return False  # 프로그램 종료 신호
    
    return True  # 프로그램 계속 실행

def main():
    """메인 함수 - 프로그램 실행"""
    while True:
        display_menu()
        choice = get_user_choice()
        
        # handle_menu가 False를 반환하면 프로그램 종료
        if not handle_menu(choice):
            break

if __name__ == "__main__":
    main()