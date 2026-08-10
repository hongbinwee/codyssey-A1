# A1-2 Runtime and Evaluation Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A1-2를 실제 설정된 OpenAI/Kakao 키로 실행 가능하게 만들고, 사전평가에서 지적된 핵심 보완점과 제출 문서를 검증 가능한 상태로 정리한다.

**Architecture:** 현재 표준 라이브러리 단일 파일 CLI 구조를 유지한다. OpenAI 호출은 모델별 지원 파라미터를 안전하게 구성하고, Kakao 호출은 검색 제공자 인터페이스 뒤로 감싼다. 날짜별 raw 결과를 재사용하는 캐시와 도시명 정규화를 추가하되, 기존 결과 형식과 오류 누적 흐름은 보존한다.

**Tech Stack:** Python 3.10+, 표준 라이브러리(`argparse`, `json`, `urllib`, `unittest`), OpenAI Chat Completions API, Kakao Local Keyword Search API, Markdown/JSON.

## Global Constraints

- API 키는 `A1-2/.env` 또는 환경변수에서만 읽고 코드·README·결과·커밋에 실제 값을 기록하지 않는다.
- CLI는 터미널에서 실행하며 `-date`와 `--date`로 `YYYY-MM-DD` 날짜를 받는다.
- LLM 1차 결과는 `recommended_city`, `weather`, `events`, `reason` 필수 키와 타입을 검증한다.
- `events`는 1~3개의 문자열이고 `reason`은 2~4문장이라는 미션 기준을 검증한다.
- LLM JSON 파싱 실패 재시도는 최대 1회이며, HTTP/API 요청 실패를 JSON 파싱 재시도로 오인하지 않는다.
- Kakao 검색 실패나 결과 0건에도 프로그램은 중단하지 않고 최종 리포트에 `데이터 없음`을 기록한다.
- 결과는 `A1-2/results/YYYY-MM-DD_raw.json`과 `A1-2/results/YYYY-MM-DD_travel_plan.md`에 저장한다.
- 기존 사용자가 남긴 `A1-2/.env.example`, `A1-2/A1-2 미션 원문.md`, 루트 PNG 파일은 작업 범위에 포함하지 않으며 루트 PNG는 절대 스테이징하지 않는다.
- 구현은 서브에이전트가 담당하고, 메인 에이전트는 각 작업 후 diff·테스트·실행 결과를 직접 재확인한다.

## File Map

- Modify: `A1-2/travel_planner.py` — 모델 호환성, 오류 분류, 스키마 검증, 검색 추상화, 도시 정규화, 캐시, 저장 실패 처리를 구현한다.
- Create: `A1-2/tests/test_travel_planner.py` — 외부 네트워크 없이 핵심 함수와 결과 형식을 회귀 검증한다.
- Modify: `A1-2/README.md` — GET/POST 선택 근거, 프롬프트·재시도 정책, 오류 스키마, 401/403 점검, 캐시·정규화 동작을 문서화한다.
- Modify: `A1-2/handoff.md` — 실제 검증 범위와 다음 작업을 현재 상태로 갱신한다.
- Modify: `AGENTS.md` — 서브에이전트 구현 → 작업별 리뷰 → 메인 직접 검증 워크플로우를 지속 규칙으로 기록한다.
- Create: `.superpowers/sdd/a1-2-runtime-and-evaluation-improvements/progress.md` — 이 계획의 작업 ledger를 기록한다(작업 스크래치 파일).

---

### Task 1: OpenAI runtime compatibility and offline regression coverage

**Files:**
- Modify: `A1-2/travel_planner.py`
- Create: `A1-2/tests/test_travel_planner.py`

**Interfaces:**
- `call_openai_chat(api_key, model, messages, temperature=None)` keeps the existing return type (`str`) and omits unsupported sampling parameters for GPT-5-family models.
- `validate_recommendation(data)` raises `ValueError` for missing keys, wrong types, event counts outside 1–3, non-string events, or reasons outside 2–4 sentences.
- `generate_recommendation(...)` retries only parse/validation failures once; transport, authentication, quota, and HTTP failures are recorded with their existing error shape and are not retried as parse failures.

- [ ] **Step 1: Add offline tests for request payload and validation boundaries.**

  Mock the module's JSON request function so tests never call the network. Assert that a GPT-5-family payload does not contain `temperature`, a legacy model can retain a supported temperature, valid recommendations pass, and invalid event/reason boundaries raise `ValueError`.

- [ ] **Step 2: Add tests for retry classification and fallback behavior.**

  Use deterministic mocked responses to assert one retry for malformed JSON, zero parse retries for an HTTP failure, and a Markdown fallback containing the required headings when final report generation fails.

- [ ] **Step 3: Implement the smallest code change that makes the tests pass.**

  Preserve the existing public CLI and result keys. Keep error messages safe and exclude response bodies that could contain sensitive request information.

- [ ] **Step 4: Run the focused and complete offline checks.**

  Run `python3 -m unittest discover -s A1-2/tests -v`, `python3 -m py_compile A1-2/travel_planner.py`, `python3 A1-2/travel_planner.py --help`, and the invalid-date check. All must pass without network access.

- [ ] **Step 5: Commit the task in the agent worktree.**

  Use commit message `fix: make A1-2 OpenAI calls model compatible` and report the commit hash, changed files, tests, and any assumptions.

### Task 2: Search abstraction, city normalization, cache, and write-error handling

**Files:**
- Modify: `A1-2/travel_planner.py`
- Modify: `A1-2/tests/test_travel_planner.py`

