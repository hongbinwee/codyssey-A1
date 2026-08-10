# A1-2 Handoff

## 현재 상태

- A1-2 미션 원문을 `A1-2 미션 원문.md`로 보존했다.
- OpenAI 계열 API + Kakao Local API 조합을 사용한다.
- `travel_planner.py`에 GPT-5 모델 호환 요청, 추천 JSON 검증, JSON 오류 1회 재시도, 장소 검색 추상화, 도시명 정규화, raw JSON 기준 날짜별 결과 캐시, Markdown 필수 섹션 검증, 저장 오류 기록을 반영했다.
- API 키는 로컬 `.env`에만 있으며 문서·코드·결과에는 기록하지 않는다.

## 생성한 문서

- `SPEC.md`
- `README.md`
- `mission_brief_template.md`
- `pre_submission_checklist.md`
- `handoff.md`
- `mission_analysis.md`
- `.env.example`
- `travel_planner.py`
- `results/.gitkeep`

## 검증 결과

- `python3 -m unittest discover -s A1-2/tests -v`: 12개 통과.
- `python3 -m py_compile A1-2/travel_planner.py`: 확인 필요.
- `--help`, 잘못된 날짜, 키 누락 동작: 기존 확인 완료.
- 실제 OpenAI/Kakao 실행: OpenAI 추천·최종 리포트는 성공했고, Kakao는 `HTTP 403`이 발생했다. 응답 원인은 앱의 `OPEN_MAP_AND_LOCAL` 서비스 비활성화이며, 프로그램은 `데이터 없음`으로 계속 진행해 결과 파일을 저장했다.
- 캐시 보완: raw JSON만 있고 Markdown이 없는 경우에도 API 없이 fallback Markdown을 생성하도록 회귀 테스트로 확인했다.

## 다음 작업

1. `python3 -m py_compile A1-2/travel_planner.py`를 실행한다.
2. `A1-2/.env`의 키 존재 여부만 확인한다(`SET/MISSING` 방식).
3. `python3 travel_planner.py --date "2026-03-15"`를 실행한다.
4. 생성된 raw JSON·Markdown의 필수 구조와 오류 기록을 확인한다.
5. 결과·문서·Git diff에 실제 키가 없는지 검사한다.

## 주의사항

- 미션 원문에 없는 조건을 임의로 추가하지 않는다.
- 모호한 조건은 질문으로 남긴다.
- AI가 만든 분석 결과는 `pre_submission_checklist.md` 기준으로 다시 검토한다.
