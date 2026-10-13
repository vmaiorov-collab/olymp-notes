"""Иллюстрации для «Занятие 5. Параллель X — Корневые эвристики»."""
from kit import *


def fig_flow_paint():
    b = text(380, 24, "Раскраска: разрез в сети = выбор цветов клеток", 15)
    S, T = (60, 140), (700, 140)
    b += circle(*S, 24, "S", GREEN, 16) + circle(*T, 24, "T", RED, 16)
    cells = [(240, 70, "A"), (240, 210, "B"), (460, 70, "C"), (460, 210, "D")]
    for x, y, n in cells:
        b += circle(x, y, 22, n, BLUE, 15)
    for x, y, n in [(240, 70, 0), (240, 210, 1)]:
        b += line(S[0] + 22, S[1] + (-14 if y < 140 else 14), x - 22, y, GREEN, 2, arrow=True)
    for x, y, n in [(460, 70, 0), (460, 210, 1)]:
        b += line(x + 22, y, T[0] - 22, T[1] + (-14 if y < 140 else 14), RED, 2, arrow=True)
    b += line(262, 70, 438, 70, ORANGE, 2.5) + line(262, 210, 438, 210, ORANGE, 2.5)
    b += line(240, 94, 240, 186, ORANGE, 2.5) + line(460, 94, 460, 186, ORANGE, 2.5)
    b += text(120, 80, "белая → чёрная: цена", 11, GREEN, "middle") + text(600, 70, "чёрная → белая: цена", 11, RED)
    b += text(350, 60, "g", 13, ORANGE) + text(228, 142, "g", 13, ORANGE, "end")
    b += text(380, 270, "клетка в S — чёрная, в T — белая · соседи по разные стороны разреза платят штраф g", 13, TEXT)
    b += text(380, 294, "минимальный разрез = минимальная суммарная цена", 13, MUTED)
    return figure(svg(760, 310, b), "Каждая клетка — вершина. Рёбра из истока и в сток кодируют цену перекраски, двусторонние рёбра между соседями ёмкости g — штраф за границу цветов. Минимальный разрез даёт оптимальную картинку.")


def fig_flow_project():
    b = text(380, 24, "Выбор тем с зависимостями: разрез и бесконечные рёбра", 15)
    S, T = (60, 160), (700, 160)
    b += circle(*S, 24, "S", GREEN, 16) + circle(*T, 24, "T", RED, 16)
    pos = {"+3": (270, 70), "+1": (270, 160), "−2": (480, 250), "g": (270, 250)}
    b += circle(*pos["+3"], 24, "3", GREEN, 15) + circle(*pos["+1"], 24, "1", GREEN, 15)
    b += circle(*pos["g"], 24, "g", GREEN, 15) + circle(*pos["−2"], 24, "−2", RED, 14)
    b += line(84, 150, 246, 74, GREEN, 2, arrow=True) + text(150, 96, "3", 12, GREEN)
    b += line(84, 160, 246, 160, GREEN, 2, arrow=True) + text(160, 152, "1", 12, GREEN)
    b += line(84, 175, 246, 244, GREEN, 2, arrow=True) + text(150, 226, "x_g", 12, GREEN)
    b += line(504, 242, 676, 172, RED, 2, arrow=True) + text(610, 222, "2", 12, RED)
    b += line(294, 250, 454, 250, YELLOW, 3, arrow=True) + text(374, 240, "∞", 16, YELLOW)
    b += text(380, 296, "g → i с ёмкостью ∞: нельзя взять g и не взять i", 13, TEXT)
    b += text(380, 320, "ответ = сумма положительных − минимальный разрез", 13, MUTED)
    return figure(svg(760, 336, b), "Положительные темы соединены с истоком, отрицательные — со стоком. Бесконечное ребро g → i запрещает разрезать его, то есть выбрать g без i.")


def fig_flow_pathcover():
    b = text(380, 24, "Разбиение DAG на пути = паросочетание в двудольном графе", 15)
    xs, ys = (110, 300), 70
    b += text(xs[0] + 50, 54, "левые копии", 12, MUTED) + text(xs[1] + 50, 54, "правые копии", 12, MUTED)
    # слева DAG
    nodes = {1: (520, 90), 2: (620, 90), 3: (570, 190), 4: (680, 190)}
    for k, (x, y) in nodes.items():
        b += circle(x, y, 20, str(k), BLUE, 14)
    import math
    for a, c in [(1, 2), (1, 3), (2, 4), (3, 4)]:
        (x1, y1), (x2, y2) = nodes[a], nodes[c]
        d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        b += line(x1 + ux * 22, y1 + uy * 22, x2 - ux * 25, y2 - uy * 25, MUTED, 2, arrow=True)
    b += text(600, 240, "исходный DAG", 12, MUTED)
    for i in range(4):
        y = 80 + i * 50
        b += circle(xs[0], y, 18, str(i + 1), BLUE, 13) + circle(xs[1] + 100, y, 18, str(i + 1), ORANGE, 13)
    match = [(1, 2), (2, 4), (3, 4)]
    allE = [(1, 2), (1, 3), (2, 4), (3, 4)]
    for a, c in allE:
        col = GREEN if (a, c) in [(1, 2), (2, 4)] else EDGE
        b += line(xs[0] + 18, 80 + (a - 1) * 50, xs[1] + 82, 80 + (c - 1) * 50, col, 3 if col == GREEN else 1.5)
    b += text(380, 300, "пути: 1 → 2 → 4 и отдельно 3 · всего 4 − |паросочетание| = 4 − 2 = 2 пути", 13, TEXT)
    return figure(svg(760, 316, b), "Ребро i → j превращается в ребро между левой копией i и правой копией j. Каждое рёбрышко паросочетания склеивает два пути в один, поэтому число путей равно n минус размер паросочетания.")


