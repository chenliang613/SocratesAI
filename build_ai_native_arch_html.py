# -*- coding: utf-8 -*-
"""
生成自包含 HTML+SVG 架构图（architecture-diagram 深色设计系统）：
面向 Agent 时代的 AI 原生八层架构 —— Google Cloud × AWS × Azure，
并标注 MCP（纵向：Agent → 工具/知识/数据）与 A2A（横向：Agent ⇄ Agent，跨云）
如何把各层串联起来。

运行：python build_ai_native_arch_html.py
输出：output/AI原生架构图.html（浏览器打开即可，内置 PNG/PDF 导出按钮）
"""
import os

OUT = "/Users/apple/SocratesAI/output"
os.makedirs(OUT, exist_ok=True)

# ---------------- 颜色 ----------------
SLATE   = "#64748b"
SLATE_L = "#94a3b8"
TXT     = "#cbd5e1"
CYAN    = "#22d3ee"   # MCP
ORANGE  = "#fb923c"   # A2A / Agent 平台层高亮
ROSE    = "#fb7185"   # 安全治理
TEALC   = "#2dd4bf"   # 知识层
VIOLET  = "#a78bfa"   # Tokens / 数据
GCP_C, GCP_F   = "#34d399", "rgba(6, 78, 59, 0.4)"
AWS_C, AWS_F   = "#fbbf24", "rgba(120, 53, 15, 0.3)"
AZ_C,  AZ_F    = "#60a5fa", "rgba(30, 58, 138, 0.4)"
CELL_F  = "rgba(30, 41, 59, 0.5)"
MASK    = "#0f172a"

# ---------------- 几何 ----------------
LBL_X, LBL_W = 20, 145
COLS = [(180, 330), (525, 330), (870, 330)]        # (x, w) × 3
COL_CX = [x + w / 2 for x, w in COLS]
GRID_R = COLS[2][0] + COLS[2][1]                    # 1200
RAIL_X = 1268                                       # MCP 纵向总线
VB_W, VB_H = 1450, 1170
HDR_Y, HDR_H = 34, 48

VENDORS = [
    ("Google Cloud", "全栈自研 · 模型驱动", GCP_C, GCP_F),
    ("AWS", "开放组合 · 基础设施驱动", AWS_C, AWS_F),
    ("Azure", "生态嵌入 · Copilot 驱动", AZ_C, AZ_F),
]

