"""Иллюстрации и плееры для «Занятие 2. Параллель B — Применения DFS»."""
import json
from kit import *


def fig_dfstree():
    b = text(380, 24, "Дерево DFS: нет «горизонтальных» рёбер — все лишние рёбра вертикальные (предок — потомок)", 15)
    pos = {1: (380, 70), 2: (260, 140), 3: (500, 140), 4: (190, 215), 5: (330, 215), 6: (500, 215)}
    tree = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    back = [(4, 1), (5, 1), (6, 1)]
    for a, c in tree: b += line(*pos[a], *pos[c], BLUE, 3)
    for a, c in back:
        xa, ya = pos[a]; xc, yc = pos[c]
        mx = (xa + xc) / 2 + (-70 if a in (4, 5) else 70)
        b += f'<path d="M {xa} {ya} Q {mx} {(ya+yc)/2} {xc} {yc+14}" fill="none" stroke="{ORANGE}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    for v, (x, y) in pos.items(): b += circle(x, y, 20, str(v), GREEN if v == 1 else None, 15)
    b += line(120, 275, 160, 275, BLUE, 3) + text(170, 280, "ребро дерева", 13, TEXT, "start")
    b += line(320, 275, 360, 275, ORANGE, 3, dash="6 4") + text(370, 280, "вертикальное (обратное) ребро", 13, TEXT, "start")
    b += text(380, 312, "Ребра между разными поддеревьями (между 4 и 6, например) DFS бы обязательно «прошёл» и они стали бы деревянными", 12.5, MUTED)
    return figure(svg(760, 330, b), "DFS не меняет граф, а «поворачивает» его: каждое ребро либо ведёт из вершины к потомку, либо является ребром дерева.")


def fig_condense():
    b = text(380, 24, "Конденсация: компоненты сильной связности сжаты в вершины — получается DAG", 15)
    def comp(cx, cy, nodes, col):
        out = f'<ellipse cx="{cx}" cy="{cy}" rx="{70}" ry="{44}" fill="{SOFT[col]}" fill-opacity="0.55" stroke="{col}" stroke-width="2"/>'
        n = len(nodes)
        for i, v in enumerate(nodes):
            ang = i * 6.283 / n
            out += circle(cx + 26 * (1 if n > 1 else 0) * __import__("math").cos(ang), cy + 18 * (1 if n > 1 else 0) * __import__("math").sin(ang), 11, str(v), None, 12)
        return out
    b += comp(150, 110, [1, 2, 3], BLUE) + comp(380, 110, [4, 5], GREEN) + comp(610, 110, [6, 7], ORANGE) + comp(380, 230, [8], PURPLE)
    b += line(220, 110, 308, 110, MUTED, 2.5, arrow=True) + line(450, 110, 538, 110, MUTED, 2.5, arrow=True) + line(380, 154, 380, 192, MUTED, 2.5, arrow=True)
    b += text(150, 180, "C₁", 14, BLUE) + text(380, 70, "C₂", 14, GREEN) + text(610, 180, "C₃", 14, ORANGE) + text(440, 232, "C₄", 14, PURPLE, "start")
    b += text(380, 295, "Номера в алгоритме Косарайю идут от «стоков» к «истокам»: у C₃ (сток) номер 0.", 13, MUTED)
    return figure(svg(760, 310, b), "Внутри компоненты из любой вершины можно дойти в любую; между компонентами рёбра образуют ациклический граф.")


def fig_implication():
    b = text(380, 24, "Дизъюнкт (a ∨ b) = два ребра: ¬a → b и ¬b → a", 15)
    P = {"a": (200, 90), "¬a": (200, 210), "b": (560, 90), "¬b": (560, 210)}
    for k, (x, y) in P.items(): b += circle(x, y, 26, k, GREEN if "¬" not in k else RED, 16)
    b += line(226, 200, 534, 100, YELLOW, 3, arrow=True) + line(534, 200, 226, 100, YELLOW, 3, arrow=True)
    b += text(380, 280, "Транзитивность импликации: путь ¬a ⇒ … ⇒ b означает «если a ложно, то b истинно»", 13.5, TEXT)
    b += text(380, 306, "x и ¬x в одной компоненте ⇒ решения нет;  иначе true получает та вершина пары, что стоит ПОЗЖЕ в топсорте", 13, MUTED)
    return figure(svg(760, 326, b), "Граф импликаций симметричен: вместе с ребром $u\\to v$ в нём есть и ребро $\\neg v\\to\\neg u$.")


