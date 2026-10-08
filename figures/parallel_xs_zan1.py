"""Иллюстрации и плееры для «Занятие 1. Параллель XS — Деревья»."""
import json
from kit import *

PAL = [BLUE, GREEN, ORANGE, PURPLE, RED]
MARK = ('<defs><marker id="ar2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>')


def arc(x1, y1, x2, y2, color=MUTED, w=2, bend=-40, dash=None):
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 + bend
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1},{y1} Q{cx},{cy} {x2},{y2}" fill="none" stroke="{color}" stroke-width="{w}"{d} '
            f'marker-end="url(#ar2)"/>')


# ---------------------------------------------------------------- дерево-образец
# родители: корень 0
P1 = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 3, 8: 5, 9: 5, 10: 7}


def children(par, n=None):
    ch = {}
    for v in sorted(par):
        ch.setdefault(par[v], []).append(v)
    return ch


def layout(par, x0, y0, dx, dy, root=0):
    ch = children(par)
    pos = {}
    cnt = [0]

    def go(v, d):
        if v not in ch:
            pos[v] = (x0 + cnt[0] * dx, y0 + d * dy)
            cnt[0] += 1
        else:
            for u in ch[v]:
                go(u, d + 1)
            xs = [pos[u][0] for u in ch[v]]
            pos[v] = ((min(xs) + max(xs)) / 2, y0 + d * dy)
    go(root, 0)
    return pos


def draw_tree(par, pos, colors=None, edge_colors=None, r=17, labels=None, size=14):
    colors = colors or {}
    edge_colors = edge_colors or {}
    s = ""
    for v, p in par.items():
        (x1, y1), (x2, y2) = pos[p], pos[v]
        s += line(x1, y1, x2, y2, edge_colors.get(v, EDGE), 3 if v in edge_colors else 2)
    for v, (x, y) in pos.items():
        s += circle(x, y, r, str((labels or {}).get(v, v)), colors.get(v), size)
    return s


def depth_of(par):
    d = {0: 0}
    for v in sorted(par):
        d[v] = d[par[v]] + 1
    return d


def euler_order(par):
    ch = children(par)
    tin, order = {}, []

    def go(v):
        tin[v] = len(order)
        order.append(v)
        for u in ch.get(v, []):
            go(u)
    go(0)
    return tin, order


# ---------------------------------------------------------------- двоичные подъёмы
def fig_binup():
    pos = layout(P1, 70, 60, 70, 62)
    path = [10, 7, 3, 1, 0]
    col = {10: YELLOW, 7: BLUE, 3: GREEN, 0: ORANGE}
    b = text(380, 24, "Предки вершины 10: на 1, 2 и 4 ребра вверх", 15)
    b += draw_tree(P1, pos, col, {10: BLUE, 7: BLUE, 3: BLUE, 1: BLUE})
    b = b.replace('</svg>', '')
    x10, y10 = pos[10]
    for j, (a, c) in enumerate([(10, 7), (10, 3), (10, 0)]):
        pass
    b += arc(pos[10][0] + 14, pos[10][1] - 8, pos[7][0] + 15, pos[7][1] + 10, BLUE, 2, 30)
    b += arc(pos[10][0] + 18, pos[10][1] - 3, pos[3][0] + 18, pos[3][1] + 8, GREEN, 2, 60)
    b += arc(pos[10][0] + 20, pos[10][1] + 2, pos[0][0] + 18, pos[0][1] + 6, ORANGE, 2, 95)
    b += text(560, 70, "up[0][10] = 7", 14, BLUE, "start") + text(560, 96, "up[1][10] = 3", 14, GREEN, "start")
    b += text(560, 122, "up[2][10] = 0", 14, ORANGE, "start")
    b += text(560, 168, "up[j][v] = up[j−1][ up[j−1][v] ]", 14, YELLOW, "start")
    b += text(560, 194, "подняться на k: идём по битам k", 13, MUTED, "start")
    b += text(560, 214, "и прыгаем по каждой единице", 13, MUTED, "start")
    return figure(svg(760, 260, b), "Таблица $\\mathrm{up}[j][v]$: предок на $2^j$ рёбер выше. Подъём на $k$ — это прыжки по единичным битам числа $k$.")


