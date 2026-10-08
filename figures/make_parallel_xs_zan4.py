"""Собирает src/parallel-xs/parallel-xs-zan4-matematika-1.src.html."""
import json, re, pathlib, html
from parallel_xs_zan4 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Математика 1", "parallel": "parallel-xs", "pname": "Параллель XS", "porder": 2, "n": 4,
        "video": "video-232575486_456239912",
        "subtitle": "Разбор контеста по строкам и дистанционного тура; решето Эратосфена и линейное решето, мультипликативные функции, теорема Эйлера, расширенный Евклид, китайская теорема, включения-исключения, биномиальные коэффициенты, числа Каталана.",
        "chips": ["Разбор + лекция", "≈ 5 ч", "Язык кода: C++"]}
text = (pathlib.Path(__file__).parent / "text" / "parallel_xs_zan4_1.html").read_text()
src = (pathlib.Path(__file__).parent / "code" / "parallel_xs_zan4.cpp").read_text()
parts = re.split(r"^//---- (\w+)\n", src, flags=re.M)
code = {parts[i]: parts[i + 1].rstrip("\n") for i in range(1, len(parts), 2)}
text = re.sub(r"<!--CPP:(\w+)-->", lambda m: '<pre class="cpp">' + html.escape(code[m.group(1)], quote=False) + "</pre>", text)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), text)
d = ROOT / "src" / "parallel-xs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-xs-zan4-matematika-1.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-xs-zan4-matematika-1.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
