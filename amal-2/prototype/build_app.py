#!/usr/bin/env python3
"""رفيق سيدي بوسعيد — générateur du prototype.

Le prototype est une application HTML autonome, produite par ce script à partir
des traductions (i18n/) et des données marquées (data/). Aucun texte visible
n'est écrit dans le code : tout vient des fichiers JSON.

Lancement :
    python prototype/build_app.py
    # puis ouvrir refek-sidi-bou-said.html
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
    """Rassemble tout ce que la page a besoin de connaître."""
    return {
        "i18n": {lang: load_json(f"i18n/{lang}.json") for lang in LANGS},
        "knowledge": load_json("data/knowledge.json"),
        "events": load_json("data/events.json"),
        "suggestions": load_json("data/suggestions.json"),
        "langLabels": LANG_LABELS,
    }


TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rafik Sidi Bou Said</title>
<style>
  :root {
    --blue-deep:#123A5C; --blue:#2E7BB5; --gold:#C9A227; --gold-soft:#F6EEDA;
    --surface:#FAF7F0; --user:#E9EBEE; --ink:#1F2A33; --muted:#5A6570;
    --radius:18px;
  }
  * { box-sizing:border-box; }
  body {
    margin:0; background:#0E2438; min-height:100vh;
    display:flex; align-items:center; justify-content:center; padding:24px 12px;
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif;
  }
  .phone {
    width:420px; max-width:100%; height:900px; max-height:94vh; background:var(--surface);
    border-radius:34px; overflow:hidden; display:flex; flex-direction:column;
    box-shadow:0 30px 70px rgba(0,0,0,.45); position:relative;
  }
  header { background:linear-gradient(135deg,var(--blue-deep),var(--blue)); color:#fff; padding:16px 20px 14px;
           border-bottom:4px solid var(--gold); position:relative; overflow:hidden; }
  header .arches { position:absolute; inset:0; opacity:.18; }
  .idrow { display:flex; align-items:center; gap:12px; position:relative; }
  .avatar { width:48px; height:48px; border-radius:50%; background:var(--gold-soft);
            border:2px solid var(--gold); flex:0 0 auto; }
  h1 { font-size:18px; margin:0; letter-spacing:.3px; }
  .sub { font-size:11px; color:#D8E6F2; margin-top:2px; }
  .tag { font-size:11px; color:#E3C567; margin-top:2px; }
  .langs { display:flex; gap:6px; margin-inline-start:auto; }
  .langs button { background:rgba(255,255,255,.16); color:#fff; border:0; border-radius:14px;
                  padding:6px 10px; font-size:11px; cursor:pointer; }
  .langs button[aria-pressed="true"] { background:var(--gold); color:#22303B; font-weight:600; }
  .unesco { background:var(--gold-soft); color:#7A5C10; font-size:11px; padding:8px 20px; }
  .tabs { display:flex; background:#fff; border-bottom:1px solid #E4DECF; }
  .tabs button { flex:1; border:0; background:none; padding:10px 4px; font-size:12px; color:var(--muted);
                 cursor:pointer; border-bottom:2px solid transparent; }
  .tabs button[aria-selected="true"] { color:var(--blue-deep); border-bottom-color:var(--gold); font-weight:600; }
  main { flex:1; overflow-y:auto; padding:16px; background-image:
          radial-gradient(circle at 20px 20px, rgba(201,162,39,.18) 2px, transparent 2px);
          background-size:56px 56px; }
  .msg { display:flex; margin-bottom:12px; }
  .msg.user { justify-content:flex-end; }
  .bubble { max-width:82%; padding:12px 14px; border-radius:var(--radius); font-size:13.5px; line-height:1.55; }
  .msg.ai .bubble { background:linear-gradient(135deg,#EAF2F9,#F6EEDA); border:1px solid rgba(201,162,39,.55);
                    color:var(--blue-deep); border-start-start-radius:6px; }
  .msg.user .bubble { background:var(--user); color:var(--ink); border-end-end-radius:6px; }
  .badge { display:inline-block; margin-top:8px; font-size:10.5px; padding:4px 10px; border-radius:12px; }
  .badge.warn { background:#FFF3D6; color:#8A6A12; border:1px solid var(--gold); }
  .badge.ok { background:#E7F1F8; color:#1B5C86; border:1px solid var(--blue); }
  .src { display:block; margin-top:6px; font-size:10.5px; color:var(--muted); }
  .chips { display:flex; flex-wrap:wrap; gap:8px; margin:4px 0 14px; }
  .chips button { background:#fff; border:1px solid #D9D2C2; border-radius:16px; padding:7px 12px;
                  font-size:11.5px; color:var(--blue-deep); cursor:pointer; }
  .chips-label { font-size:11px; color:var(--muted); margin-bottom:6px; }
  .card { background:#fff; border:1px solid #E4DECF; border-radius:var(--radius); padding:14px 16px;
          margin-bottom:12px; border-inline-start:6px solid var(--gold); }
  .card h3 { margin:0 0 4px; font-size:14px; color:var(--blue-deep); }
  .card p { margin:2px 0; font-size:12px; color:var(--muted); }
  .maplike { height:150px; border-radius:var(--radius); margin-bottom:12px;
             background:linear-gradient(#BFD9EC,#8FC0DF); position:relative; overflow:hidden; }
  .maplike .land { position:absolute; inset:auto 0 0 0; height:64px; background:#EFE7D6; border-top:2px solid var(--gold); }
  .maplike .note { position:absolute; inset-inline-start:10px; bottom:10px; background:rgba(255,255,255,.92);
                   font-size:10px; color:var(--muted); padding:4px 10px; border-radius:12px; }
  footer { background:#fff; border-top:1px solid #E4DECF; padding:12px 14px 0; }
  .composer { display:flex; align-items:center; gap:8px; background:#F2F4F6; border:1px solid #D5DCE3;
              border-radius:24px; padding:6px 8px; }
  .composer input { flex:1; border:0; background:none; font-size:13px; padding:8px; color:var(--ink); outline:none; }
  .composer button { border:0; border-radius:50%; width:38px; height:38px; cursor:pointer; font-size:15px; }
  .mic { background:none; color:var(--blue-deep); }
  .send { background:var(--gold); color:#fff; }
  nav { display:flex; background:var(--blue-deep); margin-top:12px; }
  nav button { flex:1; background:none; border:0; color:#D8E6F2; font-size:10px; padding:9px 0 11px; cursor:pointer; }
  nav button[aria-current="page"] { color:#E3C567; font-weight:600; }
  nav .ico { display:block; font-size:15px; margin-bottom:2px; }
  [dir="rtl"] .msg.ai .bubble { border-start-start-radius:var(--radius); border-start-end-radius:6px; }
  [dir="rtl"] body, [dir="rtl"] .phone { font-family:"Noto Naskh Arabic","Amiri",system-ui,serif; }
</style>
</head>
<body>
<div class="phone" id="phone">
  <header>
    <svg class="arches" viewBox="0 0 420 110" preserveAspectRatio="none" aria-hidden="true">
      <g fill="none" stroke="#fff" stroke-width="1.5">
        <path d="M30 110 V60 a30 30 0 0 1 60 0 V110"/>
        <path d="M330 110 V60 a30 30 0 0 1 60 0 V110"/>
      </g>
    </svg>
    <div class="idrow">
      <svg class="avatar" viewBox="0 0 48 48" role="img" aria-label="AI guide">
        <circle cx="24" cy="24" r="23" fill="#F6EEDA"/>
        <path d="M12 36 v-12 a12 12 0 0 1 24 0 v12 z" fill="#2E7BB5"/>
        <path d="M19 36 v-9 a5 5 0 0 1 10 0 v9 z" fill="#F6EEDA"/>
        <circle cx="24" cy="12" r="3" fill="#C9A227"/>
      </svg>
      <div>
        <h1 id="t-title"></h1>
        <div class="sub" id="t-sub"></div>
        <div class="tag" id="t-tag"></div>
      </div>
      <div class="langs" id="langs"></div>
    </div>
  </header>
  <div class="unesco" id="t-unesco"></div>
  <div class="tabs" id="tabs"></div>
  <main id="view"></main>
  <footer>
    <div class="composer">
      <button class="mic" id="mic" title="">&#127908;</button>
      <input id="input" type="text">
      <button class="send" id="send" title="">&#10148;</button>
    </div>
    <nav id="nav"></nav>
  </footer>
</div>
<script>
const DATA = __DATA__;
let lang = "fr";
let tab = "chat";
let thread = [];

const t = (key) => DATA.i18n[lang][key] || "\\u00ab" + key + "\\u00bb";
const isRTL = () => lang === "ar";

function renderShell() {
  document.documentElement.setAttribute("dir", isRTL() ? "rtl" : "ltr");
  document.documentElement.setAttribute("lang", lang);
  document.getElementById("t-title").textContent = t("app.title");
  document.getElementById("t-sub").textContent = t("app.subtitle");
  document.getElementById("t-tag").textContent = t("app.tagline");
  document.getElementById("t-unesco").textContent = t("app.badge_unesco");
  document.getElementById("input").placeholder = t("chat.placeholder");
  document.getElementById("send").title = t("chat.send");
  document.getElementById("mic").title = t("chat.voice");

  const langs = document.getElementById("langs");
  langs.innerHTML = "";
  for (const code of Object.keys(DATA.langLabels)) {
    const b = document.createElement("button");
    b.textContent = code.toUpperCase();
    b.setAttribute("aria-pressed", code === lang);
    b.onclick = () => { lang = code; thread = []; renderShell(); renderView(); };
    langs.appendChild(b);
  }

  const tabs = document.getElementById("tabs");
  tabs.innerHTML = "";
  for (const [id, key] of [["chat", "nav.chat"], ["events", "nav.events"]]) {
    const b = document.createElement("button");
    b.textContent = t(key);
    b.setAttribute("aria-selected", id === tab);
    b.onclick = () => { tab = id; renderShell(); renderView(); };
    tabs.appendChild(b);
  }

  const nav = document.getElementById("nav");
  nav.innerHTML = "";
  const items = [["nav.home", "\\u2302"], ["nav.events", "\\u25A6"], ["nav.chat", "\\u2709"], ["nav.profile", "\\u25CB"]];
  const ordered = isRTL() ? items.slice().reverse() : items;
  for (const [key, ico] of ordered) {
    const b = document.createElement("button");
    b.innerHTML = '<span class="ico">' + ico + "</span>" + t(key);
    if ((key === "nav.chat" && tab === "chat") || (key === "nav.events" && tab === "events")) {
      b.setAttribute("aria-current", "page");
    }
    b.onclick = () => { tab = key === "nav.events" ? "events" : "chat"; renderShell(); renderView(); };
    nav.appendChild(b);
  }
}

function bubble(who, text, status) {
  const wrap = document.createElement("div");
  wrap.className = "msg " + who;
  const b = document.createElement("div");
  b.className = "bubble";
  b.textContent = text;
  if (status) {
    const badge = document.createElement("span");
    badge.className = "badge " + (status.verified ? "ok" : "warn");
    badge.textContent = status.verified ? t("common.verified") : t("common.to_verify");
    b.appendChild(badge);
    if (status.source) {
      const s = document.createElement("span");
      s.className = "src";
      s.textContent = t("common.source") + " · " + status.source;
      b.appendChild(s);
    }
  }
  wrap.appendChild(b);
  return wrap;
}

function answerFor(query) {
  const q = query.toLowerCase();
  for (const entry of DATA.knowledge) {
    if ((entry.keywords[lang] || []).some(k => q.includes(k.toLowerCase()))) {
      return { text: entry.answer[lang], verified: entry.verified, source: entry.source };
    }
  }
  const eventWords = { ar: ["برنامج", "فعاليات", "ورشة", "معرض"], fr: ["programme", "événement", "atelier", "expo"], en: ["event", "programme", "program", "workshop", "expo"] };
  if ((eventWords[lang] || []).some(k => q.includes(k))) {
    const ev = DATA.events[0];
    return { text: ev.title[lang] + " — " + ev.when[lang] + " · " + ev.place[lang], verified: false, source: "" };
  }
  return { text: t("empty.no_results"), verified: false, source: "" };
}

function ask(query) {
  thread.push({ who: "user", text: query });
  const a = answerFor(query);
  thread.push({ who: "ai", text: a.text, status: { verified: a.verified, source: a.source } });
  renderView();
}

function renderChat(view) {
  view.appendChild(bubble("ai", t("chat.greeting")));
  const label = document.createElement("div");
  label.className = "chips-label";
  label.textContent = t("chat.suggestions");
  view.appendChild(label);
  const chips = document.createElement("div");
  chips.className = "chips";
  for (const s of DATA.suggestions) {
    const b = document.createElement("button");
    b.textContent = s.label[lang];
    b.onclick = () => ask(s.query[lang]);
    chips.appendChild(b);
  }
  view.appendChild(chips);
  for (const m of thread) view.appendChild(bubble(m.who, m.text, m.status));
}

function renderEvents(view) {
  const map = document.createElement("div");
  map.className = "maplike";
  map.innerHTML = '<div class="land"></div><div class="note">' + t("events.map_note") + "</div>";
  view.appendChild(map);
  for (const ev of DATA.events) {
    const c = document.createElement("div");
    c.className = "card";
    const h = document.createElement("h3");
    h.textContent = ev.title[lang];
    const when = document.createElement("p");
    when.textContent = ev.when[lang] + " · " + ev.place[lang];
    const badge = document.createElement("span");
    badge.className = "badge " + (ev.verified ? "ok" : "warn");
    badge.textContent = ev.verified ? t("common.verified") : t("common.to_verify");
    c.append(h, when, badge);
    view.appendChild(c);
  }
}

function renderView() {
  const view = document.getElementById("view");
  view.innerHTML = "";
  view.scrollTop = 0;
  if (tab === "chat") renderChat(view); else renderEvents(view);
  view.scrollTop = view.scrollHeight;
}

document.getElementById("send").onclick = () => {
  const input = document.getElementById("input");
  const v = input.value.trim();
  if (!v) return;
  input.value = "";
  tab = "chat";
  renderShell();
  ask(v);
};
document.getElementById("input").addEventListener("keydown", (e) => {
  if (e.key === "Enter") document.getElementById("send").click();
});
document.getElementById("mic").onclick = () => {
  thread.push({ who: "ai", text: t("chat.voice_demo"), status: { verified: false, source: "" } });
  renderView();
};

renderShell();
renderView();
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    payload = json.dumps(collect(), ensure_ascii=False)
    out.write_text(TEMPLATE.replace("__DATA__", payload), encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "refek-sidi-bou-said.html"
    built = build(target)
    verified = sum(1 for e in load_json("data/knowledge.json") if e["verified"])
    total = len(load_json("data/knowledge.json")) + len(load_json("data/events.json"))
    sys.stdout.write(f"HTML -> {built}\n")
    sys.stdout.write(f"{verified} fiches verifiees / {total} enregistrements\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
