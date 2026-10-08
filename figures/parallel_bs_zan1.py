"""Иллюстрации и плееры для «Занятие 1. Параллель BS — STL и жадные алгоритмы»."""
import json
from kit import *


# ---------------------------------------------------------------- вектор: size и capacity
def fig_vector():
    b = text(380, 24, "size — сколько элементов лежит; capacity — сколько памяти выделено", 15)
    def row(y, cap, size, title, col):
        out = text(24, y + 22, title, 12, MUTED, "start")
        for i in range(cap):
            out += cell(170 + i * 52, y, 46, 34, str(i + 1) if i < size else "", col if i < size else None, 14)
        out += text(170 + cap * 52 + 8, y + 22, f"size={size}, cap={cap}", 12, MUTED, "start")
        return out
    b += row(50, 4, 4, "заполнен", BLUE)
    b += row(112, 8, 5, "после push_back", GREEN)
    b += line(380, 90, 380, 108, YELLOW, 2, arrow=True)
    b += text(540, 100, "size = capacity → выделяем 2·capacity, копируем", 12, YELLOW)
    b += text(380, 190, "один push_back иногда дорогой (копирование), но в среднем — O(1)", 14)
    b += text(380, 214, "(амортизированно: суммарно удвоений ≈ log n, копируется ≤ 2n элементов)", 13, MUTED)
    return figure(svg(760, 236, b), "Размер и ёмкость — разные числа. Удвоение — не точное правило стандарта, а типичная реализация.")


# ---------------------------------------------------------------- итераторы: полуинтервал
def fig_iter():
    b = text(380, 24, "Полуинтервал [begin, end): левая граница включена, правая — нет", 15)
    vals = [7, 3, 9, 5, 1]
    for i, v in enumerate(vals):
        b += cell(120 + i * 80, 60, 70, 40, str(v), BLUE if i != 2 else YELLOW, 17)
        b += text(120 + i * 80 + 35, 120, f"v[{i}]", 12, MUTED)
    b += cell(120 + 5 * 80, 60, 70, 40, "", None) + text(120 + 5 * 80 + 35, 120, "за концом", 12, MUTED)
    b += line(155, 172, 155, 108, GREEN, 2, arrow=True) + text(155, 192, "v.begin()", 13, GREEN)
    b += line(155 + 5 * 80, 172, 155 + 5 * 80, 108, RED, 2, arrow=True) + text(155 + 5 * 80, 192, "v.end()", 13, RED)
    b += line(315, 172, 315, 108, YELLOW, 2, arrow=True) + text(315, 192, "it = v.begin() + 2", 13, YELLOW)
    b += text(380, 232, "*it = 9;   it − v.begin() = 2 (индекс);   v.end() − v.begin() = size", 14)
    return figure(svg(760, 256, b), "Итератор — «указатель» на элемент. Разыменование даёт элемент, разность итераторов — расстояние.")


# ---------------------------------------------------------------- сжатие координат
def fig_compress():
    b = text(380, 24, "Сжатие координат: sort → unique → lower_bound", 15)
    a = [50, 10, 50, 30, 10, 90]
    sa = sorted(set(a)); idx = {v: i for i, v in enumerate(sa)}
    def row(y, vals, title, col=None, hl=None):
        out = text(24, y + 22, title, 12, MUTED, "start")
        for i, v in enumerate(vals):
            out += cell(210 + i * 70, y, 62, 34, str(v), (hl or {}).get(i, col), 15)
        return out
    b += row(50, a, "исходный a", BLUE)
    b += row(112, sorted(a), "после sort", None)
    b += row(174, sa, "после unique+erase", GREEN)
    b += row(236, [idx[v] for v in a], "b[i] = lower_bound − begin", ORANGE)
    for y0 in (86, 148, 210):
        b += line(380, y0, 380, y0 + 22, MUTED, 1.5, arrow=True)
    b += text(380, 296, "равные числа → равные индексы; порядок сохранён; max(b) минимален", 13, MUTED)
    return figure(svg(760, 316, b), "Числа 10, 30, 50, 90 получили номера 0, 1, 2, 3 — ровно по порядку возрастания.")


