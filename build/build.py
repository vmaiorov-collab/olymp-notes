#!/usr/bin/env python3
"""Сборка сайта: src/<параллель>/<файл>.src.html -> <параллель>/<файл>.html и index.html.

Исходник — это фрагмент HTML с первой строкой-метой:
  <!--meta {"title":"…","subtitle":"…","parallel":"parallel-c","pname":"Параллель C","n":1,"video":"…"}-->
Заголовки <h2 data-tc="мм:сс"> и <h3 data-tc="…"> получают id, номера, оглавление и боковое меню.
Блоки <pre class="cpp"> оборачиваются в карточку кода с подсветкой и кнопкой «копировать».
Формулы ($…$, $$…$$) рендерит встроенный KaTeX. Всё встроено в файл — страницы работают офлайн.

    python3 build/build.py
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "build"
CSS = (B / "style.css").read_text()
KCSS = (B / "katex.inline.css").read_text()
KJS = (B / "package/dist/katex.min.js").read_text()
KAUTO = (B / "package/dist/contrib/auto-render.min.js").read_text()
APP = (B / "app.js").read_text()
BASE_URL = "https://vmaiorov-collab.github.io/olymp-notes/"
HIT_URL = "https://olymp-notes-bots.d6544559.workers.dev/hit"

THEME_BOOT = ("(function(){try{var t=localStorage.getItem('olympTheme');if(!t){t=matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}"
              "document.documentElement.setAttribute('data-theme',t)}catch(e){document.documentElement.setAttribute('data-theme','light')}})();")
# маячок счётчика: без cookie, не мешает офлайн-чтению
BEACON = ("try{if(location.protocol.indexOf('http')===0&&navigator.sendBeacon)navigator.sendBeacon('" + HIT_URL +
          "?p='+encodeURIComponent(location.pathname))}catch(e){}")

CPP_KW = set("""alignas auto bool break case catch char class const constexpr continue default delete do double else enum explicit extern false
float for friend goto if inline int long namespace new noexcept nullptr operator private protected public return short signed sizeof static struct
switch template this throw true try typedef typename union unsigned using virtual void volatile while""".split())
CPP_TY = set("""string vector map set unordered_map unordered_set pair array deque queue stack priority_queue bitset multiset cin cout cerr endl
size_t int64_t int32_t uint64_t uint32_t ll ld ull mt19937 iostream istream ostream""".split())
TOK = re.compile(r'(?P<c>//[^\n]*|/\*.*?\*/)|(?P<s>"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\')|(?P<p>^[ \t]*#[^\n]*)|(?P<n>\b\d[\w.]*\b)|(?P<w>[A-Za-z_]\w*)',
                 re.S | re.M)


def hl_cpp(code: str) -> str:
    def rep(m):
        t = html.escape(m.group(0), quote=False)
        if m.group("c"): return f'<span class="c">{t}</span>'
        if m.group("s"): return f'<span class="s">{t}</span>'
        if m.group("p"): return f'<span class="p">{t}</span>'
        if m.group("n"): return f'<span class="n">{t}</span>'
        w = m.group("w")
        if w in CPP_KW: return f'<span class="k">{t}</span>'
        if w in CPP_TY: return f'<span class="t">{t}</span>'
        return t
    out, pos = [], 0
    for m in TOK.finditer(code):
        out.append(html.escape(code[pos:m.start()], quote=False)); out.append(rep(m)); pos = m.end()
    out.append(html.escape(code[pos:], quote=False))
    return "".join(out)


def wrap_code(body: str) -> str:
    def rep(m):
        lang, raw = m.group(1), html.unescape(m.group(2)).strip("\n")
        inner = hl_cpp(raw) if lang in ("cpp", "c++") else html.escape(raw, quote=False)
        return (f'<div class="code"><div class="code-head"><span>{lang.upper() if lang!="text" else "ПСЕВДОКОД"}</span>'
                f'<button type="button">копировать</button></div><pre><code>{inner}</code></pre></div>')
    return re.sub(r'<pre class="(\w+\+*)">(.*?)</pre>', rep, body, flags=re.S)


def process_headings(body: str):
    items, n2, n3 = [], 0, 0

    def rep(m):
        nonlocal n2, n3
        lvl, attrs, text = m.group(1), m.group(2), m.group(3)
        tcm = re.search(r'data-tc="([^"]+)"', attrs)
        tc = tcm.group(1) if tcm else ""
        plain = re.sub(r"<[^>]+>", "", text)
        if lvl == "2": n2 += 1; n3 = 0; num = f"{n2}"; hid = f"s{n2}"
        else: n3 += 1; num = f"{n2}.{n3}"; hid = f"s{n2}-{n3}"
        items.append((lvl, hid, num, plain, tc))
        tcs = f'<span class="tc">{tc}</span>' if tc else ""
        numh = f'<span class="num">{num}</span>' if lvl == "2" else ""
        return f'<h{lvl} id="{hid}">{numh}{text}{tcs}</h{lvl}>'
    body = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", rep, body, flags=re.S)
    return body, items


def page(meta, body, prev, nxt):
    body = wrap_code(body)
    body, items = process_headings(body)
    toc = "".join(
        f'<li><a href="#{i[1]}">{html.escape(i[3])}</a>' + (f'<span class="tc">{i[4]}</span>' if i[4] else "") + "</li>"
        for i in items if i[0] == "2")
    side = "".join(
        f'<a href="#{i[1]}"' + (' class="sub"' if i[0] == "3" else "") + f'>{i[2]}&nbsp; {html.escape(i[3])}</a>' for i in items)
    title = f'{meta["pname"]} · Занятие {meta["n"]}: {meta["title"]}'
    pager = ""
    if prev or nxt:
        pager = '<nav class="pager" style="display:flex;justify-content:space-between;gap:12px;margin-top:40px">'
        pager += (f'<a href="../{prev["href"]}">← {html.escape(prev["title"])}</a>' if prev else "<span></span>")
        pager += (f'<a href="../{nxt["href"]}">{html.escape(nxt["title"])} →</a>' if nxt else "<span></span>") + "</nav>"
    chips = "".join(f'<span class="chip">{c}</span>' for c in meta.get("chips", []))
    return f"""<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta.get('subtitle',''))}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:type" content="article">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%230d7c72'/%3E%3Cstop offset='1' stop-color='%23f0a94a'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='9' fill='url(%23g)'/%3E%3C/svg%3E">