# ---------------------------------------------------------------- разреженная таблица
def fig_sparse():
    a = [5, 3, 8, 6, 2, 7, 4, 9, 1, 6]
    l, r = 2, 8
    b = text(380, 24, "Запрос [2, 8]: длина 7 → берём $2^2 = 4$ и два отрезка длины 4, перекрывающихся", 15).replace("$2^2 = 4$", "2² = 4")
    for i, v in enumerate(a):
        c = None
        if l <= i <= r: c = BLUE
        b += cell(40 + i * 66, 60, 60, 38, str(v), c, 16, sub=str(i))
    b += line(40 + l * 66, 124, 40 + (l + 4) * 66 - 6, 124, GREEN, 4) + text(40 + (l + 2) * 66 - 3, 146, "sp[2][2] = min на [2..5]", 13, GREEN)
    b += line(40 + (r - 3) * 66, 164, 40 + (r + 1) * 66 - 6, 164, ORANGE, 4) + text(40 + (r - 1) * 66 - 3, 186, "sp[2][5] = min на [5..8]", 13, ORANGE)
    b += text(380, 226, "ответ = min(sp[2][2], sp[2][5]) = min(2, 1) = 1", 16, YELLOW)
    return figure(svg(760, 246, b), "Два перекрывающихся блока длины $2^j$ покрывают весь отрезок; пересечение минимуму не мешает.")


# ---------------------------------------------------------------- эйлеров обход
def euler_seq(par):
    ch = children(par)
    seq = []

    def go(v):
        seq.append(v)
        for u in ch.get(v, []):
            go(u)
            seq.append(v)
    go(0)
    return seq


def fig_euler():
    pos = layout(P1, 60, 56, 52, 52)
    seq = euler_seq(P1)
    d = depth_of(P1)
    u, v = 6, 9
    first = {}
    for i, x in enumerate(seq):
        first.setdefault(x, i)
    l, r = first[u], first[v]
    b = text(380, 22, "Эйлеров обход: пишем вершину при каждом проходе, длина 2n − 1", 15)
    b += draw_tree(P1, pos, {u: GREEN, v: ORANGE}, r=14, size=12)
    w = 31
    x0 = 20
    y0 = 214
    m = min(range(l, r + 1), key=lambda i: d[seq[i]])
    for i, x in enumerate(seq):
        c = None
        if l <= i <= r: c = BLUE
        if i == l: c = GREEN
        if i == r: c = ORANGE
        if i == m: c = YELLOW
        b += cell(x0 + i * w, y0, w - 3, 30, str(x), c, 12)
        b += text(x0 + i * w + (w - 3) / 2, y0 + 48, str(d[x]), 11, MUTED)
    b += text(x0, y0 + 48, "", 11) + text(14, y0 - 8, "обход", 12, MUTED, "start") + text(14, y0 + 66, "высота", 12, MUTED, "start")
    b += text(560, 90, f"u = {u}, v = {v}", 14, TEXT, "start")
    b += text(560, 116, f"first[u] = {l}, first[v] = {r}", 14, TEXT, "start")
    b += text(560, 142, f"минимум высоты на [{l}, {r}] — вершина {seq[m]}", 14, YELLOW, "start")
    b += text(560, 168, f"LCA({u}, {v}) = {seq[m]}", 15, YELLOW, "start")
    return figure(svg(760, 300, b), "Между первыми вхождениями $u$ и $v$ нет вершин выше $\\mathrm{LCA}$, а сама она там есть: LCA — вершина минимальной высоты на отрезке.")


