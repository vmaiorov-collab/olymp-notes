"""Иллюстрации и плееры для «Занятие 4. Параллель C — Разбор контестов».
Кадры плееров считаются теми же алгоритмами, что проверены случайными тестами против перебора."""
import json
from kit import *


# ---------------------------------------------------------------- вспомогательное
def stack_col(x, y_bottom, items, w=96, h=34, title="", color=None, hl_top=False):
    """Стек, дно снизу. items — список подписей снизу вверх."""
    out = text(x + w / 2, y_bottom + 22, title, 13, MUTED)
    out += line(x - 8, y_bottom, x + w + 8, y_bottom, AXIS, 2)
    for i, lab in enumerate(items):
        y = y_bottom - (i + 1) * (h + 4)
        out += cell(x, y, w, h, lab, (color if (color and (not hl_top or i == len(items) - 1)) else None), 14)
    return out


# ---------------------------------------------------------------- 1.2 очередь на двух стеках
def fig_two_stacks():
    b = text(380, 28, "Очередь = два стека; в каждой ячейке пара (число, минимум под ним)", 15, TEXT)
    b += stack_col(70, 260, ["(4, 4)", "(2, 2)", "(5, 2)"], title="вход — сюда приходят", color=BLUE, hl_top=True)
    b += text(118, 40 + 20, "", 1)
    b += stack_col(500, 260, ["(5, 5)", "(2, 2)", "(4, 2)"], title="выход — отсюда уходят", color=GREEN, hl_top=True)
    b += line(210, 150, 480, 150, YELLOW, 3, arrow=True)
    b += text(345, 134, "если выход пуст:", 13, YELLOW)
    b += text(345, 172, "перекладываем всё сверху вниз", 13, YELLOW)
    b += text(345, 215, "первым пришёл — окажется на вершине", 12, MUTED)
    b += text(345, 290, "минимум очереди = min(минимум входа, минимум выхода)", 14, TEXT)
    return figure(svg(700, 310, b), "Слева — стек тех, кто пришёл (4, затем 2, затем 5). Когда нужно удалить первого, а выходной стек пуст, всё перекладывается в выходной: вершиной становится 4 — самый ранний.")


# ---------------------------------------------------------------- 1.3 шарики
BALLS = [1, 2, 2, 3, 3, 3, 3, 2, 1, 1]


def balls_groups(a):
    g = []
    for x in a:
        if g and g[-1][0] == x: g[-1][1] += 1
        else: g.append([x, 1])
    return g


def fig_balls():
    g = balls_groups(BALLS); b = text(380, 26, "Шарики сворачиваем в группы (цвет × длина)", 15)
    x = 40
    for c in BALLS:
        b += circle(x + 14, 66, 14, "", COLORS[c]); x += 34
    b += line(380, 96, 380, 126, MUTED, 2, arrow=True)
    x = 70
    for c, k in g:
        w = 56 + 10 * k
        b += cell(x, 136, w, 58, f"{c} × {k}", COLORS[c], 16); x += w + 14
    b += text(380, 232, "лопаются группы, которые вместе с вершиной стека дают не меньше 3 шариков", 13, MUTED)
    return figure(svg(760, 252, b), "Десять шариков превращаются в пять групп. Дальше достаточно обрабатывать группы стеком.")


def algo_balls():
    g = balls_groups(BALLS); frames = []; st = []; burst = 0

    def draw(cur, note):
        s = text(380, 24, "группы слева направо; стек справа", 13, MUTED); x = 30
        for i, (c, k) in enumerate(g):
            w = 52 + 8 * k
            s += cell(x, 40, w, 46, f"{c}×{k}", YELLOW if i == cur else COLORS[c], 15); x += w + 10
        s += stack_col(560, 220, [f"{c}×{k}" for c, k in st], w=100, h=28, title="стек")
        s += text(150, 150, f"лопнуло шариков: {burst}", 18, ORANGE if burst else MUTED)
        return s
    for i, (c, k) in enumerate(g):
        frames.append({"svg": draw(i, ""), "msg": f"Берём группу {c}×{k}."})
        if st and st[-1][0] == c:
            st[-1][1] += k; k2 = st[-1][1]
            if k2 >= 3:
                burst += k2; st.pop(); msg = f"Совпала цветом с вершиной: теперь {k2} подряд, лопаем."
            else: msg = f"Совпала цветом с вершиной: теперь {k2}."
        elif k >= 3: burst += k; msg = f"Группа сама из {k} шариков — лопает."
        else: st.append([c, k]); msg = "Другой цвет — кладём на стек."
        frames.append({"svg": draw(i, ""), "msg": msg})
    frames.append({"svg": draw(-1, ""), "msg": f"Готово: лопнуло {burst} из {len(BALLS)}, осталось {len(BALLS) - burst}."})
    return {"title": "Шарики: стек групп", "vb": "0 0 760 250", "frames": frames}


