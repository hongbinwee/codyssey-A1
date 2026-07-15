PROMPT_CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]


# 프로그램 시작 시 사용할 기본 데이터를 만드는 함수입니다.
# 프롬프트 1개는 딕셔너리로, 여러 프롬프트는 리스트로 관리합니다.
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


# 사용자 입력 검증을 담당하는 공통 함수입니다.
# 제목, 내용, 직접 입력 카테고리처럼 비어 있으면 안 되는 값에 재사용합니다.
def get_non_empty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


# 프롬프트 제목 중복 여부를 확인합니다.
# 중복 검사는 프롬프트 추가 기능과 분리해 검증 기준을 따로 설명할 수 있게 했습니다.
def is_duplicate_title(prompts, title):
    normalized_title = title.lower()
    for prompt in prompts:
        if prompt["title"].lower() == normalized_title:
            return True
    return False


# 새 프롬프트 제목을 입력받는 함수입니다.
# 빈 입력과 중복 제목을 모두 막아 프롬프트 목록이 헷갈리지 않게 합니다.
def get_unique_title(prompts):
    while True:
        title = get_non_empty_input("제목: ")
        if not is_duplicate_title(prompts, title):
            return title
        print("이미 등록된 제목입니다. 다른 제목을 입력해주세요.")


# 카테고리 선택만 담당하는 함수입니다.
# 프롬프트 추가와 카테고리 조회에서 카테고리 목록 기준을 동일하게 유지합니다.
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


# 프롬프트 추가 기능입니다.
# 제목, 내용, 카테고리를 입력받아 하나의 딕셔너리로 만든 뒤 리스트에 저장합니다.
def add_prompt(prompts):
    print("\n=== 프롬프트 추가 ===")
    title = get_unique_title(prompts)
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


# 목록 형태로 보여줄 때 공통으로 사용하는 출력 함수입니다.
# 목록, 검색 결과, 카테고리 조회, 즐겨찾기 목록에서 같은 형식으로 출력합니다.
def print_prompt_summary(index, prompt):
    favorite_mark = " ⭐" if prompt["favorite"] else ""
    print(f"{index}. [{prompt['category']}] {prompt['title']}{favorite_mark}")


# 전체 프롬프트 목록을 보여주는 함수입니다.
# 저장된 모든 프롬프트를 번호와 함께 출력합니다.
def show_list(prompts):
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(prompts, start=1):
        print_prompt_summary(index, prompt)
    print(f"\n총 {len(prompts)}개의 프롬프트")


# 카테고리별 조회 기능입니다.
# 사용자가 선택한 카테고리와 같은 프롬프트만 골라 출력합니다.
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


# 검색 기능입니다.
# 입력한 키워드가 제목 또는 내용에 포함된 프롬프트를 찾아 출력합니다.
def search_prompt(prompts):
    print("\n=== 프롬프트 검색 ===")
    keyword = get_non_empty_input("검색어: ").lower()
    results = []

    for prompt in prompts:
        title = prompt["title"].lower()
        content = prompt["content"].lower()
        if keyword in title or keyword in content:
            results.append(prompt)

    if not results:
        print("검색 결과가 없습니다.")
        return

    print("\n검색 결과:")
    for index, prompt in enumerate(results, start=1):
        print_prompt_summary(index, prompt)
    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")


# 번호로 프롬프트를 선택하는 공통 함수입니다.
# 상세 보기와 즐겨찾기 관리에서 같은 번호 검증 로직을 재사용합니다.
def get_prompt_by_number(prompts, message="번호 입력: "):
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return None

    choice = input(message).strip()
    if not choice.isdigit():
        print("숫자로 입력해주세요.")
        return None

    number = int(choice)
    if number < 1 or number > len(prompts):
        print("잘못된 번호입니다.")
        return None

    return prompts[number - 1]


# 상세 보기 기능입니다.
# 선택한 프롬프트의 제목, 카테고리, 즐겨찾기 여부, 전체 내용을 출력합니다.
def show_prompt_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    show_list(prompts)
    prompt = get_prompt_by_number(prompts)
    if prompt is None:
        return

    print("\n=== 상세 내용 ===")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'예' if prompt['favorite'] else '아니오'}")
    print("내용:")
    print(prompt["content"])


# 즐겨찾기 추가/해제 기능입니다.
# 선택한 프롬프트의 favorite 값을 True와 False 사이에서 바꿉니다.
def toggle_favorite(prompts):
    print("\n=== 즐겨찾기 관리 ===")
    show_list(prompts)
    prompt = get_prompt_by_number(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print("즐겨찾기에 추가되었습니다.")
    else:
        print("즐겨찾기가 해제되었습니다.")


# 즐겨찾기 목록 기능입니다.
# favorite 값이 True인 프롬프트만 모아서 출력합니다.
def show_favorites(prompts):
    print("\n=== 즐겨찾기 목록 ===")
    favorites = [prompt for prompt in prompts if prompt["favorite"]]
    if not favorites:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(favorites, start=1):
        print_prompt_summary(index, prompt)
    print(f"\n총 {len(favorites)}개의 즐겨찾기 프롬프트")


# 메뉴 출력만 담당하는 함수입니다.
# 메뉴를 따로 분리해 기능 추가/수정 시 전체 흐름을 쉽게 관리합니다.
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


# 프로그램의 전체 실행 흐름을 담당하는 함수입니다.
# 메뉴 번호에 따라 각 기능 함수를 호출하고, 종료 전까지 데이터가 유지됩니다.
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
        elif choice == "4":
            search_prompt(prompts)
        elif choice == "5":
            show_prompt_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    run()