# ---------------------------------------------------------------- мешки Тарьяна
def fig_bags():
    b = text(380, 24, "Вершина $u$ и «мешки» уже просмотренных поддеревьев: у всех в мешке один LCA с $u$", 15).replace("$u$", "u")
    xs = [90, 230, 370, 510]
    ys = [70, 120, 170, 220]
    names = ["корень", "a₁", "a₂", "u"]
    for i in range(4):
        if i + 1 < 4:
            b += line(xs[i], ys[i], xs[i + 1], ys[i + 1], EDGE, 3)
    cols = [ORANGE, PURPLE, GREEN, YELLOW]
    for i in range(4):
        b += circle(xs[i], ys[i], 20, names[i] if i else "r", cols[i], 14)
    for i in range(3):
        bx, by = xs[i] - 75, ys[i] + 28
        b += f'<ellipse cx="{bx}" cy="{by}" rx="48" ry="24" fill="{SOFT[cols[i]]}" stroke="{cols[i]}" stroke-width="2" stroke-dasharray="5 4"/>'
        b += text(bx, by + 5, "мешок", 13, TEXT)
        b += line(xs[i] - 14, ys[i] + 12, bx + 30, by - 14, cols[i], 2)
    b += text(610, 76, "LCA(u, x) для x из мешка", 13, MUTED, "start")
    b += text(610, 98, "верхнего = корень", 13, ORANGE, "start")
    b += text(610, 130, "среднего = a₁", 13, PURPLE, "start")
    b += text(610, 162, "нижнего = a₂", 13, GREEN, "start")
    b += text(610, 204, "Каждый мешок — множество СНМ", 13, YELLOW, "start")
    b += text(610, 224, "с представителем-предком", 13, YELLOW, "start")
    return figure(svg(760, 270, b), "При выходе из ребёнка его мешок объединяется с мешком родителя: представителем становится сам родитель.")


# ---------------------------------------------------------------- стек минимумов + СНМ
def fig_stackdsu():
    a = [5, 2, 6, 3, 4]
    st = [1, 3, 4]
    comp = {0: 1, 1: 1, 2: 3, 3: 3, 4: 4}
    cols = {1: BLUE, 3: GREEN, 4: ORANGE}
    b = text(380, 24, "Префикс до r = 4: стек минимумов [1, 3, 4] и отрезки левых границ", 15)
    for i, v in enumerate(a):
        b += cell(110 + i * 110, 60, 90, 40, str(v), cols[comp[i]], 18, sub=f"i = {i}")
    for s_, e_, c in [(0, 1, BLUE), (2, 3, GREEN), (4, 4, ORANGE)]:
        b += line(110 + s_ * 110, 128, 110 + e_ * 110 + 90, 128, c, 5)
    b += text(110 + 55 + 0, 156, "l ∈ {0, 1} → min = a[1] = 2", 13, BLUE, "start")
    b += text(110 + 2 * 110, 156, "l ∈ {2, 3} → a[3] = 3", 13, GREEN, "start")
    b += text(110 + 4 * 110 - 40, 182, "l = 4 → a[4] = 4", 13, ORANGE, "start")
    b += text(380, 232, "минимум на [l, r] = a[ find(l) ] — ближайший справа к l элемент стека", 15, YELLOW)
    return figure(svg(760, 256, b), "Элементы стека минимумов делят левые границы на отрезки; каждый отрезок — одна компонента СНМ.")


# ---------------------------------------------------------------- линейные бинапы
def jump_len(D):
    s = [0] * (D + 1)
    for d in range(1, D + 1):
        p = d - 1
        s[d] = 2 * s[p] + 1 if s[p] == s[p - s[p]] else 1
    return s


def fig_linjump():
    D = 15
    s = jump_len(D)
    x0, y = 40, 170
    step = 43
    b = text(380, 24, "Из вершины глубины d прыжок ведёт на глубину d − s(d); длины s(d) = 2ᵏ − 1", 15)
    colmap = {1: MUTED, 3: BLUE, 7: GREEN, 15: ORANGE}
    for d in range(D + 1):
        b += circle(x0 + d * step, y, 13, str(d), None, 11)
    for d in range(1, D + 1):
        L = s[d]
        c = colmap.get(L, PURPLE)
        x1, x2 = x0 + d * step, x0 + (d - L) * step
        if L == 1:
            continue
        b += arc(x1 - 6, y - 12, x2 + 6, y - 12, c, 2, -18 - L * 9)
    b += text(380, 224, "s(d):  " + " ".join(str(v) for v in s), 13, MUTED)
    b += text(380, 248, "прыжок длины 1 — просто в родителя; остальные дуги нарисованы выше", 13, MUTED)
    return figure(svg(760, 270, b), "Глубины $0\\ldots15$ одного пути и прыжки вверх: длины $1,1,3,1,1,3,7,1,1,3,1,1,3,7,15$. Прыжки вложены друг в друга, как отрезки в двоичной записи.")


