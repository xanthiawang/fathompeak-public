"""硅基流动 / Together AI / Fireworks AI 业务线扩张泳道图（每家一张）。

数据来源：本目录 sources/<公司>/ 下的招股书、官方博客、文档更新日志与媒体页面；
每个事件的出处见 硅基流动与海外同类_业务市场营销调研_2026-10-14.qmd 对应章节。
日期只精确到月的事件取当月 15 日作图。
运行：python3 fig_三家业务线时间线_2026-10-14.py
"""
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["PingFang SC", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).parent
PALETTE = ["#8A8F98", "#2563EB", "#0B7285", "#B45309", "#7C3AED",
           "#047857", "#BE185D", "#334155"]

# (泳道, 日期, 标签, 是否为该业务线首次出现)
SILICONFLOW = {
    "title": "硅基流动业务线扩张时间线（2023-08 至 2026-10）",
    "lanes": ["融资", "开源工具", "公有云 Token API", "企业实例/私有化",
              "海外与渠道", "Token 工厂/联合运营"],
    "start": date(2023, 8, 1),
    "events": [
        ("融资", date(2023, 12, 28), "天使\n投后2.8亿", True),
        ("融资", date(2024, 5, 24), "天使+\n投后5.7亿", False),
        ("融资", date(2025, 1, 16), "Pre-A\n投后9.9亿", False),
        ("融资", date(2025, 5, 15), "A 2.86亿\n投后22.9亿", False),
        ("融资", date(2026, 2, 15), "A+\n投后31.2亿", False),
        ("融资", date(2026, 4, 30), "B 5.2亿\n投后50.2亿", False),
        ("融资", date(2026, 6, 9), "B+ 7.4亿\n投后77.4亿", False),
        ("融资", date(2026, 6, 30), "港交所递表", False),

        ("开源工具", date(2023, 11, 6), "OneDiff", True),
        ("开源工具", date(2024, 7, 15), "BizyAir\n(ComfyUI)", False),

        ("公有云 Token API", date(2024, 6, 1), "SiliconCloud\n送3亿Token", True),
        ("公有云 Token API", date(2024, 6, 25), "小模型\n永久免费", False),
        ("公有云 Token API", date(2024, 8, 3), "邀请双方\n各2000万", False),
        ("公有云 Token API", date(2025, 2, 1), "DeepSeek×昇腾\n首发", False),
        ("公有云 Token API", date(2025, 12, 17), "赠金改\n代金券", False),
        ("公有云 Token API", date(2026, 5, 15), "强制实名", False),
        ("公有云 Token API", date(2026, 9, 1), "分时定价\n2–8点半价", False),

        ("企业实例/私有化", date(2023, 12, 15), "首笔收入\n软件订阅", True),
        ("企业实例/私有化", date(2024, 7, 15), "专属实例", False),
        ("企业实例/私有化", date(2025, 2, 10), "昇腾一体机\n私有MaaS", False),
        ("企业实例/私有化", date(2025, 9, 15), "私有化MaaS\n方案", False),

        ("海外与渠道", date(2024, 11, 14), "海外端点", True),
        ("海外与渠道", date(2025, 6, 15), "国际站上线", False),
        ("海外与渠道", date(2025, 6, 19), "阿里云\n繁花计划", False),
        ("海外与渠道", date(2025, 8, 15), "OpenRouter", False),
        ("海外与渠道", date(2026, 5, 15), "海外月收入\n>100万美元", False),

        ("Token 工厂/联合运营", date(2026, 5, 21), "光谷爱计算", True),
        ("Token 工厂/联合运营", date(2026, 6, 15), "60个月\n34.9亿算力长约", False),
        ("Token 工厂/联合运营", date(2026, 7, 2), "贵州移动", False),
        ("Token 工厂/联合运营", date(2026, 8, 26), "浙江数据集团", False),
    ],
    "side": {"港交所递表": -1, "B+ 7.4亿\n投后77.4亿": 1, "B 5.2亿\n投后50.2亿": -1,
             "阿里云\n繁花计划": -1, "国际站上线": 1, "贵州移动": 2,
             "60个月\n34.9亿算力长约": -1},
    "out": "fig_硅基流动业务线时间线_2026-10-14",
}

