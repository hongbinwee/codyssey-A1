import json, urllib.request, urllib.error

BASE = "http://127.0.0.1:4318/api/diagnose"
GOOD = {
    "role": "팀장·실무 책임자", "stage": "팀 단위로 활용", "goal": "반복 업무 시간 단축",
    "target": "8명 규모의 콘텐츠 마케팅 팀",
    "work": "매주 여러 자료를 모아 보고서 초안을 만드는 데 시간이 걸립니다.",
    "frequency": "매주 1회, 3명이 각 2시간씩 사용",
    "data": "문서·엑셀 중심",
    "readiness": "한 달 안에 한 가지 업무를 시범 적용하고 팀이 함께 써보는 것",
}

fails = 0
def check(name, cond, extra=""):
    global fails
    print(("PASS" if cond else "FAIL"), name, extra)
    if not cond: fails += 1

def post(body, raw=None):
    data = raw if raw is not None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(BASE, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

# 1) 정상 POST
s, d = post({"answers": GOOD})
check("200 ok", s == 200 and d.get("ok") is True, "status=" + str(s))
check("result+evaluation", "result" in d and "evaluation" in d)
check("disclaimer", "disclaimer" in d)
check("5 scores", len(d.get("evaluation", {}).get("scores", {})) == 5)

# 2) GET → 405
req = urllib.request.Request(BASE, method="GET")
try:
    urllib.request.urlopen(req, timeout=10)
    check("GET 405", False)
except urllib.error.HTTPError as e:
    check("GET 405", e.code == 405)

# 3) 빈 본문 → 400
req = urllib.request.Request(BASE, data=b"", headers={"Content-Type": "application/json"}, method="POST")
try:
    urllib.request.urlopen(req, timeout=10)
    check("empty body 400", False)
except urllib.error.HTTPError as e:
    check("empty body 400", e.code == 400)

# 4) 잘못된 JSON → 400
s, d = post(None, raw=b"{not json")
check("bad json 400", s == 400)

# 5) 필수 답변 누락 → 400
bad = dict(GOOD); del bad["work"]
s, d = post({"answers": bad})
check("missing answer 400", s == 400 and d["error"]["code"] == "INVALID_ANSWERS")

# 6) 연락처 키 포함 → 400 (AI 요청에 연락처 불포함 원칙과 일치)
bad2 = dict(GOOD); bad2["email"] = "a@b.c"
s, d = post({"answers": bad2})
check("contact key rejected", s == 400)

# 7) 16KiB 초과 → 413
big = "가" * (17 * 1024)
req = urllib.request.Request(BASE, data=json.dumps({"answers": dict(GOOD, work=big)}).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
try:
    urllib.request.urlopen(req, timeout=10)
    check("413 too large", False)
except urllib.error.HTTPError as e:
    check("413 too large", e.code == 413)

print("FAILS:", fails)
import sys; sys.exit(1 if fails else 0)
