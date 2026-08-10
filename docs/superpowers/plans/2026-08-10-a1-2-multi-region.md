# A1-2 Multi-Region Bonus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an opt-in `--multi-region` mode that recommends 2–3 cities, searches Kakao restaurants per city, stores region-separated results, and preserves the existing single-region mode and cache.

**Architecture:** Keep the current single-file CLI and provider abstraction. Add mode-aware recommendation validation, region-loop search, mode-specific raw/cache validation, and a multi-region fallback/report prompt while leaving the existing single-mode data shape intact.

**Tech Stack:** Python 3.10+, standard library only, `unittest`, OpenAI Chat Completions, Kakao Local API.

## Global Constraints

- The default command `python travel_planner.py --date "YYYY-MM-DD"` remains single-region.
- `--multi-region` is optional and must not become a required condition for the base mission.
- Existing raw JSON without `mode` is treated as a valid single-region cache.
- Multi-region raw JSON uses `mode: "multi"`, `recommendation.recommended_cities`, `recommendation.region_details`, and `restaurants_by_city`.
- Never print, persist, or commit real API keys.
- Do not touch or stage unrelated root PNG files.
- Do not make real API calls during automated tests.

### Task 1: Add mode-aware recommendation schemas and CLI option

**Files:**
- Modify: `A1-2/travel_planner.py`
- Test: `A1-2/tests/test_travel_planner.py`

- [x] Write failing tests for parsing/validating a 3-city recommendation and rejecting fewer than 2 or more than 3 cities.
- [x] Run the focused tests and confirm they fail because multi-region validation is absent.
- [x] Add `--multi-region` with default `False` to `parse_args()`.
- [x] Add `validate_multi_recommendation()` and make `extract_json_object()`/recommendation generation select the single or multi schema by mode.
- [x] Keep `validate_recommendation()` and the existing single prompt behavior unchanged.
- [x] Run the focused schema tests and confirm they pass.

### Task 2: Implement region-loop search and mode-specific fallback reports

**Files:**
- Modify: `A1-2/travel_planner.py`
- Test: `A1-2/tests/test_travel_planner.py`

- [x] Write failing tests using a fake provider for three city searches, including one empty result and one raised API error.
- [x] Run the focused tests and confirm the loop behavior is not implemented.
- [x] Add a helper that iterates over normalized recommended cities, stores `restaurants_by_city`, and appends city-aware errors without stopping the loop.
- [x] Add a multi-region fallback report with separate city sections, local restaurants, schedule, and errors.
- [x] Extend report generation with a mode-specific prompt and required-section validation while preserving single mode.
- [x] Run the region-loop and report tests and confirm they pass.

### Task 3: Make cache loading/saving mode-aware

**Files:**
- Modify: `A1-2/travel_planner.py`
- Test: `A1-2/tests/test_travel_planner.py`

- [x] Write failing tests for multi-region cache reuse and single/multi cache mismatch.
- [x] Run the focused tests and confirm they fail before cache changes.
- [x] Add `mode` to newly saved raw JSON and treat a missing mode as single for backward compatibility.
- [x] Validate single caches only against single fields and multi caches only against multi fields.
- [x] Ensure cached Markdown without required mode-specific sections is replaced by the correct fallback without API calls.
- [x] Run all cache tests and confirm both modes remain isolated.

### Task 4: Wire the CLI and update documentation

**Files:**
- Modify: `A1-2/travel_planner.py`
- Modify: `A1-2/README.md`
- Modify: `A1-2/mission_analysis.md`
- Modify: `A1-2/pre_submission_checklist.md`
- Modify: `A1-2/handoff.md`

- [x] Wire `main()` to pass the selected mode through cache loading, recommendation generation, region search, report generation, and saving.
- [x] Add single and multi command examples, JSON shapes, cache compatibility rules, and error behavior to README.
- [x] Mark multi-region as implemented bonus and keep any unimplemented bonus explicitly labeled.
- [x] Record the test count and API-free verification accurately in handoff/checklist.
- [x] Run the full unittest suite, `py_compile`, help, invalid-date, and cache reuse checks.
- [x] Run `git diff --check`, inspect the staged file list, and verify no keys or root PNGs are included.

### Task 5: Review, commit, and push

**Files:**
- Review: all changed files above and the design/plan documents.

- [ ] Review the full diff against the approved design and mission original.
- [ ] Show the user the final changed-file scope before commit/push if it differs from the agreed scope.
- [ ] Commit only the A1-2 implementation, tests, docs, design, and plan files.
- [ ] Push `codex-a1-2-task-1-openai-compat` after verification.
