"""Иллюстрации и плееры для «Занятие 2. Параллель BS — бинарный поиск и два указателя»."""
import json, math
from kit import *


def poly(pts, color, w=3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{w}"{d}/>'


# ---------------------------------------------------------------- делим пополам
def fig_halve():
    b = text(380, 24, "Угадываем число от 1 до 100: каждый вопрос вдвое сужает область", 15)
    sizes = [100, 50, 25, 13, 7, 4, 2, 1]
    for i, s in enumerate(sizes):
        y = 48 + i * 30
        w = s * 6
        b += f'<rect x="{80}" y="{y}" width="{w}" height="22" rx="4" fill="{SOFT[BLUE] if i < 7 else SOFT[GREEN]}" stroke="{BLUE if i < 7 else GREEN}" stroke-width="1.5"/>'
        b += text(60, y + 16, f"{i}", 12, MUTED, "end") + text(80 + w + 10, y + 16, f"{s}", 13, TEXT, "start")
    b += text(560, 110, "2⁶ = 64 < 100 ≤ 2⁷ = 128", 14, YELLOW, "start")
    b += text(560, 140, "значит нужно 7 вопросов:", 14, TEXT, "start")
    b += text(560, 164, "⌈log₂ 100⌉ = 7", 16, GREEN, "start", "700")
    b += text(560, 200, "основание логарифма в", 13, MUTED, "start") + text(560, 218, "асимптотике не пишут", 13, MUTED, "start")
    return figure(svg(760, 300, b), "После каждого вопроса остаётся половина кандидатов; за $7$ вопросов от $100$ остаётся один. Число вопросов — это $\\lceil\\log_2 n\\rceil$.")


# ---------------------------------------------------------------- нули и единицы
def fig_zero_one():
    b = text(380, 24, "Бинпоиск — это поиск границы между «нет» и «да»", 15)
    vals = [1, 2, 2, 3, 3, 3, 5, 5, 6]
    x = 3
    for i, v in enumerate(vals):
        ok = v >= x
        b += cell(70 + i * 70, 56, 62, 36, str(v), GREEN if ok else RED, 16)
        b += text(70 + i * 70 + 31, 112, "1" if ok else "0", 14, GREEN if ok else RED, weight="700")
    b += text(24, 78, "a[i]", 12, MUTED, "start") + text(24, 112, "a[i]≥3", 12, MUTED, "start")
    b += line(70 + 3 * 70 - 4, 126, 70 + 3 * 70 - 4, 150, YELLOW, 2)
    b += line(70 + 3 * 70 + 35, 170, 70 + 3 * 70 + 35, 120, GREEN, 2, arrow=True) + text(70 + 3 * 70 + 35, 190, "r — первая «1»", 13, GREEN)
    b += line(70 + 2 * 70 + 31, 170, 70 + 2 * 70 + 31, 120, RED, 2, arrow=True) + text(70 + 2 * 70 + 31, 190, "l — последний «0»", 13, RED)
    b += text(380, 230, "l и r сходятся к границе: на каждом шаге a[l] — «0», a[r] — «1»", 14)
    b += text(380, 254, "это и есть lower_bound(3): первый индекс с a[i] ≥ 3 (ответ 3)", 13, MUTED)
    return figure(svg(760, 276, b), "Условие делит массив на нули и единицы; бинпоиск находит их границу за $O(\\log n)$ проверок.")


# ---------------------------------------------------------------- коровы
def fig_cows():
    xs = [1, 3, 7, 8, 12, 13, 18]
    b = text(380, 24, "Стойла и расстояние d = 5: ставим корову, как только расстояние достаточно", 15)
    X = lambda v: 50 + v * 36
    b += line(40, 100, 720, 100, AXIS, 2)
    last = None; cows = []
    for v in xs:
        if last is None or v - last >= 5: cows.append(v); last = v
    for v in xs:
        c = v in cows
        b += circle(X(v), 100, 11, "", GREEN if c else None)
        b += text(X(v), 128, str(v), 12, MUTED)
        if c: b += text(X(v), 76, "🐄", 18)
    for a, c in zip(cows, cows[1:]):
        b += line(X(a), 150, X(c), 150, YELLOW, 1.5) + text((X(a) + X(c)) / 2, 168, f"{c - a}", 13, YELLOW)
    b += text(380, 208, f"поставлено {len(cows)} коров при d = 5", 14)
    b += text(380, 232, f"если нужно не больше {len(cows)} коров — d = 5 подходит; чем больше d, тем меньше коров помещается → ответ монотонен", 13, MUTED)
    return figure(svg(760, 252, b), "Проверка «помещаются ли $k$ коров с расстоянием $\\ge d$» — жадность за один проход; затем бинпоиск по $d$.")


# ---------------------------------------------------------------- тернарный поиск
def _curve(f, x0, x1, X, Y, n=80):
    return [(X(x0 + (x1 - x0) * i / n), Y(f(x0 + (x1 - x0) * i / n))) for i in range(n + 1)]


def fig_tern():
    f = lambda x: 1 - (x - 0.55) ** 2 * 2.2
    X = lambda x: 60 + x * 300; Y = lambda y: 190 - y * 130
    def panel(ox, m1, m2, cut_right):
        s = f'<g transform="translate({ox},0)">'
        s += line(50, 190, 380, 190, AXIS, 1.5)
        s += poly(_curve(f, 0, 1, X, Y), BLUE, 3)
        for m, nm in ((m1, "m₁"), (m2, "m₂")):
            s += line(X(m), 190, X(m), Y(f(m)), YELLOW, 1.5, "4 3") + circle(X(m), Y(f(m)), 5, "", YELLOW) + text(X(m), 208, nm, 13, YELLOW)
        if cut_right: s += f'<rect x="{X(m2)}" y="48" width="{X(1) - X(m2)}" height="140" fill="{RED}" opacity=".18"/>'
        else: s += f'<rect x="{X(0)}" y="48" width="{X(m1) - X(0)}" height="140" fill="{RED}" opacity=".18"/>'
        s += text(X(0), 208, "l", 13, MUTED) + text(X(1), 208, "r", 13, MUTED)
        return s + "</g>"
    b = text(190, 26, "f(m₁) > f(m₂): r := m₂", 14, GREEN) + text(570, 26, "f(m₁) ≤ f(m₂): l := m₁", 14, GREEN)
    b += panel(-20, 1 / 3, 2 / 3 + 0.1, True)
    b += panel(360, 1 / 3 - 0.05, 2 / 3 - 0.02, False).replace("f(m₁)", "f(m₁)")
    b += text(380, 250, "красное отбрасываем: там максимума нет, потому что слева от пика функция растёт, а справа убывает", 13, MUTED)
    return figure(svg(760, 270, b), "Тернарный поиск максимума: по сравнению значений в двух точках отбрасываем треть отрезка, в которой максимума заведомо нет.")


def fig_plateau():
    b = text(380, 24, "Плато ломает тернарный поиск", 15)
    pts = [(60, 170), (200, 90), (330, 90), (460, 90), (560, 40), (680, 170)]
    b += line(50, 190, 710, 190, AXIS, 1.5)
    b += poly(pts, BLUE, 3)
    b += line(250, 190, 250, 90, YELLOW, 1.5, "4 3") + circle(250, 90, 5, "", YELLOW) + text(250, 208, "m₁", 13, YELLOW)
    b += line(400, 190, 400, 90, YELLOW, 1.5, "4 3") + circle(400, 90, 5, "", YELLOW) + text(400, 208, "m₂", 13, YELLOW)
    b += circle(560, 40, 6, "", GREEN) + text(560, 28, "максимум", 13, GREEN)
    b += text(380, 236, "f(m₁) = f(m₂): по значениям не понять, где максимум — слева или справа от плато", 13, MUTED)
    b += text(380, 258, "если сдвинуть любую границу, можно потерять точку максимума", 13, RED)
    return figure(svg(760, 280, b), "Тернарный поиск требует строгой унимодальности: на плато сравнение $f(m_1)$ и $f(m_2)$ ничего не говорит.")


# ---------------------------------------------------------------- два указателя
def fig_twoptr():
    a = [2, 1, 3, 4, 2, 5, 1, 3]
    b = text(380, 24, "Два указателя: отрезок [l, r) и его сумма; ищем сумму S = 9", 15)
    l, r = 3, 5
    for i, v in enumerate(a):
        col = YELLOW if l <= i < r else None
        b += cell(70 + i * 76, 60, 66, 40, str(v), col, 17) + text(70 + i * 76 + 33, 118, str(i), 11, MUTED)
    b += line(70 + l * 76 - 3, 134, 70 + r * 76 - 10, 134, YELLOW, 3) + text((70 + l * 76 + 70 + r * 76) / 2 - 6, 154, "[l, r) — сумма 6 < 9", 13, YELLOW)
    b += line(70 + l * 76, 190, 70 + l * 76, 160, GREEN, 2, arrow=True) + text(70 + l * 76 + 6, 208, "l", 14, GREEN)
    b += line(70 + r * 76 - 10, 190, 70 + r * 76 - 10, 160, ORANGE, 2, arrow=True) + text(70 + r * 76 - 10, 208, "r", 14, ORANGE)
    b += text(380, 240, "cur < S → сдвигаем r вправо;  cur > S → сдвигаем l вправо;  cur = S → нашли", 14)
    b += text(380, 264, "каждый указатель только растёт — всего ≤ 2n шагов", 13, MUTED)
    return figure(svg(760, 286, b), "Для неотрицательных чисел сумма окна растёт при расширении и убывает при сжатии — это и есть монотонность.")


def fig_inv():
    b = text(380, 24, "Почему не пропустим ответ: нужный отрезок [L*, R*) не может лежать «левее» текущих указателей", 14)
    b += line(60, 90, 700, 90, AXIS, 2)
    b += cell(240, 70, 200, 40, "", YELLOW) + text(340, 96, "текущий [l, r)", 14, YELLOW)
    b += cell(300, 150, 90, 30, "", ORANGE) + text(345, 170, "[L*, R*)", 13, ORANGE)
    b += text(345, 200, "внутри: сумма в нём ≤ суммы текущего", 12, MUTED)
    b += text(380, 232, "значит r не двигали бы вправо (мы расширяем r, только если сумма < S)", 13, TEXT)
    b += text(380, 254, "аналогично для l: левую границу сдвигаем, только если сумма уже > S, а такой отрезок ответом не был", 13, TEXT)
    return figure(svg(760, 276, b), "Инвариант: $l\\le L^*$ и $r\\le R^*$ для любого ещё не найденного ответа; идея доказательства от противного.")


# ---------------------------------------------------------------- единичный квадрат
def fig_square():
    X = lambda x: 80 + x * 300; Y = lambda y: 270 - y * 240
    b = text(380, 20, "Скорость v₁ при x < r, скорость v₂ при x ≥ r; ломаная (0,0) → (r, y) → (1,1)", 14)
    b += f'<rect x="{X(0)}" y="{Y(1)}" width="300" height="240" fill="none" stroke="{AXIS}" stroke-width="1.5"/>'
    r, y = 0.45, 0.62
    b += f'<rect x="{X(0)}" y="{Y(1)}" width="{X(r) - X(0)}" height="240" fill="{BLUE}" opacity=".10"/>'
    b += line(X(r), Y(0), X(r), Y(1), YELLOW, 2, "5 3") + text(X(r), Y(0) + 18, "x = r", 13, YELLOW)
    b += line(X(0), Y(0), X(r), Y(y), GREEN, 3) + line(X(r), Y(y), X(1), Y(1), ORANGE, 3)
    b += circle(X(r), Y(y), 6, "", RED) + text(X(r) + 14, Y(y) - 8, "(r, y)", 13, RED, "start")
    b += circle(X(0), Y(0), 5, "") + circle(X(1), Y(1), 5, "")
    b += text(X(0) + 12, Y(1) + 34, "v₁", 15, BLUE, "start") + text(X(1) - 12, Y(1) + 34, "v₂", 15, ORANGE, "end")
    b += text(470, 80, "время(y) =", 14, TEXT, "start")
    b += text(470, 108, "√(r² + y²) / v₁", 15, GREEN, "start")
    b += text(470, 134, "+ √((1−r)² + (1−y)²) / v₂", 15, ORANGE, "start")
    b += text(470, 176, "обе части выпуклы по y →", 13, MUTED, "start") + text(470, 196, "сумма выпукла →", 13, MUTED, "start")
    b += text(470, 216, "тернарный поиск по y ∈ [0, 1]", 14, YELLOW, "start")
    return figure(svg(760, 300, b), "Минимизируем время по ординате $y$ точки пересечения границы $x=r$; на каждой стороне оптимально идти прямо.")


# ---------------------------------------------------------------- фонари
def fig_lamps():
    h = [2, 4, 5, 8, 11, 12, 16]
    R = 2
    b = text(380, 24, "Радиус R = 2: ставим фонарь в (самый левый неосвещённый дом) + R", 15)
    X = lambda v: 50 + v * 38
    b += line(40, 120, 720, 120, AXIS, 2)
    pos = []; i = 0
    covered = set()
    while i < len(h):
        p = h[i] + R; pos.append(p)
        for j, v in enumerate(h):
            if abs(v - p) <= R: covered.add(j)
        i = max(j for j in covered) + 1
    cols = [BLUE, GREEN, ORANGE, PURPLE]
    for k, p in enumerate(pos):
        b += f'<rect x="{X(p - R)}" y="{96}" width="{X(p + R) - X(p - R)}" height="48" fill="{cols[k % 4]}" opacity=".16" stroke="{cols[k % 4]}" stroke-width="1.2"/>'
        b += text(X(p), 82, "💡", 18) + text(X(p), 166, f"p={p}", 12, cols[k % 4])
    for v in h:
        b += circle(X(v), 120, 8, "", YELLOW) + text(X(v), 190, str(v), 12, MUTED)
    b += text(380, 224, f"домов: {len(h)}, понадобилось фонарей: {len(pos)}; если k ≥ {len(pos)} — радиус 2 подходит", 14)
    return figure(svg(760, 246, b), "Крайний дом обязан быть освещён; фонарь выгодно сдвинуть вправо до границы его зоны — левее освещать нечего.")


# ---------------------------------------------------------------- пик
def fig_peak():
    a = [3, 5, 8, 6, 2, 4, 7, 1]
    b = text(380, 24, "a[−1] = a[n] = −∞, соседние различны: локальный максимум существует всегда", 14)
    base = 200
    for i, v in enumerate(a):
        h = v * 18
        col = GREEN if i == 2 else (ORANGE if i == 6 else BLUE)
        b += f'<rect x="{110 + i * 70}" y="{base - h}" width="52" height="{h}" rx="4" fill="{SOFT[col]}" stroke="{col}" stroke-width="1.8"/>'
        b += text(110 + i * 70 + 26, base - h - 8, str(v), 13) + text(110 + i * 70 + 26, base + 18, str(i), 11, MUTED)
    b += text(60, base - 4, "−∞", 13, MUTED) + text(700, base - 4, "−∞", 13, MUTED)
    b += text(380, 244, "m: если a[m] < a[m+1] — пик справа (l := m+1), иначе пик в [l, m] (r := m)", 13, MUTED)
    return figure(svg(760, 264, b), "Любой подъём вправо рано или поздно кончается: либо спуск, либо $-\\infty$ на краю — значит пик внутри.")


# ---------------------------------------------------------------- медиана
def fig_median():
    pts = [1, 2, 6, 7, 11]
    X = lambda v: 60 + v * 54
    f = lambda x: sum(abs(x - p) for p in pts)
    Y = lambda y: 250 - y * 4.8
    b = text(380, 24, "f(x) = Σ|x − pᵢ| — ломаная, наклон меняется на каждой точке", 15)
    b += line(50, 250, 720, 250, AXIS, 1.5)
    b += poly([(X(x / 10), Y(f(x / 10))) for x in range(0, 125)], BLUE, 3)
    for p in pts: b += circle(X(p), 250, 5, "", YELLOW) + text(X(p), 270, str(p), 12, MUTED)
    b += circle(X(6), Y(f(6)), 7, "", GREEN) + text(X(6), Y(f(6)) - 14, "медиана", 13, GREEN)
    b += text(110, 70, "наклон = (точек слева) − (точек справа)", 13, MUTED, "start")
    b += text(110, 92, "до медианы наклон < 0, после — > 0", 13, MUTED, "start")
    return figure(svg(760, 290, b), "Сдвиг вправо на $\\delta$ меняет сумму на $\\delta\\,(\\#\\text{слева}-\\#\\text{справа})$; минимум — там, где знак меняется.")


# ---------------------------------------------------------------- работники: не унимодально
def fig_workers():
    n, K, t = 4, 1, 1
    f = [K * w + (-(-n // w) * t) ** 2 for w in range(1, n + 1)]
    b = text(380, 24, "n = 4, K = 1, t = 1:  f(w) = w + ⌈4/w⌉²", 15)
    for w, v in enumerate(f, start=1):
        h = v * 9
        col = GREEN if v == min(f) else BLUE
        b += f'<rect x="{120 + (w - 1) * 140}" y="{210 - h}" width="80" height="{h}" rx="4" fill="{SOFT[col]}" stroke="{col}" stroke-width="1.8"/>'
        b += text(120 + (w - 1) * 140 + 40, 210 - h - 8, str(v), 14) + text(120 + (w - 1) * 140 + 40, 232, f"w={w}", 12, MUTED)
    b += text(380, 262, "17 → 6 → 7 → 5: после подъёма снова спуск — функция не унимодальна", 14, RED)
    b += text(380, 284, "тернарный поиск по w может остановиться на 6, хотя минимум 5", 13, MUTED)
    return figure(svg(760, 304, b), "Из-за округления вверх $\\lceil n/w\\rceil$ значения образуют «ступеньки»: унимодальности нет.")


# ---------------------------------------------------------------- плеер: lower_bound
def algo_bsearch(a=(1, 2, 2, 3, 3, 3, 5, 5, 6), x=3):
    a = list(a); n = len(a); frames = []
    def draw(l, r, m, note):
        s = text(24, 22, f"ищем первый индекс i с a[i] ≥ {x}  (l — «нет», r — «да»)", 13, MUTED, "start")
        for i, v in enumerate(a):
            col = None
            if l is not None and i <= l: col = RED
            if r is not None and i >= r: col = GREEN
            if m == i: col = YELLOW
            s += cell(30 + i * 56, 40, 50, 36, str(v), col, 15) + text(30 + i * 56 + 25, 92, str(i), 11, MUTED)
        lab = lambda p, nm, c: (text(30 + p * 56 + 25, 118, nm, 13, c, weight="700") if 0 <= p < n else "")
        s += lab(l, "l", RED) + lab(r, "r", GREEN) + (lab(m, "m", YELLOW) if m is not None else "")
        if l is not None and l < 0: s += text(30, 118, "l = −1", 12, RED, "start")
        if r is not None and r >= n: s += text(30 + n * 56 - 6, 118, f"r = {n}", 12, GREEN, "end")
        s += text(24, 152, note, 13, MUTED, "start")
        return s
    l, r = -1, n
    frames.append({"svg": draw(l, r, None, "инвариант: a[l] < x (или l = −1), a[r] ≥ x (или r = n)"), "msg": f"Старт: l = −1, r = {n}. Между ними ещё нужно найти границу."})
    while r - l > 1:
        m = (l + r) // 2
        if a[m] < x:
            frames.append({"svg": draw(l, r, m, f"a[{m}] = {a[m]} < {x} → l := m"), "msg": f"m = {m}, a[m] = {a[m]} < {x}: m — «нулевой», ответ правее, l := {m}."}); l = m
        else:
            frames.append({"svg": draw(l, r, m, f"a[{m}] = {a[m]} ≥ {x} → r := m"), "msg": f"m = {m}, a[m] = {a[m]} ≥ {x}: m — «единичный», ответ в m или левее, r := {m}."}); r = m
    frames.append({"svg": draw(l, r, None, f"r − l = 1: ответ r = {r}"), "msg": f"Границы сошлись: r = {r} — первый индекс с a[i] ≥ {x}."})
    return {"title": "lower_bound: поиск границы нулей и единиц", "vb": "0 0 540 170", "frames": frames}


# ---------------------------------------------------------------- плеер: тернарный поиск
def algo_tern():
    f = lambda x: 10 - (x - 6.3) ** 2
    l, r = 0.0, 10.0; frames = []
    W, H = 560, 230
    X = lambda x: 30 + x * 50; Y = lambda y: 190 - (y + 5) * 7
    def draw(l, r, m1, m2, note):
        s = line(24, 200, 540, 200, AXIS, 1.5)
        s += poly([(X(i / 10), Y(f(i / 10))) for i in range(0, 101)], BLUE, 2.5)
        s += f'<rect x="{X(l)}" y="40" width="{X(r) - X(l)}" height="160" fill="{GREEN}" opacity=".10"/>'
        s += text(X(l), 216, "l", 13, GREEN) + text(X(r), 216, "r", 13, GREEN)
        for m, nm in ((m1, "m₁"), (m2, "m₂")):
            if m is not None: s += line(X(m), 200, X(m), Y(f(m)), YELLOW, 1.5, "4 3") + circle(X(m), Y(f(m)), 5, "", YELLOW) + text(X(m), 230, nm, 13, YELLOW)
        s += text(24, 22, note, 13, MUTED, "start")
        return s
    frames.append({"svg": draw(l, r, None, None, "ищем максимум на [0, 10]"), "msg": "Функция унимодальна: растёт до точки максимума и убывает после неё."})
    for k in range(6):
        m1 = l + (r - l) / 3; m2 = r - (r - l) / 3
        if f(m1) > f(m2):
            frames.append({"svg": draw(l, r, m1, m2, f"f(m₁) = {f(m1):.1f} > f(m₂) = {f(m2):.1f} → r := m₂"), "msg": f"f(m₁) > f(m₂): правее m₂ максимума нет, r := {m2:.2f}."}); r = m2
        else:
            frames.append({"svg": draw(l, r, m1, m2, f"f(m₁) = {f(m1):.1f} ≤ f(m₂) = {f(m2):.1f} → l := m₁"), "msg": f"f(m₁) ≤ f(m₂): левее m₁ максимума нет, l := {m1:.2f}."}); l = m1
    frames.append({"svg": draw(l, r, None, None, f"отрезок [{l:.2f}, {r:.2f}] — длина уменьшилась в (3/2)⁶ ≈ 11 раз"), "msg": "После шести шагов отрезок сжался в $(3/2)^6$ раз; настоящий максимум в $x=6.3$."})
    frames[-1]["msg"] = f"После шести шагов отрезок сжался примерно в 11 раз; настоящий максимум в x = 6.3."
    return {"title": "Тернарный поиск максимума", "vb": f"0 0 {W} {H}", "frames": frames}


# ---------------------------------------------------------------- плеер: два указателя
def algo_twoptr(a=(2, 1, 3, 4, 2, 5, 1, 3), S=9):
    a = list(a); n = len(a); frames = []
    def draw(l, r, cur, note):
        s = text(24, 22, f"ищем отрезок с суммой S = {S}  (окно [l, r))", 13, MUTED, "start")
        for i, v in enumerate(a):
            s += cell(30 + i * 56, 40, 50, 36, str(v), YELLOW if l <= i < r else None, 15) + text(30 + i * 56 + 25, 92, str(i), 11, MUTED)
        s += text(30 + l * 56 + 25, 114, "l", 14, GREEN, weight="700") + text(30 + r * 56 - 3, 114, "r", 14, ORANGE, weight="700")
        s += text(24, 146, f"сумма окна = {cur}", 15, BLUE, "start") + text(24, 170, note, 13, MUTED, "start")
        return s
    l = r = 0; cur = 0
    frames.append({"svg": draw(l, r, cur, "окно пусто"), "msg": "Окно пусто: l = r = 0, сумма 0."})
    while True:
        if cur == S and r > l:
            frames.append({"svg": draw(l, r, cur, f"нашли: [{l}, {r})"), "msg": f"Сумма равна {S}: отрезок [{l}, {r}) — ответ."}); break
        if cur < S or r == l:
            if r == n: frames.append({"svg": draw(l, r, cur, "r = n, расширять нечем"), "msg": "Правый конец достиг конца массива — ответа нет."}); break
            cur += a[r]; r += 1
            frames.append({"svg": draw(l, r, cur, f"сумма меньше {S} → r++ (добавили {a[r - 1]})"), "msg": f"Сумма меньше {S}: сдвигаем r, добавляем {a[r - 1]}."})
        else:
            cur -= a[l]; l += 1
            frames.append({"svg": draw(l, r, cur, f"сумма больше {S} → l++ (убрали {a[l - 1]})"), "msg": f"Сумма больше {S}: сдвигаем l, убираем {a[l - 1]}."})
    return {"title": "Два указателя: отрезок с заданной суммой", "vb": "0 0 480 190", "frames": frames}


# ---------------------------------------------------------------- плеер: коровы
def algo_cows(xs=(1, 3, 7, 8, 12, 13, 18), k=3):
    frames = []
    lo, hi = 0, xs[-1] - xs[0] + 1
    X = lambda v: 30 + v * 24
    def draw(d, cows, note, cur=None):
        s = text(24, 22, f"k = {k} коров, проверяем расстояние d = {d}", 13, MUTED, "start") if d is not None else ""
        s += line(24, 80, 480, 80, AXIS, 2)
        for v in xs:
            c = v in cows
            s += circle(X(v), 80, 9, "", GREEN if c else (YELLOW if v == cur else None)) + text(X(v), 108, str(v), 11, MUTED)
        s += text(24, 140, note, 13, MUTED, "start")
        return s
    def place(d):
        cows = [xs[0]]
        for v in xs[1:]:
            if v - cows[-1] >= d: cows.append(v)
        return cows
    frames.append({"svg": draw(0, [], f"бинпоиск по ответу d ∈ [0, {hi - 1}]"), "msg": "Ищем наибольшее d, при котором помещаются k коров. Ответ монотонен: чем больше d, тем меньше коров."})
    l, r = lo, hi
    while r - l > 1:
        m = (l + r) // 2
        cows = place(m); ok = len(cows) >= k
        frames.append({"svg": draw(m, cows, f"d = {m}: помещается {len(cows)} коров → {'подходит, l := ' + str(m) if ok else 'не подходит, r := ' + str(m)}"),
                       "msg": f"d = {m}: жадно ставим коров — получается {len(cows)}. {'Хватает (≥ ' + str(k) + '): l := ' + str(m) if ok else 'Мало (< ' + str(k) + '): r := ' + str(m)}."})
        if ok: l = m
        else: r = m
    frames.append({"svg": draw(l, place(l), f"ответ: d = {l}"), "msg": f"Границы сошлись: наибольшее подходящее d = {l}."})
    return {"title": "Бинпоиск по ответу: коровы в стойлах", "vb": "0 0 500 160", "frames": frames}


FIGS = {"halve": fig_halve, "zero_one": fig_zero_one, "cows": fig_cows, "tern": fig_tern, "plateau": fig_plateau,
        "twoptr": fig_twoptr, "inv": fig_inv, "square": fig_square, "lamps": fig_lamps, "peak": fig_peak,
        "median": fig_median, "workers": fig_workers}


def algos_js():
    data = {"bsearch": algo_bsearch(), "tern": algo_tern(), "twoptr": algo_twoptr(), "cows": algo_cows()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
