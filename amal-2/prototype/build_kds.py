#!/usr/bin/env python3
"""شاشة المطبخ — écran cuisine (KDS).

Reçoit les commandes de l'application de réservation par BroadcastChannel (fenêtres
du même navigateur) ou par collage du code de secours. Les tickets sont triés par
heure de lancement de la préparation, avec compte à rebours et changement d'état.

Aucun serveur, aucune base : c'est une maquette à deux écrans.

Lancement :
    python prototype/build_kds.py
    # puis ouvrir cuisine-kds.html
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
        "channel": load_json("data/venues.json")["meta"]["channel"],
        "backend": load_json("data/backend.json"),
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Écran cuisine — Sidi Bou Saïd</title>
<style>
  :root { --navy:#0A1628; --deep:#123A5C; --gold:#D4A017; --teal:#00B4D8; --red:#C4564F;
          --paper:#FAF7F0; --muted:#8FA3B5; --line:rgba(255,255,255,.12); }
  * { box-sizing:border-box; }
  html, body { margin:0; min-height:100%; background:var(--navy); color:#EAF2F9;
               font-family:system-ui,-apple-system,"Segoe UI",sans-serif; }
  html[dir="rtl"] body { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }

  header { padding:14px 18px; display:flex; align-items:center; gap:10px; flex-wrap:wrap;
           border-bottom:1px solid var(--line); background:linear-gradient(180deg,#0D1E33,#0A1628);
           position:sticky; top:0; z-index:5; }
  header h1 { font-size:18px; margin:0; }
  header .sub { font-size:10.5px; color:var(--muted); margin-top:2px; }
  .clock { font-size:26px; font-variant-numeric:tabular-nums; color:var(--gold); font-weight:600; }
  .spacer { margin-inline-start:auto; }
  .chip { background:rgba(255,255,255,.09); border:1px solid var(--line); color:#EAF2F9;
          border-radius:14px; padding:7px 12px; font-size:11.5px; cursor:pointer; text-decoration:none; }
  .chip[aria-pressed="true"], .chip.gold { background:var(--gold); color:#22303B; border-color:var(--gold); font-weight:600; }
  .chip.teal { background:var(--teal); color:#062733; border-color:var(--teal); font-weight:600; }

  .tools { padding:10px 18px; display:flex; gap:8px; flex-wrap:wrap; align-items:center;
           border-bottom:1px solid var(--line); }
  .tools input { flex:1; min-width:180px; background:#0A1628; border:1px solid var(--line); color:#9DE8F7;
                 border-radius:10px; padding:8px 10px; font-size:11px; font-family:ui-monospace,monospace; }

  .board { display:grid; grid-template-columns:repeat(auto-fill, minmax(250px, 1fr)); gap:12px; padding:16px; }
  .ticket { background:#12293F; border:1px solid var(--line); border-radius:16px; padding:14px 15px;
            border-inline-start:6px solid var(--gold); }
  .ticket.late { border-inline-start-color:var(--red); background:#2A1A22; }
  .ticket.doing { border-inline-start-color:var(--teal); }
  .ticket.ready { border-inline-start-color:#5FBF7E; opacity:.85; }
  .ticket.served { opacity:.45; }
  .ticket h2 { margin:0 0 2px; font-size:15px; }
  .ticket .meta { font-size:10.5px; color:var(--muted); }
  .ticket ul { margin:8px 0; padding-inline-start:18px; font-size:13px; }
  .count { font-size:22px; font-variant-numeric:tabular-nums; margin-top:6px; }
  .count.late { color:#FF9A92; }
  .count.soon { color:var(--gold); }
  .times { font-size:11px; color:var(--muted); margin-top:4px; }
  .acts { display:flex; gap:6px; margin-top:10px; flex-wrap:wrap; }
  .empty { padding:40px 18px; color:var(--muted); font-size:13px; text-align:center; }
  .sim { padding:12px 18px; font-size:10px; color:var(--muted); border-top:1px solid var(--line); }
  .warn { margin:10px 18px; background:rgba(212,160,23,.14); border:1px solid var(--gold); color:#F0D083;
          padding:9px 11px; border-radius:11px; font-size:11px; }
</style>
</head>
<body>
<header>
  <div>
    <h1 id="t-title"></h1>
    <div class="sub" id="t-sub"></div>
  </div>
  <div class="spacer"></div>
  <div class="clock" id="clock"></div>
  <span id="langs"></span>
</header>

<div class="tools">
  <input id="code" placeholder="">
  <button class="chip teal" id="load"></button>
  <button class="chip" id="demo"></button>
  <button class="chip" id="clear"></button>
  <a class="chip" id="back" href="cafe-reservation-3d.html"></a>
</div>
<div class="tools">
  <span class="chip" id="mode" aria-pressed="false"></span>
  <input id="beUrl" placeholder="">
  <input id="beKey" placeholder="">
  <button class="chip teal" id="beConnect"></button>
  <span class="sub" id="sync" style="font-size:10.5px;color:var(--muted)"></span>
</div>
<div id="msg"></div>

<div class="board" id="board"></div>
<div class="empty" id="empty"></div>
<div class="sim" id="t-sim"></div>

<script>
__BACKEND__
</script>
<script>
const DATA = __DATA__;
let lang = "fr";
let tickets = [];   // en mémoire uniquement : rien n'est stocké sur la machine

const t = (k) => DATA.i18n[lang][k] || "\\u00ab" + k + "\\u00bb";
const fmt = (ms) => new Date(ms).toLocaleTimeString(lang === "ar" ? "ar-TN" : lang,
  { hour: "2-digit", minute: "2-digit" });

function countdown(ms) {
  const d = Math.round((ms - Date.now()) / 1000);
  const sign = d < 0 ? "−" : "";
  const a = Math.abs(d);
  return sign + String(Math.floor(a / 60)).padStart(2, "0") + ":" + String(a % 60).padStart(2, "0");
}

/* ---------- réception ---------- */
const backend = window.makeBackend(Object.assign({}, DATA.backend, { channel: DATA.channel }));

backend.subscribe(
  (tk) => addTicket(tk),
  (list) => {
    // le serveur fait foi : on fusionne sans écraser l'état déjà avancé localement
    list.forEach((row) => {
      const known = tickets.find((x) => (x.id && x.id === row.id)
        || (!x.id && x.table === row.table && x.start === row.start));
      if (!known) { row.state = row.state || "todo"; tickets.push(row); }
      else if (known.id && row.state && known.state !== row.state) { known.state = row.state; }
      else if (!known.id) { known.id = row.id; }
    });
    render();
  }
);

function addTicket(tk) {
  if (!tk || !tk.start) return;
  if (tickets.some((x) => x.ts === tk.ts && x.table === tk.table)) return;   // pas de doublon
  tk.state = "todo";
  tickets.push(tk);
  render();
}

function decode(str) {
  try { return JSON.parse(decodeURIComponent(escape(atob(str.trim())))); }
  catch (err) { return null; }
}

/* ---------- rendu ---------- */
function ticketCard(tk, i) {
  const late = tk.state === "todo" && tk.start < Date.now();
  const card = document.createElement("div");
  card.className = "ticket " + tk.state + (late ? " late" : "");

  const h = document.createElement("h2");
  h.textContent = t("cafe.table") + " " + tk.table + " · " + tk.vname;
  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = t("cafe.prep_at") + " " + fmt(tk.start) + " · " + tk.prep + " min";

  const ul = document.createElement("ul");
  tk.items.forEach((it) => {
    const li = document.createElement("li");
    li.textContent = it.q + " × " + (it.n[lang] || it.n.fr);
    ul.appendChild(li);
  });

  const c = document.createElement("div");
  const target = tk.state === "todo" ? tk.start : tk.ready;
  const secs = (target - Date.now()) / 1000;
  c.className = "count" + (secs < 0 ? " late" : secs < 300 ? " soon" : "");
  c.textContent = (tk.state === "todo" ? t("kds.start_in") : t("cafe.ready_at")) + " " + countdown(target);

  const times = document.createElement("div");
  times.className = "times";
  times.textContent = t("cafe.ready_at") + " " + fmt(tk.ready) + " · " + t("cafe.arrive_at") + " " + fmt(tk.arrival);

  const acts = document.createElement("div");
  acts.className = "acts";
  const flow = [["todo", "kds.doing"], ["doing", "kds.ready"], ["ready", "kds.served"]];
  flow.forEach(([from, label]) => {
    if (tk.state !== from) return;
    const b = document.createElement("button");
    b.className = "chip gold";
    b.textContent = t(label);
    b.onclick = () => {
      tk.state = from === "todo" ? "doing" : from === "doing" ? "ready" : "served";
      backend.setState(tk.id, tk.state);   // sans effet en mode local
      render();
    };
    acts.appendChild(b);
  });
  if (tk.state === "served") {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = "✕";
    b.onclick = () => { tickets.splice(i, 1); render(); };
    acts.appendChild(b);
  }

  card.append(h, meta, ul, c, times, acts);
  return card;
}

function render() {
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("kds.title");
  document.getElementById("t-sub").textContent = t("kds.sub");
  document.getElementById("t-sim").textContent =
    (backend.mode === "cloud" ? t("be.warn_key") : t("kds.sim")) + " " + t("be.schema");
  document.getElementById("code").placeholder = t("kds.paste");
  document.getElementById("load").textContent = t("kds.load");
  document.getElementById("demo").textContent = t("kds.demo");
  document.getElementById("clear").textContent = t("kds.clear");
  document.getElementById("back").textContent = t("cafe.back");
  document.getElementById("beUrl").placeholder = t("be.url");
  document.getElementById("beKey").placeholder = t("be.key");
  document.getElementById("beConnect").textContent = t("be.connect");
  const modeEl = document.getElementById("mode");
  modeEl.textContent = backend.mode === "cloud" ? t("be.mode_cloud") : t("be.mode_local");
  modeEl.setAttribute("aria-pressed", String(backend.mode === "cloud"));
  document.getElementById("sync").textContent = backend.lastSync
    ? t("be.synced") + " " + fmt(backend.lastSync) : "";
  document.getElementById("clock").textContent = fmt(Date.now());

  const langs = document.getElementById("langs");
  langs.innerHTML = "";
  Object.keys(DATA.langLabels).forEach((code) => {
    const b = document.createElement("button");
    b.className = "chip"; b.style.marginInlineStart = "6px";
    b.textContent = code.toUpperCase();
    b.setAttribute("aria-pressed", code === lang);
    b.onclick = () => { lang = code; render(); };
    langs.appendChild(b);
  });

  // tri : ce qui doit partir en cuisine en premier arrive en premier
  const order = { todo: 0, doing: 1, ready: 2, served: 3 };
  const sorted = tickets.slice().sort((a, b) =>
    (order[a.state] - order[b.state]) || (a.start - b.start));

  const board = document.getElementById("board");
  board.innerHTML = "";
  sorted.forEach((tk, i) => board.appendChild(ticketCard(tk, tickets.indexOf(tk))));
  document.getElementById("empty").textContent = tickets.length ? "" : t("kds.waiting");
}

/* ---------- outils ---------- */
document.getElementById("load").onclick = () => {
  const raw = document.getElementById("code").value;
  const tk = decode(raw);
  const msg = document.getElementById("msg");
  msg.innerHTML = "";
  if (!tk) {
    const w = document.createElement("div");
    w.className = "warn";
    w.textContent = t("kds.bad_code");
    msg.appendChild(w);
    return;
  }
  addTicket(tk);
  document.getElementById("code").value = "";
};

document.getElementById("demo").onclick = () => {
  const now = Date.now();
  addTicket({
    v: "nattes", vname: "Café des Nattes", table: "T07",
    items: [{ id: "m1", q: 2, n: { ar: "قهوة عربي", fr: "Café arabe", en: "Arabic coffee" } },
            { id: "m4", q: 1, n: { ar: "بمبالوني", fr: "Bambalouni", en: "Bambalouni" } }],
    prep: 11, start: now + 3 * 60000, ready: now + 14 * 60000, arrival: now + 29 * 60000, ts: now
  });
};

document.getElementById("clear").onclick = () => { tickets = []; render(); };

document.getElementById("beConnect").onclick = () => {
  const btn = document.getElementById("beConnect");
  const msg = document.getElementById("msg");
  btn.textContent = t("be.testing");
  msg.innerHTML = "";
  backend.connect(document.getElementById("beUrl").value, document.getElementById("beKey").value)
    .then(() => backend.fetchRecent())
    .then((list) => {
      list.forEach((row) => { if (!tickets.some((x) => x.id === row.id)) tickets.push(row); });
      const ok = document.createElement("div");
      ok.className = "warn";
      ok.style.borderColor = "var(--teal)";
      ok.style.color = "#9DE8F7";
      ok.textContent = t("be.ok");
      msg.appendChild(ok);
      render();
    })
    .catch((e) => {
      const w = document.createElement("div");
      w.className = "warn";
      w.textContent = t("be.fail") + " " + e.message;
      msg.appendChild(w);
      render();
    });
};

render();
setInterval(render, 1000);
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    backend_js = (BASE / "ui" / "backend.js").read_text(encoding="utf-8")
    html = (TEMPLATE
            .replace("__BACKEND__", backend_js)
            .replace("__DATA__", json.dumps(collect(), ensure_ascii=False)))
    out.write_text(html, encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "cuisine-kds.html"
    built = build(target)
    sys.stdout.write(f"HTML KDS -> {built}\n")
    sys.stdout.write(f"canal: {collect()['channel']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
