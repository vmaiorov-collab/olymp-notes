"""Собирает src/parallel-x/parallel-x-zan3-potoki.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_x_zan3 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Введение в потоки", "parallel": "parallel-x", "pname": "Параллель X", "porder": 1, "n": 3,
        "video": "video-232575486_456239901",
        "subtitle": "Разбор задач на суффиксный массив и лекция про потоки: максимальный поток и минимальный разрез, алгоритмы Форда—Фалкерсона, Эдмонса—Карпа и Диница, паросочетания, гаджеты для разрезов.",
        "chips": ["Разбор + лекция", "≈ 2 ч 40 мин", "Язык кода: C++ (в разборе — псевдокод)"]}
body = "".join((pathlib.Path(__file__).parent / "text" / f"parallel_x_zan3_{i}.html").read_text() for i in (1, 2))
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-x"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-x-zan3-potoki.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-x-zan3-potoki.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