# (键, 层名, 副标, 强调色, 标签底色, y, h, 单元格行数, [GCP行, AWS行, Azure行])
ROWS = [
    ("saas", "SaaS 层", "场景价值兑现", SLATE_L, CELL_F, 100, 84, 2, [
        ["Google Workspace（Gemini 内嵌）", "行业方案 · ISV 市场"],
        ["Amazon Connect · Supply Chain", "Marketplace（三方 SaaS 生态）"],
        ["Microsoft 365 / Dynamics 365", "Teams · Power Platform"]]),
    ("app", "Agent 应用层", "开箱即用助手", SLATE_L, CELL_F, 220, 84, 2, [
        ["Gemini Enterprise · Code Assist", "Customer Engagement Suite"],
        ["Amazon Q Business / Q Developer", "Kiro（Agentic IDE）· AWS Transform"],
        ["M365 Copilot · GitHub Copilot", "Copilot Studio（低代码 Agent）"]]),
    ("plat", "Agent 平台层", "开发·运行·治理", ORANGE, "rgba(251, 146, 60, 0.22)", 340, 120, 3, [
        ["Vertex AI Agent Builder", "Agent Engine（运行时·记忆）", "ADK 开源框架 + A2A 协议"],
        ["Bedrock AgentCore（Runtime·Memory）", "AgentCore Gateway · Identity", "Strands Agents SDK（任意框架）"],
        ["Foundry Agent Service", "Agent Framework（SK + AutoGen）", "Agent 365（Agent 管控面）"]]),
    ("sec", "AI 安全治理层", "信任与合规", ROSE, "rgba(136, 19, 55, 0.4)", 496, 84, 2, [
        ["Model Armor · SAIF 安全框架", "Security Command Center AI"],
        ["Bedrock Guardrails（安全护栏）", "AgentCore Identity · GuardDuty"],
        ["AI Content Safety · Entra Agent ID", "Purview · Defender for AI"]]),
    ("know", "知识层", "供 Agent 调用", TEALC, "rgba(19, 78, 74, 0.4)", 616, 84, 2, [
        ["Vertex AI Search · RAG Engine", "AlloyDB / Spanner 向量检索"],
        ["Bedrock Knowledge Bases", "S3 Vectors · OpenSearch · Kendra"],
        ["Azure AI Search（混合检索）", "Cosmos DB（向量·记忆）· Fabric IQ"]]),
    ("tok", "Tokens 工厂层", "数据+算力→智能", VIOLET, "rgba(76, 29, 149, 0.4)", 736, 104, 3, [
        ["Gemini 3 系列 · Gemma", "Veo / Imagen 多模态生成", "Model Garden（200+ 模型）"],
        ["Amazon Nova 自研系列", "Bedrock 多模型（Claude 等）", "SageMaker AI（训练·微调·推理）"],
        ["Azure OpenAI（GPT-5 系列）", "MAI / Phi 自研模型", "Foundry Models（万级目录）"]]),
    ("data", "数据层", "供模型训练", VIOLET, "rgba(76, 29, 149, 0.4)", 876, 110, 2, [
        ["BigQuery 湖仓 · Dataflow", "Vertex AI 数据集 · 标注"],
        ["S3 数据湖 · Glue · EMR", "Clean Rooms · Data Exchange"],
        ["Microsoft Fabric · OneLake", "Synapse · Data Factory"]]),
    ("infra", "AI 基础设施层", "算力地基", SLATE_L, CELL_F, 1022, 84, 2, [
        ["TPU（Trillium/Ironwood）· A3/A4 GPU", "GKE · 动态负载调度"],
        ["Trainium / Inferentia · UltraServers", "SageMaker HyperPod"],
        ["Maia / Cobalt · ND GB200/GB300", "AKS · Azure Boost"]]),
]
ROW = {r[0]: r for r in ROWS}

# 层间连接牌：(上层键, 下层键, 颜色, 文案, 牌宽, 箭头模式 both|up)
GAPS = [
    ("saas", "app",  ORANGE, "A2A · SaaS 内嵌 Agent ⇄ 企业 Agent 协作", 400, "both"),
    ("app",  "plat", ORANGE, "A2A · 任务委派 · 多 Agent 编排（应用 = 平台上的 Agent）", 520, "both"),
    ("plat", "sec",  ROSE,   "所有 MCP / A2A / LLM 调用必经：安全护栏 · Agent 身份 · 审计追踪", 580, "both"),
    ("sec",  "know", CYAN,   "MCP · 知识检索工具调用（RAG 检索 / 长期记忆读写）", 480, "both"),
    ("know", "tok",  SLATE,  "LLM API · prompt + 知识上下文 → tokens（推理生成）", 480, "both"),
    ("tok",  "data", SLATE,  "训练 / 微调数据管道：高质量数据 → 模型权重", 420, "up"),
    ("data", "infra", SLATE, "湖仓存储 · 训练 / 推理算力承载", 320, "up"),
]

MK = {SLATE: "sl", CYAN: "cy", ORANGE: "or", ROSE: "ro"}
S = []  # SVG 片段


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(x, y, w, h, fill, stroke=None, sw=1.5, rx=6, dash=None, mask=False):
    if mask:
        S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{MASK}"/>')
    d = f' stroke-dasharray="{dash}"' if dash else ""
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{d}/>')


def text(x, y, t, fill=TXT, size=10, bold=False, anchor="middle"):
    b = ' font-weight="600"' if bold else ""
    S.append(f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"{b} '
             f'text-anchor="{anchor}">{esc(t)}</text>')


def line(x1, y1, x2, y2, color, w=1.3, dash=None, start=False, end=False):
    m = MK[color]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ms = f' marker-start="url(#ahr-{m})"' if start else ""
    me = f' marker-end="url(#ah-{m})"' if end else ""
    S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
             f'stroke="{color}" stroke-width="{w}"{d}{ms}{me}/>')


