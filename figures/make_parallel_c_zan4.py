"""Собирает src/parallel-c/parallel-c-zan4-razbor.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_c_zan4 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Разбор контестов", "parallel": "parallel-c", "pname": "Параллель C", "porder": 1, "n": 4,
        "video": "video-232575486_456239903",
        "subtitle": "Разбор задач трёх контестов: контейнеры (стек, очередь, дек), линейные алгоритмы (префиксные суммы, два указателя) и бинарный поиск (по ответу, вещественный, вложенный).",
        "chips": ["Разбор трёх контестов", "≈ 3 ч 15 мин", "Псевдокод"]}
body = "".join((pathlib.Path(__file__).parent / "text" / f"parallel_c_zan4_{i}.html").read_text() for i in (1, 2, 3))
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-c"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-c-zan4-razbor.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-c-zan4-razbor.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
