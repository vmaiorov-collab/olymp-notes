"""Иллюстрации и плееры для «Занятие 1. Параллель B — Дерево отрезков»."""
import json
from kit import *


def fig_zeros():
    b = text(380, 24, "Склейка двух отрезков: четыре числа в вершине и формулы пересчёта", 15)
    def box(x, vals, col, title):
        out = text(x + 120, 54, title, 14, col)
        for i, v in enumerate(vals):
            out += cell(x + i * 30, 70, 28, 34, str(v), col if v == 0 else None, 16)
        return out
    L = [1, 0, 0, 0, 1]; R = [0, 0, 1, 0]
    b += box(60, L, GREEN, "левая половина")
    b += box(400, R, BLUE, "правая половина")
    b += text(130, 128, "pre = 0, suf = 0, best = 3", 13, MUTED) + text(480, 128, "pre = 2, suf = 1, best = 2", 13, MUTED)
    # склейка: суффикс левой нулей 0, но показываем другой пример
    b += text(380, 175, "best = max( best левой ,  best правой ,  suf левой + pre правой )", 15, YELLOW)
    b += text(380, 205, "pre  = левая вся из нулей ?  len левой + pre правой  :  pre левой", 14, TEXT)
    b += text(380, 230, "suf  = правая вся из нулей ?  len правой + suf левой  :  suf правой", 14, TEXT)
    b += text(380, 262, "all  = all левой  и  all правой        нейтральный элемент: len = 0, pre = suf = best = 0, all = true", 12.5, MUTED)
    return figure(svg(760, 290, b), "Для задачи «самая длинная серия нулей на отрезке» в каждой вершине хранится четвёрка (префикс, суффикс, лучшая серия, флаг «весь из нулей»). Склейка за $O(1)$ — это и есть слияние детей.")


def fig_nextequal():
    a = [3, 1, 3, 2, 1, 3]
    b = text(380, 24, "Следующий равный: nxt[i] — позиция ближайшего справа такого же числа", 15)
    x0, w, y = 70, 100, 110
    nxt = []
    for i, v in enumerate(a):
        j = next((k for k in range(i + 1, len(a)) if a[k] == v), len(a))
        nxt.append(j)
    for i, v in enumerate(a):
        b += cell(x0 + i * w, y, 64, 40, str(v), BLUE if v == 3 else (GREEN if v == 1 else ORANGE), 20)
        b += text(x0 + i * w + 32, y + 64, f"i={i}", 12, MUTED)
        b += text(x0 + i * w + 32, y + 88, f"nxt={nxt[i]}", 13, YELLOW)
    for i in range(len(a)):
        if nxt[i] < len(a):
            xa, xb = x0 + i * w + 32, x0 + nxt[i] * w + 32
            mid = (xa + xb) / 2; h = 30 + 6 * (nxt[i] - i)
            b += f'<path d="M {xa} {y} Q {mid} {y-h} {xb} {y}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#ar)"/>'
    b += text(380, 250, "Запрос [l, r): есть два равных  ⇔  min nxt[l..r−1] < r", 16, YELLOW)
    b += text(380, 278, "Здесь для [0,3): min = 2 < 3 — да;  для [1,4): min = 4 ≥ 4 — нет", 13, MUTED)
    return figure(svg(760, 300, b), "Из-за цепочки указателей только последний в группе равных «смотрит» за пределы отрезка; если все указатели ведут за границу $r$, повторов на отрезке нет.")


def fig_msort():
    a = [5, 3, 6, 7, 2, 8, 1]
    b = text(380, 24, "Merge Sort Tree для массива 5 3 6 7 2 8 1: в вершине — отсортированный отрезок", 15)
    def node(l, r):
        return sorted(a[l:r])
    def draw(cx, y, l, r, w):
        arr = node(l, r); n = len(arr)
        out = ""
        x0 = cx - n * 17
        out += f'<rect x="{x0-4}" y="{y-4}" width="{n*34+6}" height="34" rx="6" fill="none" stroke="{EDGE}"/>'
        for i, v in enumerate(arr): out += cell(x0 + i * 34, y, 30, 26, str(v), None, 14)
        if r - l > 1:
            m = (l + r) // 2
            out += line(cx, y + 30, cx - w / 2, y + 66, EDGE, 1.5) + line(cx, y + 30, cx + w / 2, y + 66, EDGE, 1.5)
            out += draw(cx - w / 2, y + 70, l, m, w / 2) + draw(cx + w / 2, y + 70, m, r, w / 2)
        return out
    b += draw(380, 50, 0, 7, 360)
    b += text(380, 340, "Память O(n log n): на каждом из ⌈log n⌉ уровней записано ровно n чисел.", 13, MUTED)
    return figure(svg(760, 360, b), "Запрос «сколько чисел меньше $x$ на отрезке»: $O(\\log n)$ вершин разбиения, в каждой — бинарный поиск, итого $O(\\log^2 n)$.")


