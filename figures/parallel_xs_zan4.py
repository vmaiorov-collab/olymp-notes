"""Иллюстрации и плееры для «Занятие 4. Параллель XS — Разбор контеста по строкам, разбор дистура, Математика 1»."""
import json
from kit import *


# ---------------------------------------------------------------- почти вхождение: префикс + суффикс
def fig_almost():
    P = "abcab"; T = "xabdabx"
    b = text(380, 24, "Одна ошибка в позиции i: совпал префикс, потом одна буква, потом совпал суффикс", 15)
    b += text(24, 70, "P", 14, MUTED, "start")
    cols = [GREEN, GREEN, RED, GREEN, GREEN]
    for i, ch in enumerate(P):
        b += cell(70 + i * 56, 50, 50, 34, ch, cols[i], 16)
    b += text(24, 140, "T[i..]", 14, MUTED, "start")
    for i, ch in enumerate("abdab"):
        b += cell(70 + i * 56, 120, 50, 34, ch, cols[i], 16)
    b += line(70, 98, 70 + 2 * 56 - 6, 98, GREEN, 2) + text(70 + 56 - 3, 114, "pre[i]", 12, GREEN)
    b += line(70 + 3 * 56 + 6, 98, 70 + 5 * 56 - 6, 98, GREEN, 2) + text(70 + 4 * 56 - 3, 114, "suf[i+m−1]", 12, GREEN)
    b += text(480, 76, "pre[i]  — длина общего префикса P и T[i..]  (Z-функция P#T)", 13, MUTED, "start")
    b += text(480, 102, "suf[j]  — длина общего суффикса P и T[..j]  (Z-функция от", 13, MUTED, "start")
    b += text(480, 122, "развёрнутых строк)", 13, MUTED, "start")
    b += text(380, 200, "почти вхождение  ⇔  pre[i] + suf[i+m−1] ≥ m − 1", 16, YELLOW)
    b += text(380, 226, "если сумма ≥ m, то это точное вхождение — тоже подходит", 13, MUTED)
    return figure(svg(760, 246, b), "Фиксируем начало окна $i$: конец окна известен, поэтому остаётся сравнить два куска.")


# ---------------------------------------------------------------- циклический сдвиг + xor
def fig_xor():
    a = [3, 1, 2, 0]
    b_ = text(380, 24, "Сдвиг и xor с константой сохраняют xor соседних элементов", 15)
    def row(y, vals, title, col):
        out = text(24, y + 22, title, 12, MUTED, "start")
        for i, v in enumerate(vals):
            out += cell(150 + i * 70, y, 60, 34, str(v), col, 16)
        return out
    sh = a[1:] + a[:1]; x = 2; bb = [v ^ x for v in sh]
    b_ += row(50, a, "a", BLUE)
    b_ += row(112, sh, "сдвиг на k=1", None)
    b_ += row(174, bb, f"b = (…) xor {x}", GREEN)
    ca = [a[i] ^ a[(i + 1) % 4] for i in range(4)]; cb = [bb[i] ^ bb[(i + 1) % 4] for i in range(4)]
    b_ += text(480, 74, "c[i] = a[i] xor a[i+1 mod n]:", 13, MUTED, "start") + text(480, 98, str(ca) + " → циклически сдвинутый", 14, TEXT, "start")
    b_ += text(480, 192, "d[i] = b[i] xor b[i+1 mod n]:", 13, MUTED, "start") + text(480, 216, str(cb), 14, TEXT, "start")
    b_ += text(380, 262, "ищем d как подстроку cc = c+c; позиция входа даёт k, а x = a[k] xor b[0]", 13, YELLOW)
    return figure(svg(760, 282, b_), "Константа $x$ при xor соседей сокращается, поэтому от неё можно избавиться и свести задачу к поиску подстроки.")


