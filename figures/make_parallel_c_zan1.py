"""Собирает src/parallel-c/parallel-c-zan1-kontejnery.src.html."""
import json, re, pathlib
from parallel_c_zan1 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Контейнеры", "parallel": "parallel-c", "pname": "Параллель C", "porder": 5, "n": 1,
        "video": "video-232575486_456239861",
        "subtitle": "Организация курса и оценка, повторение асимптотики, стек, очередь и дек; стек и очередь с минимумом, проверка скобочной последовательности, постфиксная запись.",
        "chips": ["Лекция", "≈ 2 ч 10 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_c_zan1_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-c"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-c-zan1-kontejnery.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-c-zan1-kontejnery.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
