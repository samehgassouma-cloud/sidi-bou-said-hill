#!/usr/bin/env python3
"""هضبة سيدي بوسعيد — التوعية والتحليل الجيوتقني الأولي.

Deux volets dans une page autonome et trilingue (AR/FR/EN, RTL) :

  1. Sensibilisation — signes de danger, gestes à avoir, suivi officiel 2026.
  2. Outil géotechnique — méthode de Bishop simplifiée, cercles de glissement,
     recherche automatique du cercle critique, vue 3D (Three.js r128) avec repli
     canvas 2D quand WebGL ou le CDN manquent.

Les valeurs par défaut de `data/defaults.json` sont des EXEMPLES. Les résultats
sont indicatifs : ils ne remplacent pas l'étude géotechnique de terrain et ne
constituent l'évaluation officielle d'aucun bâtiment ni d'aucun site.

Lancement :
    python prototype/build_landslide.py
    # puis ouvrir sidi-bou-said-landslide.html
"""
from __future__ import annotations

import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
LANGS = ("ar", "fr", "en")
FIELD_IDS = ("H", "beta", "zw", "q", "qd", "qB", "kh")


def load_json(rel: str):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))


def collect() -> dict:
    i18n = {lang: load_json(f"i18n/{lang}.json") for lang in LANGS}
    keys = {lang: set(d) for lang, d in i18n.items()}
    if len(set(map(frozenset, keys.values()))) != 1:
        missing = {l: sorted(set().union(*keys.values()) - k) for l, k in keys.items()}
        raise SystemExit(f"i18n incomplet · ترجمات ناقصة : {missing}")
    return {"i18n": i18n, "defaults": load_json("data/defaults.json")}


def field_attrs(field: dict) -> str:
    order = ("value", "min", "max", "step")
    return " ".join(f'{k}="{field[k]}"' for k in order if k in field)