# ---------------------------------------------------------------- расстояния до следующей такой же буквы
def fig_next():
    s = "abacab"; t = "xyxzxy"
    def nx(w):
        r = []; 
        for i in range(len(w)):
            j = next((k for k in range(i + 1, len(w)) if w[k] == w[i]), None)
            r.append(j - i if j is not None else "*")
        return r
    b = text(380, 24, "Равенство с точностью до переименования букв: сравниваем расстояния до следующей такой же", 15)
    for r, (w, y, col) in enumerate([(s, 54, BLUE), (t, 130, GREEN)]):
        for i, ch in enumerate(w):
            b += cell(110 + i * 70, y, 60, 34, ch, col, 17)
            v = nx(w)[i]
            b += cell(110 + i * 70, y + 44, 60, 28, str(v), None, 14)
        b += text(24, y + 22, "строка", 12, MUTED, "start") + text(24, y + 64, "next", 12, MUTED, "start")
    b += text(380, 232, "«*» (следующей нет) совпадает с любым числом — это «джокер» при сравнении", 13, YELLOW)
    b += text(380, 256, "запускаем КМП на next-строках; джокер считаем равным любому значению", 13, MUTED)
    return figure(svg(760, 276, b), "abacab и xyxzxy отличаются только переименованием букв: next-массивы совпадают.")


# ---------------------------------------------------------------- Ахо—Корасик по бору
def fig_trie_walk():
    b = text(380, 24, "Одновременный обход двух боров: бор запроса T и автомат Ахо—Корасик по набору", 15)
    # левый бор T
    for (x, y, l) in [(130, 70, "корень"), (70, 140, "a"), (190, 140, "b"), (70, 210, "b")]:
        b += circle(x, y, 20, "", BLUE if l != "корень" else None)
    b += line(130, 90, 78, 124, EDGE, 2) + line(130, 90, 182, 124, EDGE, 2) + line(70, 160, 70, 190, EDGE, 2)
    b += text(104, 112, "a", 12, MUTED) + text(160, 112, "b", 12, MUTED) + text(58, 178, "b", 12, MUTED)
    b += text(130, 250, "бор T (в нём идём DFS)", 13, MUTED)
    # правый автомат
    for (x, y) in [(560, 70), (500, 140), (620, 140), (500, 210)]:
        b += circle(x, y, 20, "", GREEN if y > 100 else None)
    b += line(560, 90, 508, 124, EDGE, 2) + line(560, 90, 612, 124, EDGE, 2) + line(500, 160, 500, 190, EDGE, 2)
    b += text(560, 250, "автомат: вершина v по ходу DFS", 13, MUTED)
    b += line(150, 140, 480, 140, YELLOW, 1.5, dash="5 4", arrow=True)
    b += text(315, 128, "state[u] = переход(state[parent], буква)", 12, YELLOW)
    b += text(380, 280, "вершину автомата запоминаем в каждой вершине T — при возврате вверх она не теряется", 13, MUTED)
    b += text(380, 302, "ответ += cnt[state], где cnt[v] = терминальные на пути по суффиксным ссылкам", 13, MUTED)
    return figure(svg(760, 322, b), "Вложенный обход: спускаясь по бору $T$, спускаемся по автоматным рёбрам; по возвращении вершина восстанавливается.")


# ---------------------------------------------------------------- игра: бор по битам
def fig_game():
    b = text(380, 24, "Игра с xor: смотрим на старший бит, считаем cnt₁ и cnt₀", 15)
    def node(x, y, lab, col=None): return circle(x, y, 22, lab, col)
    b += node(380, 62, "бит L") + node(220, 140, "0", BLUE) + node(540, 140, "1", ORANGE)
    b += line(380, 84, 236, 124, EDGE, 2) + line(380, 84, 524, 124, EDGE, 2)
    b += text(220, 188, "cnt₀ чётно", 13, BLUE) + text(540, 188, "cnt₁ чётно", 13, ORANGE)
    b += text(380, 232, "чётно: Боб отвечает «парой» → бит L в ответе не появится;", 14)
    b += text(380, 254, "две независимые игры, ответ — max из двух", 14, YELLOW)
    b += text(380, 284, "нечётно: ровно одна пара из разных половин; Алиса берёт x,", 14)
    b += text(380, 306, "Боб берёт y из другой половины с минимальным x xor y; ответ — max по x", 14, YELLOW)
    return figure(svg(760, 326, b), "Разбор по старшему биту сверху вниз; нечётный случай заканчивает рекурсию в этой вершине.")


