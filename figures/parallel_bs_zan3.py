"""Иллюстрации и плеер для «Занятие 3. Параллель BS — Линейные алгоритмы»."""
import json
from kit import *


def bars(x0, base, vals, unit=30, cw=44, colors=None, labels=True, gap=6):
    out = ""
    for i, v in enumerate(vals):
        col = colors.get(i) if colors else None
        fill = SOFT[col] if col else NODE; stroke = col or EDGE
        if v > 0: out += f'<rect x="{x0 + i * cw}" y="{base - v * unit}" width="{cw - gap}" height="{v * unit}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        if labels: out += text(x0 + i * cw + (cw - gap) / 2, base + 18, str(v), 12, MUTED)
    return out


# ---------------------------------------------------------------- объединение отрезков
def fig_union():
    b = text(380, 24, "Сортировка по левому концу; R — самая правая уже учтённая граница", 15)
    segs = [(40, 220, BLUE, "1"), (140, 330, GREEN, "2"), (180, 260, ORANGE, "3"), (400, 540, PURPLE, "4")]
    for i, (l, r, c, n) in enumerate(segs):
        y = 60 + i * 34
        b += f'<rect x="{l}" y="{y}" width="{r - l}" height="22" rx="5" fill="{SOFT[c]}" stroke="{c}" stroke-width="2"/>' + text(l + 12, y + 16, n, 13, TEXT)
    b += line(40, 215, 560, 215, AXIS, 2)
    b += line(330, 205, 330, 225, YELLOW, 3) + text(330, 244, "R после отрезка 2", 12, YELLOW)
    b += text(380, 280, "отрезок 3 целиком внутри (r ≤ R) — пропускаем;  отрезок 4 левее R не заходит — добавляем всю длину", 13, MUTED)
    b += text(380, 302, "три случая: не пересекается · частично пересекается (добавляем r − R) · внутри (ничего)", 13, MUTED)
    return figure(svg(760, 322, b), "Добавка отрезка: $r-\\max(l,R)$, если $r>R$, и ничего иначе; затем $R=\\max(R,r)$.")


# ---------------------------------------------------------------- события
def fig_events():
    b = text(380, 24, "Одна координата — три вида событий; порядок: открыть, запрос, закрыть", 15)
    names = [("открыть отрезок (+1)", GREEN, 0), ("запрос в точке x", YELLOW, 1), ("закрыть отрезок (−1)", RED, 2)]
    for i, (nm, col, pr) in enumerate(names):
        x = 80 + i * 230
        b += cell(x, 70, 190, 54, nm, col, 14) + text(x + 95, 150, f"приоритет {pr}", 13, MUTED)
    b += text(380, 200, "отрезок [l, r] включает обе границы: поэтому при равных координатах", 14)
    b += text(380, 224, "сначала открываем, потом отвечаем, и только потом закрываем", 14, YELLOW)
    b += text(380, 270, "сортировка пар (координата, приоритет, номер) — O((2n + q) log(2n + q))", 13, MUTED)
    return figure(svg(760, 292, b), "Если закрыть отрезок раньше запроса, точка на его правой границе окажется не покрытой — ошибка на ровном месте.")


# ---------------------------------------------------------------- три разворота
def fig_rotate():
    b = text(380, 24, "Циклический сдвиг влево на x = 3 за O(n) времени и O(1) памяти", 15)
    def row(y, vals, hl, title):
        out = text(30, y + 22, title, 12, MUTED, "start")
        for i, v in enumerate(vals):
            c = hl.get(i)
            out += cell(150 + i * 60, y, 54, 34, str(v), c, 15)
        return out
    A = [0, 1, 2]; Bp = [3, 4, 5, 6, 7]
    b += row(50, list(range(8)), {0: BLUE, 1: BLUE, 2: BLUE, 3: GREEN, 4: GREEN, 5: GREEN, 6: GREEN, 7: GREEN}, "исходный")
    b += row(110, [2, 1, 0, 3, 4, 5, 6, 7], {0: BLUE, 1: BLUE, 2: BLUE}, "развернуть [0, x)")
    b += row(170, [2, 1, 0, 7, 6, 5, 4, 3], {3: GREEN, 4: GREEN, 5: GREEN, 6: GREEN, 7: GREEN}, "развернуть [x, n)")
    b += row(230, [3, 4, 5, 6, 7, 0, 1, 2], {0: GREEN, 1: GREEN, 2: GREEN, 3: GREEN, 4: GREEN, 5: BLUE, 6: BLUE, 7: BLUE}, "развернуть всё")
    b += text(380, 290, "(A B) → (Aᴿ Bᴿ) → (Bᴀ): развороты по частям и целиком дают B A", 13, MUTED)
    return figure(svg(760, 310, b), "Попытка сдвигать «по циклам» свопами ломается: значение, которое надо подставить, уже перезаписано, и его пришлось бы искать по всему массиву.")