# ---------------------------------------------------------------- сжатое дерево
def fig_virtual():
    pos = layout(P1, 50, 70, 46, 52)
    marked = {6, 10, 9}
    lcas = {3, 0}
    col = {v: GREEN for v in marked}
    col.update({v: ORANGE for v in lcas})
    b = text(190, 24, "Исходное дерево", 14, MUTED) + text(590, 24, "Сжатое дерево", 14, MUTED)
    b += draw_tree(P1, pos, col, r=15, size=12)
    # справа: 0 -(2)- 3, 3 -(1)- 6, 3 -(2)- 10, 0 -(3)- 9
    q = {0: (590, 70), 3: (520, 150), 6: (470, 235), 10: (570, 235), 9: (670, 150)}
    ed = [(0, 3, 2), (3, 6, 1), (3, 10, 2), (0, 9, 3)]
    for a, c_, w in ed:
        (x1, y1), (x2, y2) = q[a], q[c_]
        b += line(x1, y1, x2, y2, EDGE, 2) + text((x1 + x2) / 2 + (12 if x2 >= x1 else -12), (y1 + y2) / 2, str(w), 13, YELLOW)
    for v, (x, y) in q.items():
        b += circle(x, y, 16, str(v), col[v], 13)
    b += text(590, 290, "числа на рёбрах — длина пути в исходном дереве", 12, MUTED)
    return figure(svg(760, 306, b), "Выбраны 6, 9, 10 (зелёные). Добавляем LCA соседних по $\\mathrm{tin}$ (оранжевые) и стираем всё остальное: структура ветвления сохранена.")


# ---------------------------------------------------------------- лесенки
def fig_ladder():
    pos = layout(P1, 40, 60, 46, 54)
    pathcol = {0: BLUE, 1: BLUE, 3: BLUE, 7: BLUE, 10: BLUE, 6: GREEN, 4: ORANGE, 2: PURPLE, 5: PURPLE, 8: PURPLE, 9: RED}
    b = text(150, 24, "Длинные пути", 14, MUTED) + text(540, 24, "Лестницы (продолжены вверх на длину пути)", 14, MUTED)
    ec = {v: pathcol[v] for v in P1 if pathcol[v] == pathcol[P1[v]]}
    b += draw_tree(P1, pos, pathcol, ec, r=15, size=12)
    rows = [([0, 1, 3, 7, 10], 0, BLUE), ([3, 6], 1, GREEN), ([1, 4], 1, ORANGE), ([0, 2, 5, 8], 1, PURPLE), ([5, 9], 1, RED)]
    for k, (lad, ext, c) in enumerate(rows):
        y = 70 + k * 44
        for i, v in enumerate(lad):
            b += cell(380 + i * 44, y, 38, 32, str(v), c if i >= ext else None, 14)
        if ext:
            b += text(380 + 5 * 44 + 6, y + 21, "← продолжение", 11, MUTED, "start") if len(lad) < 4 else ""
    b += text(540, 300, "сумма длин лестниц ≤ 2n", 14, YELLOW)
    return figure(svg(760, 320, b), "Каждый путь (цвет) удваивается вверх; бледные ячейки — добавленные предки. Кто начал прыжок на $2^j$, тот попадает на лестницу, где ответ лежит рядом.")