def fig_wavelet():
    a = [6, 7, 2, 1, 8, 5, 4, 3]
    b = text(380, 24, "Wavelet Tree: делим не отрезок позиций, а диапазон значений; порядок внутри сохраняется", 15)
    def build(arr, lo, hi, depth, idx, out):
        out.append((depth, idx, lo, hi, arr))
        if lo == hi or len(arr) <= 1: return
        mid = (lo + hi) // 2
        build([x for x in arr if x <= mid], lo, mid, depth + 1, idx * 2, out)
        build([x for x in arr if x > mid], mid + 1, hi, depth + 1, idx * 2 + 1, out)
    nodes = []; build(a, 1, 8, 0, 0, nodes)
    for depth, idx, lo, hi, arr in nodes:
        slots = 2 ** depth; cx = 20 + (idx + 0.5) * 720 / slots; y = 50 + depth * 76
        n = len(arr); x0 = cx - n * 14
        b += f'<rect x="{x0-3}" y="{y-3}" width="{n*28+4}" height="30" rx="6" fill="none" stroke="{EDGE}"/>'
        for i, v in enumerate(arr): b += cell(x0 + i * 28, y, 26, 24, str(v), BLUE if v <= (lo + hi) // 2 else ORANGE, 13)
        b += text(cx, y + 42, f"значения {lo}..{hi}", 10.5, MUTED)
        if depth < 3 and len(arr) > 1 and lo != hi:
            ch = 2 ** (depth + 1); mid = (lo + hi) // 2
            for k, cidx in enumerate((idx * 2, idx * 2 + 1)):
                if any(n2[0] == depth + 1 and n2[1] == cidx for n2 in nodes):
                    cx2 = 20 + (cidx + 0.5) * 720 / ch
                    b += line(cx, y + 48, cx2, y + 70, EDGE, 1.2)
    return figure(svg(760, 360, b), "Синие числа ушли влево ($\\le$ середины диапазона значений), оранжевые — вправо. Для каждой вершины хранится «маска» направлений и префиксные суммы по ней.")


FIGS = {"zeros": fig_zeros, "nextequal": fig_nextequal, "msort": fig_msort, "wavelet": fig_wavelet}


def algo_wavelet():
    a = [6, 7, 2, 1, 8, 5, 4, 3]; l0, r0, x = 1, 6, 6
    nodes = {}
    def build(arr, lo, hi, depth, idx):
        nodes[(depth, idx)] = (lo, hi, arr)
        if lo == hi or len(arr) <= 1: return
        mid = (lo + hi) // 2
        build([v for v in arr if v <= mid], lo, mid, depth + 1, idx * 2)
        build([v for v in arr if v > mid], mid + 1, hi, depth + 1, idx * 2 + 1)
    build(a, 1, 8, 0, 0)
    visits = []  # (depth, idx, l, r, kind, add)
    def rec(depth, idx, l, r):
        if l >= r: return 0
        lo, hi, arr = nodes[(depth, idx)]
        if x <= lo: visits.append((depth, idx, l, r, "out", 0)); return 0
        if hi < x: visits.append((depth, idx, l, r, "take", r - l)); return r - l
        mid = (lo + hi) // 2
        pref = [0]
        for v in arr: pref.append(pref[-1] + (v <= mid))
        ll, lr = pref[l], pref[r]
        visits.append((depth, idx, l, r, "go", 0))
        return rec(depth + 1, idx * 2, ll, lr) + rec(depth + 1, idx * 2 + 1, l - ll, r - lr)
    total = rec(0, 0, l0, r0)
    frames = []
    def draw(upto):
        s = text(24, 20, f"запрос: позиции [{l0}, {r0}), чисел меньше {x}", 13, MUTED, "start")
        seen = {(v[0], v[1]): v for v in visits[:upto]}
        acc = sum(v[5] for v in visits[:upto])
        for (depth, idx), (lo, hi, arr) in nodes.items():
            slots = 2 ** depth; cx = 20 + (idx + 0.5) * 720 / slots; y = 40 + depth * 62
            n = len(arr); x0 = cx - n * 12
            v = seen.get((depth, idx))
            for i, val in enumerate(arr):
                col = None
                if v:
                    inside = v[2] <= i < v[3]
                    col = (GREEN if v[4] == "take" else (RED if v[4] == "out" else YELLOW)) if inside else None
                s += cell(x0 + i * 24, y, 22, 22, str(val), col, 12)
            s += text(cx, y + 36, f"{lo}..{hi}", 10, MUTED)
        s += text(380, 270, f"накоплено: {acc}", 16, YELLOW)
        return s
    msgs = {"go": "диапазон значений вершины пересекает «< x» частично — спускаемся, отрезок пересчитываем по маске",
            "take": "все значения вершины меньше x — берём весь текущий отрезок целиком (зелёный)",
            "out": "все значения не меньше x — вклад 0 (красный)"}
    for k in range(1, len(visits) + 1):
        v = visits[k - 1]
        frames.append({"svg": draw(k), "msg": f"Вершина значений {nodes[(v[0], v[1])][0]}..{nodes[(v[0], v[1])][1]}, отрезок [{v[2]}, {v[3]}): {msgs[v[4]]}."})
    frames.append({"svg": draw(len(visits)), "msg": f"Итого чисел меньше {x} на [{l0}, {r0}): {total}."})
    return {"title": "Wavelet Tree: сколько чисел меньше 6 на позициях [1, 6)", "vb": "0 0 760 290", "frames": frames}


def algos_js():
    data = {"wave": algo_wavelet()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
