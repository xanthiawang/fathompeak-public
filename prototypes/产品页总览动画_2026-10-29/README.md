# 沐仞产品页 · 总览动画

直接打开 `ov-anim.html`。无需构建、服务器或运行时依赖。左侧没有文字；右侧四行 HTML 通过 `ovlayer` 事件同步。

## 嵌入

将 `ov-anim.css`、`ov-anim.js`、`layers/` 和原始 `engineering-stack_2026-10-14.png` 一起复制到网站资源目录，例如 `/assets/overview/`：

```html
<link rel="stylesheet" href="/assets/overview/ov-anim.css">
<div class="ov-anim" data-layer="0" role="img"
     aria-label="接入、调度、计算、电力四层基础设施">
  <img class="ov-original"
       src="/assets/overview/engineering-stack_2026-10-14.png"
       width="1254" height="1254" alt="" decoding="async">
</div>
<script src="/assets/overview/ov-anim.js" defer></script>
```

容器宽度由页面布局决定，组件 `width:100%`、`max-width:620px`、正方形比例；SVG `viewBox="0 0 1254 1254"`。设计范围 280–620px。组件样式均限定在 `.ov-anim` 下；演示页排版样式只在 HTML 内，不需复制。

默认分层资源相对于 **JS 文件所在目录** 寻找 `layers/layer-0.webp` 至 `layer-3.webp`。如需分开放置，在根元素添加 `data-assets="/your/path/layers/"`；该自定义路径相对于页面 URL 解析。原图 `src` 相对于页面 URL 解析。

## 事件接口

```js
const root = document.querySelector('.ov-anim');
root.addEventListener('ovlayer', ({ detail: { layer } }) => {
  document.querySelectorAll('.overview-copy > li').forEach((row, i) => {
    row.classList.toggle('is-active', i === layer);
  });
});
// 随时读取当前层：Number(root.dataset.layer)
```

层号：`0` 接入 / 绿色 Token 交易平台；`1` 调度 / 算电协同世界模型基座；`2` 计算 / FPTM 系列 Token 一体机；`3` 电力 / 光伏、风电、水电场站。

图片加载成功后首次发出层 0 事件；以后每 2 秒切换一次，8 秒一轮。事件从根元素发出并冒泡，`detail` 为 `{layer: 0..3}`。先注册监听器，或使用 `dataset.layer` 同步已经初始化的组件。

鼠标进入某层立即选中该层，暂停轮播、浮动和光点；移开后从该层重新计时 2 秒。触屏不锁定悬停。页面进入后台时暂停，返回后继续。支持同页多个实例。

动态插入根元素后调用 `window.OvAnimation.init(root)`；销毁时调用 `root.ovAnimation.destroy()`，会清理计时器、全局监听器和 SVG，并恢复原图。重复初始化不生成重复 SVG。

## 动画与素材

- 7.6 秒呼吸周期，四层错开 1.9 秒。位移为画布高度的 ±0.24%，在 620px 宽时约 ±1.49px。
- 蓝色 `#2F63B8` 沿可见竖管向下，浅紫 `#D6CBDD` 向上；SVG 分段避开设备和接线盒遮挡。管线光点与所属图片共用同一个浮动组。
- 淡蓝平台边缘光晕与前缘描边同步点亮，650ms 渐变。
- `prefers-reduced-motion: reduce` 时隐藏整个 SVG、停止计时，只显示原始 PNG。无 JS 或任意分层加载失败也保留原图。
- 不新增文字或虚构设施；保留原图颜色。动画叠加只使用指定色板；演示背景为 `#F7F7F5`。
- 四张新增 WebP 合计 **595,426 字节**，低于严格的 600,000 字节上限；原有 PNG 仍用于静态回退，不计入新增图片。无额外 PNG 备份或截图随组件部署。
- 四张图保持完整 1254×1254 透明画布，互斥多边形分区；连接管归上层。不补画原图被遮挡的区域，因此保持很小的浮动幅度。
- WebP 使用近无损 RGB 预处理，再恢复源图 alpha 并无损编码。复合透明通道与原图逐像素一致；可见 RGB 单通道最大误差 4/255，平均绝对误差 0.805811/255。**不是 RGB 位级无损**，没有缩放或几何位移。

## 验证与复现（2026-10-29）

`layers/manifest.json` 记录源图 SHA-256、原始修改时间、分层边界、字节数与压缩误差。分层导出：

```sh
# 开发工具：Python + Pillow + NumPy，以及 libwebp 的 cwebp；网站不需要这些依赖。
python3 build_layers_2026-10-29.py
node --check ov-anim.js
# 安装 jsdom 后运行；也可通过 NODE_PATH 指定现有 jsdom 安装路径。
node verify_ov_2026-10-29.cjs
```

