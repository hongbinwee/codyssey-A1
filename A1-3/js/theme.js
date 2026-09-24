/* AX Ground — theme.js
   다크 모드: 첫 방문은 prefers-color-scheme, 이후 localStorage("axg-theme") 유지.
   <head>의 인라인 스크립트가 초기 테마를 먼저 적용하고, 이 파일이 토글을 담당한다. */
(() => {
  const STORAGE_KEY = "axg-theme";
  const html = document.documentElement;

  const current = () => (html.dataset.theme === "dark" ? "dark" : "light");

  const applyTheme = (theme, persist) => {
    html.dataset.theme = theme;
    if (persist) {
      try { window.localStorage.setItem(STORAGE_KEY, theme); } catch (_) { /* 저장 실패 무시 */ }
    }
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.setAttribute("aria-label", theme === "dark" ? "라이트 모드로 전환" : "다크 모드로 전환");
      btn.setAttribute("aria-pressed", String(theme === "dark"));
    });
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", theme === "dark" ? "#161617" : "#ffffff");
  };

  const init = () => {
    document.querySelectorAll(".theme-toggle").forEach((btn) => {
      btn.addEventListener("click", () => {
        applyTheme(current() === "dark" ? "light" : "dark", true);
      });
    });
    // aria 상태를 실제 테마와 동기화
    applyTheme(current(), false);
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
