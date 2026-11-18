// Render 1200x630 share cards: a real frame of the hero press footage + brand + page title. Run: node og_cards.mjs
import fs from "node:fs";
import puppeteer from "/Users/aaron/Library/Application Support/Claude/scratch-workspaces/4b4926b4-c1d7-4113-86c2-3aa98b44a83c/737bc7b7-ca9f-4ea3-a9e9-839dc5802c65/scratch-2026-10-29-9fe393/tools/a11y-audit/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js";
const pages = JSON.parse(fs.readFileSync("og_pages.json", "utf8"));
const b = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true, args: ["--autoplay-policy=no-user-gesture-required"] });
const p = await b.newPage(); await p.setViewport({ width: 1200, height: 630 });
for (const pg of pages) {
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700&family=JetBrains+Mono:wght@500&display=swap');
  *{margin:0;box-sizing:border-box} body{width:1200px;height:630px;overflow:hidden;background:#05070d;font-family:Inter,system-ui,sans-serif;color:#f2f5fb;position:relative}
  video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(.7) contrast(1.15) brightness(.8)}
  .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,7,13,.95) 0%,rgba(5,7,13,.82) 45%,rgba(5,7,13,.25) 80%,rgba(5,7,13,.1) 100%),linear-gradient(180deg,transparent 60%,rgba(5,7,13,.8))}
  .c{position:absolute;inset:0;padding:64px 70px;display:flex;flex-direction:column}
  .brand{display:flex;align-items:center;gap:14px;font-weight:600;font-size:28px}
  .brand svg{width:44px;height:44px}
  .eb{margin-top:auto;font:500 18px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#6ff0d2}
  h1{font-size:${pg.size || 64}px;line-height:1.04;letter-spacing:-.03em;font-weight:700;margin:16px 0 18px;max-width:760px}
  h1 span{background:linear-gradient(90deg,#fff,#8fb0ff 60%,#6ff0d2);-webkit-background-clip:text;color:transparent}
  .sub{font-size:24px;color:#c3cbdb;max-width:720px}
  .hud{position:absolute;inset:26px;border:1px solid transparent}
  .hud:before,.hud:after{content:"";position:absolute;width:26px;height:26px;border:2px solid rgba(143,176,255,.7)}
  .hud:before{top:0;left:0;border-right:0;border-bottom:0}.hud:after{bottom:0;right:0;border-left:0;border-top:0}
  .url{position:absolute;right:70px;top:72px;font:500 16px 'JetBrains Mono',monospace;color:#949fb5;letter-spacing:.06em}
  </style></head><body>
  <video id="v" src="https://videos.pexels.com/video-files/29906414/12837347_1280_720_24fps.mp4" muted playsinline preload="auto"></video>
  <div class="shade"></div><div class="hud"></div>
  <div class="c"><div class="brand"><svg viewBox="0 0 32 32"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8fb0ff"/><stop offset="1" stop-color="#6ff0d2"/></linearGradient></defs><rect x="1" y="1" width="30" height="30" rx="9" fill="none" stroke="url(#g)" stroke-width="2"/><path d="M7 20c3-6 5-6 8 0s5 6 10-8" fill="none" stroke="url(#g)" stroke-width="2.4" stroke-linecap="round"/></svg>SignalFeed</div>
  <div class="eb">${pg.eyebrow}</div><h1>${pg.title}</h1><div class="sub">${pg.sub}</div></div>
  </body></html>`;
  await p.setContent(html, { waitUntil: "domcontentloaded", timeout: 60000 }); await new Promise(r => setTimeout(r, 1500));
  await p.evaluate(async t => { const v = document.getElementById("v"); await new Promise(r => { if (v.readyState >= 2) r(); else v.addEventListener("loadeddata", r, { once: true }); }); v.currentTime = t; await new Promise(r => v.addEventListener("seeked", r, { once: true })); await document.fonts.ready; }, pg.t || 6);
  await p.screenshot({ path: `assets/og/${pg.slug}.jpg`, type: "jpeg", quality: 86 });
  console.log("card", pg.slug);
}
await b.close();
