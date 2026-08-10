# A1-2 크로스 체크 후속 수정 계획

## 목표

이전 보안·미션 산출물 점검에서 확인한 문서 불일치를 해소하고, 날짜별 캐시 재사용 시 오래되거나 불완전한 Markdown이 그대로 사용되지 않도록 보완한다.

## 범위

1. `A1-2/README.md`, `A1-2/mission_analysis.md`, `A1-2/handoff.md`, `A1-2/pre_submission_checklist.md`의 캐시 보너스·검증 상태를 실제 구현과 일치시킨다.
2. `A1-2/travel_planner.py`의 캐시 로딩 시 기존 Markdown 필수 섹션을 검증하고, 누락 시 fallback Markdown을 재생성한다.
3. `A1-2/tests/test_travel_planner.py`에 잘못된 캐시 Markdown 회귀 테스트를 추가한다.
4. 루트 PNG, `.env`, `results/` 생성 파일은 커밋·푸시하지 않는다.

## 검증 기준

- 외부 API를 호출하지 않는 테스트가 모두 통과한다.
- `py_compile`이 통과한다.
- 같은 날짜의 불완전한 캐시 Markdown이 fallback으로 교체되는 테스트가 통과한다.
- README·mission_analysis·handoff·checklist의 상태가 서로 일치한다.
- 선택 파일만 스테이징하고 원격 브랜치에 푸시한다.
