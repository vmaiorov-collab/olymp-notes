"""Иллюстрации и плеер для «Занятие 5. Параллель B — Дерево отрезков и разбор динамики»."""
import json
from kit import *


# ---------------------------------------------------------------- дерево отрезков: запрос get
def fig_seg_get():
    ql, qr = 2, 6                                            # запрос [2, 6) на массиве из 8 элементов
    W, H = 760, 330
    pos = {}
    def place(l, r, depth):
        x = 60 + (l + r) / 2 * 80 - 40 + 40 * 0                # центр над листьями
        pos[(l, r)] = (30 + (l + r) / 2 * 90, 50 + depth * 78)
        if r - l > 1:
            m = (l + r) // 2; place(l, m, depth + 1); place(m, r, depth + 1)
    place(0, 8, 0)
    def kind(l, r):
        if r <= ql or qr <= l: return "out"
        if ql <= l and r <= qr: return "in"
        return "split"
    body = text(380, 24, "Запрос get на [2, 6): зелёные — разделяемся, красные — берём значение, серые — сразу выходим", 14)
    edges = ""; nodes = ""
    for (l, r), (x, y) in pos.items():
        if r - l > 1:
            m = (l + r) // 2
            for c in ((l, m), (m, r)):
                if kind(l, r) == "split":                      # путь рекурсии проходит только из разделившихся вершин
                    cx, cy = pos[c]; edges += line(x, y + 16, cx, cy - 16, EDGE, 2)
    for (l, r), (x, y) in pos.items():
        k = kind(l, r)
        if not any(((l, r) == c) for c in pos): continue
        # вершины-дети разделившихся показываем, остальные скрываем (в них не заходим)
        parent_ok = (l, r) == (0, 8)
        for (pl, pr) in pos:
            if pr - pl > 1 and kind(pl, pr) == "split":
                m = (pl + pr) // 2
                if (l, r) in ((pl, m), (m, pr)): parent_ok = True
        if not parent_ok: continue
        col = GREEN if k == "split" else (RED if k == "in" else None)
        w = 52 if r - l > 1 else 40
        nodes += cell(x - w / 2, y - 16, w, 32, f"[{l},{r})" if r - l > 1 else str(l), col, 12 if r - l > 1 else 14)
    body += edges + nodes
    return figure(svg(W, H, body), "Посещённых вершин не больше $4\\log n$: все «зелёные» — предки самого левого или самого правого листа запроса, а из каждой зелёной вершины рекурсия идёт в двух детей.")


# ---------------------------------------------------------------- Фенвик: блоки
def fig_fenwick():
    n = 16; cw = 40; ox = 60
    body = text(380, 24, "Фенвик: в ячейке i лежит сумма a[i − lowbit(i) + 1 … i]", 15)
    for i in range(1, n + 1):
        body += cell(ox + (i - 1) * cw, 250, cw - 4, 30, str(i), None, 14)
    levels = {}
    for i in range(1, n + 1):
        lb = i & -i; levels.setdefault(lb, []).append(i)
    row = 0
    for lb in sorted(levels):
        for i in levels[lb]:
            x1 = ox + (i - lb) * cw; x2 = ox + i * cw - 4
            y = 232 - row * 30
            col = [BLUE, GREEN, ORANGE, PURPLE, RED][row]
            body += line(x1 + 2, y, x2, y, col, 5) + text((x1 + x2) / 2, y - 7, f"{i}", 11, col)
        row += 1
    body += text(380, 308, "блоки длин 1, 2, 4, 8, 16 — каждая ячейка отвечает за отрезок длины lowbit(i)", 13, MUTED)
    return figure(svg(760, 330, body), "Цвет — длина блока. Для префикса 13 берём ячейки 13, 12, 8: $13\\to12\\to8\\to0$ (каждый раз вычитаем младший бит).")


