#!/usr/bin/env python3
"""Telegram-бот статистики olymp-notes на данных GoatCounter.

Команды: /stats [дни] · /today · /top [дни] · /parallels [дни]; те же разделы кнопками.
Работает через long polling, пока запущен процесс. Секреты берутся из окружения
или из файла ~/.config/olymp-stats-bot.env (в репозиторий не попадают):
  TELEGRAM_BOT_TOKEN  токен бота от @BotFather
  GC_TOKEN            API-токен GoatCounter (Settings → API)
  GC_SITE             код сайта GoatCounter (vmaiorov)
Запуск: python3 tools/stats_bot.py
"""
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PREFIX = '/olymp-notes'
SITE_URL = 'https://vmaiorov-collab.github.io/olymp-notes/'
LABELS = {'c': 'Параллель C', 'bs': 'Параллель BS', 'b': 'Параллель B', 'xs': 'Параллель XS', 'x': 'Параллель X'}
SPARK = '▁▂▃▄▅▆▇█'
PERIODS = [1, 7, 30, 90]
VIEWS = [('stats', '📊 Сводка'), ('top', '🏆 Топ'), ('par', '🧩 Параллели')]
WEEKDAYS = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']


def load_env():
    p = os.path.expanduser('~/.config/olymp-stats-bot.env')
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k, v)


load_env()
TG = os.environ.get('TELEGRAM_BOT_TOKEN')
GC_TOKEN = os.environ.get('GC_TOKEN')
GC_SITE = os.environ.get('GC_SITE', 'vmaiorov')
if not TG or not GC_TOKEN:
    sys.exit('Нужны TELEGRAM_BOT_TOKEN и GC_TOKEN (см. docstring)')


def http(url, data=None, headers=None, timeout=60):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def tg(method, **params):
    body = json.dumps(params).encode()
    return http(f'https://api.telegram.org/bot{TG}/{method}', body, {'Content-Type': 'application/json'}, 70)


# ── GoatCounter ──
def gc_hits(start):
    """Страницы olymp-notes с числом визитов за период и разбивкой по дням."""
    out, after = [], None
    while True:
        q = {'start': start.strftime('%Y-%m-%dT00:00:00Z'), 'limit': '100'}
        if after:
            q['after'] = after
        d = http(f'https://{GC_SITE}.goatcounter.com/api/v0/stats/hits?' + urllib.parse.urlencode(q),
                 headers={'Authorization': f'Bearer {GC_TOKEN}'})
        out += [h for h in d['hits'] if h['path'].startswith(PREFIX)]
        if not d.get('more') or not d['hits']:
            return out
        after = d['hits'][-1]['path_id']


def today():
    return dt.datetime.now(dt.timezone.utc).date()


def window(days):
    end = today()
    return end - dt.timedelta(days=days - 1), end


def per_day(hits, start, end):
    m = {}
    for h in hits:
        for s in h['stats']:
            m[s['day']] = m.get(s['day'], 0) + s['daily']
    days = []
    d = start
    while d <= end:
        days.append((d, m.get(d.isoformat(), 0)))
        d += dt.timedelta(days=1)
    return days


# ── оформление ──
esc = html.escape


def spark(v):
    mx = max(v) if v else 0
    return ''.join(SPARK[min(7, round(x / mx * 7))] if mx else SPARK[0] for x in v)


def bar(v, mx, w=10):
    n = max(1 if v > 0 else 0, round(v / mx * w)) if mx else 0
    return '█' * n + '░' * (w - n)


def label(d):
    return 'сегодня' if d == 1 else f'{d} дн.'


def page_name(path):
    p = path[len(PREFIX):].strip('/')
    m = re.match(r'parallel-(\w+)/(.*)', p)
    if not p or p == 'index.html':
        return 'Главная'
    if m:
        k, rest = m.groups()
        if rest in ('', 'index.html'):
            return f'{LABELS.get(k, k)} · список'
        return f'{LABELS.get(k, k)} · {rest.replace(".html", "")[len("parallel-" + k) + 1:]}'
    return p


def report_stats(days):
    start, end = window(days)
    hits = gc_hits(start - dt.timedelta(days=days))   # с запасом: текущий + прошлый период
    rows = per_day(hits, start - dt.timedelta(days=days), end)
    cur, prev = rows[days:], rows[:days]
    total, ptotal = sum(x for _, x in cur), sum(x for _, x in prev)
    if not ptotal:
        dlt = 'новое' if total else '—'
    else:
        p = round((total - ptotal) / ptotal * 100)
        dlt = f"{'▲ +' if p > 0 else '▼ −' if p < 0 else '• '}{abs(p)}%"
    lines = [f'📊 <b>Статистика olymp-notes</b> · {label(days)}', '',
             f'👥 Просмотров: <b>{total}</b>  <i>{dlt} к прошлому периоду ({ptotal})</i>']
    if days > 1:
        best = max(cur, key=lambda r: r[1])
        lines.append(f'📈 В среднем: <b>{total / days:.1f}</b> в день')
        if best[1]:
            lines.append(f'🔥 Рекорд: <b>{best[1]}</b> — {best[0].strftime("%d.%m")} ({WEEKDAYS[best[0].weekday()]})')
        lines += ['', f'<code>{spark([x for _, x in cur])}</code>',
                  f'<i>{cur[0][0].strftime("%d.%m")} → сегодня</i>']
    if not total:
        lines += ['', 'Данных пока нет.']
    return '\n'.join(lines)


