#!/usr/bin/env python3
"""خريطة تونس التفاعلية — générateur de la carte.

Carte SVG autonome : pas de tuiles, pas de CDN, pas de clé d'API. Les limites des
gouvernorats viennent de Natural Earth (domaine public) et les villes de GeoNames ;
aucune coordonnée n'est inventée. Ce que les sources ne couvrent pas est signalé
dans l'interface plutôt que comblé.

Lancement :
    python prototype/build_map.py
    # puis ouvrir carte-tunisie.html
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
        "geo": load_json("data/tunisia-geo.json"),
        "unesco": load_json("data/unesco.json"),
        "knowledge": load_json("data/knowledge.json"),
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Carte interactive de la Tunisie</title>
<style>
  :root { --navy:#0A1628; --deep:#123A5C; --blue:#2E7BB5; --gold:#D4A017; --teal:#00B4D8;
          --paper:#FAF7F0; --muted:#8FA3B5; --line:rgba(255,255,255,.12); }
  * { box-sizing:border-box; }
  html, body { margin:0; height:100%; background:var(--navy); color:#EAF2F9;
               font-family:system-ui,-apple-system,"Segoe UI",sans-serif; overflow:hidden; }
  html[dir="rtl"] body { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }
  .app { display:flex; flex-direction:column; height:100%; }

  header { padding:12px 16px; display:flex; align-items:center; gap:12px; flex-wrap:wrap;
           border-bottom:1px solid var(--line); background:linear-gradient(180deg,#0D1E33,#0A1628); }
  header h1 { font-size:16px; margin:0; }
  header .sub { font-size:10.5px; color:var(--muted); margin-top:2px; }
  .spacer { margin-inline-start:auto; }
  .chip { background:rgba(255,255,255,.09); border:1px solid var(--line); color:#EAF2F9;
          border-radius:14px; padding:7px 12px; font-size:11.5px; cursor:pointer; }
  .chip[aria-pressed="true"] { background:var(--gold); color:#22303B; border-color:var(--gold); font-weight:600; }
  .chip.gold { background:var(--gold); color:#22303B; font-weight:600; border-color:var(--gold); }

  .body { flex:1; display:flex; min-height:0; }
  .map { flex:1; position:relative; touch-action:none; background:
         radial-gradient(circle at 50% 20%, #17324C, #0A1628 70%); }
  svg { width:100%; height:100%; display:block; cursor:grab; }
  svg.drag { cursor:grabbing; }
  .gov { fill:#1B4B73; stroke:#6E9CC4; stroke-width:.5px; vector-effect:non-scaling-stroke; }
  .gov:hover { fill:#27689B; }
  .gov.sel { fill:#2E7BB5; stroke:var(--gold); stroke-width:1.6px; }
  .city { fill:#F6EEDA; stroke:#0A1628; stroke-width:.4px; vector-effect:non-scaling-stroke; cursor:pointer; }
  .city.big { fill:var(--teal); }
  .city.sbs { fill:var(--gold); stroke:#fff; stroke-width:1px; }
  .clabel { fill:#EAF2F9; font-size:3px; paint-order:stroke; stroke:#0A1628; stroke-width:.8px; pointer-events:none; }

  aside { width:310px; max-width:46vw; border-inline-start:1px solid var(--line); display:flex;
          flex-direction:column; background:#0C1D30; }
  .search { padding:10px; border-bottom:1px solid var(--line); }
  .search input { width:100%; background:#0A1628; border:1px solid var(--line); color:#EAF2F9;
                  border-radius:12px; padding:9px 12px; font-size:12.5px; outline:none; }
  .list { flex:1; overflow-y:auto; padding:8px; }
  .row { display:flex; align-items:center; gap:8px; padding:8px 10px; border-radius:10px; cursor:pointer;
         font-size:12px; }
  .row:hover { background:rgba(255,255,255,.06); }
  .row.head { color:var(--gold); font-size:10.5px; letter-spacing:.6px; cursor:default; padding-top:12px; }
  .row .pop { margin-inline-start:auto; color:var(--muted); font-size:10.5px; }
  .row.sbs { border:1px solid var(--gold); background:rgba(212,160,23,.10); }

  .panel { border-top:1px solid var(--line); padding:12px; font-size:12px; line-height:1.55; }
  .panel h2 { margin:0 0 6px; font-size:14px; color:var(--gold); }
  .panel p { margin:4px 0; color:#CBDBE8; }
  .badge { display:inline-block; margin-top:8px; font-size:10px; padding:4px 10px; border-radius:11px; }
  .badge.ok { background:rgba(46,123,181,.22); color:#9FD3F0; border:1px solid var(--blue); }
  .badge.warn { background:rgba(212,160,23,.16); color:#F0D083; border:1px solid var(--gold); }
  .links { display:flex; gap:8px; flex-wrap:wrap; margin-top:10px; }
  .links a { text-decoration:none; }
  footer { padding:8px 12px; font-size:9.5px; color:var(--muted); border-top:1px solid var(--line); }
  .zoom { position:absolute; inset-inline-end:12px; bottom:12px; display:flex; flex-direction:column; gap:6px; }
  .zoom button { width:36px; height:36px; border-radius:10px; border:1px solid var(--line);
                 background:rgba(10,22,40,.85); color:#EAF2F9; font-size:16px; cursor:pointer; }
  @media (max-width:820px) {
    .body { flex-direction:column; }
    aside { width:100%; max-width:none; height:44%; border-inline-start:0; border-top:1px solid var(--line); }
  }
</style>
</head>
<body>
<div class="app">
  <header>
    <div>
      <h1 id="t-title"></h1>
      <div class="sub" id="t-sub"></div>
    </div>
    <div class="spacer"></div>
    <button class="chip gold" id="btnFocus"></button>
    <button class="chip" id="btnReset"></button>
    <span id="langs"></span>
  </header>

  <div class="body">
    <div class="map" id="map">
      <svg id="svg" role="img" aria-label="Carte de la Tunisie"></svg>
      <div class="zoom">
        <button id="zin">+</button>
        <button id="zout">−</button>
      </div>
    </div>
    <aside>
      <div class="search"><input id="q" type="text"></div>
      <div class="list" id="list"></div>
      <div class="panel" id="panel"></div>
      <footer id="sources"></footer>
    </aside>
  </div>
</div>

<script>
const DATA = __DATA__;
let lang = "fr";
let selected = null;
const t = (k) => DATA.i18n[lang][k] || "\\u00ab" + k + "\\u00bb";

/* ---------- projection : équirectangulaire corrigée en longitude ---------- */
const LAT0 = 34.0, K = Math.cos(LAT0 * Math.PI / 180);
const px = (lon) => lon * K * 100;
const py = (lat) => -lat * 100;

const SBS = { name: "Sidi Bou Saïd", c: [10.3417, 36.8687] };

/* ---------- vue (viewBox) ---------- */
let view = { x: 0, y: 0, w: 0, h: 0 };
let full = null;

function bounds() {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  DATA.geo.governorates.forEach((g) => g.polys.forEach((poly) => poly[0].forEach((c) => {
    const x = px(c[0]), y = py(c[1]);
    if (x < x0) x0 = x; if (x > x1) x1 = x;
    if (y < y0) y0 = y; if (y > y1) y1 = y;
  })));
  const pad = 12;
  return { x: x0 - pad, y: y0 - pad, w: (x1 - x0) + pad * 2, h: (y1 - y0) + pad * 2 };
}

function applyView() {
  document.getElementById("svg").setAttribute("viewBox",
    view.x + " " + view.y + " " + view.w + " " + view.h);
  document.querySelectorAll(".clabel").forEach((el) => {
    el.style.display = view.w < 220 ? "block" : "none";
  });
}

function zoomTo(lon, lat, span) {
  const box = document.getElementById("map").getBoundingClientRect();
  const h = span * ((box.height || 1) / (box.width || 1));
  view = { x: px(lon) - span / 2, y: py(lat) - h / 2, w: span, h: h };
  applyView();
}

/* ---------- rendu ---------- */
function pathOf(poly) {
  return poly.map((ring) =>
    "M" + ring.map((c) => px(c[0]).toFixed(2) + " " + py(c[1]).toFixed(2)).join("L") + "Z"
  ).join(" ");
}

function draw() {
  const svg = document.getElementById("svg");
  svg.innerHTML = "";
  const NS = "http://www.w3.org/2000/svg";

  DATA.geo.governorates.forEach((g) => {
    g.polys.forEach((poly) => {
      const p = document.createElementNS(NS, "path");
      p.setAttribute("d", pathOf(poly));
      p.setAttribute("class", "gov");
      p.dataset.iso = g.iso;
      p.onclick = () => selectGov(g);
      svg.appendChild(p);
    });
  });

  DATA.geo.cities.forEach((c) => {
    const isSBS = c.n === SBS.name;
    const dot = document.createElementNS(NS, "circle");
    dot.setAttribute("cx", px(c.c[0]).toFixed(2));
    dot.setAttribute("cy", py(c.c[1]).toFixed(2));
    dot.setAttribute("r", isSBS ? 2.4 : (c.p > 100000 ? 2 : c.p > 20000 ? 1.3 : 0.8));
    dot.setAttribute("class", "city" + (isSBS ? " sbs" : c.p > 100000 ? " big" : ""));
    dot.onclick = (e) => { e.stopPropagation(); selectCity(c); };
    svg.appendChild(dot);

    if (c.p > 20000 || isSBS) {
      const lab = document.createElementNS(NS, "text");
      lab.setAttribute("x", (px(c.c[0]) + 3).toFixed(2));
      lab.setAttribute("y", (py(c.c[1]) + 1).toFixed(2));
      lab.setAttribute("class", "clabel");
      lab.textContent = c.n;
      lab.style.display = "none";
      svg.appendChild(lab);
    }
  });
}

/* ---------- panneaux ---------- */
function govName(iso) {
  const g = DATA.geo.governorates.find((x) => x.iso === iso);
  return g ? (g.name[lang] || g.name.fr) : "—";
}

function selectGov(g) {
  selected = { type: "gov", iso: g.iso };
  document.querySelectorAll(".gov").forEach((p) =>
    p.classList.toggle("sel", p.dataset.iso === g.iso));
  const cities = DATA.geo.cities.filter((c) => c.g === g.iso);
  renderList(cities, g.name[lang] || g.name.fr);
  const panel = document.getElementById("panel");
  panel.innerHTML = "";
  const h = document.createElement("h2");
  h.textContent = (g.name[lang] || g.name.fr) + " · " + g.iso;
  const p = document.createElement("p");
  p.textContent = t("map.cities") + " : " + cities.length;
  panel.append(h, p);
}

function selectCity(c) {
  selected = { type: "city", n: c.n };
  zoomTo(c.c[0], c.c[1], c.n === SBS.name ? 3 : 14);
  const panel = document.getElementById("panel");
  panel.innerHTML = "";
  const h = document.createElement("h2");
  h.textContent = c.n;
  const g = document.createElement("p");
  g.textContent = t("map.governorates") + " : " + (c.g ? govName(c.g) : "—");
  const pop = document.createElement("p");
  pop.textContent = t("map.population") + " : " + c.p.toLocaleString(lang === "ar" ? "ar-TN" : lang);
  const badge = document.createElement("span");
  badge.className = "badge warn";
  badge.textContent = t("map.pop_note");
  panel.append(h, g, pop, badge);

  if (c.n === SBS.name) {
    const U = DATA.unesco;
    const title = document.createElement("h2");
    title.style.marginTop = "12px";
    title.textContent = t("unesco.title");
    const area = document.createElement("p");
    area.textContent = t("unesco.core") + " : " + U.core_ha + " ha · "
      + t("unesco.buffer") + " : " + U.buffer_ha + " ha";
    const why = document.createElement("p");
    why.textContent = t("unesco.criterion") + " " + U.criterion + " — " + U.why[lang];
    const scope = document.createElement("p");
    scope.textContent = U.scope[lang];
    const rank = document.createElement("p");
    rank.textContent = U.rank[lang];
    const note = document.createElement("p");
    note.style.marginTop = "10px";
    note.textContent = U.dossier[lang];
    const ok = document.createElement("span");
    ok.className = "badge ok";
    ok.textContent = t("common.verified") + " · " + U.source;
    panel.append(title, area, why, scope, rank);
    const links = document.createElement("div");
    links.className = "links";
    [["sidi-bou-said-carte.html", "vill.title"], ["refek-sidi-bou-said-3d.html", "map.open_3d"],
     ["refek-sidi-bou-said.html", "map.open_chat"]]
      .forEach(([href, key]) => {
        // Un <button> imbriqué dans un <a> avale le clic : le lien EST le bouton.
        const a = document.createElement("a");
        a.className = "chip gold";
        a.href = href;
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = t(key);
        a.onclick = (e) => {
          const w = window.open(href, "_blank");
          if (w) { e.preventDefault(); return; }
          // ouverture refusée (aperçu isolé, fichier absent) : on le dit au lieu de ne rien faire
          e.preventDefault();
          const warn = document.createElement("p");
          warn.style.color = "#F0D083";
          warn.textContent = t("link.same_folder");
          links.after(warn);
        };
        links.appendChild(a);
      });
    panel.append(note, ok, links);
  }
}

function renderList(cities, title) {
  const list = document.getElementById("list");
  list.innerHTML = "";
  const head = document.createElement("div");
  head.className = "row head";
  head.textContent = (title || t("map.cities")).toUpperCase();
  list.appendChild(head);
  if (!cities.length) {
    const empty = document.createElement("div");
    empty.className = "row";
    empty.textContent = t("map.no_result");
    list.appendChild(empty);
    return;
  }
  cities.slice(0, 200).forEach((c) => {
    const row = document.createElement("div");
    row.className = "row" + (c.n === SBS.name ? " sbs" : "");
    const n = document.createElement("span");
    n.textContent = c.n;
    const p = document.createElement("span");
    p.className = "pop";
    p.textContent = c.p.toLocaleString(lang === "ar" ? "ar-TN" : lang);
    row.append(n, p);
    row.onclick = () => selectCity(c);
    list.appendChild(row);
  });
}

function renderChrome() {
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("map.title");
  document.getElementById("t-sub").textContent = t("map.subtitle");
  document.getElementById("q").placeholder = t("map.search");
  document.getElementById("btnFocus").textContent = t("map.focus_btn");
  document.getElementById("btnReset").textContent = t("map.reset");
  document.getElementById("sources").textContent =
    t("map.sources") + " — " + DATA.geo.meta.gov_source + " · " + DATA.geo.meta.city_source
    + " · " + t("map.coast_note") + " · " + t("map.gov_missing");

  const langs = document.getElementById("langs");
  langs.innerHTML = "";
  Object.keys(DATA.langLabels).forEach((code) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.style.marginInlineStart = "6px";
    b.textContent = code.toUpperCase();
    b.setAttribute("aria-pressed", code === lang);
    b.onclick = () => { lang = code; renderChrome(); renderList(DATA.geo.cities, t("map.cities")); };
    langs.appendChild(b);
  });
}

/* ---------- recherche ---------- */
document.getElementById("q").addEventListener("input", (e) => {
  const q = e.target.value.trim().toLowerCase();
  if (!q) { renderList(DATA.geo.cities, t("map.cities")); return; }
  const gov = DATA.geo.governorates.filter((g) =>
    Object.values(g.name).some((n) => n && n.toLowerCase().includes(q)));
  const cities = DATA.geo.cities.filter((c) => c.n.toLowerCase().includes(q)
    || gov.some((g) => g.iso === c.g));
  renderList(cities, q);
});

/* ---------- navigation : glisser, molette, pincement ---------- */
const svgEl = document.getElementById("svg");
let dragging = null;

svgEl.addEventListener("pointerdown", (e) => {
  dragging = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y };
  svgEl.classList.add("drag");
});
addEventListener("pointerup", () => { dragging = null; svgEl.classList.remove("drag"); }, { passive: true });
addEventListener("pointermove", (e) => {
  if (!dragging) return;
  const box = svgEl.getBoundingClientRect();
  view.x = dragging.vx - (e.clientX - dragging.x) * view.w / box.width;
  view.y = dragging.vy - (e.clientY - dragging.y) * view.h / box.height;
  applyView();
}, { passive: true });

function scale(f) {
  const cx = view.x + view.w / 2, cy = view.y + view.h / 2;
  view.w = Math.max(2, Math.min(full.w * 1.4, view.w * f));
  view.h = Math.max(2, Math.min(full.h * 1.4, view.h * f));
  view.x = cx - view.w / 2; view.y = cy - view.h / 2;
  applyView();
}
svgEl.addEventListener("wheel", (e) => { e.preventDefault(); scale(e.deltaY > 0 ? 1.15 : 0.87); });
document.getElementById("zin").onclick = () => scale(0.75);
document.getElementById("zout").onclick = () => scale(1.33);

document.getElementById("btnReset").onclick = () => { view = Object.assign({}, full); applyView(); };
document.getElementById("btnFocus").onclick = () => {
  const c = DATA.geo.cities.find((x) => x.n === SBS.name);
  if (c) selectCity(c);
};

/* ---------- démarrage ---------- */
full = bounds();
const box0 = document.getElementById("map").getBoundingClientRect();
const ratio = (box0.width || 1) / (box0.height || 1);
// le pays est nettement plus haut que large : on cale sur la dimension contraignante
if (full.w / full.h < ratio) {
  const w = full.h * ratio;
  full.x -= (w - full.w) / 2; full.w = w;
} else {
  const h = full.w / ratio;
  full.y -= (h - full.h) / 2; full.h = h;
}
view = Object.assign({}, full);
draw();
applyView();
renderChrome();
renderList(DATA.geo.cities, t("map.cities"));
addEventListener("resize", () => applyView(), { passive: true });
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    out.write_text(TEMPLATE.replace("__DATA__", json.dumps(collect(), ensure_ascii=False)), encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "carte-tunisie.html"
    built = build(target)
    geo = load_json("data/tunisia-geo.json")
    sys.stdout.write(f"HTML carte -> {built}\n")
    sys.stdout.write(f"{len(geo['governorates'])} gouvernorats · {len(geo['cities'])} localites\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