def algo_fenwick(x=13, n=16):
    frames = []; cur = x; got = []
    def draw(cur, got, note):
        s = text(380, 24, f"сумма на префиксе a[1..{x}]", 15)
        for i in range(1, n + 1):
            col = GREEN if i in got else (YELLOW if i == cur else None)
            s += cell(40 + (i - 1) * 42, 70, 38, 32, str(i), col, 14)
        for i in got:
            lb = i & -i
            s += line(40 + (i - lb) * 42 + 2, 128, 40 + i * 42 - 6, 128, GREEN, 5)
        s += text(380, 175, note, 14, MUTED)
        return s
    frames.append({"svg": draw(cur, got, ""), "msg": f"Начинаем с x = {x} (двоично {x:b}). Накопленная сумма пока пуста."})
    while cur > 0:
        got.append(cur); lb = cur & -cur
        frames.append({"svg": draw(cur, got, f"берём ячейку {cur}: блок длины {lb}"), "msg": f"Берём ячейку {cur}: она хранит сумму блока длины lowbit({cur}) = {lb}."})
        cur -= lb
        frames.append({"svg": draw(cur, got, f"x −= lowbit → {cur}"), "msg": f"Вычитаем младший бит: x = {cur}." + (" Дошли до нуля." if cur == 0 else "")})
    return {"title": f"Фенвик: сумма на префиксе {x}", "vb": "0 0 760 200", "frames": frames}


# ---------------------------------------------------------------- заметающая прямая
def fig_rect_sweep():
    b = text(380, 24, "Площадь объединения: сканирующая прямая и дерево отрезков по y", 15)
    ox, oy, s = 60, 50, 36
    for i in range(9):
        b += line(ox + i * s, oy, ox + i * s, oy + 7 * s, EDGE, 1)
    for j in range(8):
        b += line(ox, oy + j * s, ox + 8 * s, oy + j * s, EDGE, 1)
    b += f'<rect x="{ox + 1 * s}" y="{oy + 1 * s}" width="{4 * s}" height="{3 * s}" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'
    b += f'<rect x="{ox + 3 * s}" y="{oy + 2 * s}" width="{4 * s}" height="{3 * s}" fill="{SOFT[ORANGE]}" stroke="{ORANGE}" stroke-width="2"/>'
    b += line(ox + 4 * s + s / 2, oy - 6, ox + 4 * s + s / 2, oy + 7 * s + 6, YELLOW, 3, dash="6 4") + text(ox + 4.5 * s, oy + 7 * s + 24, "сканирующая прямая x", 12, YELLOW)
    cnt = [0, 1, 2, 2, 1, 1, 0]                             # покрытие по y на этой прямой
    for j, c in enumerate(cnt):
        b += cell(400, oy + j * s, 56, s - 4, str(c), GREEN if c == 0 else (ORANGE if c == 2 else BLUE), 16)
    b += text(428, oy - 8, "в дереве по y", 12, MUTED)
    b += text(470, oy + 70, "считаем клетки с нулём:", 14, anchor="start") + text(470, oy + 95, "минимум и сколько раз он встречается", 13, MUTED, anchor="start")
    b += text(470, oy + 140, "занято = всего − нулей", 14, YELLOW, anchor="start")
    return figure(svg(760, 360, b), "Прямоугольник открывается событием «+1 на [y1, y2)», закрывается событием «−1 на [y1, y2)». Клетка занята, если в ней число больше нуля.")