def build_svg():
    # defs：箭头 × 4 色 + 网格
    S.append('<defs>')
    for color, m in MK.items():
        S.append(f'<marker id="ah-{m}" markerWidth="10" markerHeight="7" refX="9" refY="3.5" '
                 f'orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="{color}"/></marker>')
        S.append(f'<marker id="ahr-{m}" markerWidth="10" markerHeight="7" refX="1" refY="3.5" '
                 f'orient="auto"><polygon points="10 0, 0 3.5, 10 7" fill="{color}"/></marker>')
    S.append('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>'
             '</pattern></defs>')
    S.append('<rect width="100%" height="100%" fill="url(#grid)"/>')

    # ---- 层间连接线（先画，压在牌子和单元格下面） ----
    for up, dn, color, label, pw, mode in GAPS:
        y1 = ROW[up][5] + ROW[up][6]
        y2 = ROW[dn][5]
        for cx in COL_CX:
            if mode == "up":
                line(cx, y2 - 1, cx, y1 + 1, color, end=True)
            else:
                line(cx, y1 + 1, cx, y2 - 1, color, start=True, end=True)

    # ---- 表头 ----
    text(LBL_X + LBL_W / 2, HDR_Y + 29, "八层架构", SLATE_L, 11, True)
    for (name, pos, c, f), (x, w) in zip(VENDORS, COLS):
        rect(x, HDR_Y, w, HDR_H, f, c, mask=True)
        text(x + w / 2, HDR_Y + 20, name, "white", 13, True)
        text(x + w / 2, HDR_Y + 37, pos, SLATE_L, 9)

    # ---- 八层 ----
    for key, name, sub, ac, lf, y, h, nlines, cols in ROWS:
        cell_h = h
        if key == "plat":
            cell_h = 88
        if key == "data":
            cell_h = 80
        # 左侧层名牌
        rect(LBL_X, y, LBL_W, h, lf if lf != CELL_F else "rgba(30,41,59,0.85)",
             ac, sw=2 if key == "plat" else 1.5, mask=True)
        text(LBL_X + LBL_W / 2, y + h / 2 - 4, name, "white", 12, True)
        text(LBL_X + LBL_W / 2, y + h / 2 + 13, sub, SLATE_L, 8.5)
        # 三厂商单元格
        for (vn, vp, vc, vf), (x, w), lines_ in zip(VENDORS, COLS, cols):
            rect(x, y, w, cell_h, CELL_F,
                 ORANGE if key == "plat" else "#334155",
                 sw=1.5 if key == "plat" else 1, mask=True)
            if nlines == 2:
                ys = [y + cell_h / 2 - 9, y + cell_h / 2 + 11]
            else:
                ys = [y + cell_h / 2 - 25, y + cell_h / 2 - 5, y + cell_h / 2 + 15]
            for ty, tline in zip(ys, lines_):
                S.append(f'<rect x="{x + 14}" y="{ty - 6}" width="5" height="5" fill="{vc}"/>')
                text(x + 26, ty, tline, TXT, 10, anchor="start")

    # ---- Agent 平台层：A2A 跨云横向总线 ----
    py, ph = ROW["plat"][5], 88
    bus_y = py + ph + 16                     # 436+8 → 452 内？行高120：340+88=428，bus 444
    bus_y = py + 120 - 16                    # 444
    for cx in COL_CX:
        line(cx, py + 88, cx, bus_y - 2, ORANGE, dash="3,3")
    line(COLS[0][0] + 20, bus_y, GRID_R - 20, bus_y, ORANGE, w=2, dash="6,4",
         start=True, end=True)
    rect(490, bus_y - 11, 400, 22, MASK, ORANGE, sw=1.2, rx=11)
    text(690, bus_y + 4, "A2A · 跨云跨厂商 Agent 互操作：GCP ⇄ AWS ⇄ Azure", ORANGE, 10, True)
    # 高亮徽标
    rect(1042, py - 9, 160, 18, ORANGE, rx=4)
    text(1122, py + 4, "Agent 时代新增核心层", "#020617", 8.5, True)

    # ---- 层间连接牌 ----
    for up, dn, color, label, pw, mode in GAPS:
        y1 = ROW[up][5] + ROW[up][6]
        y2 = ROW[dn][5]
        cy = (y1 + y2) / 2
        rect(690 - pw / 2, cy - 12, pw, 24, MASK, color, sw=1.2, rx=12)
        text(690, cy + 4, label, color, 10, True)

    # ---- 数据层：跨云数据平台条（Databricks / Snowflake） ----
    dy = ROW["data"][5]
    rect(COLS[0][0], dy + 86, GRID_R - COLS[0][0], 22,
         "rgba(76, 29, 149, 0.35)", VIOLET, sw=1, dash="4,4", rx=4, mask=True)
    text((COLS[0][0] + GRID_R) / 2, dy + 101,
         "跨云数据平台：Databricks（湖仓一体 · Mosaic AI） ｜ Snowflake（AI Data Cloud · Cortex AI）"
         " —— 三云均可部署，向上供训练数据与知识检索", VIOLET, 9.5, True)

    # ---- MCP 纵向工具总线（右侧） ----
    text(1330, 100, "MCP 工具调用总线", CYAN, 11, True)
    text(1330, 114, "Agent 纵向调用 工具 / 知识 / 数据", SLATE_L, 8)
    S.append(f'<line x1="{RAIL_X}" y1="124" x2="{RAIL_X}" y2="940" '
             f'stroke="{CYAN}" stroke-width="2" stroke-dasharray="6,4"/>')
    taps = [
        (142, "in",  "SaaS 工具", "= MCP Server（被调用）"),
        (384, "out", "Agent 平台", "= MCP Client（发起调用）"),
        (658, "in",  "知识检索", "= MCP Server（被调用）"),
        (916, "in",  "数据查询", "= MCP Server（被调用）"),
    ]
    for ty, dr, l1, l2 in taps:
        if dr == "in":     # 总线 → 层（Agent 经总线调到该层）
            line(RAIL_X, ty, GRID_R + 6, ty, CYAN, w=1.5, dash="4,3", end=True)
        else:              # 层 → 总线（Agent 发起）
            line(GRID_R + 4, ty, RAIL_X - 2, ty, CYAN, w=1.5, dash="4,3", end=True)
        S.append(f'<circle cx="{RAIL_X}" cy="{ty}" r="3.5" fill="{CYAN}"/>')
        text(RAIL_X + 14, ty - 3, l1, "white", 9, True, anchor="start")
        text(RAIL_X + 14, ty + 10, l2, SLATE_L, 8, anchor="start")

    # ---- 图例 ----
    ly = 1134
    S.append(f'<line x1="30" y1="{ly}" x2="58" y2="{ly}" stroke="{CYAN}" '
             f'stroke-width="2" stroke-dasharray="6,4"/>')
    text(66, ly + 4, "MCP · 纵向：Agent → 工具/知识/数据", SLATE_L, 9, anchor="start")
    S.append(f'<line x1="330" y1="{ly}" x2="358" y2="{ly}" stroke="{ORANGE}" '
             f'stroke-width="2" stroke-dasharray="6,4"/>')
    text(366, ly + 4, "A2A · 横向：Agent ⇄ Agent（跨云）", SLATE_L, 9, anchor="start")
    S.append(f'<line x1="614" y1="{ly}" x2="642" y2="{ly}" stroke="{SLATE}" stroke-width="2"/>')
    text(650, ly + 4, "数据 / 算力供给流", SLATE_L, 9, anchor="start")
    S.append(f'<rect x="800" y="{ly - 6}" width="16" height="11" rx="2" '
             f'fill="rgba(136, 19, 55, 0.4)" stroke="{ROSE}"/>')
    text(824, ly + 4, "安全治理检查点（全调用必经）", SLATE_L, 9, anchor="start")
    S.append(f'<rect x="1080" y="{ly - 6}" width="16" height="11" rx="2" '
             f'fill="rgba(251, 146, 60, 0.22)" stroke="{ORANGE}"/>')
    text(1104, ly + 4, "Agent 时代新增核心层", SLATE_L, 9, anchor="start")

    return "\n        ".join(S)


HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 原生层次化架构 · Agent 时代</title>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js" integrity="sha384-ZZ1pncU3bQe8y31yfZdMFdSpttDoPmOZg2wguVK9almUodir1PghgT0eY7Mrty8H" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js" integrity="sha384-en/ztfPSRkGfME4KIm05joYXynqzUgbsG5nMrj/xEFAHXkeZfO3yMK8QQ+mP7p1/" crossorigin="anonymous"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'JetBrains Mono', 'PingFang SC', 'Microsoft YaHei', monospace;
      background: #020617; min-height: 100vh; padding: 2rem; color: white;
    }
    .container { max-width: 1500px; margin: 0 auto; }
    .header { margin-bottom: 2rem; }
    .header-row { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; }
    .pulse-dot { width: 12px; height: 12px; background: #22d3ee; border-radius: 50%;
                 animation: pulse 2s infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    h1 { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.025em; }
    .subtitle { color: #94a3b8; font-size: 0.875rem; margin-left: 1.75rem; }
    .diagram-container { background: rgba(15, 23, 42, 0.5); border-radius: 1rem;
                         border: 1px solid #1e293b; padding: 1.5rem; overflow-x: auto; }
    svg { width: 100%; min-width: 1100px; display: block; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
             gap: 1rem; margin-top: 2rem; }
    .card { background: rgba(15, 23, 42, 0.5); border-radius: 0.75rem;
            border: 1px solid #1e293b; padding: 1.25rem; }
    .card-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem; }
    .card-dot { width: 8px; height: 8px; border-radius: 50%; }
    .card-dot.cyan { background: #22d3ee; }
    .card-dot.orange { background: #fb923c; }
    .card-dot.rose { background: #fb7185; }
    .card h3 { font-size: 0.875rem; font-weight: 600; }
    .card ul { list-style: none; color: #94a3b8; font-size: 0.75rem; }
    .card li { margin-bottom: 0.375rem; }
    .footer { text-align: center; margin-top: 1.5rem; color: #475569; font-size: 0.75rem; }
    .toolbar { display: flex; gap: 0.5rem; margin-left: auto; flex-shrink: 0; align-items: center; }
    .toolbar-toggle { background: transparent; border: none; color: #475569; cursor: pointer;
                      font-size: 1.25rem; line-height: 1; padding: 0.25rem 0.5rem;
                      border-radius: 0.375rem; transition: color 0.2s, background 0.2s; }
    .toolbar-toggle:hover { color: #94a3b8; background: rgba(30, 41, 59, 0.5); }
    .toolbar-actions { display: none; gap: 0.5rem; }
    .toolbar.expanded .toolbar-actions { display: flex; }
    .toolbar-actions button { background: rgba(30, 41, 59, 0.8); border: 1px solid #334155;
                              color: #94a3b8; padding: 0.375rem 0.75rem; border-radius: 0.375rem;
                              font-family: inherit; font-size: 0.75rem; cursor: pointer;
                              transition: all 0.2s; white-space: nowrap; }
    .toolbar-actions button:hover { background: rgba(51, 65, 85, 0.8); color: white;
                                    border-color: #475569; }
    @media print { body { background: #020617; padding: 1rem; }
                   .toolbar { display: none !important; } }
  </style>
</head>
<body>
  <div class="container" id="report-container">
    <div class="header">
      <div class="header-row">
        <div class="pulse-dot"></div>
        <h1>AI 原生层次化架构 · Agent 时代</h1>
        <div class="toolbar">
          <div class="toolbar-actions">
            <button onclick="copyAsImage(this)">📋 Copy</button>
            <button onclick="downloadPNG(this)">🖼️ PNG</button>
            <button onclick="downloadPDF(this)">📄 PDF</button>
          </div>
          <button class="toolbar-toggle" onclick="this.parentElement.classList.toggle('expanded')" title="Export options" aria-label="Export options">⋯</button>
        </div>
      </div>
      <p class="subtitle">Google Cloud × AWS × Azure 八层收敛 —— MCP 纵向串联（Agent → 工具 / 知识 / 数据）· A2A 横向串联（Agent ⇄ Agent · 跨云）</p>
    </div>

    <div class="diagram-container">
      <svg viewBox="0 0 %VB_W% %VB_H%" xmlns="http://www.w3.org/2000/svg">
        %SVG%
      </svg>
    </div>

    <div class="cards">
      <div class="card">
        <div class="card-header">
          <div class="card-dot cyan"></div>
          <h3>MCP —— 纵向串联（Agent → 工具 / 数据）</h3>
        </div>
        <ul>
          <li>• Agent 平台层是 MCP Client，统一发起工具调用</li>
          <li>• SaaS 工具、知识检索、数据查询以 MCP Server 暴露</li>
          <li>• 每次调用必经 AI 安全治理层：护栏 · 身份 · 审计</li>
          <li>• 三云原生支持：AgentCore Gateway / ADK / Foundry</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-dot orange"></div>
          <h3>A2A —— 横向串联（Agent ⇄ Agent）</h3>
        </div>
        <ul>
          <li>• SaaS 内嵌 Agent 与企业 Agent 跨边界协作</li>
          <li>• 应用层把任务委派给平台层的多 Agent 编排</li>
          <li>• 跨云跨厂商互操作：GCP ⇄ AWS ⇄ Azure</li>
          <li>• Google 发起、Linux 基金会托管，三云共同支持</li>
        </ul>
      </div>
      <div class="card">
        <div class="card-header">
          <div class="card-dot rose"></div>
          <h3>八层收敛与新控制点</h3>
        </div>
        <ul>
          <li>• 数据（供模型训练）与知识（供 Agent 调用）分离</li>
          <li>• Tokens 工厂层：数据 + 算力 → 智能（tokens）</li>
          <li>• Databricks / Snowflake 跨云供数，中立数据平台</li>
          <li>• Agent 平台层是 Agent 时代新的控制点</li>
        </ul>
      </div>
    </div>

    <p class="footer">
      AI 原生架构 · Agent 时代三大云分层对标（截至 2026-07 公开信息） · chenliang
    </p>
  </div>

  <script>
    async function copyAsImage(btn) {
      const orig = btn.textContent;
      try {
        const el = document.getElementById('report-container');
        const r = el.getBoundingClientRect();
        const pad = 32;
        const canvas = await html2canvas(document.body, { backgroundColor: '#020617', scale: 2, useCORS: true, ignoreElements: (e) => e.classList && e.classList.contains('toolbar'), x: r.left + window.scrollX - pad, y: r.top + window.scrollY - pad, width: r.width + pad * 2, height: r.height + pad * 2 });
        const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
        btn.textContent = '✓ Copied!';
      } catch (e) { btn.textContent = '✗ Failed'; }
      setTimeout(() => btn.textContent = orig, 2000);
    }
    async function downloadPNG(btn) {
      const orig = btn.textContent;
      btn.textContent = '⏳ ...';
      try {
        const el = document.getElementById('report-container');
        const r = el.getBoundingClientRect();
        const pad = 32;
        const canvas = await html2canvas(document.body, { backgroundColor: '#020617', scale: 2, useCORS: true, ignoreElements: (e) => e.classList && e.classList.contains('toolbar'), x: r.left + window.scrollX - pad, y: r.top + window.scrollY - pad, width: r.width + pad * 2, height: r.height + pad * 2 });
        const link = document.createElement('a');
        link.download = 'ai-native-architecture.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
        btn.textContent = '✓ Done!';
      } catch (e) { btn.textContent = '✗ Failed'; }
      setTimeout(() => btn.textContent = orig, 2000);
    }
    async function downloadPDF(btn) {
      const orig = btn.textContent;
      btn.textContent = '⏳ ...';
      try {
        const el = document.getElementById('report-container');
        const r = el.getBoundingClientRect();
        const pad = 32;
        const canvas = await html2canvas(document.body, { backgroundColor: '#020617', scale: 2, useCORS: true, ignoreElements: (e) => e.classList && e.classList.contains('toolbar'), x: r.left + window.scrollX - pad, y: r.top + window.scrollY - pad, width: r.width + pad * 2, height: r.height + pad * 2 });
        const imgData = canvas.toDataURL('image/png');
        const { jsPDF } = window.jspdf;
        const orientation = canvas.width > canvas.height ? 'landscape' : 'portrait';
        const pdf = new jsPDF({ orientation, unit: 'px', format: [canvas.width, canvas.height], hotfixes: ['px_scaling'] });
        pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
        pdf.save('ai-native-architecture.pdf');
        btn.textContent = '✓ Done!';
      } catch (e) { btn.textContent = '✗ Failed'; }
      setTimeout(() => btn.textContent = orig, 2000);
    }
  </script>
</body>
</html>
"""


def main():
    svg = build_svg()
    html = (HEAD.replace("%VB_W%", str(VB_W)).replace("%VB_H%", str(VB_H))
            .replace("%SVG%", svg))
    path = os.path.join(OUT, "AI原生架构图.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("saved:", path)


if __name__ == "__main__":
    main()
