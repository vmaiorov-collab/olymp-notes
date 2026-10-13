"""Иллюстрации для «Занятие 5. Параллель XS — Структуры данных 1»."""
from kit import *


def fig_lazy_push():
    b = text(380, 24, "Ленивое прибавление: add[v] — «ещё не передано сыновьям»", 15)
    def panel(ox, title, pushed):
        o = text(ox + 180, 56, title, 12, MUTED)
        P = {"r": (ox + 170, 100), "l": (ox + 90, 190), "q": (ox + 250, 190)}
        for k, (x, y) in {"a": (ox + 50, 280), "b": (ox + 130, 280), "c": (ox + 210, 280), "d": (ox + 290, 280)}.items():
            pass
        leaves = [(ox + 50, 280), (ox + 130, 280), (ox + 210, 280), (ox + 290, 280)]
        o += line(*P["r"], *P["l"], EDGE, 2) + line(*P["r"], *P["q"], EDGE, 2)
        o += line(P["l"][0], P["l"][1], leaves[0][0], leaves[0][1], EDGE, 2) + line(P["l"][0], P["l"][1], leaves[1][0], leaves[1][1], EDGE, 2)
        o += line(P["q"][0], P["q"][1], leaves[2][0], leaves[2][1], EDGE, 2) + line(P["q"][0], P["q"][1], leaves[3][0], leaves[3][1], EDGE, 2)
        o += cell(P["r"][0] - 62, P["r"][1] - 22, 124, 44, "sum = 14", BLUE, 14)
        o += cell(P["l"][0] - 62, P["l"][1] - 22, 124, 44, "sum = 12" , YELLOW if not pushed else BLUE, 14)
        o += text(P["l"][0] - 48, P["l"][1] - 30, "add = 0" if pushed else "add = +5", 13, GREEN if pushed else YELLOW)
        o += cell(P["q"][0] - 62, P["q"][1] - 22, 124, 44, "sum = 2", BLUE, 14)
        vals = [(1 + 5, 6), (1 + 5, 6), (1, 1), (1, 1)] if pushed else [(1, 1), (1, 1), (1, 1), (1, 1)]
        for i, (x, y) in enumerate(leaves):
            col = GREEN if (pushed and i < 2) else BLUE
            o += cell(x - 28, y - 18, 56, 36, str(vals[i][0]), col, 15)
        if not pushed:
            o += text(ox + 70, 330, "листья пока старые (1, 1)", 12, RED)
        else:
            o += text(ox + 70, 330, "после push листья 6, 6", 12, GREEN)
        return o
    b += panel(0, "+5 на [0, 1]: сумма верна, дети не знают", False)
    b += panel(380, "push(v): add передан детям и обнулён", True)
    b += text(380, 360, "sum[левого] = 2·(1) + 2·5 = 12 сразу, а в листья 5 уйдёт позже", 13, TEXT)
    return figure(svg(760, 380, b), "Прибавление остановилось в накрытой вершине: её сумма сразу верна, а детям оставлена пометка add. Вызов push перед любым спуском вниз передаёт пометку детям.")


def fig_rect_sweep():
    b = text(380, 24, "Площадь объединения: заметающая прямая и полоски по y", 15)
    ox, oy, W, H = 40, 40, 400, 240
    b += f'<rect x="{ox}" y="{oy}" width="{W}" height="{H}" rx="8" fill="{NODE}" stroke="{EDGE}"/>'
    rects = [(40, 40, 200, 150, BLUE), (120, 110, 300, 210, GREEN), (250, 20, 360, 120, ORANGE)]
    for x1, y1, x2, y2, c in rects:
        b += f'<rect x="{ox + x1}" y="{oy + y1}" width="{x2 - x1}" height="{y2 - y1}" fill="{SOFT[c]}" stroke="{c}" stroke-width="2" opacity="0.85"/>'
    sx = 180
    b += line(ox + sx, oy - 6, ox + sx, oy + H + 6, YELLOW, 3, dash="6 4")
    b += text(ox + sx, oy + H + 24, "x", 14, YELLOW)
    # полоски y
    ys = [20, 40, 110, 120, 150, 210]
    counts = {(20, 40): 0, (40, 110): 1, (110, 120): 2, (120, 150): 2, (150, 210): 1}
    px = 480
    b += text(px + 100, 54, "число накрывающих", 12, MUTED)
    for (y1, y2), c in counts.items():
        col = GREEN if c else None
        b += cell(px, oy + y1, 90, y2 - y1 - 2 if y2 - y1 > 8 else y2 - y1, str(c) if y2 - y1 > 12 else "", col, 13)
        b += f'<rect x="{ox + sx - 2}" y="{oy + y1}" width="4" height="{y2 - y1}" fill="{GREEN if c else RED}" opacity="0.9"/>'
    b += text(px + 100, oy + 236, "вес полоски — её длина", 12, TEXT)
    b += text(380, 306, "ненулевые = всё минус вес минимумов при min = 0", 13, TEXT)
    b += text(380, 332, "площадь += (покрытая длина) · (x_следующее − x_текущее)", 14, YELLOW)
    return figure(svg(760, 348, b), "Между соседними x набор покрытых полосок постоянен. В дереве хранится минимум числа накрытий и вес минимумов; нулевые полоски — те, где минимум равен нулю.")


