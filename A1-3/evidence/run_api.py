"""로컬 API 러너 — api/diagnose.py 의 Vercel 핸들러를 로컬 HTTP로 실행.

사용: python evidence/run_api.py [port]   (기본 포트 4318)
AXG_MOCK_AI=1 환경 변수와 함께 실행하면 실제 AI 호출 없이 mock 결과를 반환한다.
배포 환경에서는 Vercel이 api/ 안의 파일을 Function으로 직접 실행한다.
"""

import os
import sys
from http.server import HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --mock: 실제 AI 호출 없이 mock 결과를 반환한다 (로컬 검증 전용).
if "--mock" in sys.argv:
    os.environ["AXG_MOCK_AI"] = "1"
    sys.argv.remove("--mock")

from api.diagnose import handler  # noqa: E402


class RoutedHandler(handler):
    """경로를 확인한 뒤 Vercel 핸들러의 do_* 로 위임한다."""

    def _route(self):
        return self.path.split("?")[0].rstrip("/") or "/"

    def do_POST(self):
        if self._route() == "/api/diagnose":
            super().do_POST()
        else:
            self._not_found()

    def do_GET(self):
        if self._route() == "/api/diagnose":
            super().do_GET()
        else:
            self._not_found()

    def _not_found(self):
        body = b"{\"ok\": false, \"error\": {\"code\": \"NOT_FOUND\", \"message\": \"unknown api path\"}}"
        self.send_response(404)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4318
    server = HTTPServer(("127.0.0.1", port), RoutedHandler)
    print("AX Ground local API: http://127.0.0.1:" + str(port) + "/api/diagnose")
    server.serve_forever()
