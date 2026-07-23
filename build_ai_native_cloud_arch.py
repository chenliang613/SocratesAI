# -*- coding: utf-8 -*-
"""
单页架构图：面向 Agent 时代的 AI 原生层次化架构 —— Google Cloud × AWS × Azure 对标。

矩阵式版图（自上而下八层）：
  SaaS 层 / Agent 应用层 / Agent 平台层 / AI 安全治理层 /
  知识层（供 Agent 调用）/ Tokens 工厂层（模型）/ 数据层（供模型训练）/ AI 基础设施层
  横轴 = 三大云厂商各自的对应服务
  数据层内嵌跨云数据平台条：Databricks / Snowflake（三云均可部署）
  右侧纵贯条 = 互操作协议：MCP / A2A
其中「Agent 平台层」是 Agent 时代新增的核心层，用珊瑚色高亮。

复用 ppt_kit 的设计系统。运行：python build_ai_native_cloud_arch.py
"""
import os
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

from ppt_kit import (new_prs, slide, rect, txt, R, save,
                     INK, NAVY, BLUE, SKY, TEAL, AMBER, CORAL, PURPLE,
                     GREY, LGREY, LINE, WHITE, PANEL, PANEL2)

OUT = "/Users/apple/SocratesAI/output"
os.makedirs(OUT, exist_ok=True)
AUTHOR = "chenliang  ·  2026-07"
FOOT = RGBColor(0xC2, 0xCE, 0xDB)
In = Inches

# ---------------- 版面几何 ----------------
SW, SH = In(13.333), In(7.5)
MX = In(0.5)                      # 左右页边距
LBL_W = In(1.35)                  # 左侧层名列宽
BAR_W = In(0.55)                  # 右侧互操作条宽
GAP = In(0.08)
COL_W = (SW - MX * 2 - LBL_W - BAR_W - GAP * 4) / 3   # 厂商列宽

HDR_Y, HDR_H = In(1.18), In(0.40)                     # 厂商表头行
GRID_Y = In(1.66)                                     # 八层起点
GRID_B = In(6.46)                                     # 八层终点
RGAP = In(0.055)                                      # 行间距
STRIP_H = In(0.24)                                    # 跨云数据平台条高

VENDORS = [
    ("Google Cloud", "全栈自研 · 模型驱动", BLUE),
    ("AWS", "开放组合 · 基础设施驱动", AMBER),
    ("Azure", "生态嵌入 · Copilot 驱动", SKY),
]

