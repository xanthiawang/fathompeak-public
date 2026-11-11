# B. 海外推理 / 模型 API 平台与聚合器：产品线、定价与销路

沐仞科技内部竞品资料｜12 家｜2026-11-02 整理

**范围。** Together AI、Fireworks AI、OpenRouter、Groq、Baseten、DeepInfra、Novita AI、Replicate、Modal、Cerebras、SambaNova、fal。

**口径。**

- **日期：** 带「访问 2026-11-02」的是本次在线抓取；Together、Fireworks、OpenRouter 的细节价目沿用本地 10-14 / 10-21 快照（见 `../全部竞品_产品收费与定价_2026-10-21.qmd` 与 `../硅基流动与海外同类/`），本次只补新变化。
- **单位：** 美元；"M"＝百万 Token；GPU 价格统一换成"美元/卡时"。
- **标记：** 【官】公司官网/新闻稿/SEC 文件；【媒】可信媒体；【三方】Sacra 等第三方估算或价格追踪站；【传】报道中的谈判、未完成；【算】我自己换算；【判断】分析判断；【待核实】只有弱来源或互相矛盾。
- 没查到的数字一律写"未公开"，不估。

---

## 0. 一页总览

| 公司 | 产品线 | 计费方式 | 代表价格（访问日见各节） | 解决方案 / 主打场景 | 销路 |
|---|---|---|---|---|---|
| **Together AI** | Serverless 推理、Batch、预留吞吐、专属推理、GPU 集群（Instant / 预留）、微调与 Post-training/RL、代码沙箱、存储、Together Link、AI Factory | 按 Token；按卡时；按 vCPU 时；按 GiB；全部预付 | GLM-5.3 1.40/4.40；Batch 5 折；H100 集群按需 3.99、可抢占 1.99、预留 3.19–3.69；专属推理 H100 5.49、B200 8.99；B200 Post-training 按需 11.00（首发价 9.00） | 开源模型替代闭源（编码代理、客服 Agent）、训练到推理全周期、主权/区域 AI 工厂 | 自助预付 + SDE 转大单；Strategic AE + FDE；AWS Marketplace、Hugging Face、OpenRouter；模型厂首发（月之暗面）；Startup Accelerator；研究品牌（FlashAttention） |
| **Fireworks AI** | Serverless（Standard/Priority/Fast/US-only 四档）、Batch、按需 GPU 部署、预留吞吐、BYOC、训练（SFT/DPO/RFT/Training API）、Nexus、FireRouter | 按 Token（分速度/区域档）；按 GPU 秒；按训练 Token；预留按美元/分钟 | Kimi K3 Standard 3/15、Fast 与 US-only 4.50/22.50；Batch 5 折；H100/H200 8.00、B200 13.00、B300 15.00、GB300 20.00 /卡时；SFT/DPO 0.5–40 /M 训练 Token | "Own your AI"：用客户数据训练专用模型；AI 编程（Nexus）；低延迟产品体验 | 自助 Tier 1–4 → 企业 AE（AI 原生 / 企业两线）；AWS SCA、AWS/GCP Marketplace、微软 Foundry；咨询伙伴（BCG、Deloitte）；创业计划；Discord；DevDay / Forge 大会 |
| **OpenRouter**（已被 Stripe 宣布收购） | 统一 API 接 600+ 模型 / 80+ 供应商、自动路由、BYOK、预算与管理 API、私有端点 | **不定价**：按供应商标价 + 买 credit 时收平台费 | Standard 5.5%、Business 8%、Enterprise 合同折扣；BYOK 每月 2.5 万美元标价用量内免费，超出 5% | 多模型路由、成本优化、出海模型分发 | 纯自助 + 企业合同；排行榜（Rankings）本身就是获客；支付宝、USDC 付款；供应商是"货架"上的卖家 |
| **Groq** | GroqCloud API（LPU 旧集群 + NVIDIA 系统）、Flex / Batch / Performance 服务档、语音转写与 TTS、数据中心容量（NCP） | 按 Token；语音按小时；企业合同 | GPT OSS 120B 0.15/0.60、GPT OSS 20B 0.075/0.30；Llama 系列改为"联系销售"；Whisper Large V3 0.111/小时、Turbo 0.04/小时；Orpheus TTS 22–40 /M 字符 | 极低延迟（语音、实时 Agent）；中大型 NVIDIA 集群租赁 | 开发者自助（自称 600 万开发者）；企业销售；作为 NVIDIA Cloud Partner 卖集群 |
| **Baseten** | Model APIs、Dedicated Inference、Training、Model Labs（自有模型系列 joey/elephant/mammoth）、多云容量管理、FDE、自托管/混合部署 | 按 Token；专属部署与训练按 GPU **分钟**；Pro/Enterprise 量折 | GLM-5.3 1.40/4.40（Fast 版 2.10/6.60）；DeepSeek V4 Pro 1.32/3.96；H100 0.10833/分钟≈6.50/卡时【算】、B200≈9.98【算】 | 生产级专属推理：语音转写、TTS、编码、医疗（Abridge、OpenEvidence） | Basic 自助 → Pro/Enterprise 报价；Enterprise 可走客户 VPC / 自托管 / 混合并抵扣客户云承诺消费；FDE 驻场 |
| **DeepInfra** | Model APIs（100+ 模型：LLM、嵌入、语音、图像、视频、音乐）、Custom LLM 专属部署、GPU 租用、DeepCluster 长约集群 | 按 Token / 按图 / 按音频分钟；GPU 按分钟；服务档倍率 Standard 1×、Priority 1.5×、Flex 0.8× | DeepSeek-V3.2 0.26/0.38；Kimi-K2.6 0.75/3.50；专属 H100 2.90、H200 3.49、B200 4.89、B300 5.89 /卡时；**DeepCluster B300 5 年期 1.98 /卡时** | 低价批量推理；长期包机房 | 自助（零长约）+ 企业咨询；美国 8 个数据中心；OpenRouter 上的低价供应商 |
| **Novita AI** | Model APIs（Serverless + Dedicated Endpoint）、GPU 实例（按需 / Spot / 裸金属）、Serverless GPU、Agent Sandbox、Embeddings、AI Search（转售 Exa / Tavily） | 按 Token；GPU 按小时/按秒；搜索按次 | DeepSeek V4 Pro 1.60/3.20；GLM-5.3 1.40/4.40；Batch 5 折（推广期）；H100 按需 3.39、Spot 1.70【三方】 | 开源模型 API + Agent 基础设施一站式 | 自助 + 创业计划 + 联盟（affiliate）+ 首月促销；在 OpenRouter 上做供应商 |
| **Replicate**（2025-12 被 Cloudflare 收购） | 公共模型按次调用（5 万+ 模型）、私有模型部署、快速启动微调、Cog 打包工具 | 公共模型按秒或按输出；私有模型按在线时长（含空闲） | H100 5.49 /卡时、A100 5.04、L40S 3.51；flux-1.1-pro 0.04/张；wan-2.1 720p 0.25/秒视频 | 开发者快速试模型，尤其图像/视频 | 开发者社区（模型作者上传）；并入 Cloudflare Workers AI；企业承诺消费 |
| **Modal** | Serverless Python 计算（GPU/CPU）、Sandboxes、推理、多节点训练、Batch、Notebooks | 按秒计费 + 月费档；区域选择 1.15–1.75×，不可抢占 3× | Team 月费 250 美元；H100 3.95、B200 6.25、B300 7.10 /卡时【算】；Sandbox CPU 为基础价 3× | AI Agent 代码沙箱（年化 3 亿美元）、推理、生成媒体、机器人、药物发现 | 开发者自助（Python SDK）为主；Team / Enterprise；创业与学术额度 |
| **Cerebras**（已上市 CBRS） | Inference Cloud（共享 + 专属）、Training Cloud、CS-3/CS-4 系统、晶圆级芯片 | 共享推理按 Token；专属/企业报价；硬件销售 | GPT OSS 120B 0.35/0.75、Qwen 3.8 27B 0.99/1.49；免费试用送 5 美元 | 极速推理（编码、Agent、实时）；为 OpenAI 等大客户建专属容量 | 自助 Developer 档 + 企业；AWS Marketplace、OpenRouter、Hugging Face、Vercel、OCI；大合同（OpenAI 750 MW） |
| **SambaNova** | SambaCloud（API）、SambaStack（软件栈）、SambaRack SN40-16 / SN50（整机）、RDU 芯片 | 云端按 Token；硬件与本地部署按合同 | gpt-oss-120b 0.22/0.59；MiniMax-M3.1-Flash 0.30/1.20；DeepSeek-V3.2 3.00/4.50 | 本地/主权 AI、Neocloud 交钥匙、金融机构私有推理（JPMorgan）、电力行业（TEPCO Systems） | 企业直销 + 硬件销售；Intel 联合销售（与 Xeon 打包）；OpenRouter、Hugging Face 上做供应商 |
| **fal** | Model APIs（图像/视频/音频生成 600+ 端点）、Serverless GPU、私有部署 | 按输出（每张、每百万像素、每秒视频、每千 Token）；GPU 按秒 | FLUX 2 0.012/百万像素；Kling v3 Pro 0.14/秒；Seedance 2.0 Fast 0.0112/千 Token；Nano Banana Pro 0.15/张；H100 列表 4.50、最低 2.49 /卡时 | 生成媒体：广告、电商、游戏、影视 | 自助预付 + 企业销售；模型厂首发合作（BFL、字节、可灵）；开发者社区 |