# ---------------------------------------------------------------- палиндромы → прямоугольники
def fig_rect():
    b = text(380, 24, "Пары центров (i, j) → точки и прямоугольники → сканлайн", 15)
    b += line(60, 260, 700, 260, AXIS, 1.5, arrow=True) + line(60, 260, 60, 40, AXIS, 1.5, arrow=True)
    b += text(700, 280, "i", 13, MUTED) + text(40, 40, "2w", 13, MUTED)
    pts = [(120, 220), (200, 150), (260, 190), (340, 100), (420, 170), (500, 130)]
    for (x, y) in pts: b += f'<circle cx="{x}" cy="{y}" r="5" fill="{BLUE}"/>'
    b += f'<rect x="230" y="110" width="200" height="100" fill="{SOFT[GREEN]}" stroke="{GREEN}" stroke-width="2" opacity=".85"/>'
    b += text(330, 98, "прямоугольник центра j", 13, GREEN)
    b += text(380, 306, "точка i внутри прямоугольника j  ⇔  палиндромы вокруг i и j достают друг до друга", 13, MUTED)
    b += text(380, 328, "считаем точки в «четверти» и вычитаем: событийная сортировка + дерево Фенвика", 13, YELLOW)
    return figure(svg(760, 348, b), "Условия вида «левая часть зависит от $i$, правая — от $j$» превращаются в подсчёт точек в прямоугольниках.")


# ---------------------------------------------------------------- гармонический ряд (ступеньки)
def fig_harm():
    b = text(380, 24, "Сумма 1/i: оцениваем сверху ступеньками — каждая группа весит не больше 1", 15)
    X0, Y0, H = 70, 250, 190
    b += line(X0, Y0, 700, Y0, AXIS, 1.5, arrow=True) + line(X0, Y0, X0, 40, AXIS, 1.5, arrow=True)
    # реальные значения 1/i, i=1..32 (масштаб по x логарифмический не нужен — просто колонки)
    n = 32; w = 18
    for i in range(1, n + 1):
        h = H / i
        b += f'<rect x="{X0 + (i - 1) * w + 2}" y="{Y0 - h:.1f}" width="{w - 4}" height="{h:.1f}" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="1"/>'
    # ступеньки: 1/1 | 1/2 (x2: i=2,3) | 1/4 (x4: i=4..7) | 1/8 (x8: i=8..15) | 1/16 (x16: i=16..31)
    for lo, hi in [(1, 1), (2, 3), (4, 7), (8, 15), (16, 31)]:
        h = H / lo
        b += line(X0 + (lo - 1) * w, Y0 - h, X0 + hi * w, Y0 - h, YELLOW, 2.5)
    b += text(560, 90, "группа [2ᵏ, 2ᵏ⁺¹): 2ᵏ членов", 13, YELLOW, "start") + text(560, 112, "каждый ≤ 1/2ᵏ  →  сумма ≤ 1", 13, YELLOW, "start")
    b += text(560, 146, "групп log₂A  →  сумма ≤ log₂A", 13, TEXT, "start")
    b += text(380, 286, "вывод: решето по всем i — A·log A; только по простым i — A·log log A", 14)
    return figure(svg(760, 306, b), "Гармонический ряд растёт как $\\ln A$ ($\\approx 14$ при $A=10^6$), поэтому «сумма $A/i$» — это $O(A\\log A)$.")


