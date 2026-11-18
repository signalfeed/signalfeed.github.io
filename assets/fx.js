// SignalFeed motion layer: a perspective "signal field" that bends with time, pointer and scroll,
// SVG ribbons that warp as you scroll, and reveal-on-scroll. Honors prefers-reduced-motion.
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let scrollY = window.scrollY;
  addEventListener("scroll", () => { scrollY = window.scrollY; }, { passive: true });

  // ---- Signal field ----
  const canvas = document.getElementById("field");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    let w = 0, h = 0, dpr = 1, px = 0.5, py = 0.5, running = true, t0 = performance.now();
    const ROWS = 46, COLS = 120;
    const stars = Array.from({ length: 220 }, () => ({ x: Math.random(), y: Math.random(), r: Math.random() * 1.1 + 0.2, d: Math.random() * 0.8 + 0.2, p: Math.random() * 6.28 }));
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 2);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    size(); addEventListener("resize", size);
    addEventListener("pointermove", e => { px = e.clientX / innerWidth; py = e.clientY / innerHeight; }, { passive: true });
    const height = (x, z, t, s) =>
      Math.sin(x * 2.1 + t * 0.55 + z * 0.9) * 0.42 +
      Math.sin(x * 4.3 - t * 0.35 + z * 2.2) * 0.18 +
      Math.cos(z * 3.1 + t * 0.4 + s * 3.0) * 0.30 +
      Math.exp(-((x - (px - 0.5) * 3) ** 2 + (z - 1.2) ** 2) * 1.6) * (0.9 - py * 0.6);
    const draw = now => {
      const t = reduce ? 4 : (now - t0) / 1000;
      const s = Math.min(scrollY / Math.max(h, 1), 1.5);
      ctx.clearRect(0, 0, w, h);
      for (const st of stars) {                                   // deep-space parallax
        const sx = ((st.x + t * 0.004 * st.d) % 1) * w, sy = (st.y * h - scrollY * 0.15 * st.d + h) % h;
        ctx.globalAlpha = (0.25 + 0.55 * st.d) * (0.6 + 0.4 * Math.sin(t * 1.3 + st.p));
        ctx.fillStyle = st.d > 0.75 ? "#cfe0ff" : "#8fb0ff";
        ctx.beginPath(); ctx.arc(sx, sy, st.r, 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = 1;
      const horizon = h * (0.18 - s * 0.10), fov = Math.min(w, 1500) * 0.95;
      for (let r = ROWS - 1; r >= 0; r--) {
        const z = 0.35 + (r / ROWS) * 3.2;                       // depth
        const depth = 1 - r / ROWS;
        ctx.beginPath();
        for (let c = 0; c <= COLS; c++) {
          const x = (c / COLS - 0.5) * 6;
          const y = height(x, z, t, s) * (1 + s * 1.6);          // the field bends harder as you scroll
          const sx = w * 0.62 + (x * fov) / (z + 1.2);
          const sy = horizon + ((1.6 - y * 0.55) * fov * 0.32) / (z + 0.4);
          c ? ctx.lineTo(sx, sy) : ctx.moveTo(sx, sy);
        }
        const g = ctx.createLinearGradient(0, 0, w, 0);
        const a = 0.16 + depth * 0.7;
        g.addColorStop(0, `rgba(143,176,255,0)`);
        g.addColorStop(0.25, `rgba(143,176,255,${a})`);
        g.addColorStop(0.7, `rgba(111,240,210,${a * 0.9})`);
        g.addColorStop(1, `rgba(111,240,210,0)`);
        ctx.strokeStyle = g; ctx.lineWidth = 0.7 + depth * 1.3; ctx.stroke();
      }
      if (!reduce && running) requestAnimationFrame(draw);
    };
    new IntersectionObserver(([e]) => {
      const was = running; running = e.isIntersecting;
      if (running && !was && !reduce) requestAnimationFrame(draw);
    }).observe(canvas);
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) running = false; else if (!reduce) { running = true; requestAnimationFrame(draw); }
    });
    requestAnimationFrame(draw);
  }

  // ---- Scroll-driven background stage ----
  // Tones chosen so every text color on the site keeps WCAG AA contrast at every point of the blend.
  const STOPS = [
    { bg: [5, 7, 13],   glow: [37, 65, 178, .24],  glow2: [20, 150, 130, .10] },  // midnight blue
    { bg: [9, 6, 22],   glow: [96, 58, 196, .22],  glow2: [37, 65, 178, .12] },   // deep violet
    { bg: [3, 14, 17],  glow: [18, 140, 122, .20], glow2: [96, 58, 196, .10] },   // abyssal teal
    { bg: [7, 8, 24],   glow: [90, 120, 230, .22], glow2: [18, 140, 122, .10] },  // indigo
  ];
  const stage = document.createElement("div"); stage.className = "bg-stage"; stage.setAttribute("aria-hidden", "true");
  document.body.prepend(stage);
  const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
  const rgba = c => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${c.length > 3 ? c[3].toFixed(3) : 1})`;
  let stageQueued = false;
  const paintStage = () => {
    stageQueued = false;
    const max = Math.max(document.documentElement.scrollHeight - innerHeight, 1);
    const p = Math.min(Math.max(scrollY / max, 0), 1) * (STOPS.length - 1);
    const i = Math.min(Math.floor(p), STOPS.length - 2), k = p - i;
    const e = k * k * (3 - 2 * k);                                   // smoothstep between tones
    const A = STOPS[i], B = STOPS[i + 1];
    const st = stage.style;
    st.setProperty("--stage", rgba(mix(A.bg, B.bg, e)));
    st.setProperty("--glow", rgba(mix(A.glow, B.glow, e)));
    st.setProperty("--glow2", rgba(mix(A.glow2, B.glow2, e)));
    st.setProperty("--gx", (18 + 64 * (p / (STOPS.length - 1))).toFixed(1) + "%");
    st.setProperty("--gy", (15 + 50 * Math.abs(Math.sin(p * 1.3))).toFixed(1) + "%");
  };
  addEventListener("scroll", () => { if (!stageQueued) { stageQueued = true; requestAnimationFrame(paintStage); } }, { passive: true });
  addEventListener("resize", paintStage); paintStage();

  // ---- Scrollytelling: laptop opens, tags appear, checks verify ----
  const story = document.querySelector(".story");
  if (story) {
    const caps = [...story.querySelectorAll(".captions li")];
    const clamp01 = v => Math.min(Math.max(v, 0), 1);
    const run = () => {
      let p = 1;
      if (!reduce) { const r = story.getBoundingClientRect(); p = clamp01(-r.top / Math.max(r.height - innerHeight, 1)); }
      const lid = clamp01(p / 0.3), tags = clamp01((p - 0.3) / 0.35), verify = clamp01((p - 0.62) / 0.3);
      story.style.setProperty("--lid", lid.toFixed(3));
      story.style.setProperty("--tags", tags.toFixed(3));
      story.style.setProperty("--verify", verify.toFixed(3));
      const step = p < 0.3 ? 0 : p < 0.62 ? 1 : 2;
      caps.forEach((c, i) => c.classList.toggle("on", reduce ? true : i === step));
    };
    addEventListener("scroll", () => requestAnimationFrame(run), { passive: true }); addEventListener("resize", run); run();
  }

  // ---- Hero video: pause control (WCAG 2.2.2), reduced motion, scroll push-in ----
  const vid = document.getElementById("heroVideo"), tog = document.getElementById("vidToggle"), hero = vid ? vid.closest(".hero-x, .article-head") : null;
  if (vid && tog) {
    const setState = paused => { tog.setAttribute("aria-label", paused ? "Play background video" : "Pause background video"); tog.classList.toggle("paused", paused); };
    if (reduce) { vid.removeAttribute("autoplay"); vid.pause(); setState(true); }
    tog.addEventListener("click", () => { if (vid.paused) { vid.play(); setState(false); } else { vid.pause(); setState(true); } });
    const push = () => { const r = hero.getBoundingClientRect(); hero.style.setProperty("--hs", Math.min(Math.max(-r.top / r.height, 0), 1).toFixed(3)); };
    if (!reduce) { addEventListener("scroll", () => requestAnimationFrame(push), { passive: true }); push(); }
  }

  // ---- Live UTC readout (real time, not decoration) ----
  const utc = document.getElementById("utc");
  if (utc) { const tick = () => { utc.textContent = "UTC " + new Date().toISOString().slice(11, 19); }; tick(); setInterval(tick, 1000); }

  // ---- Ribbons that bend with scroll ----
  const ribbons = [...document.querySelectorAll(".ribbon path")];
  const bend = () => {
    for (const [i, p] of ribbons.entries()) {
      const box = p.ownerSVGElement.getBoundingClientRect();
      const k = reduce ? 0 : (box.top + box.height / 2 - innerHeight / 2) / innerHeight;  // -1..1 across the viewport
      const amp = 70 * k * (i % 2 ? -1 : 1), off = i * 14;
      p.setAttribute("d", `M0 ${100 + off} C 300 ${100 + off + amp} 500 ${100 + off - amp * 1.4} 800 ${100 + off} S 1300 ${100 + off + amp} 1600 ${100 + off}`);
    }
    if (!reduce) requestAnimationFrame(bend);
  };
  if (ribbons.length) bend();

  // ---- Reveal on scroll (position check; content stays visible if this script never runs) ----
  const pending = new Set(document.querySelectorAll(".reveal"));
  const reveal = () => {
    for (const el of pending) {
      const r = el.getBoundingClientRect();
      if (r.top < innerHeight * 0.92 && r.bottom > 0) { el.classList.add("in"); pending.delete(el); }
    }
  };
  document.documentElement.classList.add("fx");
  addEventListener("scroll", reveal, { passive: true }); addEventListener("resize", reveal);
  reveal(); setTimeout(reveal, 300);
})();