TOGETHER = {
    "title": "Together AI 业务线扩张时间线（2022 至 2026-10）",
    "lanes": ["融资", "开源研究", "推理 API", "GPU 集群/AI Factory",
              "训练/评测", "收购与新产品", "渠道与海外"],
    "start": date(2022, 9, 1),
    "events": [
        ("融资", date(2023, 5, 15), "种子 $20M", True),
        ("融资", date(2023, 11, 29), "A $102.5M", False),
        ("融资", date(2024, 3, 13), "A2 $106M\n估值$12.5亿", False),
        ("融资", date(2025, 2, 20), "B $305M\n估值$33亿", False),
        ("融资", date(2026, 7, 1), "C $8亿\n估值$83亿", False),

        ("开源研究", date(2022, 11, 29), "GPT-JT", True),
        ("开源研究", date(2023, 4, 17), "RedPajama", False),
        ("开源研究", date(2023, 7, 17), "FlashAttn-2", False),
        ("开源研究", date(2024, 6, 11), "MoA", False),
        ("开源研究", date(2025, 10, 10), "ATLAS", False),
        ("开源研究", date(2026, 3, 5), "AI Native Conf\nFlashAttn-4", False),

        ("推理 API", date(2023, 8, 15), "Together API", True),
        ("推理 API", date(2023, 11, 13), "推理引擎", False),
        ("推理 API", date(2024, 7, 23), "Llama 3.1\n首发", False),
        ("推理 API", date(2025, 2, 12), "DeepSeek R1", False),
        ("推理 API", date(2025, 6, 11), "Batch 5折", False),
        ("推理 API", date(2026, 4, 22), "全面预付", False),
        ("推理 API", date(2026, 7, 8), "Provisioned\nThroughput", False),
        ("推理 API", date(2026, 7, 29), "Kimi首发\n协议", False),
        ("推理 API", date(2026, 10, 1), "Together\nLink", False),

        ("GPU 集群/AI Factory", date(2023, 12, 2), "GPU Clusters", True),
        ("GPU 集群/AI Factory", date(2024, 11, 18), "Hypertec\n3.6万卡", False),
        ("GPU 集群/AI Factory", date(2025, 6, 12), "欧洲2GW\n规划", False),
        ("GPU 集群/AI Factory", date(2025, 9, 9), "Instant\nClusters GA", False),
        ("GPU 集群/AI Factory", date(2026, 7, 20), "YC\n集群", False),
        ("GPU 集群/AI Factory", date(2026, 8, 11), "IBM B300", False),
        ("GPU 集群/AI Factory", date(2026, 8, 31), "HUMAIN\n250MW", False),

        ("训练/评测", date(2023, 8, 16), "微调", True),
        ("训练/评测", date(2025, 7, 28), "Evaluations", False),
        ("训练/评测", date(2026, 10, 13), "Post-training", False),

        ("收购与新产品", date(2024, 12, 12), "收购\nCodeSandbox", True),
        ("收购与新产品", date(2025, 3, 24), "Together Chat", False),
        ("收购与新产品", date(2025, 5, 15), "收购Refuel", False),

        ("渠道与海外", date(2024, 12, 2), "AWS\nMarketplace", True),
        ("渠道与海外", date(2025, 1, 28), "HF Inference\nProviders", False),
        ("渠道与海外", date(2025, 3, 11), "NVIDIA\nCloud Partner", False),
        ("渠道与海外", date(2025, 9, 4), "瑞典上线", False),
        ("渠道与海外", date(2025, 10, 15), "Startup\nAccelerator", False),
    ],
    "side": {"Kimi首发\n协议": 1, "Together\nLink": -1, "Provisioned\nThroughput": -1,
             "全面预付": 1, "IBM B300": -1, "HUMAIN\n250MW": 1, "YC\n集群": 1,
             "NVIDIA\nCloud Partner": 1, "HF Inference\nProviders": -1},
    "out": "fig_Together业务线时间线_2026-10-14",
}

