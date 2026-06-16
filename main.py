# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 20907
# 프로젝트 주제: 음식 추천 프로그램
#
# - 2차원 리스트(foods): 한 행 = 음식 하나, 열 = [이름, 가격, 종류, 특징]
# - 함수 4개로 기능 분리, if 조건문, while/for 반복문
# - 사용자 입력(예산, 종류)에 따라 추천 결과가 달라짐

# 2차원 리스트: 행=음식, 열=[이름, 가격, 종류, 특징]
foods = [
    ["김밥", 3500, "식사", "가벼움"],
    ["라면", 4000, "식사", "매움"],
    ["돈까스", 8000, "식사", "든든함"],
    ["아이스티", 2500, "음료", "시원함"],
    ["아메리카노", 3000, "음료", "쌉쌀함"],
    ["케이크", 6000, "디저트", "달콤함"],
]


def show_all():
    """전체 메뉴를 출력한다."""
    print("\n[ 전체 메뉴 ]")
    for food in foods:  # 반복문 for
        print(f" - {food[0]} | {food[1]}원 | {food[2]} | {food[3]}")


def recommend_by_budget(budget):
    """예산 안에서 먹을 수 있는 음식을 추천한다."""
    print(f"\n[ {budget}원으로 먹을 수 있는 음식 ]")
    found = False
    for food in foods:
        if food[1] <= budget:  # 조건문 if: 예산 비교
            print(f" - {food[0]} ({food[1]}원, {food[3]})")
            found = True
    if not found:  # 결과가 없을 때 처리
        print(" 예산에 맞는 음식이 없습니다.")


def recommend_by_type(kind):
    """종류(식사/음료/디저트)로 음식을 추천한다."""
    print(f"\n[ '{kind}' 추천 결과 ]")
    found = False
    for food in foods:
        if food[2] == kind:  # 조건문 if: 종류 비교
            print(f" - {food[0]} ({food[1]}원, {food[3]})")
            found = True
    if not found:
        print(" 해당 종류의 음식이 없습니다.")


def main():
    while True:  # 반복문 while: 메뉴 반복
        print("\n===== 음식 추천 프로그램 =====")
        print("1. 전체 메뉴 보기")
        print("2. 예산으로 추천받기")
        print("3. 종류로 추천받기")
        print("0. 종료")
        choice = input("메뉴 선택: ")  # 사용자 입력

        if choice == "1":
            show_all()
        elif choice == "2":
            money = input("예산을 입력하세요(원): ")
            if money.isdigit():  # 잘못된 입력 처리
                recommend_by_budget(int(money))
            else:
                print("숫자만 입력하세요.")
        elif choice == "3":
            kind = input("종류 입력(식사/음료/디저트): ")
            recommend_by_type(kind)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")


if __name__ == "__main__":
    main()
