"""Собирает src/parallel-bs/parallel-bs-zan2-binpoisk-dva-ukazatelya.src.html из текстов (figures/text) и иллюстраций."""
import json, re, pathlib
from parallel_bs_zan2 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Бинпоиск и два указателя", "parallel": "parallel-bs", "pname": "Параллель BS", "porder": 4, "n": 2,
        "video": "video-232575486_456239872",
        "subtitle": "Бинарный поиск по массиву, по функции, по ответу и по вещественным числам; тернарный поиск; метод двух указателей и его доказательство; разбор задач контеста.",
        "chips": ["Лекция + разбор", "≈ 4 ч 41 мин", "Язык кода: C++"]}
import html
src = (pathlib.Path(__file__).parent / "code" / "parallel_bs_zan2.cpp").read_text()
parts = re.split(r"^//---- (\w+)\n", src, flags=re.M)
code = {parts[i]: parts[i + 1].rstrip("\n") for i in range(1, len(parts), 2)}
body = (pathlib.Path(__file__).parent / "text" / "parallel_bs_zan2_1.html").read_text()
body = re.sub(r"<!--CPP:(\w+)-->", lambda m: html.escape(code[m.group(1)], quote=False), body)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-bs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-bs-zan2-binpoisk-dva-ukazatelya.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-bs-zan2-binpoisk-dva-ukazatelya.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
