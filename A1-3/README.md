# AX Ground — A1-3 미션 제출

AI 교육부터 자동화, AX 전환까지. 조직과 개인의 업무·학습 환경을 살펴보고 맞춤형 교육과 실행 방향을 제안하는 웹 서비스입니다.

## 서비스 소개

- 서비스명: AX Ground (AX그라운드)
- 대상: AI 교육이나 AX 컨설팅을 찾는 중소기업 실무팀, 기관·학교 담당자, 일반 직장인
- 핵심 서비스: 맞춤형 AI 교육, 업무 진단·AX 로드맵, AI 도구·MVP 제작
- AI 기능: 8개 문항 진단 답변을 바탕으로 현재 상태, 우선 과제, 추천 교육·AX 실행 방향을 생성합니다.

## 서비스 주소

- 배포 사이트: https://codyssey-a1.vercel.app/
- GitHub 저장소: https://github.com/hongbinwee/codyssey-A1/tree/main/A1-3

웹사이트는 Vercel에 배포되어 있습니다. 로컬 mock 응답과 API 흐름은 테스트했으며, 배포 환경에서 실제 AI 응답까지 성공하는지는 별도 확인이 필요합니다. mock 진단 결과는 실제 AI 응답 증빙으로 사용하지 않습니다.

## 기술 스택

- 프론트엔드: 순수 HTML, CSS, Vanilla JavaScript
- 백엔드: `api/`의 Python Vercel Serverless Function
- AI API: OpenAI 호환 게이트웨이 `https://copa.codyssey.kr/v1/chat/completions`, 모델 `gpt-5.5`
- Python 외부 패키지: 없음. `requirements.txt` 참고
- 배포: GitHub + Vercel

## 요청 흐름과 학습 기록

1. HTML은 홈·진단·상담 화면의 구조와 입력 폼을 정의합니다.
2. CSS는 레이아웃, 반응형 화면, 라이트·다크 테마를 담당합니다.
3. JavaScript는 입력을 검증하고 `fetch('/api/diagnose')`로 Python API를 호출한 뒤 JSON 결과를 화면에 표시합니다.
4. Python 함수는 서버에서 입력을 검증하고 규칙 평가와 AI API 호출을 수행합니다.
5. AI 키는 브라우저 코드에 두지 않고 서버 환경 변수 `AI_API_KEY`로 관리합니다.
6. 로컬에서는 Python 핸들러와 Node 정적 서버를 함께 사용합니다. Vercel에서는 `api/` 함수가 배포 환경에서 실행됩니다.

자세한 학습 목표와 코드 근거는 [`docs/learning_log.md`](docs/learning_log.md)에 기록했습니다.

## 로컬 실행

정적 화면만 확인하려면 A1-3 폴더에서 정적 서버를 실행합니다.

```sh
npx serve .
```

진단 API 흐름을 실제 AI 호출 없이 mock 모드로 확인하려면 두 터미널에서 실행합니다.

```sh
python evidence/run_api.py --mock 4318
```

```sh
node evidence/serve.mjs 4317
```

로컬 주소는 `http://127.0.0.1:4317/`입니다. `serve.mjs`가 `/api` 요청을 로컬 Python 핸들러로 전달합니다.

## 환경 변수

실제 AI API 호출에는 서버 환경 변수 `AI_API_KEY`가 필요합니다. 실제 키 값은 코드, 문서, 스크린샷, Git 저장소에 넣지 않습니다.

| 변수 | 용도 | 기본값 |
| --- | --- | --- |
| `AI_API_KEY` | AI 게이트웨이 인증 키 | 없음, 필수 |
| `AI_API_BASE` | Chat Completions 엔드포인트 | `https://copa.codyssey.kr/v1/chat/completions` |
| `AI_MODEL` | 사용할 모델 | `gpt-5.5` |
| `AI_TIMEOUT` | AI 요청 시간 제한(초) | `20` |

- 로컬: 셸 환경 변수로 설정한 뒤 `python evidence/run_api.py 4318`을 실행합니다. `.env.example`은 설정 예시이며 자동으로 로드되지 않습니다.
- Vercel: 프로젝트 Settings의 Environment Variables에 변수명을 등록하고 재배포합니다.
- `AXG_MOCK_AI=1`은 로컬 테스트 전용입니다.

## 검증 상태

- 로컬 mock 백엔드 테스트: 12개 통과
- HTTP 통합 테스트: 10개 통과
- Playwright 화면 검증: 33개 통과
- 반응형 화면 확인: 1440px, 768px, 390px
- 실제 배포 AI 응답: 확인 대기

테스트 스크린샷과 범위는 [`evidence/README.md`](evidence/README.md)를 참고하세요.

## 프로젝트 구조

```text
index.html                  # 홈과 서비스 섹션
diagnosis.html              # 8문항 진단과 결과
contact.html                # 맞춤 상담 문의
css/style.css               # 디자인 토큰, 반응형, 라이트·다크 모드
js/                         # 테마, 메뉴, 슬라이드, Workflow, 진단 동작
api/diagnose.py             # POST /api/diagnose
api_services/               # 점수 규칙, AI 게이트웨이 어댑터, mock 결과
requirements.txt            # Python 의존성
.env.example                # 환경 변수 이름과 설명
docs/service_plan.md        # 서비스 기획서
docs/learning_log.md        # 미션 학습 기록
evidence/                   # 테스트와 화면 증빙
```

## 아직 연결하지 않은 기능

- 상담·후속 요청을 저장하는 `POST /api/requests`, Neon 데이터베이스, 관리자 인증, 이메일 발송은 구현하지 않았습니다.
- 상담 폼과 진단 후속 패널은 입력 검증까지만 동작하며 실제 전송·저장은 하지 않습니다.
- 후속 요청이 없는 익명 진단 답변은 저장하지 않고, 연락처는 AI 요청에 포함하지 않습니다.
- 진단 점수와 추천 경계값은 초기 참고안이며 전문 컨설팅 기준이 아닙니다.
- 개인정보 동의 문구는 법적 검토가 필요합니다.