# ---------------------------------------------------------------- 1.4 соседние буквы
def algo_letters(s="abebcab"):
    frames = []; st = []

    def draw(cur, note):
        out = text(380, 24, "строка: " + " ".join(s), 14, MUTED)
        out += text(380, 52, f"читаем: «{cur}»" if cur else "", 20, YELLOW)
        out += stack_col(330, 250, [c.upper() for c in st], w=100, h=34, title="стек", color=BLUE, hl_top=True)
        return out
    for ch in s:
        c = ch; frames.append({"svg": draw(c, ""), "msg": f"Читаем «{c}». Вершина стека: {st[-1] if st else 'пусто'}."})
        while st and abs(ord(st[-1]) - ord(c)) == 1:
            top = st.pop(); keep = min(top, c)
            frames.append({"svg": draw(c, ""), "msg": f"«{top}» и «{c}» — соседние буквы, остаётся меньшая «{keep}»."}); c = keep
        st.append(c)
        frames.append({"svg": draw("", ""), "msg": f"Кладём «{c}»."})
    frames.append({"svg": draw("", ""), "msg": "Ответ: " + "".join(st)})
    return {"title": "Соседние буквы: стек", "vb": "0 0 760 270", "frames": frames}


# ---------------------------------------------------------------- 1.5 парикмахерская
def fig_barber():
    ax = 70; scale = 3.4; t0 = 55
    X = lambda t: ax + (t - t0) * scale
    b = text(380, 24, "Парикмахерская: каждого стригут 20 минут; ушёл сразу, если людей перед ним больше терпимости", 14)
    b += line(ax, 150, 700, 150, AXIS, 2)
    for t in (60, 80, 100, 120, 140, 160):
        b += line(X(t), 146, X(t), 156, AXIS, 2) + text(X(t), 174, str(t), 12, MUTED)
    bars = [(60, 80, BLUE, "клиент 1"), (120, 140, BLUE, "клиент 2"), (140, 160, GREEN, "клиент 4")]
    for l, r, col, lab in bars:
        b += cell(X(l), 96, X(r) - X(l), 40, lab, col, 12)
    for t, lab, tol in ((60, "1", "терп. любая"), (120, "2", "терп. 0"), (121, "3", "терп. 0"), (122, "4", "терп. 3"), (123, "5", "терп. 0")):
        y = 60 if t in (121, 123) else 66
        b += line(X(t), y + 8, X(t), 96, MUTED, 1.5, dash="3 3")
    b += text(X(121), 52, "клиент 3 уходит сразу", 12, RED) + text(X(123) + 20, 40, "клиент 5 уходит сразу", 12, RED)
    b += text(X(122), 205, "клиент 4 приходит в 122, ждёт клиента 2 и выйдет в 140 + 20 = 160", 13, GREEN)
    return figure(svg(760, 225, b), "Моменты прихода (пунктир) и стрижка. Клиент 3 в 121 видит перед собой клиента 2 (терпимость 0) и уходит; клиент 4 готов ждать троих и выходит в 160.")


# ---------------------------------------------------------------- 1.6 тупик
def algo_trains(order=(4, 1, 3, 2)):
    frames = []; st = []; need = 1; out = []

    def draw(note=""):
        s = text(380, 24, "приходят: " + " ".join(map(str, order)), 14, MUTED)
        s += stack_col(330, 240, [str(x) for x in st], w=90, h=32, title="тупик (стек)", color=BLUE, hl_top=True)
        s += text(130, 100, f"ждём вагон: {need}", 20, YELLOW)
        s += text(130, 150, "на втором пути: " + (" ".join(map(str, out)) or "—"), 15, GREEN)
        return s
    for x in order:
        st.append(x); frames.append({"svg": draw(), "msg": f"Приехал вагон {x}, кладём в тупик."})
        while st and st[-1] == need:
            out.append(st.pop()); need += 1
            frames.append({"svg": draw(), "msg": f"Вершина — вагон {out[-1]}, он нужен: отправляем на второй путь."})
    frames.append({"svg": draw(), "msg": "Тупик пуст — отсортировать удалось." if not st else "В тупике остались вагоны — невозможно."})
    return {"title": "Тупик: 4 1 3 2", "vb": "0 0 760 260", "frames": frames}


