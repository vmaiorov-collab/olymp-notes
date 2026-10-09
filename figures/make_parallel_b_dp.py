"""Собирает src/parallel-b/parallel-b-zan3-dinamicheskoe-programmirovanie-1.src.html."""
import html, json, re, pathlib
from parallel_b_dp import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Динамическое программирование 1", "parallel": "parallel-b", "pname": "Параллель B", "porder": 3, "n": 3,
        "video": "video-232575486_456239887",
        "subtitle": "Разбор контеста по DFS, обзор приёмов динамики (подотрезки, поддеревья, комбинаторные ДП, экономия памяти) и семинар: НВП, рюкзак на bitset, подотрезки, переподвешивание, динамика по цифрам, телефоны.",
        "chips": ["Разбор + лекция + семинар", "≈ 5 ч", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_b_dp_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
body = re.sub(r"<!--ALGO:(\w+)-->", lambda m: f'<div class="algo" data-frames="{m.group(1)}"></div>', body)
body = re.sub(r"<!--CPP:(\w+)-->", lambda m: html.escape((pathlib.Path(__file__).parent / "code" / (m.group(1) + ".cpp")).read_text().strip("\n"), quote=False), body)
d = ROOT / "src" / "parallel-b"; d.mkdir(parents=True, exist_ok=True)
name = "parallel-b-zan3-dinamicheskoe-programmirovanie-1"
(d / f"{name}.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / f"{name}.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