def fig_fenwick_ranges():
    b = text(380, 24, "Дерево Фенвика: ячейка i хранит сумму на (i − lowbit(i), i]", 15)
    W, X0, Y0 = 70, 70, 52
    for i in range(1, 9):
        b += cell(X0 + (i - 1) * W, Y0, W - 6, 34, str(i), None, 15)
    for i in range(1, 9):
        lb = i & -i
        lvl = {1: 0, 2: 1, 4: 2, 8: 3}[lb]
        y = Y0 + 56 + lvl * 34
        x1 = X0 + (i - lb) * W; x2 = X0 + i * W - 6
        qcol = {7: GREEN, 6: GREEN, 4: GREEN}.get(i, BLUE)
        b += f'<rect x="{x1 + 2}" y="{y}" width="{x2 - x1 - 2}" height="24" rx="6" fill="{SOFT[qcol]}" stroke="{qcol}" stroke-width="2"/>'
        b += text((x1 + x2) / 2, y + 17, f"t[{i}]", 13)
    b += text(380, 252, "pref(7) = t[7] + t[6] + t[4]:  7 → 6 → 4 → 0  (убираем младший бит)", 14, GREEN)
    b += text(380, 278, "add(5): 5 → 6 → 8  (прибавляем младший бит) — обновляются t[5], t[6], t[8]", 14, YELLOW)
    return figure(svg(760, 296, b), "Ячейки разной «ширины»: длина промежутка равна младшему биту номера. Префикс собирается из O(log n) промежутков, обновление идёт по тем, что содержат изменяемый элемент.")


def fig_mst_cascade():
    b = text(380, 24, "Каскадирование: одна позиция в корне задаёт позиции в сыновьях", 15)
    root = [1, 2, 3, 5, 6, 7, 8, 9]; src = "RLRLRRLL"
    left = [2, 5, 8, 9]; right = [1, 3, 6, 7]
    W = 62
    X0 = 130
    for i, v in enumerate(root):
        b += cell(X0 + i * W, 60, W - 6, 36, str(v), BLUE if src[i] == "L" else GREEN, 15)
        b += text(X0 + i * W + (W - 6) / 2, 112, str(i), 11, MUTED)
    b += text(X0 - 14, 84, "корень", 13, MUTED, "end")
    for i, v in enumerate(left):
        b += cell(150 + i * W, 220, W - 6, 36, str(v), BLUE, 15)
        b += text(150 + i * W + (W - 6) / 2, 272, str(i), 11, MUTED)
    for i, v in enumerate(right):
        b += cell(430 + i * W, 220, W - 6, 36, str(v), GREEN, 15)
        b += text(430 + i * W + (W - 6) / 2, 272, str(i), 11, MUTED)
    b += text(136, 244, "левый сын", 13, BLUE, "end") + text(716, 244, "", 13)
    b += text(560, 300, "правый сын", 13, GREEN)
    p = 3
    b += f'<rect x="{X0 + p * W - 3}" y="56" width="{W}" height="44" rx="8" fill="none" stroke="{YELLOW}" stroke-width="3"/>'
    b += text(X0 + p * W + 28, 40, "x = 4: первый ≥ 4 стоит на позиции 3", 13, YELLOW)
    lpos, rpos = 1, 2
    b += line(X0 + p * W + 20, 100, 150 + lpos * W + 26, 218, BLUE, 2.5, arrow=True)
    b += line(X0 + p * W + 40, 100, 430 + rpos * W + 26, 218, GREEN, 2.5, arrow=True)
    b += text(210, 168, "toL[3] = 1 из первых 3", 12, BLUE) 
    b += text(560, 168, "3 − 1 = 2", 12, GREEN)
    b += text(380, 328, "в левом сыне позиция 1 (значение 5), в правом — 2 (значение 6): бинпоиск не нужен", 13, TEXT)
    return figure(svg(760, 344, b), "Массив корня — слияние массивов сыновей. Для каждой позиции заранее запомнено, сколько из первых элементов пришло слева; по одной найденной позиции получаются позиции в обоих сыновьях.")