TEMPLATE = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<!-- صفحة مُولَّدة · page générée · generated page : python prototype/build_landslide.py -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>هضبة سيدي بوسعيد — التوعية والتحليل الجيوتقني الأولي</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;500;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#F6F8FA;--ink:#12304A;--muted:#4F6577;--blue:#1F5FA8;--soft:#DCE8F5;--ochre:#B98A52;--line:#C9D6E2;--card:#FFF;
--ok:#3F7A3A;--okb:#E3F0DF;--warn:#8A5E00;--warnb:#FBF0D4;--bad:#A8285F;--badb:#F8DDE8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#0F1C27;--ink:#E6EEF5;--muted:#9FB2C2;--blue:#6FA6E6;--soft:#1A3550;--line:#2A3F52;--card:#152636;--ok:#8CCB84;--okb:#1B3320;--warn:#F0C35A;--warnb:#3A2F12;--bad:#F08AB5;--badb:#3D1A2A}}
:root[data-theme="dark"]{--bg:#0F1C27;--ink:#E6EEF5;--muted:#9FB2C2;--blue:#6FA6E6;--soft:#1A3550;--line:#2A3F52;--card:#152636;--ok:#8CCB84;--okb:#1B3320;--warn:#F0C35A;--warnb:#3A2F12;--bad:#F08AB5;--badb:#3D1A2A}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans Arabic","Segoe UI",Tahoma,Arial,sans-serif;line-height:1.6}
.wrap{max-width:1180px;margin:0 auto;padding:18px 16px 30px}
header{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:flex-start}
h1{margin:0;font-size:clamp(1.3rem,3vw,1.9rem);color:var(--blue)}
.sub{margin:4px 0 0;color:var(--muted);max-width:64ch}
.seg{display:flex;border:1.5px solid var(--blue);border-radius:999px;overflow:hidden}
.seg button{border:0;background:none;color:var(--blue);font:inherit;font-weight:500;padding:6px 13px;cursor:pointer}
.seg button[aria-pressed="true"],.seg button[aria-selected="true"]{background:var(--blue);color:var(--bg)}
.tabs{margin:18px 0 14px;width:max-content;max-width:100%}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:14px}
h2{font-size:1.15rem;margin:0 0 10px}
h3{font-size:1rem;margin:14px 0 6px}
.cols{display:grid;gap:14px}
@media(min-width:820px){.cols{grid-template-columns:1fr 1fr}}
ul.clean{margin:0;padding-inline-start:1.2em}
ul.clean li{margin:4px 0}
.call{display:flex;flex-wrap:wrap;gap:12px;align-items:center;background:var(--badb);color:var(--bad);border-radius:12px;padding:14px 16px;margin-bottom:14px}
.call strong{font-size:2rem;line-height:1;direction:ltr}
.tl{list-style:none;margin:0;padding:0}
.tl li{border-inline-start:3px solid var(--ochre);padding:2px 12px 8px;margin-inline-start:4px}
.tl b{display:block;color:var(--blue)}
.small{font-size:.86rem;color:var(--muted)}
.banner{background:var(--warnb);color:var(--warn);border-radius:12px;padding:12px 16px;margin-bottom:14px;font-weight:500}
.eng{display:grid;gap:14px}
@media(min-width:960px){.eng{grid-template-columns:360px 1fr}}
.f{display:grid;grid-template-columns:1fr 92px;gap:6px 10px;align-items:center;font-size:.92rem}
input[type=number]{width:100%;font:inherit;padding:5px 7px;border:1px solid var(--line);border-radius:7px;background:var(--bg);color:var(--ink);direction:ltr}
.tbl{width:100%;border-collapse:collapse;font-size:.88rem}
.tbl th,.tbl td{padding:4px;text-align:center;border-bottom:1px solid var(--line)}
.tbl input{min-width:56px}
.scroll{overflow-x:auto}
.go{width:100%;margin-top:12px;padding:11px;border:0;border-radius:8px;background:var(--blue);color:var(--bg);font:inherit;font-weight:700;cursor:pointer}
.go:disabled{opacity:.5}
canvas{display:block;width:100%;background:var(--bg);border-radius:10px}
.res{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}
.kpi{border-radius:10px;padding:10px 12px}
.kpi span{display:block;font-size:.85rem}
.kpi strong{font-size:1.9rem;direction:ltr;display:inline-block;line-height:1.2}
.ok{background:var(--okb);color:var(--ok)}.warn{background:var(--warnb);color:var(--warn)}.bad{background:var(--badb);color:var(--bad)}
.err{color:var(--bad);font-weight:500;min-height:1.2em}
details summary{cursor:pointer;font-weight:500}
button:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid var(--ochre);outline-offset:2px}
.eq{direction:ltr;text-align:center;font-weight:700;background:var(--soft);border-radius:8px;padding:8px;overflow-x:auto;white-space:nowrap}
footer{text-align:center;color:var(--muted);font-size:.9rem;margin-top:18px}
#v3{position:relative;border-radius:12px;overflow:hidden;background:linear-gradient(#8EC3EA,#E4F1FA 60%,#1C5A86 60%);min-height:220px;direction:ltr}
#v3 canvas{display:block;width:100%;border-radius:0;background:none}
#v3.nogl{min-height:260px;display:flex;align-items:center;justify-content:center}
#v3msg{position:absolute;inset:auto 16px 16px;margin:0;background:rgba(255,255,255,.92);color:#12304A;border-radius:10px;padding:12px;font-weight:500;text-align:center}
.hud{position:absolute;top:10px;left:10px;display:flex;gap:8px;flex-wrap:wrap;pointer-events:none}
.hud div{background:rgba(10,22,40,.78);color:#fff;border-radius:10px;padding:6px 10px;font-size:.8rem;border:1px solid rgba(212,160,23,.6)}
.hud span{display:block;opacity:.8}.hud b{font-size:1.35rem;direction:ltr;display:inline-block}
.cok{color:#8CE08A}.cwarn{color:#F5C74E}.cbad{color:#FF8DB8}
.wm{position:absolute;top:12px;right:12px;background:rgba(255,255,255,.8);color:#4F6577;font-size:.75rem;border-radius:6px;padding:2px 8px;pointer-events:none}
.zoom{position:absolute;bottom:10px;right:10px;display:flex;flex-direction:column;gap:6px}
.zoom button{width:38px;height:38px;border-radius:50%;border:0;background:rgba(10,22,40,.78);color:#fff;font-size:1.3rem;cursor:pointer}
@media(max-width:600px){.wm{top:auto;bottom:12px;left:12px;right:auto}}
.toggles{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.toggles label{display:flex;align-items:center;gap:5px;background:var(--soft);border-radius:999px;padding:4px 11px;font-size:.86rem;cursor:pointer}
.toggles input{accent-color:var(--blue)}
.insp{margin-top:10px}.insp label{font-weight:500;font-size:.92rem}.insp output{direction:ltr;color:var(--blue);font-weight:700}
.insp input{width:100%;accent-color:#D4A017}
#s3d{position:relative;border-radius:12px;overflow:hidden;background:#0A1628;min-height:160px}
#s3d canvas{display:block;width:100%;border-radius:0}
.busy{position:absolute;inset:0;background:rgba(10,22,40,.35);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.st3{font-weight:500;min-height:1.4em;margin:10px 0 0}
.row3{display:flex;gap:10px}.row3 .go{margin-top:8px}
.go.alt{background:var(--soft);color:var(--ink);flex:0 0 38%}
.legend{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.88rem}
.legend i{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:-2px;margin-inline-end:6px}
[hidden]{display:none!important}
.eng>*,.cols>*{min-width:0}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div><h1 data-i="title"></h1><p class="sub" data-i="sub"></p></div>
  <div class="seg" role="group" aria-label="Language">
    <button data-l="ar" aria-pressed="true">العربية</button><button data-l="fr" aria-pressed="false">Français</button><button data-l="en" aria-pressed="false">English</button>
  </div>
</header>
<div class="seg tabs" role="tablist">
  <button role="tab" id="t1" aria-selected="true" aria-controls="p1" data-i="tab1"></button>
  <button role="tab" id="t2" aria-selected="false" aria-controls="p2" data-i="tab2"></button>
</div>

<!-- ============ AWARENESS ============ -->
<section id="p1" role="tabpanel" aria-labelledby="t1">
  <div class="call"><strong>198</strong><div><b data-i="callT"></b><div data-i="callD"></div></div></div>
  <div class="cols">
    <div class="card"><h2 data-i="signsT"></h2><ul class="clean" data-list="signs"></ul></div>
    <div class="card"><h2 data-i="actT"></h2><ul class="clean" data-list="acts"></ul></div>
  </div>
  <div class="cols">
    <div class="card"><h2 data-i="causeT"></h2><ul class="clean" data-list="causes"></ul></div>
    <div class="card"><h2 data-i="tlT"></h2><ul class="tl" data-tl="tl"></ul><p class="small" data-i="src"></p></div>
  </div>
</section>

<!-- ============ ENGINEERING ============ -->
<section id="p2" role="tabpanel" aria-labelledby="t2" hidden>
  <div class="banner" data-i="warnEng"></div>
  <div class="eng">
    <div class="card">
      <h2 data-i="inT"></h2>
      <h3 data-i="geoT"></h3>
      <div class="f">
        <label for="H" data-i="iH"></label><input type="number" id="H" __IN_H__>
        <label for="beta" data-i="iB"></label><input type="number" id="beta" __IN_BETA__>
        <label for="zw" data-i="iZw"></label><input type="number" id="zw" __IN_ZW__>
      </div>
      <p class="small" data-i="zwNote"></p>
      <h3 data-i="layT"></h3>
      <div class="scroll"><table class="tbl">
        <thead><tr><th></th><th data-i="cBot"></th><th>γ<br>kN/m³</th><th>c′<br>kPa</th><th>φ′<br>°</th></tr></thead>
        <tbody id="lay"></tbody>
      </table></div>
      <p class="small" data-i="layNote"></p>
      <h3 data-i="loadT"></h3>
      <div class="f">
        <label for="q" data-i="iQ"></label><input type="number" id="q" __IN_Q__>
        <label for="qd" data-i="iQd"></label><input type="number" id="qd" __IN_QD__>
        <label for="qB" data-i="iQB"></label><input type="number" id="qB" __IN_QB__>
        <label for="kh" data-i="iKh"></label><input type="number" id="kh" __IN_KH__>
      </div>
      <div class="err" id="err" role="alert"></div>
      <button class="go" id="run" data-i="run"></button>
    </div>

    <div>
      <div class="card">
        <h2 data-i="outT"></h2>
        <div id="v3" role="img" aria-label="3D slope model with critical slip circle">
          <div class="hud">
            <div><span data-i="fsS"></span><b id="h3f">—</b></div>
            <div><span data-i="hudE"></span><b id="h3e">—</b></div>
            <div><span data-i="hudW"></span><b id="h3w">—</b></div>
          </div>
          <div class="wm" data-i="wm"></div>
          <div class="zoom"><button id="zin" aria-label="Zoom in">+</button><button id="zout" aria-label="Zoom out">−</button></div>
          <div class="busy" id="busy" hidden></div>
          <p id="v3msg" hidden></p>
        </div>
        <canvas id="cv" hidden role="img" aria-label="Slope section with critical slip circle"></canvas>
        <div class="toggles" id="tgl">
          <label><input type="checkbox" data-g="grid" checked><span data-i="tgGrid"></span></label>
          <label><input type="checkbox" data-g="slices" checked><span data-i="tgSl"></span></label>
          <label><input type="checkbox" data-g="water" checked><span data-i="tgW"></span></label>
          <label><input type="checkbox" data-g="houses" checked><span data-i="tgH"></span></label>
          <label><input type="checkbox" data-g="labels" checked><span data-i="tgLb"></span></label>
        </div>
        <div class="insp">
          <label for="slc"><span data-i="insp"></span> <output id="slcN">15</output></label>
          <input type="range" id="slc" __IN_SLC__>
          <p class="small" id="slcR"></p>
        </div>
        <p class="st3" id="h3s" aria-live="polite"></p>
        <div class="row3"><button class="go" id="storm" data-i="storm"></button><button class="go alt" id="reset3" data-i="reset3"></button></div>
        <ul class="legend" id="leg3"></ul>
        <div class="res">
          <div class="kpi" id="k1"><span data-i="fsS"></span><strong id="v1">—</strong><span id="s1"></span></div>
          <div class="kpi" id="k2"><span data-i="fsE"></span><strong id="v2">—</strong><span id="s2"></span></div>
        </div>
        <p class="small" id="circ"></p>
        <p class="small" data-i="target"></p>
      </div>
      <div class="card">
        <h2 data-i="sensT"></h2>
        <div id="s3d" role="img" aria-label="3D bar chart of factor of safety versus water level"></div>
        <canvas id="cv2" hidden role="img" aria-label="Factor of safety versus water level"></canvas>
        <p class="small" data-i="sensNote"></p>
      </div>
      <div class="card">
        <details><summary data-i="slT"></summary>
          <div class="scroll"><table class="tbl" id="slices"></table></div>
        </details>
        <h3 data-i="methT"></h3>
        <div class="eq">F = Σ [ (c′·b + (W − u·b)·tanφ′) / mα ] ÷ Σ [ W·sinα + kh·W·(yc − yg)/R ]</div>
        <div class="eq" style="margin-top:6px">mα = cosα + sinα·tanφ′ / F</div>
        <ul class="clean small" data-list="assume" style="margin-top:8px"></ul>
      </div>
    </div>
  </div>
</section>

<footer>سماح قسومة — مدرّبة دولية · مستشارة جبائية<span id="ftr"></span></footer>
</div>
<script>
const DATA = __DATA__;
const T = DATA.i18n, CFG = DATA.defaults;
const $ = id => document.getElementById(id);

__BISHOP__

__SCENE3D__

__APP__
</script>
</body>
</html>
"""


def build(out: pathlib.Path) -> pathlib.Path:
    data = collect()
    fields = {f["id"]: f for f in data["defaults"]["fields"]}
    missing = [i for i in FIELD_IDS if i not in fields]
    if missing:
        raise SystemExit(f"champs absents de defaults.json : {missing}")

    html = TEMPLATE
    for fid in FIELD_IDS:
        html = html.replace(f"__IN_{fid.upper()}__", field_attrs(fields[fid]))
    html = html.replace(
        "__IN_SLC__",
        f'min="1" max="{data["defaults"]["slices"]}" value="{data["defaults"]["slices"] // 2}"',
    )
    for token, rel in (("__BISHOP__", "ui/bishop.js"),
                       ("__SCENE3D__", "ui/scene3d.js"),
                       ("__APP__", "ui/app.js")):
        html = html.replace(token, (BASE / rel).read_text(encoding="utf-8"))
    html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))

    left = [t for t in ("__DATA__", "__BISHOP__", "__SCENE3D__", "__APP__") if t in html]
    if left or "__IN_" in html:
        raise SystemExit(f"jetons non remplacés : {left}")

    out.write_text(html, encoding="utf-8")
    return out


def main() -> int:
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BASE.parent / "sidi-bou-said-landslide.html"
    built = build(target)
    d = collect()
    sys.stdout.write(f"HTML landslide -> {built} ({built.stat().st_size // 1024} Ko)\n")
    sys.stdout.write(
        f"{len(d['defaults']['layers'])} couches · {d['defaults']['slices']} tranches · "
        f"{len(d['i18n']['ar'])} cles x {len(LANGS)} langues\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