**一句话结论【判断】：** 海外这 12 家没有一家只卖 Token。它们都把"按 Token 的 Serverless"当入口，把钱赚在后面三层：**按承诺强度递增的容量产品**（Batch→预留吞吐→专属部署→长约集群）、**训练/定制**（让客户的模型留在平台上）、**分发与渠道**（Marketplace、聚合器、模型厂首发）。详见第 13 节。

---

## 1. Together AI

**定位：** "AI Native Cloud"，开源模型推理 + GPU 集群，覆盖训练到推理。

**产品线**

- **Serverless Inference**：按 Token 调用 100+ 开源模型。
- **Batch API**：异步批量，5 折。
- **Provisioned Throughput**：按 Token 计价的预留容量，SLA 99%，1 个月起订（2026-07 推出）。
- **Dedicated Inference**：独占 GPU 跑指定模型。
- **GPU Clusters / Instant Clusters**：可抢占、按需、3–180 天阶梯预留；181 天以上找销售。
- **Fine-tuning / Post-training / RL API**：按训练 Token 或 GPU 时计价；2026-10 新增 B200 按需 Post-training。
- **Code Sandbox / Code Interpreter**（收购 CodeSandbox 而来）、托管存储。
- **Together Link**（2026-10）：在 Claude Code、Codex 里切换成开源模型。
- **AI Factory**：与伙伴合建大型数据中心（Hypertec、IBM、沙特 HUMAIN）。

**定价（美元）**