# ---------------------------------------------------------------- коробки: цепочки
def fig_boxes():
    a = [1, 2, 2, 3, 3, 3, 5, 5, 6]
    b = text(380, 24, "Коробки 1, 2, 2, 3, 3, 3, 5, 5, 6: ответ — 3 цепочки (максимум кратности)", 15)
    chains = [[6, 5, 3, 2, 1], [5, 3, 2], [3]]
    cols = [BLUE, GREEN, ORANGE]
    for r, ch in enumerate(chains):
        y = 56 + r * 66
        b += text(24, y + 28, f"цепочка {r + 1}", 12, MUTED, "start")
        for i, v in enumerate(ch):
            w = 36 + v * 12
            x = 140 + i * 110 + (84 - w) / 2 + 10
            b += cell(x, y + 4, w, 40, str(v), cols[r], 16)
            if i + 1 < len(ch): b += text(140 + i * 110 + 96, y + 30, "⊃", 18, MUTED)
    b += text(380, 270, "Три тройки не могут лежать в одной цепочке (равные коробки не вкладываются) → нужно ≥ 3.", 13, MUTED)
    b += text(380, 292, "Строим 3 цепочки: j-я копия каждого размера уходит в цепочку j — внутри цепочки размеры строго убывают.", 13, MUTED)
    return figure(svg(760, 312, b), "Нижняя оценка — максимальная кратность $k$; конструкция из $k$ цепочек её достигает.")


# ---------------------------------------------------------------- Хаффман: две очереди
def fig_twoq():
    b = text(380, 24, "Две очереди: исходные числа (по возрастанию) и суммы (тоже по возрастанию)", 15)
    A = [3, 5, 6, 7, 7, 8]; Q = [8, 13, 15]
    b += text(24, 66, "A:", 14, MUTED, "start")
    for i, v in enumerate(A): b += cell(60 + i * 56, 46, 50, 34, str(v), BLUE if i >= 2 else None, 15)
    b += text(24, 136, "B:", 14, MUTED, "start")
    for i, v in enumerate(Q): b += cell(60 + i * 56, 116, 50, 34, str(v), GREEN, 15)
    b += text(60, 100, "не обработаны ↑ (указатель i)", 12, MUTED, "start")
    b += text(60, 172, "первое число B ↑", 12, MUTED, "start")
    b += text(480, 66, "Кандидаты на слияние — только три пары:", 14, YELLOW, "start")
    b += text(480, 96, "A[i] + A[i+1]", 14, TEXT, "start")
    b += text(480, 120, "A[i] + B[front]", 14, TEXT, "start")
    b += text(480, 144, "B[front] + B[front+1]", 14, TEXT, "start")
    b += text(380, 212, "новая сумма больше всех предыдущих → кладём в конец B, B остаётся отсортированной", 13, MUTED)
    return figure(svg(760, 232, b), "Достаточно смотреть на два первых числа в $A$ и два первых в $B$; общая сложность $O(n)$ при отсортированных входных данных.")


# ---------------------------------------------------------------- восстановление строки
def fig_string():
    k = 2
    v = "0110110"
    b = text(380, 24, "k = 2: v[i] = s[i−2] ИЛИ s[i+2] (существующие)", 15)
    n = len(v)
    s = ["1"] * n
    for i in range(n):
        if v[i] == "0":
            if i - k >= 0: s[i - k] = "0"
            if i + k < n: s[i + k] = "0"
    for i in range(n):
        b += cell(110 + i * 70, 56, 60, 34, v[i], RED if v[i] == "0" else GREEN, 16)
        b += cell(110 + i * 70, 150, 60, 34, s[i], RED if s[i] == "0" else GREEN, 16)
        b += text(110 + i * 70 + 30, 108, str(i), 11, MUTED)
    b += text(24, 78, "v", 14, MUTED, "start") + text(24, 172, "s", 14, MUTED, "start")
    for i in range(n):
        if v[i] == "0":
            for j in (i - k, i + k):
                if 0 <= j < n:
                    b += line(140 + i * 70, 94, 140 + j * 70, 148, RED, 1.5, dash="4 3", arrow=True)
    b += text(380, 222, "нулей в v → нули в s на расстоянии k; все остальные позиции s — единицы", 14)
    b += text(380, 246, "затем пересчитываем v по s и сравниваем с заданной", 13, MUTED)
    return figure(svg(760, 268, b), "Нуль в $v_i$ обнуляет $s_{i-k}$ и $s_{i+k}$. Единицы везде, где обнулять не заставили, — это максимальная из подходящих строк.")