# ---------------------------------------------------------------- метод четырёх русских
def fig_blocks():
    h = [0, 1, 2, 1, 2, 3, 2, 1, 0, 1, 2, 1]
    B = 3
    b = text(380, 24, "Массив ±1, блоки по B = 3; запрос [1, 10] разбит на три части", 15)
    for i, v in enumerate(h):
        c = None
        if 1 <= i <= 10: c = BLUE
        b += cell(50 + i * 54, 60, 50, 36, str(v), c, 16, sub=str(i))
    for k in range(5):
        x = 50 + k * B * 54 - 2
        b += line(x, 50, x, 106, AXIS, 2, "4 3")
    b += text(50 + 54 * 1.5, 130, "суффикс блока", 12, GREEN) + line(50 + 54, 118, 50 + 54 * 3 - 4, 118, GREEN, 4)
    b += text(50 + 54 * 6, 130, "целые блоки: sparse по минимумам блоков", 12, YELLOW) + line(50 + 54 * 3, 118, 50 + 54 * 9 - 4, 118, YELLOW, 4)
    b += text(50 + 54 * 10, 130, "префикс", 12, ORANGE) + line(50 + 54 * 9, 118, 50 + 54 * 11 - 4, 118, ORANGE, 4)
    b += text(380, 184, "внутри блока ответ зависит только от формы (вверх/вниз), масок всего 2^(B−1)", 14, TEXT)
    b += text(380, 212, "при B = (log n)/2 это √n масок, таблицы для всех — O(√n · log² n)", 14, MUTED)
    return figure(svg(760, 236, b), "Метод четырёх русских: на коротких блоках ответ берётся из таблицы по «форме» блока.")


# ---------------------------------------------------------------- декартово дерево
def fig_cartesian():
    a = [5, 1, 4, 2, 6, 3]
    pos = {1: (380, 70), 0: (240, 150), 3: (520, 150), 2: (440, 230), 5: (600, 230), 4: (540, 300)}
    ed = [(1, 0), (1, 3), (3, 2), (3, 5), (5, 4)]
    b = text(380, 22, "Декартово дерево: x — индекс, y — значение (мин. сверху)", 15)
    for p_, c_ in ed:
        b += line(*pos[p_], *pos[c_], EDGE, 2)
    for i, (x, y) in pos.items():
        col = YELLOW if i == 3 else (GREEN if i in (2, 4) else None)
        b += circle(x, y, 22, str(a[i]), col, 16) + text(x + 30, y - 18, f"i={i}", 11, MUTED)
    b += text(120, 250, "RMQ(2, 4):", 14, TEXT, "start") + text(120, 274, "вершины 4 и 6 (индексы 2 и 4)", 12, MUTED, "start")
    b += text(120, 296, "LCA = вершина 2 (индекс 3)", 13, YELLOW, "start")
    return figure(svg(760, 330, b), "Для массива 5 1 4 2 6 3 минимум на $[2,4]$ — это значение в $\\mathrm{LCA}$ вершин с индексами 2 и 4.")


FIGS = {"binup": fig_binup, "sparse": fig_sparse, "euler": fig_euler, "bags": fig_bags, "stackdsu": fig_stackdsu,
        "linjump": fig_linjump, "virtual": fig_virtual, "ladder": fig_ladder, "blocks": fig_blocks, "cartesian": fig_cartesian}


# ================================================================ плееры
# ---- двоичные подъёмы: LCA способом 1
P2 = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 2, 8: 7, 9: 8, 10: 4, 11: 10}


