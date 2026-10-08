"""Собирает src/parallel-bs/parallel-bs-zan3-linejnye.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_bs_zan3 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Линейные алгоритмы", "parallel": "parallel-bs", "pname": "Параллель BS", "porder": 4, "n": 3,
        "video": "video-232575486_456239885",
        "subtitle": "Префиксные суммы и разностные массивы, сканирующая прямая, второй максимум, сдвиг на месте, ближайшие большие и меньшие элементы, гистограммы и дождевая вода.",
        "chips": ["Лекция + семинар", "≈ 5 ч", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_bs_zan3_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-bs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-bs-zan3-linejnye.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-bs-zan3-linejnye.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
