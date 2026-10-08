"""Собирает src/parallel-bs/parallel-bs-zan1-stl-zhadniki.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_bs_zan1 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "STL и жадные алгоритмы", "parallel": "parallel-bs", "pname": "Параллель BS", "porder": 4, "n": 1,
        "video": "video-232575486_456239856",
        "subtitle": "Организация курса; вектор, итераторы, сортировка и компараторы, lower_bound, сжатие координат, set, map, multiset, стек, дек, очередь, быстрый ввод-вывод; семинар по жадным алгоритмам.",
        "chips": ["Лекция + семинар", "≈ 4 ч 28 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_bs_zan1_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-bs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-bs-zan1-stl-zhadniki.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-bs-zan1-stl-zhadniki.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
