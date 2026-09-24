"""AI·AX 진단 규칙 평가.

PRD §6: 규칙 기반 로직이 5개 평가 영역의 점수와 추천 시작 경로를 결정한다.
점수는 방향 탐색용 참고값(1~5)이며 정식 컨설팅 결과가 아니다.
배점·가중치·경계값은 PRD 미정 항목이므로 초기안으로 두고
추후 사용자 승인과 테스트 사례로 조정한다.
"""

QUESTION_IDS = (
    "role", "stage", "goal", "target", "work", "frequency", "data", "readiness"
)

# 라디오 문항의 허용 선택값 (프론트 js/diagnosis.js QUESTIONS와 동일하게 유지)
ALLOWED_OPTIONS = {
    "role": [
        "개인 학습자", "기업 대표·임원", "팀장·실무 책임자",
        "교육·인사 담당자", "기획·IT·개발 담당자",
    ],
    "stage": [
        "거의 사용하지 않음", "개인적으로 일부 사용", "팀 단위로 활용",
        "업무 프로세스에 정착", "전사적으로 활용",
    ],
    "goal": [
        "역량 향상", "반복 업무 시간 단축", "결과물 품질 향상",
        "고객 응대·영업 개선", "AI 서비스·도구 제작", "우선순위 탐색",
    ],
    "data": [
        "문서·엑셀 중심", "메일·메신저 중심", "CRM·사내 시스템 보유",
        "자료 디지털화 전", "개인정보·기밀 포함",
    ],
}

FREE_TEXT_IDS = ("target", "work", "frequency", "readiness")
FREE_TEXT_MAX = 500

_STAGE_SCORE = {
    "거의 사용하지 않음": 1,
    "개인적으로 일부 사용": 2,
    "팀 단위로 활용": 3,
    "업무 프로세스에 정착": 4,
    "전사적으로 활용": 5,
}

_DATA_SCORE = {
    "자료 디지털화 전": 1,
    "개인정보·기밀 포함": 2,
    "메일·메신저 중심": 3,
    "문서·엑셀 중심": 4,
    "CRM·사내 시스템 보유": 5,
}

_ROLE_BASE = {
    "개인 학습자": 1,
    "기업 대표·임원": 2,
    "팀장·실무 책임자": 2,
    "교육·인사 담당자": 2,
    "기획·IT·개발 담당자": 3,
}

_PATH_LABELS = {
    "education_first": "교육 우선형",
    "ax_assessment_first": "AX 진단 우선형",
    "mvp_experiment": "소규모 MVP·자동화 실험형",
    "education_and_pilot": "교육·시범 프로젝트 병행형",
}

_SECURITY_KEYWORDS = ("담당", "검토", "승인", "결재", "보안", "개인정보", "기밀")


def validate_answers(payload):
    """요청 바디를 검증한다. 성공 시 정제된 answers dict, 실패 시 오류 메시지를 반환."""
    if not isinstance(payload, dict):
        return None, "요청 형식이 올바르지 않습니다."
    answers = payload.get("answers")
    if not isinstance(answers, dict):
        return None, "answers 필드가 없습니다."
    unknown = [k for k in answers if k not in QUESTION_IDS]
    if unknown:
        return None, "허용되지 않은 문항 키가 포함되어 있습니다."
    cleaned = {}
    for qid in QUESTION_IDS:
        value = answers.get(qid)
        if not isinstance(value, str) or not value.strip():
            return None, "필수 답변이 비어 있습니다: " + qid
        value = value.strip()
        if qid in ALLOWED_OPTIONS:
            if value not in ALLOWED_OPTIONS[qid]:
                return None, "허용되지 않은 선택값입니다: " + qid
        elif len(value) > FREE_TEXT_MAX:
            return None, "자유 입력이 최대 길이를 초과했습니다: " + qid
        cleaned[qid] = value
    return cleaned, None


def _clip(score):
    return max(1, min(5, score))


