# -*- coding: utf-8 -*-
"""
把 output/AI原生架构图.html（architecture-diagram 深色 SVG）转成单页 PPT：
  1. 抽取 HTML 中的 SVG，写入临时页面，用 headless Chrome 截成高分辨率 PNG；
  2. 生成 16:9 深色幻灯片：左侧放架构图，右侧放 MCP / A2A / 八层收敛三张要点卡。
运行：python build_ai_native_arch_new_ppt.py
输出：output/AI原生架构图new.pptx
"""
import os
import re
import subprocess
import tempfile

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from ppt_kit import new_prs, slide, rect, txt, R, oval, save

OUT = "/Users/apple/SocratesAI/output"
SRC_HTML = os.path.join(OUT, "AI原生架构图.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
In = Inches

# 深色主题（与 HTML 一致）
BG    = RGBColor(0x02, 0x06, 0x17)
CARD  = RGBColor(0x0F, 0x17, 0x2A)
BORDER = RGBColor(0x1E, 0x29, 0x3B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SLATE = RGBColor(0x94, 0xA3, 0xB8)
CYAN  = RGBColor(0x22, 0xD3, 0xEE)
ORANGE = RGBColor(0xFB, 0x92, 0x3C)
ROSE  = RGBColor(0xFB, 0x71, 0x85)

VB_W, VB_H = 1450, 1170            # SVG viewBox
PNG_W = 2900                       # 2x 截图宽
PNG_H = round(PNG_W * VB_H / VB_W)

CARDS = [
    (CYAN, "MCP —— 纵向串联（Agent → 工具/数据）", [
        "Agent 平台层是 MCP Client，统一发起工具调用",
        "SaaS 工具、知识检索、数据查询以 MCP Server 暴露",
        "每次调用必经 AI 安全治理层：护栏 · 身份 · 审计",
        "三云原生支持：AgentCore Gateway / ADK / Foundry"]),
    (ORANGE, "A2A —— 横向串联（Agent ⇄ Agent）", [
        "SaaS 内嵌 Agent 与企业 Agent 跨边界协作",
        "应用层任务委派 → 平台层多 Agent 编排",
        "跨云跨厂商互操作：GCP ⇄ AWS ⇄ Azure",
        "Google 发起、Linux 基金会托管，三云共同支持"]),
    (ROSE, "八层收敛与新控制点", [
        "数据（供模型训练）与知识（供 Agent 调用）分离",
        "Tokens 工厂层：数据 + 算力 → 智能（tokens）",
        "Databricks / Snowflake 跨云供数，中立数据平台",
        "Agent 平台层是 Agent 时代新的控制点"]),
]


def render_png(tmpdir):
    with open(SRC_HTML, encoding="utf-8") as f:
        html = f.read()
    m = re.search(r"<svg .*?</svg>", html, re.S)
    if not m:
        raise SystemExit("未在 HTML 中找到 SVG")
    page = (f'<!doctype html><html><head><meta charset="utf-8"><style>'
            f'body{{margin:0;background:#020617}}svg{{display:block;width:{PNG_W}px}}'
            f'</style></head><body>{m.group(0)}</body></html>')
    tmp_html = os.path.join(tmpdir, "diagram.html")
    png = os.path.join(tmpdir, "diagram.png")
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(page)
    subprocess.run([CHROME, "--headless", "--disable-gpu",
                    f"--window-size={PNG_W},{PNG_H}",
                    f"--screenshot={png}", f"file://{tmp_html}"],
                   check=True, capture_output=True)
    return png


def build(png):
    prs = new_prs()
    s = slide(prs)
    SW, SH = In(13.333), In(7.5)
    rect(s, 0, 0, SW, SH, BG)

    # ---- 标题 ----
    oval(s, In(0.35), In(0.30), In(0.14), CYAN)
    txt(s, In(0.62), In(0.16), In(9.5), In(0.42),
        [[R("AI 原生层次化架构 · Agent 时代", 19, WHITE, True)]])
    txt(s, In(0.63), In(0.55), In(12.4), In(0.28),
        [[R("Google Cloud × AWS × Azure 八层收敛 —— MCP 纵向串联（Agent → 工具/知识/数据）· "
            "A2A 横向串联（Agent ⇄ Agent · 跨云）", 10, SLATE)]])

    # ---- 左侧：架构图 ----
    img_y = In(0.92)
    img_h = In(6.40)
    img_w = img_h * VB_W / VB_H
    s.shapes.add_picture(png, In(0.25), img_y, height=img_h)

    # ---- 右侧：三张要点卡 ----
    px = In(0.25) + img_w + In(0.25)
    pw = SW - px - In(0.25)
    gap = In(0.15)
    ch = (img_h - gap * 2) / 3
    for i, (c, head, items) in enumerate(CARDS):
        y = img_y + i * (ch + gap)
        rect(s, px, y, pw, ch, CARD, line=BORDER, line_w=1.0, round_=True)
        oval(s, px + In(0.2), y + In(0.20), In(0.11), c)
        txt(s, px + In(0.42), y + In(0.12), pw - In(0.55), In(0.3),
            [[R(head, 11.5, WHITE, True)]])
        txt(s, px + In(0.22), y + In(0.50), pw - In(0.42), ch - In(0.6),
            [[R("· ", 9.5, c, True), R(it, 9.5, SLATE)] for it in items],
            line_spacing=1.12, space_after=4)

    # ---- 页脚 ----
    txt(s, In(0.25), SH - In(0.16), SW - In(0.5), In(0.14),
        [[R("AI 原生架构 · Agent 时代三大云分层对标（截至 2026-07 公开信息） · chenliang",
            7.5, RGBColor(0x47, 0x55, 0x69))]], align=PP_ALIGN.CENTER)

    save(prs, os.path.join(OUT, "AI原生架构图new.pptx"))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as td:
        build(render_png(td))
