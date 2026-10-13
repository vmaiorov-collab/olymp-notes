"""Иллюстрации для «Занятие 6. Параллель B — Кратчайшие пути»."""
from kit import *


def fig_bfs_queue():
    b = text(380, 26, "Очередь BFS: префикс с расстоянием x, суффикс с расстоянием x + 1", 15)
    W, X0 = 62, 200
    def row(y, vals, title, lab):
        o = text(X0 - 14, y + 20, title, 13, MUTED, "end") + text(X0 - 14, y + 38, lab, 11, MUTED, "end")
        for i, v in enumerate(vals):
            col = BLUE if v == 0 else (GREEN if v == 1 else ORANGE)
            o += cell(X0 + i * W, y, W - 6, 44, ["x", "x+1", "x+2"][v], col, 15)
        return o
    b += row(60, [0, 0, 0, 1, 1], "было", "")
    b += row(150, [0, 0, 1, 1, 1, 1], "стало", "достали x, дописали x+1")
    b += row(240, [1, 1, 1, 2, 2], "если все были x+1:", "тот же вид, x → x+1")
    b += line(X0 + 26, 108, X0 + 26, 144, MUTED, 2, arrow=True)
    b += text(X0 + 26, 56, "достаём ▼", 12, YELLOW)
    b += text(X0 + 6 * W + 10, 178, "◄ дописываем", 12, YELLOW, "start")
    b += text(380, 318, "порядок «сначала x, потом x+1» не нарушается — достаём всегда минимум", 13, TEXT)
    return figure(svg(760, 336, b), "Очередь BFS всегда состоит из блока «x» и блока «x + 1»: из начала берём вершину с расстоянием x, в конец дописываем вершины с расстоянием x + 1.")


def fig_dijkstra_proof():
    b = text(380, 26, "Доказательство Дейкстры: кратчайший путь из S в U выходит из помеченных вершин", 15)
    b += f'<ellipse cx="190" cy="160" rx="160" ry="105" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="7 5"/>'
    b += text(190, 74, "помеченные вершины", 14, BLUE)
    b += circle(80, 160, 22, "S", GREEN, 16)
    b += circle(230, 130, 22, "", BLUE) + circle(260, 190, 22, "Y", BLUE, 16)
    b += circle(440, 130, 24, "X", ORANGE, 16)
    b += circle(640, 170, 24, "U", RED, 16)
    b += line(100, 154, 208, 132, BLUE, 3, arrow=True)
    b += line(250, 132, 252, 168, BLUE, 3, arrow=True)
    b += line(282, 184, 416, 138, ORANGE, 3, arrow=True)
    b += line(464, 136, 616, 164, ORANGE, 3, arrow=True)
    b += text(372, 178, "w(Y,X)", 12, ORANGE)
    b += text(440, 176, "первая непомеченная", 12, ORANGE)
    b += text(640, 214, "вынимаем из очереди", 12, RED)
    b += text(380, 304, "D[U] ≤ D[X] = dist[X] ≤ dist[U] ≤ D[U]", 17, YELLOW, mono=True)
    b += text(380, 334, "U — минимум очереди · Y помечена · веса ≥ 0 · D — длина какого-то пути", 12, MUTED)
    return figure(svg(760, 350, b), "Цепочка неравенств замыкается, поэтому D[U] = dist[U]. При отрицательных рёбрах разрушается третье звено: префикс пути до X может быть длиннее всего пути.")


def fig_dial():
    K = 3
    b = text(380, 22, "Циклические очереди: K + 1 = 4 корзины, номер = расстояние mod (K+1)", 15)
    W, X0, y = 150, 60, 70
    names = ["≡ 0 (mod 4)", "≡ 1", "≡ 2", "≡ 3"]
    items = [["d=4"], ["d=1", "d=5"], ["d=2"], ["d=3", "d=3"]]
    for i in range(K + 1):
        col = YELLOW if i == 0 else BLUE
        b += cell(X0 + i * (W + 10), y, W, 40, names[i], col, 14)
        for j, it in enumerate(items[i]):
            b += cell(X0 + i * (W + 10) + 10, y + 56 + j * 42, W - 20, 34, it, None, 13)
    b += text(X0 + W / 2, 56, "▼ сейчас разбираем", 12, YELLOW)
    # циклическая стрелка
    b += f'<path d="M {X0 + 3 * (W + 10) + W / 2} {y + 160} C {X0 + 3 * (W + 10) + W / 2} 235, {X0 + W / 2} 235, {X0 + W / 2} {y + 160}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#ar)"/>'
    b += text(380, 246, "после последней корзины возвращаемся к нулевой", 13, MUTED)
    b += text(380, 280, "ребро длины c из вершины с d[v] кладёт её в корзину (d[v] + c) mod (K+1)", 13, TEXT)
    return figure(svg(760, 300, b), "Как сортировка подсчётом, только корзины зациклены: в любой момент в них лежат расстояния из диапазона [x, x + K], поэтому K + 1 корзины хватает.")


