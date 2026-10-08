#!/usr/bin/env python3
"""Картинки превью ссылок (1200×630) для страниц параллелей: og-parallel-<ключ>.png.

Названия занятий берутся из parallel-*/index.html. Рендер — headless Chrome (CHROME в окружении
или стандартный путь macOS), шрифт Onest подгружается из Google Fonts. Запуск: python3 tools/build_og.py
"""
import html
import os
import re
import subprocess
import tempfile

CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
ORDER = ['c', 'bs', 'b', 'xs', 'x']
PASTEL = {'c': '#b9e6c9', 'bs': '#ffd3b0', 'b': '#cfe3ff', 'xs': '#e4d6ff', 'x': '#ffdd2d'}
TAG = {'c': 'Начальный', 'x': 'Продвинутый'}
URL = 'vmaiorov-collab.github.io/olymp-notes'
esc = html.escape

BASE = '''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400..800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}html,body{margin:0}
body{width:1200px;height:630px;background:#fff;font-family:"Onest",Helvetica,Arial,sans-serif;color:#000;padding:28px}
.panel{position:relative;width:100%;height:100%;border-radius:44px;padding:52px 60px;overflow:hidden}
.chip{display:inline-block;padding:9px 20px;border-radius:12px;background:rgba(255,255,255,.75);font-size:25px;font-weight:500}
h1{margin:26px 0 0;font-weight:800;letter-spacing:-.045em;line-height:.98;font-size:132px}
ul{list-style:none;margin:32px 0 0;padding:0;display:grid;gap:12px;max-width:820px}
li{display:flex;gap:18px;align-items:center;font-size:38px;font-weight:600;letter-spacing:-.02em}
li em{display:flex;align-items:center;justify-content:center;flex:none;width:46px;height:46px;border-radius:12px;background:#000;color:#fff;font-style:normal;font-size:24px;font-weight:700}
.big{position:absolute;right:60px;top:60px;display:flex;align-items:center;justify-content:center;width:230px;height:230px;border-radius:50%;background:rgba(255,255,255,.6);font-weight:800;font-size:128px;letter-spacing:-.04em}
.foot{position:absolute;left:60px;right:60px;bottom:44px;display:flex;justify-content:space-between;align-items:baseline;font-size:26px}
.foot b{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:24px}
.foot span{color:#444}
</style>
'''

for k in ORDER:
    page = open(f'parallel-{k}/index.html', encoding='utf-8').read()
    titles = [html.unescape(t) for t in re.findall(r'<span class="tt">(.*?)</span>', page)]
    n = len(titles)
    word = f'{n} занятие' if n == 1 else f'{n} занятия' if n < 5 else f'{n} занятий'
    chip = 'Т-Поколение · конспекты' + (f' · {TAG[k].lower()}' if k in TAG else '')
    items = ''.join(f'<li><em>{i + 1}</em>{esc(t)}</li>' for i, t in enumerate(titles))
    markup = BASE + (f'<div class="panel" style="background:{PASTEL[k]}"><span class="chip">{esc(chip)}</span>'
                     f'<h1>Параллель {k.upper()}</h1><ul>{items}</ul><div class="big">{k.upper()}</div>'
                     f'<div class="foot"><b>{URL}</b><span>{word}</span></div></div>')
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(markup)
        path = f.name
    out = f'og-parallel-{k}.png'
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=9000',
                    '--window-size=1200,630', f'--screenshot={out}', f'file://{path}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.unlink(path)
    print('готово:', out)
