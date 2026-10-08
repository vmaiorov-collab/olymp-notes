"""Собирает src/parallel-x/parallel-x-zan2-teoriya-chisel.src.html."""
import json, re, pathlib
from parallel_x_zan2 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Теория чисел", "parallel": "parallel-x", "pname": "Параллель X", "porder": 1, "n": 2,
        "video": "video-232575486_456239867",
        "subtitle": "Разбор контеста по дереву отрезков; алгоритм Евклида, дерево Штерна—Броко, геометрия решёток, рациональная реконструкция, floor sum, решёта, мультипликативные функции, НОД-свёртки.",
        "chips": ["Разбор + лекция", "≈ 4 ч 08 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_x_zan2_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-x"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-x-zan2-teoriya-chisel.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-x-zan2-teoriya-chisel.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
