"""Иллюстрации и плееры для «Занятие 2. Параллель X — Теория чисел»."""
import json
from kit import *


def euc_rows(a, b):
    """Строки (s, q, x, y); q_i = s_{i-1} // s_i — сколько раз строку i вычитаем из строки i-1."""
    s = [a, b]; x = [1, 0]; y = [0, 1]
    while s[-1] != 0:
        q = s[-2] // s[-1]
        s.append(s[-2] - q * s[-1]); x.append(x[-2] - q * x[-1]); y.append(y[-2] - q * y[-1])
    return [(s[i], (s[i - 1] // s[i] if i >= 1 and s[i] != 0 else None), x[i], y[i]) for i in range(len(s))]


def fig_euc():
    rows = euc_rows(13, 7)
    b = text(380, 24, "Алгоритм Евклида для (13, 7) с двумя дополнительными столбцами", 15)
    heads = ["i", "s", "q", "x", "y", "s = 13x + 7y"]
    xs = [60, 140, 220, 300, 380, 520]
    for h, x in zip(heads, xs): b += text(x, 56, h, 13, MUTED)
    for i, (s, q, x, y) in enumerate(rows):
        yy = 66 + i * 38
        last = i == len(rows) - 1; g = i == len(rows) - 2
        col = GREEN if g else (RED if last else None)
        vals = [str(i), str(s), "" if q is None else str(q), str(x), str(y), f"13·({x}) + 7·({y}) = {13 * x + 7 * y}"]
        for v, xx, w in zip(vals, xs, [50, 60, 60, 60, 60, 220]):
            if v != "": b += cell(xx - w / 2, yy, w, 30, v, col, 14)
    b += text(380, 66 + len(rows) * 38 + 22, "предпоследняя строка: НОД = 1 = 13·(−1) + 7·2;  последняя: (x, y) = (7, −13) = (b/g, −a/g)", 13, YELLOW)
    return figure(svg(760, 66 + len(rows) * 38 + 40, b), "Каждая строка — равенство $s_i = a x_i + b y_i$. Новая строка получается вычитанием $q_i$ раз предыдущей, поэтому равенство сохраняется для всех трёх чисел сразу.")


def fig_sb():
    b = text(380, 24, "Дерево Штерна—Броко: у вершины с границами a/b и c/d значение (a+c)/(b+d)", 15)
    levels = [[(1, 1)], [(1, 2), (2, 1)], [(1, 3), (2, 3), (3, 2), (3, 1)], [(1, 4), (2, 5), (3, 5), (3, 4), (4, 3), (5, 3), (5, 2), (4, 1)]]
    path = {(1, 1), (1, 2), (2, 3), (3, 5)}
    pos = {}
    for d, lv in enumerate(levels):
        for i, f in enumerate(lv):
            pos[f] = (380 + (i - (len(lv) - 1) / 2) * (680 / len(lv)) * (1 if d else 0), 60 + d * 70)
    kids = {(1, 1): [(1, 2), (2, 1)], (1, 2): [(1, 3), (2, 3)], (2, 1): [(3, 2), (3, 1)],
            (1, 3): [(1, 4), (2, 5)], (2, 3): [(3, 5), (3, 4)], (3, 2): [(4, 3), (5, 3)], (3, 1): [(5, 2), (4, 1)]}
    for f, cs in kids.items():
        for g in cs:
            on = f in path and g in path
            b += line(pos[f][0], pos[f][1], pos[g][0], pos[g][1], GREEN if on else EDGE, 3 if on else 2)
    for f, (x, y) in pos.items():
        col = GREEN if f in path else None
        b += circle(x, y, 24, "", col) + text(x, y + 5, f"{f[0]}/{f[1]}", 13)
    b += text(380, 318, "путь к 7/13:  1/1 → 1/2 → 2/3 → 3/5 → 4/7 → 5/9 → 6/11 → 7/13 ,  то есть  L R L L L L L", 13, YELLOW)
    b += text(380, 340, "длины серий  1, 1, 5  =  q₁, q₂, q₃ − 1  из алгоритма Евклида для (13, 7)", 13, MUTED)
    return figure(svg(760, 360, b), "Каждая положительная несократимая дробь встречается ровно один раз; путь в дереве — это последовательность $q_i$ алгоритма Евклида (серии шагов влево и вправо чередуются).")


def fig_lattice(m=29, a=12):
    rows = []
    r0, t0, r1, t1 = m, 0, a, 1
    rows = [(r0, t0), (r1, t1)]
    while rows[-1][0] != 0:
        (ra, ta), (rb, tb) = rows[-2], rows[-1]
        q = ra // rb
        rows.append((ra - q * rb, ta - q * tb))
    X0, X1 = -14, 30
    sx, sy, ox, oy = 15, 9, 70, 290
    px = lambda x: ox + (x - X0) * sx
    py = lambda y: oy - y * sy
    b = text(380, 22, f"Решётка точек (x, y) с y ≡ {a}·x (mod {m}); точки алгоритма Евклида (x = tᵢ, y = rᵢ)", 15)
    b += line(px(X0), py(0), px(X1), py(0), AXIS, 1.5) + line(px(0), py(0), px(0), py(m + 2), AXIS, 1.5)
    b += text(px(X1) - 6, py(0) + 16, "x", 12, MUTED) + text(px(0) + 12, py(m + 2) + 12, "y", 12, MUTED)
    for x in range(X0, X1 + 1):
        y = (a * x) % m
        for yy in (y, y + m):
            if 0 <= yy <= m + 1: b += f'<circle cx="{px(x)}" cy="{py(yy)}" r="2.6" fill="#3b4a63"/>'
    pts = [(t, r) for r, t in rows]
    b += "".join(line(px(pts[i][0]), py(pts[i][1]), px(pts[i + 1][0]), py(pts[i + 1][1]), YELLOW, 2) for i in range(len(pts) - 1))
    for i, (x, y) in enumerate(pts):
        b += circle(px(x), py(y), 6, "", GREEN) + text(px(x) + 14, py(y) - 8, f"({x}; {y})", 11, GREEN, "start")
    b += text(380, 326, "все точки — целочисленная комбинация (1; a) и (0; m); точки Евклида образуют нижнюю выпуклую оболочку и оптимальны по Парето", 12, MUTED)
    return figure(svg(760, 340, b), "Рациональная реконструкция: $p/q\\equiv a$ означает точку $(q, p)$ этой решётки в маленьком прямоугольнике; кандидатов дают лишь точки алгоритма Евклида.")


def fig_floor():
    a, bb, c, n = 3, 1, 5, 8
    sx, sy, ox, oy = 70, 50, 60, 250
    b = text(380, 22, f"Σ ⌊({a}x+{bb})/{c}⌋ по x = 1..{n}: число целых точек под прямой", 15)
    b += line(ox, oy, ox + (n + 1) * sx, oy, AXIS, 1.5) + line(ox, oy, ox, oy - 5 * sy - 20, AXIS, 1.5)
    b += line(ox, oy - (bb / c) * sy, ox + (n + 1) * sx, oy - ((a * (n + 1) + bb) / c) * sy, YELLOW, 2)
    tot = 0
    for x in range(1, n + 1):
        v = (a * x + bb) // c; tot += v
        b += text(ox + x * sx, oy + 18, str(x), 12, MUTED)
        for y in range(1, v + 1): b += circle(ox + x * sx, oy - y * sy, 8, "", GREEN)
        if v: b += text(ox + x * sx + 20, oy - v * sy + 4, str(v), 11, MUTED, "start")
    b += text(380, 292, f"сумма = {tot};  точки под прямой считаются построчно (по x) или по столбцам (по y) — это и есть замена a ↔ c", 13, YELLOW)
    return figure(svg(760, 308, b), "Комбинаторный смысл суммы: количество точек $(x,y)$, $1\\le x\\le n$, $1\\le y\\le (ax+b)/c$. Если считать по $y$, получается такая же сумма с другими числами — на этом строится алгоритм.")


def fig_string():
    a, c = 3, 5
    s = ""; xr, yr = 0, 0
    # идём вдоль прямой y = 3x/5 от x=0 до x=5: пересечения вертикалей x=k (R) и горизонталей y=k (U)
    ev = []
    for k in range(1, c + 1): ev.append((k / c, "R"))
    for k in range(1, a + 1): ev.append((k / a, "U"))
    ev.sort(key=lambda e: (e[0], 0 if e[1] == "U" else 1))
    s = "".join(e[1] for e in ev)
    b = text(380, 22, "Прямая с наклоном 3/5 — строка из букв R (пересекли вертикаль) и U (пересекли горизонталь)", 15)
    ox, oy, sx, sy = 120, 220, 100, 60
    for i in range(c + 1): b += line(ox + i * sx, oy, ox + i * sx, oy - a * sy, EDGE, 1)
    for j in range(a + 1): b += line(ox, oy - j * sy, ox + c * sx, oy - j * sy, EDGE, 1)
    b += line(ox, oy, ox + c * sx, oy - a * sy, YELLOW, 3)
    b += text(380, 262, "строка:  " + " ".join(s), 18, GREEN, mono=True)
    b += text(380, 290, "равномерность: на любых двух отрезках одинаковой длины число букв R отличается не больше чем на 1", 13, MUTED)
    return figure(svg(760, 310, b), "Равномерная строка. Её можно собирать по алгоритму Евклида, склеивая блоки, и держать в каждой склейке моноид (сумму, число инверсий и т. п.).")


def fig_lintree():
    N = 16
    lp = {}
    for n in range(2, N + 1):
        d = 2
        while n % d: d += 1
        lp[n] = d
    par = {n: n // lp[n] for n in range(2, N + 1)}
    depth = {1: 0}
    for n in range(2, N + 1):
        k, m = 0, n
        while m > 1: m //= lp[m]; k += 1
        depth[n] = k
    by = {}
    for n in range(1, N + 1): by.setdefault(depth[n], []).append(n)
    pos = {}
    for d, lv in by.items():
        for i, n in enumerate(lv): pos[n] = (380 + (i - (len(lv) - 1) / 2) * min(80, 700 / len(lv)), 50 + d * 70)
    b = text(380, 22, "Дерево «предок = n / lp(n)» для n ≤ 16: у каждого числа ровно один предок", 15)
    for n in range(2, N + 1): b += line(pos[n][0], pos[n][1], pos[par[n]][0], pos[par[n]][1], EDGE, 2)
    for n in range(1, N + 1):
        pr = n > 1 and lp[n] == n
        b += circle(pos[n][0], pos[n][1], 17, "", GREEN if pr else None) + text(pos[n][0], pos[n][1] + 5, str(n), 13)
        if n > 1: b += text(pos[n][0] + 22, pos[n][1] - 14, f"{lp[n]}", 10, MUTED, "start")
    b += text(380, 50 + 4 * 70 + 6, "зелёные — простые;  маленькое число — lp(n);  дети числа k:  k·p для простых p ≤ lp(k)", 13, YELLOW)
    return figure(svg(760, 50 + 4 * 70 + 24, b), "Линейное решето обходит это дерево: каждое составное число $n=k\\cdot p$ посещается ровно один раз — как ребёнок $k=n/\\operatorname{lp}(n)$.")


def fig_values():
    n = 36
    big = [n // k for k in range(1, 7)]; small = list(range(1, 7))
    b = text(380, 22, f"Значения ⌊n/k⌋ при n = {n}: всего порядка 2√n различных", 15)
    b += text(30, 70, "k ≤ √n:", 13, MUTED, "start")
    for i, v in enumerate(big):
        b += cell(120 + i * 90, 50, 80, 36, str(v), BLUE, 16, f"k = {i + 1}")
    b += text(30, 150, "v ≤ √n:", 13, MUTED, "start")
    for i, v in enumerate(small):
        b += cell(120 + i * 90, 130, 80, 36, str(v), GREEN, 16)
    b += text(380, 210, "ключ в таблице f: для любого v = ⌊n/k⌋ значение ⌊v/p⌋ снова имеет вид ⌊n/k'⌋", 13, YELLOW)
    return figure(svg(760, 230, b), "Динамика считается только в точках $\\lfloor n/k\\rfloor$: их $\\approx 2\\sqrt n$, и при делении на $p$ мы остаёмся внутри этого множества.")


def fig_conv():
    b = text(380, 22, "Общая схема: преобразование → поэлементное действие → обратное преобразование", 15)
    boxes = [("массив a", None), ("Φ: суммы по кратным", BLUE), ("â", None), ("действие\n(произведение, 2^x…)", ORANGE), ("ĉ", None), ("Φ⁻¹", BLUE), ("ответ c", GREEN)]
    xs = [20, 120, 255, 330, 465, 540, 640]
    ws = [90, 120, 60, 120, 60, 80, 100]
    for (lab, col), x, w in zip(boxes, xs, ws):
        parts = lab.split("\n")
        b += f'<rect x="{x}" y="60" width="{w}" height="64" rx="8" fill="{SOFT[col] if col else NODE}" stroke="{col or EDGE}" stroke-width="2"/>'
        for i, p in enumerate(parts): b += text(x + w / 2, 96 + (i - (len(parts) - 1) / 2) * 16, p, 12)
    for i in range(len(xs) - 1): b += line(xs[i] + ws[i] + 2, 92, xs[i + 1] - 2, 92, MUTED, 2, arrow=True)
    b += text(380, 170, "Φ(f)[x] = Σ f[y] по y, кратным x;   Φ⁻¹ — те же операции в обратном порядке с минусом", 13, YELLOW)
    b += text(380, 194, "Φ нужно считать «на месте»: для x по возрастанию  f[x] += f[2x] + f[3x] + …;  обратное: x по убыванию  f[x] −= f[2x] + …", 12, MUTED)
    return figure(svg(760, 214, b), "Для НОД-свёрток действие — поточечное произведение: число пар с обоими числами, кратными $x$, равно произведению соответствующих счётчиков.")


FIGS = {"euc": fig_euc, "sb": fig_sb, "lattice": fig_lattice, "floor": fig_floor, "string": fig_string,
        "lintree": fig_lintree, "values": fig_values, "conv": fig_conv}


def algo_euc(a=13, b=7):
    rows = euc_rows(a, b)
    frames = []
    def draw(k, note):
        s = text(24, 22, f"НОД({a}, {b}): растём вниз, строка = (s, x, y), всегда s = {a}x + {b}y", 13, MUTED, "start")
        for j, h in enumerate(["i", "s", "q", "x", "y"]): s += text(60 + j * 80, 52, h, 12, MUTED)
        for i in range(k + 1):
            sv, q, x, y = rows[i]
            col = YELLOW if i == k else None
            for j, v in enumerate([str(i), str(sv), "" if q is None else str(q), str(x), str(y)]):
                if v != "": s += cell(60 + j * 80 - 30, 60 + i * 34, 60, 28, v, col, 13)
        s += text(24, 70 + (len(rows)) * 34 + 16, note, 13, MUTED, "start")
        return s
    for k in range(len(rows)):
        if k == 0: msg = f"Строка 0: {a} = {a}·1 + {b}·0."
        elif k == 1: msg = f"Строка 1: {b} = {a}·0 + {b}·1."
        else:
            sv, q, x, y = rows[k]
            msg = f"q = ⌊{rows[k-2][0]} / {rows[k-1][0]}⌋ = {rows[k-1][1]}. Строка {k} = строка {k-2} − {rows[k-1][1]}·(строка {k-1}): s = {sv}, x = {x}, y = {y}."
        if k == len(rows) - 2: msg += f" Это НОД; {a}·({x if False else rows[k][2]}) + {b}·({rows[k][3]}) = {rows[k][0]}."
        if k == len(rows) - 1: msg += f" Последняя строка (x, y) = (±b/g, ∓a/g): ({rows[k][2]}, {rows[k][3]})."
        frames.append({"svg": draw(k, ""), "msg": msg})
    return {"title": f"Расширенный алгоритм Евклида как таблица ({a}, {b})", "vb": f"0 0 460 {80 + len(rows) * 34 + 30}", "frames": frames}


def algo_linsieve(N=30):
    lp = [0] * (N + 1); pr = []; frames = []
    cells = {}
    def draw(i, newly, note):
        s = text(20, 20, "lp[n] — минимальный простой делитель; ячейка заполняется ровно один раз", 13, MUTED, "start")
        for n in range(2, N + 1):
            c = (n - 2) % 10; r = (n - 2) // 10
            x, y = 20 + c * 56, 34 + r * 70
            col = YELLOW if n in newly else (GREEN if lp[n] == n else (BLUE if lp[n] else None))
            s += cell(x, y, 52, 48, str(n), col, 15, sub=(f"lp={lp[n]}" if lp[n] else None))
        s += text(20, 34 + 3 * 70 + 6, note, 13, MUTED, "start")
        return s
    for i in range(2, N // 2 + 1):
        newly = []
        if not lp[i]: lp[i] = i; pr.append(i)
        for p in pr:
            if p > lp[i] or i * p > N: break
            lp[i * p] = p; newly.append(i * p)
        if not newly: continue
        frames.append({"svg": draw(i, newly, f"i = {i}, lp(i) = {lp[i]}: помечаем i·p для простых p ≤ lp(i)"),
                       "msg": f"i = {i} (lp = {lp[i]}). Простые p ≤ {lp[i]}: {', '.join(str(p) for p in pr if p <= lp[i])}. Помечены: {', '.join(f'{i}·{n // i} = {n}' for n in newly)}."})
    for n in range(N // 2 + 1, N + 1):
        if not lp[n]: lp[n] = n; pr.append(n)
    frames.append({"svg": draw(0, [], "готово: остальные простые заполнились при проходе по i"), "msg": f"Все числа до {N} заполнены; простые — {', '.join(map(str, pr))}."})
    return {"title": "Линейное решето для n ≤ 30", "vb": "0 0 590 260", "frames": frames}


def algo_lucy(n=20):
    r = int(n ** 0.5)
    vals = sorted({n // k for k in range(1, n + 1)}, reverse=True)
    f = {v: v - 1 for v in vals}
    frames = []
    def draw(p, note):
        s = text(20, 22, f"f(v) = количество непросеянных чисел среди 2..v;  n = {n}", 13, MUTED, "start")
        for i, v in enumerate(vals):
            s += cell(20 + i * 62, 40, 56, 40, str(f[v]), GREEN if (p and v >= p * p) else None, 16, sub=f"v={v}")
        s += text(20, 120, note, 13, MUTED, "start")
        return s
    frames.append({"svg": draw(0, "начало: f(v) = v − 1 (все числа от 2 до v считаем простыми)"), "msg": "Начальные значения f(v) = v − 1 для всех v вида ⌊n/k⌋."})
    for p in range(2, r + 1):
        if f[p] == f[p - 1]: continue
        cp = f[p - 1]
        for v in vals:
            if v >= p * p: f[v] -= f[v // p] - cp
        frames.append({"svg": draw(p, f"просеяли простое p = {p}: для v ≥ {p*p}:  f(v) −= f(⌊v/{p}⌋) − f({p-1})"),
                       "msg": f"p = {p}: для всех v ≥ {p*p} (подсвечены) вычитаем числа, у которых наименьший простой делитель равен {p}: f(v) −= f(⌊v/{p}⌋) − {cp}."})
    frames.append({"svg": draw(0, f"ответ: π({n}) = f({n}) = {f[n]}"), "msg": f"Остались только простые: π({n}) = {f[n]}."})
    return {"title": f"Подсчёт простых по значениям ⌊n/k⌋, n = {n}", "vb": f"0 0 {40 + len(vals) * 62} 140", "frames": frames}


def algos_js():
    data = {"euc": algo_euc(), "linsieve": algo_linsieve(), "lucy": algo_lucy()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