# ---------------------------------------------------------------- линейное решето: c = lp * i
def fig_linear():
    b = text(380, 24, "Каждое составное c появляется один раз: c = i · x, где x = lp(c) и x ≤ lp(i)", 15)
    rows = [(12, 6, 2), (18, 9, 2), (45, 15, 3), (30, 15, 2), (49, 7, 7), (75, 25, 3)]
    for r, (c, i, x) in enumerate(rows):
        y = 50 + r * 44
        b += cell(40, y, 60, 32, str(c), BLUE, 16) + text(112, y + 21, "=", 16, MUTED)
        b += cell(126, y, 60, 32, str(i), None, 16) + text(198, y + 21, "·", 16, MUTED) + cell(210, y, 50, 32, str(x), GREEN, 16)
    b += text(300, 76, "x = lp(c) — наименьший простой делитель c; i = c / x", 13, MUTED, "start")
    b += text(300, 108, "75 = 25·3: число 75 получается только при i = 25, x = 3", 13, TEXT, "start")
    b += text(300, 130, "при i = 15 перебор простых останавливается на x = 3 = lp(15),", 13, TEXT, "start")
    b += text(300, 152, "поэтому 15·5 = 75 повторно не записывается", 13, TEXT, "start")
    b += text(300, 204, "условие остановки внутреннего цикла: x > lp(i)", 14, ORANGE, "start")
    return figure(svg(760, 330, b), "Число $c$ единственным образом записывается как «наименьший простой делитель» $\\cdot$ «остальное» — отсюда $O(A)$.")


# ---------------------------------------------------------------- φ: таблица n × m
def fig_phi():
    n, m = 3, 4
    b = text(380, 24, "φ мультипликативна: числа 0…nm−1 в таблице n×m (по строкам)", 15)
    from math import gcd
    for r in range(n):
        for c in range(m):
            v = r * m + c
            ok_m = gcd(c, m) == 1
            b += cell(110 + c * 70, 50 + r * 46, 62, 36, str(v), BLUE if ok_m else None, 16)
    b += text(24, 74, "n=3, m=4", 13, MUTED, "start")
    for c in range(m):
        b += text(110 + c * 70 + 31, 50 + n * 46 + 14, f"mod {m} = {c}", 11, GREEN if gcd(c, m) == 1 else MUTED)
    b += text(450, 80, "• взаимно просты с m — целые столбцы (φ(m) штук)", 13, BLUE, "start")
    b += text(450, 106, "• в каждом столбце остатки по n — все различные (m, n взаимно просты)", 13, TEXT, "start")
    b += text(450, 132, "• в столбце φ(n) чисел взаимно просты с n", 13, TEXT, "start")
    b += text(450, 174, "итого φ(nm) = φ(m)·φ(n)", 16, YELLOW, "start")
    return figure(svg(760, 240, b), "Столбец — фиксированный остаток по $m$; внутри столбца остатки по $n$ пробегают все значения.")


