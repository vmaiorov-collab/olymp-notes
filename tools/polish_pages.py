#!/usr/bin/env python3
"""Доводит страницы занятий (после build/build.py) до вида опубликованного сайта: og-мета, светлая тема по умолчанию,
шапка «← Параллель X / Все параллели», скруглённые кнопки, подвал, «к списку» вместо «дальше» на последнем занятии.
Идемпотентно (страницы с og:site_name пропускаются). Запуск: python3 tools/polish_pages.py parallel-b/*.html"""
import html, re, sys

BASE = 'https://vmaiorov-collab.github.io/olymp-notes/'
ROUND = ('<style>\n/* скруглённые кнопки в конспектах */\n.sitelink,.theme-toggle,.look-toggle,.toplink,.code .copy{border-radius:999px!important}\n'
         '.top .sitelink,.top .theme-toggle,.top .look-toggle{padding:5px 14px!important}\n</style>\n')
FOOT = ('<footer style="text-align:center;padding:24px 16px 32px;font-size:14px;opacity:.75"><a href="https://education.tbank.ru/school/generation/algo/" style="color:inherit">education.tbank.ru/school/generation/algo</a> · '
        '<a href="https://t.me/t_conspectus_ideas_bot" target="_blank" rel="noopener" style="color:inherit">нашли ошибку? напишите в бот</a></footer>\n')
GRID = re.compile(r'html\[data-look="book"\] body::before\{\s*content:"";.*?\n\}', re.S)

for path in sys.argv[1:]:
    if path.endswith('index.html'): continue
    s = open(path, encoding='utf-8').read()
    if 'og:site_name' in s: continue
    par = re.search(r'parallel-(\w+)/', path.replace('\\', '/')).group(1)
    title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', s).group(1))
    url = BASE + path.replace('\\', '/')
    e = lambda x: html.escape(x, quote=True)
    og = (f'<meta property="og:site_name" content="Олимп-конспекты">\n<meta property="og:description" content="{e(desc)}">\n'
          f'<meta property="og:image" content="{BASE}og-parallel-{par}.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
          f'<meta property="og:url" content="{url}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{e(title)}">\n'
          f'<meta name="twitter:description" content="{e(desc)}">\n<meta name="twitter:image" content="{BASE}og-parallel-{par}.png">\n'
          f'<link rel="apple-touch-icon" href="{BASE}apple-touch-icon.png">\n\n')
    s = s.replace('<script>(function(){try{var t=localStorage.getItem("olympTheme")||"dark"', og + '<script>(function(){try{var t=localStorage.getItem("olympTheme")||"dark"', 1)
    s = s.replace('||"dark";document.documentElement', '||"light";document.documentElement').replace('catch(e){document.documentElement.setAttribute("data-theme","dark")}', 'catch(e){document.documentElement.setAttribute("data-theme","light")}')
    s = GRID.sub('html[data-look="book"] body::before{display:none}', s, count=1)
    s = s.replace('</head>', ROUND + '</head>', 1)
    s = re.sub(r'<a class="sitelink" href="https://vmaiorov-collab.github.io/">← На главный сайт</a><a class="back" href="\.\./index.html">← Все конспекты</a>',
               f'<a class="sitelink" href="index.html">← Параллель {par.upper()}</a><a class="back" href="../index.html">Все параллели</a>', s, count=1)
    s = re.sub(r'<a class="next" href="\.\./index\.html"><small>дальше</small><b>Все конспекты</b></a>',
               f'<a class="next" href="index.html"><small>к списку</small><b>Параллель {par.upper()}</b></a>', s, count=1)
    s = s.replace('</body>', FOOT + '</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('polished', path)
