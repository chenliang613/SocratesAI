# -*- coding: utf-8 -*-
"""
单页逻辑图：Agent 原生的完整工作逻辑
  场景 1：LLM + MCP 工具        —— 简单问答与内容生成
  场景 2：LLM + RAG / SKILL     —— 知识库定边界，SKILL 规范业务流程
  场景 3：多 Agent               —— 调度 · 协同 · 自适应
  场景 4：一个大框包含场景 1/2/3 —— 这就是 Harness 的内涵
复用 ppt_kit 的设计系统（颜色 / 字体 / 图元），全部为可编辑原生形状。
运行：python build_agent_native.py  →  output/Agent原生.pptx
"""
import os
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from ppt_kit import (new_prs, slide, rect, txt, R, save,
                     INK, BLUE, TEAL, PURPLE, AMBER, CORAL, GREY, LGREY,
                     LINE, WHITE, PANEL, PANEL2)

OUT = "/Users/apple/SocratesAI/output"
os.makedirs(OUT, exist_ok=True)
AUTHOR = "chenliang  ·  2026-07"
FOOT = RGBColor(0xC2, 0xCE, 0xDB)
In = Inches


# ---------------- 小图元 ----------------
def arrow(s, shape, x, y, w, h, fill):
    a = s.shapes.add_shape(shape, x, y, w, h)
    a.fill.solid(); a.fill.fore_color.rgb = fill
    a.line.fill.background()
    a.shadow.inherit = False
    return a


def node(s, x, y, w, h, label_lines, fill=None, line=None, tcolor=INK,
         sz=10, bold=True, sz2=8.5):
    """一个节点盒：单行或两行文字，居中。"""
    rect(s, x, y, w, h, fill, line=line, line_w=1.2, round_=True)
    paras = [[R(label_lines[0], sz, tcolor, bold)]]
    if len(label_lines) > 1:
        paras.append([R(label_lines[1], sz2, tcolor)])
    txt(s, x, y, w, h, paras, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
        space_after=0, line_spacing=1.0)


def darrow(s, cx, y, color, h=In(0.16)):
    arrow(s, MSO_SHAPE.DOWN_ARROW, cx - In(0.10), y, In(0.20), h, color)


# ---------------- 场景卡片 ----------------
CW, CH = In(3.72), In(3.50)          # 卡片宽高
CY = In(2.10)                        # 卡片顶
CORAL_BG = RGBColor(0xFD, 0xF0, 0xED)  # 场景 4 大框底色（整圈同属 Harness）