def fig_blockcut():
    b = text(380, 24, "Граф и его круглоквадратное дерево: блоки — квадраты, вершины — круги", 15)
    pos = {1: (60, 80), 2: (150, 80), 3: (150, 170), 4: (240, 125), 5: (330, 125), 6: (420, 80), 7: (420, 170), 8: (500, 125)}
    ed = [(1, 2), (2, 3), (2, 4), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (6, 7), (5, 8)]
    cols = {(1, 2): RED, (2, 3): BLUE, (2, 4): BLUE, (3, 4): BLUE, (4, 5): GREEN}
    for e in ed: b += line(*pos[e[0]], *pos[e[1]], cols.get(e, PURPLE), 3)
    for v, (x, y) in pos.items(): b += circle(x, y, 15, str(v), None, 13)
    # дерево
    tx = {1: 90, 2: 190, 3: 290, 4: 390, 5: 490, 6: 590, 7: 690, 8: 740}
    # квадраты: R{1,2}, B{2,3,4}, G{4,5}, P{5,6,7,8}
    sq = {"R": (150, 270, RED), "B": (260, 270, BLUE), "G": (370, 270, GREEN), "P": (520, 270, PURPLE)}
    circ = {1: (60, 345), 2: (150, 345), 3: (230, 345), 4: (320, 345), 5: (430, 345), 6: (500, 345), 7: (550, 345), 8: (600, 345)}
    for name, (x, y, c) in sq.items(): b += f'<rect x="{x-17}" y="{y-17}" width="34" height="34" rx="5" fill="{SOFT[c]}" stroke="{c}" stroke-width="2.5"/>' + text(x, y + 6, name, 15)
    for blk, vs in {"R": [1, 2], "B": [2, 3, 4], "G": [4, 5], "P": [5, 6, 7, 8]}.items():
        x, y, c = sq[blk]
        for v in vs: b += line(x, y + 17, *circ[v], c, 2, ) if False else ""
    # рёбра дерева
    for blk, vs in {"R": [1, 2], "B": [2, 3, 4], "G": [4, 5], "P": [5, 6, 7, 8]}.items():
        x, y, c = sq[blk]
        for v in vs: b += line(x, y + 17, circ[v][0], circ[v][1] - 14, c, 2)
    for v, (x, y) in circ.items(): b += circle(x, y, 14, str(v), None, 13)
    b += text(380, 395, "точки сочленения 2, 4, 5 — круги степени ≥ 2;  мосты — блоки R и G из двух вершин", 13, MUTED)
    return figure(svg(760, 410, b), "Простой путь между $a$ и $b$ проходит через те же блоки, что и путь в дереве; вершина $c$ достижима на таком пути, если её блок лежит на дереве-пути.")


FIGS = {"dfstree": fig_dfstree, "condense": fig_condense, "implication": fig_implication, "blockcut": fig_blockcut}


def algo_euler():
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]
    pos = {0: (380, 110), 1: (250, 40), 2: (250, 180), 3: (510, 40), 4: (510, 180)}
    adj = {v: [] for v in pos}
    for i, (a, c) in enumerate(edges): adj[a].append((c, i)); adj[c].append((a, i))
    used = [False] * len(edges); ptr = {v: 0 for v in pos}; stack = [0]; res = []
    frames = []
    def draw(cur, msg):
        s = ""
        for i, (a, c) in enumerate(edges):
            s += line(*pos[a], *pos[c], "#3b4a63" if used[i] else BLUE, 2.2 if used[i] else 3.5, dash="5 5" if used[i] else None)
        for v, (x, y) in pos.items(): s += circle(x, y, 17, str(v), YELLOW if v == cur else None, 15)
        s += text(24, 232, "стек: " + " ".join(map(str, stack)), 14, TEXT, "start")
        s += text(24, 254, "ответ (в порядке выхода): " + " ".join(map(str, res)), 14, GREEN, "start")
        return s
    frames.append({"svg": draw(0, ""), "msg": "Старт в вершине 0: все рёбра свободны. Стек = [0]."})
    while stack:
        v = stack[-1]
        while ptr[v] < len(adj[v]) and used[adj[v][ptr[v]][1]]: ptr[v] += 1
        if ptr[v] == len(adj[v]):
            res.append(v); stack.pop()
            frames.append({"svg": draw(stack[-1] if stack else None, ""), "msg": f"Из {v} выходить некуда — выносим {v} из стека в ответ."})
            continue
        to, i = adj[v][ptr[v]]; used[i] = True; stack.append(to)
        frames.append({"svg": draw(to, ""), "msg": f"Идём по свободному ребру {v}—{to}, ребро удаляем (пунктир). Стек растёт."})
    frames.append({"svg": draw(None, ""), "msg": "Стек пуст. Ответ содержит " + str(len(res)) + " вершин = 6 рёбер + 1: эйлеров цикл найден."})
    return {"title": "Алгоритм Хирхольцера на двух треугольниках с общей вершиной", "vb": "0 0 760 270", "frames": frames}


def algos_js():
    data = {"euler": algo_euler()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
