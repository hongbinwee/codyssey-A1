PROMPT_CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]


def create_default_prompts():
    return [
        {
            "title": "블로그 글 작성 도우미",
            "content": "주어진 주제에 대해 서론, 본론, 결론 구조로 블로그 글을 작성해주세요.",
            "category": "텍스트 생성",
            "favorite": False,
        },
        {
            "title": "제품 썸네일 이미지 프롬프트",
            "content": "제품이 중앙에 보이는 밝고 깔끔한 썸네일 이미지를 생성해주세요.",
            "category": "이미지 생성",
            "favorite": False,
        },
        {
            "title": "뉴스 요약 자동화 프롬프트",
            "content": "오늘의 주요 뉴스를 3줄로 요약하고 핵심 키워드를 정리해주세요.",
            "category": "자동화",
            "favorite": False,
        },
    ]


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def run():
    prompts = create_default_prompts()

    while True:
        show_menu()
        choice = input("선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break

        print(f"현재 {len(prompts)}개의 기본 프롬프트가 준비되어 있습니다.")
        print("선택한 기능은 아직 구현 중입니다.")


if __name__ == "__main__":
    run()
