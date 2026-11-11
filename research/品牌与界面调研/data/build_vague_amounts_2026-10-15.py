"""合同与订单金额不写具体数字（Zixin 2026-10-15："不写具体数字 写数千万"，附图：首页「客户合作」四张卡）。叠在线上 d85f366 上。
 · 5,000 万元海外词元采购合同 → 数千万元海外词元采购合同
 · 已签词元订单超 6,000 万元 → 已签词元订单数千万元（首页卡片、关于我们「业务」两处）
 · 1,000 万元推理服务协议 → 千万元级推理服务协议（一千万写成「数千万」会夸大，用站内已有的「千万级」说法）
 · 海外订单占比超 83% → 以海外订单为主（同样不写具体比例）
不动：电站合作卡片里的装机（100MW、35 座、1GW）——那是项目规模，不是金额；示例订单里的「1000 万词元」是词元数。
用法：python3 -I build_vague_amounts_2026-10-15.py <线上 index.html（d85f366）> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


A, B, C = '数千万元海外词元采购合同', '千万元级推理服务协议', '已签词元订单数千万元'
D, E, F = '截至 2026 年第三季度，其中以海外订单为主。', '2026 年第三季度已签词元订单数千万元', '其中以海外订单为主'
rep('<b>5,000 万元海外词元采购合同</b>', f'<b>{A}</b>')
rep('<b>1,000 万元推理服务协议</b>', f'<b>{B}</b>')
rep('<b>已签词元订单超 6,000 万元</b><p>截至 2026 年第三季度，其中海外订单占比超 83%。</p>', f'<b>{C}</b><p>{D}</p>')
rep('<b>2026 年第三季度已签词元订单超 6000 万元</b><span class="s">其中海外订单占比超 83%</span>', f'<b>{E}</b><span class="s">{F}</span>')
# 旧的英文词条里也有具体金额（RMB 50 / 60 million、83%），看源码能看到，一并删掉
import re
OLD_KEYS = ['5,000 万元海外词元采购合同', '1,000 万元推理服务协议', '已签词元订单超 6,000 万元', '截至 2026 年第三季度，其中海外订单占比超 83%。',
            '2026 年第三季度已签词元订单超 6000 万元', '其中海外订单占比超 83%', '订单金额 83% 以上来自海外客户']
gone = 0
for k in OLD_KEYS:
    pat = re.compile(r'"' + re.escape(k) + r'"\s*:\s*"(?:[^"\\]|\\.)*"\s*,\s*')
    s, n = pat.subn('', s); gone += n
if gone != 9: sys.exit(f"[停止] 旧英文词条删了 {gone} 条（应为 9）")
for k in ['50 million', '60 million', '83%', '83 %']:
    if k in s: sys.exit('[停止] 源码里还有：' + k)
cut = s.find('var I18N')
for k in ['5,000 万', '6,000 万', '6000 万元', '1,000 万元', '83%']:
    if k in s[:cut]: sys.exit('[停止] 页面里还有具体金额：' + k)
EN = {A: 'Overseas token purchase contract worth tens of millions of RMB', B: 'Inference service agreement in the RMB 10-million range',
      C: 'Tens of millions of RMB in signed token orders', D: 'As of Q3 2026, mostly from overseas customers.',
      E: 'Tens of millions of RMB in token orders signed as of Q3 2026', F: 'mostly from overseas customers'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 金额不写具体数字 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
