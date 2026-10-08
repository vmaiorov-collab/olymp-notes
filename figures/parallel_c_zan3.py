"""Иллюстрации и плееры для «Занятие 3. Параллель C — Бинарный поиск»."""
import json, math
from kit import *


def fig_guess():
    b = text(380, 24, "Угадай число от 1 до 100: каждый вопрос вдвое сужает отрезок", 15)
    secret = 37; y = 50; steps = []; l, r = 0, 101
    while l + 1 < r:
        m = (l + r) // 2
        steps.append((l, r, m))
        if m < secret: l = m
        else: r = m
    X = lambda v: 40 + (v / 101) * 680
    for k, (l0, r0, m) in enumerate(steps):
        yy = y + k * 34
        b += f'<rect x="{X(l0)}" y="{yy}" width="{X(r0) - X(l0)}" height="18" rx="4" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'
        b += line(X(m), yy - 3, X(m), yy + 21, YELLOW, 3)
        b += text(X(m) + 6, yy + 14, f"{k + 1}: m={m}", 12, TEXT, "start") if X(m) < 560 else text(X(m) - 6, yy + 14, f"{k + 1}: m={m}", 12, TEXT, "end")
    b += text(380, y + len(steps) * 34 + 14, f"загадано {secret}: после {len(steps)} вопросов L = {l}, R = {r} — соседи, ответ R", 14, YELLOW)
    return figure(svg(760, y + len(steps) * 34 + 36, b), "Жёлтая черта — вопрос; закрашен отрезок, где ответ ещё возможен. $\\lceil\\log_2 100\\rceil=7$ вопросов.")


FIGS = {"guess": fig_guess}


def algo_lb(a=(1, 3, 5, 10, 12, 13, 15, 19), x=14):
    frames = []; n = len(a); l, r = -1, n
    def draw(note, m=None):
        s = text(24, 22, f"ищем первое a[i] ≥ {x}", 13, MUTED, "start")
        for i, v in enumerate(a):
            col = None
            if i <= l: col = RED
            elif i >= r: col = GREEN
            if i == m: col = YELLOW
            s += cell(40 + i * 56, 40, 52, 34, str(v), col, 15) + text(40 + i * 56 + 26, 92, str(i), 11, MUTED)
        s += text(24, 124, f"L = {l}   R = {r}" + ("" if r < n else "  (R = n: «фиктивная ∞»)"), 14, TEXT, "start")
        s += text(24, 150, note, 13, MUTED, "start")
        return s
    frames.append({"svg": draw("L не подходит, R подходит (фиктивные)"), "msg": "L = −1 (до начала) точно не подходит, R = n (после конца) точно подходит."})
    while l + 1 < r:
        m = (l + r) // 2
        frames.append({"svg": draw(f"m = {m}: a[m] = {a[m]}", m), "msg": f"Смотрим середину m = {m}: a[m] = {a[m]}."})
        if a[m] < x: l = m; msg = f"{a[m]} < {x}: не подходит → L = {m}."
        else: r = m; msg = f"{a[m]} ≥ {x}: подходит → R = {m}."
        frames.append({"svg": draw(msg), "msg": msg})
    frames.append({"svg": draw(f"L+1 = R → ответ: позиция {r}, значение {a[r] if r < n else '—'}"), "msg": f"Границы соседние. Ответ: R = {r}" + (f", a[R] = {a[r]}." if r < n else " (нет такого).")})
    return {"title": "Бинпоиск: первое число ≥ x", "vb": "0 0 500 170", "frames": frames}


def algo_real(f=lambda x: x * x + math.sqrt(x) - 20, l=0.0, r=100.0, steps=12):
    frames = []
    W = 460; X = lambda v: 30 + (v - 0) / 100 * W
    def draw(l, r, m, note):
        s = line(30, 80, 30 + W, 80, AXIS, 2)
        s += f'<rect x="{X(l)}" y="62" width="{max(2, X(r) - X(l))}" height="36" rx="4" fill="{SOFT[BLUE]}" stroke="{BLUE}" stroke-width="2"/>'
        s += line(X(l), 52, X(l), 108, RED, 3) + line(X(r), 52, X(r), 108, GREEN, 3)
        if m is not None: s += line(X(m), 52, X(m), 108, YELLOW, 3)
        s += text(24, 22, f"L = {l:.6g} (f<0)    R = {r:.6g} (f>0)", 13, TEXT, "start")
        s += text(24, 132, note, 13, MUTED, "start")
        return s
    frames.append({"svg": draw(l, r, None, "f(0) = −20 < 0, f(100) > 0"), "msg": "Начальные границы: f(0) < 0, f(100) > 0 — корень внутри."})
    for it in range(steps):
        m = (l + r) / 2
        v = f(m)
        frames.append({"svg": draw(l, r, m, f"m = {m:.6g}, f(m) = {v:.4g}"), "msg": f"Итерация {it + 1}: m = {m:.6g}, f(m) = {v:.4g}."})
        if v > 0: r = m
        else: l = m
        frames.append({"svg": draw(l, r, None, "f(m) > 0 → R = m" if v > 0 else "f(m) < 0 → L = m"), "msg": ("f(m) > 0 — подходит: R = m." if v > 0 else "f(m) ≤ 0 — не подходит: L = m.")})
    return {"title": "Вещественный бинпоиск: x² + √x − 20 = 0", "vb": "0 0 520 150", "frames": frames}


def algos_js():
    data = {"lb": algo_lb(), "real": algo_real()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
