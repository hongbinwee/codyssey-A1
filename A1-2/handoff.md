# A1-2 Handoff

## 현재 상태

- A1-2 미션 전용 폴더를 생성했다.
- 미션 원문을 분석하고 산출물 제작으로 연결하기 위한 기본 문서를 만들었다.
- 미션 원문 기준으로 OpenAI 계열 API + Kakao Local API 조합을 선택했다.
- CLI 프로그램 `travel_planner.py`와 제출용 `README.md`를 작성했다.

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

- 번들 Python으로 `travel_planner.py --help` 실행 확인 완료.
- 잘못된 날짜 입력 시 argparse 사용법과 오류 메시지 출력 확인 완료.
- `ast.parse()` 방식으로 문법 검증 완료.
- API 키가 없을 때 `OPENAI_API_KEY` 설정 안내 후 종료하는 동작 확인 완료.
- 실제 OpenAI/Kakao API 호출은 API 키가 없어 아직 실행하지 않았다.

## 다음 작업

1. 실제 API 키를 `A1-2/.env` 또는 환경변수로 설정한다.
2. `python travel_planner.py --date "2026-03-15"` 형태로 실제 API 호출을 검증한다.
3. 생성된 `results/YYYY-MM-DD_raw.json`과 `results/YYYY-MM-DD_travel_plan.md`를 확인한다.
4. 필요하면 실행 결과 스크린샷을 추가한다.

## 주의사항

- 미션 원문에 없는 조건을 임의로 추가하지 않는다.
- 모호한 조건은 질문으로 남긴다.
- AI가 만든 분석 결과는 `pre_submission_checklist.md` 기준으로 다시 검토한다.
