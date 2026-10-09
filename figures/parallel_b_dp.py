"""Иллюстрации и плееры для «Занятие 3. Параллель B — Динамическое программирование 1»."""
import json
from kit import *


def fig_orient():
    b = text(380, 24, "Дни — рёбра между проектами; ориентация ребра = кто какой проект делает", 15)
    P = {"A": (380, 70), "B": (230, 200), "C": (530, 200)}
    for a, c, col in [("A", "B", BLUE), ("B", "C", GREEN), ("C", "A", ORANGE)]:
        (x1, y1), (x2, y2) = P[a], P[c]
        dx, dy = x2 - x1, y2 - y1; L = (dx * dx + dy * dy) ** 0.5
        b += line(x1 + dx / L * 28, y1 + dy / L * 28, x2 - dx / L * 28, y2 - dy / L * 28, col, 3.5, arrow=True)
    for k, (x, y) in P.items(): b += circle(x, y, 24, k, None, 17)
    b += text(380, 270, "в каждой вершине входящих рёбер столько же, сколько исходящих ⇒ проект делают поровну", 14, TEXT)
    b += text(380, 296, "Такая ориентация — направление обхода эйлерова цикла (степени всех вершин чётны)", 13, MUTED)
    return figure(svg(760, 316, b), "Алексей делает проект в начале стрелки, Иван — в конце. Цикл $A\\to B\\to C\\to A$: каждый проект встречается один раз как начало и один раз как конец.")


def fig_interval():
    b = text(380, 24, "Динамика по подотрезкам: dp[l][r] собирается из dp[l][k] и dp[k][r]", 15)
    xs = [0, 2, 5, 9, 14]
    X = lambda v: 60 + v * 45
    b += line(X(0), 80, X(14), 80, AXIS, 4)
    for i, v in enumerate(xs): b += circle(X(v), 80, 6, "", YELLOW) + text(X(v), 110, f"x{i}={v}", 12.5, MUTED)
    b += f'<rect x="{X(0)}" y="64" width="{X(14)-X(0)}" height="32" rx="8" fill="none" stroke="{BLUE}" stroke-width="2"/>'
    b += text(380, 150, "первый разрез по x₂ = 5:  стоимость = (14 − 0)  +  dp[0][2]  +  dp[2][4]", 15, YELLOW)
    b += f'<rect x="{X(0)}" y="168" width="{X(5)-X(0)}" height="26" rx="6" fill="{SOFT[GREEN]}" stroke="{GREEN}" stroke-width="2"/>'
    b += f'<rect x="{X(5)}" y="168" width="{X(14)-X(5)}" height="26" rx="6" fill="{SOFT[ORANGE]}" stroke="{ORANGE}" stroke-width="2"/>'
    b += text((X(0) + X(5)) / 2, 186, "dp[0][2]", 14, TEXT) + text((X(5) + X(14)) / 2, 186, "dp[2][4]", 14, TEXT)
    b += text(380, 240, "оба куска короче исходного ⇒ считаем отрезки по возрастанию длины;  n² состояний × n разрезов = O(n³)", 13.5, MUTED)
    return figure(svg(760, 262, b), "Стоимость разреза — длина текущего куска. Перебирая первый разрез $k$, получаем два независимых подзадачи.")


