# Git 작업 가이드

현재 상태:
- 로컬 Git 저장소 초기화 완료
- 기본 브랜치: `main`
- 첫 커밋 완료
- 원격 `origin/main` 연결 완료
- `feature/a1-1-list-view` 브랜치 생성 및 `main` 병합 완료
- `user.name = codex_hongbin`
- `user.email = project99hong@gmail.com`

## 1. 사용자 정보 설정
현재 저장소에는 이미 아래 정보가 설정되어 있습니다.

```bash
git config user.name "codex_hongbin"
git config user.email "project99hong@gmail.com"
```

## 2. 다음 커밋 추천 순서
```bash
git add A1-1/main_a1_1.py
git commit -m "feat: improve prompt manager flow"
```

## 3. 10개 커밋 예시
1. `chore: initialize codyssey a1 workspace`
2. `feat: add default prompt data`
3. `feat: implement main menu`
4. `feat: add prompt creation flow`
5. `feat: implement prompt list view`
6. `feat: add category filter`
7. `feat: implement keyword search`
8. `feat: add prompt detail view`
9. `feat: implement favorites toggle and list`
10. `docs: write readme and submission checklist`

현재 구현 이력에는 `main_a1_1.py` 기준으로 메뉴, 기본 데이터, 프롬프트 추가, 목록, 카테고리 조회, 검색, 상세 보기, 즐겨찾기 관리 기능이 기능 단위 커밋으로 쌓여 있습니다.

## 4. 브랜치 생성 및 병합 예시
목록 기능을 별도 브랜치에서 작업한 기록을 남기고 싶다면:

```bash
git checkout -b feature/prompt-list
git add A1-1/main_a1_1.py
git commit -m "feat: implement prompt list view"
git checkout main
git merge feature/prompt-list
```

## 5. GitHub 연결 예시
현재 저장소는 이미 아래 원격과 연결되어 있습니다.

```bash
git remote -v
```

연결된 원격:

- `origin https://github.com/hongbinwee/codyssey-A1.git`

## 6. 제출용 캡처 추천 순서
1. VSCode 화면과 Python 버전
2. Git 버전과 사용자 설정
3. 프로그램 실행 화면
4. 프롬프트 추가 / 검색 / 즐겨찾기 화면
5. `git log --oneline --graph` 화면
