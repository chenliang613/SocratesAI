# -*- coding: utf-8 -*-
"""
单页逻辑架构图：企业 AI 落地的三层结构（自上而下）
  顶层：企业应用      —— 需求方 / 价值兑现处
  中层：SaaS 厂商     —— 把模型能力 Agent 化，封装进业务场景
  底层：AI 模型厂商    —— 推理 / 工具调用，Agent 的智能底座
三层之间通过「Agent 调用」上下协同（下发调用 ⇄ 返回结果），解决企业 AI 落地。
复用 ppt_kit 的设计系统（颜色 / 字体 / 图元）。运行：python build_agent_native_arch.py
"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from ppt_kit import (new_prs, slide, rect, txt, R, save,
                     INK, BLUE, PURPLE, AMBER, CORAL, GREY, LGREY,
                     LINE, WHITE, PANEL, PANEL2)

OUT = "/Users/apple/SocratesAI/output"
os.makedirs(OUT, exist_ok=True)
AUTHOR = "chenliang  ·  2026-06"
FOOT = RGBColor(0xC2, 0xCE, 0xDB)
In = Inches


def arrow(s, shape, x, y, w, h, fill):
    a = s.shapes.add_shape(shape, x, y, w, h)
    a.fill.solid(); a.fill.fore_color.rgb = fill
    a.line.fill.background()
    a.shadow.inherit = False
    return a


def layer(s, x, y, w, h, color, name, sub, items):
    """一层：白卡 + 彩色名牌 + 副标题 + 4 个能力小块。"""
    rect(s, x, y, w, h, WHITE, line=LINE, round_=True, shadow=True)
    rect(s, x, y, In(0.1), h, color, round_=True)
    # 名牌
    rect(s, x + In(0.3), y + In(0.17), In(2.15), In(0.44), color, round_=True)
    txt(s, x + In(0.3), y + In(0.17), In(2.15), In(0.44),
        [[R(name, 13, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + In(2.65), y + In(0.17), w - In(3.0), In(0.44),
        [[R(sub, 11.5, GREY)]], anchor=MSO_ANCHOR.MIDDLE)
    # 能力小块
    n = len(items); gap = In(0.24)
    iw = (w - In(0.7) - (n - 1) * gap) / n
    iy = y + In(0.72); ih = h - In(0.84)
    for i, it in enumerate(items):
        ix = x + In(0.35) + i * (iw + gap)
        rect(s, ix, iy, iw, ih, PANEL, round_=True)
        rect(s, ix + In(0.16), iy + ih / 2 - In(0.07), In(0.14), In(0.14), color)
        txt(s, ix + In(0.42), iy, iw - In(0.55), ih,
            [[R(it, 11, INK)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)


def agent_gap(s, y0, h, down_text, up_text):
    """两层之间的 Agent 调用连接：下发调用 ▼  /  返回结果 ▲。"""
    cx = In(6.665)
    # 中央 Agent 调用 名牌
    chip_w = In(1.55); chip_h = In(0.42)
    rect(s, cx - chip_w / 2, y0 + (h - chip_h) / 2, chip_w, chip_h, CORAL, round_=True, shadow=True)
    txt(s, cx - chip_w / 2, y0 + (h - chip_h) / 2, chip_w, chip_h,
        [[R("Agent 调用", 12, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # 两侧箭头（向下=调用，向上=返回）
    ay = y0 + (h - In(0.42)) / 2
    arrow(s, MSO_SHAPE.DOWN_ARROW, cx - chip_w / 2 - In(0.5), ay, In(0.3), In(0.42), CORAL)
    arrow(s, MSO_SHAPE.UP_ARROW, cx + chip_w / 2 + In(0.2), ay, In(0.3), In(0.42), CORAL)
    # 左右说明
    txt(s, In(0.95), y0, In(4.55), h,
        [[R("▼ 调用：", 11, CORAL, True), R(down_text, 11, INK)]],
        align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
    txt(s, In(7.85), y0, In(4.6), h,
        [[R("▲ 返回：", 11, CORAL, True), R(up_text, 11, INK)]],
        anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)


def build():
    prs = new_prs()
    s = slide(prs)
    SW, SH = In(13.333), In(7.5)
    rect(s, 0, 0, SW, SH, WHITE)

    # ---- 标题栏 ----
    rect(s, In(0.6), In(0.30), In(0.12), In(0.5), CORAL)
    txt(s, In(0.85), In(0.24), In(11.5), In(0.3),
        [[R("AGENT 原生时代 · 企业 AI 落地架构", 11.5, CORAL, True)]])
    txt(s, In(0.85), In(0.50), In(11.8), In(0.5),
        [[R("企业应用 · SaaS 厂商 · AI 模型厂商：通过 Agent 调用，让 AI 在企业落地", 20, INK, True)]])
    rect(s, 0, In(1.10), SW, Pt(1.2), LINE)

    X = In(0.85); W = In(11.6); LH = In(1.40)

    # ---- ① 企业应用层（顶层 · 需求方） ----
    layer(s, X, In(1.26), W, LH, AMBER, "企业应用",
          "业务场景 · 一线员工 · 真实流程 —— AI 落地的需求方与价值兑现处", [
              "业务部门发起需求", "嵌入日常工作流", "数据与权限归企业", "按业务结果衡量 ROI"])

    agent_gap(s, In(2.66), In(0.54),
              "企业把业务任务交给 Agent，由其调用 SaaS 能力",
              "SaaS Agent 办成事，结果回流到业务流程")

    # ---- ② SaaS 厂商层（中层 · 场景封装） ----
    layer(s, X, In(3.20), W, LH, BLUE, "SaaS 厂商",
          "把模型能力 Agent 化，封装进业务场景 —— 连接企业与模型的中间层", [
              "Agent 化业务应用", "行业 know-how / 工作流", "私有数据接入与治理", "系统 / 工具编排"])

    agent_gap(s, In(4.60), In(0.54),
              "SaaS 通过 Agent 调用模型推理与工具能力",
              "模型返回决策 / 生成，工具返回执行结果")

    # ---- ③ AI 模型厂商层（底层 · 智能底座） ----
    layer(s, X, In(5.14), W, LH, PURPLE, "AI 模型厂商",
          "推理 · 规划 · 可靠工具调用 —— Agent 的智能底座", [
              "基础模型与推理", "工具调用 / 函数执行", "安全对齐与护栏", "API / MCP 开放接口"])

    # ---- 结论条 ----
    rect(s, X, In(6.66), W, In(0.40), PANEL2, round_=True)
    txt(s, X, In(6.66), W, In(0.40),
        [[R("企业 AI 落地 = 模型智能 × SaaS 场景封装 × 企业流程承接 ——  三者经 Agent 调用链上下协同、闭环交付",
            11, INK, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 页脚 ----
    rect(s, 0, SH - In(0.32), SW, In(0.32), INK)
    txt(s, In(0.6), SH - In(0.30), In(11), In(0.28),
        [[R("AI 产业六层模型 · Agent 原生时代 · 模型 / SaaS / 企业应用三层协作架构    |    " + AUTHOR,
            8.5, FOOT)]], anchor=MSO_ANCHOR.MIDDLE)

    save(prs, os.path.join(OUT, "Agent原生时代新的生态.pptx"))


if __name__ == "__main__":
    build()