| 项目 | 价格 | 来源 |
|---|---|---|
| GLM-5.3 / Kimi K3 / DeepSeek V4 Pro | 1.40/4.40；3.00/15.00；1.32/3.96 | 本地快照 10-14 |
| Batch | Serverless 价 5 折 | 同上 |
| GPU 集群 H100 | 可抢占 1.99、按需 3.99、预留 3.69 / 3.45 / 3.19（3–30 / 31–90 / 91–180 天） | 同上 |
| GPU 集群 B200 | 可抢占 4.09、按需 8.19、预留 7.99 / 7.79 / 6.79 | 同上 |
| 专属推理 | H100 5.49、B200 8.99 | 同上 |
| B200 Post-training 按需 | 列表 11.00，首发促销 9.00（2026-10-20 上架）【三方】 | [pricingsaas 追踪](https://pricingsaas.com/companies/together/diffs/2026D293)，访问 2026-11-02 |
| 沙箱 / 存储 | 0.0446 /vCPU 时；0.16 /GiB/月 | 本地快照 10-14 |
| 付款 | 全部预付，首充 ≥15 美元；2026-04 取消用户分级 | 同上 |

10 月价格页还有几处小变动【三方】：下架 Gemma 4 31B、DeepSeek V4 Flash 0731、Llama 3.3 70B、MiniMax M2.7 四个 Serverless 模型；Kimi K3 缓存价上调（来源同上）。

**解决方案**：开源模型替代闭源（Decagon 客服、Cursor 编码），DeepSWE 成本对比内容，主权 / 区域 AI 工厂。

**销路**

- 自助预付，Sales Development Engineer 把自助用户转成大单。
- 战略客户经理 + 方案架构师 + FDE 做 POC。
- 渠道：AWS Marketplace（可抵扣 AWS 承诺消费）、Hugging Face Inference Providers、NVIDIA DGX Cloud Lepton、Vercel、OpenRouter。
- 模型厂首发：2026-07-29 与月之暗面签约，Kimi K3 起其开源模型在 Together 首发。
- Startup Accelerator：按融资阶段发 1.5 / 3 / 5 万美元额度 + FDE 工时 + 联合推广。

**数字**

- C 轮 8 亿美元、投后 83 亿美元（2026-07-01）【官】；上季度年度 bookings 超过 11.5 亿美元【官】；年化收入 12 亿美元【媒·NYT】。
- 收入结构未披露；Sacra 估计 API 占三到四成，其余是 GPU 出租【三方】；毛利约 45%【三方】。
- 自述在 OpenRouter 上承接 DeepSeek V4.1 Flash 40.8%、GLM 5.3 Flash 28.2%、Kimi K3 23.1% 的 Token（截至 2026-09-30）【官】。
- 来源：本地 `../硅基流动与海外同类/硅基流动与海外同类_业务市场营销调研_2026-10-14.qmd` §3 及其 `sources/together/`（原始链接：[价格页](https://www.together.ai/pricing)、[C 轮博客](https://www.together.ai/blog)、[Together Link](https://www.together.ai/blog/together-link-frontier-quality-open-models-in-the-harness-you-already-use)）。

---

## 2. Fireworks AI

**定位：** 开源模型推理 + 用客户数据训练专用模型（"Own Your Specialized Intelligence"）。

**产品线**

- **Serverless**：四档——Standard、Priority（约 1.25×）、Fast（1.5×）、US-only（1.5×，只在美国处理）。
- **Batch**：5 折。
- **On-demand Deployments**：按 GPU 秒；锁定单一区域加价 50%。
- **Reserved Throughput**：按美元/分钟购买，附 SLA。
- **BYOC**：部署到客户自己的云（Virtual Cloud，18+ 区域、8 家云）。
- **训练**：SFT / DPO / RFT、Training API（2026-08 GA）、专属训练按 GPU 时。
- **Nexus**（2026-07）：抢企业 AI 编程预算；**FireRouter** 路由；自研基准 SII 与模型 Ember-1。
- 2026-06-10 主动下线音频推理和图像生成。

**定价（美元，本地快照 10-14）**

| 项目 | 价格 |
|---|---|
| Kimi K3 | Standard 3.00/15.00；Priority 3.75/18.75；Fast 与 US-only 4.50/22.50 |
| DeepSeek V4.1 Flash | 0.30/1.20（10-01 由 0.22/0.66 上调） |
| 按需 GPU | H100 / H200 8.00、B200 13.00、B300 15.00、GB300 20.00 /卡时 |
| 训练 | SFT/DPO 0.5–40 /M 训练 Token；微调后模型按基础模型同价推理 |
| 账户 | 自助 Tier 1–4（累计 50 / 500 / 5,000 美元解锁）；2026-07 起自助预付，合同客户后付 |

**解决方案**：AI 编程（Cursor、Sourcegraph）、低延迟产品（Notion 2 秒→350 毫秒）、法律（Harvey）、专用模型训练闭环。

**销路**

- 自助 → 企业 AE（AI 原生团队、企业两条线，含 EMEA）+ FDE（新加坡、伦敦）。
- AWS 战略合作协议（含联合创业计划）、AWS / GCP Marketplace、微软 Foundry。
- 咨询伙伴 BCG、Deloitte；专门招"AI Factory 伙伴"岗位。
- 首发营销（Qwen 3.6 Plus 除阿里外只在 Fireworks 提供）、Artificial Analysis 测速、Discord 社区约 1.3 万人、DevDay、Forge 大会（2026-11-03）。

**数字**

- ARR 超过 10 亿美元，同比约 5 倍；日处理超过 40 万亿 Token（2026-07-15）【官】。
- D 轮 15.05 亿美元，投后 175 亿美元（2026-07）【官】。
- 2026-10-20 前后报道在谈 300–400 亿美元估值的新一轮【传】（[aiweekly](https://aiweekly.co/alerts/fireworks-ai-advances-fresh-funding-on-inference-cloud-boom)，访问 2026-11-02）。
- 不自有 GPU，从 20 多家云租（Oracle、AWS、Crusoe、微软、AMD）【媒/官】；毛利约 50%【媒·The Information 转述】。
- 来源：本地 10-14 调研 §4 与 `sources/fireworks/`（原始链接：[价格页](https://fireworks.ai/pricing)、[serverless 价格文档](https://docs.fireworks.ai/serverless/pricing)、[changelog](https://docs.fireworks.ai/updates/changelog)）。

---

## 3. OpenRouter

**定位：** 模型聚合路由，"Token 交易所"。自己不跑推理。

**产品线**

- 统一 OpenAI 兼容 API：600+ 模型、80+ 供应商（价格页口径；Stripe 新闻稿写的是 400+ / 80+）。
- 自动路由（按价格、速度、可用性）、Fallback、预算与 Key 管理、管理 API、缓存。
- BYOK：用户自带供应商 Key。
- Business 档：欧盟 / 美国境内路由、Workload Identity Federation、1,000 个工作区。
- Enterprise：Private Endpoints（加购）、托管策略、SSO/SAML/SCIM、合同 SLA、DPA 定制、专属支持与 FDE。
- 公开排行榜（Rankings）：按模型、应用、供应商统计 Token 份额。

**定价**（[openrouter.ai/pricing](https://openrouter.ai/pricing)，访问 2026-11-02）

| 档位 | 平台费 | 说明 |
|---|---|---|
| Free | — | 25+ 免费模型；每天 50 次、每分钟 20 次；充值满 10 美元后每天 1,000 次 |
| Standard | 5.5% | 平台费在**买 credit 时**收，不按请求；推理按供应商标价 |
| Business | 8% | 加区域路由、高级通知、签署版 DPA |
| Enterprise | 合同折扣 | 开票 / 采购单付款 |
| BYOK | Standard/Business 每月 2.5 万美元标价用量免费，超出收 5% | Free 档不能用 |

付款方式含信用卡、**支付宝**、USDC。

**解决方案**：多模型路由与成本优化；对供应商而言是分发渠道——沐仞若上架，就和 Together、DeepInfra、Novita、硅基流动在同一页比价。

**销路**：几乎全靠自助和口碑；排行榜和应用榜单本身就是增长飞轮；客户含 NVIDIA、Zoom、Lovable【官·Stripe 新闻稿】。

**数字**

- Stripe 2026-08-19 宣布收购，价格未披露【官】；媒体报道 70 亿–80 亿美元以上，多为股票【媒】（[Stripe 新闻稿](https://stripe.com/newsroom/news/stripe-agrees-to-acquire-openrouter)、[Orrick](https://www.orrick.com/en/News/2026/08/OpenRouter-to-be-Acquired-by-Stripe-to-Help-Businesses-Optimize-Token-Routing-and-Usage)、[The Next Web](https://thenextweb.com/news/stripe-openrouter-acquisition-confirmed)，访问 2026-11-02）。Stripe 收购理由："Tokens are the central currency"——Token 是 AI 公司的核心货币。
- 2026-05 B 轮 1.13 亿美元，CapitalG 领投，估值约 13 亿美元【媒】（[shopifreaks 汇总](https://www.shopifreaks.com/openrouter-raises-113m-series-b-led-by-capitalg-at-1-3b-valuation-more-than-doubling-from-547m-a-year-ago/)）。
- Sacra 估 2026-07 年化**收入**（平台抽成，不是 GMV）约 1.4 亿美元，近四个月环比 +29%；月吞吐约 250 万亿 Token；中国开源模型占 50% 以上用量；每 Token 变现率下降约 60%（费率不变、Token 变便宜）【三方】（[Sacra](https://sacra.com/research/openrouter-growing-29-mom-at-140m-year)，访问 2026-11-02）。按 5% 抽成反推年化流水约 28 亿美元【算】。

---

## 4. Groq

**定位：** 从"LPU 芯片公司"转成"推理云 + NVIDIA 集群运营商"。

**背景变化（重要）**

- 2025-12-24 与 NVIDIA 签非独家技术授权；NVIDIA 同时聘走创始人兼 CEO Jonathan Ross 及大部分工程团队。媒体普遍报道交易约 200 亿美元，双方未确认【媒】。
- NVIDIA 2026-03 GTC 发布基于该技术的 Groq 3 LPX 机架【媒】。
- Groq 保持独立，CEO 改由 Simon Edwards 担任；2026-06 融 6.5 亿美元，2026-08-17 宣布 3.5 亿美元 A 轮、估值 35 亿美元（Disruptive 领投，NVIDIA 计划参投），2025-09 估值曾为 69 亿美元【官】。
- 2026-08 起成为 NVIDIA Cloud Partner，卖"中大型 NVIDIA 集群用于训练和推理"，旧 LPU 云并行运行【官】。
- 13 个数据中心（北美、欧洲、中东、亚太），计划从 54 MW 扩到 2027 年 200 MW 以上【媒】。
- 来源：[Groq 新闻稿](https://groq.com/newsroom/groq-closes-usd350-million-series-a-building-the-world-s-leading-ai-inference-cloud)、[ai2.work 汇总](https://ai2.work/blog/groq-s-350m-reset-from-nvidia-rival-to-nvidia-powered-neocloud)，访问 2026-11-02。

**产品线**

- GroqCloud API：LLM、语音转写（Whisper）、TTS（Orpheus，预览）。
- 服务档：On-demand、**Flex**（同价、限流放宽 10 倍、容量不足时快速失败，仅付费用户）、Performance、Batch。
- 企业：专属容量、NVIDIA 集群租赁。

**定价**（[console.groq.com/docs/models](https://console.groq.com/docs/models)，访问 2026-11-02）

| 模型 | 价格 |
|---|---|
| GPT OSS 120B | 0.15 / 0.60（约 500 Token/秒） |
| GPT OSS 20B | 0.075 / 0.30（约 1,000 Token/秒） |
| Llama 3.1 8B、Llama 3.3 70B | 改为"Contact Sales (Enterprise)" |
| Whisper Large V3 / Turbo | 0.111 / 0.04 美元每音频小时 |
| Orpheus TTS（预览） | 英文 22、阿拉伯语 40 美元/百万字符 |

Batch 与缓存 5 折的说法只见于第三方页面【待核实】。

**解决方案**：极低延迟——语音 Agent、实时对话、阿拉伯语 TTS（中东客户）。

**销路**：开发者自助（自称 600 万以上开发者【官】）+ 企业销售 + NVIDIA 生态（NCP）。

**数字**：收入未披露；MLQ 称 NVIDIA 交易前后年收入约 1 亿美元【媒·转述，待核实】。

---

## 5. Baseten

**定位：** 生产级专属推理平台，强在"把客户自己的模型稳定跑起来"。

**产品线**（[Series F 公告](https://www.baseten.co/blog/announcing-our-series-f/)，访问 2026-11-02）

- **Model APIs**：按 Token 的共享 API。
- **Dedicated Inference**：客户模型独占部署，自动扩缩。
- **Training**：与专属部署同一套 GPU 价格。
- **Model Labs**：自有模型系列 joey-1 / elephant-1 / mammoth-1（价目表上最便宜的几行）。
- 平台层：Model Runtimes、多云容量管理。
- **FDE**：驻场工程师。
- 部署形态：Baseten Cloud、客户 VPC、自托管、混合。

**定价**（[baseten.co/pricing](https://www.baseten.co/pricing/)，访问 2026-11-02）

| 项目 | 价格 |
|---|---|
| 套餐 | Basic 0 美元月费按量；Pro、Enterprise 报价，含量折。页面未列平台费 |
| Model APIs | GLM-5.3 1.40/4.40（**Fast 版 2.10/6.60**）；DeepSeek V4 Pro 0813 1.32/3.96；DeepSeek V4.1 Flash 0.30/1.20（Fast 版 0.60/2.40）；Kimi K3 3.00/15.00；GPT OSS 120B 0.10/0.50；joey-1 输入 0.01 |
| 专属部署 / 训练（页面价格列未标单位，按分钟理解【判断】） | H100 0.10833 →约 6.50 /卡时【算】；B200 0.16633 →约 9.98【算】；A100 0.06667 →约 4.00【算】；L4 →约 0.85【算】；按分钟计费 |
| Enterprise 附加 | 自托管、抵扣客户已有云承诺消费、数据驻留、自定义区域、高级 RBAC、定制 SLA |

**解决方案**：语音转写与 TTS、编码（Cursor）、医疗（Abridge、OpenEvidence）、企业（HubSpot、Notion、Harvey）、客服（Decagon）。

**销路**：自助 Basic → 销售报价 Pro/Enterprise；以 FDE 驻场 + 自托管/混合部署打大企业；"可用你已有的云承诺消费"降低采购门槛。

**数字**

- Series F 15 亿美元、估值 130 亿美元（2026-06-22），Altimeter、Conviction、Spark 领投；过去一年收入增长 20 倍、推理量增长 40 倍【官】。
- 2026-01 E 轮 3 亿美元、估值 50 亿美元（NVIDIA 出 1.5 亿）【媒】。
- 年化收入约 6 亿美元（2026-03，The Information）【媒·转述】；2026-09 传在谈约 260 亿美元估值【传·待核实】。

---

## 6. DeepInfra

**定位：** 低价、高吞吐的开源模型推理云，自建/托管美国机房。

**产品线**（[deepinfra.com](https://deepinfra.com/)、[pricing](https://deepinfra.com/pricing)，访问 2026-11-02）

- **Model APIs**：100+ 模型，LLM、嵌入、重排、语音识别/TTS、文生图、文生视频、文生音乐、世界模型；也转售 Claude、Gemini。
- **Custom LLMs**：自带模型专属部署，按在线时长计费、按分钟计、周结发票。
- **GPU 租用**：DGX B300 按需。
- **DeepCluster**：B300 专属集群，5 年期，256–5,000 卡。

**定价**

| 项目 | 价格 |
|---|---|
| LLM | DeepSeek-V3.2 0.26/0.38；Kimi-K2.6 0.75/3.50；Qwen3.5-397B 0.45/3.00；Llama 3.3 70B Turbo 0.10/0.32；（转售）claude-sonnet-4-6 3.00/15.00 |
| 服务档倍率 | Standard 1×、Priority 1.5×、**Flex 0.8×** |
| 嵌入 / 图 / 语音 | bge-m3 0.01 /M；FLUX-2-pro 0.015 /张；ASR 0.0002–0.003 /音频分钟 |
| 专属 GPU | A100 1.49、H100 2.90、H200 3.49、B200 4.89、B300 5.89 /卡时 |
| **DeepCluster** | **B300 5 年期 1.98 /卡时**，Tier 3 机房，SLA 99.982% |
| 付款 | 绑卡或预付；开票客户次月初结 |

**解决方案**：成本敏感的批量推理、开源模型 API、长期包集群。

**销路**：自助、无长约；企业咨询；在 OpenRouter 上常是低价供应商。SOC 2、ISO 27001、零留存（ZDR）。

**数字**：B 轮 1.07 亿美元（2026-05，500 Global 与 Georges Harik 联合领投，NVIDIA、Samsung Next、Supermicro 参投），估值未披露；美国 8 个数据中心；自称 A 轮后 Token 量增长 25 倍【官/媒】（[SDxCentral](https://www.sdxcentral.com/news/ai-cloud-deepinfra-raises-107m-in-series-b-funding-round/)，访问 2026-11-02）。收入未公开。

---

## 7. Novita AI

**定位：** 开源模型 API + GPU 云 + Agent 沙箱的一站式开发者云。

**与沐仞的关系【待核实】：** 业内常说 Novita AI 是 PPIO 派欧云的海外品牌，两者产品结构（模型 API、GPU 实例、Agent 沙箱）高度一致；但本次没找到招股书或官方声明原文。如属实，它就是"中国团队做 Token 出海"的直接样本，需要在 PPIO 招股书里核对。

**产品线**（[novita.ai/pricing](https://novita.ai/pricing)，访问 2026-11-02）

- Model APIs：Serverless Endpoints、Dedicated Endpoints。
- GPU：按需实例、Spot（官网称最多省 50%）、裸金属、Serverless GPU（按秒计、30 秒缩到零）。
- Agent Sandbox。
- Embeddings；AI Search（转售 Exa、Tavily，按次）。

**定价**

| 项目 | 价格 |
|---|---|
| LLM | DeepSeek V4 Pro 1.60/3.20；DeepSeek V4.1 Flash 0.30/1.20；GLM-5.3 1.40/4.40；Kimi K3 3.00/15.00；Kimi K2.6 0.80/3.40；Qwen3.8 Max 2.00/6.00；GPT OSS 120B 0.05/0.25 |
| Batch | 推广期 5 折 |
| AI Search | Exa 0.007–0.015 /次；Tavily 0.008–0.016 /次 |
| GPU | H100 SXM 按需 3.39、Spot 1.70 /卡时（2026-09-23 抓取）【三方】；官网 GPU 页价格动态加载，本次未直接读到 |

**解决方案**：AI 应用开发者、Agent 运行环境。

**销路**：自助；创业计划；联盟推广（affiliate）；Build Month 等促销（最高 8 折）；OpenRouter 供应商；Ramp 支出数据里被列为头部 AI 基础设施供应商之一【三方】。

**数字**：融资、收入均未查到可靠数据（Latka 等聚合站的数据与常识不符，不采用）【待核实】。

---

## 8. Replicate（Cloudflare 旗下）

**定位：** 开发者"一行代码跑任意模型"的模型托管市场，强在图像/视频。

**归属：** Cloudflare 2025-11-17 宣布收购，**2025-12-01 交割**，现金对价 5,740 万美元，对 Cloudflare 财务不重大【官·SEC 10-Q/10-K】；保留独立品牌和 API，模型并入 Workers AI【媒】（[Cloudflare 10-Q](https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000038/cloud-20260331.htm)，访问 2026-11-02）。

**产品线**

- 公共模型：5 万+ 社区与官方模型，按次调用。
- 私有模型：专属硬件部署。
- 快速启动微调（只收处理时间）。
- Cog：开源模型打包工具。

**定价**（[replicate.com/pricing](https://replicate.com/pricing)，访问 2026-11-02）

| 项目 | 价格 |
|---|---|
| 硬件（按秒） | CPU 0.09–0.36、T4 0.81、L40S 3.51、A100 80G 5.04、H100 5.49、H200 5.49 /小时；8×H100 43.92 /小时 |
| 官方模型按输出 | flux-1.1-pro 0.04 /张；flux-schnell 3 美元/千张；ideogram-v3-quality 0.09 /张；wan-2.1 i2v 480p 0.09、720p 0.25 /秒视频；deepseek-r1 输入 3.75 /M、输出 0.01 /千 Token |
| 私有模型 | 按在线时长收费，含启动和空闲 |
| 企业 | 承诺消费换多卡 A100/H100、H200 容量；量折；性能 SLA |

**解决方案**：原型验证、图像/视频生成、模型作者发布与变现。

**销路**：开发者社区（模型作者上传带来长尾流量）；现在加上 Cloudflare 的开发者与企业渠道。

**数字**：收购价 5,740 万美元【官】，远低于其历史估值——说明"纯托管市场"单独估值有限【判断】。

---

## 9. Modal

**定位：** Serverless AI 计算平台（Python 原生），不按模型卖 Token，按秒卖算力；Agent 沙箱是增长最快的业务。

**产品线**

- Serverless Functions（GPU / CPU，按秒，自动扩缩）。
- **Sandboxes**：给 AI Agent 跑代码的隔离环境，自称累计创建近 30 亿个、可并行 100 万个。
- 推理服务、多节点训练（无需容量承诺）、Batch、Notebooks、HTTP 服务。

**定价**（[modal.com/pricing](https://modal.com/pricing)，访问 2026-11-02）

| 项目 | 价格 |
|---|---|
| 套餐 | Starter 0 月费、含 30 美元/月额度；Team 250 美元/月、含 100 美元额度；Enterprise 定制 |
| GPU（官网按秒） | H100 0.001097/秒 ≈ 3.95；H200 ≈ 4.54；B200 ≈ 6.25；B300 ≈ 7.10；A100 80G ≈ 2.50；L4 ≈ 0.80 /卡时【算】 |
| CPU / 内存 | 0.0000131 /物理核·秒；0.00000222 /GiB·秒 |
| 倍率 | 指定区域 1.15–1.75×；不可抢占 3×；Sandbox 的 CPU/内存按 3× 计 |
| 额度 | 创业公司免费额度（金额未写）；学术最高 1 万美元 |

**解决方案**：编码 Agent（Cognition、Ramp、Linear）、视频/音乐生成（Runway、Suno）、机器人（Physical Intelligence、1X）、药物发现（Chai Discovery）。

**销路**：开发者自助为主（Python SDK、文档、口碑），Team / Enterprise 销售；不自建机房，从 20 多家云聚合 GPU 再转售【媒】。

**数字**：D 轮 7.5 亿美元、投后 157.5 亿美元（2026-10-14，Accel 领投）；年化收入超过 10 亿美元，其中 Sandboxes 约 3 亿；5 月 C 轮时为 3 亿美元、估值 46.5 亿【官/媒】（[cloudnews.tech](https://cloudnews.tech/modal-tops-1-billion-in-annualized-revenue-raises-750m/)、[Pillsbury 新闻稿](https://www.pillsburylaw.com/en/news-and-insights/pillsbury-advises-modal-labs-on-750-million-financing.html)，访问 2026-11-02）。

---

## 10. Cerebras（Nasdaq: CBRS）

**定位：** 晶圆级芯片公司，推理云已成最大收入来源。

**产品线**

- **Inference Cloud**：共享推理（Developer 档）+ 专属推理（企业，预留容量、更多模型、SLA）。
- Training Cloud；微调与训练服务（按协议）。
- CS-3 / CS-4 系统销售；Wafer Scale Engine。

**定价**（[cerebras.ai/pricing](https://www.cerebras.ai/pricing) 页面源码，访问 2026-11-02）

| 项目 | 价格 |
|---|---|
| GPT OSS 120B | 0.35 / 0.75（约 3,000 Token/秒） |
| Qwen 3.8 27B | 0.99 / 1.49（约 1,850 Token/秒） |
| Developer 档 | 自助按量，绑卡送一次性 5 美元（30 天有效）；社区 Discord 支持 |
| Enterprise | 报价；全部模型、优先级、更高限流、可定制权重 |

共享推理目前只剩 2 个模型；此前的 Cerebras Code（Pro 50 / Max 200 美元/月）未出现在当前价格页【待核实是否停售】。

**解决方案**：极速推理——编码、Agent、实时应用；为 OpenAI 建专属推理容量。

**销路**：自助 + 企业；AWS Marketplace、OpenRouter、Hugging Face、Vercel，OCI 计划上架【官】；大客户合同（OpenAI 750 MW，已上调到 200 亿美元以上【媒】）。

**数字**

- 2026-05-14 上市，募资约 55.5 亿美元，发行价 185 美元【媒】。
- 2025 年收入 5.10 亿美元【媒】。
- 2026 Q2：GAAP 收入 1.801 亿美元；**云（推理）收入 1.26 亿美元，同比 +281%**；GAAP 毛利率 14%、core 毛利率 41%；剩余履约义务 254 亿美元；已签约数据中心容量 600 MW；全年 core 收入指引 8.8–8.9 亿美元【官·8-K】（[SEC 8-K](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056186/cbrsannouncesfinancialresu.htm)，访问 2026-11-02）。
- 客户集中度高（此前 G42 / MBZUAI 占大头）【媒】。

---

## 11. SambaNova

**定位：** 自研 RDU 芯片，主攻本地/主权部署和"交钥匙推理机架"，云 API 是展示窗。

**产品线**（[sambanova.ai](https://sambanova.ai/)，访问 2026-11-02）

- **SambaCloud**：OpenAI 兼容的托管推理 API。
- **SambaStack**：软件栈，支持自带权重（BYOC checkpoint）、SambaOrchestrator 调度监控。
- **SambaRack SN40-16 / SN50**：整机柜；SN40-16 主打低功耗、多模型并行（官网称平均约 20 kWh），SN50 主打大模型 Agent 推理。
- RDU 芯片（数据流架构、三级内存）。

**定价**（[cloud.sambanova.ai/plans/pricing](https://cloud.sambanova.ai/plans/pricing)，访问 2026-11-02）

| 模型 | 输入 / 输出（缓存） |
|---|---|
| MiniMax-M3.1-Flash | 0.30 / 1.20（0.03） |
| gpt-oss-120b | 0.22 / 0.59 |
| gemma-4-31B-it | 0.38 / 1.15 |
| Llama-3.3-70B | 0.60 / 1.20 |
| DeepSeek-V3.1 / V3.2 | 3.00 / 4.50 |

硬件与本地部署按合同，不公开。

**解决方案**：主权 AI、Neocloud 交钥匙（官网称 6 个月回本，属厂商口径）、美国公共部门、金融（JPMorgan 用 SN40L/SN50 做本地推理【媒】）、**电力行业（TEPCO Systems，官网案例）**、"能效 AI 基础设施 for power utilities"。

**销路**：企业直销 + 硬件；与 Intel 联合销售（与 Xeon 打包）【媒】；OpenRouter、Hugging Face 供应商。

**数字**：2026-07-08 Series F 首轮交割 10 亿美元、估值 110 亿美元（General Atlantic 领投）【官】（[General Atlantic](https://generalatlantic.com/media-article/sambanova-completes-first-close-of-1-billion-financing-at-11-billion-valuation)，访问 2026-11-02）；此前 Intel 约 16 亿美元收购谈判于 2026-01 搁浅，2026-02 E 轮 3.5 亿美元【媒】。收入未公开。

---

## 12. fal

**定位：** 生成媒体（图像、视频、音频）专用推理平台。

**产品线**（[fal.ai/pricing](https://fal.ai/pricing)，访问 2026-11-02）

- **Model APIs**：图像、视频、音频、3D 等生成模型端点，按输出计价，从预付额度扣；服务器错误和排队时间不收费。
- **Serverless GPUs**：按小时定价、按秒计费；排队和拉镜像不计费。
- 企业定制部署（销售）。

**定价**

| 项目 | 价格 |
|---|---|
| 图像 | FLUX 2 0.012、FLUX.1 dev 0.025、schnell 0.003 /百万像素；Nano Banana 0.0398、Nano Banana 2 0.08、Pro 0.15 /张 |
| 视频 | Kling v2.6 Pro 0.07 /秒；Kling v3 Pro / O3 Pro 0.14 /秒；FLUX 3 Max 0.085 /秒；Seedance 2.0 Mini 0.007、Fast 0.0112 /千 Token；Seedance 1.5 Pro 1.20 /M Token |
| GPU | H100 列表 4.50、最低 2.49；H200 6.00 / 2.99；B200 7.99 / 5.49 /卡时 |

**解决方案**：广告与电商素材、游戏、影视、创意工具。

**销路**：自助预付 + 企业销售；模型厂首发合作（Black Forest Labs、字节 Seedance、可灵）；开发者社区（2025 年自称 200 万+ 开发者、300+ 企业客户【媒】）。

**数字**

- 2025-12 D 轮 1.4 亿美元、估值 45 亿美元（红杉领投）【媒·Bloomberg】。
- 年化收入：2025-10 超过 2 亿美元 → 2026-03 约 4 亿 → The Information 报道约 8 亿美元【媒·转述】；在谈 150 亿美元以上估值【传】（[Bloomberg](https://www.bloomberg.com/news/articles/2025-12-09/sequoia-led-funding-vaults-ai-startup-fal-to-4-5-billion-valuation)、[dealroom](https://dealroom.co/news/126961-fal-targets-8b-valuation-in-new-raise-as-ai-inference-revenue-doubles-to/)，访问 2026-11-02）。

---

## 13. 横向规律【判断】

### 13.1 同模型同价，差异在"档位"

- GLM-5.3 在 Together、Fireworks、Baseten、Novita 都是 1.40/4.40；DeepSeek V4 Pro 在 Together、Baseten 都是 1.32/3.96（Novita 1.60/3.20 是唯一的不同结构）。单价由模型厂标价锁定。
- 拉开差距的是**服务档**：
  - 速度档：Fireworks Fast 1.5×、Baseten "Fast" 版 1.5×、DeepInfra Priority 1.5×。
  - 区域/合规档：Fireworks US-only 1.5×、Modal 指定区域 1.15–1.75×、OpenRouter Business 才有欧盟/美国境内路由。
  - 降级档：DeepInfra Flex 0.8×、Groq Flex（同价、限流 10 倍、可能失败）、各家 Batch 5 折。
- 即"同一模型按 SLA 分层卖"已是通行做法。沐仞的"绿电时段价"可以直接套进这个框架：做一个 **Green / Flex 档**（价格更低、在电站出力高时优先处理、可能排队），再做一个正常档。

### 13.2 承诺阶梯是主收入来源

几乎每家都有一条从按量到长约的阶梯：

| 承诺强度 | 代表产品 | 例 |
|---|---|---|
| 无承诺 | Serverless 按 Token | 全部 |
| 时间弹性 | Batch / Flex | Together、Fireworks、Novita 5 折；DeepInfra 0.8× |
| 月度 | 预留吞吐 | Together（1 个月起、SLA 99%）、Fireworks |
| 独占 | 专属部署 | H100 2.90（DeepInfra）–8.00（Fireworks）/卡时 |
| 天/月 | 预留集群 | Together 3–180 天阶梯 |
| 多年 | 长约集群 / AI Factory | DeepInfra DeepCluster 5 年 B300 1.98；Together AI Factory；Cerebras 对 OpenAI 750 MW |

Together 的收入里 GPU 出租估计占六到七成【三方】；Cerebras 剩余履约义务 254 亿美元来自少数大合同。**Token 是获客入口，长约容量才是收入主体。**

### 13.3 托管溢价：同一张 H100，1.70 到 8.00 美元

- 裸卡 / Spot：Novita Spot 1.70【三方】、Together 可抢占 1.99、DeepInfra 专属 2.90。
- 托管推理：Modal 3.95、fal 列表 4.50、Replicate 5.49、Together 专属 5.49、Baseten 约 6.50、Fireworks 8.00。
- 差价买的是推理优化、自动扩缩、运维和 SLA。沐仞一体机如果对外提供"专属推理"，定价可以对标中间段，而不是裸卡价。

### 13.4 产品线扩张的四个方向

1. **向上做"让模型留下来"**：训练/RL/Post-training（Together、Fireworks、Baseten、Cerebras）、自有模型（Baseten Model Labs、Fireworks Ember-1、Together 研究）。
2. **向旁做 Agent 基础设施**：沙箱（Modal 年化 3 亿、Together Code Sandbox、Novita Agent Sandbox）、搜索转售（Novita 卖 Exa/Tavily）、编码工具接入（Together Link、Fireworks Nexus）。
3. **向下做容量和机房**：Groq 转成 NVIDIA 集群运营商、DeepInfra 自建 8 个机房、Together AI Factory、SambaNova 卖整机柜给 Neocloud 和电力公司。
4. **向外做分发**：Marketplace（AWS/GCP/Azure Foundry）、聚合器（OpenRouter 上的供应商位）、模型厂首发合同（Together×月之暗面、fal×字节/可灵）。

### 13.5 GTM 的共同骨架

- **自助预付 → 销售转化**：Together、Fireworks、Novita 都取消了免费额度或改成预付，免费改为"创业计划"按融资阶段发额度并附 FDE 工时。
- **FDE 驻场**：Together、Baseten、OpenRouter Enterprise、Fireworks 都在招 FDE；企业大单靠工程师陪跑。
- **抵扣云承诺消费**：Together 走 AWS Marketplace、Baseten Enterprise 可用客户已有云承诺消费——帮客户的采购部门省流程。
- **首发 + 测速榜单**：新模型首日上线 + Artificial Analysis / OpenRouter 份额当广告。

### 13.6 资本市场在为"非 Token"收入付溢价

- 估值 / 收入倍数【算，口径不一，仅作量级参考】：Fireworks 约 17.5×、Modal 约 15.75×、Baseten 约 22×（对 6 亿年化），Together 约 7×（GPU 出租占比高）。
- 纯托管市场 Replicate 被以 5,740 万美元收购；纯路由 OpenRouter 因"Token 是货币"的支付叙事被 Stripe 高价收购——**两端（结算层、专用模型层）都值钱，中间的通用托管不值钱**。

---

## 14. 对沐仞产品线的启示【判断】

1. **把"绿电时段"做成服务档，而不是单纯打折。** 参照 Groq Flex / DeepInfra Flex / Batch 5 折：推出 "Green Flex" 档（电站出力高时优先、允许排队、价更低）和"Green Priority"档（保证延迟、附绿电产地证明）。这比"公开价 4 折起"更能讲清楚折扣从哪来，也天然和世界模型调度挂钩。
2. **补齐承诺阶梯。** 现在沐仞只有按量 Token 和私有化两端。中间缺"月度预留吞吐"（参照 Together 1 个月起、SLA 99%）和"电站侧专属推理"（按卡时，对标 3–6 美元/卡时的托管段）。电站合作方的一体机产能可以直接打包成这类产品卖。
3. **长约产品要对准电站的特性。** DeepInfra 用 5 年期 B300 1.98 美元/卡时锁客户；沐仞的电站算力天然是长期资产，可以给大客户卖"多年绿电算力包"，价格挂钩电价，这正是 Groq、Cerebras 这类公司在做的"容量合同"。
4. **出海走"供应商位 + 中国模型首发"，别和美国平台拼美国托管。** OpenRouter 上中国开源模型占 50% 以上用量，Together 一家就承接了 DeepSeek V4.1 Flash 四成。沐仞可以作为 OpenRouter 供应商上架（注意 OpenRouter 现属 Stripe，付款端支持支付宝），并主打亚洲节点和价格；若能拿到国内模型厂的海外首发或独家时段，就有 Together×月之暗面式的筹码。
5. **Agent 基础设施是低成本的第二条线。** Modal 沙箱一年做到 3 亿美元年化；Novita 已经把沙箱和搜索转售打包。沐仞可以在 Token 平台上加"沙箱 + 搜索"组合，按秒/按次计费，复用同一个 API Key 和钱包。
6. **能源行业本身是一个客户行业。** SambaNova 把 TEPCO Systems 和"电力公司能效 AI"放在官网首页。沐仞已经在和电站谈合作，可以顺势做"电力行业私有推理"（调度、巡检、客服）这条解决方案线，客户与供给方重合。
7. **定制训练是留住大客户的方式，但不必自建。** Fireworks、Baseten 都靠"微调后同价推理"把客户锁在平台上。沐仞可以先做轻量微调（LoRA）+ 同价推理，作为企业套餐的附加项。

---

## 15. 待核实

| 项目 | 情况 |
|---|---|
| Novita AI 是否为 PPIO 派欧云海外品牌 | 常见说法，本次未找到一手出处；需查 PPIO 港股招股书 |
| Novita GPU 实例官方价格 | 官网动态加载，本次只有第三方追踪价（H100 按需 3.39 / Spot 1.70） |
| Baseten 专属部署价格单位 | 页面列未标单位，按"每分钟"换算；与 Baseten 过往公开价一致，但应再截图确认 |
| Groq Batch / 缓存折扣 | 只见于第三方 |
| Cerebras Code 订阅是否停售 | 当前价格页未列 |
| Groq、DeepInfra、Novita、SambaNova、Replicate 收入 | 未公开；Groq 约 1 亿美元只是媒体转述 |
| OpenRouter 收购价 | 70–80 亿美元以上为媒体报道，双方未确认 |
| fal 8 亿美元 ARR、Baseten 260 亿美元估值谈判、Fireworks 300–400 亿美元估值谈判 | 均为二手报道 |
| 所有价格 | 各家频繁调价（Together 10 月就改了 5 次以上），引用前重新抓取 |

---

## 来源汇总（访问日期 2026-11-02，除非另注）

- **本地已有资料**：`../全部竞品_产品收费与定价_2026-10-21.qmd`（Together、Fireworks、OpenRouter 价格，10-14/10-21 快照）；`../硅基流动与海外同类/硅基流动与海外同类_业务市场营销调研_2026-10-14.qmd` 及 `sources/`（Together、Fireworks 时间线、融资、GTM）。
- Together：[pricingsaas 价格变动追踪](https://pricingsaas.com/companies/together/diffs/2026D293)
- Fireworks：[aiweekly 新一轮融资报道](https://aiweekly.co/alerts/fireworks-ai-advances-fresh-funding-on-inference-cloud-boom)
- OpenRouter：[价格页](https://openrouter.ai/pricing)、[Stripe 新闻稿](https://stripe.com/newsroom/news/stripe-agrees-to-acquire-openrouter)、[Orrick](https://www.orrick.com/en/News/2026/08/OpenRouter-to-be-Acquired-by-Stripe-to-Help-Businesses-Optimize-Token-Routing-and-Usage)、[The Next Web](https://thenextweb.com/news/stripe-openrouter-acquisition-confirmed)、[Sacra](https://sacra.com/research/openrouter-growing-29-mom-at-140m-year)、[B 轮汇总](https://www.shopifreaks.com/openrouter-raises-113m-series-b-led-by-capitalg-at-1-3b-valuation-more-than-doubling-from-547m-a-year-ago/)
- Groq：[模型与价格文档](https://console.groq.com/docs/models)、[Flex 文档](https://console.groq.com/docs/flex-processing)、[A 轮新闻稿](https://groq.com/newsroom/groq-closes-usd350-million-series-a-building-the-world-s-leading-ai-inference-cloud)、[ai2.work 汇总](https://ai2.work/blog/groq-s-350m-reset-from-nvidia-rival-to-nvidia-powered-neocloud)
- Baseten：[价格页](https://www.baseten.co/pricing/)、[Series F 公告](https://www.baseten.co/blog/announcing-our-series-f/)、[dealroom](https://dealroom.co/news/129868-baseten-in-talks-to-raise-1b-at-11b-valuation-as-inference-boom-accelera/)
- DeepInfra：[首页](https://deepinfra.com/)、[价格页](https://deepinfra.com/pricing)、[SDxCentral B 轮](https://www.sdxcentral.com/news/ai-cloud-deepinfra-raises-107m-in-series-b-funding-round/)
- Novita：[价格页](https://novita.ai/pricing)、[GPU 页](https://novita.ai/gpus)、[usagepricing H100 追踪](https://www.usagepricing.com/blueprint/activity/novita-ai-2026-09-23-h100-self-serve-returns)
- Replicate：[价格页](https://replicate.com/pricing)、[Cloudflare 10-Q](https://www.sec.gov/Archives/edgar/data/0001477333/000147733326000038/cloud-20260331.htm)、[Cloudflare 收购公告](https://www.businesswire.com/news/home/20251117400765/en)
- Modal：[价格页](https://modal.com/pricing)、[cloudnews.tech D 轮](https://cloudnews.tech/modal-tops-1-billion-in-annualized-revenue-raises-750m/)、[Pillsbury](https://www.pillsburylaw.com/en/news-and-insights/pillsbury-advises-modal-labs-on-750-million-financing.html)
- Cerebras：[价格页](https://www.cerebras.ai/pricing)、[模型文档](https://inference-docs.cerebras.ai/models/overview)、[Q2 2026 8-K](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056186/cbrsannouncesfinancialresu.htm)、[DCD 上市报道](https://www.datacenterdynamics.com/en/news/cerebras-prices-its-ipo-at-185-a-share-expects-to-raise-55bn-from-sale/)
- SambaNova：[官网](https://sambanova.ai/)、[价格页](https://cloud.sambanova.ai/plans/pricing)、[General Atlantic 公告](https://generalatlantic.com/media-article/sambanova-completes-first-close-of-1-billion-financing-at-11-billion-valuation)、[DCD：Intel 谈判搁浅](https://www.datacenterdynamics.com/en/news/sambanova-seeking-500m-in-funding-after-acquisition-talks-with-intel-stall-report)
- fal：[价格页](https://fal.ai/pricing)、[Bloomberg D 轮](https://www.bloomberg.com/news/articles/2025-12-09/sequoia-led-funding-vaults-ai-startup-fal-to-4-5-billion-valuation)、[dealroom](https://dealroom.co/news/126961-fal-targets-8b-valuation-in-new-raise-as-ai-inference-revenue-doubles-to/)
