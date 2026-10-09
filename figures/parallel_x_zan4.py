"""Иллюстрации и плеер для «Занятие 3. Параллель X — Введение в потоки»."""
import json, math
from kit import *


def edge(x1, y1, x2, y2, label="", color=EDGE, w=2.5, r=22, curve=0, lab_dy=-8, lab_color=None, dash=None):
    dx, dy = x2 - x1, y2 - y1; d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    sx, sy = x1 + ux * r, y1 + uy * r; ex, ey = x2 - ux * (r + 4), y2 - uy * (r + 4)
    out = line(sx, sy, ex, ey, color, w, dash=dash, arrow=True)
    if label:
        mx, my = (sx + ex) / 2 - uy * 14 * (1 if curve == 0 else curve), (sy + ey) / 2 + ux * 14 * (1 if curve == 0 else curve) + lab_dy + 6
        out += text(mx, my, label, 13, lab_color or color)
    return out


# ---------------------------------------------------------------- сеть с потоком и разрезом
def fig_flow_example():
    b = text(380, 26, "Сеть: на рёбрах «поток / пропускная способность»", 15)
    P = {"s": (90, 150), "a": (290, 70), "b": (290, 230), "t": (630, 150)}
    b += edge(*P["s"], *P["a"], "2/3", BLUE) + edge(*P["s"], *P["b"], "1/2", BLUE)
    b += edge(*P["a"], *P["t"], "2/2", GREEN) + edge(*P["b"], *P["t"], "1/4", BLUE) + edge(*P["a"], *P["b"], "0/1", EDGE)
    b += line(470, 20, 470, 270, YELLOW, 3, dash="7 5") + text(470, 290, "ST-разрез: S слева, T справа", 13, YELLOW)
    for k, (x, y) in P.items():
        b += circle(x, y, 22, k, GREEN if k in "st" else None, 17)
    b += text(380, 318, "поток через разрез = 2 + 1 = 3 = величина потока; пропускная способность разреза = 2 + 4 = 6", 13, MUTED)
    return figure(svg(760, 336, b), "Поток через любой ST-разрез равен величине потока, а величина потока не превосходит пропускной способности каждого разреза.")


# ---------------------------------------------------------------- зачем нужны обратные рёбра
def fig_reverse():
    b = text(380, 26, "Все рёбра с пропускной способностью 1: жадный путь мешает, обратное ребро помогает", 15)
    def net(ox, flows, title, highlight=None):
        P = {"s": (ox, 150), "a": (ox + 110, 70), "b": (ox + 110, 230), "t": (ox + 220, 150)}
        out = text(ox + 110, 56 - 30, title, 13, MUTED)
        spec = [("s", "a"), ("s", "b"), ("a", "b"), ("a", "t"), ("b", "t")]
        for u, v in spec:
            f = flows.get((u, v), 0)
            col = ORANGE if (highlight and (u, v) in highlight) else (GREEN if f else EDGE)
            out += edge(*P[u], *P[v], f"{f}/1", col, w=3 if f else 2, r=18, lab_color=col)
        for k, (x, y) in P.items(): out += circle(x, y, 18, k, GREEN if k in "st" else None, 15)
        return out
    b += net(40, {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}, "1-й путь: s→a→b→t")
    b += net(280, {("s", "a"): 1, ("a", "b"): 1, ("b", "t"): 1}, "ищем ещё путь: s→b→(a)→t", highlight={("s", "b"), ("a", "b"), ("a", "t")})
    b += net(520, {("s", "a"): 1, ("s", "b"): 1, ("a", "t"): 1, ("b", "t"): 1}, "итог: поток 2")
    b += text(380, 295, "второй путь идёт по ребру a→b против потока — «отменяет» его; без обратных рёбер максимального потока не найти", 13, MUTED)
    return figure(svg(760, 320, b), "Если искать путь только по прямым рёбрам, застрянем на потоке 1. Обратное ребро с остаточной способностью 1 позволяет отменить поток по $a\\to b$.")


