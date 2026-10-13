"""Иллюстрации для «Занятие 4. Параллель BS — Динамическое программирование 1»."""
from kit import *


def fig_bin_states():
    b = text(380, 26, "Переходы dp[i][c]: c — на что заканчивается строка", 15)
    xs = [150, 520]
    b += text(xs[0] + 50, 62, "длина i − 1", 14, MUTED) + text(xs[1] + 50, 62, "длина i", 14, MUTED)
    ys = {0: 90, 1: 190}
    for c in (0, 1):
        b += cell(xs[0], ys[c], 100, 56, f"на {c}", BLUE if c == 0 else GREEN, 16)
        b += cell(xs[1], ys[c], 100, 56, f"на {c}", BLUE if c == 0 else GREEN, 16)
    b += line(252, 118, 518, 118, BLUE, 3, arrow=True)           # 0 -> 0
    b += line(252, 128, 518, 208, BLUE, 3, arrow=True)           # 0 -> 1
    b += line(252, 208, 518, 134, BLUE, 3, arrow=True)           # 1 -> 0
    b += line(252, 218, 518, 218, RED, 2, dash="6 5")             # 1 -> 1 запрещён
    b += text(385, 214, "✕ «11» нельзя", 13, RED)
    b += text(385, 110, "ставим 0", 12, MUTED)
    b += text(380, 280, "dp[i][0] = dp[i−1][0] + dp[i−1][1]", 14, YELLOW, mono=True)
    b += text(380, 304, "dp[i][1] = dp[i−1][0]", 14, YELLOW, mono=True)
    return figure(svg(760, 326, b), "В состояние «на 0» можно прийти из любого состояния, в состояние «на 1» — только из «на 0»: две единицы подряд запрещены.")


def fig_lis_tails():
    arr = [3, 7, 6, 10, 8, 9]
    INF = "∞"
    d = [INF] * 5; d[0] = "−∞"
    rows = [("старт", list(d), None)]
    for v in arr:
        pos = next(k for k in range(5) if d[k] == INF or (d[k] != "−∞" and d[k] >= v))
        d[pos] = v
        rows.append((f"+ {v}", list(d), pos))
    W, X0, Y0, H = 84, 190, 56, 40
    b = text(380, 26, "Массив d[len]: наименьший конец НВП длины len. Массив 3 7 6 10 8 9", 15)
    for k in range(5):
        b += text(X0 + k * W + (W - 8) / 2, Y0 - 8, f"len = {k}", 12, MUTED)
    for r, (lab, row, pos) in enumerate(rows):
        y = Y0 + r * (H + 8)
        b += text(X0 - 14, y + H / 2 + 5, lab, 14, YELLOW if pos is not None else MUTED, "end", mono=True)
        for k, v in enumerate(row):
            col = YELLOW if k == pos else (None if v in (INF,) else BLUE)
            b += cell(X0 + k * W, y, W - 8, H, str(v), col, 15)
    b += text(380, Y0 + 7 * (H + 8) + 14, "ответ — число ячеек, не равных ∞: здесь 4 (3, 6, 8, 9)", 13, TEXT)
    return figure(svg(760, Y0 + 7 * (H + 8) + 34, b), "Жёлтым выделена единственная ячейка, меняющаяся при добавлении числа. Сами числа 3 6 8 9 здесь оказались настоящей НВП, но в общем случае массив d не обязан быть подпоследовательностью.")


