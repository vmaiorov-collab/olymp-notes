#!/usr/bin/env python3
"""Собирает главную (index.html) и страницы параллелей (parallel-*/index.html).

Данные берутся из мета-комментариев в src/<параллель>/*.src.html.
Стили и скрипты лежат в assets/home.css и assets/home.js.
Запуск из корня репозитория: python3 tools/build_home.py
"""
import glob, html, json, os, re

BASE = 'https://vmaiorov-collab.github.io/olymp-notes/'
ORDER = ['c', 'bs', 'b', 'xs', 'x']
TAG = {'c': 'Начальный', 'x': 'Продвинутый'}
DESC = {
    'c': 'Контейнеры, линейные алгоритмы, бинарный поиск.',
    'bs': 'STL, жадные алгоритмы, бинпоиск и два указателя.',
    'b': 'Дерево отрезков и динамическое программирование.',
    'xs': 'Деревья и математика.',
    'x': 'Дерево отрезков, теория чисел, потоки.',
}


def word(n):
    if n % 10 == 1 and n % 100 != 11:
        return f'{n} занятие'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return f'{n} занятия'
    return f'{n} занятий'


def esc(x):
    return html.escape(x, quote=True)


lessons = {k: [] for k in ORDER}
for p in glob.glob('src/*/*.src.html'):
    src = open(p, encoding='utf-8').read()
    meta = json.loads(re.match(r'<!--meta (\{.*?\})\s*-->', src, re.S).group(1))
    key = meta['parallel'].replace('parallel-', '')
    chips = meta.get('chips') or []
    if isinstance(chips, str):
        chips = [chips]
    dur = next((c for c in chips if '≈' in c), '')
    page = os.path.basename(p).replace('.src.html', '.html')
    lessons[key].append(dict(n=meta['n'], title=meta['title'], sub=meta.get('subtitle', ''),
                             dur=dur, href=f"parallel-{key}/{page}"))
for k in lessons:
    lessons[k].sort(key=lambda x: x['n'])
total = sum(len(v) for v in lessons.values())

THEME = ('<script>(function(){try{var t=localStorage.getItem("olympTheme")||"dark";'
         'document.documentElement.setAttribute("data-theme",t)}catch(e){'
         'document.documentElement.setAttribute("data-theme","dark")}})();</script>\n'
         '<script>document.documentElement.setAttribute("data-look","book");</script>')
ICON = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'%3E'
        '%3Crect width=\'32\' height=\'32\' rx=\'7\' fill=\'%23ffdd2d\'/%3E%3Ctext x=\'16\' y=\'23\' font-size=\'20\' '
        'font-family=\'Georgia\' font-weight=\'700\' text-anchor=\'middle\' fill=\'%23333\'%3E%D0%9E%3C/text%3E%3C/svg%3E">')


def head(title, desc, url, prefix):
    t, d = esc(title), esc(desc)
    img = BASE + 'og-image.png'
    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{ICON}
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="#ffdd2d">
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Олимп-конспекты">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<link rel="apple-touch-icon" href="{BASE}apple-touch-icon.png">
{THEME}
<link rel="stylesheet" href="{prefix}assets/home.css">
</head>
'''


def tail(prefix, extra=''):
    return f'''<button class="toplink" id="topBtn">↑ наверх</button>
{extra}<script src="{prefix}assets/home.js"></script>
<script data-goatcounter="https://vmaiorov.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body></html>
'''


def footer(prefix):
    return ('<footer class="foot"><a href="https://education.tbank.ru/school/generation/algo/">'
            'education.tbank.ru/school/generation/algo</a>'
            '<a href="https://vmaiorov-collab.github.io/">все проекты</a>'
            '<a href="https://vmaiorov.goatcounter.com/" target="_blank" rel="noopener">статистика посещений</a></footer>')


SITE = '<a class="sitelink" href="https://vmaiorov-collab.github.io/">← На главный сайт</a>'
TOGGLE = '<button type="button" id="theme-toggle" class="theme-toggle" aria-label="Переключить тему">тёмная тема</button>'

# ── главная ──
cards = ''
for k in ORDER:
    ls = lessons[k]
    tag = f'<span class="lg">{TAG[k]}</span>' if k in TAG else ''
    cards += (f'<a class="lv" href="parallel-{k}/index.html"><div class="lh"><span class="lk">{k.upper()}</span>'
              f'<div><h3>Параллель {k.upper()}</h3>{tag}</div></div>'
              f'<div class="lt">{esc(DESC[k])}</div>'
              f'<div class="lc"><span>{word(len(ls))}</span><em>открыть →</em></div></a>')
data = [dict(t=f'Параллель {k.upper()} · {l["title"]}', s=l['sub'], h=l['href'])
        for k in ORDER for l in lessons[k]]
index = head('Олимп-конспекты',
             'Подробные офлайн-конспекты занятий по олимпиадному программированию: дерево отрезков, теория чисел, потоки, бинпоиск, STL.',
             BASE, '') + f'''<body>
