# A1-3 학습 기록

이 문서는 미션의 학습 목표를 실제 AX Ground 코드와 연결한 설명 초안이다. 제출 전 학습자가 각 내용을 이해한 뒤 자신의 말로 설명할 수 있는지 확인하고 보완한다. 구현·검증하지 않은 내용은 완료한 것처럼 표시하지 않는다.

## 학습 목표

### 1. HTML, CSS, JavaScript의 역할

- 상태: 설명 초안 작성; 학습자 본인의 이해 확인 필요
- 내 설명: HTML은 `index.html`의 11개 섹션과 `diagnosis.html`/`contact.html`의 폼 구조를 담당한다. CSS(`css/style.css`)는 색상 토큰·레이아웃·반응형·다크 모드를 담당하고, JavaScript(`js/`)는 테마 저장, 슬라이드 전환, Workflow 렌더링, 폼 검증처럼 화면의 동작과 상태를 담당한다.
- 코드 근거: `index.html`의 `<section>` 구조, `css/style.css`의 `:root`/`[data-theme="dark"]` 토큰, `js/slides.js`의 슬라이드 마운트·전환, `js/diagnosis.js`의 문항 렌더링

### 2. 입력에서 화면 출력까지의 요청 흐름

- 상태: mock·HTTP 흐름 검증; 배포 환경의 실제 게이트웨이 응답은 미검증
- 흐름: 사용자 입력 → JavaScript `fetch` → Python API → JSON 응답 → 화면 갱신
- 내 설명: 8개 문항의 답변을 `answers` 객체에 모으고, 마지막 문항 제출 시 `fetch('/api/diagnose', {method:'POST', body: JSON.stringify({answers})})`로 보낸다. 서버는 필수값·선택값을 검증하고 규칙 평가 + AI 설명을 JSON으로 돌려주며, 프론트는 `ok`와 `result`를 확인해 결과 블록을 DOM으로 채운다. 실패(4xx/5xx/타임아웃/연결 불가)는 오류 화면으로 분기한다.
- 코드 근거: `js/diagnosis.js`의 `requestDiagnosis()`·`runDiagnosis()`·`renderResult()`, `api/diagnose.py`의 `do_POST`, `api_services/diagnosis_rules.py`의 `validate_answers()`·`evaluate()`

### 3. Vercel Python Serverless Functions

- 상태: 설명 초안 작성; 학습자 본인의 이해 확인 필요
- 내 설명: `api/` 폴더의 Python 파일이 배포되면 Vercel이 각 파일을 HTTP 요청을 받는 함수로 실행한다. `api/diagnose.py`는 `BaseHTTPRequestHandler`를 상속한 `handler` 클래스로 `do_POST`를 구현하고, 요청 크기·JSON·필수 답변을 서버에서 다시 검증한 뒤 규칙 평가와 AI 호출을 거쳐 JSON을 반환한다. 프론트는 같은 사이트의 `/api/diagnose` 경로로 호출하므로 브라우저에 키가 노출되지 않는다.
- 코드 근거: `api/diagnose.py`의 `class handler(BaseHTTPRequestHandler)`와 `do_POST`/`do_GET`, `evidence/run_api.py`(로컬에서 같은 핸들러를 HTTPServer로 실행해 검증)

### 4. 환경 변수와 API 키

- 상태: 설명 초안 작성; 학습자 본인의 이해 확인 필요
- 내 설명: AI 키를 프론트 코드나 저장소에 넣으면 누구나 볼 수 있어 비용·보안 사고로 이어진다. 그래서 키는 서버 함수가 `os.environ.get("AI_API_KEY")`로만 읽고, 로컬은 셸 환경 변수·배포는 Vercel 환경 변수로 주입한다. `.env.example`에는 변수명과 설명만 두고 실제 값은 커밋하지 않는다.
- 설정 확인 근거: `api_services/ai_provider.py`의 `os.environ.get("AI_API_KEY")`, `.env.example`, `evidence/check_keys.py`(변수명만 나열해 키 유무 확인에 사용). 실제 키 값은 어디에도 기록하지 않는다.

