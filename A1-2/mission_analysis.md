# A1-2 Mission Analysis

## 미션 핵심 요약

- 미션 이름: 인터넷 정보를 받아와서 여행지 추천해주는 파이썬 프로그램 만들기
- 분야: AI 활용 학습
- 학습 시간: 40시간
- 핵심 목표: LLM API와 지도/장소 검색 API를 연결해 국내 여행 추천 CLI 프로그램을 만든다.
- 입력: `-date "YYYY-MM-DD"` 또는 `--date "YYYY-MM-DD"`
- 출력: 진행 로그, 결과 저장 경로, 원본 JSON, 최종 Markdown 여행 리포트
- 구현 방식: Python 3.10 이상, 터미널에서 실행되는 CLI 프로그램
- 선택한 API 제공자: OpenAI 계열 API + Kakao Local API

## 필수 산출물 정리

| 필수 산출물 | 원문 근거 | 완료 기준 | 상태 |
| --- | --- | --- | --- |
| CLI 기반 Python 프로그램 | "CLI 기반 Python 프로그램" | `argparse`로 날짜 옵션을 받아 실행된다. | 완료 |
| 실행 결과 원본 JSON | "원본 데이터 JSON 1개 이상" | 1차 추천 JSON, 맛집 검색 결과, 오류 요약이 들어간다. | 구현 완료, API 키 설정 후 생성 |
| 최종 여행 리포트 Markdown | "최종 여행 리포트 Markdown 1개" | 추천 지역, 날씨, 행사, 맛집, 1일 일정, 오류 요약이 포함된다. | 구현 완료, API 키 설정 후 생성 |
| README.md | "프로그램 개요, 실행 방법, API 키 설정 방법..." | 실행/키 설정/결과 확인/보안 주의가 적혀 있다. | 완료 |

## 선택/보너스 과제 정리

| 선택/보너스 과제 | 원문 근거 | 진행 여부 |
| --- | --- | --- |
| 복수 지역 추천 | recommended_city를 2~3개로 확장 | 이번 기본 제출에서는 제외 |
| 결과 캐싱 | 같은 `-date` 재실행 시 기존 JSON 활용 | 이번 기본 제출에서는 제외 |

보너스 과제는 필수가 아니므로 기본 제출 완성 후 여유가 있을 때만 추가한다.

## 추천 진행 순서

1. CLI 인자와 날짜 검증을 먼저 만든다.
2. API 키를 `.env` 또는 환경변수에서 읽는다.
3. OpenAI API로 1차 추천 JSON을 생성한다.
4. JSON 파싱 실패 시 1회만 재시도한다.
5. Kakao Local API로 추천 도시의 맛집을 검색한다.
6. 장소 검색 실패나 0건은 "데이터 없음"으로 처리한다.
7. OpenAI API로 최종 Markdown 리포트를 생성한다.
8. 원본 JSON과 Markdown 리포트를 `results/`에 저장한다.
9. README와 요구사항 대응표를 실제 구현 기준으로 정리한다.
10. 문법 검증과 Git 상태 확인 후 제출한다.

## 기능 요구사항 체크

| 기능 요구사항 | 필수 여부 | 구현 위치 | 검증 방법 | 상태 |
| --- | --- | --- | --- | --- |
| `argparse` CLI | 필수 | `travel_planner.py` | `python travel_planner.py --help` | 완료 |
| `-date` 날짜 입력 | 필수 | `parse_args()` | 잘못된 날짜 입력 테스트 | 완료 |
| OpenAI 계열 API 연동 | 필수 | `call_openai_chat()` | API 키 설정 후 실행 | 구현 완료 |
| LLM 1차 결과 JSON 파싱 | 필수 | `generate_recommendation()` | 원본 JSON 저장 확인 | 구현 완료 |
| Kakao Local 맛집 검색 | 필수 | `search_kakao_restaurants()` | 맛집 리스트 또는 0건 처리 확인 | 구현 완료 |
| 검색 결과 0건 처리 | 필수 | `search_kakao_restaurants()` | `restaurants: []` 상태로 리포트 생성 | 구현 완료 |
| 최종 Markdown 리포트 생성 | 필수 | `generate_report()` | `.md` 파일 생성 확인 | 구현 완료 |
| API/파싱 오류 처리 | 필수 | 각 API 함수 | 오류 목록 `errors` 확인 | 구현 완료 |
| API 키 보안 | 필수 | `.env.example`, README | 실제 키 미포함 확인 | 완료 |
| 결과 저장 | 필수 | `save_outputs()` | `results/` 파일 확인 | 구현 완료 |

## 제출물 구조 설계

```text
A1-2/
├── README.md
├── travel_planner.py
├── .env.example
├── results/
│   └── .gitkeep
├── mission_analysis.md
├── pre_submission_checklist.md
├── mission_brief_template.md
├── SPEC.md
└── handoff.md
```

## AI 결과 오류, 과장, 누락 검토

| 검토 항목 | 점검 결과 | 수정 필요 여부 |
| --- | --- | --- |
| 원문에 없는 조건을 만들어냈는가? | OpenAI + Kakao 조합은 원문에서 허용한 택1 제공자다. | 없음 |
| 필수 산출물을 빠뜨렸는가? | CLI, JSON, Markdown, README를 모두 산출물에 포함했다. | 없음 |
| 기능 요구사항을 잘못 해석했는가? | `-date`와 `--date`를 모두 지원해 원문과 예시를 함께 만족시킨다. | 없음 |
| 모호한 부분을 확인 질문 없이 단정했는가? | 보너스 과제는 제외로 표시했고 필수처럼 다루지 않았다. | 없음 |
| 어려운 개념을 사용자 수준에 맞게 설명했는가? | README에서 REST API, API 키, 오류 처리를 쉬운 말로 설명한다. | 진행 중 |
| 참고자료 링크를 지어냈는가? | 현재 참고자료 링크를 임의로 추가하지 않았다. | 없음 |

## 제출 전 점검

- [x] `python travel_planner.py --help`가 동작한다.
- [x] 잘못된 날짜를 입력하면 사용법을 출력하고 종료한다.
- [x] `.env.example`에는 실제 키가 없다.
- [x] `README.md`에 API 키 설정 방법이 있다.
- [ ] `results/`에 원본 JSON과 최종 Markdown이 생성된다. API 키 설정 후 확인 필요.
- [ ] `errors` 배열이 원본 JSON에 포함된다. API 키 설정 후 확인 필요.
- [x] Git 상태에서 불필요한 임시 파일이 없다.
