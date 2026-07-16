import json
from pathlib import Path


PROMPT_CATEGORIES = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]

DATA_FILE = Path(__file__).with_name("prompts.json")
EXPORT_DIR = Path(__file__).with_name("exports")
EXPORT_FILE = EXPORT_DIR / "prompts_by_category.md"


# 프롬프트 1개를 만드는 함수입니다.
# 모든 프롬프트가 같은 필드를 갖도록 생성 기준을 한 곳에 모았습니다.
def create_prompt(title, content, category, favorite=False, use_count=0):
    return {
        "title": title,
        "content": content,
        "category": category,
        "favorite": favorite,
        "use_count": use_count,
    }


# 프로그램 시작 시 사용할 기본 데이터를 만드는 함수입니다.
# 프롬프트 1개는 딕셔너리로, 여러 프롬프트는 리스트로 관리합니다.
def create_default_prompts():
    return [
        create_prompt(
            "블로그 글 작성 도우미",
            "주어진 주제에 대해 서론, 본론, 결론 구조로 블로그 글을 작성해주세요.",
            "텍스트 생성",
        ),
        create_prompt(
            "제품 썸네일 이미지 프롬프트",
            "제품이 중앙에 보이는 밝고 깔끔한 썸네일 이미지를 생성해주세요.",
            "이미지 생성",
        ),
        create_prompt(
            "뉴스 요약 자동화 프롬프트",
            "오늘의 주요 뉴스를 3줄로 요약하고 핵심 키워드를 정리해주세요.",
            "자동화",
        ),
    ]


# 저장 파일을 불러올 때 누락된 필드를 보완합니다.
# 이전 버전 데이터가 있더라도 title/content/category/favorite/use_count 구조를 유지합니다.
def normalize_prompt(prompt):
    return create_prompt(
        prompt.get("title", "제목 없음"),
        prompt.get("content", ""),
        prompt.get("category", "기타"),
        prompt.get("favorite", False),
        prompt.get("use_count", 0),
    )


# JSON 파일에서 프롬프트를 불러오는 함수입니다.
# 파일이 없거나 읽기 실패하면 기본 데이터로 시작합니다.
def load_prompts():
    if not DATA_FILE.exists():
        return create_default_prompts()

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("저장 파일을 읽을 수 없어 기본 데이터로 시작합니다.")
        return create_default_prompts()

    if not isinstance(data, list):
        print("저장 파일 형식이 올바르지 않아 기본 데이터로 시작합니다.")
        return create_default_prompts()

    return [normalize_prompt(prompt) for prompt in data]


# 현재 프롬프트 목록을 JSON 파일로 저장합니다.
# 추가, 수정, 삭제, 즐겨찾기, 상세 조회수 변경 후 호출합니다.
def save_prompts(prompts):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(prompts, file, ensure_ascii=False, indent=2)