FIREWORKS = {
    "title": "Fireworks AI 业务线扩张时间线（2022 至 2026-10）",
    "lanes": ["融资", "Serverless 推理/首发", "专用部署/企业", "训练",
              "自有模型", "多云与硬件", "Agent/编程"],
    "start": date(2023, 6, 1),
    "events": [
        ("融资", date(2024, 3, 26), "A $25M\n(公开)", True),
        ("融资", date(2024, 7, 11), "B $52M\n估值$5.5亿", False),
        ("融资", date(2025, 10, 28), "C $250M\n估值$40亿", False),
        ("融资", date(2026, 7, 15), "D $15亿\n估值$175亿", False),

        ("Serverless 推理/首发", date(2023, 8, 17), "平台发布", True),
        ("Serverless 推理/首发", date(2023, 12, 14), "Mixtral\n抢先上线", False),
        ("Serverless 推理/首发", date(2024, 4, 18), "Llama 3\n联合首发", False),
        ("Serverless 推理/首发", date(2025, 1, 24), "DeepSeek R1", False),
        ("Serverless 推理/首发", date(2026, 6, 10), "下线\n音频/图像", False),
        ("Serverless 推理/首发", date(2026, 7, 27), "Kimi K3首发\n美国托管", False),
        ("Serverless 推理/首发", date(2026, 9, 1), "US-only\n1.5倍价", False),

        ("专用部署/企业", date(2023, 10, 27), "SOC2/HIPAA", True),
        ("专用部署/企业", date(2024, 3, 1), "专用部署\n后付费", False),
        ("专用部署/企业", date(2025, 6, 16), "Virtual Cloud\nBYOC", False),
        ("专用部署/企业", date(2026, 7, 1), "自助改预付", False),

        ("训练", date(2024, 3, 8), "微调", True),
        ("训练", date(2024, 9, 18), "Multi-LoRA", False),
        ("训练", date(2025, 6, 9), "RFT Beta", False),
        ("训练", date(2026, 4, 6), "Training\n预览", False),
        ("训练", date(2026, 8, 31), "Training\nAPI GA", False),

        ("自有模型", date(2023, 12, 20), "函数调用\n模型", True),
        ("自有模型", date(2024, 11, 15), "f1", False),
        ("自有模型", date(2026, 9, 23), "Ember-1", False),

        ("多云与硬件", date(2024, 10, 15), "AMD\nFireAttn V3", True),
        ("多云与硬件", date(2025, 10, 20), "AMD\n多年协议", False),
        ("多云与硬件", date(2025, 11, 24), "AWS SCA", False),
        ("多云与硬件", date(2026, 3, 8), "收购Hathora\n上微软Foundry", False),

        ("Agent/编程", date(2025, 8, 4), "Eval Protocol", True),
        ("Agent/编程", date(2026, 7, 26), "Nexus", False),
        ("Agent/编程", date(2026, 9, 28), "FireRouter", False),
    ],
    "side": {"AWS SCA": 1, "AMD\n多年协议": -1},
    "out": "fig_Fireworks业务线时间线_2026-10-14",
}


def draw(spec: dict) -> None:
    lanes = spec["lanes"]
    color = {lane: PALETTE[i % len(PALETTE)] for i, lane in enumerate(lanes)}
    side = spec.get("side", {})
    fig, ax = plt.subplots(figsize=(15, 1.0 * len(lanes) + 1.6), dpi=150)
    y_of = {lane: len(lanes) - i for i, lane in enumerate(lanes)}
    end = date(2026, 10, 31)
    for lane in lanes:
        y = y_of[lane]
        ax.axhline(y, color="#E5E7EB", lw=1, zorder=0)
        first = min(d for l, d, _, _ in spec["events"] if l == lane)
        ax.plot([first, end], [y, y], color=color[lane], lw=3, alpha=0.25,
                solid_capstyle="butt", zorder=1)
    seen: dict[str, int] = {}
    for lane, d, label, is_first in spec["events"]:
        y = y_of[lane]
        k = seen.get(lane, 0)
        seen[lane] = k + 1
        ax.scatter(d, y, s=70 if is_first else 36, color=color[lane],
                   edgecolor="white", lw=1, zorder=3, marker="D" if is_first else "o")
        pos = side.get(label, 1 if k % 2 == 0 else -1)  # ±1 常规，±2 再错开一层
        up = pos > 0
        off = 13 + 22 * (abs(pos) - 1)
        ax.annotate(label, (d, y), xytext=(0, off if up else -off),
                    textcoords="offset points", ha="center",
                    va="bottom" if up else "top", fontsize=7.4,
                    color="#1F2937", linespacing=1.05)
    ax.set_yticks([y_of[l] for l in lanes])
    ax.set_yticklabels(lanes, fontsize=10)
    for t in ax.get_yticklabels():
        t.set_color(color[t.get_text()])
    ax.set_ylim(0.35, len(lanes) + 0.8)
    ax.set_xlim(spec["start"], date(2026, 11, 20))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.tick_params(axis="x", labelsize=9)
    for yr in range(spec["start"].year + 1, 2027):
        ax.axvline(date(yr, 1, 1), color="#D1D5DB", lw=0.8, ls="--", zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title(spec["title"] + "（◆ = 该业务线首次出现）", fontsize=12.5, loc="left", pad=12)
    fig.text(0.01, 0.01, "来源：招股书、官方博客与文档更新日志、媒体报道；核查日 2026-10-14。"
             "融资金额为人民币（硅基流动）或美元（海外）。", fontsize=8, color="#6B7280")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    for ext in ("png", "pdf"):
        fig.savefig(HERE / f"{spec['out']}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print("saved", spec["out"])


if __name__ == "__main__":
    for spec in (SILICONFLOW, TOGETHER, FIREWORKS):
        draw(spec)
