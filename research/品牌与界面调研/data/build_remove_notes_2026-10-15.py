"""删除网站里的示意文字（Zixin 2026-10-15："删除网站里的所有示意文字"，附图：首页流程动画下的「流程与设备示意 · 非实时运行数据」和「暂停 / 重播」）。叠在线上 0ddb9d1 上。
 1 首页「任务处理流程」：删掉底部说明「流程与设备示意 · 非实时运行数据」和右上角「暂停 / 重播」按钮
   （脚本里对这两个按钮的引用改成可空；点上方步骤仍能停在某一步，系统开了「减少动态效果」时仍是静态）。
 2 控制台里的黄色审阅标签（「待公司确认」「需平台支持」「待公司提供」等 9 处）全部删除；只装着标签的说明段落整段删掉。
   体验中心底部的「生成式人工智能服务备案号：--」是空占位，标签删掉后只剩「--」，一并删掉，拿到备案号再加回。
不删：交易看板上的「示例数据」标注（看板数字是示例，去掉标注会被当成真实成交）；体验中心「内容由人工智能生成，仅供参考」（生成式 AI 服务的提示要求）。
用法：python3 -I build_remove_notes_2026-10-15.py <线上 index.html（0ddb9d1）> <输出 html>
"""
import re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


# ---------- 1 首页流程动画 ----------
rep('\n<small class="flow-note">流程与设备示意 · 非实时运行数据</small>', '')
s, n = re.subn(r'<div class="flow-controls"><button type="button" data-flow-pause[^>]*>.*?</button><button type="button" data-flow-replay>.*?</button></div>', '', s, flags=re.S)
if n != 1: sys.exit(f'[停止] 暂停 / 重播按钮匹配 {n} 次')
rep("var label=reduced.matches?'静态模式':manual?'播放':'暂停';if(pause.querySelector('span').textContent!==label)pause.querySelector('span').textContent=label;pause.disabled=reduced.matches;pause.querySelector('path').setAttribute('d',manual||reduced.matches?'M3 2l7 4-7 4z':'M4 2v8M8 2v8');pause.setAttribute('aria-pressed',String(manual||reduced.matches))}",
    "if(pause){var label=reduced.matches?'静态模式':manual?'播放':'暂停';if(pause.querySelector('span').textContent!==label)pause.querySelector('span').textContent=label;pause.disabled=reduced.matches;pause.querySelector('path').setAttribute('d',manual||reduced.matches?'M3 2l7 4-7 4z':'M4 2v8M8 2v8');pause.setAttribute('aria-pressed',String(manual||reduced.matches))}}")
rep("pause.addEventListener('click',function(){manual=!manual;sync()});replay.addEventListener('click',function(){manual=false;elapsed=0;render();sync()});",
    "if(pause)pause.addEventListener('click',function(){manual=!manual;sync()});if(replay)replay.addEventListener('click',function(){manual=false;elapsed=0;render();sync()});")

# ---------- 2 控制台黄色审阅标签 ----------
rep('生成式人工智能服务备案号：--<span class="tbc">待公司提供</span>', '')
# 体验中心提示：标签删掉后两段文字会并成一个文本节点，英文词条就对不上了；把 AI 提示单独包一层
rep('。<span class="tbc">待公司确认</span>　内容由人工智能生成，仅供参考，请遵守', '。　<span>内容由人工智能生成，仅供参考，请遵守</span>')
s, n1 = re.subn(r'\s*<p class="(?:cs|ad)-fine"><span class="tbc">[^<]*</span></p>', '', s)
s, n2 = re.subn(r'<span class="tbc">[^<]*</span>', '', s)
if (n1, n2) != (5, 2): sys.exit(f'[停止] 审阅标签：整段 {n1}（应为 5）、行内 {n2}（应为 2）')
if 'class="tbc"' in s or '示意' in s.split('var I18N')[0]: sys.exit('[停止] 还有审阅标签或示意文字')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
