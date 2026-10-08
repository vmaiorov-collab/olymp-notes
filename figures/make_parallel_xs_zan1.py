"""Собирает src/parallel-xs/parallel-xs-zan1-derevya.src.html."""
import json, re, pathlib, html
from parallel_xs_zan1 import FIGS, algos_js

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Деревья", "parallel": "parallel-xs", "pname": "Параллель XS", "porder": 2, "n": 1,
        "video": "video-232575486_456239858",
        "subtitle": "Двоичные подъёмы и LCA, разреженная таблица, эйлеров обход и запросы на путях, алгоритмы Тарьяна, подъёмы с линейной памятью, сжатое дерево, лесенки, метод четырёх русских, декартово дерево.",
        "chips": ["Лекция", "≈ 4,5 ч", "Язык кода: C++"]}
text = (pathlib.Path(__file__).parent / "text" / "parallel_xs_zan1_1.html").read_text()
src = (pathlib.Path(__file__).parent / "code" / "parallel_xs_zan1.cpp").read_text()
parts = re.split(r"^//---- (\w+)\n", src, flags=re.M)
code = {parts[i]: parts[i + 1].rstrip("\n") for i in range(1, len(parts), 2)}
text = re.sub(r"<!--CPP:(\w+)-->", lambda m: '<pre class="cpp">' + html.escape(code[m.group(1)], quote=False) + "</pre>", text)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), text)
d = ROOT / "src" / "parallel-xs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-xs-zan1-derevya.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
(d / "parallel-xs-zan1-derevya.algos.js").write_text(algos_js())
print("ok", len(body) // 1024, "KB")
