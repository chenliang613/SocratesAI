# -*- coding: utf-8 -*-
"""
AWS Bedrock 详细分析 deck：按 AI 服务分层，逐层拆解 Bedrock 的产品架构、
定价机制、竞争格局与战略逻辑。数据截至 2026 年中。
复用 ppt_kit 的设计系统与版式模板。运行：python build_aws_bedrock.py
"""
import os
from ppt_kit import (new_prs, cover, toc, cards, two_col, steps, takeaways, closing, save,
                     R, BLUE, TEAL, PURPLE, AMBER, CORAL, SKY, GREY, INK)

OUT = "/Users/apple/SocratesAI/output"
os.makedirs(OUT, exist_ok=True)
AUTHOR = "chenliang  ·  2026-07"

# 分层配色：模型=PURPLE 推理=BLUE 定制=SKY 知识=TEAL Agent=CORAL 治理=AMBER


def deck_bedrock():
    prs = new_prs()
    T = 19
    F = "AWS Bedrock 详细分析 · AI 服务六层拆解 · 数据截至 2026 年中"

    # ---- 1 封面 ----
    cover(prs, "AWS BEDROCK · 云服务详细分析", "AWS Bedrock", "生成式 AI 平台拆解",
          [R("模型货架 · 推理电网 · 定制 · 知识 · ", 19, GREY),
           R("Agent 运行时 · 治理", 19, AMBER, True)],
          ["Bedrock 已从「几个模型前面的一层 API 代理」，长成一个完整的企业 AI 平台：",
           "近百个 Serverless 模型、托管 RAG、Agent 云底座 AgentCore——本报告逐层拆解。"],
          AUTHOR, accent=PURPLE)

    # ---- 2 目录 ----
    toc(prs, [
        ("01", "服务概述", "Bedrock 是什么：三年演进史与栈中定位", BLUE),
        ("02", "六层框架", "一个 API 之下的 AI 服务分层地图", PURPLE),
        ("03", "模型层", "近百个 Serverless 模型的货架逻辑", CORAL),
        ("04", "推理层", "五种推理形态与真实定价", SKY),
        ("05", "定制层", "微调 / 蒸馏 / 自带模型的取舍", TEAL),
        ("06", "知识层", "Knowledge Bases：托管 RAG 的全链路", AMBER),
        ("07", "Agent 层", "Agents / Flows / AgentCore 深拆", BLUE),
        ("08", "治理层", "Guardrails 与企业级信任体系", CORAL),
        ("09", "生态与竞争", "AWS 内部协同 + 三强对比 + 优劣势", PURPLE),
        ("10", "关键判断", "五个必须记住的结论", AMBER),
    ], 2, T, F)

    # ---- 3 发展沿革 ----
    steps(prs, "01 服务概述", "三年演进：从 API 代理到企业 AI 平台",
          "Bedrock 2023 年 9 月 GA 至今三年，每年完成一次能力跃迁：先聚合模型，再长出 RAG 与治理，最后押注 Agent 运行时。", [
        ("2023", "聚合模型", "4 月预览、9 月 GA：统一 API 接入 Anthropic / AI21 / Stability / Titan；年底 Agents、Knowledge Bases 上线", BLUE),
        ("2024", "补齐平台", "Guardrails GA、模型评估、Prompt 管理与 Flows；12 月发布自研 Nova 系列与 Bedrock Marketplace（100+ 专业模型）", TEAL),
        ("2025", "押注 Agent", "AgentCore 7 月预览、10 月 GA；re:Invent 一次上新 18 个开源权重模型；Serverless 模型近 100 个", CORAL),
        ("2026", "走向纵深", "全托管 Knowledge Base（6 月 GA）、AgentCore Policy / Evaluations / Payments、Agent Registry、强化微调扩展到 GPT-OSS / Qwen3", PURPLE),
    ], 3, T, F,
          bottom=("演进主线：", "每一步都在把「模型能力」封装成「运营能力」——模型本身从主角逐渐退居为平台上的可替换部件。"))

    # ---- 4 三层栈定位 ----
    steps(prs, "01 服务概述", "AWS 生成式 AI 三层栈：Bedrock 是中间层的唯一承载",
          "AWS 官方将生成式 AI 栈分为三层，服务三类客户。Bedrock 独占中间层，是 AWS 生成式 AI 战略的营收与叙事重心。", [
        ("底层 · 基础设施", "自己造模型", "EC2 GPU（NVIDIA）、自研 Trainium2 / Inferentia 芯片、SageMaker AI 训练平台；Project Rainier 数十万芯片集群供 Anthropic 训练 Claude——按算力计费", BLUE),
        ("中间层 · Bedrock", "用模型造应用", "统一 API 聚合多厂商模型 + 定制、RAG、Agent、治理等托管能力；企业开发者的主入口——按 token / 容量计费", PURPLE),
        ("顶层 · 应用", "直接要结果", "Amazon Q Developer / Q Business、Q in Connect 等成品应用，自身构建在 Bedrock 之上——按席位计费", AMBER),
    ], 4, T, F,
          bottom=("对标关系：", "Bedrock ↔ Azure AI Foundry ↔ Google Vertex AI。三家共同的判断：多数企业不会自己训模型，中间层（模型即服务）才是企业预算主入口。"))

    # ---- 5 六层总览 ----
    takeaways(prs, "02 六层框架", "Bedrock 内部：一个 API 之下的六层 AI 服务", [
        ("① 基础模型层", "近 100 个 Serverless 模型 + Marketplace 100+ 专业模型：Amazon Nova、Anthropic Claude、Meta Llama、Mistral、DeepSeek、Qwen、OpenAI 开源权重（GPT-OSS）、Google Gemma 等"),
        ("② 推理服务层", "Converse / InvokeModel 统一 API；按需、预置吞吐、批量（五折）、提示词缓存（省 90%）、智能路由、跨区域推理——把推理做成水电煤"),
        ("③ 模型定制层", "微调、强化微调（RFT）、持续预训练、模型蒸馏、自定义模型导入——产出模型仍托管在 Bedrock，数据不出账户"),
        ("④ 数据知识层", "Knowledge Bases 托管 RAG（2026.6 全托管 GA：向量库、嵌入、重排一体）+ Bedrock Data Automation 非结构化数据处理 + GraphRAG"),
        ("⑤ Agent 编排层", "Bedrock Agents、多 Agent 协作、Flows 可视化编排；AgentCore（Runtime / Memory / Gateway / Identity / Policy / Evaluations）承接任意框架的生产级 Agent"),
        ("⑥ 治理安全层", "Guardrails 内容护栏（含 Automated Reasoning 可证明校验）、模型评估、水印检测、KMS / PrivateLink / 合规认证——横切所有层"),
    ], 5, T, F)

    # ---- 6 模型层：货架 ----
    cards(prs, "03 模型层", "模型货架：近 100 个 Serverless 模型的「不押注」策略",
          "Bedrock 的第一性选择是「货架而非单一模型」：自研保底价、投资绑旗舰、开源补长尾、Marketplace 收长尾流量——2025 年 12 月一次上架 18 个开源权重模型，为史上最大扩容。", [
        ("自研 · Amazon Nova", "价格锚点", "Micro / Lite / Pro / Premier 文本多模态 + Canvas（图）/ Reel（视频）/ Sonic（语音）——以极低单价守住成本敏感场景", PURPLE),
        ("旗舰 · Anthropic Claude", "能力天花板", "AWS 累计投资 80 亿美元；Claude 是 Bedrock 事实旗舰，Opus / Sonnet / Haiku 全系首发同步上架", CORAL),
        ("开源权重阵营", "长尾覆盖", "Meta Llama、Mistral、DeepSeek、Qwen3、OpenAI GPT-OSS、Google Gemma、Cohere、AI21、Stability——开源模型全托管化", BLUE),
        ("Marketplace", "专业模型", "100+ 行业与专业模型（医疗、金融、蛋白质、时序…），统一走 Bedrock API 与安全体系，按需拉起专用算力", TEAL),
        ("统一接入", "一次集成", "所有模型共用一套 API / SDK / IAM / 计费，切换模型只改 model ID——选型权与议价权留在客户手里", SKY),
        ("自定义导入", "自带模型", "自己微调的 Llama / Mistral / Qwen 架构权重可导入托管，与官方模型同栈运行，Serverless 计费", AMBER),
    ], 6, T, F, ncols=3,
          bottom=("与 Azure 对照：", "Azure 深度绑定 OpenAI 一家，Bedrock 用「模型中立」把模型间的竞争转化为自己的流量——模型会贬值，货架不会。"))

    # ---- 7 双引擎 two_col ----
    two_col(prs, "03 模型层", "双引擎：自研 Nova 守成本，投资 Claude 攻高端",
            "货架需要「锚」。Bedrock 用两个引擎覆盖价格-能力光谱的两端，其余模型填充中间地带。",
            ("Amazon Nova · 自研引擎", PURPLE, [
                "Micro $0.035 / Lite $0.06 / Pro $0.80（每百万输入 token）——同档能力下显著低价",
                "多模态全覆盖：文本、图像（Canvas）、视频（Reel）、语音到语音（Sonic）",
                "定制最开放：微调、蒸馏、持续预训练全支持，是定制层的默认底座",
                "战略角色：守住「够用就好」的海量企业场景，防止低端被开源自建分流",
            ]),
            ("Anthropic Claude · 投资引擎", CORAL, [
                "Opus 4.6 $5/$25、Sonnet 4.6 $3/$15、Haiku 4.5 $1/$5（每百万 token 输入/输出）",
                "Bedrock 上事实的旗舰：编码、Agent、长上下文场景的默认选择",
                "AWS 累计投资 80 亿美元；Project Rainier Trainium 集群反哺 Claude 训练——算力换股权换独家性",
                "战略角色：对抗 Azure-OpenAI 组合的能力天花板，撑住高端叙事",
            ]),
            7, T, F,
            bottom=("组合含义：", "Nova 保证「不依赖别人也能开张」，Claude 保证「最好的模型也在我家」——两头都不押死，风险与收益都对冲。"))

    # ---- 8 推理层 ----
    cards(prs, "04 推理层", "推理即电网：一套 API，五种供电模式",
          "推理层是 Bedrock 的营收主体。围绕「稳定、便宜、低延迟」提供多种消费形态——类似电网的峰谷电价、包月专线与错峰用电。", [
        ("统一 API", "Converse / InvokeModel", "对话、流式、多模态、工具调用一套接口通吃所有模型；SDK 与 LangChain / LlamaIndex 原生集成；OpenAI 兼容端点降低迁移成本", BLUE),
        ("按需 On-Demand", "默认模式", "严格按 token 计费、零承诺零最低消费；跨区域推理（Cross-Region）自动分流峰值，全球端点提升可用性", PURPLE),
        ("预置吞吐 Provisioned", "包月专线", "按「模型单元」小时计费，1 / 6 个月承诺（约 $21–50/小时/单元）——为生产级稳定流量买确定性", SKY),
        ("批量 Batch", "错峰五折", "S3 递交 JSONL 异步处理、24 小时内返回，价格为按需的 50%——评估、打标、批量摘要等离线场景的默认选择", TEAL),
        ("提示词缓存", "重复上下文省 90%", "缓存命中部分输入价格降至 1/10；长系统提示、多轮对话、RAG 场景收益最大", AMBER),
        ("智能路由 + 低延迟", "自动省钱", "Intelligent Prompt Routing 按请求难度自动路由到够用的最便宜模型（同族省最高 30%）；Latency-Optimized 推理服务实时场景", CORAL),
    ], 8, T, F, ncols=3,
          bottom=("电网逻辑：", "推理形态越丰富，客户的成本结构就越依赖平台的调度能力——「电网级」运营是超大规模云厂商对模型创业公司的真正壁垒。"))

    # ---- 9 定价 ----
    cards(prs, "04 推理层", "真实定价：token 价格战下的价格光谱（2026）",
          "每百万 token（输入/输出）计价。三个数量级的价格光谱让「模型选型」变成一道成本工程题——这正是智能路由与蒸馏存在的理由。", [
        ("旗舰档", "Claude Opus 4.6 · $5 / $25", "Sonnet 4.6 $3/$15；复杂推理、编码、Agent 场景——单位任务价值高，贵得起", CORAL),
        ("主力档", "Claude Haiku 4.5 · $1 / $5", "Nova Pro $0.80/$3.20；日常对话、摘要、客服——性能价格比的主战场", BLUE),
        ("走量档", "Nova Lite · $0.06 / $0.24", "Nova Micro $0.035/$0.14；分类、抽取、路由等高频小任务——比旗舰便宜两个数量级", TEAL),
        ("降本组合拳", "叠加可省 70%+", "批量五折 × 缓存省 90% × 智能路由省 30% × 蒸馏后小模型跑大模型的活——账单优化空间巨大", AMBER),
    ], 9, T, F, ncols=2,
          bottom=("商业观察：", "模型单价三年降了一个数量级，但用量涨得更快——Bedrock 赌的是「杰文斯悖论」：越便宜，用得越多，总盘子越大。"))

    # ---- 10 定制层 ----
    cards(prs, "05 定制层", "定制：让通用模型长出企业私有能力",
          "定制层解决「通用模型不懂我的业务」。由轻到重五条路径，全部托管化：产出模型留在 Bedrock 内运行，训练数据不出客户账户、不回流基础模型。", [
        ("微调 Fine-tuning", "轻定制", "标注数据调整行为与格式，适配领域术语与输出规范；支持 Nova、Claude Haiku、Llama、GPT-OSS 20B、Qwen3 32B 等；支持在已定制模型上迭代微调", SKY),
        ("强化微调 RFT", "新范式", "2026 年扩展到 GPT-OSS / Qwen3：以自动化强化学习工作流对齐业务目标，不需要人工偏好标注团队——定制门槛大幅下降", PURPLE),
        ("持续预训练", "深定制", "海量无标注领域语料继续预训练，让模型「读完」企业的行业文献——医疗、法律、金融等深度领域适配", TEAL),
        ("模型蒸馏", "降本利器", "大模型（教师）自动生成数据训练小模型（学生），以约 1/5 推理成本获得接近旗舰的领域表现——与走量档定价形成组合", BLUE),
        ("自定义模型导入", "自带模型", "在 SageMaker 或任何地方训练的开源架构权重导入 Bedrock，Serverless 托管、按需计费——训练自由 + 运维托管两头兼得", AMBER),
        ("与 SageMaker 分界", "轻重分流", "重度自研训练（自定义架构、大规模预训练）走 SageMaker；「以用为主、轻量定制」留在 Bedrock——两个入口互为漏斗", CORAL),
    ], 10, T, F, ncols=3,
          bottom=("定制的本质：", "把「模型能力差异」转化为「数据资产差异」——定制越深，模型越不可替换，客户与平台互相锁定。"))

    # ---- 11 知识层 ----
    cards(prs, "06 知识层", "Knowledge Bases + Data Automation：托管 RAG 全链路",
          "模型的价值取决于能接触的数据。Bedrock 把 RAG 从「工程项目」压缩成「配置项」，2026 年 6 月全托管 Knowledge Base GA 后连向量库也不用自己管。", [
        ("Knowledge Bases", "托管 RAG 流水线", "文档摄取、切分、向量化、检索、重排、引用溯源全自动；数据源覆盖 S3、Confluence、SharePoint、Salesforce、Web 爬虫", AMBER),
        ("全托管模式（2026.6 GA）", "零基础设施", "向量存储、嵌入模型、重排与检索优化全部由 Bedrock 托管并自动扩缩容；支持 Agentic Retrieval 多跳推理检索与多模态摄取", CORAL),
        ("自选后端模式", "开放兼容", "OpenSearch Serverless、Aurora PostgreSQL（pgvector）、Neptune，及 Pinecone、Redis、MongoDB Atlas 等第三方向量库——不强绑", TEAL),
        ("Data Automation", "非结构化 ETL", "文档、图片、音视频批量转结构化数据（IDP 智能文档处理、媒体分析），直接喂给 RAG 与下游分析——解决「数据脏」的第一公里", BLUE),
        ("GraphRAG", "图谱增强", "Neptune 自动构建知识图谱辅助检索，跨文档关联推理显著优于朴素向量检索——复杂企业知识场景的差异化能力", PURPLE),
        ("结构化数据检索", "NL2SQL", "自然语言直接查询 Redshift / Glue 数据表，RAG 范围从文档扩展到数仓——打通「文档知识 + 业务数据」两个世界", SKY),
    ], 11, T, F, ncols=3,
          bottom=("战略意图：", "企业数据已在 S3 / Redshift 里——Bedrock 让「数据不动、智能上门」，数据引力反过来锁定数据继续留在 AWS。"))

    # ---- 12 Agent 编排层 ----
    cards(prs, "07 Agent 层", "从「回答问题」到「完成任务」：两代 Agent 产品并行",
          "Agent 层是 Bedrock 演进最快的一层，当前两代产品并行：内置 Agents / Flows 服务快速上手，AgentCore 承接生产级、任意框架的 Agent 工作负载。", [
        ("Bedrock Agents", "内置编排", "模型自动拆解任务、调用 Lambda / API、查询知识库、执行多步操作；托管编排循环与会话状态——低代码快速起步", CORAL),
        ("多 Agent 协作", "Supervisor 模式", "监督者 Agent 分派子 Agent 并行工作、汇总结果——把复杂流程拆成可独立演进的专家 Agent 组合", PURPLE),
        ("Flows", "可视化编排", "拖拽式把提示词、知识库、Agent、Lambda 串成确定性工作流——流程固定的业务自动化不需要「自由发挥」的 Agent", SKY),
        ("开放协议", "MCP / A2A", "Gateway 原生支持 MCP 工具接入与 Agent 间协议；Strands Agents 开源 SDK——不锁框架、不锁协议，意在做「所有 Agent 的运行环境」", BLUE),
    ], 12, T, F, ncols=2,
          bottom=("形态判断：", "Agents/Flows 是「Bedrock 里的功能」，AgentCore 是「独立的 Agent 云」——后者才是平台级卡位，下一页深拆。"))

    # ---- 13 AgentCore 深拆 ----
    takeaways(prs, "07 Agent 层", "AgentCore 深拆：企业 Agent 的「EC2 时刻」", [
        ("Runtime · 运行时", "microVM 会话级隔离、最长 8 小时长任务、按实际用量计费；框架无关——LangGraph、CrewAI、Strands、任意代码皆可托管，2025.10 GA"),
        ("Memory · 记忆", "长短期记忆托管；re:Invent 2025 情景记忆（Episodic）GA——Agent 自动沉淀用户偏好与历史事件，跨会话复用"),
        ("Gateway + Identity", "把企业 API / Lambda 一键转成 MCP 工具并托管鉴权；Identity 管理 Agent 的身份与最小权限——解决「Agent 能动什么」的安全命题"),
        ("Browser + Code Interpreter", "托管无头浏览器与沙箱代码执行——Agent 自主上网操作与跑代码的两大高危能力，以托管方式圈进安全边界"),
        ("Policy + Evaluations（2026 预览）", "自然语言定义行为边界，Gateway 逐动作强制校验；13 套预置评估器（正确性、安全、工具选择准确率…）持续度量 Agent 质量"),
        ("Registry + Payments + CLI", "Agent Registry 治理化的 Agent / 工具目录；Payments 让 Agent 可以安全付款（预览）；CLI + Managed Harness 支持会话挂起恢复与 IaC 部署"),
    ], 13, T, F)

    # ---- 14 治理层 ----
    cards(prs, "08 治理层", "Guardrails 与信任体系：横切六层，决定成交",
          "生成式 AI 进企业的最大阻力不是能力而是风险。治理层不直接产生营收，却是 CIO 签字的前提——Bedrock 在这层的投入密度全行业最高。", [
        ("Guardrails 内容护栏", "六类策略", "有害内容过滤（文本+图像）、自然语言定义禁止话题、词表过滤、PII 脱敏、上下文事实性校验拦截幻觉；独立于模型、任何调用皆可挂载；2024 年底降价 85% 后约 $0.15/千文本单元", CORAL),
        ("Automated Reasoning", "可证明的校验", "用形式化逻辑验证模型输出是否符合企业规则文档——从「概率上大概对」到「逻辑上可证明」，监管行业（金融、医疗）的关键卖点", PURPLE),
        ("模型评估", "选型度量", "自动指标 + 人工评估 + LLM-as-a-Judge，用企业自己的数据集横向比较模型——「选哪个模型」从信仰变成可度量决策", BLUE),
        ("数据边界与合规", "企业资质", "客户数据不用于训练基础模型；KMS 加密、PrivateLink 私网、VPC 隔离；CloudTrail / CloudWatch 全程审计；GDPR / HIPAA / SOC / ISO 随 AWS 体系继承", TEAL),
    ], 14, T, F, ncols=2,
          bottom=("竞争含义：", "对企业客户，「合规的 90 分模型」永远赢过「裸奔的 100 分模型」——治理层是 Bedrock 对阵纯模型 API 厂商的胜负手。"))

    # ---- 15 生态协同 ----
    cards(prs, "09 生态与竞争", "AWS 体系内协同：Bedrock 是枢纽而非孤岛",
          "Bedrock 的每一层都与 AWS 存量服务咬合——这既是产品设计，也是商业设计：Bedrock 的用量会自动带动存储、计算与数据服务的用量。", [
        ("向下 · 算力与训练", "SageMaker + 自研芯片", "SageMaker 训练的模型经 Custom Model Import 进 Bedrock 托管；Trainium2 降低推理成本——全栈自持让降价空间自己可控", BLUE),
        ("向上 · 成品应用", "Amazon Q 系列", "Q Developer（编码）、Q Business（企业搜索问答）构建在 Bedrock 之上——AWS 自己是 Bedrock 最大的客户与试验场", AMBER),
        ("横向 · 数据服务", "S3 / Redshift / Glue", "Knowledge Bases 直连 S3，NL2SQL 直连 Redshift，Data Automation 接 Glue——数据在哪，推理就在哪结算", TEAL),
        ("外围 · 生态市场", "Marketplace + Registry", "模型、Agent、工具三类资产上架交易；合作伙伴（埃森哲、德勤等 SI）批量复制行业方案——平台生意的飞轮", PURPLE),
    ], 15, T, F, ncols=2,
          bottom=("枢纽效应：", "每 1 美元 Bedrock 推理收入，都拖着数美元的存储、网络与数据服务收入——这是纯模型厂商没有的账。"))

    # ---- 16 三强对比 ----
    steps(prs, "09 生态与竞争", "三强对比：Bedrock vs Azure AI Foundry vs Vertex AI",
          "三家都在做「企业 AI 中间层」：模型目录 + 定制 + RAG + Agent + 治理。差异不在功能清单，而在各自的引力来源。", [
        ("AWS Bedrock", "数据引力", "强项：模型中立货架、企业数据在 S3 的存量、AgentCore 运行时最完整；弱项：自研模型心智弱、追赶者姿态。最适合 AWS 原生、数据重的企业", PURPLE),
        ("Azure AI Foundry", "办公引力", "强项：OpenAI 独家 + M365 / Copilot 渗透（财富 500 的 75% 是微软客户）；弱项：深度绑定单一模型厂商、议价权外置。最适合微软系企业", BLUE),
        ("Google Vertex AI", "自研引力", "强项：Gemini 全自研全栈、TPU 成本、BigQuery 数据科学生态最成熟；弱项：企业销售与信任积累最浅。最适合工程驱动的 GCP 组织", TEAL),
    ], 16, T, F,
          bottom=("格局判断：", "云市场 AWS 份额约 29%（2025Q3）仍居首但被追赶；企业普遍多云混布 2+ 平台——中间层的战争远未到终局。"))

    # ---- 17 优势与挑战 ----
    two_col(prs, "09 生态与竞争", "结构性优势与现实挑战",
            "Bedrock 按 token / 容量 / 定制训练量计费，是典型「用量型」生意。优势是结构性的，挑战也是真实的。",
            ("结构性优势", TEAL, [
                "数据引力：企业数据已在 AWS，就近推理迁移阻力最小，且推理反哺数据服务收入",
                "模型中立：近百模型货架 + Claude 旗舰，不受单一模型厂商绑架，客户议价权最大",
                "全栈自持：Trainium 芯片 → Nova 模型 → Bedrock 平台 → Q 应用，成本曲线自己可控",
                "Agent 先手：AgentCore 的运行时 / 记忆 / 策略 / 评估组合当前最完整，且框架协议全开放",
            ]),
            ("现实挑战", CORAL, [
                "自研模型弱势：Nova 心智不敌 GPT / Gemini，旗舰能力依赖投资关系（Anthropic）而非自有",
                "心智追赶：Azure 借 OpenAI 先占「企业 AI = Copilot」的叙事，Bedrock 品牌认知偏工程侧",
                "复杂度税：六层能力、两代 Agent 产品、多种定价并存——学习曲线陡，中小客户易流失",
                "利润挤压：token 价格战持续，模型层毛利趋薄——价值必须向 Agent / 数据 / 治理层迁移",
            ]),
            17, T, F,
            bottom=("商业本质：", "Bedrock 不靠模型赚钱，靠模型带动的推理用量、数据存储与上层服务——「卖铲子」升级为「卖电 + 卖电器 + 收物业费」。"))

    # ---- 18 关键判断 ----
    takeaways(prs, "10 关键判断", "关于 AWS Bedrock 的五个关键判断", [
        ("中间层是企业预算主入口", "三层栈中，底层算力同质化、顶层应用碎片化；「用模型造应用」的中间层承接最大企业预算——Bedrock 是 AWS 生成式 AI 战略的重心所在"),
        ("六层 = 价值上移的路线图", "模型引流 → 推理走量 → 定制加深 → 知识沉淀 → Agent 锁定 → 治理成交：越往上差异化越强、粘性越高、越难被单点替代"),
        ("「模型中立 + 数据引力」是护城河", "不与任何单一模型共存亡，让企业数据留在 AWS 成为智能化默认场所——模型可以换，数据搬不走，这是对 Azure-OpenAI 绑定模式的非对称打法"),
        ("下一战场在 Agent 运行时", "AgentCore 在复制 EC2 剧本：框架中立、按用量收费、把高危能力（浏览器 / 代码 / 支付）圈进托管安全边界——谁托管企业的 Agent，谁定义下一个十年的云"),
        ("风险在「借来的旗舰」", "能力天花板系于 Anthropic 投资关系；若旗舰模型格局生变，Nova 能否接住高端是 Bedrock 叙事的最大变数——观察指标：Nova 在旗舰基准上的追赶速度"),
    ], 18, T, F)

    # ---- 19 结语 ----
    closing(prs, "模型会贬值，货架与电网不会",
            ["Bedrock 的第一性原理：把模型封装成基础设施来运营——",
             "以中立货架聚合模型，以电网级推理规模化，以数据、Agent 与治理沉淀不可迁移的价值。"],
            "AWS Bedrock · 云服务详细分析", AUTHOR, accent=PURPLE)

    save(prs, os.path.join(OUT, "AWS Bedrock分析.pptx"))


if __name__ == "__main__":
    deck_bedrock()
