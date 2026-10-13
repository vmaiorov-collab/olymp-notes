"""Собирает src/parallel-bs/parallel-bs-zan4-dinamika-1.src.html."""
import json, re, pathlib
from parallel_bs_zan4 import FIGS

ROOT = pathlib.Path(__file__).resolve().parent.parent
meta = {"title": "Динамическое программирование 1", "parallel": "parallel-bs", "pname": "Параллель BS", "porder": 4, "n": 4,
        "video": None,
        "subtitle": "Четыре пункта ДП, строки без двух единиц подряд, наибольшая возрастающая подпоследовательность за n² и n log n с доказательством и восстановлением, наибольшая общая подпоследовательность; семинар: шахты, неубывающие массивы с суммой, пловцы.",
        "chips": ["Лекция", "≈ 4 ч 35 мин", "Язык кода: C++"],
        "youtube": "https://youtu.be/PkH2esyWW5I"}
t = pathlib.Path(__file__).parent / "text"
body = "\n".join((t / f"parallel_bs_zan4_{i}.html").read_text() for i in (1, 2, 3))
# таймкоды M:SS -> 0:MM:SS
body = re.sub(r'(<ts t=")(\d+:\d\d)("\s*/>)', r'\g<1>0:\2\3', body)
body = re.sub(r'(data-tc=")(\d+:\d\d)(")', r'\g<1>0:\2\3', body)
body = re.sub(r"<!--FIG:(\w+)-->", lambda m: FIGS[m.group(1)](), body)
d = ROOT / "src" / "parallel-bs"; d.mkdir(parents=True, exist_ok=True)
(d / "parallel-bs-zan4-dinamika-1.src.html").write_text("<!--meta " + json.dumps(meta, ensure_ascii=False) + "-->\n" + body)
print("ok", len(body) // 1024, "KB")
