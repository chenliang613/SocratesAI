# -*- coding: utf-8 -*-
"""
AI 治理全生命周期分析（一页 PPT）。
按 AI 全生命周期四阶段（数据准备/数据工程 → 模型训练 → 智能体开发 → 行业应用部署），
对比六家厂商（Anthropic / OpenAI / Google / Microsoft / AWS / Salesforce）的
AI 安全治理能力布局。沿用 ppt_kit 的视觉语言（配色、字体、卡片样式），
但版式为单页 4x6 矩阵，非多页模板。

运行：python build_ai_governance_lifecycle.py  →  output/AI治理全生命周期分析.pptx

事实基线（截至 2026-07，公开资料）：
  Anthropic： RSP v3.0（ASL 阶梯）、宪法 AI、Constitutional Classifiers、
              Computer Use/Claude Agent SDK 沙箱、MCP 协议安全评审、企业级使用政策。
  OpenAI：    Preparedness Framework v2（High/Critical 阈值）、SAG 评估+CEO 否决权、
              Model Spec、外部红队网络、Agent 类产品按能力分级处理风险。
  Google：    DeepMind FSF v3、SAIF 2.0（含 Agent 场景）、Vertex AI 治理工具链、
              SynthID 溯源、Model Armor、Dataplex 数据治理。
  Microsoft： 负责任 AI 标准 v2、前沿治理框架（FGF）、与 OpenAI 共设部署安全委员会（DSB）、
              Prompt Shields、PyRIT 开源红队、负责任 AI 办公室（ORA）+年度透明度报告。
  AWS：       首家 ISO/IEC 42001 认证大型云厂商、前沿模型安全框架（FMSF）、
              Bedrock Guardrails/AgentCore/Automated Reasoning、Lake Formation + Macie。
  Salesforce：Einstein Trust Layer（脱敏/接地/毒性检测/护栏）、Agentforce 人工介入机制、
              道德人性化科技办公室、模型无关架构（不自研前沿基座模型）。
"""
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from ppt_kit import (new_prs, slide, header, rect, txt, oval, R, save,
                     BLUE, TEAL, PURPLE, AMBER, CORAL, SKY, INK, GREY, LGREY,
                     LINE, PANEL, WHITE, CLOUD, In)

FOOTER = "AI 治理全生命周期分析 · 数据工程 → 模型训练 → 智能体开发 → 行业部署 · 截至 2026-07"

# 厂商配色：模型实验室（Anthropic/OpenAI）→ 云厂商（Google/Microsoft/AWS）→ SaaS（Salesforce）
VENDORS = [
    ("Anthropic", "模型实验室", CORAL),
    ("OpenAI", "模型实验室", PURPLE),
    ("Google", "云 + 前沿研究", TEAL),
    ("Microsoft", "云 + 生态治理", SKY),
    ("AWS", "云基础设施", AMBER),
    ("Salesforce", "企业级 Agent", BLUE),
]

STAGES = [
    ("01", "数据准备/数据工程", "DATA & ENGINEERING"),
    ("02", "模型训练阶段", "MODEL TRAINING"),
    ("03", "智能体开发阶段", "AGENT DEVELOPMENT"),
    ("04", "行业应用部署阶段", "INDUSTRY DEPLOYMENT"),
]

# 四个阶段行标签的编号配色（与厂商配色相互独立）
STAGE_COLORS = [BLUE, TEAL, PURPLE, AMBER]

# 矩阵内容：CELLS[stage_idx][vendor_idx]，顺序与 VENDORS 一致
CELLS = [
    [
        "版权敏感的数据溯源与最小化采集，训练语料经甄别过滤，支持内容方 opt-out。",
        "数据来源与授权协议渐趋公开；API/企业数据默认不用于训练，符合 DPA。",
        "Dataplex 治理+差分隐私管道；SynthID 标注素材来源，全链路血缘可溯。",
        "负责任 AI 标准 v2 要求数据来源审查；Purview+合规管理器覆盖 Copilot 数据血缘。",
        "Lake Formation+Macie 自动识别 PII；Bedrock 默认不用客户数据训练。",
        "Data Cloud 零拷贝集成；Trust Layer 在数据入模前完成脱敏与毒性检测。",
    ],
    [
        "RSP v3.0 按 ASL 等级设阈值；宪法 AI 替代人工标注，Opus 4 首次激活 ASL-3。",
        "Preparedness v2 设 High/Critical 两档阈值；SAG 评估后 CEO 保留否决权。",
        "DeepMind FSF v3 覆盖操纵与抗关机风险；安全案例评审贯穿 Gemini 全系。",
        "前沿治理框架（FGF）对齐 NIST 四步循环；与 OpenAI 共设 DSB 联合把关发布。",
        "前沿模型安全框架（FMSF）约束 Nova；SageMaker Clarify 做偏见评测。",
        "不自研前沿基座模型，走模型无关架构；自有小模型遵循 AI 可接受使用政策。",
    ],
    [
        "Computer Use/Agent SDK 内置沙箱与权限确认；MCP 协议开放但设安全评审。",
        "Agent 类产品按能力分级处理风险；外部红队网络+沙箱限制越权操作。",
        "SAIF 2.0 扩展至 Agent 场景；Vertex Agent Builder+Model Armor 防注入。",
        "Copilot Studio 内置 Prompt Shields 防注入；PyRIT 开源红队支撑 Agent 测试。",
        "Bedrock AgentCore 提供隔离运行时；Guardrails+Automated Reasoning 验证行动。",
        "Agentforce 由 Trust Layer 全程把关：动态接地、提示防御，高风险动作强制人工介入。",
    ],
    [
        "分行业使用政策限制高风险场景；宪法分类器护栏支撑企业级部署与问责。",
        "Model Spec 公开应答准则；企业版增设数据保留控制，无年度综合透明度报告。",
        "Vertex AI 合规工具覆盖医疗/金融；模型卡+进展报告，SynthID 保障内容溯源。",
        "负责任 AI 办公室（ORA）+年度透明度报告制度化最强；Limited Access 门禁高风险场景。",
        "首家获 ISO/IEC 42001 认证并通过零缺陷监督审计；ApplyGuardrail API 跨模型套用。",
        "道德人性化科技办公室监督；Trust Layer 审计留痕，行业合规内嵌 Health/Financial Cloud。",
    ],
]

