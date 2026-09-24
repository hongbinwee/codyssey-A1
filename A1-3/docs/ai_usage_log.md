# AI 코딩 도구 사용 과정 증빙

## 목적

A1-3 미션의 증빙 자료 중 “AI 코딩 도구 사용 과정(대화 로그 또는 스크린샷) 1세트”를 정리하기 위한 문서다.

## 기록 방식

아래 표에 주요 요청과 AI 응답 요약, 사람이 확인하거나 수정한 내용을 남긴다. 필요하면 실제 대화 화면 스크린샷을 `evidence/` 폴더에 저장한다.

| 날짜 | 요청 내용 | AI 응답/작업 요약 | 사람이 확인/수정한 내용 | 증빙 파일 |
| --- | --- | --- | --- | --- |
| 2026-07-17 | A1-3 미션 분석 요청 | 미션 핵심 요약, 필수 산출물, 요구사항 체크리스트 작성 | 원문 기준으로 분석 결과 검토 필요 |  |
| 2026-09-23 | MVP PRD의 진단·이메일 흐름과 관리자 범위를 구체화하고, 첫 화면 CTA 결정은 새 와이어프레임 검토 뒤로 미룸 | 진단 결과를 화면에 먼저 표시하고, 이메일 결과 발송과 상담 신청을 분리하는 흐름을 제안. 요청된 문의·진단 관리와 사이트 콘텐츠 편집 항목을 PRD 및 handoff에 반영 | 사용자가 이메일 흐름 결정을 AI에 위임하고 관리자 항목 반영을 요청함. CTA는 새 와이어프레임을 보고 결정하며 기존 HTML 목업은 사용하지 않기로 함. PRD는 사용자 검토 전 초안 | `docs/product_prd.md`, 대화 기록 |
| 2026-09-23 | 이전에 구체화한 AI 진단이 문서에서 미정으로 남은 문제를 지적하고 기존 대화 반영을 요청 | 이전 대화에서 승인된 5개 평가 영역, 최대 9개 적응형 문항, 규칙 기반 평가와 AI 설명 생성, 8개 결과 블록을 복원해 PRD·서비스 기획서·미션 현황·handoff를 갱신 | 사용자가 “이미 구체화했다”는 점을 확인했고, AI가 반복 설계 제안을 정정함. 세부 배점과 기술 구현만 미정으로 분리 | `docs/product_prd.md`, `docs/service_plan.md`, `mission_analysis.md`, `handoff.md`, 대화 기록 |
| 2026-09-23 | 승인된 제품 요구사항을 시스템 구성과 데이터 흐름으로 정리하도록 ARCHITECTURE.md 작성 요청 | Vercel 정적 사이트·Python Functions, Neon 접근 경계, 규칙 기반 진단과 AI 설명 생성, 관리자 API, 이메일 요청 흐름을 설계 초안으로 작성하고 공식 문서 링크를 기록 | 관리자 인증, 진단 데이터 저장 동의 범위, 이메일·AI 공급자는 아직 확정되지 않아 제안 또는 미정으로 표시함. 문서는 사용자 검토 전 | `ARCHITECTURE.md`, 대화 기록 |
| 2026-09-23 | AI 제공자와 익명 진단 저장 여부를 답하고, 기본 설정은 AI가 정리해 문서에 반영하도록 요청 | 공급자는 미정으로 유지하고 교체 가능한 API 경계를 제안. 익명 진단 원자료는 MVP에서 저장하지 않고 추후 비식별 집계 확장 지점만 남김. AI 길이·시간 제한, 관리자 인증, 다크 모드 기본값, 학습 기록과 키 유출 절차를 아키텍처·PRD·서비스 기획서·미션 분석·점검표·handoff에 반영 | 공급자와 월 예산은 사용자 미정으로 유지. 인증·시간 제한·다크 모드 동작은 권장 기본값이지 최종 승인이나 구현 완료가 아님을 확인. AI가 정한 수치와 보안 흐름은 실제 공급자·Vercel 런타임 검증 후 확정해야 함 | `ARCHITECTURE.md`, `docs/product_prd.md`, `docs/service_plan.md`, `mission_analysis.md`, `docs/learning_log.md`, `submission_checklist.md`, `handoff.md`, 대화 기록 |
| 2026-09-23 | 최근 ChatGPT 논의에서 확정된 Hero·Home 정보구조·빠른 상담 변경만 검토해 반영 요청 | Hero 메인 카피와 CTA 위계, Node Workflow 구성, Customer Problems, Home 섹션 순서, 진단과 빠른 상담의 역할·폼 항목을 PRD·서비스 기획서·구조 계획·아키텍처·체크리스트·handoff에 정리. 참고 사이트에서는 문제 장면→해결 단계→구체 예시→CTA의 스토리텔링 원칙만 참고 | 기존 PRD의 Hero 문구와 미정 CTA 상태를 수정. 실제 앱 코드와 Figma 파일은 만들지 않음. Desktop Workflow가 상하 전폭인지 오른쪽인지 지시가 상충해 미정으로 남김. Trust/Cases에는 검증된 자료만 허용하고 개인정보 문구는 미확정 처리 | `docs/product_prd.md`, `docs/service_plan.md`, `project_structure_plan.md`, `ARCHITECTURE.md`, `submission_checklist.md`, `mission_analysis.md`, `handoff.md`, 대화 기록 |