def counts(hits, start, end):
    """Просмотры страницы за окно (по дням, а не за весь запрошенный период)."""
    res = []
    for h in hits:
        n = sum(s['daily'] for s in h['stats'] if start.isoformat() <= s['day'] <= end.isoformat())
        if n:
            res.append((h['path'], n))
    return sorted(res, key=lambda x: -x[1])


def report_top(days, n=8):
    start, end = window(days)
    rows = counts(gc_hits(start), start, end)[:n]
    head = f'🏆 <b>Топ страниц</b> · {label(days)}'
    if not rows:
        return f'{head}\n\nПока нет данных.'
    mx, medals, lines = rows[0][1], ['🥇', '🥈', '🥉'], [head, '']
    for i, (p, c) in enumerate(rows):
        lines += [f'{medals[i] if i < 3 else f"<b>{i + 1}.</b>"} {esc(page_name(p))}',
                  f'     <code>{bar(c, mx)}</code> <b>{c}</b>']
    return '\n'.join(lines)


def report_par(days):
    start, end = window(days)
    tot = {}
    for p, c in counts(gc_hits(start), start, end):
        m = re.match(PREFIX + r'/parallel-(\w+)/', p)
        k = LABELS.get(m.group(1), m.group(1)) if m else 'Главная'
        tot[k] = tot.get(k, 0) + c
    head = f'🧩 <b>Просмотры по параллелям</b> · {label(days)}'
    if not tot:
        return f'{head}\n\nПока нет данных.'
    rows = sorted(tot.items(), key=lambda x: -x[1])
    mx, s = rows[0][1], sum(tot.values())
    lines = [head, '']
    for name, c in rows:
        lines += [esc(name), f'<code>{bar(c, mx)}</code> <b>{c}</b> · {round(c / s * 100)}%']
    return '\n'.join(lines)


def keyboard(view, days):
    periods = [{'text': f'• {label(d).capitalize()} •' if d == days else label(d).capitalize(),
                'callback_data': f'{view}:{d}'} for d in PERIODS]
    views = [{'text': ('✔ ' if v == view else '') + t, 'callback_data': f'{v}:{days}'} for v, t in VIEWS]
    return {'inline_keyboard': [periods, views,
                                [{'text': '🔄 Обновить', 'callback_data': f'{view}:{days}'},
                                 {'text': '🌐 Открыть сайт', 'url': SITE_URL}]]}


def render(view, days):
    return {'top': report_top, 'par': report_par}.get(view, report_stats)(days)


HELP = ('👋 <b>Бот статистики olymp-notes</b>\n\nВыберите период и раздел кнопками — сообщение обновится на месте.\n\n'
        'Команды: /stats [дни] · /today · /top [дни] · /parallels [дни]')


def days_of(arg, default=7):
    try:
        return max(1, min(int(arg), 365))
    except (TypeError, ValueError):
        return default


def send(chat, view, days):
    tg('sendMessage', chat_id=chat, text=render(view, days), parse_mode='HTML',
       reply_markup=keyboard(view, days), disable_web_page_preview=True)


def handle(u):
    if 'callback_query' in u:
        cq = u['callback_query']
        view, d = cq['data'].split(':')
        try:
            tg('editMessageText', chat_id=cq['message']['chat']['id'], message_id=cq['message']['message_id'],
               text=render(view, int(d)), parse_mode='HTML', reply_markup=keyboard(view, int(d)),
               disable_web_page_preview=True)
        except urllib.error.HTTPError:
            pass   # «message is not modified»
        tg('answerCallbackQuery', callback_query_id=cq['id'])
        return
    msg = u.get('message') or {}
    text = (msg.get('text') or '').strip()
    if not text.startswith('/'):
        return
    cmd, _, arg = text.partition(' ')
    cmd = cmd.split('@')[0].lower()
    chat = msg['chat']['id']
    if cmd in ('/start', '/help'):
        tg('sendMessage', chat_id=chat, text=HELP, parse_mode='HTML', reply_markup=keyboard('stats', 7))
    elif cmd == '/stats':
        send(chat, 'stats', days_of(arg))
    elif cmd == '/today':
        send(chat, 'stats', 1)
    elif cmd == '/top':
        send(chat, 'top', days_of(arg))
    elif cmd in ('/parallels', '/par'):
        send(chat, 'par', days_of(arg))


def main():
    me = tg('getMe')['result']
    print(f'Бот @{me["username"]} запущен. Ctrl+C — остановить.', flush=True)
    tg('deleteWebhook')
    offset = None
    while True:
        try:
            ups = tg('getUpdates', timeout=50, offset=offset, allowed_updates=['message', 'callback_query'])['result']
        except Exception as e:
            print('ошибка опроса:', e, flush=True)
            time.sleep(5)
            continue
        for u in ups:
            offset = u['update_id'] + 1
            try:
                handle(u)
            except Exception as e:
                print('ошибка обработки:', repr(e), flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        for fn, a in ((report_stats, 7), (report_top, 30), (report_par, 30)):
            print(re.sub('<[^>]+>', '', fn(a)), '\n')
    else:
        main()
