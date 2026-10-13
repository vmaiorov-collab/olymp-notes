"""Иллюстрации для «Занятие 2. Параллель XS — SQRT-декомпозиция»."""
import random
from kit import *


def fig_blocks_query():
    b = text(380, 24, "Сумма на [3, 17): блоки по B = 5", 15)
    n, B, W, X0, Y0 = 20, 5, 34, 40, 60
    l, r = 3, 17
    for i in range(n):
        inside = l <= i < r
        full = (i // B) * B >= l and (i // B) * B + B <= r
        col = GREEN if full else (YELLOW if inside else None)
        b += cell(X0 + i * W, Y0, W - 4, 34, str(i), col, 13)
    for k in range(4):
        x1 = X0 + k * B * W
        b += f'<rect x="{x1 - 3}" y="{Y0 - 8}" width="{B * W}" height="50" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.5"/>'
        b += cell(x1 + 8, Y0 + 70, B * W - 24, 30, f"blk[{k}]", GREEN if k in (1, 2) else None, 13)
    b += text(X0 + 1.0 * B * W + 20, Y0 + 130, "прыжок на блок: i += B", 13, GREEN)
    b += line(X0 + 1.0 * B * W + 8, Y0 + 44, X0 + 1.0 * B * W + 8, Y0 + 66, GREEN, 2, arrow=True)
    b += text(X0 + 1.6 * W, Y0 + 130, "по одному", 13, YELLOW) + text(X0 + 17.5 * W - 30, Y0 + 130, "по одному", 13, YELLOW)
    b += text(380, 238, "запрос: не более 2·(B − 1) одиночных элементов + n / B блоков  ⇒  O(B + n / B) = O(√n)", 14, TEXT)
    b += text(380, 264, "изменение элемента: поправить a[i] и blk[i / B], O(1)", 14, BLUE)
    return figure(svg(760, 282, b), "Целые блоки пропускаются одним прыжком, а края (префикс и суффикс запроса) проходятся поэлементно. Лучший B получается из равенства B = n / B.")


def fig_prefix_lazy():
    b = text(380, 24, "Префиксы внутри блоков + «отложенная» добавка к блокам правее", 15)
    n, B, W, X0, Y0 = 20, 5, 34, 40, 60
    p = 7
    for i in range(n):
        blk = i // B
        col = ORANGE if (blk == p // B and i >= p) else (YELLOW if blk > p // B else None)
        b += cell(X0 + i * W, Y0, W - 4, 34, "in", col, 12)
    for k in range(4):
        x1 = X0 + k * B * W
        b += f'<rect x="{x1 - 3}" y="{Y0 - 8}" width="{B * W}" height="50" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.5"/>'
        b += cell(x1 + 8, Y0 + 70, B * W - 24, 30, f"before[{k}]", YELLOW if k > p // B else None, 12)
    b += f'<circle cx="{X0 + p * W + 15}" cy="{Y0 + 17}" r="22" fill="none" stroke="{RED}" stroke-width="2.5"/>'
    b += text(X0 + p * W + 15, Y0 - 16, "a[7] += d", 13, RED)
    b += text(X0 + 2.5 * W * 3, Y0 + 130, "свой блок: in[j] += d для j ≥ 7  (≤ B операций)", 13, ORANGE, "start")
    b += text(X0 + 2.5 * W * 3, Y0 + 152, "правые блоки: before[b] += d  (≤ n / B операций)", 13, YELLOW, "start")
    b += text(380, 250, "pref(i) = in[i − 1] + before[блок(i − 1)]   — запрос за O(1)", 14, GREEN)
    return figure(svg(760, 270, b), "Если запросов суммы намного больше, чем изменений, префиксные суммы поддерживаются корневой декомпозицией: изменение стоит O(√n), запрос — O(1).")


def fig_strips():
    rnd = random.Random(7)
    b = text(380, 24, "Обход точек полосами ширины B: вверх, вниз, вверх, ...", 15)
    N, B = 300, 60
    ox, oy, w, h = 60, 44, 640, 300
    b += f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="8" fill="{NODE}" stroke="{EDGE}"/>'
    for k in range(1, N // B):
        x = ox + k * B * w / N
        b += line(x, oy, x, oy + h, EDGE, 1.5, dash="5 4")
    pts = [(rnd.randint(2, N - 2), rnd.randint(2, N - 2)) for _ in range(40)]
    pts.sort(key=lambda p: (p[0] // B, p[1] if (p[0] // B) % 2 == 0 else -p[1]))
    def P(p): return (ox + p[0] * w / N, oy + h - p[1] * h / N)
    path = [(ox, oy + h)] + [P(p) for p in pts]
    for i in range(len(path) - 1):
        col = BLUE if (pts[i - 1][0] // B if i else 0) % 2 == 0 else GREEN
        b += line(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1], col, 1.8)
    for p in pts:
        x, y = P(p); b += f'<circle cx="{x}" cy="{y}" r="4" fill="{YELLOW}"/>'
    b += text(380, 372, "по y — не больше n на полосу, по x — не больше B на точку:  (n / B)·n + n·B  ⇒  O(n√n) при B = √n", 13, TEXT)
    return figure(svg(760, 390, b), "Внутри полосы точки отсортированы по y (чётные полосы — вверх, нечётные — вниз). Путь внутри полосы почти вертикален, а между соседними точками по x двигаемся не больше чем на B.")


def fig_mo_snake():
    rnd = random.Random(11)
    b = text(380, 24, "Алгоритм Мо: запрос [l, r] — точка плоскости, блоки по l", 15)
    N, B = 300, 75
    ox, oy, w, h = 70, 44, 600, 280
    b += f'<rect x="{ox}" y="{oy}" width="{w}" height="{h}" rx="8" fill="{NODE}" stroke="{EDGE}"/>'
    b += f'<polygon points="{ox},{oy + h} {ox},{oy} {ox + w},{oy}" fill="{SOFT[BLUE]}" opacity="0.35"/>'
    b += text(ox + 60, oy + 40, "r ≥ l", 13, MUTED)
    for k in range(1, N // B):
        x = ox + k * B * w / N; b += line(x, oy, x, oy + h, EDGE, 1.5, dash="5 4")
    pts = []
    while len(pts) < 44:
        l, r = rnd.randint(0, N - 1), rnd.randint(0, N - 1)
        if l <= r: pts.append((l, r))
    pts.sort(key=lambda p: (p[0] // B, p[1] if (p[0] // B) % 2 == 0 else -p[1]))
    def P(p): return (ox + p[0] * w / N, oy + h - p[1] * h / N)
    for i in range(len(pts) - 1):
        a, c = P(pts[i]), P(pts[i + 1])
        col = BLUE if (pts[i][0] // B) % 2 == 0 else GREEN
        b += line(a[0], a[1], c[0], c[1], col, 1.8)
    for p in pts:
        x, y = P(p); b += f'<circle cx="{x}" cy="{y}" r="4" fill="{YELLOW}"/>'
    b += text(ox + w / 2, oy + h + 20, "l  →", 13, MUTED) + text(ox - 14, oy + 10, "r ↑", 13, MUTED, "end")
    b += text(380, 362, "r движется по блоку l в одну сторону (змейка), l внутри блока смещается не больше чем на B", 13, TEXT)
    b += text(380, 384, "всего O(n · n / B + q · B)  ⇒  при B = n / √q получается O(n√q)", 13, YELLOW)
    return figure(svg(760, 402, b), "Сортировка запросов по (⌊l / B⌋, r), причём на нечётных блоках r идёт по убыванию: так не приходится возвращаться в начало после каждого блока.")


def fig_mex_blocks():
    b = text(380, 24, "mex: счётчики значений + число «дырок» в каждом блоке", 15)
    cnt = [2, 1, 3, 1, 1, 2, 0, 1, 1, 0, 0, 2, 1, 0, 1, 1]
    B, W, X0, Y0 = 4, 42, 40, 60
    for i, c in enumerate(cnt):
        b += cell(X0 + i * W, Y0, W - 4, 34, str(c), RED if c == 0 else BLUE, 14)
        b += text(X0 + i * W + (W - 4) / 2, Y0 + 52, str(i), 11, MUTED)
    for k in range(4):
        x1 = X0 + k * B * W
        z = sum(1 for c in cnt[k * B:(k + 1) * B] if c == 0)
        b += f'<rect x="{x1 - 3}" y="{Y0 - 8}" width="{B * W}" height="50" rx="8" fill="none" stroke="{EDGE}" stroke-width="1.5"/>'
        b += cell(x1 + 14, Y0 + 80, B * W - 34, 30, f"zeros = {z}", GREEN if z == 0 else YELLOW, 13)
    b += text(X0 + 0.5 * B * W, Y0 + 134, "пропускаем", 13, GREEN) + text(X0 + 1.5 * B * W, Y0 + 134, "здесь дырка", 13, YELLOW)
    b += f'<circle cx="{X0 + 6 * W + 19}" cy="{Y0 + 17}" r="24" fill="none" stroke="{YELLOW}" stroke-width="3"/>'
    b += text(X0 + 6 * W + 19, Y0 + 190, "mex = 6", 16, YELLOW)
    b += text(380, 270, "add / rem — O(1): меняем cnt[x] и, когда он становится нулём или перестаёт им быть, zeros[x / B]", 13, TEXT)
    b += text(380, 292, "mex — O(√V): первый блок с zeros > 0, затем честный поиск нуля внутри него", 13, TEXT)
    return figure(svg(760, 310, b), "Множество чисел с быстрым добавлением и удалением и корневым запросом mex. Именно такой дисбаланс (много изменений, мало запросов) и нужен алгоритму Мо.")


def fig_euler_twice():
    b = text(380, 24, "Путь 3 → 7 в эйлеровом обходе: ровно один раз встречаются вершины пути", 15)
    P = {1: (330, 70), 5: (210, 140), 8: (450, 140), 3: (140, 215), 4: (280, 215), 6: (280, 280), 7: (450, 215)}
    for a, c in [(1, 5), (1, 8), (5, 3), (5, 4), (4, 6), (8, 7)]:
        b += line(*P[a], *P[c], EDGE, 2)
    for v, (x, y) in P.items():
        col = GREEN if v in (3, 5, 8, 7) else (YELLOW if v == 1 else None)
        b += circle(x, y, 18, str(v), col, 15)
    b += text(560, 70, "lca = 1", 13, YELLOW, "start") + text(560, 94, "добавляем отдельно", 12, YELLOW, "start")
    seq = [1, 5, 3, 3, 4, 6, 6, 4, 5, 8, 7, 7, 8, 1]
    W, X0, Y0 = 48, 40, 330
    for i, v in enumerate(seq):
        inside = 3 <= i <= 10
        once = inside and seq.count(v) == 2 and (seq[3:11].count(v) == 1)
        col = GREEN if once else (RED if inside else None)
        b += cell(X0 + i * W, Y0, W - 4, 34, str(v), col, 14)
        b += text(X0 + i * W + (W - 4) / 2, Y0 + 52, str(i), 11, MUTED)
    b += text(X0 + 3 * W, Y0 - 12, "от tout[3]", 12, MUTED, "start") + text(X0 + 10 * W + 40, Y0 - 12, "до tin[7]", 12, MUTED, "end")
    b += text(380, 408, "зелёные — один раз (на пути), красные 4 и 6 — два раза (вне пути): их «гасим»", 13, TEXT)
    return figure(svg(760, 426, b), "Отрезок эйлерова обхода между выходом из u и входом в v содержит вершины пути по одному разу, остальное — по два. Если v предок, берётся отрезок от tin[u] до tin[v].")


def fig_heavy_light():
    b = text(380, 24, "Тяжёлые и лёгкие вершины: порог B = √(2m)", 15)
    # лёгкая
    lx, ly = 150, 190
    nb = [(60, 110), (60, 270), (250, 120), (250, 260)]
    for (x, y) in nb:
        b += line(lx, ly, x, y, BLUE, 2, arrow=True)
        b += circle(x, y, 16, "+x", BLUE, 12)
    b += circle(lx, ly, 22, "v", GREEN, 16)
    b += text(lx, 320, "лёгкая (deg ≤ B): обойти соседей", 13, GREEN) + text(lx, 340, "и прибавить x каждому", 13, GREEN)
    # тяжёлая
    hx, hy = 560, 190
    for k in range(8):
        import math
        a = k * math.pi / 4
        x, y = hx + 85 * math.cos(a), hy + 85 * math.sin(a)
        b += line(hx, hy, x, y, EDGE, 1.5) + circle(x, y, 9, "", None)
    b += circle(hx, hy, 30, "h", RED, 18)
    b += cell(hx - 55, hy - 140, 110, 30, "pend[h] += x", YELLOW, 13)
    b += line(hx, hy - 110, hx, hy - 34, YELLOW, 2, arrow=True)
    b += text(hx, 320, "тяжёлая (deg > B): не обходить —", 13, RED) + text(hx, 340, "записать отложенное pend[h]", 13, RED)
    b += text(380, 376, "тяжёлых не больше 2m / B;  get(u) = val[u] + Σ по тяжёлым h, смежным с u, pend[h]", 13, TEXT)
    b += text(380, 398, "матрица «тяжёлая × вершина» занимает (2m / B)·n ячеек", 13, MUTED)
    return figure(svg(760, 416, b), "Сумма степеней равна 2m, поэтому вершин со степенью больше B не больше 2m / B. Лёгкие вершины работают «в лоб», тяжёлых так мало, что для них можно хранить таблицу смежности.")


def fig_jump_residues():
    b = text(380, 24, "Прыжки a[i] = 3: из каждой клетки дальше только вдоль класса вычетов", 15)
    n, W, X0, Y0 = 18, 38, 40, 90
    cols = [BLUE, GREEN, ORANGE]
    for i in range(n):
        b += cell(X0 + i * W, Y0, W - 4, 34, str(i), cols[i % 3] if i % 3 == 2 else None, 13)
        if i % 3 != 2:
            b += f'<rect x="{X0 + i * W}" y="{Y0}" width="{W - 4}" height="34" rx="6" fill="none" stroke="{EDGE}" stroke-width="1.2"/>'
    for t in range(2, n - 3, 3):
        x1, x2 = X0 + t * W + 17, X0 + (t + 3) * W + 17
        mid = (x1 + x2) / 2
        b += f'<path d="M {x1} {Y0} Q {mid} {Y0 - 46} {x2} {Y0}" fill="none" stroke="{ORANGE}" stroke-width="2"/>'
    b += text(380, 170, "всё, что положили в f[3][2], увидят ВСЕ клетки i ≡ 2 (mod 3) правее", 14, ORANGE)
    b += text(380, 206, "малый шаг l < B:  f[l][i % l] += dp[i]  — один раз; дальше dp[j] += Σ_l f[l][j % l]  (B слагаемых)", 13, TEXT)
    b += text(380, 230, "большой шаг a[i] ≥ B:  прыгаем честно вперёд, не более n / B прыжков", 13, TEXT)
    b += text(380, 262, "итого O(n√n) времени и O(n) памяти (f[l] имеет длину l)", 14, GREEN)
    return figure(svg(760, 280, b), "Для малых шагов не нужно запоминать, кто куда прыгал: достаточно суммы dp по классу вычетов.")


def fig_floor_blocks():
    b = text(380, 24, "Различные значения ⌊x / i⌋ при x = 36: не больше 2√x", 15)
    x = 36
    X0, Y0, W, H = 50, 50, 17, 220
    for i in range(1, x + 1):
        k = x // i
        col = BLUE if i <= 6 else GREEN
        h = k * H / x
        b += f'<rect x="{X0 + (i - 1) * W}" y="{Y0 + H - h}" width="{W - 3}" height="{h}" fill="{SOFT[col]}" stroke="{col}" stroke-width="1.5"/>'
        if i <= 8 or i in (9, 12, 18, 36):
            b += text(X0 + (i - 1) * W + 7, Y0 + H + 14, str(i), 10, MUTED)
        if i <= 6 or i in (7, 9, 12, 18, 36):
            b += text(X0 + (i - 1) * W + 7, Y0 + H - h - 5, str(k), 11, TEXT)
    xs = X0 + 6 * W - 1
    b += line(xs, Y0 - 4, xs, Y0 + H + 4, YELLOW, 2, dash="5 4")
    b += text(xs + 6, Y0 + 10, "i = √x", 12, YELLOW, "start")
    b += text(X0 + 3 * W, Y0 + H + 42, "i ≤ √x: не больше √x значений", 12, BLUE, "start")
    b += text(X0 + 17 * W, Y0 + H + 42, "i > √x: значение ⌊x / i⌋ < √x", 12, GREEN, "start")
    b += text(380, 332, "переход: i ← ⌊x / ⌊x / i⌋⌋ + 1", 15, YELLOW)
    return figure(svg(760, 350, b), "Слева — не больше √x разных i (каждое со своим значением), справа — значения меньше √x, их тоже не больше √x. Каждая «ступенька» перебирается за O(1).")


def fig_query_blocks():
    b = text(380, 24, "Корневая по запросам: блок из B запросов и «прибитые гвоздями» рёбра", 15)
    X0, W = 80, 640
    ys = {"A": 70, "B": 100, "C": 130, "D": 160, "E": 190}
    spans = {"A": (0, 1.0, False), "B": (0, 0.4, True), "C": (0.35, 0.75, True), "D": (0.3, 1.0, True), "E": (0.62, 0.9, True)}
    for k in range(5):
        x = X0 + k * W / 4
        b += line(x, 50, x, 224, EDGE, 1.5, dash="5 4")
    b += text(X0 + W / 8, 44, "блок 1", 12, MUTED) + text(X0 + 3 * W / 8, 44, "блок 2", 12, MUTED) + text(X0 + 5 * W / 8, 44, "блок 3", 12, MUTED) + text(X0 + 7 * W / 8, 44, "блок 4", 12, MUTED)
    for name, y in ys.items():
        s, e, fl = spans[name]
        col = ORANGE if fl and name in "BCD" else BLUE
        # для блока 2 (0.25–0.5) определим, плавающее ли
        b += text(X0 - 14, y + 5, f"ребро {name}", 12, MUTED, "end")
        b += f'<rect x="{X0 + s * W}" y="{y - 6}" width="{(e - s) * W}" height="12" rx="6" fill="{SOFT[col]}" stroke="{col}" stroke-width="1.5"/>'
    # подсветка блока 2
    b += f'<rect x="{X0 + W / 4}" y="52" width="{W / 4}" height="172" fill="{YELLOW}" opacity="0.07"/>'
    b += text(X0 + W * 3 / 8, 244, "в блоке 2 меняются B, C, D; A — «прибито»", 12, YELLOW)
    b += text(380, 282, "рёбра, не менявшиеся внутри блока, ведут себя как константа — их обрабатываем один раз на весь блок", 13, TEXT)
    b += text(380, 304, "остальных не больше B: ими управляем «в лоб» на каждый запрос", 13, TEXT)
    b += text(380, 332, "время: (q / B)·(предподсчёт) + q·(работа с B плавающими рёбрами)", 14, GREEN)
    return figure(svg(760, 350, b), "Удаления не мешают: ребро, которое добавлялось или удалялось внутри блока, объявляется плавающим сразу на весь блок, и таких рёбер не больше B.")


FIGS = {"blocks_query": fig_blocks_query, "prefix_lazy": fig_prefix_lazy, "strips": fig_strips, "mo_snake": fig_mo_snake,
        "mex_blocks": fig_mex_blocks, "euler_twice": fig_euler_twice, "heavy_light": fig_heavy_light,
        "jump_residues": fig_jump_residues, "floor_blocks": fig_floor_blocks, "query_blocks": fig_query_blocks}