def card_frame(s, x, color, no, eng, title, sub):
    """白卡 + 彩色头带（场景编号 + 标题）+ 副标题。返回图区顶 y。"""
    rect(s, x, CY, CW, CH, WHITE, line=LINE, round_=True, shadow=True)
    rect(s, x, CY, CW, In(0.60), color, round_=True)
    txt(s, x, CY + In(0.05), CW, In(0.52),
        [[R(f"场景 {no}", 9.5, WHITE, True), R(f"  ·  {eng}", 8.5, WHITE)],
         [R(title, 13, WHITE, True)]],
        align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
    txt(s, x + In(0.15), CY + In(0.66), CW - In(0.3), In(0.26),
        [[R(sub, 9.5, GREY)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def caption(s, x, text, color):
    txt(s, x + In(0.15), CY + CH - In(0.36), CW - In(0.3), In(0.3),
        [[R("◆ ", 9, color, True), R(text, 9.5, GREY, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def scene1(s, x):
    c = BLUE
    card_frame(s, x, c, 1, "LLM + MCP", "LLM + MCP 工具",
               "简单问答 · 内容生成 —— 开箱即用的基础 Agent")
    cx = x + CW / 2
    y = CY + In(1.06)
    node(s, cx - In(1.1), y, In(2.2), In(0.32), ["用户提问 / 生成指令"],
         fill=PANEL2, sz=9.5)
    darrow(s, cx, y + In(0.36), LGREY)
    # LLM ⇄ MCP 工具
    y2 = y + In(0.56)
    node(s, x + In(0.28), y2, In(1.20), In(0.62), ["LLM", "理解 · 推理 · 生成"],
         fill=c, tcolor=WHITE, sz=12)
    arrow(s, MSO_SHAPE.LEFT_RIGHT_ARROW, x + In(1.54), y2 + In(0.20),
          In(0.42), In(0.22), c)
    node(s, x + In(2.02), y2, In(1.42), In(0.62), ["MCP 工具", "搜索 · 文件 · API"],
         fill=WHITE, line=c, sz=10.5, tcolor=c)
    darrow(s, cx, y2 + In(0.66), LGREY)
    node(s, cx - In(1.2), y2 + In(0.86), In(2.4), In(0.36),
         ["回答 / 内容产出"], fill=PANEL2, line=c, tcolor=c, sz=10)
    caption(s, x, "模型大脑 + 标准化工具接口", c)


def scene2(s, x):
    c = TEAL
    card_frame(s, x, c, 2, "LLM + RAG / SKILL", "LLM + RAG / SKILL",
               "知识库定边界 · SKILL 规范业务流程")
    cx = x + CW / 2
    y = CY + In(1.06)
    node(s, cx - In(1.1), y, In(2.2), In(0.32), ["业务请求 / 任务"],
         fill=PANEL2, sz=9.5)
    darrow(s, cx, y + In(0.36), LGREY)
    # 知识库 → LLM ← SKILL
    y2 = y + In(0.56)
    node(s, x + In(0.12), y2, In(1.05), In(0.62), ["知识库", "RAG 检索增强"],
         fill=WHITE, line=c, sz=10.5, tcolor=c)
    arrow(s, MSO_SHAPE.RIGHT_ARROW, x + In(1.20), y2 + In(0.20),
          In(0.24), In(0.22), c)
    node(s, x + In(1.46), y2, In(0.88), In(0.62), ["LLM", "按知识作答"],
         fill=c, tcolor=WHITE, sz=12)
    arrow(s, MSO_SHAPE.LEFT_ARROW, x + In(2.36), y2 + In(0.20),
          In(0.24), In(0.22), c)
    node(s, x + In(2.62), y2, In(1.05), In(0.62), ["SKILL", "流程 · 规范"],
         fill=WHITE, line=c, sz=10.5, tcolor=c)
    darrow(s, cx, y2 + In(0.66), LGREY)
    node(s, cx - In(1.35), y2 + In(0.86), In(2.7), In(0.36),
         ["按业务流程规范执行与输出"], fill=PANEL2, line=c, tcolor=c, sz=10)
    caption(s, x, "知识给依据，SKILL 给章法", c)


def scene3(s, x):
    c = PURPLE
    card_frame(s, x, c, 3, "MULTI-AGENT", "多 Agent 协同",
               "调度 · 协同 · 自适应 —— 应对复杂任务")
    cx = x + CW / 2
    y = CY + In(1.02)
    node(s, cx - In(1.1), y, In(2.2), In(0.30), ["复杂任务 / 目标"],
         fill=PANEL2, sz=9.5)
    darrow(s, cx, y + In(0.33), LGREY, h=In(0.13))
    # 调度 Agent
    y2 = y + In(0.49)
    node(s, cx - In(1.25), y2, In(2.5), In(0.38), ["调度 Agent（规划 · 分派）"],
         fill=c, tcolor=WHITE, sz=10.5)
    # 三个执行 Agent
    y3 = y2 + In(0.56)
    labels = [["检索", "Agent"], ["分析", "Agent"], ["执行", "Agent"]]
    aw, gap = In(0.98), In(0.14)
    ax0 = cx - (aw * 3 + gap * 2) / 2
    for i, lab in enumerate(labels):
        ax = ax0 + i * (aw + gap)
        darrow(s, ax + aw / 2, y2 + In(0.41), c, h=In(0.13))
        node(s, ax, y3, aw, In(0.50), lab, fill=WHITE, line=c, sz=10, tcolor=c)
        if i < 2:
            txt(s, ax + aw, y3 + In(0.10), gap, In(0.3),
                [[R("⇄", 10, c, True)]], align=PP_ALIGN.CENTER)
    darrow(s, cx, y3 + In(0.54), LGREY, h=In(0.13))
    node(s, cx - In(1.35), y3 + In(0.70), In(2.7), In(0.34),
         ["协同产出 · 结果汇聚"], fill=PANEL2, line=c, tcolor=c, sz=10)
    # 自适应反馈回路（右侧上行箭头）
    arrow(s, MSO_SHAPE.UP_ARROW, x + In(3.44), y2 + In(0.44), In(0.14), In(1.30), AMBER)
    txt(s, x + In(3.30), y2 + In(0.10), In(0.42), In(0.3),
        [[R("自适应", 7.5, AMBER, True)]], align=PP_ALIGN.CENTER)
    caption(s, x, "任务分而治之，反馈动态调整", c)


# ---------------- 整页 ----------------
def build():
    prs = new_prs()
    s = slide(prs)
    SW, SH = In(13.333), In(7.5)
    rect(s, 0, 0, SW, SH, WHITE)

    # 标题栏
    rect(s, In(0.6), In(0.28), In(0.12), In(0.5), CORAL)
    txt(s, In(0.85), In(0.22), In(11.5), In(0.3),
        [[R("AGENT NATIVE · 完整工作逻辑", 11.5, CORAL, True)]])
    txt(s, In(0.85), In(0.48), In(11.8), In(0.5),
        [[R("Agent 原生：从 LLM+工具 到 多 Agent 协同，统一运行在 Harness 之中", 20, INK, True)]])
    rect(s, 0, In(1.08), SW, Pt(1.2), LINE)

    # ---- 场景 4：整个大圈就是 Harness（圈内=场景 1/2/3 的全部内容）----
    FX, FY, FW, FH = In(0.5), In(1.36), In(12.33), In(5.28)
    rect(s, FX, FY, FW, FH, CORAL_BG, line=CORAL, line_w=3.0, round_=True)
    # 场景 4 标牌骑在框线正中：整个大框即场景 4
    LW = In(6.0)
    rect(s, (SW - LW) / 2, In(1.14), LW, In(0.44), CORAL, round_=True, shadow=True)
    txt(s, (SW - LW) / 2, In(1.14), LW, In(0.44),
        [[R("场景 4 · Harness —— 把场景 1 / 2 / 3 全部包含的整个大框", 12, WHITE, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, In(0.85), In(1.68), In(11.63), In(0.32),
        [[R("圈内的一切 —— 工具调用 · 知识与流程 · 多 Agent 协同 —— 都由同一框架统一承载，这就是 ", 10.5, GREY),
          R("Harness 的内涵", 10.5, CORAL, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 场景 1 / 2 / 3 三张卡片 + 演进箭头 ----
    xs = [In(0.85), In(4.805), In(8.76)]
    scene1(s, xs[0]); scene2(s, xs[1]); scene3(s, xs[2])
    for gx in (In(4.585), In(8.54)):
        arrow(s, MSO_SHAPE.RIGHT_ARROW, gx, In(3.70), In(0.20), In(0.26), CORAL)

    # ---- Harness 内涵条（框内底部）----
    rect(s, In(0.85), In(5.74), In(1.50), In(0.66), CORAL, round_=True)
    txt(s, In(0.85), In(5.74), In(1.50), In(0.66),
        [[R("Harness", 11, WHITE, True)], [R("统一能力底座", 8.5, WHITE)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    feats = ["统一上下文与记忆", "工具 / MCP 路由", "知识 · SKILL 加载",
             "多 Agent 调度", "权限与安全护栏"]
    fw, fg = In(1.90), In(0.13)
    for i, f in enumerate(feats):
        fx = In(2.55) + i * (fw + fg)
        rect(s, fx, In(5.87), fw, In(0.40), WHITE, line=CORAL, line_w=1.1, round_=True)
        txt(s, fx, In(5.87), fw, In(0.40), [[R(f, 9.5, INK, True)]],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 结论条 ----
    rect(s, In(0.85), In(6.72), In(11.63), In(0.38), PANEL2, round_=True)
    txt(s, In(0.85), In(6.72), In(11.63), In(0.38),
        [[R("Agent 原生 = LLM 大脑 × MCP 工具 × RAG/SKILL 知识 × 多 Agent 协同，"
            "由 Harness 统一承载、调度与护航", 11, INK, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 页脚 ----
    rect(s, 0, SH - In(0.32), SW, In(0.32), INK)
    txt(s, In(0.6), SH - In(0.30), In(11), In(0.28),
        [[R("Agent 原生完整工作逻辑 · 场景 1 工具 / 场景 2 知识 / 场景 3 协同 / 场景 4 Harness    |    "
            + AUTHOR, 8.5, FOOT)]], anchor=MSO_ANCHOR.MIDDLE)

    save(prs, os.path.join(OUT, "Agent原生.pptx"))


if __name__ == "__main__":
    build()
