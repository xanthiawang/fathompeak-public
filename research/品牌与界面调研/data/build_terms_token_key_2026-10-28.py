"""全站统一叫法（Zixin 2026-10-28）：
 · 「记得检查所有的词元改成 token」→ 中文里的「词元」一律改为「Token」，和汉字、数字相邻处补空格（「百万词元」→「百万 Token」）；
   「词元（Token）」这类重复写法并成一个「Token」。
 · 「API 之后在中文的网站不出现，可以叫 FathomPeak Key，统一更正 apikey 称呼」→ 客户在沐仞创建的 Key 统一叫「FathomPeak Key」
   （原「API Key」「API 密钥」）。例外：
   - 运营后台渠道编辑里粘贴的是上游厂商给我们的凭证，改叫「上游密钥」，不是 FathomPeak Key；
   - AWS / Vertex 渠道的密钥类型「API Key」是厂商自己的凭证名称，不改；
   - 英文字典的译文、代码里的变量与请求头（API_KEY、apiKey、x-api-key）不改，英文版仍写 API key。
 · 首页演示回答（Zixin 截图标 1/2/3）：「绿电」→「绿色余电」，「电站旁」→「电站内」，「生产词元」→「生产绿色 Token」。
英文翻译按中文原句做键：中文改了，键同步改，译文不动，所以中英对照不会断。
只有「FathomPeak Key」这种不含汉字的标签，翻译函数原本会跳过；这里让它也能译成 API key。
 · 「企业合作改成企业订购」：导航、页面标题、各处「查看企业合作 →」、运营后台说明统一改（英文仍是 Enterprise）。
用法：python3 -I build_terms_token_key_2026-10-28.py <站点根目录（含 index.html 与 mini-preview/）>
"""
import re, sys
from pathlib import Path

ROOT = Path(sys.argv[1])
HAN = re.compile(r'[一-鿿]')


def tokenize(s):
    """词元 → Token，和汉字或字母数字相邻时补一个空格。"""
    s = re.sub(r'词元[（(]\s*[Tt]oken\s*[)）]|[Tt]oken\s*[（(]词元[)）]', '词元', s)
    # 脚本里不带引号的对象键（如 {词元采购:'Token purchase'}）改成带引号，否则补空格后不是合法键名
    s = re.sub(r'([{,]\s*)([一-鿿]*词元[一-鿿]*)(\s*:)', lambda m: m.group(1) + "'" + m.group(2) + "'" + m.group(3), s)

    def sub(m):
        a = s[m.start() - 1] if m.start() else ''
        b = s[m.end()] if m.end() < len(s) else ''
        sp = lambda c: bool(c) and (bool(HAN.match(c)) or c.isascii() and c.isalnum())
        return (' ' if sp(a) else '') + 'Token' + (' ' if sp(b) else '')
    return re.sub('词元', sub, s)


def rename_key(s, protect):
    """「API Key」→「FathomPeak Key」，跳过 protect 里的区间（英文译文、厂商凭证名称）。"""
    out, last = [], 0
    for m in re.finditer(r'API Key', s):
        if any(a <= m.start() < b for a, b in protect): continue
        out.append(s[last:m.start()]); out.append('FathomPeak Key'); last = m.end()
    out.append(s[last:])
    return ''.join(out)


def rep(s, old, new, n=1, name=''):
    c = s.count(old)
    if c != n: sys.exit(f'[停止] {name} 匹配 {c} 次（应为 {n}）：{old[:90]}')
    return s.replace(old, new)


# ---------------- index.html ----------------
p = ROOT / 'index.html'
s = p.read_text(encoding='utf8')
if 'var NCJK=' in s: sys.exit('[停止] 已经改过')
before = (s.count('词元'), s.count('API Key'), len(re.findall('API ?密钥', s)))

# 首页演示回答：先改这一句（data-t、data-en 与英文字典）
OLD = '把算力任务调度到绿电所在之处：一体机部署在电站旁，用富余绿电生产词元。'
NEW = '把算力任务调度到绿色余电所在之处：一体机部署在电站内，用富余绿电生产绿色 Token。'
NEW_EN = 'Compute tasks are routed to where the surplus green power is: appliances sit inside the plants and turn surplus green power into green tokens.'
s = rep(s, f'data-t="{OLD}"', f'data-t="{NEW}"', name='演示回答')
s = rep(s, 'data-en="Compute tasks are routed to where the green power is: appliances sit beside the plants and turn surplus green power into tokens."', f'data-en="{NEW_EN}"', name='演示回答英文')
s = rep(s, f'"{OLD}":"Compute tasks are routed to where the green power is: appliances sit beside the plants and turn surplus green power into tokens."', f'"{NEW}":"{NEW_EN}"', name='演示回答字典')

