"""Собирает src/parallel-b/parallel-b-zan6-kratchajshie-puti.src.html."""
import json, re, pathlib, html
from parallel_b_zan6 import FIGS

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = pathlib.Path(__file__).parent
meta = {"title": "Кратчайшие пути", "parallel": "parallel-b", "pname": "Параллель B", "porder": 3, "n": 6,
        "video": None,
        "subtitle": "Разбор контеста по деревьям отрезков; BFS, Дейкстра с доказательством, 0-1 BFS и веса до K, Флойд, Форд–Беллман, отрицательные циклы, цикл минимального среднего веса, Дейкстра на неявном графе с деревом отрезков.",
        "chips": ["Лекция", "≈ 4 ч 59 мин", "Язык кода: C++"],
        "youtube": "https://youtu.be/h2odhLX7xQw"}
FILES = {"paths": HERE / "code" / "b_zan6_paths.cpp", "ford": HERE / "code" / "b_zan6_ford.cpp"}


def code_block(fname, name):
    lines = FILES[fname].read_text().split("\n")
    idx = next(i for i, l in enumerate(lines) if re.match(rf"^(?:[\w:<>,\s]+?[\s\*&]){re.escape(name)}\s*[\(\{{]", l) or l.startswith(f"struct {name}"))
    start = idx - 1 if idx > 0 and lines[idx - 1].startswith("//") else idx
    end = idx
    if not lines[idx].rstrip().endswith(("};", "}")) or lines[idx].count("{") != lines[idx].count("}"):
        while lines[end] not in ("}", "};"):
            end += 1
    txt = "\n".join(lines[start:end + 1])
    return '<pre class="cpp">' + html.escape(txt, quote=False) + "</pre>"


t = HERE / "text"
body = "\n".join((t / f"parallel_b_zan6_{i}.html").read_text() for i in (1, 2, 3))
body = re.sub(r'(<ts t=")(\d+:\d\d)("\s*/>)', r'\g<1>0:\2\3', body)
body = re.sub(r'(data-tc=")(\d+:\d\d)(")', r'\g<1>0:\2\3', body)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
body = re.sub(r"<!--CODE:(\w+):(\w+)-->", lambda m: code_block(m.group(1), m.group(2)), body)
d = ROOT / "src" / "parallel-b"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-b-zan6-kratchajshie-puti.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
print("ok", len(body) // 1024, "KB")