# ---------------------------------------------------------------- 1.7 середина очереди
def fig_midqueue():
    b = text(380, 26, "Две половины-дека: левая (|L| = |R| или |R|+1) и правая", 15)
    x = 40
    for v in (1, 2, 3):
        b += cell(x, 60, 56, 42, str(v), BLUE, 16); x += 62
    b += text(130, 124, "L — левая половина", 13, MUTED)
    x = 440
    for v in (4, 5):
        b += cell(x, 60, 56, 42, str(v), GREEN, 16); x += 62
    b += text(500, 124, "R — правая половина", 13, MUTED)
    b += line(372, 50, 372, 112, YELLOW, 3, dash="5 4") + text(372, 44, "середина", 12, YELLOW, "middle")
    b += cell(300, 160, 56, 42, "6", ORANGE, 16) + line(328, 158, 392, 108, ORANGE, 2, arrow=True)
    b += text(250, 232, "вклиниться = положить в НАЧАЛО правой половины (push_front), потом выровнять размеры", 13, TEXT)
    b += text(250, 256, "уйти из начала — pop_front у L; прийти в конец — push_back у R", 13, TEXT)
    return figure(svg(760, 275, b), "Очередь 1 2 3 | 4 5. Новый участник 6 встаёт сразу за серединой — это начало правой половины.")


# ---------------------------------------------------------------- 1.8 жемчужины
def fig_pearls():
    a = [1, 2, 2, 1, 3, 3]; b = text(380, 26, "Жемчужины: k = 3 цвета, m = 2 (в группе разница позиций ≤ 2)", 15)
    for i, c in enumerate(a):
        x = 70 + i * 100
        b += circle(x, 80, 24, str(c), COLORS[c], 18) + text(x, 124, f"поз. {i}", 12, MUTED)
    b += line(70 + 2 * 100 - 30, 150, 70 + 4 * 100 + 30, 150, YELLOW, 4) + text(370, 176, "группа: позиции 2, 3, 4 — цвета 2, 1, 3", 14, YELLOW)
    b += text(380, 218, "для каждого цвета — своя очередь позиций; позиции, отстоящие больше чем на m от текущей, из очередей удаляем", 12, MUTED)
    b += text(380, 240, "когда все k очередей непусты — берём из каждой первую позицию и закрываем группу", 12, MUTED)
    return figure(svg(760, 258, b), "В группу попадает 2, 1, 3 (позиции 2–4). Группа 1, 2, 3 из позиций 0, 1, 4 запрещена: позиции 0 и 4 отстоят на 4 > 2.")


# ---------------------------------------------------------------- 2.8 прямоугольник
def fig_rect2d():
    n, m = 6, 7; cs = 52; ox, oy = 40, 50
    b = text(380, 26, "Прибавление на прямоугольнике: меняем только 4 клетки", 15)
    for i in range(n):
        for j in range(m):
            inside = 1 <= i <= 3 and 2 <= j <= 4
            b += cell(ox + j * cs, oy + i * cs, cs - 4, cs - 4, "", BLUE if inside else None, 12, rx=4)
    marks = [(1, 2, "+d", GREEN), (1, 5, "−d", RED), (4, 2, "−d", RED), (4, 5, "+d", GREEN)]
    for i, j, lab, col in marks:
        b += text(ox + j * cs + cs / 2 - 2, oy + i * cs + cs / 2 + 4, lab, 16, col, weight="700")
    b += text(560, 150, "затем два прохода:", 14, TEXT)
    b += text(560, 178, "1) по столбцам сверху вниз:", 13, MUTED) + text(560, 198, "t[i][j] += t[i-1][j]", 13, YELLOW, mono=True)
    b += text(560, 232, "2) по строкам слева направо:", 13, MUTED) + text(560, 252, "t[i][j] += t[i][j-1]", 13, YELLOW, mono=True)
    return figure(svg(760, 380, b), "Синий — прямоугольник запроса. Ставим +d в левый верхний угол, −d справа и снизу от прямоугольника, +d в правый нижний угол. Два прохода восстанавливают настоящие значения.")