<script>{THEME_BOOT}</script>
<style>{KCSS}</style>
<style>{CSS}</style>
</head>
<body>
<div id="progress"></div>
<button class="burger" id="burger" aria-label="Меню">☰</button>
<button class="theme" id="themeBtn" aria-label="Сменить тему">☾</button>
<div class="layout">
<aside class="side">
  <div class="brand"><i></i>Олимп-конспекты</div>
  <a class="back" href="../index.html">← Все конспекты</a>
  <h4>{html.escape(meta['pname'])} · занятие {meta['n']}</h4>
  <nav>{side}</nav>
</aside>
<main><div class="wrap">
<header class="hero">
  <div class="kicker">{html.escape(meta['pname'])} · Занятие {meta['n']}</div>
  <h1>{html.escape(meta['title'])}</h1>
  <div class="sub">{meta.get('subtitle','')}</div>
  <div class="chips">{chips}</div>
</header>
<nav class="toc"><h2>Содержание</h2><ol>{toc}</ol></nav>
{body}
{pager}
<footer class="end">Олимп-конспекты · конспект составлен по видеозаписи занятия; материалы лекции принадлежат их авторам.</footer>
</div></main>
</div>
<script>{KJS}</script>
<script>{KAUTO}</script>
<script>{meta.get('algos_js','')}</script>
<script>{APP}</script>
<script>{BEACON}</script>
</body>
</html>
"""


def index(parallels):
    cards = ""
    for p in parallels:
        ls = "".join(
            f'<a class="lec" href="{l["href"]}"><span class="n">{l["n"]}</span><span class="tt">{html.escape(l["title"])}</span>'
            f'<span class="sb">{html.escape(l.get("subtitle",""))}</span></a>' for l in p["lessons"])
        cards += f'<section class="par"><h2>{html.escape(p["pname"])}</h2><div class="grid">{ls}</div></section>'
    data = json.dumps([{"t": f'{p["pname"]} · {l["title"]}', "h": l["href"]} for p in parallels for l in p["lessons"]], ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ru" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Олимп-конспекты</title>
<meta name="description" content="Подробные офлайн-конспекты занятий по олимпиадному программированию.">
<script>{THEME_BOOT}</script>
<style>{CSS}
.home{{max-width:980px;margin:0 auto;padding:60px 20px 100px}}
.home .hero{{margin-bottom:34px}}
.par h2{{font-family:var(--serif);border:0;margin:1.6em 0 .5em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
.lec{{display:flex;flex-direction:column;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--ink);box-shadow:var(--shadow);transition:transform .15s,border-color .15s}}
.lec:hover{{transform:translateY(-2px);border-color:var(--accent);text-decoration:none}}
.lec .n{{font-size:.72rem;text-transform:uppercase;letter-spacing:.1em;color:var(--accent)}}
.lec .tt{{font-weight:650;font-size:1.05rem}}.lec .sb{{color:var(--muted);font-size:.86rem}}
#q{{width:100%;padding:12px 16px;border-radius:12px;border:1px solid var(--line);background:var(--card);color:var(--ink);font:inherit;margin-bottom:6px}}
</style></head><body>
<button class="theme" id="themeBtn" aria-label="Сменить тему">☾</button>
<div class="home"><header class="hero"><div class="kicker">Олимпиадное программирование</div><h1>Олимп-конспекты</h1>
<div class="sub">Подробные самодостаточные конспекты занятий: определения, доказательства, разборы задач, код и схемы. Каждая страница работает офлайн.</div></header>
<input id="q" placeholder="Поиск по занятиям…" autocomplete="off"><div id="hits"></div>
{cards}</div>
<script>var D={data};
var q=document.getElementById('q'),h=document.getElementById('hits');
q.addEventListener('input',function(){{var v=q.value.trim().toLowerCase();h.innerHTML=v?D.filter(function(x){{return x.t.toLowerCase().indexOf(v)>=0}}).map(function(x){{return '<p><a href="'+x.h+'">'+x.t+'</a></p>'}}).join(''):''}});</script>
<script>{APP}</script>
<script>{BEACON}</script>
</body></html>
"""