def algo_binlca():
    par = dict(P2); par[0] = 0
    d = depth_of(P2)
    pos = layout(P2, 60, 50, 56, 44)
    up = {0: dict(par)}
    LGN = 3
    for j in range(1, LGN):
        up[j] = {v: up[j - 1][up[j - 1][v]] for v in par}
    tin, order = euler_order(P2)
    ch = children(P2)
    sz = {}

    def go(v):
        sz[v] = 1 + sum(go(u) for u in ch.get(v, []))
        return sz[v]
    go(0)

    def anc(a, b):
        return tin[a] <= tin[b] < tin[a] + sz[a]
    u, v = 6, 9
    frames = []

    def draw(vcur, cand, note, done=None):
        col = {u: GREEN, vcur: ORANGE}
        if cand is not None and cand != vcur: col[cand] = YELLOW
        if done is not None: col[done] = PURPLE
        s = MARK + draw_tree(P2, pos, col, r=15, size=12)
        s += text(530, 70, f"u = {u} (зафиксирована)", 13, GREEN, "start") + text(530, 94, f"v = {vcur}", 13, ORANGE, "start")
        s += text(530, 140, note, 13, TEXT, "start")
        return s
    frames.append({"svg": draw(v, None, "ищем LCA(6, 9)"), "msg": f"u = {u}, v = {v}. Вершина v не предок u, поэтому поднимаем v, пока можем остаться не-предком u."})
    for j in range(LGN - 1, -1, -1):
        cand = up[j][v]
        ok = not anc(cand, u)
        frames.append({"svg": draw(v, cand, f"j = {j}: up = {cand}, предок u? {'да' if not ok else 'нет'}"),
                       "msg": f"j = {j}: кандидат {cand} на {2 ** j} выше. " + ("Он НЕ предок u — прыгаем." if ok else "Он предок u (или сама u) — перелетели бы LCA, не прыгаем.")})
        if ok:
            v = cand
            frames.append({"svg": draw(v, None, f"прыгнули: v = {v}"), "msg": f"Теперь v = {v}."})
    res = up[0][v]
    frames.append({"svg": draw(v, None, f"ответ — родитель v = {res}", res), "msg": f"v стоит прямо под LCA, значит LCA = родитель = {res}."})
    return {"title": "LCA двоичными подъёмами (способ с проверкой предка)", "vb": "0 0 760 330", "frames": frames}


# ---- офлайн RMQ Тарьяна
def algo_offrmq():
    a = [5, 2, 6, 3, 4, 1, 7]
    n = len(a)
    queries = [(0, 3), (2, 4), (3, 6), (4, 5)]
    ans = {}
    frames = []
    st = []
    dsu = list(range(n))

    def find(x):
        while dsu[x] != x: x = dsu[x]
        return x

    def draw(r, note):
        s = ""
        for i in range(n):
            col = None
            if i > r: s += cell(40 + i * 82, 40, 70, 40, str(a[i]), None, 18, sub=f"i={i}"); continue
            root = find(i)
            col = PAL[st.index(root) % len(PAL)] if root in st else None
            if i == r: col = YELLOW
            s += cell(40 + i * 82, 40, 70, 40, str(a[i]), col, 18, sub=f"i={i}")
        s += text(40, 112, "стек: " + " ".join(f"{i}({a[i]})" for i in st), 14, TEXT, "start")
        y = 140
        for (l, rr), v in ans.items():
            s += text(40, y, f"min[{l}..{rr}] = {v}", 13, GREEN, "start"); y += 22
        s += text(40, 232 if y < 232 else y + 6, note, 13, MUTED, "start")
        return s
    for r in range(n):
        dsu[r] = r
        popped = []
        while st and a[st[-1]] >= a[r]:
            dsu[st[-1]] = r; popped.append(st.pop())
        st.append(r)
        msg = f"r = {r}, a[r] = {a[r]}. " + (f"Снимаем со стека {popped} и вливаем их отрезки в {r}. " if popped else "Снимать нечего. ")
        frames.append({"svg": draw(r, f"добавили {r}; снято: {popped or 'ничего'}"), "msg": msg})
        for (l, rr) in queries:
            if rr == r:
                ans[(l, rr)] = a[find(l)]
                frames.append({"svg": draw(r, f"запрос [{l},{rr}]: find({l}) = {find(l)}"), "msg": f"Запрос [{l}, {rr}]: find({l}) = {find(l)}, минимум {a[find(l)]}."})
    return {"title": "Офлайн RMQ: стек минимумов и СНМ", "vb": "0 0 640 270", "frames": frames}


