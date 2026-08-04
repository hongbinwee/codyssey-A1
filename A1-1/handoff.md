# A1-1 handoff

## 1. 현재 미션 상태

- 현재 작업공간은 `Codyssey_A1`
- 활성 미션 폴더는 `A1-1/`
- A1-1 미션은 `파이썬 콘솔 기반 프롬프트 관리 프로그램 제작 + Git/GitHub 작업 이력 제출` 과제
- 기초 구현, 제출용 README 통합, GitHub 업로드, Git 로그와 프로그램 실행 스크린샷 정리는 완료됨
- 이 문서는 데스크톱과 현재 작업환경에서 함께 이어가기 위한 GitHub 공유 인계 문서임
- 현재 필수 미완료 작업은 없으며, 새 작업을 시작할 때 Git 상태와 이 문서를 먼저 확인함

## 2. 현재 파일 구조

### 루트

- `AGENTS.md`
- `.gitignore`

### A1-1 폴더

- `README.md`
- `main_a1_1.py`
- `스크린샷/`
- `handoff.md` (GitHub 공유 인계 문서)

## 3. 이미 완료된 작업

- 미션 1~11단계 요약 문서 작성 완료
- 콘솔 프로그램 기본 구현 완료
- README 최종 제출 문서 통합 완료
- 실행 파일명을 `main_a1_1.py`로 확정 완료
- `main.py`는 최신 산출물에서 제거하고 `main_a1_1.py` 기준으로 정리 완료
- 로컬 Git 저장소 `main` 브랜치로 초기화 완료
- 프로그램 실행 검증 완료
- `PYTHONPYCACHEPREFIX=/tmp/codyssey-a1-pycache python3 -m py_compile main_a1_1.py` 검증 완료
- `feature/a1-1-list-view` 브랜치 생성 및 `main` 병합 완료
- `main_a1_1.py` 기능 단위 구현 커밋 진행 완료
- 보조 문서 내용을 README에 통합하고 불필요한 md 파일 정리 완료
- `handoff.md`를 GitHub 공유 인계 문서로 전환
- `스크린샷/07-final-git-log-graph.png` 최종 Git 로그 스크린샷 추가 완료
- `main_a1_1.py`에 함수 분리 기준과 각 함수 역할 설명 주석 추가 완료

## 4. 현재 프로그램 구현 상태

`A1-1/main_a1_1.py`에 아래 기능이 구현되어 있음.

- 프롬프트 추가
- 중복 제목 방지
- 전체 목록 보기
- 카테고리별 조회
- 키워드 검색
- 상세 보기
- 즐겨찾기 추가/해제
- 즐겨찾기 목록
- 잘못된 입력 처리
- 기본 프롬프트 3개 포함
- 기능별 함수 분리 및 설명 주석 포함

프롬프트 데이터는 `prompts.json`에 저장하며, 프로그램 시작 시 불러옴.
추가로 수정/삭제, 조회수 기록과 Top 목록, 카테고리별 Markdown 내보내기 기능이 구현되어 있음.

## 5. 현재 남은 작업

현재 필수 미완료 작업은 없음.
새로운 작업을 시작할 때는 먼저 아래 순서로 확인함.

1. `git status --short --branch`로 로컬 변경사항 확인
2. 필요하면 `git fetch origin --prune` 후 원격 변경사항 확인
3. 다른 컴퓨터에서 작업한 변경사항이 있으면 `git pull --ff-only origin main` 실행
4. 작업 후 검증하고 의미 있는 단위로 커밋 및 push

## 6. 다음 에이전트가 먼저 확인할 것

- GitHub에 올라가는 A1-1 파일은 `README.md`, `main_a1_1.py`, `스크린샷/`, `handoff.md`임
- `prompts.json`과 `exports/`는 실행 중 생성되는 로컬 데이터라 `.gitignore`로 제외함
- 루트는 작업공간 안내와 Git 루트 역할로 유지하면 됨
- 사용자는 미션별 폴더 정리를 중요하게 생각함
- 여러 파일을 동시에 바꾸는 작업이면 먼저 Spec 또는 간단한 계획을 세우는 것이 루트 규칙에 맞음

## 7. 데스크톱에서 작업 이어가기

새 컴퓨터에서 저장소를 처음 받는 경우:

```bash
git clone https://github.com/hongbinwee/codyssey-A1.git
cd codyssey-A1
git status --short --branch
```

이미 clone한 저장소라면:

```bash
git status --short --branch
git pull --ff-only origin main
```

그다음 `AGENTS.md`, `A1-1/README.md`, `A1-1/handoff.md`를 읽고 `A1-1/`에서 작업을 시작함.

## 8. 실행 및 검증 방법

프로그램 실행:

```bash
cd A1-1
python3 main_a1_1.py
```

문법 검증:

```bash
cd A1-1
PYTHONPYCACHEPREFIX=/tmp/codyssey-a1-pycache python3 -m py_compile main_a1_1.py
```

Git 상태 확인:

```bash
git status --short --branch
```

## 9. 확인된 현재 상태

- Git 저장소는 생성되어 있음
- GitHub `origin/main`과 연결되어 있음
- 현재 `main`은 원격 추적 상태임
- `user.name = codex_hongbin`
- `user.email = project99hong@gmail.com`
- GitHub 원격 저장소는 `origin`으로 연결되어 있음
- 작업 재개 전 `git fetch origin --prune`으로 원격 상태를 새로 확인함

## 10. 작업 시 주의사항

- 미션별 산출물은 가능한 한 해당 미션 폴더 기준으로 정리
- README 안의 경로 설명은 실제 파일 위치와 반드시 맞춰야 함
- 원문에 없는 제출 조건은 추가하지 않기
- 사용자가 초보자 제출 흐름을 중요하게 보므로 문서는 실행 순서가 보이게 유지하기
- `handoff.md`는 GitHub에 공유하는 인계 문서이므로 작업 상태가 바뀌면 함께 갱신함
- `prompts.json`과 `exports/`는 로컬 실행 데이터이므로 GitHub에 올리지 않음