# ---------------------------------------------------------------- переподвешивание
def fig_reroot():
    b = text(380, 24, "Ответ для ребёнка через ответ для родителя", 15)
    b += circle(380, 70, 22, "p", BLUE) + circle(250, 170, 22, "u", GREEN) + circle(510, 170, 22, "", None)
    b += line(367, 88, 262, 152, EDGE, 3) + line(393, 88, 498, 152, EDGE, 3) + text(300, 106, "w", 16, YELLOW)
    b += f'<ellipse cx="250" cy="225" rx="70" ry="30" fill="{SOFT[GREEN]}" stroke="{GREEN}" stroke-width="2"/>' + text(250, 230, "поддерево u: sz[u]", 13)
    b += f'<ellipse cx="515" cy="225" rx="88" ry="30" fill="{SOFT[ORANGE]}" stroke="{ORANGE}" stroke-width="2"/>' + text(515, 230, "остальные: n − sz[u]", 13)
    b += text(380, 285, "ans[u] = ans[p] − w·sz[u] + w·(n − sz[u])", 17, YELLOW, mono=True)
    b += text(380, 312, "вершины поддерева u стали ближе на w, все остальные — дальше на w", 13, MUTED)
    return figure(svg(760, 330, b), "Переход по ребру $(p,u)$ длины $w$ меняет расстояние до каждой вершины ровно на $\\pm w$.")


# ---------------------------------------------------------------- вложенная покраска
def fig_fence():
    b = text(380, 24, "Покраска: пересекающиеся отрезки не нужны, достаточно вложенных", 15)
    cols = [BLUE, ORANGE, GREEN, ORANGE, BLUE]
    for i, c in enumerate(cols):
        b += cell(80 + i * 120, 140, 110, 40, "", c)
    b += f'<rect x="76" y="62" width="608" height="26" rx="6" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>' + text(380, 80, "1) всё в синий", 13)
    b += f'<rect x="196" y="94" width="368" height="26" rx="6" fill="{SOFT[ORANGE]}" stroke="{ORANGE}" stroke-width="2"/>' + text(380, 112, "2) середину в оранжевый", 13)
    b += f'<rect x="316" y="126" width="128" height="8" rx="3" fill="{SOFT[GREEN]}" stroke="{GREEN}" stroke-width="2"/>' + text(380, 202, "3) центр в зелёный", 13, GREEN)
    b += text(380, 250, "красим сверху вниз: сначала большой отрезок, потом вложенные в него", 14, MUTED)
    return figure(svg(760, 270, b), "Цвета досок 1-2-3-2-1: три операции. Это интервальная динамика по отрезкам $[l, r]$.")


# ---------------------------------------------------------------- циклы подарков
def fig_gifts():
    b = text(380, 24, "Подарки: каждый дарит следующему по циклу; «не принёс» ломает двоих", 15)
    import math
    def cyc(cx, cy, n, nobring, title_lines):
        if isinstance(title_lines, str):
            title_lines = [title_lines]
        out = ""
        for i, line_s in enumerate(title_lines):
            out += text(cx, cy - 90 + i * 14, line_s, 11, MUTED)
        pts = [(cx + 52 * math.cos(2 * math.pi * i / n - math.pi / 2), cy + 52 * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
        for i in range(n):
            x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
            dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy)
            out += line(x1 + dx / d * 17, y1 + dy / d * 17, x2 - dx / d * 17, y2 - dy / d * 17, EDGE, 2, arrow=True)
        for i, (x, y) in enumerate(pts):
            lost = i in nobring or ((i - 1) % n) in nobring
            col = RED if i in nobring else (ORANGE if lost else GREEN)
            out += circle(x, y, 16, str(i + 1), col, 13)
        return out
    b += cyc(170, 160, 4, {0, 2}, ["чётный цикл: через одного —", "теряются все 4"])
    b += cyc(380, 160, 5, {0, 2}, ["нечётный: 2 не принесли —", "теряются 4 из 5"])
    b += cyc(590, 160, 3, {0, 1, 2}, ["весь цикл:", "теряются только 3"])
    b += text(380, 275, "красный — не принёс, оранжевый — не получил из-за соседа, зелёный — получил", 13, MUTED)
    return figure(svg(760, 295, b), "Максимум потерь — расставить не принёсших через одного; минимум — брать циклы целиком.")


FIGS = {"seg_get": fig_seg_get, "fenwick": fig_fenwick, "rect_sweep": fig_rect_sweep, "reroot": fig_reroot, "fence": fig_fence, "gifts": fig_gifts}


def algos_js():
    data = {"fenwick": algo_fenwick()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
