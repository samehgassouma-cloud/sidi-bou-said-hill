#!/usr/bin/env python3
"""احجز قبل ما توصل — application de réservation en terrasse 3D.

L'utilisateur choisit sa table dans une terrasse en gradins rendue en 3D (prise
électrique, vue, ombre visibles sur le plan), compose sa commande, donne son heure
d'arrivée : l'application calcule à rebours le moment où la préparation doit démarrer
pour que tout soit prêt avant qu'il s'asseye.

Rien n'est envoyé à l'établissement : c'est une maquette fonctionnelle, et la page
le dit à chaque étape.

Lancement :
    python prototype/build_cafe.py
    # puis ouvrir cafe-reservation-3d.html
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
        "venues": load_json("data/venues.json"),
        "backend": load_json("data/backend.json"),
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Réserver avant d'arriver — Sidi Bou Saïd</title>
<style>
  :root { --navy:#0A1628; --deep:#123A5C; --blue:#2E7BB5; --gold:#D4A017; --teal:#00B4D8;
          --paper:#FAF7F0; --muted:#8FA3B5; --line:rgba(255,255,255,.12); }
  * { box-sizing:border-box; }
  html, body { margin:0; height:100%; background:var(--navy); color:#EAF2F9; overflow:hidden;
               font-family:system-ui,-apple-system,"Segoe UI",sans-serif; }
  html[dir="rtl"] body { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }
  .app { display:flex; flex-direction:column; height:100%; }

  header { padding:12px 16px; display:flex; align-items:center; gap:10px; flex-wrap:wrap;
           border-bottom:1px solid var(--line); background:linear-gradient(180deg,#0D1E33,#0A1628); }
  header h1 { font-size:16px; margin:0; }
  header .sub { font-size:10.5px; color:var(--muted); margin-top:2px; }
  .spacer { margin-inline-start:auto; }
  .chip { background:rgba(255,255,255,.09); border:1px solid var(--line); color:#EAF2F9;
          border-radius:14px; padding:7px 12px; font-size:11.5px; cursor:pointer; text-decoration:none; }
  .chip[aria-pressed="true"], .chip.gold { background:var(--gold); color:#22303B; border-color:var(--gold); font-weight:600; }
  .chip.teal { background:var(--teal); color:#062733; border-color:var(--teal); font-weight:600; }
  .chip:disabled { opacity:.45; cursor:not-allowed; }

  .body { flex:1; display:flex; min-height:0; }
  .view { flex:1; position:relative; min-height:220px; background:#0E2438; }
  canvas { position:absolute; inset:0; width:100%; height:100%; display:block; touch-action:none; }
  .fallback { position:absolute; inset:0; display:none; padding:16px; overflow:auto; }
  .fallback.on { display:block; }
  .fbTable { display:inline-block; width:118px; margin:6px; padding:10px; border-radius:14px;
             background:#12293F; border:1px solid var(--line); cursor:pointer; font-size:11.5px; }
  .fbTable[aria-pressed="true"] { border-color:var(--gold); background:#1B3A55; }

  aside { width:340px; max-width:48vw; border-inline-start:1px solid var(--line); background:#0C1D30;
          display:flex; flex-direction:column; }
  .steps { display:flex; border-bottom:1px solid var(--line); }
  .steps button { flex:1; background:none; border:0; color:var(--muted); font-size:11px; padding:10px 4px;
                  cursor:pointer; border-bottom:2px solid transparent; }
  .steps button[aria-selected="true"] { color:var(--gold); border-bottom-color:var(--gold); font-weight:600; }
  .pane { flex:1; overflow-y:auto; padding:12px; }
  .row { display:flex; align-items:center; gap:8px; padding:9px 10px; border-radius:10px; font-size:12px;
         background:rgba(255,255,255,.04); margin-bottom:7px; }
  .row .tag { font-size:9.5px; padding:2px 7px; border-radius:9px; border:1px solid var(--line); color:var(--muted); }
  .row .tag.pw { color:#9DE8F7; border-color:var(--teal); }
  .row .tag.vw { color:#F0D083; border-color:var(--gold); }
  .row.sel { border:1px solid var(--gold); background:rgba(212,160,23,.12); }
  .row button { margin-inline-start:auto; }
  .qty { display:flex; align-items:center; gap:6px; margin-inline-start:auto; }
  .qty button { width:26px; height:26px; border-radius:8px; border:1px solid var(--line);
                background:#12293F; color:#EAF2F9; cursor:pointer; }
  h3 { font-size:11px; letter-spacing:.6px; color:var(--gold); margin:14px 0 8px; }
  .slots { display:flex; flex-wrap:wrap; gap:6px; }
  .warn { background:rgba(212,160,23,.14); border:1px solid var(--gold); color:#F0D083;
          padding:9px 11px; border-radius:11px; font-size:11px; margin-top:10px; }
  .field { display:flex; gap:6px; margin-top:8px; }
  .field input { flex:1; background:#0A1628; border:1px solid var(--line); color:#EAF2F9;
                 border-radius:10px; padding:8px 10px; font-size:12px; outline:none; }
  .code { width:100%; background:#0A1628; border:1px solid var(--line); color:#9DE8F7; border-radius:10px;
          padding:8px; font-size:10.5px; font-family:ui-monospace,monospace; word-break:break-all;
          max-height:76px; overflow:auto; margin-top:6px; }
  .ok { background:rgba(0,180,216,.14); border:1px solid var(--teal); color:#9DE8F7;
        padding:8px 11px; border-radius:11px; font-size:11px; margin-top:8px; }
  .sim { font-size:10px; color:var(--muted); padding:10px 12px; border-top:1px solid var(--line); }

  /* ---- chronologie de la commande ---- */
  .tl { margin-top:10px; border-inline-start:2px solid var(--line); padding-inline-start:14px; }
  .tl .ev { position:relative; padding:8px 0; font-size:12px; }
  .tl .ev::before { content:""; position:absolute; inset-inline-start:-20px; top:13px; width:9px; height:9px;
                    border-radius:50%; background:var(--gold); }
  .tl .ev.now::before { background:var(--teal); }
  .tl .ev b { display:block; font-size:15px; }
  .ticket { background:var(--paper); color:#1F2A33; border-radius:16px; padding:14px 16px; margin-top:12px;
            border:1px solid rgba(212,160,23,.6); }
  .ticket h2 { margin:0 0 4px; font-size:16px; color:var(--deep); }
  .ticket p { margin:3px 0; font-size:12.5px; color:#33424F; }
  .bar { height:8px; border-radius:5px; background:#12293F; overflow:hidden; margin-top:4px; }
  .bar i { display:block; height:100%; background:linear-gradient(90deg,var(--teal),var(--gold)); }
  @media (max-width:860px) {
    .body { flex-direction:column; }
    aside { width:100%; max-width:none; height:52%; border-inline-start:0; border-top:1px solid var(--line); }
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
    <span id="venues"></span>
    <a class="chip" id="back" href="../amal-2/sidi-bou-said-carte.html"></a>
    <span id="langs"></span>
  </header>

  <div class="body">
    <div class="view">
      <canvas id="gl"></canvas>
      <div class="fallback" id="fb"></div>
    </div>
    <aside>
      <div class="steps" id="steps"></div>
      <div class="pane" id="pane"></div>
      <div class="sim" id="t-sim"></div>
    </aside>
  </div>
</div>

<script>
__BACKEND__
</script>
<script>
__CAFE3D__
</script>
<script>
const DATA = __DATA__;
let lang = "fr", venue = DATA.venues.venues[0], step = 0;
let table = null, order = {}, arrivalMin = 30, lead = DATA.venues.meta.ready_lead_default_min;
let gl = null, onlyPower = false;

const t = (k) => DATA.i18n[lang][k] || "\\u00ab" + k + "\\u00bb";
const fmt = (d) => d.toLocaleTimeString(lang === "ar" ? "ar-TN" : lang, { hour: "2-digit", minute: "2-digit" });
const plus = (min) => new Date(Date.now() + min * 60000);

/* ---------- calcul du minutage ----------
   On part de l'heure d'arrivée et on remonte : prêt = arrivée − avance souhaitée,
   début de préparation = prêt − temps de préparation de la commande. */
function timing() {
  const items = Object.keys(order).filter((k) => order[k] > 0);
  const prep = items.length
    ? Math.max.apply(null, items.map((k) => venue.menu.find((m) => m.id === k).prep_min))
      + venue.prep_buffer_min + (items.length - 1) * 2
    : 0;
  const arrival = plus(arrivalMin);
  const ready = new Date(arrival.getTime() - lead * 60000);
  const start = new Date(ready.getTime() - prep * 60000);
  return { prep, arrival, ready, start, tight: start.getTime() < Date.now(), items: items.length };
}

/* ---------- panneaux ---------- */
function tableRow(tb) {
  const row = document.createElement("div");
  row.className = "row" + (table === tb.id ? " sel" : "");
  const n = document.createElement("span");
  n.textContent = t("cafe.table") + " " + tb.id + " · " + tb.seats + " " + t("cafe.seats");
  row.appendChild(n);
  if (tb.power) { const g = document.createElement("span"); g.className = "tag pw"; g.textContent = "⚡"; row.appendChild(g); }
  if (tb.view) { const g = document.createElement("span"); g.className = "tag vw"; g.textContent = "🌊"; row.appendChild(g); }
  const z = document.createElement("span");
  z.className = "tag";
  z.textContent = t("cafe." + tb.zone);
  row.appendChild(z);
  row.onclick = () => { pickTable(tb.id); };
  return row;
}

function paneTables(pane) {
  const filt = document.createElement("button");
  filt.className = "chip";
  filt.textContent = t("cafe.filter_power");
  filt.setAttribute("aria-pressed", String(onlyPower));
  filt.onclick = () => { onlyPower = !onlyPower; render(); };
  pane.appendChild(filt);

  const facts = document.createElement("div");
  facts.className = "row";
  facts.style.display = "block";
  facts.textContent = venue.facts[lang];
  pane.appendChild(facts);

  const note = document.createElement("div");
  note.className = "warn";
  note.textContent = venue.layout_note[lang];
  pane.appendChild(note);

  const list = venue.tables.filter((tb) => !onlyPower || tb.power);
  if (gl) gl.highlight(list.map((tb) => tb.id));
  const h = document.createElement("h3");
  h.textContent = t("cafe.step1");
  pane.appendChild(h);
  list.forEach((tb) => pane.appendChild(tableRow(tb)));
}

function paneOrder(pane) {
  const h = document.createElement("h3");
  h.textContent = t("cafe.order");
  pane.appendChild(h);

  venue.menu.forEach((m) => {
    const row = document.createElement("div");
    row.className = "row";
    const n = document.createElement("span");
    n.textContent = m.name[lang] + " · " + m.prep_min + " min";
    const q = document.createElement("div");
    q.className = "qty";
    const minus = document.createElement("button"); minus.textContent = "−";
    const val = document.createElement("span"); val.textContent = order[m.id] || 0;
    const add = document.createElement("button"); add.textContent = "+";
    minus.onclick = () => { order[m.id] = Math.max(0, (order[m.id] || 0) - 1); render(); };
    add.onclick = () => { order[m.id] = (order[m.id] || 0) + 1; render(); };
    q.append(minus, val, add);
    row.append(n, q);
    pane.appendChild(row);
  });

  const price = document.createElement("div");
  price.className = "warn";
  price.textContent = t("cafe.price_note");
  pane.appendChild(price);

  const h2 = document.createElement("h3");
  h2.textContent = t("cafe.arrival");
  pane.appendChild(h2);
  const slots = document.createElement("div");
  slots.className = "slots";
  [15, 30, 45, 60, 90].forEach((min) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = t("cafe.in_min").replace("%s", min) + " · " + fmt(plus(min));
    b.setAttribute("aria-pressed", String(arrivalMin === min));
    b.onclick = () => { arrivalMin = min; render(); };
    slots.appendChild(b);
  });
  pane.appendChild(slots);

  const h3 = document.createElement("h3");
  h3.textContent = t("cafe.lead");
  pane.appendChild(h3);
  const leads = document.createElement("div");
  leads.className = "slots";
  [0, 5, 15].forEach((min) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = min + " min";
    b.setAttribute("aria-pressed", String(lead === min));
    b.onclick = () => { lead = min; render(); };
    leads.appendChild(b);
  });
  pane.appendChild(leads);

  const tm = timing();
  if (tm.items && tm.tight) {
    const w = document.createElement("div");
    w.className = "warn";
    w.textContent = t("cafe.tight");
    pane.appendChild(w);
  }
}

function paneConfirm(pane) {
  const tm = timing();
  const tb = venue.tables.find((x) => x.id === table);

  const ticket = document.createElement("div");
  ticket.className = "ticket";
  const h = document.createElement("h2");
  h.textContent = venue.name[lang];
  const p1 = document.createElement("p");
  p1.textContent = t("cafe.table") + " " + (tb ? tb.id + " · " + tb.seats + " " + t("cafe.seats")
    + " · " + t("cafe." + tb.zone) : "—");
  const p2 = document.createElement("p");
  const feats = [];
  if (tb && tb.power) feats.push(t("cafe.power"));
  if (tb && tb.view) feats.push(t("cafe.view"));
  if (tb && tb.shade) feats.push(t("cafe.shade"));
  p2.textContent = feats.join(" · ");
  const p3 = document.createElement("p");
  p3.textContent = Object.keys(order).filter((k) => order[k] > 0)
    .map((k) => order[k] + " × " + venue.menu.find((m) => m.id === k).name[lang]).join(" · ")
    || t("cafe.empty_order");
  ticket.append(h, p1, p2, p3);
  pane.appendChild(ticket);

  if (tm.items) {
    const tl = document.createElement("div");
    tl.className = "tl";
    [[t("cafe.prep_at"), tm.start, tm.tight],
     [t("cafe.ready_at"), tm.ready, false],
     [t("cafe.arrive_at"), tm.arrival, false]].forEach(([label, when, warnFlag], i) => {
      const ev = document.createElement("div");
      ev.className = "ev" + (i === 1 ? " now" : "");
      const b = document.createElement("b");
      b.textContent = fmt(when);
      const s = document.createElement("span");
      s.textContent = label + (warnFlag ? " ⚠" : "");
      ev.append(b, s);
      tl.appendChild(ev);
    });
    pane.appendChild(tl);

    const bar = document.createElement("div");
    bar.className = "bar";
    const i = document.createElement("i");
    const total = tm.arrival - Date.now();
    const done = Math.max(0, Math.min(1, (Date.now() - (tm.start - 0)) / (tm.arrival - tm.start)));
    i.style.width = (total > 0 ? done * 100 : 100) + "%";
    bar.appendChild(i);
    pane.appendChild(bar);

    if (tm.tight) {
      const w = document.createElement("div");
      w.className = "warn";
      w.textContent = t("cafe.tight");
      pane.appendChild(w);
    }
  }

  /* ---------- transmission : WhatsApp, canal cuisine, code de secours ---------- */
  const ticketData = {
    v: venue.id, vname: venue.name.fr, table: table,
    items: Object.keys(order).filter((k) => order[k] > 0)
      .map((k) => ({ id: k, q: order[k], n: venue.menu.find((m) => m.id === k).name })),
    start: tm.start.getTime(), ready: tm.ready.getTime(), arrival: tm.arrival.getTime(),
    prep: tm.prep, ts: Date.now()
  };

  function message() {
    const lines = [
      venue.name[lang],
      t("cafe.table") + " " + (tb ? tb.id : "—") + (tb && tb.power ? " ⚡" : ""),
      ticketData.items.map((i) => i.q + " × " + i.n[lang]).join(", "),
      t("cafe.ready_at") + " " + fmt(tm.ready),
      t("cafe.arrive_at") + " " + fmt(tm.arrival)
    ];
    // saut de ligne construit sans échappement : le gabarit traverse deux couches de citation
    return lines.filter(Boolean).join(String.fromCharCode(10));
  }

  if (tm.items && table) {
    const h3 = document.createElement("h3");
    h3.textContent = t("wa.title");
    pane.appendChild(h3);

    const hint = document.createElement("div");
    hint.className = "sim";
    hint.style.padding = "0 0 6px";
    hint.textContent = t("wa.hint");
    pane.appendChild(hint);

    const field = document.createElement("div");
    field.className = "field";
    const input = document.createElement("input");
    input.type = "tel";
    input.placeholder = "+216 XX XXX XXX";
    input.value = venue.phone || "";
    input.oninput = () => { venue.phone = input.value.trim(); };
    const send = document.createElement("button");
    send.className = "chip gold";
    send.textContent = t("wa.send");
    send.onclick = () => {
      const num = (venue.phone || "").replace(/[^0-9]/g, "");
      if (num.length < 8) {
        const w = document.createElement("div");
        w.className = "warn";
        w.textContent = t("wa.missing");
        field.after(w);
        return;
      }
      // deep link WhatsApp : rien n'est envoyé sans que la personne appuie sur « envoyer »
      window.open("https://wa.me/" + num + "?text=" + encodeURIComponent(message()), "_blank");
    };
    field.append(input, send);
    pane.appendChild(field);

    const copy = document.createElement("button");
    copy.className = "chip";
    copy.style.marginTop = "8px";
    copy.textContent = t("wa.copy");
    copy.onclick = () => {
      const txt = message();
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(() => { copy.textContent = t("wa.copied"); });
      else { copy.textContent = t("wa.copied"); }
    };
    pane.appendChild(copy);

    // canal vers l'écran cuisine ouvert dans une autre fenêtre du même navigateur
    const push = document.createElement("button");
    push.className = "chip teal";
    push.style.marginInlineStart = "8px";
    push.textContent = t("kds.open");
    push.onclick = () => {
      publish(ticketData);
      const w = window.open("cuisine-kds.html", "_blank");
      if (!w) {
        const warn = document.createElement("div");
        warn.className = "warn";
        warn.textContent = t("link.same_folder");
        push.after(warn);
      }
    };
    pane.appendChild(push);

    const sent = document.createElement("div");
    sent.className = "ok";
    sent.textContent = t("kds.sent");
    sent.style.display = "none";
    pane.appendChild(sent);
    publish(ticketData, function (mode, err) {
      sent.style.display = "block";
      sent.textContent = mode === "cloud" ? t("be.sent")
        : mode === "error" ? t("be.fail") + " " + err
        : t("kds.sent");
      sent.className = mode === "error" ? "warn" : "ok";
    });

    // ---- connexion serveur : ce qui fait passer les commandes d'un appareil à l'autre
    const bh = document.createElement("h3");
    bh.textContent = t("be.title") + " · " + (backend.mode === "cloud" ? t("be.mode_cloud") : t("be.mode_local"));
    pane.appendChild(bh);

    const bhint = document.createElement("div");
    bhint.className = "sim";
    bhint.style.padding = "0 0 6px";
    bhint.textContent = t("be.hint");
    pane.appendChild(bhint);

    const f1 = document.createElement("div");
    f1.className = "field";
    const uIn = document.createElement("input");
    uIn.placeholder = t("be.url");
    uIn.value = DATA.backend.url || "";
    f1.appendChild(uIn);
    pane.appendChild(f1);

    const f2 = document.createElement("div");
    f2.className = "field";
    const kIn = document.createElement("input");
    kIn.placeholder = t("be.key");
    kIn.value = DATA.backend.anon_key || "";
    const conn = document.createElement("button");
    conn.className = "chip teal";
    conn.textContent = t("be.connect");
    const res = document.createElement("div");
    conn.onclick = function () {
      conn.textContent = t("be.testing");
      backend.connect(uIn.value, kIn.value)
        .then(function () {
          conn.textContent = t("be.connect");
          res.className = "ok";
          res.textContent = t("be.ok");
          render();
        })
        .catch(function (e) {
          conn.textContent = t("be.connect");
          res.className = "warn";
          res.textContent = t("be.fail") + " " + e.message;
        });
    };
    f2.append(kIn, conn);
    pane.append(f2, res);

    const kw = document.createElement("div");
    kw.className = "warn";
    kw.textContent = t("be.warn_key") + " " + t("be.schema");
    pane.appendChild(kw);

    const cl = document.createElement("h3");
    cl.textContent = t("kds.code");
    pane.appendChild(cl);
    const code = document.createElement("div");
    code.className = "code";
    code.textContent = encodeTicket(ticketData);
    code.onclick = () => {
      if (navigator.clipboard) navigator.clipboard.writeText(code.textContent);
    };
    pane.appendChild(code);
  }

  const again = document.createElement("button");
  again.className = "chip gold";
  again.style.marginTop = "12px";
  again.textContent = t("cafe.again");
  again.onclick = () => { order = {}; table = null; step = 0; if (gl) gl.overview(); render(); };
  pane.appendChild(again);
}

/* ---------- transmission sans serveur ----------
   BroadcastChannel relie les fenêtres du même navigateur : c'est suffisant pour une
   démonstration à deux écrans. Le code encodé sert de secours quand le canal n'existe
   pas (autre appareil, navigateur ancien) : on le colle dans l'écran cuisine. */
const backend = window.makeBackend(Object.assign({}, DATA.backend, { channel: DATA.venues.meta.channel }));

function encodeTicket(o) {
  return btoa(unescape(encodeURIComponent(JSON.stringify(o))));
}

function publish(ticket, onSent) {
  // part toujours sur le canal local ; si le serveur est configuré, il est écrit aussi
  backend.send(ticket)
    .then(function (res) { if (onSent) onSent(res.mode); })
    .catch(function (e) { if (onSent) onSent("error", e.message); });
  return true;
}

/* ---------- rendu général ---------- */
function render() {
  document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("cafe.title");
  document.getElementById("t-sub").textContent = t("cafe.sub");
  document.getElementById("t-sim").textContent = t("cafe.sim");
  document.getElementById("back").textContent = t("cafe.back");

  const vs = document.getElementById("venues");
  vs.innerHTML = "";
  DATA.venues.venues.forEach((v) => {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = v.name[lang];
    b.setAttribute("aria-pressed", String(v.id === venue.id));
    b.onclick = () => { venue = v; table = null; order = {}; step = 0; reloadScene(); render(); };
    vs.appendChild(b);
  });

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

  const steps = document.getElementById("steps");
  steps.innerHTML = "";
  ["cafe.step1", "cafe.step2", "cafe.step3"].forEach((key, i) => {
    const b = document.createElement("button");
    b.textContent = t(key);
    b.setAttribute("aria-selected", String(i === step));
    b.disabled = (i > 0 && !table);
    b.onclick = () => { step = i; render(); };
    steps.appendChild(b);
  });

  const pane = document.getElementById("pane");
  pane.innerHTML = "";
  if (step === 0) paneTables(pane);
  else if (step === 1) paneOrder(pane);
  else paneConfirm(pane);

  if (!gl) renderFallback();
}

function pickTable(id) {
  table = id;
  if (gl) gl.select(id);
  if (step === 0) step = 1;
  render();
}

/* ---------- repli sans WebGL : le plan de salle en liste ---------- */
function renderFallback() {
  const fb = document.getElementById("fb");
  fb.classList.add("on");
  fb.innerHTML = "";
  venue.tables.forEach((tb) => {
    const b = document.createElement("div");
    b.className = "fbTable";
    b.setAttribute("aria-pressed", String(table === tb.id));
    b.textContent = tb.id + " · " + tb.seats + (tb.power ? " ⚡" : "") + (tb.view ? " 🌊" : "");
    b.onclick = () => pickTable(tb.id);
    fb.appendChild(b);
  });
}

/* ---------- 3D optionnelle ---------- */
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

function buildScene(THREE) {
  if (gl) { gl.stop(); gl = null; }
  // le canvas garde son contexte WebGL : on le remplace pour repartir d'une scène propre
  const old = document.getElementById("gl");
  const fresh = old.cloneNode(false);
  old.parentNode.replaceChild(fresh, old);
  gl = window.buildCafe(THREE, fresh, {
    tables: venue.tables,
    levels: venue.levels,
    layout: venue.layout,
    onPick: (id) => pickTable(id)
  });
  if (!gl) { renderFallback(); return; }
  document.getElementById("fb").classList.remove("on");
  render();
}

function start3d() {
  loadThree().then(buildScene).catch(() => renderFallback());
}

function reloadScene() {
  if (window.THREE) buildScene(window.THREE);
  else renderFallback();
}

render();
start3d();
setInterval(() => { if (step === 2) render(); }, 30000);
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    cafe_js = (BASE / "ui" / "cafe3d.js").read_text(encoding="utf-8")
    backend_js = (BASE / "ui" / "backend.js").read_text(encoding="utf-8")
    html = (TEMPLATE
            .replace("__BACKEND__", backend_js)
            .replace("__CAFE3D__", cafe_js)
            .replace("__DATA__", json.dumps(collect(), ensure_ascii=False)))
    out.write_text(html, encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "cafe-reservation-3d.html"
    built = build(target)
    v = load_json("data/venues.json")
    sys.stdout.write(f"HTML cafe -> {built}\n")
    sys.stdout.write(f"{len(v['venues'])} lieux · {len(v['venues'][0]['tables'])} tables par salle\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