# ---------------------------------------------------------------- ближайший больший: прыжки
def fig_jumps():
    a = [5, 2, 1, 3, 4, 2, 6]
    b = text(380, 24, "Ближайший больший справа: от i прыгаем по уже найденным ответам b[j]", 15)
    ox, base = 70, 200
    b += bars(ox, base, a, unit=24, cw=84, colors={0: BLUE, 1: ORANGE, 3: GREEN, 4: GREEN, 6: GREEN})
    for i in range(len(a)): b += text(ox + i * 84 + 39, base + 36, f"i={i}", 11, MUTED)
    b += line(ox + 1 * 84 + 39, 70, ox + 3 * 84 + 39, 70, ORANGE, 3, arrow=True) + text(ox + 2 * 84 + 39, 60, "a[2]≤a[1] → j = b[2] = 3", 12, ORANGE)
    b += line(ox + 3 * 84 + 39, 98, ox + 4 * 84 + 39, 98, ORANGE, 3, arrow=True) + text(ox + 3.5 * 84 + 39, 90, "a[3]>a[1]: стоп", 12, ORANGE)
    b += text(380, 275, "глубина прыжков «поднимается» не больше чем на 1 за шаг и не уходит ниже 0 ⇒ суммарно O(n)", 13, MUTED)
    return figure(svg(760, 295, b), "Между $j$ и $b[j]$ нет элементов больше $a[j]$, поэтому весь этот промежуток можно перепрыгнуть одним шагом.")


# ---------------------------------------------------------------- вклад минимума
def fig_contrib():
    a = [3, 1, 4, 1, 5]
    b = text(380, 24, "Сумма минимумов: каждый a[i] минимален в (i − L) · (R − i) подотрезках", 15)
    ox, base = 90, 190
    b += bars(ox, base, a, unit=26, cw=100, colors={2: ORANGE})
    b += f'<rect x="{ox + 1 * 100}" y="{base - 140}" width="{3 * 100 - 6}" height="140" fill="none" stroke="{YELLOW}" stroke-width="2" stroke-dasharray="6 4"/>'
    b += text(ox + 2.5 * 100, base - 148, "i=2: слева ближайший ≤ — позиция 1, справа ближайший < — позиция 5 (нет)", 12, YELLOW)
    b += text(380, 255, "для равных нужно сломать симметрию: слева «≤», справа «<» (или наоборот) — иначе подотрезок с двумя равными минимумами теряется", 12, MUTED)
    return figure(svg(760, 275, b), "Левых границ $i-L$, правых границ $R-i$; выбор левой и правой границы независим, поэтому количество подотрезков — произведение.")


# ---------------------------------------------------------------- гистограмма
def fig_hist():
    h = [2, 1, 5, 6, 2, 3]
    b = text(380, 24, "Наибольший прямоугольник в гистограмме: [2, 1, 5, 6, 2, 3]", 15)
    ox, base = 100, 220
    b += bars(ox, base, h, unit=28, cw=90, colors={2: ORANGE, 3: ORANGE})
    b += f'<rect x="{ox + 2 * 90}" y="{base - 5 * 28}" width="{2 * 90 - 6}" height="{5 * 28}" fill="none" stroke="{YELLOW}" stroke-width="3" stroke-dasharray="6 4"/>'
    b += text(ox + 3 * 90 - 3, base - 5 * 28 - 8, "высота 5 × ширина 2 = 10", 14, YELLOW)
    b += text(380, 270, "для столбца i: L — ближайший слева ниже, R — ближайший справа ниже; ширина = R − L − 1", 13, MUTED)
    return figure(svg(760, 290, b), "Для каждого столбца берём самый широкий прямоугольник его высоты; ответ — максимум по всем столбцам.")