# ---------------------------------------------------------------- слоистая сеть Диница
def fig_layers():
    b = text(380, 26, "BFS строит слои; поток проталкивается только вдоль рёбер «на слой дальше»", 15)
    layers = [["s"], ["a", "b"], ["c", "d", "e"], ["t"]]
    X = [70, 270, 470, 670]; pos = {}
    for i, L in enumerate(layers):
        for j, v in enumerate(L):
            pos[v] = (X[i], 80 + (j + (3 - len(L)) / 2) * 80 + 20)
    good = [("s", "a"), ("s", "b"), ("a", "c"), ("a", "d"), ("b", "d"), ("b", "e"), ("c", "t"), ("d", "t"), ("e", "t")]
    for u, v in good: b += edge(*pos[u], *pos[v], "", BLUE, w=2.5, r=18)
    b += edge(*pos["d"], *pos["c"], "", EDGE, w=2, r=18, dash="4 4") + edge(*pos["c"], *pos["a"], "", EDGE, w=2, r=18, dash="4 4")
    for i, x in enumerate(X): b += text(x, 55, f"слой {i}", 13, MUTED)
    for v, (x, y) in pos.items(): b += circle(x, y, 18, v, GREEN if v in "st" else None, 15)
    b += text(380, 300, "сплошные — рёбра слоистой сети (dist[to] = dist[from] + 1); пунктир — рёбра внутри слоя и назад: их Диниц игнорирует", 12, MUTED)
    return figure(svg(760, 320, b), "Блокирующий поток ищется DFS по слоистой сети; указатель ptr у вершины запоминает ребро, с которого продолжать, чтобы не обходить безнадёжные рёбра заново.")


# ---------------------------------------------------------------- вершинное ограничение
def fig_split():
    b = text(380, 26, "Ограничение потока через вершину — раздвоение вершины", 15)
    b += circle(110, 120, 24, "x", BLUE, 18) + text(110, 168, "вершина с ограничением c", 12, MUTED)
    b += line(150, 120, 230, 120, YELLOW, 3, arrow=True)
    b += circle(330, 120, 20, "x₁", None, 15) + circle(520, 120, 20, "x₂", None, 15)
    b += line(352, 120, 496, 120, ORANGE, 4, arrow=True) + text(424, 106, "ёмкость c", 14, ORANGE)
    for dy in (-45, 45):
        b += line(250, 120 + dy, 312, 120 + dy * 0.3, EDGE, 2.5, arrow=True) + line(540, 120 + dy * 0.3, 610, 120 + dy, EDGE, 2.5, arrow=True)
    b += text(280, 62, "входящие", 12, MUTED) + text(590, 62, "исходящие", 12, MUTED)
    b += text(380, 215, "все входящие рёбра идут в x₁, все исходящие выходят из x₂; новое ребро x₁→x₂ ограничивает поток", 13, MUTED)
    b += text(380, 240, "работает для ориентированного графа; неориентированное ребро сначала заменяют двумя ориентированными", 13, MUTED)
    return figure(svg(760, 260, b), "Если рёбра сделать бесконечными, а вершины — единичными, потоки превращаются в непересекающиеся по вершинам пути.")


# ---------------------------------------------------------------- паросочетание
def fig_matching():
    b = text(380, 26, "Паросочетание = поток: исток → левая доля → правая доля → сток", 15)
    L = [(230, 70 + i * 60) for i in range(4)]; R = [(530, 70 + i * 60) for i in range(4)]
    b += circle(60, 160, 22, "s", GREEN, 17) + circle(700, 160, 22, "t", GREEN, 17)
    for p in L: b += edge(60, 160, *p, "", EDGE, 2, r=22)
    for p in R: b += edge(*p, 700, 160, "", EDGE, 2, r=18)
    match = [(0, 1), (1, 0), (2, 2)]; other = [(0, 0), (1, 1), (2, 3), (3, 2), (3, 3)]
    for i, j in other: b += edge(*L[i], *R[j], "", EDGE, 1.5, r=16, dash="3 4")
    for i, j in match: b += edge(*L[i], *R[j], "", ORANGE, 4, r=16)
    for p in L: b += circle(*p, 16, "", None)
    for p in R: b += circle(*p, 16, "", None)
    b += text(230, 52, "левая доля", 13, MUTED) + text(530, 52, "правая доля", 13, MUTED)
    b += text(380, 320, "все рёбра у истока и стока — ёмкость 1; рёбра посередине можно сделать бесконечными", 13, MUTED)
    return figure(svg(760, 340, b), "Оранжевые рёбра — паросочетание: по ним течёт единица потока. Алгоритм Куна — это Форд—Фалкерсон на такой сети.")


