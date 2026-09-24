"""AI 공급자 어댑터 — OpenAI 호환 chat completions 게이트웨이.

교육기관 게이트웨이: https://copa.codyssey.kr/v1/chat/completions
- API 키는 환경 변수 AI_API_KEY 로만 읽는다. 코드·로그에 값을 남기지 않는다.
- reasoning_effort 옵션은 사용하지 않는다 (게이트웨이에서 미지원 확인).
- response_format·max_completion_tokens 등 부가 옵션은 게이트웨이가
  unsupported_feature(400)를 반환해 사용하지 않는다. 요청은 model+messages만 보내고,
  시스템 프롬프트의 JSON 지시와 응답 파싱·스키마 검증으로 구조를 보장한다.
- 외부 패키지 없이 표준 라이브러리만 사용한다 (로컬 번들 Python과 동일하게 동작).
- AXG_MOCK_AI=1 이면 실제 호출 없이 mock_ai_result.json 내용을 반환한다.
  로컬 검증 전용이며 배포 환경에서는 설정하지 않는다.
"""

import json
import os
import urllib.error
import urllib.request

DEFAULT_BASE_URL = "https://copa.codyssey.kr/v1/chat/completions"
DEFAULT_MODEL = "gpt-5.5"
DEFAULT_TIMEOUT = 20  # PRD 권장 기본값: 공급자 요청 20초


class AIProviderError(Exception):
    """AI 호출 실패. 사용자에게 노출 가능한 일반 메시지만 담는다."""


class AIResponseError(AIProviderError):
    """AI가 형식에 맞지 않는 응답을 반환했다."""


SYSTEM_PROMPT = (
    "당신은 AX Ground의 AI·AX 진단 컨설턴트입니다. "
    "방문자의 8개 진단 답변과 규칙 기반 평가 결과를 바탕으로, "
    "지정된 JSON 스키마에 맞는 한국어 진단 결과를 생성합니다. "
    "규칙: (1) 답변에 근거가 없는 사실, 절감률, 비용, 성과 수치를 만들지 않습니다. "
    "(2) 확인할 수 없는 내용은 '추가 확인 필요'로 표시합니다. "
    "(3) 결과는 참고용 초기 제안이며 전문 컨설팅이나 성과 보장으로 표현하지 않습니다. "
    "(4) 회사명, 이름, 이메일 등 연락 정보는 언급하지 않습니다. "
    "(5) 출력은 반드시 유효한 JSON 객체 하나입니다. 설명 문장이나 마크다운을 붙이지 않습니다."
)

_RESULT_SCHEMA_DESC = """{
  "summary": "현재 상태 요약 1~2문장",
  "priority_tasks": ["우선 해결 과제 2~4개"],
  "recommended_path": {"label": "4개 경로 중 하나", "reason": "답변 근거 1~2문장"},
  "education": {
    "audience": "추천 교육 대상",
    "modules": ["교육 모듈 3개"],
    "outcome": "실습 결과물",
    "format": "권장 방식과 시간"
  },
  "ax_candidates": [
    {"task": "적용 후보 업무", "expected_effect": "기대 효과(정성적)", "difficulty": "낮음/중간/높음", "verify_first": true}
  ],
  "roadmap": [
    {"phase": "1단계 확인·교육", "items": ["행동"]},
    {"phase": "2단계 소규모 시범 적용", "items": ["행동"]},
    {"phase": "3단계 결과 측정·확대", "items": ["행동"]}
  ],
  "cautions": ["주의사항·추가 확인 질문 2~4개"],
  "consultation": {"service": "적합한 서비스", "topics": ["상담 시 논의할 항목"]}
}"""

_PATH_LABELS = "교육 우선형 / AX 진단 우선형 / 소규모 MVP·자동화 실험형 / 교육·시범 프로젝트 병행형"


