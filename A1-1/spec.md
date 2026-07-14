# A1-1 제출물 완성 Spec

## 목표

`A1-1` 미션 산출물을 하나의 폴더 안에서 일관되게 관리하고, 제출에 필요한 코드, 문서, Git 작업 흐름을 완성 가능한 상태로 정리한다.

## 입력 자료

- 미션 안내문 기반 요약: `mission_summary.md`
- 현재 프로그램 코드: `A1-1/main_a1_1.py`
- 현재 제출 안내 문서: `README.md`, `submission_checklist.md`, `git_workflow_guide.md`, `handoff.md`
- 루트 작업 규칙: `../AGENTS.md`

## 작업 단계

1. 실행 파일을 `A1-1/main_a1_1.py`로 관리한다.
2. 현재 파일명 기준으로 실행 명령과 문서 경로를 수정한다.
3. `README.md`, `handoff.md`, `submission_checklist.md`, `git_workflow_guide.md`를 현재 구조 기준으로 정리한다.
4. `A1-1` 폴더 기준으로 프로그램 실행과 문법 검증을 다시 수행한다.
5. 이후 제출물 완성 작업의 다음 우선순위를 정리한다.

## 산출물

- `A1-1/main_a1_1.py`
- 현재 구조를 반영한 `A1-1/README.md`
- 현재 구조를 반영한 `A1-1/handoff.md`
- 현재 구조를 반영한 `A1-1/submission_checklist.md`
- 현재 구조를 반영한 `A1-1/git_workflow_guide.md`
- 진행 기준 문서 `A1-1/spec.md`

## 검증 방법

- `cd A1-1 && python3 main_a1_1.py`
- `cd A1-1 && PYTHONPYCACHEPREFIX=/tmp/codyssey-a1-pycache python3 -m py_compile main_a1_1.py`
- `rg -n "main_a1_1.py|python3 main_a1_1.py|A1-1/" A1-1 AGENTS.md`
- `git status --short`

## 확인 질문

- 실행 파일과 문서를 모두 `A1-1/` 안으로 모으는 구조로 확정하는가
- 루트에는 `AGENTS.md`, `.gitignore`, `.git/` 정도만 남겨도 되는가
- 이후 커밋 분할 작업도 `A1-1` 기준으로 진행할 것인가