# 渠道编辑里的上游凭证：「API 密钥」→「上游密钥」（标签、脚本里的切换文字、英文字典键）
s = rep(s, "'API 密钥（每行一个）'", "'上游密钥（每行一个）'", name='上游密钥')
s = rep(s, "(editing?'API 密钥':'API 密钥 *')", "(editing?'上游密钥':'上游密钥 *')", name='上游密钥')
s = rep(s, "c?'API 密钥':'API 密钥 *'", "c?'上游密钥':'上游密钥 *'", name='上游密钥')
s = rep(s, '<label for="rtCEk" id="rtCEkL">API 密钥</label>', '<label for="rtCEk" id="rtCEkL">上游密钥</label>', name='上游密钥')
s = rep(s, '"API 密钥": "API key", "API 密钥 *": "API key *"', '"上游密钥": "Upstream key", "上游密钥 *": "Upstream key *"', name='上游密钥字典')
s = rep(s, '"API 密钥（每行一个）": "API keys (one per line)"', '"上游密钥（每行一个）": "Upstream keys (one per line)"', name='上游密钥字典')
# 客户端里填的是我们的 Key（Cherry Studio 说明）
s = rep(s, '再填 API 密钥，添加模型名称。', '再填 FathomPeak Key，添加模型名称。', 2, name='Cherry Studio')
if re.search('API ?密钥', s): sys.exit('[停止] 还有没处理的「API 密钥」')

# 词元 → Token（英文译文里没有「词元」，键和正文一起改，对照不断）
s = tokenize(s)
# 企业合作 → 企业订购（同样是中文键与正文一起改）
print('企业合作 → 企业订购：', s.count('企业合作'), '处')
s = s.replace('企业合作', '企业订购')

# API Key → FathomPeak Key：保护英文译文与厂商凭证名称
protect = []
for m in re.finditer(r'"((?:[^"\\\n]|\\.)*)"\s*:\s*"((?:[^"\\\n]|\\.)*)"', s):
    k, v = m.group(1), m.group(2)
    if not HAN.search(v) and (HAN.search(k) or k == v or k == 'API Key'):
        protect.append((m.start(2), m.end(2)))           # 译文
for pat in ['<option value="api_key">API Key</option>', '用 API Key 时填；JSON 模式从服务账号里读。']:
    for m in re.finditer(re.escape(pat), s): protect.append((m.start(), m.end()))   # AWS / Vertex 的密钥类型
s = rename_key(s, protect)

# 「FathomPeak Key」这类不含汉字的标签也能译成英文
s = rep(s, 'function tx(node){ var src=node.__zh!=null?node.__zh:node.nodeValue; if(!src||!CJK.test(src)) return;',
        'var NCJK=/^FathomPeak Key$/;  /* 不含汉字、但中文版要换说法的标签（2026-10-28） */\n  function tx(node){ var src=node.__zh!=null?node.__zh:node.nodeValue; if(!src||!(CJK.test(src)||NCJK.test(src.trim()))) return;', name='翻译函数')
s = rep(s, '  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})({"FathomPeak Key":"API key"});  /* 统一叫法 */\n  syncAuthLocale(); applyLang();', name='字典')

p.write_text(s, encoding='utf8')
after = (s.count('词元'), s.count('API Key'), len(re.findall('API ?密钥', s)))
print('index.html  词元 / API Key / API 密钥：', before, '→', after, '（剩下的 API Key 都在英文译文或厂商凭证名称里）')

# ---------------- 小程序（只有中文，没有翻译字典） ----------------
for f in sorted((ROOT / 'mini-preview').glob('*.js')) + sorted((ROOT / 'mini-preview').glob('*.html')):
    t = f.read_text(encoding='utf8'); b = (t.count('词元'), t.count('API Key'), t.count('企业合作'))
    if not any(b): continue
    t = tokenize(t).replace('API Key', 'FathomPeak Key').replace('企业合作', '企业订购')
    f.write_text(t, encoding='utf8'); print(f'mini-preview/{f.name}  词元 / API Key：', b, '→', (t.count('词元'), t.count('API Key')))
print('done')
