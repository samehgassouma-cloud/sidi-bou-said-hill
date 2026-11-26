#!/usr/bin/env python3
"""خريطة سيدي بوسعيد التفاعلية — plan du village avec médaillons pop-up 3D.

La page s'ouvre sur le contour réel de la Tunisie (Natural Earth, déjà dans
data/tunisia-geo.json) puis plonge sur le village : c'est la même continuité que
depuis la carte nationale. Les repères sont placés à leurs positions relatives
réelles (vérifiées via Google Places) sur un fond dessiné, et surgissent un à un
le long du parcours, comme les plats du menu 3D.

Lancement :
    python prototype/build_village.py
    # puis ouvrir sidi-bou-said-carte.html
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
    geo = load_json("data/tunisia-geo.json")
    return {
        "i18n": {lang: load_json(f"i18n/{lang}.json") for lang in LANGS},
        "village": load_json("data/sbs-landmarks.json"),
        "unesco": load_json("data/unesco.json"),
        "outline": [g["polys"] for g in geo["governorates"]],
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sidi Bou Saïd — carte interactive</title>
<style>
  :root { --navy:#0A1628; --deep:#123A5C; --blue:#2E7BB5; --gold:#D4A017; --teal:#00B4D8;
          --paper:#FAF7F0; --muted:#8FA3B5; --line:rgba(255,255,255,.12); }
  * { box-sizing:border-box; }
  html, body { margin:0; height:100%; background:var(--navy); color:#EAF2F9; overflow:hidden;
               font-family:system-ui,-apple-system,"Segoe UI",sans-serif; }
  html[dir="rtl"] body { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }

  .stage { position:relative; height:100%; perspective:1500px; overflow:hidden; }

  /* ---- vol d'entrée : le pays puis le village ---- */
  .flight { position:absolute; inset:0; z-index:9; display:flex; align-items:center; justify-content:center;
            background:radial-gradient(circle at 50% 45%, #17324C, #060F1B 70%);
            transition:opacity 1s ease; }
  .flight.gone { opacity:0; pointer-events:none; }
  .flight svg { width:min(70vw, 380px); height:auto;
                transition:transform 2.4s cubic-bezier(.6,.02,.2,1), opacity 1.6s ease; }
  .flight.zoom svg { transform:scale(26) translate(-2.5%, -13%); opacity:0; }
  .flight .cap { position:absolute; bottom:14%; text-align:center; font-size:13px; color:var(--muted); }
  .flight button { position:absolute; bottom:8%; background:var(--gold); color:#22303B; border:0;
                   font-weight:600; border-radius:22px; padding:12px 26px; font-size:14px; cursor:pointer; }
  .pin { fill:var(--gold); }

  /* ---- plan du village ---- */
  .plan { position:absolute; inset:0; transform-style:preserve-3d;
          transition:transform .6s cubic-bezier(.2,.7,.3,1); }
  .plan svg { position:absolute; inset:0; width:100%; height:100%; }
  .sea { fill:url(#seaGrad); }
  .land { fill:#EFE7D6; }
  .cliff { fill:none; stroke:var(--gold); stroke-width:1.4; opacity:.7; }
  .street { fill:none; stroke:#D8CBB0; stroke-width:2.4; stroke-linecap:round; }
  .route { fill:none; stroke:var(--teal); stroke-width:2; stroke-dasharray:5 4; opacity:.85; }
  .routeDone { fill:none; stroke:var(--gold); stroke-width:2.6; stroke-linecap:round; }

  /* ---- médaillons pop-up, comme les plats du menu 3D ---- */
  .marks { position:absolute; inset:0; transform-style:preserve-3d; }
  .mark { position:absolute; width:104px; margin-inline-start:-52px; text-align:center;
          transform-style:preserve-3d; opacity:0; pointer-events:none;
          transition:opacity .5s ease, transform .75s cubic-bezier(.2,.9,.25,1); }
  .mark.up { opacity:1; pointer-events:auto; }
  .medal { width:84px; height:84px; margin:0 auto; border-radius:50%; background:var(--paper);
           border:3px solid var(--gold); box-shadow:0 16px 30px rgba(0,0,0,.5);
           display:flex; align-items:center; justify-content:center; overflow:hidden;
           transform:rotateX(58deg) translateZ(0); transform-origin:50% 100%;
           transition:transform .75s cubic-bezier(.2,.9,.25,1), box-shadow .3s ease; cursor:pointer; }
  .mark.up .medal { transform:rotateX(0deg) translateZ(30px); }
  .mark.active .medal { border-color:var(--teal); box-shadow:0 22px 40px rgba(0,180,216,.35); }
  .medal:hover { transform:rotateX(0) translateZ(46px) scale(1.06); }
  .mark .stem { width:2px; height:22px; margin:0 auto; background:linear-gradient(var(--gold), transparent); }
  .mark .dot { width:9px; height:9px; border-radius:50%; background:var(--gold); margin:0 auto;
               box-shadow:0 0 0 4px rgba(212,160,23,.25); }
  .mark .cap { font-size:10.5px; margin-top:5px; color:#EAF2F9; text-shadow:0 2px 6px #0A1628; }
  .mark .num { position:absolute; top:-6px; inset-inline-start:22px; width:22px; height:22px; border-radius:50%;
               background:var(--navy); border:1px solid var(--gold); font-size:11px; line-height:20px;
               color:var(--gold); }

  /* ---- interface ---- */
  header { position:absolute; top:0; inset-inline:0; z-index:7; padding:14px 18px; display:flex;
           align-items:center; gap:12px; flex-wrap:wrap;
           background:linear-gradient(rgba(10,22,40,.92), rgba(10,22,40,0)); }
  header h1 { font-size:16px; margin:0; }
  header .sub { font-size:10.5px; color:var(--muted); margin-top:2px; }
  .spacer { margin-inline-start:auto; }
  .chip { background:rgba(255,255,255,.10); border:1px solid var(--line); color:#EAF2F9;
          border-radius:14px; padding:7px 12px; font-size:11.5px; cursor:pointer; text-decoration:none; }
  .chip[aria-pressed="true"], .chip.gold { background:var(--gold); color:#22303B; border-color:var(--gold); font-weight:600; }

  .card { position:absolute; z-index:8; bottom:86px; inset-inline-start:50%; transform:translateX(-50%);
          width:min(92vw, 460px); background:var(--paper); color:#1F2A33; border-radius:18px;
          padding:16px 18px; border:1px solid rgba(212,160,23,.6); box-shadow:0 24px 60px rgba(0,0,0,.55);
          transition:opacity .4s ease, transform .5s ease; }
  html[dir="rtl"] .card { transform:translateX(50%); }
  .card.hidden { opacity:0; pointer-events:none; }
  .card h2 { margin:0 34px 4px 0; font-size:17px; color:var(--deep); }
  html[dir="rtl"] .card h2 { margin:0 0 4px 34px; }
  .card p { margin:6px 0 0; font-size:13px; line-height:1.6; color:#33424F; }
  .card .close { position:absolute; top:12px; inset-inline-end:12px; width:28px; height:28px; border-radius:50%;
                 border:1px solid #D9D2C2; background:#fff; color:#5A6570; cursor:pointer; }
  .badge { display:inline-block; margin-top:10px; font-size:10.5px; padding:4px 10px; border-radius:12px; }
  .badge.ok { background:#E7F1F8; color:#1B5C86; border:1px solid var(--blue); }
  .badge.warn { background:#FFF3D6; color:#8A6A12; border:1px solid var(--gold); }

  .rail { position:absolute; bottom:18px; inset-inline:0; z-index:8; display:flex; gap:8px;
          justify-content:center; flex-wrap:wrap; padding:0 14px; }
  .note { position:absolute; bottom:60px; inset-inline:0; text-align:center; font-size:10px;
          color:var(--muted); z-index:6; }
  @media (prefers-reduced-motion: reduce) { .mark, .medal, .flight svg, .plan { transition:none !important; } }
</style>
</head>
<body>
<div class="stage" id="stage">

  <div class="plan" id="plan">
    <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Plan schématique de Sidi Bou Saïd">
      <defs>
        <linearGradient id="seaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#1E5E8C"/><stop offset="1" stop-color="#0B2A44"/>
        </linearGradient>
      </defs>
      <rect class="sea" width="100" height="100"/>
      <!-- promontoire dessiné à la main : ce n'est pas un tracé cadastral -->
      <path class="land" d="M0 26 C14 20 30 14 46 13 C64 12 78 18 84 30 C92 46 88 66 74 76
                            C60 86 34 90 16 84 C4 80 -2 60 0 26 Z"/>
      <path class="cliff" d="M84 30 C92 46 88 66 74 76"/>
      <g class="street">
        <path d="M8 38 C24 36 40 34 56 31"/>
        <path d="M56 31 C60 26 62 18 64 11"/>
        <path d="M56 31 C58 42 58 50 58 57"/>
        <path d="M58 57 C70 52 80 48 89 45"/>
        <path d="M89 45 C92 60 92 76 92 88"/>
      </g>
      <g id="unescoZone" style="display:none">
        <ellipse id="zBuffer" fill="rgba(212,160,23,.10)" stroke="#D4A017"
                 stroke-width="0.6" stroke-dasharray="2 1.6"/>
        <ellipse id="zCore" fill="rgba(0,180,216,.12)" stroke="#00B4D8" stroke-width="0.8"/>
      </g>
      <path class="route" id="routeLine"/>
      <path class="routeDone" id="routeDone"/>
    </svg>
    <div class="marks" id="marks"></div>
  </div>

  <header>
    <div>
      <h1 id="t-title"></h1>
      <div class="sub" id="t-sub"></div>
    </div>
    <div class="spacer"></div>
    <a class="chip" id="backMap" href="carte-tunisie.html"></a>
    <a class="chip" id="to3d" href="refek-sidi-bou-said-3d.html"></a>
    <button class="chip" id="btnUnesco" aria-pressed="false"></button>
    <button class="chip" id="btnAll"></button>
    <button class="chip" id="btnWalk" aria-pressed="false"></button>
    <span id="langs"></span>
  </header>

  <div class="card hidden" id="card"></div>
  <div class="note" id="t-note"></div>
  <div class="rail">
    <button class="chip" id="prev"></button>
    <button class="chip gold" id="next"></button>
  </div>

  <div class="flight" id="flight">
    <svg id="outline" viewBox="0 0 100 100" aria-label="Contour de la Tunisie"></svg>
    <div class="cap" id="t-fly"></div>
    <button id="enter"></button>
  </div>
</div>

<script>
const DATA = __DATA__;
let lang = "fr", step = -1, walking = null, showAll = false;
const t = (k) => DATA.i18n[lang][k] || "\\u00ab" + k + "\\u00bb";
const LM = DATA.village.landmarks;

/* ---------- illustrations des médaillons : SVG originaux, un par repère ---------- */
const ART = {
  train: `<svg viewBox="0 0 60 60" width="66" height="66"><rect x="12" y="16" width="36" height="26" rx="5" fill="#2E6FA8"/><rect x="17" y="21" width="11" height="9" fill="#F6EEDA"/><rect x="32" y="21" width="11" height="9" fill="#F6EEDA"/><rect x="16" y="34" width="28" height="4" fill="#D4A017"/><circle cx="21" cy="46" r="4" fill="#123A5C"/><circle cx="39" cy="46" r="4" fill="#123A5C"/><path d="M8 52h44" stroke="#123A5C" stroke-width="2"/></svg>`,
  house: `<svg viewBox="0 0 60 60" width="66" height="66"><rect x="12" y="22" width="36" height="30" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M9 22 30 10 51 22" fill="none" stroke="#123A5C" stroke-width="2"/><path d="M24 52V36a6 6 0 0112 0v16z" fill="#2E6FA8"/><circle cx="30" cy="30" r="4" fill="none" stroke="#D4A017" stroke-width="2"/><path d="M16 52h28" stroke="#D4A017" stroke-width="2"/></svg>`,
  cafe: `<svg viewBox="0 0 60 60" width="66" height="66"><path d="M16 24h26v12a13 13 0 01-26 0z" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M42 27h6a5 5 0 010 10h-6" fill="none" stroke="#123A5C" stroke-width="2"/><path d="M22 18c0-3 3-3 3-6M30 18c0-3 3-3 3-6" stroke="#D4A017" stroke-width="2" fill="none"/><path d="M12 50h36" stroke="#2E6FA8" stroke-width="3"/></svg>`,
  dome: `<svg viewBox="0 0 60 60" width="66" height="66"><rect x="14" y="34" width="32" height="18" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M16 34a14 10 0 0128 0z" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M30 24v-6" stroke="#D4A017" stroke-width="2"/><circle cx="30" cy="15" r="3" fill="#D4A017"/><path d="M25 52V42a5 5 0 0110 0v10z" fill="#2E6FA8"/></svg>`,
  lighthouse: `<svg viewBox="0 0 60 60" width="66" height="66"><path d="M24 52 26 24h8l2 28z" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><rect x="24" y="18" width="12" height="7" fill="#D4A017"/><path d="M22 14h16l-3 4H25z" fill="#2E6FA8"/><path d="M14 20l8 2M46 20l-8 2" stroke="#D4A017" stroke-width="2"/><path d="M16 52h28" stroke="#2E6FA8" stroke-width="3"/></svg>`,
  palace: `<svg viewBox="0 0 60 60" width="66" height="66"><rect x="10" y="28" width="40" height="24" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M16 52V40a5 5 0 0110 0v12zM34 52V40a5 5 0 0110 0v12z" fill="#2E6FA8"/><path d="M10 28h40" stroke="#D4A017" stroke-width="2"/><path d="M20 28V18h20v10" fill="none" stroke="#123A5C" stroke-width="2"/><circle cx="30" cy="14" r="3" fill="#D4A017"/></svg>`,
  terrace: `<svg viewBox="0 0 60 60" width="66" height="66"><path d="M8 52h14V42h12V32h18" fill="none" stroke="#123A5C" stroke-width="2"/><rect x="34" y="20" width="18" height="12" fill="#2E6FA8"/><circle cx="18" cy="36" r="4" fill="#D4A017"/><path d="M8 52h44" stroke="#D4A017" stroke-width="2"/></svg>`,
  boat: `<svg viewBox="0 0 60 60" width="66" height="66"><path d="M12 40h36l-6 10H18z" fill="#F3EFE6" stroke="#123A5C" stroke-width="2"/><path d="M30 38V12l14 20z" fill="#2E6FA8"/><path d="M28 38V18L16 38z" fill="#D4A017"/><path d="M8 54h44" stroke="#2E7BB5" stroke-width="3"/></svg>`
};

/* ---------- vol d'entrée : contour réel du pays ---------- */
function drawOutline() {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  DATA.outline.forEach((polys) => polys.forEach((poly) => poly[0].forEach((c) => {
    if (c[0] < x0) x0 = c[0]; if (c[0] > x1) x1 = c[0];
    if (c[1] < y0) y0 = c[1]; if (c[1] > y1) y1 = c[1];
  })));
  const sx = 100 / (x1 - x0), sy = 100 / (y1 - y0), s = Math.min(sx, sy);
  const ox = (100 - (x1 - x0) * s) / 2, oy = (100 - (y1 - y0) * s) / 2;
  const P = (c) => [(c[0] - x0) * s + ox, (y1 - c[1]) * s + oy];

  const svg = document.getElementById("outline");
  const NS = "http://www.w3.org/2000/svg";
  DATA.outline.forEach((polys) => polys.forEach((poly) => {
    const p = document.createElementNS(NS, "path");
    p.setAttribute("d", "M" + poly[0].map((c) => P(c).map((v) => v.toFixed(2)).join(" ")).join("L") + "Z");
    p.setAttribute("fill", "#1B4B73");
    p.setAttribute("stroke", "#6E9CC4");
    p.setAttribute("stroke-width", "0.25");
    svg.appendChild(p);
  }));
  // repère de Sidi Bou Saïd, aux vraies coordonnées
  const [mx, my] = P([10.3417, 36.8687]);
  const pin = document.createElementNS(NS, "circle");
  pin.setAttribute("cx", mx.toFixed(2)); pin.setAttribute("cy", my.toFixed(2));
  pin.setAttribute("r", "1.4"); pin.setAttribute("class", "pin");
  svg.appendChild(pin);
}

/* ---------- plan : repères et parcours ---------- */
function buildMarks() {
  const holder = document.getElementById("marks");
  holder.innerHTML = "";
  LM.forEach((l, i) => {
    const m = document.createElement("div");
    m.className = "mark";
    m.style.insetInlineStart = l.plan[0] + "%";
    m.style.top = l.plan[1] + "%";
    m.dataset.i = i;

    const medal = document.createElement("div");
    medal.className = "medal";
    medal.innerHTML = ART[l.art] || ART.house;
    medal.onclick = () => goTo(i);

    const num = document.createElement("span");
    num.className = "num";
    num.textContent = l.order;

    const stem = document.createElement("div");
    stem.className = "stem";
    const dot = document.createElement("div");
    dot.className = "dot";
    const cap = document.createElement("div");
    cap.className = "cap";
    cap.textContent = l.name[lang];

    m.append(num, medal, stem, dot, cap);
    holder.appendChild(m);
  });
  const d = "M" + LM.map((l) => l.plan[0] + " " + l.plan[1]).join("L");
  document.getElementById("routeLine").setAttribute("d", d);
}

function paintRoute() {
  const done = LM.slice(0, Math.max(step + 1, 0));
  document.getElementById("routeDone").setAttribute("d",
    done.length > 1 ? "M" + done.map((l) => l.plan[0] + " " + l.plan[1]).join("L") : "");
}

function renderMarks() {
  document.querySelectorAll(".mark").forEach((m, i) => {
    const visible = showAll || i <= step;
    m.classList.toggle("up", visible);
    m.classList.toggle("active", i === step);
  });
  paintRoute();
}

function renderCard() {
  const card = document.getElementById("card");
  if (step < 0) { card.classList.add("hidden"); return; }
  const l = LM[step];
  card.innerHTML = "";
  const close = document.createElement("button");
  close.className = "close"; close.textContent = "\\u2715";
  close.onclick = () => card.classList.add("hidden");
  const h = document.createElement("h2");
  h.textContent = t("vill.step") + " " + l.order + " · " + l.name[lang];
  const p = document.createElement("p");
  p.textContent = l.text[lang];
  const badge = document.createElement("span");
  badge.className = "badge " + (l.verified ? "ok" : "warn");
  badge.textContent = (l.verified ? t("common.verified") : t("common.to_verify"))
    + (l.verify_note ? " · " + l.verify_note : "");
  card.append(close, h, p, badge);

  // les cafés du parcours ouvrent la réservation de table
  if (l.id === "nattes" || l.id === "delices") {
    const a = document.createElement("a");
    a.className = "chip gold";
    a.style.display = "inline-block";
    a.style.marginTop = "10px";
    a.href = "../amal-3/cafe-reservation-3d.html";
    a.textContent = t("cafe.open_cafe");
    a.onclick = (e) => {
      e.preventDefault();
      const w = window.open(a.getAttribute("href"), "_blank");
      if (!w) document.getElementById("t-note").textContent = t("link.same_folder");
    };
    card.appendChild(a);
  }
  card.classList.remove("hidden");
}

function goTo(i) {
  step = Math.max(0, Math.min(LM.length - 1, i));
  // la scène glisse pour amener le repère courant vers le centre
  const l = LM[step];
  const plan = document.getElementById("plan");
  plan.style.transform = "translate(" + (46 - l.plan[0]) * 0.55 + "%, " + (48 - l.plan[1]) * 0.55 + "%) scale(1.12)";
  renderMarks();
  renderCard();
}

/* ---------- interface ---------- */
function renderChrome() {
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("vill.title");
  document.getElementById("t-sub").textContent = t("vill.sub");
  document.getElementById("t-note").textContent = t("vill.plan_note");
  document.getElementById("t-fly").textContent = t("vill.flying");
  document.getElementById("enter").textContent = t("vill.enter");
  document.getElementById("next").textContent = t("vill.next");
  document.getElementById("prev").textContent = t("vill.prev");
  document.getElementById("btnAll").textContent = t("vill.all");
  document.getElementById("btnUnesco").textContent = t("unesco.toggle");
  document.getElementById("btnWalk").textContent = t("vill.walk");
  document.getElementById("backMap").textContent = t("vill.back_map");
  document.getElementById("to3d").textContent = t("map.open_3d");

  const langs = document.getElementById("langs");
  langs.innerHTML = "";
  Object.keys(DATA.langLabels).forEach((code) => {
    const b = document.createElement("button");
    b.className = "chip"; b.style.marginInlineStart = "6px";
    b.textContent = code.toUpperCase();
    b.setAttribute("aria-pressed", code === lang);
    b.onclick = () => { lang = code; renderChrome(); buildMarks(); renderMarks(); renderCard(); };
    langs.appendChild(b);
  });
}

// Les liens entre pages ne marchent que si les fichiers sont côte à côte :
// si l'ouverture est refusée, on affiche la raison plutôt que de rester muet.
["backMap", "to3d"].forEach((id) => {
  const a = document.getElementById(id);
  a.target = "_blank";
  a.rel = "noopener";
  a.onclick = (e) => {
    e.preventDefault();
    const w = window.open(a.getAttribute("href"), "_blank");
    if (!w) document.getElementById("t-note").textContent = t("link.same_folder");
  };
});

/* ---------- périmètre UNESCO : surface exacte, tracé indicatif ----------
   Le plan couvre une emprise réelle connue (span_m) : on convertit donc les rayons
   équivalents en pourcentages du plan, séparément en X et en Y puisque le fond est
   étiré. Ce sont des cercles de surface juste, pas la limite officielle. */
function placeUnescoZone() {
  const span = DATA.village.meta.span_m;          // [largeur_m, hauteur_m] du parcours
  const U = DATA.unesco;
  // le parcours occupe 84 % de la largeur et 78 % de la hauteur du plan
  const mPerX = span[0] / 84, mPerY = span[1] / 78;
  const centre = LM.find((l) => l.id === "mosquee") || LM[0];
  [["zCore", U.equiv_radius_m.core], ["zBuffer", U.equiv_radius_m.core_plus_buffer]].forEach(([id, r]) => {
    const el = document.getElementById(id);
    el.setAttribute("cx", centre.plan[0]);
    el.setAttribute("cy", centre.plan[1]);
    el.setAttribute("rx", (r / mPerX).toFixed(2));
    el.setAttribute("ry", (r / mPerY).toFixed(2));
  });
}

function unescoCard() {
  const U = DATA.unesco;
  const card = document.getElementById("card");
  card.innerHTML = "";
  const close = document.createElement("button");
  close.className = "close"; close.textContent = "\u2715";
  close.onclick = () => card.classList.add("hidden");
  const h = document.createElement("h2");
  h.textContent = t("unesco.title");
  const area = document.createElement("p");
  area.textContent = t("unesco.core") + " : " + U.core_ha + " ha (" + t("unesco.equiv") + " ≈ "
    + U.equiv_radius_m.core + " m) · " + t("unesco.buffer") + " : " + U.buffer_ha + " ha";
  const crit = document.createElement("p");
  crit.textContent = t("unesco.criterion") + " " + U.criterion + " — " + U.why[lang];
  const scope = document.createElement("p");
  scope.textContent = U.scope[lang];
  const shape = document.createElement("p");
  shape.textContent = U.shape_note[lang];
  const badge = document.createElement("span");
  badge.className = "badge ok";
  badge.textContent = t("common.verified") + " · " + U.source;
  card.append(close, h, area, crit, scope, shape, badge);
  card.classList.remove("hidden");
}

document.getElementById("btnUnesco").onclick = () => {
  const z = document.getElementById("unescoZone");
  const on = z.style.display === "none";
  z.style.display = on ? "block" : "none";
  document.getElementById("btnUnesco").setAttribute("aria-pressed", String(on));
  if (on) unescoCard();
};

document.getElementById("next").onclick = () => goTo(step + 1);
document.getElementById("prev").onclick = () => goTo(step - 1);
document.getElementById("btnAll").onclick = () => { showAll = !showAll; renderMarks(); };
document.getElementById("btnWalk").onclick = () => {
  const b = document.getElementById("btnWalk");
  if (walking) { clearInterval(walking); walking = null; }
  else {
    walking = setInterval(() => {
      if (step >= LM.length - 1) { clearInterval(walking); walking = null; b.setAttribute("aria-pressed", "false"); return; }
      goTo(step + 1);
    }, 5200);
  }
  b.setAttribute("aria-pressed", String(!!walking));
};
addEventListener("keydown", (e) => {
  if (e.key === "ArrowRight" || e.key === "ArrowDown") goTo(step + 1);
  if (e.key === "ArrowLeft" || e.key === "ArrowUp") goTo(step - 1);
});

document.getElementById("enter").onclick = () => {
  const f = document.getElementById("flight");
  f.classList.add("zoom");
  setTimeout(() => { f.classList.add("gone"); goTo(0); }, 2200);
};

drawOutline();
buildMarks();
placeUnescoZone();
renderChrome();
renderMarks();
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    out.write_text(TEMPLATE.replace("__DATA__", json.dumps(collect(), ensure_ascii=False)), encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "sidi-bou-said-carte.html"
    built = build(target)
    v = load_json("data/sbs-landmarks.json")
    sys.stdout.write(f"HTML village -> {built}\n")
    sys.stdout.write(f"{len(v['landmarks'])} reperes · emprise {v['meta']['span_m'][0]}m x {v['meta']['span_m'][1]}m\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
