"""Иллюстрации и плееры для «Занятие 2. Параллель C — Линейные алгоритмы»."""
import json
from kit import *


def row(x0, y, vals, cw=56, h=34, colors=None, size=15, idx=True, start=0):
    o = ""
    for k, v in enumerate(vals):
        c = (colors or {}).get(k)
        o += cell(x0 + k * cw, y, cw - 4, h, str(v), c, size)
        if idx: o += text(x0 + k * cw + (cw - 4) / 2, y + h + 15, str(k + start), 11, MUTED)
    return o


def fig_pref():
    a = [1, 3, 2, -1, 7, 4, 2]; P = [0]
    for v in a: P.append(P[-1] + v)
    b = text(380, 24, "Сумма на отрезке [3, 6] = P[6] − P[2]", 15)
    b += text(40, 66, "a", 14, MUTED, "start") + row(80, 50, [""] + a, colors={3: BLUE, 4: BLUE, 5: BLUE, 6: BLUE}, idx=True)
    b += text(40, 146, "P", 14, MUTED, "start") + row(80, 130, P, colors={2: ORANGE, 6: GREEN})
    b += text(80 + 6 * 56 + 26, 194, "P[6] = 16", 13, GREEN) + text(80 + 2 * 56 + 26, 194, "P[2] = 4", 13, ORANGE)
    b += text(380, 238, "16 − 4 = 12 = 2 + (−1) + 7 + 4", 15, YELLOW)
    b += text(380, 262, "вычитаем P[L−1], а не P[L]: иначе потеряем сам a[L]", 13, MUTED)
    return figure(svg(760, 284, b), "Префиксная сумма $P_i$ — сумма первых $i$ элементов; разность двух префиксов оставляет ровно нужный отрезок.")


def fig_rect2d():
    b = text(380, 24, "Запрос на прямоугольник = 4 значения P: + − − +", 15)
    x0, y0, w, h = 120, 50, 360, 220
    b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'
    cx, cy = 230, 120
    b += f'<rect x="{x0}" y="{y0}" width="{cx - x0}" height="{h}" fill="{SOFT[RED]}" stroke="none" opacity=".75"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{cy - y0}" fill="{SOFT[ORANGE]}" stroke="none" opacity=".75"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{cx - x0}" height="{cy - y0}" fill="{SOFT[PURPLE]}" stroke="none"/>'
    b += f'<rect x="{cx}" y="{cy}" width="{x0 + w - cx}" height="{y0 + h - cy}" fill="{SOFT[GREEN]}" stroke="{GREEN}" stroke-width="3"/>'
    b += text((cx + x0 + w) / 2, (cy + y0 + h) / 2, "ответ", 20, GREEN, weight="700")
    b += text(x0 + 55, y0 + 100, "P[L−1][Y]", 13, TEXT) + text(x0 + 55, y0 + 118, "вычесть", 12, MUTED)
    b += text((cx + x0 + w) / 2, y0 + 40, "P[R][X−1]: вычесть полосу слева", 13, TEXT)
    b += text(x0 + 55, y0 + 40, "+P[L−1][X−1]", 13, YELLOW)
    b += text(540, 100, "S = P[R][Y]", 15, TEXT, "start") + text(540, 124, "− P[L−1][Y]", 15, RED, "start") + text(540, 148, "− P[R][X−1]", 15, RED, "start") + text(540, 172, "+ P[L−1][X−1]", 15, YELLOW, "start")
    return figure(svg(760, 292, b), "Большой прямоугольник до $(R,Y)$ минус две полосы; угол вычтен дважды — добавляем его обратно.")


def fig_diff():
    a = [1, 2, -1, 4, 6]; a2 = [1, 5, 2, 7, 6]
    D = [a[0]] + [a[i] - a[i - 1] for i in range(1, 5)] + [-a[4]]
    D2 = [a2[0]] + [a2[i] - a2[i - 1] for i in range(1, 5)] + [-a2[4]]
    b = text(380, 24, "Запрос L=2, R=4, X=3: в D меняются только две позиции", 15)
    b += text(30, 66, "a до", 12, MUTED, "start") + row(100, 50, a, colors={1: BLUE, 2: BLUE, 3: BLUE}, start=1)
    b += text(30, 136, "a после", 12, MUTED, "start") + row(100, 120, a2, colors={1: GREEN, 2: GREEN, 3: GREEN}, start=1)
    b += text(30, 216, "D до", 12, MUTED, "start") + row(100, 200, D[:5], start=1)
    b += text(30, 286, "D после", 12, MUTED, "start") + row(100, 270, D2[:5], colors={1: GREEN, 4: RED}, start=1)
    b += text(560, 226, "D[2] += 3", 15, GREEN, "start") + text(560, 252, "D[5] −= 3", 15, RED, "start")
    b += text(560, 290, "(D[5] = a[5]−a[4]: ушло в D[R+1])", 12, MUTED, "start")
    return figure(svg(760, 330, b), "Внутри отрезка соседние разности не меняются; меняются только на левой границе (+X) и сразу за правой (−X).")


