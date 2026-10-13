"""Собирает src/parallel-xs/parallel-xs-zan2-sqrt-dekompoziciya.src.html."""
import json, re, pathlib, html
from parallel_xs_zan2 import FIGS

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
meta = {"title": "SQRT-декомпозиция", "parallel": "parallel-xs", "pname": "Параллель XS", "porder": 2, "n": 2,
        "video": None,
        "subtitle": "Разбор контеста по деревьям (эйлеров обход, сжатое дерево, стек максимумов); корневая декомпозиция и алгоритм Мо (в том числе на дереве и с изменениями); тяжёлые и лёгкие вершины; корневая по запросам: связность, ближайшая чёрная клетка, остов; перебор значений floor(x / i).",
        "chips": ["Лекция + разбор + семинар", "≈ 4 ч 59 мин", "Язык кода: C++"],
        "youtube": "https://youtu.be/1WZ6chwdyFg"}
FILES = {"sq": HERE / "code" / "xs_zan2_sqrt.cpp"}


def code_block(fname, name):
    lines = FILES[fname].read_text().split("\n")
    idx = next(i for i, l in enumerate(lines) if re.match(rf"^(?:[\w:<>,\s]+?[\s\*&]){re.escape(name)}\s*[\(\{{]", l) or l.startswith(f"struct {name}"))
    start = idx
    while start > 0 and lines[start - 1].startswith("//") and not lines[start - 1].startswith("// ---"):
        start -= 1
    end = idx
    if not lines[idx].rstrip().endswith(("};", "}")) or lines[idx].count("{") != lines[idx].count("}"):
        while lines[end] not in ("}", "};"):
            end += 1
    txt = "\n".join(lines[start:end + 1])
    return '<pre class="cpp">' + html.escape(txt, quote=False) + "</pre>"


t = HERE / "text"
body = "\n".join((t / f"parallel_xs_zan2_{i}.html").read_text() for i in (1, 2, 3))
body = re.sub(r'(<ts t=")(\d+:\d\d)("\s*/>)', r'\g<1>0:\2\3', body)
body = re.sub(r'(data-tc=")(\d+:\d\d)(")', r'\g<1>0:\2\3', body)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
body = re.sub(r"<!--CODE:(\w+):(\w+)-->", lambda m: code_block(m.group(1), m.group(2)), body)
d = ROOT / "src" / "parallel-xs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-xs-zan2-sqrt-dekompoziciya.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
print("ok", len(body) // 1024, "KB")
