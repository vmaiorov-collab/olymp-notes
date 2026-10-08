#!/usr/bin/env python3
"""Сборка сайта: src/<параллель>/<файл>.src.html -> <параллель>/<файл>.html и index.html.

Оформление и разметка страниц повторяют conspectus (стили и скрипты лежат в build/theme/,
палитра заменена на свою). Исходник — фрагмент HTML с первой строкой-метой:
  <!--meta {"title":"…","subtitle":"…","parallel":"parallel-c","pname":"Параллель C","porder":1,"n":1,"video":"video-232575486_456239903","chips":["…"]}-->
Заголовки <h2 data-tc="1:02:30"> и <h3> получают id, номера и таймкод-ссылку на запись (VK),
<ts t="12:30"/> внутри текста — такая же ссылка. Блоки <pre class="cpp"> оборачиваются в карточку кода.

    python3 build/build.py
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / "build"
TH = B / "theme"
HIT_URL = "https://olymp-notes-bots.d6544559.workers.dev/hit"


def th(name):
    return (TH / name).read_text()


HEAD_CSS = "".join(f"<style>{th(n)}</style>\n" for n in ["base.css"]) + f"<style>{(B / 'katex.inline.css').read_text()}</style>\n" + \
    "".join(f"<style>{th(n)}</style>\n" for n in ["back.css", "paper.css", "accent.css", "book.css", "extras.css"])
KJS = (B / "package/dist/katex.min.js").read_text()
KAUTO = (B / "package/dist/contrib/auto-render.min.js").read_text()
TAIL_JS = "".join(f"<script>{th(n)}</script>\n" for n in
                  ["clicks.js", "topbtn.js", "render.js", "theme.js", "algos1.js", "algos2.js", "frames.js", "look.js", "reader.js"])
BOOT = f"<script>{th('boot-theme.js')}</script>\n<script>{th('boot-look.js')}</script>\n"
GOAT = '<script data-goatcounter="https://vmaiorov.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'
# маячок бота статистики: без cookie
BEACON = ("<script>try{if(location.protocol.indexOf('http')===0&&navigator.sendBeacon)navigator.sendBeacon('" + HIT_URL +
          "?p='+encodeURIComponent(location.pathname))}catch(e){}</script>")
FAVICON = ("<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E"
           "%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%230d7c72'/%3E%3Cstop offset='1' stop-color='%23f0a94a'/%3E"
           "%3C/linearGradient%3E%3C/defs%3E%3Crect width='32' height='32' rx='9' fill='url(%23g)'/%3E%3C/svg%3E\">")

CPP_KW = set("""alignas auto bool break case catch char class const constexpr continue default delete do double else enum explicit extern false
float for friend goto if inline int long namespace new noexcept nullptr operator private protected public return short signed sizeof static struct
switch template this throw true try typedef typename union unsigned using virtual void volatile while""".split())
CPP_TY = set("""string vector map set unordered_map unordered_set pair array deque queue stack priority_queue bitset multiset cin cout cerr endl
size_t int64_t int32_t uint64_t uint32_t ll ld ull mt19937 iostream istream ostream""".split())
TOK = re.compile(r'(?P<c>//[^\n]*|/\*.*?\*/)|(?P<s>"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])\')|(?P<p>^[ \t]*#[^\n]*)|(?P<n>\b\d[\w.]*\b)|(?P<w>[A-Za-z_]\w*)(?P<call>\s*\()?',
                 re.S | re.M)


def hl_cpp(code: str) -> str:
    out, pos = [], 0
    for m in TOK.finditer(code):
        out.append(html.escape(code[pos:m.start()], quote=False))
        pos = m.end()
        t = html.escape(m.group(0), quote=False)
        if m.group("c"): out.append(f'<span class="c">{t}</span>')
        elif m.group("s"): out.append(f'<span class="s">{t}</span>')
        elif m.group("p"): out.append(f'<span class="p">{t}</span>')
        elif m.group("n"): out.append(f'<span class="n">{t}</span>')
        else:
            w = m.group("w")
            rest = html.escape(m.group(0)[len(w):], quote=False)
            if w in CPP_KW: out.append(f'<span class="k">{w}</span>{rest}')
            elif w in CPP_TY: out.append(f'<span class="t">{w}</span>{rest}')
            elif m.group("call"): out.append(f'<span class="f">{w}</span>{rest}')
            else: out.append(t)
    out.append(html.escape(code[pos:], quote=False))
    return "".join(out)


def wrap_code(body: str) -> str:
    def rep(m):
        lang, raw = m.group(1), html.unescape(m.group(2)).strip("\n")
        if lang in ("cpp", "c++"):
            return (f'<div class="code"><div class="code-head"><span>C++</span><button class="copy" type="button">копировать</button></div>'
                    f'<pre class="hl"><code>{hl_cpp(raw)}</code></pre></div>')
        label = {"template": "шаблон", "pseudo": "псевдокод"}.get(lang, "текст")
        return (f'<div class="code"><div class="code-head"><span>{label}</span><button class="copy" type="button">копировать</button></div>'
                f'<pre class="hl"><code>{html.escape(raw, quote=False)}</code></pre></div>')
    return re.sub(r'<pre class="([\w+]+)">(.*?)</pre>', rep, body, flags=re.S)


def tc_seconds(tc):
    sec = 0
    for x in tc.split(":"): sec = sec * 60 + int(x)
    return sec


def tc_label(tc):
    t = tc_seconds(tc)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def ts_link(video, tc):
    t = tc_seconds(tc)
    h, m, s = t // 3600, t % 3600 // 60, t % 60
    q = (f"{h}h" if h else "") + (f"{m}m" if m or h else "") + f"{s}s"
    return (f'<a class="ts" href="https://vkvideo.ru/{video}?t={q}" target="_blank" rel="noopener" '
            f'title="Смотреть лекцию с этого момента">{tc_label(tc)}</a>')


def process_headings(body: str, video: str):
    items, n2, n3 = [], 0, 0

    def rep(m):
        nonlocal n2, n3
        lvl, attrs, text = m.group(1), m.group(2), m.group(3)
        text = re.sub(r"^\s*(?:\d+\.)+\s*", "", text)          # номера ставит сборщик; ручные («1.4.») убираем
        tcm = re.search(r'data-tc="([^"]+)"', attrs)
        tc = tcm.group(1) if tcm else ""
        if lvl == "2": n2 += 1; n3 = 0; num = f"{n2}."; hid = f"s{n2}"
        else: n3 += 1; num = f"{n2}.{n3}."; hid = f"s{n2}-{n3}"
        items.append((lvl, hid, num, re.sub(r"<[^>]+>", "", text), tc_label(tc) if tc else ""))
        return f'<h{lvl} id="{hid}">{num} {text}{" " + ts_link(video, tc) if tc else ""}</h{lvl}>'
    body = re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", rep, body, flags=re.S)
    body = re.sub(r'<ts t="([\d:]+)"\s*/>', lambda m: ts_link(video, m.group(1)), body)
    return body, items


def page(meta, body, prev, nxt):
    video = meta["video"]
    body = wrap_code(body)
    body, items = process_headings(body, video)
    toc = "".join(
        f'<li class="t{i[0]}"><a href="#{i[1]}"><span class="tn">{i[2]}</span> {html.escape(i[3])}</a>'
        + (f'<span class="tt">{i[4]}</span>' if i[4] else "") + "</li>" for i in items)
    title = f'Занятие {meta["n"]}. {meta["pname"]} — {meta["title"]}'
    chips = "".join(f'<span class="chip">{c}</span>' for c in meta.get("chips", []))
    pg = f'<a class="prev" href="../{prev["href"]}"><small>← занятие {prev["n"]}</small><b>{html.escape(prev["title"])}</b></a>' if prev else ""
    pg += (f'<a class="next" href="../{nxt["href"]}"><small>занятие {nxt["n"]} →</small><b>{html.escape(nxt["title"])}</b></a>' if nxt
           else '<a class="next" href="../index.html"><small>дальше</small><b>Все конспекты</b></a>')
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{FAVICON}
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(meta.get('subtitle', ''))}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:locale" content="ru_RU">
{BOOT}{HEAD_CSS}</head>
<body>
<div class="wrap">
<div class="top"><a class="back" href="../index.html">← Все конспекты</a><button type="button" id="theme-toggle" class="theme-toggle" aria-label="Переключить тему">тёмная тема</button><button type="button" id="look-toggle" class="look-toggle">↩ старый вид</button></div>

<header class="hero">
  <h1>{html.escape(title)}</h1>
  <div class="sub">{meta.get('subtitle', '')}</div>
  <div class="meta">{chips}</div>
</header>

<nav class="toc">
  <h2>Содержание</h2>
  <ol>{toc}</ol>
</nav>
{body}
<footer>
  Конспект подготовлен по записи занятия. Таймкоды соответствуют исходной видеозаписи. Код приведён в виде, эквивалентном разобранному на занятии.
</footer>
<nav class="pager" aria-label="Соседние занятия">{pg}</nav>
</div>

<button class="toplink" id="topBtn">↑ наверх</button>
<script>{KJS}</script>
<script>{KAUTO}</script>
<script>{meta.get('algos_js', '')}</script>
{TAIL_JS}{BEACON}
{GOAT}
</body>
</html>
"""