# ---------------------------------------------------------------- 3.8 коровы
def fig_cows():
    xs = [2, 5, 7, 11, 15, 20]; sx = lambda v: 50 + (v - 2) * 36
    b = text(380, 26, "Коровы: стойла 2 5 7 11 15 20, нужно расставить 3, расстояние d = 9", 15)
    b += line(40, 110, 740, 110, AXIS, 2)
    for v in xs:
        chosen = v in (2, 11, 20)
        b += circle(sx(v), 110, 13, str(v), GREEN if chosen else None, 12)
    for a, c in ((2, 11), (11, 20)):
        b += line(sx(a), 74, sx(c), 74, YELLOW, 2) + text((sx(a) + sx(c)) / 2, 64, "9", 14, YELLOW)
    b += text(380, 170, "жадно: первое стойло занимаем, дальше — ближайшее, отстоящее не меньше чем на d", 13, MUTED)
    return figure(svg(760, 190, b), "Для d = 9 жадность ставит коров в 2, 11, 20 — три штуки. Для d = 10 уже не получится, значит ответ 9.")


# ---------------------------------------------------------------- 3.9 лист бумаги
def fig_paper():
    b = text(380, 26, "Лист: ширина W задана, высота H — неизвестна; разрез — любой", 15)
    b += cell(60, 50, 640, 180, "", None, 12, rx=8)
    b += line(330, 50, 330, 230, YELLOW, 3, dash="6 5") + text(330, 248, "разрез: левой части нужна ширина A, правой — B", 13, YELLOW)
    rows = [[3, 2, 4], [5, 2], [4, 3]]
    for r, words in enumerate(rows):
        x = 76
        for w in words:
            b += cell(x, 66 + r * 40, w * 18, 30, "", BLUE, 12, rx=4); x += w * 18 + 18
    rows2 = [[2, 3], [6], [2, 2, 2]]
    for r, words in enumerate(rows2):
        x = 350
        for w in words:
            b += cell(x, 66 + r * 40, w * 18, 30, "", GREEN, 12, rx=4); x += w * 18 + 18
    b += text(380, 274, "нужно: A + B ≤ W; каждую часть проверяем отдельным бинпоиском по ширине", 13, MUTED)
    return figure(svg(760, 292, b), "Слова записываются в строки через пробел, не помещающееся слово переносится целиком. Две колонки не зависят друг от друга, поэтому для высоты H ищем наименьшую ширину каждой.")


# ---------------------------------------------------------------- 3.10 пиццы
def fig_pizza():
    a = [3, 5, 2, 6, 4, 1, 3]; b = text(380, 26, "Участники идут навстречу и съедают по пицце за секунду", 15)
    for i, v in enumerate(a):
        x = 70 + i * 90
        b += cell(x - 24, 190 - v * 22, 48, v * 22, str(v), ORANGE, 14, rx=4) + text(x, 214, f"т.{i}", 12, MUTED)
    b += line(70, 236, 270, 236, GREEN, 3, arrow=True) + text(170, 256, "левый идёт вправо", 13, GREEN)
    b += line(610, 236, 410, 236, BLUE, 3, arrow=True) + text(510, 256, "правый идёт влево", 13, BLUE)
    b += text(380, 290, "разговор начинается, когда расстояние между ними стало ≤ k", 14, YELLOW)
    return figure(svg(760, 308, b), "Расстояние между участниками со временем только уменьшается, поэтому момент разговора ищем бинпоиском по времени.")


FIGS = {
    "two_stacks": fig_two_stacks, "balls": fig_balls, "barber": fig_barber, "midqueue": fig_midqueue,
    "pearls": fig_pearls, "rect2d": fig_rect2d, "cows": fig_cows, "paper": fig_paper, "pizza": fig_pizza,
}


def algos_js():
    data = {"balls": algo_balls(), "letters": algo_letters(), "trains": algo_trains()}
    return "window.ALGOS=window.ALGOS||{};\n" + "\n".join(
        f"window.ALGOS.{k}=function(){{return {json.dumps(v, ensure_ascii=False)}}};" for k, v in data.items())
