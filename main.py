# AI 활용 자유 주제 파이썬 미니 프로젝트
# 이름 또는 학번: 20907
# 프로젝트 주제: 책 검색·추천·다운로드 프로그램 (Anna's Archive API 활용)

# ============================================================
# 프로그램 설명
# ------------------------------------------------------------
# 내가 만든 책 목록(2차원 리스트)을 가지고
#   1) 제목/저자로 검색하고
#   2) 형식(EPUB/PDF)으로 거르고
#   3) 출판연도 최신순으로 정렬하고
#   4) 형식별 권수·평균 평점 같은 통계를 내고
#   5) 평점과 연도를 점수로 환산해 책 한 권을 추천하고
#   6) 고른 책의 md5 해시를 Anna's Archive 회원 API로 보내
#      실제 다운로드 링크를 받아오는 프로그램이다.
#
# [수행평가 필수 조건과 연결]
#   - 2차원 리스트  : books (제목·저자·형식·연도·평점·md5)
#   - 함수 3개 이상 : load_api_key / search_books / filter_by_format /
#                     sort_by_year / show_statistics / recommend_book /
#                     print_books / get_download_link / main  (총 9개)
#   - 조건문        : 메뉴 분기, 검색·필터 판단, 통계 비교, 입력 검사, API 성공/실패
#   - 반복문        : 메뉴 반복, 책 목록 순회, 통계 집계
#   - 실행 결과 출력 : 검색·정렬·통계·추천 결과와 다운로드 링크
# ============================================================

import os


# ------------------------------------------------------------
# 1. 데이터 준비: 2차원 리스트
# ------------------------------------------------------------
# 한 행 = 책 한 권. 각 열의 의미:
#   0번 열: 제목(문자열)
#   1번 열: 저자(문자열)
#   2번 열: 형식(EPUB, PDF 등 문자열)
#   3번 열: 출판연도(정수)
#   4번 열: 평점(0.0 ~ 5.0 실수)
#   5번 열: md5 해시(문자열)
#           -> annas-archive.org 에서 책을 검색해 클릭하면 주소가
#              https://annas-archive.org/md5/XXXX... 가 된다.
#              그 뒤 32자리(영문 소문자+숫자)를 복사해 붙여넣으면
#              다운로드 기능이 동작한다. 아직 안 넣었으면 다운로드만 안 된다.
books = [
    ["1984",                 "George Orwell",       "EPUB", 2009, 4.7, "md5_here"],
    ["Pride and Prejudice",  "Jane Austen",         "EPUB", 2008, 4.5, "md5_here"],
    ["The Great Gatsby",     "F. Scott Fitzgerald", "PDF",  2021, 4.2, "md5_here"],
    ["Hamlet",               "William Shakespeare", "PDF",  2000, 4.0, "md5_here"],
    ["Frankenstein",         "Mary Shelley",        "EPUB", 1993, 3.9, "md5_here"],
    ["The Old Man and the Sea", "Ernest Hemingway", "PDF",  2002, 4.3, "md5_here"],
]

# Anna's Archive 다운로드 API 주소
FAST_DOWNLOAD_URL = "https://annas-archive.org/dyn/api/fast_download.json"