def index(parallels):
    cards = ""
    for p in parallels:
        ls = "".join(
            f'<a class="lec" href="{l["href"]}"><span class="n">Занятие {l["n"]}</span><span class="tt">{html.escape(l["title"])}</span>'
            f'<span class="sb">{html.escape(l.get("subtitle", ""))}</span></a>' for l in p["lessons"])
        cards += f'<section class="par"><h2>{html.escape(p["pname"])}</h2><div class="grid">{ls}</div></section>'
    data = json.dumps([{"t": f'{p["pname"]} · {l["title"]}', "h": l["href"]} for p in parallels for l in p["lessons"]], ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{FAVICON}
<title>Олимп-конспекты</title>
<meta name="description" content="Подробные офлайн-конспекты занятий по олимпиадному программированию.">
{BOOT}{HEAD_CSS}<style>
.par h2{{font-size:1.4rem;margin:1.8em 0 .5em}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}}
.lec{{display:flex;flex-direction:column;gap:3px;background:var(--card);border:1px solid var(--line);padding:14px 16px;color:var(--ink)}}
.lec:hover{{border-color:var(--accent);text-decoration:none}}
.lec .n{{font-family:var(--mono);font-size:.72rem;color:var(--accent);letter-spacing:.06em;text-transform:uppercase}}
.lec .tt{{font-family:var(--serif);font-weight:700;font-size:1.08rem}}.lec .sb{{color:var(--muted);font-size:.85rem}}
#q{{width:100%;padding:11px 14px;border:1px solid var(--rule-hard,var(--line));background:var(--card);color:var(--ink);font:inherit;margin:22px 0 4px}}
html[data-look="book"] .wrap{{padding:0 64px 64px}}
html[data-look="book"] .top{{margin-left:0}}
@media(max-width:680px){{html[data-look="book"] .wrap{{padding:0 18px 48px}}}}
</style></head>
<body>
<div class="wrap">
<div class="top"><span>olymp-notes</span><button type="button" id="theme-toggle" class="theme-toggle" aria-label="Переключить тему">тёмная тема</button><button type="button" id="look-toggle" class="look-toggle">↩ старый вид</button></div>
<header class="hero"><h1>Олимп-конспекты</h1>
<div class="sub">Подробные самодостаточные конспекты занятий по олимпиадному программированию: определения, доказательства, разборы задач, код и схемы. Каждая страница работает офлайн.</div></header>
<input id="q" placeholder="Поиск по занятиям…" autocomplete="off"><div id="hits"></div>
{cards}
<footer><a href="https://vmaiorov.goatcounter.com/" target="_blank" rel="noopener">статистика посещений</a></footer>
</div>
<button class="toplink" id="topBtn">↑ наверх</button>
<script>var D={data};
var q=document.getElementById('q'),h=document.getElementById('hits');
q.addEventListener('input',function(){{var v=q.value.trim().toLowerCase();h.innerHTML=v?D.filter(function(x){{return x.t.toLowerCase().indexOf(v)>=0}}).map(function(x){{return '<p><a href="'+x.h+'">'+x.t+'</a></p>'}}).join(''):''}});</script>
{TAIL_JS}{BEACON}
{GOAT}
</body></html>
"""


def main():
    src = ROOT / "src"
    parallels = {}
    for f in sorted(src.glob("*/*.src.html")):
        text = f.read_text()
        m = re.match(r"\s*<!--meta (.*?)-->\s*", text, re.S)
        meta = json.loads(m.group(1)); body = text[m.end():]
        algos = f.with_name(f.name.replace(".src.html", ".algos.js"))
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
