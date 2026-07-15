# 나만의 프롬프트 관리 프로그램

Codyssey A1-1 미션 산출물입니다. 파이썬 콘솔 프로그램으로 프롬프트를 추가하고, 목록 확인, 카테고리 조회, 검색, 상세 보기, 즐겨찾기 관리를 할 수 있습니다.

## 제출 정보

- GitHub 저장소: https://github.com/hongbinwee/codyssey-A1
- 미션 폴더: `A1-1/`
- 실행 파일: `main_a1_1.py`
- 스크린샷 폴더: `스크린샷/`

## 실행 방법

작업공간 루트에서 아래 명령어를 실행합니다.

```bash
cd A1-1
python3 main_a1_1.py
```

문법 검증:

```bash
cd A1-1
PYTHONPYCACHEPREFIX=/tmp/codyssey-a1-pycache python3 -m py_compile main_a1_1.py
```

## 주요 기능

- 프롬프트 추가
- 전체 프롬프트 목록 보기
- 카테고리별 조회
- 제목/내용 키워드 검색
- 프롬프트 상세 보기
- 즐겨찾기 추가 및 해제
- 즐겨찾기 목록 보기
- 중복 제목 입력 방지
- 잘못된 번호 및 빈 입력 안내

## 기본 데이터

프로그램 시작 시 기본 프롬프트 3개가 등록됩니다.

- 텍스트 생성: 블로그 글 작성 도우미
- 이미지 생성: 제품 썸네일 이미지 프롬프트
- 자동화: 뉴스 요약 자동화 프롬프트

데이터는 리스트와 딕셔너리로 관리하며, 프로그램 실행 중에만 유지됩니다.

## 요구사항 대응표

| 미션 요구사항 | 반영 내용 |
| --- | --- |
| Python 3.10 이상 사용 | Python 버전 확인 스크린샷 포함 |
| 콘솔 메뉴 기반 프로그램 | `main_a1_1.py` 실행 시 번호 선택 메뉴 제공 |
| 기본 프롬프트 3개 이상 | 기본 데이터 3개 포함 |
| 프롬프트 추가 | 제목, 내용, 카테고리 입력 후 등록 |
| 프롬프트 목록 | 번호, 카테고리, 제목, 즐겨찾기 표시 |
| 카테고리별 조회 | 선택한 카테고리의 프롬프트만 출력 |
| 검색 | 제목 또는 내용 키워드 검색 |
| 상세 보기 | 선택한 번호의 전체 내용 출력 |
| 즐겨찾기 관리 | 즐겨찾기 추가/해제 및 목록 보기 |
| 잘못된 입력 처리 | 빈 입력, 잘못된 번호, 잘못된 카테고리 안내 |
| 함수 분리 | 기능별 함수로 코드 구성 |
| Git 커밋 10개 이상 | 기능 단위 커밋 10개 이상 생성 |
| 브랜치 생성 및 병합 | `feature/a1-1-list-view` 브랜치 생성 후 `main`에 병합 |
| GitHub 업로드 | `origin/main`에 push 완료 |

## 코드 구조

- `create_default_prompts()`: 기본 프롬프트 데이터 생성
- `show_menu()`: 메뉴 출력
- `add_prompt()`: 프롬프트 추가
- `show_list()`: 전체 목록 출력
- `show_categories()`: 카테고리별 조회
- `search_prompt()`: 키워드 검색
- `show_prompt_detail()`: 상세 보기
- `toggle_favorite()`: 즐겨찾기 추가/해제
- `show_favorites()`: 즐겨찾기 목록 출력

## Git 작업 요약

- `main_a1_1.py` 기준으로 기능 단위 커밋을 쌓았습니다.
- `feature/a1-1-list-view` 브랜치에서 목록 기능을 구현한 뒤 `main`으로 병합했습니다.
- 최종 Git 로그는 `스크린샷/07-final-git-log-graph.png`에서 확인할 수 있습니다.

## 제출 스크린샷

### 1. Python 버전 확인 및 Hello 실행

![Python 버전 확인 및 Hello 실행](./스크린샷/01-python-version-hello.png)

### 2. Git 저장소 초기화 및 원격 저장소 연결

![Git 저장소 초기화 및 원격 저장소 연결](./스크린샷/02-git-init-remote.png)

### 3. Git commit/log 연습

![Git commit log 연습](./스크린샷/03-git-commit-log-practice.png)

### 4. 원격 저장소 push 및 upstream 설정

![원격 저장소 push 및 upstream 설정](./스크린샷/04-git-push-origin-main.png)

### 5. .gitignore, README 작성 및 push

![gitignore README push](./스크린샷/05-gitignore-readme-push.png)

### 6. GitHub 저장소 화면

![GitHub 저장소 화면](./스크린샷/06-github-repository-initial.png)

### 7. 최종 git log 그래프

![최종 git log 그래프](./스크린샷/07-final-git-log-graph.png)

## 남은 제출 전 확인

- 프로그램 메뉴 화면 캡처
- 프롬프트 추가 완료 화면 캡처
- 목록, 검색, 즐겨찾기 화면 캡처