# (层名, 一句定位, 层色, 高度权重, 高亮?, 跨云条?, [GCP 行, AWS 行, Azure 行])
LAYERS = [
    ("SaaS 层", "场景价值兑现", NAVY, 1.0, False, False, [
        ["Google Workspace（Gemini 内嵌）", "行业方案 · ISV 市场"],
        ["Amazon Connect · Supply Chain", "Marketplace（三方 SaaS 生态）"],
        ["Microsoft 365 / Dynamics 365", "Teams · Power Platform"]]),
    ("Agent 应用层", "开箱即用助手", NAVY, 1.0, False, False, [
        ["Gemini Enterprise · Code Assist", "Customer Engagement Suite"],
        ["Amazon Q Business / Q Developer", "Kiro（Agentic IDE）· AWS Transform"],
        ["M365 Copilot · GitHub Copilot", "Copilot Studio（低代码 Agent）"]]),
    ("Agent 平台层", "开发·运行·治理", CORAL, 1.3, True, False, [
        ["Vertex AI Agent Builder",
         "Agent Engine（运行时·记忆）",
         "ADK 开源框架 + A2A 协议"],
        ["Bedrock AgentCore（Runtime·Memory）",
         "AgentCore Gateway · Identity",
         "Strands Agents SDK（任意框架）"],
        ["Foundry Agent Service",
         "Agent Framework（SK + AutoGen）",
         "Agent 365（Agent 管控面）"]]),
    ("AI 安全治理层", "信任与合规", PURPLE, 1.0, False, False, [
        ["Model Armor · SAIF 安全框架", "Security Command Center AI"],
        ["Bedrock Guardrails（安全护栏）", "AgentCore Identity · GuardDuty"],
        ["AI Content Safety · Entra Agent ID", "Purview · Defender for AI"]]),
    ("知识层", "供 Agent 调用", TEAL, 1.0, False, False, [
        ["Vertex AI Search · RAG Engine", "AlloyDB / Spanner 向量检索"],
        ["Bedrock Knowledge Bases", "S3 Vectors · OpenSearch · Kendra"],
        ["Azure AI Search（混合检索）", "Cosmos DB（向量·记忆）· Fabric IQ"]]),
    ("Tokens 工厂层", "数据+算力→智能", NAVY, 1.3, False, False, [
        ["Gemini 3 系列 · Gemma",
         "Veo / Imagen 多模态生成",
         "Model Garden（200+ 模型）"],
        ["Amazon Nova 自研系列",
         "Bedrock 多模型（Claude 等）",
         "SageMaker AI（训练·微调·推理）"],
        ["Azure OpenAI（GPT-5 系列）",
         "MAI / Phi 自研模型",
         "Foundry Models（万级目录）"]]),
    ("数据层", "供模型训练", TEAL, 1.45, False, True, [
        ["BigQuery 湖仓 · Dataflow", "Vertex AI 数据集 · 标注"],
        ["S3 数据湖 · Glue · EMR", "Clean Rooms · Data Exchange"],
        ["Microsoft Fabric · OneLake", "Synapse · Data Factory"]]),
    ("AI 基础设施层", "算力地基", NAVY, 1.0, False, False, [
        ["TPU（Trillium / Ironwood）· A3/A4 GPU", "GKE · 动态负载调度"],
        ["Trainium / Inferentia · EC2 UltraServers", "SageMaker HyperPod"],
        ["Maia / Cobalt · ND GB200/GB300", "AKS · Azure Boost"]]),
]

STRIP_TEXT = ("跨云数据平台：Databricks（湖仓一体 · Mosaic AI）｜ Snowflake（AI Data Cloud · Cortex AI）"
              "—— 三云均可部署，向上供训练数据与知识检索")


