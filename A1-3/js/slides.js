/* AX Ground — slides.js
   서비스 미리보기 5개 슬라이드 캐러셀.

   규칙:
   - 5개 슬라이드는 초기 로드 시 모두 DOM에 마운트된다. 전환 시 DOM을 만들거나 제거하지 않는다.
   - 활성: opacity 1 / z-index 10 / pointer-events auto
   - 비활성: opacity 0 / z-index 0 / pointer-events none (+ inert, aria-hidden)
   - 전환은 opacity만, 0.35s ease-in-out (CSS .slide / .slide.is-active)
   - 비디오는 최초 초기화 때 한 번만 연결한다. 슬라이드 변경 시 HLS 인스턴스를 재생성하지 않는다.
   - Safari 네이티브 HLS(canPlayType) 우선, 미지원 브라우저는 hls.js 사용.
   - 비활성 비디오는 로드 상태를 유지하되 재생은 활성 슬라이드만 한다.
   - 자동 넘김 없음 (Figma 근거 없음): 이전/다음 버튼과 인디케이터만 제공.
   - prefers-reduced-motion: 전환 최소화 (CSS에서 처리)

   영상 자산:
   - Mux Playback URL이 아직 제공되지 않아 videoUrl은 null이다.
     URL이 준비되면 각 항목의 videoUrl에 "https://stream.mux.com/{PLAYBACK_ID}.m3u8" 형식으로 넣는다.
     URL이 없는 슬라이드는 .slide-fallback 프리뷰를 표시한다. */

const SLIDES = [
  {
    id: "slide-education",
    title: "맞춤형 AI 교육",
    caption: "직무와 수준에 맞춘 실습 중심 교육",
    desc: "조직의 목표와 업무 맥락에 맞춰 설계하는 AI 교육 장면",
    videoUrl: null, // TODO: Mux Playback URL 제공 시 연결
    poster: null,
  },
  {
    id: "slide-diagnosis",
    title: "업무 진단 · AX 로드맵",
    caption: "현재 업무를 진단하고 실행 우선순위를 제안",
    desc: "반복 업무와 병목을 찾아 AX 실행 순서를 정리하는 장면",
    videoUrl: null,
    poster: null,
  },
  {
    id: "slide-automation",
    title: "업무 자동화 흐름",
    caption: "수집부터 분류, 알림, 보고서까지 이어지는 흐름",
    desc: "AI가 업무를 분류하고 자동화로 연결하는 흐름 예시",
    videoUrl: null,
    poster: null,
  },
  {
    id: "slide-mvp",
    title: "AI 도구 · MVP 제작",
    caption: "작은 도구로 먼저 검증하고 확장",
    desc: "실제 문제를 AI 도구와 MVP로 빠르게 검증하는 장면",
    videoUrl: null,
    poster: null,
  },
  {
    id: "slide-ax",
    title: "AX 실행 방향",
    caption: "교육과 자동화를 AX 로드맵으로 연결",
    desc: "검증 결과를 단계별 AX 실행 방향으로 확장하는 장면",
    videoUrl: null,
    poster: null,
  },
];

