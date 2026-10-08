"""Собирает src/parallel-c/parallel-c-zan3-binarnyj-poisk.src.html."""
import json, re, pathlib
from parallel_c_zan3 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Бинарный поиск", "parallel": "parallel-c", "pname": "Параллель C", "porder": 5, "n": 3,
        "video": "video-232575486_456239888",
        "subtitle": "Игра «угадай число» и логарифмическая асимптотика, инвариант «L не подходит, R подходит», lower_bound и upper_bound, вещественный бинпоиск, бинпоиск по ответу.",
        "chips": ["Лекция", "≈ 2 ч 40 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_c_zan3_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-c"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-c-zan3-binarnyj-poisk.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-c-zan3-binarnyj-poisk.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