def build():
    prs = new_prs()
    s = slide(prs)
    rect(s, 0, 0, SW, SH, WHITE)

    # ---- 标题栏 ----
    rect(s, MX, In(0.26), In(0.12), In(0.5), CORAL)
    txt(s, MX + In(0.25), In(0.20), In(11.8), In(0.3),
        [[R("AGENT 时代 · 三大云 AI 服务对标", 11.5, CORAL, True)]])
    txt(s, MX + In(0.25), In(0.46), In(12.2), In(0.5),
        [[R("AI 原生层次化架构：Google Cloud × AWS × Azure 殊途同归的八层收敛", 20, INK, True)]])
    rect(s, 0, In(1.06), SW, Pt(1.2), LINE)

    col_x = [MX + LBL_W + GAP + i * (COL_W + GAP) for i in range(3)]

    # ---- 厂商表头 ----
    txt(s, MX, HDR_Y, LBL_W, HDR_H, [[R("八层架构", 10.5, LGREY, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    for (name, pos, c), x in zip(VENDORS, col_x):
        rect(s, x, HDR_Y, COL_W, HDR_H, c, round_=True, shadow=True)
        txt(s, x, HDR_Y + In(0.03), COL_W, In(0.22),
            [[R(name, 12, WHITE, True)]], align=PP_ALIGN.CENTER)
        txt(s, x, HDR_Y + In(0.22), COL_W, In(0.16),
            [[R(pos, 8, WHITE)]], align=PP_ALIGN.CENTER)

    # ---- 八层 × 三厂商 ----
    wsum = sum(w for (_, _, _, w, _, _, _) in LAYERS)
    unit = (GRID_B - GRID_Y - RGAP * (len(LAYERS) - 1)) / wsum
    y = GRID_Y
    for (name, sub, lc, w, hot, strip, cols) in LAYERS:
        rh = unit * w
        cell_h = rh - STRIP_H - In(0.04) if strip else rh
        # 左侧层名牌（贯穿整行，含跨云条）
        rect(s, MX, y, LBL_W, rh, lc, round_=True)
        txt(s, MX + In(0.05), y, LBL_W - In(0.10), rh,
            [[R(name, 10.5, WHITE, True)], [R(sub, 7.5, FOOT)]],
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
            line_spacing=1.0, space_after=1)
        # 三厂商单元格
        for (vn, vp, vc), x, lines in zip(VENDORS, col_x, cols):
            rect(s, x, y, COL_W, cell_h, PANEL,
                 line=CORAL if hot else LINE, line_w=1.5 if hot else 0.75,
                 round_=True)
            paras = [[R("▪ ", 8.5, vc, True), R(ln, 9, INK)] for ln in lines]
            txt(s, x + In(0.13), y, COL_W - In(0.24), cell_h,
                paras, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0, space_after=2)
        if hot:
            # 高亮标签：Agent 时代新增核心层
            tag_w = In(1.65)
            rect(s, SW - MX - BAR_W - GAP - tag_w + In(0.02), y - In(0.10),
                 tag_w, In(0.24), CORAL, round_=True)
            txt(s, SW - MX - BAR_W - GAP - tag_w + In(0.02), y - In(0.10),
                tag_w, In(0.24), [[R("Agent 时代新增核心层", 8.5, WHITE, True)]],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if strip:
            # 跨云数据平台条（横贯三列）
            sx = col_x[0]
            sw_ = col_x[2] + COL_W - sx
            sy = y + cell_h + In(0.04)
            rect(s, sx, sy, sw_, STRIP_H, PANEL2, line=TEAL, line_w=1.0, round_=True)
            txt(s, sx, sy, sw_, STRIP_H, [[R(STRIP_TEXT, 8.5, INK, True)]],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += rh + RGAP

    # ---- 右侧互操作条（旋转文字） ----
    bar_x = SW - MX - BAR_W
    bar_h = GRID_B - GRID_Y
    rect(s, bar_x, GRID_Y, BAR_W, bar_h, INK, round_=True)
    cx = bar_x + BAR_W / 2
    cy = GRID_Y + bar_h / 2
    tb = txt(s, cx - bar_h / 2, cy - In(0.25), bar_h, In(0.5),
             [[R("互操作协议纵贯全栈：MCP（工具调用） · A2A（Agent 协作）",
                 10, WHITE, True)]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb.rotation = 270

    # ---- 结论条 ----
    rect(s, MX, In(6.56), SW - MX * 2, In(0.40), PANEL2, round_=True)
    txt(s, MX, In(6.56), SW - MX * 2, In(0.40),
        [[R("三云殊途同归：", 10.5, CORAL, True),
          R("算力 → 数据 → Tokens 工厂 → 知识 → Agent 平台 → Agent 应用 → SaaS 八层收敛，安全治理与 MCP / A2A 纵贯全栈 —— ",
            10.5, INK),
          R("Agent 平台层是 Agent 时代新的控制点", 10.5, INK, True)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # ---- 页脚 ----
    rect(s, 0, SH - In(0.32), SW, In(0.32), INK)
    txt(s, In(0.6), SH - In(0.30), In(11), In(0.28),
        [[R("AI 原生架构 · Agent 时代三大云服务分层对标（截至 2026-07 公开信息）    |    " + AUTHOR,
            8.5, FOOT)]], anchor=MSO_ANCHOR.MIDDLE)

    save(prs, os.path.join(OUT, "AI原生架构图.pptx"))


if __name__ == "__main__":
    build()
