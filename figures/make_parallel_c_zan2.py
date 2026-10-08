"""Собирает src/parallel-c/parallel-c-zan2-linejnye.src.html."""
import json, re, pathlib
from parallel_c_zan2 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Линейные алгоритмы", "parallel": "parallel-c", "pname": "Параллель C", "porder": 5, "n": 2,
        "video": "video-232575486_456239863",
        "subtitle": "Префиксные суммы (одномерные и двумерные), максимальный подотрезок, разностный массив и метод двух указателей: общие элементы, слияние, пары точек.",
        "chips": ["Лекция", "≈ 2 ч 30 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_c_zan2_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-c"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-c-zan2-linejnye.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-c-zan2-linejnye.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
