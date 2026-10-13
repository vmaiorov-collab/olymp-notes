"""Собирает src/parallel-c/parallel-c-zan5-stl.src.html."""
import json, re, pathlib
from parallel_c_zan5 import FIGS

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "STL: ввод-вывод, итераторы, компараторы, контейнеры", "parallel": "parallel-c", "pname": "Параллель C", "porder": 5, "n": 5,
        "video": None,
        "subtitle": "Быстрый ввод-вывод и файлы, итераторы и полуинтервалы, sort/unique/lower_bound, лямбды и компараторы, переполнение типов, set/multiset/map и отладка _GLIBCXX_DEBUG.",
        "chips": ["Лекция", "≈ 1 ч 50 мин", "Язык кода: C++"],
        "youtube": "https://youtu.be/htNZw0_IcPI"}
body = (pathlib.Path(__file__).parent / "text" / "parallel_c_zan5_1.html").read_text()
body = body.replace('data-tc="1:36:02"', 'data-tc="1:43:00"')
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-c"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-c-zan5-stl.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
print("ok", len(body) // 1024, "KB")
