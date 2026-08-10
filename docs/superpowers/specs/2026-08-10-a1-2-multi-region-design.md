# A1-2 복수 지역 추천 보너스 설계

## 목표

기존 단일 지역 여행 추천 CLI를 유지하면서 `--multi-region` 선택 모드에서 2~3개 국내 지역을 추천하고, 지역별 Kakao 맛집 검색 결과와 최종 리포트를 생성한다.

## 모드 구분

- 기본 모드: 기존 실행 명령을 그대로 사용하며 `recommended_city`와 `restaurants`를 사용한다.
- 복수 지역 모드: `--multi-region`을 지정할 때만 활성화하며 `recommended_cities`, `region_details`, `restaurants_by_city`를 사용한다.
- 선택 옵션이므로 기본 과제에 새로운 필수 입력 조건을 추가하지 않는다.

## 복수 지역 추천 스키마

```json
{
  "recommended_cities": ["제주", "강릉", "부산"],
  "region_details": [
    {
      "city": "제주",
      "weather": "...",
      "events": ["..."],
      "reason": "두 문장 이상의 추천 이유입니다."
    }
  ]
}
```

`recommended_cities`는 중복 없는 문자열 2~3개여야 하며, `region_details`는 모든 지역을 정확히 한 번씩 설명해야 한다. 각 지역의 `events`는 1~3개 문자열, `reason`은 2~4문장으로 검증한다.

## 결과와 캐시

복수 지역 raw JSON은 다음 필드를 가진다.

```json
{
  "date": "YYYY-MM-DD",
  "mode": "multi",
  "recommendation": {"recommended_cities": [], "region_details": []},
  "restaurants_by_city": {"제주": [], "강릉": [], "부산": []},
  "errors": []
}
```

기존 raw JSON에 `mode`가 없으면 단일 모드로 해석한다. 복수 모드는 `mode=multi`와 복수 지역 필드를 모두 만족하는 캐시만 재사용한다. 모드가 다르거나 JSON 구조가 손상되면 캐시를 무시하고 API 흐름을 다시 실행한다. Markdown이 없거나 필수 섹션이 없으면 API 없이 fallback 리포트를 재생성한다.

## 오류 처리

지역별 검색은 순서대로 반복한다. 한 지역의 결과가 0건이면 해당 지역 목록을 빈 배열로 저장하고 `EMPTY_RESULT`를 기록한다. HTTP·네트워크 오류도 해당 지역을 포함한 `errors` 항목으로 저장한 뒤 다음 지역 검색을 계속한다.

## 리포트

복수 지역 리포트는 지역별 추천 정보, 지역별 날씨·행사, 지역별 맛집을 구분한다. 모든 모드에서 `1일 일정 제안`과 `오류 요약(errors)`을 포함하며, 누락 시 fallback 리포트로 대체한다.

## 검증 범위

- 기존 단일 지역 JSON·검색·리포트·캐시 회귀
- 복수 지역 JSON 파싱 및 2~3개 개수 검증
- 3개 지역 반복 검색
- 한 지역 0건 및 한 지역 API 오류 후 다음 지역 처리
- 복수 지역 캐시 재사용과 단일/복수 형식 불일치 재실행
- 복수 지역 Markdown 필수 섹션 검증
- 외부 API 호출 없이 모든 테스트 실행