| 2026-09-23 | Desktop Hero Workflow 위치를 기존 전달문 기준으로 정리 | 사용자가 전달문에 맞춰 진행하라고 확인함. #2의 "좌우 2열이 아니라 상하 구조"를 우선해 Desktop 카피·CTA 위, 넓은 Workflow 아래로 문서의 미정 표기를 갱신 | #6의 "Hero 오른쪽" 문구는 좌우 2열로 적용하지 않는 것으로 정리. 앱 코드와 Figma 파일은 만들지 않음 | `docs/product_prd.md`, `docs/service_plan.md`, `project_structure_plan.md`, `mission_analysis.md`, `handoff.md`, 대화 기록 |
| 2026-09-23 | Figma 와이어프레임 기준 AX Ground 프론트엔드 구현 요청(HTML/CSS/Vanilla JS, 반응형·다크 모드·5개 슬라이드·폼 검증) | `index.html`·`diagnosis.html`·`contact.html`·`css/style.css`·`js/*.js`를 작성하고 Playwright로 1440/768/390 검증(27/27 통과). 구현 중 `renderQuestion()` 초기 호출 누락과 이메일 정규식 백슬래시 소실을 발견해 수정 | 사용자가 백엔드·Git·배포 연동은 금지하고 Figma 우선순위와 Hero 상하 구조를 명시함. Mux URL·법적 문구·Trust 근거는 미제공으로 표시 유지 | `index.html`, `diagnosis.html`, `contact.html`, `css/style.css`, `js/`, `evidence/`, `handoff.md`, 대화 기록 |
| 2026-09-24 | "모션그래픽이 안 된다, 폰트 위치가 안 맞는다" 피드백과 설치된 디자인 스킬 반영 요청 | Figma `get_motion_context`가 빈 결과를 반환해 `[SCROLL INTERACTION]` 주석 기준으로 모션을 직접 구현(Hero 진입, Workflow 스크롤 순차 생성, 마이크로 인터랙션). Pretendard Variable 추가와 Figma 타이포 불일치 수정. impeccable 탐지기로 대비·레이아웃 애니메이션 결함 3건 수정 | 사용자가 모션 부재와 폰트 위치 불일치를 지적하고 스킬 활용을 요청함. Figma에 모션 데이터·모바일 프레임이 없어 주석과 토큰을 근거로 자체 구현 | `css/style.css`, `js/workflow.js`, `js/app.js`, `js/diagnosis.js`, `index.html`, `evidence/`, 대화 기록 |
| 2026-09-24 | 브라우저 코멘트로 Workflow를 n8n 느낌으로 바꾸고(박스 크기·레이아웃·이모지), 문제 카드의 박스 크기·글자 레이아웃 조정 요청 | 워크플로우 노드를 이모지 아이콘+라벨+포트 카드로 재구성, 직선을 베지어 곡선으로 교체, jA/jB 정크션 허브로 19개 연결선 재배선, 스크롤 순차 생성 타이밍 재계산. 문제 카드는 space-between 상하 앵커와 자간 보정. 세로 모드 인라인 좌표 덮어쓰기 결함을 !important 해제로 수정 후 검증 27/27 통과 | 사용자가 n8n 캔버스 스크린샷을 첨부해 방향을 제시하고, 카드·글자 레이아웃 조정을 요청함. n8n UI를 그대로 복제하지 않고 톤만 참조 | `js/workflow.js`, `css/style.css`, `evidence/check-wf-canvas.png`, `evidence/check-wf-mobile.png`, `evidence/check-problems.png`, `handoff.md`, 대화 기록 |