# ---------------------------------------------------------------- путь и отражение
def fig_catalan():
    N = 4
    b = text(380, 24, "Правильные скобочные последовательности длины 2n = 8: пути не заходят выше диагонали", 15)
    X0, Y0, S = 80, 50, 40
    for i in range(N + 2):
        b += line(X0, Y0 + i * S, X0 + (N + 1) * S, Y0 + i * S, "#232d3b", 1)
        b += line(X0 + i * S, Y0, X0 + i * S, Y0 + (N + 1) * S, "#232d3b", 1)
    b += line(X0, Y0, X0 + N * S, Y0 + N * S, AXIS, 2, dash="6 4")
    b += line(X0, Y0 + S, X0 + (N - 1) * S, Y0 + N * S, RED, 1.5, dash="3 4")
    def poly(pts, col, w, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<polyline points="{" ".join(f"{X0 + x * S},{Y0 + y * S}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="{w}"{d}/>'
    b += poly([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4)], GREEN, 3)
    b += poly([(0, 0), (1, 0), (1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (4, 3), (4, 4)], RED, 3)
    b += poly([(1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5)], ORANGE, 3, "6 4")
    b += text(X0 + N * S + 26, Y0 + N * S + 6, "(n,n)", 12, MUTED) + text(X0 + 3 * S + 26, Y0 + 5 * S + 6, "(n−1,n+1)", 12, ORANGE)
    b += text(480, 90, "зелёный — корректный путь", 13, GREEN, "start")
    b += text(480, 116, "красный — плохой: касается прямой y = x + 1", 13, RED, "start")
    b += text(480, 140, "оранжевый — остаток после первого касания,", 13, ORANGE, "start") + text(480, 160, "отражённый (шаги → и ↓ поменяли местами)", 13, ORANGE, "start")
    b += text(480, 204, "плохих путей = C(2n, n−1)", 14, TEXT, "start")
    b += text(480, 236, "Catₙ = C(2n, n) − C(2n, n−1)", 15, YELLOW, "start") + text(480, 260, "= C(2n, n) / (n+1)", 15, YELLOW, "start")
    return figure(svg(760, 296, b), "Отражение остатка пути относительно прямой $y=x+1$ переводит каждый плохой путь в путь в клетку $(n-1,\\,n+1)$, и обратно.")


# ---------------------------------------------------------------- шары и перегородки
def fig_balls():
    b = text(380, 24, "m шаров в n ящиков: расставляем m шаров и n−1 перегородку в один ряд", 15)
    s = "●●|●|●●●||●"
    for i, ch in enumerate(s):
        b += cell(70 + i * 56, 60, 48, 40, ch, ORANGE if ch == "|" else BLUE, 20)
    b += text(380, 134, "ящики:  2 · 1 · 3 · 0 · 1   (n = 5, m = 7, перегородок 4)", 14, TEXT)
    b += text(380, 170, "число способов  =  C(n + m − 1, m)", 17, YELLOW)
    return figure(svg(760, 190, b), "Выбираем, на каких $n+m-1$ местах стоят шары — остальные места занимают перегородки.")


FIGS = {"almost": fig_almost, "xor": fig_xor, "nextd": fig_next, "triewalk": fig_trie_walk, "game": fig_game,
        "rect": fig_rect, "harm": fig_harm, "linear": fig_linear, "phi": fig_phi, "catalan": fig_catalan, "balls": fig_balls}


# ---------------------------------------------------------------- плеер: линейное решето
def algo_linsieve(A=20):
    lp = [0] * (A + 1); pr = []; frames = []
    def draw(i, x, note):
        s = ""
        for k in range(2, A + 1):
            col = None
            if lp[k]:
                col = GREEN if lp[k] == k else BLUE
            if k == i: col = YELLOW
            if k == i * x if x else False: col = ORANGE
            r, c = divmod(k - 2, 10)
            s += cell(20 + c * 52, 20 + r * 56, 48, 34, str(k), col, 14, sub=(str(lp[k]) if lp[k] else None))
        s += text(20, 210, "простые: " + " ".join(map(str, pr)), 13, GREEN, "start")
        s += text(20, 234, note, 13, MUTED, "start")
        return s
    for i in range(2, A + 1):
        if lp[i] == 0:
            lp[i] = i; pr.append(i)
            frames.append({"svg": draw(i, 0, f"{i}: lp ещё нет → простое"), "msg": f"i = {i}: наименьшего простого делителя нет — число простое, lp[{i}] = {i}."})
        for x in pr:
            if x > lp[i] or i * x > A:
                frames.append({"svg": draw(i, 0, f"стоп: x = {x}" + (" > lp(i)" if x > lp[i] else f", {i}·{x} > {A}")), "msg": f"Для i = {i} перебор простых останавливается на x = {x}: " + (f"x > lp(i) = {lp[i]}." if x > lp[i] else f"{i}·{x} выходит за границу.")})
                break
            lp[i * x] = x
            frames.append({"svg": draw(i, x, f"{i}·{x} = {i * x}: lp[{i * x}] = {x}"), "msg": f"i = {i}, x = {x}: записываем lp[{i * x}] = {x}. Число {i * x} получено ровно один раз."})
        else:
            frames.append({"svg": draw(i, 0, "простые закончились"), "msg": f"Простые для i = {i} закончились."})
    return {"title": "Линейное решето: каждое составное — один раз", "vb": "0 0 560 250", "frames": frames}


def algos_js():
    data = {"linsieve": algo_linsieve()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