def fig_bitset():
    b = text(380, 24, "Рюкзак в bitset: новый слой = старый | (старый << w)", 15)
    old = [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    w = 2
    sh = [0] * w + old[:-w]
    new = [a | c for a, c in zip(old, sh)]
    rows = [("dp (старый)", old, BLUE), (f"dp << {w}", sh, ORANGE), ("dp | (dp << w)", new, GREEN)]
    for r, (lab, bits, col) in enumerate(rows):
        y = 60 + r * 62
        b += text(30, y + 22, lab, 14, MUTED, "start")
        for i, v in enumerate(bits): b += cell(190 + i * 40, y, 36, 32, str(v), col if v else None, 15)
    for i in range(12): b += text(190 + i * 40 + 18, 252, str(i), 11, MUTED)
    b += text(380, 280, "один сдвиг и одно OR обрабатывают 64 суммы за такт: время n·S/64", 13.5, TEXT)
    return figure(svg(760, 300, b), "Бит $s$ равен 1, если вес $s$ можно набрать. Предмет веса $w$ добавляет к множеству достижимых сумм его же сдвиг.")


def fig_digit():
    b = text(380, 24, "Динамика по цифрам: пока префикс равен префиксу R — «прижаты», потом — «свободны»", 15)
    digs = "4730"
    for i, ch in enumerate(digs):
        b += cell(70 + i * 90, 60, 76, 44, ch, BLUE, 22)
    b += text(70, 130, "R = 4730: на каждой позиции цифра либо равна цифре R (остаёмся прижатыми), либо меньше (переходим во «свободны»)", 12.5, MUTED, "start")
    b += cell(140, 160, 200, 40, "флаг = 0 (равны R)", BLUE, 15) + cell(420, 160, 220, 40, "флаг = 1 (уже меньше R)", GREEN, 15)
    b += line(340, 180, 418, 180, YELLOW, 3, arrow=True) + text(380, 170, "d < цифры R", 12, YELLOW)
    b += f'<path d="M 240 160 Q 240 140 290 140" fill="none" stroke="{MUTED}" stroke-width="1.8"/>' + text(240, 136, "d = цифре R", 12, MUTED)
    b += f'<path d="M 530 200 Q 530 232 580 232 Q 630 232 630 204" fill="none" stroke="{MUTED}" stroke-width="1.8"/>' + text(530, 252, "любая цифра 0–9", 12, MUTED)
    b += text(380, 290, "Состояние: (позиция, сумма цифр / остаток, флаг);  ответ на [L, R] = f(R) − f(L − 1)", 14, TEXT)
    return figure(svg(760, 312, b), "Сравнение чисел слева направо: до первой различающейся позиции префиксы равны.")


FIGS = {"orient": fig_orient, "interval": fig_interval, "bitset": fig_bitset, "digit": fig_digit}


def algo_lis(a=(3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)):
    frames = []; d = []
    import bisect
    def draw(i, pos, note, tails):
        s = text(24, 22, "массив a:", 13, MUTED, "start")
        for k, v in enumerate(a):
            col = YELLOW if k == i else (None if k > i else SOFT[BLUE] and BLUE)
            s += cell(40 + k * 50, 34, 44, 32, str(v), (YELLOW if k == i else (BLUE if k < i else None)), 15)
        s += text(24, 100, "d (хвосты возрастающих подпоследовательностей по длинам):", 13, MUTED, "start")
        for k in range(max(len(tails), 1)):
            if k < len(tails): s += cell(40 + k * 50, 112, 44, 32, str(tails[k]), (GREEN if k == pos else None), 15) + text(62 + k * 50, 160, f"len {k+1}", 10.5, MUTED)
        s += text(24, 196, note, 13, TEXT, "start")
        return s
    frames.append({"svg": draw(-1, -1, "Пока пусто. Для каждого x ищем первое d[len] ≥ x (lower_bound).", []), "msg": "Начало: список хвостов пуст."})
    for i, x in enumerate(a):
        pos = bisect.bisect_left(d, x)
        before = list(d)
        frames.append({"svg": draw(i, pos, f"x = {x}: первое d ≥ x стоит на месте {pos + 1}" + ("" if pos < len(d) else " (его нет — удлиняем)"), before), "msg": f"Читаем {x}: lower_bound даёт позицию {pos + 1}."})
        if pos == len(d): d.append(x)
        else: d[pos] = x
        frames.append({"svg": draw(i, pos, f"записали x на место {pos + 1}: теперь длина {pos + 1} заканчивается минимально возможным числом {x}", list(d)), "msg": f"d[{pos + 1}] = {x}. Длина НВП = {len(d)}."})
    return {"title": "НВП за O(n log n): массив хвостов d", "vb": "0 0 620 210", "frames": frames}


def algos_js():
    data = {"lis": algo_lis()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