| 2026-09-24 | 오픈디자인v1.html 목업 기준으로 A1-3/오픈디자인 폴더에 AX Ground 화면을 이어서 구현 요청(반응형·다크 모드·5개 슬라이드·HLS 자리·폼 검증, 백엔드 미연동) | `오픈디자인/index.html` 단일 페이지에 확정 IA 순서로 배치하고 Hero Workflow 노드 5개와 슬라이드 5개를 1:1 연결한 캐러셀을 구현. 목업의 관리자 데모 섹션은 확정 IA에 없어 제외. 진단은 7문항 위자드+클라이언트 검증까지만 동작하고 완료 시 "AI 분석 연동을 준비하고 있어요" 안내. Chrome 자동화로 1440/768/390·Light/Dark·슬라이드 전환·폼 게이트를 확인했고 콘솔 오류와 가로 스크롤 없음 | 사용자가 목업을 시각 기준·문서를 기능 기준으로 지정하고 Desktop Workflow 상하 구조를 재확인함. Mux Playback URL, 개인정보 법적 문구, 실제 사례·수치는 미제공 상태 유지. 목업의 관리자 데모는 IA 밖이라 제외한 점을 보고에 명시 | `오픈디자인/index.html`, `오픈디자인/css/style.css`, `오픈디자인/js/`, `오픈디자인/serve.mjs`, `오픈디자인/README.md`, `handoff.md`, 대화 기록 |

| 2026-09-24 | A1-3 루트 화면을 최종 기준으로 확정하고, 미션 필수인 AI 진단의 입력→Python API→화면 결과 흐름 완성 요청(디자인 재작업 없이) | `api/diagnose.py`(Vercel Function, 16KiB·필수값·선택값 검증, JSON 오류 코드), `api_services/diagnosis_rules.py`(5영역 점수·추천 경로 초기안), `api_services/ai_provider.py`(교육기관 OpenAI 호환 게이트웨이, gpt-5.5, stdlib, AI_API_KEY 환경변수, reasoning_effort 미사용), mock 결과·requirements.txt·.env.example을 구현. 프론트는 연락처 카드를 결과 뒤 후속 패널로 이동하고 로딩(8초 안내/25초 타임아웃)·오류·재시도 화면을 추가. 로컬은 run_api.py --mock + serve.mjs /api 프록시로 통합 검증(백엔드 12/12, HTTP 10/10, Playwright 33/33) | 사용자가 최종 기준을 루트 화면으로 확정하고 오픈디자인·first-screen은 실험본 보존으로 지정. API 키를 환경 변수로만 읽고 값을 복사하지 않는 조건, reasoning_effort 미사용, 비용 절약을 위한 최소 호출을 지시함. AI_API_KEY가 환경에 없어 실제 호출은 미검증으로 표시하고 사용자 행동만 안내 | `api/diagnose.py`, `api_services/`, `requirements.txt`, `.env.example`, `js/diagnosis.js`, `diagnosis.html`, `css/style.css`, `evidence/`, `handoff.md`, 대화 기록 |