<div class="wrap">
<div class="top">{SITE}{TOGGLE}</div>
<header class="home"><div class="eyebrow"><i></i>Т-Поколение · олимпиадное программирование</div>
<h1>Олимп-<mark>конспекты</mark></h1>
<p class="lead">Подробные конспекты занятий: определения, доказательства, разборы задач, код и схемы. Каждая страница — один файл, который работает офлайн.</p>
<div class="facts"><span><b>{total}</b> занятий</span><span><b>{len(ORDER)}</b> параллелей</span><span><b>офлайн</b> без интернета</span></div>
<input id="q" placeholder="Поиск по занятиям: например, бинпоиск или потоки" autocomplete="off"><div id="hits"></div>
<div class="lvh">Выберите параллель</div><nav class="levels big">{cards}</nav>
</header>
{footer('')}
</div>
'''
index += tail('', '<script>var D=' + json.dumps(data, ensure_ascii=False) + ';</script>\n')
open('index.html', 'w', encoding='utf-8').write(index)

# ── страницы параллелей ──
for i, k in enumerate(ORDER):
    ls = lessons[k]
    tag = f'<span>{TAG[k]}</span>' if k in TAG else ''
    cards = ''.join(
        f'<a class="lec" href="{os.path.basename(l["href"])}"><span class="n">Занятие {l["n"]}</span>'
        f'<span class="tt">{esc(l["title"])}</span><span class="sb">{esc(l["sub"])}</span>'
        + (f'<span class="du">{esc(l["dur"])}</span>' if l['dur'] else '') + '</a>' for l in ls)
    prev = (f'<a href="../parallel-{ORDER[i-1]}/index.html"><small>← предыдущая</small><b>Параллель {ORDER[i-1].upper()}</b></a>'
            if i else '<a class="ph0"></a>')
    nxt = (f'<a href="../parallel-{ORDER[i+1]}/index.html"><small>следующая →</small><b>Параллель {ORDER[i+1].upper()}</b></a>'
           if i < len(ORDER) - 1 else '')
    page = head(f'Параллель {k.upper()} — Олимп-конспекты', DESC[k], f'{BASE}parallel-{k}/', '../') + f'''<body>
<div class="wrap">
<div class="top"><a class="sitelink" data-up href="../index.html">← Все параллели</a>{TOGGLE}</div>
<header class="phead"><div class="tagrow"><span class="lk">{k.upper()}</span>{tag}<span>{word(len(ls))}</span></div>
<h1>Параллель {k.upper()}</h1><p class="lead">{esc(DESC[k])}</p></header>
<div class="grid" style="margin-top:22px">{cards}</div>
<nav class="pnav">{prev}{nxt}</nav>
{footer('../')}
</div>
''' + tail('../')
    open(f'parallel-{k}/index.html', 'w', encoding='utf-8').write(page)
print('ok', total, {k: len(v) for k, v in lessons.items()})