def fig_cdq_four():
    b = text(380, 24, "Четырёхмерное доминирование: разделяй и властвуй по a", 15)
    # левая часть: две половины и слияние по b
    b += cell(40, 50, 150, 34, "левая: a меньше", BLUE, 13) + cell(200, 50, 150, 34, "правая: a больше", GREEN, 13)
    b += text(195, 106, "решили рекурсивно обе половины", 12, MUTED)
    seq = [("L", 1), ("R", 2), ("L", 3), ("R", 4), ("R", 5), ("L", 6)]
    W = 56
    for i, (s, v) in enumerate(seq):
        c = BLUE if s == "L" else GREEN
        b += cell(40 + i * W, 140, W - 6, 34, f"{s}{v}", c, 13)
    b += text(195, 132, "слили по b (возрастание)", 12, MUTED)
    b += line(40 + 5 * W + 24, 190, 40 + 0 * W + 24, 190, YELLOW, 2.5, arrow=True)
    b += text(195, 212, "идём справа налево: по убыванию b", 12, YELLOW)
    b += text(195, 250, "R → добавить (c, d) в структуру", 13, GREEN)
    b += text(195, 274, "L → спросить: есть ли c' > c и d' > d?", 13, BLUE)
    # правая часть: ступенчатая структура
    ox, oy, w, h = 440, 50, 280, 240
    b += f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="8" fill="{NODE}" stroke="{EDGE}"/>'
    b += text(ox + w / 2, oy - 10, "структура по (c, d): ступенька", 13, MUTED)
    pts = [(40, 190), (90, 140), (150, 90), (215, 50)]
    path = f"M {ox + 20} {oy + 190}"
    for (x, y) in pts:
        pass
    for x, y in pts:
        b += f'<circle cx="{ox + x}" cy="{oy + y}" r="6" fill="{GREEN}"/>'
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        b += line(ox + x1, oy + y1, ox + x2, oy + y1, GREEN, 1.5, dash="4 3") + line(ox + x2, oy + y1, ox + x2, oy + y2, GREEN, 1.5, dash="4 3")
    b += f'<circle cx="{ox + 100}" cy="{oy + 190}" r="7" fill="{RED}"/>'
    b += text(ox + 100, oy + 216, "нас убивают", 12, RED)
    b += f'<circle cx="{ox + 70}" cy="{oy + 60}" r="7" fill="{BLUE}"/>'
    b += text(ox + 70, oy + 44, "выживает", 12, BLUE)
    b += text(ox + w - 6, oy + h - 8, "c →", 12, MUTED, "end") + text(ox + 10, oy + 16, "d ↑", 12, MUTED, "start")
    b += text(380, 330, "O(n log n) на уровень рекурсии, всего O(n log² n)", 13, TEXT)
    return figure(svg(760, 346, b), "Левые элементы может убить только правая половина. Слияние по b даёт порядок обработки, а ступенчатая структура по (c, d) отвечает на вопрос «есть ли точка строго правее и выше».")


def fig_dfs_index():
    b = text(380, 24, "Нумерация в порядке обхода в глубину: левый x + 1, правый x + 2·(размер левого)", 15)
    n = 6
    nodes = []
    def go(x, l, r, d):
        nodes.append((x, l, r, d))
        if r - l == 1: return
        m = (l + r) // 2
        go(x + 1, l, m, d + 1); go(x + 2 * (m - l), m, r, d + 1)
    go(0, 0, n, 0)
    pos = {}
    for x, l, r, d in nodes:
        pos[(l, r)] = ((l + r) / 2 / n * 640 + 60, 70 + d * 62, x)
    for x, l, r, d in nodes:
        if r - l > 1:
            m = (l + r) // 2
            for ch in ((l, m), (m, r)):
                b += line(pos[(l, r)][0], pos[(l, r)][1], pos[ch][0], pos[ch][1], EDGE, 2)
    for x, l, r, d in nodes:
        px, py, _ = pos[(l, r)]
        b += circle(px, py, 19, str(x), BLUE if r - l > 1 else GREEN, 14)
        b += text(px, py + 36, f"[{l},{r})", 11, MUTED)
    b += text(380, 326, "ячейки 0 … 2n − 2 используются ровно по разу, пропусков нет", 13, TEXT)
    return figure(svg(760, 344, b), "Для n = 6: у левого поддерева 2s − 1 вершин (s — число листьев), так что правый сын идёт сразу за ним. Вершины соседних уровней лежат рядом в памяти.")


