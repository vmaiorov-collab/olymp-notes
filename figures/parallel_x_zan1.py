"""Иллюстрации и плеер для «Занятие 1. Параллель X — Применение дерева отрезков»."""
import json
from kit import *


def fig_persist():
    b = text(380, 24, "Персистентность: обновление копирует только путь, остальное — общие ссылки", 15)
    def tree(ox, oy, title, new):
        out = text(ox + 110, oy - 12, title, 13, MUTED)
        pos = {0: (ox + 110, oy + 20), 1: (ox + 50, oy + 80), 2: (ox + 170, oy + 80), 3: (ox + 20, oy + 140), 4: (ox + 80, oy + 140), 5: (ox + 140, oy + 140), 6: (ox + 200, oy + 140)}
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        for a, c in edges:
            col = GREEN if (a in new and c in new) else EDGE
            out += line(pos[a][0], pos[a][1], pos[c][0], pos[c][1], col, 2)
        for k, (x, y) in pos.items():
            out += circle(x, y, 15, "", GREEN if k in new else BLUE)
        return out
    b += tree(40, 60, "версия i−1", set())
    b += tree(330, 60, "версия i (зелёное — новые вершины)", {0, 1, 4})
    b += line(300, 130, 330, 130, MUTED, 2, arrow=True)
    b += text(380, 270, "Новая версия делит с прежней все поддеревья, которые не изменились: O(log n) новых вершин на вставку", 13, MUTED)
    b += text(380, 292, "запрос (l, r) = (версия r) − (версия l−1)  —  спуск сразу по двум деревьям", 13, YELLOW)
    return figure(svg(760, 312, b), "Каждая версия — отдельный корень. Старые версии остаются доступны, поэтому на запросы можно отвечать онлайн.")


def fig_distinct():
    a = [3, 1, 3, 2, 1, 3, 2]
    last = {}; prev = []
    for i, v in enumerate(a):
        prev.append(last.get(v, -1)); last[v] = i
    b = text(380, 24, "prev[i] — индекс предыдущего такого же; на отрезке [l, r] считаем i с prev[i] < l", 15)
    l, r = 2, 5
    b += text(30, 76, "a", 13, MUTED, "start") + text(30, 120, "prev", 13, MUTED, "start") + text(30, 164, "учитывается", 13, MUTED, "start")
    for i, v in enumerate(a):
        inr = l <= i <= r
        cnt = inr and prev[i] < l
        b += cell(110 + i * 80, 56, 70, 34, str(v), BLUE if inr else None, 16) + text(145 + i * 80, 110 - 14, str(i), 11, MUTED) if False else cell(110 + i * 80, 56, 70, 34, str(v), BLUE if inr else None, 16) + text(145 + i * 80, 108, f"i={i}", 11, MUTED)
        b += cell(110 + i * 80, 112, 70, 34, str(prev[i]), (GREEN if cnt else (RED if inr else None)), 16)
        b += text(145 + i * 80, 176, "да" if cnt else ("нет" if inr else ""), 14, GREEN if cnt else RED)
    b += text(380, 224, f"запрос [l, r] = [{l}, {r}]: условие prev[i] < l = {l} — 3 различных значения (1, 3, 2)", 14, YELLOW)
    return figure(svg(760, 246, b), "В отрезке учитывается только первое вхождение каждого значения: у него предыдущее вхождение лежит левее $l$.")


def fig_dst():
    b = text(380, 24, "Disjoint sparse table: два готовых значения на любой отрезок", 15)
    n = 8
    for lev, (ytop, half) in enumerate([(54, 4), (112, 2), (170, 1)]):
        for bl in range(n // (2 * half)):
            mid = bl * 2 * half + half
            for i in range(mid - half, mid + half):
                col = ORANGE if i < mid else GREEN
                b += cell(60 + i * 80, ytop, 74, 34, "суфф." if i < mid else "преф.", col, 12)
        b += text(30, ytop + 22, f"{lev}", 12, MUTED)
    b += text(380, 238, "запрос [l, r]: уровень = старший бит l XOR r;  ответ = t[уровень][l] ⊕ t[уровень][r]", 14, YELLOW)
    return figure(svg(760, 262, b), "На каждом уровне: суффиксы левой половины и префиксы правой для всех блоков. Отрезок через границу блока — сумма двух кусков.")


def fig_nopush():
    b = text(380, 24, "Без push: у вершины свой модификатор, предков он не касается", 15)
    pos = {0: (380, 70), 1: (230, 150), 2: (530, 150), 3: (150, 230), 4: (310, 230), 5: (450, 230), 6: (610, 230)}
    for a, c in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]: b += line(pos[a][0], pos[a][1], pos[c][0], pos[c][1], EDGE, 2)
    mods = {1: "+3"}
    for k, (x, y) in pos.items():
        col = GREEN if k == 1 else None
        b += circle(x, y, 22, "", col)
        b += text(x, y + 5, "mn" if k != 1 else "mn", 12, TEXT)
    b += text(230 + 38, 143, "mod = +3", 13, GREEN, "start")
    b += text(380, 280, "mn[v] = min(mn[левый], mn[правый]) + mod[v];  get(v) возвращает ответ без модификаторов предков", 13, MUTED)
    b += text(380, 302, "годится, когда операции перестановочны (сложение); присваивание так не сделать", 13, YELLOW)
    return figure(svg(760, 322, b), "Запрос, проходя вверх по рекурсии, добавляет модификатор каждой вершины на пути — отдельный push не нужен.")


FIGS = {"persist": fig_persist, "distinct": fig_distinct, "dst": fig_dst, "nopush": fig_nopush}


def algo_mex(a=(0, 2, 1, 4, 1, 0, 3), l=2):
    n = len(a); frames = []; last = [-1] * (n + 1)
    def draw(r, note, mex=None):
        s = text(24, 22, f"запрос: l = {l}", 13, MUTED, "start")
        for i, v in enumerate(a):
            s += cell(40 + i * 54, 34, 50, 32, str(v), YELLOW if i == r else (BLUE if i <= r else None), 15) + text(40 + i * 54 + 25, 82, str(i), 11, MUTED)
        s += text(24, 110, "last[x]:", 13, MUTED, "start")
        for x in range(n + 1):
            col = GREEN if last[x] >= l else RED
            s += cell(40 + x * 54, 118, 50, 32, str(last[x]), col, 15) + text(40 + x * 54 + 25, 166, f"x={x}", 11, MUTED)
        s += text(24, 198, note, 13, MUTED, "start")
        if mex is not None: s += text(24, 224, f"mex = {mex} (первый x с last[x] < {l})", 15, YELLOW, "start")
        return s
    for r, v in enumerate(a):
        if v <= n: last[v] = r
        frames.append({"svg": draw(r, f"читаем a[{r}] = {v}: last[{v}] = {r}"), "msg": f"Добавили a[{r}] = {v}: last[{v}] = {r}."})
    mex = next(x for x in range(n + 1) if last[x] < l)
    frames.append({"svg": draw(n - 1, "красные x: last[x] < l — на [l, r] отсутствуют", mex), "msg": f"Для l = {l} и r = {n - 1}: ищем минимальный x с last[x] < {l}. Это x = {mex}."})
    return {"title": "MEX на отрезке: last[x] и первое x с last[x] < l", "vb": "0 0 540 240", "frames": frames}


def algos_js():
    data = {"mex": algo_mex()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
