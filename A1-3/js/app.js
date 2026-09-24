/* AX Ground — app.js
   공통 UI: 모바일 메뉴, 스크롤 리빌, 빠른 상담 폼 클라이언트 검증.
   실제 전송은 백엔드(/api/...) 연동 전이므로 하지 않는다. */
(() => {
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  /* JS 활성 시에만 리빌 초기 상태(숨김)를 적용 — JS 실패 시 콘텐츠가 그대로 보이도록 */
  document.documentElement.classList.add("js");

  /* ---------- Hero 진입 모션 (한 번만) ---------- */
  const hero = $(".hero");
  if (hero) requestAnimationFrame(() => hero.classList.add("is-in"));

  /* ---------- 모바일 메뉴 ---------- */
  const menuToggle = $("#menuToggle");
  const mobileNav = $("#mobileNav");
  if (menuToggle && mobileNav) {
    const setOpen = (open) => {
      mobileNav.classList.toggle("is-open", open);
      menuToggle.setAttribute("aria-expanded", String(open));
      menuToggle.setAttribute("aria-label", open ? "메뉴 닫기" : "메뉴 열기");
    };
    menuToggle.addEventListener("click", () => {
      setOpen(!mobileNav.classList.contains("is-open"));
    });
    mobileNav.addEventListener("click", (e) => {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && mobileNav.classList.contains("is-open")) {
        setOpen(false);
        menuToggle.focus();
      }
    });
    // 화면이 커지면 패널 정리
    window.matchMedia("(min-width: 1025px)").addEventListener("change", (e) => {
      if (e.matches) setOpen(false);
    });
  }

  /* ---------- 스크롤 리빌 ---------- */
  const revealTargets = $$("[data-reveal]");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (revealTargets.length && !reduced && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add("is-revealed"));
  }

  /* ---------- 빠른 상담 폼 (클라이언트 검증만) ---------- */
  const form = $("#quickConsultForm");
  if (form) {
    const email = $("#qcEmail");
    const concern = $("#qcConcern");
    const org = $("#qcOrg");
    const interest = $("#qcInterest");
    const consent = $("#qcConsent");
    const submit = $("#qcSubmit");
    const status = $("#qcStatus");

    const setError = (input, msg) => {
      const field = input.closest(".field");
      const err = field ? field.querySelector(".field-error") : null;
      if (err) err.textContent = msg || "";
      if (field) field.classList.toggle("has-error", Boolean(msg));
      input.setAttribute("aria-invalid", msg ? "true" : "false");
    };

    const emailOk = () => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim());

    const validate = (show) => {
      let ok = true;
      if (!org.value) { if (show) setError(org, "회사/기관 유형을 선택해 주세요."); ok = false; }
      else setError(org, "");
      if (!interest.value) { if (show) setError(interest, "관심 분야를 선택해 주세요."); ok = false; }
      else setError(interest, "");
      if (!concern.value.trim()) { if (show) setError(concern, "현재 고민을 간단히 입력해 주세요."); ok = false; }
      else setError(concern, "");
      if (!emailOk()) { if (show) setError(email, "유효한 이메일 주소를 입력해 주세요."); ok = false; }
      else setError(email, "");
      return ok;
    };

    const updateSubmit = () => {
      // 필수 동의 전에는 제출 버튼 비활성 (PRD)
      submit.disabled = !(consent.checked);
    };

    [org, interest, concern, email].forEach((el) => {
      el.addEventListener("input", () => { setError(el, ""); });
      el.addEventListener("blur", () => { if (el.value) validate(true); });
    });
    consent.addEventListener("change", updateSubmit);
    updateSubmit();

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validate(true)) {
        status.textContent = "필수 항목을 확인해 주세요.";
        status.className = "form-status is-error";
        const bad = form.querySelector(".has-error input, .has-error select, .has-error textarea");
        if (bad) bad.focus();
        return;
      }
      if (!consent.checked) return;
      // 백엔드 미연동: 실제 전송하지 않고 연동 예정 상태를 명확히 표시
      submit.disabled = true;
      status.textContent =
        "입력을 확인했습니다. 현재 상담 접수 백엔드 연동 전이라 실제로 전송·저장되지 않습니다. (POST /api/requests 연동 예정)";
      status.className = "form-status is-ok";
    });
  }
})();
