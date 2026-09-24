import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api_services.ai_provider import _extract_json, _validate_result, AIResponseError

fails = 0
def check(name, cond):
    global fails
    print(("PASS" if cond else "FAIL"), name)
    if not cond: fails += 1

obj = {"a": 1, "b": {"c": "텍스트 {괄호} \"인용\" 포함"}}
s = json.dumps(obj, ensure_ascii=False)

check("plain json", _extract_json(s) == obj)
check("fenced json", _extract_json("```json\n" + s + "\n```") == obj)
check("fenced no-lang", _extract_json("```\n" + s + "\n```") == obj)
check("text around", _extract_json("결과입니다.\n" + s + "\n이상입니다.") == obj)
check("leading text inline", _extract_json("답변: " + s) == obj)

# 비JSON·비객체·잘린 JSON은 모두 AIResponseError
for bad in ("", "no json here", "{\"a\": 1", "결과: [1,2,3]"):
    try:
        _extract_json(bad)
        check("reject: " + repr(bad[:20]), False)
    except AIResponseError:
        check("reject: " + repr(bad[:20]), True)

# 필수 키가 빠진 객체는 스키마 검증에서 걸러진다
try:
    _validate_result({"summary": "x"})
    check("missing keys rejected", False)
except AIResponseError:
    check("missing keys rejected", True)

print("FAILS:", fails)
sys.exit(1 if fails else 0)
