"""Иллюстрации и плееры для «Занятие 1. Параллель C — Контейнеры»."""
import json
from kit import *


def stack_col(x, base, vals, w=56, h=34, colors=None, title=None):
    out = line(x - 6, base - 6 * h - 10, x - 6, base, AXIS, 2) + line(x + w + 6, base - 6 * h - 10, x + w + 6, base, AXIS, 2) + line(x - 6, base, x + w + 6, base, AXIS, 2)
    for i, v in enumerate(vals):
        c = (colors or {}).get(i)
        out += cell(x, base - (i + 1) * h, w, h - 3, str(v), c, 15)
    if title: out += text(x + w / 2, base + 22, title, 12, MUTED)
    return out


def fig_stack():
    b = text(380, 24, "Стек: доступ только к верхнему элементу", 15)
    b += stack_col(120, 250, [5, 4, 6], colors={2: YELLOW}, title="стек")
    b += line(260, 90, 260, 140, GREEN, 3, arrow=True) + text(330, 112, "push(x) — сверху", 13, GREEN)
    b += line(260, 205, 260, 155, RED, 3, arrow=True) + text(330, 192, "pop() — сверху", 13, RED)
    b += text(330, 232, "top() — смотрим, не удаляя", 13, YELLOW)
    b += text(560, 120, "LIFO", 24, BLUE, weight="700") + text(560, 148, "последним пришёл —", 13, MUTED) + text(560, 166, "первым вышел", 13, MUTED)
    return figure(svg(760, 276, b), "Стопка блинов или тарелок: класть и брать можно только сверху.")


def fig_amort():
    b = text(380, 24, "push_back: удвоение вместимости, редкие дорогие операции", 15)
    n = 17; base = 200
    for i in range(n):
        h = 14
        if i in (1, 2, 4, 8, 16): h = 14 + {1: 6, 2: 10, 4: 18, 8: 34, 16: 66}[i]
        col = RED if i in (1, 2, 4, 8, 16) else BLUE
        b += f'<rect x="{40 + i * 40}" y="{base - h}" width="32" height="{h}" fill="{SOFT[col]}" stroke="{col}" stroke-width="2"/>' + text(40 + i * 40 + 16, base + 16, str(i + 1), 11, MUTED)
    b += text(380, 238, "номер операции", 12, MUTED)
    b += text(380, 262, "копирования при размерах 1, 2, 4, 8, 16, …: 1 + 2 + 4 + … + 2ᵏ < 2n", 14, YELLOW)
    return figure(svg(760, 284, b), "Высота столбика — стоимость операции. Красные редкие, и их сумма не больше $2n$: амортизированно $O(1)$.")


def fig_minstack():
    b = text(380, 24, "Стек с минимумом: два стека, на каждой глубине — минимум до неё", 15)
    vals = [5, 4, 6, 3]; mins = [5, 4, 4, 3]
    b += stack_col(150, 260, vals, colors={3: YELLOW}, title="основной стек")
    b += stack_col(400, 260, mins, colors={3: GREEN}, title="стек минимумов")
    for i in range(4):
        y = 260 - (i + 1) * 34 + 15
        b += line(212, y, 394, y, EDGE, 1.5, dash="4 4")
    b += text(600, 100, "push(x): m = min(x, верх мин.)", 13, TEXT, "start")
    b += text(600, 126, "pop(): убрать из обоих", 13, TEXT, "start")
    b += text(600, 152, "min(): верх стека минимумов", 13, GREEN, "start")
    b += text(600, 178, "всё за O(1)", 13, YELLOW, "start")
    return figure(svg(760, 292, b), "После <code>push 5, 4, 6, 3</code> минимум равен 3; после <code>pop</code> — снова 4: он уже лежит под вершиной.")


def fig_deque():
    b = text(380, 24, "Дек: четыре быстрые операции по краям + доступ по индексу", 15)
    for i, v in enumerate([7, 2, 9, 4, 6]):
        b += cell(200 + i * 70, 90, 64, 44, str(v), BLUE if i in (0, 4) else None, 17) + text(232 + i * 70, 154, f"d[{i}]", 12, MUTED)
    b += line(180, 80, 180, 60, GREEN, 3, arrow=True)
    b += text(110, 56, "push_front", 13, GREEN) + text(110, 76, "pop_front", 13, RED)
    b += line(570, 80, 570, 60, GREEN, 3, arrow=True)
    b += text(640, 56, "push_back", 13, GREEN) + text(640, 76, "pop_back", 13, RED)
    b += text(380, 200, "front() = d[0],  back() = d[size−1],  d[i] — за O(1)", 14, YELLOW)
    b += text(380, 224, "вставка в середину всё ещё дорогая", 13, MUTED)
    return figure(svg(760, 246, b), "Дек умеет всё, что умеют стек и очередь; платит за это большей константой, чем вектор.")


