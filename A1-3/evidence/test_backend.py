import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_services.diagnosis_rules import validate_answers, evaluate
os.environ["AXG_MOCK_AI"] = "1"
from api_services.ai_provider import generate_result

GOOD = {
    "role": "팀장·실무 책임자",
    "stage": "팀 단위로 활용",
    "goal": "반복 업무 시간 단축",
    "target": "8명 규모의 콘텐츠 마케팅 팀",
    "work": "매주 여러 자료를 모아 보고서 초안을 만드는 데 시간이 걸립니다.",
    "frequency": "매주 1회, 3명이 각 2시간씩 사용",
    "data": "문서·엑셀 중심",
    "readiness": "한 달 안에 한 가지 업무를 시범 적용하고 팀이 함께 써보는 것, 담당자 검토 포함",
}

fails = 0
def check(name, cond):
    global fails
    print(("PASS" if cond else "FAIL"), name)
    if not cond: fails += 1

# 1) 정상 검증
cleaned, err = validate_answers({"answers": GOOD})
check("validate ok", err is None and cleaned["role"] == GOOD["role"])

# 2) 빈 답변
bad = dict(GOOD); bad["work"] = "  "
_, err = validate_answers({"answers": bad})
check("empty answer rejected", err is not None)

# 3) 허용되지 않은 선택값
bad2 = dict(GOOD); bad2["stage"] = "엉뚱한 값"
_, err = validate_answers({"answers": bad2})
check("bad option rejected", err is not None)

# 4) 알 수 없는 키
bad3 = dict(GOOD); bad3["email"] = "x@y.z"
_, err = validate_answers({"answers": bad3})
check("unknown key rejected", err is not None)

# 5) 500자 초과
bad4 = dict(GOOD); bad4["work"] = "가" * 501
_, err = validate_answers({"answers": bad4})
check("overlength rejected", err is not None)

# 6) 평가 결과
ev = evaluate(GOOD)
scores = ev["scores"]
check("5 scores", len(scores) == 5)
check("score range", all(1 <= v["score"] <= 5 for v in scores.values()))
check("path label", ev["recommended_path"]["label"] == "교육·시범 프로젝트 병행형")

# 7) 경로 분기: 미사용 → 교육 우선형
low = dict(GOOD); low["stage"] = "거의 사용하지 않음"
check("low stage -> education_first", evaluate(low)["recommended_path"]["label"] == "교육 우선형")

# 8) 경로 분기: 우선순위 탐색 → AX 진단 우선형
nav = dict(GOOD); nav["goal"] = "우선순위 탐색"
check("nav goal -> ax_assessment", evaluate(nav)["recommended_path"]["label"] == "AX 진단 우선형")

# 9) 모의 AI 결과
r = generate_result(GOOD, ev)
check("mock result keys", all(k in r for k in ("summary","priority_tasks","recommended_path","education","ax_candidates","roadmap","cautions","consultation")))

# 10) 키 없을 때 실제 호출 경로는 AIProviderError
del os.environ["AXG_MOCK_AI"]
os.environ.pop("AI_API_KEY", None)
try:
    generate_result(GOOD, ev)
    check("missing key raises", False)
except Exception as e:
    check("missing key raises", "AI_API_KEY" in str(e))

print("FAILS:", fails)
sys.exit(1 if fails else 0)
