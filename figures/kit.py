"""Общие примитивы для SVG-иллюстраций в стиле 3Blue1Brown (палитра — ровно эти hex: страницы перекрашивают их под тему)."""
import html

PANEL = "#141a24"; NODE = "#1E2836"; EDGE = "#3b4a63"; TEXT = "#dfe7f1"; MUTED = "#9aa4b2"; AXIS = "#7c8aa0"
BLUE, GREEN, YELLOW, RED, ORANGE, PURPLE = "#58c4dd", "#83c167", "#ffff00", "#fc6255", "#ff8c1a", "#c78bff"
SOFT = {BLUE: "#1d4257", GREEN: "#27431f", RED: "#4f1f1b", YELLOW: "#4d4d00", ORANGE: "#53300a", PURPLE: "#3a2858"}
COLORS = {1: BLUE, 2: GREEN, 3: ORANGE, 4: PURPLE, 5: RED}


def esc(s): return html.escape(str(s), quote=False)


def svg(w, h, body, defs=""):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" xmlns="http://www.w3.org/2000/svg"><defs>{defs}'
            f'<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker></defs>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{PANEL}"/>{body}</svg>')


def text(x, y, s, size=15, fill=TEXT, anchor="middle", weight="400", mono=False):
    fam = ' font-family="ui-monospace,Menlo,monospace"' if mono else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}"{fam}>{esc(s)}</text>'


def cell(x, y, w, h, label="", color=None, size=15, sub=None, rx=6):
    fill = SOFT[color] if color else NODE
    stroke = color or EDGE
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{2 if color else 1.5}"/>'
    if label != "":
        ty = y + h / 2 + (size * 0.35 if sub is None else -2)
        out += text(x + w / 2, ty, label, size)
    if sub is not None:
        out += text(x + w / 2, y + h - 7, sub, 11, MUTED)
    return out


def line(x1, y1, x2, y2, color=EDGE, w=2, dash=None, arrow=False):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = ' marker-end="url(#ar)"' if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}{m}/>'


def circle(x, y, r, label="", color=None, size=14):
    fill = SOFT[color] if color else NODE
    out = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{color or EDGE}" stroke-width="2"/>'
    if label != "": out += text(x, y + size * 0.35, label, size)
    return out


def figure(svgs, caption):
    return f'<figure class="viz">{svgs}<figcaption>{caption}</figcaption></figure>'
