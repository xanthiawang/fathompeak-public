# E｜聚合平台除了卖 Token，还有哪些产品线？

沐仞科技内部竞品资料｜2026-11-02 整理｜覆盖 A 篇 13 家国内平台 + B 篇 12 家海外平台，共 25 家

**问题**：聚合平台除了卖 Token、一体机、芯片和中转运营之外，是不是都有自己其他的产品线？

**怎么读**

- 事实沿用 `A_国内MaaS平台.md`（下称 A）与 `B_海外推理平台.md`（下称 B），只补了几条带日期的产品线变化，新事实都附 URL，访问日期 2026-11-02。
- **核心四项**的记法：**T** = 按 Token 卖推理 API（含自托管开源模型）；**机** = 一体机 / 整机 / 硬件销售；**芯** = 自研芯片；**转** = 转售或路由第三方闭源 API（自己不跑推理）。只写有的项。
- **非核心产品线分类**（固定 11 类）：① 自研模型；② 训练与微调；③ 智能体基础设施；④ 应用层产品；⑤ 多模态生成（按张 / 秒 / 分钟计价）；⑥ 搜索 / 数据 / 向量；⑦ GPU / 算力云；⑧ 原有主业；⑨ 解决方案 / 行业；⑩ 市场 / 生态；⑪ 其他。
- Token Plan、Coding Plan 这类"按月买 Token 额度"的订阅，算 Token 的包装方式，不算独立产品线。
- 标记同 A / B：【媒】【三方】【算】【判断】【待核实】。

---

## 1. 25 家平台逐行表