def fig_floyd():
    b = text(380, 26, "Флойд: путь a → b либо обходится без c, либо идёт через c", 15)
    b += circle(90, 110, 26, "a", GREEN, 18) + circle(670, 110, 26, "b", GREEN, 18) + circle(380, 190, 26, "c", ORANGE, 18)
    b += line(120, 108, 640, 108, BLUE, 3, arrow=True)
    b += text(380, 98, "dp[c−1][a][b] — без вершины c", 13, BLUE)
    b += line(110, 132, 354, 180, ORANGE, 3, arrow=True)
    b += line(406, 180, 650, 132, ORANGE, 3, arrow=True)
    b += text(210, 176, "dp[c−1][a][c]", 13, ORANGE) + text(560, 176, "dp[c−1][c][b]", 13, ORANGE)
    b += text(380, 252, "d[a][b] = min(d[a][b], d[a][k] + d[k][b])", 17, YELLOW, mono=True)
    b += text(380, 282, "для ориентированного графа порядок a → k → b важен · внешний цикл по k", 12, MUTED)
    return figure(svg(760, 302, b), "Кратчайший путь a → b среди путей с промежуточными вершинами ≤ c либо не заходит в c, либо разбивается в c на два пути, использующих лишь вершины < c.")


def fig_ford_perm():
    b = text(380, 26, "Перестановка рёбер, повторённая несколько раз: любой путь — подпоследовательность", 15)
    names = ["e1", "e2", "e3", "e4"]
    X0, W, y = 60, 48, 70
    for blk in range(3):
        for i, nm in enumerate(names):
            hi = (blk == 0 and nm == "e3") or (blk == 1 and nm == "e1") or (blk == 2 and nm == "e4")
            b += cell(X0 + blk * 4 * W * 1.18 + i * W, y, W - 4, 40, nm, GREEN if hi else None, 14)
        b += text(X0 + blk * 4 * W * 1.18 + 2 * W - 2, y + 62, f"блок {blk + 1}", 12, MUTED)
    b += text(380, 190, "путь e3 → e1 → e4: первое ребро берём из блока 1, второе из блока 2, третье из блока 3", 13, GREEN)
    b += text(380, 224, "n блоков по m рёбер ⇒ O(n·m)", 17, YELLOW, mono=True)
    b += text(380, 254, "если за целый проход ничего не улучшилось — выходим", 13, MUTED)
    return figure(svg(760, 276, b), "Не зная правильного порядка рёбер кратчайшего пути, мы проходим по всем рёбрам снова и снова. Кратчайший путь содержит не более n − 1 рёбер, поэтому n проходов хватит.")


def fig_implicit():
    b = text(380, 26, "Неявный граф: одно ребро-отрезок u → [l, r] с весом w", 15)
    X0, W, y = 70, 56, 120
    for i in range(10):
        inside = 3 <= i <= 7
        b += cell(X0 + i * W, y, W - 4, 40, str(i), PURPLE if inside else None, 14)
    b += circle(X0 + 1 * W + 24, 60, 20, "u", BLUE, 16)
    b += line(X0 + 1 * W + 40, 72, X0 + 3 * W + 24, 118, PURPLE, 2, arrow=True)
    b += line(X0 + 1 * W + 44, 66, X0 + 7 * W + 24, 118, PURPLE, 2, arrow=True)
    b += text(380, 212, "chmin на отрезке [3, 7] значением d[u] + w — одна операция за O(log n)", 13, PURPLE)
    b += text(380, 244, "минимум из корня дерева — следующая вершина Дейкстры; вынутую вершину «выключаем»", 13, TEXT)
    return figure(svg(760, 268, b), "Вместо O(r − l + 1) отдельных рёбер выполняется одна массовая операция «chmin» на дереве отрезков. Всего (n + m) операций по O(log n).")


FIGS = {"bfs_queue": fig_bfs_queue, "dijkstra_proof": fig_dijkstra_proof, "dial": fig_dial,
        "floyd": fig_floyd, "ford_perm": fig_ford_perm, "implicit": fig_implicit}