# ---------------------------------------------------------------- таблица 0/1
def fig_table():
    b = text(380, 26, "Таблица 0/1 с ограничениями на суммы строк и столбцов", 15)
    rows = [(160, 80, 3), (160, 140, 2), (160, 200, 3)]; cols = [(540, 70, 2), (540, 130, 3), (540, 190, 1), (540, 250, 2)]
    b += circle(50, 160, 20, "s", GREEN, 16) + circle(710, 160, 20, "t", GREEN, 16)
    for x, y, a in rows: b += edge(50, 160, x, y, f"a={a}", BLUE, 2.5, r=20, lab_color=BLUE) + circle(x, y, 18, "", BLUE)
    for x, y, bb in cols: b += edge(x, y, 710, 160, f"b={bb}", GREEN, 2.5, r=18, lab_color=GREEN) + circle(x, y, 18, "", GREEN)
    for _, ry, _ in rows:
        for _, cy, _ in cols: b += line(178, ry, 522, cy, EDGE, 1, dash="2 5")
    b += text(350, 300, "ребро строка → столбец с ёмкостью 1 — клетка; поток по нему = число в клетке (0 или 1)", 13, MUTED)
    return figure(svg(760, 320, b), "Максимальный поток равен максимальному числу единиц. Но сеть огромна, поэтому ответ ищут как минимальный разрез.")


