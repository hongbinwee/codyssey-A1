import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib import error, parse, request


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
KAKAO_KEYWORD_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"


def load_dotenv(env_path):
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Recommend a Korean travel destination and create a Markdown travel report."
    )
    parser.add_argument(
        "-date",
        "--date",
        required=True,
        help='Travel date in YYYY-MM-DD format. Example: --date "2026-03-15"',
    )
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        parser.error('date must use YYYY-MM-DD format. Example: --date "2026-03-15"')

    return args


def require_env(name, setup_hint):
    value = os.getenv(name)
    if value:
        return value

    print(f"Error: {name} is not set.")
    print(setup_hint)
    sys.exit(1)


def call_json_api(url, method="GET", headers=None, payload=None, timeout=30):
    body = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = request.Request(url, data=body, method=method, headers=headers or {})
    with request.urlopen(req, timeout=timeout) as response:
        text = response.read().decode("utf-8")
        return json.loads(text)


def call_openai_chat(api_key, model, messages, temperature=0.4):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = call_json_api(
        OPENAI_CHAT_COMPLETIONS_URL,
        method="POST",
        headers=headers,
        payload=payload,
        timeout=60,
    )
    return data["choices"][0]["message"]["content"]


def extract_json_object(text):
    cleaned = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)```", cleaned, flags=re.DOTALL)
    if fence_match:
        cleaned = fence_match.group(1).strip()

    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last != -1 and first < last:
        cleaned = cleaned[first : last + 1]

    parsed = json.loads(cleaned)
    validate_recommendation(parsed)
    return parsed


def validate_recommendation(data):
    required = {
        "recommended_city": str,
        "weather": str,
        "events": list,
        "reason": str,
    }
    for key, expected_type in required.items():
        if key not in data:
            raise ValueError(f"missing key: {key}")
        if not isinstance(data[key], expected_type):
            raise ValueError(f"{key} must be {expected_type.__name__}")

    if not all(isinstance(item, str) for item in data["events"]):
        raise ValueError("events must be an array of strings")


def generate_recommendation(api_key, model, travel_date, errors):
    system_prompt = (
        "You are a Korean domestic travel recommendation assistant. "
        "Return only a JSON object. Do not wrap it in Markdown."
    )
    user_prompt = f"""
Recommend one Korean city for a trip on {travel_date}.

Return JSON only with this exact schema:
{{
  "recommended_city": "string",
  "weather": "string",
  "events": ["string", "string"],
  "reason": "2-4 Korean sentences"
}}

The weather and event information can be a general seasonal estimate.
Do not include API keys, citations, or unverified links.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        first_response = call_openai_chat(api_key, model, messages, temperature=0.2)
        return extract_json_object(first_response)
    except Exception as exc:
        errors.append(
            {
                "step": "llm_recommendation",
                "type": "JSON_PARSE_RETRY",
                "message": str(exc),
            }
        )

    repair_messages = messages + [
        {
            "role": "assistant",
            "content": locals().get("first_response", ""),
        },
        {
            "role": "user",
            "content": (
                "The previous answer could not be parsed. "
                "Return only valid JSON with the required keys: "
                "recommended_city, weather, events, reason."
            ),
        },
    ]
    try:
        retry_response = call_openai_chat(api_key, model, repair_messages, temperature=0.0)
        return extract_json_object(retry_response)
    except Exception as exc:
        errors.append(
            {
                "step": "llm_recommendation",
                "type": "JSON_PARSE_FAILED",
                "message": str(exc),
            }
        )
        raise


def classify_http_error(step, exc):
    status = getattr(exc, "code", None)
    if status in (401, 403):
        error_type = "AUTH_ERROR"
    elif status == 429:
        error_type = "QUOTA_ERROR"
    else:
        error_type = "HTTP_ERROR"

    return {
        "step": step,
        "type": error_type,
        "message": f"HTTP {status}",
    }


def search_kakao_restaurants(kakao_key, city, errors, size=5):
    query = f"{city} 맛집"
    params = parse.urlencode({"query": query, "size": size})
    url = f"{KAKAO_KEYWORD_SEARCH_URL}?{params}"
    headers = {"Authorization": f"KakaoAK {kakao_key}"}

    try:
        data = call_json_api(url, headers=headers, timeout=30)
    except error.HTTPError as exc:
        errors.append(classify_http_error("place_search", exc))
        return []
    except Exception as exc:
        errors.append(
            {
                "step": "place_search",
                "type": "NETWORK_OR_PARSE_ERROR",
                "message": str(exc),
            }
        )
        return []

    documents = data.get("documents", [])
    if not documents:
        errors.append(
            {
                "step": "place_search",
                "type": "EMPTY_RESULT",
                "message": f"0 results for query={query}",
            }
        )
        return []

    restaurants = []
    for item in documents[:size]:
        restaurants.append(
            {
                "name": item.get("place_name", ""),
                "address": item.get("road_address_name") or item.get("address_name", ""),
                "category": item.get("category_name", ""),
                "url": item.get("place_url", ""),
                "x": safe_float(item.get("x")),
                "y": safe_float(item.get("y")),
            }
        )
    return restaurants


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_fallback_report(travel_date, recommendation, restaurants, errors):
    lines = [
        f"# {travel_date} 국내 여행 추천 리포트",
        "",
        "## 추천 지역",
        recommendation["recommended_city"],
        "",
        "## 추천 이유",
        recommendation["reason"],
        "",
        "## 날씨 요약",
        recommendation["weather"],
        "",
        "## 행사/축제",
    ]
    lines.extend([f"- {event}" for event in recommendation["events"]] or ["- 데이터 없음"])
    lines.extend(["", "## 맛집 추천"])
    if restaurants:
        for restaurant in restaurants:
            detail = restaurant["address"] or "주소 정보 없음"
            lines.append(f"- {restaurant['name']} ({detail})")
    else:
        lines.append("- 데이터 없음 (장소 검색 결과 0건 또는 API 오류)")

    lines.extend(
        [
            "",
            "## 1일 일정 제안",
            "- 오전: 추천 지역의 대표 관광지 방문",
            "- 오후: 지역 행사 또는 산책 코스 즐기기",
            "- 저녁: 맛집 방문 후 숙소 이동",
            "",
            "## 오류 요약(errors)",
        ]
    )
    if errors:
        lines.extend([f"- {item['step']}: {item['type']} - {item['message']}" for item in errors])
    else:
        lines.append("- 없음")

    return "\n".join(lines) + "\n"


def generate_report(api_key, model, travel_date, recommendation, restaurants, errors):
    prompt = f"""
Create a Korean Markdown travel report.

Travel date: {travel_date}
Recommendation JSON:
{json.dumps(recommendation, ensure_ascii=False, indent=2)}

Restaurant search results:
{json.dumps(restaurants, ensure_ascii=False, indent=2)}

Errors:
{json.dumps(errors, ensure_ascii=False, indent=2)}

The report must include these sections:
- 추천 지역
- 추천 이유
- 날씨 요약
- 행사/축제
- 맛집 추천
- 1일 일정 제안
- 오류 요약(errors)

If restaurants are empty, write "데이터 없음" in the restaurant section.
Do not include API keys or invented reference links.
"""
    messages = [
        {
            "role": "system",
            "content": "You create concise Korean Markdown travel reports.",
        },
        {"role": "user", "content": prompt},
    ]

    try:
        return call_openai_chat(api_key, model, messages, temperature=0.5).strip() + "\n"
    except Exception as exc:
        errors.append(
            {
                "step": "llm_report",
                "type": "REPORT_GENERATION_FALLBACK",
                "message": str(exc),
            }
        )
        return build_fallback_report(travel_date, recommendation, restaurants, errors)


def save_outputs(base_dir, travel_date, recommendation, restaurants, errors, report):
    results_dir = base_dir / "results"
    results_dir.mkdir(exist_ok=True)

    raw_path = results_dir / f"{travel_date}_raw.json"
    report_path = results_dir / f"{travel_date}_travel_plan.md"

    raw_data = {
        "date": travel_date,
        "recommendation": recommendation,
        "restaurants": restaurants,
        "errors": errors,
    }

    raw_path.write_text(
        json.dumps(raw_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    report_path.write_text(report, encoding="utf-8")

    return raw_path, report_path


def main():
    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / ".env")
    args = parse_args()

    openai_key = require_env(
        "OPENAI_API_KEY",
        'Set it in PowerShell: $env:OPENAI_API_KEY="YOUR_KEY"',
    )
    kakao_key = require_env(
        "KAKAO_REST_API_KEY",
        'Set it in PowerShell: $env:KAKAO_REST_API_KEY="YOUR_KEY"',
    )
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    errors = []

    print("[1/3] 1차 추천 생성 중(LLM)...")
    recommendation = generate_recommendation(openai_key, model, args.date, errors)
    print(f'  - recommended_city: "{recommendation["recommended_city"]}"')

    print("[2/3] 맛집 검색 중(지도/장소 API)...")
    restaurants = search_kakao_restaurants(
        kakao_key,
        recommendation["recommended_city"],
        errors,
    )
    if restaurants:
        print(f"  - 맛집 {len(restaurants)}곳 검색 완료")
    else:
        print("  - 맛집 데이터 없음. 리포트 생성을 계속 진행합니다.")

    print("[3/3] 최종 리포트 생성 중(LLM)...")
    report = generate_report(
        openai_key,
        model,
        args.date,
        recommendation,
        restaurants,
        errors,
    )
    raw_path, report_path = save_outputs(
        base_dir,
        args.date,
        recommendation,
        restaurants,
        errors,
        report,
    )
    print("  - 리포트 생성 완료")
    print()
    print(f"완료! {report_path} 를 확인하세요.")
    print(f"원본 데이터: {raw_path}")


if __name__ == "__main__":
    main()