| 公司 | 核心四项 | 其他产品线（类别） | 计费方式（非核心部分） | 收入占比（公开） | 来源 |
|---|---|---|---|---|---|
| 火山引擎·方舟 | T | ① 豆包 Seed 2.x；⑤ Seedance / Seedream / Seed-Audio；③ AgentKit、方舟 CLI、HiAgent、ArkClaw；④ 扣子、Coding / Agent Plan 订阅；⑧ 火山引擎云 | 多模态按量；订阅 40 / 200 元/月；Seedance 满血版只给年框客户 | MaaS 2025 约 15 亿元，2026 目标 150 亿；Seedance 单月 >10 亿【媒】 | A §1 |
| 阿里云·百炼 | T、芯（平头哥 PPU，自用） | ① Qwen 全系；③ Qwen Cloud 独立站、AgentStudio；⑧ 阿里云公有云；⑩ 伙伴分成（抽 30% + 1.5 倍系数）、繁花计划 | 节省计划预付换折扣；伙伴按消耗分成 | AI 相关 89.71 亿元/季度，占外部收入 >30%；AI 模型与应用 ARR >80 亿 | A §2 |
| 百度智能云·千帆 | T、机（软硬一体） | ① ERNIE 5.1；② ModelBuilder 数据 / 精调 / 评测；⑦ 百舸 GPU 云；⑨ 政企行业大模型、私有化 | GPU 按卡时；私有化按项目 | AI 业务 125 亿元/季度；AI 云基础设施 73 亿（GPU 云 +283%）；上半年中标 13.85 亿【媒】 | A §3 |
| 腾讯云·TokenHub | T | ① 混元 Hy3 / Hy4；③ ADP 智能体开发平台；④ CodeBuddy、WorkBuddy；⑧ 腾讯云 | ADP 平台月费 0–4,880 元 + 资源包【媒】 | 未拆分 | A §4 |
| 硅基流动 | T、机（昇腾等国产卡一体机） | ⑨ 私有化 MaaS / AI 网关（本地部署）；⑩ Token 工厂联合运营（分成）；⑤ BizyAir（ComfyUI 云节点）、图像 / 视频 / 语音 API；⑪ OneDiff 开源 | 许可 + 实施 + 维保；联合运营按服务量分成；预留实例月租 | 2025 收入 5,533 万：公有云 52.9%、本地部署 47.1%；毛利 82.5% vs −119% | A §5 |
| PPIO 派欧云 | T | ⑧ 边缘云 / 边缘 CDN（主业）；③ Agent 沙箱、Agent 托管、MCP / Skills / CLI；⑦ GPU SPOT、Serverless GPU（容器实例下线中）；⑤ 图像 / 视频 API | 沙箱按时长；GPU 按时（4090 1.16 元/时）；边缘云按带宽 | 边缘云占收入 84.5%（2025）【旧】；AI 云 2024 占 1.9%（1,039 万）→ 2025 1.192 亿 / 7.703 亿 ≈ 15.5%【算】 | A §6；[36氪招股书解读](https://www.36kr.com/p/3848636043590528) |
| 无问芯穹 | T、机（一体机、InfiniClaw Box）、芯（LPU IP） | ⑦ AIStudio GPU；⑤ ComfyUI 托管、ONEtake 短剧；③ 智能体服务平台、AgentWorks；⑨ 政府算力平台、运营商合作；① Megrez 端侧模型 | ComfyUI 按秒；GPU 包月（H100 8 卡 11 万元）；积分；项目合同 | 未拆分（2024 营收 >8,500 万，非审计） | A §7 |
| 七牛云 | T、转（上架豆包等） | ⑧ 音视频云 / CDN / 存储（主业）；⑤ 生图 0.3 元/张、视频 0.6 元/秒、OCR / ASR / TTS；⑥ 联网搜索按次；③ MCP / Agent 接入、LAS；⑩ CPS 返现、AI 推荐官 | 按张 / 按秒 / 按次；资源包抵扣 | AI 云 17.57%（2026H1）；AI 相关 24.7%（2025） | A §8 |
| 优刻得 / 优云智算 | T、转（上架 doubao） | ⑦ GPU 实例（4090 / 5090 / A800 / H20）、孔明智算平台；⑧ UCloud 公有云、私有云、自建数据中心；④ AI 生图 / 音频工作室、桌面客户端；③ Agent 托管；⑩ 镜像社区 | GPU 按时 / 日 / 月（4090 2.15 元/时）；高校企业 95 折 | AI 相关 >40%（2026H1）；毛利 28.36%，净利首次转正 | A §9 |
| 并行科技 | T | ⑧ 超算云（北龙超云）；⑦ 智算云 GPU；④ AI Coding 平台（山东联通）；⑨ HPC 系统集成、国资合资智算中心；⑪ 并行算网调度 | 卡时 / 包月 / 长约合同（合同负债 7.36 亿） | 算力服务 94.62%（8.95 / 9.46 亿）；智算 6.47 亿 ≈ 68%【算】；毛利 19.16% | A §10 |
| 共绩科技 | T | ⑦ Serverless 弹性部署、云主机、裸金属、Job 批处理；⑪ 分布式闲时算力调度、算电协同；⑩ 算力供给方生态（个人、网吧、智算中心） | 纯动态按量，无订阅费 | 未公开 | A §11；[北京科委](https://www.ncsti.gov.cn/kjdt/scyq/zgckxc/zgcdt/202601/t20260129_236780.html)、[中华网](https://m.tech.china.com/articles/20250526/202505261677295.html) |
| 蓝耘科技 | T | ⑦ 智算云 GPU、裸金属、容器云、GPU 调度云（2025-10）；⑨ 私有化部署；⑧ IT 系统集成（2023 研报分两块业务） | 阶梯 / 预充值【三方】；GPU 按量 | 未拆分（年报有，待核） | A §12；[东方财富研报 2023-10](https://pdf.dfcfw.com/pdf/H3_AP202310151601475150_1.pdf)、[蓝耘新闻稿](https://lanyun.net/aboutUs/news/lanyun-MetaGen-GPU-scheduling-cloud-engine/_payload.json) |
| 胜算云 | T、转（Claude / GPT / Gemini） | ⑦ GPU 资源、模型集群；⑩ 模型超市（均只见第三方页，弱证据） | 未公开 | 未公开 | A §13【三方】 |
| Together AI | T | ⑦ GPU 集群（可抢占 / 按需 / 预留）、专属推理、AI Factory；② 微调、Post-training、RL；③ Code Sandbox（2024-12-12 收购 CodeSandbox）、Together Link；⑪ 研究品牌（FlashAttention）；⑩ Startup Accelerator、模型厂首发 | H100 1.99–5.49 美元/卡时；训练按 Token 或 GPU 时；沙箱按 vCPU 时 | GPU 出租 60–70%、API 30–40%【三方 Sacra】；毛利约 45%【三方】 | B §1；[Together 博客](https://together.ai/blog/codesandbox-acquisition-together-code-interpreter) |
| Fireworks AI | T | ② SFT / DPO / RFT、Training API（2026-08 GA）；④ Nexus 企业 AI 编程（2026-07）；① Ember-1、SII 基准；⑦ 按需 GPU 部署、预留吞吐、BYOC；③ FireRouter | 训练 0.5–40 美元/M 训练 Token；GPU 8–20 美元/卡时 | 未拆分；ARR >10 亿美元；毛利约 50%【媒】 | B §2 |
| OpenRouter | T（路由）、转 | 无独立非核心产品线。BYOK、预算 / Key 管理、Private Endpoints、Rankings 都是路由平台的功能或加购 | 平台费 5.5% / 8%；BYOK 超额 5% | 平台费年化约 1.4 亿美元【三方】；2026-08 被 Stripe 宣布收购 | B §3 |
| Groq | T、芯（LPU，已非独家授权 NVIDIA） | ⑤ Whisper 转写、Orpheus TTS；⑦ NVIDIA 集群租赁（2026-08 起 NCP）；⑪ 数据中心容量 54 MW → 200 MW | 语音按音频小时 / 百万字符；集群按合同 | 约 1 亿美元【媒·待核实】 | B §4；[insideHPC](https://insidehpc.com/2024/03/groq-acquires-definitive-intelligence-to-launch-groqcloud) |
| Baseten | T | ⑦ Dedicated Inference（按 GPU 分钟）；② Training；① Model Labs（joey / elephant / mammoth）；⑨ FDE 驻场、自托管 / 混合部署；⑪ 多云容量管理 | H100 约 6.50、B200 约 9.98 美元/卡时【算】；Enterprise 报价 | 未拆分；年化约 6 亿美元【媒】 | B §5 |
| DeepInfra | T、转（Claude / Gemini） | ⑦ 专属 GPU、DeepCluster 5 年长约；② Custom LLM 专属部署；⑥ 嵌入 / 重排；⑤ 图像 / 视频 / 音乐 / 语音 | H100 2.90、B300 长约 1.98 美元/卡时；嵌入 0.01 美元/M | 未公开 | B §6 |
| Novita AI | T | ⑦ GPU 实例、Spot、裸金属、Serverless GPU；③ Agent Sandbox；⑥ Embeddings、AI Search（转售 Exa / Tavily） | GPU 按时 / 秒（H100 3.39、Spot 1.70【三方】）；搜索 0.007–0.016 美元/次 | 未公开 | B §7 |
| Replicate | T（按次 / 按秒） | ⑤ 图像 / 视频按输出；⑦ 硬件按秒、私有模型部署；② 快速微调；⑩ 模型市场（5 万+ 社区模型）；⑪ Cog 打包工具 | flux 0.04 美元/张；H100 5.49 美元/卡时；私有模型按在线时长 | 2025-12 被 Cloudflare 以 5,740 万美元收购 | B §8 |
| Modal | 无 Token API（按秒卖算力） | ⑦ Serverless GPU / CPU；③ Sandboxes（2025-01-21 全面开放）；② 多节点训练；⑪ Notebooks、Batch | 按秒；Team 250 美元/月；Sandbox CPU 3× | Sandboxes 约 3 亿 / 年化 10 亿美元 ≈ 30%【算】 | B §9；[Modal 博客](https://modal.com/blog/sandbox-launch) |
| Cerebras | T、芯（WSE）、机（CS-3 / CS-4） | ② Training Cloud；⑦ 专属推理容量（已签 600 MW）；⑪ 硬件销售 | 专属按合同（OpenAI 750 MW） | 2026Q2 云收入 1.26 亿 / 1.801 亿美元 ≈ 70%【算】，+281%；core 毛利 41% | B §10；[新闻稿 2024-08-27](https://cerebras.ai/press-release/cerebras-launches-the-worlds-fastest-ai-inference) |
| SambaNova | T、芯（RDU）、机（SambaRack） | ⑪ SambaStack 软件栈；⑨ 主权 AI、金融（JPMorgan）、电力行业（TEPCO Systems）方案；⑩ Intel 联合销售 | 硬件与本地部署按合同 | 未公开 | B §11 |
| fal | T（按输出计价的生成媒体 API） | ⑤ 图像 / 视频 / 音频 / 3D 按张 / 百万像素 / 秒（主业）；⑦ Serverless GPU；⑨ 企业定制部署；⑩ 模型厂首发（BFL、字节、可灵） | H100 2.49–4.50 美元/卡时；按输出 | 未拆分；年化约 8 亿美元【媒】 | B §12；[startuphub 对 2023 转型的叙述](https://www.startuphub.ai/news/fal-ais-generative-media-ascent-a-strategic-pivot-to-untapped-frontiers)【三方】 |

---

## 2. 类别频次（25 家中出现次数）【算，按上表归类】

| 类别 | 家数 | 哪些 |
|---|---|---|
| ⑦ GPU / 算力云 | 18 | 百度、PPIO、无问、优刻得、并行、共绩、蓝耘、胜算云、Together、Fireworks、Baseten、DeepInfra、Novita、Replicate、Modal、Cerebras、fal、Groq |
| ③ 智能体基础设施 | 11 | 火山、阿里、腾讯、PPIO、无问、七牛、优刻得、Together、Fireworks、Novita、Modal |
| ⑪ 其他 | 11 | 硅基、无问、并行、共绩、Together、Groq、Baseten、Replicate、Modal、Cerebras、SambaNova |
| ⑩ 市场 / 生态 | 10 | 阿里、硅基、七牛、优刻得、共绩、胜算云、Together、Replicate、SambaNova、fal |
| ⑤ 多模态生成 | 9 | 火山、硅基、PPIO、无问、七牛、Groq、DeepInfra、Replicate、fal |
| ⑧ 原有主业 | 9 | 火山、阿里、百度、腾讯、PPIO、七牛、优刻得、并行、蓝耘 |
| ⑨ 解决方案 / 行业 | 8 | 百度、硅基、无问、蓝耘、并行、Baseten、SambaNova、fal |
| ① 自研模型 | 7 | 火山、阿里、百度、腾讯、无问、Fireworks、Baseten |
| ② 训练与微调 | 7 | 百度、Together、Fireworks、Baseten、Replicate、Modal、Cerebras |
| ④ 应用层产品 | 6 | 火山、腾讯、无问、优刻得、并行、Fireworks |
| ⑥ 搜索 / 数据 / 向量 | 4 | 百度、七牛、DeepInfra、Novita |

有 ≥1 条非核心产品线的：**24 / 25**。唯一例外 OpenRouter。胜算云（只见第三方页）和 Replicate（微调、GPU、模型市场都很薄）是"接近纯转售"的两家。Modal 反过来：没有按 Token 的 API，全部是算力和沙箱。

---

## 3. 分析【判断】

**是不是"都有"。** 25 家里 24 家有至少一条 Token、一体机、芯片、中转之外的产品线，只有 OpenRouter 是纯路由。而纯路由和接近纯托管的两家，结局都不是独立长大：OpenRouter 2026-08 被 Stripe 宣布收购，媒体报价 70–80 亿美元，Stripe 买的是"Token 是货币"这一结算位置，而它自己的平台费年化只有约 1.4 亿美元，且每 Token 变现率一年降了约 60%【三方】；Replicate 2025-12 被 Cloudflare 以 5,740 万美元现金收走，远低于历史估值。胜算云靠长三角国创中心扶持，连价格都不公开。所以答案是：是的，几乎都有，而没有的要么被收购，要么没有自己的收入故事。

**哪些线最常见。** 频次最高的是 ⑦ GPU / 算力云（18 家）和 ③ 智能体基础设施（11 家）。算力云是"向下"的默认动作——同一批卡，Token 卖不完就按卡时卖。智能体基础设施是 2025 年后的新增项，沙箱、托管、MCP 几乎成了标配。

**哪些线和利润、估值挂钩。** 从有公开数字的几家看：
- 不是 Token 在赚钱。硅基流动本地部署毛利 82.5%，公有云 −119%，两者收入几乎各半；PPIO 边缘云占收入 84.5%，整体毛利 9.4%，AI 云从 2024 年的 1.9% 升到 2025 年约 15.5%【算】，但还在亏；并行科技算力服务占 94.6%，毛利 19.2%，靠合同预收；优刻得 AI 相关 >40% 后毛利 28.4%、净利首次转正。
- 海外估值最高的几家，溢价都来自非 Token 层：Together GPU 出租占六到七成，估值约 7× 收入；Modal 沙箱年化 3 亿、估值 157.5 亿（约 15.75×）；Baseten 靠专属推理 + FDE，130 亿估值对 6 亿收入（约 22×）；Fireworks 训练 + Nexus，175 亿。Cerebras 上市后云收入占季度收入约 70%，剩余履约义务 254 亿美元来自少数容量合同。
- 结论：**容量合同（⑦）、专用模型 / 训练（①②）、沙箱（③）和本地部署（⑨）在赚钱；通用 Token 托管在补贴。**

**先有 Token 还是先有别的。** 两个方向都有，取决于起点：
- 原有主业 → 加 Token：PPIO 2023 年从边缘云进入 AI 云，2024 年 AI 云只占 1.9%，2026 年起下线 GPU 容器、转向 Token Plan + 沙箱；七牛 2025-02 在音视频云上开 Token API，2025-03 补 OCR / ASR / TTS，2026 做 Token Plan；共绩 2023 年成立做闲时算力调度，2025-05 推 Serverless GPU，再加 MaaS。
- 芯片 / 硬件 → 加 Token 云：Cerebras 2024-08-27 推 Inference，两年后云收入占七成；Groq 2024-03-01 正式发布 GroqCloud，2025-12 把 LPU 技术授权 NVIDIA，2026-08 转为 NVIDIA 集群运营商。
- Token 起家 → 向上下两头加：硅基 2024-06 前后 SiliconCloud 公测，2025 年做国产卡私有化、一体机，到 2025 年本地部署已占收入 47.1%；Together 2024-12-12 收购 CodeSandbox 加沙箱，2026-07 加预留吞吐，2026-10 加 B200 Post-training。
- 共同点：没有一家停在 Token 上。Token 是入口，加线是生存动作，不是扩张动作。

**对电站侧算力公司的含义。** 25 家样本里最赚钱的三类线——长约容量、本地部署、沙箱——沐仞都具备天然条件：电站旁的一体机既是私有化产品，也是可以按卡时或多年合同卖的容量；绿电时段的闲置算力适合沙箱、Batch 这类可排队的负载。样本里唯一和沐仞叙事重叠的共绩，走的是轻资产聚合，没有电站侧确定性。真正的空白是：**没有一家把电价 / 出力曲线写进产品分档**，也没有一家把能源行业当作客户行业（只有 SambaNova 把 TEPCO 放在首页）。Token 还是要卖，但产品线的重心应该放在容量合同和私有化上，这是样本给出的最硬证据。

---

## 4. 待核实

| 项目 | 情况 |
|---|---|
| 阿里百炼微调、腾讯 TokenHub 微调、Together / Novita 多模态 API | 这些平台可能有但 A / B 篇未记录，本表按未记录处理，频次可能偏低 |
| 胜算云 GPU 资源、模型超市 | 只见第三方页（ai-bot.cn） |
| 蓝耘 2025 年报收入拆分、"私有化"是否仍在售 | 年报已发布但未读业务章节 |
| 硅基 SiliconCloud 公测日期 | 按 2024-07 融资报道"公测约一个月"倒推为 2024-06 前后【媒·推算】 |
| GroqCloud 日期 | 2024-02-19 软上线只见 wiki 类来源；2024-03-01 新闻稿为可靠日期 |
| fal 2023 转型 | 第三方叙述，来源之间 2022 / 2023 不一致 |
| Modal Sandboxes 收入 3 亿 | 媒体转述公司口径 |
| Together GPU 占比 60–70%、毛利 45% | Sacra 估算 |
| PPIO 2025 AI 云占比 15.5% | 由 1.192 亿 / 7.703 亿 自算，两次递表口径可能不同 |
| OpenRouter 收购价 | 媒体报道，双方未确认 |
| 频次表 | 归类有主观判断（如 Baseten 专属推理归 ⑦、Cerebras 硬件归 ⑪），换口径会差 1–2 家 |

## 新增来源（访问 2026-11-02）

- PPIO 2024 收入结构：[36氪](https://www.36kr.com/p/3848636043590528)；2023 进入 AI 云：[量子位](https://www.qbitai.com/2025/06/301513.html)
- Together 收购 CodeSandbox（2024-12-12）：[Together 博客](https://together.ai/blog/codesandbox-acquisition-together-code-interpreter)
- Cerebras Inference 发布（2024-08-27）：[新闻稿](https://cerebras.ai/press-release/cerebras-launches-the-worlds-fastest-ai-inference)
- GroqCloud 发布（2024-03-01）：[insideHPC](https://insidehpc.com/2024/03/groq-acquires-definitive-intelligence-to-launch-groqcloud)
- Modal Sandboxes 全面开放（2025-01-21）：[Modal 博客](https://modal.com/blog/sandbox-launch)
- 硅基 SiliconCloud 公测与天使+轮（2024-07 报道）：[钛媒体](https://www.tmtpost.com/7462510.html)
- 七牛 Token API 上线（2025-02）：[老虎资讯](https://itiger.com/news/2510529848)；平台升级多媒体 API：[老虎资讯](https://itiger.com/news/2522640508)
- 共绩成立 2023：[北京科委](https://www.ncsti.gov.cn/kjdt/scyq/zgckxc/zgcdt/202601/t20260129_236780.html)；Serverless GPU 2025-05：[中华网](https://m.tech.china.com/articles/20250526/202505261677295.html)
- 蓝耘两块业务（2023 研报）：[东方财富](https://pdf.dfcfw.com/pdf/H3_AP202310151601475150_1.pdf)；GPU 调度云（2025-10）：[蓝耘官网](https://lanyun.net/aboutUs/news/lanyun-MetaGen-GPU-scheduling-cloud-engine/_payload.json)
- fal 2023 转型：[startuphub.ai](https://www.startuphub.ai/news/fal-ais-generative-media-ascent-a-strategic-pivot-to-untapped-frontiers)【三方】