(() => {
  const stage = document.getElementById("slideStage");
  const dotsWrap = document.getElementById("slideDots");
  const prevBtn = document.getElementById("slidePrev");
  const nextBtn = document.getElementById("slideNext");
  const countEl = document.getElementById("slideCount");
  if (!stage || !dotsWrap || !prevBtn || !nextBtn) return;

  const hlsInstances = []; // 슬라이드 전환과 무관하게 유지되는 HLS 인스턴스 목록
  const videos = [];
  let current = 0;

  const supportsNativeHls = (video) =>
    typeof video.canPlayType === "function" &&
    video.canPlayType("application/vnd.apple.mpegurl") !== "";

  /* hls.js는 네이티브 HLS 미지원 + videoUrl이 실제로 있을 때만 동적 로드한다.
     (영상 URL 미제공 상태에서는 CDN 요청 자체가 발생하지 않음) */
  const HLS_SRC = "https://cdn.jsdelivr.net/npm/hls.js@1.5.20/dist/hls.min.js";
  let hlsLoading = null;
  const loadHlsJs = () => {
    if (window.Hls) return Promise.resolve();
    if (!hlsLoading) {
      hlsLoading = new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = HLS_SRC;
        s.onload = resolve;
        s.onerror = () => { hlsLoading = null; reject(new Error("hls.js load failed")); };
        document.head.appendChild(s);
      });
    }
    return hlsLoading;
  };
  const attachHls = (video, url) => {
    const hls = new window.Hls({ maxBufferLength: 30 });
    hls.loadSource(url);
    hls.attachMedia(video);
    hlsInstances.push(hls);
  };

  /* ---------- 초기 마운트: 5개 슬라이드를 모두 DOM에 생성 ---------- */
  SLIDES.forEach((slide, i) => {
    const el = document.createElement("div");
    el.className = "slide";
    el.id = slide.id;
    el.setAttribute("role", "group");
    el.setAttribute("aria-roledescription", "slide");
    el.setAttribute("aria-label", (i + 1) + " / " + SLIDES.length + ": " + slide.title);

    const video = document.createElement("video");
    video.muted = true;
    video.playsInline = true;
    video.loop = true;
    video.preload = "auto";
    video.setAttribute("aria-hidden", "true");
    video.tabIndex = -1;
    if (slide.poster) video.poster = slide.poster;

    if (slide.videoUrl) {
      if (supportsNativeHls(video)) {
        video.src = slide.videoUrl; // Safari 등 네이티브 HLS
      } else {
        loadHlsJs()
          .then(() => {
            if (window.Hls && window.Hls.isSupported()) attachHls(video, slide.videoUrl);
            else video.dataset.unsupported = "true";
          })
          .catch(() => { video.dataset.unsupported = "true"; });
      }
      el.appendChild(video);
    } else {
      video.hidden = true;
      el.appendChild(video);
      const fallback = document.createElement("div");
      fallback.className = "slide-fallback";
      const no = document.createElement("span");
      no.className = "slide-no";
      no.textContent = "0" + (i + 1);
      const name = document.createElement("span");
      name.className = "slide-name";
      name.textContent = slide.title;
      const desc = document.createElement("span");
      desc.className = "slide-desc";
      desc.textContent = slide.desc;
      fallback.append(no, name, desc);
      el.appendChild(fallback);
    }

    const caption = document.createElement("p");
    caption.className = "slide-caption";
    const strong = document.createElement("strong");
    strong.textContent = slide.title;
    caption.append(strong, document.createTextNode(slide.caption));
    el.appendChild(caption);

    stage.appendChild(el);

    const dot = document.createElement("button");
    dot.className = "slide-dot";
    dot.type = "button";
    dot.setAttribute("role", "tab");
    dot.setAttribute("aria-label", (i + 1) + "번 슬라이드: " + slide.title);
    dot.addEventListener("click", () => goTo(i));
    dotsWrap.appendChild(dot);

    videos.push(video);
  });

  const slideEls = [...stage.querySelectorAll(".slide")];
  const dotEls = [...dotsWrap.querySelectorAll(".slide-dot")];

  /* ---------- 전환: 클래스/ARIA만 변경, DOM과 비디오 인스턴스는 유지 ---------- */
  const apply = (index) => {
    slideEls.forEach((el, i) => {
      const active = i === index;
      el.classList.toggle("is-active", active);
      el.setAttribute("aria-hidden", String(!active));
      if (active) el.removeAttribute("inert");
      else el.setAttribute("inert", "");
    });
    dotEls.forEach((d, i) => {
      d.setAttribute("aria-current", String(i === index));
      d.setAttribute("aria-selected", String(i === index));
    });
    if (countEl) countEl.textContent = (index + 1) + " / " + SLIDES.length;

    // 활성 슬라이드만 재생, 나머지는 로드 상태 유지하며 일시정지
    videos.forEach((v, i) => {
      if (!SLIDES[i].videoUrl || v.dataset.unsupported) return;
      if (i === index) {
        const p = v.play();
        if (p && p.catch) p.catch(() => {});
      } else {
        v.pause();
      }
    });
  };

  const goTo = (index) => {
    current = (index + SLIDES.length) % SLIDES.length;
    apply(current);
  };

  prevBtn.addEventListener("click", () => goTo(current - 1));
  nextBtn.addEventListener("click", () => goTo(current + 1));

  stage.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") { e.preventDefault(); goTo(current - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); goTo(current + 1); }
  });

  apply(0);
})();