**Interfaces:**
- `PlaceSearchProvider.search(city, errors)` returns a list of restaurant dictionaries and owns provider-specific API details.
- `KakaoPlaceSearchProvider(api_key).search(city, errors)` implements the existing Kakao Local behavior.
- `normalize_city_name(city)` returns a stable search label, including equivalent forms such as `서울시` → `서울`.
- The date-specific raw JSON is a cache only when it is valid JSON and contains the same date, recommendation, restaurants, and errors keys; invalid or incomplete cache files are ignored and replaced.

- [ ] **Step 1: Add offline tests for provider delegation and city normalization.**

  Test that a fake provider receives the normalized city and that `서울`, `서울시`, and surrounding whitespace resolve to the same search label without invoking the network.

- [ ] **Step 2: Add offline tests for valid-cache reuse and invalid-cache bypass.**

  Use a temporary results directory. Assert that a valid date-matching raw file is reused without calling the LLM/provider, while malformed or date-mismatched JSON is ignored and the normal path remains available.

- [ ] **Step 3: Implement the provider interface and normalization.**

  Keep Kakao's HTTP GET and authentication classification behavior unchanged behind the provider class. Do not add a second remote provider.

- [ ] **Step 4: Implement the conservative date cache.**

  Reuse the complete raw result for the same date before making paid calls. On cache hit, regenerate or reuse the matching Markdown report without exposing keys. Cache read/write failures become structured errors and do not crash the CLI.

- [ ] **Step 5: Handle output write failures explicitly.**

  Catch `OSError` separately for raw JSON and Markdown writes, append `OUTPUT_WRITE_ERROR` entries with `step`, `type`, and safe `message`, and show a user-facing failure message.

- [ ] **Step 6: Run focused tests and commit.**

  Run `python3 -m unittest discover -s A1-2/tests -v` and `python3 -m py_compile A1-2/travel_planner.py`. Commit as `feat: harden A1-2 search and result reuse` and report the hash.

### Task 3: Documentation, handoff, and durable subagent workflow

**Files:**
- Modify: `A1-2/README.md`
- Modify: `A1-2/handoff.md`
- Modify: `AGENTS.md`

**Interfaces:**
- README examples use the current configurable `OPENAI_MODEL` without recording a real key.
- Handoff distinguishes confirmed offline checks, confirmed live checks, and remaining checks.
- AGENTS records that implementation is delegated to subagents, each task receives a fresh reviewer, and the main agent directly verifies merged changes before claiming completion.

- [ ] **Step 1: Update README's API method explanation.**

  Explain that OpenAI uses POST because the prompt/messages are sent in a request body, while Kakao keyword search uses GET because the search query and filters are read-only query parameters. State that this is an HTTP design rationale, not a security guarantee.

- [ ] **Step 2: Document the prompt and retry policy.**

  Include the JSON-only required keys, the 1–3 event and 2–4 sentence validation rules, and that only parsing/validation failures receive one repair retry; HTTP/auth/quota failures are not reparsed.

- [ ] **Step 3: Document error schema and troubleshooting.**

  Show `step`, `type`, and `message` as the error record shape. Add 401/403 checks for `.env` variable names, header format, Kakao REST key permissions, and OpenAI project/model access without printing secrets.

- [ ] **Step 4: Document cache, normalization, and optional scope.**

  Explain same-date raw reuse, conservative invalid-cache bypass, city-label normalization, and that only one Kakao provider is currently implemented even though the internal interface permits replacement.

- [ ] **Step 5: Update handoff with evidence and next action.**

  Remove the stale “keys are not configured” statement. Record the exact offline commands and live execution result at a secret-safe summary level; leave any unresolved external limitation explicit.

- [ ] **Step 6: Record the workflow in AGENTS.md.**

  Add a Korean workflow section covering plan/spec first, disjoint subagent tasks, fresh task review, main-agent direct verification, no secret output, and selective staging that excludes unrelated root PNGs.

- [ ] **Step 7: Commit the documentation task.**

  Use commit message `docs: record A1-2 validation and agent workflow` and report changed files and the commit hash.

### Task 4: Whole-branch review and main-agent verification

**Files:**
- Review all changes in `A1-2/` and `AGENTS.md`; modify only through a scoped fix subagent if a finding is confirmed.

- [ ] **Step 1: Run a fresh diff and secret-safe status audit.**

  Confirm only intended files are changed, `.env` is ignored, no API key value appears in tracked or untracked deliverables, and root PNGs remain unstaged.

- [ ] **Step 2: Run the full offline verification suite.**

  Run `python3 -m unittest discover -s A1-2/tests -v`, `python3 -m py_compile A1-2/travel_planner.py`, CLI help, invalid-date, and missing-key checks.

- [ ] **Step 3: Run one live end-to-end execution with the configured date.**

  Run `python3 A1-2/travel_planner.py --date "2026-03-15"` from `A1-2/` only if the key presence check passes. Inspect the generated raw JSON and Markdown structurally without printing secret values. A provider-side failure may remain in `errors`, but the program must save both outputs.

- [ ] **Step 4: Dispatch a final broad review subagent.**

  The reviewer checks the mission original, this plan, the final diff, test output, and generated output shape. It must report findings with severity and file/line evidence, not merely restate the implementation.

- [ ] **Step 5: Resolve or explicitly record final findings.**

  Confirm all load-bearing findings are fixed or document why they are outside the original mission scope. Only then report completion; do not claim live success if the API run did not reach saved outputs.
