/* AX Ground — workflow.js
   Hero의 AI Workflow Preview를 렌더링한다.
   - 데스크톱(>1024px): Figma 좌표 기반 절대 배치 + SVG 연결선 (viewBox 1190x560)
   - 태블릿/모바일(<=1024px): DOM 순서를 세로 흐름으로 재배치, CSS 세로 연결선
   노드·연결선이 화면 밖으로 잘리지 않도록 캔버스는 aspect-ratio로 비례 축소된다. */
(() => {
  const canvas = document.getElementById("workflowCanvas");
  if (!canvas) return;

  const NS = "http://www.w3.org/2000/svg";

  /* Figma "Workflow Canvas" 좌표 (1190 x 560 기준) */
  const STAGES = [
    { label: "01 INPUT", x: 34 },
    { label: "02 AI PROCESS", x: 300 },
    { label: "03 AUTOMATION", x: 690 },
    { label: "04 OUTCOME", x: 1015 },
  ];

  /* 노드: n8n 스타일 카드(아이콘+라벨+포트). 좌표는 Figma 기준, 높이는 아이콘을 위해 확장 */
  const NODES = [
    { id: "in1", icon: "💬", label: "고객 문의", x: 36, y: 86, w: 118, h: 74, stage: 0, out: true },
    { id: "in2", icon: "📝", label: "회의 기록", x: 36, y: 180, w: 118, h: 74, stage: 0, out: true },
    { id: "in3", icon: "📄", label: "사내 문서", x: 36, y: 274, w: 118, h: 74, stage: 0, out: true },
    { id: "in4", icon: "📊", label: "업무 데이터", x: 36, y: 368, w: 118, h: 74, stage: 0, out: true },
    { id: "ai1", icon: "📥", label: "AI 수집 · 정리", x: 240, y: 216, w: 126, h: 76, stage: 1, in: true, out: true },
    { id: "ai2", icon: "🧠", label: "AI 분류", x: 410, y: 216, w: 112, h: 76, stage: 1, in: true, out: true },
    { id: "ai3", icon: "📌", label: "핵심 요약", x: 560, y: 148, w: 112, h: 76, stage: 1, in: true, out: true },
    { id: "ai4", icon: "🎯", label: "우선순위 판단", x: 560, y: 288, w: 120, h: 76, stage: 1, in: true, out: true },
    { id: "auto1", icon: "👤", label: "담당자 배정", x: 730, y: 72, w: 124, h: 74, stage: 2, in: true, out: true },
    { id: "auto2", icon: "📧", label: "이메일 · Slack 알림", x: 730, y: 168, w: 134, h: 74, stage: 2, in: true, out: true },
    { id: "auto3", icon: "📑", label: "보고서 생성", x: 730, y: 264, w: 124, h: 74, stage: 2, in: true, out: true },
    { id: "auto4", icon: "📅", label: "Task · 일정 등록", x: 730, y: 360, w: 134, h: 74, stage: 2, in: true, out: true },
    { id: "out1", icon: "🎓", label: "교육 방향 추천", x: 1000, y: 156, w: 140, h: 76, stage: 3, in: true },
    { id: "out2", icon: "🗺️", label: "AX 전환 로드맵", x: 1000, y: 292, w: 140, h: 76, stage: 3, in: true },
  ];

  /* 노드 합류/분기 지점 (n8n의 머지·분기 포트에 해당) */
  const JUNCTIONS = [
    { id: "jA", x: 700, y: 262, stage: 2 },  // AI → 자동화 분기 허브
    { id: "jB", x: 936, y: 270, stage: 3 },  // 자동화 → 결과 합류 허브
  ];

  /* 노드 포트 좌표: in=왼쪽 중앙, out=오른쪽 중앙 */
  const nodeById = Object.fromEntries(NODES.map((n) => [n.id, n]));
  const port = (id, side) => {
    const n = nodeById[id];
    return { x: side === "out" ? n.x + n.w : n.x, y: n.y + n.h / 2 };
  };
  const J = Object.fromEntries(JUNCTIONS.map((j) => [j.id, j]));

  /* n8n식 베지어 연결: 소스 out 포트 → 대상 in 포트(또는 정크션) */
  const LINKS = [
    ["in1", "ai1"], ["in2", "ai1"], ["in3", "ai1"], ["in4", "ai1"],
    ["ai1", "ai2"],
    ["ai2", "ai3"], ["ai2", "ai4"],
    ["ai3", "jA"], ["ai4", "jA"],
    ["jA", "auto1"], ["jA", "auto2"], ["jA", "auto3"], ["jA", "auto4"],
    ["auto1", "jB"], ["auto2", "jB"], ["auto3", "jB"], ["auto4", "jB"],
    ["jB", "out1"], ["jB", "out2"],
  ];

  const endPoint = (ref, side) => (J[ref] ? { x: J[ref].x, y: J[ref].y } : port(ref, side));
  const curve = (a, b) => {
    const dx = Math.min(90, Math.max(26, Math.abs(b.x - a.x) * 0.5));
    return "M" + a.x + " " + a.y + " C" + (a.x + dx) + " " + a.y + " " + (b.x - dx) + " " + b.y + " " + b.x + " " + b.y;
  };
  const EDGES = LINKS.map(([from, to]) => curve(endPoint(from, "out"), endPoint(to, "in")));

  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "wf-links");
  svg.setAttribute("viewBox", "0 0 1190 560");
  svg.setAttribute("preserveAspectRatio", "none");
  svg.setAttribute("aria-hidden", "true");

  EDGES.forEach((d) => {
    const path = document.createElementNS(NS, "path");
    path.setAttribute("d", d);
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "var(--colors-body-muted)");
    path.setAttribute("stroke-opacity", "0.65");
    path.setAttribute("stroke-width", "2");
    path.setAttribute("vector-effect", "non-scaling-stroke");
    path.setAttribute("pathLength", "1"); // CSS에서 dasharray:1로 드로잉 길이를 정규화
    svg.appendChild(path);
  });

  canvas.appendChild(svg);

  STAGES.forEach((s) => {
    const el = document.createElement("span");
    el.className = "wf-stage-label";
    el.textContent = s.label;
    el.style.left = (s.x / 1190) * 100 + "%";
    canvas.appendChild(el);
  });

  NODES.forEach((n) => {
    const el = document.createElement("div");
    el.className = "wf-node";
    el.dataset.stage = String(n.stage);
    el.style.left = (n.x / 1190) * 100 + "%";
    el.style.top = (n.y / 560) * 100 + "%";
    el.style.width = (n.w / 1190) * 100 + "%";
    el.style.height = (n.h / 560) * 100 + "%";
    if (n.in) {
      const p = document.createElement("i");
      p.className = "wf-port wf-port--in";
      el.appendChild(p);
    }
    const icon = document.createElement("span");
    icon.className = "wf-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = n.icon;
    const label = document.createElement("span");
    label.className = "wf-label";
    label.textContent = n.label;
    el.append(icon, label);
    if (n.out) {
      const p = document.createElement("i");
      p.className = "wf-port wf-port--out";
      el.appendChild(p);
    }
    canvas.appendChild(el);
  });

  JUNCTIONS.forEach((j) => {
    const el = document.createElement("i");
    el.className = "wf-junction";
    el.dataset.stage = String(j.stage);
    el.style.left = (j.x / 1190) * 100 + "%";
    el.style.top = (j.y / 560) * 100 + "%";
    canvas.appendChild(el);
  });

  const note = document.createElement("p");
  note.className = "wf-note";
  note.textContent = "※ 실제 고객사 프로세스가 아닌 AX Ground 서비스 방향을 설명하기 위한 예시 워크플로우";
  canvas.appendChild(note);

  /* ---------- 스크롤 순차 생성 모션 ----------
     Figma [SCROLL INTERACTION] 주석 구현: 노드 → 연결선 → 결과가
     스테이지 순서대로 나타난다. 지연값은 --wf-d로 각 요소에 부여한다.
     순서: 라벨 → 입력 노드+선 → AI 노드+선 → 자동화 노드+선 → 결과 선+노드 → 노트 */
  const edges = [...svg.querySelectorAll("path")];
  const NODE_DELAY = [160, 300, 440, 580, 980, 1500, 2000, 2120, 2900, 3020, 3140, 3260, 4480, 4600];
  const EDGE_DELAY = [720, 800, 880, 960, 1380, 1880, 1960, 2400, 2480, 3300, 3380, 3460, 3540, 3900, 3980, 4060, 4140, 4880, 4960];
  const JUNCTION_DELAY = [2700, 4240];

  const stageLabelEls = [...canvas.querySelectorAll(".wf-stage-label")];
  const nodeList = [...canvas.querySelectorAll(".wf-node")];
  const junctionEls = [...canvas.querySelectorAll(".wf-junction")];

  stageLabelEls.forEach((el, i) => el.style.setProperty("--wf-d", (i * 90) + "ms"));
  nodeList.forEach((el, i) => el.style.setProperty("--wf-d", NODE_DELAY[i] + "ms"));
  edges.forEach((p, i) => p.style.setProperty("--wf-d", EDGE_DELAY[i] + "ms"));
  junctionEls.forEach((el, i) => el.style.setProperty("--wf-d", JUNCTION_DELAY[i] + "ms"));
  note.style.setProperty("--wf-d", "5300ms");

  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduced && "IntersectionObserver" in window) {
    canvas.classList.add("wf-live");
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          canvas.classList.add("wf-on");
          io.disconnect();
        }
      });
    }, { threshold: 0.35 });
    io.observe(canvas);
  }

  /* ---------- 반응형: 세로 흐름 전환 ---------- */
  const mq = window.matchMedia("(max-width: 1024px)");
  const stageLabels = [...canvas.querySelectorAll(".wf-stage-label")];
  const nodeEls = [...canvas.querySelectorAll(".wf-node")];

  const setVertical = (vertical) => {
    canvas.classList.toggle("wf-vertical", vertical);
    if (vertical) {
      // 스테이지 라벨 다음에 해당 노드들을 순서대로 배치
      stageLabels.forEach((label, i) => {
        canvas.appendChild(label);
        nodeEls.filter((n) => n.dataset.stage === String(i)).forEach((n) => canvas.appendChild(n));
      });
      canvas.appendChild(note);
    } else {
      // SVG → 라벨 → 노드 → 노트 순으로 원복
      canvas.appendChild(svg);
      stageLabels.forEach((l) => canvas.appendChild(l));
      nodeEls.forEach((n) => canvas.appendChild(n));
      canvas.appendChild(note);
    }
  };

  setVertical(mq.matches);
  mq.addEventListener("change", (e) => setVertical(e.matches));
})();
