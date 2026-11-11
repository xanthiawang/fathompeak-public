# 控制台订单改版（接在 build_gap_now_2026-10-14.py 之后）：两个页签都是空状态；
# 产地卡只做字段说明，不填数值、不加示例标签（交易看板 T 本身是测试站演示数据，不能当订单来源）。
# 用法：python3 build_orders_fix_2026-10-14.py <site/index.html>
import re, sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'anchor count {n}: {old[:80]!r}')
    s = s.replace(old, new)

def rep_re(pat, new):
    global s
    m = re.findall(pat, s, flags=re.S)
    if len(m) != 1:
        sys.exit(f'regex count {len(m)}: {pat[:80]!r}')
    s = re.sub(pat, lambda _: new, s, flags=re.S)

if 'class="od-fields"' in s:
    sys.exit('already applied')

# 已完成页签：空状态 + 产地卡字段说明
rep_re(r'        <div class="od-p" data-os="done" hidden>\n.*?</p>\n        </div>\n',
       '        <div class="od-p" data-os="done" hidden><div class="cs-empty"><b>没有已完成的订单</b><span>订单完成后显示在这里。</span></div></div>\n'
       '        <div class="od-spec"><h3 class="cs-h3">产地卡</h3><p>调用完成后，平台为每笔订单生成一张产地卡，包含以下字段。</p>\n'
       '          <dl class="od-fields"><div><dt>电站</dt><dd></dd></div><div><dt>时段</dt><dd></dd></div><div><dt>用电量 kWh</dt><dd></dd></div>'
       '<div><dt>词元数</dt><dd></dd></div><div><dt>单价</dt><dd></dd></div><div><dt>减排</dt><dd></dd></div></dl></div>\n')

# 去掉由交易看板行生成订单的脚本
rep_re(r"\n  \(function\(\)\{var el=\$\('#odList'\);.*?\}\)\}\)\}\)\(\);\n", '\n')

# CSS：删订单行与展开卡样式，换成字段说明
rep_re(r"\.od-hd\{.*?\.od-card \.cs-dl dd:last-of-type\{border-bottom:0\}\n",
       ".od-spec{margin-top:8px} .od-spec p{margin:0 0 14px;font-size:14px;color:var(--ink-70)}\n"
       ".od-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;margin:0;background:var(--card);border:1px solid var(--line);border-radius:var(--r16);overflow:hidden}\n"
       ".od-fields>div{padding:16px 18px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)} .od-fields>div:nth-child(3n){border-right:0} .od-fields>div:nth-child(n+4){border-bottom:0}\n"
       ".od-fields dt{font-size:13px;color:var(--ink-50)} .od-fields dd{margin:10px 0 0;height:1px;background:var(--line)}\n")
rep("  .od-h{grid-template-columns:minmax(0,1fr) auto;gap:4px 12px} .od-h .od-go{grid-column:2;grid-row:1} .od-h .od-p2{grid-column:1}\n",
    "  .od-fields{grid-template-columns:1fr 1fr} .od-fields>div:nth-child(3n){border-right:1px solid var(--line)} .od-fields>div:nth-child(2n){border-right:0} .od-fields>div:nth-child(n+4){border-bottom:1px solid var(--line)} .od-fields>div:nth-child(n+5){border-bottom:0}\n")

# 英文：删掉不再出现的键，补新键
for k in ["你的账户还没有已完成的订单。下面是平台交易看板的订单，点开查看产地卡。",
          "示例数据取自平台交易看板。发电时段、用电量与产出词元在平台接口接入后按订单显示。",
          "电站类型", "成交价", "发电时段", "产出词元"]:
    pat = '"' + k + '": "'
    i = s.find(pat)
    if i < 0 or s.count(pat) != 1:
        sys.exit('i18n key ' + k)
    j = s.index('"', i + len(pat))
    while s[j - 1] == '\\':
        j = s.index('"', j + 1)
    s = s[:i] + s[j + 1:].lstrip(', ') if s[j + 1:j + 3] == ', ' else s[:i] + s[j + 1:]
rep('"没有进行中的订单": "No running orders",',
    '"没有进行中的订单": "No running orders", "没有已完成的订单": "No completed orders", "订单完成后显示在这里。": "Completed orders appear here.", '
    '"调用完成后，平台为每笔订单生成一张产地卡，包含以下字段。": "Once a call completes, the platform generates an origin card for each order with these fields.", '
    '"时段": "Time window", "用电量 kWh": "Energy (kWh)", "词元数": "Tokens", "单价": "Unit price",')

open(path, 'w', encoding='utf-8').write(s)
print('ok')