# 사용자 입력 검증을 담당하는 공통 함수입니다.
# 제목, 내용, 직접 입력 카테고리처럼 비어 있으면 안 되는 값에 재사용합니다.
def get_non_empty_input(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("입력값이 비어 있습니다. 다시 입력해주세요.")


# 수정 기능에서 빈 입력이면 기존 값을 유지하도록 돕습니다.
def get_optional_input(message, current_value):
    value = input(f"{message} (현재: {current_value}, 유지하려면 Enter): ").strip()
    if value:
        return value
    return current_value


# 프롬프트 제목 중복 여부를 확인합니다.
# 수정 중인 항목의 인덱스는 제외해 자기 자신과 충돌하지 않게 합니다.
def is_duplicate_title(prompts, title, ignore_index=None):
    normalized_title = title.lower()
    for index, prompt in enumerate(prompts):
        if index == ignore_index:
            continue
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


# 수정할 제목을 입력받는 함수입니다.
# Enter를 누르면 기존 제목을 유지하고, 새 제목은 중복 검사를 거칩니다.
def get_updated_title(prompts, current_title, prompt_index):
    while True:
        title = get_optional_input("새 제목", current_title)
        if not is_duplicate_title(prompts, title, prompt_index):
            return title
        print("이미 등록된 제목입니다. 다른 제목을 입력해주세요.")


# 카테고리 선택만 담당하는 함수입니다.
# 프롬프트 추가, 수정, 카테고리 조회에서 카테고리 목록 기준을 동일하게 유지합니다.
def choose_category(current_category=None):
    print("\n카테고리 선택:")
    for index, category in enumerate(PROMPT_CATEGORIES, start=1):
        print(f"{index}. {category}")
    print("0. 직접 입력")
    if current_category is not None:
        print("Enter. 현재 카테고리 유지")

    while True:
        choice = input("선택: ").strip()
        if current_category is not None and choice == "":
            return current_category
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

    prompts.append(create_prompt(title, content, category))
    save_prompts(prompts)
    print("프롬프트가 추가되었습니다!")


# 목록 형태로 보여줄 때 공통으로 사용하는 출력 함수입니다.
# 조회수까지 함께 표시해 Top 목록과 일반 목록의 기준을 설명하기 쉽게 했습니다.
def print_prompt_summary(index, prompt):
    favorite_mark = " ⭐" if prompt["favorite"] else ""
    print(
        f"{index}. [{prompt['category']}] {prompt['title']}"
        f"{favorite_mark} (조회수: {prompt['use_count']})"
    )


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


# 번호로 프롬프트 인덱스를 선택하는 공통 함수입니다.
# 상세 보기, 수정, 삭제, 즐겨찾기 관리에서 같은 번호 검증 로직을 재사용합니다.
def get_prompt_index_by_number(prompts, message="번호 입력: "):
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

    return number - 1


# 번호로 프롬프트를 선택하는 공통 함수입니다.
def get_prompt_by_number(prompts, message="번호 입력: "):
    prompt_index = get_prompt_index_by_number(prompts, message)
    if prompt_index is None:
        return None
    return prompts[prompt_index]


# 상세 보기 기능입니다.
# 선택한 프롬프트의 전체 내용을 출력하고 조회수를 1 증가시킵니다.
def show_prompt_detail(prompts):
    print("\n=== 프롬프트 상세 보기 ===")
    show_list(prompts)
    prompt = get_prompt_by_number(prompts)
    if prompt is None:
        return

    prompt["use_count"] += 1
    save_prompts(prompts)

    print("\n=== 상세 내용 ===")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {'예' if prompt['favorite'] else '아니오'}")
    print(f"조회수: {prompt['use_count']}")
    print("내용:")
    print(prompt["content"])


# 프롬프트 수정 기능입니다.
# 제목, 내용, 카테고리를 바꾸되 빈 입력은 기존 값을 유지합니다.
def edit_prompt(prompts):
    print("\n=== 프롬프트 수정 ===")
    show_list(prompts)
    prompt_index = get_prompt_index_by_number(prompts, "수정할 번호 입력: ")
    if prompt_index is None:
        return

    prompt = prompts[prompt_index]
    prompt["title"] = get_updated_title(prompts, prompt["title"], prompt_index)
    prompt["content"] = get_optional_input("새 내용", prompt["content"])
    prompt["category"] = choose_category(prompt["category"])
    save_prompts(prompts)
    print("프롬프트가 수정되었습니다.")


# 프롬프트 삭제 기능입니다.
# 삭제 전 확인 질문을 두어 실수로 데이터를 지우는 것을 막습니다.
def delete_prompt(prompts):
    print("\n=== 프롬프트 삭제 ===")
    show_list(prompts)
    prompt_index = get_prompt_index_by_number(prompts, "삭제할 번호 입력: ")
    if prompt_index is None:
        return

    prompt = prompts[prompt_index]
    confirm = input(f"'{prompt['title']}' 프롬프트를 삭제할까요? (y/n): ").strip().lower()
    if confirm != "y":
        print("삭제를 취소했습니다.")
        return

    deleted_prompt = prompts.pop(prompt_index)
    save_prompts(prompts)
    print(f"'{deleted_prompt['title']}' 프롬프트를 삭제했습니다.")


# 즐겨찾기 추가/해제 기능입니다.
# 선택한 프롬프트의 favorite 값을 True와 False 사이에서 바꿉니다.
def toggle_favorite(prompts):
    print("\n=== 즐겨찾기 관리 ===")
    show_list(prompts)
    prompt = get_prompt_by_number(prompts)
    if prompt is None:
        return

    prompt["favorite"] = not prompt["favorite"]
    save_prompts(prompts)
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


# 조회수 기준 Top 목록 기능입니다.
# 상세 보기를 많이 한 프롬프트가 위에 오도록 정렬해서 보여줍니다.
def show_top_prompts(prompts):
    print("\n=== 조회수 Top 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    sorted_prompts = sorted(prompts, key=lambda prompt: prompt["use_count"], reverse=True)
    for index, prompt in enumerate(sorted_prompts, start=1):
        print_prompt_summary(index, prompt)


# 전체 프롬프트를 카테고리별 Markdown 파일로 내보냅니다.
# 제출물에는 코드만 올리고, 실행 결과 파일은 로컬에서 생성되도록 분리했습니다.
def export_prompts_to_markdown(prompts):
    print("\n=== Markdown 내보내기 ===")
    EXPORT_DIR.mkdir(exist_ok=True)

    lines = ["# 프롬프트 목록", ""]
    categories = sorted({prompt["category"] for prompt in prompts})
    for category in categories:
        lines.append(f"## {category}")
        lines.append("")
        category_prompts = [prompt for prompt in prompts if prompt["category"] == category]
        for prompt in category_prompts:
            favorite_text = "예" if prompt["favorite"] else "아니오"
            lines.append(f"### {prompt['title']}")
            lines.append("")
            lines.append(f"- 즐겨찾기: {favorite_text}")
            lines.append(f"- 조회수: {prompt['use_count']}")
            lines.append("")
            lines.append(prompt["content"])
            lines.append("")

    EXPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Markdown 파일로 내보냈습니다: {EXPORT_FILE}")


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
    print("8. 프롬프트 수정")
    print("9. 프롬프트 삭제")
    print("10. 조회수 Top 목록")
    print("11. Markdown 내보내기")
    print("0. 종료")


# 프로그램의 전체 실행 흐름을 담당하는 함수입니다.
# JSON 파일에서 데이터를 불러오고, 종료 전까지 메뉴를 반복합니다.
def run():
    prompts = load_prompts()

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
        elif choice == "8":
            edit_prompt(prompts)
        elif choice == "9":
            delete_prompt(prompts)
        elif choice == "10":
            show_top_prompts(prompts)
        elif choice == "11":
            export_prompts_to_markdown(prompts)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    run()
