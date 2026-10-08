"""Собирает src/parallel-b/parallel-b-zan5-derevo-otrezkov.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_b_zan5 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Дерево отрезков и разбор динамики", "parallel": "parallel-b", "pname": "Параллель B", "porder": 3, "n": 5,
        "video": "video-232575486_456239902",
        "subtitle": "Разбор контеста по динамике (деревья, строки, отрезки, подарки по циклам) и лекция про дерево отрезков с массовыми операциями, деревья Фенвика, неявные деревья и приём с потенциалом.",
        "chips": ["Разбор контеста + лекция", "≈ 3 ч 40 мин", "Язык кода: C++ (в разборе — псевдокод)"]}
body = "".join((pathlib.Path(__file__).parent / "text" / f"parallel_b_zan5_{i}.html").read_text() for i in (1, 2))
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-b"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-b-zan5-derevo-otrezkov.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-b-zan5-derevo-otrezkov.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