def main():
    src = ROOT / "src"
    parallels = {}
    for f in sorted(src.glob("*/*.src.html")):
        text = f.read_text()
        m = re.match(r"\s*<!--meta (.*?)-->\s*", text, re.S)
        meta = json.loads(m.group(1)); body = text[m.end():]
        algos = f.with_suffix("").with_suffix(".algos.js")
        meta["algos_js"] = algos.read_text() if algos.exists() else ""
        out_rel = f"{f.parent.name}/{f.name.replace('.src.html', '.html')}"
        p = parallels.setdefault(meta["parallel"], {"pname": meta["pname"], "order": meta.get("porder", 99), "lessons": []})
        p["lessons"].append({"n": meta["n"], "title": meta["title"], "subtitle": meta.get("subtitle", ""), "href": out_rel,
                             "meta": meta, "body": body, "out": ROOT / out_rel})
    plist = sorted(parallels.values(), key=lambda p: p["order"])
    for p in plist:
        p["lessons"].sort(key=lambda l: l["n"])
        for i, l in enumerate(p["lessons"]):
            prev = p["lessons"][i - 1] if i else None
            nxt = p["lessons"][i + 1] if i + 1 < len(p["lessons"]) else None
            l["out"].parent.mkdir(parents=True, exist_ok=True)
            l["out"].write_text(page(l["meta"], l["body"], prev, nxt))
            print("built", l["href"], l["out"].stat().st_size // 1024, "KB")
    (ROOT / "index.html").write_text(index([{"pname": p["pname"], "lessons": [{k: l[k] for k in ("n", "title", "subtitle", "href")} for l in p["lessons"]]} for p in plist]))
    print("built index.html")


if __name__ == "__main__":
    main()