def fig_lis_split():
    b = text(380, 26, "Добавили число x: что происходит с d (строго возрастает)", 15)
    vals = ["−∞", "2", "5", "7", "9", "12", "∞"]
    x = 6   # x между 5 и 7 -> заменяем 7
    W, X0, y = 92, 50, 90
    for k, v in enumerate(vals):
        col = BLUE if v != "∞" and k < 3 else (YELLOW if k == 3 else (None if v == "∞" else PURPLE))
        b += cell(X0 + k * W, y, W - 8, 50, v, col, 16)
        b += text(X0 + k * W + (W - 8) / 2, y + 70, f"d[{k}]", 12, MUTED, mono=True)
    b += line(X0, 76, X0 + 3 * W - 8, 76, BLUE, 3) + text(X0 + (3 * W - 8) / 2, 68, "d < x: x им не поможет", 13, BLUE)
    b += f'<rect x="{X0 + 3 * W}" y="{y - 6}" width="{W - 8}" height="62" rx="8" fill="none" stroke="{YELLOW}" stroke-width="2" stroke-dasharray="6 4"/>'
    b += text(X0 + 3 * W + (W - 8) / 2, 176, "первое d ≥ x", 13, YELLOW) + text(X0 + 3 * W + (W - 8) / 2, 194, "заменяем на x = 6", 13, YELLOW)
    b += line(X0 + 4 * W, 76, X0 + 7 * W - 8, 76, PURPLE, 3) + text(X0 + 5.5 * W, 68, "дальше: x не продолжит НВП", 13, PURPLE)
    b += text(380, 250, "lower_bound(d.begin(), d.end(), x) — это и есть позиция замены; если все d меньше x — занимаем первую ∞", 12, MUTED)
    return figure(svg(760, 280, b), "Слева все d меньше x: их конец уже лучше, помогать нечему. Справа — слишком большие, к ним x приписать нельзя. Меняется ровно одна ячейка.")


def fig_lcs():
    A, B = "ABCBD", "BDCAB"
    n, m = len(A), len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i-1][j-1] + 1 if A[i-1] == B[j-1] else max(dp[i-1][j], dp[i][j-1])
    path = {(5, 5), (4, 5), (3, 4), (3, 3), (2, 2), (2, 1), (1, 0), (0, 0)}
    match = {(4, 5), (3, 3), (2, 1)}
    W, X0, Y0 = 70, 150, 70
    b = text(380, 26, "dp[i][j] для A = ABCBD и B = BDCAB, ответ — 3 (BCB)", 15)
    for j in range(1, m + 1):
        b += text(X0 + j * W + 30, Y0 - 10, B[j - 1], 16, YELLOW, weight="700")
    for i in range(1, n + 1):
        b += text(X0 - 18, Y0 + i * 46 + 29, A[i - 1], 16, YELLOW, "end", "700")
    for i in range(n + 1):
        for j in range(m + 1):
            col = GREEN if (i, j) in match else (BLUE if (i, j) in path and i and j else None)
            b += cell(X0 + j * W, Y0 + i * 46, W - 6, 40, str(dp[i][j]), col, 16)
    b += text(X0 + 3 * W, Y0 + 6 * 46 + 12, "зелёные клетки — совпавшие символы при обратном ходе", 13, GREEN)
    return figure(svg(760, Y0 + 6 * 46 + 34, b), "Собственный пример. Обратный ход начинается в правом нижнем углу: при равных символах идём по диагонали и запоминаем символ, иначе — в сторону большего соседа.")


def fig_swim():
    b = text(380, 26, "Штраф — сумма сдвигов границ: |P₁−Q₁| + |P₂−Q₂|", 15)
    X0, U = 150, 56  # 1 человек = U пикселей
    def bar(y, vals, title, col):
        s = text(X0 - 6, y + 22, title, 13, MUTED, "end")
        x = X0
        for v in vals:
            if v:
                s += cell(x, y, v * U - 4, 36, str(v), col, 15)
            else:
                s += f'<rect x="{x}" y="{y}" width="8" height="36" rx="3" fill="none" stroke="{MUTED}" stroke-dasharray="3 3"/>' + text(x + 4, y + 52, "0", 12, MUTED)
            x += v * U
        return s
    b += bar(70, [8, 0, 2], "было 8 0 2", BLUE)
    b += bar(200, [4, 3, 3], "стало 4 3 3", GREEN)
    # границы
    for P, Q, c, lab in ((8, 4, ORANGE, "|8 − 4| = 4"), (8, 7, RED, "|8 − 7| = 1")):
        xp, xq = X0 + P * U, X0 + Q * U
        yy = 128 if c == ORANGE else 160
        b += line(xp, yy, xq, yy, c, 3, arrow=True)
        b += text(xp + 10, yy + 5, lab, 13, c, "start")
    b += text(380, 290, "итого 4 + 1 = 5 «потревоженных» — как в примере на лекции", 14, YELLOW)
    return figure(svg(760, 312, b), "Каждая граница дорожки сдвигается с префиксной суммы P на Q; человек, оказавшийся между старым и новым положением границы, считается один раз за каждую такую границу.")


FIGS = {"binstates": fig_bin_states, "tails": fig_lis_tails, "split": fig_lis_split, "lcs": fig_lcs, "swim": fig_swim}
