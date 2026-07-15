# 나만의 프롬프트 관리 프로그램

파이썬으로 만든 콘솔 기반 프롬프트 관리 프로그램입니다. 메뉴 번호를 입력해 프롬프트를 추가하고, 목록을 확인하고, 카테고리별 조회, 검색, 상세 보기, 즐겨찾기 관리를 할 수 있습니다.

## 프로젝트 위치

이 미션의 실제 산출물은 `A1-1/` 폴더 안에서 관리합니다.

- 실행 파일: `main_a1_1.py`
- 미션 요약: `mission_summary.md`
- 제출 체크리스트: `submission_checklist.md`
- Git 작업 가이드: `git_workflow_guide.md`
- 작업 인계 문서: `handoff.md`
- 진행 Spec: `spec.md`

## 실행 방법
1. Python 3.10 이상이 설치되어 있는지 확인합니다.
2. 터미널에서 작업공간 루트로 이동합니다.
3. 아래 명령어로 `A1-1` 폴더 안의 프로그램을 실행합니다.

```bash
cd A1-1
python3 main_a1_1.py
```

문법 검증은 아래처럼 할 수 있습니다.

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

## 기본 데이터 설명
프로그램 시작 시 아래 성격의 기본 프롬프트가 포함됩니다.
- 텍스트 생성
- 이미지 생성
- 자동화

기본 데이터는 예시 프롬프트 3개로 구성되어 있으며, 모두 리스트와 딕셔너리를 사용해 저장합니다.

## 요구사항 대응 요약

- 콘솔 메뉴 기반 프로그램
- 기본 프롬프트 3개 포함
- 리스트와 딕셔너리 사용
- 기능별 함수 분리
- 목록, 카테고리 조회, 검색, 상세 보기, 즐겨찾기 기능 포함
- 잘못된 입력 안내 처리 포함
- 데이터는 프로그램 실행 중에만 유지

## 사용한 코드 구조
기능별로 함수를 분리했습니다.
- `show_menu()`
- `add_prompt()`
- `show_list()`
- `show_categories()`
- `search_prompt()`
- `show_prompt_detail()`
- `toggle_favorite()`
- `show_favorites()`

## 카테고리 목록
- 텍스트 생성
- 이미지 생성
- 영상 생성
- 페르소나
- 자동화
- 기타

## 제출 전에 확인할 것
- 프로그램 실행 화면 캡처
- 프롬프트 추가 화면 캡처
- 목록/검색/즐겨찾기 결과 캡처
- 개발 환경 설정 화면 캡처
- `git log --oneline --graph` 캡처

## 스크린샷 증빙 파일

스크린샷은 `스크린샷/` 폴더 안에서 관리합니다.

- `01-python-version-hello.png`: Python 버전 확인 및 `print("Hello")` 실행 화면
- `02-git-init-remote.png`: Git 저장소 초기화 및 원격 저장소 연결 화면
- `03-git-commit-log-practice.png`: Git commit/log 연습 화면
- `04-git-push-origin-main.png`: 원격 저장소 push 및 upstream 설정 화면
- `05-gitignore-readme-push.png`: `.gitignore`, README 작성 및 push 작업 화면
- `06-github-repository-initial.png`: GitHub 저장소 화면
- `07-final-git-log-graph.png`: 최종 `git log --oneline --graph --decorate` 화면

프로그램 메뉴, 프롬프트 추가, 목록, 검색, 즐겨찾기 실행 결과 화면은 추가 캡처가 필요합니다.

## Git 작업 상태
- `main_a1_1.py` 기준으로 기능 단위 커밋을 쌓았습니다.
- `feature/a1-1-list-view` 브랜치에서 목록 기능을 구현한 뒤 `main`으로 병합했습니다.
- 최종 제출 전 `git log --oneline --graph` 화면을 캡처하면 커밋 흐름과 브랜치 병합 기록을 함께 확인할 수 있습니다.