FIGS = {"pref": fig_pref, "rect2d": fig_rect2d, "diff": fig_diff}


def algo_inter(a=(1, 3, 4, 5, 8, 10), b=(2, 3, 8, 9, 10)):
    frames = []; i = j = ans = 0
    def draw(note):
        s = text(24, 24, "A", 13, MUTED, "start") + row(60, 8, a, cw=50, h=32, colors={i: YELLOW} if i < len(a) else None, idx=False)
        s += text(24, 84, "B", 13, MUTED, "start") + row(60, 68, b, cw=50, h=32, colors={j: YELLOW} if j < len(b) else None, idx=False)
        s += text(24, 140, f"общих: {ans}", 15, GREEN, "start") + text(24, 168, note, 13, MUTED, "start")
        return s
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            frames.append({"svg": draw(f"A[{i}]={a[i]} = B[{j}]={b[j]}: нашли общее"), "msg": f"Числа равны ({a[i]}) — ответ +1, двигаем оба указателя."})
            ans += 1; i += 1; j += 1
        elif a[i] < b[j]:
            frames.append({"svg": draw(f"{a[i]} < {b[j]}: двигаем i"), "msg": f"{a[i]} < {b[j]}: A[i] уже не встретится в B правее — двигаем i."}); i += 1
        else:
            frames.append({"svg": draw(f"{a[i]} > {b[j]}: двигаем j"), "msg": f"{a[i]} > {b[j]}: двигаем j."}); j += 1
    frames.append({"svg": draw("один из указателей вышел за границу"), "msg": f"Конец. Общих чисел: {ans}."})
    return {"title": "Два указателя: общие элементы", "vb": "0 0 360 184", "frames": frames}


def algo_merge(a=(1, 4, 6, 9), b=(2, 3, 7, 10, 12)):
    frames = []; i = j = 0; c = []
    def draw(note):
        s = text(24, 22, "A", 13, MUTED, "start") + row(60, 6, a, cw=48, h=30, colors={i: YELLOW} if i < len(a) else None, idx=False)
        s += text(24, 72, "B", 13, MUTED, "start") + row(60, 56, b, cw=48, h=30, colors={j: YELLOW} if j < len(b) else None, idx=False)
        s += text(24, 128, "C", 13, MUTED, "start") + row(60, 112, c + [""] * (len(a) + len(b) - len(c)), cw=48, h=30, colors={k: GREEN for k in range(len(c))}, idx=False)
        s += text(24, 170, note, 13, MUTED, "start")
        return s
    while i < len(a) and j < len(b):
        if a[i] < b[j]: c.append(a[i]); frames.append({"svg": draw(f"{a[i]} < {b[j]}: берём из A"), "msg": f"{a[i]} < {b[j]} — пишем {a[i]} в C."}); i += 1
        else: c.append(b[j]); frames.append({"svg": draw(f"{b[j]} ≤ {a[i]}: берём из B"), "msg": f"{b[j]} не больше {a[i]} — пишем {b[j]} в C."}); j += 1
    while i < len(a): c.append(a[i]); i += 1; frames.append({"svg": draw("хвост A дописываем"), "msg": "B закончился — дописываем остаток A."})
    while j < len(b): c.append(b[j]); j += 1; frames.append({"svg": draw("хвост B дописываем"), "msg": "A закончился — дописываем остаток B."})
    return {"title": "Слияние отсортированных массивов", "vb": "0 0 360 184", "frames": frames}


def algo_pairs(x=(1, 3, 4, 5, 7, 10), k=2):
    frames = []; n = len(x); r = 0; ans = 0
    def draw(i, note):
        s = text(24, 22, f"k = {k}", 13, MUTED, "start")
        for t, v in enumerate(x):
            col = YELLOW if t == i else (GREEN if i < t <= r else None)
            s += cell(40 + t * 54, 40, 50, 34, str(v), col, 15) + text(40 + t * 54 + 25, 92, str(t), 11, MUTED)
        s += text(24, 124, f"ответ: {ans}", 15, GREEN, "start") + text(24, 152, note, 13, MUTED, "start")
        return s
    for i in range(n):
        r = max(r, i)
        frames.append({"svg": draw(i, f"i = {i}, r = {r}"), "msg": f"i = {i} (x = {x[i]}). Двигаем r вправо, пока x[r+1] − x[i] ≤ {k}."})
        while r + 1 < n and x[r + 1] - x[i] <= k:
            r += 1; frames.append({"svg": draw(i, f"r → {r}: {x[r]} − {x[i]} ≤ {k}"), "msg": f"x[{r}] − x[{i}] = {x[r] - x[i]} ≤ {k}: r = {r}."})
        ans += r - i
        frames.append({"svg": draw(i, f"+ (r − i) = {r - i}"), "msg": f"К ответу добавляем r − i = {r - i} пар (i, i+1)…(i, r)."})
    return {"title": "Пары точек на расстоянии ≤ k", "vb": "0 0 360 170", "frames": frames}


def algos_js():
    data = {"inter": algo_inter(), "merge": algo_merge(), "pairs": algo_pairs()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