prs = new_prs()
s = slide(prs)
SW, SH = prs.slide_width, prs.slide_height

header(s, prs, "AI GOVERNANCE · FULL LIFECYCLE",
       "AI 治理全生命周期能力对比：Anthropic × OpenAI × Google × Microsoft × AWS × Salesforce",
       1, 1, FOOTER)

txt(s, In(0.85), In(1.28), In(11.6), In(0.32),
    [[R("同一张全生命周期地图，三种打法：模型实验室重训练期治理，云厂商重合规与护栏产品化，SaaS 厂商把治理前移到应用层。",
        12, GREY)]], line_spacing=1.1)

# ---------------- 矩阵几何 ----------------
x0 = In(0.85)
row_label_w = In(1.35)
col_gap = In(0.1)
n_vendors = len(VENDORS)
grid_w = SW - 2 * x0
vendor_col_w = (grid_w - row_label_w - (n_vendors - 1) * col_gap) / n_vendors

grid_top = In(1.7)
bottom_reserve = In(0.85)          # 底部结论条 + footer 之间的空间
col_header_h = In(0.46)
row_gap = In(0.08)
n_stages = len(STAGES)
avail_h = (SH - In(0.32)) - grid_top - bottom_reserve
row_h = (avail_h - col_header_h - row_gap - (n_stages - 1) * row_gap) / n_stages

# ---------------- 列头（厂商） ----------------
col_header_y = grid_top
for j, (name, tag, color) in enumerate(VENDORS):
    x = x0 + row_label_w + col_gap + j * (vendor_col_w + col_gap)
    rect(s, x, col_header_y, vendor_col_w, col_header_h, color, round_=True)
    txt(s, x, col_header_y + In(0.03), vendor_col_w, In(0.24),
        [[R(name, 12.5, WHITE, True)]], align=PP_ALIGN.CENTER)
    txt(s, x, col_header_y + In(0.26), vendor_col_w, In(0.18),
        [[R(tag, 7.5, CLOUD)]], align=PP_ALIGN.CENTER)

# ---------------- 行 + 单元格 ----------------
rows_top = col_header_y + col_header_h + row_gap
for i, (no, stage_name, stage_en) in enumerate(STAGES):
    y = rows_top + i * (row_h + row_gap)
    sc = STAGE_COLORS[i]

    # 行标签
    rect(s, x0, y, row_label_w, row_h, PANEL, round_=True)
    rect(s, x0, y, In(0.08), row_h, sc, round_=True)
    oval(s, x0 + In(0.18), y + In(0.14), In(0.36), sc)
    txt(s, x0 + In(0.18), y + In(0.14), In(0.36), In(0.36),
        [[R(no, 12.5, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x0 + In(0.12), y + In(0.56), row_label_w - In(0.22), row_h - In(0.62),
        [[R(stage_name, 10.5, INK, True)], [R(stage_en, 7, LGREY)]],
        align=PP_ALIGN.CENTER, line_spacing=1.05)

    # 六个厂商单元格
    for j in range(n_vendors):
        x = x0 + row_label_w + col_gap + j * (vendor_col_w + col_gap)
        _, _, color = VENDORS[j]
        rect(s, x, y, vendor_col_w, row_h, WHITE, line=LINE, round_=True, shadow=True)
        rect(s, x, y, In(0.06), row_h, color, round_=True)
        txt(s, x + In(0.14), y + In(0.1), vendor_col_w - In(0.26), row_h - In(0.2),
            [[R(CELLS[i][j], 8.5, GREY)]], line_spacing=1.12)

# ---------------- 底部结论条 ----------------
concl_y = SH - In(0.32) - In(0.62)
rect(s, x0, concl_y, grid_w, In(0.5), INK, round_=True)
txt(s, x0 + In(0.28), concl_y, In(1.5), In(0.5),
    [[R("全局判断", 12.5, SKY, True)]], anchor=MSO_ANCHOR.MIDDLE)
txt(s, x0 + In(1.7), concl_y, grid_w - In(1.95), In(0.5),
    [[R("Anthropic/OpenAI 的治理重心在训练期（RSP/Preparedness 阈值把关）；Google/Microsoft/AWS 把治理产品化为云端合规与护栏；"
        "Salesforce 把治理前移到应用层的数据脱敏与人工介入——六段能力彼此互补，而非相互替代。",
        10, CLOUD)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.12)

save(prs, "/Users/apple/SocratesAI/output/AI治理全生命周期分析.pptx")