def fig_heavy_light():
    b = text(380, 24, "Тяжёлые и лёгкие вершины: порог K по степени", 15)
    b += circle(150, 150, 36, "H", RED, 18)
    for i in range(5):
        a = -0.9 + i * 0.45
        import math
        x, y = 150 + 120 * math.cos(a + 0.0) + 60, 150 + 110 * math.sin(a)
        b += circle(x + 30, y, 14, "", BLUE) + line(184, 150, x + 16, y, EDGE, 1.5)
    b += text(150, 220, "степень > K: тяжёлая", 13, RED) + text(150, 238, "их не больше 2m/K", 12, MUTED)
    b += circle(500, 110, 22, "v", GREEN, 15)
    for i, (dx, dy) in enumerate([(-70, 50), (-20, 70), (40, 70), (90, 50)]):
        b += circle(500 + dx, 110 + dy, 12, "", BLUE) + line(500, 110 + 22, 500 + dx, 110 + dy - 12, EDGE, 1.5)
    b += text(500, 220, "степень ≤ K: лёгкая", 13, GREEN)
    b += cell(300, 262, 160, 36, "прибавить лёгкой: O(K)", GREEN, 12) + cell(470, 262, 270, 36, "прибавить тяжёлой: O(1) (запомнить)", RED, 12)
    b += cell(300, 306, 440, 36, "узнать значение: своё + ленивые от тяжёлых соседей, O(m/K)", YELLOW, 12)
    b += text(380, 372, "K = √m  →  каждая операция O(√m)", 14, TEXT)
    return figure(svg(760, 388, b), "Для лёгкой вершины обновляем всех соседей сразу, для тяжёлой — только пометку у неё. Тяжёлых мало, поэтому при запросе их можно перебрать.")


