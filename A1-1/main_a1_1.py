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


def get_non_empty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


def choose_category():
    print("\n카테고리 선택:")
    for index, category in enumerate(PROMPT_CATEGORIES, start=1):
        print(f"{index}. {category}")
    print("0. 직접 입력")

    while True:
        choice = input("선택: ").strip()
        if choice == "0":
            return get_non_empty_input("직접 입력할 카테고리: ")
        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(PROMPT_CATEGORIES):
                return PROMPT_CATEGORIES[number - 1]
        print("올바른 카테고리 번호를 입력해주세요.")


def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = get_non_empty_input("제목: ")
    content = get_non_empty_input("내용: ")
    category = choose_category()

    prompts.append(
        {
            "title": title,
            "content": content,
            "category": category,
            "favorite": False,
        }
    )
    print("프롬프트가 추가되었습니다!")


def print_prompt_summary(index, prompt):
    favorite_mark = " ⭐" if prompt["favorite"] else ""
    print(f"{index}. [{prompt['category']}] {prompt['title']}{favorite_mark}")


def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(prompts, start=1):
        print_prompt_summary(index, prompt)
    print(f"\n총 {len(prompts)}개의 프롬프트")


def show_categories(prompts):
    print("\n=== 카테고리별 조회 ===")
    for index, category in enumerate(PROMPT_CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:
        choice = input("선택: ").strip()
        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(PROMPT_CATEGORIES):
                selected_category = PROMPT_CATEGORIES[number - 1]
                break
        print("올바른 카테고리 번호를 입력해주세요.")

    filtered = [prompt for prompt in prompts if prompt["category"] == selected_category]
    if not filtered:
        print("해당 카테고리에 프롬프트가 없습니다.")
        return

    print(f"\n[{selected_category}] 카테고리 프롬프트:")
    for index, prompt in enumerate(filtered, start=1):
        print_prompt_summary(index, prompt)
    print(f"\n총 {len(filtered)}개의 프롬프트")


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

        if choice == "1":
            add_prompt(prompts)
        elif choice == "2":
            show_list(prompts)
        elif choice == "3":
            show_categories(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print(f"현재 {len(prompts)}개의 프롬프트가 준비되어 있습니다.")
            print("선택한 기능은 아직 구현 중입니다.")


if __name__ == "__main__":
    run()