# ---- линейные бинапы: подъём на заданную глубину
def algo_linjump():
    D = 15
    s = jump_len(D)
    x0, y = 40, 120
    step = 43
    frames = []
    start, target = 14, 3

    def base(cur, cand, note):
        b = ""
        for d in range(1, D + 1):
            L = s[d]
            if L == 1: continue
            c = {3: BLUE, 7: GREEN, 15: ORANGE}.get(L, PURPLE)
            b += arc(x0 + d * step - 6, y - 12, x0 + (d - L) * step + 6, y - 12, c + "88" if False else c, 1, -18 - L * 7, "3 3")
        for d in range(D + 1):
            col = None
            if d == target: col = GREEN
            if d == cand: col = YELLOW
            if d == cur: col = ORANGE
            b += circle(x0 + d * step, y, 13, str(d), col, 11)
        b += text(40, 215, note, 13, TEXT, "start")
        return MARK + b
    cur = start
    frames.append({"svg": base(cur, None, f"поднимаемся с глубины {start} на глубину {target}"), "msg": f"Нужно попасть на глубину {target}. Текущая вершина — глубина {cur}."})
    while cur > target:
        jd = cur - s[cur]
        if jd >= target:
            frames.append({"svg": base(cur, jd, f"прыжок {cur} → {jd}: не перелетает цель"), "msg": f"Прыжок из {cur} ведёт на глубину {jd} ≥ {target} — прыгаем."})
            cur = jd
        else:
            frames.append({"svg": base(cur, jd, f"прыжок {cur} → {jd} перелетает, идём в родителя"), "msg": f"Прыжок из {cur} вёл бы на глубину {jd} < {target} — перелёт. Делаем шаг в родителя."})
            cur -= 1
        frames.append({"svg": base(cur, None, f"теперь на глубине {cur}"), "msg": f"Глубина {cur}."})
    return {"title": "Линейные бинапы: подъём на заданную глубину", "vb": "0 0 720 240", "frames": frames}


# ---- Тарьян LCA
def algo_tarjan():
    par = dict(P1)
    ch = children(P1)
    pos = layout(P1, 40, 40, 52, 50)
    qs = [(6, 9), (10, 4), (10, 7)]
    qmap = {}
    for i, (a, b_) in enumerate(qs):
        qmap.setdefault(a, []).append((b_, i)); qmap.setdefault(b_, []).append((a, i))
    dsu = {v: v for v in P1}; dsu[0] = 0
    vis = set()
    ans = {}
    frames = []

    def find(x):
        while dsu[x] != x: x = dsu[x]
        return x

    def draw(cur, note):
        col = {}
        roots = sorted({find(v) for v in vis})
        for v in vis:
            col[v] = PAL[roots.index(find(v)) % len(PAL)]
        if cur is not None: col[cur] = YELLOW
        s = draw_tree(P1, pos, col, r=15, size=12)
        for v, (x, y) in pos.items():
            if v in vis and find(v) != v:
                s += text(x, y + 28, f"→{find(v)}", 10, MUTED)
        s += text(560, 60, "запросы: " + ", ".join(f"({a},{b})" for a, b in qs), 13, TEXT, "start")
        y = 90
        for i, v in sorted(ans.items()):
            s += text(560, y, f"LCA{qs[i]} = {v}", 13, GREEN, "start"); y += 22
        s += text(40, 290, note, 13, MUTED, "start")
        return s

    def go(v):
        vis.add(v)
        frames.append({"svg": draw(v, f"вошли в {v}"), "msg": f"Входим в {v}: она отмечена посещённой, её компонента — она сама."})
        for u in ch.get(v, []):
            go(u)
            dsu[find(u)] = v
            frames.append({"svg": draw(v, f"вышли из {u}, влили его компоненту в {v}"), "msg": f"Вышли из {u}: компонента {u} объединена с {v}. Теперь все её вершины имеют представителя {v}."})
        for (w, i) in qmap.get(v, []):
            if w in vis and i not in ans:
                ans[i] = find(w)
                frames.append({"svg": draw(v, f"запрос {qs[i]}: LCA = find({w}) = {find(w)}"), "msg": f"Запрос {qs[i]}: второй конец {w} уже посещён, LCA = find({w}) = {find(w)}."})
    go(0)
    return {"title": "Алгоритм Тарьяна: LCA офлайн", "vb": "0 0 760 310", "frames": frames}


def algos_js():
    data = {"binlca": algo_binlca(), "offrmq": algo_offrmq(), "linjump": algo_linjump(), "tarjan": algo_tarjan()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
