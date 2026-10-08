"""Собирает src/parallel-x/parallel-x-zan1-primenenie-do.src.html."""
import json, re, pathlib
from parallel_x_zan1 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Применение дерева отрезков", "parallel": "parallel-x", "pname": "Параллель X", "porder": 1, "n": 1,
        "video": "video-232575486_456239857",
        "subtitle": "Организация параллели X; подсчёт на отрезке, персистентное дерево отрезков, число различных, MEX, k-я статистика на отрезке и на пути, disjoint sparse table, дерево отрезков без push.",
        "chips": ["Лекция", "≈ 1 ч 45 мин", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_x_zan1_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-x"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-x-zan1-primenenie-do.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-x-zan1-primenenie-do.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