def fig_mex_stack():
    b = text(380, 24, "mex = max + 1 ⇔ max + 1 − distinct = 0, массив v для фиксированного R", 15)
    a = [3, 0, 2, 1, 1]
    X0, W = 170, 100
    labels = ["a[i]", "max(a[i..R])", "distinct(a[i..R])", "v = max + 1 − distinct"]
    mx = [3, 2, 2, 1, 1]; di = [4, 3, 2, 1, 1]
    v = [mx[i] + 1 - di[i] for i in range(5)]
    for r, lab in enumerate(labels):
        y = 60 + r * 50
        b += text(X0 - 14, y + 22, lab, 12, MUTED, "end")
        for i in range(5):
            val = [a[i], mx[i], di[i], v[i]][r]
            col = None
            if r == 1: col = [BLUE, ORANGE, ORANGE, PURPLE, PURPLE][i]
            if r == 3: col = GREEN if v[i] == 0 else RED
            b += cell(X0 + i * W, y, W - 8, 34, str(val), col, 15)
    for i in range(5):
        b += text(X0 + i * W + (W - 8) / 2, 52, f"i = {i}", 11, MUTED)
    b += text(380, 282, "стек блоков суффиксных максимумов: [0] (3), [1..2] (2), [3..4] (1)", 13, TEXT)
    b += text(380, 306, "новый x: v −= 1 на (prev(x), R]; блоки с max ≤ x сливаются, на них v += x − старый max", 13, YELLOW)
    b += text(380, 330, "ответ на [L, R]: минимум v и число минимумов; если минимум = 0, то ответ — это число", 13, GREEN)
    return figure(svg(760, 348, b), "Зелёные клетки — позиции, для которых на суффиксе есть все числа от 0 до максимума. Нулей среди неотрицательных v ищем как «минимум и число минимумов».")


def fig_or_points():
    b = text(380, 24, "OR строго возрастает: группы начал и точки (j, y) с весами dp", 15)
    # слева: группы для фиксированного правого конца
    a = [4, 1, 2, 8, 1]
    X0, W = 40, 62
    for i, v in enumerate(a):
        b += cell(X0 + i * W, 60, W - 6, 34, str(v), None, 15)
        b += text(X0 + i * W + (W - 6) / 2, 110, f"{i + 1}", 11, MUTED)
    ors = [15, 11, 11, 9, 1]
    cols = [RED, ORANGE, ORANGE, YELLOW, GREEN]
    for i, v in enumerate(ors):
        b += cell(X0 + i * W, 128, W - 6, 28, str(v), cols[i], 13)
    b += text(X0 + 2.5 * W, 52, "a", 12, MUTED) 
    b += text(X0 + 2.5 * W - 20, 174, "OR(a[p..5]) для начал p — не больше log A значений", 12, MUTED)
    # справа: плоскость
    ox, oy, w, h = 400, 50, 330, 230
    b += f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="8" fill="{NODE}" stroke="{EDGE}"/>'
    b += f'<rect x="{ox + 120}" y="{oy + 100}" width="110" height="{h - 100}" fill="{SOFT[YELLOW]}" stroke="{YELLOW}" stroke-width="2" stroke-dasharray="6 4" opacity="0.9"/>'
    import random
    rnd = random.Random(2)
    for j in range(1, 9):
        for _ in range(rnd.randint(1, 3)):
            y = rnd.randint(16, h - 16)
            b += f'<circle cx="{ox + 20 + j * 34}" cy="{oy + y}" r="4" fill="{BLUE}"/>'
    b += text(ox + w / 2, oy + h + 18, "j  →", 12, MUTED)
    b += text(ox + 14, oy + 12, "y ↑", 12, MUTED, "start")
    b += text(ox + 175, oy + 92, "j ∈ [l_x, r_x],  y < x", 12, YELLOW)
    b += text(380, 318, "dp[i][x] = сумма весов в прямоугольнике = F(r_x, x) − F(l_x − 1, x)", 13, TEXT)
    b += text(380, 342, "заметаем по j, в Фенвике по y храним суммы добавленных точек", 13, GREEN)
    return figure(svg(760, 360, b), "Для фиксированного правого конца значений OR не больше log A, и каждому соответствует промежуток j. Состояния динамики — точки плоскости, запрос — прямоугольник, считаем оффлайн заметающей прямой.")


FIGS = {"lazy_push": fig_lazy_push, "rect_sweep": fig_rect_sweep, "fenwick_ranges": fig_fenwick_ranges,
        "mst_cascade": fig_mst_cascade, "cdq_four": fig_cdq_four, "dfs_index": fig_dfs_index,
        "mex_stack": fig_mex_stack, "or_points": fig_or_points}
