"""Собирает src/parallel-b/parallel-b-zan2-primeneniya-dfs.src.html."""
import html, json, re, pathlib
from parallel_b_dfs import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Применения DFS", "parallel": "parallel-b", "pname": "Параллель B", "porder": 3, "n": 2,
        "video": "video-232575486_456239871",
        "subtitle": "Разбор контеста по дереву отрезков и лекция по графам: мосты и точки сочленения, нечётные циклы, эйлеров цикл, топологическая сортировка, компоненты сильной связности, 2-SAT, круглоквадратное дерево.",
        "chips": ["Разбор + лекция", "≈ 5 ч", "Язык кода: C++"]}
body = (pathlib.Path(__file__).parent / "text" / "parallel_b_dfs_1.html").read_text()
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
body = re.sub(r"<!--ALGO:(\w+)-->", lambda m: f'<div class="algo" data-frames="{m.group(1)}"></div>', body)
body = re.sub(r"<!--CPP:(\w+)-->", lambda m: html.escape((pathlib.Path(__file__).parent / "code" / (m.group(1) + ".cpp")).read_text().strip("\n"), quote=False), body)
d = ROOT / "src" / "parallel-b"; d.mkdir(parents=True, exist_ok=True)
name = "parallel-b-zan2-primeneniya-dfs"
(d / f"{name}.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / f"{name}.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
