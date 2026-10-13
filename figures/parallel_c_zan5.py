"""Иллюстрации для «Занятие 5. Параллель C — STL: ввод-вывод, итераторы, компараторы, контейнеры»."""
from kit import *


def fig_buffer():
    """'\\n' копит текст в буфере, endl ещё и сбрасывает буфер."""
    b = text(380, 26, "Куда попадает вывод: буфер и flush", 15)
    for lane, (y, title, col) in enumerate([(52, "'\\n' — только перенос строки", BLUE), (170, "endl = '\\n' + flush", YELLOW)]):
        b += text(40, y + 4, title, 14, col, "start", "700")
        yy = y + 18
        b += cell(40, yy, 150, 60, "программа", None, 15)
        b += cell(300, yy, 170, 60, "буфер", BLUE if lane == 0 else YELLOW, 15, sub="копится порциями")
        b += cell(580, yy, 140, 60, "экран / файл", None, 15)
        b += line(192, yy + 30, 298, yy + 30, MUTED, 2, arrow=True)
        b += text(245, yy + 20, "cout <<", 12, MUTED, mono=True)
        if lane == 0:
            b += line(472, yy + 30, 578, yy + 30, MUTED, 2, dash="6 5", arrow=True)
            b += text(525, yy + 20, "потом", 12, MUTED)
            b += text(380, yy + 84, "быстро, но вывод может «застрять» в буфере", 12, MUTED)
        else:
            b += line(472, yy + 30, 578, yy + 30, YELLOW, 3, arrow=True)
            b += text(525, yy + 20, "сразу", 12, YELLOW)
            b += text(380, yy + 84, "гарантированно напечатано, но заметно медленнее", 12, MUTED)
    return figure(svg(760, 300, b), "Буфер ускоряет вывод. Без явного сброса программа не обязана печатать всё немедленно — для интерактивных задач это критично.")


def fig_set_iter():
    b = text(380, 26, "Итераторы set: [begin, end) — полуинтервал", 15)
    xs = [150, 270, 390]; y = 80
    for x, v in zip(xs, ("1", "2", "3")):
        b += cell(x, y, 100, 56, v, BLUE, 20)
    b += f'<rect x="510" y="{y}" width="100" height="56" rx="6" fill="none" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 5"/>'
    b += text(560, y + 34, "пусто", 13, MUTED)
    # скобка полуинтервала
    b += line(150, 62, 510, 62, YELLOW, 2)
    b += text(150, 56, "[", 18, YELLOW) + text(510, 56, ")", 18, YELLOW)
    b += text(330, 52, "элементы множества", 12, YELLOW)
    # подписи под ячейками
    b += line(200, 144, 200, 168, GREEN, 3, arrow=True) + text(200, 190, "begin()", 14, GREEN, mono=True) + text(200, 208, "минимум", 12, MUTED)
    b += line(440, 144, 440, 168, ORANGE, 3, arrow=True) + text(440, 190, "prev(end())", 14, ORANGE, mono=True) + text(440, 208, "= end() − 1, максимум", 12, MUTED)
    b += line(560, 144, 560, 168, RED, 3, arrow=True) + text(560, 190, "end()", 14, RED, mono=True) + text(560, 208, "за последним", 12, MUTED)
    b += text(380, 250, "*end() разыменовывать нельзя — там нет элемента; *prev(end()) даёт 3", 13, TEXT)
    return figure(svg(760, 270, b), "end() указывает не на последний элемент, а на «позицию после последнего». Чтобы получить максимум, нужно сделать шаг назад.")


def fig_unique():
    b = text(380, 26, "sort → unique → resize на примере 5 2 1 4 3 2", 15)
    W = 70; X0 = 100

    def row(y, vals, colors, label, idx=True):
        s = text(24, y + 32, label, 13, MUTED, "start")
        for i, (v, c) in enumerate(zip(vals, colors)):
            s += cell(X0 + 90 + i * W, y, W - 6, 44, v, c, 17)
            if idx: s += text(X0 + 90 + i * W + (W - 6) / 2, y + 62, str(i), 11, MUTED)
        return s
    b += row(48, ["1", "2", "2", "3", "4", "5"], [GREEN, GREEN, RED, GREEN, GREEN, GREEN], "после sort")
    b += row(140, ["1", "2", "3", "4", "5", "?"], [GREEN, GREEN, GREEN, GREEN, GREEN, None], "после unique")
    # указатель, который вернул unique
    px = X0 + 90 + 5 * W + (W - 6) / 2
    b += line(px, 214, px, 192, YELLOW, 3, arrow=True)
    b += text(px, 232, "unique вернул сюда", 12, YELLOW)
    b += text(px, 248, "(новый конец)", 12, YELLOW)
    b += row(262, ["1", "2", "3", "4", "5"], [GREEN] * 5, "после resize", idx=False)
    b += text(380, 340, "resize(unique(a.begin(), a.end()) − a.begin()): размер = 5", 13, TEXT)
    return figure(svg(760, 360, b), "Красная — лишняя копия. Хвост после unique содержит неопределённое значение («?»), поэтому его обязательно отрезают resize.")


def fig_reverse():
    b = text(380, 26, "Прямые и обратные итераторы одного массива", 15)
    W = 100; X0 = 130; y = 112
    for i, v in enumerate(("a[0]", "a[1]", "a[2]", "a[3]", "a[4]")):
        b += cell(X0 + i * W, y, W - 8, 52, v, BLUE, 16)
    # прямые, сверху
    b += line(X0 + 46, y - 14, X0 + 46, y - 2, GREEN, 3, arrow=True) + text(X0 + 46, y - 24, "begin()", 14, GREEN, mono=True)
    ex = X0 + 5 * W - 8 + 4
    b += f'<line x1="{ex}" y1="{y - 8}" x2="{ex}" y2="{y + 60}" stroke="{RED}" stroke-width="3" stroke-dasharray="5 4"/>' + text(ex, y - 24, "end()", 14, RED, mono=True)
    # обратные, снизу
    lx = X0 - 4
    b += f'<line x1="{lx}" y1="{y - 8}" x2="{lx}" y2="{y + 60}" stroke="{PURPLE}" stroke-width="3" stroke-dasharray="5 4"/>' + text(lx, y + 82, "rend()", 14, PURPLE, mono=True)
    b += line(X0 + 4 * W + 46, y + 70, X0 + 4 * W + 46, y + 58, ORANGE, 3, arrow=True) + text(X0 + 4 * W + 46, y + 86, "rbegin()", 14, ORANGE, mono=True)
    b += line(X0 + 4 * W + 40, y + 130, X0 + 14, y + 130, ORANGE, 2, arrow=True)
    b += text(380, y + 152, "rbegin → rend: проход справа налево", 12, ORANGE)
    return figure(svg(760, 300, b), "sort(a.rbegin(), a.rend()) расставляет элементы так, что при взгляде справа налево они идут по возрастанию — то есть по убыванию слева направо.")


FIGS = {"buffer": fig_buffer, "setiter": fig_set_iter, "unique": fig_unique, "reverse": fig_reverse}
