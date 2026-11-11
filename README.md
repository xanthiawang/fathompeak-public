# 沐仞科技 FathomPeak · 设计与产品资料（公开版）

王子欣在沐仞科技期间（2026 年 10–11 月）做的官网、后台、品牌与调研资料，整理成一个公开仓库，方便交接和查阅。

- 内容以中文为主，按用途分文件夹。
- 只收公开也没关系的东西。公司内部资料（BP、融资、合作协议、内部定价与成本等）不在这里，已另行交接。
- 和公司原来的私有仓库分开，互不影响。

**在线打开：[UI 总览](https://xanthiawang.github.io/fathompeak-public/UI总览.html)**，仓库里所有能打开的界面汇总在一页。

## 目录

| 文件夹 | 内容 |
|---|---|
| [总则](总则/) | **UI 总则与视觉总则**：色卡、字体字号、组件、动态与插画、Logo 使用规则；附原始规范 PDF / PPT |
| [site/projects/website](site/projects/website/) | 官网与后台源码（单文件 `index.html`），含控制台预览、按身份分开的后台、小程序预览、色卡页、开发交接说明 |
| [site/projects/visual-materials](site/projects/visual-materials/) | 视觉素材库：色彩与字体、字体文件、图标、插画与背景、品牌标识、页面截图、公众号视觉 |
| [site/publications](site/publications/) | 业务与合作介绍；Seedance 2.0 移动供应商与官方对照 |
| [brand](brand/) | 现用 Logo v31、当前设计素材、图形探索、UI 视觉交付包、公司介绍 v6、品牌叙事页 v4 |
| [公众号文章](公众号文章/) | 业务与合作、公司介绍、人才招聘、央视报道（Word）；配图与网页版在视觉素材库 `09_公众号视觉` |
| [prototypes](prototypes/) | 交互原型：官网与登录页、首页文案与合作方、产品页总览（三套 + 动画）、行业解决方案、设置密码、按身份分开的后台、绿洲进控制台、企业认证、Logo 替换、配色与字体样张 |
| [历史版本方案](历史版本方案/) | 加入应用页之前的历史方案：最早整站初稿、能源青暖金版、松绿油画版、紫青版、Logo 探索分支 |
| [research](research/) | 基于公开资料的调研与测试：竞品对比与定价、竞品产品线、国内开源模型 Token 价格、硅基流动与海外同类、品牌与界面调研、小程序界面、Seedance 与 H3 测试 |
| [expo-2026](expo-2026/) | 进博会印刷物料（三折页、小册子、易拉宝，中英文） |
| [tools](tools/) | 新闻周检报告、LightX2V WebUI |

## 官网版本

`site/projects/website` 是 **2026-11-06 的官网**（提交 `1405e9f`，加入「应用页」之前），另外补上了后台「认证有礼」：个人账户还没实名认证时，进「钱包与账单」弹一次，完成实名认证到账 ¥15 体验金，所有模型可用，30 天内有效。实名认证服务还没接入，目前不实际发放。

### 在线打开

- 官网：https://xanthiawang.github.io/fathompeak-public/site/projects/website/
- 后台预览（个人）：https://xanthiawang.github.io/fathompeak-public/site/projects/website/#console-preview
- 其他身份：在后台预览地址后面换成 `#console-preview-admin`（企业管理员）、`#console-preview-member`（企业成员）、`#console-preview-root`（超级管理员）

### 本地打开

```bash
python3 -m http.server 8000
```

在仓库根目录运行，然后打开 http://localhost:8000/UI总览.html 。

后台预览是只在浏览器内存里的空账户，不连接真实接口、不写入数据。

## 说明

- 设计规范以 [总则](总则/) 为入口，细节以 `site/projects/website/design/DESIGN_HANDOFF.md` 和在线色卡页为准。
- 每个交互原型只保留最后一轮，同一页面的早期轮次没有收进来。
- 单个超过 50 MB 的文件（下载合集压缩包、长视频）、公开数据集原始文件没有收进来。
- 公司官网：https://www.fathompeak.cn/