# ---------------------------------------------------------------- плеер: коробки
def algo_boxes(a=(1, 2, 2, 3, 3, 3, 5, 5, 6)):
    a = sorted(a); frames = []
    def draw(i, run, best, note):
        s = text(300, 22, "отсортированные размеры, run — длина текущей группы равных", 13, MUTED)
        for k, v in enumerate(a):
            col = YELLOW if k == i else (GREEN if k < i else None)
            s += cell(30 + k * 60, 44, 54, 34, str(v), col, 15)
        s += text(30, 120, f"run = {run}", 15, BLUE, "start") + text(150, 120, f"best = {best}", 15, ORANGE, "start")
        s += text(30, 152, note, 13, MUTED, "start")
        return s
    run = 0; best = 0
    for i, v in enumerate(a):
        run = run + 1 if i and a[i - 1] == v else 1
        best = max(best, run)
        frames.append({"svg": draw(i, run, best, "равен предыдущему: run+1" if run > 1 else "новое значение: run = 1"),
                       "msg": f"Элемент {v}: {'такой же, как предыдущий' if run > 1 else 'новый размер'}, run = {run}; максимум пока {best}."})
    frames.append({"svg": draw(len(a), run, best, "ответ = best"), "msg": f"Ответ: {best} — минимум оставшихся коробок."})
    return {"title": "Коробки: максимум кратности в отсортированном массиве", "vb": "0 0 600 180", "frames": frames}


# ---------------------------------------------------------------- плеер: слияние королевств (две очереди)
def algo_merge(a=(3, 5, 6, 7, 7, 8)):
    A = list(a); frames = []; Q = []; i = 0; total = 0
    def draw(note):
        s = text(24, 24, "A (по возрастанию):", 13, MUTED, "start")
        for k, v in enumerate(A): s += cell(24 + k * 56, 34, 50, 32, str(v), BLUE if k >= i else None, 14)
        s += text(24, 106, "B (суммы):", 13, MUTED, "start")
        for k, v in enumerate(Q): s += cell(24 + k * 56, 116, 50, 32, str(v), GREEN, 14)
        s += text(24, 180, f"сумма затрат: {total}", 15, ORANGE, "start")
        s += text(24, 204, note, 13, MUTED, "start")
        return s
    frames.append({"svg": draw("берём два наименьших из голов A и B"), "msg": "Кладём все числа в A. Каждый шаг: берём два наименьших среди голов двух очередей."})
    def take():
        nonlocal i
        if not Q or (i < len(A) and A[i] <= Q[0]): i += 1; return A[i - 1]
        return Q.pop(0)
    for step in range(len(A) - 1):
        x = take(); y = take(); total += x + y; Q.append(x + y)
        frames.append({"svg": draw(f"слили {x} и {y} → {x + y} (затраты +{x + y})"), "msg": f"Слили {x} и {y}, получили {x + y}; стоимость +{x + y}, итого {total}. Сумму кладём в конец B."})
    return {"title": "Слияние королевств: две очереди", "vb": "0 0 420 220", "frames": frames}


FIGS = {"vector": fig_vector, "iter": fig_iter, "compress": fig_compress, "boxes": fig_boxes, "twoq": fig_twoq, "string": fig_string}


def algos_js():
    data = {"boxes": algo_boxes(), "merge": algo_merge()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