| 2026-09-24 | GitHub `hongbinwee/codyssey-A1` 푸시에 앞서 A1-3 제출 패키지 문서 정리 요청(커밋·푸시·Vercel 설정은 금지) | README를 제품 README로 재작성(로컬 mock 실행·환경 변수·배포 URL 자리·미연동 범위), `docs/service_plan.md`를 실제 구현(8문항, 실패 처리 구현, copa 게이트웨이·gpt-5.5, 익명 미저장, 후속 패널)으로 갱신, `.gitignore` 추가(.env 계열·.vercel·__pycache__·.agents·.superpowers·실험본 폴더·루트 handoff.md), 스크린샷 개인정보 포함 여부 확인(테스트 입력만), mock 결과 캡처를 실제 AI 증빙으로 표시하지 않음을 명시 | 사용자가 원격 main이 로컬보다 A1-2 커밋 5개 앞선 상태임을 알리고 동기화·커밋·푸시를 금지함. ARCHITECTURE·PRD는 공개 제출 패키지에서 제외 후보로 분류. 실제 gpt-5.5 응답 캡처와 AI 코딩 도구 대화 로그는 별도 증빙 필요로 보고 | `README.md`, `docs/service_plan.md`, `.gitignore`, `submission_checklist.md`, `docs/ai_usage_log.md`, `docs/learning_log.md`, 대화 기록 |
| 2026-09-24 | 수정된 `gpt-5.5` 어댑터를 가상 답변으로 1회 호출하고 제출용 증빙 상태 확인 | mock 백엔드 테스트 12/12와 HTTP 통합 테스트 10/10 통과. 실제 게이트웨이 호출은 DNS 조회 후에도 이 로컬 환경에서 TCP 443 연결에 실패해 응답을 확인하지 못함. 증빙 안내를 갱신해 진단 결과 화면을 mock으로 명확히 표시하고, 실제 AI 응답 및 대화 화면 캡처를 남은 항목으로 기록 | 테스트 입력에는 가상 팀 정보만 사용. 키 값은 소스·문서·스크린샷에 기록하지 않음. 실호출 미확인을 성공으로 표현하지 않고 Vercel 환경 변수 설정 후 재검증 필요로 구분 | `evidence/README.md`, `evidence/test_backend.py`, `evidence/test_api_http.py`, `evidence/desktop-1440-diagnosis-result.png`, 대화 기록 |

## 최신 상태 보완 (2026-09-24)

- 사용자가 README에 배포 전 문구가 남아 있음을 지적해 미션 제출 문서의 배포·검증 상태를 다시 확인했다.
- GitHub 기준 저장소 `hongbinwee/codyssey-A1`의 `main`에는 A1-3 패키지가 이미 포함되어 있음을 확인했다. 이번 문서 변경은 로컬 검토 후 A1-3 범위만 선별해 반영한다.
- 배포 사이트 주소를 README와 증빙 안내에 기록하되, 배포 환경에서 실제 AI 요청이 성공했는지는 확인 전 상태로 남긴다. Vercel 환경 변수 설정 여부와 실제 응답 성공을 같은 것으로 취급하지 않는다.
- 공유된 와이어프레임 이미지는 참고 예시로 분류하며 미션 필수 산출물로 보지 않는다.
- 갱신한 파일: `README.md`, `docs/service_plan.md`, `docs/learning_log.md`, `evidence/README.md`, `mission_analysis.md`, `submission_checklist.md`.
- 이 문서의 요약은 미션이 요구하는 대화 로그 또는 스크린샷 세트를 대신하지 않으므로 실제 AI 도구 사용 증빙을 별도로 준비해야 한다.

## 기록해야 할 장면

- [ ] 미션 원문을 분석하는 장면
- [ ] 서비스 아이디어를 정리하는 장면
- [ ] HTML/CSS/JavaScript 코드를 만드는 장면
- [ ] Python API 코드를 만드는 장면
- [ ] 오류가 발생했을 때 원인을 찾고 수정하는 장면
- [ ] 배포 또는 배포 오류를 점검하는 장면

## 주의사항

- API 키가 화면에 보이는 스크린샷은 제출하지 않는다.
- `.env` 내용, Vercel 환경 변수 값, API 키 문자열은 가린다.
- AI가 만든 내용을 그대로 제출하지 말고, 원문 요구사항과 실제 동작 기준으로 검토한 흔적을 남긴다.