# ------------------------------------------------------------
# 2. 함수 정의
# ------------------------------------------------------------
def load_api_key():
    """.env 파일에서 AA_API_KEY 값을 읽어 돌려준다.
    .env 는 git에 올라가지 않으므로 비밀 키를 안전하게 보관할 수 있다."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    try:
        with open(env_path, encoding="utf-8") as f:
            for line in f:                          # 반복문: 한 줄씩 확인
                line = line.strip()
                if line.startswith("AA_API_KEY="):  # 조건문: 키가 있는 줄인지
                    return line.split("=", 1)[1]
    except FileNotFoundError:
        pass
    return ""


def search_books(data, keyword):
    """제목이나 저자에 keyword 가 들어간 책만 골라 새 2차원 리스트로 돌려준다."""
    results = []
    keyword = keyword.lower()
    for row in data:                                # 반복문: 모든 책을 하나씩 확인
        title = row[0].lower()
        author = row[1].lower()
        if keyword in title or keyword in author:   # 조건문: 검색어 포함 여부
            results.append(row)
    return results


def filter_by_format(data, book_format):
    """원하는 형식(EPUB/PDF 등)의 책만 골라 돌려준다."""
    results = []
    book_format = book_format.upper()
    for row in data:                                # 반복문
        if row[2].upper() == book_format:           # 조건문: 형식 일치
            results.append(row)
    return results


def sort_by_year(data):
    """출판연도(3번 열)를 기준으로 최신순으로 정렬해 돌려준다."""
    return sorted(data, key=lambda row: row[3], reverse=True)


def show_statistics(data):
    """형식별 권수, 평균 평점, 가장 최신 책을 계산해서 출력한다."""
    if len(data) == 0:                              # 조건문: 데이터 없음 처리
        print("통계를 낼 책이 없습니다.")
        return

    format_count = {}     # 형식 -> 권수
    rating_sum = 0.0
    newest_row = data[0]

    for row in data:                                # 반복문: 통계 집계
        book_format = row[2]
        if book_format in format_count:             # 조건문: 이미 센 형식인지
            format_count[book_format] += 1
        else:
            format_count[book_format] = 1
        rating_sum += row[4]
        if row[3] > newest_row[3]:                  # 조건문: 더 최신 책 갱신
            newest_row = row

    average_rating = rating_sum / len(data)

    print("총 책 수:", len(data), "권")
    for book_format in sorted(format_count):        # 반복문: 형식별 권수 출력
        print(f"  - {book_format}: {format_count[book_format]}권")
    print(f"평균 평점: {average_rating:.2f}")
    print(f"가장 최신 책: {newest_row[0]} ({newest_row[3]}년)")


def recommend_book(data):
    """평점과 출판연도를 점수로 환산해 가장 점수가 높은 책 한 권을 추천한다.
    점수 = 평점 * 2 + (출판연도 - 2000) * 0.05  (최신이고 평점 높을수록 점수↑)"""
    if len(data) == 0:                              # 조건문
        return None

    best_row = data[0]
    best_score = -1.0
    for row in data:                                # 반복문: 점수 계산
        score = row[4] * 2 + (row[3] - 2000) * 0.05
        if score > best_score:                      # 조건문: 최고 점수 판정
            best_score = score
            best_row = row
    return best_row, round(best_score, 2)


def print_books(data):
    """책 목록을 번호와 함께 보기 좋게 출력한다."""
    if len(data) == 0:                              # 조건문: 결과 없음
        print("조건에 맞는 책이 없습니다.")
        return
    for number, row in enumerate(data, start=1):    # 반복문: 번호 붙여 출력
        print(f"{number}. {row[0]} / {row[1]} / {row[2]} / {row[3]}년 / 평점 {row[4]}")


def get_download_link(md5, api_key):
    """md5 해시를 Anna's Archive API에 보내 실제 다운로드 링크를 받아온다."""
    # 조건문들: 호출 전에 잘못된 상황을 먼저 걸러낸다.
    if not api_key:
        return "오류: .env 에 AA_API_KEY 가 없습니다."
    if len(md5) != 32:
        return "오류: 올바른 md5 해시가 아닙니다. (32자리 필요 / 책 목록에 md5를 넣으세요)"

    try:
        import requests  # 다운로드할 때만 필요한 외부 라이브러리 (선생님 허락 후 사용)
    except ImportError:
        return "오류: requests 가 없습니다. 터미널에서 'pip install -r requirements.txt' 실행하세요."

    try:
        response = requests.get(
            FAST_DOWNLOAD_URL,
            params={"md5": md5, "key": api_key},
            timeout=30,
        )
    except requests.RequestException as error:
        return f"오류: 네트워크 문제 - {error}"

    if response.status_code != 200:                 # 조건문: 서버 정상 응답 확인
        return f"오류: 서버 응답 코드 {response.status_code}"

    try:
        result = response.json()
    except ValueError:
        return "오류: 서버가 올바른 JSON을 주지 않았습니다. (키가 틀렸거나 차단된 경우)"

    if "download_url" in result:                    # 조건문: 성공/실패 판정
        return result["download_url"]
    return f"오류: {result.get('error', '다운로드 링크를 받지 못했습니다.')}"


def main():
    api_key = load_api_key()

    while True:                                     # 반복문: 메뉴를 계속 보여 준다
        print("\n" + "=" * 48)
        print("  책 검색·추천·다운로드 (Anna's Archive)")
        print("=" * 48)
        print("1. 제목/저자 검색")
        print("2. 형식으로 거르기 (EPUB/PDF)")
        print("3. 최신순 정렬해서 보기")
        print("4. 통계 보기")
        print("5. 책 추천 받기")
        print("6. 다운로드 링크 받기")
        print("0. 종료")

        choice = input("메뉴 번호를 입력하세요: ")

        if choice == "1":                           # 조건문: 메뉴 분기
            keyword = input("검색어(제목/저자): ")
            print_books(search_books(books, keyword))

        elif choice == "2":
            book_format = input("형식(EPUB 또는 PDF): ")
            print_books(filter_by_format(books, book_format))

        elif choice == "3":
            print_books(sort_by_year(books))

        elif choice == "4":
            show_statistics(books)

        elif choice == "5":
            result = recommend_book(books)
            if result is None:                      # 조건문: 추천할 책이 없을 때
                print("추천할 책이 없습니다.")
            else:
                book, score = result
                print(f"오늘의 추천: {book[0]} (점수 {score})")

        elif choice == "6":
            print_books(books)
            answer = input("다운로드할 책 번호(0=취소): ")
            if not answer.isdigit():                # 조건문: 잘못된 입력 처리
                print("숫자를 입력해야 합니다.")
            else:
                number = int(answer)
                if number <= 0 or number > len(books):  # 조건문: 범위 확인
                    print("취소했습니다.")
                else:
                    book = books[number - 1]
                    print(f"'{book[0]}' 의 다운로드 링크를 요청합니다...")
                    print("결과:", get_download_link(book[5], api_key))

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break                                   # 반복문 종료

        else:
            print("잘못된 입력입니다. 0~6 중에서 고르세요.")


# ------------------------------------------------------------
# 3. 프로그램 실행
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