已执行并通过：图片字节上限、alpha 逐像素重建、RGB 误差检查、分层及复合图静态目视检查、管线坐标叠加检查、JS 语法、DOM 初始化、层事件顺序、悬停暂停/恢复、减少动态模式停止计时、后台暂停、销毁清理。DOM 检查结果见 `verification_2026-10-29.json`；其中图片加载完成信号及计时器由测试环境提供，不能替代浏览器验收。

**浏览器验收未完成**：本次环境中系统 Chrome 和官方独立 headless shell 均因 macOS 沙箱 `bootstrap_check_in ... Permission denied (1100)` 无法启动；CUA 浏览器 host 也不可用。静态图检查是 PIL 图像复合检查，不是网页截图。尚未确认实际浏览器中 280/620px 布局、CSS 动画、SVG 发光滤镜和系统减少动态偏好的最终渲染表现。后续在允许启动浏览器的环境打开演示页，检查上述尺寸、四层悬停以及减少动态模式即可。

参考页：https://www.infinigence-ai.com/agentic-infra/llm-inference.html 。已读取页面内容；首屏动态截图同样受浏览器限制，节奏依据任务书指定的安静循环效果实现。

当前目录原本不是 Git 仓库；尝试 `git init` 被沙箱拒绝，因此未能执行提交。所有输入文件均保留，只新增上述组件及验证文件。

## 第二轮修改

2026-10-29。本节覆盖前文第一轮的动画参数、图片字节数和互斥切图说明；第一轮截图与检查报告保留。

- **管道光点**：移除短虚线，10 段可见管道各使用 1 个 SVG 圆点，以 `animateMotion` 沿管道运动，2.4 秒循环、错开出发。实心半径 7、柔光半径 18、柔光透明度 .35；下行为 `#2F63B8`，上行为 `#5284D7` 柔光和描边配白芯，路径反向播放。
- **接缝**：采用向下 **12px 出血重叠**。保留源图真实像素，先绘下层、再由上层覆盖，不生成隐藏结构。四层在原图坐标中 **±9px** 浮动，周期 **7.2 秒**、相邻层错开 **0.8 秒**。当前 ease-in-out 曲线的斜率小于 2，因此相邻层位移差保守上界为 `18 / 3.6 × 2 × 0.8 = 8px`，低于出血量并留出栅格取整余量。修改幅度、周期或相位差时，需重新核算并检查出血。
- **平台流动**：每层 3 条沿原图可见蓝色走线描出的路径，共 12 个半径 4 的光点，3.6 秒循环。与所属平台一起浮动。风机叶片保持原图，未做独立旋转。
- **点亮高亮**：前缘描边透明度 .8、边缘光晕 .6。
- **保持接口**：零运行时依赖，CSS 限定 `.ov-anim`，`ovlayer` 事件不变。悬停及后台暂停同时控制 CSS 浮动和每个实例的 SVG 时间轴；减少动态模式暂停 SVG、停止轮播并显示原始 PNG。
- **资源**：`layers/layer-0.webp` 至 `layer-3.webp` 共 **607,964 字节**，低于 650,000 字节，无新增部署图片。新增出血区域仍保留源 alpha；因图层重叠，不再将完整叠加图描述为 alpha 逐像素重建。manifest 中 `original_owner_alpha_mismatches` 仅指原始归属区域的 alpha 校验。

验证：已运行分层导出、JS 语法和 DOM 行为检查。导出脚本在一个完整周期的 145 个采样时刻检查分区遮罩，内部未覆盖像素数为 0（不含画布上下各 20px 的外边缘）；这是切分遮罩检查，不是浏览器抗锯齿或实际画面验收。DOM 检查覆盖 10 个管道圆点、12 个平台圆点、事件顺序、悬停暂停/恢复 SVG 时间轴、减少动态、后台暂停及销毁，结果见 `verification_round2_2026-10-29.json`。DOM 环境提供图片加载、计时器和 SVG 暂停方法替身，不能证明真实浏览器动画渲染。

本轮尝试启动系统 Chrome，进程以 SIGABRT 退出，工具日志包含 `kill EPERM`，未生成第二轮浏览器截图。最终光点观感、设备遮挡及任何帧是否仍有可见白线，待真实 Chrome 截图验收。直接打开 `ov-anim.html`；已打开的页面请刷新以加载本轮 CSS、JS 和切图。

当前目录无 Git 仓库，`git init` 被沙箱以 `Operation not permitted` 拒绝，无法提交。修改前涉及的文件已保存在 `archive/第二轮修改前_2026-10-29.tar.gz`，不随网站部署。