# ---------------------------------------------------------------- прогрессия
def fig_ap():
    b = text(380, 24, "Прогрессия a, a+d, a+2d… на [l, r]: разностный массив второго порядка", 15)
    heads = ["i", "l", "l+1", "…", "r", "r+1", "r+2"]
    rows = [("d₂[i]", ["", "+a", "+(d−a)", "", "", "−(a+(r−l+1)d)", "+(a+(r−l)d)"], BLUE),
            ("1-я сумма", ["0", "a", "d", "d", "d", "−(a+(r−l)d)", "0"], GREEN),
            ("2-я сумма", ["0", "a", "a+d", "…", "a+(r−l)d", "0", "0"], ORANGE)]
    for j, h in enumerate(heads): b += text(150 + j * 85, 58, h, 12, MUTED)
    for i, (nm, vals, col) in enumerate(rows):
        y = 75 + i * 52
        b += text(20, y + 24, nm, 12, MUTED, "start")
        for j, v in enumerate(vals): b += cell(112 + j * 85, y, 76, 36, v, col if v else None, 11)
    b += text(380, 258, "четыре точечных изменения вместо r − l + 1: два префиксных прохода в конце восстанавливают массив", 13, MUTED)
    return figure(svg(760, 276, b), "Вариант из трёх точек (без компенсации в $r+2$) оставляет ненулевой «хвост» справа от отрезка.")


# ---------------------------------------------------------------- дождевая вода
def fig_water():
    h = [3, 0, 1, 4, 0, 2, 1, 3]
    b = text(380, 24, "Дождевая вода: над столбцом i: min(макс слева, макс справа) − h[i]", 15)
    ox, base = 70, 210
    mxl = [max(h[:i + 1]) for i in range(len(h))]; mxr = [max(h[i:]) for i in range(len(h))]
    for i, v in enumerate(h):
        x = ox + i * 78; w = min(mxl[i], mxr[i])
        if w > v: b += f'<rect x="{x}" y="{base - w * 30}" width="72" height="{(w - v) * 30}" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="1.5"/>'
        if v: b += f'<rect x="{x}" y="{base - v * 30}" width="72" height="{v * 30}" fill="{NODE}" stroke="{EDGE}" stroke-width="2"/>'
        b += text(x + 36, base + 18, str(v), 12, MUTED)
    b += text(380, 255, "два указателя L и R: сдвигаем сторону с меньшим столбцом — для неё ограничение известно точно", 13, MUTED)
    return figure(svg(760, 275, b), "Синий — вода. Памяти $O(1)$: максимум с отстающей стороны не нужен, раз с другой стороны есть столбец не ниже.")


# ---------------------------------------------------------------- плеер: монотонный стек
def algo_stack(a=(5, 3, 1, 2, 4, 3)):
    frames = []; st = []; res = []

    def draw(i, note):
        s = text(300, 22, "массив: " + " ".join(map(str, a)), 14, MUTED)
        for k, v in enumerate(a):
            col = YELLOW if k == i else (GREEN if k in st else None)
            s += cell(40 + k * 62, 44, 56, 34, str(v), col, 15) + text(40 + k * 62 + 28, 98, f"{k}", 11, MUTED)
        for k, r in enumerate(res): s += text(40 + k * 62 + 28, 126, str(r), 14, ORANGE, weight="700")
        s += text(24, 126, "L:", 13, MUTED, "start")
        s += text(24, 170, "стек (индексы):  " + (" ".join(map(str, st)) if st else "пуст"), 14, BLUE, "start")
        s += text(24, 196, note, 13, MUTED, "start")
        return s
    for i, v in enumerate(a):
        frames.append({"svg": draw(i, f"читаем a[{i}] = {v}"), "msg": f"Берём a[{i}] = {v}. Пока на вершине стека элемент не меньше {v}, он не может быть ответом ни для кого дальше — снимаем."})
        while st and a[st[-1]] >= v:
            t = st.pop()
            frames.append({"svg": draw(i, f"a[{t}] = {a[t]} ≥ {v}: снимаем"), "msg": f"Снимаем индекс {t} (значение {a[t]} не меньше {v})."})
        ans = st[-1] if st else -1
        res.append(ans); st.append(i)
        frames.append({"svg": draw(i, f"L[{i}] = {ans}, кладём {i}"), "msg": f"Ответ для {i}: ближайший слева меньший — индекс {ans}. Кладём {i} в стек."})
    return {"title": "Ближайший слева меньший: монотонный стек", "vb": "0 0 420 220", "frames": frames}


FIGS = {"union": fig_union, "events": fig_events, "rotate": fig_rotate, "jumps": fig_jumps, "contrib": fig_contrib,
        "hist": fig_hist, "ap": fig_ap, "water": fig_water}


def algos_js():
    data = {"stack": algo_stack()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