def evaluate(answers):
    """5개 영역 점수(1~5)와 추천 시작 경로를 계산한다."""
    notes = {}

    # 1) 목표 명확도
    score = 2
    if len(answers["target"]) >= 10:
        score += 1
    if len(answers["readiness"]) >= 10:
        score += 1
    scores_goal = _clip(score)
    notes["goal_clarity"] = (
        "목표와 적용 대상·성공 기준을 함께 입력했습니다."
        if scores_goal >= 4
        else "목표는 선택했지만 적용 대상이나 성공 기준의 구체성은 제한적입니다."
    )

    # 2) 인력·교육 준비도
    scores_people = _clip(_STAGE_SCORE[answers["stage"]] * 0.7 + _ROLE_BASE[answers["role"]] * 0.3)
    notes["people_readiness"] = (
        "조직 차원의 AI 활용이 이미 진행 중입니다."
        if _STAGE_SCORE[answers["stage"]] >= 4
        else "조직 차원의 AI 활용은 아직 초기 단계입니다."
    )

    # 3) 업무 기회도
    score = 2
    if len(answers["work"]) >= 20:
        score += 1
    if len(answers["frequency"]) >= 8:
        score += 1
    scores_work = _clip(score)
    notes["work_opportunity"] = (
        "개선 대상 업무와 빈도·소요가 비교적 구체적으로 확인됩니다."
        if scores_work >= 4
        else "개선 대상 업무가 있지만 빈도·소요 정보는 제한적입니다."
    )

    # 4) 데이터·기술 준비도
    scores_data = _DATA_SCORE[answers["data"]]
    notes["data_readiness"] = "현재 자료·시스템 환경: " + answers["data"]

    # 5) 보안·운영 준비도
    sensitive = answers["data"] == "개인정보·기밀 포함"
    has_owner = any(k in answers["readiness"] for k in _SECURITY_KEYWORDS)
    scores_security = 2 if sensitive else (4 if has_owner else 3)
    if sensitive:
        notes["security_ops"] = "개인정보·기밀 포함 자료가 있어 적용 범위와 검토 절차를 먼저 확인해야 합니다."
    elif has_owner:
        notes["security_ops"] = "담당·검토 체계에 대한 언급이 있어 운영 준비가 비교적 확인됩니다."
    else:
        notes["security_ops"] = "운영 책임·검토 체계는 추가 확인이 필요합니다."

    scores = {
        "goal_clarity": {"score": scores_goal, "note": notes["goal_clarity"]},
        "people_readiness": {"score": scores_people, "note": notes["people_readiness"]},
        "work_opportunity": {"score": scores_work, "note": notes["work_opportunity"]},
        "data_readiness": {"score": scores_data, "note": notes["data_readiness"]},
        "security_ops": {"score": scores_security, "note": notes["security_ops"]},
    }

    # 추천 시작 경로 (초기 경계값 — PRD 미정 항목)
    stage_n = _STAGE_SCORE[answers["stage"]]
    goal = answers["goal"]
    if goal == "우선순위 탐색":
        path_key = "ax_assessment_first"
    elif goal == "AI 서비스·도구 제작" and stage_n >= 3:
        path_key = "mvp_experiment"
    elif stage_n <= 2:
        path_key = "education_first"
    else:
        path_key = "education_and_pilot"

    return {
        "scores": scores,
        "recommended_path": {
            "key": path_key,
            "label": _PATH_LABELS[path_key],
            "reason": _path_reason(path_key, answers, stage_n),
        },
    }


def _path_reason(path_key, answers, stage_n):
    if path_key == "education_first":
        return "현재 AI 활용 단계가 초기라 공통 역량을 먼저 만드는 교육이 시작점으로 적합합니다."
    if path_key == "ax_assessment_first":
        return "목표가 우선순위 탐색이라 업무 진단으로 적용 후보를 먼저 정리하는 것이 적합합니다."
    if path_key == "mvp_experiment":
        return "활용 단계가 진행 중이고 도구 제작이 목표라 작은 실험으로 검증하는 경로가 적합합니다."
    return "활용 경험이 있어 교육과 시범 프로젝트를 병행하면 실행 속도를 높일 수 있습니다."
