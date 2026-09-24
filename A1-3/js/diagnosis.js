/* AX Ground — diagnosis.js
   AI·AX 맞춤 진단 플로우.
   - 8개 문항 → POST /api/diagnose(로딩/오류/타임아웃 처리) → 결과 8블록 렌더
   - 결과는 이메일 입력 없이 화면에서 먼저 확인한다 (PRD §4).
   - 결과 아래 후속 패널(결과 이메일/맞춤 상담)은 동의 게이트만 구현.
     실제 접수 API(/api/requests)는 아직 미구현이므로 제출 시 안내만 표시한다.
   - 연락처는 AI 요청에 포함하지 않고, 익명 진단은 저장하지 않는다. */
(() => {
  const $ = (sel, root = document) => root.querySelector(sel);

  /* PRD의 9개 문항 주제를 Figma의 8단계 진행 표시(2/8)에 맞춰 8문항으로 구성.
     (PRD 5번·6번 "개선 업무 + 업무 기회도"를 한 문항으로 병합)
     서버 api_services/diagnosis_rules.py 의 QUESTION_IDS·ALLOWED_OPTIONS와 동일하게 유지 */
  const QUESTIONS = [
    {
      id: "role",
      title: "Q1. 어떤 입장에서 알아보고 계신가요?",
      helper: "현재 상황에 가장 가까운 하나를 선택해 주세요.",
      type: "radio",
      options: ["개인 학습자", "기업 대표·임원", "팀장·실무 책임자", "교육·인사 담당자", "기획·IT·개발 담당자"],
    },
    {
      id: "stage",
      title: "Q2. 현재 조직에서 AI를 어느 정도 활용하고 있나요?",
      helper: "개인과 조직 중 더 가까운 기준으로 선택해 주세요.",
      type: "radio",
      options: ["거의 사용하지 않음", "개인적으로 일부 사용", "팀 단위로 활용", "업무 프로세스에 정착", "전사적으로 활용"],
    },
    {
      id: "goal",
      title: "Q3. AI로 가장 먼저 만들고 싶은 변화는 무엇인가요?",
      helper: "지금 가장 중요한 목표를 하나 선택해 주세요.",
      type: "radio",
      options: ["역량 향상", "반복 업무 시간 단축", "결과물 품질 향상", "고객 응대·영업 개선", "AI 서비스·도구 제작", "우선순위 탐색"],
    },
    {
      id: "target",
      title: "Q4. 어떤 업무나 팀에 적용하고 싶은가요?",
      helper: "업종·직무·참여 인원 중 아는 범위만 적어 주세요.",
      type: "textarea",
      placeholder: "예: 8명 규모의 콘텐츠 마케팅 팀",
    },
    {
      id: "work",
      title: "Q5. 가장 개선하고 싶은 업무는 무엇인가요?",
      helper: "현재 업무 순서, 병목, 사람이 판단해야 하는 부분을 자유롭게 적어 주세요.",
      type: "textarea",
      placeholder: "예: 매주 여러 자료를 모아 보고서 초안을 만드는 데 시간이 걸립니다.",
    },
    {
      id: "frequency",
      title: "Q6. 그 업무는 얼마나 자주, 얼마나 걸리나요?",
      helper: "발생 빈도와 1회 소요 시간, 참여 인원을 대략 적어 주세요.",
      type: "textarea",
      placeholder: "예: 매주 1회, 3명이 각 2시간씩 사용",
    },
    {
      id: "data",
      title: "Q7. 현재 자료와 시스템 환경은 어떤가요?",
      helper: "가장 가까운 항목을 하나 선택해 주세요.",
      type: "radio",
      options: ["문서·엑셀 중심", "메일·메신저 중심", "CRM·사내 시스템 보유", "자료 디지털화 전", "개인정보·기밀 포함"],
    },
    {
      id: "readiness",
      title: "Q8. 언제, 어떤 기준으로 시작하고 싶나요?",
      helper: "희망 시작 시기와 성공 기준을 함께 적어 주세요. (예: 시간 절감, 결과물 완성, 활용률 향상)",
      type: "textarea",
      placeholder: "예: 한 달 안에 한 가지 업무를 시범 적용하고 팀이 함께 써보는 것",
    },
  ];

  const card = $("#questionCard");
  if (!card) return;

  const loadingView = $("#loadingView");
  const errorView = $("#errorView");
  const resultView = $("#resultView");
  const mount = $("#questionMount");
  const titleEl = $("#questionTitle");
  const helperEl = $("#questionHelper");
  const errorEl = $("#questionError");
  const prevBtn = $("#prevQuestion");
  const nextBtn = $("#nextQuestion");
  const progressLabel = $("#progressLabel");
  const progressFill = $("#progressFill");
  const progressBar = $("#progressBar");

  const answers = {};
  let index = 0;
  let submitting = false;

  const TOTAL = QUESTIONS.length;

  const setProgress = (n, label) => {
    progressLabel.textContent = label || n + " / " + TOTAL;
    progressFill.style.transform = "scaleX(" + Math.min(1, n / TOTAL) + ")";
    progressBar.setAttribute("aria-valuenow", String(n));
    progressBar.setAttribute("aria-valuemax", String(TOTAL));
  };

  const showOnly = (view) => {
    card.hidden = view !== card;
    loadingView.hidden = view !== loadingView;
    errorView.hidden = view !== errorView;
    resultView.hidden = view !== resultView;
  };

  /* ---------- 문항 렌더링 ---------- */
  const renderQuestion = () => {
    const q = QUESTIONS[index];
    titleEl.textContent = q.title;
    helperEl.textContent = q.helper;
    errorEl.textContent = "";
    setProgress(index + 1);
    prevBtn.disabled = index === 0;
    nextBtn.textContent = index === TOTAL - 1 ? "진단 결과 보기 →" : "다음 →";

    mount.innerHTML = "";
    if (q.type === "radio") {
      const list = document.createElement("div");
      list.className = "choice-list";
      list.setAttribute("role", "radiogroup");
      q.options.forEach((opt) => {
        const label = document.createElement("label");
        label.className = "choice";
        const input = document.createElement("input");
        input.type = "radio";
        input.name = "answer";
        input.value = opt;
        if (answers[q.id] === opt) input.checked = true;
        const span = document.createElement("span");
        span.textContent = opt;
        label.append(input, span);
        list.appendChild(label);
      });
      mount.appendChild(list);
    } else {
      const field = document.createElement("div");
      field.className = "field";
      const ta = document.createElement("textarea");
      ta.name = "answer";
      ta.maxLength = 500;
      ta.placeholder = q.placeholder;
      ta.value = answers[q.id] || "";
      ta.setAttribute("aria-label", q.title);
      field.appendChild(ta);
      mount.appendChild(field);
    }
    const first = mount.querySelector("input, textarea");
    if (first) first.focus();
  };

  const readAnswer = () => {
    const checked = mount.querySelector('input[name="answer"]:checked');
    if (checked) return checked.value;
    const ta = mount.querySelector('textarea[name="answer"]');
    return ta ? ta.value.trim() : "";
  };

  /* ---------- API 호출 ---------- */
  const SLOW_HINT_MS = 8000;      // 8초 경과 시 진행 안내 (PRD 권장 기본값)
  const TOTAL_TIMEOUT_MS = 25000; // 브라우저 전체 타임아웃 25초

  const requestDiagnosis = async () => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), TOTAL_TIMEOUT_MS);
    try {
      const res = await fetch("/api/diagnose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
        signal: controller.signal,
      });
      let data = null;
      try { data = await res.json(); } catch (e) { data = null; }
      if (!res.ok) {
        const msg = data && data.error && data.error.message
          ? data.error.message
          : "진단 서버가 오류를 반환했습니다. (HTTP " + res.status + ")";
        const err = new Error(msg);
        err.status = res.status;
        throw err;
      }
      if (!data || !data.ok || !data.result) {
        throw new Error("진단 결과 형식을 해석할 수 없습니다.");
      }
      return data;
    } catch (e) {
      if (e.name === "AbortError") {
        throw new Error("응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.");
      }
      if (e instanceof TypeError) {
        throw new Error("진단 서버에 연결할 수 없습니다. 네트워크 상태를 확인해 주세요.");
      }
      throw e;
    } finally {
      clearTimeout(timer);
    }
  };

  /* ---------- 결과 렌더링 ---------- */
  const SCORE_LABELS = {
    goal_clarity: "목표 명확도",
    people_readiness: "인력·교육 준비도",
    work_opportunity: "업무 기회도",
    data_readiness: "데이터·기술 준비도",
    security_ops: "보안·운영 준비도",
  };

  const fillList = (el, items, renderItem) => {
    el.innerHTML = "";
    (items || []).forEach((item) => {
      const li = document.createElement("li");
      renderItem(li, item);
      el.appendChild(li);
    });
  };

  const renderResult = (data) => {
    const r = data.result;
    const ev = data.evaluation || {};

    $("#resultSummary").textContent = r.summary || "";

    // 입력 답변 요약(근거 표시)
    const summary = $("#answerSummary");
    summary.innerHTML = "";
    QUESTIONS.forEach((q) => {
      const li = document.createElement("li");
      const strong = document.createElement("strong");
      strong.textContent = q.title.replace(/^Q\d+\.\s*/, "").slice(0, 14) + "…";
      const span = document.createElement("span");
      const val = answers[q.id] || "";
      span.textContent = val.length > 60 ? val.slice(0, 60) + "…" : val;
      li.append(strong, span);
      summary.appendChild(li);
    });

    // 5개 영역 평가 (규칙 기반 참고 점수)
    const scoreList = $("#scoreList");
    scoreList.innerHTML = "";
    Object.keys(SCORE_LABELS).forEach((key) => {
      const item = ev.scores && ev.scores[key];
      if (!item) return;
      const li = document.createElement("li");
      const label = document.createElement("span");
      label.className = "score-label";
      label.textContent = SCORE_LABELS[key];
      const meter = document.createElement("span");
      meter.className = "score-meter";
      meter.setAttribute("aria-hidden", "true");
      for (let i = 1; i <= 5; i++) {
        const dot = document.createElement("i");
        if (i <= item.score) dot.className = "on";
        meter.appendChild(dot);
      }
      const sr = document.createElement("span");
      sr.className = "sr-only";
      sr.textContent = item.score + "점(5점 만점)";
      const note = document.createElement("span");
      note.className = "score-note";
      note.textContent = item.note;
      li.append(label, meter, sr, note);
      scoreList.appendChild(li);
    });

    fillList($("#resultTasks"), r.priority_tasks, (li, t) => { li.textContent = t; });

    $("#resultPath").textContent = (r.recommended_path && r.recommended_path.label) || "—";
    $("#resultPathReason").textContent = (r.recommended_path && r.recommended_path.reason) || "";

    const edu = $("#resultEducation");
    edu.innerHTML = "";
    if (r.education) {
      const rows = [
        ["추천 대상", r.education.audience],
        ["교육 모듈", Array.isArray(r.education.modules) ? r.education.modules.join(" · ") : r.education.modules],
        ["실습 결과물", r.education.outcome],
        ["권장 방식", r.education.format],
      ];
      rows.forEach(([dt, dd]) => {
        if (!dd) return;
        const dtEl = document.createElement("dt");
        dtEl.textContent = dt;
        const ddEl = document.createElement("dd");
        ddEl.textContent = dd;
        edu.append(dtEl, ddEl);
      });
    }

    fillList($("#resultAx"), r.ax_candidates, (li, c) => {
      const head = document.createElement("strong");
      head.textContent = c.task + (c.verify_first ? " (우선 검증)" : "");
      const meta = document.createElement("span");
      meta.className = "ax-meta";
      meta.textContent = "난이도 " + (c.difficulty || "—") + " · " + (c.expected_effect || "");
      li.append(head, meta);
    });

    fillList($("#resultRoadmap"), r.roadmap, (li, p) => {
      const head = document.createElement("strong");
      head.textContent = p.phase || "";
      const items = document.createElement("span");
      items.textContent = Array.isArray(p.items) ? p.items.join(" · ") : "";
      li.append(head, items);
    });

    fillList($("#resultCautions"), r.cautions, (li, t) => { li.textContent = t; });

    $("#resultService").textContent = (r.consultation && r.consultation.service) || "—";
    fillList($("#resultTopics"), r.consultation && r.consultation.topics, (li, t) => { li.textContent = t; });

    $("#resultDisclaimer").textContent =
      (data.disclaimer || "") + " 입력한 답변은 저장되지 않습니다.";
  };

  /* ---------- 상태 전환 ---------- */
  let slowTimer = null;

  const showLoading = () => {
    showOnly(loadingView);
    setProgress(TOTAL, "분석 중");
    $("#loadingStatus").textContent = "규칙 평가와 맞춤 제안을 생성하는 중입니다.";
    clearTimeout(slowTimer);
    slowTimer = setTimeout(() => {
      $("#loadingStatus").textContent = "응답이 지연되고 있습니다. 조금만 더 기다려 주세요.";
    }, SLOW_HINT_MS);
  };

  const showError = (message) => {
    clearTimeout(slowTimer);
    showOnly(errorView);
    setProgress(TOTAL, "오류");
    $("#errorMessage").textContent = message;
    $("#errorRetry").focus();
  };

  const showResult = (data) => {
    clearTimeout(slowTimer);
    renderResult(data);
    showOnly(resultView);
    setProgress(TOTAL, "완료");
    resultView.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  const runDiagnosis = async () => {
    if (submitting) return;
    submitting = true;
    showLoading();
    try {
      const data = await requestDiagnosis();
      showResult(data);
    } catch (e) {
      showError(e.message || "일시적인 오류가 발생했습니다.");
    } finally {
      submitting = false;
    }
  };

  /* ---------- 이벤트 ---------- */
  card.addEventListener("submit", (e) => {
    e.preventDefault();
    const value = readAnswer();
    if (!value) {
      errorEl.textContent = "필수 항목입니다. 현재 상황에 가까운 답을 선택하거나 입력해 주세요.";
      const first = mount.querySelector("input, textarea");
      if (first) first.focus();
      return;
    }
    answers[QUESTIONS[index].id] = value;
    if (index === TOTAL - 1) runDiagnosis();
    else { index += 1; renderQuestion(); }
  });

  prevBtn.addEventListener("click", () => {
    if (index > 0) {
      answers[QUESTIONS[index].id] = readAnswer();
      index -= 1;
      renderQuestion();
    }
  });

  $("#errorRetry").addEventListener("click", runDiagnosis);
  $("#errorBack").addEventListener("click", () => {
    index = TOTAL - 1;
    showOnly(card);
    renderQuestion();
  });

  /* ---------- 후속 패널 (결과 이메일 / 맞춤 상담) ---------- */
  const dgEmail = $("#dgEmail");
  const emailBtn = $("#dgEmailBtn");
  const consultBtn = $("#dgConsultBtn");
  const consentEmail = $("#dgConsentEmail");
  const consentConsult = $("#dgConsentConsult");
  const followupStatus = $("#followupStatus");
  let followupAction = null;

  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const updateFollowupButtons = () => {
    emailBtn.disabled = !consentEmail.checked;
    consultBtn.disabled = !consentConsult.checked;
  };
  [consentEmail, consentConsult].forEach((c) => c.addEventListener("change", updateFollowupButtons));
  [emailBtn, consultBtn].forEach((b) => b.addEventListener("click", () => { followupAction = b.dataset.action; }));

  $("#followupPanel").addEventListener("submit", (e) => {
    e.preventDefault();
    const emailField = dgEmail.closest(".field");
    const errEl = emailField.querySelector(".field-error");
    const emailValue = dgEmail.value.trim();

    if (!EMAIL_RE.test(emailValue)) {
      errEl.textContent = "후속 요청에는 유효한 이메일이 필요합니다.";
      emailField.classList.add("has-error");
      dgEmail.focus();
      return;
    }
    errEl.textContent = "";
    emailField.classList.remove("has-error");

    // /api/requests 는 아직 미구현: 실제 전송·저장 없이 안내만 표시한다.
    followupStatus.className = "form-status";
    followupStatus.textContent =
      (followupAction === "consult" ? "상담 요청" : "결과 이메일") +
      " 접수 API는 아직 연동 전입니다. 현재는 contact.html의 빠른 상담으로 문의할 수 있습니다.";
  });

  renderQuestion();
})();
