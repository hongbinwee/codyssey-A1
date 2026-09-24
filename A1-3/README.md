# AX Ground — A1-3 미션 제출

AI 교육부터 자동화, AX 전환까지. 조직의 업무·학습 환경을 진단하고 맞춤형 AI 교육과 AX 로드맵으로 연결하는 웹 서비스입니다.

## 서비스 소개

- 서비스명: AX Ground (AX그라운드)
- 대상: AI 교육이나 AX 컨설팅을 찾는 중소기업 실무팀, 기관·학교 담당자, 일반 직장인
- 핵심 서비스: 맞춤형 AI 교육, 업무 진단·AX 로드맵, AI 도구·MVP 제작
- AI 기능: 8개 문항의 AI·AX 실행 준비도 진단. 답변을 Python API로 보내 규칙 평가 + AI 설명 결과(현황 요약, 5개 영역 평가, 추천 경로, 교육안, AX 후보, 로드맵, 주의사항, 상담 연결)를 화면에 표시합니다.

## 기술 스택

- 프론트엔드: HTML, CSS, Vanilla JavaScript (프레임워크 없음)
- 백엔드: `api/`의 Python — Vercel Serverless Functions (`BaseHTTPRequestHandler` 패턴)
- AI API: OpenAI 호환 게이트웨이 `https://copa.codyssey.kr/v1/chat/completions`, 모델 `gpt-5.5` (`reasoning_effort` 미사용)
- 외부 패키지 없음(표준 라이브러리만 사용). `requirements.txt` 참고
- 배포: GitHub + Vercel

## 배포 URL

- 배포 전입니다. Vercel 배포 후 이 자리에 URL을 기재합니다.

## 로컬 실행

정적 화면만 보려면 아무 정적 서버나 실행하면 됩니다.

```
npx serve .
```

AI 진단 API까지 로컬에서 확인하려면 두 프로세스가 필요합니다.

```
python evidence\run_api.py --mock 4318   # 로컬 API (mock 모드 — 실제 AI 호출 없음)
node evidence\serve.mjs 4317            # 정적 서버 + /api 프록시 → http://127.0.0.1:4317/
```

로컬 정적 서버는 Python `/api`를 실행할 수 없어 `serve.mjs`가 `/api` 요청을 `run_api.py`로 프록시합니다. 배포 환경에서는 Vercel이 같은 경로를 Function으로 직접 연결합니다.

## 환경 변수

실제 AI 게이트웨이를 호출하려면 서버 실행 환경에 아래 변수를 설정합니다. 키 값은 코드·문서·스크린샷에 넣지 않습니다.

| 변수 | 용도 | 기본값 |
| --- | --- | --- |
| `AI_API_KEY` | AI 게이트웨이 인증 키 (필수) | 없음 |
| `AI_API_BASE` | chat completions 엔드포인트 | `https://copa.codyssey.kr/v1/chat/completions` |
| `AI_MODEL` | 사용 모델 | `gpt-5.5` |
| `AI_TIMEOUT` | AI 요청 제한 시간(초) | `20` |

- 로컬: 셸 환경 변수로 설정한 뒤 `python evidence\run_api.py 4318` (`--mock` 없이 실행)
- 배포: Vercel 프로젝트 환경 변수에 등록
- 검증 전용 `AXG_MOCK_AI=1`은 로컬에서만 사용하고 배포에서는 설정하지 않습니다.
- `.env.example`에 변수명과 설명이 있습니다.

## 구조

```
index.html          # Home 11개 섹션
diagnosis.html      # AI·AX 맞춤 진단 (8문항 → 결과 → 후속 패널)
contact.html        # 빠른 상담 문의
css/style.css       # 디자인 토큰, Light/Dark, 반응형
js/                 # theme / app / slides / workflow / diagnosis
api/diagnose.py     # POST /api/diagnose (Vercel Function)
api_services/       # 규칙 평가 + AI 어댑터 + mock 결과
requirements.txt    # Python 의존성 (현재 외부 패키지 없음)
.env.example        # 환경 변수 예시
evidence/           # 로컬 검증 스크립트·스크린샷
```

## 미연동 범위 (이번 단계에서 제외)

- 문의·후속 요청 접수 API(`POST /api/requests`), Neon DB 저장, 관리자 인증, 이메일 발송은 구현하지 않았습니다.
- 진단 결과 아래 후속 패널(결과 이메일·맞춤 상담)과 빠른 상담 폼은 클라이언트 검증까지만 동작하고 실제 전송·저장은 하지 않습니다.
- 후속 요청 없는 익명 진단 답변·결과는 저장하지 않습니다. 연락처는 AI 요청에 포함하지 않습니다.
- 5개 영역 평가 점수·추천 경계값은 초기안이며 정식 컨설팅 기준이 아닙니다.
- 개인정보 법적 문구는 `[법적 문구 검토 필요]`로 표시해 두었습니다.