def _build_user_prompt(answers, evaluation):
    lines = ["[진단 답변]"]
    labels = {
        "role": "입장", "stage": "AI 활용 단계", "goal": "우선 목표",
        "target": "적용 대상", "work": "개선 희망 업무", "frequency": "빈도·소요",
        "data": "자료·시스템 환경", "readiness": "시작 시기·성공 기준",
    }
    for qid, label in labels.items():
        lines.append("- " + label + ": " + answers[qid])
    lines.append("")
    lines.append("[규칙 기반 평가]")
    for key, item in evaluation["scores"].items():
        lines.append("- " + key + ": " + str(item["score"]) + "/5 — " + item["note"])
    lines.append("- 추천 경로(규칙): " + evaluation["recommended_path"]["label"])
    lines.append("")
    lines.append("[요청]")
    lines.append("위 답변과 평가를 근거로 아래 JSON 스키마로만 출력하세요.")
    lines.append("recommended_path.label은 다음 중 하나: " + _PATH_LABELS)
    lines.append(_RESULT_SCHEMA_DESC)
    return "\n".join(lines)


def _load_mock():
    path = os.path.join(os.path.dirname(__file__), "mock_ai_result.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_result(answers, evaluation):
    """AI 설명 결과 dict를 반환한다. 실패 시 AIProviderError를 던진다."""
    if os.environ.get("AXG_MOCK_AI") == "1":
        return _load_mock()

    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        raise AIProviderError("AI_API_KEY 환경 변수가 설정되지 않았습니다.")

    base_url = os.environ.get("AI_API_BASE", DEFAULT_BASE_URL)
    model = os.environ.get("AI_MODEL", DEFAULT_MODEL)
    try:
        timeout = float(os.environ.get("AI_TIMEOUT", DEFAULT_TIMEOUT))
    except ValueError:
        timeout = DEFAULT_TIMEOUT

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(answers, evaluation)},
        ],
    }
    req = urllib.request.Request(
        base_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            payload = json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise AIProviderError("AI 서비스가 오류를 반환했습니다. (HTTP " + str(e.code) + ")")
    except (urllib.error.URLError, TimeoutError) as e:
        raise AIProviderError("AI 서비스 응답이 지연되거나 연결에 실패했습니다.")
    except (json.JSONDecodeError, KeyError):
        raise AIResponseError("AI 서비스 응답 형식을 해석할 수 없습니다.")

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise AIResponseError("AI 서비스 응답 형식을 해석할 수 없습니다.")

    result = _extract_json(content)
    _validate_result(result)
    return result


def _extract_json(content):
    """AI 응답 텍스트에서 JSON 객체를 안전하게 꺼낸다.

    마크다운 코드펜스나 앞뒤 설명 문장이 붙어도
    첫 번째 최상위 { ... } 블록만 추출해 파싱한다.
    구조가 맞지 않으면 AIResponseError를 던진다.
    """
    if not isinstance(content, str):
        raise AIResponseError("AI 결과 텍스트가 비어 있습니다.")
    text = content.strip()
    # 코드펜스 제거
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
        text = text.strip()
    # 전체가 JSON이면 바로 파싱
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # 앞뒤 설명이 붙은 경우 첫 { ~ 짝이 맞는 } 범위를 추출
    start = text.find("{")
    if start == -1:
        raise AIResponseError("AI 결과가 JSON 형식이 아닙니다.")
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == chr(34):
                in_str = False
        elif ch == chr(34):
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    raise AIResponseError("AI 결과가 JSON 형식이 아닙니다.")
    raise AIResponseError("AI 결과가 JSON 형식이 아닙니다.")


_REQUIRED_KEYS = (
    "summary", "priority_tasks", "recommended_path", "education",
    "ax_candidates", "roadmap", "cautions", "consultation",
)


def _validate_result(result):
    """필수 키와 최소 형식을 검사한다. 부족하면 AIResponseError."""
    if not isinstance(result, dict):
        raise AIResponseError("AI 결과가 객체가 아닙니다.")
    for key in _REQUIRED_KEYS:
        if key not in result:
            raise AIResponseError("AI 결과에 필수 항목이 없습니다: " + key)
    if not isinstance(result["priority_tasks"], list) or not result["priority_tasks"]:
        raise AIResponseError("AI 결과 형식이 올바르지 않습니다: priority_tasks")
    if not isinstance(result["roadmap"], list) or not result["roadmap"]:
        raise AIResponseError("AI 결과 형식이 올바르지 않습니다: roadmap")
