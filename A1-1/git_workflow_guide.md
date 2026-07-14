# Git 작업 가이드

현재 상태:
- 로컬 Git 저장소 초기화 완료
- 기본 브랜치: `main`
- 아직 커밋 없음
- `user.name`, `user.email` 설정 필요
- 원격 GitHub 저장소 연결 필요

## 1. 사용자 정보 설정
아래 명령어의 값을 본인 정보로 바꿔서 실행하세요.

```bash
git config --global user.name "본인 이름"
git config --global user.email "본인 이메일"
```

## 2. 첫 커밋 전 추천 순서
```bash
git add .
git commit -m "chore: initialize prompt manager project"
```

## 3. 10개 커밋 예시
1. `chore: initialize prompt manager project`
2. `feat: add default prompt data`
3. `feat: implement main menu`
4. `feat: add prompt creation flow`
5. `feat: implement prompt list view`
6. `feat: add category filter`
7. `feat: implement keyword search`
8. `feat: add prompt detail view`
9. `feat: implement favorites toggle and list`
10. `docs: write readme and submission checklist`

## 4. 브랜치 생성 및 병합 예시
목록 기능을 별도 브랜치에서 작업한 기록을 남기고 싶다면:

```bash
git checkout -b feature/prompt-list
git add main.py
git commit -m "feat: implement prompt list view"
git checkout main
git merge feature/prompt-list
```

## 5. GitHub 연결 예시
GitHub에서 새 저장소를 만든 뒤 아래처럼 연결합니다.

```bash
git remote add origin <GitHub 저장소 URL>
git push -u origin main
```

## 6. 제출용 캡처 추천 순서
1. VSCode 화면과 Python 버전
2. Git 버전과 사용자 설정
3. 프로그램 실행 화면
4. 프롬프트 추가 / 검색 / 즐겨찾기 화면
5. `git log --oneline --graph` 화면
