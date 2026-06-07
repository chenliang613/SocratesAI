# -*- coding: utf-8 -*-
"""
ppt_kit —— 可复用的 PPT 设计系统与版式模板。
设计系统沿用 make_ppt.py，封装为模板函数，供各公司分析 deck 共用。

版式模板（均接收 prs，自动新建 slide）：
  cover / toc / cards / two_col / steps / takeaways / closing
内容数据驱动：cards/takeaways 等接收 (标题, 描述, 颜色) 元组列表。
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------- 设计系统 ----------------
INK    = RGBColor(0x0B, 0x1F, 0x33)
NAVY   = RGBColor(0x10, 0x2A, 0x43)
BLUE   = RGBColor(0x1B, 0x6E, 0xF3)
SKY    = RGBColor(0x35, 0xB8, 0xE0)
TEAL   = RGBColor(0x14, 0xB8, 0xA6)
AMBER  = RGBColor(0xF5, 0x9E, 0x0B)
CORAL  = RGBColor(0xF4, 0x6A, 0x5E)
PURPLE = RGBColor(0x7C, 0x5C, 0xFF)
GREY   = RGBColor(0x5B, 0x6B, 0x7B)
LGREY  = RGBColor(0x8A, 0x98, 0xA6)
LINE   = RGBColor(0xD7, 0xDE, 0xE6)
PANEL  = RGBColor(0xF4, 0xF7, 0xFB)
PANEL2 = RGBColor(0xEC, 0xF1, 0xF8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
CLOUD  = RGBColor(0xC8, 0xD6, 0xE6)

PALETTE = [BLUE, TEAL, PURPLE, AMBER, CORAL, SKY]
FONT = "Microsoft YaHei"

In = Inches


def new_prs():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def _sw(prs):
    return prs.slide_width


def _sh(prs):
    return prs.slide_height


def slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ---------------- 基础图元 ----------------
def rect(s, x, y, w, h, fill, line=None, line_w=0.75, shadow=False, round_=False):
    shp = s.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE, x, y, w, h)
    if round_:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    if shadow:
        el = shp._element.spPr
        ef = el.makeelement(qn('a:effectLst'), {})
        sh = ef.makeelement(qn('a:outerShdw'),
                            {'blurRad': '90000', 'dist': '40000', 'dir': '5400000', 'rotWithShape': '0'})
        clr = sh.makeelement(qn('a:srgbClr'), {'val': '0B1F33'})
        alpha = clr.makeelement(qn('a:alpha'), {'val': '18000'})
        clr.append(alpha); sh.append(clr); ef.append(sh); el.append(ef)
    return shp


def oval(s, x, y, d, fill, line=None, line_w=2.0):
    o = s.shapes.add_shape(MSO_SHAPE.OVAL, x, y, d, d)
    if fill is None:
        o.fill.background()
    else:
        o.fill.solid(); o.fill.fore_color.rgb = fill
    if line is None:
        o.line.fill.background()
    else:
        o.line.color.rgb = line; o.line.width = Pt(line_w)
    o.shadow.inherit = False
    return o


def txt(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space_after=6, line_spacing=1.0, wrap=True):
    """runs: 段落列表；每段 = [(text, size, color, bold, italic), ...]"""
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space_after); p.space_before = Pt(0)
        p.line_spacing = line_spacing
        for (t, sz, c, b, it) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.color.rgb = c; r.font.bold = b
            r.font.italic = it; r.font.name = FONT
    return tb


def R(t, sz, c, b=False, it=False):
    return (t, sz, c, b, it)


def chip(s, x, y, w, label, color, h=Inches(0.34)):
    rect(s, x, y, w, h, color, round_=True)
    txt(s, x, y, w, h, [[R(label, 11, WHITE, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ---------------- 页眉 / 页脚 ----------------
def header(s, prs, kicker, title, idx, total, footer):
    SW, SH = _sw(prs), _sh(prs)
    rect(s, 0, 0, SW, Inches(1.18), WHITE)
    rect(s, Inches(0.6), Inches(0.34), Inches(0.12), Inches(0.5), BLUE)
    txt(s, Inches(0.85), Inches(0.26), Inches(10.5), Inches(0.32),
        [[R(kicker, 11.5, BLUE, True)]])
    txt(s, Inches(0.85), Inches(0.52), Inches(11.3), Inches(0.5),
        [[R(title, 22, INK, True)]])
    txt(s, SW - Inches(1.4), Inches(0.42), Inches(0.9), Inches(0.4),
        [[R(f"{idx:02d}", 17, BLUE, True), R(f" / {total:02d}", 11, LGREY)]],
        align=PP_ALIGN.RIGHT)
    rect(s, 0, Inches(1.18), SW, Pt(1.2), LINE)
    rect(s, 0, SH - Inches(0.32), SW, Inches(0.32), INK)
    txt(s, Inches(0.6), SH - Inches(0.30), Inches(9), Inches(0.28),
        [[R(footer, 8.5, RGBColor(0xC2, 0xCE, 0xDB))]], anchor=MSO_ANCHOR.MIDDLE)


def _bottom(s, label, text, color=CORAL):
    txt(s, Inches(0.85), Inches(6.62), Inches(11.6), Inches(0.55),
        [[R(label, 12.5, color, True), R(text, 12, INK)]], line_spacing=1.1)


# ---------------- 版式模板 ----------------
def cover(prs, eyebrow, title_top, title_big, sub_runs, tagline_lines, author, accent=BLUE):
    s = slide(prs)
    SW, SH = _sw(prs), _sh(prs)
    rect(s, 0, 0, SW, SH, INK)
    rect(s, Inches(8.6), 0, Inches(4.73), SH, NAVY)
    for i, (cx, cy, d, col) in enumerate([
        (Inches(9.4), Inches(1.2), Inches(1.5), accent),
        (Inches(11.3), Inches(2.6), Inches(2.4), RGBColor(0x18, 0x3A, 0x5C)),
        (Inches(9.9), Inches(4.4), Inches(1.9), TEAL),
        (Inches(11.8), Inches(5.4), Inches(1.2), AMBER)]):
        if i == 1:
            oval(s, cx, cy, d, None, line=RGBColor(0x2A, 0x4D, 0x70), line_w=1.3)
        else:
            oval(s, cx, cy, d, col)
    rect(s, Inches(0.9), Inches(1.15), Inches(0.7), Pt(4), accent)
    txt(s, Inches(0.9), Inches(1.35), Inches(7.5), Inches(0.5),
        [[R(eyebrow, 13, SKY, True)]])
    txt(s, Inches(0.9), Inches(2.05), Inches(7.6), Inches(2.4),
        [[R(title_top, 40, WHITE, True)], [R(title_big, 50, WHITE, True)]],
        line_spacing=1.0, space_after=2)
    txt(s, Inches(0.9), Inches(4.5), Inches(7.4), Inches(1.0), [sub_runs])
    rect(s, Inches(0.92), Inches(5.4), Inches(4.6), Pt(1.2), RGBColor(0x33, 0x52, 0x73))
    txt(s, Inches(0.9), Inches(5.65), Inches(7.5), Inches(0.95),
        [[R(t, 12.5, RGBColor(0x9F, 0xB2, 0xC6))] for t in tagline_lines],
        line_spacing=1.15)
    txt(s, Inches(0.9), Inches(6.75), Inches(7), Inches(0.4),
        [[R(author, 11, RGBColor(0x6E, 0x84, 0x9B))]])
    return s


def toc(prs, items, idx, total, footer, title="目录 · 分析框架"):
    s = slide(prs)
    header(s, prs, "CONTENTS", title, idx, total, footer)
    x0 = Inches(0.85); y0 = Inches(1.6); cw = Inches(11.6)
    n = len(items); gap = Inches(0.12)
    ch = (Inches(7.5) - y0 - Inches(0.55) - (n - 1) * gap) / n
    for i, (no, t, d, c) in enumerate(items):
        y = y0 + i * (ch + gap)
        rect(s, x0, y, cw, ch, PANEL, round_=True)
        rect(s, x0, y, Inches(0.09), ch, c, round_=True)
        txt(s, x0 + Inches(0.35), y, Inches(1.1), ch, [[R(no, 24, c, True)]], anchor=MSO_ANCHOR.MIDDLE)
        txt(s, x0 + Inches(1.5), y, Inches(3.2), ch, [[R(t, 15.5, INK, True)]], anchor=MSO_ANCHOR.MIDDLE)
        rect(s, x0 + Inches(4.7), y + Inches(0.16), Pt(1.2), ch - Inches(0.32), LINE)
        txt(s, x0 + Inches(5.0), y, Inches(6.4), ch, [[R(d, 13, GREY)]], anchor=MSO_ANCHOR.MIDDLE)
    return s


def cards(prs, kicker, title, lead, items, idx, total, footer, ncols=2, bottom=None):
    """items: [(head, big, desc, color), ...]"""
    s = slide(prs)
    header(s, prs, kicker, title, idx, total, footer)
    top = Inches(1.95)
    if lead:
        txt(s, Inches(0.85), Inches(1.32), Inches(11.6), Inches(0.55),
            [[R(lead, 13, GREY)]], line_spacing=1.1)
    n = len(items); nrows = -(-n // ncols)
    bottom_reserve = Inches(0.7) if bottom else Inches(0.3)
    if ncols == 2:
        cw = Inches(5.6); gx = Inches(0.4)
    elif ncols == 3:
        cw = Inches(3.72); gx = Inches(0.22)
    else:
        cw = Inches(2.78); gx = Inches(0.18)
    x0 = Inches(0.85); gy = Inches(0.28)
    avail = Inches(7.5) - top - bottom_reserve
    ch = (avail - (nrows - 1) * gy) / nrows
    for i, (head, big, desc, c) in enumerate(items):
        x = x0 + (i % ncols) * (cw + gx)
        y = top + (i // ncols) * (ch + gy)
        rect(s, x, y, cw, ch, WHITE, line=LINE, round_=True, shadow=True)
        rect(s, x, y, Inches(0.1), ch, c, round_=True)
        ty = y + Inches(0.2)
        txt(s, x + Inches(0.35), ty, cw - Inches(0.6), Inches(0.35), [[R(head, 12, c, True)]])
        if big:
            txt(s, x + Inches(0.35), ty + Inches(0.34), cw - Inches(0.6), Inches(0.5),
                [[R(big, 19, INK, True)]])
            dy = ty + Inches(0.92)
        else:
            dy = ty + Inches(0.42)
        txt(s, x + Inches(0.35), dy, cw - Inches(0.6), ch - (dy - y) - Inches(0.18),
            [[R(desc, 12, GREY)]], line_spacing=1.2)
    if bottom:
        _bottom(s, bottom[0], bottom[1])
    return s


def two_col(prs, kicker, title, lead, left, right, idx, total, footer, bottom=None):
    """left/right: (col_title, color, [item, ...])"""
    s = slide(prs)
    header(s, prs, kicker, title, idx, total, footer)
    if lead:
        txt(s, Inches(0.85), Inches(1.32), Inches(11.6), Inches(0.5),
            [[R(lead, 13, GREY)]], line_spacing=1.1)
    oy = Inches(1.95) if lead else Inches(1.6)
    oh = Inches(6.55) - oy if bottom else Inches(6.95) - oy
    cw = Inches(5.6)
    for (col, x) in ((left, Inches(0.85)), (right, Inches(6.95))):
        ctitle, c, items = col
        rect(s, x, oy, cw, oh, PANEL, line=c, line_w=1.3, round_=True, shadow=True)
        rect(s, x, oy, cw, Inches(0.6), c, round_=True)
        txt(s, x, oy, cw, Inches(0.6), [[R(ctitle, 15, WHITE, True)]],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ni = len(items)
        ih = (oh - Inches(0.85)) / ni
        for i, it in enumerate(items):
            yy = oy + Inches(0.78) + i * ih
            rect(s, x + Inches(0.35), yy + Inches(0.07), Inches(0.16), Inches(0.16), c)
            txt(s, x + Inches(0.65), yy, cw - Inches(1.0), ih - Inches(0.06),
                [[R(it, 12.5, INK)]], line_spacing=1.12)
    if bottom:
        _bottom(s, bottom[0], bottom[1])
    return s


def steps(prs, kicker, title, lead, items, idx, total, footer, bottom=None):
    """items: [(tag, head, desc, color), ...]"""
    s = slide(prs)
    header(s, prs, kicker, title, idx, total, footer)
    if lead:
        txt(s, Inches(0.85), Inches(1.32), Inches(11.6), Inches(0.5),
            [[R(lead, 13, GREY)]], line_spacing=1.1)
    y0 = Inches(1.95) if lead else Inches(1.65)
    n = len(items); gx = Inches(0.18)
    cw = (Inches(11.6) - (n - 1) * gx) / n
    ch = (Inches(6.5) if bottom else Inches(6.8)) - y0
    for i, (tag, head, desc, c) in enumerate(items):
        x = Inches(0.85) + i * (cw + gx)
        rect(s, x, y0, cw, ch, WHITE, line=LINE, round_=True, shadow=True)
        rect(s, x, y0, cw, Inches(1.0), c, round_=True)
        txt(s, x, y0 + Inches(0.14), cw, Inches(0.35), [[R(tag, 12, WHITE, True)]], align=PP_ALIGN.CENTER)
        txt(s, x, y0 + Inches(0.46), cw, Inches(0.5), [[R(head, 15, WHITE, True)]], align=PP_ALIGN.CENTER)
        txt(s, x + Inches(0.22), y0 + Inches(1.2), cw - Inches(0.44), ch - Inches(2.0),
            [[R(desc, 12, GREY)]], line_spacing=1.22)
        o = oval(s, x + cw / 2 - Inches(0.32), y0 + ch - Inches(0.82), Inches(0.64), PANEL, line=c, line_w=1.5)
        txt(s, x + cw / 2 - Inches(0.32), y0 + ch - Inches(0.82), Inches(0.64), Inches(0.64),
            [[R(str(i + 1), 20, c, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if i < n - 1:
            txt(s, x + cw, y0 + ch / 2 - Inches(0.2), Inches(0.18), Inches(0.4),
                [[R("›", 22, LGREY, True)]], align=PP_ALIGN.CENTER)
    if bottom:
        _bottom(s, bottom[0], bottom[1])
    return s


def takeaways(prs, kicker, title, points, idx, total, footer):
    """points: [(head, desc), ...]，自动配色"""
    s = slide(prs)
    header(s, prs, kicker, title, idx, total, footer)
    x0 = Inches(0.85); y0 = Inches(1.6); w = Inches(11.6)
    n = len(points); gap = Inches(0.12)
    h = (Inches(7.5) - y0 - Inches(0.35) - (n - 1) * gap) / n
    for i, (t, d) in enumerate(points):
        c = PALETTE[i % len(PALETTE)]
        y = y0 + i * (h + gap)
        rect(s, x0, y, w, h, PANEL, round_=True)
        o = oval(s, x0 + Inches(0.28), y + (h - Inches(0.5)) / 2, Inches(0.5), c)
        txt(s, x0 + Inches(0.28), y + (h - Inches(0.5)) / 2, Inches(0.5), Inches(0.5),
            [[R(str(i + 1), 17, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        txt(s, x0 + Inches(1.0), y, Inches(3.0), h, [[R(t, 14.5, INK, True)]], anchor=MSO_ANCHOR.MIDDLE)
        rect(s, x0 + Inches(3.95), y + Inches(0.18), Pt(1.2), h - Inches(0.36), LINE)
        txt(s, x0 + Inches(4.2), y, w - Inches(4.5), h, [[R(d, 12.5, GREY)]],
            anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.12)
    return s


def closing(prs, big, sub_lines, footer_title, author, accent=AMBER):
    s = slide(prs)
    SW, SH = _sw(prs), _sh(prs)
    rect(s, 0, 0, SW, SH, INK)
    rect(s, 0, Inches(2.7), SW, Inches(2.1), NAVY)
    txt(s, Inches(1), Inches(1.4), Inches(11.3), Inches(0.5),
        [[R("CONCLUSION", 14, SKY, True)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(2.85), Inches(11.3), Inches(0.9),
        [[R(big, 32, WHITE, True)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(1.3), Inches(3.9), Inches(10.7), Inches(0.8),
        [[R(t, 15, CLOUD)] for t in sub_lines], align=PP_ALIGN.CENTER, line_spacing=1.3)
    rect(s, Inches(5.66), Inches(5.25), Inches(2), Pt(2), accent)
    txt(s, Inches(1), Inches(5.5), Inches(11.3), Inches(0.5),
        [[R(footer_title, 14, WHITE, True)]], align=PP_ALIGN.CENTER)
    txt(s, Inches(1), Inches(6.05), Inches(11.3), Inches(0.4),
        [[R(author, 11.5, RGBColor(0x7E, 0x93, 0xAB))]], align=PP_ALIGN.CENTER)
    return s


def save(prs, path):
    prs.save(path)
    print("saved:", path, "slides:", len(prs.slides._sldIdLst))