# ---------------------------------------------------------------- банки по кругу
def fig_ring():
    b = text(380, 26, "Банки по кругу: деньги a, лимит сохранения b, перевод c", 15)
    n = 6; cx, cy, R = 380, 180, 100
    pts = [(cx + R * math.cos(2 * math.pi * i / n - math.pi / 2), cy + R * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        b += edge(x1, y1, x2, y2, "c", ORANGE, 2.5, r=16, lab_color=ORANGE)
    for i, (x, y) in enumerate(pts): b += circle(x, y, 16, str(i + 1), BLUE, 13)
    b += circle(110, 180, 22, "s", GREEN, 16) + circle(650, 180, 22, "t", GREEN, 16)
    b += edge(110, 180, *pts[5], "a", BLUE, 2, r=22, lab_color=BLUE) + edge(110, 180, *pts[4], "", BLUE, 2, r=22)
    b += edge(*pts[1], 650, 180, "b", GREEN, 2, r=16, lab_color=GREEN) + edge(*pts[2], 650, 180, "", GREEN, 2, r=16)
    b += text(380, 320, "из истока в каждый банк — ёмкость a, из каждого банка в сток — ёмкость b (показаны лишь некоторые)", 13, MUTED)
    return figure(svg(760, 340, b), "При точечных изменениях $a_i$ минимальный разрез считается динамикой по кругу, которую можно слить в дерево отрезков.")


# ---------------------------------------------------------------- гаджет прямоугольника
def fig_gadget():
    b = text(380, 26, "Штраф x за прямоугольник с обоими цветами: две вспомогательные вершины", 15)
    cells = [(90, 70 + i * 55) for i in range(4)]
    b += circle(300, 140, 22, "p", ORANGE, 17) + circle(500, 140, 22, "q", ORANGE, 17)
    for x, y in cells:
        b += circle(x, y, 17, "", None) + edge(x, y, 300, 140, "", BLUE, 2, r=17) + edge(500, 140, x + 20, y + 4, "", GREEN, 1.4, r=22, dash="3 4")
    b += edge(300, 140, 500, 140, "x", YELLOW, 4, r=22, lab_color=YELLOW)
    b += text(200, 250, "клетка v → p (∞)", 12, BLUE) + text(500, 250, "q → клетка v (∞)", 12, GREEN)
    b += text(380, 285, "есть клетка в S ⇒ p в S;  есть клетка в T ⇒ q в T;  оба сразу ⇒ режется ребро p→q (цена x)", 13, MUTED)
    return figure(svg(760, 305, b), "Верный гаджет. Первая попытка лектора — одна вершина, соединённая со всеми клетками, — давала штраф за меньший из цветов, а не за «оба цвета».")


# ---------------------------------------------------------------- гистограмма LCP
def fig_lcp():
    h = [0, 2, 3, 1, 4, 4, 2, 0]
    b = text(380, 26, "Гистограмма LCP: подстрока с k вхождениями — прямоугольник из k − 1 столбцов", 15)
    ox, oy, cw, unit = 80, 250, 70, 34
    for i, v in enumerate(h):
        b += f'<rect x="{ox + i * cw}" y="{oy - v * unit}" width="{cw - 6}" height="{v * unit}" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="1.5"/>' if v else ""
        b += text(ox + i * cw + cw / 2 - 3, oy + 20, str(v), 13, MUTED)
    b += f'<rect x="{ox + 4 * cw}" y="{oy - 4 * unit}" width="{2 * cw - 6}" height="{4 * unit}" fill="none" stroke="{YELLOW}" stroke-width="3" stroke-dasharray="6 4"/>'
    b += f'<rect x="{ox + 1 * cw}" y="{oy - 2 * unit}" width="{6 * cw - 6}" height="{2 * unit}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="6 4"/>'
    b += text(ox + 5 * cw, oy - 4 * unit - 10, "экстремальный: 2 столбца, высота 4 → 3 вхождения длины 4", 12, YELLOW)
    b += text(ox + 4 * cw, oy - 2 * unit - 10, "экстремальный: 6 столбцов, высота 2", 12, ORANGE)
    b += text(380, 295, "значения: длина × вхождения = высота × (столбцов + 1)", 14, TEXT)
    return figure(svg(760, 315, b), "Ответ в задачах «максимизировать функцию подстроки» достигается на экстремальном прямоугольнике — таком, который нельзя ни поднять вверх, ни расширить вбок.")


# ---------------------------------------------------------------- плеер: Форд—Фалкерсон
def algo_ff():
    P = {"s": (80, 120), "a": (260, 50), "b": (260, 190), "t": (440, 120)}
    spec = [("s", "a"), ("s", "b"), ("a", "b"), ("a", "t"), ("b", "t")]
    cap = {e: 1 for e in spec}; flow = {e: 0 for e in spec}
    frames = []

    def draw(path, msg_top):
        s = text(260, 20, msg_top, 13, MUTED)
        for u, v in spec:
            f = flow[(u, v)]
            col = GREEN if f else EDGE
            on = path and (u, v) in path
            if on: col = ORANGE
            s += edge(*P[u], *P[v], f"{f}/{cap[(u, v)]}", col, 3.2 if (f or on) else 2, r=20, lab_color=col)
        for k, (x, y) in P.items(): s += circle(x, y, 20, k, GREEN if k in "st" else None, 16)
        return s
    frames.append({"svg": draw(None, "сеть: у всех рёбер ёмкость 1"), "msg": "Исходная сеть, поток нулевой. Ищем увеличивающий путь в остаточной сети."})

    def find(order):
        seen = {"s"}; res = []
        def dfs(v, path):
            if v == "t": res.append(list(path)); return True
            seen.add(v)
            for u, w, sgn in order(v):
                if w not in seen:
                    res_cap = (cap[(u, w)] - flow[(u, w)]) if sgn > 0 else flow[(w, u)]
                    if res_cap > 0:
                        path.append((u, w, sgn))
                        if dfs(w, path): return True
                        path.pop()
            return False
        dfs("s", [])
        return res[0] if res else None

    def order(v):
        out = []
        for (u, w) in spec:
            if u == v: out.append((u, w, +1))
            if w == v: out.append((w, u, -1))
        return out
    step = 1
    while True:
        p = find(order)
        if not p: break
        edges_on = set(((a, b) if sg > 0 else (b, a)) for a, b, sg in p)
        names = " → ".join(["s"] + [b for a, b, sg in p])
        back = any(sg < 0 for _, _, sg in p)
        frames.append({"svg": draw(edges_on, f"путь {step}: {names}"), "msg": f"Путь {step}: {names}." + (" Здесь есть переход по обратному ребру — он отменяет часть прежнего потока." if back else "")})
        for a, b, sg in p:
            if sg > 0: flow[(a, b)] += 1
            else: flow[(b, a)] -= 1
        frames.append({"svg": draw(None, f"после пути {step}"), "msg": f"Протолкнули единицу потока. Величина потока = {sum(flow[e] for e in spec if e[0]=='s')}."})
        step += 1
    frames.append({"svg": draw(None, "пути нет — поток максимален"), "msg": f"Больше увеличивающих путей нет: поток {sum(flow[e] for e in spec if e[0]=='s')} максимален."})
    return {"title": "Форд—Фалкерсон: DFS по остаточной сети", "vb": "0 0 520 240", "frames": frames}


FIGS = {"flow_example": fig_flow_example, "reverse": fig_reverse, "layers": fig_layers, "split": fig_split, "matching": fig_matching,
        "table": fig_table, "ring": fig_ring, "gadget": fig_gadget, "lcp": fig_lcp}


def algos_js():
    data = {"ff": algo_ff()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
