#!/usr/bin/env python3
"""رفيق سيدي بوسعيد — version Pop-up 3D.

Architecture « 3D optionnel » : la page fonctionne d'abord en couches CSS 3D, sans
WebGL et sans CDN. Three.js (r128, cdnjs) est chargé dynamiquement et n'ajoute qu'une
profondeur volumétrique ; s'il échoue, la scène reste complète — jamais de page noire.

Lancement :
    python prototype/build_3d.py
    # puis ouvrir refek-sidi-bou-said-3d.html
"""
from __future__ import annotations

import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
LANGS = ("ar", "fr", "en")
LANG_LABELS = {"ar": "العربية", "fr": "Français", "en": "English"}


def load_json(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def collect() -> dict:
    return {
        "i18n": {lang: load_json(f"i18n/{lang}.json") for lang in LANGS},
        "knowledge": load_json("data/knowledge.json"),
        "events": load_json("data/events.json"),
        "scenes": load_json("data/scenes.json"),
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rafik Sidi Bou Said — pop-up 3D</title>
<style>
  :root {
    --navy:#0A1628; --blue-deep:#123A5C; --blue:#2E7BB5; --gold:#D4A017;
    --gold-soft:#F6EEDA; --teal:#00B4D8; --paper:#FAF7F0; --muted:#8FA3B5;
  }
  * { box-sizing:border-box; }
  html, body { margin:0; height:100%; background:var(--navy); color:#EAF2F9;
               font-family:system-ui,-apple-system,"Segoe UI",sans-serif; overflow:hidden; }
  html[dir="rtl"] body { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }

  .stage { position:relative; height:100%; width:100%; perspective:1400px; overflow:hidden; }
  #gl { position:absolute; inset:0; z-index:1; opacity:0; transition:opacity 1.2s ease; }
  #gl.on { opacity:1; }

  /* ---- décor en couches CSS : fonctionne sans WebGL ---- */
  .layers { position:absolute; inset:0; z-index:2; transform-style:preserve-3d;
            transition:transform .35s cubic-bezier(.2,.7,.3,1), opacity .9s ease; }
  /* Le décor CSS et la scène WebGL occupent le même espace : quand la 3D rend
     vraiment, on efface le décor de repli, sinon il masquerait le canvas. */
  .stage.gl .layers { opacity:0; pointer-events:none; }
  .stage.gl .card { backdrop-filter:blur(2px); box-shadow:0 26px 70px rgba(0,0,0,.62); }
  .layer { position:absolute; inset:0; }
  .sky   { background:linear-gradient(#0A1628 0%, #13314C 45%, #2E7BB5 100%); }
  .sun   { position:absolute; top:12%; inset-inline-start:16%; width:120px; height:120px; border-radius:50%;
           background:radial-gradient(circle, rgba(212,160,23,.85), rgba(212,160,23,0) 70%); }
  .sea   { position:absolute; bottom:0; height:42%; width:100%;
           background:linear-gradient(#1E5E8C, #0E3350); }
  .sea::after { content:""; position:absolute; inset:0; opacity:.35;
           background:repeating-linear-gradient(transparent 0 12px, rgba(255,255,255,.10) 12px 13px); }
  .cliff { position:absolute; bottom:0; height:46%; width:100%; }

  .hint { position:absolute; inset-inline:0; bottom:14px; text-align:center; font-size:11.5px;
          color:var(--muted); z-index:6; }

  /* ---- livre pop-up ---- */
  .book { position:absolute; inset:0; z-index:4; display:flex; align-items:center; justify-content:center;
          transform-style:preserve-3d; }
  .pop { position:relative; width:min(92vw,860px); transform-style:preserve-3d; }
  .card { position:absolute; inset-inline-start:50%; top:50%; width:min(78vw,420px);
          transform:translate(-50%,-50%) translateZ(60px) rotateX(72deg); opacity:0;
          background:var(--paper); color:#1F2A33; border-radius:20px; padding:20px 22px;
          border:1px solid rgba(212,160,23,.6); box-shadow:0 26px 60px rgba(0,0,0,.5);
          transform-origin:50% 100%; transition:transform .7s cubic-bezier(.2,.9,.25,1), opacity .5s ease;
          pointer-events:none; }
  .card.up { transform:translate(-50%,-50%) translateZ(120px) rotateX(0deg); opacity:1; pointer-events:auto; }
  .card h2 { margin:0 40px 4px 0; font-size:19px; color:var(--blue-deep); }
  html[dir="rtl"] .card h2 { margin:0 0 4px 40px; }
  .card .close { position:absolute; top:12px; inset-inline-end:12px; width:30px; height:30px;
                 border-radius:50%; border:1px solid #D9D2C2; background:#fff; color:#5A6570;
                 font-size:15px; line-height:1; cursor:pointer; }
  .card .close:hover { background:#F1EDE3; }
  .reopen { position:absolute; top:112px; inset-inline-start:20px; z-index:7; display:none; }
  .reopen.show { display:inline-block; }
  .drop { position:absolute; inset:0; z-index:9; display:none; align-items:center; justify-content:center;
          background:rgba(10,22,40,.78); border:3px dashed var(--gold); font-size:15px; text-align:center;
          padding:40px; }
  .drop.on { display:flex; }
  .toast { position:absolute; bottom:96px; inset-inline:0; text-align:center; z-index:8; }
  .toast span { background:rgba(10,22,40,.9); border:1px solid var(--gold); color:#F6EEDA;
                padding:8px 16px; border-radius:16px; font-size:11.5px; }
  .card p  { margin:8px 0 0; font-size:13.5px; line-height:1.6; color:#33424F; }
  .badge { display:inline-block; margin-top:12px; font-size:10.5px; padding:5px 11px; border-radius:12px; }
  .badge.ok   { background:#E7F1F8; color:#1B5C86; border:1px solid var(--blue); }
  .badge.warn { background:#FFF3D6; color:#8A6A12; border:1px solid var(--gold); }
  .src { display:block; margin-top:8px; font-size:10.5px; color:#6B7885; }

  /* ---- silhouettes pop-up (SVG originaux, dessinés inline) ---- */
  .prop { position:absolute; bottom:0; inset-inline-start:50%; transform-style:preserve-3d;
          transition:transform .8s cubic-bezier(.2,.9,.25,1), opacity .6s ease; opacity:0; }
  .prop.up { opacity:1; }
  .prop svg { display:block; }

  /* ---- chrome ---- */
  header { position:absolute; top:0; inset-inline:0; z-index:7; padding:16px 20px;
           display:flex; align-items:center; gap:14px;
           background:linear-gradient(rgba(10,22,40,.92), rgba(10,22,40,0)); }
  header h1 { font-size:16px; margin:0; letter-spacing:.4px; }
  header .sub { font-size:10.5px; color:var(--muted); margin-top:2px; }
  .spacer { margin-inline-start:auto; }
  .chip { background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.18); color:#EAF2F9;
          border-radius:14px; padding:6px 11px; font-size:11px; cursor:pointer; }
  .chip[aria-pressed="true"] { background:var(--gold); color:#22303B; border-color:var(--gold); font-weight:600; }
  .unesco { position:absolute; top:64px; inset-inline-start:20px; z-index:7; font-size:10.5px;
            color:var(--gold); background:rgba(10,22,40,.6); padding:5px 12px; border-radius:12px; }

  .rail { position:absolute; bottom:44px; inset-inline:0; z-index:7; display:flex; gap:8px;
          justify-content:center; flex-wrap:wrap; padding:0 16px; }
  .rail button { background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.16);
                 color:#EAF2F9; border-radius:16px; padding:8px 14px; font-size:11.5px; cursor:pointer; }
  .rail button[aria-current="true"] { background:var(--teal); color:#062733; border-color:var(--teal); font-weight:600; }

  .cover { position:absolute; inset:0; z-index:8; display:flex; flex-direction:column;
           align-items:center; justify-content:center; gap:18px; text-align:center;
           background:radial-gradient(circle at 50% 40%, rgba(46,123,181,.35), rgba(10,22,40,.96) 65%);
           transition:opacity .8s ease, transform .8s ease; }
  .cover.gone { opacity:0; transform:scale(1.08); pointer-events:none; }
  .cover h2 { margin:0; font-size:26px; }
  .cover button { background:var(--gold); border:0; color:#22303B; font-weight:600;
                  border-radius:22px; padding:12px 26px; font-size:14px; cursor:pointer; }
  @media (prefers-reduced-motion: reduce) {
    .layers, .card, .prop, .cover { transition:none !important; }
  }
</style>
</head>
<body>
<div class="stage" id="stage">
  <canvas id="gl"></canvas>

  <div class="layers" id="layers">
    <div class="layer sky"><div class="sun"></div></div>
    <div class="layer">
      <svg class="cliff" viewBox="0 0 1200 400" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 400 V250 C160 190 320 140 520 132 C740 123 940 168 1200 140 V400 Z" fill="#12283C"/>
        <path d="M0 400 V290 C200 250 420 226 640 220 C880 213 1040 240 1200 226 V400 Z" fill="#0C1E2E"/>
      </svg>
      <div class="sea"></div>
    </div>
    <div class="layer" id="props"></div>
  </div>

  <div class="book" id="book"><div class="pop" id="pop"></div></div>

  <header>
    <svg width="38" height="38" viewBox="0 0 48 48" role="img" aria-label="guide">
      <circle cx="24" cy="24" r="23" fill="#F6EEDA"/>
      <path d="M12 36 v-12 a12 12 0 0 1 24 0 v12 z" fill="#2E7BB5"/>
      <path d="M19 36 v-9 a5 5 0 0 1 10 0 v9 z" fill="#F6EEDA"/>
      <circle cx="24" cy="12" r="3" fill="#D4A017"/>
    </svg>
    <div>
      <h1 id="t-title"></h1>
      <div class="sub" id="t-sub"></div>
    </div>
    <div class="spacer"></div>
    <button class="chip" id="btnMedia"></button>
    <button class="chip" id="btnAuto" aria-pressed="false"></button>
    <button class="chip" id="btn3d" aria-pressed="false"></button>
    <span id="langs"></span>
  </header>
  <div class="unesco" id="t-unesco"></div>
  <button class="chip reopen" id="reopen"></button>
  <input type="file" id="file" accept="image/*,video/*" hidden>
  <div class="drop" id="drop"><span id="t-drop"></span></div>
  <div class="toast" id="toast"></div>

  <div class="rail" id="rail"></div>
  <div class="hint" id="t-hint"></div>

  <div class="cover" id="cover">
    <h2 id="t-cover"></h2>
    <button id="openBtn"></button>
    <div class="sub" id="t-cover-sub" style="color:#8FA3B5;font-size:11.5px"></div>
  </div>
</div>

<script>
__SCENE3D__
</script>
<script>
const DATA = __DATA__;
let lang = "fr", index = 0, want3d = true, gl = null, auto = null, cardHidden = false;
const t = (k) => DATA.i18n[lang][k] || "\\u00ab" + k + "\\u00bb";
const knowledge = (id) => DATA.knowledge.find(e => e.id === id);

/* ---------- décors : SVG dessinés à la main, un par scène ---------- */
const PROPS = {
  village: `<svg width="520" height="200" viewBox="0 0 520 200">
      <g fill="#F3EFE6" stroke="#123A5C" stroke-width="2">
        <path d="M40 200 v-70 h90 v70z"/><path d="M150 200 v-100 h120 v100z"/>
        <path d="M290 200 v-84 h80 v84z"/><path d="M390 200 v-62 h96 v62z"/>
      </g>
      <g fill="#2E7BB5">
        <rect x="70" y="150" width="24" height="50" rx="12"/><rect x="196" y="132" width="28" height="68" rx="14"/>
        <rect x="316" y="152" width="24" height="48" rx="12"/><rect x="424" y="164" width="24" height="36" rx="12"/>
      </g>
      <g fill="none" stroke="#D4A017" stroke-width="1.6">
        <path d="M150 100 h120"/><path d="M290 116 h80"/><path d="M40 130 h90"/><path d="M390 138 h96"/>
      </g>
    </svg>`,
  doors: `<svg width="360" height="230" viewBox="0 0 360 230">
      <rect x="60" y="20" width="240" height="210" rx="10" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/>
      <path d="M120 230 V110 a60 60 0 0 1 120 0 V230z" fill="#2E7BB5" stroke="#123A5C" stroke-width="2"/>
      <g fill="#D4A017">
        <circle cx="180" cy="96" r="4"/><circle cx="150" cy="120" r="4"/><circle cx="210" cy="120" r="4"/>
        <circle cx="132" cy="156" r="4"/><circle cx="228" cy="156" r="4"/><circle cx="180" cy="140" r="4"/>
        <circle cx="150" cy="188" r="4"/><circle cx="210" cy="188" r="4"/><circle cx="180" cy="172" r="4"/>
      </g>
      <path d="M180 230 V110" stroke="#123A5C" stroke-width="2"/>
    </svg>`,
  shrine: `<svg width="360" height="220" viewBox="0 0 360 220">
      <rect x="70" y="110" width="220" height="110" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/>
      <path d="M90 110 a90 60 0 0 1 180 0z" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/>
      <path d="M180 50 v-16" stroke="#D4A017" stroke-width="3"/><circle cx="180" cy="30" r="6" fill="#D4A017"/>
      <path d="M150 220 v-58 a30 30 0 0 1 60 0 v58z" fill="#2E7BB5"/>
      <g fill="none" stroke="#D4A017" stroke-width="1.4">
        <rect x="96" y="130" width="30" height="30"/><rect x="234" y="130" width="30" height="30"/>
      </g>
    </svg>`,
  palace: `<svg width="440" height="230" viewBox="0 0 440 230">
      <rect x="20" y="150" width="400" height="80" fill="#EDE4CE" stroke="#123A5C" stroke-width="2"/>
      <g fill="none" stroke="#F3EFE6" stroke-width="3">
        <path d="M60 150 V80 a26 26 0 0 1 52 0 V150"/><path d="M150 150 V80 a26 26 0 0 1 52 0 V150"/>
        <path d="M240 150 V80 a26 26 0 0 1 52 0 V150"/><path d="M330 150 V80 a26 26 0 0 1 52 0 V150"/>
      </g>
      <g fill="#D4A017"><rect x="56" y="72" width="60" height="8"/><rect x="146" y="72" width="60" height="8"/>
        <rect x="236" y="72" width="60" height="8"/><rect x="326" y="72" width="60" height="8"/></g>
      <ellipse cx="220" cy="196" rx="54" ry="18" fill="#2E7BB5" stroke="#D4A017" stroke-width="2"/>
      <path d="M220 196 v-26" stroke="#D4A017" stroke-width="4"/>
    </svg>`,
  events: `<svg width="420" height="200" viewBox="0 0 420 200">
      <g fill="none" stroke="#F3EFE6" stroke-width="2">
        <rect x="40" y="60" width="150" height="120" rx="12"/><rect x="230" y="40" width="150" height="140" rx="12"/>
      </g>
      <g stroke="#D4A017" stroke-width="2" fill="none">
        <path d="M62 96 h106"/><path d="M62 122 h80"/><path d="M252 76 h106"/><path d="M252 102 h68"/>
      </g>
      <g fill="#2E7BB5"><circle cx="115" cy="156" r="10"/><circle cx="305" cy="140" r="10"/></g>
    </svg>`
};

const PROP_POS = {
  village: { z: 40,  x: -260, scale: 1.0 },
  doors:   { z: 140, x: -180, scale: .95 },
  shrine:  { z: 100, x: -180, scale: .95 },
  palace:  { z: 120, x: -220, scale: .95 },
  events:  { z: 80,  x: -210, scale: .95 }
};

function renderChrome() {
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("app.title");
  document.getElementById("t-sub").textContent = t("app.subtitle");
  document.getElementById("t-unesco").textContent = t("app.badge_unesco");
  document.getElementById("t-hint").textContent = t("popup.hint");
  document.getElementById("t-cover").textContent = t("popup.title");
  document.getElementById("t-cover-sub").textContent = t("app.tagline");
  document.getElementById("openBtn").textContent = t("popup.open");
  document.getElementById("btnMedia").textContent = t("popup.add_media");
  document.getElementById("reopen").textContent = t("popup.show_card");
  document.getElementById("t-drop").textContent = t("popup.media_hint");
  const ba = document.getElementById("btnAuto");
  ba.textContent = t("popup.autoplay");
  ba.setAttribute("aria-pressed", String(auto !== null));
  const b3 = document.getElementById("btn3d");
  b3.textContent = t("popup.mode3d");
  b3.setAttribute("aria-pressed", String(!!gl && want3d));

  const langs = document.getElementById("langs");
  langs.innerHTML = "";
  for (const code of Object.keys(DATA.langLabels)) {
    const b = document.createElement("button");
    b.className = "chip"; b.textContent = code.toUpperCase();
    b.setAttribute("aria-pressed", code === lang);
    b.style.marginInlineStart = "6px";
    b.onclick = () => { lang = code; renderChrome(); renderScene(); };
    langs.appendChild(b);
  }

  const rail = document.getElementById("rail");
  rail.innerHTML = "";
  DATA.scenes.forEach((s, i) => {
    const b = document.createElement("button");
    b.textContent = t(s.title_key);
    b.setAttribute("aria-current", String(i === index));
    b.onclick = () => { index = i; renderChrome(); renderScene(); };
    rail.appendChild(b);
  });
}

function sceneBody(s) {
  if (s.knowledge_id) {
    const k = knowledge(s.knowledge_id);
    return { text: k.answer[lang], verified: k.verified, source: k.source };
  }
  const lines = DATA.events.map(e => "• " + e.title[lang] + " — " + e.when[lang] + " · " + e.place[lang]);
  return { text: lines.join("\\n"), verified: false, source: "" };
}

function renderScene() {
  const s = DATA.scenes[index];
  const body = sceneBody(s);

  const pop = document.getElementById("pop");
  pop.innerHTML = "";
  const card = document.createElement("div");
  card.className = "card";
  const close = document.createElement("button");
  close.className = "close";
  close.textContent = "\u2715";
  close.title = t("popup.hide_card");
  close.onclick = () => { cardHidden = true; renderScene(); };
  card.appendChild(close);
  const h = document.createElement("h2"); h.textContent = t(s.title_key);
  const p = document.createElement("p"); p.textContent = body.text;
  const badge = document.createElement("span");
  badge.className = "badge " + (body.verified ? "ok" : "warn");
  badge.textContent = body.verified ? t("common.verified") : t("common.to_verify");
  card.append(h, p, badge);
  if (body.source) {
    const src = document.createElement("span");
    src.className = "src"; src.textContent = t("common.source") + " · " + body.source;
    card.appendChild(src);
  }
  pop.appendChild(card);

  const props = document.getElementById("props");
  props.innerHTML = "";
  const pos = PROP_POS[s.layer] || PROP_POS.village;
  const holder = document.createElement("div");
  holder.className = "prop";
  holder.innerHTML = PROPS[s.layer] || PROPS.village;
  holder.style.transform = `translateX(${pos.x}px) translateZ(${pos.z}px) scale(${pos.scale}) rotateX(6deg)`;
  props.appendChild(holder);

  card.style.display = cardHidden ? "none" : "block";
  document.getElementById("reopen").classList.toggle("show", cardHidden);
  requestAnimationFrame(() => {
    if (!cardHidden) card.classList.add("up");
    holder.classList.add("up");
  });
  if (gl) gl.focus(index);
}

/* ---------- parallaxe pointeur, sans dépendance ---------- */
let tiltX = 0, tiltY = 0;
function applyTilt(px, py) {
  tiltY = (px - .5) * 14;
  tiltX = (.5 - py) * 8;
  document.getElementById("layers").style.transform =
    `rotateX(${tiltX}deg) rotateY(${tiltY}deg)`;
  document.getElementById("book").style.transform =
    `rotateX(${tiltX * .5}deg) rotateY(${tiltY * .5}deg)`;
  if (gl) gl.tilt(tiltY, tiltX);
}
const stage = document.getElementById("stage");
stage.addEventListener("pointermove", (e) => applyTilt(e.clientX / innerWidth, e.clientY / innerHeight), { passive: true });
stage.addEventListener("touchmove", (e) => {
  const p = e.touches[0];
  if (p) applyTilt(p.clientX / innerWidth, p.clientY / innerHeight);
}, { passive: true });
addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "ArrowDown") { index = (index + 1) % DATA.scenes.length; renderChrome(); renderScene(); }
  if (e.key === "ArrowLeft" || e.key === "ArrowUp") { index = (index + DATA.scenes.length - 1) % DATA.scenes.length; renderChrome(); renderScene(); }
});

/* ---------- couche Three.js : strictement optionnelle ---------- */
function loadThree() {
  return new Promise((resolve, reject) => {
    if (window.THREE) return resolve(window.THREE);
    const s = document.createElement("script");
    s.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";
    s.onload = () => resolve(window.THREE);
    s.onerror = reject;
    document.head.appendChild(s);
  });
}

function toast(key) {
  const box = document.getElementById("toast");
  box.innerHTML = "";
  const s = document.createElement("span");
  s.textContent = t(key);
  box.appendChild(s);
  setTimeout(() => { if (box.firstChild === s) box.innerHTML = ""; }, 4200);
}

function handleFile(file) {
  if (!file) return;
  if (!gl) { toast("popup.fallback"); return; }
  gl.loadMedia(file, index, (state) => {
    if (state === "ok") toast("popup.media_ok");
    else if (state === "blocked") toast("popup.media_blocked");
    else toast("popup.media_err");
  });
}

const fileInput = document.getElementById("file");
document.getElementById("btnMedia").onclick = () => fileInput.click();
fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

const drop = document.getElementById("drop");
["dragenter", "dragover"].forEach((ev) =>
  addEventListener(ev, (e) => { e.preventDefault(); drop.classList.add("on"); }));
["dragleave", "drop"].forEach((ev) =>
  addEventListener(ev, (e) => { e.preventDefault(); if (ev === "dragleave" && e.relatedTarget) return; drop.classList.remove("on"); }));
addEventListener("drop", (e) => {
  e.preventDefault();
  drop.classList.remove("on");
  const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
  handleFile(f);
});

document.getElementById("reopen").onclick = () => { cardHidden = false; renderScene(); };

function setGL(on) {
  document.getElementById("gl").classList.toggle("on", on);
  document.getElementById("stage").classList.toggle("gl", on);
  document.getElementById("btn3d").setAttribute("aria-pressed", String(on));
}

document.getElementById("btnAuto").onclick = () => {
  if (auto) { clearInterval(auto); auto = null; }
  else {
    auto = setInterval(() => {
      index = (index + 1) % DATA.scenes.length;
      renderChrome(); renderScene();
    }, 9000);
  }
  renderChrome();
};

document.getElementById("btn3d").onclick = () => {
  want3d = !want3d;
  setGL(want3d && !!gl);
  if (!gl && want3d) start3d();
};

function start3d() {
  loadThree().then((THREE) => {
    gl = window.buildScene(THREE, document.getElementById('gl'));
    if (!gl) { degrade(); return; }
    setGL(true);
    gl.focus(index);
  }).catch(degrade);
}

function degrade() {
  gl = null;
  want3d = false;
  document.getElementById("gl").classList.remove("on");
  document.getElementById("stage").classList.remove("gl");
  const b = document.getElementById("btn3d");
  b.setAttribute("aria-pressed", "false");
  b.disabled = true;
  document.getElementById("t-hint").textContent = t("popup.fallback");
}

document.getElementById("openBtn").onclick = () => {
  document.getElementById("cover").classList.add("gone");
  renderScene();
  start3d();
};

renderChrome();
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    """Assemble la page : données JSON + module de scène 3D, inlinés (page autonome)."""
    scene_js = (BASE / "ui" / "scene3d.js").read_text(encoding="utf-8")
    html = (TEMPLATE
            .replace("__SCENE3D__", scene_js)
            .replace("__DATA__", json.dumps(collect(), ensure_ascii=False)))
    out.write_text(html, encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "refek-sidi-bou-said-3d.html"
    built = build(target)
    scenes = load_json("data/scenes.json")
    sys.stdout.write(f"HTML 3D -> {built}\n")
    sys.stdout.write(f"{len(scenes)} scenes · fallback CSS actif sans WebGL\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