### 5. 로컬과 배포 환경, 수정·재배포

- 상태: 설명 초안 작성; 배포 후 확인 기록 보완 필요
- 내 설명: 로컬에서는 정적 파일만 서빙하는 Node 서버가 `/api`를 실행할 수 없어, 같은 핸들러를 `HTTPServer`로 감싼 `evidence/run_api.py`를 별도 포트로 띄우고 `serve.mjs`가 `/api` 요청을 프록시한다. 배포 환경에서는 Vercel이 `api/`의 Python 파일을 Function으로 직접 실행하므로 프록시가 필요 없다. 환경 변수도 로컬은 셸, 배포는 Vercel 프로젝트 설정으로 주입 경로가 다르다.
- 로컬과 배포 환경의 차이: 로컬 = `serve.mjs`(정적+프록시) + `run_api.py`(Python 핸들러); 배포 = Vercel이 정적 사이트와 `api/` Function을 같은 도메인에서 제공. 검증용 `AXG_MOCK_AI`는 로컬 전용이며 배포에서는 설정하지 않는다.
- 배포 확인: `https://codyssey-a1.vercel.app/`에서 웹사이트가 배포된 상태다. 로컬에서는 `serve.mjs`와 `run_api.py`를 함께 쓰지만 Vercel에서는 `/api/diagnose`가 Python Function으로 실행된다는 차이를 확인했다. 배포 URL에서 페이지가 열린다는 것과 실제 AI 응답이 성공한다는 것은 별개의 검증 항목이다.
- 남은 검증: 배포 환경에서 진단을 제출해 실제 AI 응답·결과 렌더링을 확인하고, 오류 발생 시 Vercel 로그를 확인한 뒤 수정 사항을 재배포한다. 실제 응답 확인 전에는 완료로 표시하지 않는다.

### 6. AI 생성 코드 오류 분석

- 상태: 오류 원인과 로컬 수정 사례 기록; 학습자 본인의 설명 확인 필요
- 증상과 재현 방법: 진단 페이지에서 첫 문항이 렌더링되지 않아 자동 검증이 "no input found"로 멈췄다. 문의 폼은 올바른 이메일+동의를 입력해도 제출 버튼이 활성화되지 않았다.
- 원인 확인 근거: `js/diagnosis.js`에서 `renderQuestion()` 정의만 있고 초기 호출이 없었고, 첫 수정 시 `const` 선언 전에 호출해 TDZ 오류("Cannot access before initialization")가 났다. `contact.html`/`diagnosis.js`의 이메일 정규식이 `/^[^s@]+@[^s@]+.[^s@]+$/`로 백슬래시가 빠져 `tester@example.com`도 실패했다.
- 수정 내용과 이유: `renderQuestion()` 호출을 IIFE 끝(함수 정의 이후)으로 옮겼다. 정규식은 `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`로 복구했다.
- 수정 후 테스트 확인: Playwright 자동 검증으로 진단 8문항·결과 화면과 문의 동의 게이트를 확인했다. 이 테스트는 로컬 브라우저 검증이며, 실제 배포 AI 응답 검증을 대신하지 않는다.
- 추가 사례(2026-09-24): impeccable 탐지기가 모바일 내비에서 `.mobile-nav a`(0,1,1)가 `.btn--primary`(0,1,0)의 `color`를 덮어써 primary 버튼 글자가 배경색과 같은 계열로 보이는 결함을 찾았고, `a:not(.btn)`으로 범위를 좁혀 수정했다. `transition: width` 레이아웃 스래시는 `transform: scaleX`로 바꿨다.

## 기록 원칙

- 실행하지 않은 기능은 동작한다고 쓰지 않는다.
- 설명은 생성형 AI 문구를 그대로 복사하지 않고 직접 이해한 말로 작성한다.
- 증빙에 API 키, 개인정보, 실제 고객 진단 내용을 포함하지 않는다.
- 제출본에서는 핵심 설명을 최종 웹사이트 `README.md`에도 간결하게 반영한다.
