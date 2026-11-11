"""核查高亮版网站（Zixin 2026-10-14："做一个html把所有占位符信息高亮"；"你定的文案……html 高亮不确定的地方"；登录页"保持"）。
不改任何文字，只在页面上给有问题的字加颜色标记，鼠标悬停看说明；右侧"核查清单"可逐条定位。
依据：事实核查子代理报告（企业信息表、BP、报价单 10-08、飞书梳理、英文资料）+ 设计审查 + 占位符扫描 + 公开网络核查（央视/杭州网、英伟达中国、清华 x-lab、new-api GitHub、Anthropic 文档、汕头试点报道；2026-10-14）。
类别：x 与资料矛盾 / n 无出处 / c 示例当真 / p 占位符 / q 待确认（含 Zixin 定的文案）。
用法：python3 -I build_factcheck_highlight_2026-10-14.py <预览 index.html> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()

TRACE = '平台也销售其他算力中心生产的词元（企业信息表第 10、17 行），逐模型供给来源未核实（飞书梳理 §4、§7）。建议只对自营电站节点的订单这么说，或标"规划中"。'
TENSE = '一体机目前在"机房与电站实验测试"阶段（信息表第 170 行），电站项目多在协议或方案阶段（第 148–163 行）。建议改进行时，如"正在电站旁试点部署"。'
QUOTE = '你定的文案。唯一出处是 10-08 单一客户机密报价单（只有 GLM-5.3 是 5 折，有效期到 11-07，保密条款还写着别家公司名）。需公司确认能否公开。'
NODE = '示例数据里用了电站名：北京大兴、新疆、天津分布式在任何资料里都没有；河北深州、江苏高邮、江西水电仍在方案或筛选阶段（信息表第 148–159 行）。建议用"示例电站 A/B"或删除。'
API3 = '公开核查：#api 页的文字（如"根据请求头自动识别返回格式"）以及 Sora、Kling、即梦、DALL·E、gpt-4o-realtime 等，都来自开源网关 new-api 的官方接口文档模板（GitHub QuantumNous/new-api），不是沐仞实际开通的接口。建议只保留实际开通的接口。'
EDU = '教育优惠的认证规则和折扣力度都没有公司资料（备忘："待公司定"）。'
NOTRY = '客户端兼容性未实测（飞书梳理 §2）。'

R = [
    # —— 首页 ——
    ('x', '绿电从哪来，每一单都查得到', TRACE),
    ('x', '每笔订单一张产地卡', TRACE),
    ('x', '每笔订单均可追溯至电站', TRACE),
    ('x', '订单的能源记录', TRACE),
    ('x', '模型是同一个，区别在算力来源', '不是所有调用都调度到电站一体机。' + TRACE),
    ('x', '词元用电站富余的绿电生产，成本更低', '不是所有词元都由电站绿电生产；"成本更低"的因果也没有数据。' + TRACE),
    ('x', '绿色词元，直供全球', '不是所有词元都是绿色词元。' + TRACE + ' 备选标语："同样的模型，更低的账单。"'),
    ('x', '一体机部署在电站旁', TENSE),
    ('x', '部署于光伏、风电、水电等新能源电站', TENSE),
    ('x', '我们把算力搬到电站旁边', TENSE + ' 可改"我们正在把算力搬到电站旁边"。'),
    ('q', '低成本、高可用、全兼容', '你定的文案。"高可用"没有可用率/SLA 数据；"全兼容"目前只确认 OpenAI 与 Gemini 格式。需公司确认。'),
    ('q', '价低至 5', QUOTE),
    ('q', '企业报价低至公开价 5', QUOTE),
    ('q', '一个平台，低至半价', QUOTE),
    ('q', '企业报价 5', QUOTE + ' 8.2 折对应 kimi-k3，网站模型目录里没有。'),
    ('q', '连起所有的 AI 工具', '你定的文案。"所有"是绝对化说法，客户端兼容性未测试。'),
    ('q', '免费试用 API', '你定的文案。目前没有自助试用额度政策；按钮通向的登录页所有方式都"尚未开通"。报价单只写"如需试用额度，欢迎申请免费测试包"（企业、需申请）。'),
    ('p', '<沐仞接入地址>', '占位符。已核实真实地址：https://api.fathompeak.cn/v1'),
    ('p', 'YOUR_API_HOST', '占位符。已核实真实地址：https://api.fathompeak.cn（控制台显示 /v1/chat/completions）'),
    ('c', '北京大兴区分布式光伏电站', NODE), ('c', '天津分布式光伏电站', NODE), ('c', '新疆集中式光伏电站', NODE),
    ('c', '江苏高邮集中式光伏电站', NODE), ('c', '河北深州集中式光伏电站', NODE), ('c', '江西水电电站', NODE),
    ('c', 'Qwen3.8-Plus', '不在网站模型目录（7 个模型）里，价格也没有出处。'),
    ('c', 'MiniMax-H3', '不在网站模型目录（7 个模型）里；指南还推荐它写代码，照抄会调用失败。'),
    ('c', '天津分布式光伏', '产地卡示例：这座电站不在任何资料里。'),
    ('c', '38.6 kWh', '产地卡示例：38.6 kWh 对应 −3.72 kg CO₂e（约 0.096 kg/kWh），远低于电网排放因子，ESG 读者会质疑。'),
    ('q', 'DeepSeek 官方价格页', 'BP 第 26 页写 DeepSeek 高峰定价自 2026 年 7 月起，这里写 8 月；负电价数据不在公司资料里，建议附来源链接。'),
    ('q', '官方 API 最贵的时候，电站的电最便宜', '比较级说法；两组数据来自不同来源和年份（图注已说明）。建议附来源、语气放软。'),
    ('q', '出海运营主体持网信办词元出海批复', '资料提到（信息表第 5、106、122 行；BP），但没看到批复文件；资料里"牌照/批复/资质确认"说法不一。公开核查：新闻只说汕头华侨试验区"来数加工"试点经"国家有关部委"批复，没点名网信办，报道里也没有沐仞。'),
    ('q', '中央网信办词元出海业务批复', '资料提到，但没看到批复文件；资料里"牌照/批复/资质确认"说法不一。公开核查：新闻只说汕头"来数加工"试点经"国家有关部委"批复，没点名网信办，也没有沐仞。'),
    # —— 关于 ——
    ('x', '落成算电协同试点', '试点是短期目标（信息表第 21 行）；天津能源项目在"数据交换与技术方案设计阶段"（第 148 行）；只完成了中美跨境调用"验证"（第 106 行）。建议："正在推进试点；已完成中美跨境词元调用与结算验证"。'),
    ('x', '共建算电协同联合研发中心', '信息表第 172 行：研发中心"正在履行研究院内部审核程序"；公开搜索也没有相关报道。建议改"正在筹建"。'),
    ('n', '创始人与核心团队的科研来源', '资料只说团队成员来自清华，不等于"机构支持"。建议移到团队背景。'),
    ('n', '计算机与人工智能方向技术骨干来源', '资料只说团队成员来自北大，不等于"机构支持"。建议移到团队背景。'),
    ('n', '赢在 AI+', '公开核查：央视/杭州网 2026-09-24 报道确认路畅团队参加《赢在AI+》第二季"智效跃迁"专场（9 月 25 日播出），但报道没有给任何团队排名。"第一名"只有 BP 第 31 页写，最新企业信息表的荣誉里也没有。建议改"参加总台《赢在AI+》智效跃迁专场"，拿到名次证明再写第一名。'),
    ('n', '均有开放职位', '没有公司资料支持。'),
    ('q', '微软亚洲研究院、字节跳动、英伟达', '信息表写的是"前……"，建议"曾任职于"；团队简历里没有英伟达。'),
    ('q', '数十篇论文', 'BP 注明为团队成员累计、含申请中。建议"团队成员累计……（含申请中）"。'),
    ('q', '两个月内完成天使轮', '信息表前后不一（第 6、49 行"两个月两轮"，第 175 行"一个月内完成千万级天使轮"）；融资信息对外公开需公司确认。'),
    # —— 产品与服务 / 电站合作 ——
    ('x', '100%绿电', '节点标签、评分、电价系数来自测试站前端写死的数据，不是真实运行节点；"100%绿电"是绝对化说法。建议删除。'),
    ('c', '超低碳', '节点标签来自测试站前端写死的数据。'), ('c', '优先曝光', '节点标签来自测试站前端写死的数据（卖方运营用语）。'),
    ('c', '低价捡漏', '节点标签来自测试站前端写死的数据（卖方运营用语）。'),
    ('q', 'DeepSeek 为空闲时段价格', '报价单里是 DeepSeek-V4.1-Flash，刊例输出 4 元（闲时）/ 8 元（忙时）；网站写 V4-Flash ¥4.50。需在平台核对型号与价格。'),
    ('q', '300P', '算力单位/精度（FP16/FP8/INT8）没写。'),
    ('n', '可部署在客户场站', '资料只说资产方采购一体机部署于能源场站、闲置算力中心和边缘节点（信息表第 14、99 行），没有"客户机房/实验室、沐仞远程运营"。'),
    ('c', '中午时段价格只有外面的1/3', '编造的用户评价（标了示例也有法律风险）。建议删除整块"节点评价"。'),
    ('c', '接入手册 PDF', '这份 PDF 不存在，点了只弹提示。'),
    # —— 定价 / 教育 / 企业 ——
    ('n', '在线充值', '个人在线充值到账未验证（9/24 尚未接通；现在钱包有微信/支付宝入口，但没测过）。企业"预付或月结"有报价单支持。'),
    ('n', '从余额扣费', '个人在线充值到账未验证。'),
    ('n', '富余绿电时段的词元更便宜', '目前没有按绿电时段定价；报价单 DeepSeek 的闲时/忙时按钟点（22–8 点），不是绿电时段。'),
    ('n', 'edu.cn', EDU), ('n', '学生证', EDU), ('n', '按学期结算', EDU),
    ('q', '来数加工在境内合规处理', '没有回答国内客户"数据会不会出境"；隐私政策又写请求可能转发给第三方模型服务商。建议重写。'),
    # —— 文档 / 指南 / API ——
    ('x', '可用率与故障补偿写进服务协议', '用户服务协议里没有 SLA，写的是按"现状"提供并有责任上限。'),
    ('n', 'Claude Code', '公开核查：Anthropic 官方文档写明"不支持通过任何网关让 Claude Code 调用非 Claude 模型"，且网关要提供 Anthropic 格式接口。经沐仞用 GLM/DeepSeek 等驱动 Claude Code 不在官方支持范围内。'),
    ('n', 'Codex CLI', NOTRY), ('n', 'CC Switch', NOTRY),
    ('c', '完整结构图可向商务索取', '暗示的材料目前没有。'),
    ('n', '每周一封', '峰谷周报一期都没发过（往期周报页会直接跳到新闻页）。'),
    ('n', 'Sora', API3), ('n', 'dall-e-3', API3), ('n', 'gpt-image-1', API3), ('n', 'gpt-4o-realtime', API3),
    ('n', 'Kling', API3), ('n', '可灵', API3), ('n', '即梦', API3), ('n', 'minimax-h3-fl2va', 'new-api 模板里没有这个名字，可能来自真实平台的模型列表；网站模型目录里没有。需在平台核对。'),
    ('n', 'Anthropic', '未确认平台支持 Anthropic（Claude）格式；之前记录是不支持。'),
    # —— 法务 / 页脚 / 新闻 / 其他 ——
    ('q', '拼好算', '网站其他地方都叫"绿色词元交易平台"（信息表第 74、87 行另有"低碳词元直销平台"）；法律文件里的平台名需公司确认，也有品牌近似风险。'),
    ('n', '融合智慧算网中枢', '网站其他地方没有这个服务。'),
    ('q', '粤ICP备2026126659号', '公司资料里没有；"粤"字号通常属于广东主体，却和北京沐仞并列。公开核查：两个第三方备案查询站都没返回结果；工信部官网查询要输验证码，请你在 beian.miit.gov.cn 手动查 fathompeak.cn 的备案主体。'),
    ('q', 'fathompeak@163.com', '只来自测试站页脚；BP 和英文资料给的是电话和官网。需确认官方邮箱；表单经 formsubmit.co 转发，隐私政策没有披露。'),
    ('q', '首都热线', '这条新闻的链接现在显示"信息未审核或下架中"，建议换稳定来源。'),
    ('q', '预告该期节目', '节目已于 9 月 25 日播出，"预告"过时了。改过去式并附播出链接。'),
    ('p', '产品更新记录', '空壳页：没有任何更新条目，导航里也没有入口。建议先隐藏。'),
    ('c', '未注册的手机号验证后将自动创建账户', '所有登录方式都"尚未开通"，这句承诺不会发生。（登录页按你的决定保持不变，这里只标出）'),
]
IMG = [
    ('x', 'nvidia-inception', '公开核查：英伟达中国官网与清华 x-lab 页面显示，Inception 会员和 2024 年度"荣耀企业"是深涌智能（路畅曾任联合创始人兼 COO），不是沐仞（信息表第 27 行同）。建议删除。'),
    ('x', 'stategrid', '国家电网是创始人过往的"青海省国网算电协同调度项目"，不是公司合作方。建议删除。'),
    ('n', 'longi', '隆基在任何资料文字里都没有（只出现在 BP 第 4 页 logo 墙）；公开搜索也没有沐仞与隆基合作的报道。'),
    ('n', 'ascend-cann', '昇腾 CANN 在任何资料文字里都没有；公开搜索也没有沐仞与华为昇腾合作的报道。'),
    ('q', 'cgn', '中广核：老挝 1GW 只是初步合作意向；logo 也让匿名案例露了名。'),
    ('q', 'shenzhen-gas', '深圳燃气：江苏高邮项目仍在论证。'),
    ('q', 'boe', '京东方：仍在筛选候选电站。'),
]
NOTES = [
    ('c', '控制台（要登录才看得到）', '生成看起来真实的 sk- 密钥、"已提交"之类的假提示、推荐计划、订单与产地卡、"绿电折扣"列、支付宝/微信充值、TOTP/Passkey——都是界面示意，没有接通。'),
    ('c', '往期周报页', '一期都没有；打开会跳到新闻页，按返回键会被困住。'),
    ('q', '英文版', '"出海运营主体"译成 overseas entity（实际是汕头主体）；愿景译成已完成时；"the first"容易被理解为行业首个。'),
]
VERIFIED = '已核实为真：公司名/地址/研发地；创始人路畅背景；团队 20 余人；Q3 已签订单超 6,000 万、海外超 83%、新加坡 5,000 万、清华系 1,000 万；Soul 战略合作；4 个电站案例及状态；北京卫视第一、挑战杯亚军、国创赛十佳、互联网+ 金奖、U25、荣誉 40 余项；张文宇简历；两轮天使；GLM-5.3 / GLM-5.3-Flash / DeepSeek-V4-Pro 刊例价；4 条新闻都真实发生。'

rules = [{'id': f'r{i}', 'c': c, 't': t, 'n': n} for i, (c, t, n) in enumerate(R)]
imgs = [{'id': f'i{i}', 'c': c, 'img': k, 'n': n} for i, (c, k, n) in enumerate(IMG)]
notes = [{'c': c, 't': t, 'n': n} for c, t, n in NOTES]

CSS = '''
<style id="fc-css">
mark.fc,#home2 mark.fc{all:unset;color:inherit;border-radius:2px;padding:0 1px;cursor:help;border-bottom:2px solid var(--fcc);background:var(--fcbg);-webkit-box-decoration-break:clone;box-decoration-break:clone}
mark.fc-x,#home2 mark.fc-x,.fc-img.fc-x,#home2 .fc-img.fc-x{--fcc:#E5484D;--fcbg:rgba(229,72,77,.22)}
mark.fc-n,#home2 mark.fc-n,.fc-img.fc-n,#home2 .fc-img.fc-n{--fcc:#F76B15;--fcbg:rgba(247,107,21,.22)}
mark.fc-c,#home2 mark.fc-c,.fc-img.fc-c,#home2 .fc-img.fc-c{--fcc:#8E4EC6;--fcbg:rgba(142,78,198,.2)}
mark.fc-p,#home2 mark.fc-p,.fc-img.fc-p,#home2 .fc-img.fc-p{--fcc:#D4A106;--fcbg:rgba(255,214,10,.45)}
mark.fc-q,#home2 mark.fc-q,.fc-img.fc-q,#home2 .fc-img.fc-q{--fcc:#2F63B8;--fcbg:rgba(47,99,184,.18)}
.fc-img,#home2 .fc-img{outline:3px solid var(--fcc)!important;outline-offset:3px;border-radius:4px;cursor:help}
body.fc-off-x .fc-x,body.fc-off-n .fc-n,body.fc-off-c .fc-c,body.fc-off-p .fc-p,body.fc-off-q .fc-q{background:none!important;border-bottom:0!important;outline:0!important}
.fc-flash{animation:fcflash 1.4s ease 2}
@keyframes fcflash{50%{box-shadow:0 0 0 6px rgba(255,214,10,.9)}}
#fc-ui{position:fixed;right:14px;top:92px;z-index:10000;font:13px/1.5 system-ui,-apple-system,"PingFang SC",sans-serif;color:#111}
#fc-ui .tg{display:flex;align-items:center;gap:8px;margin-left:auto;padding:8px 14px;border:0;border-radius:999px;background:#111;color:#fff;font:600 13px system-ui,"PingFang SC";cursor:pointer;box-shadow:0 4px 18px rgba(0,0,0,.25)}
#fc-ui .pn{display:none;width:400px;max-width:calc(100vw - 28px);max-height:76vh;overflow:auto;margin-top:8px;padding:14px;border-radius:14px;background:#fff;box-shadow:0 12px 40px rgba(0,0,0,.25)}
#fc-ui.open .pn{display:block}
#fc-ui h4{margin:14px 0 6px;font:600 13px system-ui,"PingFang SC";color:#555}
#fc-ui .lg{display:flex;flex-wrap:wrap;gap:6px}
#fc-ui .lg label{display:inline-flex;align-items:center;gap:5px;padding:3px 8px;border-radius:999px;background:#f2f2f2;cursor:pointer;font-size:12px}
#fc-ui .dot{display:inline-block;width:10px;height:10px;border-radius:50%}
#fc-ui .it{display:grid;grid-template-columns:auto 1fr auto;gap:8px;align-items:start;padding:8px 0;border-top:1px solid #eee}
#fc-ui .it b{font-weight:600}
#fc-ui .it p{margin:2px 0 0;color:#555;font-size:12px}
#fc-ui .it button{border:1px solid #ddd;background:#fff;border-radius:8px;padding:2px 8px;font-size:12px;cursor:pointer}
#fc-ui .it button[disabled]{opacity:.4;cursor:default}
#fc-ui .ok{margin-top:10px;padding:8px 10px;border-radius:10px;background:#EEF7EE;color:#245c2a;font-size:12px}
#fc-tip{position:fixed;z-index:10001;max-width:340px;padding:10px 12px;border-radius:10px;background:#111;color:#fff;font:12.5px/1.55 system-ui,"PingFang SC",sans-serif;pointer-events:none;display:none;box-shadow:0 8px 24px rgba(0,0,0,.3)}
#fc-tip b{display:block;margin-bottom:3px}
@media (max-width:600px){#fc-ui{top:auto;bottom:84px;right:10px}}
</style>
'''

JS = '<script id="fc-js">\n(function(){\nvar R=' + json.dumps(rules, ensure_ascii=False) + ',IMG=' + json.dumps(imgs, ensure_ascii=False) + \
     ',NOTES=' + json.dumps(notes, ensure_ascii=False) + ',VERIFIED=' + json.dumps(VERIFIED, ensure_ascii=False) + r''';
var CAT={x:['与资料矛盾','#E5484D'],n:['无出处','#F76B15'],c:['示例当真','#8E4EC6'],p:['占位符','#D4A106'],q:['待确认（含你定的文案）','#2F63B8']};
var BY={}; R.concat(IMG).forEach(function(r){BY[r.id]=r});
var TR=R.slice().sort(function(a,b){return b.t.length-a.t.length});
var SKIP='script,style,textarea,option,title,mark.fc,#fc-ui,#fc-tip';
function wrap(node){ var txt=node.nodeValue,best=null;
  for(var i=0;i<TR.length;i++){var j=txt.indexOf(TR[i].t); if(j>=0&&(!best||j<best.j||(j===best.j&&TR[i].t.length>best.r.t.length))) best={j:j,r:TR[i]}}
  if(!best) return; var mid=node.splitText(best.j), rest=mid.splitText(best.r.t.length);
  var m=document.createElement('mark'); m.className='fc fc-'+best.r.c; m.setAttribute('data-rid',best.r.id);
  mid.parentNode.replaceChild(m,mid); m.appendChild(mid); wrap(rest) }
function scan(){ var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentNode; if(!p||!p.closest||p.closest(SKIP)) return 2; return n.nodeValue.trim()?1:2}});
  var l=[],n; while((n=w.nextNode())) l.push(n); l.forEach(wrap);
  [].forEach.call(document.querySelectorAll('img:not(.fc-img)'),function(im){var src=im.getAttribute('src')||''; IMG.forEach(function(r){ if(src.indexOf('/'+r.img+'.')>=0||src.indexOf(r.img+'.png')>=0){im.classList.add('fc-img','fc-'+r.c); im.setAttribute('data-rid',r.id)} })});
  count() }
var busy=false,tmr=null; new MutationObserver(function(recs){ if(busy) return; if(recs.every(function(m){var t=m.target, el=t.nodeType===1?t:t.parentNode; return el&&el.closest&&el.closest('#fc-ui,#fc-tip')})) return; clearTimeout(tmr); tmr=setTimeout(function(){busy=true; scan(); busy=false},350) }).observe(document.body,{childList:true,subtree:true,characterData:true});
function routeOf(el){ var s=el.closest('[data-route]'); return s?s.getAttribute('data-route'):'(全站共用：导航/页脚/浮窗)' }
var ui=document.createElement('div'); ui.id='fc-ui'; ui.innerHTML='<button class="tg" type="button">核查清单 <span id="fc-n"></span></button><div class="pn"><div style="font-size:12px;color:#666">核查高亮版 · 不是线上网站 · 请在<b>中文模式</b>下看。鼠标停在高亮字上看说明，点"定位"跳到对应位置。</div><h4>颜色（点击可隐藏该类）</h4><div class="lg" id="fc-lg"></div><div id="fc-list"></div><h4>页面上没法高亮的</h4><div id="fc-notes"></div><div class="ok">'+VERIFIED+'</div></div>';
document.body.appendChild(ui); var tip=document.createElement('div'); tip.id='fc-tip'; document.body.appendChild(tip);
ui.querySelector('.tg').addEventListener('click',function(){ui.classList.toggle('open')});
document.getElementById('fc-lg').innerHTML=Object.keys(CAT).map(function(k){return '<label><input type="checkbox" checked data-k="'+k+'"><span class="dot" style="background:'+CAT[k][1]+'"></span>'+CAT[k][0]+' <span data-cnt="'+k+'"></span></label>'}).join('');
[].forEach.call(document.querySelectorAll('#fc-lg input'),function(c){c.addEventListener('change',function(){document.body.classList.toggle('fc-off-'+c.dataset.k,!c.checked)})});
document.getElementById('fc-notes').innerHTML=NOTES.map(function(n){return '<div class="it"><span class="dot" style="background:'+CAT[n.c][1]+';margin-top:5px"></span><div><b>'+n.t+'</b><p>'+n.n+'</p></div><span></span></div>'}).join('');
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function count(){ var groups={}, per={x:0,n:0,c:0,p:0,q:0};
  R.concat(IMG).forEach(function(r){ var els=document.querySelectorAll('[data-rid="'+r.id+'"]'); var g=els.length?routeOf(els[0]):'(打开对应页面后才会出现)'; (groups[g]=groups[g]||[]).push({r:r,k:els.length}); if(els.length) per[r.c]+=1 });
  var total=0; Object.keys(per).forEach(function(k){total+=per[k]; var e=document.querySelector('[data-cnt="'+k+'"]'); if(e) e.textContent=per[k]});
  document.getElementById('fc-n').textContent='('+total+' 项)';
  var order=Object.keys(groups).sort(function(a,b){return (a.charAt(0)==='('?1:0)-(b.charAt(0)==='('?1:0)});
  document.getElementById('fc-list').innerHTML=order.map(function(g){return '<h4>'+esc(g==='home'?'首页':g)+'</h4>'+groups[g].map(function(o){var r=o.r; return '<div class="it"><span class="dot" style="background:'+CAT[r.c][1]+';margin-top:5px"></span><div><b>'+esc(r.t||('logo：'+r.img))+'</b>'+(o.k>1?' <span style="color:#999">×'+o.k+'</span>':'')+'<p>'+esc(r.n)+'</p></div><button type="button" data-go="'+r.id+'"'+(o.k?'':' disabled')+'>定位</button></div>'}).join('')}).join('');
  [].forEach.call(document.querySelectorAll('#fc-list [data-go]'),function(b){b.addEventListener('click',function(){ var el=document.querySelector('[data-rid="'+b.dataset.go+'"]'); if(!el) return; var rt=el.closest('[data-route]'); var go=function(){ el.scrollIntoView({block:'center',behavior:'smooth'}); el.classList.add('fc-flash'); setTimeout(function(){el.classList.remove('fc-flash')},3000) };
    if(rt&&!rt.classList.contains('on')){ location.hash='#'+rt.getAttribute('data-route'); setTimeout(go,600) } else go() })}) }
document.addEventListener('mouseover',function(e){ var t=e.target.closest&&e.target.closest('[data-rid]'); if(!t||t.closest('#fc-ui')){tip.style.display='none';return} var r=BY[t.getAttribute('data-rid')]; if(!r) return;
  tip.innerHTML='<b style="color:'+CAT[r.c][1]+'">'+CAT[r.c][0]+'</b>'+esc(r.n); tip.style.display='block' });
document.addEventListener('mousemove',function(e){ if(tip.style.display!=='block') return; var x=Math.min(e.clientX+14,innerWidth-360), y=e.clientY+18; if(y+tip.offsetHeight>innerHeight) y=e.clientY-tip.offsetHeight-12; tip.style.left=x+'px'; tip.style.top=y+'px' });
document.title='【核查高亮】'+document.title;
setTimeout(scan,600);
})();
</script>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
k = s.rindex('</body>'); s = s[:k] + JS + s[k:]
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT, len(rules), 'text rules,', len(imgs), 'logo rules')
