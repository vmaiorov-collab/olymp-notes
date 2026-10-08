#!/usr/bin/env python3
"""Картинки превью ссылок (1200×630) в стиле сайта «Т-Поколение»: графит и жёлтый.

og-image.png — главная, og-parallel-<ключ>.png — страницы параллелей и их лекции.
Названия занятий берутся из parallel-*/index.html. Рендер — headless Chrome (CHROME в окружении
или стандартный путь macOS), шрифт Onest подгружается из Google Fonts.
Запуск из корня репозитория: python3 tools/build_og.py
"""
import html
import os
import re
import subprocess
import tempfile

CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
ORDER = ['c', 'bs', 'b', 'xs', 'x']
TAG = {'c': 'начальный', 'x': 'продвинутый'}
URL = 'vmaiorov-collab.github.io/olymp-notes'
YELLOW, BG, INK, MUTED = '#ffdd2d', '#17181c', '#ececf0', '#a3a6b0'
esc = html.escape

BASE = f'''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400..800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}html,body{{margin:0}}
body{{width:1200px;height:630px;background:#0d0e11;font-family:"Onest",Helvetica,Arial,sans-serif;color:{INK};padding:28px}}
.panel{{position:relative;width:100%;height:100%;border-radius:36px;padding:52px 60px;overflow:hidden;background:{BG};border:2px solid #2c2e35}}
.chip{{display:inline-block;padding:9px 20px;border-radius:12px;background:{YELLOW};color:#111;font-size:25px;font-weight:700}}
h1{{margin:26px 0 0;font-weight:800;letter-spacing:-.045em;line-height:.98;font-size:112px;white-space:nowrap}}
.hi{{background:linear-gradient(transparent 62%,{YELLOW} 62%,{YELLOW} 94%,transparent 94%);color:{INK};padding:0 .05em}}
.lead{{margin:26px 0 0;font-size:36px;line-height:1.35;color:{MUTED};max-width:540px}}
ul{{list-style:none;margin:30px 0 0;padding:0;display:grid;gap:12px;max-width:820px}}
li{{display:flex;gap:18px;align-items:center;font-size:38px;font-weight:600;letter-spacing:-.02em}}
li em{{display:flex;align-items:center;justify-content:center;flex:none;width:46px;height:46px;border-radius:12px;background:{YELLOW};color:#111;font-style:normal;font-size:24px;font-weight:800}}
.big{{position:absolute;right:60px;top:60px;display:flex;align-items:center;justify-content:center;width:230px;height:230px;border-radius:50%;background:{YELLOW};color:#111;font-weight:800;font-size:128px;letter-spacing:-.04em}}
.row{{position:absolute;right:60px;bottom:116px;display:flex;gap:12px}}
.row i{{display:flex;align-items:center;justify-content:center;width:80px;height:80px;border-radius:50%;background:{YELLOW};color:#111;font-style:normal;font-weight:800;font-size:32px}}
.foot{{position:absolute;left:60px;right:60px;bottom:44px;display:flex;justify-content:space-between;align-items:baseline;font-size:26px}}
.foot b{{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:24px;color:{INK}}}
.foot span{{color:{MUTED}}}
</style>
'''


def word(n):
    return f'{n} занятие' if n == 1 else f'{n} занятия' if n < 5 else f'{n} занятий'


def render(markup, out):
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(markup)
        path = f.name
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=9000',
                    '--window-size=1200,630', f'--screenshot={out}', f'file://{path}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    os.unlink(path)
    print('готово:', out)


titles = {}
for k in ORDER:
    page = open(f'parallel-{k}/index.html', encoding='utf-8').read()
    titles[k] = [html.unescape(t) for t in re.findall(r'<span class="tt">(.*?)</span>', page)]
total = sum(len(v) for v in titles.values())

circles = ''.join(f'<i>{k.upper()}</i>' for k in ORDER)
render(BASE + f'<div class="panel"><span class="chip">Т-Поколение · олимпиадное программирование</span>'
              f'<h1>Олимп-<span class="hi">конспекты</span></h1>'
              f'<p class="lead">Разборы задач, код и схемы. Работают офлайн.</p>'
              f'<div class="row">{circles}</div>'
              f'<div class="foot"><b>{URL}</b><span>{total} занятий · {len(ORDER)} параллелей</span></div></div>', 'og-image.png')

for k in ORDER:
    chip = 'Т-Поколение · конспекты' + (f' · {TAG[k]}' if k in TAG else '')
    items = ''.join(f'<li><em>{i + 1}</em>{esc(t)}</li>' for i, t in enumerate(titles[k]))
    render(BASE + f'<div class="panel"><span class="chip">{esc(chip)}</span><h1>Параллель {k.upper()}</h1>'
                  f'<ul>{items}</ul><div class="big">{k.upper()}</div>'
                  f'<div class="foot"><b>{URL}</b><span>{word(len(titles[k]))}</span></div></div>', f'og-parallel-{k}.png')