def fig_sqrt_blocks():
    b = text(380, 24, "Блочное разбиение массива: n = 16, K = 4", 15)
    vals = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3]
    W, X0, y = 42, 44, 90
    for i, v in enumerate(vals):
        blk = i // 4
        b += cell(X0 + i * W + blk * 8, y, W - 4, 40, str(v), [BLUE, GREEN, ORANGE, PURPLE][blk], 15)
    for blk in range(4):
        x = X0 + blk * (4 * W + 8)
        b += cell(x, y + 70, 4 * W - 4, 34, f"sum = {sum(vals[blk*4:blk*4+4])}", [BLUE, GREEN, ORANGE, PURPLE][blk], 14)
        b += line(x + 2 * W - 2, y + 40, x + 2 * W - 2, y + 70, MUTED, 1.5, arrow=True)
    l, r = 2, 12
    xl = X0 + l * W + (l // 4) * 8; xr = X0 + r * W + (r // 4) * 8 + W - 4
    b += f'<rect x="{xl - 3}" y="{y - 8}" width="{xr - xl + 6}" height="56" rx="8" fill="none" stroke="{YELLOW}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += text(380, 244, "запрос [2, 12]: хвост блока 0 + целые блоки 1, 2 + начало блока 3", 13, TEXT)
    b += text(380, 270, "≤ 2K отдельных элементов + ≤ n/K блоков", 13, MUTED)
    b += text(380, 300, "+x к a[i]: a[i] += x, sum[блок] += x — O(1)", 13, GREEN)
    return figure(svg(760, 316, b), "Сумма на отрезке — неполные края поэлементно и целые блоки по готовым суммам. Точечное прибавление трогает два числа.")


def fig_mo_moves():
    b = text(380, 24, "Алгоритм Мо: запросы (l, r) сортируются по блоку l, затем по r", 15)
    ox, oy, s = 70, 270, 5.2
    b += line(ox, oy, ox + 560, oy, AXIS, 2, arrow=True) + line(ox, oy, ox, oy - 220, AXIS, 2, arrow=True)
    b += text(ox + 556, oy + 22, "l", 13, MUTED) + text(ox - 14, oy - 214, "r", 13, MUTED)
    K = 20
    for k in range(1, 5):
        b += line(ox + k * K * s * 1.0 / 1, oy, ox + k * K * s, oy - 200, EDGE, 1, dash="4 4")
    import random
    rnd = random.Random(5)
    pts = []
    for blk in range(4):
        n = 5
        rs = sorted(rnd.randint(blk * K + 5, 78) for _ in range(n))
        if blk % 2: rs = rs[::-1]
        for r in rs:
            l = blk * K + rnd.randint(0, K - 1)
            pts.append((l, max(r, l + 1)))
    P = [(ox + l * s, oy - r * 2.2) for l, r in pts]
    for (x1, y1), (x2, y2) in zip(P, P[1:]):
        b += line(x1, y1, x2, y2, BLUE, 1.6)
    for x, y in P:
        b += f'<circle cx="{x}" cy="{y}" r="4" fill="{YELLOW}"/>'
    b += text(ox + 40 * s, oy - 206, "внутри блока: r монотонно (змейка) → всего n шагов", 12, GREEN)
    b += text(380, 308, "r: ≤ n на блок → n²/K · l: ≤ K на запрос → qK · K = n/√q → O(n√q)", 13, TEXT)
    return figure(svg(760, 324, b), "Запрос — точка (l, r). Обход точек блок за блоком: указатель r проходит каждый блок один раз, указатель l в блоке прыгает не дальше чем на K.")


def fig_euler_path():
    b = text(380, 24, "Мо на дереве: рёбра в эйлеровом обходе встречаются дважды", 15)
    nd = {"1": (130, 70), "2": (60, 160), "3": (200, 160), "4": (130, 250), "5": (270, 250)}
    for a, c in [("1", "2"), ("1", "3"), ("3", "4"), ("3", "5")]:
        b += line(nd[a][0], nd[a][1], nd[c][0], nd[c][1], EDGE, 2)
    for k, (x, y) in nd.items():
        b += circle(x, y, 18, k, BLUE, 14)
    seq = ["1-2", "1-2", "1-3", "3-4", "3-4", "3-5", "3-5", "1-3"]
    W = 58
    cols = {"1-2": GREEN, "1-3": BLUE, "3-4": ORANGE, "3-5": PURPLE}
    for i, e in enumerate(seq):
        c = cols[e]
        inpath = e in ("1-3", "3-4") 
        b += cell(340 + (i % 4) * (W + 8), 70 + (i // 4) * 60, W, 40, e, c, 13)
    b += text(520, 54, "порядок обхода (вниз, вверх)", 12, MUTED)
    b += text(520, 210, "путь 2 → 4: берём отрезок обхода между двумя первыми входами", 12, TEXT)
    b += text(520, 232, "рёбра общего предка встречаются 2 раза — «гаснут»", 12, TEXT)
    b += text(520, 262, "в структуре — только числа с нечётным числом вхождений", 12, YELLOW)
    return figure(svg(760, 284, b), "Каждое ребро записано при спуске и при подъёме. Отрезок обхода между вершинами u и v содержит рёбра пути по одному разу, а все остальные — по два.")


def fig_mo_rollback():
    b = text(380, 24, "Мо без удалений: откат левого хвоста", 15)
    W, X0, y = 36, 40, 80
    for i in range(18):
        blk = i // 6
        b += cell(X0 + i * W + blk * 10, y, W - 3, 34, "", [BLUE, GREEN, ORANGE][blk], 12)
    b += text(X0 + 3 * W, y - 12, "блок t", 12, GREEN) + text(X0 + 3 * W + 6 * W + 10, y - 12, "блок t+1", 12, ORANGE)
    bx = X0 + 6 * W + 10
    b += cell(bx, y + 60, 6 * W - 3 + 6 * W + 10 - 6 * W, 28, "основная часть: от границы вправо, только добавляем (r растёт)", PURPLE, 12) if False else ""
    b += f'<rect x="{bx}" y="{y + 56}" width="{8 * W}" height="24" rx="6" fill="{SOFT[PURPLE]}" stroke="{PURPLE}" stroke-width="2"/>'
    b += text(bx + 4 * W, y + 73, "шаг 1: растёт r, только добавляем", 12)
    b += f'<rect x="{X0 + 2 * W}" y="{y + 92}" width="{4 * W + 10}" height="24" rx="6" fill="{SOFT[YELLOW]}" stroke="{YELLOW}" stroke-width="2"/>'
    b += text(X0 + 4 * W + 5, y + 109, "шаг 2: времен. слева ≤ K", 12)
    b += text(380, 208, "ответили → откатили левый хвост (последние добавленные удаляются первыми)", 13, TEXT)
    b += text(380, 234, "при смене блока структуру очищаем: O(n) на блок, всего O(n²/K)", 13, MUTED)
    return figure(svg(760, 250, b), "Структура, умеющая только добавлять, и стек откатов. Правая граница движется монотонно вправо внутри блока, левую часть добавляем на время запроса и откатываем.")
FIGS = {"flow_paint": fig_flow_paint, "flow_project": fig_flow_project, "flow_pathcover": fig_flow_pathcover,
        "heavy_light": fig_heavy_light, "sqrt_blocks": fig_sqrt_blocks, "mo_moves": fig_mo_moves,
        "euler_path": fig_euler_path, "mo_rollback": fig_mo_rollback}