FIGS = {"stack": fig_stack, "amort": fig_amort, "minstack": fig_minstack, "deque": fig_deque}


# ---------------------------------------------------------------- плеер: скобки
def algo_brackets(s="[()][(())]("):
    frames = []; st = []
    def draw(i, note, bad=None):
        o = text(24, 22, "строка:", 13, MUTED, "start")
        for k, ch in enumerate(s):
            col = RED if bad == k else (YELLOW if k == i else (GREEN if k < i else None))
            o += cell(100 + k * 46, 8, 40, 34, ch, col, 17)
        o += stack_col(80, 246, st, w=50, h=30, title="стек открытых")
        o += text(300, 200, note, 14, MUTED, "start")
        return o
    opens = "([{"; pair = {")": "(", "]": "[", "}": "{"}
    verdict = None
    for i, ch in enumerate(s):
        if ch in opens:
            st.append(ch)
            frames.append({"svg": draw(i, f"«{ch}» открывающая — в стек"), "msg": f"Символ {i}: «{ch}» — кладём в стек открытых."})
        else:
            if not st:
                frames.append({"svg": draw(i, "стек пуст — закрывать нечего", i), "msg": f"Символ {i}: «{ch}», а стек пуст — не ПСП."}); verdict = "нет"; break
            if pair[ch] != st[-1]:
                frames.append({"svg": draw(i, f"«{ch}» не подходит к «{st[-1]}»", i), "msg": f"Символ {i}: «{ch}» не закрывает «{st[-1]}» — не ПСП."}); verdict = "нет"; break
            st.pop()
            frames.append({"svg": draw(i, f"«{ch}» закрыла «{pair[ch]}» — снимаем"), "msg": f"Символ {i}: «{ch}» закрывает верх стека — снимаем его."})
    if verdict is None:
        ok = not st
        frames.append({"svg": draw(len(s), "строка кончилась; стек " + ("пуст → ПСП" if ok else "не пуст → не ПСП")), "msg": "Конец строки: " + ("стек пуст, это ПСП." if ok else f"в стеке осталось {len(st)} незакрытых — не ПСП.")})
    return {"title": "Проверка ПСП стеком", "vb": "0 0 560 276", "frames": frames}


# ---------------------------------------------------------------- плеер: очередь на двух стеках
def algo_queue2(ops=(("push", 5), ("push", 4), ("push", 3), ("front", 0), ("push", 2), ("push", 1), ("front", 0), ("pop", 0), ("pop", 0), ("pop", 0), ("front", 0))):
    frames = []; inn = []; out = []
    def draw(note, hl=None):
        o = stack_col(70, 250, inn, w=50, h=30, title="in (сюда push)")
        o += stack_col(330, 250, out, w=50, h=30, colors={len(out) - 1: YELLOW} if out else None, title="out (отсюда front/pop)")
        o += text(24, 22, note, 14, MUTED, "start")
        o += line(160, 130, 290, 130, ORANGE, 2, arrow=True) + text(225, 120, "balance", 12, ORANGE)
        return o
    def bal():
        while inn:
            out.append(inn.pop())
            frames.append({"svg": draw("balance: перекладываем верх in в out"), "msg": f"balance: переложили {out[-1]} из in в out."})
    for op, x in ops:
        if op == "push":
            inn.append(x); frames.append({"svg": draw(f"push({x}) → в in"), "msg": f"push({x}): кладём в in."})
        else:
            if not out:
                if inn: frames.append({"svg": draw("out пуст → нужна перебалансировка"), "msg": "out пуст, а нужен самый старый — перекладываем всё из in."})
                bal()
            if not out: continue
            if op == "front": frames.append({"svg": draw(f"front() = {out[-1]} (верх out)"), "msg": f"front() = {out[-1]}: верх out — самый старый элемент."})
            else:
                v = out.pop(); frames.append({"svg": draw(f"pop() убрал {v}"), "msg": f"pop(): убрали {v} с верха out."})
    return {"title": "Очередь на двух стеках", "vb": "0 0 520 280", "frames": frames}


def algos_js():
    data = {"brackets": algo_brackets(), "queue2": algo_queue2()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
