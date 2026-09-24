"""POST /api/diagnose — AI·AX 맞춤 진단.

Vercel Python Function (BaseHTTPRequestHandler 패턴).
흐름: 요청 크기·형식 검증 → 규칙 기반 평가 → AI 설명 생성 → JSON 응답.
연락처는 요청에 포함하지 않고, 익명 진단은 저장하지 않는다.
"""

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Vercel은 프로젝트 루트를 sys.path에 두지만, 로컬 단독 실행 대비로 루트를 추가한다.
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from api_services.ai_provider import AIProviderError, generate_result  # noqa: E402
from api_services.diagnosis_rules import evaluate, validate_answers  # noqa: E402

MAX_BODY_BYTES = 16 * 1024  # PRD 권장 기본값: 요청 본문 최대 16 KiB

DISCLAIMER = (
    "이 결과는 입력한 답변을 바탕으로 생성한 참고용 제안입니다. "
    "정식 컨설팅 결과나 성과 보장이 아니며, 점수는 방향 탐색을 위한 참고값입니다."
)


def _json(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def _error(handler, status, code, message):
    _json(handler, status, {"ok": False, "error": {"code": code, "message": message}})


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            _error(self, 400, "EMPTY_BODY", "요청 본문이 비어 있습니다.")
            return
        if length > MAX_BODY_BYTES:
            _error(self, 413, "BODY_TOO_LARGE", "요청이 허용 크기를 초과했습니다.")
            return

        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            _error(self, 400, "INVALID_JSON", "JSON 형식을 해석할 수 없습니다.")
            return

        answers, err = validate_answers(payload)
        if err:
            _error(self, 400, "INVALID_ANSWERS", err)
            return

        evaluation = evaluate(answers)
        try:
            ai_result = generate_result(answers, evaluation)
        except AIProviderError as e:
            # 내부 예외·키·스택은 응답에 포함하지 않는다.
            _error(self, 502, "AI_UNAVAILABLE", str(e))
            return

        _json(self, 200, {
            "ok": True,
            "result": ai_result,
            "evaluation": evaluation,
            "disclaimer": DISCLAIMER,
        })

    def do_GET(self):
        _error(self, 405, "METHOD_NOT_ALLOWED", "POST 요청만 지원합니다.")

    def do_PUT(self):
        _error(self, 405, "METHOD_NOT_ALLOWED", "POST 요청만 지원합니다.")

    def do_DELETE(self):
        _error(self, 405, "METHOD_NOT_ALLOWED", "POST 요청만 지원합니다.")

    def log_message(self, format, *args):
        # 기본 접근 로그는 억제한다 (진단 원문·개인정보를 로그에 남기지 않는 방침).
        pass
